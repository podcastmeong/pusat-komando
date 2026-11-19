# ======================================================================
# PUSAT KOMANDO — pembantu bersama tim Agent 9 (9A Rancang, 9B Bangun,
# 9C Jualan, 9D Bangun-2, 9E Bangun-3, 9F Verifikasi & Katalog). Bukan
# agent/tab sendiri: hanya data + fungsi bersama untuk alur produksi
# (pipa) game & aplikasi di data/produksi_game.json.
# Ditambahkan 19 Nov 2026 atas perintah Cipta ("tambah 3 tim Agent 9",
# "langsung hubungkan dengan wadah"). Tim 9D/9E/9F ditambahkan 19 Nov 2026
# ("tambah 3 tim Agent 9 agar lebih cepat").
#
# Alur status: antrean -> spesifikasi-selesai (9A) -> diuji-lolos (9B/9D/9E)
#              -> siap-jual (9C) -> di-toko (9C, setelah listing masuk toko).
# Klaim bangun: proyek berstatus spesifikasi-selesai hanya boleh dikerjakan
# SATU tim bangun (9B/9D/9E) dalam satu waktu — field "klaim" berisi
# {"oleh": tim, "tanggal": ...} atau None. Uji otomatis mengklaim bila
# proyek masih bebas, dan menolak bila sudah diklaim tim lain (anti
# double-build). Verifikasi independen 9F dicatat di "verifikasi_9f".
# Semua output tim adalah DRAF untuk persetujuan Cipta (SOP v1.3).
# ======================================================================
"""Pembantu bersama tim Agent 9 — alur produksi game & aplikasi."""

import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = BASE_DIR / "produksi_game.json"

STATUS_ALUR = ["antrean", "spesifikasi-selesai", "diuji-lolos", "siap-jual", "di-toko"]
JENIS_PROYEK = ["aplikasi", "game"]

# Tim bangun paralel (boleh mengklaim + menguji proyek spesifikasi-selesai).
TIM_BANGUN = ["9B", "9D", "9E"]

# Daftar verifikasi 5 butir (sama untuk 9B, 9D, 9E, 9F).
# Butir 5 = buku panduan penggunaan — standar produk Cipta 19 Nov 2026.
CHECKLIST_UJI = [
    ("fitur_jalan", "Semua fitur utama jalan (tombol, form, hitung-hitungan benar)"),
    ("tanpa_error", "Tanpa error konsol / tanpa halaman rusak"),
    ("data_contoh_benar", "Data contoh benar dan masuk akal (nama, harga, angka konsisten)"),
    ("responsif_hp", "Tampilan rapi di HP dan laptop (tanpa scroll menyamping)"),
    ("panduan_lengkap", "Buku panduan penggunaan ada dan lengkap (cara memakai tiap fitur, Bahasa Indonesia)"),
]

# Field yang wajib ada di tiap proyek (migrasi otomatis di muat_data()).
FIELD_WAJIB = {"klaim": None, "spesifikasi": None, "hasil_uji": None,
               "listing": None, "verifikasi_9f": None, "terverifikasi_9f": False}

# Antrean produksi Agent 9 per 19 Nov 2026 (keputusan Cipta).
# Dipakai sebagai isi awal bila data/produksi_game.json belum ada.
SEED = [
    {"nama": "Kasir Toko", "jenis": "aplikasi", "status": "di-toko",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Selesai 19 Nov 2026; di Toko Aplikasi — Siap Dipakai (tombol Coba Demo). Dibangun langsung oleh Muse sebelum tim 9A/9B/9C dibentuk."},
    {"nama": "Absensi Online", "jenis": "aplikasi", "status": "di-toko",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Selesai 19 Nov 2026; di Toko Aplikasi — Siap Dipakai (tombol Coba Demo). Dibangun langsung oleh Muse sebelum tim 9A/9B/9C dibentuk."},
    {"nama": "Distributor & Grosir", "jenis": "aplikasi", "status": "di-toko",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Selesai 19 Nov 2026; konsep BINTANG DISTRIBUTOR SYSTEM; di Toko Aplikasi — Siap Dipakai. Dibangun langsung oleh Muse sebelum tim 9A/9B/9C dibentuk."},
    {"nama": "Arsip Dokumen", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (DMS — bagian dari peta aplikasi perusahaan)."},
    {"nama": "Aset Perusahaan", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9."},
    {"nama": "Program Bengkel", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (kasir niche bengkel)."},
    {"nama": "OCR", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (baca teks dari foto struk/dokumen)."},
    {"nama": "Accounting", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (akuntansi sederhana UMKM)."},
    {"nama": "Rekap", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (laporan/rekap bisnis)."},
    {"nama": "CRM", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (kelola pelanggan + prospek — kandidat dari peta aplikasi perusahaan)."},
    {"nama": "Pembelian", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (supplier + PO)."},
    {"nama": "Toko Online", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (penjualan produk secara online)."},
    {"nama": "Sistem Laundry", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (target: pengusaha laundry)."},
    {"nama": "Sistem Restoran", "jenis": "aplikasi", "status": "antrean",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Antrean produksi Agent 9 (target: restoran dan kafe)."},
    {"nama": "Distributor khusus (1 jenis paling sering digunakan)", "jenis": "aplikasi",
     "status": "antrean", "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Diputuskan nanti (Cipta, 19 Nov 2026): khusus buat 1 saja yang paling sering digunakan; jenisnya diputuskan berdasarkan yang paling sering dipakai pembeli."},
    {"nama": "Oyen Tangkap Ikan", "jenis": "game", "status": "siap-jual",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Game HTML5 selesai + teruji; di Toko Aplikasi berstatus Segera Hadir — menunggu akun itch.io + keputusan harga Cipta."},
    {"nama": "Spookify", "jenis": "game", "status": "di-toko",
     "spesifikasi": None, "hasil_uji": None, "listing": None,
     "catatan": "Live di GitHub Pages (podcastmeong.github.io/spookify/); di Toko Aplikasi sebagai game gratis."},
]


def _hari_ini():
    return date.today().isoformat()


def _normalisasi(data):
    """Pastikan tiap proyek punya semua field wajib (migrasi data lama)."""
    for p in data:
        if not isinstance(p, dict):
            continue
        for kunci, nilai in FIELD_WAJIB.items():
            p.setdefault(kunci, nilai)
    return data


def muat_data():
    """Muat antrean produksi; bila file belum ada, isi awal dari SEED."""
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return _normalisasi(data)
        except Exception:
            pass
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    data = [dict(e) for e in SEED]
    _normalisasi(data)
    simpan_data(data)
    return data


def simpan_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cari(data, nama):
    """Cari proyek berdasarkan nama (tidak peduli huruf besar/kecil)."""
    nama = (nama or "").strip().lower()
    for p in data:
        if str(p.get("nama", "")).lower() == nama:
            return p
    return None


def daftar_nama(data, status=None):
    """Daftar nama proyek, opsional disaring berdasarkan status."""
    if status is None:
        return [p.get("nama", "") for p in data]
    if isinstance(status, str):
        status = [status]
    return [p.get("nama", "") for p in data if p.get("status") in status]


# ---------------------------------------------------------------------------
# Klaim bangun (anti double-build): satu proyek spesifikasi-selesai hanya
# boleh dikerjakan satu tim bangun (9B/9D/9E) dalam satu waktu.
# ---------------------------------------------------------------------------
def daftar_siap_bangun(data=None):
    """Nama proyek spesifikasi-selesai yang belum diklaim tim mana pun."""
    if data is None:
        data = muat_data()
    return [p.get("nama", "") for p in data
            if p.get("status") == "spesifikasi-selesai" and not p.get("klaim")]


def daftar_klaim(data=None):
    """Daftar klaim aktif: [(nama, tim, tanggal)]."""
    if data is None:
        data = muat_data()
    out = []
    for p in data:
        klaim = p.get("klaim") or {}
        if klaim.get("oleh"):
            out.append((p.get("nama", ""), klaim.get("oleh"),
                        klaim.get("tanggal", "?")))
    return out


def klaim(nama, tim):
    """Klaim proyek spesifikasi-selesai untuk satu tim bangun.

    Kembalikan (pesan, tabel). Menolak bila proyek tidak ada, statusnya
    bukan spesifikasi-selesai, tim bukan tim bangun, atau sudah diklaim
    tim lain. Klaim oleh tim yang sama tidak dibuat duplikat.
    """
    nama = (nama or "").strip()
    tim = (tim or "").strip()
    if tim not in TIM_BANGUN:
        return "Tim '{}' bukan tim bangun (9B/9D/9E).".format(tim), tabel_pipeline()
    data = muat_data()
    proyek = cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), tabel_pipeline()
    if proyek.get("status") != "spesifikasi-selesai":
        return ("Proyek '{}' belum bisa diklaim (status: {}). "
                "Klaim hanya dari status spesifikasi-selesai.".format(
                    nama, proyek.get("status"))), tabel_pipeline()
    klaim_lama = proyek.get("klaim") or {}
    if klaim_lama.get("oleh") == tim:
        return ("Proyek '{}' sudah diklaim tim {} — lanjut bangun/uji.".format(
            nama, tim)), tabel_pipeline()
    if klaim_lama.get("oleh"):
        return ("⛔ Proyek '{}' sedang dikerjakan tim {} (sejak {}). "
                "Pilih proyek lain yang belum diklaim — jangan membangun "
                "aplikasi yang sama.".format(
                    nama, klaim_lama.get("oleh"), klaim_lama.get("tanggal", "?"))), tabel_pipeline()
    proyek["klaim"] = {"oleh": tim, "tanggal": _hari_ini()}
    simpan_data(data)
    return ("🔒 Proyek '{}' diklaim tim {} — tim bangun lain tidak bisa "
            "membangun aplikasi yang sama.".format(nama, tim)), tabel_pipeline()


def lepas(nama, tim):
    """Lepas klaim proyek (hanya tim pemilik klaim yang boleh melepas)."""
    nama = (nama or "").strip()
    tim = (tim or "").strip()
    data = muat_data()
    proyek = cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), tabel_pipeline()
    klaim_lama = proyek.get("klaim") or {}
    if not klaim_lama.get("oleh"):
        return "Proyek '{}' sedang tidak diklaim siapa pun.".format(nama), tabel_pipeline()
    if klaim_lama.get("oleh") != tim:
        return ("⛔ Klaim '{}' milik tim {} — hanya tim itu yang boleh "
                "melepasnya.".format(nama, klaim_lama.get("oleh"))), tabel_pipeline()
    proyek["klaim"] = None
    simpan_data(data)
    return "🔓 Klaim '{}' dilepas tim {} — proyek bebas diklaim tim lain.".format(
        nama, tim), tabel_pipeline()


def uji_bersama(data, nama, checklist, catatan, tim):
    """Logika uji 5 butir bersama untuk tim bangun 9B/9D/9E.

    Kembalikan (pesan, proyek_atau_None). Aturan klaim: bila proyek belum
    diklaim, tim ini otomatis mengklaimnya; bila sudah diklaim tim lain,
    uji ditolak (anti double-build). Klaim dilepas setelah uji selesai,
    apa pun hasilnya.
    """
    nama = (nama or "").strip()
    proyek = cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), None
    if proyek.get("status") != "spesifikasi-selesai":
        return ("Proyek '{}' belum bisa diuji (status: {}). "
                "Uji hanya dari status spesifikasi-selesai.".format(
                    nama, proyek.get("status"))), None
    klaim_lama = proyek.get("klaim") or {}
    if klaim_lama.get("oleh") and klaim_lama.get("oleh") != tim:
        return ("⛔ Proyek '{}' sedang dikerjakan tim {} (sejak {}). "
                "Uji ditolak — jangan membangun aplikasi yang sama.".format(
                    nama, klaim_lama.get("oleh"), klaim_lama.get("tanggal", "?"))), None
    if not klaim_lama.get("oleh"):
        proyek["klaim"] = {"oleh": tim, "tanggal": _hari_ini()}
    checklist = {kunci: bool(checklist.get(kunci)) for kunci, _label in CHECKLIST_UJI}
    lolos = all(checklist.values())
    proyek["hasil_uji"] = {
        "tanggal": _hari_ini(),
        "checklist": checklist,
        "lolos": lolos,
        "catatan_perbaikan": (catatan or "").strip(),
        "diuji_oleh": tim,
    }
    proyek["klaim"] = None
    if lolos:
        proyek["status"] = "diuji-lolos"
    if lolos:
        pesan = ("✅ '{}' LOLOS UJI tim {} (status: diuji-lolos). "
                 "Lanjut ke verifikasi 9F / listing 9C.".format(nama, tim))
    else:
        gagal = [label for kunci, label in CHECKLIST_UJI if not checklist[kunci]]
        pesan = ("❌ '{}' BELUM LOLOS UJI tim {} — status tetap "
                 "spesifikasi-selesai. Yang gagal: {}. Perbaiki dulu "
                 "(spesifikasi bisa ditulis ulang di tab 9A), lalu uji lagi.".format(
                     nama, tim, "; ".join(gagal)))
    return pesan, proyek


def ringkasan_status(data=None):
    """Hitung proyek per status alur. Kembalikan dict."""
    if data is None:
        data = muat_data()
    hasil = {s: 0 for s in STATUS_ALUR}
    for p in data:
        hasil[p.get("status", "?")] = hasil.get(p.get("status", "?"), 0) + 1
    return hasil


def tabel_pipeline(data=None):
    """Tabel antrean produksi sebagai Markdown + ringkasan per status."""
    if data is None:
        data = muat_data()
    if not data:
        return "Belum ada proyek. Tambahkan proyek pertama di tab 9A."
    baris = ["| Nama | Jenis | Status | Klaim | Catatan |", "|---|---|---|---|---|"]
    for p in data:
        klaim = p.get("klaim") or {}
        klaim_teks = klaim.get("oleh", "-") if klaim.get("oleh") else "-"
        baris.append("| {n} | {j} | {s} | {k} | {c} |".format(
            n=p.get("nama", "-"), j=p.get("jenis", "-"),
            s=p.get("status", "-"), k=klaim_teks,
            c=(p.get("catatan", "-") or "-")[:120]))
    ringkas = ringkasan_status(data)
    total = "Ringkasan: " + ", ".join(
        "{s}: {n}".format(s=s, n=n) for s, n in ringkas.items() if n)
    klaim_aktif = daftar_klaim(data)
    if klaim_aktif:
        total += "\nKlaim aktif: " + ", ".join(
            "{} (tim {})".format(n, t) for n, t, _ in klaim_aktif)
    return "\n".join(baris) + "\n\n" + total
