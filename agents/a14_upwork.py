# ======================================================================
# PUSAT KOMANDO — Agent 14 Upwork.
# Dibuat 20 Nov 2026 atas perintah Cipta ("Bangun Tim lagi untuk upwork"
# + "Iya") — tim agen AI khusus Upwork, mengikuti pola 13 agen yang
# sudah ada di Pusat Komando (pola terbaru: a04_penjualan_harian).
# Total agent menjadi 14 (slot 1-14 penuh) + Muse = 15.
#
# Tugas: kerja freelance di Upwork (global) sebagai "AI Video Creator &
# Web Developer" — cari job yang cocok, tulis draf proposal (cover
# letter), lacak lamaran, laporkan harian.
#
# STATUS AKUN — MODE PERSIAPAN / DRAF (20 Nov 2026):
# Akun Upwork BELUM ADA. Signup tertahan di Cloudflare "Verify you are
# human" (klik robot gagal 4x); Cipta akan klik sendiri besok (21 Nov
# 2026), baru Muse lanjutkan isian. Rencana akun: freelancer Masduki,
# masduki1189@gmail.com, Jakarta Selatan, +62 812-4798-6994; judul
# "AI Video Creator & Web Developer", $10/jam (placeholder); password
# hanya via kartu aman; BERHENTI di kode SMS; tanpa pembayaran; KTP
# hanya setelah bertanya. Setelah Upwork: Fiverr, Freelancer.com,
# Sribulancer, Projects.co.id, Fastwork.
# Karena akun belum ada, agent ini bekerja MODE PERSIAPAN: riset kategori
# job yang cocok, siapkan teks profil freelancer + template proposal,
# dan siapkan log pelacakan lamaran. Semua siap dipakai besok begitu
# akun jadi.
#
# ATURAN KERAS (SOP Kerja Sama Agent AI v1.3):
# - Semua output adalah DRAF untuk persetujuan Cipta.
# - Agent TIDAK PERNAH mengirim proposal/lamaran, membayar (connects /
#   membership), atau submit KTP/dokumen — pengiriman apa pun hanya
#   setelah Cipta menyetujui isi persisnya. Modul ini TIDAK PUNYA fungsi
#   kirim apa pun, sengaja.
# - Dilarang mengarang portofolio, klien, penghasilan, rating, atau janji
#   views / viral / penjualan naik. Bila data kurang, tulis
#   "belum cukup data".
# - Jangan lamar job yang sama dua kali (cek duplikat dulu).
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
DATA_FILE = BASE / "lamaran_upwork.json"
MODEL = "gemini-2.0-flash"

TARGET_HARIAN = 5  # job diteliti per hari (Upwork: kualitas > kuantitas)
TARIF_PER_JAM_USD = 10  # placeholder (perintah Cipta 20 Nov 2026)

# ---------------------------------------------------------------- profil freelancer
NAMA = "Masduki"
EMAIL = "masduki1189@gmail.com"
LOKASI = "Jakarta Selatan, Indonesia"
TELEPON = "+62 812-4798-6994"
JUDUL_PROFIL = "AI Video Creator & Web Developer"
WEBSITE = "https://podcastmeong.github.io/"
YOUTUBE = "https://www.youtube.com/@Podcastmeong"
TIKTOK = "https://www.tiktok.com/@podcast_kucing"

# Portofolio nyata (tautan live yang sudah terverifikasi 20 Nov 2026).
PORTOFOLIO = [
    ("Website + toko (Podcast Meong)", WEBSITE),
    ("Video AI — Guardio contest ad (43 dtk, vertikal)",
     "https://youtube.com/shorts/Aq98mScKCLA"),
    ("Demo aplikasi Kasir Toko (login + dasbor + laporan)",
     "https://podcastmeong.github.io/kasir-toko/"),
    ("Demo Digital Menu QR (multi-cabang, PWA)",
     "https://podcastmeong.github.io/digital-menu-qr/"),
    ("Game Oyen Benang (HTML5, 10 level)",
     "https://podcastmeong.github.io/oyen-benang/"),
]

KB = """DATA RESMI — PROFIL FREELANCER UPWORK (satu-satunya sumber kebenaran):
- Nama: Masduki, Jakarta Selatan, Indonesia. Email masduki1189@gmail.com.
- Judul profil: "AI Video Creator & Web Developer". Tarif: $10/jam (placeholder).
- Keahlian: video AI (Google Flow, Kling, Runway), video vertikal 9:16
  (TikTok/Reels/Shorts), website statis HTML/CSS/JS, aplikasi web satu file
  (kasir, booking, inventaris, dasbor + laporan), game HTML5.
- Portofolio: website https://podcastmeong.github.io/ ; video AI
  https://youtube.com/shorts/Aq98mScKCLA ; demo Kasir Toko
  https://podcastmeong.github.io/kasir-toko/ ; demo Digital Menu QR
  https://podcastmeong.github.io/digital-menu-qr/ ; game
  https://podcastmeong.github.io/oyen-benang/ .
- ATURAN JUJUR: jangan klaim klien, penghasilan, rating, atau jumlah job
  yang belum ada. Jangan janjikan views, viral, atau penjualan naik.
  Yang ditawarkan hanya jasa + isi paketnya + contoh kerja nyata."""

# Kategori job yang dicari (riset — bukan janji dapat job).
KATEGORI_JOB = [
    {"id": "video-ai", "nama": "AI video creation / video ads",
     "kata_kunci": ["AI video", "AI-generated video", "product video ad",
                    "short video ad", "promo video"],
     "catatan": "Video iklan/produk vertikal 9:16, 15-60 detik, dari naskah "
                "sampai jadi. Contoh kerja: Guardio ad (43 dtk)."},
    {"id": "video-pendek", "nama": "Short-form video editing",
     "kata_kunci": ["short-form video", "TikTok", "Reels", "Shorts",
                    "video editing"],
     "catatan": "Edit video pendek + subtitle + hook 2 detik pertama. "
                "AI-assisted, bukan janji viral."},
    {"id": "web-statis", "nama": "Web development — landing / company profile",
     "kata_kunci": ["landing page", "business website", "company profile",
                    "static website", "HTML CSS"],
     "catatan": "Website statis HTML/CSS/JS, file jadi milik klien, "
                "7 hari kerja untuk 1-5 halaman."},
    {"id": "web-app", "nama": "Web app satu file (alat bisnis)",
     "kata_kunci": ["web app", "POS", "booking system", "inventory",
                    "dashboard", "single-page app"],
     "catatan": "Aplikasi satu file: kasir, booking servis, inventaris, "
                "dasbor + laporan + ekspor CSV. Data per perangkat, offline."},
    {"id": "game-html5", "nama": "Game HTML5 sederhana",
     "kata_kunci": ["HTML5 game", "browser game", "casual game", "web game"],
     "catatan": "Game browser ringan (contoh: Oyen Benang, Tangkap Ikan). "
                "Maksimal Level 3 — tanpa server."},
]

# Saringan job — tolak job yang tidak memenuhi ini.
SYARAT_JOB = {
    "pembayaran_terverifikasi": True,
    "anggaran_min_usd": 50,       # job fixed-price di bawah ini dilewati
    "tarif_min_usd_per_jam": 10,  # job hourly di bawah ini dilewati
    "tolak": ["unpaid test", "free trial", "free sample", "guaranteed viral",
              "crypto", "guaranteed sales", "spec work"],
}

STATUS_LAMARAN = ["riset", "draf", "disetujui", "dikirim", "dibalas",
                  "wawancara", "menang", "tolak", "tidak_merespons"]
JENIS_JOB = ["fixed", "hourly"]
KATA_TERLARANG = ["viral", "views naik", "penjualan naik", "pasti laku",
                  "dijamin", "guaranteed", "testimoni", "100% viral"]


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


def status_akun():
    """Status akun Upwork yang diketahui (20 Nov 2026)."""
    return {
        "akun_ada": False,
        "status": "belum_ada",
        "keterangan": "Signup tertahan di Cloudflare 'Verify you are human' "
                      "(klik robot gagal 4x). Cipta klik sendiri besok "
                      "(21 Nov 2026), baru Muse lanjutkan isian. Sampai akun "
                      "jadi, agent bekerja MODE PERSIAPAN: riset + draf saja.",
        "rencana": {"nama": NAMA, "email": EMAIL, "lokasi": LOKASI,
                    "judul": JUDUL_PROFIL, "tarif_per_jam_usd": TARIF_PER_JAM_USD},
    }


# ---------------------------------------------------------------- data (JSON lokal)
def _data_file(data_file=None):
    return Path(data_file) if data_file else DATA_FILE


def load_lamaran(data_file=None):
    f = _data_file(data_file)
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text(encoding="utf-8")).get("lamaran", [])
    except Exception:
        return []


def save_lamaran(daftar, data_file=None):
    f = _data_file(data_file)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"lamaran": daftar}, ensure_ascii=False, indent=1),
                 encoding="utf-8")


def _normal(teks):
    s = unicodedata.normalize("NFKD", (teks or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def sudah_ada(judul, klien="", tautan="", daftar=None, data_file=None):
    """True bila job (judul+klien sama ATAU tautan sama) sudah ada di log."""
    daftar = load_lamaran(data_file) if daftar is None else daftar
    j = _normal(judul)
    k = _normal(klien)
    t = (tautan or "").strip().lower()
    for l in daftar:
        if j and k and _normal(l.get("judul", "")) == j \
                and _normal(l.get("klien", "")) == k:
            return True
        if t and (l.get("tautan", "") or "").strip().lower() == t:
            return True
    return False


def tambah_job(judul, klien="", kategori="video-ai", jenis="fixed",
               anggaran_usd=None, tautan="", catatan="", data_file=None):
    """Tambah job hasil riset. Tolak bila duplikat / kategori / jenis salah."""
    if not (judul or "").strip():
        return None, "Judul job wajib diisi."
    if not any(k["id"] == kategori for k in KATEGORI_JOB):
        return None, "Kategori tidak dikenal: {}".format(kategori)
    if jenis not in JENIS_JOB:
        return None, "Jenis job tidak dikenal: {}".format(jenis)
    daftar = load_lamaran(data_file)
    if sudah_ada(judul, klien, tautan, daftar):
        return None, "Sudah ada di log — jangan lamar ganda: {}".format(judul.strip())
    nomor = max([int(l["id"].split("-")[1]) for l in daftar
                 if re.match(r"lam-\d+$", l.get("id", ""))], default=0) + 1
    job = {
        "id": "lam-%02d" % nomor,
        "judul": judul.strip(),
        "klien": (klien or "").strip(),
        "kategori": kategori,
        "jenis": jenis,
        "anggaran_usd": anggaran_usd,
        "tautan": (tautan or "").strip(),
        "tanggal_ditemukan": str(date.today()),
        "proposal": "",
        "status": "riset",
        "tanggal_status": str(date.today()),
        "followup_ke": 0,
        "catatan": (catatan or "").strip(),
    }
    daftar.append(job)
    save_lamaran(daftar, data_file)
    return job, "Ditambahkan: {} ({})".format(job["id"], job["judul"])


def ubah_status(lamaran_id, status, catatan="", data_file=None):
    if status not in STATUS_LAMARAN:
        return None, "Status tidak dikenal: {}".format(status)
    daftar = load_lamaran(data_file)
    for l in daftar:
        if l["id"] == lamaran_id:
            l["status"] = status
            l["tanggal_status"] = str(date.today())
            if catatan:
                l["catatan"] = catatan.strip()
            save_lamaran(daftar, data_file)
            return l, "Status {} menjadi '{}'.".format(lamaran_id, status)
    return None, "Lamaran tidak ditemukan: {}".format(lamaran_id)


def simpan_proposal(lamaran_id, proposal, data_file=None):
    daftar = load_lamaran(data_file)
    for l in daftar:
        if l["id"] == lamaran_id:
            l["proposal"] = (proposal or "").strip()
            save_lamaran(daftar, data_file)
            return l, "Proposal disimpan untuk {}.".format(lamaran_id)
    return None, "Lamaran tidak ditemukan: {}".format(lamaran_id)


# ---------------------------------------------------------------- teks profil freelancer
def teks_profil():
    """Teks profil freelancer Upwork (English — Upwork global). DRAF."""
    portofolio = "\n".join(
        "- {}: {}".format(nama, tautan) for nama, tautan in PORTOFOLIO)
    return (
        "{}\n"
        "AI Video Creator & Web Developer | Jakarta, Indonesia\n\n"
        "I create AI-generated promo videos and build fast, single-file "
        "web apps for small businesses.\n\n"
        "What I do:\n"
        "- AI promo videos (15-60 seconds, vertical 9:16) for TikTok, "
        "Reels and Shorts — script, visuals and edit included.\n"
        "- Static business websites (HTML/CSS/JS) — landing pages and "
        "company profiles, delivered as files you own.\n"
        "- Single-file web apps — POS/cashier, booking, inventory, "
        "dashboards with reports and CSV export. No server needed, "
        "works offline.\n"
        "- Simple HTML5 browser games.\n\n"
        "Portfolio:\n{}\n\n"
        "Rate: ${}/hour. Fixed-price projects quoted per scope.\n"
        "I reply fast and deliver on the agreed schedule. Let's talk "
        "about your project.".format(
            NAMA, portofolio, TARIF_PER_JAM_USD))


def teks_profil_singkat():
    """Ringkasan profil 2 kalimat (untuk bio singkat / overview)."""
    return ("AI Video Creator & Web Developer from Jakarta. I make "
            "AI promo videos (15-60s, vertical) and fast single-file web "
            "apps for small businesses — portfolio: {}.".format(WEBSITE))


# ---------------------------------------------------------------- template proposal
def template_proposal(judul_job, klien="", jenis="fixed",
                      anggaran_usd=None):
    """Cover letter Upwork (English). DRAF — wajib disetujui Cipta."""
    job = (judul_job or "[Job title]").strip()
    klien_teks = "Hi {},\n\n".format((klien or "").strip()) if (klien or "").strip() else "Hi,\n\n"
    tarif = ("My rate is ${}/hour.".format(TARIF_PER_JAM_USD) if jenis == "hourly"
             else "For fixed-price work I quote per scope after seeing the "
                  "details.")
    return (
        "{}"
        "I'm Masduki, an AI Video Creator & Web Developer from Jakarta. "
        "I read your job post for \"{}\" and I'd like to help.\n\n"
        "Relevant work:\n"
        "- AI promo video (43s, vertical): "
        "https://youtube.com/shorts/Aq98mScKCLA\n"
        "- Business web app demo (cashier + dashboard + reports): "
        "https://podcastmeong.github.io/kasir-toko/\n"
        "- Website + store: {}\n\n"
        "How I'd approach your project: first I confirm the exact scope "
        "and deadline with you, then I deliver a first version for your "
        "review, and revise once based on your feedback. {}\n\n"
        "Happy to answer any questions. Thank you for considering my "
        "proposal.\n\n"
        "Best regards,\nMasduki".format(klien_teks, job, WEBSITE, tarif))


def template_proposal_singkat(judul_job):
    """Cover letter pendek (untuk job yang minta jawaban singkat)."""
    return (
        "Hi, I'm Masduki — AI Video Creator & Web Developer from Jakarta. "
        "For \"{}\": I can deliver a first version quickly for your review, "
        "then revise once based on your feedback. Portfolio: {} "
        "(video: https://youtube.com/shorts/Aq98mScKCLA). "
        "Rate: ${}/hour. Thank you!".format(
            (judul_job or "[Job title]").strip(), WEBSITE, TARIF_PER_JAM_USD))


def template_followup(judul_job, klien=""):
    """Follow-up sopan 1x — hanya bila klien sudah membalas/dilihat."""
    sapaan = "Hi {},\n\n".format((klien or "").strip()) if (klien or "").strip() else "Hi,\n\n"
    return (
        "{}Just following up on my proposal for \"{}\". I'm still "
        "available and happy to answer any questions about my approach or "
        "portfolio. No rush at all — thank you for your time.\n\n"
        "Best regards,\nMasduki".format(
            sapaan, (judul_job or "[Job title]").strip()))


def cek_proposal(proposal):
    """Periksa proposal: tautan + tarif benar, tanpa janji terlarang."""
    masalah = []
    d = (proposal or "")
    dl = d.lower()
    for kata in KATA_TERLARANG:
        if kata in dl:
            masalah.append("Kata terlarang: '{}'".format(kata))
    if WEBSITE not in d and "Aq98mScKCLA" not in d:
        masalah.append("Tautan portofolio tidak ada.")
    if "$10" not in d and "per scope" not in d and "per jam" not in d:
        masalah.append("Tarif tidak disebut (per jam / per scope).")
    if "Masduki" not in d:
        masalah.append("Nama pengirim tidak ada.")
    return masalah


def buat_proposal_untuk_job(lamaran_id, jenis_template="panjang",
                            pakai_ai=False, data_file=None):
    """Buat draf proposal untuk satu job + simpan ke log."""
    daftar = load_lamaran(data_file)
    job = next((l for l in daftar if l["id"] == lamaran_id), None)
    if job is None:
        return None, "Lamaran tidak ditemukan: {}".format(lamaran_id)
    if jenis_template == "singkat":
        proposal = template_proposal_singkat(job["judul"])
    else:
        proposal = template_proposal(job["judul"], job.get("klien", ""),
                                     job.get("jenis", "fixed"),
                                     job.get("anggaran_usd"))
    if pakai_ai:
        hasil_ai = gemini_ask(
            "You are a freelance proposal writer. Improve this Upwork cover "
            "letter: keep it short, polite, professional English. Do NOT "
            "change rates, links, or facts. Do NOT add promises about views, "
            "viral results, or sales. Do NOT invent clients, earnings, or "
            "ratings.\n\n" + proposal)
        if hasil_ai:
            proposal = hasil_ai
    masalah = cek_proposal(proposal)
    if masalah:
        return None, "Proposal ditolak pemeriksaan: " + "; ".join(masalah)
    job["proposal"] = proposal
    job["status"] = "draf"
    job["tanggal_status"] = str(date.today())
    save_lamaran(daftar, data_file)
    return proposal, "Draf proposal dibuat (mode: {}).".format(
        "gemini" if pakai_ai and mode_ai() == "gemini" else "template")


# ---------------------------------------------------------------- riset job
def daftar_kategori():
    """Daftar kategori job yang dicari + kata kunci + saringan."""
    return [dict(k) for k in KATEGORI_JOB]


def cek_job_layak(judul, deskripsi="", pembayaran_terverifikasi=False,
                  anggaran_usd=None, jenis="fixed"):
    """Nilai apakah sebuah job layak dilamar. Kembalikan (layak, alasan)."""
    alasan = []
    dl = "{} {}".format(judul or "", deskripsi or "").lower()
    for kata in SYARAT_JOB["tolak"]:
        if kata in dl:
            alasan.append("Mengandung '{}' — tolak.".format(kata))
    if SYARAT_JOB["pembayaran_terverifikasi"] and not pembayaran_terverifikasi:
        alasan.append("Pembayaran klien belum terverifikasi.")
    if jenis == "fixed" and anggaran_usd is not None \
            and anggaran_usd < SYARAT_JOB["anggaran_min_usd"]:
        alasan.append("Anggaran ${} di bawah minimum ${}.".format(
            anggaran_usd, SYARAT_JOB["anggaran_min_usd"]))
    if jenis == "hourly" and anggaran_usd is not None \
            and anggaran_usd < SYARAT_JOB["tarif_min_usd_per_jam"]:
        alasan.append("Tarif ${}/jam di bawah minimum ${}/jam.".format(
            anggaran_usd, SYARAT_JOB["tarif_min_usd_per_jam"]))
    if alasan:
        return False, " ".join(alasan)
    return True, "Layak dilamar (draf dulu — kirim hanya setelah Cipta setuju)."


# ---------------------------------------------------------------- ringkasan & rencana harian
def ringkasan(data_file=None):
    daftar = load_lamaran(data_file)
    by_status = {s: sum(1 for l in daftar if l.get("status") == s)
                 for s in STATUS_LAMARAN}
    by_kat = {k["id"]: sum(1 for l in daftar if l.get("kategori") == k["id"])
              for k in KATEGORI_JOB}
    return {"total": len(daftar), "per_status": by_status,
            "per_kategori": by_kat, "mode": mode_ai(),
            "akun_ada": status_akun()["akun_ada"]}


def rencana_harian(data_file=None, hari_ini=None):
    """Rencana hari ini: target 5 job diteliti, draf siap, follow-up."""
    hari = hari_ini or str(date.today())
    daftar = load_lamaran(data_file)
    job_hari_ini = [l for l in daftar if l.get("tanggal_ditemukan") == hari]
    perlu_draf = [l for l in daftar if l.get("status") == "riset"]
    siap_kirim = [l for l in daftar if l.get("status") == "disetujui"]
    batas = date.today() - timedelta(days=3)
    followup = []
    for l in daftar:
        if l.get("status") in ("dibalas", "tidak_merespons"):
            try:
                tgl = date.fromisoformat(l.get("tanggal_status", hari))
            except ValueError:
                continue
            if tgl <= batas:
                followup.append(l)
    kurang = max(0, TARGET_HARIAN - len(job_hari_ini))
    aksi = []
    if not status_akun()["akun_ada"]:
        aksi.append({
            "judul": "MODE PERSIAPAN — akun Upwork belum ada",
            "detail": "Signup tertahan di Cloudflare. Cipta klik 'Verify you "
                      "are human' besok (21 Nov), baru Muse lanjutkan isian "
                      "akun. Hari ini: riset job + siapkan draf proposal + "
                      "rapikan teks profil. JANGAN kirim lamaran apa pun "
                      "sebelum akun jadi dan Cipta menyetujui proposal persisnya.",
            "job": []})
    if kurang > 0:
        aksi.append({
            "judul": "Teliti {} job baru hari ini (target {} job/hari)".format(
                kurang, TARGET_HARIAN),
            "detail": "Cari di Upwork per kategori (video AI, video pendek, "
                      "web statis, web app, game HTML5). Cek: pembayaran "
                      "klien terverifikasi, anggaran memadai, deskripsi "
                      "cocok dengan keahlian. Tolak job 'unpaid test' / "
                      "'free trial' / janji viral. Jangan tambah job yang "
                      "sudah ada di log.",
            "job": []})
    else:
        aksi.append({
            "judul": "Target {} job hari ini TERCAPAI ({})".format(
                TARGET_HARIAN, len(job_hari_ini)),
            "detail": "Fokus ke draf proposal + follow-up di bawah.",
            "job": []})
    if perlu_draf:
        aksi.append({
            "judul": "Buat draf proposal untuk {} job (status riset)".format(
                len(perlu_draf)),
            "detail": "Job: " + ", ".join(l["judul"] for l in perlu_draf[:5]) +
                      (", ..." if len(perlu_draf) > 5 else "") +
                      ". Pakai tab Buat Proposal. Periksa dulu sebelum "
                      "Cipta setuju.",
            "job": [l["id"] for l in perlu_draf[:5]]})
    if siap_kirim:
        aksi.append({
            "judul": "Tunjukkan {} proposal yang sudah disetujui ke Cipta".format(
                len(siap_kirim)),
            "detail": "Job: " + ", ".join(l["judul"] for l in siap_kirim[:5]) +
                      ". Cipta yang mengirim sendiri — agent TIDAK mengirim.",
            "job": [l["id"] for l in siap_kirim[:5]]})
    if followup:
        aksi.append({
            "judul": "Follow-up {} lamaran (dibalas / belum merespons >= 3 hari)".format(
                len(followup)),
            "detail": "Job: " + ", ".join(l["judul"] for l in followup[:5]) +
                      ". Satu follow-up sopan per job, jangan spam.",
            "job": [l["id"] for l in followup[:5]]})
    return {"tanggal": hari, "target_harian": TARGET_HARIAN,
            "job_hari_ini": len(job_hari_ini), "kurang": kurang,
            "belum_ada_draf": len(perlu_draf), "siap_kirim": len(siap_kirim),
            "followup": len(followup), "total_log": len(daftar), "aksi": aksi}


# ---------------------------------------------------------------- UI Gradio
def _tabel_lamaran(daftar=None):
    daftar = load_lamaran() if daftar is None else daftar
    return [[l.get("id", ""), l.get("judul", ""), l.get("klien", ""),
             l.get("kategori", ""), l.get("jenis", ""),
             l.get("anggaran_usd", ""), l.get("status", ""),
             l.get("tanggal_ditemukan", "")] for l in daftar]


def _rencana_markdown():
    r = rencana_harian()
    baris = ["# 📋 Rencana Harian — {}\n".format(r["tanggal"]),
             "Target: **{} job/hari** · diteliti hari ini: **{}** · kurang: "
             "**{}** · belum ada draf: **{}** · siap kirim (disetujui): "
             "**{}** · follow-up: **{}** · total di log: **{}**\n".format(
                 r["target_harian"], r["job_hari_ini"], r["kurang"],
                 r["belum_ada_draf"], r["siap_kirim"], r["followup"],
                 r["total_log"])]
    for i, a in enumerate(r["aksi"], 1):
        baris.append("**{}. {}**\n{}".format(i, a["judul"], a["detail"]))
    return "\n\n".join(baris)


def _tambah_job_ui(judul, klien, kategori, jenis, anggaran, tautan, catatan):
    try:
        anggaran_usd = float(anggaran) if (anggaran or "").strip() else None
    except ValueError:
        anggaran_usd = None
    _, info = tambah_job(judul, klien, kategori, jenis, anggaran_usd,
                         tautan, catatan)
    return info, _tabel_lamaran()


def _buat_proposal_ui(lamaran_id, jenis_template, pakai_ai):
    if not (lamaran_id or "").strip():
        return "Pilih job dulu (ID, contoh: lam-01).", _tabel_lamaran()
    proposal, info = buat_proposal_untuk_job(
        lamaran_id.strip(), jenis_template, pakai_ai=bool(pakai_ai))
    return (proposal or info), _tabel_lamaran()


def _ubah_status_ui(lamaran_id, status, catatan):
    if not (lamaran_id or "").strip():
        return "Isi ID lamaran dulu.", _tabel_lamaran()
    _, info = ubah_status(lamaran_id.strip(), status, catatan)
    return info, _tabel_lamaran()


def _cek_job_ui(judul, deskripsi, terverifikasi, anggaran, jenis):
    try:
        anggaran_usd = float(anggaran) if (anggaran or "").strip() else None
    except ValueError:
        anggaran_usd = None
    layak, alasan = cek_job_layak(judul, deskripsi, bool(terverifikasi),
                                  anggaran_usd, jenis)
    return ("✅ LAYAK — " if layak else "❌ TIDAK LAYAK — ") + alasan


def build_ui():
    import gradio as gr
    with gr.Blocks(title="Agent 14 — Upwork",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 💼 Agent 14 — Upwork\n"
            "Tim agen AI khusus Upwork: cari job yang cocok (AI video creator "
            "+ web developer), tulis draf proposal, lacak lamaran, laporkan "
            "harian.\n\n"
            "🔒 **MODE PERSIAPAN — akun Upwork BELUM ADA.** Signup tertahan di "
            "Cloudflare 'Verify you are human'; Cipta klik sendiri besok "
            "(21 Nov 2026), baru Muse lanjutkan isian. Sampai akun jadi, "
            "agent hanya riset + draf — **TIDAK PERNAH mengirim proposal / "
            "lamaran, membayar, atau submit KTP.** Semua output adalah DRAF — "
            "Cipta menyetujui isi persisnya dulu.\n\n"
            "💰 **Tarif:** $10/jam (placeholder). **Profil:** Masduki, Jakarta "
            "Selatan — 'AI Video Creator & Web Developer'. **Portofolio:** "
            "website, video AI Guardio, demo Kasir Toko, Digital Menu QR, "
            "game Oyen Benang. Jangan klaim klien / penghasilan / rating "
            "yang belum ada; jangan janjikan views / viral / penjualan naik.")
        with gr.Tab("📋 Rencana & Log"):
            btn_rencana = gr.Button("📋 Tampilkan Rencana Hari Ini", variant="primary")
            rencana_out = gr.Markdown("")
            btn_rencana.click(fn=_rencana_markdown, outputs=rencana_out)
            gr.Markdown("### 💼 Log Lamaran (semua)")
            tabel = gr.Dataframe(
                value=_tabel_lamaran(),
                headers=["ID", "Judul Job", "Klien", "Kategori", "Jenis",
                         "Anggaran $", "Status", "Ditemukan"],
                interactive=False, wrap=True)
            btn_muat = gr.Button("🔄 Muat Ulang Tabel")
            btn_muat.click(fn=_tabel_lamaran, outputs=tabel)
        with gr.Tab("🔍 Riset Job"):
            gr.Markdown("### 🎯 Kategori yang dicari")
            for k in KATEGORI_JOB:
                gr.Markdown("**{}** — kata kunci: {}. {}".format(
                    k["nama"], ", ".join(k["kata_kunci"]), k["catatan"]))
            gr.Markdown(
                "### ✅ Cek kelayakan job\n"
                "Saringan: pembayaran klien terverifikasi · fixed ≥ $50 · "
                "hourly ≥ $10/jam · tolak 'unpaid test' / 'free trial' / "
                "janji viral / crypto.")
            with gr.Row():
                c_judul = gr.Textbox(label="Judul job *")
                c_jenis = gr.Dropdown(choices=JENIS_JOB, value="fixed",
                                      label="Jenis")
                c_anggaran = gr.Textbox(label="Anggaran $ (fixed) / tarif $/jam")
                c_verif = gr.Checkbox(label="Pembayaran klien terverifikasi",
                                      value=False)
            c_desk = gr.Textbox(label="Deskripsi job (tempel ringkasannya)",
                                lines=3)
            btn_cek = gr.Button("✅ Cek Kelayakan", variant="primary")
            cek_out = gr.Markdown("")
            btn_cek.click(fn=_cek_job_ui,
                          inputs=[c_judul, c_desk, c_verif, c_anggaran, c_jenis],
                          outputs=cek_out)
            gr.Markdown("### ➕ Tambah Job ke Log")
            with gr.Row():
                j_judul = gr.Textbox(label="Judul job *")
                j_klien = gr.Textbox(label="Nama klien")
                j_kat = gr.Dropdown(choices=[k["id"] for k in KATEGORI_JOB],
                                    value="video-ai", label="Kategori")
            with gr.Row():
                j_jenis = gr.Dropdown(choices=JENIS_JOB, value="fixed",
                                      label="Jenis")
                j_anggaran = gr.Textbox(label="Anggaran $")
                j_tautan = gr.Textbox(label="Tautan job Upwork")
            j_catatan = gr.Textbox(label="Catatan")
            btn_tambah = gr.Button("➕ Tambah Job", variant="primary")
            pesan_tambah = gr.Markdown("")
            btn_tambah.click(fn=_tambah_job_ui,
                             inputs=[j_judul, j_klien, j_kat, j_jenis,
                                     j_anggaran, j_tautan, j_catatan],
                             outputs=[pesan_tambah, tabel])
        with gr.Tab("✍️ Buat Proposal"):
            gr.Markdown("Pilih job (ID dari tabel), lalu buat draf proposal "
                        "(cover letter Bahasa Inggris). Draf tersimpan ke log "
                        "dan wajib diperiksa + disetujui Cipta sebelum dikirim.")
            with gr.Row():
                p_id = gr.Textbox(label="ID lamaran *", placeholder="Contoh: lam-01")
                p_jenis = gr.Dropdown(choices=["panjang", "singkat"],
                                      value="panjang", label="Jenis proposal")
                p_ai = gr.Checkbox(label="Perbaiki dengan Gemini (bila ada key)",
                                   value=False)
            btn_proposal = gr.Button("✍️ Buat Draf Proposal", variant="primary")
            proposal_out = gr.Textbox(label="Draf proposal (periksa dulu sebelum Cipta setuju)",
                                      lines=12)
            btn_proposal.click(fn=_buat_proposal_ui,
                               inputs=[p_id, p_jenis, p_ai],
                               outputs=[proposal_out, tabel])
            gr.Markdown("### 📩 Template follow-up (1x, sopan, bila klien membalas)")
            with gr.Row():
                f_judul = gr.Textbox(label="Judul job")
                f_klien = gr.Textbox(label="Nama klien")
            btn_follow = gr.Button("📩 Tampilkan Template Follow-up")
            follow_out = gr.Textbox(label="Template follow-up", lines=5)
            btn_follow.click(fn=lambda j, k: template_followup(j, k),
                             inputs=[f_judul, f_klien], outputs=follow_out)
        with gr.Tab("👤 Profil Freelancer"):
            gr.Markdown("Teks profil siap pakai untuk besok saat akun jadi "
                        "(salin ke Upwork). DRAF — Cipta periksa dulu.")
            profil_out = gr.Textbox(label="Profil freelancer (English)",
                                    value=teks_profil(), lines=16)
            gr.Markdown("### Ringkasan 2 kalimat (bio singkat)")
            gr.Textbox(label="Bio singkat", value=teks_profil_singkat(), lines=2)
        with gr.Tab("📒 Status & Follow-up"):
            gr.Markdown("Ubah status lamaran setelah ada perkembangan. "
                        "**Status 'dikirim' hanya diisi SETELAH Cipta mengirim "
                        "sendiri dari Upwork-nya.** Follow-up: 1x sopan per job, "
                        "jangan spam.")
            with gr.Row():
                s_id = gr.Textbox(label="ID lamaran *", placeholder="Contoh: lam-01")
                s_status = gr.Dropdown(choices=STATUS_LAMARAN, value="disetujui",
                                       label="Status baru")
            s_catatan = gr.Textbox(label="Catatan")
            btn_status = gr.Button("💾 Simpan Status", variant="primary")
            pesan_status = gr.Markdown("")
            btn_status.click(fn=_ubah_status_ui,
                             inputs=[s_id, s_status, s_catatan],
                             outputs=[pesan_status, tabel])
    return demo


if __name__ == "__main__":
    import sys
    print("Agent 14 — Upwork | mode:", mode_ai())
    print("Akun Upwork ada:", status_akun()["akun_ada"], "|",
          status_akun()["keterangan"])
    print("Total lamaran di log:", len(load_lamaran()))
    print("Rencana hari ini:", rencana_harian().get("kurang"),
          "job lagi untuk mencapai target", TARGET_HARIAN)
    sys.exit(0)
