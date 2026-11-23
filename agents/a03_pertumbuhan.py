# ======================================================================
# PUSAT KOMANDO — salinan dari agent-pertumbuhan (Agent 3 Pertumbuhan).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Pertumbuhan Podcast Meong — penasihat pertumbuhan organik
(Gradio + Gemini free tier + mode template lokal).

Cara jalan:
  pip install -r requirements.txt
  python app.py                       # mode template saja
  GEMINI_API_KEY=xxx python app.py    # mode AI penuh (Gemini free tier)

ATURAN PALING PENTING — ORGANIK SAJA:
  Agent ini TIDAK membeli follower/like, TIDAK memakai bot auto-follow/
  auto-like/auto-komen, dan TIDAK spam. Agent adalah penasihat strategi +
  pembuat konten + pelacak angka. Semua saran harus sesuai aturan platform
  (YouTube/TikTok/Instagram/Threads/Facebook). Draf balasan komentar SELALU
  ditandai "butuh persetujuan Cipta sebelum dikirim".

  - API key HANYA dari environment variable GEMINI_API_KEY. Jangan pernah
    tulis key di file ini atau di file lain.
  - Angka HANYA dari baseline terverifikasi di bawah + angka yang dimasukkan
    pengguna. Jangan mengarang angka. Bila data kurang, katakan
    "belum cukup data".
  - Data harian pengguna disimpan di data.json (file lokal di folder ini).
"""

import json
import os
import re

import gradio as gr

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))  # PUSAT KOMANDO: folder data bersama
DATA_FILE = os.path.join(BASE_DIR, "pertumbuhan_data.json")  # PUSAT KOMANDO

# ---------------------------------------------------------------------------
# Baseline terverifikasi — 18 Nov 2026 (dari analytics-2026-11-18.md).
# SATU-SATUNYA sumber angka awal. Jangan tambah angka lain tanpa data.
# ---------------------------------------------------------------------------

BASELINE = {
    "tanggal": "18 Nov 2026",
    "youtube_utama": {
        "label": "YouTube @Podcastmeong (utama)",
        "subs": 75,
        "views_28d": 13313,
        "ctr": 2.9,
        "catatan": (
            "Subscriber +36 dalam 28 hari, TAPI hanya +1 dalam 14 hari terakhir "
            "(mandek). Video Oktober 1.000+ views, video baru November hanya "
            "7–60 views. 82,8% traffic dari Feed Shorts — feed-nya ada, "
            "video baru tidak kepilih. Video teratas 28 hari: "
            "\"Mantan minta balikan jilid 2\" (1.726 views)."
        ),
    },
    "tiktok_utama": {
        "label": "TikTok @podcast_kucing (utama)",
        "followers": 72,
        "likes": 550,
        "video": 32,
        "catatan": (
            "Video teratas: \"Ngaku kerja, malah rebutan kasur\" (270 views), "
            "Aparat (223), Hoki (195). Video baru Pantai (3) dan Kolam (2) "
            "masih sangat kecil."
        ),
    },
    "instagram_utama": {
        "label": "Instagram podcast_meong (utama)",
        "followers": 2,
        "views_7d": 235,
        "reach_7d": 174,
        "interaksi_7d": 16,
        "catatan": (
            "Status akun: KREATOR (terverifikasi). 7 hari NAIK dari 129 views / "
            "118 reach / 2 interaksi menjadi 235 / 174 / 16 — bukan anjlok, "
            "tapi cold start (baru 2 follower). Reel Tentara 135 views dan "
            "The Last Key 105 views, 100% dari non-follower (discovery jalan)."
        ),
    },
    "promo": {
        "label": "5 akun promo @meongcast",
        "catatan": (
            "Instagram @meongcast, Threads @ciptabintanglestari (belum sinkron "
            "ke @meongcast), TikTok @meongcast, YouTube @meongcast (0 subscriber), "
            "Facebook \"Kiki Iyo\". Nama tampilan: Cipta Bintang Lestari. "
            "Video jasa promo tayang 18 Nov di YT + IG + Threads; TikTok dan "
            "Facebook gagal (verifikasi). Belum ada angka kinerja promo — "
            "masukkan angka harian di tab Analisis."
        ),
    },
}

AKUN = [
    ("youtube_utama", "YouTube @Podcastmeong (utama)"),
    ("tiktok_utama", "TikTok @podcast_kucing (utama)"),
    ("instagram_utama", "Instagram podcast_meong (utama)"),
    ("ig_meongcast", "Instagram @meongcast (promo)"),
    ("threads_meongcast", "Threads @meongcast (promo)"),
    ("tiktok_meongcast", "TikTok @meongcast (promo)"),
    ("yt_meongcast", "YouTube @meongcast (promo)"),
    ("fb_kiki", "Facebook Kiki Iyo (promo)"),
]
AKUN_KEYS = [k for k, _ in AKUN]
AKUN_LABEL = dict(AKUN)

HASHTAG_SOP = "#PodcastMeong #Oyen #KucingOren #PodcastKucing #FYP"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODE_AI = bool(GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "Kamu adalah Agent Pertumbuhan Podcast Meong, penasihat pertumbuhan "
    "organik berbahasa Indonesia untuk podcast komedi kucing Oyen (oren) dan "
    "Momo (abu-abu). Tugasmu membantu menaikkan view, like, subscribe, dan "
    "follow secara ORGANIK di YouTube, TikTok, Instagram, Threads, dan "
    "Facebook. DILARANG menyarankan: membeli follower/like, bot auto-follow/"
    "auto-like/auto-komen, spam, atau apa pun yang melanggar aturan platform. "
    "Jawablah singkat, praktis, dan jujur. Jangan mengarang angka — pakai "
    "hanya angka dari baseline berikut dan angka yang diberikan pengguna. "
    "Bila data kurang, katakan \"belum cukup data\".\n\n"
    "BASELINE 18 NOV 2026: YouTube @Podcastmeong 75 subs, 13.313 views/28d, "
    "CTR 2,9%, subs mandek +1/14 hari, video baru 7–60 views vs video Okt "
    "1.000+. TikTok @podcast_kucing 72 pengikut, 550 suka, 32 video. "
    "Instagram podcast_meong 2 pengikut, 7d 235 views/174 reach/16 interaksi "
    "(naik dari 129/118/2 — cold start, discovery jalan). Akun promo "
    "@meongcast: IG, Threads, TikTok, YouTube (0 subs), FB Kiki Iyo.\n"
    "Format konten: video pendek 20–30 detik (3 klip x 10 detik), dialog "
    "Inggris, target global, hook 2 detik, punchline cepat, tawa penutup. "
    "Upload video/podcast 07:00 & 19:00 WIB, konten lain mulai 08:00 WIB. "
    "Hashtag: #PodcastMeong #Oyen #KucingOren #PodcastKucing #FYP. "
    "Musik hanya dari pustaka gratis (YouTube Audio Library / TikTok "
    "Commercial / IG Music Library)."
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
            generation_config={"temperature": 0.7, "max_output_tokens": 700},
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
# Penyimpanan data harian (data.json lokal)
# Entri: {"tanggal": "2026-11-19", "akun": "youtube_utama",
#         "views": 120, "likes": 5, "followers": 76, "subs": 76}
# ---------------------------------------------------------------------------

def _muat_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _simpan_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def _angka(x):
    """Ubah input menjadi int atau None (kosong/invalid -> None)."""
    if x is None or x == "":
        return None
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None


def simpan_angka(tanggal, akun, views, likes, followers, subs):
    """Simpan (atau timpa) angka harian satu akun."""
    tanggal = (tanggal or "").strip()
    if not tanggal:
        return "⚠️ Isi tanggal dulu (format YYYY-MM-DD, mis. 2026-11-19)."
    if not akun:
        return "⚠️ Pilih akun dulu."
    entri = {
        "tanggal": tanggal,
        "akun": akun,
        "views": _angka(views),
        "likes": _angka(likes),
        "followers": _angka(followers),
        "subs": _angka(subs),
    }
    if all(v is None for k, v in entri.items() if k not in ("tanggal", "akun")):
        return "⚠️ Isi minimal satu angka (views / likes / followers / subs)."
    data = _muat_data()
    data = [d for d in data
            if not (d.get("tanggal") == tanggal and d.get("akun") == akun)]
    data.append(entri)
    data.sort(key=lambda d: (d.get("tanggal", ""), d.get("akun", "")))
    _simpan_data(data)
    label = AKUN_LABEL.get(akun, akun)
    isi = ", ".join(
        "{}: {}".format(k, v) for k, v in
        (("views", entri["views"]), ("likes", entri["likes"]),
         ("followers", entri["followers"]), ("subs", entri["subs"]))
        if v is not None
    )
    return "✅ Tersimpan: {} — {} ({})".format(label, tanggal, isi)


def _delta_teks(nama, lama, baru):
    if lama is None or baru is None:
        return None
    selisih = baru - lama
    persen = (selisih / lama * 100) if lama else None
    arah = "naik" if selisih > 0 else ("turun" if selisih < 0 else "tetap")
    persen_teks = " ({:+.1f}%)".format(persen) if persen is not None else ""
    return "{} {} {:+d}{} ({} → {})".format(nama, arah, selisih, persen_teks,
                                            lama, baru)


def analisis_akun(akun):
    """Analisis tren satu akun dari baseline + data harian yang dimasukkan."""
    label = AKUN_LABEL.get(akun, akun)
    data = [d for d in _muat_data() if d.get("akun") == akun]
    data.sort(key=lambda d: d.get("tanggal", ""))

    baris = ["## 📈 {} — {}".format(label, BASELINE["tanggal"])]
    if akun == "youtube_utama":
        b = BASELINE["youtube_utama"]
        baris.append(
            "Baseline: {} subs, {} views/28 hari, CTR {}%.\n{}".format(
                b["subs"], b["views_28d"], b["ctr"], b["catatan"]))
    elif akun == "tiktok_utama":
        b = BASELINE["tiktok_utama"]
        baris.append(
            "Baseline: {} pengikut, {} suka, {} video.\n{}".format(
                b["followers"], b["likes"], b["video"], b["catatan"]))
    elif akun == "instagram_utama":
        b = BASELINE["instagram_utama"]
        baris.append(
            "Baseline: {} pengikut; 7 hari {} views / {} reach / {} interaksi.\n{}".format(
                b["followers"], b["views_7d"], b["reach_7d"],
                b["interaksi_7d"], b["catatan"]))
    else:
        baris.append("Baseline: " + BASELINE["promo"]["catatan"])

    if len(data) < 2:
        baris.append(
            "\n⚠️ **Belum cukup data untuk tren.** Baru ada {} entri harian "
            "untuk akun ini. Masukkan angka minimal 2 hari berbeda, "
            "lalu analisis tren akan muncul di sini. "
            "Jangan mengambil kesimpulan dari satu hari saja.".format(len(data)))
        return "\n".join(baris)

    pertama, terakhir = data[0], data[-1]
    baris.append(
        "\n**Data harian:** {} entri, {} s.d. {}.".format(
            len(data), pertama["tanggal"], terakhir["tanggal"]))
    perubahan = []
    for kunci, nama in (("views", "Views"), ("likes", "Likes"),
                        ("followers", "Followers"), ("subs", "Subscriber")):
        teks = _delta_teks(nama, pertama.get(kunci), terakhir.get(kunci))
        if teks:
            perubahan.append("- " + teks)
    if perubahan:
        baris.append("\n**Perubahan {} → {}:**\n{}".format(
            pertama["tanggal"], terakhir["tanggal"], "\n".join(perubahan)))
    else:
        baris.append("\nBelum ada angka yang bisa dibandingkan antar hari.")

    # Interpretasi jujur berdasarkan pola yang sudah diketahui.
    baris.append("\n**Interpretasi (berdasarkan pola yang ada):**")
    if akun == "youtube_utama":
        baris.append(
            "- Bila subs tetap/datar sementara views naik: video ditonton "
            "tapi belum mengubah penonton jadi subscriber — perkuat CTA "
            "subscribe di 2 detik terakhir dan hook 2 detik pertama.\n"
            "- Bila views video baru tetap 7–60: masalah distribusi Shorts "
            "feed, bukan kualitas semata — coba variasi judul/hook dan jam "
            "posting 07:00 / 19:00 WIB.\n"
            "- Ingat: video Oktober butuh berminggu-minggu untuk mencapai "
            "1.000+ views; jangan bandingkan video berumur 1–2 hari dengan "
            "video lama.")
    elif akun == "instagram_utama":
        baris.append(
            "- Views naik dengan follower sedikit = discovery jalan (Reel "
            "menjangkau non-follower). Fokus: konsistensi Reel + hook kuat.\n"
            "- Bila interaksi naik lebih lambat dari views: tambah CTA "
            "komentar (pertanyaan di caption) dan balas komentar cepat.")
    elif akun == "tiktok_utama":
        baris.append(
            "- TikTok hidup dari 2–3 detik pertama. Bila views rendah, "
            "perbaiki hook (klaim absurd / pertanyaan), bukan durasi.\n"
            "- Video teratas lama (270 views) vs video baru kecil: coba "
            "ulang pola video teratas dengan topik baru.")
    else:
        baris.append(
            "- Akun promo masih di tahap awal (0 / belum ada angka). "
            "Target awal yang realistis: konsistensi posting harian + "
            "1 video jasa promo per hari, lalu ukur setelah 7 hari.\n"
            "- Jangan bandingkan akun promo dengan akun utama; bandingkan "
            "akun promo dengan dirinya sendiri minggu lalu.")
    return "\n".join(baris)


def ringkasan_semua():
    """Ringkasan semua akun: baseline + jumlah entri + tren singkat."""
    data = _muat_data()
    baris = ["# Ringkasan Pertumbuhan — Baseline {}".format(BASELINE["tanggal"]),
             "",
             "## Akun utama",
             "- **YouTube @Podcastmeong:** 75 subs, 13.313 views/28 hari, "
             "CTR 2,9%. Subs mandek (+1/14 hari).",
             "- **TikTok @podcast_kucing:** 72 pengikut, 550 suka, 32 video.",
             "- **Instagram podcast_meong:** 2 pengikut; 7 hari 235 views / "
             "174 reach / 16 interaksi (naik dari 129/118/2).",
             "",
             "## 5 akun promo @meongcast",
             "- IG, Threads, TikTok, YouTube (0 subs), Facebook Kiki Iyo. "
             "Belum ada angka kinerja — masukkan angka harian di tab Analisis.",
             "",
             "## Entri harian tersimpan: {} (file data.json lokal)".format(len(data))]
    for kunci in AKUN_KEYS:
        entri = [d for d in data if d.get("akun") == kunci]
        if len(entri) >= 2:
            pertama, terakhir = entri[0], entri[-1]
            bagian = []
            for k, nama in (("views", "views"), ("likes", "likes"),
                            ("followers", "followers"), ("subs", "subs")):
                t = _delta_teks(nama, pertama.get(k), terakhir.get(k))
                if t:
                    bagian.append(t)
            baris.append("- **{}**: {} entri ({} → {}): {}".format(
                AKUN_LABEL[kunci], len(entri), pertama["tanggal"],
                terakhir["tanggal"], "; ".join(bagian) if bagian else "tanpa angka pembanding"))
        elif len(entri) == 1:
            baris.append("- **{}**: 1 entri ({}), belum cukup untuk tren.".format(
                AKUN_LABEL[kunci], entri[0]["tanggal"]))
        else:
            baris.append("- **{}**: belum ada entri harian.".format(AKUN_LABEL[kunci]))
    baris.append(
        "\n> Semua angka di atas hanya dari baseline terverifikasi 18 Nov 2026 "
        "dan angka yang kamu masukkan sendiri. Agent tidak mengarang angka.")
    return "\n".join(baris)

# ---------------------------------------------------------------------------
# Generator ide konten — pola yang sudah terbukti (komedi absurd Oyen & Momo:
# hook 2 detik, pertanyaan/keluhan -> pertanyaan balik singkat -> punchline
# kata-kata -> tawa penutup; kucing diam = pendengar aktif).
# ---------------------------------------------------------------------------

TEMA_IDE = [
    "Oyen & Momo — komedi absurd",
    "Oyen & Momo — pertanyaan netizen",
    "Jasa video promo (KikiWorks)",
    "eBook Cerita Nabi / Orang Sholeh",
    "Di balik layar (BTS)",
    "Tren / format viral",
]

HOOKS = [
    "Kenapa Oyen marah sama {topik}?",
    "{topik} itu ternyata {klaim}!",
    "Momo, jangan bilang siapa-siapa… {topik} itu {klaim}.",
    "Oyen: \"{topik}? Itu makanan favoritku!\"",
    "Semua kucing tahu {topik} itu {klaim}. Manusia saja yang tidak tahu.",
    "Momo ketahuan {aksi} jam 3 pagi. Oyen langsung interogasi.",
    "Peringatan: jangan pernah kasih {topik} ke Oyen. Ini alasannya.",
    "Oyen mengklaim dia bisa {aksi}. Momo tidak percaya.",
]

KLAIM_ABSURD = [
    "ikan goreng raksasa",
    "kucing yang menyamar",
    "pintu ke dunia ikan",
    "bos besar para kucing",
    "alat pengendali manusia",
]

AKSI_LUCU = [
    "mencuri ikan tetangga",
    "belajar bahasa manusia",
    "membuka kulkas sendiri",
    "mengadakan rapat kucing",
    "menyamar jadi patung",
]

TOPIK_CEPAT = [
    "bulan", "kulkas", "ikan goreng", "tikus", "sofa", "tangga",
    "kardus", "lampu", "cermin", "kasur",
]

JUDUL_POLAS = [
    "{HOOK_SINGKAT}",
    "OYEN {KATA_KUNCI}?! 😹",
    "MOMO CAUGHT OYEN {KATA_KUNCI}!",
    "THE {BENDA} IS {KLAIM}!",
]

JAM_SARAN = {
    "YouTube Shorts": "07:00 & 19:00 WIB (jadwal video/podcast tetap)",
    "TikTok": "07:00, 12:00, atau 19:00 WIB",
    "Instagram Reels": "08:00, 12:00, atau 19:00 WIB",
    "Threads": "08:00 atau 20:00 WIB (teks + cuplikan video)",
    "Facebook": "08:00 atau 19:00 WIB",
}

CAPTION_TAMBAHAN = {
    "Oyen & Momo — komedi absurd": (
        "Oyen yakin banget. Momo tidak percaya. Siapa yang benar? 😹"),
    "Oyen & Momo — pertanyaan netizen": (
        "Pertanyaan dari komentar kemarin — Oyen jawab langsung. 😹"),
    "Jasa video promo (KikiWorks)": (
        "Mau video seperti ini untuk tokomu? 15 detik Rp75.000, "
        "30 detik Rp150.000, 60 detik Rp250.000. DM Instagram "
        "@podcast_meong sekarang! 🎥"),
    "eBook Cerita Nabi / Orang Sholeh": (
        "Cerita untuk anak, terverifikasi dari Al-Quran dan hadis sahih. "
        "Rp29.000 di KaryaKarsa — link di website kami. 📚"),
    "Di balik layar (BTS)": (
        "Begini jadinya kalau Oyen dan Momo syuting. Ngakak di akhir. 😹"),
    "Tren / format viral": (
        "Ikut tren, tapi tetap gaya Oyen & Momo. 😹"),
}


def _pilih(daftar, benih):
    """Pilih deterministik dari daftar berdasarkan benih teks."""
    if not daftar:
        return ""
    jumlah = sum(ord(c) for c in str(benih))
    return daftar[jumlah % len(daftar)]


def buat_ide(platform, tema):
    """Hasilkan hook + judul + caption + hashtag + jam posting (mode template)."""
    import datetime as _dt
    hari_ini = _dt.date.today().isoformat()
    benih = hari_ini + "|" + (platform or "") + "|" + (tema or "")
    topik = _pilih(TOPIK_CEPAT, benih + "t")
    klaim = _pilih(KLAIM_ABSURD, benih + "k")
    aksi = _pilih(AKSI_LUCU, benih + "a")
    hook = _pilih(HOOKS, benih + "h").format(
        topik=topik, klaim=klaim, aksi=aksi)
    judul = hook.upper() if len(hook) <= 45 else (
        "OYEN {}?! 😹".format(topik.upper()))
    caption = "{} {}\n\n{}".format(
        CAPTION_TAMBAHAN.get(tema, ""), HASHTAG_SOP, "")
    caption = (CAPTION_TAMBAHAN.get(tema, "") + "\n" + HASHTAG_SOP).strip()
    jam = JAM_SARAN.get(platform, "07:00 atau 19:00 WIB")
    hasil = (
        "## 💡 Ide konten — {} | {}\n\n"
        "**Hook (2 detik pertama):** {}\n\n"
        "**Judul:** {}\n\n"
        "**Caption:**\n{}\n\n"
        "**Jam posting yang disarankan:** {}\n\n"
        "**Pola yang dipakai:** pertanyaan/keluhan → pertanyaan balik "
        "singkat → punchline kata-kata → tawa penutup. "
        "Format 20–30 detik (3 klip x 10 detik), dialog Inggris, target global."
    ).format(platform or "-", tema or "-", hook, judul, caption, jam)

    if MODE_AI:
        tambahan = _tanya_gemini(
            "Buatkan SATU variasi hook + judul lain untuk video pendek "
            "Podcast Meong (Oyen & Momo, komedi absurd). Platform: {}. "
            "Tema: {}. Hook awal: {}. Jawab singkat saja: 1 hook, 1 judul, "
            "1 kalimat caption.".format(platform, tema, hook))
        if tambahan:
            hasil += "\n\n---\n**✨ Variasi dari AI:**\n" + tambahan
        else:
            hasil += "\n\n(Catatan: mode AI sedang tidak tersedia, variasi tidak dibuat.)"
    return hasil


# ---------------------------------------------------------------------------
# Saran aksi harian — 3 aksi organik per hari, rotasi berdasarkan tanggal.
# Semua aksi organik: tanpa bot, tanpa beli, tanpa spam.
# ---------------------------------------------------------------------------

AKSI_BANK = [
    ("Balas 5 komentar terbaru di video kemarin (akun utama + @meongcast)",
     "Komentar yang dibalas cepat menaikkan interaksi dan membuat penonton "
     "kembali. Pakai suara brand Oyen & Momo, sopan dan lucu."),
    ("Posting 1 video/reel di jam 07:00 atau 19:00 WIB",
     "Jam tetap yang sudah terbukti; konsistensi dua kali sehari menjaga "
     "distribusi Shorts feed."),
    ("Bagikan cuplikan 10 detik episode terbaru ke Threads + Facebook",
     "Satu video, banyak pintu masuk. Threads dan Facebook masih sepi — "
     "mereka butuh konten yang sama, bukan konten baru."),
    ("Pin video dengan views tertinggi minggu ini di profil TikTok & IG",
     "Pengunjung baru langsung melihat video terbaik dulu (contoh: pola "
     "video teratas \"Ngaku kerja, malah rebutan kasur\")."),
    ("Tulis 1 caption dengan pertanyaan di akhir (pancing komentar)",
     "Interaksi (bukan sekadar views) yang membuat algoritma menyebarkan "
     "Reels/Shorts lebih jauh."),
    ("Cek 1 kompetitor/kreator kucing lain, catat 1 pola yang bisa di-ATM",
     "Amati-Tiru-Modifikasi: pola Goldy & Sapi (tanya-jawab cepat, "
     "punchline, tawa penutup) sudah terbukti bekerja."),
    ("Buat 1 video jasa promo 15 detik untuk 1 pet shop target",
     "Jasa promo adalah jalur uang paling langsung; 1 video contoh per "
     "hari = 1 peluang closing per hari."),
    ("Posting 1 konten eBook (kutipan / halaman / cover) di IG & Threads",
     "Konten produk menjaga toko tetap terlihat tanpa terasa seperti iklan "
     "terus-menerus."),
    ("Follow-back + sapa 5 akun pecinta kucing yang aktif berkomentar",
     "Pertumbuhan organik = hubungan. Sapa manusia, bukan bot — tanpa "
     "auto-follow massal."),
    ("Repost video lama yang performanya bagus dengan judul/hook baru",
     "Video Oktober masih ditonton ribuan — daur ulang yang sudah terbukti "
     "lebih aman daripada selalu membuat dari nol."),
    ("Cek insight harian dan catat angkanya di tab Analisis",
     "Keputusan tanpa angka = tebak-tebakan. 2 menit mencatat menghemat "
     "berjam-jam salah arah."),
    ("Buat 1 polling/pertanyaan di Threads: \"Oyen harus apa besok?\"",
     "Threads suka percakapan. Pertanyaan ringan mengundang balasan dan "
     "menaikkan jangkauan akun promo."),
]


def aksi_harian():
    """Tampilkan 3 aksi organik hari ini + alasan singkat."""
    import datetime as _dt
    hari_ini = _dt.date.today()
    benih = hari_ini.toordinal()
    mulai = benih % len(AKSI_BANK)
    pilihan = [AKSI_BANK[(mulai + i) % len(AKSI_BANK)] for i in range(3)]
    baris = ["# ✅ 3 Aksi Organik Hari Ini — {}".format(
        hari_ini.strftime("%d %b %Y"))]
    for i, (aksi, alasan) in enumerate(pilihan, 1):
        baris.append("\n**{}. {}**\n   Kenapa: {}".format(i, aksi, alasan))
    baris.append(
        "\n> Semua aksi di atas organik: tanpa bot, tanpa beli follower/like, "
        "tanpa spam. Bila ada yang tidak sempat, lakukan besok — konsistensi "
        "lebih penting dari kuantitas.")
    if MODE_AI:
        tambahan = _tanya_gemini(
            "Beri SATU saran aksi organik tambahan hari ini untuk akun "
            "Podcast Meong (YouTube 75 subs mandek, IG 2 follower tapi views "
            "naik, TikTok 72 pengikut). Satu aksi + satu kalimat alasan.")
        if tambahan:
            baris.append("\n**✨ Tambahan dari AI:**\n" + tambahan)
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# Draf balasan komentar — template berdasarkan sentimen + suara brand.
# SELALU ditandai butuh persetujuan Cipta sebelum dikirim.
# ---------------------------------------------------------------------------

PERINGATAN_DRAF = (
    "\n\n---\n⚠️ **Draf ini BUTUH PERSETUJUAN Cipta sebelum dikirim.** "
    "Jangan kirim otomatis. Cek dulu nadanya, lalu kirim manual.")

PUJIAN_KATA = ["luc", "ngakak", "gemas", "gemes", "lucu", "keren", "bagus",
               "mantap", "love", "suka", "ketawa", "haha", "😂", "😹", "❤",
               "imut", "cakep", "hebat"]
TANYA_KATA = ["?", "berapa", "kapan", "dimana", "di mana", "gimana",
              "bagaimana", "apa", "kenapa", "kok", "apakah", "bisakah"]
KELUH_KATA = ["jelek", "bosan", "membosankan", "tidak suka", "ga suka",
              "gagal", "buruk", "mengecewakan", "nggak lucu", "gak lucu",
              "basi", "cringe", "aneh"]


def _sentimen(komentar):
    teks = komentar.lower()
    if any(k in teks for k in KELUH_KATA):
        return "keluhan"
    if any(k in teks for k in TANYA_KATA):
        return "pertanyaan"
    if any(k in teks for k in PUJIAN_KATA):
        return "pujian"
    return "lain"


def draf_balasan(komentar, platform):
    """Buat draf balasan komentar dari template + suara brand."""
    komentar = (komentar or "").strip()
    if not komentar:
        return "⚠️ Tempel dulu teks komentarnya."
    jenis = _sentimen(komentar)
    if jenis == "pujian":
        draf = (
            "Makasih banyak! 😹 Oyen senang banget kamu suka. "
            "Jangan lupa subscribe/follow ya — episode baru tayang 07:00 "
            "dan 19:00 WIB setiap hari! 🐱")
    elif jenis == "pertanyaan":
        draf = (
            "Makasih pertanyaannya! 🙏 Info lengkapnya ada di website kami "
            "https://podcastmeong.github.io/ — atau DM Instagram "
            "@podcast_meong ya, nanti kami jawab detail. 😊")
    elif jenis == "keluhan":
        draf = (
            "Maaf ya kalau episode ini kurang cocok. 🙏 Boleh cerita bagian "
            "mana yang kurang? Masukanmu membantu Oyen & Momo jadi lebih "
            "baik di episode berikutnya. 😊")
    else:
        draf = (
            "Makasih sudah mampir! 😹 Oyen & Momo tayang tiap hari 07:00 "
            "dan 19:00 WIB — sampai ketemu di episode berikutnya! 🐱")

    if MODE_AI:
        variasi = _tanya_gemini(
            "Buatkan SATU draf balasan komentar untuk Podcast Meong "
            "(Oyen & Momo, ramah, lucu, sopan, Bahasa Indonesia). "
            "Platform: {}. Komentar: \"{}\". "
            "Balasan maksimal 2 kalimat.".format(platform, komentar))
        if variasi:
            draf += "\n\n**✨ Variasi dari AI:**\n" + variasi
    return ("**Draf balasan ({}) — jenis: {}**\n\n{}".format(
        platform or "-", jenis, draf) + PERINGATAN_DRAF)

# ---------------------------------------------------------------------------
# Antarmuka Gradio — 4 tab: Analisis, Ide Konten, Aksi Harian, Balasan.
# ---------------------------------------------------------------------------

MODE_TEKS = ("Mode: AI penuh (Gemini)." if MODE_AI
             else "Mode: template (tanpa API key — semua jawaban dari pola "
                  "dan data resmi yang sudah terverifikasi).")

with gr.Blocks(
    title="Agent Pertumbuhan Podcast Meong",
    analytics_enabled=False,  # tidak ada telemetri / penyimpanan data
) as demo:
    gr.Markdown(
        "# 📈 Agent Pertumbuhan Podcast Meong\n"
        "Penasihat pertumbuhan **organik** untuk akun utama + 5 akun promo. "
        "Tanpa bot, tanpa beli follower/like, tanpa spam. " + MODE_TEKS +
        "\n\n**Baseline 18 Nov 2026:** YouTube @Podcastmeong 75 subs "
        "(mandek +1/14 hari) · TikTok @podcast_kucing 72 pengikut, 550 suka "
        "· Instagram podcast_meong 2 pengikut, views 7 hari naik 129 → 235."
    )

    with gr.Tabs():
        with gr.Tab("📈 Analisis Pertumbuhan"):
            gr.Markdown(
                "Masukkan angka harian per akun. Agent menyimpan ke "
                "`data.json` (file lokal) dan menghitung tren. "
                "Jujur: bila data kurang dari 2 hari, agent akan bilang "
                "\"belum cukup data\" — tidak mengarang.")
            with gr.Row():
                in_tanggal = gr.Textbox(
                    label="Tanggal (YYYY-MM-DD)",
                    placeholder="2026-11-19")
                in_akun = gr.Dropdown(
                    label="Akun", choices=[k for k, _ in AKUN],
                    value="youtube_utama")
            with gr.Row():
                in_views = gr.Number(label="Views (hari itu)", precision=0)
                in_likes = gr.Number(label="Likes (hari itu)", precision=0)
                in_followers = gr.Number(label="Followers / pengikut",
                                         precision=0)
                in_subs = gr.Number(label="Subscriber (YouTube)", precision=0)
            btn_simpan = gr.Button("💾 Simpan angka", variant="primary")
            out_simpan = gr.Textbox(label="Status simpan", interactive=False)
            btn_analisis = gr.Button("📊 Analisis tren akun ini")
            out_analisis = gr.Markdown()
            btn_ringkasan = gr.Button("📋 Ringkasan semua akun")
            out_ringkasan = gr.Markdown()
            btn_simpan.click(
                simpan_angka,
                inputs=[in_tanggal, in_akun, in_views, in_likes,
                        in_followers, in_subs],
                outputs=out_simpan)
            btn_analisis.click(analisis_akun, inputs=in_akun,
                               outputs=out_analisis)
            btn_ringkasan.click(ringkasan_semua, inputs=[],
                                outputs=out_ringkasan)

        with gr.Tab("💡 Ide Konten"):
            gr.Markdown(
                "Generator hook + judul + caption + hashtag berdasarkan pola "
                "episode yang sudah terbukti (komedi absurd, punchline cepat, "
                "tawa penutup).")
            with gr.Row():
                in_platform = gr.Dropdown(
                    label="Platform",
                    choices=list(JAM_SARAN.keys()),
                    value="YouTube Shorts")
                in_tema = gr.Dropdown(
                    label="Tema", choices=TEMA_IDE,
                    value="Oyen & Momo — komedi absurd")
            btn_ide = gr.Button("✨ Buat ide konten", variant="primary")
            out_ide = gr.Markdown()
            btn_ide.click(buat_ide, inputs=[in_platform, in_tema],
                          outputs=out_ide)

        with gr.Tab("✅ Aksi Harian"):
            gr.Markdown(
                "Tiga aksi organik hari ini, beserta alasannya. "
                "Tanpa bot, tanpa beli, tanpa spam.")
            btn_aksi = gr.Button("📋 Tampilkan aksi hari ini",
                                 variant="primary")
            out_aksi = gr.Markdown()
            btn_aksi.click(aksi_harian, inputs=[], outputs=out_aksi)

        with gr.Tab("💬 Balasan Komentar"):
            gr.Markdown(
                "Tempel komentar, agent buatkan draf balasan sesuai suara "
                "brand. **Draf SELALU butuh persetujuan Cipta sebelum dikirim "
                "— jangan kirim otomatis.**")
            in_komentar = gr.Textbox(
                label="Teks komentar",
                placeholder="Contoh: lucu banget oyennya 😂",
                lines=3)
            in_platform_k = gr.Dropdown(
                label="Platform komentar",
                choices=["YouTube", "TikTok", "Instagram", "Threads",
                         "Facebook"],
                value="TikTok")
            btn_draf = gr.Button("✍️ Buat draf balasan", variant="primary")
            out_draf = gr.Markdown()
            btn_draf.click(draf_balasan,
                           inputs=[in_komentar, in_platform_k],
                           outputs=out_draf)

    gr.Markdown(
        "---\n"
        "Aturan: organik saja — tanpa bot auto-follow/like/komen, tanpa beli "
        "follower/like, tanpa spam. Data harian tersimpan lokal di `data.json` "
        "di folder Space ini (akan hilang bila Space di-rebuild — ekspor "
        "berkala bila perlu). Batasan gratis: Gemini free tier ada kuota "
        "harian (bila habis, agent jatuh ke mode template); Spaces gratis "
        "CPU basic tidur bila lama tak dipakai."
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        share=False,
    )
