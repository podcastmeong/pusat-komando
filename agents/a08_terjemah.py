# ======================================================================
# PUSAT KOMANDO — salinan dari agent-terjemah-inggris (Agent 8 Terjemah Inggris).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Terjemah Podcast Meong — menerjemahkan eBook & artikel Podcast Meong
dari Bahasa Indonesia ke Bahasa Inggris untuk pasar luar negeri
(KDP / Amazon dan Google Play Books global).
Gradio + Gemini free tier + mode panduan lokal.

Cara jalan:
  pip install -r requirements.txt
  python app.py                       # mode panduan saja
  GEMINI_API_KEY=xxx python app.py    # mode AI penuh

ATURAN PALING PENTING — KEJUJURAN TERJEMAHAN:
  - Terjemahan harus SETIA pada naskah asli. Jangan menambah, mengurangi,
    atau mengubah isi cerita.
  - Ayat Al-Quran diterjemahkan dengan terjemahan Inggris yang mapan
    (Sahih International) dan SELALU cantumkan nomor surah:ayat.
    Hanya ayat yang ada di VERSE_BANK (sudah terverifikasi di artikel
    Inggris website) yang boleh dipakai langsung. Ayat lain ditandai
    "PERLU VERIFIKASI" — jangan terjemahkan bebas.
  - Hadis diterjemahkan setia dengan rujukan kitab + nomor yang sama
    seperti aslinya. Jangan mengarang hadis atau mengubah rujukan.
  - Bagian yang meragukan ditandai "PERLU VERIFIKASI", bukan diterjemahkan
    bebas. Semua output adalah DRAF — menunggu persetujuan Cipta sebelum
    diterbitkan.
  - Glosarium di bawah ini DIKUNCI: terjemahan istilah-istilah ini tidak
    boleh berubah antar buku.

  - API key HANYA dari environment variable GEMINI_API_KEY. Jangan pernah
    tulis key di file ini atau di file lain.
  - Terjemahan tersimpan lokal di folder terjemahan/ + progress.json.
    Agent bekerja di bawah komando Muse (Muse mengarahkan, mengoordinasikan,
    dan memeriksa hasil kerja agent); keputusan penting tetap di tangan Cipta.
"""

import datetime
import json
import os
import re

import gradio as gr

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))  # PUSAT KOMANDO: folder data bersama
TERJEMAHAN_DIR = os.path.join(BASE_DIR, "terjemahan")
PROGRESS_FILE = os.path.join(BASE_DIR, "terjemah_progress.json")  # PUSAT KOMANDO

os.makedirs(TERJEMAHAN_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Glosarium TERKUNCI — terjemahan istilah ini tidak boleh berubah antar buku.
# (nama, istilah Islam, judul buku, merek)
# ---------------------------------------------------------------------------

GLOSARIUM = {
    # Nama nabi & tokoh
    "Nabi Nuh": "Prophet Noah",
    "Nabi Ayub": "Prophet Job",
    "Nabi Yusuf": "Prophet Joseph",
    "Nabi Yunus": "Prophet Jonah",
    "Nabi Musa": "Prophet Moses",
    "Nabi Ibrahim": "Prophet Abraham",
    "Nabi Muhammad": "Prophet Muhammad",
    "Abu Bakar": "Abu Bakr",
    "Umar bin Khattab": "Umar ibn al-Khattab",
    "Umar": "Umar",
    "Imam Syafi'i": "Imam Al-Shafi'i",
    "Salahuddin Al-Ayyubi": "Salahuddin Al-Ayyubi",
    "Oyen": "Oyen",
    "Momo": "Momo",
    # Istilah Islam
    "Allah": "Allah",
    "Al-Quran": "the Quran",
    "Al Quran": "the Quran",
    "hadis": "hadith",
    "Hadis": "Hadith",
    "sabar": "patience",
    "Sabar": "Patience",
    "syukur": "gratitude",
    "doa": "prayer",
    "Doa": "Prayer",
    "masjid": "mosque",
    "surga": "Paradise",
    "neraka": "Hellfire",
    "malaikat": "angel",
    "nabi": "prophet",
    "Nabi": "Prophet",
    "rasul": "messenger",
    "Rasul": "Messenger",
    "iman": "faith",
    "taqwa": "God-consciousness",
    "pahala": "reward",
    "dosa": "sin",
    "ampunan": "forgiveness",
    "taubat": "repentance",
    "cobaan": "trial",
    "ujian": "test",
    "rezeki": "provision",
    "berkah": "blessing",
    "shalat": "prayer",
    "Shalat": "Prayer",
    "puasa": "fasting",
    "zakat": "zakat",
    "haji": "Hajj",
    "kaum": "people",
    "bahtera": "ark",
    "Bahtera": "Ark",
    # Judul buku & merek (judul Inggris yang SUDAH terverifikasi di website
    # tidak ditandai; yang masih usulan ditandai "(usulan)" di daftar buku)
    "Si Oyen Penjaga Kolam Ikan": "Oyen the Pond Keeper",
    "Dunia Kiki": "Dunia Kiki",
    "Podcast Meong": "Podcast Meong",
    "KikiWorks": "KikiWorks",
}

# ---------------------------------------------------------------------------
# Bank ayat TERVERIFIKASI — wording Sahih International yang sudah tayang di
# artikel Inggris website Podcast Meong. HANYA ayat-ayat ini yang boleh
# dipakai langsung. Ayat lain = PERLU VERIFIKASI.
# ---------------------------------------------------------------------------

VERSE_BANK = {
    "21:87": {
        "teks": ("There is no god but You. Glory be to You. "
                 "Indeed, I have been of the wrongdoers."),
        "sumber": ("Sahih International — terverifikasi di artikel Inggris "
                   "'The Prayer of Prophet Yunus'"),
    },
    "21:88": {
        "teks": ("He answered his prayer and saved him from distress. "
                 "And thus do We save the believers."),
        "sumber": ("Sahih International — terverifikasi di artikel Inggris "
                   "'The Prayer of Prophet Yunus'"),
    },
    "21:83": {
        "teks": ("Indeed, adversity has touched me, and You are the Most "
                 "Merciful of the merciful."),
        "sumber": ("Sahih International — terverifikasi di artikel Inggris "
                   "'The Patience of Prophet Ayub'"),
    },
}

# Judul buku Inggris yang SUDAH terverifikasi di website (artikel Inggris).
# Judul lain di daftar buku ditandai "(usulan)" — belum dikunci.
JUDUL_EN_TERVERIFIKASI = {
    "yunus": "Prophet Yunus Inside the Whale",
    "ayub": "Prophet Ayub and the Patience That Never Ran Out",
    "nuh": "Prophet Nuh and the Saving Ark",
    "artikel-yunus": "The Prayer of Prophet Yunus: A Prayer for Hard Times",
    "artikel-ayub": "The Patience of Prophet Ayub: Patience Without Limits",
    "artikel-nuh": "The Ark of Prophet Nuh: Obedient Even When Mocked",
    "artikel-kucing": "Caring for an Orange Cat: 5 Basics",
}

# ---------------------------------------------------------------------------
# Daftar buku & artikel yang perlu diterjemahkan.
# status awal: artikel sudah selesai (versi Inggris sudah tayang di website),
# buku lain "belum". Status bisa diubah di tab Progres.
# ---------------------------------------------------------------------------

BUKU = [
    ("nuh", "Nabi Nuh — Cerita Nabi untuk Anak",
     "Prophet Nuh and the Saving Ark"),
    ("ayub", "Nabi Ayub — Cerita Nabi untuk Anak",
     "Prophet Ayub and the Patience That Never Ran Out"),
    ("yusuf", "Nabi Yusuf — Cerita Nabi untuk Anak",
     "Prophet Joseph (usulan judul)"),
    ("yunus", "Nabi Yunus — Cerita Nabi untuk Anak",
     "Prophet Yunus Inside the Whale"),
    ("musa", "Nabi Musa — Cerita Nabi untuk Anak",
     "Prophet Moses (usulan judul)"),
    ("ibrahim", "Nabi Ibrahim — Cerita Nabi untuk Anak",
     "Prophet Abraham (usulan judul)"),
    ("abu-bakar", "Abu Bakar — Orang Sholeh",
     "Abu Bakr (usulan judul)"),
    ("umar", "Umar — Orang Sholeh",
     "Umar (usulan judul)"),
    ("syafii", "Imam Syafi'i — Orang Sholeh",
     "Imam Al-Shafi'i (usulan judul)"),
    ("salahuddin", "Salahuddin Al-Ayyubi — Orang Sholeh",
     "Salahuddin Al-Ayyubi (usulan judul)"),
    ("kolam", "Si Oyen Penjaga Kolam Ikan",
     "Oyen the Pond Keeper (usulan)"),
    ("rindu", "Rindu di Ujung Senja — Puisi & Cerpen",
     "Longing at Dusk (usulan judul)"),
    ("artikel-yunus", "Artikel: Doa Nabi Yunus",
     "The Prayer of Prophet Yunus: A Prayer for Hard Times"),
    ("artikel-ayub", "Artikel: Sabar Nabi Ayub",
     "The Patience of Prophet Ayub: Patience Without Limits"),
    ("artikel-nuh", "Artikel: Bahtera Nabi Nuh",
     "The Ark of Prophet Nuh: Obedient Even When Mocked"),
    ("artikel-kucing", "Artikel: Merawat Kucing Oren",
     "Caring for an Orange Cat: 5 Basics"),
]

BUKU_ID = [b[0] for b in BUKU]
BUKU_LABEL = {b[0]: b[1] for b in BUKU}
BUKU_EN = {b[0]: b[2] for b in BUKU}

STATUS_AWAL = {
    "artikel-yunus": "selesai",
    "artikel-ayub": "selesai",
    "artikel-nuh": "selesai",
    "artikel-kucing": "selesai",
}
STATUS_CHOICES = ["belum", "sebagian", "selesai"]

JENIS_CHOICES = [
    "Halaman eBook",
    "Artikel",
    "Puisi",
    "Cerpen",
    "Judul / sampul",
]

# ---------------------------------------------------------------------------
# Kamus umum Indonesia-Inggris (mode panduan / template).
# Dipakai HANYA untuk draf kasar per kalimat — bukan terjemahan final.
# Kata yang tidak ada di kamus dibiarkan dalam [tanda kurung] supaya manusia
# yang melengkapinya, bukan ditebak agent.
# ---------------------------------------------------------------------------

KAMUS_UMUM = {
    "dan": "and", "yang": "who/that", "di": "in/at", "ke": "to",
    "dari": "from", "untuk": "for", "dengan": "with", "tidak": "not",
    "adalah": "is", "ini": "this", "itu": "that", "ia": "he/she",
    "dia": "he/she", "mereka": "they", "kami": "we", "kita": "we",
    "kamu": "you", "aku": "I", "saya": "I", "pada": "on",
    "dalam": "in/inside", "kemudian": "then", "lalu": "then",
    "setelah": "after", "sebelum": "before", "ketika": "when",
    "jika": "if", "karena": "because", "tetapi": "but", "namun": "however",
    "sangat": "very", "besar": "big", "kecil": "small", "baik": "good",
    "anak": "child", "anak-anak": "children", "orang": "person",
    "hari": "day", "malam": "night", "tahun": "year", "air": "water",
    "laut": "sea", "kapal": "ship", "ikan": "fish", "paus": "whale",
    "berdoa": "prayed", "sabar": "patient", "bersabar": "be patient",
    "berkata": "said", "pergi": "went", "datang": "came",
    "melihat": "saw", "mendengar": "heard", "memberi": "gave",
    "membantu": "helped", "menyelamatkan": "saved",
    "mendengarkan": "listened", "percaya": "believed",
    "taat": "obedient", "patuh": "obedient", "tertawa": "laughed",
    "senang": "happy", "sedih": "sad", "marah": "angry",
    "takut": "afraid", "lapar": "hungry", "makan": "ate",
    "minum": "drank", "tidur": "slept", "bangun": "woke up",
    "rumah": "house", "kota": "city", "desa": "village",
    "jalan": "road", "teman": "friend", "keluarga": "family",
    "ibu": "mother", "ayah": "father", "saudara": "brother/sister",
    "raja": "king", "rakyat": "people", "dunia": "world",
    "hidup": "lived", "mati": "died", "lahir": "was born",
    "tumbuh": "grew", "belajar": "learned", "mengajar": "taught",
    "menulis": "wrote", "membaca": "read", "berbicara": "spoke",
    "bertanya": "asked", "menjawab": "answered", "berjanji": "promised",
    "memohon": "pleaded", "mengampuni": "forgave", "mengasihi": "loved",
    "menjaga": "guarded", "mengikuti": "followed",
    "meninggalkan": "left", "kembali": "returned",
    "menemukan": "found", "mencari": "searched",
    "menunggu": "waited", "bekerja": "worked",
    "membangun": "built", "membuat": "made", "mengambil": "took",
    "membawa": "brought", "meletakkan": "put", "membuka": "opened",
    "menutup": "closed", "naik": "climbed", "turun": "went down",
    "masuk": "entered", "keluar": "went out", "duduk": "sat",
    "berdiri": "stood", "berjalan": "walked", "berlari": "ran",
    "berenang": "swam", "terbang": "flew", "menyanyi": "sang",
    "menangis": "cried", "tersenyum": "smiled",
    "berteriak": "shouted", "berbisik": "whispered",
    "mengucapkan": "said", "mengingatkan": "reminded",
    "menasihati": "advised", "memperingatkan": "warned",
    "mengumumkan": "announced", "mengirim": "sent",
    "menerima": "received", "memberikan": "gave",
    "membagikan": "shared", "mengumpulkan": "gathered",
    "membagi": "divided", "menghitung": "counted",
    "memotong": "cut", "memasak": "cooked", "menanam": "planted",
    "menyiram": "watered", "memetik": "picked",
    "membeli": "bought", "menjual": "sold", "membayar": "paid",
    "bermain": "played", "bercanda": "joked",
    "bersedih": "grieved", "bersyukur": "was thankful",
    "meminta": "asked for", "memaafkan": "forgave",
    "perut": "belly", "gigi": "tooth", "mata": "eye",
    "tangan": "hand", "kaki": "foot", "kepala": "head",
    "hati": "heart", "suara": "voice", "cahaya": "light",
    "api": "fire", "pohon": "tree", "bunga": "flower",
    "burung": "bird", "kucing": "cat", "anjing": "dog",
    "unta": "camel", "domba": "sheep", "sapi": "cow",
    "gurun": "desert", "gunung": "mountain", "sungai": "river",
    "hujan": "rain", "angin": "wind", "awan": "cloud",
    "bintang": "star", "bulan": "moon", "matahari": "sun",
    "pertama": "first", "kedua": "second", "ketiga": "third",
    "semua": "all", "banyak": "many", "sedikit": "a little",
    "baru": "new", "lama": "old/long", "indah": "beautiful",
    "gelap": "dark", "terang": "bright", "panas": "hot",
    "dingin": "cold", "cepat": "fast", "lambat": "slow",
    "tinggi": "high/tall", "rendah": "low",
    "sakit": "sick", "sehat": "healthy", "kuat": "strong",
    "lemah": "weak", "kaya": "rich", "miskin": "poor",
    "muda": "young", "tua": "old",
}

# Frasa dua/tiga kata yang harus dicek SEBELUM kata tunggal
# ("di dalam" -> "inside", bukan "in" + "in").
KAMUS_FRASA = {
    "di dalam": "inside",
    "pada suatu hari": "one day",
    "suatu hari": "one day",
    "di atas": "on",
    "di bawah": "under",
    "di samping": "beside",
    "di depan": "in front of",
    "di belakang": "behind",
    "di antara": "among",
    "di tengah": "in the middle of",
    "tidak ada": "there is no",
}

# Kata-kata Inggris yang berasal dari nilai glosarium (mis. "Prophet",
# "Jonah", "Ark") — draf kasar TIDAK boleh membungkusnya dalam [kurung].
KATA_GLOSARIUM = {w.lower() for v in GLOSARIUM.values()
                  for w in re.findall(r"[A-Za-z]+", v)}

# Awalan/akhiran Indonesia yang dicoba dilepas untuk mencari kata dasar.
PREFIXES = ("meng", "men", "mem", "me", "ber", "ter", "di", "ke", "se", "pe")
SUFFIXES = ("kan", "nya", "lah", "kah", "ku", "mu", "i", "an")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODE_AI = bool(GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are the translation agent for Podcast Meong, translating children's "
    "books and educational articles from Indonesian to English for the "
    "overseas market (Amazon KDP and Google Play Books). Style: simple, warm, "
    "child-friendly English, short sentences, like the published English "
    "articles on podcastmeong.github.io.\n\n"
    "STRICT RULES (never break them):\n"
    "1. Translate FAITHFULLY. Never add, remove, or change story content.\n"
    "2. Quran verses: use the established Sahih International wording and "
    "ALWAYS include the surah:verse number. Use ONLY these verified wordings "
    "from the verse bank below. For any other verse, do NOT translate it "
    "freely — write the verse reference followed by "
    "'[PERLU VERIFIKASI — check Sahih International at quran.com]'.\n"
    "3. Hadith: translate faithfully and keep the EXACT same book + number "
    "reference as the original. Never invent a hadith or change its reference.\n"
    "4. Use the LOCKED glossary below for all names and Islamic terms — "
    "never translate them differently.\n"
    "5. Any part you are unsure about: mark it '[PERLU VERIFIKASI]' and "
    "explain briefly why, in Indonesian. Do not guess.\n"
    "6. Output ONLY the English translation (plus PERLU VERIFIKASI notes "
    "where needed). No extra commentary.\n\n"
    "LOCKED GLOSSARY (Indonesian -> English):\n"
    + "\n".join(f"- {k} -> {v}" for k, v in GLOSARIUM.items())
    + "\n\nVERIFIED VERSE BANK (Sahih International, already published on "
      "the Podcast Meong website — use these exact wordings):\n"
    + "\n".join(
        f"- Quran {ref}: \"{v['teks']}\" ({v['sumber']})"
        for ref, v in VERSE_BANK.items())
    + "\n\nBook title in English (if the title is given in the text): "
      "use the title from the glossary/book list; titles marked '(usulan)' "
      "are proposals, keep them as-is."
)

_model = None


def _get_model():
    """Inisialisasi model Gemini sekali saja (hanya bila ada API key)."""
    global _model
    if _model is None:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            model_name="gemini-4-hydrogen",
            system_instruction=SYSTEM_PROMPT,
            generation_config={"temperature": 0.3, "max_output_tokens": 1500},
        )
    return _model


def _tanya_gemini(prompt):
    """Tanya Gemini; kembalikan None bila tidak ada key / gagal."""
    if not MODE_AI:
        return None
    try:
        balasan = _get_model().generate_content(prompt)
        teks = (balasan.text or "").strip()
        return teks or None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Alat bantu teks
# ---------------------------------------------------------------------------

def _slug(teks):
    """Ubah teks menjadi slug aman untuk nama file."""
    teks = teks.lower().strip()
    teks = re.sub(r"[^a-z0-9]+", "-", teks)
    return teks.strip("-") or "bagian"


def _pecah_kalimat(teks):
    """Pecah teks menjadi kalimat (per . ! ? dan baris baru)."""
    bagian = []
    for baris in teks.splitlines():
        baris = baris.strip()
        if not baris:
            continue
        potong = re.split(r"(?<=[.!?])\s+", baris)
        bagian.extend(p.strip() for p in potong if p.strip())
    return bagian


def _cari_ayat(teks):
    """Cari rujukan ayat (QS 21:87 / Q.S. 21:87 / Quran 21:87) dalam teks."""
    pola = re.compile(
        r"(?:QS|Q\.S\.|Quran|Qur'an|Al-Quran)\s*(\d{1,3}:\d{1,3})",
        re.IGNORECASE)
    return pola.findall(teks)


def _cari_hadis(teks):
    """Cari penanda hadis (HR., Hadis Riwayat, Bukhari, Muslim, dll)."""
    penanda = ["HR.", "HR ", "Hadis Riwayat", "Hadits", "Hadis",
               "Bukhari", "Muslim", "Tirmidzi", "Abu Dawud",
               "An-Nasa'i", "Ibnu Majah", "shahih", "sahih", "hasan"]
    rendah = teks.lower()
    return [p for p in penanda if p.lower() in rendah]


def _terapkan_glosarium(teks):
    """Terapkan glosarium terkunci pada teks (frasa terpanjang dulu).

    Mengembalikan (teks_hasil, [istilah yang ditemukan]).
    """
    ditemukan = []
    hasil = teks
    for istilah in sorted(GLOSARIUM, key=len, reverse=True):
        pola = re.compile(r"\b" + re.escape(istilah) + r"\b",
                          re.IGNORECASE)
        if pola.search(hasil):
            ditemukan.append(istilah)
            hasil = pola.sub(GLOSARIUM[istilah], hasil)
    return hasil, ditemukan


def _cari_kata_dasar(kata):
    """Cari terjemahan kata di kamus, coba lepas awalan/akhiran Indonesia."""
    rendah = kata.lower()
    if rendah in KAMUS_UMUM:
        return KAMUS_UMUM[rendah]
    for aw in PREFIXES:
        if rendah.startswith(aw) and len(rendah) > len(aw) + 2:
            dasar = rendah[len(aw):]
            if dasar in KAMUS_UMUM:
                return KAMUS_UMUM[dasar]
            for ak in SUFFIXES:
                if dasar.endswith(ak) and len(dasar) > len(ak) + 1:
                    if dasar[:-len(ak)] in KAMUS_UMUM:
                        return KAMUS_UMUM[dasar[:-len(ak)]]
    for ak in SUFFIXES:
        if rendah.endswith(ak) and len(rendah) > len(ak) + 2:
            if rendah[:-len(ak)] in KAMUS_UMUM:
                return KAMUS_UMUM[rendah[:-len(ak)]]
    return None


def _draf_kasar(kalimat):
    """Buat draf kasar Inggris per kalimat (mode panduan).

    Glosarium diterapkan dulu, lalu kata-per-kata dari kamus umum.
    Kata yang tidak dikenal dibiarkan dalam [kurung] supaya manusia
    yang melengkapinya — bukan ditebak agent.
    """
    sesudah_glosarium, _ = _terapkan_glosarium(kalimat)
    token = re.findall(r"[A-Za-zÀ-ÿ']+|[0-9]+|[^\w\s]", sesudah_glosarium)
    hasil = []
    i = 0
    while i < len(token):
        tok = token[i]
        if re.match(r"^[A-Za-zÀ-ÿ']+$", tok):
            # 1) Frasa dua/tiga kata dulu ("di dalam" -> "inside").
            frasa = None
            for panjang in (3, 2):
                if i + panjang <= len(token):
                    potong = token[i:i + panjang]
                    if all(re.match(r"^[A-Za-zÀ-ÿ']+$", t) for t in potong):
                        gabung = " ".join(t.lower() for t in potong)
                        if gabung in KAMUS_FRASA:
                            frasa = KAMUS_FRASA[gabung]
                            i += panjang
                            break
            if frasa:
                hasil.append(frasa)
                continue
            # 2) Kata Inggris hasil glosarium — biarkan apa adanya.
            if tok.lower() in KATA_GLOSARIUM:
                hasil.append(tok)
                i += 1
                continue
            # 3) Kamus umum (dengan lepas awalan/akhiran).
            arti = _cari_kata_dasar(tok)
            if arti:
                hasil.append(arti.split("/")[0])
            else:
                hasil.append("[" + tok + "]")
        else:
            hasil.append(tok)
        i += 1
    draf = " ".join(hasil)
    draf = re.sub(r"\s+([,.!?;:])", r"\1", draf)
    return draf


def _cek_glosarium(teks_id, hasil_en):
    """Periksa: istilah glosarium yang ada di teks asli, apakah bentuk
    Inggrisnya muncul di hasil terjemahan? Kembalikan daftar yang HILANG."""
    hilang = []
    for istilah in sorted(GLOSARIUM, key=len, reverse=True):
        if re.search(r"\b" + re.escape(istilah) + r"\b", teks_id,
                     re.IGNORECASE):
            bentuk_en = GLOSARIUM[istilah]
            if not re.search(re.escape(bentuk_en), hasil_en, re.IGNORECASE):
                hilang.append(f"{istilah} -> {bentuk_en}")
    return hilang


# ---------------------------------------------------------------------------
# Terjemah — mode AI (Gemini) dan mode panduan (template lokal)
# ---------------------------------------------------------------------------

def terjemah_template(teks, jenis):
    """Mode panduan (tanpa API key): panduan per kalimat + glosarium.

    BUKAN terjemahan final — draf kasar yang harus dirapikan manusia.
    Ayat terverifikasi dipakai langsung; ayat lain ditandai PERLU VERIFIKASI.
    """
    kalimat_list = _pecah_kalimat(teks)
    if not kalimat_list:
        return "Teks kosong — tempel teks Bahasa Indonesia dulu."
    blok = []
    blok.append(
        "### PANDUAN TERJEMAH (mode template — tanpa API key)\n"
        "Ini BUKAN terjemahan final. Di bawah ini ada draf kasar per kalimat "
        "yang harus dirapikan manusia. Kata dalam [kurung] belum diterjemahkan "
        "— lengkapi manual, jangan ditebak.\n")
    for i, kalimat in enumerate(kalimat_list, 1):
        _, istilah = _terapkan_glosarium(kalimat)
        ayat = _cari_ayat(kalimat)
        hadis = _cari_hadis(kalimat)
        blok.append(f"**Kalimat {i} (asli):** {kalimat}")
        if istilah:
            blok.append(
                "**Istilah terkunci:** "
                + ", ".join(f"{s} → {GLOSARIUM[s]}" for s in istilah))
        if ayat:
            for ref in ayat:
                if ref in VERSE_BANK:
                    blok.append(
                        f"**Ayat QS {ref} (terverifikasi, Sahih "
                        f"International):** “{VERSE_BANK[ref]['teks']}” "
                        f"— Quran {ref}")
                else:
                    blok.append(
                        f"**⚠ PERLU VERIFIKASI — QS {ref}:** ayat ini belum "
                        f"ada di bank ayat terverifikasi. Pakai terjemahan "
                        f"Sahih International (cek quran.com), jangan "
                        f"terjemahkan bebas.")
        if hadis:
            blok.append(
                "**⚠ PERLU VERIFIKASI — hadis (" + ", ".join(hadis) + "):** "
                "terjemahkan setia, pertahankan rujukan kitab + nomor yang "
                "sama seperti aslinya. Jangan ubah rujukan.")
        blok.append(f"**Draf kasar:** {_draf_kasar(kalimat)}\n")
    draf_gabung = " ".join(_draf_kasar(k) for k in kalimat_list)
    blok.append("---\n**Draf kasar gabungan (perlu dirapikan):**\n" + draf_gabung)
    blok.append(
        "\n---\n*DRAF — menunggu persetujuan Cipta. Jenis: " + jenis + ". "
        "Mode: template (tanpa API key).*")
    return "\n".join(blok)


def terjemah_ai(teks, jenis, buku_id):
    """Mode AI penuh (Gemini): terjemahan setia + cek glosarium."""
    judul_en = BUKU_EN.get(buku_id, "")
    prompt = (
        f"Translate the following Indonesian {jenis} text to English. "
        f"Book: {BUKU_LABEL.get(buku_id, buku_id)} "
        f"(English title: {judul_en}).\n\n"
        f"INDONESIAN TEXT:\n{teks}"
    )
    hasil = _tanya_gemini(prompt)
    if hasil is None:
        return None
    hilang = _cek_glosarium(teks, hasil)
    catatan = []
    if hilang:
        catatan.append(
            "\n\n⚠ **Catatan cek glosarium** — istilah terkunci berikut ada "
            "di teks asli tapi bentuk Inggrisnya TIDAK muncul di hasil "
            "terjemahan (periksa manual): " + "; ".join(hilang))
    ayat = _cari_ayat(teks)
    ayat_belum = [r for r in ayat if r not in VERSE_BANK]
    if ayat_belum and "PERLU VERIFIKASI" not in hasil:
        catatan.append(
            "\n\n⚠ **PERLU VERIFIKASI — ayat " + ", ".join(
                "QS " + r for r in ayat_belum) + ":** rujukan ini belum ada "
            "di bank ayat terverifikasi. Pastikan terjemahannya memakai "
            "Sahih International (cek quran.com).")
    if catatan:
        hasil += "".join(catatan)
    hasil += (
        "\n\n---\n*DRAF — menunggu persetujuan Cipta. Jenis: " + jenis
        + ". Mode: AI (Gemini).*")
    return hasil


def terjemah(teks, buku_id, jenis):
    """Fungsi utama tab Terjemah."""
    if not teks or not teks.strip():
        return "Tempel dulu teks Bahasa Indonesia yang mau diterjemahkan."
    teks = teks.strip()
    if MODE_AI:
        hasil = terjemah_ai(teks, jenis, buku_id)
        if hasil is not None:
            return hasil
        return (
            "Gemini tidak menjawab (kuota habis / gagal). "
            "Hasil panduan template di bawah ini sebagai gantinya:\n\n"
            + terjemah_template(teks, jenis))
    return terjemah_template(teks, jenis)


CONTOH_YUNUS = (
    "Nabi Yunus berdoa di dalam perut ikan paus. Doanya pendek tetapi indah. "
    "Nabi Yunus berkata, “Tidak ada Tuhan selain Engkau. Maha Suci Engkau. "
    "Sungguh, aku termasuk orang-orang yang zalim.” (QS 21:87) "
    "Allah mendengar doanya dan menyelamatkannya. "
    "Kesabaran dan doa selalu didengar oleh Allah."
)

# ---------------------------------------------------------------------------
# Simpan terjemahan + pelacak progres (progress.json lokal)
# ---------------------------------------------------------------------------

def _muat_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _simpan_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _status_buku(buku_id):
    progress = _muat_progress()
    if buku_id in progress:
        return progress[buku_id].get("status", "belum")
    return STATUS_AWAL.get(buku_id, "belum")


def simpan_terjemahan(hasil, buku_id, bagian):
    """Simpan hasil terjemahan sebagai file .md + tandai buku 'sebagian'."""
    if not hasil or not hasil.strip():
        return "Tidak ada hasil terjemahan untuk disimpan."
    if not bagian or not bagian.strip():
        return "Isi dulu nama bagian (contoh: Halaman 3)."
    nama_file = f"{buku_id}-{_slug(bagian)}-en.md"
    path = os.path.join(TERJEMAHAN_DIR, nama_file)
    hari_ini = datetime.date.today().isoformat()
    isi = (
        f"# {BUKU_LABEL.get(buku_id, buku_id)} — {bagian.strip()}\n\n"
        f"- Judul Inggris: {BUKU_EN.get(buku_id, '')}\n"
        f"- Tanggal: {hari_ini}\n"
        f"- Status: DRAF — menunggu persetujuan Cipta\n\n"
        f"{hasil.strip()}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(isi)
    progress = _muat_progress()
    entri = progress.get(buku_id, {})
    if entri.get("status") != "selesai":
        entri["status"] = "sebagian"
    entri["terakhir"] = hari_ini
    progress[buku_id] = entri
    _simpan_progress(progress)
    return (f"✅ Tersimpan: terjemahan/{nama_file}\n"
            f"Status buku '{BUKU_LABEL.get(buku_id, buku_id)}' → sebagian.")


def atur_status(buku_id, status):
    """Ubah status progres sebuah buku secara manual."""
    if status not in STATUS_CHOICES:
        return "Status tidak dikenal."
    progress = _muat_progress()
    entri = progress.get(buku_id, {})
    entri["status"] = status
    entri["terakhir"] = datetime.date.today().isoformat()
    progress[buku_id] = entri
    _simpan_progress(progress)
    return (f"✅ Status '{BUKU_LABEL.get(buku_id, buku_id)}' → {status}.")


def tampilkan_progres():
    """Tabel progres semua buku + jumlah file terjemahan tersimpan."""
    try:
        file_tersimpan = [f for f in os.listdir(TERJEMAHAN_DIR)
                          if f.endswith("-en.md")]
    except OSError:
        file_tersimpan = []
    hitung = {}
    for nama in file_tersimpan:
        for buku_id in BUKU_ID:
            if nama.startswith(buku_id + "-"):
                hitung[buku_id] = hitung.get(buku_id, 0) + 1
                break
    baris = ["| Buku | Judul Inggris | Status | File tersimpan |",
             "|---|---|---|---|"]
    for buku_id, label, judul_en in BUKU:
        baris.append(
            f"| {label} | {judul_en} | **{_status_buku(buku_id)}** | "
            f"{hitung.get(buku_id, 0)} |")
    selesai = sum(1 for b in BUKU_ID if _status_buku(b) == "selesai")
    sebagian = sum(1 for b in BUKU_ID if _status_buku(b) == "sebagian")
    belum = len(BUKU) - selesai - sebagian
    ringkas = (f"**Ringkasan:** {selesai} selesai · {sebagian} sebagian · "
               f"{belum} belum · total {len(file_tersimpan)} file terjemahan "
               f"tersimpan.\n\n"
               f"Artikel edukasi sudah selesai (versi Inggris sudah tayang "
               f"di website). Seri Cerita Nabi & Orang Sholeh masih menunggu "
               f"terjemahan.\n\n")
    return ringkas + "\n".join(baris)


def daftar_file(buku_id):
    """Daftar file terjemahan tersimpan untuk satu buku."""
    try:
        semua = sorted(f for f in os.listdir(TERJEMAHAN_DIR)
                       if f.endswith("-en.md"))
    except OSError:
        return []
    return [f for f in semua if f.startswith(buku_id + "-")]


def baca_file(nama_file):
    """Baca isi satu file terjemahan tersimpan."""
    if not nama_file:
        return "Pilih dulu file terjemahan."
    path = os.path.join(TERJEMAHAN_DIR, nama_file)
    if not os.path.exists(path):
        return "File tidak ditemukan."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Glosarium
# ---------------------------------------------------------------------------

def tampilkan_glosarium(pencarian=""):
    """Tampilkan glosarium terkunci (dengan filter pencarian)."""
    cari = (pencarian or "").strip().lower()
    baris = ["| Istilah Indonesia | Terjemahan Inggris (terkunci) |",
             "|---|---|"]
    for istilah, arti in sorted(GLOSARIUM.items()):
        if cari and cari not in istilah.lower() and cari not in arti.lower():
            continue
        baris.append(f"| {istilah} | {arti} |")
    if len(baris) == 2:
        return "Tidak ada istilah yang cocok dengan pencarian itu."
    catatan = (
        "Glosarium ini **DIKUNCI** — terjemahan istilah di atas tidak boleh "
        "berubah antar buku. Judul buku Inggris yang sudah terverifikasi di "
        "website: Prophet Yunus Inside the Whale · Prophet Ayub and the "
        "Patience That Never Ran Out · Prophet Nuh and the Saving Ark · "
        "The Prayer of Prophet Yunus · The Patience of Prophet Ayub · "
        "The Ark of Prophet Nuh · Caring for an Orange Cat: 5 Basics. "
        "Judul lain masih usulan.\n\n")
    return catatan + "\n".join(baris)


def tampilkan_bank_ayat():
    """Tampilkan bank ayat terverifikasi (Sahih International)."""
    baris = ["| Ayat | Terjemahan Inggris (Sahih International) |",
             "|---|---|"]
    for ref, data in sorted(VERSE_BANK.items()):
        baris.append(f"| Quran {ref} | “{data['teks']}” |")
    return (
        "Ayat-ayat di bawah ini **sudah terverifikasi** (wording Sahih "
        "International yang sudah tayang di artikel Inggris website). "
        "Ayat lain TIDAK BOLEH diterjemahkan bebas — tandai PERLU VERIFIKASI "
        "dan cek di quran.com.\n\n" + "\n".join(baris))

# ---------------------------------------------------------------------------
# Antarmuka Gradio — 3 tab: Terjemah, Glosarium, Progres & Arsip.
# ---------------------------------------------------------------------------

MODE_TEKS = ("Mode: AI penuh (Gemini)." if MODE_AI
             else "Mode: panduan (tanpa API key — panduan per kalimat + "
                  "glosarium + bank ayat terverifikasi, bukan terjemahan "
                  "final).")

PILIHAN_BUKU = [(f"{label} — EN: {judul_en}", buku_id)
                for buku_id, label, judul_en in BUKU]

with gr.Blocks(
    title="Agent Terjemah Podcast Meong",
    analytics_enabled=False,  # tidak ada telemetri / penyimpanan data
) as demo:
    gr.Markdown(
        "# 🌍 Agent Terjemah Podcast Meong\n"
        "Menerjemahkan eBook & artikel dari Bahasa Indonesia ke Bahasa "
        "Inggris untuk pasar luar negeri (KDP / Amazon dan Google Play "
        "Books global). " + MODE_TEKS +
        "\n\n**Aturan kejujuran:** terjemahan setia pada naskah asli. Ayat "
        "Al-Quran memakai Sahih International + nomor surah:ayat. Hadis "
        "setia + rujukan sama. Yang meragukan ditandai **PERLU VERIFIKASI**. "
        "Semua output adalah **DRAF — menunggu persetujuan Cipta** sebelum "
        "diterbitkan."
    )

    with gr.Tabs():
        with gr.Tab("📝 Terjemah"):
            gr.Markdown(
                "Tempel teks Indonesia (satu halaman atau satu bagian), "
                "lalu tekan **Terjemahkan**. Hasilnya draf — periksa dulu, "
                "baru simpan.")
            with gr.Row():
                in_buku = gr.Dropdown(
                    label="Buku / Artikel",
                    choices=PILIHAN_BUKU,
                    value="yunus")
                in_jenis = gr.Dropdown(
                    label="Jenis teks", choices=JENIS_CHOICES,
                    value="Halaman eBook")
            in_bagian = gr.Textbox(
                label="Nama bagian (contoh: Halaman 3)",
                placeholder="Halaman 3")
            in_teks = gr.Textbox(
                label="Teks Bahasa Indonesia",
                placeholder="Tempel teks di sini...",
                lines=8)
            with gr.Row():
                btn_contoh = gr.Button("📄 Isi contoh (Nabi Yunus)")
                btn_terjemah = gr.Button("🌍 Terjemahkan", variant="primary")
            out_hasil = gr.Textbox(
                label="Hasil terjemahan (DRAF)",
                lines=18)
            btn_simpan = gr.Button("💾 Simpan hasil sebagai draf")
            out_simpan = gr.Textbox(label="Status simpan", interactive=False)
            btn_contoh.click(
                lambda: CONTOH_YUNUS, inputs=[], outputs=in_teks)
            btn_terjemah.click(
                terjemah,
                inputs=[in_teks, in_buku, in_jenis],
                outputs=out_hasil)
            btn_simpan.click(
                simpan_terjemahan,
                inputs=[out_hasil, in_buku, in_bagian],
                outputs=out_simpan)

        with gr.Tab("📖 Glosarium"):
            gr.Markdown(
                "Glosarium **terkunci** — terjemahan istilah di bawah ini "
                "tidak boleh berubah antar buku, supaya semua edisi Inggris "
                "konsisten.")
            in_cari = gr.Textbox(
                label="Cari istilah (kosongkan untuk semua)",
                placeholder="Contoh: Yunus, sabar, bahtera")
            btn_glosarium = gr.Button("🔍 Tampilkan glosarium",
                                      variant="primary")
            out_glosarium = gr.Markdown()
            btn_glosarium.click(
                tampilkan_glosarium, inputs=in_cari, outputs=out_glosarium)
            btn_ayat = gr.Button("📜 Bank ayat terverifikasi")
            out_ayat = gr.Markdown()
            btn_ayat.click(tampilkan_bank_ayat, inputs=[], outputs=out_ayat)

        with gr.Tab("📊 Progres & Arsip"):
            gr.Markdown(
                "Lacak buku mana yang sudah diterjemahkan, sebagian, atau "
                "belum. File terjemahan tersimpan di folder `terjemahan/` "
                "dengan nama `<buku>-<bagian>-en.md`.")
            btn_progres = gr.Button("📋 Tampilkan progres", variant="primary")
            out_progres = gr.Markdown()
            btn_progres.click(tampilkan_progres, inputs=[], outputs=out_progres)
            with gr.Row():
                in_buku_status = gr.Dropdown(
                    label="Buku", choices=PILIHAN_BUKU, value="yunus")
                in_status = gr.Dropdown(
                    label="Status baru", choices=STATUS_CHOICES,
                    value="sebagian")
            btn_status = gr.Button("✏️ Ubah status buku")
            out_status = gr.Textbox(label="Status", interactive=False)
            btn_status.click(
                atur_status,
                inputs=[in_buku_status, in_status],
                outputs=out_status)
            with gr.Row():
                in_buku_file = gr.Dropdown(
                    label="Buku (arsip)", choices=PILIHAN_BUKU,
                    value="yunus")
                btn_daftar = gr.Button("📂 Muat daftar file")
            out_daftar = gr.Dropdown(
                label="File terjemahan tersimpan", choices=[],
                interactive=True)
            btn_baca = gr.Button("📖 Baca file terpilih")
            out_baca = gr.Textbox(label="Isi file", lines=12)
            btn_daftar.click(
                daftar_file, inputs=in_buku_file, outputs=out_daftar)
            btn_baca.click(baca_file, inputs=out_daftar, outputs=out_baca)

    gr.Markdown(
        "---\n"
        "Aturan: terjemahan setia — ayat Sahih International + surah:ayat, "
        "hadis setia + rujukan sama, yang ragu ditandai PERLU VERIFIKASI, "
        "semua output DRAF. Data tersimpan lokal di `terjemahan/` + "
        "`progress.json` di folder Space ini (akan hilang bila Space "
        "di-rebuild — unduh berkala bila perlu). Batasan gratis: Gemini "
        "free tier ada kuota harian (bila habis, agent jatuh ke mode "
        "panduan); Spaces gratis CPU basic tidur bila lama tak dipakai."
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        share=False,
    )
