"""BINTANG COMMAND CENTER — CRM Penjualan (crm.py).
Dibuat 21 Nov 2026 atas perintah Cipta ("Iya pasang itu buat penjualan kan").

CRM = database pelanggan/prospek toko untuk penjualan (A25 Sales Manager,
A26 Customer Service, di bawah A02). Satu sumber kebenaran untuk:
- daftar toko target + kontaknya (dari data yang SUDAH ADA saja),
- status penawaran tiap toko (target -> dihubungi -> ... -> deal/tolak),
- draf penawaran yang disetujui (DRAF saja — TIDAK PERNAH mengirim),
- jadwal follow-up (H+1/H+3/H+7, pola A25).

KEJUJURAN WAJIB — BACA DULU:
- Modul ini PASIF: dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri.
- Modul ini TIDAK PUNYA fungsi kirim / bayar / publikasi / submit / upload /
  hapus apa pun, sengaja. CRM hanya MENCATAT dan MENYIAPKAN DRAF.
  Penawaran dikirim oleh A25 (atau Cipta) HANYA setelah Cipta setuju isi
  persisnya, lewat saluran yang disetujui (IG/TikTok/Threads DM; Facebook
  DITAHAN). CRM tidak pernah menghubungi toko sendiri.
- Data pelanggan disimpan di data/crm.json — BUKAN di memori_bersama.db
  (ingatan bersama bukan database CRM). Modul ini sengaja TIDAK mengimpor
  memori_bersama.
- Jangan mengarang nomor telepon, username, atau status toko. Bila data
  tidak ada di sumber, tulis "belum cukup data".
- Harga yang dipakai adalah harga yang SUDAH DIPUTUSKAN (video 15 dtk
  Rp75.000 / 30 dtk Rp150.000 / 60 dtk Rp250.000; aplikasi Kasir Toko
  Rp499.000/Rp999.000/Rp1.999.000; website Rp1.500.000/Rp4.500.000/
  Rp9.900.000; poster Rp35.000). Jangan mengubah harga di sini.

SUMBER DATA (impor_dari_data):
- data/penjualan_toko.json — 15 pet shop Jaksel (status + draf disetujui).
- daftar-target-petshop-10.md — tabel 15 pet shop (cek silang nama).
- daftar-target-toko-umum.md — 15 toko umum (detail + draf DM TikTok).
- 6 draf A25 yang menunggu persetujuan (Balini, Michelle, Gentoo, Jangki,
  BB, Faunafella) = subset dari 15 pet shop, status "menunggu_persetujuan".
- data/leads.json (impor_leads, 21 Nov 2026): 27 lead A25 — status
  "baru" -> target, "dm-tiktok-terkirim" -> dihubungi; skor_minat,
  jadwal_follow_up, dan draf_follow_up ikut tersimpan.

STATUS CRM: target, dihubungi, menunggu_balasan, menunggu_persetujuan,
menawar, deal, tolak, dilewati.
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
CRM_FILE = DATA / "crm.json"
MD_DIR_DEFAULT = REPO.parent  # ~/workspace/your_files/oyen-podcast

KODE = "CRM"
NAMA = "CRM Penjualan"
DIVISI = "Penjualan"
ATASAN = "A02"
STATUS_DIIZINKAN = ["target", "dihubungi", "menunggu_balasan",
                    "menunggu_persetujuan", "menawar", "deal", "tolak",
                    "dilewati"]
BELUM = "belum cukup data"

# 6 draf A25 yang menunggu persetujuan Cipta (21 Nov 2026).
DRAF_MENUNGGU_PERSETUJUAN = {"toko-03", "toko-04", "toko-05", "toko-06",
                             "toko-08", "toko-09"}

# Produk utama per toko umum (urutan penawaran di daftar-target-toko-umum.md:
# kelontong -> kasir dulu; baju/mainan -> website dulu; roti/makan -> video).
PRODUK_UTAMA_UMUM = {
    "umum-01": "aplikasi", "umum-02": "website", "umum-03": "video",
    "umum-04": "video", "umum-05": "website", "umum-06": "video",
    "umum-07": "video", "umum-08": "website", "umum-09": "website",
    "umum-10": "aplikasi", "umum-11": "video", "umum-12": "video",
    "umum-13": "aplikasi", "umum-14": "aplikasi", "umum-15": "website",
}

KATEGORI_UMUM = {
    "umum-01": "resto + roti", "umum-02": "mainan robot vintage",
    "umum-03": "coffee shop", "umum-04": "bakery roti pisang",
    "umum-05": "fashion batik", "umum-06": "bakery + kafe",
    "umum-07": "bakery + resto", "umum-08": "fashion + kafe",
    "umum-09": "mainan koleksi", "umum-10": "padang + catering",
    "umum-11": "bakery", "umum-12": "bakery + snack box",
    "umum-13": "elektronik", "umum-14": "kelontong/sembako",
    "umum-15": "fashion kurasi",
}


def _hari_ini():
    return date.today().isoformat()


def _muat():
    """Baca data/crm.json. Bila belum ada/rusak, kembalikan struktur kosong."""
    try:
        with open(CRM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("kontak"), list):
            data.setdefault("riwayat", [])
            data.setdefault("log_impor", [])
            return data
    except Exception:
        pass
    return {"kontak": [], "riwayat": [], "log_impor": []}


def _simpan(data):
    """Tulis data/crm.json (indent 2, UTF-8)."""
    CRM_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CRM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def _catat_riwayat(data, kontak_id, aksi, status_baru="", catatan=""):
    data.setdefault("riwayat", []).append({
        "waktu": _hari_ini(),
        "id": kontak_id,
        "aksi": aksi,
        "status_baru": status_baru,
        "catatan": catatan,
    })


def _normal_nama(nama):
    return re.sub(r"\s+", " ", (nama or "").strip().lower())


def tambah_pelanggan(kontak):
    """Tambah satu kontak. Kontak = dict (nama wajib). Status tidak dikenal
    ditolak. Bila id sudah ada, ditolak (pakai ubah_status untuk mengubah).
    Kembalikan (ok_bool, pesan)."""
    kontak = dict(kontak or {})
    nama = (kontak.get("nama") or "").strip()
    if not nama:
        return False, "DITOLAK: nama wajib diisi."
    status = (kontak.get("status") or "target").strip()
    if status not in STATUS_DIIZINKAN:
        return False, f"DITOLAK: status {status!r} tidak dikenal."
    data = _muat()
    cid = (kontak.get("id") or "").strip()
    if not cid:
        cid = "crm-{:03d}".format(len(data["kontak"]) + 1)
    if any(k.get("id") == cid for k in data["kontak"]):
        return False, f"DITOLAK: id {cid!r} sudah ada."
    if any(_normal_nama(k.get("nama")) == _normal_nama(nama)
           for k in data["kontak"]):
        return False, f"DITOLAK: nama {nama!r} sudah ada di CRM."
    baru = {
        "id": cid,
        "nama": nama,
        "jenis": kontak.get("jenis") or "lainnya",
        "kategori": kontak.get("kategori") or BELUM,
        "platform": kontak.get("platform") or BELUM,
        "kontak": kontak.get("kontak") or BELUM,
        "medsos": kontak.get("medsos") or BELUM,
        "alamat": kontak.get("alamat") or BELUM,
        "kecamatan": kontak.get("kecamatan") or BELUM,
        "observasi": kontak.get("observasi") or BELUM,
        "produk_ditawarkan": kontak.get("produk_ditawarkan") or BELUM,
        "produk_utama": kontak.get("produk_utama") or "video",
        "status": status,
        "tanggal_dihubungi": kontak.get("tanggal_dihubungi") or "",
        "tanggal_followup": kontak.get("tanggal_followup") or "",
        "tanggal_status": _hari_ini(),
        "followup_ke": int(kontak.get("followup_ke") or 0),
        "kanal": kontak.get("kanal") or "",
        "draf": kontak.get("draf") or "",
        "catatan": kontak.get("catatan") or "",
        "sumber": kontak.get("sumber") or "tambah manual",
        "sumber_id": kontak.get("sumber_id") or "",
        "terverifikasi": bool(kontak.get("terverifikasi")),
    }
    data["kontak"].append(baru)
    _catat_riwayat(data, cid, "tambah", status, "Kontak baru.")
    _simpan(data)
    return True, f"Kontak {nama!r} ditambah sebagai {cid}."


def ubah_status(kontak_id, status, catatan=""):
    """Ubah status satu kontak. Status tidak dikenal / id tidak ada ditolak.
    Bila status baru 'dihubungi' dan belum ada tanggal_dihubungi, isi hari
    ini + tanggal_followup H+1. Kembalikan (ok_bool, pesan)."""
    status = (status or "").strip()
    if status not in STATUS_DIIZINKAN:
        return False, f"DITOLAK: status {status!r} tidak dikenal."
    data = _muat()
    for k in data["kontak"]:
        if k.get("id") == kontak_id:
            lama = k.get("status", "")
            k["status"] = status
            k["tanggal_status"] = _hari_ini()
            if catatan:
                k["catatan"] = ((k.get("catatan") or "") + " | " + catatan
                                ).strip(" |") if k.get("catatan") else catatan
            if status == "dihubungi" and not k.get("tanggal_dihubungi"):
                k["tanggal_dihubungi"] = _hari_ini()
                k["tanggal_followup"] = (
                    date.today() + timedelta(days=1)).isoformat()
            _catat_riwayat(data, kontak_id, "ubah_status", status,
                           f"{lama} -> {status}. {catatan}".strip())
            _simpan(data)
            return True, (f"Status {k.get('nama')} diubah: "
                          f"{lama} -> {status}.")
    return False, f"DITOLAK: id {kontak_id!r} tidak ditemukan di CRM."


def daftar_pelanggan(status=None):
    """Daftar kontak (semua, atau yang berstatus tertentu saja)."""
    data = _muat()
    if status:
        return [k for k in data["kontak"] if k.get("status") == status]
    return list(data["kontak"])


def cari_pelanggan(kata_kunci):
    """Cari kontak berdasarkan nama/kontak/medsos/alamat (substring,
    tidak peduli huruf besar-kecil)."""
    cari = (kata_kunci or "").strip().lower()
    if not cari:
        return []
    out = []
    for k in _muat()["kontak"]:
        teks = " ".join(str(k.get(f, "") or "") for f in
                        ("nama", "kontak", "medsos", "alamat", "kategori",
                         "kecamatan", "jenis")).lower()
        if cari in teks:
            out.append(k)
    return out


def riwayat(kontak_id):
    """Riwayat perubahan satu kontak (urut kronologis)."""
    return [r for r in _muat().get("riwayat", [])
            if r.get("id") == kontak_id]


def ringkasan(tanggal=None):
    """Total per status + daftar yang perlu follow-up hari ini
    (tanggal_followup == hari ini, status dihubungi/menunggu_balasan)
    + daftar yang menunggu persetujuan Cipta."""
    hari = tanggal or _hari_ini()
    data = _muat()
    per_status = {}
    for k in data["kontak"]:
        per_status[k.get("status", "?")] = \
            per_status.get(k.get("status", "?"), 0) + 1
    perlu = [k for k in data["kontak"]
             if k.get("tanggal_followup") == hari
             and k.get("status") in ("dihubungi", "menunggu_balasan")]
    menunggu = [k for k in data["kontak"]
                if k.get("status") == "menunggu_persetujuan"]
    return {
        "tanggal": hari,
        "total_kontak": len(data["kontak"]),
        "per_status": per_status,
        "perlu_followup_hari_ini": [
            {"id": k["id"], "nama": k["nama"], "status": k["status"],
             "kontak": k.get("kontak", ""), "kanal": k.get("kanal", "")}
            for k in perlu],
        "menunggu_persetujuan": [
            {"id": k["id"], "nama": k["nama"]} for k in menunggu],
    }


# ----------------------------------------------------------------------
# Impor dari data yang sudah ada
# ----------------------------------------------------------------------

def _ambil_telepon(teks):
    """Ambil nomor telepon/HP pertama dari teks. Bila tidak ada, kembalikan
    'belum cukup data'. Nomor landline (021) ikut diambil bila itu
    satu-satunya yang ada."""
    teks = teks or ""
    m = re.search(r"(\(?0\d{2,3}\)?[\s\-]?\d[\d\s\-]{5,}\d)", teks)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\+62[\s\-]?\d[\d\s\-]{7,})", teks)
    if m:
        return m.group(1).strip()
    return BELUM


def _parse_tabel_petshop_md(teks):
    """Parse tabel ringkasan daftar-target-petshop-10.md -> list nama toko.
    Dipakai sebagai cek silang (harus 15 nama, cocok dengan JSON)."""
    nama = []
    for baris in (teks or "").splitlines():
        m = re.match(r"\|\s*\d+\s*\|\s*([^|]+?)\s*\|", baris)
        if m and "Nama toko" not in m.group(1):
            nama.append(m.group(1).strip())
    return nama


def _parse_umum_md(teks):
    """Parse daftar-target-toko-umum.md:
    - Bagian B: blok '### N. Nama — STATUS' -> detail toko.
    - Bagian C: blok '### Draf N — Nama (...)' -> teks draf.
    Kembalikan list 15 dict (id umum-01..15). Bila parsing gagal untuk
    satu toko, toko itu TIDAK dibuat (jangan dikarang) — dilaporkan."""
    teks = teks or ""
    blok = re.split(r"^### ", teks, flags=re.M)
    detail = {}
    draf = {}
    for b in blok:
        if not b.strip():
            continue
        kepala, _, isi = b.partition("\n")
        kepala = kepala.strip()
        m_draf = re.match(r"Draf\s+(\d+)\s*[—\-]\s*(.+?)\s*(?:\(.*\))?$", kepala)
        if m_draf:
            nomor = int(m_draf.group(1))
            teks_draf = " ".join(
                ln[2:].strip() for ln in isi.splitlines()
                if ln.strip().startswith("> ")).strip()
            if teks_draf:
                draf[nomor] = teks_draf
            continue
        m_det = re.match(r"(\d+)\.\s*(.+?)\s*[—\-]\s*(.+)$", kepala)
        if not m_det:
            continue
        nomor = int(m_det.group(1))
        nama = m_det.group(2).strip()
        status_md = m_det.group(3).strip()
        field = {}
        for ln in isi.splitlines():
            m_f = re.match(r"-\s*\*\*(.+?):\*\*\s*(.*)$", ln.strip())
            if m_f:
                field[m_f.group(1).strip()] = m_f.group(2).strip()
        detail[nomor] = {"nama": nama, "field": field}
    out = []
    for nomor in sorted(detail):
        d = detail[nomor]
        f = d["field"]
        telp = f.get("Telepon/WA", "")
        tiktok = f.get("TikTok", "")
        ig = f.get("Instagram", "")
        medsos = []
        if ig and "belum terkonfirmasi" not in ig and "TIDAK ADA" not in ig:
            m_ig = re.search(r"@[\w\.]+", ig)
            if m_ig:
                medsos.append("IG " + m_ig.group(0))
        if tiktok and "belum terkonfirmasi" not in tiktok \
                and "TIDAK ADA" not in tiktok:
            m_tt = re.search(r"@[\w\.]+", tiktok)
            if m_tt:
                medsos.append("TikTok " + m_tt.group(0))
        if "TikTok" in " ".join(medsos):
            platform = "tiktok"
        elif medsos:
            platform = "instagram"
        else:
            platform = BELUM
        kontak = _ambil_telepon(telp)
        catatan = ""
        if "tidak ditemukan" in telp:
            catatan = "Nomor telepon tidak ditemukan di sumber."
        if nomor == 12:
            catatan = ("Nomor WA di bio IG berbeda dengan nomor GoFood — "
                       "verifikasi dulu mana yang benar sebelum kirim.")
        out.append({
            "id": "umum-{:02d}".format(nomor),
            "nama": d["nama"],
            "jenis": "toko umum",
            "kategori": KATEGORI_UMUM.get("umum-{:02d}".format(nomor), BELUM),
            "platform": platform,
            "kontak": kontak,
            "medsos": " · ".join(medsos) if medsos else BELUM,
            "alamat": f.get("Alamat", BELUM),
            "kecamatan": "Jakarta Selatan",
            "observasi": f.get("Observasi", BELUM),
            "produk_ditawarkan": "video, website, aplikasi kasir",
            "produk_utama": PRODUK_UTAMA_UMUM.get(
                "umum-{:02d}".format(nomor), "video"),
            "status": "target",
            "tanggal_dihubungi": "",
            "tanggal_followup": "",
            "tanggal_status": _hari_ini(),
            "followup_ke": 0,
            "kanal": "",
            "draf": draf.get(nomor, ""),
            "catatan": catatan,
            "sumber": "daftar-target-toko-umum.md",
            "sumber_id": "umum-{:02d}".format(nomor),
            "terverifikasi": status_md != "PERLU DICEK",
        })
    return out


def _petshop_ke_kontak(t):
    """Satu entri penjualan_toko.json -> dict kontak CRM."""
    tid = t.get("id", "")
    status_json = (t.get("status") or "").strip()
    if status_json == "terkirim":
        status = "dihubungi"
    elif status_json == "dilewati":
        status = "dilewati"
    elif tid in DRAF_MENUNGGU_PERSETUJUAN:
        status = "menunggu_persetujuan"
    elif tid in ("toko-07", "toko-15"):
        # Zoom + Efxi: laporan-penawaran-dm.md — medsos tidak aktif.
        status = "dilewati"
    else:
        status = "target"
    tanggal_hub = t.get("tanggal_status", "") if status == "dihubungi" else ""
    tanggal_fu = ""
    if tanggal_hub:
        try:
            y, m, d = map(int, tanggal_hub.split("-"))
            tanggal_fu = (date(y, m, d) + timedelta(days=1)).isoformat()
        except Exception:
            tanggal_fu = ""
    catatan = t.get("catatan", "") or ""
    if tid == "toko-07":
        catatan += (" | DILEWATI — medsos tidak aktif "
                    "(IG terakhir 31 Agu 2025).")
    if tid == "toko-15":
        catatan += (" | DILEWATI — medsos tidak aktif "
                    "(IG terakhir 9 Nov 2018).")
    if tid == "toko-11":
        catatan += " | Dilewati: toko di Pemalang, bukan Jaksel."
    return {
        "id": tid,
        "nama": t.get("nama", BELUM),
        "jenis": "petshop",
        "kategori": "pet shop",
        "platform": ("tiktok" if "TikTok" in (t.get("kanal") or "")
                     else ("instagram" if (t.get("medsos") or "")
                           .startswith("IG") else BELUM)),
        "kontak": t.get("kontak_hp") or BELUM,
        "medsos": t.get("medsos") or BELUM,
        "alamat": t.get("alamat") or BELUM,
        "kecamatan": t.get("kecamatan") or BELUM,
        "observasi": t.get("observasi") or BELUM,
        "produk_ditawarkan": "video",
        "produk_utama": "video",
        "status": status,
        "tanggal_dihubungi": tanggal_hub,
        "tanggal_followup": tanggal_fu,
        "tanggal_status": t.get("tanggal_status", "") or _hari_ini(),
        "followup_ke": int(t.get("followup_ke") or 0),
        "kanal": t.get("kanal") or "",
        "draf": t.get("draf") or "",
        "catatan": catatan.strip(" |"),
        "sumber": "penjualan_toko.json",
        "sumber_id": tid,
        "terverifikasi": True,
    }


def impor_dari_data(path_json=None, md_dir=None):
    """Impor data penjualan yang sudah ada ke CRM. Idempotent: kontak yang
    sudah ada (berdasarkan id) TIDAK diduplikasi dan statusnya TIDAK
    ditimpa — hanya kontak baru yang ditambah. Kembalikan laporan impor."""
    laporan = {"ditambah": 0, "sudah_ada": 0, "peringatan": [],
               "total": 0, "per_status": {}}
    data = _muat()
    ada = {k.get("id") for k in data["kontak"]}

    def _tambah(kontak):
        if kontak["id"] in ada:
            laporan["sudah_ada"] += 1
            return
        data["kontak"].append(kontak)
        ada.add(kontak["id"])
        laporan["ditambah"] += 1
        _catat_riwayat(data, kontak["id"], "impor", kontak["status"],
                       "Impor dari " + kontak.get("sumber", ""))

    # 1) Pet shop dari penjualan_toko.json (sumber kebenaran status).
    p_json = Path(path_json) if path_json else DATA / "penjualan_toko.json"
    try:
        with open(p_json, "r", encoding="utf-8") as f:
            isi = json.load(f)
        toko = isi.get("toko", []) if isinstance(isi, dict) else isi
        for t in toko:
            _tambah(_petshop_ke_kontak(t))
        laporan["petshop_json"] = len(toko)
    except Exception as e:  # noqa: BLE001
        laporan["peringatan"].append(
            f"penjualan_toko.json gagal dibaca: {e}")

    # 2) Cek silang tabel daftar-target-petshop-10.md (harus 15 nama).
    md = Path(md_dir) if md_dir else MD_DIR_DEFAULT
    try:
        nama_md = _parse_tabel_petshop_md(
            (md / "daftar-target-petshop-10.md").read_text(encoding="utf-8"))
        laporan["petshop_md_nama"] = len(nama_md)
        nama_json = {_normal_nama(k.get("nama")) for k in data["kontak"]
                     if k.get("jenis") == "petshop"}
        hilang = [n for n in nama_md if _normal_nama(n) not in nama_json]
        if hilang:
            laporan["peringatan"].append(
                "Nama di md petshop tapi tidak di JSON: " + ", ".join(hilang))
    except Exception as e:  # noqa: BLE001
        laporan["peringatan"].append(
            f"daftar-target-petshop-10.md gagal dibaca: {e}")

    # 3) Toko umum dari daftar-target-toko-umum.md (detail + draf).
    try:
        umum = _parse_umum_md(
            (md / "daftar-target-toko-umum.md").read_text(encoding="utf-8"))
        laporan["toko_umum"] = len(umum)
        for u in umum:
            _tambah(u)
        if len(umum) != 15:
            laporan["peringatan"].append(
                f"Toko umum ter-parse {len(umum)}, seharusnya 15 — "
                "cek file sumber.")
    except Exception as e:  # noqa: BLE001
        laporan["peringatan"].append(
            f"daftar-target-toko-umum.md gagal dibaca: {e}")

    _simpan(data)
    data["log_impor"].append({"waktu": _hari_ini(), **laporan})
    _simpan(data)
    laporan["total"] = len(data["kontak"])
    laporan["per_status"] = ringkasan()["per_status"]
    return laporan


# ----------------------------------------------------------------------
# Impor leads.json (27 lead A25)
# ----------------------------------------------------------------------

STATUS_LEAD_KE_CRM = {"baru": "target",
                      "dm-tiktok-terkirim": "dihubungi"}

_KATA_STOP_NAMA = {"petshop", "pet", "shop", "and", "care", "clinic",
                   "store", "official", "the", "dokter", "hewan"}

_BULAN = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6,
          "jul": 7, "agu": 8, "sep": 9, "okt": 10, "nov": 11, "des": 12}


def _token_nama(nama):
    """Token nama toko setelah huruf kecil + buang tanda baca + buang kata
    stop (petshop/pet/shop/dll.) — untuk pencocokan nama yang ejaannya
    berbeda (mis. 'Jangki Petshop' vs 'Jangki Petshop Cilandak')."""
    teks = re.sub(r"[^a-z0-9 ]", " ", (nama or "").lower())
    return {t for t in teks.split() if t not in _KATA_STOP_NAMA}


def _nama_sama(a, b):
    """Dua nama dianggap toko yang sama bila tokennya sama persis, atau
    token salah satunya himpunan bagian dari yang lain (nama yang satu
    lebih panjang, mis. tambahan 'Cilandak'). Bila kedua nama habis
    jadi kata stop, bandingkan nama mentahnya."""
    ta, tb = _token_nama(a), _token_nama(b)
    if not ta or not tb:
        return _normal_nama(a) == _normal_nama(b)
    return ta == tb or ta <= tb or tb <= ta


def _medsos_dari_kontak(teks):
    """Ambil handle medsos dari string kontak lead: IG @x, TikTok @x,
    Chat Shopee (x)."""
    teks = teks or ""
    out = []
    for kanal, pola in (("IG", r"IG\s+(@[\w\.]+)"),
                        ("TikTok", r"TikTok\s+(@[\w\.]+)"),
                        ("Shopee", r"Chat Shopee\s*\(([^)]+)\)")):
        m = re.search(pola, teks)
        if m:
            out.append(f"{kanal} {m.group(1)}")
    return " · ".join(out) if out else BELUM


def _platform_dari_kontak(teks):
    """Kanal utama dari string kontak lead (tiktok/instagram/shopee)."""
    teks = teks or ""
    if "TikTok" in teks:
        return "tiktok"
    if re.search(r"IG\s+@", teks):
        return "instagram"
    if "Shopee" in teks:
        return "shopee"
    return BELUM


def _tanggal_terkirim(catatan):
    """Ambil tanggal 'TERKIRIM 21 Nov 2026' dari catatan lead -> (ISO,
    ISO H+1). Bila tidak ada, kembalikan ('', '')."""
    m = re.search(r"TERKIRIM\s+(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})",
                  catatan or "")
    if not m:
        return "", ""
    bulan = _BULAN.get(m.group(2).lower())
    if not bulan:
        return "", ""
    try:
        tgl = date(int(m.group(3)), bulan, int(m.group(1)))
    except ValueError:
        return "", ""
    return tgl.isoformat(), (tgl + timedelta(days=1)).isoformat()


def _lead_ke_kontak(l):
    """Satu entri leads.json -> dict kontak CRM. Status lead yang tidak
    dikenal -> None (tidak diimpor, dilaporkan sebagai peringatan).
    Tanggal dihubungi diambil dari catatan lead sendiri ('TERKIRIM ...'),
    bukan dikarang."""
    lid = (l.get("id") or "").strip()
    status_lead = (l.get("status") or "").strip()
    status = STATUS_LEAD_KE_CRM.get(status_lead)
    if not status:
        return None
    jenis_lead = (l.get("jenis") or "").strip().lower()
    jenis = {"pet shop": "petshop", "toko online": "toko online",
             "klinik hewan": "klinik hewan"}.get(jenis_lead,
                                                 jenis_lead or "lainnya")
    kontak_teks = l.get("kontak") or ""
    catatan = (l.get("catatan") or "").strip()
    sumber = (l.get("sumber") or "").strip()
    if sumber:
        catatan = (catatan + " | Sumber: " + sumber).strip(" |")
    tanggal_hub = ""
    tanggal_fu = ""
    kanal = ""
    if status == "dihubungi":
        tanggal_hub, tanggal_fu = _tanggal_terkirim(catatan)
        m = re.search(r"dari\s+(@[\w\.]+)", catatan or "")
        kanal = ("TikTok DM " + m.group(1)) if m else "TikTok DM"
    return {
        "id": lid,
        "nama": (l.get("nama") or BELUM).strip(),
        "jenis": jenis,
        "kategori": jenis_lead or BELUM,
        "platform": _platform_dari_kontak(kontak_teks),
        "kontak": _ambil_telepon(kontak_teks),
        "medsos": _medsos_dari_kontak(kontak_teks),
        "alamat": (l.get("alamat") or BELUM).strip(),
        "kecamatan": BELUM,
        "observasi": BELUM,
        "produk_ditawarkan": "video",
        "produk_utama": "video",
        "status": status,
        "tanggal_dihubungi": tanggal_hub,
        "tanggal_followup": tanggal_fu,
        "tanggal_status": _hari_ini(),
        "followup_ke": 0,
        "kanal": kanal,
        "draf": "",
        "draf_followup": (l.get("draf_follow_up") or "").strip(),
        "jadwal_followup": dict(l.get("jadwal_follow_up") or {}),
        "skor_minat": l.get("skor_minat"),
        "catatan": catatan,
        "sumber": "leads.json",
        "sumber_id": lid,
        "terverifikasi": bool(l.get("terverifikasi")),
    }


def impor_leads(path_json=None):
    """Impor data/leads.json (27 lead A25) ke CRM. Idempotent: lead yang
    namanya sudah ada di CRM (pencocokan nama ternormalisasi — ejaan
    'Petshop'/'Pet Shop' dan tambahan kata seperti 'Cilandak' diabaikan)
    TIDAK diduplikasi. Hanya lead baru yang ditambah. Kembalikan laporan
    impor."""
    laporan = {"ditambah": 0, "sudah_ada": 0, "duplikat": [],
               "peringatan": [], "total": 0, "per_status": {}}
    p_json = Path(path_json) if path_json else DATA / "leads.json"
    try:
        with open(p_json, "r", encoding="utf-8") as f:
            isi = json.load(f)
        leads = isi.get("leads", []) if isinstance(isi, dict) else isi
    except Exception as e:  # noqa: BLE001
        laporan["peringatan"].append(f"leads.json gagal dibaca: {e}")
        return laporan
    laporan["leads_file"] = len(leads)
    data = _muat()
    for l in leads:
        kontak = _lead_ke_kontak(l)
        if kontak is None:
            laporan["peringatan"].append(
                f"Lead {l.get('id')} ({l.get('nama')}) status "
                f"{l.get('status')!r} tidak dikenal — dilewati.")
            continue
        cocok = next((k for k in data["kontak"]
                      if _nama_sama(k.get("nama"), kontak["nama"])), None)
        if cocok is not None:
            laporan["sudah_ada"] += 1
            laporan["duplikat"].append({
                "lead_id": kontak["id"], "nama": kontak["nama"],
                "cocok_dengan": f"{cocok.get('id')} "
                                f"({cocok.get('nama')})"})
            continue
        data["kontak"].append(kontak)
        laporan["ditambah"] += 1
        _catat_riwayat(data, kontak["id"], "impor", kontak["status"],
                       "Impor dari leads.json")
    _simpan(data)
    data["log_impor"].append({"waktu": _hari_ini(), **laporan})
    _simpan(data)
    laporan["total"] = len(data["kontak"])
    laporan["per_status"] = ringkasan()["per_status"]
    return laporan


# ----------------------------------------------------------------------
# Draf penawaran (DRAF saja — tidak pernah mengirim)
# ----------------------------------------------------------------------

def draf_penawaran(kontak_id, produk=None):
    """Buat draf penawaran untuk satu kontak CRM.
    - Bila kontak sudah punya draf tersimpan (dari file sumber yang
      disetujui), pakai draf itu apa adanya.
    - Bila belum ada, bangun dari template A25 yang disetujui
      (b25.buat_draf_penawaran -> a04.draf_personal; fallback template
      lokal yang sama polanya).
    Draf dicatat di CRM. DRAF saja — kirim hanya setelah Cipta setuju
    isi persisnya."""
    data = _muat()
    kontak = next((k for k in data["kontak"] if k.get("id") == kontak_id),
                  None)
    if kontak is None:
        return {"ok": False, "id": kontak_id,
                "error": "Kontak tidak ditemukan di CRM."}
    teks = (kontak.get("draf") or "").strip()
    sumber = "draf tersimpan (dari file sumber yang disetujui)"
    if not teks:
        produk_pakai = produk or kontak.get("produk_utama") or "video"
        try:
            import b25_sales_manager as B25
            hasil = B25.buat_draf_penawaran(
                kontak.get("nama", ""), produk_pakai,
                kontak.get("observasi", "") or "")
            teks = (hasil or {}).get("teks", "") or ""
            sumber = "template A25 disetujui (" + str(
                (hasil or {}).get("sumber", "b25")) + ")"
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "id": kontak_id,
                    "error": f"Template A25 gagal dipakai: {e}"}
        if not teks:
            return {"ok": False, "id": kontak_id,
                    "error": "belum cukup data — draf tidak bisa dibuat."}
        kontak["draf"] = teks
        _catat_riwayat(data, kontak_id, "draf_dibuat",
                       kontak.get("status", ""),
                       "Draf dibuat dari " + sumber)
        _simpan(data)
    return {
        "ok": True,
        "id": kontak_id,
        "nama": kontak.get("nama"),
        "produk": produk or kontak.get("produk_utama") or "video",
        "teks": teks,
        "sumber": sumber,
        "catatan": ("DRAF — kirim hanya setelah Cipta setuju isi "
                    "persisnya. Saluran: IG/TikTok/Threads DM; "
                    "Facebook DITAHAN."),
    }


def info():
    """Metadata modul (untuk tes + tab Pusat Komando)."""
    return {
        "kode": KODE,
        "nama": NAMA,
        "divisi": DIVISI,
        "atasan": ATASAN,
        "job_desc": "CRM penjualan — database pelanggan/prospek toko, "
                    "status penawaran, draf, dan jadwal follow-up",
        "status": "Aktif",
        "file_data": str(CRM_FILE),
        "status_diizinkan": list(STATUS_DIIZINKAN),
        "pasif": True,
        "catatan": ("DRAF-only. Tidak ada fungsi kirim/bayar/publikasi/"
                    "submit/upload/hapus."),
    }


def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    r = ringkasan()
    if r["total_kontak"] == 0:
        return {"catatan": "CRM masih kosong — jalankan impor_dari_data().",
                "ringkasan": r}
    draf = draf_penawaran("toko-01")
    return {"ringkasan": r, "contoh_draf": draf}
