"""BINTANG COMMAND CENTER — Agent A28 Opportunity Hunter.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Mencari lomba, freelance, hibah dan kemitraan
Divisi: Peluang & Keuangan · Atasan: A02
Dipetakan ke (sistem kita): A6 + A14
Pemetaan Gemini #1: Divisi 5 — Freelance & Finance — 5A — Freelance & Gig Bidder
Status nyata: Aktif

SKILL BARU 21 Nov 2026 (perintah Cipta "Semuanya"):
- Isi profil otomatis dari CV Cipta (lihat PROFIL_CV + BIO_ID/BIO_EN).
- Panduan hadapi CAPTCHA per platform (lihat PANDUAN_CAPTCHA).
- Checklist pembuatan akun per platform (lihat CHECKLIST_AKUN).
- ATURAN PILIH LOWONGAN (Cipta, 21 Nov 2026 10:32, DIPERKETAT 10:35):
  HANYA ambil lowongan yang MUDAH saja (lihat KRITERIA_LOWONGAN).
  Yang sedang/sulit JANGAN diambil.
- ROUTING TUGAS (Cipta, 21 Nov 2026 11:26): cari tugas yang mudah-mudah;
  bila lowongan DITERIMA/dapat, KABARI Cipta segera. Tugas pengetikan
  diserahkan ke A35 (Ngetik); tugas copywriting diserahkan ke A36
  (Copywriter). A28 hanya mencari + mengajukan (draf), eksekusi oleh
  agent spesialisnya.
- DUKUNGAN (perintah Cipta 21 Nov 2026 19:35): bila A28 dapat lowongan,
  SEMUA support membantunya. Setiap draf mencatat agen pendukung di field
  "dukungan" (lihat DUKUNGAN_PER_JENIS); semua draf tersimpan di
  data/draf_sribu.json + memori bersama (jenis "sribu_draf") sehingga agen
  mana pun bisa membaca + membantu. A26 (Customer Service) bila perlu.
- INFO DULU (perintah Cipta 21 Nov 2026 19:41: "Klo ada lowongan iya info
  dulu"): setiap lowongan COCOK yang baru dibuat drafnya DITANDAI
  info_cipta=True dan DITONJOLKAN di awal ringkasan jalankan() — Muse yang
  menjalankan engine WAJIB mengabari Cipta di chat SEBELUM langkah lain,
  lalu tandai_diinfo(). Bila Cipta menerima lowongan itu, tandai_diterima().
  Telegram/n8n BELUM AKTIF (21 Nov) — untuk sekarang info lewat hasil run
  engine + memori, BUKAN Telegram; alihkan ke Telegram setelah n8n aktif
  (langkah lanjutan, bukan bagian alur ini).

SKILL BARU 21 Nov 2026 — lanjutan (tinjauan peninjau skill):
- Tarif pasar riset 2026 untuk 3 jasa baru (lihat TARIF_PASAR_RISET_2026):
  jasa ngetik, copywriter, translate bahasa — tarif pasar, bukan harga
  jual kita dan bukan janji penghasilan.

KEJUJURAN WAJIB — BACA DULU:
- Agent ini PASIF: dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri.
  A01 CEO = Muse sebagai koordinator (bukan agent yang berjalan sendiri).
- Semua output adalah DRAF untuk persetujuan Cipta. Modul ini TIDAK PUNYA
  fungsi kirim / bayar / publikasi / submit apa pun, sengaja.
- Dilarang mengarang portofolio, klien, penghasilan, rating, angka, atau
  janji views / viral / penjualan. Bila data kurang, tulis
  "belum cukup data".
- Target/KPI Gemini di bawah adalah TARGET RANCANGAN (Share Gemini #1),
  bukan hasil nyata dan bukan janji.
- Pusat komando BUKAN Agent.ai (dialihkan ke builderpack.com, cek live
  21 Nov 2026) dan database BUKAN Google Sheets (kita tetap JSON).
  Tidak ada framework otonom (CrewAI/AutoGen ditolak) dan tidak ada
  otomasi 24 jam.
- Gemini free tier HANYA dari env var GEMINI_API_KEY — tidak pernah
  ditulis di file. Tanpa key, semua fitur tetap jalan mode template.
"""
import json
import os
from datetime import date
from pathlib import Path

# MEMORI BERSAMA (21 Nov 2026): A28 menyimpan profil freelance ke memori
# bersama supaya agen lain (A25/A35/A36) membaca profil yang sama
# (lihat simpan_profil_memori + baca_profil_memori). Import aman: bila modul
# tidak ada, fungsi memori mengembalikan "tidak tersedia" tanpa merusak
# fungsi lain. Modul ini TETAP tidak punya fungsi kirim/bayar/publikasi.
try:
    import memori_bersama as MEMORI
except Exception:
    MEMORI = None

BASE = Path(__file__).resolve().parent.parent / "data"
MODEL = "gemini-4-hydrogen"

KODE = "A28"
NAMA = "Opportunity Hunter"
DIVISI = "Peluang & Keuangan"
ATASAN = "A02"
JOB_DESC = "Mencari lomba, freelance, hibah dan kemitraan"
DIPETAKAN_KE = "A6 + A14"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 5 — Freelance & Finance"
GEMINI_PERAN = "5A — Freelance & Gig Bidder"
GEMINI_KPI = ['5 proposal/hari — DRAF saja, kirim hanya setelah Cipta setuju (target rancangan)', 'Target 1–2 proyek didapat/bulan (target rancangan)']
GEMINI_TOOLS = []


KATA_TERLARANG = ["viral", "views naik", "penjualan naik", "pasti laku",
                  "dijamin", "guaranteed", "testimoni", "100% viral",
                  "penghasilan pasti"]


# SKILL BARU 21 Nov 2026 — isi profil otomatis dari CV Cipta.
# Sumber: ~/workspace/user/files/MDUKI_JOBSTREET_Resume.docx (+ PDF paket
# lamaran 16 halaman, diterima 21 Nov 2026). NIK TIDAK dicatat di mana pun.
PROFIL_CV = {
    "nama_legal": "Masduki",
    "nama_tampil": "Cipta Bintang Lestari",
    "email_daftar": "ciptabintanglestari@gmail.com",
    "email_cv": "kikimtflb@gmail.com",
    "telepon": "+62 81247986994",
    "pendidikan": "Diploma Computer Science/Information Technology, "
                   "Bina Sarana Informatika, lulus 2014",
    "pekerjaan_terkini": "Pemilik Bisnis, PT Mibe Anak Bangsa (Des 2021–sekarang)",
    "riwayat": [
        "Penaksir Emas, PT Gadai MAS (Mei 2021–Jul 2023)",
        "Surveyor, PT Mandiri Tunas Finance (Jun 2017–Jan 2020)",
        "Marketing, Bank Mandiri (Okt 2014–Mar 2017)",
        "Telemarketing, PT CIMB Niaga (Mei 2012–Mar 2013)",
    ],
    "keahlian": ["Microsoft Office", "Canva", "Akuntansi", "Adobe Dreamweaver",
                 "Bahasa Pemrograman", "Membangun Tim", "Memecahkan Masalah"],
    "bahasa": ["Bahasa Indonesia", "Inggris"],
    "portofolio": "https://podcastmeong.github.io/toko.html",
}

# Draf bio profil (versi bagus — ditulis dari CV + portofolio nyata, bukan
# salin mentah). Angka portofolio: toko 129 aplikasi, 12 eBook, 7 game
# (rekonsiliasi 21 Nov 2026: toko 171 vs katalog 170 — selisih hanya kartu
# "Aplikasi Sesuai Kebutuhan" di toko, bukan entri katalog).
# Angka ini JUGA tersimpan di data/A28_config.json — modul ini membaca
# file itu tiap kali dijalankan (_muat_config di bawah), jadi bio bisa
# diperbarui tanpa mengedit modul ini.
BIO_ID = (
    "Saya Masduki (Cipta Bintang Lestari), pembuat aplikasi dan konten digital "
    "dari Jakarta Selatan. Saya membangun aplikasi bisnis siap pakai — kasir toko, "
    "klinik & apotek, gudang, akuntansi, HRD, sekolah, restoran, laundry — dalam "
    "satu file yang mudah dipakai, lengkap dengan panduan dan garansi perbaikan bug. "
    "Di toko saya sendiri sudah ada 129 aplikasi, 12 eBook, dan 7 game, plus ratusan "
    "video podcast komedi kucing \"Podcast Meong\" (Oyen & Momo) di YouTube, TikTok, "
    "dan Instagram. Saya juga membuat video promo AI 15/30/60 detik, desain poster, "
    "serta menulis puisi, cerpen, dan eBook. Yang saya tawarkan: hasil jadi yang bisa "
    "langsung dipakai, komunikasi cepat, revisi jelas, dan harga transparan di depan."
)

BIO_EN = (
    "Hi, I'm Masduki (Cipta Bintang Lestari), an app builder and digital content "
    "creator from South Jakarta, Indonesia. I build ready-to-use business apps — "
    "point-of-sale, clinic & pharmacy systems, warehouse, accounting, HR, school, "
    "restaurant, laundry — delivered as a single easy-to-use file, complete with a "
    "user guide and a bug-fix warranty. My own store already lists 129 apps, 12 eBooks, "
    "and 7 games, plus hundreds of AI comedy cat videos (\"Podcast Meong\", starring "
    "Oyen & Momo) on YouTube, TikTok, and Instagram. I also create 15/30/60-second AI "
    "promo videos, digital posters, and write poetry, short stories, and eBooks. What "
    "you get from me: a finished product you can use right away, fast communication, "
    "clear revisions, and transparent pricing upfront."
)


def _muat_config():
    """Baca data/A28_config.json (DeepSeek: bio ke file konfigurasi,
    agen baca tiap kali dijalankan, jangan hardcode).

    Bila file ada dan berisi bio_id/bio_en, timpa konstanta BIO_ID/
    BIO_EN di atas. Bila file hilang/rusak, pakai konstanta di atas
    (fallback) dan kembalikan False. Tidak pernah melempar error.
    """
    global BIO_ID, BIO_EN
    try:
        # CATATAN: di modul ini BASE sudah menunjuk ke folder data
        # (BASE = .../pusat-komando/data), jadi langsung BASE / file.
        cfg = json.loads((BASE / "A28_config.json").read_text(
            encoding="utf-8"))
    except Exception:
        return False
    bio_id = (cfg.get("bio_id") or "").strip()
    bio_en = (cfg.get("bio_en") or "").strip()
    if bio_id:
        BIO_ID = bio_id
    if bio_en:
        BIO_EN = bio_en
    return bool(bio_id or bio_en)


_MUAT_CONFIG_OK = _muat_config()

# PANDUAN CAPTCHA — bila CAPTCHA tidak bisa dilewati: BERHENTI, jangan diulang
# berkali-kali (risiko akun terkunci), eskalasi ke Cipta. CAPTCHA, kode SMS,
# dan unggah KTP/foto diri HANYA dilakukan Cipta sendiri.
PANDUAN_CAPTCHA = {
    "Sribu": "Daftar pakai email (tombol Google tidak ditemukan). Tidak ada CAPTCHA "
             "di formulir daftar; verifikasi lewat email.",
    "Projects.co.id": "Formulir daftar ADA CAPTCHA (soal bergambar, mis. nama tarian "
                      "tradisional). Bila soal tidak terbaca: coba sekali lagi; bila tetap "
                      "gagal, BERHENTI dan minta Cipta membacakan jawabannya. Jangan tebak "
                      "berulang kali.",
    "Fiverr": "Daftar via Google — biasanya tanpa CAPTCHA. Verifikasi ID (KTP + selfie) "
              "terbuka SETELAH Gig pertama terbit; tenggat 14 hari.",
    "Upwork": "Daftar via Google — biasanya tanpa CAPTCHA. Verifikasi identitas KTP bila "
              "diminta; batas 7 hari setelah diminta.",
    "Freelancer.com": "Daftar via Google/Facebook/email. KYC paling berat: KTP harus "
                      "diterjemahkan ke Inggris + dilegalisasi notaris; foto keycode + "
                      "bukti alamat.",
}

# CHECKLIST pembuatan akun per platform — ringkasan dari
# ~/workspace/your_files/oyen-podcast/pendaftaran-freelance-a28.md (§6).
# Urutan disarankan: 1) Sribu + Projects.co.id, 2) Fiverr, 3) Upwork, 4) Freelancer.com.
CHECKLIST_AKUN = {
    "umum": ["Pakai email ciptabintanglestari@gmail.com untuk SEMUA platform",
             "Tombol 'Continue with Google' bila tersedia; jangan buat email baru",
             "Nama legal Masduki (sesuai KTP) di semua verifikasi; "
             "nama tampil 'Cipta Bintang Lestari'",
             "Satu orang satu akun per platform — jangan pernah buat akun kedua"],
    "Sribu": ["Daftar sebagai Freelancer (email + kata sandi)",
              "Klik tautan verifikasi email",
              "Lengkapi profil + min 4 portofolio + KTP",
              "Tunggu kurasi tim Sribu"],
    "Projects.co.id": ["Register (email, username, CAPTCHA)",
                       "Aktivasi lewat email",
                       "Lengkapi profil (self introduction ID)",
                       "Unggah foto KTP + selfie memegang KTP (wajib untuk bid & tarik dana)"],
    "Fiverr": ["Join via Google",
               "Become a Seller (nama tampil 'Cipta Bintang Lestari', bio EN)",
               "Verifikasi telepon SMS",
               "Buat Gig pertama di DESKTOP",
               "Verifikasi ID setelah Gig terbit (14 hari)"],
    "Upwork": ["Sign up via Google",
               "Pilih 'I'm a freelancer looking for work'",
               "Isi nama legal Masduki, alamat sesuai KTP, foto wajah, tarif $10/jam, ringkasan EN",
               "Verifikasi telepon SMS",
               "Verifikasi identitas KTP bila diminta (7 hari)",
               "Tunggu persetujuan profil"],
    "Freelancer.com": ["Sign up via Google",
                       "Lengkapi profil EN",
                       "KYC: KTP terjemahan Inggris + legalisasi, foto keycode, bukti alamat",
                       "Tunggu review 2–3 hari kerja"],
}

# KRITERIA PILIH LOWONGAN (Cipta, 21 Nov 2026 10:32, DIPERKETAT 10:35):
# HANYA yang MUDAH saja — yang sedang/sulit JANGAN diambil.
# Yang MUDAH (boleh diambil): video promo AI 15/30/60 detik, poster/desain
# sederhana, foto AI, tugas kecil satu file.
# TRANSLATE DITUNDA (Cipta, 21 Nov 2026 11:37: "Translate lewat dulu"):
# lowongan translate JANGAN diambil sampai Cipta bilang jalan.
# Yang JANGAN diambil: aplikasi/website standar ke atas, game, eBook besar,
# proyek yang butuh teknologi yang tidak dikuasai, butuh tim besar,
# butuh sertifikat/izin khusus, atau tenggat mustahil.
KRITERIA_LOWONGAN = {
    "bisa": ["video promo AI 15/30/60 detik", "poster/desain sederhana",
             "foto AI", "tugas kecil satu file",
             "jasa ngetik", "copywriter"],
    "ditunda": ["translate bahasa (Cipta 21 Nov 2026 11:37: lewat dulu)"],
    "prioritas": ["mudah saja — yang sedang/sulit jangan diambil"],
    "jangan_ambil": ["aplikasi/website standar ke atas", "game",
                     "eBook besar", "teknologi yang tidak dikuasai",
                     "butuh tim besar", "butuh sertifikat/izin khusus",
                     "tenggat mustahil"],
}


# SKILL BARU 21 Nov 2026 (lanjutan, tinjauan peninjau skill) — TARIF PASAR
# RISET untuk 3 jasa baru di KRITERIA_LOWONGAN ("bisa"). Hasil riset
# 21 Nov 2026. Ini TARIF PASAR RISET — BUKAN harga jual kita dan BUKAN
# janji penghasilan. Harga jual kita tetap diputuskan Cipta per pekerjaan.
TARIF_PASAR_RISET_2026 = {
    "jasa_ngetik": {"sumber": "Sribu (pasar lokal)",
                    "tarif": "Mulai Rp99.000/paket; Rp3.000–5.000/halaman",
                    "catatan": "Tarif pasar riset — bukan harga jual kita."},
    "copywriter": {"sumber": "Upwork (pasar global, pemula)",
                   "tarif": "US$10–30/jam",
                   "catatan": "Tarif pasar riset — bukan harga jual kita."},
    "translate_bahasa": {"sumber": "Pasar global, pemula",
                         "tarif": "US$0,06–0,12/kata; pasangan Inggris–Indonesia "
                                  "US$0,04–0,12/kata",
                         "catatan": "Tarif pasar riset — bukan harga jual kita. "
                                    "Pekerjaan translate sendiri DITUNDA dulu "
                                    "(perintah Cipta 21 Nov 2026 10:44)."},
}


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


def _draf_dasar(jenis, judul):
    draf = {"status": "draf", "butuh_persetujuan": True, "agent": KODE,
            "nama_agent": NAMA, "jenis": jenis, "judul": judul,
            "mode": mode_ai(), "tanggal": date.today().isoformat(),
            "catatan": "DRAF — wajib diperiksa dan disetujui Cipta sebelum dipakai/dikirim."}
    try:
        if not os.environ.get("PK_NO_LOG"):
            from dashboard import log_activity
            log_activity(KODE, "buat draf: " + jenis, judul)
    except Exception:
        pass
    return draf


def _polish(teks, pakai_ai=False):
    """Bila pakai_ai=True dan ada key, minta Gemini memperbaiki draf tanpa mengubah fakta/harga/tautan/angka."""
    if not pakai_ai or not (teks or "").strip():
        return None
    return gemini_ask("Perbaiki draf berikut tanpa mengubah fakta, harga, tautan, atau angka. "
                      "Jangan tambah janji views/viral/penjualan. Jangan karang klien, penghasilan, atau rating.\n\n" + teks)


def cek_draf(teks):
    """Periksa teks draf: kata terlarang + teks kosong. Kembalikan daftar masalah (kosong = bersih)."""
    masalah = []
    t = (teks or "")
    if not t.strip():
        masalah.append("Teks draf kosong.")
        return masalah
    rendah = t.lower()
    for kata in KATA_TERLARANG:
        if kata in rendah:
            masalah.append("Kata terlarang: '{}'".format(kata))
    return masalah


def info():
    """Metadata agent (untuk tes + tab Pusat Komando)."""
    return {"kode": KODE, "nama": NAMA, "divisi": DIVISI, "atasan": ATASAN,
            "job_desc": JOB_DESC, "dipetakan_ke": DIPETAKAN_KE, "status": STATUS,
            "gemini_divisi": GEMINI_DIVISI, "gemini_peran": GEMINI_PERAN,
            "gemini_kpi": list(GEMINI_KPI), "gemini_tools": list(GEMINI_TOOLS),
            "pasif": True}


def ringkasan():
    """Ringkasan status agent."""
    d = info()
    d["mode"] = mode_ai()
    d["catatan"] = ("Agent pasif — dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri. "
                    "Semua output DRAF untuk persetujuan Cipta.")
    return d

def simpan_profil_memori():
    """Simpan profil freelance (PROFIL_CV + BIO_ID + BIO_EN) ke memori bersama
    supaya agen lain (A25/A35/A36) membaca profil yang SAMA — tidak ada
    versi bio yang berbeda-beda di tiap agen. Kembalikan True bila ketiganya
    tersimpan, False bila memori tidak tersedia."""
    if MEMORI is None:
        return False
    ok1 = MEMORI.simpan("A28", "profil_freelance", "profil:cv", PROFIL_CV,
                        sumber="CV Cipta (MDUKI_JOBSTREET_Resume.docx)")
    ok2 = MEMORI.simpan("A28", "profil_freelance", "profil:bio_id", BIO_ID,
                        sumber="CV Cipta — bio Indonesia")
    ok3 = MEMORI.simpan("A28", "profil_freelance", "profil:bio_en", BIO_EN,
                        sumber="CV Cipta — bio Inggris")
    return bool(ok1 and ok2 and ok3)


def baca_profil_memori():
    """Baca profil freelance dari memori bersama (yang disimpan A28).
    Kembalikan dict {kunci: nilai}; dict kosong = belum ada profil di memori."""
    if MEMORI is None:
        return {}
    rows = MEMORI.baca(jenis="profil_freelance", limit=10)
    return {r["kunci"]: r.get("nilai") for r in rows}


def nilai_peluang_draf(teks, nama=""):
    """Nilai peluang lomba/freelance dari teks aturannya (DRAF).
    Delegasi ke A6 (a06 nilai_lomba) bila tersedia."""
    draf = _draf_dasar("nilai_peluang", "Penilaian peluang: {}".format((nama or "").strip() or "?"))
    penilaian = None
    try:
        import a06_lomba as A06
        penilaian = A06.nilai_lomba(teks, nama)
    except Exception:
        penilaian = None
    if not penilaian:
        draf["penilaian"] = "belum cukup data — tempel teks aturan lomba (minimal 20 karakter)."
    else:
        draf["penilaian"] = penilaian
    draf["catatan"] = ("Agent TIDAK PERNAH mendaftar/mengirim. Bila layak, tetap tunggu "
                       "persetujuan Cipta atas lomba dan karya persisnya.")
    draf["target_rancangan_gemini"] = GEMINI_KPI
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return nilai_peluang_draf("Lomba video AI gratis, boleh AI, hadiah Rp1.000.000, pendaftaran sampai 31 Desember 2026, terbuka untuk umum di Indonesia.", "Lomba Video AI")


# ===========================================================================
# SKILL SRIBU (21 Nov 2026 ~14:12, perintah Cipta: "Ini perlu agent.ai
# khusus untuk mengerjakan ini", "Tingkatkan Dan pasang skill",
# "Yang memory sudah di pasang kan", "Jadi g suka lupa lagi").
# Agen khusus Sribu: semua fungsi DRAF-only. Modul ini TIDAK PUNYA fungsi
# kirim / bayar / publikasi / submit / upload — sengaja. Setiap draf wajib
# diperiksa dan disetujui Cipta sebelum dipakai/dikirim.
# Status akun Sribu TERVERIFIKASI via browser 21 Nov 2026 13:24-13:31:
# login berhasil (Masduki, username CiptaBintangLestari,
# ciptabintanglestari@gmail.com), saldo Rp0, profil 33% (Step 1 selesai;
# Step 2 "Buat Gigs Pertamamu" + Step 3 "Atur Pembayaran" BELUM;
# KTP sudah terunggah; status kurasi TIDAK terkonfirmasi).
# Hari itu 0 Job Post buka. Upwork DILEWATI (Cipta 21 Nov 14:04 + 14:09)
# — skill ini HANYA untuk Sribu.
# ===========================================================================

# Harga JASA YANG SUDAH DIPUTUSKAN Cipta (jangan karang harga baru):
# video promo 15 dtk Rp75.000 / 30 dtk Rp150.000 / 60 dtk Rp250.000;
# poster Rp35.000/poster. Jasa ngetik/copywriter BELUM ada harga jual
# yang diputuskan (hanya tarif pasar riset) — draf memakai kalimat
# "tarif dibicarakan per paket".
HARGA_JASA_DIPUTUSKAN = {
    "video_promo_15dtk": 75000,
    "video_promo_30dtk": 150000,
    "video_promo_60dtk": 250000,
    "poster": 35000,
}
PORTOFOLIO_URL = "https://podcastmeong.github.io/toko.html"

# Status awal akun Sribu — fakta terverifikasi 21 Nov 2026 13:24-13:31.
STATUS_SRIBU_AWAL = {
    "platform": "Sribu",
    "login": True,
    "nama_tampil": "Masduki",
    "username": "CiptaBintangLestari",
    "email": "ciptabintanglestari@gmail.com",
    "saldo_rp": 0,
    "proyek_berjalan": 0,
    "profil_persen": 33,
    "step_1_lengkapi_profile": True,
    "step_2_buat_gigs": False,
    "step_3_atur_pembayaran": False,
    "ktp_terunggah": True,
    "kurasi_terkonfirmasi": False,
    "kurasi_catatan": "Tidak ada label lolos kurasi di Workspace maupun profil.",
    "lowongan_buka_hari_ini": 0,
    "lowongan_buka_tanggal": "2026-11-21",
    "terakhir_diperbarui": "2026-11-21 13:31 WIB",
    "sumber": "Verifikasi browser Muse 21 Nov 2026 13:24-13:31",
}

# 5 draf yang SUDAH ADA (dibuat via browser 21 Nov 2026 13:24-13:31 dari
# file draf-proposal-sribu-2026-11-21.md). Dicatat apa adanya: SEMUA
# lowongan sumbernya SUDAH TUTUP saat draf dibuat (status Pemilihan
# Pemenang / Ditutup / Transfer File). Draf 5 (website standar) TIDAK
# cocok dengan KRITERIA_LOWONGAN yang diperketat (hanya MUDAH) — disimpan
# sebagai arsip, bukan untuk dipakai.
DRAF_SRIBU_AWAL = [
    {"id": "SRB-20261121-01", "judul": "Video Editor Reels Restoran (Paid Per Reel)",
     "lowongan_judul": "Job Post untuk Freelance Video Editor — Restaurant Social Media Reels (Paid Per Reel)",
     "lowongan_budget": "mulai Rp800.000", "lowongan_status": "Pemilihan Pemenang",
     "lowongan_tautan": "https://www.sribu.com/id/contests-bid/66d244bd-78c0-4341-9d04-bdd5f3156b65",
     "jenis": "video promo AI",
     "teks": ("Halo, saya Masduki (Cipta Bintang Lestari), pembuat video promo AI dan konten video. "
              "Saya bisa membuat reels restoran yang cepat, menarik, dan siap tayang di IG/TikTok, lengkap dengan teks, musik, dan potongan yang rapi. "
              "Tarif saya: video promo 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000. "
              "Saya sudah membuat ratusan video Podcast Meong (Oyen & Momo) di YouTube, TikTok, dan Instagram. "
              "Contoh aplikasi dan karya saya: https://podcastmeong.github.io/toko.html. "
              "Saya siap kirim contoh video 15 detik terlebih dahulu dan revisi sesuai arahan Anda. Terima kasih."),
     "evaluasi": "cocok", "tanggal": "2026-11-21"},
    {"id": "SRB-20261121-02", "judul": "Editor + Content Planner (jangka panjang, IG/TikTok harian)",
     "lowongan_judul": "Job Post untuk Editor + Content Planner — Kerja Jangka Panjang (min. 6 bulan), Konten Harian IG/TikTok",
     "lowongan_budget": "mulai Rp800.000", "lowongan_status": "Pemilihan Pemenang",
     "lowongan_tautan": "https://www.sribu.com/id/contests-bid/b2acfaef-3c8e-4987-ac5e-e55aceda3604",
     "jenis": "video promo AI",
     "teks": ("Halo, saya Masduki (Cipta Bintang Lestari). Saya bisa membantu sebagai editor + content planner harian untuk IG/TikTok: "
              "merencanakan tema konten, mengedit video pendek, dan menjaga jadwal posting tetap konsisten. "
              "Tarif video promo saya: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000; "
              "untuk kerja harian jangka panjang, tarif dapat dibicarakan per paket bulanan. "
              "Pengalaman saya: ratusan video Podcast Meong dan 70+ aplikasi bisnis. "
              "Portofolio: https://podcastmeong.github.io/toko.html. Saya komunikatif, cepat, dan siap bekerja jangka panjang. Terima kasih."),
     "evaluasi": "cocok", "tanggal": "2026-11-21"},
    {"id": "SRB-20261121-03", "judul": "Content Creator Video AI",
     "lowongan_judul": "Content Creator Video AI",
     "lowongan_budget": "mulai Rp1.200.000", "lowongan_status": "Ditutup",
     "lowongan_tautan": "https://www.sribu.com/id/contests-bid/c72be30c-ec44-4ae7-a14d-06ab1b708f4f",
     "jenis": "video promo AI",
     "teks": ("Halo, saya Masduki (Cipta Bintang Lestari), pembuat video promo AI. Saya bisa membuat video AI 15/30/60 detik "
              "yang jelas, menarik, dan sesuai pesan brand Anda. Tarif saya: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000. "
              "Saya juga membuat desain poster Rp35.000/poster bila dibutuhkan. "
              "Portofolio dan toko karya saya: https://podcastmeong.github.io/toko.html, plus ratusan video Podcast Meong di YouTube, TikTok, dan Instagram. "
              "Saya siap membuat contoh singkat dulu sebelum lanjut ke versi final. Terima kasih."),
     "evaluasi": "cocok", "tanggal": "2026-11-21"},
    {"id": "SRB-20261121-04", "judul": "Reels TikTok & Instagram (travel)",
     "lowongan_judul": "Job Post for Creating reels for tiktok and instagram from my video and photo's for verdi.traveling",
     "lowongan_budget": "mulai Rp800.000", "lowongan_status": "Ditutup",
     "lowongan_tautan": "https://www.sribu.com/id/contests-bid/adbc7c0f-9c4e-4a0a-9f71-1fb27951872e",
     "jenis": "video promo AI",
     "teks": ("Halo, saya Masduki (Cipta Bintang Lestari). Saya bisa mengubah video dan foto perjalanan Anda menjadi reels TikTok/Instagram "
              "yang enak ditonton: potongan cepat, musik yang pas, dan teks yang jelas. "
              "Tarif video promo saya: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000. "
              "Contoh video saya: ratusan video Podcast Meong di YouTube, TikTok, dan Instagram. "
              "Portofolio: https://podcastmeong.github.io/toko.html. Silakan kirim bahan video/fotonya, saya buatkan contoh reels terlebih dahulu. Terima kasih."),
     "evaluasi": "cocok", "tanggal": "2026-11-21"},
    {"id": "SRB-20261121-05", "judul": "Website Kumpulan Doa Katolik Digital (website standar)",
     "lowongan_judul": "Job Post untuk Pembuatan Website Kumpulan Doa Katolik Digital",
     "lowongan_budget": "mulai Rp1.360.000", "lowongan_status": "Transfer File",
     "lowongan_tautan": "https://www.sribu.com/id/contests-bid/10912a90-f5f2-4bd5-8c5a-7ce66cfc2bd3",
     "jenis": "website standar",
     "teks": ("Halo, saya Masduki (Cipta Bintang Lestari), pembuat aplikasi web & game bisnis. Saya bisa membuat website standar yang rapi, "
              "mudah dibuka di HP, dan mudah dipakai — termasuk website kumpulan konten/doa seperti ini. "
              "Saya sudah menerbitkan 70+ aplikasi bisnis dalam satu file yang mudah dipakai, lengkap dengan panduan dan garansi perbaikan bug. "
              "Harga website/aplikasi bisnis dihitung per proyek, disesuaikan dengan jumlah halaman dan fiturnya. "
              "Portofolio: https://podcastmeong.github.io/toko.html. Saya siap mendiskusikan struktur halaman dan contoh tampilannya terlebih dahulu. Terima kasih."),
     "evaluasi": "tidak_cocok_kriteria_ketat",
     "evaluasi_catatan": ("Arsip saja — website standar TIDAK masuk KRITERIA_LOWONGAN (hanya MUDAH, 21 Nov 10:35). "
                          "Draf dibuat 21 Nov 13:24 dari lowongan yang sudah tutup. Jangan dipakai tanpa persetujuan Cipta."),
     "tanggal": "2026-11-21"},
]

# Kata kunci penilaian lowongan (diturunkan dari KRITERIA_LOWONGAN).
_KUNCI_BISA = {
    "video promo AI": ["video promo", "reels", "video ai", "video editor", "content creator video",
                       "shorts", "tiktok", "instagram", "edit video"],
    "poster/desain sederhana": ["poster", "desain sederhana", "flyer", "desain grafis sederhana"],
    "foto AI": ["foto ai", "foto produk ai", "gambar ai"],
    "tugas kecil satu file": ["tugas kecil", "ketik", "data entry sederhana"],
    "jasa ngetik": ["ngetik", "pengetikan", "ketik dokumen", "transkrip ketik"],
    "copywriter": ["copywriter", "copywriting", "tulis caption", "penulis konten"],
}
_KUNCI_JANGAN = ["aplikasi", "website", "game", "ebook", "tim besar", "sertifikat",
                 "izin khusus", "lisensi", "tenggat mustahil", "deadline mustahil",
                 "teknologi", "framework", "backend", "api", "database", "server"]
_KUNCI_DITUNDA = ["translate", "terjemah", "penerjemah"]

# AGEN PENDUKUNG PER JENIS LOWONGAN (perintah Cipta 21 Nov 2026 19:35:
# bila A28 dapat lowongan, SEMUA support membantunya. Field "dukungan"
# diisi otomatis di _simpan_draf; routing lama tetap berlaku: ngetik
# -> A35, copywriter -> A36. A26 (Customer Service) bila perlu.)
DUKUNGAN_PER_JENIS = {
    "jasa ngetik": ["A35"],
    "tugas kecil satu file": ["A35"],
    "copywriter": ["A36"],
    "video promo AI": ["A11"],
    "poster/desain sederhana": ["A12"],
    "foto AI": ["A12"],
}
DUKUNGAN_UMUM = ["A06", "A10"]  # riset + validator, untuk jenis lain


def _file_draf_sribu():
    return BASE / "draf_sribu.json"


def _file_status_sribu():
    return BASE / "sribu_status.json"


def _file_log_sribu():
    return BASE / "log_a28_sribu.json"


def _muat_json(path, default):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, type(default)) else default
    except Exception:
        return default


def _simpan_json(path, data):
    try:
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        return True
    except Exception:
        return False


def status_sribu():
    """Kembalikan status akun Sribu saat ini.

    Sumber: memori bersama (jenis 'sribu', kunci 'sribu:status') bila ada;
    bila kosong, pakai STATUS_SRIBU_AWAL (fakta terverifikasi 21 Nov 2026)
    dan simpan ke memori + data/sribu_status.json supaya tidak lupa.
    Tidak pernah melempar error; selalu kembalikan dict.
    """
    status = None
    if MEMORI is not None:
        try:
            rows = MEMORI.baca(kunci="sribu:status", jenis="sribu", limit=1)
            if rows:
                nilai = rows[0].get("nilai")
                if isinstance(nilai, dict):
                    status = dict(nilai)
        except Exception:
            status = None
    if status is None:
        status = _muat_json(_file_status_sribu(), None)
    if status is None:
        status = dict(STATUS_SRIBU_AWAL)
    status["jumlah_draf"] = len(daftar_draf())
    return status


def simpan_status_sribu(status=None):
    """Simpan status akun Sribu ke memori bersama DAN data/sribu_status.json.

    Bila status None, simpan status saat ini (status_sribu()). Kembalikan
    True bila minimal satu tujuan tersimpan."""
    if status is None:
        status = status_sribu()
    status = dict(status)
    status["terakhir_diperbarui"] = date.today().isoformat()
    ok_file = _simpan_json(_file_status_sribu(), status)
    ok_memori = False
    if MEMORI is not None:
        try:
            ok_memori = bool(MEMORI.simpan("A28", "sribu", "sribu:status",
                                            status,
                                            sumber="A28 — status akun Sribu terverifikasi"))
        except Exception:
            ok_memori = False
    return bool(ok_file or ok_memori)


def nilai_lowongan(lowongan):
    """Nilai kecocokan lowongan dengan KRITERIA_LOWONGAN (hanya MUDAH).

    lowongan: dict {judul, deskripsi, budget, jenis, tautan}.
    Kembalikan dict {cocok: bool, skor: 0-10, jenis_cocok, alasan: [str]}.
    Tolak: translate (ditunda Cipta 21 Nov 11:37), aplikasi/website/game/
    eBook, tim besar, sertifikat/izin khusus, tenggat mustahil, teknologi
    yang tidak dikuasai. Tidak pernah mengarang — bila judul/deskripsi
    kosong, kembalikan tidak cocok dengan alasan 'belum cukup data'."""
    hasil = {"cocok": False, "skor": 0, "jenis_cocok": "", "alasan": []}
    judul = str((lowongan or {}).get("judul") or "").strip()
    deskripsi = str((lowongan or {}).get("deskripsi") or "").strip()
    if not judul and not deskripsi:
        hasil["alasan"].append("belum cukup data — judul dan deskripsi lowongan kosong.")
        return hasil
    teks = (judul + " " + deskripsi).lower()
    for kata in _KUNCI_DITUNDA:
        if kata in teks:
            hasil["alasan"].append("DITUNDA — lowongan translate, jangan diambil dulu (perintah Cipta 21 Nov 11:37).")
            return hasil
    for kata in _KUNCI_JANGAN:
        if kata in teks:
            hasil["alasan"].append("Tolak — mengandung '{}' (bukan lowongan MUDAH).".format(kata))
            return hasil
    for jenis, kunci_list in _KUNCI_BISA.items():
        cocok_kunci = [k for k in kunci_list if k in teks]
        if cocok_kunci:
            hasil["cocok"] = True
            hasil["jenis_cocok"] = jenis
            hasil["skor"] = min(10, 5 + len(cocok_kunci))
            hasil["alasan"].append("Cocok: {} (kata kunci: {}).".format(jenis, ", ".join(cocok_kunci)))
            return hasil
    hasil["alasan"].append("Tidak cocok — tidak ada kata kunci jasa MUDAH (video promo/poster/foto AI/ngetik/copywriter).")
    return hasil


def _simpan_draf(draf):
    """Simpan satu draf ke data/draf_sribu.json DAN memori bersama.
    Kembalikan True bila minimal satu tujuan tersimpan."""
    draf = dict(draf)
    draf.setdefault("status", "draf")
    draf.setdefault("butuh_persetujuan", True)
    draf.setdefault("info_cipta", False)
    draf.setdefault("tanggal", date.today().isoformat())
    draf.setdefault("dukungan",
                    DUKUNGAN_PER_JENIS.get(draf.get("jenis"), DUKUNGAN_UMUM))
    semua = _muat_json(_file_draf_sribu(), [])
    semua = [d for d in semua if d.get("id") != draf.get("id")]
    semua.append(draf)
    ok_file = _simpan_json(_file_draf_sribu(), semua)
    ok_memori = False
    if MEMORI is not None:
        try:
            ok_memori = bool(MEMORI.simpan("A28", "sribu_draf",
                                            "draf:{}".format(draf.get("id", "?")),
                                            draf,
                                            sumber="A28 — draf proposal Sribu (DRAF, belum dikirim)"))
        except Exception:
            ok_memori = False
    return bool(ok_file or ok_memori)


def draf_dari_lowongan(lowongan):
    """Buat draf proposal Sribu dari satu lowongan (DRAF saja, tidak dikirim).

    Menilai dulu dengan nilai_lowongan(); bila tidak cocok, kembalikan
    penolakan beralasan TANPA membuat draf. Bila cocok, buat teks draf dari
    template + harga jasa yang sudah diputuskan, periksa kata terlarang
    dengan cek_draf(), simpan ke data + memori, kembalikan draf + skor."""
    penilaian = nilai_lowongan(lowongan or {})
    if not penilaian["cocok"]:
        return {"status": "ditolak", "penilaian": penilaian,
                "catatan": "Tidak dibuat draf — lowongan tidak memenuhi KRITERIA_LOWONGAN (hanya MUDAH)."}
    judul = str((lowongan or {}).get("judul") or "").strip()
    jenis = penilaian["jenis_cocok"]
    budget = str((lowongan or {}).get("budget") or "").strip()
    tautan = str((lowongan or {}).get("tautan") or "").strip()
    draf_id = "SRB-{}-{:02d}".format(date.today().strftime("%Y%m%d"),
                                     len(daftar_draf()) + 1)
    if jenis == "video promo AI":
        layanan = ("Saya bisa membuat video promo AI 15/30/60 detik yang jelas, menarik, dan sesuai pesan brand Anda. "
                   "Tarif saya: video promo 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000.")
    elif jenis == "poster/desain sederhana":
        layanan = "Saya bisa membuat desain poster sederhana. Tarif saya: Rp35.000/poster (file digital)."
    elif jenis == "foto AI":
        layanan = "Saya bisa membuat foto AI untuk kebutuhan promosi Anda. Tarif dibicarakan per paket."
    elif jenis in ("jasa ngetik", "copywriter"):
        layanan = ("Saya bisa membantu {}. Tarif dibicarakan per paket "
                   "(harga jual belum diputuskan — jangan tawar harga pasti dulu).".format(
                       "mengetik dokumen Anda" if jenis == "jasa ngetik"
                       else "menulis teks/copywriting Anda"))
    else:
        layanan = "Saya bisa membantu pekerjaan ini. Tarif dibicarakan per paket."
    teks = ("Halo, saya Masduki (Cipta Bintang Lestari), pembuat aplikasi dan konten digital dari Jakarta Selatan. "
            + layanan + " "
            "Pengalaman saya: ratusan video Podcast Meong (Oyen & Momo) di YouTube, TikTok, dan Instagram, "
            "serta 70+ aplikasi bisnis. Portofolio: {}. "
            "Saya siap membuat contoh singkat terlebih dahulu sebelum lanjut ke versi final. Terima kasih.".format(PORTOFOLIO_URL))
    masalah = cek_draf(teks)
    if masalah:
        return {"status": "gagal", "penilaian": penilaian, "masalah": masalah,
                "catatan": "Draf gagal pemeriksaan kata terlarang — tidak disimpan."}
    draf = {"id": draf_id, "judul": judul or jenis, "lowongan_judul": judul,
            "lowongan_budget": budget, "lowongan_status": "buka",
            "lowongan_tautan": tautan, "jenis": jenis, "teks": teks,
            "evaluasi": "cocok", "tanggal": date.today().isoformat(),
            "status": "draf", "butuh_persetujuan": True,
            "info_cipta": True,
            "skor": penilaian["skor"],
            "dukungan": DUKUNGAN_PER_JENIS.get(jenis, DUKUNGAN_UMUM),
            "catatan": "DRAF — wajib diperiksa dan disetujui Cipta sebelum dipakai/dikirim. INFO DULU: kabari Cipta tentang lowongan ini sebelum langkah lain."}
    _simpan_draf(draf)
    return {"status": "draf", "draf": draf, "penilaian": penilaian}


def daftar_draf(status=None):
    """Daftar semua draf Sribu yang tersimpan (data/draf_sribu.json + memori).

    Gabung keduanya berdasarkan id; bila satu sumber hilang, sumber lain
    tetap dipakai supaya draf tidak hilang/lupa. Kembalikan list dict
    (diurutkan berdasarkan id). status: bila diisi (mis. "draf" atau
    "diterima"), hanya draf dengan status itu yang dikembalikan."""
    gabung = {}
    for d in _muat_json(_file_draf_sribu(), []):
        if isinstance(d, dict) and d.get("id"):
            gabung[d["id"]] = d
    if MEMORI is not None:
        try:
            for r in MEMORI.baca(jenis="sribu_draf", limit=100):
                nilai = r.get("nilai")
                if isinstance(nilai, dict) and nilai.get("id"):
                    gabung.setdefault(nilai["id"], nilai)
        except Exception:
            pass
    semua = [gabung[k] for k in sorted(gabung)]
    if status is not None:
        semua = [d for d in semua if d.get("status") == status]
    return semua


def daftar_perlu_info():
    """Draf lowongan COCOK yang baru dan BELUM diinfo ke Cipta.

    Yaitu draf dengan info_cipta=True. Muse yang menjalankan engine WAJIB
    mengabari Cipta tentang draf ini di chat SEBELUM langkah lain, lalu
    tandai_diinfo(). Draf lama (tanpa field info_cipta) dianggap sudah
    diinfo — tidak masuk daftar ini."""
    return [d for d in daftar_draf() if d.get("info_cipta") is True]


def daftar_diterima():
    """Draf lowongan yang sudah DITERIMA Cipta (status 'diterima')."""
    return daftar_draf(status="diterima")


def tandai_diinfo(draf_id):
    """Tandai draf sudah diinfo ke Cipta (info_cipta=False).

    Dipanggil Muse SETELAH mengabari Cipta di chat tentang lowongan itu.
    Kembalikan {"ok": True, "draf": ...} atau {"ok": False, "alasan": ...}.
    Hanya mencatat — tidak mengirim apa pun."""
    for d in daftar_draf():
        if d.get("id") == draf_id:
            d = dict(d)
            d["info_cipta"] = False
            d["diinfo_tanggal"] = date.today().isoformat()
            _simpan_draf(d)
            return {"ok": True, "draf": d}
    return {"ok": False, "alasan": "Draf {} tidak ditemukan.".format(draf_id)}


def tandai_diterima(draf_id, catatan=""):
    """Tandai lowongan DITERIMA Cipta (status draf menjadi 'diterima').

    Dipanggil HANYA setelah Cipta menyetujui/menerima lowongan itu.
    Draf arsip (evaluasi bukan 'cocok') TIDAK bisa ditandai diterima.
    Hanya mencatat — tidak mengirim, tidak membayar, tidak menghubungi
    siapa pun. Kembalikan {"ok": True, "draf": ...} atau
    {"ok": False, "alasan": ...}."""
    for d in daftar_draf():
        if d.get("id") == draf_id:
            if d.get("evaluasi") != "cocok":
                return {"ok": False,
                        "alasan": "Draf {} arsip (evaluasi: {}) — bukan lowongan cocok, jangan ditandai diterima.".format(
                            draf_id, d.get("evaluasi"))}
            d = dict(d)
            d["status"] = "diterima"
            d["info_cipta"] = False
            d["diterima_tanggal"] = date.today().isoformat()
            d["diterima_catatan"] = str(catatan or "")
            _simpan_draf(d)
            return {"ok": True, "draf": d}
    return {"ok": False, "alasan": "Draf {} tidak ditemukan.".format(draf_id)}


def daftarkan_draf_5():
    """Daftarkan ke-5 draf Sribu yang sudah ada (21 Nov 2026) ke data + memori.

    Sumber: DRAF_SRIBU_AWAL (isi file draf-proposal-sribu-2026-11-21.md).
    Idempotent — draf yang sudah terdaftar tidak diduplikasi. Kembalikan
    jumlah draf yang terdaftar setelah pemanggilan."""
    for draf in DRAF_SRIBU_AWAL:
        _simpan_draf(draf)
    return len(daftar_draf())


def jalankan():
    """Rutinitas harian A28 untuk Sribu (dipanggil mesin lewat FUNGSI_JALAN).

    Baca memori -> status_sribu() -> daftar_draf() -> tulis log run
    (tanggal, status, jumlah draf) ke memori + data/log_a28_sribu.json ->
    kembalikan ringkasan teks singkat. Tidak pernah melempar error;
    bila memori tidak tersedia, tetap jalan dari file data/."""
    try:
        status = status_sribu()
    except Exception:
        status = dict(STATUS_SRIBU_AWAL)
    try:
        drafs = daftar_draf()
    except Exception:
        drafs = []
    try:
        perlu_info = daftar_perlu_info()
    except Exception:
        perlu_info = []
    try:
        diterima = daftar_diterima()
    except Exception:
        diterima = []
    try:
        simpan_status_sribu(status)
    except Exception:
        pass
    # INFO DULU (perintah Cipta 21 Nov 2026 19:41): peringatan di AWAL
    # ringkasan supaya terlihat juga di hasil ringkas engine (120 karakter
    # pertama) dan di memori. Muse yang menjalankan engine WAJIB mengabari
    # Cipta tentang draf ini di chat SEBELUM langkah lain.
    peringatan = ""
    if perlu_info:
        peringatan = ("PERLU INFO KE CIPTA: {} lowongan cocok baru ({}) — "
                      "kabari Cipta dulu sebelum langkah lain. ".format(
                          len(perlu_info),
                          ", ".join(d.get("id", "?") for d in perlu_info)))
    if diterima:
        peringatan += ("DITERIMA: {} ({}). ".format(
            len(diterima), ", ".join(d.get("id", "?") for d in diterima)))
    ringkasan = (peringatan +
                 "A28 Sribu {}: login {}; profil {}% (Step 2 gig {}; Step 3 pembayaran {}; kurasi {}); "
                 "lowongan buka hari ini {}; draf tersimpan {} ({} cocok, {} arsip tidak cocok). "
                 "Semua draf menunggu persetujuan Cipta — tidak ada yang dikirim.".format(
                     date.today().isoformat(),
                     "ya" if status.get("login") else "belum",
                     status.get("profil_persen", "?"),
                     "selesai" if status.get("step_2_buat_gigs") else "belum",
                     "selesai" if status.get("step_3_atur_pembayaran") else "belum",
                     "terkonfirmasi" if status.get("kurasi_terkonfirmasi") else "belum terkonfirmasi",
                     status.get("lowongan_buka_hari_ini", "?"),
                     len(drafs),
                     sum(1 for d in drafs if d.get("evaluasi") == "cocok"),
                     sum(1 for d in drafs if d.get("evaluasi") != "cocok")))
    if perlu_info:
        ringkasan += (" Lowongan baru yang perlu diinfo ke Cipta: " +
                      "; ".join("{} — {} (dukungan: {})".format(
                          d.get("id", "?"), d.get("judul", "?"),
                          ", ".join(d.get("dukungan") or []))
                          for d in perlu_info))
    log = {"tanggal": date.today().isoformat(), "agent": KODE,
           "ringkasan": ringkasan, "jumlah_draf": len(drafs),
           "perlu_info_ke_cipta": [d.get("id") for d in perlu_info],
           "diterima": [d.get("id") for d in diterima],
           "profil_persen": status.get("profil_persen"),
           "lowongan_buka_hari_ini": status.get("lowongan_buka_hari_ini")}
    try:
        semua_log = _muat_json(_file_log_sribu(), [])
        semua_log = [l for l in semua_log if l.get("tanggal") != log["tanggal"]]
        semua_log.append(log)
        _simpan_json(_file_log_sribu(), semua_log)
    except Exception:
        pass
    if MEMORI is not None:
        try:
            MEMORI.catat_tugas("A28", "rutinitas harian Sribu", ringkasan, status="selesai")
        except Exception:
            pass
    return ringkasan


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
