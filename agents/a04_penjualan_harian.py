# ======================================================================
# PUSAT KOMANDO — Agent 4 Penjualan Harian.
# Dibuat 20 Nov 2026 atas perintah Cipta ("Exsekusi / Buatkan") untuk
# mengisi slot Agent 4 yang dulu dihapus (upload tugas harian).
# Total agent menjadi 13 (slot 1-13 penuh) + Muse = 14.
#
# Tugas: penjualan harian ke toko-toko (alur kerja 4 Cipta) — cari
# minimal 15 toko/hari (nomor HP dari Google Maps / listing tempat),
# verifikasi nomor, buat draf penawaran PERSONAL per toko dari katalog
# baru, catat hasil + follow-up di data/penjualan_toko.json.
#
# ATURAN KERAS (SOP Kerja Sama Agent AI v1.3):
# - Semua output adalah DRAF untuk persetujuan Cipta.
# - Agent TIDAK PERNAH mengirim pesan (WA / DM / email) — Cipta yang
#   mengirim sendiri dari WA-nya setelah menyetujui draf persisnya.
#   Modul ini TIDAK PUNYA fungsi kirim apa pun, sengaja.
# - Dilarang mengarang harga, tautan, testimoni, atau janji views /
#   viral / penjualan naik. Bila data kurang, tulis "belum cukup data".
# - Jangan hubungi toko yang sudah ada di log (cek duplikat dulu).
# - DIBANTU AGENT 2 UNTUK MEMASARKAN (perintah Cipta 20 Nov 2026):
#   draf penawaran memakai generator promosi Agent 2 (a02_penjualan —
#   wa_outreach / wa_followup / dm_ig / email / caption); modul ini
#   TIDAK membuat generator promosi baru. Alur data: toko terverifikasi
#   Agent 4 masuk sebagai lead ke Agent 2 (leads.json); lead Agent 2
#   berstatus "baru" bisa diambil Agent 4 untuk penawaran harian.
# - GRATIS: model Google Gemini free tier (google-genai). API key HANYA
#   dari environment variable GEMINI_API_KEY — tidak pernah ditulis di
#   file. Tanpa key, semua fitur tetap jalan dalam mode template.
# ======================================================================
import json
import os
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"  # folder data bersama
DATA_FILE = BASE / "penjualan_toko.json"
MODEL = "gemini-2.0-flash"

TARGET_HARIAN = 15  # toko per hari (perintah Cipta 20 Nov 2026)

# ---------------------------------------------------------------- knowledge base
KB = """DATA RESMI PODCAST MEONG (satu-satunya sumber kebenaran — jangan mengarang di luar ini):
- Podcast Meong: podcast komedi kucing Oyen (oren) & Momo (abu-abu). Website: https://podcastmeong.github.io/ (bagian #jasa).
- JASA VIDEO PROMO (KikiWorks): video vertikal 9:16 (TikTok, Reels, WhatsApp).
  Sederhana 15 detik Rp75.000 / Standar 30 detik Rp150.000 / Storytelling 60 detik Rp250.000.
  Termasuk naskah singkat + 1x revisi kecil. DP minimal 50% sebelum produksi. Maks 7 hari kalender.
- APLIKASI (satu file HTML, data per perangkat, bisa offline): Beli sekali Basic Rp499.000 / Professional Rp999.000 / Business Rp1.999.000; langganan Rp49.000 / Rp99.000 / Rp199.000 per bulan; APK Android +Rp400.000; garansi bug 30 / 60 / 90 hari.
- JASA WEBSITE: Basic Rp1.500.000 / Professional Rp4.500.000 / Business Rp9.900.000 (domain & hosting tidak termasuk).
- JASA SISTEM (custom): Basic Rp4.900.000 / Professional Rp9.900.000, produksi 7 hari.
- JASA POSTER: Rp35.000 per poster (file digital). JASA FOTO & DESAIN: Basic Rp50.000 / Professional Rp150.000.
- Video contoh jasa: https://www.youtube.com/shorts/ONkM6dQQHxg
- ATURAN JUJUR: jangan janjikan views, viral, atau penjualan naik. Yang dijual hanya jasa/produk + isi paketnya. Tidak ada klaim penghasilan palsu. Target realistis: 1-3 pelanggan dari 10-15 penawaran pertama."""

WEBSITE = "https://podcastmeong.github.io/"
CONTOH_VIDEO = "https://www.youtube.com/shorts/ONkM6dQQHxg"

VERIFIKASI = ["wa_terkonfirmasi", "kemungkinan_wa", "landline_saja", "perlu_dicek"]
STATUS_TOKO = ["draf", "disetujui", "dikirim", "dibalas", "order", "tolak",
               "tidak_merespons"]
PRODUK_TAWARAN = ["video", "aplikasi", "website", "poster", "paket_lengkap"]

KATA_TERLARANG = ["viral", "views naik", "penjualan naik", "pasti laku",
                  "dijamin", "testimoni"]


# ---------------------------------------------------------------- Gemini (opsional)
def gemini_client():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception:
        return None


def gemini_ask(prompt: str):
    """Kembalikan teks jawaban Gemini, atau None bila key tidak ada / gagal."""
    client = gemini_client()
    if client is None:
        return None
    try:
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        text = (getattr(resp, "text", "") or "").strip()
        return text or None
    except Exception:
        return None


def mode_ai():
    return "gemini" if os.environ.get("GEMINI_API_KEY", "").strip() else "template"


# ---------------------------------------------------------------- Agent 2 (dibantu memasarkan)
def _a02():
    """Muat modul Agent 2 (generator promosi + leads) bila tersedia.

    Agent 4 memakai generator promosi Agent 2 — bukan membuat generator
    baru. Bila a02 tidak bisa dimuat (mis. FastAPI belum terpasang),
    kembalikan None dan pemanggil memakai template darurat lokal.
    """
    try:
        import a02_penjualan as a02
        return a02
    except Exception:
        return None


def _sisip_katalog(draf):
    """Sisipkan tautan katalog website sebelum penutup 'Terima kasih'."""
    penutup = "Terima kasih 🙏"
    katalog = "Katalog jasa: {} (bagian #jasa). ".format(WEBSITE)
    if WEBSITE in draf:
        return draf
    if penutup in draf:
        return draf.replace(penutup, katalog + penutup, 1)
    return draf.rstrip() + " " + katalog


# ---------------------------------------------------------------- data (JSON lokal)
def _data_file(data_file=None):
    return Path(data_file) if data_file else DATA_FILE


def load_toko(data_file=None):
    f = _data_file(data_file)
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text(encoding="utf-8")).get("toko", [])
    except Exception:
        return []


def save_toko(daftar, data_file=None):
    f = _data_file(data_file)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"toko": daftar}, ensure_ascii=False, indent=1),
                 encoding="utf-8")


def _normal(nama):
    s = unicodedata.normalize("NFKD", (nama or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def _normal_hp(hp):
    return re.sub(r"\D", "", hp or "")[-10:] if hp else ""


def sudah_ada(nama, hp="", daftar=None, data_file=None):
    """True bila toko (nama sama ATAU nomor HP sama) sudah ada di log."""
    daftar = load_toko(data_file) if daftar is None else daftar
    n = _normal(nama)
    h = _normal_hp(hp)
    for t in daftar:
        if n and _normal(t.get("nama", "")) == n:
            return True
        if h and _normal_hp(t.get("kontak_hp", "")) == h:
            return True
    return False


def tambah_toko(nama, jenis="pet shop", alamat="", kecamatan="", kontak_hp="",
                kontak_sumber="Google Maps", medsos="", verifikasi="perlu_dicek",
                observasi="", produk_tawaran="video", data_file=None):
    """Tambah toko baru. Tolak bila duplikat (nama / nomor sudah ada)."""
    if not (nama or "").strip():
        return None, "Nama toko wajib diisi."
    if verifikasi not in VERIFIKASI:
        return None, "Status verifikasi tidak dikenal: {}".format(verifikasi)
    if produk_tawaran not in PRODUK_TAWARAN:
        return None, "Produk tawaran tidak dikenal: {}".format(produk_tawaran)
    daftar = load_toko(data_file)
    if sudah_ada(nama, kontak_hp, daftar):
        return None, "Sudah ada di log — jangan hubungi ganda: {}".format(nama.strip())
    nomor = max([int(t["id"].split("-")[1]) for t in daftar
                 if re.match(r"toko-\d+$", t.get("id", ""))], default=0) + 1
    toko = {
        "id": "toko-%02d" % nomor,
        "nama": nama.strip(),
        "jenis": (jenis or "pet shop").strip(),
        "alamat": (alamat or "").strip(),
        "kecamatan": (kecamatan or "").strip(),
        "kontak_hp": (kontak_hp or "").strip(),
        "kontak_sumber": (kontak_sumber or "Google Maps").strip(),
        "medsos": (medsos or "").strip(),
        "verifikasi": verifikasi,
        "tanggal_ditemukan": str(date.today()),
        "observasi": (observasi or "").strip(),
        "produk_tawaran": produk_tawaran,
        "draf": "",
        "status": "draf",
        "tanggal_status": str(date.today()),
        "followup_ke": 0,
        "catatan": "",
    }
    daftar.append(toko)
    save_toko(daftar, data_file)
    return toko, "Ditambahkan: {} ({})".format(toko["id"], toko["nama"])


def ubah_status(toko_id, status, catatan="", data_file=None):
    if status not in STATUS_TOKO:
        return None, "Status tidak dikenal: {}".format(status)
    daftar = load_toko(data_file)
    for t in daftar:
        if t["id"] == toko_id:
            t["status"] = status
            t["tanggal_status"] = str(date.today())
            if catatan:
                t["catatan"] = catatan.strip()
            save_toko(daftar, data_file)
            return t, "Status {} menjadi '{}'.".format(toko_id, status)
    return None, "Toko tidak ditemukan: {}".format(toko_id)


def simpan_draf(toko_id, draf, data_file=None):
    daftar = load_toko(data_file)
    for t in daftar:
        if t["id"] == toko_id:
            t["draf"] = (draf or "").strip()
            save_toko(daftar, data_file)
            return t, "Draf disimpan untuk {}.".format(toko_id)
    return None, "Toko tidak ditemukan: {}".format(toko_id)


# ---------------------------------------------------------------- draf penawaran
def _harga_produk(produk):
    if produk == "aplikasi":
        return ("Aplikasi siap pakai: Beli sekali Basic Rp499.000 / Professional "
                "Rp999.000 / Business Rp1.999.000, atau langganan Rp49.000 / "
                "Rp99.000 / Rp199.000 per bulan; tambah APK Android +Rp400.000; "
                "garansi bug 30/60/90 hari.")
    if produk == "website":
        return ("Jasa pembuatan website: Basic Rp1.500.000 / Professional "
                "Rp4.500.000 / Business Rp9.900.000 (domain & hosting tidak "
                "termasuk; file jadi milik Kakak).")
    if produk == "poster":
        return "Jasa desain poster: Rp35.000 per poster (file digital)."
    if produk == "paket_lengkap":
        return ("Video promosi 15 detik Rp75.000 + aplikasi kasir/toko Basic "
                "Rp499.000 — keduanya bisa dipesan terpisah; detail harga di "
                "katalog: " + WEBSITE + " (bagian #jasa).")
    return ("Video promosi AI 15 detik Rp75.000 (DP 50%, jadi maks 7 hari), "
            "30 detik Rp150.000, 60 detik Rp250.000 — sudah termasuk naskah "
            "singkat + 1x revisi kecil.")


def draf_personal(nama, observasi="", produk="video"):
    """Draf WhatsApp personal per toko — memakai generator Agent 2.

    Produk "video": panggil a02.template_generator("wa_outreach") lalu
    sisipkan tautan katalog. Produk lain (aplikasi/website/poster/
    paket_lengkap): pola kalimat sama seperti generator Agent 2, dengan
    baris harga produk dari _harga_produk(). Bila a02 tidak tersedia,
    pakai template darurat lokal dengan pola yang sama.
    """
    toko = (nama or "[Nama Toko]").strip()
    obs = (observasi or "").strip()
    a02 = _a02()
    if produk == "video":
        if a02 is not None:
            draf = a02.template_generator("wa_outreach", toko, obs or "produk", "15")
            return _sisip_katalog(draf)
        kalimat_obs = ("Saya lihat {} — ".format(obs) if obs else "")
        return (
            "Halo Kak, saya Masduki dari Podcast Meong (video kucing Oyen & Momo). "
            "{}saya tawarkan {} Contoh video: {} — katalog jasa: {} (bagian #jasa). "
            "Boleh saya buatkan contoh konsep dulu? Terima kasih 🙏".format(
                kalimat_obs, _harga_produk("video"), CONTOH_VIDEO, WEBSITE)
        )
    kalimat_obs = ("Saya lihat {} — ".format(obs) if obs else "")
    return (
        "Halo Kak, saya Masduki dari Podcast Meong (video kucing Oyen & Momo). "
        "{}saya tawarkan {} Contoh video: {} — katalog jasa: {} (bagian #jasa). "
        "Boleh saya buatkan contoh konsep dulu? Terima kasih 🙏".format(
            kalimat_obs, _harga_produk(produk), CONTOH_VIDEO, WEBSITE)
    )


def draf_followup(nama, produk="video"):
    """Draf follow-up — memakai generator Agent 2 bila tersedia."""
    toko = (nama or "[Nama Toko]").strip()
    a02 = _a02()
    if a02 is not None:
        draf = a02.template_generator("wa_followup", toko, "produk", "15")
        return _sisip_katalog(draf)
    return (
        "Halo Kak, saya Masduki dari Podcast Meong — izin follow-up penawaran "
        "untuk {} kemarin. {} Contoh video: {} — katalog jasa: {} (bagian #jasa). "
        "Kalau Kakak berkenan, saya bisa kirim contoh konsep dulu, tanpa "
        "komitmen. Terima kasih 🙏".format(
            toko, _harga_produk(produk), CONTOH_VIDEO, WEBSITE)
    )


def cek_draf(draf):
    """Periksa draf: harga/tautan benar + tanpa janji terlarang. Kembalikan daftar masalah."""
    masalah = []
    d = (draf or "")
    dl = d.lower()
    for kata in KATA_TERLARANG:
        if kata in dl:
            masalah.append("Kata terlarang: '{}'".format(kata))
    if "75.000" not in d and "499.000" not in d and "1.500.000" not in d \
            and "35.000" not in d:
        masalah.append("Tidak ada harga katalog di draf.")
    if CONTOH_VIDEO not in d:
        masalah.append("Tautan video contoh tidak ada.")
    if WEBSITE not in d:
        masalah.append("Tautan website/katalog tidak ada.")
    return masalah


def buat_draf_untuk_toko(toko_id, produk="video", pakai_ai=False, data_file=None):
    """Buat draf personal untuk satu toko + simpan ke log. Kembalikan (draf, info)."""
    daftar = load_toko(data_file)
    toko = next((t for t in daftar if t["id"] == toko_id), None)
    if toko is None:
        return None, "Toko tidak ditemukan: {}".format(toko_id)
    if produk not in PRODUK_TAWARAN:
        return None, "Produk tawaran tidak dikenal: {}".format(produk)
    draf = draf_personal(toko["nama"], toko.get("observasi", ""), produk)
    if pakai_ai:
        hasil_ai = gemini_ask(
            "Anda copywriter pemasaran Podcast Meong. Perbaiki draf penawaran "
            "berikut agar lebih menarik, tetap sopan, singkat, Bahasa Indonesia, "
            "dan JANGAN ubah harga, tautan, atau fakta apa pun. Jangan tambahkan "
            "janji viral/views/penjualan. Jangan tambahkan testimoni.\n\n" + draf)
        if hasil_ai:
            draf = hasil_ai
    masalah = cek_draf(draf)
    if masalah:
        return None, "Draf ditolak pemeriksaan: " + "; ".join(masalah)
    toko["produk_tawaran"] = produk
    toko["draf"] = draf
    save_toko(daftar, data_file)
    return draf, "Draf dibuat (mode: {}).".format("gemini" if pakai_ai and
                                                  mode_ai() == "gemini" else "template")


# ---------------------------------------------------------------- alur data dengan Agent 2
def _leads_file(leads_file=None):
    if leads_file:
        return Path(leads_file)
    a02 = _a02()
    if a02 is not None:
        return Path(a02.LEADS_FILE)
    return BASE / "leads.json"


def _muat_leads(leads_file=None):
    f = _leads_file(leads_file)
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text(encoding="utf-8")).get("leads", [])
    except Exception:
        return []


def _simpan_leads(leads, leads_file=None):
    f = _leads_file(leads_file)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"leads": leads}, ensure_ascii=False, indent=1),
                 encoding="utf-8")


def kirim_ke_agent2(toko_id, data_file=None, leads_file=None):
    """Kirim toko TERVERIFIKASI Agent 4 sebagai lead baru ke Agent 2.

    Hanya verifikasi wa_terkonfirmasi / kemungkinan_wa. Tolak bila toko
    sudah ada di leads Agent 2 (nama / nomor sama) — jangan ganda.
    """
    daftar = load_toko(data_file)
    toko = next((t for t in daftar if t["id"] == toko_id), None)
    if toko is None:
        return None, "Toko tidak ditemukan: {}".format(toko_id)
    if toko.get("verifikasi") not in ("wa_terkonfirmasi", "kemungkinan_wa"):
        return None, ("Toko {} belum terverifikasi ({}). Verifikasi nomor dulu "
                      "sebelum dikirim ke Agent 2.".format(toko_id, toko.get("verifikasi")))
    leads = _muat_leads(leads_file)
    for l in leads:
        if _normal(l.get("nama", "")) == _normal(toko["nama"]) or (
                _normal_hp(l.get("kontak", "")) and
                _normal_hp(l.get("kontak", "")) == _normal_hp(toko.get("kontak_hp", ""))):
            return None, "Sudah jadi lead Agent 2: {}".format(l.get("id"))
    nomor = max([int(l["id"].split("-")[1]) for l in leads
                 if re.match(r"lead-\d+$", l.get("id", ""))], default=0) + 1
    lead = {
        "id": "lead-%02d" % nomor,
        "nama": toko["nama"],
        "kontak": "{} | {}".format(toko.get("kontak_hp", ""),
                                   toko.get("medsos", "")).strip(" |"),
        "alamat": "{}{}".format(toko.get("alamat", ""),
                                (", " + toko["kecamatan"]) if toko.get("kecamatan") else ""),
        "jenis": toko.get("jenis", "pet shop"),
        "status": "baru",
        "terverifikasi": toko.get("verifikasi") == "wa_terkonfirmasi",
        "catatan": "Dari Agent 4 Penjualan Harian ({}). Observasi: {}".format(
            toko["id"], toko.get("observasi", "")),
    }
    leads.append(lead)
    _simpan_leads(leads, leads_file)
    return lead, "Terkirim ke Agent 2 sebagai {} ({}).".format(lead["id"], lead["nama"])


def ambil_lead_agent2(data_file=None, leads_file=None):
    """Ambil lead Agent 2 berstatus 'baru' yang belum ada di log Agent 4.

    Lead yang diambil masuk sebagai toko baru (status 'draf', verifikasi
    dipetakan dari kolom terverifikasi Agent 2). Kembalikan (daftar, info).
    """
    leads = _muat_leads(leads_file)
    daftar = load_toko(data_file)
    diambil = []
    for l in leads:
        if l.get("status") != "baru":
            continue
        if sudah_ada(l.get("nama", ""), l.get("kontak", ""), daftar):
            continue
        kontak = l.get("kontak", "")
        hp = ""
        for bagian in re.split(r"[|]", kontak):
            b = bagian.strip()
            if re.search(r"\d{4,}", b):
                hp = b
                break
        verifikasi = "wa_terkonfirmasi" if l.get("terverifikasi") else "perlu_dicek"
        toko, _info = tambah_toko(
            l.get("nama", ""), jenis=l.get("jenis", "pet shop"),
            alamat=l.get("alamat", ""), kontak_hp=hp,
            kontak_sumber="Agent 2 (leads.json)", medsos=kontak,
            verifikasi=verifikasi, observasi=l.get("catatan", ""),
            data_file=data_file)
        if toko is not None:
            daftar = load_toko(data_file)
            diambil.append(toko)
    return diambil, "Diambil {} lead baru dari Agent 2.".format(len(diambil))


# ---------------------------------------------------------------- ringkasan & rencana harian
def ringkasan(data_file=None):
    daftar = load_toko(data_file)
    by_status = {s: sum(1 for t in daftar if t.get("status") == s) for s in STATUS_TOKO}
    by_verif = {v: sum(1 for t in daftar if t.get("verifikasi") == v) for v in VERIFIKASI}
    return {"total": len(daftar), "per_status": by_status,
            "per_verifikasi": by_verif, "mode": mode_ai()}


def rencana_harian(data_file=None, hari_ini=None):
    """Rencana hari ini: target 15 toko, draf yang sudah siap, follow-up jatuh tempo."""
    hari = hari_ini or str(date.today())
    daftar = load_toko(data_file)
    draf_hari_ini = [t for t in daftar if t.get("tanggal_ditemukan") == hari]
    perlu_draf = [t for t in daftar if t.get("status") == "draf" and not t.get("draf")]
    siap_kirim = [t for t in daftar if t.get("status") == "disetujui"]
    # Follow-up: dibalas / tidak merespons, status terakhir >= 2 hari lalu.
    batas = date.today() - timedelta(days=2)
    followup = []
    for t in daftar:
        if t.get("status") in ("dibalas", "tidak_merespons"):
            try:
                tgl = date.fromisoformat(t.get("tanggal_status", hari))
            except ValueError:
                continue
            if tgl <= batas:
                followup.append(t)
    kurang = max(0, TARGET_HARIAN - len(draf_hari_ini))
    aksi = []
    if kurang > 0:
        aksi.append({
            "judul": "Cari {} toko baru hari ini (target {} toko/hari)".format(kurang, TARGET_HARIAN),
            "detail": "Cari di Google Maps / Instagram / TikTok (mulai pet shop Jakarta Selatan, "
                      "lalu semua jenis toko). Catat nama + nomor HP/WA + alamat, tandai verifikasi "
                      "nomornya. Jangan tambah toko yang sudah ada di log.",
            "toko": []})
    else:
        aksi.append({
            "judul": "Target 15 toko hari ini TERCAPAI ({} toko)".format(len(draf_hari_ini)),
            "detail": "Fokus ke draf + follow-up di bawah. Besok cari 15 toko baru lagi.",
            "toko": []})
    if perlu_draf:
        aksi.append({
            "judul": "Buat draf personal untuk {} toko (belum ada draf)".format(len(perlu_draf)),
            "detail": "Toko: " + ", ".join(t["nama"] for t in perlu_draf[:5]) +
                      (", ..." if len(perlu_draf) > 5 else "") +
                      ". Pakai generator draf di tab Buat Draf. Periksa dulu sebelum Cipta setuju.",
            "toko": [t["id"] for t in perlu_draf[:5]]})
    if siap_kirim:
        aksi.append({
            "judul": "Tunjukkan {} draf yang sudah disetujui ke Cipta untuk dikirim".format(len(siap_kirim)),
            "detail": "Toko: " + ", ".join(t["nama"] for t in siap_kirim[:5]) +
                      ". Cipta yang mengirim sendiri dari WA-nya — agent TIDAK mengirim.",
            "toko": [t["id"] for t in siap_kirim[:5]]})
    if followup:
        aksi.append({
            "judul": "Follow-up {} toko (balasan / belum merespons >= 2 hari)".format(len(followup)),
            "detail": "Toko: " + ", ".join(t["nama"] for t in followup[:5]) +
                      ". Satu follow-up sopan per toko, jangan spam.",
            "toko": [t["id"] for t in followup[:5]]})
    return {"tanggal": hari, "target_harian": TARGET_HARIAN,
            "toko_hari_ini": len(draf_hari_ini), "kurang": kurang,
            "belum_ada_draf": len(perlu_draf), "siap_kirim": len(siap_kirim),
            "followup": len(followup), "total_log": len(daftar), "aksi": aksi}


# ---------------------------------------------------------------- UI Gradio
def _tabel_toko(daftar=None):
    daftar = load_toko() if daftar is None else daftar
    return [[t.get("id", ""), t.get("nama", ""), t.get("jenis", ""),
             t.get("kontak_hp", ""), t.get("verifikasi", ""),
             t.get("status", ""), t.get("tanggal_ditemukan", ""),
             t.get("produk_tawaran", "")] for t in daftar]


def _rencana_markdown():
    r = rencana_harian()
    baris = ["# 📋 Rencana Harian — {}\n".format(r["tanggal"]),
             "Target: **{} toko/hari** · sudah ada hari ini: **{}** · kurang: **{}** · "
             "belum ada draf: **{}** · siap kirim (disetujui): **{}** · follow-up: **{}** · "
             "total di log: **{}**\n".format(r["target_harian"], r["toko_hari_ini"],
                                            r["kurang"], r["belum_ada_draf"],
                                            r["siap_kirim"], r["followup"],
                                            r["total_log"])]
    for i, a in enumerate(r["aksi"], 1):
        baris.append("**{}. {}**\n{}".format(i, a["judul"], a["detail"]))
    return "\n\n".join(baris)


def _tambah_toko_ui(nama, jenis, alamat, kecamatan, hp, sumber, medsos,
                    verifikasi, observasi, produk):
    _, info = tambah_toko(nama, jenis, alamat, kecamatan, hp, sumber, medsos,
                          verifikasi, observasi, produk)
    return info, _tabel_toko()


def _buat_draf_ui(toko_id, produk, pakai_ai):
    if not (toko_id or "").strip():
        return "Pilih toko dulu (ID, contoh: toko-01).", _tabel_toko()
    draf, info = buat_draf_untuk_toko(toko_id.strip(), produk,
                                      pakai_ai=bool(pakai_ai))
    return (draf or info), _tabel_toko()


def _ubah_status_ui(toko_id, status, catatan):
    if not (toko_id or "").strip():
        return "Isi ID toko dulu.", _tabel_toko()
    _, info = ubah_status(toko_id.strip(), status, catatan)
    return info, _tabel_toko()


def build_ui():
    import gradio as gr
    with gr.Blocks(title="Agent 4 — Penjualan Harian",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🏪 Agent 4 — Penjualan Harian\n"
            "Penjualan ke toko-toko dari medsos: nomor HP dari Google Maps, "
            "format katalog baru, **sehari minimal 15 toko** — ditawari dan "
            "dipromosikan.\n\n"
            "🔒 **Aturan keras:** agent TIDAK PERNAH mengirim pesan (WA / DM / "
            "email). Semua output adalah DRAF — Cipta menyetujui draf persisnya "
            "dulu, lalu mengirim sendiri dari WA-nya. Jangan janjikan views / "
            "viral / penjualan naik. Jangan hubungi toko yang sudah ada di log.\n\n"
            "🤝 **Dibantu Agent 2 untuk memasarkan:** draf penawaran memakai "
            "generator promosi Agent 2; toko terverifikasi masuk sebagai lead "
            "Agent 2, dan lead baru Agent 2 bisa diambil untuk penawaran harian "
            "(lihat tab 🔗 Agent 2).\n\n"
            "💰 **Katalog:** video promo 15 dtk Rp75.000 / 30 dtk Rp150.000 / "
            "60 dtk Rp250.000 (DP 50%, maks 7 hari, 1x revisi kecil) · aplikasi "
            "Basic Rp499.000 / Professional Rp999.000 / Business Rp1.999.000 "
            "(APK +Rp400.000) · website Basic Rp1.500.000 / Professional "
            "Rp4.500.000 / Business Rp9.900.000 · poster Rp35.000.")
        with gr.Tab("📋 Target & Rencana"):
            btn_rencana = gr.Button("📋 Tampilkan Rencana Hari Ini", variant="primary")
            rencana_out = gr.Markdown("")
            btn_rencana.click(fn=_rencana_markdown, outputs=rencana_out)
            gr.Markdown("### 🏪 Log Toko (semua)")
            tabel = gr.Dataframe(
                value=_tabel_toko(),
                headers=["ID", "Nama", "Jenis", "No HP/WA", "Verifikasi",
                         "Status", "Ditemukan", "Produk"],
                interactive=False, wrap=True)
            btn_muat = gr.Button("🔄 Muat Ulang Tabel")
            btn_muat.click(fn=_tabel_toko, outputs=tabel)
        with gr.Tab("✍️ Buat Draf"):
            gr.Markdown("Pilih toko (ID dari tabel), pilih produk tawaran, "
                        "lalu buat draf personal. Draf tersimpan ke log dan "
                        "wajib diperiksa + disetujui Cipta sebelum dikirim.")
            with gr.Row():
                d_id = gr.Textbox(label="ID toko *", placeholder="Contoh: toko-01")
                d_produk = gr.Dropdown(choices=PRODUK_TAWARAN, value="video",
                                       label="Produk tawaran")
                d_ai = gr.Checkbox(label="Perbaiki dengan Gemini (bila ada key)",
                                   value=False)
            btn_draf = gr.Button("✍️ Buat Draf Personal", variant="primary")
            draf_out = gr.Textbox(label="Draf (periksa dulu sebelum Cipta setuju)",
                                  lines=8)
            btn_draf.click(fn=_buat_draf_ui, inputs=[d_id, d_produk, d_ai],
                           outputs=[draf_out, tabel])
            gr.Markdown("### ➕ Tambah Toko Baru")
            with gr.Row():
                t_nama = gr.Textbox(label="Nama toko *")
                t_jenis = gr.Textbox(label="Jenis", value="pet shop")
                t_hp = gr.Textbox(label="No HP/WA")
            with gr.Row():
                t_alamat = gr.Textbox(label="Alamat")
                t_kec = gr.Textbox(label="Kecamatan")
                t_sumber = gr.Textbox(label="Sumber nomor", value="Google Maps")
            with gr.Row():
                t_medsos = gr.Textbox(label="Medsos (IG/TikTok)")
                t_verif = gr.Dropdown(choices=VERIFIKASI, value="perlu_dicek",
                                      label="Verifikasi nomor")
                t_produk = gr.Dropdown(choices=PRODUK_TAWARAN, value="video",
                                       label="Produk tawaran")
            t_obs = gr.Textbox(label="Observasi (untuk draf personal)",
                               placeholder="Contoh: jual pakan dan pasir kucing + grooming")
            btn_tambah = gr.Button("➕ Tambah Toko", variant="primary")
            pesan_tambah = gr.Markdown("")
            btn_tambah.click(fn=_tambah_toko_ui,
                             inputs=[t_nama, t_jenis, t_alamat, t_kec, t_hp,
                                     t_sumber, t_medsos, t_verif, t_obs, t_produk],
                             outputs=[pesan_tambah, tabel])
        with gr.Tab("📒 Status & Follow-up"):
            gr.Markdown("Ubah status toko setelah ada perkembangan. "
                        "**Status 'dikirim' hanya diisi SETELAH Cipta mengirim "
                        "sendiri dari WA-nya.** Follow-up: 1x sopan per toko, "
                        "jangan spam.")
            with gr.Row():
                s_id = gr.Textbox(label="ID toko *", placeholder="Contoh: toko-01")
                s_status = gr.Dropdown(choices=STATUS_TOKO, value="disetujui",
                                       label="Status baru")
            s_catatan = gr.Textbox(label="Catatan")
            btn_status = gr.Button("💾 Simpan Status", variant="primary")
            pesan_status = gr.Markdown("")
        with gr.Tab("🔗 Agent 2 (Dibantu Memasarkan)"):
            gr.Markdown(
                "Agent 4 dibantu **Agent 2 (Penjualan)** untuk memasarkan: draf "
                "penawaran memakai generator promosi Agent 2 (WA outreach / "
                "follow-up, DM IG, email, caption) — bukan generator baru.\n\n"
                "**Alur data:** toko terverifikasi Agent 4 → lead baru Agent 2 · "
                "lead Agent 2 berstatus 'baru' → diambil Agent 4 untuk penawaran "
                "harian. Tidak ada pengiriman pesan di sini — Cipta yang mengirim.")
            with gr.Row():
                btn_ambil = gr.Button("📥 Ambil Lead Baru dari Agent 2", variant="primary")
                btn_kirim = gr.Button("📤 Kirim Toko Terverifikasi → Agent 2 (Leads)")
            with gr.Row():
                a2_id = gr.Textbox(label="ID toko (untuk kirim ke Agent 2)",
                                   placeholder="Contoh: toko-01")
            pesan_a2 = gr.Markdown("")
            btn_ambil.click(fn=_ambil_lead_agent2_ui, outputs=[pesan_a2, tabel])
            btn_kirim.click(fn=_kirim_ke_agent2_ui, inputs=[a2_id],
                            outputs=[pesan_a2, tabel])
    return demo


def _ambil_lead_agent2_ui():
    diambil, info = ambil_lead_agent2()
    if diambil:
        info += " " + ", ".join(t["nama"] for t in diambil[:5])
    return info, _tabel_toko()


def _kirim_ke_agent2_ui(toko_id):
    if not (toko_id or "").strip():
        return "Isi ID toko dulu.", _tabel_toko()
    _, info = kirim_ke_agent2(toko_id.strip())
    return info, _tabel_toko()


if __name__ == "__main__":
    import sys
    print("Agent 4 — Penjualan Harian | mode:", mode_ai())
    print("Total toko di log:", len(load_toko()))
    print("Rencana hari ini:", rencana_harian().get("kurang"),
          "toko lagi untuk mencapai target", TARGET_HARIAN)
    sys.exit(0)
