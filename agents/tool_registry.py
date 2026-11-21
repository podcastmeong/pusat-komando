#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO 2.0 — tool_registry.py
# Tool Registry 3.1 — FREE EDITION (21 Nov 2026, perintah Cipta
# "Eksekusi", rencana ChatGPT "AI BUSINESS AUTONOMOUS AGENT 3.1 –
# FREE EDITION" + DeepSeek: tool execution untuk agen Python).
#
# SIFAT: modul PASIF. Tidak berjalan sendiri; hanya didaftarkan dan
# dipanggil oleh Execution Engine (agents/execution_engine.py) atau
# oleh Muse. Semua alat di sini AMAN dan LOKAL: baca/tulis file di
# workspace, baca/simpan memori bersama, panggil LLM lewat gateway.
#
# YANG TIDAK ADA DI SINI (sengaja, fail-closed):
#   - TIDAK ADA alat kirim (email/DM/WA), bayar, publikasi, submit,
#     upload, atau hapus. Alat seperti itu DITOLAK saat didaftarkan
#     (lihat DAFTAR_TERLARANG + daftarkan()).
#   - Alat yang tidak terdaftar = TIDAK BOLEH dipakai (cek_izin()
#     mengembalikan False bila tidak ada izin eksplisit).
#
# IZIN: izin per agen dicatat di memori bersama (tabel izin_alat,
# via memori_bersama.cek_izin/atur_izin) bila modul itu ada; bila
# tidak ada, dipakai IZIN_DEFAULT di bawah (fail-closed: hanya alat
# baca untuk semua agen; alat tulis/LLM hanya untuk agen yang
# disebut namanya).
#
# Standar 6 kemampuan (ChatGPT): READ, THINK, EXECUTE, SAVE, REPORT,
# HANDOFF — tiap alat dicatat kemampuan yang dipakainya.
# ======================================================================
"""Tool Registry 3.1 — daftar alat + izin per agen (fail-closed)."""

import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
WORKSPACE = Path.home() / "workspace"

# Kata yang TIDAK BOLEH ada di nama/deskripsi alat. Alat apa pun yang
# mengandung kata ini ditolak saat didaftarkan — ini pagar pengaman
# agar tidak ada alat kirim/bayar/publikasi yang lolos diam-diam.
DAFTAR_TERLARANG = [
    "kirim", "send", "bayar", "pay", "beli", "purchase", "publikasi",
    "publish", "upload", "submit", "daftar_lomba", "hapus", "delete",
    "transfer", "password", "kata_sandi", "token_rahasia",
]

# Alat bawaan (aman, lokal). "kemampuan" = dari standar 6 kemampuan.
ALAT_BAWAAN = {
    "baca_file": {
        "deskripsi": "Baca file teks di dalam ~/workspace (READ).",
        "kemampuan": ["READ"],
        "agen_boleh": "semua",
    },
    "tulis_file": {
        "deskripsi": "Tulis file teks di dalam ~/workspace (SAVE). "
        "Tidak boleh menulis di luar workspace.",
        "kemampuan": ["SAVE"],
        "agen_boleh": ["A13", "A14", "A15", "A16", "A19", "A32"],
    },
    "baca_json": {
        "deskripsi": "Baca file JSON di dalam ~/workspace (READ).",
        "kemampuan": ["READ"],
        "agen_boleh": "semua",
    },
    "tulis_json": {
        "deskripsi": "Tulis file JSON di dalam ~/workspace (SAVE).",
        "kemampuan": ["SAVE"],
        "agen_boleh": ["A09", "A13", "A14", "A25", "A28", "A32"],
    },
    "baca_memori": {
        "deskripsi": "Baca ingatan bersama (memori_bersama.db) — "
        "fakta toko/harga/keputusan (READ).",
        "kemampuan": ["READ"],
        "agen_boleh": "semua",
    },
    "simpan_memori": {
        "deskripsi": "Simpan fakta ke ingatan bersama (SAVE).",
        "kemampuan": ["SAVE"],
        "agen_boleh": "semua",
    },
    "catat_tugas": {
        "deskripsi": "Catat riwayat tugas agen ke ingatan bersama "
        "(REPORT).",
        "kemampuan": ["REPORT"],
        "agen_boleh": "semua",
    },
    "panggil_llm": {
        "deskripsi": "Panggil LLM lewat AI Gateway anti-timeout "
        "(llm_router.jalankan) — THINK. Hasil adalah DRAF.",
        "kemampuan": ["THINK"],
        # 3.1-ext 21 Nov 2026 ("Ke semua ai"): dibuka untuk semua 30 agen
        # Bintang (A01-A30). A34/A35/A36 dipertahankan dari daftar lama.
        # THINK saja, hasil DRAF — tanpa efek keluar.
        "agen_boleh": ["A01", "A02", "A03", "A04", "A05", "A06", "A07",
                       "A08", "A09", "A10", "A11", "A12", "A13", "A14",
                       "A15", "A16", "A17", "A18", "A19", "A20", "A21",
                       "A22", "A23", "A24", "A25", "A26", "A27", "A28",
                       "A29", "A30", "A34", "A35", "A36"],
    },
    "baca_harga_kompetitor": {
        "deskripsi": "Baca database harga kompetitor (READ).",
        "kemampuan": ["READ"],
        "agen_boleh": ["A09", "A01", "A05", "A25"],
    },
    "baca_crm": {
        "deskripsi": "Baca data CRM penjualan (data/crm.json) — kontak toko, "
        "status penawaran, draf (READ).",
        "kemampuan": ["READ"],
        "agen_boleh": "semua",
    },
    "simpan_crm": {
        "deskripsi": "Simpan/ubah status CRM penjualan (SAVE). Hanya "
        "mencatat — TIDAK mengirim apa pun.",
        "kemampuan": ["SAVE"],
        "agen_boleh": ["A25", "A26", "A01", "A02", "A05", "A30"],
    },
    "handoff": {
        "deskripsi": "Teruskan hasil tugas ke agen berikutnya "
        "(HANDOFF). Hanya meneruskan data, bukan mengeksekusi.",
        "kemampuan": ["HANDOFF"],
        "agen_boleh": "semua",
    },
}

# Izin default bila memori_bersama tidak tersedia. Fail-closed:
# alat tulis/LLM hanya untuk agen yang disebut; sisanya baca saja.
IZIN_DEFAULT = {
    ("A09", "baca_harga_kompetitor"): True,
    ("A25", "baca_harga_kompetitor"): True,
}


def _memori():
    try:
        import memori_bersama

        return memori_bersama
    except ImportError:
        return None


def _diizinkan(nama_alat):
    """True bila nama alat mengandung kata terlarang."""
    rendah = nama_alat.lower()
    return any(k in rendah for k in DAFTAR_TERLARANG)


def daftar_alat():
    """Kembalikan salinan daftar alat bawaan (tanpa fungsi)."""
    return {k: dict(v) for k, v in ALAT_BAWAAN.items()}


def daftarkan(nama, deskripsi, kemampuan, agen_boleh):
    """Daftarkan alat baru. DITOLAK bila mengandung kata terlarang.

    Mengembalikan (berhasil_bool, pesan). Alat baru hanya tercatat
    di memori proses ini (tidak persisten) — pendaftaran permanen
    dilakukan dengan menambahkannya ke ALAT_BAWAAN di file ini.
    """
    if _diizinkan(nama) or _diizinkan(deskripsi):
        return False, (
            f"DITOLAK: alat {nama!r} mengandung kata terlarang "
            "(kirim/bayar/publikasi/submit/upload/hapus). Alat seperti "
            "itu tidak boleh ada di registry."
        )
    if nama in ALAT_BAWAAN:
        return False, f"DITOLAK: alat {nama!r} sudah terdaftar."
    ALAT_BAWAAN[nama] = {
        "deskripsi": deskripsi,
        "kemampuan": list(kemampuan),
        "agen_boleh": agen_boleh,
    }
    return True, f"Alat {nama!r} terdaftar."


def _izin_memori(agen, alat):
    """Baca izin eksplisit dari memori bersama (tabel izin_alat).

    Mengembalikan True/False bila ada baris eksplisit, None bila
    tidak ada baris (alat ini belum diatur di memori bersama — dalam
    hal itu registry memakai daftar agen_boleh-nya sendiri).
    Tidak mengubah apa pun (hanya SELECT).
    """
    try:
        import sqlite3

        db_path = BASE / "data" / "memori_bersama.db"
        if not db_path.is_file():
            return None
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            r = con.execute(
                "SELECT boleh FROM izin_alat WHERE agen = ? AND alat = ?",
                (str(agen).strip(), str(alat).strip()),
            ).fetchone()
            return bool(r[0]) if r else None
        finally:
            con.close()
    except Exception:
        return None


def cek_izin(agen, alat):
    """Apakah agen boleh memakai alat? Fail-closed: tidak ada izin
    eksplisit = TIDAK BOLEH."""
    if alat not in ALAT_BAWAAN:
        return False
    info = ALAT_BAWAAN[alat]
    boleh = info["agen_boleh"]
    if boleh != "semua" and agen not in boleh:
        return False
    # Bila memori bersama punya baris izin eksplisit untuk alat ini,
    # baris itu yang berlaku; bila tidak ada baris, pakai daftar
    # agen_boleh registry (alat baru yang belum diatur di memori).
    izin = _izin_memori(agen, alat)
    if izin is not None:
        return izin
    return True


def _dalam_workspace(path):
    """Pastikan path berada di dalam ~/workspace."""
    try:
        p = Path(path).expanduser().resolve()
    except (OSError, RuntimeError):
        return None
    if str(p).startswith(str(WORKSPACE.resolve())):
        return p
    return None


def jalankan_alat(agen, alat, **kwargs):
    """Jalankan alat untuk agen. Kembalikan dict hasil terstruktur.

    Bila izin tidak ada -> {"ok": False, "error": "izin ditolak"} dan
    TIDAK mengeksekusi apa pun (fail-closed).
    """
    if alat not in ALAT_BAWAAN:
        return {"ok": False, "agen": agen, "alat": alat,
                "error": f"alat tidak dikenal: {alat!r}"}
    if not cek_izin(agen, alat):
        return {"ok": False, "agen": agen, "alat": alat,
                "error": f"izin ditolak: {agen} tidak boleh memakai {alat!r}"}
    try:
        if alat == "baca_file":
            p = _dalam_workspace(kwargs["path"])
            if p is None or not p.is_file():
                return {"ok": False, "agen": agen, "alat": alat,
                        "error": "path di luar workspace / file tidak ada"}
            return {"ok": True, "agen": agen, "alat": alat,
                    "teks": p.read_text(encoding="utf-8")}
        if alat == "tulis_file":
            p = _dalam_workspace(kwargs["path"])
            if p is None:
                return {"ok": False, "agen": agen, "alat": alat,
                        "error": "path di luar workspace — ditolak"}
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(kwargs.get("konten", ""), encoding="utf-8")
            return {"ok": True, "agen": agen, "alat": alat,
                    "path": str(p), "bytes": len(kwargs.get("konten", ""))}
        if alat == "baca_json":
            p = _dalam_workspace(kwargs["path"])
            if p is None or not p.is_file():
                return {"ok": False, "agen": agen, "alat": alat,
                        "error": "path di luar workspace / file tidak ada"}
            return {"ok": True, "agen": agen, "alat": alat,
                    "data": json.loads(p.read_text(encoding="utf-8"))}
        if alat == "tulis_json":
            p = _dalam_workspace(kwargs["path"])
            if p is None:
                return {"ok": False, "agen": agen, "alat": alat,
                        "error": "path di luar workspace — ditolak"}
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(kwargs.get("data", {}), ensure_ascii=False,
                                    indent=2), encoding="utf-8")
            return {"ok": True, "agen": agen, "alat": alat, "path": str(p)}
        if alat in ("baca_memori", "simpan_memori", "catat_tugas"):
            mem = _memori()
            if mem is None:
                return {"ok": False, "agen": agen, "alat": alat,
                        "error": "memori_bersama tidak tersedia"}
            if alat == "baca_memori":
                return {"ok": True, "agen": agen, "alat": alat,
                        "data": mem.baca(kunci=kwargs.get("kunci"),
                                         jenis=kwargs.get("jenis"),
                                         agen=kwargs.get("agen_cari"),
                                         limit=int(kwargs.get("limit", 100)))}
            if alat == "simpan_memori":
                ok = mem.simpan(agen, kwargs["jenis"], kwargs["kunci"],
                                kwargs["nilai"], kwargs.get("sumber", ""))
                return {"ok": bool(ok), "agen": agen, "alat": alat}
            mem.catat_tugas(agen, kwargs.get("tugas", ""),
                            kwargs.get("hasil", ""),
                            kwargs.get("status", "selesai"))
            return {"ok": True, "agen": agen, "alat": alat}
        if alat == "panggil_llm":
            import llm_router

            hasil = llm_router.jalankan(
                kwargs.get("kelas", "cepat"),
                kwargs.get("tugas", f"panggil_llm:{agen}"),
                kwargs.get("prompt", ""),
                timeout=int(kwargs.get("timeout", 600)),
                max_tokens=int(kwargs.get("max_tokens", 512)),
            )
            return {"ok": bool(hasil.get("ok")), "agen": agen, "alat": alat,
                    "hasil": hasil}
        if alat == "baca_harga_kompetitor":
            import harga_kompetitor

            return {"ok": True, "agen": agen, "alat": alat,
                    "data": harga_kompetitor.daftar_harga(
                        kategori=kwargs.get("kategori"),
                        limit=int(kwargs.get("limit", 100)))}
        if alat == "baca_crm":
            import crm

            if kwargs.get("id"):
                hasil = [k for k in crm.daftar_pelanggan()
                         if k.get("id") == kwargs["id"]]
                return {"ok": True, "agen": agen, "alat": alat,
                        "data": hasil}
            if kwargs.get("kata_kunci"):
                return {"ok": True, "agen": agen, "alat": alat,
                        "data": crm.cari_pelanggan(kwargs["kata_kunci"])}
            return {"ok": True, "agen": agen, "alat": alat,
                    "data": crm.daftar_pelanggan(
                        status=kwargs.get("status"))}
        if alat == "simpan_crm":
            import crm

            aksi = kwargs.get("aksi", "ubah_status")
            if aksi == "ubah_status":
                ok, pesan = crm.ubah_status(
                    kwargs["id"], kwargs["status"],
                    kwargs.get("catatan", ""))
                return {"ok": bool(ok), "agen": agen, "alat": alat,
                        "pesan": pesan}
            if aksi == "tambah":
                ok, pesan = crm.tambah_pelanggan(kwargs.get("kontak", {}))
                return {"ok": bool(ok), "agen": agen, "alat": alat,
                        "pesan": pesan}
            return {"ok": False, "agen": agen, "alat": alat,
                    "error": f"aksi simpan_crm tidak dikenal: {aksi!r}"}
        if alat == "handoff":
            return {"ok": True, "agen": agen, "alat": alat,
                    "lanjut_ke": kwargs.get("lanjut_ke"),
                    "data": kwargs.get("data")}
    except Exception as e:  # noqa: BLE001 - laporkan apa adanya
        return {"ok": False, "agen": agen, "alat": alat,
                "error": f"{type(e).__name__}: {e}"}
    return {"ok": False, "agen": agen, "alat": alat,
            "error": "alat tidak punya pelaksana"}


def info():
    return {
        "modul": "tool_registry",
        "versi": "3.1 FREE EDITION",
        "jumlah_alat": len(ALAT_BAWAAN),
        "alat": sorted(ALAT_BAWAAN),
        "catatan": "Tidak ada alat kirim/bayar/publikasi/submit/upload/hapus.",
    }


if __name__ == "__main__":
    print(json.dumps(info(), ensure_ascii=False, indent=2))
    print("cek_izin A09 baca_harga_kompetitor:",
          cek_izin("A09", "baca_harga_kompetitor"))
    print("cek_izin A09 kirim_email:",
          cek_izin("A09", "kirim_email"))
    print("daftarkan kirim_wa:",
          daftarkan("kirim_wa", "kirim WA", ["EXECUTE"], "semua"))
