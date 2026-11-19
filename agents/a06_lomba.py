# ======================================================================
# PUSAT KOMANDO — salinan dari agent-lomba (Agent 6 Lomba).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Lomba Podcast Meong
=========================
Agent AI gratis yang mencari lomba, menilai aturannya, mengingatkan tenggat,
dan mengecek pemenang setelah lomba ditutup.

ATURAN KERAS (tidak boleh dilanggar):
- Agent ini TIDAK PERNAH mendaftar atau mengirim karya apa pun.
- Pendaftaran/pengiriman hanya setelah Cipta menyetujui lomba dan karya persisnya.
- Syarat ikut: GRATIS, AMAN (resmi/legit, Indonesia boleh ikut), AI DIIZINKAN.
- Bila kebijakan AI belum terverifikasi, agent TIDAK BOLEH menyarankan kirim.

Model: Google Gemini free tier (gemini-2.0-flash), API key HANYA dari env var
GEMINI_API_KEY. Tanpa key, agent tetap jalan dalam mode template + database lokal.
Tidak ada layanan berbayar yang dipakai. Telemetri Gradio dimatikan.
"""
import json
import os
import re
from datetime import date, timedelta

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "lomba.json")  # PUSAT KOMANDO: folder data bersama

KATEGORI = ["foto", "video", "puisi", "cerpen", "eBook", "POD", "musik", "lagu",
            "ide usaha", "website", "sistem", "poster/desain", "film",
            "aplikasi", "game", "lainnya"]
KEBIJAKAN_AI = ["diizinkan", "dilarang", "belum terverifikasi"]
STATUS = ["baru", "dicek", "dikirim", "ditolak", "menang", "kalah"]

# ---------------------------------------------------------------------------
# Database awal (terverifikasi 18 Nov 2026 — jangan mengarang lomba baru)
# ---------------------------------------------------------------------------
SEED = [
    {"nama": "AdArena — Micro Drama", "hadiah": "$5.000 (40 pemenang)",
     "tenggat": "2026-11-20", "kategori": "video", "kebijakan_ai": "diizinkan",
     "status": "dikirim",
     "catatan": "The Last Key dikirim 17 Nov (Entry #1 dari 2 kuota). Pemenang ≤7 hari setelah tutup.",
     "cek_berikutnya": "2026-11-27"},
    {"nama": "Kemenkes — Poster Skrining Mata", "hadiah": "Rp6.000.000",
     "tenggat": "2026-11-30", "kategori": "poster/desain",
     "kebijakan_ai": "diizinkan", "status": "dicek",
     "catatan": "2 poster tayang di IG. Formulir draf tersimpan; MENUNGGU surat pernyataan orisinalitas bertanda tangan dari Cipta.",
     "cek_berikutnya": "2026-12-10"},
    {"nama": "Artefact", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-01", "kategori": "film", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Konsep film 'The Number She Never Deleted' sudah draf, menunggu persetujuan Cipta.",
     "cek_berikutnya": ""},
    {"nama": "HeyGen — Video AI", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-01", "kategori": "video", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Butuh akun HeyGen + akun X. Muse bisa pakai MCP HeyGen.",
     "cek_berikutnya": ""},
    {"nama": "Kiroween (Devpost)", "hadiah": "$100.000",
     "tenggat": "2026-12-05", "kategori": "website", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Spookify selesai + Pages live. Akun Devpost DITANGGUHKAN, menunggu banding — JANGAN submit sebelum banding selesai.",
     "cek_berikutnya": ""},
    {"nama": "Deck the Pixels", "hadiah": "$25.000",
     "tenggat": "2026-12-07", "kategori": "poster/desain",
     "kebijakan_ai": "diizinkan", "status": "baru",
     "catatan": "Karya kartu Natal belum jadi — Nano Banana di Firefly gagal 11x. Menunggu keputusan Cipta.",
     "cek_berikutnya": ""},
    {"nama": "AKOOL — AI Video", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-18", "kategori": "video", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Konsep trailer 'The Last Postman of the Moon' sudah draf, menunggu persetujuan Cipta.",
     "cek_berikutnya": ""},
    {"nama": "AOYF (AI Art)", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-20", "kategori": "foto", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Konsep 'The News That Never Happened' sudah draf, menunggu persetujuan Cipta. Tutup 20 Des 23:59 CET.",
     "cek_berikutnya": ""},
    {"nama": "Lirika 14", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-20", "kategori": "puisi",
     "kebijakan_ai": "belum terverifikasi", "status": "baru",
     "catatan": "Kebijakan AI BELUM terverifikasi — JANGAN kirim puisi sebelum membaca pedoman resmi.",
     "cek_berikutnya": ""},
    {"nama": "NEXMUSE", "hadiah": "lihat halaman resmi",
     "tenggat": "2026-12-28", "kategori": "musik", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Prioritas rendah — keterbatasan alat musik.",
     "cek_berikutnya": ""},
    {"nama": "Chroma Awards", "hadiah": "lihat halaman resmi",
     "tenggat": "2027-01-07", "kategori": "film", "kebijakan_ai": "diizinkan",
     "status": "dikirim",
     "catatan": "The Last Key SUBMITTED (ID fdf0dc2e-de40-4654-843d-a1ab2174831b). Pemenang 11 Feb 2027.",
     "cek_berikutnya": "2027-02-11"},
    {"nama": "NMWP (New Media Writing Prize)", "hadiah": "lihat halaman resmi",
     "tenggat": "2027-02-01", "kategori": "website",
     "kebijakan_ai": "belum terverifikasi", "status": "baru",
     "catatan": "Aturan resmi TIDAK menyebut AI — belum terverifikasi. Konsep 'Oyen & the Last Fish' sudah draf.",
     "cek_berikutnya": ""},
    # --- Kategori aplikasi / game / website (perluasan 18 Nov 2026) ---
    {"nama": "Codegeist 2026 (Devpost)", "hadiah": "$120.000",
     "tenggat": "2026-12-22", "kategori": "aplikasi", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Atlassian/Devpost. Bangun aplikasi Forge (Jira/Confluence/Rovo) — AI agent jadi tema utama. Gratis (NO PURCHASE NECESSARY). Indonesia boleh (tidak ada di daftar pengecualian). Pemenang ~15 Feb 2027. BUTUH akun Devpost — akun pemilik sedang ditangguhkan, selesaikan banding dulu.",
     "cek_berikutnya": ""},
    {"nama": "#BuildHybridAI 2026 (Devpost)", "hadiah": "$30.000",
     "tenggat": "2026-11-30", "kategori": "aplikasi", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Google/Firebase. Bangun aplikasi Gen AI via Firebase AI Logic (Web/Android/iOS). Gratis; proyek harus open source + gratis. MEDET — tutup 30 Nov. BUTUH akun Devpost — akun pemilik sedang ditangguhkan.",
     "cek_berikutnya": ""},
    {"nama": "QNX Global Hackathon 2026 (Devpost)", "hadiah": "$50.000",
     "tenggat": "2026-12-15", "kategori": "aplikasi",
     "kebijakan_ai": "belum terverifikasi", "status": "baru",
     "catatan": "BlackBerry/QNX. Bangun software di QNX SDP 8.0 (robotik, medis, otomotif). Gratis; Indonesia boleh. Kebijakan AI TIDAK disebut di aturan resmi — JANGAN kirim sebelum baca rules. BUTUH akun Devpost — akun pemilik sedang ditangguhkan.",
     "cek_berikutnya": ""},
    {"nama": "Reddit's Game of the Day Hackathon (Devpost)", "hadiah": "$35.000",
     "tenggat": "2026-12-08", "kategori": "game", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "Reddit/Devpost. Buat daily game di platform Devvit (web: React/Phaser/three.js atau Godot/Unity). AI diizinkan eksplisit ('Did you use AI? Fantastic!'). Gratis. BUTUH akun Devpost — akun pemilik sedang ditangguhkan.",
     "cek_berikutnya": ""},
    {"nama": "Open Agentic Web Challenge (DevPost)", "hadiah": "$13.000",
     "tenggat": "2027-01-11", "kategori": "website", "kebijakan_ai": "diizinkan",
     "status": "baru",
     "catatan": "World Wide Agentic Web (Cognizant AI Lab, MIT Media Lab NANDA, Mozilla). Bangun website agen AI yang terbuka & saling terhubung. AI adalah inti lomba. Pemenang diumumkan di Davos Jan 2027. BUTUH akun Devpost — akun pemilik sedang ditangguhkan.",
     "cek_berikutnya": ""},
    # --- Dicoret (terverifikasi, disimpan sebagai pengingat agar tidak diulang) ---
    {"nama": "KSEI — Short Video", "hadiah": "Rp54.000.000",
     "tenggat": "2026-11-30", "kategori": "video", "kebijakan_ai": "dilarang",
     "status": "ditolak",
     "catatan": "DICORET: butuh ≥70% rekaman asli — karya AI tidak bisa ikut.",
     "cek_berikutnya": ""},
    {"nama": "Tag Comics", "hadiah": "—",
     "tenggat": "", "kategori": "lainnya", "kebijakan_ai": "dilarang",
     "status": "ditolak",
     "catatan": "DICORET: AI dilarang (terverifikasi di halaman resmi).",
     "cek_berikutnya": ""},
    {"nama": "Writers of the Future", "hadiah": "—",
     "tenggat": "", "kategori": "cerpen", "kebijakan_ai": "dilarang",
     "status": "ditolak",
     "catatan": "DICORET: AI dilarang (terverifikasi di halaman resmi).",
     "cek_berikutnya": ""},
    {"nama": "After the End", "hadiah": "—",
     "tenggat": "", "kategori": "cerpen", "kebijakan_ai": "dilarang",
     "status": "ditolak",
     "catatan": "DICORET: AI dilarang (terverifikasi di halaman resmi).",
     "cek_berikutnya": ""},
    {"nama": "Awwwards — Site of the Day", "hadiah": "—",
     "tenggat": "", "kategori": "website",
     "kebijakan_ai": "belum terverifikasi", "status": "ditolak",
     "catatan": "DICORET: biaya submit $65/€65 per website — lomba berbayar, tidak ada jalur gratis.",
     "cek_berikutnya": ""},
    {"nama": "CSS Design Awards — Website of the Day", "hadiah": "—",
     "tenggat": "", "kategori": "website",
     "kebijakan_ai": "belum terverifikasi", "status": "ditolak",
     "catatan": "DICORET: biaya submit ~$50 per website — lomba berbayar.",
     "cek_berikutnya": ""},
    {"nama": "Game Off 2026 (GitHub)", "hadiah": "— (tanpa hadiah uang)",
     "tenggat": "2026-12-01", "kategori": "game", "kebijakan_ai": "diizinkan",
     "status": "ditolak",
     "catatan": "DICORET: tanpa hadiah uang/fisik — hanya 'nerd cred' + tampil di blog GitHub. AI diizinkan, tapi tidak memenuhi syarat hadiah jelas. Tema 2026: Shift.",
     "cek_berikutnya": ""},
    {"nama": "Global Game Jam 2027", "hadiah": "— (tanpa hadiah uang)",
     "tenggat": "2027-01-31", "kategori": "game",
     "kebijakan_ai": "belum terverifikasi", "status": "ditolak",
     "catatan": "DICORET: tanpa hadiah uang — fokus kreativitas/komunitas; biaya tergantung situs lokal (ada yang berbayar). Kebijakan AI merujuk ke pedoman GGJ — belum terverifikasi. 25–31 Jan 2027.",
     "cek_berikutnya": ""},
]


# ---------------------------------------------------------------------------
# Penyimpanan lokal (lomba.json)
# ---------------------------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    save_data(SEED)
    return [dict(c) for c in SEED]


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse_tanggal(s):
    try:
        return date.fromisoformat(s.strip())
    except (ValueError, AttributeError):
        return None


def tambah_lomba(nama, hadiah, tenggat, kategori, kebijakan_ai, status, catatan):
    nama = (nama or "").strip()
    if not nama:
        return "❌ Nama lomba wajib diisi.", tabel_lomba()
    if tenggat and not _parse_tanggal(tenggat):
        return "❌ Format tenggat salah — pakai YYYY-MM-DD (contoh: 2026-12-20).", tabel_lomba()
    data = load_data()
    if any(c["nama"].lower() == nama.lower() for c in data):
        return f"❌ Lomba '{nama}' sudah ada di database.", tabel_lomba()
    data.append({
        "nama": nama, "hadiah": (hadiah or "—").strip(),
        "tenggat": (tenggat or "").strip(), "kategori": kategori,
        "kebijakan_ai": kebijakan_ai, "status": status,
        "catatan": (catatan or "").strip(), "cek_berikutnya": "",
    })
    save_data(data)
    return f"✅ Lomba '{nama}' ditambahkan.", tabel_lomba()


def ubah_status(nama, status_baru):
    data = load_data()
    for c in data:
        if c["nama"] == nama:
            c["status"] = status_baru
            save_data(data)
            return f"✅ Status '{nama}' diubah menjadi '{status_baru}'.", tabel_lomba()
    return f"❌ Lomba '{nama}' tidak ditemukan.", tabel_lomba()


def tabel_lomba():
    data = load_data()
    rows = [[c["nama"], c["hadiah"], c["tenggat"] or "—", c["kategori"],
             c["kebijakan_ai"], c["status"], c["cek_berikutnya"] or "—"]
            for c in data]
    return rows


def daftar_nama():
    return [c["nama"] for c in load_data()]


# ---------------------------------------------------------------------------
# Penilai lomba (mode template + Gemini bila ada key)
# ---------------------------------------------------------------------------
BIAYA_BEBAS = ["free entry", "free to enter", "no entry fee", "no registration fee",
               "no submission fee", "no fee", "free of charge", "gratis",
               "tanpa biaya", "tanpa biaya pendaftaran", "free", "no cost",
               "no purchase or payment necessary", "no purchase necessary"]
BIAYA_BERBAYAR = ["entry fee", "registration fee", "submission fee",
                   "participation fee", "biaya pendaftaran", "biaya registrasi",
                   "biaya masuk", "entry cost", "pay to enter"]
AI_DILARANG = ["ai is not allowed", "no ai", "ai-generated content is not allowed",
               "ai generated content is not allowed", "ai prohibited", "ai banned",
               "not use ai", "ai dilarang", "dilarang menggunakan ai",
               "must be entirely human", "no ai-generated", "ai not permitted",
               "tidak boleh menggunakan ai", "tidak diizinkan menggunakan ai",
               "ai tidak diperbolehkan"]
AI_DIIZINKAN = ["ai is allowed", "ai allowed", "ai permitted", "ai tools are allowed",
                "ai-assisted", "ai assisted", "ai boleh", "ai diizinkan",
                "ai sebagai alat bantu", "ai welcome", "generative ai",
                "ai-generated", "ai generated", "artificial intelligence",
                "ai agent", "ai-powered"]
INDONESIA_BOLEH = ["open to all", "worldwide", "international", "global",
                    "indonesia", "all countries", "open to everyone",
                    "terbuka untuk umum", "seluruh dunia", "open worldwide"]
INDONESIA_TIDAK = ["us only", "us residents only", "uk only",
                    "students only", "khusus mahasiswa", "united states only",
                    "residents of the united states", "eu only"]


def _cek_frasa(teks, frasa_list):
    return [f for f in frasa_list if f in teks]


def nilai_template(teks):
    """Penilaian berbasis kata kunci. Jujur: yang tidak disebut = belum terverifikasi."""
    t = " " + re.sub(r"\s+", " ", teks.lower()) + " "
    hasil = {}

    # 1) Biaya
    if _cek_frasa(t, BIAYA_BEBAS):
        hasil["biaya"] = ("GRATIS", "ditemukan frasa bebas biaya: " +
                          ", ".join(_cek_frasa(t, BIAYA_BEBAS)[:3]))
    elif _cek_frasa(t, BIAYA_BERBAYAR):
        hasil["biaya"] = ("BERBAYAR", "ditemukan frasa biaya: " +
                          ", ".join(_cek_frasa(t, BIAYA_BERBAYAR)[:3]))
    else:
        hasil["biaya"] = ("TIDAK DISEBUT", "teks tidak menyebut biaya pendaftaran — verifikasi di halaman resmi")

    # 2) Kebijakan AI — cek larangan dulu (lebih kuat), lalu izin
    if _cek_frasa(t, AI_DILARANG):
        hasil["ai"] = ("DILARANG", "ditemukan: " + ", ".join(_cek_frasa(t, AI_DILARANG)[:3]))
    elif _cek_frasa(t, AI_DIIZINKAN):
        hasil["ai"] = ("DIIZINKAN", "ditemukan: " + ", ".join(_cek_frasa(t, AI_DIIZINKAN)[:3]))
    elif "ai" in t or "artificial intelligence" in t:
        hasil["ai"] = ("BELUM TERVERIFIKASI", "AI disebut tapi kebijakannya tidak jelas dari teks ini")
    else:
        hasil["ai"] = ("BELUM TERVERIFIKASI", "teks tidak menyebut AI sama sekali")

    # 3) Indonesia boleh ikut?
    if _cek_frasa(t, INDONESIA_TIDAK):
        hasil["indonesia"] = ("TIDAK BOLEH", "ditemukan batasan: " + ", ".join(_cek_frasa(t, INDONESIA_TIDAK)[:3]))
    elif _cek_frasa(t, INDONESIA_BOLEH):
        hasil["indonesia"] = ("BOLEH", "ditemukan: " + ", ".join(_cek_frasa(t, INDONESIA_BOLEH)[:3]))
    else:
        hasil["indonesia"] = ("TIDAK DISEBUT", "teks tidak menyebut wilayah peserta — verifikasi di halaman resmi")

    # 4) Keamanan (penyelenggara / hadiah / tenggat disebut?)
    sinyal = [s for s in ["prize", "hadiah", "deadline", "closes", "tutup",
                          "organizer", "penyelenggara", "jury", "juri"]
              if s in t]
    if len(sinyal) >= 2:
        hasil["aman"] = ("CUKUP JELAS", "disebut: " + ", ".join(sinyal[:4]))
    elif sinyal:
        hasil["aman"] = ("KURANG INFO", "hanya disebut: " + ", ".join(sinyal) +
                         " — verifikasi penyelenggara & hadiah di halaman resmi")
    else:
        hasil["aman"] = ("KURANG INFO", "tidak disebut penyelenggara, hadiah, atau tenggat — verifikasi dulu")

    # Verdict akhir
    if hasil["biaya"][0] == "BERBAYAR":
        verdict = "⛔ TIDAK LAYAK — lomba berbayar."
    elif hasil["ai"][0] == "DILARANG":
        verdict = "⛔ TIDAK LAYAK — AI dilarang."
    elif hasil["indonesia"][0] == "TIDAK BOLEH":
        verdict = "⛔ TIDAK LAYAK — Indonesia tidak boleh ikut."
    elif hasil["ai"][0] == "BELUM TERVERIFIKASI":
        verdict = "⏸️ JANGAN KIRIM DULU — kebijakan AI belum terverifikasi. Baca pedoman resmi sebelum memutuskan."
    elif hasil["biaya"][0] == "TIDAK DISEBUT" or hasil["indonesia"][0] == "TIDAK DISEBUT":
        verdict = "⚠️ PERLU VERIFIKASI LEBIH LANJUT — ada syarat yang tidak disebut di teks ini."
    elif hasil["aman"][0] == "KURANG INFO":
        verdict = "⚠️ PERLU VERIFIKASI LEBIH LANJUT — cek penyelenggara & hadiah di halaman resmi."
    else:
        verdict = "✅ LAYAK IKUT — gratis, AI diizinkan, Indonesia boleh, info cukup jelas."
    return hasil, verdict


def _nilai_gemini(teks):
    """Coba nilai dengan Gemini; kembalikan None bila gagal (fallback ke template)."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "Kamu penilai lomba untuk kreator Indonesia yang karyanya dibuat dengan AI.\n"
            "Nilai teks aturan lomba berikut dan jawab dalam Bahasa Indonesia dengan format persis ini:\n"
            "BIAYA: <GRATIS / BERBAYAR / TIDAK DISEBUT> - <alasan singkat>\n"
            "AI: <DIIZINKAN / DILARANG / BELUM TERVERIFIKASI> - <alasan singkat>\n"
            "INDONESIA: <BOLEH / TIDAK BOLEH / TIDAK DISEBUT> - <alasan singkat>\n"
            "AMAN: <CUKUP JELAS / KURANG INFO> - <alasan singkat>\n"
            "VERDICT: <LAYAK IKUT / JANGAN KIRIM DULU / TIDAK LAYAK / PERLU VERIFIKASI> - <alasan singkat>\n"
            "Aturan: bila teks tidak menyebut AI, jawab BELUM TERVERIFIKASI dan verdict JANGAN KIRIM DULU. "
            "Jangan mengarang. Bila ragu, katakan tidak disebut.\n\nTeks aturan:\n" + teks
        )
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        print("Gemini gagal, fallback ke template:", e)
        return None


def nilai_lomba(teks, nama_lomba=""):
    teks = (teks or "").strip()
    if len(teks) < 20:
        return "❌ Tempel teks aturan lomba (minimal 20 karakter). Bila hanya punya tautan, buka halamannya dan salin teks aturannya ke sini."
    hasil, verdict = nilai_template(teks)
    mode = "template (tanpa API key)"
    tambahan = ""
    gemini = _nilai_gemini(teks)
    if gemini:
        mode = "Gemini (gemini-2.0-flash)"
        tambahan = "\n\n---\n**Penilaian Gemini:**\n\n" + gemini
    judul = f"## Penilaian: {nama_lomba.strip() or '(tanpa nama)'}\n\n"
    baris = [f"- **Biaya:** {hasil['biaya'][0]} — {hasil['biaya'][1]}",
             f"- **Kebijakan AI:** {hasil['ai'][0]} — {hasil['ai'][1]}",
             f"- **Indonesia boleh ikut:** {hasil['indonesia'][0]} — {hasil['indonesia'][1]}",
             f"- **Keamanan/kejelasan:** {hasil['aman'][0]} — {hasil['aman'][1]}",
             "", f"### {verdict}",
             "",
             "⚠️ Agent ini TIDAK PERNAH mendaftar/mengirim. Bila verdict LAYAK, tetap tunggu persetujuan Cipta atas lomba dan karya persisnya.",
             f"\n_Mode: {mode}_"]
    return judul + "\n".join(baris) + tambahan


# ---------------------------------------------------------------------------
# Pengingat tenggat & cek pasca-tutup
# ---------------------------------------------------------------------------
def pengingat_tenggat():
    hari_ini = date.today()
    data = load_data()
    mendesak, dekat, lama = [], [], []
    for c in data:
        if c["status"] in ("ditolak", "menang", "kalah"):
            continue
        tg = _parse_tanggal(c["tenggat"])
        if not tg:
            continue
        sisa = (tg - hari_ini).days
        baris = f"- **{c['nama']}** — {c['hadiah']} — tenggat {c['tenggat']} ({sisa} hari lagi) — AI: {c['kebijakan_ai']} — status: {c['status']}"
        if sisa < 0:
            continue  # sudah tutup, masuk daftar cek pasca-tutup
        elif sisa <= 7:
            mendesak.append(baris)
        elif sisa <= 30:
            dekat.append(baris)
        else:
            lama.append(baris)
    out = [f"# ⏰ Pengingat Tenggat — {hari_ini.isoformat()}", ""]
    out.append("## 🔴 ≤ 7 hari (mendesak)")
    out += mendesak if mendesak else ["- Tidak ada."]
    out.append("")
    out.append("## 🟡 8–30 hari")
    out += dekat if dekat else ["- Tidak ada."]
    out.append("")
    out.append("## 🟢 > 30 hari")
    out += lama if lama else ["- Tidak ada."]
    return "\n".join(out)


def cek_pasca_tutup():
    hari_ini = date.today()
    data = load_data()
    belum, sudah_dicek = [], []
    for c in data:
        tg = _parse_tanggal(c["tenggat"])
        if not tg or tg >= hari_ini:
            continue
        if c["status"] in ("ditolak",):
            continue
        cek = _parse_tanggal(c["cek_berikutnya"]) if c["cek_berikutnya"] else tg + timedelta(days=7)
        baris = (f"- **{c['nama']}** — tutup {c['tenggat']} — status: {c['status']} — "
                 f"cek berikutnya: {cek.isoformat() if cek else '—'} — {c['catatan']}")
        if c["status"] in ("menang", "kalah"):
            sudah_dicek.append(baris)
        else:
            belum.append(baris)
    out = [f"# 🏆 Cek Pasca-Tutup — {hari_ini.isoformat()}", "",
           "Aturan: SETIAP lomba, setelah ditutup, dicek kembali. Bila menang, tanyakan kapan hadiah bisa diambil.", ""]
    out.append("## 🔎 Sudah tutup, BELUM dicek hasilnya")
    out += belum if belum else ["- Tidak ada."]
    out.append("")
    out.append("## ✅ Sudah dicek (menang/kalah)")
    out += sudah_dicek if sudah_dicek else ["- Belum ada."]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# UI Gradio
# ---------------------------------------------------------------------------
def build_app():
    import gradio as gr

    with gr.Blocks(title="Agent Lomba Podcast Meong", analytics_enabled=False) as app:
        gr.Markdown(
            "# 🏆 Agent Lomba Podcast Meong\n"
            "Mencari lomba, menilai aturan, mengingatkan tenggat, dan mengecek pemenang.\n\n"
            "⚠️ **Aturan keras:** agent ini TIDAK PERNAH mendaftar atau mengirim karya. "
            "Pendaftaran/pengiriman hanya setelah Cipta menyetujui lomba dan karya persisnya.\n"
            "Syarat ikut: **GRATIS, AMAN, AI DIIZINKAN**. Bila kebijakan AI belum terverifikasi — JANGAN kirim."
        )
        with gr.Tabs():
            with gr.Tab("📋 Database Lomba"):
                tabel = gr.Dataframe(
                    headers=["Nama", "Hadiah", "Tenggat", "Kategori", "Kebijakan AI", "Status", "Cek berikutnya"],
                    value=tabel_lomba, interactive=False, wrap=True)
                btn_refresh = gr.Button("🔄 Muat Ulang")
                gr.Markdown("### Tambah lomba baru")
                with gr.Row():
                    in_nama = gr.Textbox(label="Nama lomba")
                    in_hadiah = gr.Textbox(label="Hadiah")
                    in_tenggat = gr.Textbox(label="Tenggat (YYYY-MM-DD)", placeholder="2026-12-20")
                with gr.Row():
                    in_kategori = gr.Dropdown(KATEGORI, value="video", label="Kategori")
                    in_kebijakan = gr.Dropdown(KEBIJAKAN_AI, value="belum terverifikasi", label="Kebijakan AI")
                    in_status = gr.Dropdown(STATUS, value="baru", label="Status")
                in_catatan = gr.Textbox(label="Catatan", lines=2)
                out_tambah = gr.Textbox(label="Hasil", interactive=False)
                btn_tambah = gr.Button("➕ Tambah Lomba")
                gr.Markdown("### Ubah status lomba")
                with gr.Row():
                    in_nama_status = gr.Dropdown(daftar_nama(), label="Lomba")
                    in_status_baru = gr.Dropdown(STATUS, value="dicek", label="Status baru")
                out_status = gr.Textbox(label="Hasil", interactive=False)
                btn_status = gr.Button("✏️ Ubah Status")

                btn_tambah.click(tambah_lomba,
                                 [in_nama, in_hadiah, in_tenggat, in_kategori, in_kebijakan, in_status, in_catatan],
                                 [out_tambah, tabel], api_name="tambah_lomba")
                btn_status.click(ubah_status, [in_nama_status, in_status_baru], [out_status, tabel], api_name="ubah_status")
                btn_refresh.click(lambda: tabel_lomba(), None, tabel, api_name="tabel_lomba")

            with gr.Tab("🔍 Penilai Lomba"):
                gr.Markdown("Tempel teks aturan lomba (dari halaman resmi). Agent menilai: gratis? aman? AI diizinkan? Indonesia boleh?")
                in_nama_nilai = gr.Textbox(label="Nama lomba (opsional)")
                in_teks = gr.Textbox(label="Teks aturan lomba", lines=10,
                                     placeholder="Tempel di sini... contoh: 'This contest is free to enter, open worldwide. AI-generated images are allowed.'")
                btn_nilai = gr.Button("🔍 Nilai Lomba")
                out_nilai = gr.Markdown()
                btn_nilai.click(nilai_lomba, [in_teks, in_nama_nilai], out_nilai, api_name="nilai_lomba")

            with gr.Tab("⏰ Pengingat Tenggat"):
                btn_tenggat = gr.Button("🔄 Lihat Pengingat")
                out_tenggat = gr.Markdown(value=pengingat_tenggat())
                btn_tenggat.click(pengingat_tenggat, None, out_tenggat, api_name="pengingat_tenggat")

            with gr.Tab("🏆 Cek Pasca-Tutup"):
                btn_cek = gr.Button("🔄 Lihat Daftar Cek")
                out_cek = gr.Markdown(value=cek_pasca_tutup())
                btn_cek.click(cek_pasca_tutup, None, out_cek, api_name="cek_pasca_tutup")
                gr.Markdown("Setelah hasil dicek, ubah status lomba di tab **Database Lomba** menjadi `menang` atau `kalah`.")
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    build_app().launch(server_name="0.0.0.0", server_port=port)
