"""BINTANG COMMAND CENTER — Mesin Penjualan (penjualan.py).
Dibuat 21 Nov 2026 atas perintah Cipta ("Pasang" — keputusan mesin
penjualan + pemasaran, 21 Nov 2026 19:20 WIB).

Mesin Penjualan = pencatatan transaksi, target penjualan, dan pemasukan
(uang masuk per produk/platform) + laporan pemasukan untuk SatuKiki.
Dibangun di atas CRM (agents/crm.py) dan A25 Sales Manager — modul ini
TIDAK menggantikan CRM, hanya mencatat hasil penjualannya.

KEJUJURAN WAJIB — BACA DULU:
- Modul ini PASIF: dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri.
- Modul ini TIDAK PUNYA fungsi kirim / bayar / publikasi / submit /
  upload / hapus / transfer apa pun, sengaja. Modul ini hanya
  MENCATAT transaksi yang SUDAH terjadi (uang masuk yang sudah
  dicek manual di platform) dan MENYIAPKAN laporan. Uang tidak
  pernah bergerak lewat modul ini.
- Data transaksi disimpan di data/penjualan.json — BUKAN di
  memori_bersama.db. Modul ini sengaja TIDAK mengimpor
  memori_bersama.
- Data awal KOSONG: pemasukan selama ini masih dicek manual per
  platform, jadi tidak ada angka transaksi yang dikarang di sini.
  Transaksi dicatat HANYA bila ada bukti (tangkapan layar / riwayat
  platform / konfirmasi pembeli) — bila tidak ada bukti, jangan
  dicatat, tulis "belum cukup data".
- Harga acuan adalah harga yang SUDAH DIPUTUSKAN (video 15 dtk
  Rp75.000 / 30 dtk Rp150.000 / 60 dtk Rp250.000; aplikasi
  Rp499.000/Rp999.000/Rp1.999.000; website Rp1.500.000/Rp4.500.000/
  Rp9.900.000; poster Rp35.000; eBook Rp29.000/Rp19.000). Harga acuan
  hanya dipakai sebagai pembanding di laporan — jumlah transaksi
  yang dicatat adalah jumlah SEBENARNYA (bisa beda karena diskon /
  harga khusus yang disetujui Cipta). Jangan mengubah harga di sini.

PRODUK: video, aplikasi, website, ebook, pod, game, poster, jasa,
lainnya.
PLATFORM: karyakarsa, lynk.id, zazzle, kbm, saweria, trakteer, mayar,
etsy, adobe, dreamstime, whatsapp, lainnya.
STATUS TRANSAKSI: dicatat (uang masuk terlihat di platform, belum
dicek silang), terverifikasi (uang sudah terlihat di PayPal/BCA),
dibatalkan.
PERIODE TARGET: "YYYY-MM" (bulanan).
"""
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
PENJUALAN_FILE = DATA / "penjualan.json"

KODE = "PENJUALAN"
NAMA = "Mesin Penjualan"
DIVISI = "Penjualan"
ATASAN = "A02"
STATUS_DIIZINKAN = ["dicatat", "terverifikasi", "dibatalkan"]
BELUM = "belum cukup data"

PRODUK_DIIZINKAN = ["video", "aplikasi", "website", "ebook", "pod",
                    "game", "poster", "jasa", "lainnya"]
PLATFORM_DIIZINKAN = ["karyakarsa", "lynk.id", "zazzle", "kbm",
                      "saweria", "trakteer", "mayar", "etsy", "adobe",
                      "dreamstime", "whatsapp", "lainnya"]

# Harga acuan yang SUDAH DIPUTUSKAN (pembanding laporan saja).
HARGA_ACUAN = {
    "video_15dtk": 75000, "video_30dtk": 150000, "video_60dtk": 250000,
    "aplikasi_basic": 499000, "aplikasi_pro": 999000,
    "aplikasi_business": 1999000,
    "website_pemula": 1500000, "website_profesional": 4500000,
    "website_business": 9900000,
    "poster": 35000, "ebook": 29000, "ebook_rindu": 19000,
}


def _hari_ini():
    return date.today().isoformat()


def _tanggal_valid(teks):
    """True bila teks format YYYY-MM-DD dan tanggalnya nyata."""
    try:
        y, m, d = map(int, (teks or "").split("-"))
        date(y, m, d)
        return True
    except Exception:
        return False


def _periode_valid(teks):
    """True bila teks format YYYY-MM dan bulannya nyata (01-12)."""
    try:
        y, m = map(int, (teks or "").split("-"))
        return 1 <= m <= 12 and y >= 2000
    except Exception:
        return False


def _muat():
    """Baca data/penjualan.json. Bila belum ada/rusak, kembalikan
    struktur kosong."""
    try:
        with open(PENJUALAN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(
                data.get("transaksi"), list):
            data.setdefault("target", [])
            data.setdefault("riwayat", [])
            return data
    except Exception:
        pass
    return {"transaksi": [], "target": [], "riwayat": []}


def _simpan(data):
    """Tulis data/penjualan.json (indent 2, UTF-8)."""
    PENJUALAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PENJUALAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def _catat_riwayat(data, trx_id, aksi, catatan=""):
    data.setdefault("riwayat", []).append({
        "waktu": _hari_ini(),
        "id": trx_id,
        "aksi": aksi,
        "catatan": catatan,
    })


def catat_transaksi(transaksi):
    """Catat satu transaksi (uang masuk yang SUDAH terjadi + ada
    bukti). Transaksi = dict: produk (wajib), platform (wajib),
    jumlah (wajib, Rp, bilangan bulat > 0), tanggal (wajib,
    YYYY-MM-DD), pembeli + keterangan (opsional). Status awal
    'dicatat'. Id duplikat ditolak. Kembalikan (ok_bool, pesan)."""
    trx = dict(transaksi or {})
    produk = (trx.get("produk") or "").strip().lower()
    if produk not in PRODUK_DIIZINKAN:
        return False, (f"DITOLAK: produk {produk!r} tidak dikenal. "
                       f"Pakai salah satu: {', '.join(PRODUK_DIIZINKAN)}.")
    platform = (trx.get("platform") or "").strip().lower()
    if platform not in PLATFORM_DIIZINKAN:
        return False, (f"DITOLAK: platform {platform!r} tidak dikenal. "
                       f"Pakai salah satu: "
                       f"{', '.join(PLATFORM_DIIZINKAN)}.")
    try:
        jumlah = int(trx.get("jumlah"))
    except (TypeError, ValueError):
        return False, "DITOLAK: jumlah wajib bilangan bulat (Rp)."
    if jumlah <= 0:
        return False, "DITOLAK: jumlah harus > 0."
    tanggal = (trx.get("tanggal") or "").strip()
    if not _tanggal_valid(tanggal):
        return False, "DITOLAK: tanggal wajib format YYYY-MM-DD."
    data = _muat()
    tid = (trx.get("id") or "").strip()
    if not tid:
        tid = "trx-{:03d}".format(len(data["transaksi"]) + 1)
    if any(t.get("id") == tid for t in data["transaksi"]):
        return False, f"DITOLAK: id {tid!r} sudah ada."
    baru = {
        "id": tid,
        "tanggal": tanggal,
        "produk": produk,
        "platform": platform,
        "jumlah": jumlah,
        "pembeli": (trx.get("pembeli") or "").strip() or BELUM,
        "keterangan": (trx.get("keterangan") or "").strip(),
        "bukti": (trx.get("bukti") or "").strip() or BELUM,
        "status": "dicatat",
        "tanggal_catat": _hari_ini(),
    }
    data["transaksi"].append(baru)
    _catat_riwayat(data, tid, "catat",
                   f"{produk} {platform} Rp{jumlah:,}.")
    _simpan(data)
    return True, f"Transaksi {tid} dicatat: {produk} {platform} Rp{jumlah:,}."


def ubah_status_transaksi(trx_id, status, catatan=""):
    """Ubah status satu transaksi: dicatat / terverifikasi /
    dibatalkan. Id tidak ada / status tidak dikenal ditolak.
    Kembalikan (ok_bool, pesan)."""
    status = (status or "").strip()
    if status not in STATUS_DIIZINKAN:
        return False, f"DITOLAK: status {status!r} tidak dikenal."
    data = _muat()
    for t in data["transaksi"]:
        if t.get("id") == trx_id:
            lama = t.get("status", "")
            t["status"] = status
            if catatan:
                t["keterangan"] = ((t.get("keterangan") or "") + " | "
                                   + catatan).strip(" |") \
                    if t.get("keterangan") else catatan
            _catat_riwayat(data, trx_id, "ubah_status",
                           f"{lama} -> {status}. {catatan}".strip())
            _simpan(data)
            return True, (f"Status {trx_id} diubah: "
                          f"{lama} -> {status}.")
    return False, f"DITOLAK: id {trx_id!r} tidak ditemukan."


def daftar_transaksi(produk=None, platform=None, dari=None, sampai=None,
                     status=None):
    """Daftar transaksi, difilter produk / platform / rentang tanggal
    (YYYY-MM-DD) / status. Tanpa filter = semua, urut tanggal."""
    out = []
    for t in _muat()["transaksi"]:
        if produk and t.get("produk") != produk:
            continue
        if platform and t.get("platform") != platform:
            continue
        if status and t.get("status") != status:
            continue
        if dari and t.get("tanggal", "") < dari:
            continue
        if sampai and t.get("tanggal", "") > sampai:
            continue
        out.append(t)
    return sorted(out, key=lambda x: x.get("tanggal", ""))


def total_pemasukan(produk=None, platform=None, dari=None, sampai=None):
    """Total pemasukan (hanya transaksi status dicatat +
    terverifikasi; yang dibatalkan TIDAK dihitung) + rincian per
    produk dan per platform. Kembalikan dict."""
    transaksi = daftar_transaksi(produk=produk, platform=platform,
                                 dari=dari, sampai=sampai)
    aktif = [t for t in transaksi if t.get("status") != "dibatalkan"]
    total = sum(t.get("jumlah", 0) for t in aktif)
    per_produk = {}
    per_platform = {}
    for t in aktif:
        per_produk[t.get("produk", "?")] = \
            per_produk.get(t.get("produk", "?"), 0) + t.get("jumlah", 0)
        per_platform[t.get("platform", "?")] = \
            per_platform.get(t.get("platform", "?"), 0) + t.get("jumlah", 0)
    return {
        "total": total,
        "jumlah_transaksi": len(aktif),
        "dibatalkan_tidak_dihitung": len(transaksi) - len(aktif),
        "per_produk": per_produk,
        "per_platform": per_platform,
        "filter": {"produk": produk, "platform": platform,
                   "dari": dari, "sampai": sampai},
    }


def atur_target(target):
    """Atur target penjualan satu periode. Target = dict: periode
    (wajib, YYYY-MM), nominal (wajib, Rp, > 0), produk / platform
    (opsional — kosong berarti semua). Satu periode + produk +
    platform hanya boleh ada satu target (atur ulang = timpa).
    Kembalikan (ok_bool, pesan)."""
    tgt = dict(target or {})
    periode = (tgt.get("periode") or "").strip()
    if not _periode_valid(periode):
        return False, "DITOLAK: periode wajib format YYYY-MM."
    try:
        nominal = int(tgt.get("nominal"))
    except (TypeError, ValueError):
        return False, "DITOLAK: nominal wajib bilangan bulat (Rp)."
    if nominal <= 0:
        return False, "DITOLAK: nominal harus > 0."
    produk = (tgt.get("produk") or "").strip().lower()
    if produk and produk not in PRODUK_DIIZINKAN:
        return False, f"DITOLAK: produk {produk!r} tidak dikenal."
    platform = (tgt.get("platform") or "").strip().lower()
    if platform and platform not in PLATFORM_DIIZINKAN:
        return False, f"DITOLAK: platform {platform!r} tidak dikenal."
    data = _muat()
    for t in data["target"]:
        if (t.get("periode") == periode
                and t.get("produk", "") == produk
                and t.get("platform", "") == platform):
            t["nominal"] = nominal
            t["tanggal_atur"] = _hari_ini()
            _catat_riwayat(data, t.get("id", ""), "atur_target",
                           f"{periode} {produk or 'semua'} "
                           f"{platform or 'semua'} Rp{nominal:,}.")
            _simpan(data)
            return True, (f"Target {periode} diperbarui: "
                          f"Rp{nominal:,}.")
    tid = "tgt-{:03d}".format(len(data["target"]) + 1)
    data["target"].append({
        "id": tid,
        "periode": periode,
        "produk": produk,
        "platform": platform,
        "nominal": nominal,
        "tanggal_atur": _hari_ini(),
    })
    _catat_riwayat(data, tid, "atur_target",
                   f"{periode} {produk or 'semua'} "
                   f"{platform or 'semua'} Rp{nominal:,}.")
    _simpan(data)
    return True, f"Target {periode} diatur: Rp{nominal:,}."


def cek_target(periode=None):
    """Cek capaian tiap target (tercapai + persen) pada periodenya.
    Tanpa periode = semua target. Kembalikan list dict."""
    data = _muat()
    out = []
    for t in data["target"]:
        if periode and t.get("periode") != periode:
            continue
        per = t.get("periode", "")
        tercapai = total_pemasukan(
            produk=t.get("produk") or None,
            platform=t.get("platform") or None,
            dari=per + "-01", sampai=per + "-31")["total"]
        nominal = t.get("nominal", 0)
        out.append({
            "id": t.get("id"),
            "periode": per,
            "produk": t.get("produk") or "semua",
            "platform": t.get("platform") or "semua",
            "nominal": nominal,
            "tercapai": tercapai,
            "persen": round(tercapai / nominal * 100, 1) if nominal else 0,
            "status": "tercapai" if tercapai >= nominal else "belum",
        })
    return out


def laporan_pemasukan(dari=None, sampai=None):
    """Laporan pemasukan: total + rincian per produk / platform /
    bulan + capaian target pada rentang. Bila tanpa rentang, pakai
    semua transaksi. Kembalikan dict."""
    transaksi = daftar_transaksi(dari=dari, sampai=sampai)
    aktif = [t for t in transaksi if t.get("status") != "dibatalkan"]
    per_bulan = {}
    for t in aktif:
        bulan = (t.get("tanggal", "") or "")[:7]
        per_bulan[bulan] = per_bulan.get(bulan, 0) + t.get("jumlah", 0)
    total = total_pemasukan(dari=dari, sampai=sampai)
    return {
        "dari": dari,
        "sampai": sampai,
        "total_pemasukan": total["total"],
        "jumlah_transaksi": total["jumlah_transaksi"],
        "per_produk": total["per_produk"],
        "per_platform": total["per_platform"],
        "per_bulan": dict(sorted(per_bulan.items())),
        "capaian_target": cek_target(),
        "catatan": ("Hanya transaksi berstatus dicatat/terverifikasi "
                    "yang dihitung; yang dibatalkan tidak dihitung."),
    }


def info():
    """Metadata modul (untuk tes + tab Pusat Komando)."""
    return {
        "kode": KODE,
        "nama": NAMA,
        "divisi": DIVISI,
        "atasan": ATASAN,
        "job_desc": "Mesin penjualan — catat transaksi, target "
                    "penjualan, dan laporan pemasukan (uang masuk per "
                    "produk/platform)",
        "status": "Aktif",
        "file_data": str(PENJUALAN_FILE),
        "produk_diizinkan": list(PRODUK_DIIZINKAN),
        "platform_diizinkan": list(PLATFORM_DIIZINKAN),
        "status_diizinkan": list(STATUS_DIIZINKAN),
        "pasif": True,
        "catatan": ("DRAF/pencatatan saja. Tidak ada fungsi kirim/bayar/"
                    "publikasi/submit/upload/hapus/transfer. Data awal "
                    "kosong — transaksi dicatat hanya bila ada bukti."),
    }


def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    lap = laporan_pemasukan()
    if lap["jumlah_transaksi"] == 0:
        return {"catatan": "Belum ada transaksi — data awal kosong. "
                           "Catat transaksi bila ada bukti uang masuk.",
                "laporan": lap}
    return {"laporan": lap}
