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
#   - MODE BACA-SAja (default, aktivasi 21 Nov 2026): LLM hanya boleh
#     memakai alat BACA (READ_ONLY_ALAT). Alat tulis (tulis_file,
#     tulis_json, simpan_*, catat_tugas) TIDAK ditawarkan ke LLM —
#     pencatatan tetap dilakukan orchestrator sendiri. Mode penuh
#     (--no-read-only) hanya untuk agen yang sudah lolos bukti
#     baca-saja, dan tetap DRAF-only + DAFTAR_TERLARANG.
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

# MODE BACA-SAja (aktivasi 21 Nov 2026, perintah Cipta "1234 eksekusi"):
# alat yang BOLEH ditawarkan ke LLM bila read_only=True. Hanya alat
# baca + handoff (meneruskan data, bukan mengeksekusi). simpan_memori,
# catat_tugas, dan semua tulis_*/simpan_* TIDAK termasuk — pencatatan
# dilakukan orchestrator sendiri, bukan oleh LLM.
READ_ONLY_ALAT = {
    "baca_file", "baca_json", "baca_memori", "baca_crm",
    "baca_penjualan", "baca_akuntansi", "baca_pemasaran",
    "baca_harga_kompetitor", "handoff",
}

# Tugas aktivasi read-only, urutan A06 -> A10 -> A07 -> A25
# (rencana lama; dieksekusi 21 Nov 2026). Semua tugas HANYA baca +
# susun ringkasan DRAF; "belum cukup data" bila data kurang.
TUGAS_AKTIVASI_READONLY = [
    ("A06", "Riset pasar (BACA SAJA): baca memori riset pasar + file "
            "riset yang ada, lalu susun ringkasan DRAF: segmen pelanggan, "
            "kebutuhan, dan masalah yang paling sering muncul. Bila data "
            "kurang, tulis 'belum cukup data' — jangan mengarang."),
    ("A10", "Validasi produk (BACA SAJA): baca memori produk + katalog "
            "yang ada, lalu susun ringkasan DRAF: produk mana yang paling "
            "siap dijual dan apa yang masih kurang. Bila data kurang, "
            "tulis 'belum cukup data' — jangan mengarang."),
    ("A07", "Pantau tren (BACA SAJA): baca memori tren + riset yang ada, "
            "lalu susun ringkasan DRAF: tren minggu ini yang relevan "
            "dengan produk toko. Bila data kurang, tulis 'belum cukup "
            "data' — jangan mengarang."),
    ("A25", "Baca CRM saja (BACA SAJA — jangan ubah apa pun): baca data "
            "CRM penjualan, lalu susun ringkasan DRAF: jumlah kontak per "
            "status dan siapa yang perlu follow-up. Hanya baca."),
]

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
    read_only: bool


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


def _alat_diizinkan(agen, read_only=False):
    """Daftar alat yang BOLEH dipakai agen ini (registry, fail-closed),
    minus alat internal orchestrator. Bila read_only=True, hanya alat
    di READ_ONLY_ALAT yang ditawarkan (tulis/simpan tidak ada)."""
    hasil = []
    for nama, info in REGISTRY.daftar_alat().items():
        if nama in ALAT_INTERNAL:
            continue
        if read_only and nama not in READ_ONLY_ALAT:
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


def _prompt_pikir(agen, tugas, alat, langkah, read_only=False):
    """Prompt ReAct untuk node pikir: putuskan SATU aksi berikutnya
    atau nyatakan tugas selesai. Jawaban WAJIB JSON saja."""
    mode = (
        "MODE BACA-SAja: kamu HANYA boleh membaca data dan menyusun "
        "ringkasan DRAF. Kamu TIDAK BISA menulis file, menyimpan, "
        "mengirim, membayar, atau mempublikasi apa pun.\n\n"
        if read_only else
        "MODE PENUH (DRAF-only): hasil tetap DRAF untuk persetujuan "
        "Cipta — jangan janjikan sudah dikirim/dipublikasikan.\n\n"
    )
    return (
        "Kamu adalah agen {agen} di Pusat Komando (BINTANG COMMAND "
        "CENTER 4.0). Kerjakan tugas ini sendiri, selangkah demi "
        "selangkah, memakai alat yang diizinkan.\n\n"
        "{mode}"
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
        "7. JANGAN ulangi alat + argumen yang sudah dipakai di langkah "
        "sebelumnya — bila sudah dibaca, pakai hasilnya atau nyatakan "
        "selesai. Pengulangan akan DITOLAK.\n"
    ).format(
        agen=agen,
        mode=mode,
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
    alat = _alat_diizinkan(agen, read_only=state.get("read_only", True))
    prompt = _prompt_pikir(agen, state["tugas"], alat, state["langkah"],
                           read_only=state.get("read_only", True))
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

    # Lapis 0 — penjaga pengulangan (masalah panduan #4): alat +
    # argumen yang sama sudah dipakai di langkah sebelumnya -> tolak
    # supaya LLM tidak mengulang baca yang sama sampai batas langkah.
    sudah_dipakai = any(
        lg.get("aksi") == alat
        and json.dumps(lg.get("argumen") or {}, sort_keys=True,
                       ensure_ascii=False)
        == json.dumps(argumen, sort_keys=True, ensure_ascii=False)
        for lg in state.get("langkah", [])
    )
    if sudah_dipakai:
        hasil_alat = {
            "ok": False,
            "error": "DITOLAK oleh orchestrator: alat {!r} dengan argumen "
                     "yang sama sudah dipakai di langkah sebelumnya. "
                     "Pakai hasil yang sudah ada, pakai alat lain, atau "
                     "nyatakan selesai.".format(alat),
        }
    # Lapis 1 — pra-cek kata terlarang + alat tidak dikenal.
    rendah = alat.lower()
    if sudah_dipakai:
        pass  # hasil_alat sudah berisi penolakan pengulangan di atas
    elif any(k in rendah for k in REGISTRY.DAFTAR_TERLARANG):
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
                        catat=True, read_only=True):
    """Jalankan SATU tugas untuk SATU agen lewat graf LangGraph.

    read_only=True (default): LLM hanya boleh memakai alat BACA.
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
            "read_only": bool(read_only),
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
        "mode": "read-only" if read_only else "penuh",
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
                 "mode": hasil["mode"],
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


def jalankan_aktivasi_readonly():
    """Aktivasi LangGraph read-only untuk A06 -> A10 -> A07 -> A25.

    Perintah Cipta 21 Nov 2026 ("1234 eksekusi"). Satu tugas baca-saja
    per agen, berurutan; berhenti di agen pertama yang gagal (ok=False)
    supaya kegagalan terlihat, bukan ditutup-tutupi. Kembalikan dict
    ringkasan per agen + status keseluruhan."""
    ringkasan = {"ok": True, "mode": "read-only", "agen": []}
    for kode, tugas in TUGAS_AKTIVASI_READONLY:
        hasil = jalankan_tugas_agen(kode, tugas, read_only=True)
        ringkasan["agen"].append({
            "kode": kode,
            "ok": hasil["ok"],
            "status": hasil["status"],
            "jumlah_langkah": hasil["jumlah_langkah"],
            "hasil_akhir": hasil["hasil_akhir"][:500],
            "error": hasil["error"][:300],
        })
        if not hasil["ok"]:
            ringkasan["ok"] = False
            ringkasan["berhenti_di"] = kode
            break
    return ringkasan


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
    parser.add_argument("--aktivasi-readonly", action="store_true",
                        help="jalankan aktivasi read-only A06->A10->A07->A25")
    parser.add_argument("--read-only", dest="read_only",
                        action="store_true", default=True,
                        help="mode baca-saja (default)")
    parser.add_argument("--no-read-only", dest="read_only",
                        action="store_false",
                        help="mode penuh (DRAF-only; hanya bila sudah "
                             "lolos bukti baca-saja)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.aktivasi_readonly:
        ringkasan = jalankan_aktivasi_readonly()
        if args.json:
            print(json.dumps(ringkasan, ensure_ascii=False, indent=2))
        else:
            print("Aktivasi read-only A06->A10->A07->A25: "
                  "{}".format("OK" if ringkasan["ok"] else "BERHENTI"))
            for a in ringkasan["agen"]:
                print("  {}: {} | langkah {} | {}".format(
                    a["kode"], a["status"], a["jumlah_langkah"],
                    (a["hasil_akhir"] or a["error"] or "-")[:200]))
        return 0 if ringkasan["ok"] else 1
    if args.contoh_a09:
        hasil = jalankan_contoh_a09()
    else:
        if not args.tugas.strip():
            parser.error("--tugas wajib diisi (atau pakai --contoh-a09)")
        hasil = jalankan_tugas_agen(args.agen, args.tugas,
                                    maks_langkah=args.maks_langkah,
                                    read_only=args.read_only)
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print("Agen: {} | Tugas: {} | Mode: {}".format(
            hasil["agen"], hasil["tugas"], hasil["mode"]))
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
