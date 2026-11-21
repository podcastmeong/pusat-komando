#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO 4.0 — agents/langgraph_orchestrator.py
# LangGraph Orchestrator — agen bisa "mikir sendiri" (loop pikir-aksi).
#
# Dibuat 21 Nov 2026 atas perintah Cipta ("Pasang aja biar bisa mikir
# sendiri gmna Cara nya Dan bisa initiative. Klo Ada masalah itu urusan
# belakangan"). LangGraph 1.x open-source (pip, gratis); LLM lewat AI
# Gateway yang sudah ada (llm_router, kelas "berat" = Gemini free tier
# via helper secure storage) — TIDAK ADA API berbayar baru.
#
# SIFAT: modul PASIF seperti agen lain — hanya jalan bila dipanggil
# (oleh Muse / cron / mesin eksekusi). TIDAK ADA layanan otonom 24 jam.
#
# PAGAR PENGAMAN (TIDAK BOLEH DILANGGAR):
#   - Semua aksi HANYA lewat Tool Registry (tool_registry.jalankan_alat).
#     Alat yang tidak terdaftar = TIDAK BOLEH; alat terlarang
#     (kirim/bayar/publikasi/submit/upload/hapus — DAFTAR_TERLARANG)
#     DITOLAK dua lapis: di sini (pra-cek) DAN di registry.
#   - Semua output adalah DRAF untuk persetujuan Cipta. Graf ini TIDAK
#     BISA mengirim / membayar / mempublikasi / submit / upload / hapus
#     apa pun — alat seperti itu memang tidak ada di registry.
#   - Batas langkah maks 10 per tugas (anti loop tak berujung).
#   - Bila LLM/gateway gagal: graf GAGAL TERSTRUKTUR (status "gagal",
#     dicatat ke memori bersama) — TIDAK diam, TIDAK mengarang hasil.
#   - Semua langkah dicatat ke memori_bersama (riwayat_tugas) + hasil
#     akhir disimpan (jenis "langgraph_hasil").
#
# CARA PAKAI:
#   from agents.langgraph_orchestrator import jalankan_tugas_agen
#   hasil = jalankan_tugas_agen("A09",
#       "riset 3 harga kompetitor jasa video promo")
#   # hasil = {"ok": True/False, "status": "selesai"/"gagal"/
#   #          "batas_langkah", "agen": ..., "tugas": ...,
#   #          "langkah": [...], "hasil_akhir": ..., "error": ...}
# CLI:
#   python -m agents.langgraph_orchestrator --agen A09 \
#       --tugas "riset 3 harga kompetitor jasa video promo"
#   python -m agents.langgraph_orchestrator --contoh-a09
# ======================================================================
"""LangGraph Orchestrator 4.0 — loop pikir-aksi (ReAct) per agen."""

import argparse
import json
import sys
from pathlib import Path
from typing import Annotated, Any, TypedDict

# Modul-modul Pusat Komando diimpor sebagai modul top-level (pola yang
# sama seperti tool_registry.py): direktori agents/ harus ada di sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from langgraph.graph import END, START, StateGraph
except ImportError as e:  # pragma: no cover - gagal instalasi
    raise ImportError(
        "LangGraph belum terpasang di venv-pk. Pasang dulu: "
        "~/workspace/tmp/venv-pk/bin/pip install langgraph"
    ) from e

import llm_router
import memori_bersama as MEMORI
import tool_registry as REGISTRY

MAKS_LANGKAH = 10
VERSI = "4.0-langgraph"

# Alat yang TIDAK ditawarkan ke LLM di dalam graf (dipakai orchestrator
# sendiri, atau akan membuat panggilan LLM bersarang yang mubazir):
#   - panggil_llm: node "pikir" SUDAH memanggil LLM lewat gateway.
#   - catat_tugas: orchestrator mencatat tiap langkah sendiri.
ALAT_INTERNAL = {"panggil_llm", "catat_tugas"}

# Deskripsi argumen singkat per alat (untuk prompt LLM).
ARGUMEN_ALAT = {
    "baca_file": "argumen: {\"path\": \"jalur file di ~/workspace\"}",
    "tulis_file": "argumen: {\"path\": ..., \"konten\": \"teks\"} — HANYA agen yang diizinkan",
    "baca_json": "argumen: {\"path\": \"jalur file JSON di ~/workspace\"}",
    "tulis_json": "argumen: {\"path\": ..., \"data\": {...}} — HANYA agen yang diizinkan",
    "baca_memori": "argumen: {\"kunci\": ..., \"jenis\": ..., \"limit\": 100} (semua opsional)",
    "simpan_memori": "argumen: {\"jenis\": ..., \"kunci\": ..., \"nilai\": ..., \"sumber\": ...}",
    "baca_harga_kompetitor": "argumen: {\"kategori\": ... (opsional), \"limit\": 100}",
    "baca_crm": "argumen: {\"status\": ... | \"kata_kunci\": ... | \"id\": ...} (semua opsional)",
    "simpan_crm": "argumen: {\"aksi\": \"ubah_status\"|\"tambah\", ...} — HANYA mencatat, TIDAK mengirim",
    "handoff": "argumen: {\"lanjut_ke\": \"kode agen\", \"data\": {...}} — hanya meneruskan data",
}

BATAS_OBSERVASI = 1500  # karakter observasi yang disimpan per langkah


class StateGraf(TypedDict):
    """State graf LangGraph (satu tugas, satu agen)."""

    agen: str
    tugas: str
    langkah: list
    langkah_ke: int
    selesai: bool
    hasil_akhir: str
    error: str
    status: str
    keputusan: dict


def _kategori_harga_kompetitor():
    """Daftar kategori yang ADA di database harga kompetitor (dinamis).

    LLM tidak tahu nilai kategori yang persis (mis. "jasa_video_promo_
    desain" vs "video promo") — tanpa daftar ini, filter kategori yang
    salah mengembalikan [] dan LLM menyimpulkan database kosong.
    Kembalikan [] bila modul/DB tidak tersedia (prompt tetap jalan)."""
    try:
        import harga_kompetitor

        con = harga_kompetitor._koneksi()
        try:
            return [r[0] for r in con.execute(
                "SELECT DISTINCT kategori FROM harga_kompetitor"
                " WHERE kategori != '' ORDER BY kategori").fetchall()]
        finally:
            con.close()
    except Exception:
        return []


def _alat_diizinkan(agen):
    """Daftar alat yang BOLEH dipakai agen ini (registry, fail-closed),
    minus alat internal orchestrator. Kembalikan list dict nama+deskripsi."""
    hasil = []
    for nama, info in REGISTRY.daftar_alat().items():
        if nama in ALAT_INTERNAL:
            continue
        if REGISTRY.cek_izin(agen, nama):
            argumen = ARGUMEN_ALAT.get(nama, "argumen: {}")
            if nama == "baca_harga_kompetitor":
                kategori = _kategori_harga_kompetitor()
                if kategori:
                    argumen += (" — kategori yang ADA di database (pakai "
                                "salah satu persis seperti ini, atau kosongkan "
                                "untuk semua): " + ", ".join(kategori))
            hasil.append({
                "nama": nama,
                "deskripsi": info.get("deskripsi", ""),
                "argumen": argumen,
            })
    return hasil


def _teks_alat(alat):
    """Daftar alat dalam format teks untuk prompt LLM."""
    baris = []
    for a in alat:
        baris.append(
            "- {nama}: {deskripsi} {argumen}".format(**a)
        )
    return "\n".join(baris)


def _riwayat_teks(langkah):
    """Ringkasan langkah sejauh ini untuk prompt LLM."""
    if not langkah:
        return "(belum ada langkah)"
    baris = []
    for lg in langkah[-5:]:
        baris.append(
            "Langkah {nomor}: pikir: {pemikiran} | aksi: {aksi} "
            "| observasi: {observasi}".format(
                nomor=lg.get("nomor"),
                pemikiran=(lg.get("pemikiran") or "")[:200],
                aksi=lg.get("aksi"),
                observasi=(lg.get("observasi") or "")[:300],
            )
        )
    return "\n".join(baris)


def _prompt_pikir(agen, tugas, alat, langkah):
    """Prompt ReAct untuk node pikir: putuskan SATU aksi berikutnya
    atau nyatakan tugas selesai. Jawaban WAJIB JSON saja."""
    return (
        "Kamu adalah agen {agen} di Pusat Komando (BINTANG COMMAND "
        "CENTER 4.0). Kerjakan tugas ini sendiri, selangkah demi "
        "selangkah, memakai alat yang diizinkan.\n\n"
        "TUGAS: {tugas}\n\n"
        "ALAT YANG BOLEH DIPAKAI (hanya ini — jangan pakai alat lain):\n"
        "{daftar_alat}\n\n"
        "LANGKAH SEJAUH INI:\n{riwayat}\n\n"
        "ATURAN WAJIB:\n"
        "1. Balas HANYA dengan SATU objek JSON, tanpa teks lain.\n"
        "2. Untuk memakai alat: "
        "{{\"aksi\": \"<nama alat>\", \"argumen\": {{...}}, "
        "\"alasan\": \"<kenapa langkah ini>\"}}\n"
        "3. Bila tugas sudah selesai: "
        "{{\"selesai\": true, \"hasil\": \"<ringkasan hasil DRAF>\"}}\n"
        "4. Hanya laporkan fakta yang BENAR-BENAR dikembalikan alat. "
        "Bila data kurang, tulis 'belum cukup data'. JANGAN mengarang "
        "harga, nama pesaing, angka, atau sumber.\n"
        "5. Semua hasil adalah DRAF untuk persetujuan Cipta — jangan "
        "janjikan views/viral/penjualan, jangan klaim sudah dikirim "
        "atau dipublikasikan (kamu TIDAK BISA mengirim/mempublikasi).\n"
        "6. Jangan minta alat kirim/bayar/publikasi/submit/upload/hapus "
        "— alat itu tidak ada dan akan DITOLAK.\n"
    ).format(
        agen=agen,
        tugas=tugas,
        daftar_alat=_teks_alat(alat),
        riwayat=_riwayat_teks(langkah),
    )


def _ekstrak_json(teks):
    """Ambil objek JSON pertama dari jawaban LLM (tahan pagar kode).

    Kembalikan dict bila berhasil, None bila tidak ada JSON valid."""
    if not teks:
        return None
    t = str(teks).strip()
    for pagar in ("```json", "```"):
        t = t.replace(pagar, " ")
    awal = t.find("{")
    akhir = t.rfind("}")
    if awal < 0 or akhir <= awal:
        return None
    try:
        hasil = json.loads(t[awal:akhir + 1])
        return hasil if isinstance(hasil, dict) else None
    except json.JSONDecodeError:
        return None


# ----------------------------------------------------------------------
# Node graf
# ----------------------------------------------------------------------
def _node_pikir(state):
    """Node pikir: tanya LLM (lewat gateway) langkah berikutnya."""
    agen = state["agen"]
    if state["langkah_ke"] >= MAKS_LANGKAH:
        return {"selesai": True, "status": "batas_langkah",
                "error": "Batas langkah ({}) tercapai.".format(MAKS_LANGKAH)}
    alat = _alat_diizinkan(agen)
    prompt = _prompt_pikir(agen, state["tugas"], alat, state["langkah"])
    # Coba maks 2x: jawaban LLM kadang bukan JSON (teks penjelasan) —
    # percobaan ke-2 diingatkan lebih tegas. Bila tetap bukan JSON,
    # gagal terstruktur (bukan mengarang keputusan).
    keputusan = None
    error_llm = ""
    for percobaan in range(2):
        p = prompt if percobaan == 0 else (
            prompt + "\n\nULANGI SEKARANG: balas HANYA dengan SATU objek "
            "JSON valid, tanpa teks lain di luar JSON.")
        hasil = llm_router.jalankan(
            "berat", "langgraph:{}".format(agen), p,
            timeout=30, max_tokens=512,
        )
        if not hasil.get("ok"):
            error_llm = (hasil.get("error") or "tidak ada rincian")[:300]
            break
        keputusan = _ekstrak_json(hasil.get("teks", ""))
        if keputusan is not None:
            break
    if not hasil.get("ok"):
        return {
            "selesai": True,
            "status": "gagal",
            "error": "LLM/gateway gagal: {}".format(error_llm),
        }
    if keputusan is None:
        return {
            "selesai": True,
            "status": "gagal",
            "error": "LLM tidak mengembalikan JSON keputusan yang valid "
                     "(2 percobaan).",
        }
    if keputusan.get("selesai"):
        return {
            "selesai": True,
            "status": "selesai",
            "hasil_akhir": str(keputusan.get("hasil", ""))[:2000],
            "keputusan": keputusan,
        }
    if not keputusan.get("aksi"):
        return {
            "selesai": True,
            "status": "gagal",
            "error": "Keputusan LLM tidak berisi aksi maupun selesai.",
        }
    return {"keputusan": keputusan}


def _node_aksi(state):
    """Node aksi: jalankan SATU alat lewat Tool Registry (fail-closed).

    Pra-cek lapis pertama di sini; registry adalah lapis kedua."""
    agen = state["agen"]
    keputusan = state.get("keputusan") or {}
    alat = str(keputusan.get("aksi", "")).strip()
    argumen = keputusan.get("argumen") or {}
    if not isinstance(argumen, dict):
        argumen = {}
    alasan = str(keputusan.get("alasan", ""))[:300]

    # Lapis 1 — pra-cek kata terlarang + alat tidak dikenal.
    rendah = alat.lower()
    if any(k in rendah for k in REGISTRY.DAFTAR_TERLARANG):
        hasil_alat = {
            "ok": False,
            "error": "DITOLAK oleh orchestrator: alat {!r} mengandung "
                     "kata terlarang (kirim/bayar/publikasi/submit/"
                     "upload/hapus).".format(alat),
        }
    elif alat not in REGISTRY.daftar_alat():
        hasil_alat = {
            "ok": False,
            "error": "DITOLAK: alat {!r} tidak terdaftar di Tool "
                     "Registry.".format(alat),
        }
    else:
        # Lapis 2 — registry (cek_izin fail-closed + pelaksana).
        try:
            hasil_alat = REGISTRY.jalankan_alat(agen, alat, **argumen)
        except Exception as e:  # noqa: BLE001 - laporkan apa adanya
            hasil_alat = {"ok": False,
                          "error": "{}: {}".format(type(e).__name__, e)}

    if hasil_alat.get("ok"):
        observasi = json.dumps(hasil_alat, ensure_ascii=False)[:BATAS_OBSERVASI]
    else:
        observasi = "GAGAL/DITOLAK: {}".format(
            hasil_alat.get("error", "tidak ada rincian"))[:BATAS_OBSERVASI]

    nomor = state["langkah_ke"] + 1
    entri = {
        "nomor": nomor,
        "pemikiran": alasan,
        "aksi": alat,
        "argumen": argumen,
        "observasi": observasi,
        "ok": bool(hasil_alat.get("ok")),
    }
    langkah = list(state["langkah"]) + [entri]

    # Catat langkah ke memori bersama (riwayat_tugas) — bukti kerja.
    try:
        MEMORI.catat_tugas(
            agen,
            "langgraph langkah {}: {}".format(nomor, alat),
            observasi[:500],
            "selesai" if entri["ok"] else "ditolak/gagal",
        )
    except Exception:
        pass
    return {"langkah": langkah, "langkah_ke": nomor, "keputusan": {}}


def _rute_pikir(state):
    """Setelah pikir: selesai -> END, ada aksi -> node aksi."""
    return END if state.get("selesai") else "aksi"


def _rute_cek(state):
    """Setelah aksi: selesai / batas langkah -> END, lanjut -> pikir."""
    if state.get("selesai"):
        return END
    if state["langkah_ke"] >= MAKS_LANGKAH:
        return END
    return "pikir"


def _bangun_graf():
    """Bangun + compile StateGraph pikir -> aksi -> cek."""
    graf = StateGraph(StateGraf)
    graf.add_node("pikir", _node_pikir)
    graf.add_node("aksi", _node_aksi)
    graf.add_edge(START, "pikir")
    graf.add_conditional_edges("pikir", _rute_pikir,
                               {"aksi": "aksi", END: END})
    graf.add_edge("aksi", "cek")
    graf.add_node("cek", lambda s: s)  # node pasif, hanya titik routing
    graf.add_conditional_edges("cek", _rute_cek,
                               {"pikir": "pikir", END: END})
    return graf.compile()


# ----------------------------------------------------------------------
# Runner
# ----------------------------------------------------------------------
def jalankan_tugas_agen(agen, tugas, maks_langkah=MAKS_LANGKAH,
                        catat=True):
    """Jalankan SATU tugas untuk SATU agen lewat graf LangGraph.

    Kembalikan dict hasil akhir (ok/status/langkah/hasil_akhir/error).
    Hasil akhir + status dicatat ke memori_bersama bila catat=True.
    """
    global MAKS_LANGKAH
    batas_lama = MAKS_LANGKAH
    MAKS_LANGKAH = int(maks_langkah)
    try:
        graf = _bangun_graf()
        awal = {
            "agen": str(agen).strip(),
            "tugas": str(tugas).strip(),
            "langkah": [],
            "langkah_ke": 0,
            "selesai": False,
            "hasil_akhir": "",
            "error": "",
            "status": "berjalan",
            "keputusan": {},
        }
        akhir = graf.invoke(awal)
    finally:
        MAKS_LANGKAH = batas_lama

    status = akhir.get("status", "selesai")
    if status == "berjalan":
        status = "selesai" if akhir.get("selesai") else "gagal"
    if akhir.get("selesai") and status == "berjalan":
        status = "selesai"
    if akhir["langkah_ke"] >= int(maks_langkah) and not akhir.get("hasil_akhir"):
        status = "batas_langkah"

    hasil = {
        "ok": status == "selesai",
        "status": status,
        "agen": akhir["agen"],
        "tugas": akhir["tugas"],
        "langkah": akhir["langkah"],
        "jumlah_langkah": akhir["langkah_ke"],
        "hasil_akhir": akhir.get("hasil_akhir", ""),
        "error": akhir.get("error", ""),
        "versi": VERSI,
    }
    if catat:
        try:
            MEMORI.simpan(
                akhir["agen"], "langgraph_hasil",
                "langgraph:{}:{}".format(
                    akhir["agen"],
                    akhir["tugas"][:60].lower().replace(" ", "-")),
                {"tugas": akhir["tugas"], "status": status,
                 "jumlah_langkah": akhir["langkah_ke"],
                 "hasil_akhir": hasil["hasil_akhir"],
                 "error": hasil["error"],
                 "langkah": akhir["langkah"]},
                sumber="langgraph_orchestrator",
            )
            MEMORI.catat_tugas(
                akhir["agen"],
                "langgraph: {}".format(akhir["tugas"][:120]),
                (hasil["hasil_akhir"] or hasil["error"] or status)[:500],
                status,
            )
        except Exception:
            pass
    return hasil


def jalankan_contoh_a09():
    """Bukti pertama: A09 riset 3 harga kompetitor jasa video promo.

    Hanya baca + catat (DRAF). Tanpa aksi eksternal apa pun."""
    return jalankan_tugas_agen(
        "A09",
        "Riset 3 harga kompetitor jasa video promo. Baca dulu database "
        "harga kompetitor dan memori harga pesaing yang sudah ada, "
        "lalu susun ringkasan DRAF: pesaing, produk, harga, sumber, "
        "tanggal cek. Bila data kurang dari 3, tulis 'belum cukup data' "
        "— jangan mengarang harga.",
    )


def info():
    """Metadata modul (untuk tes + tab Pusat Komando)."""
    try:
        import importlib.metadata as _md

        versi_lg = _md.version("langgraph")
    except Exception:
        versi_lg = "?"
    return {
        "modul": "langgraph_orchestrator",
        "versi": VERSI,
        "langgraph": versi_lg,
        "maks_langkah": MAKS_LANGKAH,
        "node": ["pikir", "aksi", "cek"],
        "pagar": "DRAF-only; DAFTAR_TERLARANG utuh; aksi hanya via Tool Registry.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="LangGraph Orchestrator 4.0 — jalankan satu tugas "
                    "satu agen lewat graf pikir-aksi.")
    parser.add_argument("--agen", default="A09")
    parser.add_argument("--tugas", default="")
    parser.add_argument("--maks-langkah", type=int, default=MAKS_LANGKAH)
    parser.add_argument("--contoh-a09", action="store_true",
                        help="jalankan bukti A09 (riset 3 harga kompetitor)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.contoh_a09:
        hasil = jalankan_contoh_a09()
    else:
        if not args.tugas.strip():
            parser.error("--tugas wajib diisi (atau pakai --contoh-a09)")
        hasil = jalankan_tugas_agen(args.agen, args.tugas,
                                    maks_langkah=args.maks_langkah)
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print("Agen: {} | Tugas: {}".format(hasil["agen"], hasil["tugas"]))
        print("Status: {} | Langkah: {}".format(
            hasil["status"], hasil["jumlah_langkah"]))
        for lg in hasil["langkah"]:
            print("  {}. [{}] {} -> {}".format(
                lg["nomor"], "OK" if lg["ok"] else "DITOLAK/GAGAL",
                lg["aksi"], (lg["observasi"] or "")[:200]))
        print("Hasil akhir:", (hasil["hasil_akhir"] or "-")[:500])
        if hasil["error"]:
            print("Error:", hasil["error"][:300])
    return 0 if hasil["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
