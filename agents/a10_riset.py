# ======================================================================
# PUSAT KOMANDO — salinan dari agent-riset-produk (Agent 10 Riset Produk & Strategi).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Riset Produk & Strategi — Podcast Meong
=============================================
Agent AI gratis yang meriset peluang produk online yang laku, menciptakan
produk, dan menciptakan strategi agar produk laku, dibutuhkan pasar,
dibutuhkan customer, menyelesaikan masalah, dan menghasilkan cuan.
Ditambah 18 Nov 2026: tab Riset Konten - menilai ide konten (hook,
format, pola yang terbukti dari riset) agar konten berpotensi viral,
laku, atau mendidik, dengan aturan kejujuran yang sama.

ATURAN PALING PENTING — KEJUJURAN RISET (tidak boleh dilanggar):
- Agent TIDAK BOLEH mengarang data pasar, angka permintaan, atau statistik
  ("menurut riset, 80% orang...") bila tidak ada sumbernya.
- Bila data tidak cukup, agent HARUS jujur menulis "belum cukup data — perlu
  cek di [sumber]".
- Setiap strategi harus menyebut usaha/waktu yang dibutuhkan dan TIDAK BOLEH
  menjanjikan penghasilan pasti. Target Bulan 1 Rp3–25 juta selalu disebut
  TARGET, bukan janji.
- Produk harus legal dan aman. Semua output adalah DRAF/RENCANA untuk
  persetujuan Cipta — bukan janji cuan.

Model: Google Gemini free tier (gemini-4-hydrogen), API key HANYA dari env var
GEMINI_API_KEY. Tanpa key, agent tetap jalan dalam mode template + kerangka
penilaian lokal. Tidak ada layanan berbayar yang dipakai. Telemetri Gradio
dimatikan.
"""
import json
import os
import re
from datetime import date

import gradio as gr

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "riset.json")  # PUSAT KOMANDO: folder data bersama

DISCLAIMER = (
    "\n\n---\n⚠️ DRAF / RENCANA — untuk persetujuan Cipta. Bukan janji cuan. "
    "Angka pasar hanya dipakai bila ada sumbernya; bila tidak ada, "
    "ditulis 'belum cukup data'."
)

# ---------------------------------------------------------------------------
# Knowledge base — produk & jalur Cipta yang sudah ada (terverifikasi 18 Nov 2026)
# ---------------------------------------------------------------------------
PRODUK_CIPTA = (
    "Produk Cipta yang sudah ada: eBook Cerita Nabi & Orang Sholeh untuk anak "
    "Rp29.000; 'Si Oyen Penjaga Kolam Ikan' Rp29.000; 'Rindu di Ujung Senja' "
    "Rp19.000; POD kaos kucing Zazzle; foto stock AI (Adobe Stock/Dreamstime); "
    "video podcast kucing Oyen & Momo; jasa video promo 15 dtk Rp75rb / 30 dtk "
    "Rp150rb / 60 dtk Rp250rb; game web 'Oyen Tangkap Ikan' (dalam pembuatan)."
)
JALUR_JUALAN = (
    "Jalur jualan: KaryaKarsa (kreator 90%), KBM, Google Play Books, KDP Amazon "
    "(royalti 35–70%), Lynk.id, Mayar, Zazzle, Adobe/Dreamstime, itch.io "
    "(game), website podcastmeong.github.io."
)
TEMUAN_RISET = (
    "Temuan riset eBook (18 Nov 2026, sumber: laporan riset internal): kategori "
    "paling cocok — (1) biografi religius/Islam, (2) puisi & cerpen, "
    "(3) biografi sejarah 40–60 halaman; Indonesia membayar untuk serial "
    "romansa/horor per bab dan aplikasi Al-Quran gratis; slot buku lengkap "
    "Rp19–29rb masih jarang terisi; TIDAK ADA data publik penjualan unit "
    "per judul di KaryaKarsa/Google Play — klaim 'X eksemplar terjual' untuk "
    "judul tertentu harus dianggap belum terverifikasi."
)
ASET_CIPTA = ["ebook", "kucing", "nabi", "foto", "video", "jasa", "game",
              "musik", "puisi", "cerpen", "podcast", "oyen", "momo", "poster",
              "desain", "template", "anak", "islam", "cerita"]

KRITERIA = [
    ("masalah", "Masalah yang diselesaikan jelas"),
    ("customer", "Customer-nya terdefinisi"),
    ("bukti", "Ada bukti permintaan yang bisa dicek"),
    ("pesaing", "Pesaing sudah dipetakan"),
    ("cocok", "Cocok dengan skill & aset Cipta"),
    ("harga", "Harga masuk akal untuk pasar"),
]

JENIS_PRODUK = ["eBook", "POD (kaos/produk)", "Foto stock", "Template digital",
                "Kursus/mini-kursus", "Aplikasi", "Game", "Lagu/musik",
                "Jasa", "Lainnya"]

# Bank masalah umum per niche (template lokal — bukan data statistik)
BANK_MASALAH = {
    "anak": [
        ("Anak sulit fokus saat belajar", "eBook aktivitas/kuis interaktif anak, video pendek edukasi"),
        ("Orang tua bingung memilih bacaan anak yang aman", "Seri eBook anak bertema nilai + panduan orang tua"),
        ("Anak kecanduan gadget", "Game edukasi offline-friendly, paket aktivitas tanpa layar"),
    ],
    "kucing": [
        ("Pemilik kucing bingung merawat kucing oren", "eBook panduan perawatan kucing oren, video tips"),
        ("Pet shop butuh promosi tapi mahal", "Jasa video promo 15–60 detik Rp75–250rb"),
        ("Pecinta kucing cari merchandise lucu", "POD kaos & produk bergambar kucing"),
    ],
    "bisnis": [
        ("UMKM butuh konten promosi tapi tidak punya tim", "Jasa video promo pendek, template caption promosi"),
        ("Toko online sepi pembeli", "Paket konten + strategi posting harian"),
        ("Pemilik usaha tidak sempat kelola media sosial", "Template konten 30 hari + jasa pengelolaan"),
    ],
    "belajar": [
        ("Pelajar sulit menghafal", "eBook teknik menghafal + kartu latihan"),
        ("Orang dewasa ingin belajar skill baru tapi sibuk", "Mini-kursus video pendek per bab"),
    ],
    "musik": [
        ("Kreator butuh musik latar bebas royalti", "Paket musik/lagu bebas lisensi untuk video"),
        ("Anak butuh lagu edukasi yang mudah diingat", "Lagu anak bertema huruf/angka/nilai"),
    ],
}


# ---------------------------------------------------------------------------
# Utilitas
# ---------------------------------------------------------------------------
def _load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (OSError, ValueError):
            pass
    return []


def _save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _today():
    return date.today().isoformat()


def _gemini(prompt):
    """Panggil Gemini bila ada key; kembalikan None bila tidak ada/gagal."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-4-hydrogen")
        resp = model.generate_content(prompt)
        teks = (resp.text or "").strip()
        return teks if teks else None
    except Exception:
        return None


def _angka_harga(teks):
    """Ambil angka harga (Rp) dari teks, atau None."""
    if not teks:
        return None
    t = teks.replace(".", "").replace(",", "")
    m = re.search(r"(\d[\d\s]*)", t)
    if not m:
        return None
    try:
        return int(m.group(1).replace(" ", ""))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# 1) Riset peluang produk — penilaian jujur 6 kriteria (0–2 per kriteria)
# ---------------------------------------------------------------------------
def nilai_peluang(niche, ide, masalah, customer, bukti, pesaing, harga):
    niche = (niche or "").strip()
    ide = (ide or "").strip()
    masalah = (masalah or "").strip()
    customer = (customer or "").strip()
    bukti = (bukti or "").strip()
    pesaing = (pesaing or "").strip()
    harga = (harga or "").strip()
    if not niche or not ide:
        return "⚠️ Isi dulu niche dan ide produknya.", "", ""
    if len(masalah) < 10:
        return ("⚠️ Jelaskan masalah yang diselesaikan produk ini (minimal "
                "satu kalimat). Tanpa masalah yang jelas, produk sulit laku."), "", ""

    skor = {}
    catatan = {}
    teks_bawah = (niche + " " + ide + " " + masalah + " " + customer).lower()

    # 1. Masalah jelas
    skor["masalah"] = 2 if len(masalah) >= 40 else 1
    catatan["masalah"] = ("Masalah ditulis spesifik." if skor["masalah"] == 2
                          else "Masalah ditulis, tapi masih umum — perjelas "
                          "dengan contoh nyata customer.")
    # 2. Customer terdefinisi
    if len(customer) >= 20:
        skor["customer"] = 2
        catatan["customer"] = "Customer terdefinisi dengan jelas."
    elif len(customer) >= 5:
        skor["customer"] = 1
        catatan["customer"] = ("Customer disebut, tapi belum spesifik "
                               "(usia, kebutuhan, daya beli).")
    else:
        skor["customer"] = 0
        catatan["customer"] = ("Customer belum ditulis — produk tanpa customer "
                               "yang jelas sulit dijual.")
    # 3. Bukti permintaan
    if bukti and ("http" in bukti or "cek" in bukti.lower()
                  or len(bukti) >= 30):
        skor["bukti"] = 2
        catatan["bukti"] = "Ada bukti/cek yang bisa diverifikasi."
    elif bukti:
        skor["bukti"] = 1
        catatan["bukti"] = ("Bukti masih lemah — perlu cek nyata di marketplace "
                            "atau pencarian.")
    else:
        skor["bukti"] = 0
        catatan["bukti"] = ("BELUM CUKUP DATA — tidak ada bukti permintaan. "
                            "Perlu cek di: pencarian Tokopedia/Shopee, Google "
                            "Trends, atau grup komunitas niche ini.")
    # 4. Pesaing dipetakan
    if len(pesaing) >= 30:
        skor["pesaing"] = 2
        catatan["pesaing"] = "Pesaing dipetakan (nama + harga/kelemahan)."
    elif len(pesaing) >= 5:
        skor["pesaing"] = 1
        catatan["pesaing"] = "Pesaing disebut, tapi belum dipetakan kekuatannya."
    else:
        skor["pesaing"] = 0
        catatan["pesaing"] = ("BELUM CUKUP DATA — pesaing belum dicek. Cek 3–5 "
                              "produk sejenis dan harganya.")
    # 5. Cocok dengan aset Cipta
    cocok = [a for a in ASET_CIPTA if a in teks_bawah]
    if cocok:
        skor["cocok"] = 2
        catatan["cocok"] = ("Cocok dengan aset Cipta: " + ", ".join(cocok) + ".")
    else:
        skor["cocok"] = 0
        catatan["cocok"] = ("Belum jelas cocok dengan skill/aset Cipta "
                            "(eBook, kucing, foto, video, jasa, game, musik, "
                            "puisi, cerpen). Bila butuh skill baru, hitung "
                            "waktu belajarnya.")
    # 6. Harga masuk akal
    h = _angka_harga(harga)
    if h is None:
        skor["harga"] = 0
        catatan["harga"] = "Harga belum ditulis — tentukan harga usulan dulu."
    elif 5000 <= h <= 500000:
        skor["harga"] = 2
        catatan["harga"] = (f"Harga Rp{h:,} berada di kisaran produk digital "
                            "Indonesia yang umum.")
    else:
        skor["harga"] = 1
        catatan["harga"] = (f"Harga Rp{h:,} di luar kisaran umum produk digital "
                            "(Rp5rb–500rb) — perlu alasan kuat (premium/eksklusif).")

    total = sum(skor.values())
    if total >= 9:
        verdict = "✅ LAYAK DICOBA"
        saran = ("Lanjutkan ke tahap buat prototipe kecil (1 bab eBook / 1 desain "
                 "/ 1 demo) dan tawarkan ke 5–10 calon customer sebelum produksi penuh.")
    elif total >= 5:
        verdict = "🔶 PERLU RISET LANJUT"
        saran = ("Jangan produksi dulu. Lengkapi dulu kriteria yang skornya 0–1, "
                 "terutama bukti permintaan dan peta pesaing.")
    else:
        verdict = "🔴 TIDAK DISARANKAN (untuk sekarang)"
        saran = ("Risiko gagal tinggi: masalah/customer/bukti belum jelas. "
                 "Perbaiki dulu kerangka di atas atau pilih ide lain.")

    baris = [f"## Hasil Penilaian — {ide} (niche: {niche})",
             f"**Skor total: {total}/12 — {verdict}**", ""]
    for kunci, label in KRITERIA:
        baris.append(f"- **{label}: {skor[kunci]}/2** — {catatan[kunci]}")
    baris += ["", "**Langkah verifikasi berikutnya:**",
              "1. Cek 5 produk sejenis di Tokopedia/Shopee/KaryaKarsa (nama + harga + jumlah ulasan).",
              "2. Cek Google Trends untuk kata kunci niche ini (naik/turun/datar).",
              "3. Tanya 5 orang dari target customer: mau bayar berapa untuk solusi ini?",
              "", f"**Saran:** {saran}",
              "",
              "Catatan kejujuran: penilaian ini memakai kerangka lokal + input "
              "yang kamu isi. Bukan data statistik pasar — angka permintaan "
              "hanya sah bila dicek langsung di marketplace/tren.",
              DISCLAIMER]
    hasil = "\n".join(baris)

    # Mode AI: Gemini memperkaya penilaian (tetap dengan aturan jujur)
    ai = _gemini(
        "Kamu penasihat riset produk untuk kreator Indonesia bernama Cipta. "
        "Nilai peluang produk ini dengan JUJUR. DILARANG mengarang data pasar, "
        "angka permintaan, atau statistik. Bila data tidak ada, tulis "
        "'belum cukup data' dan sebut sumber yang harus dicek. Jangan "
        "menjanjikan penghasilan. Jawab singkat dalam Bahasa Indonesia, "
        "format: Masalah, Customer, Bukti yang perlu dicek, Pesaing, "
        "Kecocokan, Harga, Verdict (Layak dicoba / Perlu riset lanjut / "
        "Tidak disarankan).\n\n"
        f"Niche: {niche}\nIde produk: {ide}\nMasalah: {masalah}\n"
        f"Customer: {customer}\nBukti permintaan: {bukti or '(tidak ada)'}\n"
        f"Pesaing: {pesaing or '(tidak ada)'}\nHarga usulan: {harga or '(tidak ada)'}\n\n"
        f"Konteks: {PRODUK_CIPTA} {JALUR_JUALAN}")
    if ai:
        hasil += "\n\n---\n### Penilaian AI (Gemini)\n\n" + ai + DISCLAIMER

    ringkas = f"{niche} — {ide} | {total}/12 | {verdict}"
    return hasil, ringkas, f"{niche}||{ide}||{total}||{verdict}"


def simpan_riset(ringkasan):
    ringkasan = (ringkasan or "").strip()
    if not ringkasan:
        return "⚠️ Belum ada hasil penilaian untuk disimpan. Nilai peluang dulu."
    if "||" not in ringkasan:
        return "⚠️ Format ringkasan tidak dikenal — nilai ulang peluangnya."
    niche, ide, total, verdict = ringkasan.split("||", 3)
    data = _load()
    for e in data:
        if e.get("niche", "").lower() == niche.lower() \
                and e.get("ide", "").lower() == ide.lower():
            e["skor"] = total
            e["verdict"] = verdict
            e["tanggal"] = _today()
            _save(data)
            return (f"🔄 Sudah ada di log — diperbarui: {niche} — {ide} "
                    f"({total}/12, {verdict}).")
    data.append({"jenis": "produk", "niche": niche, "ide": ide, "skor": total,
                 "verdict": verdict, "tanggal": _today()})
    _save(data)
    return f"✅ Disimpan ke log riset: {niche} — {ide} ({total}/12, {verdict})."


# ---------------------------------------------------------------------------
# 2) Pencipta produk — dari masalah customer ke rancangan produk
# ---------------------------------------------------------------------------
def cipta_produk(masalah, customer, jenis):
    masalah = (masalah or "").strip()
    customer = (customer or "").strip()
    jenis = jenis or "eBook"
    if len(masalah) < 10:
        return "⚠️ Tulis dulu masalah customer-nya (minimal satu kalimat)."
    if len(customer) < 5:
        customer = "belum terdefinisi — tentukan dulu siapa yang punya masalah ini"

    outline = {
        "eBook": ("Bab 1 Pengantar masalah → Bab 2–4 Cerita/panduan inti (3 bagian) "
                  "→ Bab 5 Latihan/praktik → Bab 6 Penutup + ajakan"),
        "POD (kaos/produk)": ("1 desain utama + 2 variasi warna → mockup kaos/mug/tote "
                              "→ listing Zazzle (judul + tag Inggris)"),
        "Foto stock": ("20–50 foto satu tema → judul Inggris deskriptif + kata kunci "
                       "→ upload Adobe Stock + Dreamstime"),
        "Template digital": ("Template inti + contoh isi + panduan pakai 1 halaman "
                             "→ jual di Gumroad/Lynk.id"),
        "Kursus/mini-kursus": ("5–7 pelajaran pendek (5–10 menit) → latihan per pelajaran "
                               "→ sertifikat sederhana bila perlu"),
        "Aplikasi": ("Fitur inti 1 (selesaikan 1 masalah) → layar utama + 2 layar "
                     "pendukung → prototipe web/PWA"),
        "Game": ("Mekanik inti 1 → 3 level → skor/nyawa → suara sederhana → "
                 "uji di HP + laptop"),
        "Lagu/musik": ("Lirik/tema → 2 verse + chorus → rekaman demo → distribusi "
                       "RouteNote"),
        "Jasa": ("Paket 3 harga (kecil/sedang/besar) → contoh hasil → cara pesan "
                 "via DM"),
        "Lainnya": ("Versi kecil dulu (MVP) → uji ke 5 calon customer → perbaiki "
                    "→ luncurkan"),
    }
    harga_saran = {
        "eBook": "Rp19.000–Rp29.000 (ikuti harga eBook Cipta yang sudah jalan)",
        "POD (kaos/produk)": "Harga Zazzle mengikuti harga pasar + royalti; fokus ke desain, bukan harga murah",
        "Foto stock": "Royalti per unduhan (Adobe/Dreamstime) — volume + konsistensi tema yang menentukan",
        "Template digital": "Rp15.000–Rp99.000",
        "Kursus/mini-kursus": "Rp49.000–Rp199.000",
        "Aplikasi": "Gratis + donasi, atau Rp9.000–Rp49.000",
        "Game": "Gratis / bayar seikhlasnya di itch.io, atau $0.99",
        "Lagu/musik": "Streaming (RouteNote) + lisensi pakai",
        "Jasa": "Ikuti paket jasa video promo: 15 dtk Rp75rb / 30 dtk Rp150rb / 60 dtk Rp250rb",
        "Lainnya": "Tentukan setelah uji ke 5 calon customer",
    }
    platform = {
        "eBook": "KaryaKarsa, KBM, Google Play Books, KDP Amazon",
        "POD (kaos/produk)": "Zazzle, Redbubble",
        "Foto stock": "Adobe Stock, Dreamstime",
        "Template digital": "Gumroad, Lynk.id, Mayar",
        "Kursus/mini-kursus": "Lynk.id, Mayar, website sendiri",
        "Aplikasi": "Website sendiri (PWA), itch.io, Play Store ($25 sekali — bila sudah ada pemasukan)",
        "Game": "itch.io (gratis, bagi hasil bisa 0%), website sendiri, Game Jolt",
        "Lagu/musik": "RouteNote, YouTube, TikTok",
        "Jasa": "DM Instagram @podcast_meong + 5 akun @meongcast",
        "Lainnya": "Lynk.id / Mayar / website sendiri",
    }

    hasil = [f"## Rancangan Produk — {jenis}",
             f"**Masalah:** {masalah}",
             f"**Customer:** {customer}", "",
             f"**Jenis produk:** {jenis}",
             f"**Outline/isi:** {outline.get(jenis, outline['Lainnya'])}",
             f"**Harga usulan:** {harga_saran.get(jenis, '')}",
             f"**Platform jualan:** {platform.get(jenis, '')}", "",
             "**Usaha & waktu (jujur):** prototipe kecil dulu (1–3 hari kerja), "
             "uji ke 5 calon customer, baru produksi penuh. Jangan janjikan "
             "tanggal laku — yang bisa dijanjikan hanya kualitas dan konsistensi.",
             "",
             "**Cek sebelum produksi:**",
             "- Apakah masalah ini benar dialami customer? (tanya 5 orang)",
             "- Apakah ada produk sejenis? Apa bedanya produk ini?",
             "- Apakah harga masuk akal untuk customer ini?",
             DISCLAIMER]
    teks = "\n".join(hasil)

    ai = _gemini(
        "Kamu perancang produk untuk kreator Indonesia bernama Cipta. Buat "
        "rancangan produk dari masalah di bawah. DILARANG mengarang data pasar "
        "atau statistik; bila tidak tahu, tulis 'belum cukup data'. Jangan "
        "menjanjikan penghasilan. Bahasa Indonesia, format: Nama produk, "
        "Masalah yang diselesaikan, Customer, Isi/outline, Harga usulan, "
        "Platform jualan, Langkah pertama (3 hari).\n\n"
        f"Masalah: {masalah}\nCustomer: {customer}\nJenis produk: {jenis}\n\n"
        f"Konteks: {PRODUK_CIPTA} {JALUR_JUALAN} "
        "Prinsip: tema bebas (tidak harus kucing); video/podcast wajib kucing.")
    if ai:
        teks += "\n\n---\n### Rancangan AI (Gemini)\n\n" + ai + DISCLAIMER
    return teks


# ---------------------------------------------------------------------------
# 3) Generator strategi penjualan
# ---------------------------------------------------------------------------
def buat_strategi(produk, harga, customer, kanal):
    produk = (produk or "").strip()
    harga = (harga or "").strip()
    customer = (customer or "").strip()
    kanal = kanal or []
    if len(produk) < 5:
        return "⚠️ Tulis dulu nama produknya."
    if not kanal:
        kanal = ["Akun utama Podcast Meong"]
    daftar_kanal = ", ".join(kanal)
    h = _angka_harga(harga)
    harga_teks = f"Rp{h:,}" if h else (harga or "belum ditentukan")

    hasil = [f"## Strategi Penjualan — {produk}",
             f"**Harga:** {harga_teks} | **Customer:** {customer or 'belum terdefinisi'}",
             f"**Kanal:** {daftar_kanal}", "",
             "### Pra-peluncuran (3–5 hari sebelum)",
             "- 1 video teaser 20–30 detik (Oyen & Momo, bila produknya video/podcast; "
             "bila bukan, tetap gaya Podcast Meong).",
             "- 2 postingan: masalah customer + cuplikan isi produk.",
             "- Tawarkan ke 5–10 orang target: minta pendapat, bukan langsung jualan.",
             "",
             "### Hari peluncuran",
             "- Video utama 07:00 WIB + postingan ulang 19:00 WIB (jadwal video/podcast).",
             "- Caption: masalah → solusi → harga → cara beli (link di bio).",
             "- Balas komentar di 1 jam pertama (butuh persetujuan Cipta sebelum dikirim).",
             "",
             "### Pasca-peluncuran (7 hari)",
             "- Hari 2–3: testimoni/pertanyaan yang masuk (dengan izin).",
             "- Hari 4–5: variasi konten dari isi produk (1 tips per hari).",
             "- Hari 7: evaluasi — berapa klik, berapa terjual, apa yang ditanyakan customer.",
             "",
             "### Hook & caption (contoh, sesuaikan dengan produk)",
             f"- Hook: \"{customer or 'Kamu'} punya masalah ini? Ini solusinya.\"",
             f"- Caption: masalah singkat → apa isi {produk} → harga {harga_teks} → "
             "cara beli di bio.",
             "",
             "### Ukuran keberhasilan (7 hari pertama)",
             "- Klik ke link jualan, jumlah terjual, pertanyaan customer yang masuk.",
             "- Target realistis: 1–5 penjualan pertama = validasi, bukan kegagalan. "
             "Target Bulan 1 Rp3–25 juta adalah TARGET, bukan janji.",
             "",
             "**Usaha yang dibutuhkan:** 3–5 hari persiapan + 7 hari promosi aktif. "
             "Produk tidak laku dalam sehari bukan berarti gagal — evaluasi dulu "
             "apakah masalah, harga, atau jangkauannya yang kurang.",
             DISCLAIMER]
    teks = "\n".join(hasil)

    ai = _gemini(
        "Kamu ahli strategi penjualan untuk kreator Indonesia bernama Cipta. "
        "Buat rencana peluncuran produk di bawah. DILARANG mengarang data pasar "
        "atau menjanjikan penghasilan. Sebut usaha/waktu yang dibutuhkan. "
        "Bahasa Indonesia, format: Persona customer, Hook (3 contoh), Rencana "
        "7 hari, Kanal promosi, Ukuran keberhasilan.\n\n"
        f"Produk: {produk}\nHarga: {harga_teks}\nCustomer: {customer or '(belum terdefinisi)'}\n"
        f"Kanal: {daftar_kanal}\n\nKonteks: {PRODUK_CIPTA} {JALUR_JUALAN}")
    if ai:
        teks += "\n\n---\n### Strategi AI (Gemini)\n\n" + ai + DISCLAIMER
    return teks


# ---------------------------------------------------------------------------
# 4) Pemeta masalah–solusi per niche
# ---------------------------------------------------------------------------
def peta_masalah(niche):
    niche = (niche or "").strip().lower()
    if not niche:
        return "⚠️ Tulis dulu niche-nya (mis. anak, kucing, bisnis, belajar, musik)."
    kunci = None
    for k in BANK_MASALAH:
        if k in niche or niche in k:
            kunci = k
            break
    baris = [f"## Masalah & Solusi — niche: {niche}", ""]
    if kunci:
        baris.append("Masalah umum di niche ini (template — BUKAN data statistik, "
                     "verifikasi dengan tanya customer langsung):")
        for i, (m, s) in enumerate(BANK_MASALAH[kunci], 1):
            baris.append(f"{i}. **Masalah:** {m}\n   **Solusi produk yang mungkin:** {s}")
    else:
        baris.append("Niche ini belum ada di bank template lokal.")
        baris.append("Cara memetakan masalahnya (lakukan manual, 1–2 jam):")
        baris.append("1. Baca 20 komentar/ulasan di produk sejenis — catat keluhan yang berulang.")
        baris.append("2. Tanya 5 orang di niche ini: 'apa yang paling menyulitkanmu soal ...?'")
        baris.append("3. Cek grup/forum niche: pertanyaan apa yang paling sering muncul?")
    baris += ["",
              "**Aturan:** satu masalah = satu solusi produk. Jangan membuat produk "
              "yang mencoba menyelesaikan semua masalah sekaligus.",
              DISCLAIMER]
    teks = "\n".join(baris)

    ai = _gemini(
        "Kamu pemeta masalah customer untuk kreator Indonesia. Untuk niche di "
        "bawah, daftarkan 5 masalah nyata yang umum dialami customer dan 1 "
        "solusi produk untuk tiap masalah. DILARANG mengarang statistik atau "
        "persentase. Bila tidak yakin, tulis 'perlu verifikasi dengan tanya "
        "customer'. Bahasa Indonesia, format bernomor.\n\n"
        f"Niche: {niche}\n\nKonteks: {PRODUK_CIPTA}")
    if ai:
        teks += "\n\n---\n### Peta AI (Gemini)\n\n" + ai + DISCLAIMER
    return teks


# ---------------------------------------------------------------------------
# 5) Log riset
# ---------------------------------------------------------------------------
def tabel_log():
    data = _load()
    if not data:
        return ("Belum ada peluang produk atau ide konten yang dinilai. Nilai "
                "peluang di tab 'Riset Peluang' atau ide konten di tab "
                "'Riset Konten', lalu simpan dengan tombol 'Simpan ke Log'.")
    baris = ["## Log Riset (produk & konten)", "",
             "| Tanggal | Jenis | Niche | Ide | Skor | Verdict |",
             "|---|---|---|---|---|---|"]
    for e in sorted(data, key=lambda x: x.get("tanggal", ""), reverse=True):
        baris.append(f"| {e.get('tanggal','')} | {e.get('jenis','produk')} | "
                     f"{e.get('niche','')} | {e.get('ide','')} | "
                     f"{e.get('skor','')} | {e.get('verdict','')} |")
    baris.append("")
    baris.append(f"Total {len(data)} peluang tercatat.")
    return "\n".join(baris)


def hapus_log(niche, ide):
    niche = (niche or "").strip()
    ide = (ide or "").strip()
    if not niche or not ide:
        return "⚠️ Isi niche dan ide yang mau dihapus.", tabel_log()
    data = _load()
    baru = [e for e in data if not (e.get("niche", "").lower() == niche.lower()
                                    and e.get("ide", "").lower() == ide.lower())]
    if len(baru) == len(data):
        return f"⚠️ Tidak ditemukan: {niche} — {ide}.", tabel_log()
    _save(baru)
    return f"🗑️ Dihapus dari log: {niche} — {ide}.", tabel_log()



# ---------------------------------------------------------------------------
# 6) Riset konten — penilaian jujur ide konten (hook, format, pola terbukti)
# ---------------------------------------------------------------------------
# Pola yang TERVERIFIKASI (bukan karangan) — sumber dicantumkan di output:
# - Goldy & Sapi (10 video ditonton langsung di TikTok, 18 Nov 2026;
#   riset-podcast-kucing-lain.md bagian 7-8): durasi 10-13 dtk, 2-4 giliran
#   bicara, hampir tanpa jeda; pertanyaan balik singkat ("Kenapa?",
#   "Emang kenapa?", "Karier apa?") sebagai jembatan -> punchline
#   permainan kata -> ditutup tawa; kucing diam = pendengar aktif
#   (straight man); two-shot pembuka + close-up bergantian; teks kinetik
#   untuk kata kunci.
# - Format podcast internal (disetujui Cipta 18 Nov 2026): 20-30 dtk,
#   3 klip x 10 dtk, dialog bergantian, latar sesuai judul, suara Oyen
#   tinggi vs Momo rendah.
# - Podcast menang di YouTube (data internal 18 Nov 2026): episode
#   "Mantan minta balikan jilid 2" 1.726 views.
# - Baseline akun internal 18 Nov 2026: YT Podcast meong 75 subscriber;
#   TikTok @podcast_kucing 72 pengikut; IG podcast_meong 2 pengikut.
POLA_KONTEN_TERVERIFIKASI = (
    "Pola terverifikasi (sumber: riset-podcast-kucing-lain.md bagian 7-8, "
    "10 video Goldy & Sapi ditonton langsung 18 Nov 2026): 10-13 detik, "
    "2-4 giliran bicara, hampir tanpa jeda; pertanyaan balik singkat "
    "sebagai jembatan -> punchline permainan kata -> ditutup tawa; kucing "
    "diam = pendengar aktif (straight man); two-shot pembuka + close-up "
    "bergantian; teks kinetik untuk kata kunci. Format podcast internal "
    "(disetujui Cipta 18 Nov 2026): 20-30 detik, 3 klip x 10 detik, dialog "
    "bergantian, latar sesuai judul. Podcast menang di YouTube (data "
    "internal: 'Mantan minta balikan jilid 2' 1.726 views)."
)

FORMAT_TUJUAN = {
    "Viral": ("Durasi 10-13 detik, 2-4 giliran dialog, hampir tanpa jeda. "
              "Hook pertanyaan/konflik di detik 0-1, punchline permainan kata, "
              "ditutup tawa. Gaya: cepat, ekspresi besar."),
    "Jualan": ("Durasi 20-30 detik. Struktur: masalah customer -> solusi produk "
               "-> harga -> cara beli (link di bio). Hook = masalahnya, CTA jelas "
               "di akhir. Gaya: jelas, tidak bertele-tele."),
    "Edukasi": ("Durasi 30-60 detik. Struktur: pertanyaan -> jawaban singkat + "
                "contoh nyata -> ajakan. Gaya: tenang, jelas, satu ide per video."),
}

CATATAN_PLATFORM = {
    "TikTok": ("Akun utama @podcast_kucing 72 pengikut (baseline 18 Nov 2026). "
               "Video pendek cepat 10-30 dtk; jangkauan organik dari FYP."),
    "YouTube Shorts": ("Podcast/dialog menang di sini (data internal: 'Mantan "
                       "minta balikan jilid 2' 1.726 views). Format 20-30 dtk, "
                       "3 klip. Kanal Podcast meong 75 subscriber (baseline 18 Nov 2026)."),
    "Instagram Reels": ("Akun podcast_meong 2 pengikut (baseline 18 Nov 2026) - "
                        "mulai dari nol. Reels 15-30 dtk; teks kinetik membantu "
                        "penonton tanpa suara."),
    "Ketiganya": ("Buat 1 video 20-30 dtk yang bisa dipotong jadi 10-13 dtk "
                  "untuk TikTok. Judul/caption mengikuti bahasa dialog."),
}

HOOK_CONTOH = {
    "Viral": ["Kenapa {topik} selalu berakhir begini?",
              "{topik} - kamu tim yang mana?",
              "Jangan lakukan {topik} sebelum tahu ini!"],
    "Jualan": ["Punya masalah {topik}? Ini solusinya.",
               "{topik} bikin pusing? Coba cara ini.",
               "Berapa harga {topik}? Lebih murah dari yang kamu kira."],
    "Edukasi": ["Apa itu {topik}? Dijelaskan 30 detik.",
                "3 hal tentang {topik} yang jarang orang tahu.",
                "Kenapa {topik} penting? Ini jawabannya."],
}

KRITERIA_KONTEN = [
    ("hook", "Hook pembuka kuat"),
    ("format", "Format cocok dengan tujuan"),
    ("pola", "Pola yang terbukti dari riset"),
    ("bukti", "Ada bukti/cek di platform"),
    ("cocok", "Cocok dengan aset Cipta"),
]

KATA_HOOK_KUAT = ["?", "kenapa", "jangan", "ternyata", "rahasia", "gratis",
                  "berakhir", "tim", "coba", "tahu", "penting", "pusing",
                  "solusi", "murah", "hal"]


def nilai_konten(topik, platform, tujuan, hook, bukti):
    topik = (topik or "").strip()
    platform = platform or "Ketiganya"
    tujuan = tujuan or "Viral"
    hook = (hook or "").strip()
    bukti = (bukti or "").strip()
    if not topik:
        return "\u26a0\ufe0f Isi dulu topik/niche kontennya.", "", ""
    if tujuan not in FORMAT_TUJUAN:
        tujuan = "Viral"
    if platform not in CATATAN_PLATFORM:
        platform = "Ketiganya"

    teks_bawah = (topik + " " + tujuan + " " + platform).lower()
    skor = {}
    catatan = {}

    # 1. Hook pembuka
    if hook and len(hook) >= 10 and any(k in hook.lower() for k in KATA_HOOK_KUAT):
        skor["hook"] = 2
        catatan["hook"] = "Hook kuat: ada pertanyaan/konflik/kejutan."
    elif hook:
        skor["hook"] = 1
        catatan["hook"] = ("Hook ditulis, tapi masih umum - tambahkan pertanyaan, "
                           "konflik, atau kejutan di 1 detik pertama.")
    else:
        skor["hook"] = 0
        catatan["hook"] = ("Hook belum ditulis - pakai salah satu dari 3 contoh "
                           "di bawah ini.")

    # 2. Format cocok dengan tujuan
    skor["format"] = 2
    catatan["format"] = ("Format untuk tujuan '" + tujuan + "' sudah ada polanya: "
                         + FORMAT_TUJUAN[tujuan])

    # 3. Pola yang terbukti
    if any(k in teks_bawah for k in ["kucing", "podcast", "dialog", "oyen", "momo"]):
        skor["pola"] = 2
        catatan["pola"] = ("Topik ini cocok dengan pola terverifikasi Goldy & Sapi "
                           "(dialog dua kucing, 10-13 dtk) + format podcast internal.")
    elif any(k in teks_bawah for k in ["anak", "edukasi", "bisnis", "jualan",
                                        "cerita", "nabi", "belajar"]):
        skor["pola"] = 1
        catatan["pola"] = ("Sebagian pola ada (kerangka edukasi/jualan), tapi belum "
                           "ada contoh video terverifikasi untuk topik persis ini - "
                           "cek 5 video sejenis dulu.")
    else:
        skor["pola"] = 0
        catatan["pola"] = ("BELUM CUKUP DATA - belum ada pola terverifikasi untuk "
                           "topik ini. Tonton 5 video sejenis di platform dan catat "
                           "pola hook + durasinya sebelum produksi.")

    # 4. Bukti/cek di platform
    if bukti and ("http" in bukti or "cek" in bukti.lower() or len(bukti) >= 30):
        skor["bukti"] = 2
        catatan["bukti"] = "Ada bukti/cek yang bisa diverifikasi."
    elif bukti:
        skor["bukti"] = 1
        catatan["bukti"] = "Bukti masih lemah - catat judul + views + komentar video sejenis."
    else:
        skor["bukti"] = 0
        catatan["bukti"] = ("BELUM CUKUP DATA - belum ada yang dicek di platform. "
                            "Cek 5 video sejenis (judul, views, komentar yang berulang) "
                            "sebelum produksi.")

    # 5. Cocok dengan aset Cipta
    cocok = [a for a in ASET_CIPTA if a in teks_bawah]
    if cocok:
        skor["cocok"] = 2
        catatan["cocok"] = "Cocok dengan aset Cipta: " + ", ".join(cocok) + "."
    else:
        skor["cocok"] = 0
        catatan["cocok"] = ("Belum jelas cocok dengan aset Cipta (Oyen & Momo, "
                            "podcast kucing, eBook, foto, video, jasa). Bila butuh "
                            "tokoh/skill baru, hitung waktu persiapannya.")

    total = sum(skor.values())
    if total >= 8:
        verdict = "\u2705 LAYAK DICOBA"
        saran = ("Buat 1 video uji dulu (sesuai format di bawah), unggah, dan "
                 "lihat respons 24-48 jam pertama sebelum membuat seri.")
    elif total >= 5:
        verdict = "\U0001f536 PERLU RISET LANJUT"
        saran = ("Jangan produksi dulu. Lengkapi kriteria yang skornya 0-1, "
                 "terutama bukti cek di platform dan pola yang terbukti.")
    else:
        verdict = "\U0001f534 TIDAK DISARANKAN (untuk sekarang)"
        saran = ("Peluang viral kecil dengan data sekarang: hook/pola/bukti "
                 "belum jelas. Perbaiki kerangka di atas atau pilih topik lain.")

    contoh_hook = [h.format(topik=topik) for h in HOOK_CONTOH[tujuan]]
    baris = [f"## Hasil Penilaian Konten - {topik}",
             f"**Platform:** {platform} | **Tujuan:** {tujuan}",
             f"**Skor total: {total}/10 - {verdict}**", ""]
    for kunci, label in KRITERIA_KONTEN:
        baris.append(f"- **{label}: {skor[kunci]}/2** - {catatan[kunci]}")
    baris += ["",
              "### Hook",
              f"- **Hook kamu:** {hook if hook else '(belum ditulis)'}",
              "- **3 contoh hook (pilih/sesuaikan salah satu):**"]
    for h in contoh_hook:
        baris.append(f'  - "{h}"')
    baris += ["",
              "### Format yang cocok",
              f"- **{tujuan}:** {FORMAT_TUJUAN[tujuan]}",
              f"- **{platform}:** {CATATAN_PLATFORM[platform]}",
              "",
              "### Kenapa pola ini berpotensi",
              POLA_KONTEN_TERVERIFIKASI,
              "",
              "**Batas kejujuran:** pola di atas terverifikasi dari 10 video "
              "Goldy & Sapi + data internal Podcast Meong - BUKAN jaminan viral. "
              "Algoritma tiap platform berubah; yang bisa diukur hanya respons "
              "video uji pertama.",
              "",
              "**Langkah verifikasi sebelum produksi:**",
              "1. Tonton 5 video sejenis di platform target - catat judul, views, "
              "dan komentar yang berulang.",
              "2. Cek apakah hook serupa sudah dipakai banyak akun (bila ya, ubah sudutnya).",
              "3. Buat 1 video uji sesuai format di atas; ukur 24-48 jam pertama "
              "(views, like, komentar, share).",
              "4. Bila respons dingin, ganti hook dulu sebelum ganti topik.",
              "",
              f"**Saran:** {saran}",
              DISCLAIMER]
    hasil = "\n".join(baris)

    ai = _gemini(
        "Kamu penasihat riset konten untuk kreator Indonesia bernama Cipta "
        "(Podcast Meong: podcast kucing Oyen & Momo). Nilai ide konten ini "
        "dengan JUJUR. DILARANG mengarang data, tren, atau statistik. Bila "
        "data tidak ada, tulis 'belum cukup data' dan sebut sumber yang "
        "harus dicek. Jangan menjanjikan viral atau penghasilan. Jawab "
        "singkat dalam Bahasa Indonesia, format: Hook (3 contoh), Format "
        "yang cocok, Kenapa berpotensi, Yang harus dicek dulu, Verdict "
        "(Layak dicoba / Perlu riset lanjut / Tidak disarankan).\n\n"
        f"Topik: {topik}\nPlatform: {platform}\nTujuan: {tujuan}\n"
        f"Hook: {hook or '(belum ditulis)'}\n"
        f"Bukti/cek: {bukti or '(tidak ada)'}\n\n"
        "Pola terverifikasi: " + POLA_KONTEN_TERVERIFIKASI)
    if ai:
        hasil += "\n\n---\n### Penilaian AI (Gemini)\n\n" + ai + DISCLAIMER

    ringkas = f"{topik} | {platform} \u00b7 {tujuan} | {total}/10 | {verdict}"
    return hasil, ringkas, f"{topik}||{platform}||{tujuan}||{total}||{verdict}"


def simpan_riset_konten(ringkasan):
    ringkasan = (ringkasan or "").strip()
    if not ringkasan:
        return "\u26a0\ufe0f Belum ada hasil penilaian konten untuk disimpan. Nilai ide konten dulu."
    if "||" not in ringkasan:
        return "\u26a0\ufe0f Format ringkasan tidak dikenal - nilai ulang ide kontennya."
    bagian = ringkasan.split("||")
    if len(bagian) != 5:
        return "\u26a0\ufe0f Format ringkasan tidak dikenal - nilai ulang ide kontennya."
    topik, platform, tujuan, total, verdict = bagian
    ide = f"[{tujuan} \u00b7 {platform}] {topik}"
    data = _load()
    for e in data:
        if e.get("jenis", "produk") == "konten" \
                and e.get("niche", "").lower() == topik.lower() \
                and e.get("ide", "").lower() == ide.lower():
            e["skor"] = total
            e["verdict"] = verdict
            e["tanggal"] = _today()
            _save(data)
            return (f"\U0001f504 Sudah ada di log - diperbarui: {ide} "
                    f"({total}/10, {verdict}).")
    data.append({"jenis": "konten", "niche": topik, "ide": ide,
                 "skor": total, "verdict": verdict, "tanggal": _today()})
    _save(data)
    return f"\u2705 Disimpan ke log riset: {ide} ({total}/10, {verdict})."

# ---------------------------------------------------------------------------
# UI Gradio
# ---------------------------------------------------------------------------
def build_ui():
    with gr.Blocks(title="Agent Riset Produk & Strategi",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🔍 Agent Riset Produk & Strategi — Podcast Meong\n"
            "Riset peluang produk online yang laku, ciptakan produk, dan susun "
            "strategi agar produk laku dan dibutuhkan pasar.\n\n"
            "⚠️ **Aturan kejujuran:** agent tidak mengarang data pasar. Bila data "
            "tidak cukup, tertulis **'belum cukup data'**. Semua output adalah "
            "**DRAF/RENCANA** untuk persetujuan Cipta — bukan janji cuan. "
            "Target Bulan 1 Rp3–25 juta adalah **TARGET**, bukan janji.")
        with gr.Tab("🔍 Riset Peluang"):
            gr.Markdown("Nilai ide produk dengan kerangka jujur 6 kriteria (skor 0–12).")
            with gr.Row():
                niche_in = gr.Textbox(label="Niche / pasar", placeholder="mis. anak, kucing, bisnis, belajar")
                ide_in = gr.Textbox(label="Ide produk", placeholder="mis. eBook dongeng anak Islami")
            masalah_in = gr.Textbox(label="Masalah apa yang diselesaikan produk ini?",
                                    lines=2, placeholder="Tulis masalah nyata customer, sespesifik mungkin")
            customer_in = gr.Textbox(label="Siapa customernya?",
                                     lines=2, placeholder="Usia, kebutuhan, daya beli — sespesifik mungkin")
            bukti_in = gr.Textbox(label="Bukti permintaan (tautan/cek yang sudah dilakukan)",
                                  lines=2, placeholder="mis. tautan produk sejenis di Tokopedia + jumlah ulasan, atau kosong bila belum dicek")
            pesaing_in = gr.Textbox(label="Pesaing (nama + harga/kelemahan)",
                                    lines=2, placeholder="3–5 produk sejenis, atau kosong bila belum dicek")
            harga_in = gr.Textbox(label="Harga usulan", placeholder="mis. Rp29.000")
            nilai_btn = gr.Button("Nilai Peluang", variant="primary")
            hasil_nilai = gr.Markdown()
            with gr.Row():
                ringkas_state = gr.Textbox(label="Ringkasan (otomatis)", visible=False)
                simpan_state = gr.Textbox(label="Data simpan (otomatis)", visible=False)
            simpan_btn = gr.Button("💾 Simpan ke Log Riset")
            simpan_out = gr.Markdown()
            nilai_btn.click(nilai_peluang,
                            inputs=[niche_in, ide_in, masalah_in, customer_in,
                                    bukti_in, pesaing_in, harga_in],
                            outputs=[hasil_nilai, ringkas_state, simpan_state],
                            api_name="nilai_peluang")
            simpan_btn.click(simpan_riset, inputs=[simpan_state],
                             outputs=[simpan_out], api_name="simpan_riset")

        with gr.Tab("🎁 Pencipta Produk"):
            gr.Markdown("Dari masalah customer → rancangan produk (jenis, outline, harga, platform).")
            masalah2_in = gr.Textbox(label="Masalah customer", lines=2,
                                     placeholder="mis. orang tua bingung memilih bacaan anak yang aman")
            customer2_in = gr.Textbox(label="Customer", placeholder="mis. orang tua anak 4–8 tahun")
            jenis_in = gr.Dropdown(choices=JENIS_PRODUK, value="eBook",
                                   label="Jenis produk")
            cipta_btn = gr.Button("Buat Rancangan Produk", variant="primary")
            hasil_cipta = gr.Markdown()
            cipta_btn.click(cipta_produk,
                            inputs=[masalah2_in, customer2_in, jenis_in],
                            outputs=[hasil_cipta], api_name="cipta_produk")

        with gr.Tab("📣 Strategi Penjualan"):
            gr.Markdown("Rencana peluncuran: pra-peluncuran, hari-H, pasca, hook, dan ukuran keberhasilan.")
            produk_in = gr.Textbox(label="Nama produk", placeholder="mis. eBook Nabi Yunus untuk Anak")
            harga2_in = gr.Textbox(label="Harga", placeholder="mis. Rp29.000")
            customer3_in = gr.Textbox(label="Target customer", placeholder="mis. orang tua Muslim anak 5–9 tahun")
            kanal_in = gr.CheckboxGroup(
                choices=["Akun utama Podcast Meong", "5 akun @meongcast",
                         "KaryaKarsa/KBM", "Tokopedia/Shopee",
                         "TikTok Shop / affiliate", "Website sendiri",
                         "WhatsApp/komunitas"],
                value=["Akun utama Podcast Meong", "5 akun @meongcast"],
                label="Kanal promosi")
            strategi_btn = gr.Button("Buat Strategi", variant="primary")
            hasil_strategi = gr.Markdown()
            strategi_btn.click(buat_strategi,
                               inputs=[produk_in, harga2_in, customer3_in, kanal_in],
                               outputs=[hasil_strategi], api_name="buat_strategi")

        with gr.Tab("🧩 Masalah–Solusi"):
            gr.Markdown("Petakan masalah customer di sebuah niche → solusi produk yang mungkin.")
            niche2_in = gr.Textbox(label="Niche", placeholder="mis. anak, kucing, bisnis, belajar, musik")
            peta_btn = gr.Button("Petakan Masalah", variant="primary")
            hasil_peta = gr.Markdown()
            peta_btn.click(peta_masalah, inputs=[niche2_in],
                           outputs=[hasil_peta], api_name="peta_masalah")

        with gr.Tab("\U0001f3ac Riset Konten"):
            gr.Markdown("Nilai ide konten: hook, format yang cocok, dan pola yang terbukti dari riset.")
            topik_in = gr.Textbox(label="Topik / niche konten",
                                  placeholder="mis. kucing minta naik gaji, tips merawat kucing oren")
            with gr.Row():
                platform_in = gr.Dropdown(choices=["TikTok", "YouTube Shorts", "Instagram Reels", "Ketiganya"],
                                          value="Ketiganya", label="Platform")
                tujuan_in = gr.Radio(choices=["Viral", "Jualan", "Edukasi"], value="Viral",
                                     label="Tujuan konten")
            hook_in = gr.Textbox(label="Hook pembuka (opsional - bila kosong, diberi 3 contoh)",
                                 lines=2, placeholder="mis. Kenapa Oyen selalu minta naik gaji?")
            bukti_in = gr.Textbox(label="Apa yang sudah dicek di platform (opsional)",
                                  lines=2, placeholder="mis. 5 video sejenis ditonton; judul + views + komentar dicatat, atau kosong bila belum dicek")
            konten_btn = gr.Button("Nilai Ide Konten", variant="primary")
            hasil_konten = gr.Markdown()
            with gr.Row():
                ringkas_konten = gr.Textbox(label="Ringkasan (otomatis)", visible=False)
                simpan_konten = gr.Textbox(label="Data simpan (otomatis)", visible=False)
            simpan_konten_btn = gr.Button("\U0001f4be Simpan ke Log Riset")
            simpan_konten_out = gr.Markdown()
            konten_btn.click(nilai_konten,
                             inputs=[topik_in, platform_in, tujuan_in, hook_in, bukti_in],
                             outputs=[hasil_konten, ringkas_konten, simpan_konten],
                             api_name="nilai_konten")
            simpan_konten_btn.click(simpan_riset_konten, inputs=[simpan_konten],
                                    outputs=[simpan_konten_out], api_name="simpan_riset_konten")

        with gr.Tab("📒 Log Riset"):
            gr.Markdown("Semua peluang produk & ide konten yang pernah dinilai — agar tidak menilai ulang hal yang sama.")
            log_out = gr.Markdown()
            muat_btn = gr.Button("Muat Log")
            muat_btn.click(tabel_log, outputs=[log_out], api_name="tabel_log")
            with gr.Row():
                hapus_niche = gr.Textbox(label="Niche yang dihapus")
                hapus_ide = gr.Textbox(label="Ide yang dihapus")
            hapus_btn = gr.Button("🗑️ Hapus dari Log")
            hapus_out = gr.Markdown()
            hapus_btn.click(hapus_log, inputs=[hapus_niche, hapus_ide],
                            outputs=[hapus_out, log_out], api_name="hapus_log")
        gr.Markdown(
            "Dibuat untuk Cipta — di bawah komando Muse. Model: Gemini free tier "
            "(bila ada key) atau template lokal. Tanpa key, semua fitur tetap jalan.")
    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
