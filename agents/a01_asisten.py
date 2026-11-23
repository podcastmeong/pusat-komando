# ======================================================================
# PUSAT KOMANDO — salinan dari agent-ai-gratis (Agent 1 Asisten).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Asisten Podcast Meong — chatbot web gratis (Gradio + Gemini free tier).

Cara jalan:
  pip install -r requirements.txt
  python app.py                       # mode knowledge-base saja
  GEMINI_API_KEY=xxx python app.py    # mode AI penuh (Gemini free tier)

Aturan penting:
  - API key HANYA dari environment variable GEMINI_API_KEY. Jangan pernah
    tulis key di file ini atau di file lain.
  - Jawaban HANYA memakai knowledge base di bawah + Gemini. Jangan mengarang
    harga, tautan, atau fakta lain.
  - Tidak menyimpan data pengguna (tidak ada log, tidak ada database).
"""

import os
import re

import gradio as gr

# ---------------------------------------------------------------------------
# Knowledge base — SATU-SATUNYA sumber fakta. Jangan tambah fakta di luar ini
# tanpa persetujuan pemilik.
# Kata kunci "kuat" = kata penentu topik; "lemah" = kata konteks umum.
# ---------------------------------------------------------------------------

KB_ENTRIES = [
    {
        "topik": "youtube",
        "kuat": ["youtube", "yt", "shorts", "tonton", "video", "channel",
                 "subscribe", "nonton"],
        "lemah": ["episode"],
        "jawaban": (
            "Kamu bisa menonton Podcast Meong di YouTube: @Podcastmeong "
            "(https://www.youtube.com/@Podcastmeong). "
            "Episode baru tayang 07:00 dan 19:00 WIB. Jangan lupa subscribe ya!"
        ),
    },
    {
        "topik": "tiktok",
        "kuat": ["tiktok", "tt"],
        "lemah": [],
        "jawaban": (
            "TikTok utama Podcast Meong: @podcast_kucing "
            "(https://www.tiktok.com/@podcast_kucing). "
            "Ada juga akun promo @meongcast di TikTok."
        ),
    },
    {
        "topik": "instagram",
        "kuat": ["instagram", "ig", "dm"],
        "lemah": [],
        "jawaban": (
            "Instagram utama: @podcast_meong "
            "(https://www.instagram.com/podcast_meong). "
            "Untuk pemesanan jasa video promo, DM ke Instagram @podcast_meong ya."
        ),
    },
    {
        "topik": "jasa",
        "kuat": ["jasa", "video promo", "promo video", "iklan", "pesan video",
                 "petshop", "pet shop", "pesan"],
        "lemah": ["usaha", "toko"],
        "jawaban": (
            "Jasa video promo (KikiWorks) untuk pet shop dan usaha lain:\n"
            "• 15 detik — Rp75.000\n"
            "• 30 detik — Rp150.000\n"
            "• 60 detik — Rp250.000\n"
            "Cara pesan: DM Instagram @podcast_meong "
            "(https://www.instagram.com/podcast_meong), ceritakan produk/tokomu."
        ),
    },
    {
        "topik": "ebook",
        "kuat": ["ebook", "buku", "cerita nabi", "nabi", "orang sholeh",
                 "sholeh", "kolam", "rindu", "baca"],
        "lemah": ["beli buku"],
        "jawaban": (
            "Kami punya eBook cerita untuk anak, Rp29.000 per judul:\n"
            "• Seri Cerita Nabi & Orang Sholeh untuk anak — Rp29.000, "
            "di KaryaKarsa (cari \"Podcast Meong\" di karyakarsa.com).\n"
            "• \"Si Oyen Penjaga Kolam Ikan\" — Rp29.000.\n"
            "• \"Rindu di Ujung Senja\" (kumpulan puisi & cerpen) — Rp19.000.\n"
            "Untuk link pembelian yang pasti, cek website kami: "
            "https://podcastmeong.github.io/"
        ),
    },
    {
        "topik": "pod",
        "kuat": ["kaos", "baju", "pod", "zazzle", "merch", "merchandise"],
        "lemah": ["produk"],
        "jawaban": (
            "Kami jual kaos dan produk bergambar kucing di Zazzle, "
            "toko \"Podcast_Meong\" (https://www.zazzle.com/store/podcast_meong). "
            "Cek website kami untuk katalognya: https://podcastmeong.github.io/"
        ),
    },
    {
        "topik": "harga",
        "kuat": ["harga", "rp", "bayar", "beli", "tarif"],
        "lemah": ["berapa"],
        "jawaban": (
            "Harga produk kami:\n"
            "• eBook Cerita Nabi & Orang Sholeh — Rp29.000\n"
            "• eBook \"Si Oyen Penjaga Kolam Ikan\" — Rp29.000\n"
            "• eBook \"Rindu di Ujung Senja\" — Rp19.000\n"
            "• Jasa video promo: 15 detik Rp75.000, 30 detik Rp150.000, "
            "60 detik Rp250.000\n"
            "Detail dan link pembelian ada di https://podcastmeong.github.io/"
        ),
    },
    {
        "topik": "akun promo",
        "kuat": ["meongcast", "threads"],
        "lemah": ["promo", "akun lain"],
        "jawaban": (
            "Akun promo kami bernama @meongcast — ada di Instagram, TikTok, "
            "YouTube, dan Threads. Akun utama tetap Podcast Meong: "
            "YouTube @Podcastmeong, TikTok @podcast_kucing, "
            "Instagram @podcast_meong."
        ),
    },
    {
        "topik": "website",
        "kuat": ["website", "web", "situs"],
        "lemah": ["link", "tautan"],
        "jawaban": (
            "Website resmi kami: https://podcastmeong.github.io/ — "
            "di sana ada episode terbaru, eBook, produk, dan jasa video promo."
        ),
    },
    {
        "topik": "podcast",
        "kuat": ["oyen", "momo", "episode", "jadwal", "tayang"],
        "lemah": ["podcast", "meong", "kucing", "tentang", "siapa", "jam"],
        "jawaban": (
            "Podcast Meong adalah podcast komedi kucing berbahasa Indonesia, "
            "dibintangi Oyen (kucing oren) dan Momo (kucing abu-abu). "
            "Episode baru tayang dua kali sehari, pukul 07:00 dan 19:00 WIB. "
            "Website: https://podcastmeong.github.io/"
        ),
    },
]

# Topik yang jelas-jelas di luar urusan Podcast Meong — langsung "tidak tahu".
DI_LUAR_TOPIK = {
    "saham", "cuaca", "politik", "presiden", "bola", "skor", "resep",
    "lagu", "film", "berita", "gempa", "harga emas", "bitcoin", "crypto",
    "lowongan", "pinjam", "pinjol",
}

JAWABAN_TIDAK_TAHU = (
    "Maaf, saya tidak tahu jawaban untuk itu. Saya hanya bisa menjawab "
    "seputar Podcast Meong: episode, eBook, produk kaos, dan jasa video promo. "
    "Untuk pertanyaan lain, silakan DM Instagram @podcast_meong ya."
)

SAPAN = ("Halo! Saya Asisten Podcast Meong, teman ngobrol Oyen & Momo. "
         "Tanya apa saja seputar episode, eBook, kaos, atau jasa video promo!")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODE_AI = bool(GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "Kamu adalah Asisten Podcast Meong, chatbot ramah berbahasa Indonesia "
    "untuk podcast komedi kucing Oyen (oren) dan Momo (abu-abu). "
    "Jawablah dengan singkat, ramah, dan memakai Bahasa Indonesia. "
    "Gunakan HANYA informasi dari knowledge base berikut. Jangan mengarang "
    "harga, tautan, jadwal, atau fakta lain. Bila pertanyaan di luar knowledge "
    "base, katakan kamu tidak tahu dan arahkan ke DM Instagram @podcast_meong.\n\n"
    "KNOWLEDGE BASE:\n"
    + "\n".join("- " + e["jawaban"].replace("\n", " ") for e in KB_ENTRIES)
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
            generation_config={"temperature": 0.7, "max_output_tokens": 500},
        )
    return _model


def _normalisasi(teks):
    return re.sub(r"[^a-z0-9 ]+", " ", teks.lower())


def _bersihkan_kata(kata):
    """Lepas akhiran umum Bahasa Indonesia (-nya/-ku/-mu) supaya
    'kaosnya' tetap cocok dengan kata kunci 'kaos'."""
    for akhir in ("nya", "ku", "mu"):
        if kata.endswith(akhir) and len(kata) - len(akhir) >= 3:
            return kata[: -len(akhir)]
    return kata


def _cocok(kunci, teks, kata):
    """Cocokkan kata kunci: kata tunggal harus utuh (bukan bagian kata lain,
    mis. 'pod' tidak boleh cocok dengan 'podcast'); frasa boleh substring."""
    if " " in kunci:
        return kunci in teks
    return kunci in kata


def jawab_kb(pesan):
    """Jawab dari knowledge base saja (tanpa API). Kembalikan (jawaban, skor)."""
    teks = _normalisasi(pesan)
    kata = {_bersihkan_kata(w) for w in teks.split()}
    if any(_cocok(k, teks, kata) for k in DI_LUAR_TOPIK):
        return JAWABAN_TIDAK_TAHU, 0
    kuat_terbaik = None
    skor_kuat = 0
    lemah_terbaik = None
    skor_lemah = 0
    for entri in KB_ENTRIES:
        sk = sum(1 for k in entri["kuat"] if _cocok(k, teks, kata))
        sl = sum(1 for k in entri["lemah"] if _cocok(k, teks, kata))
        if sk > skor_kuat:
            skor_kuat = sk
            kuat_terbaik = entri
        if sl > skor_lemah:
            skor_lemah = sl
            lemah_terbaik = entri
    if kuat_terbaik is not None and skor_kuat >= 1:
        return kuat_terbaik["jawaban"], 2 * skor_kuat
    if lemah_terbaik is not None and skor_lemah >= 2:
        return lemah_terbaik["jawaban"], skor_lemah
    return JAWABAN_TIDAK_TAHU, 0


def jawab(pesan, riwayat):
    """Fungsi utama chat: Gemini bila ada key, knowledge base bila tidak."""
    pesan = (pesan or "").strip()
    if not pesan:
        return "Silakan tulis pertanyaanmu dulu ya."
    if _normalisasi(pesan) in {"halo", "hai", "hi", "hello", "pagi", "siang",
                               "sore", "malam", "assalamualaikum", "selamat pagi",
                               "selamat siang", "selamat sore", "selamat malam"}:
        return SAPAN

    if MODE_AI:
        try:
            isi = []
            for g in (riwayat or [])[-6:]:
                peran = g.get("role", "")
                konten = g.get("content", "")
                if peran and konten:
                    isi.append({"role": peran, "parts": [konten]})
            chat = _get_model().start_chat(history=isi)
            balasan = chat.send_message(pesan)
            teks = (balasan.text or "").strip()
            if teks:
                return teks
        except Exception:
            # Gagal ke Gemini (mis. kuota habis / jaringan): jatuh ke KB.
            jawaban, _ = jawab_kb(pesan)
            return jawaban + (
                "\n\n(Catatan: mode AI sedang tidak tersedia, "
                "jadi saya jawab dari info dasar.)"
            )

    jawaban, _ = jawab_kb(pesan)
    if not MODE_AI:
        return jawaban + (
            "\n\n(Saya sedang berjalan dalam mode info dasar. "
            "Mode AI penuh butuh API key Gemini.)"
        )
    return jawaban


demo = gr.ChatInterface(
    fn=jawab,
    title="Asisten Podcast Meong",
    description=(
        "Halo! Saya asisten Oyen & Momo. Tanya apa saja seputar episode, "
        "eBook, kaos, atau jasa video promo. "
        + ("Mode: AI penuh (Gemini)." if MODE_AI
           else "Mode: info dasar (tanpa API key — jawaban dari info resmi).")
    ),
    examples=[
        "Kapan episode baru tayang?",
        "Berapa harga eBook Cerita Nabi?",
        "Saya mau pesan video promo 30 detik",
        "Di mana bisa nonton Podcast Meong?",
        "Ada kaos kucingnya?",
    ],
    analytics_enabled=False,  # tidak ada telemetri / penyimpanan data
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        share=False,
    )
