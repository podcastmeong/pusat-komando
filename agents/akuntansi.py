"""BINTANG COMMAND CENTER — Modul Akuntansi (akuntansi.py).
Dibuat 21 Nov 2026 atas perintah Cipta (Pusat Komando, Item 2).

Modul Akuntansi = pencatatan pemasukan/pengeluaran, laporan keuangan,
dan saldo berjalan untuk SatuKiki. Dibangun mengikuti PERSIS pola
agents/penjualan.py (struktur fungsi, validasi, cara muat/simpan
JSON, info(), contoh()) — dan seperti penjualan.py, modul ini TIDAK
mengimpor memori_bersama.

KEJUJURAN WAJIB — BACA DULU:
- Modul ini PASIF: dijalankan Muse, BUKAN layanan otonom 24 jam.
- Modul ini TIDAK PUNYA fungsi kirim / bayar / publikasi / submit /
  upload / hapus / transfer apa pun, sengaja. Modul ini hanya
  MENCATAT pemasukan dan pengeluaran yang SUDAH terjadi (uang masuk/
  keluar yang sudah dicek manual di platform/rekening) dan MENYIAPKAN
  laporan. Uang tidak pernah bergerak lewat modul ini.
- Data entri disimpan di data/akuntansi.json — BUKAN di
  memori_bersama.db. Modul ini sengaja TIDAK mengimpor
  memori_bersama.
- Data awal KOSONG: pemasukan/pengeluaran selama ini masih dicek
  manual per platform, jadi tidak ada angka yang dikarang di sini.
  Entri dicatat HANYA bila ada bukti (tangkapan layar / riwayat
  platform / konfirmasi pembeli / struk) — bila tidak ada bukti,
  jangan dicatat, tulis "belum cukup data".
- Modul ini TIDAK menggantikan data/keuangan_data.json (baseline
  Rp0 per 18 Nov 2026 + kurs USD, dipakai a07_keuangan.py) dan TIDAK
  menggantikan data/penjualan.json (transaksi penjualan per produk/
  platform). Akuntansi mencatat arus kas menyeluruh (termasuk
  pengeluaran); penjualan mencatat pemasukan per transaksi. Bila
  satu pemasukan dicatat di kedua tempat, itu pencatatan ganda yang
  disengaja untuk dua sudut pandang — laporan akuntansi adalah yang
  dipakai untuk saldo, bukan jumlah keduanya.

JENIS: pemasukan, pengeluaran.
KATEGORI PEMASUKAN: penjualan_produk, jasa, afiliasi, iklan, lainnya.
KATEGORI PENGELUARAN: operasional, iklan, alat, langganan, lainnya.
STATUS ENTRI: dicatat (sudah terjadi, belum dicek silang),
terverifikasi (sudah terlihat di PayPal/BCA), dibatalkan.
Entri yang dibatalkan TIDAK dihitung di laporan maupun saldo.
"""
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
AKUNTANSI_FILE = DATA / "akuntansi.json"

KODE = "AKUNTANSI"
NAMA = "Modul Akuntansi"
DIVISI = "Keuangan"
ATASAN = "A02"
STATUS_DIIZINKAN = ["dicatat", "terverifikasi", "dibatalkan"]
BELUM = "belum cukup data"

JENIS_DIIZINKAN = ["pemasukan", "pengeluaran"]
KATEGORI_PEMASUKAN = ["penjualan_produk", "jasa", "afiliasi", "iklan",
                      "lainnya"]
KATEGORI_PENGELUARAN = ["operasional", "iklan", "alat", "langganan",
                        "lainnya"]
KATEGORI_DIIZINKAN = {
    "pemasukan": KATEGORI_PEMASUKAN,
    "pengeluaran": KATEGORI_PENGELUARAN,
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


def _muat():
    """Baca data/akuntansi.json. Bila belum ada/rusak, kembalikan
    struktur kosong."""
    try:
        with open(AKUNTANSI_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(
                data.get("entri"), list):
            data.setdefault("riwayat", [])
            return data
    except Exception:
        pass
    return {"entri": [], "riwayat": []}


def _simpan(data):
    """Tulis data/akuntansi.json (indent 2, UTF-8)."""
    AKUNTANSI_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AKUNTANSI_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def _catat_riwayat(data, entri_id, aksi, catatan=""):
    data.setdefault("riwayat", []).append({
        "waktu": _hari_ini(),
        "id": entri_id,
        "aksi": aksi,
        "catatan": catatan,
    })


def catat_entri(entri):
    """Catat satu entri pemasukan/pengeluaran (uang yang SUDAH terjadi
    + ada bukti). Entri = dict: jenis (wajib: pemasukan/pengeluaran),
    jumlah (wajib, Rp, bilangan bulat > 0), tanggal (wajib,
    YYYY-MM-DD), kategori (wajib, sesuai jenis), deskripsi +
    keterangan (opsional). Status awal 'dicatat'. Id duplikat
    ditolak. Kembalikan (ok_bool, pesan)."""
    e = dict(entri or {})
    jenis = (e.get("jenis") or "").strip().lower()
    if jenis not in JENIS_DIIZINKAN:
        return False, (f"DITOLAK: jenis {jenis!r} tidak dikenal. "
                       f"Pakai salah satu: {', '.join(JENIS_DIIZINKAN)}.")
    kategori = (e.get("kategori") or "").strip().lower()
    if kategori not in KATEGORI_DIIZINKAN[jenis]:
        return False, (f"DITOLAK: kategori {kategori!r} tidak dikenal "
                       f"untuk jenis {jenis!r}. Pakai salah satu: "
                       f"{', '.join(KATEGORI_DIIZINKAN[jenis])}.")
    try:
        jumlah = int(e.get("jumlah"))
    except (TypeError, ValueError):
        return False, "DITOLAK: jumlah wajib bilangan bulat (Rp)."
    if isinstance(e.get("jumlah"), bool):
        return False, "DITOLAK: jumlah wajib bilangan bulat (Rp)."
    if jumlah <= 0:
        return False, "DITOLAK: jumlah harus > 0."
    tanggal = (e.get("tanggal") or "").strip()
    if not _tanggal_valid(tanggal):
        return False, "DITOLAK: tanggal wajib format YYYY-MM-DD."
    data = _muat()
    eid = (e.get("id") or "").strip()
    if not eid:
        eid = "akt-{:03d}".format(len(data["entri"]) + 1)
    if any(x.get("id") == eid for x in data["entri"]):
        return False, f"DITOLAK: id {eid!r} sudah ada."
    baru = {
        "id": eid,
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "jumlah": jumlah,
        "deskripsi": (e.get("deskripsi") or "").strip() or BELUM,
        "keterangan": (e.get("keterangan") or "").strip(),
        "bukti": (e.get("bukti") or "").strip() or BELUM,
        "status": "dicatat",
        "tanggal_catat": _hari_ini(),
    }
    data["entri"].append(baru)
    _catat_riwayat(data, eid, "catat",
                   f"{jenis} {kategori} Rp{jumlah:,}.")
    _simpan(data)
    return True, f"Entri {eid} dicatat: {jenis} {kategori} Rp{jumlah:,}."


def ubah_status_entri(entri_id, status, catatan=""):
    """Ubah status satu entri: dicatat / terverifikasi / dibatalkan.
    Id tidak ada / status tidak dikenal ditolak.
    Kembalikan (ok_bool, pesan)."""
    status = (status or "").strip()
    if status not in STATUS_DIIZINKAN:
        return False, f"DITOLAK: status {status!r} tidak dikenal."
    data = _muat()
    for x in data["entri"]:
        if x.get("id") == entri_id:
            lama = x.get("status", "")
            x["status"] = status
            if catatan:
                x["keterangan"] = ((x.get("keterangan") or "") + " | "
                                   + catatan).strip(" |") \
                    if x.get("keterangan") else catatan
            _catat_riwayat(data, entri_id, "ubah_status",
                           f"{lama} -> {status}. {catatan}".strip())
            _simpan(data)
            return True, (f"Status {entri_id} diubah: "
                          f"{lama} -> {status}.")
    return False, f"DITOLAK: id {entri_id!r} tidak ditemukan."


def daftar_entri(jenis=None, kategori=None, dari=None, sampai=None,
                 status=None):
    """Daftar entri, difilter jenis / kategori / rentang tanggal
    (YYYY-MM-DD) / status. Tanpa filter = semua, urut tanggal."""
    out = []
    for x in _muat()["entri"]:
        if jenis and x.get("jenis") != jenis:
            continue
        if kategori and x.get("kategori") != kategori:
            continue
        if status and x.get("status") != status:
            continue
        if dari and x.get("tanggal", "") < dari:
            continue
        if sampai and x.get("tanggal", "") > sampai:
            continue
        out.append(x)
    return sorted(out, key=lambda x: (x.get("tanggal", ""),
                                      x.get("id", "")))


def _aktif(entri):
    """Hanya entri berstatus dicatat + terverifikasi; yang dibatalkan
    TIDAK dihitung."""
    return [x for x in entri if x.get("status") != "dibatalkan"]


def total_keuangan(jenis=None, kategori=None, dari=None, sampai=None):
    """Total pemasukan + total pengeluaran + saldo (hanya entri aktif;
    yang dibatalkan TIDAK dihitung) + rincian per kategori.
    Kembalikan dict."""
    entri = daftar_entri(jenis=jenis, kategori=kategori, dari=dari,
                         sampai=sampai)
    aktif = _aktif(entri)
    masuk = sum(x.get("jumlah", 0) for x in aktif
                if x.get("jenis") == "pemasukan")
    keluar = sum(x.get("jumlah", 0) for x in aktif
                 if x.get("jenis") == "pengeluaran")
    per_kategori = {}
    for x in aktif:
        kunci = f"{x.get('jenis')}/{x.get('kategori', '?')}"
        per_kategori[kunci] = per_kategori.get(kunci, 0) + \
            x.get("jumlah", 0)
    return {
        "total_pemasukan": masuk,
        "total_pengeluaran": keluar,
        "saldo": masuk - keluar,
        "jumlah_entri": len(aktif),
        "dibatalkan_tidak_dihitung": len(entri) - len(aktif),
        "per_kategori": per_kategori,
        "filter": {"jenis": jenis, "kategori": kategori,
                   "dari": dari, "sampai": sampai},
    }


def saldo_berjalan(sampai=None):
    """Saldo berjalan: tiap entri aktif urut tanggal (lalu id) dengan
    saldo setelah entri itu. Entri dibatalkan dilewati (tidak mengubah
    saldo). Kembalikan dict berisi daftar + saldo akhir."""
    entri = _aktif(daftar_entri(sampai=sampai))
    saldo = 0
    jalan = []
    for x in entri:
        if x.get("jenis") == "pemasukan":
            saldo += x.get("jumlah", 0)
        else:
            saldo -= x.get("jumlah", 0)
        jalan.append({
            "id": x.get("id"),
            "tanggal": x.get("tanggal"),
            "jenis": x.get("jenis"),
            "kategori": x.get("kategori"),
            "jumlah": x.get("jumlah"),
            "status": x.get("status"),
            "saldo_setelah": saldo,
        })
    return {
        "sampai": sampai,
        "saldo_akhir": saldo,
        "jumlah_entri": len(jalan),
        "saldo_berjalan": jalan,
        "catatan": ("Hanya entri berstatus dicatat/terverifikasi yang "
                    "dihitung; yang dibatalkan tidak dihitung."),
    }


def riwayat(entri_id):
    """Riwayat perubahan satu entri (urut kronologis)."""
    return [r for r in _muat().get("riwayat", [])
            if r.get("id") == entri_id]


def laporan_keuangan(dari=None, sampai=None):
    """Laporan keuangan: total pemasukan, total pengeluaran, saldo,
    rincian per bulan (pemasukan/pengeluaran/saldo) + per kategori +
    saldo akhir. Bila tanpa rentang, pakai semua entri.
    Kembalikan dict."""
    total = total_keuangan(dari=dari, sampai=sampai)
    aktif = _aktif(daftar_entri(dari=dari, sampai=sampai))
    per_bulan = {}
    for x in aktif:
        bulan = (x.get("tanggal", "") or "")[:7]
        slot = per_bulan.setdefault(bulan, {"pemasukan": 0,
                                            "pengeluaran": 0,
                                            "saldo": 0})
        if x.get("jenis") == "pemasukan":
            slot["pemasukan"] += x.get("jumlah", 0)
        else:
            slot["pengeluaran"] += x.get("jumlah", 0)
        slot["saldo"] = slot["pemasukan"] - slot["pengeluaran"]
    return {
        "dari": dari,
        "sampai": sampai,
        "total_pemasukan": total["total_pemasukan"],
        "total_pengeluaran": total["total_pengeluaran"],
        "saldo": total["saldo"],
        "jumlah_entri": total["jumlah_entri"],
        "dibatalkan_tidak_dihitung":
            total["dibatalkan_tidak_dihitung"],
        "per_bulan": dict(sorted(per_bulan.items())),
        "per_kategori": total["per_kategori"],
        "saldo_akhir": saldo_berjalan(sampai=sampai)["saldo_akhir"],
        "catatan": ("Hanya entri berstatus dicatat/terverifikasi yang "
                    "dihitung; yang dibatalkan tidak dihitung."),
    }


def info():
    """Metadata modul (untuk tes + tab Pusat Komando)."""
    return {
        "kode": KODE,
        "nama": NAMA,
        "divisi": DIVISI,
        "atasan": ATASAN,
        "job_desc": "Modul akuntansi — catat pemasukan/pengeluaran, "
                    "laporan keuangan, dan saldo berjalan",
        "status": "Aktif",
        "file_data": str(AKUNTANSI_FILE),
        "jenis_diizinkan": list(JENIS_DIIZINKAN),
        "kategori_pemasukan": list(KATEGORI_PEMASUKAN),
        "kategori_pengeluaran": list(KATEGORI_PENGELUARAN),
        "status_diizinkan": list(STATUS_DIIZINKAN),
        "pasif": True,
        "catatan": ("Pencatatan saja. Tidak ada fungsi kirim/bayar/"
                    "publikasi/submit/upload/hapus/transfer. Data awal "
                    "kosong — entri dicatat hanya bila ada bukti."),
    }


def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    lap = laporan_keuangan()
    if lap["jumlah_entri"] == 0:
        return {"catatan": "Belum ada entri — data awal kosong. "
                           "Catat entri bila ada bukti uang masuk/keluar.",
                "laporan": lap}
    return {"laporan": lap}
