"""BINTANG COMMAND CENTER — Mesin Pemasaran (pemasaran.py).
Dibuat 21 Nov 2026 atas perintah Cipta ("Pasang" — keputusan mesin
penjualan + pemasaran, 21 Nov 2026 19:20 WIB).

Mesin Pemasaran = koordinasi kampanye lintas 5 agen pemasaran
(A20 Instagram, A21 TikTok, A22 YouTube, A23 Threads, A24 SEO)
supaya tidak jalan sendiri-sendiri: tema kampanye, jadwal, agen
yang terlibat, dan hasil like/view/follow per kampanye per
platform + laporan kampanye.

KEJUJURAN WAJIB — BACA DULU:
- Modul ini PASIF: dijalankan Muse, BUKAN layanan otonom 24 jam.
- Modul ini TIDAK PUNYA fungsi kirim / bayar / publikasi / submit /
  upload / hapus apa pun, sengaja. Modul ini hanya MENCATAT
  rencana kampanye (DRAF) dan hasil yang SUDAH terjadi. Jadwal di
  sini adalah RENCANA — penayangan tetap dilakukan agen pemasaran
  masing-masing HANYA setelah Cipta setuju konten persisnya.
- Data kampanye disimpan di data/pemasaran.json — BUKAN di
  memori_bersama.db. Modul ini sengaja TIDAK mengimpor
  memori_bersama.
- Data awal KOSONG: jangan mengarang kampanye yang tidak ada.
  Kampanye dibuat HANYA bila Cipta / Muse sudah menyusun temanya.
- Jangan mengarang angka like/view/follow. Hasil dicatat HANYA
  dari angka yang terlihat di platform (insight/statistik akun).
  Bila belum ada angka, tulis 0 + catatan "belum ada data".

AGEN PEMASARAN: A20 (Instagram), A21 (TikTok), A22 (YouTube),
A23 (Threads), A24 (SEO).
PLATFORM: instagram, tiktok, youtube, threads, seo.
STATUS KAMPANYE: draf, berjalan, selesai, dibatalkan.
"""
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
PEMASARAN_FILE = DATA / "pemasaran.json"

KODE = "PEMASARAN"
NAMA = "Mesin Pemasaran"
DIVISI = "Pemasaran"
ATASAN = "A02"
STATUS_DIIZINKAN = ["draf", "berjalan", "selesai", "dibatalkan"]
BELUM = "belum cukup data"

AGEN_PEMASARAN = {"A20": "instagram", "A21": "tiktok",
                  "A22": "youtube", "A23": "threads", "A24": "seo"}
PLATFORM_DIIZINKAN = ["instagram", "tiktok", "youtube", "threads",
                      "seo"]


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
    """Baca data/pemasaran.json. Bila belum ada/rusak, kembalikan
    struktur kosong."""
    try:
        with open(PEMASARAN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(
                data.get("kampanye"), list):
            data.setdefault("hasil", [])
            data.setdefault("riwayat", [])
            return data
    except Exception:
        pass
    return {"kampanye": [], "hasil": [], "riwayat": []}


def _simpan(data):
    """Tulis data/pemasaran.json (indent 2, UTF-8)."""
    PEMASARAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PEMASARAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def _catat_riwayat(data, kmp_id, aksi, catatan=""):
    data.setdefault("riwayat", []).append({
        "waktu": _hari_ini(),
        "id": kmp_id,
        "aksi": aksi,
        "catatan": catatan,
    })


def buat_kampanye(kampanye):
    """Buat satu kampanye (DRAF rencana). Kampanye = dict: tema
    (wajib), agen (wajib, list subset A20-A24), tanggal_mulai +
    tanggal_selesai (wajib, YYYY-MM-DD, selesai >= mulai), jadwal
    (opsional, list {tanggal, platform, agen} — tanggal harus di
    dalam rentang kampanye, platform + agen harus cocok). Status
    awal 'draf'. Id duplikat ditolak. Kembalikan (ok_bool, pesan)."""
    kmp = dict(kampanye or {})
    tema = (kmp.get("tema") or "").strip()
    if not tema:
        return False, "DITOLAK: tema wajib diisi."
    agen = kmp.get("agen") or []
    if not isinstance(agen, list) or not agen:
        return False, "DITOLAK: agen wajib list (subset A20-A24)."
    agen_bersih = []
    for a in agen:
        a = str(a).strip().upper()
        if a not in AGEN_PEMASARAN:
            return False, (f"DITOLAK: agen {a!r} bukan agen pemasaran. "
                           "Pakai A20-A24.")
        if a not in agen_bersih:
            agen_bersih.append(a)
    mulai = (kmp.get("tanggal_mulai") or "").strip()
    selesai = (kmp.get("tanggal_selesai") or "").strip()
    if not _tanggal_valid(mulai) or not _tanggal_valid(selesai):
        return False, "DITOLAK: tanggal_mulai/selesai wajib YYYY-MM-DD."
    if selesai < mulai:
        return False, "DITOLAK: tanggal_selesai < tanggal_mulai."
    jadwal = kmp.get("jadwal") or []
    if not isinstance(jadwal, list):
        return False, "DITOLAK: jadwal wajib list."
    for i, j in enumerate(jadwal):
        if not isinstance(j, dict):
            return False, f"DITOLAK: jadwal[{i}] bukan dict."
        tgl = (j.get("tanggal") or "").strip()
        if not _tanggal_valid(tgl) or not (mulai <= tgl <= selesai):
            return False, (f"DITOLAK: jadwal[{i}] tanggal {tgl!r} "
                           "di luar rentang kampanye.")
        plat = (j.get("platform") or "").strip().lower()
        if plat not in PLATFORM_DIIZINKAN:
            return False, (f"DITOLAK: jadwal[{i}] platform {plat!r} "
                           "tidak dikenal.")
        ag = str(j.get("agen") or "").strip().upper()
        if ag not in AGEN_PEMASARAN:
            return False, (f"DITOLAK: jadwal[{i}] agen {ag!r} bukan "
                           "agen pemasaran.")
        if AGEN_PEMASARAN[ag] != plat:
            return False, (f"DITOLAK: jadwal[{i}] agen {ag} tidak "
                           f"memegang platform {plat}.")
        if ag not in agen_bersih:
            return False, (f"DITOLAK: jadwal[{i}] agen {ag} tidak "
                           "termasuk agen kampanye ini.")
    data = _muat()
    kid = (kmp.get("id") or "").strip()
    if not kid:
        kid = "kmp-{:03d}".format(len(data["kampanye"]) + 1)
    if any(k.get("id") == kid for k in data["kampanye"]):
        return False, f"DITOLAK: id {kid!r} sudah ada."
    baru = {
        "id": kid,
        "tema": tema,
        "agen": agen_bersih,
        "tanggal_mulai": mulai,
        "tanggal_selesai": selesai,
        "jadwal": [{
            "tanggal": (j.get("tanggal") or "").strip(),
            "platform": (j.get("platform") or "").strip().lower(),
            "agen": str(j.get("agen") or "").strip().upper(),
            "konten": (j.get("konten") or "").strip(),
        } for j in jadwal],
        "status": "draf",
        "tanggal_buat": _hari_ini(),
        "catatan": (kmp.get("catatan") or "").strip(),
    }
    data["kampanye"].append(baru)
    _catat_riwayat(data, kid, "buat",
                   f"Tema: {tema}. Agen: {', '.join(agen_bersih)}.")
    _simpan(data)
    return True, f"Kampanye {kid} dibuat (DRAF): {tema!r}."


def ubah_status_kampanye(kmp_id, status, catatan=""):
    """Ubah status satu kampanye: draf / berjalan / selesai /
    dibatalkan. Id tidak ada / status tidak dikenal ditolak.
    Kembalikan (ok_bool, pesan)."""
    status = (status or "").strip()
    if status not in STATUS_DIIZINKAN:
        return False, f"DITOLAK: status {status!r} tidak dikenal."
    data = _muat()
    for k in data["kampanye"]:
        if k.get("id") == kmp_id:
            lama = k.get("status", "")
            k["status"] = status
            if catatan:
                k["catatan"] = ((k.get("catatan") or "") + " | "
                                + catatan).strip(" |") \
                    if k.get("catatan") else catatan
            _catat_riwayat(data, kmp_id, "ubah_status",
                           f"{lama} -> {status}. {catatan}".strip())
            _simpan(data)
            return True, (f"Status {kmp_id} diubah: "
                          f"{lama} -> {status}.")
    return False, f"DITOLAK: id {kmp_id!r} tidak ditemukan."


def daftar_kampanye(status=None, agen=None):
    """Daftar kampanye (semua, atau yang berstatus tertentu /
    melibatkan agen tertentu)."""
    out = []
    for k in _muat()["kampanye"]:
        if status and k.get("status") != status:
            continue
        if agen and str(agen).strip().upper() not in k.get("agen", []):
            continue
        out.append(k)
    return sorted(out, key=lambda x: x.get("tanggal_mulai", ""))


def catat_hasil(hasil):
    """Catat hasil satu platform pada satu kampanye (angka dari
    insight/statistik platform — JANGAN dikarang). Hasil = dict:
    kampanye_id (wajib, harus ada), tanggal (wajib, YYYY-MM-DD),
    platform (wajib), like / view / follow (bilangan >= 0, default
    0). Kembalikan (ok_bool, pesan)."""
    h = dict(hasil or {})
    kid = (h.get("kampanye_id") or "").strip()
    data = _muat()
    if not any(k.get("id") == kid for k in data["kampanye"]):
        return False, f"DITOLAK: kampanye {kid!r} tidak ditemukan."
    tanggal = (h.get("tanggal") or "").strip()
    if not _tanggal_valid(tanggal):
        return False, "DITOLAK: tanggal wajib format YYYY-MM-DD."
    platform = (h.get("platform") or "").strip().lower()
    if platform not in PLATFORM_DIIZINKAN:
        return False, f"DITOLAK: platform {platform!r} tidak dikenal."
    angka = {}
    for kunci in ("like", "view", "follow"):
        try:
            nilai = int(h.get(kunci, 0))
        except (TypeError, ValueError):
            return False, (f"DITOLAK: {kunci} wajib bilangan bulat.")
        if nilai < 0:
            return False, f"DITOLAK: {kunci} tidak boleh negatif."
        angka[kunci] = nilai
    hid = "hsl-{:03d}".format(len(data["hasil"]) + 1)
    data["hasil"].append({
        "id": hid,
        "kampanye_id": kid,
        "tanggal": tanggal,
        "platform": platform,
        "like": angka["like"],
        "view": angka["view"],
        "follow": angka["follow"],
        "catatan": (h.get("catatan") or "").strip(),
        "tanggal_catat": _hari_ini(),
    })
    _catat_riwayat(data, kid, "catat_hasil",
                   f"{platform} {tanggal}: like {angka['like']}, "
                   f"view {angka['view']}, follow {angka['follow']}.")
    _simpan(data)
    return True, (f"Hasil {platform} {tanggal} dicatat untuk {kid}: "
                  f"like {angka['like']}, view {angka['view']}, "
                  f"follow {angka['follow']}.")


def laporan_kampanye(kampanye_id=None):
    """Laporan hasil kampanye: total like/view/follow per kampanye
    + rincian per platform. Tanpa id = semua kampanye. Bila id
    tidak ditemukan, kembalikan error. Kembalikan dict."""
    data = _muat()
    kampanye = data["kampanye"]
    if kampanye_id:
        kampanye = [k for k in kampanye if k.get("id") == kampanye_id]
        if not kampanye:
            return {"ok": False,
                    "error": f"kampanye {kampanye_id!r} tidak ditemukan."}
    per_kampanye = []
    total_like = total_view = total_follow = 0
    for k in kampanye:
        hasil = [r for r in data["hasil"]
                 if r.get("kampanye_id") == k.get("id")]
        per_platform = {}
        lk = vw = fl = 0
        for r in hasil:
            lk += r.get("like", 0)
            vw += r.get("view", 0)
            fl += r.get("follow", 0)
            p = per_platform.setdefault(
                r.get("platform", "?"),
                {"like": 0, "view": 0, "follow": 0, "catatan": 0})
            p["like"] += r.get("like", 0)
            p["view"] += r.get("view", 0)
            p["follow"] += r.get("follow", 0)
            p["catatan"] += 1
        total_like += lk
        total_view += vw
        total_follow += fl
        per_kampanye.append({
            "id": k.get("id"),
            "tema": k.get("tema"),
            "status": k.get("status"),
            "agen": k.get("agen"),
            "tanggal_mulai": k.get("tanggal_mulai"),
            "tanggal_selesai": k.get("tanggal_selesai"),
            "like": lk, "view": vw, "follow": fl,
            "jumlah_catatan_hasil": len(hasil),
            "per_platform": per_platform,
        })
    return {
        "ok": True,
        "kampanye_id": kampanye_id,
        "jumlah_kampanye": len(per_kampanye),
        "total_like": total_like,
        "total_view": total_view,
        "total_follow": total_follow,
        "per_kampanye": per_kampanye,
        "catatan": ("Angka hanya dari hasil yang dicatat (insight "
                    "platform). Kampanye tanpa catatan hasil = 0."),
    }


def info():
    """Metadata modul (untuk tes + tab Pusat Komando)."""
    return {
        "kode": KODE,
        "nama": NAMA,
        "divisi": DIVISI,
        "atasan": ATASAN,
        "job_desc": "Mesin pemasaran — koordinasi kampanye lintas 5 "
                    "agen pemasaran (tema, jadwal, hasil like/view/"
                    "follow per kampanye)",
        "status": "Aktif",
        "file_data": str(PEMASARAN_FILE),
        "agen_pemasaran": dict(AGEN_PEMASARAN),
        "platform_diizinkan": list(PLATFORM_DIIZINKAN),
        "status_diizinkan": list(STATUS_DIIZINKAN),
        "pasif": True,
        "catatan": ("DRAF/pencatatan saja. Tidak ada fungsi kirim/bayar/"
                    "publikasi/submit/upload/hapus. Jadwal adalah "
                    "RENCANA — penayangan tetap butuh persetujuan Cipta "
                    "atas konten persisnya."),
    }


def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    lap = laporan_kampanye()
    if lap["jumlah_kampanye"] == 0:
        return {"catatan": "Belum ada kampanye — data awal kosong. "
                           "Buat kampanye bila temanya sudah disusun.",
                "laporan": lap}
    return {"laporan": lap}
