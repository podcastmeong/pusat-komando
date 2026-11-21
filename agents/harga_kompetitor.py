#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO 2.0 — harga_kompetitor.py
# Database Harga Kompetitor 3.1 — FREE EDITION (21 Nov 2026, perintah
# Cipta "Eksekusi", rencana ChatGPT 3.1 + DeepSeek: A09 alur CSV).
#
# Tabel harga_kompetitor tinggal DI DALAM memori_bersama.db (ingatan
# bersama SQLite yang sudah ada) — TIDAK membuat database kedua.
# Skema mengikuti saran ChatGPT: nama pesaing, produk, paket, harga,
# fitur, sumber URL, tanggal cek, status.
#
# ATURAN JUJUR (A09): harga HANYA dari sumber resmi yang dibaca
# langsung (halaman harga/toko/listing resmi). Bila tidak ditemukan,
# status = "belum cukup data" dan harga dikosongkan — JANGAN menebak,
# JANGAN mengarang, JANGAN mengonversi mata uang (harga USD tetap
# ditulis "$..." apa adanya, tanpa kurs karangan).
#
# CSV: data/harga_kompetitor.csv — kolom: nama, produk, paket,
# harga Rp, fitur, sumber URL, tanggal cek, status. A09 membaca
# CSV ini (muat_dari_csv) atau tabelnya langsung (daftar_harga).
# Perbarui tiap 7 hari (saran ChatGPT).
#
# SIFAT: modul PASIF. Tidak berjalan sendiri. Tidak ada fungsi
# kirim/bayar/publikasi/submit.
# ======================================================================
"""Database + CSV harga kompetitor (A09) di memori_bersama.db."""

import csv
import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "data" / "memori_bersama.db"
CSV_PATH = BASE / "data" / "harga_kompetitor.csv"
JSON_AWAL = BASE / "data" / "harga_kompetitor_awal.json"

KOLOM_CSV = ["nama", "produk", "paket", "harga Rp", "fitur",
             "sumber URL", "tanggal cek", "status"]

SKEMA = """
CREATE TABLE IF NOT EXISTS harga_kompetitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pesaing TEXT NOT NULL,
    produk TEXT NOT NULL,
    kategori TEXT DEFAULT '',
    paket TEXT DEFAULT '',
    harga TEXT DEFAULT '',
    harga_rp INTEGER,
    mata_uang TEXT DEFAULT 'IDR',
    fitur TEXT DEFAULT '',
    sumber_url TEXT NOT NULL,
    tanggal_cek TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'terverifikasi',
    UNIQUE(pesaing, produk, paket, sumber_url)
)
"""


def _koneksi():
    return sqlite3.connect(DB_PATH)


def init_tabel():
    con = _koneksi()
    try:
        con.execute(SKEMA)
        con.commit()
    finally:
        con.close()


def tambah_harga(pesaing, produk, sumber_url, tanggal_cek, kategori="",
                 paket="", harga="", harga_rp=None, mata_uang="IDR",
                 fitur="", status="terverifikasi"):
    """Tambah satu baris harga. Kembalikan True bila baru, False bila
    sudah ada (UNIQUE) atau bila status 'belum cukup data' tanpa harga
    (tetap dicatat sebagai kesenjangan, bukan harga)."""
    init_tabel()
    con = _koneksi()
    try:
        cur = con.execute(
            """INSERT OR IGNORE INTO harga_kompetitor
               (pesaing, produk, kategori, paket, harga, harga_rp,
                mata_uang, fitur, sumber_url, tanggal_cek, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (pesaing, produk, kategori, paket, harga, harga_rp,
             mata_uang, fitur, sumber_url, tanggal_cek, status),
        )
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()


def muat_dari_json(path_json=None):
    """Muat harga awal dari JSON riset (harga_kompetitor_awal.json).
    Mengembalikan (baru, sudah_ada, belum_cukup_data)."""
    path_json = Path(path_json) if path_json else JSON_AWAL
    data = json.loads(Path(path_json).read_text(encoding="utf-8"))
    baru = sudah = 0
    for h in data.get("harga", []):
        ok = tambah_harga(
            pesaing=h.get("pesaing", ""),
            produk=h.get("produk", ""),
            sumber_url=h.get("sumber_url", ""),
            tanggal_cek=h.get("tanggal_cek", "2026-11-21"),
            kategori=h.get("kategori", ""),
            paket=h.get("paket", ""),
            harga=h.get("harga", ""),
            harga_rp=_angka_rp(h.get("harga", "")),
            mata_uang=h.get("mata_uang", "IDR"),
            fitur=h.get("fitur", ""),
            status=h.get("status", "terverifikasi"),
        )
        baru += 1 if ok else 0
        sudah += 0 if ok else 1
    belum = 0
    for item in data.get("belum_cukup_data", []):
        # Catat kesenjangan sebagai baris status "belum cukup data"
        # (bukan harga) agar A09 tahu apa yang masih dicari.
        ket = str(item)
        nama = ket.split(":")[0].strip()
        ok = tambah_harga(
            pesaing="(belum ada pesaing terverifikasi)",
            produk=nama,
            sumber_url="",
            tanggal_cek=data.get("tanggal_cek", "2026-11-21"),
            kategori="kesenjangan",
            paket="",
            harga="",
            fitur=ket[:500],
            status="belum cukup data",
        )
        belum += 1 if ok else 0
    return baru, sudah, belum


def _angka_rp(harga):
    """Ambil angka rupiah dari string 'Rp99.000' -> 99000.
    Harga non-IDR (mis. '$15') -> None (tidak dikonversi)."""
    if not isinstance(harga, str):
        return None
    h = harga.strip()
    if not h.startswith("Rp"):
        return None
    angka = "".join(ch for ch in h if ch.isdigit())
    return int(angka) if angka else None


def daftar_harga(kategori=None, status="terverifikasi", limit=100):
    init_tabel()
    con = _koneksi()
    con.row_factory = sqlite3.Row
    try:
        sql = "SELECT * FROM harga_kompetitor WHERE 1=1"
        args = []
        if status:
            sql += " AND status = ?"
            args.append(status)
        if kategori:
            sql += " AND kategori = ?"
            args.append(kategori)
        sql += " ORDER BY kategori, pesaing, produk LIMIT ?"
        args.append(int(limit))
        return [dict(r) for r in con.execute(sql, args)]
    finally:
        con.close()


def ringkasan():
    init_tabel()
    con = _koneksi()
    try:
        total = con.execute(
            "SELECT COUNT(*) FROM harga_kompetitor "
            "WHERE status = 'terverifikasi'").fetchone()[0]
        belum = con.execute(
            "SELECT COUNT(*) FROM harga_kompetitor "
            "WHERE status = 'belum cukup data'").fetchone()[0]
        per_kategori = con.execute(
            "SELECT kategori, COUNT(*) FROM harga_kompetitor "
            "WHERE status = 'terverifikasi' GROUP BY kategori").fetchall()
        return {
            "terverifikasi": total,
            "belum_cukup_data": belum,
            "per_kategori": dict(per_kategori),
            "db": str(DB_PATH),
            "csv": str(CSV_PATH),
        }
    finally:
        con.close()


def ekspor_csv(path_csv=None):
    """Tulis seluruh isi tabel ke CSV (kolom sesuai permintaan DeepSeek
    untuk alur A09). Mengembalikan jumlah baris yang ditulis."""
    path_csv = Path(path_csv) if path_csv else CSV_PATH
    init_tabel()
    con = _koneksi()
    con.row_factory = sqlite3.Row
    try:
        baris = con.execute(
            "SELECT pesaing, produk, paket, harga, mata_uang, fitur, "
            "sumber_url, tanggal_cek, status FROM harga_kompetitor "
            "ORDER BY kategori, pesaing, produk").fetchall()
    finally:
        con.close()
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        tulis = csv.writer(f)
        tulis.writerow(KOLOM_CSV)
        for r in baris:
            harga_tampil = r["harga"]
            if r["mata_uang"] and r["mata_uang"] != "IDR" and harga_tampil:
                harga_tampil = f"{harga_tampil} ({r['mata_uang']})"
            tulis.writerow([
                r["pesaing"], r["produk"], r["paket"], harga_tampil,
                r["fitur"], r["sumber_url"], r["tanggal_cek"], r["status"],
            ])
    return len(baris)


def muat_dari_csv(path_csv=None):
    """Baca CSV (format ekspor_csv) kembali ke tabel.
    Mengembalikan (baru, sudah_ada)."""
    path_csv = Path(path_csv) if path_csv else CSV_PATH
    baru = sudah = 0
    with open(path_csv, newline="", encoding="utf-8") as f:
        for baris in csv.DictReader(f):
            if (baris.get("status") or "").strip() == "belum cukup data":
                continue  # kesenjangan tidak dimuat ulang dari CSV
            harga = (baris.get("harga Rp") or "").strip()
            mata_uang = "IDR"
            if "(USD)" in harga:
                harga = harga.replace(" (USD)", "").strip()
                mata_uang = "USD"
            ok = tambah_harga(
                pesaing=(baris.get("nama") or "").strip(),
                produk=(baris.get("produk") or "").strip(),
                sumber_url=(baris.get("sumber URL") or "").strip(),
                tanggal_cek=(baris.get("tanggal cek") or "").strip(),
                paket=(baris.get("paket") or "").strip(),
                harga=harga,
                harga_rp=_angka_rp(harga),
                mata_uang=mata_uang,
                fitur=(baris.get("fitur") or "").strip(),
                status=(baris.get("status") or "terverifikasi").strip(),
            )
            baru += 1 if ok else 0
            sudah += 0 if ok else 1
    return baru, sudah


def info():
    return {"modul": "harga_kompetitor", "versi": "3.1 FREE EDITION",
            "tabel": "harga_kompetitor @ memori_bersama.db",
            **ringkasan()}


if __name__ == "__main__":
    print(json.dumps(info(), ensure_ascii=False, indent=2))
