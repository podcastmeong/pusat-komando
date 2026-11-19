# ======================================================================
# PUSAT KOMANDO — salinan dari agent-11-oyen (Agent 11 Oyen).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Perubahan dari aslinya:
# - aset (tokoh.json, avatars/, samples/, latar/) dipindah ke
#   agents/oyen/ di pusat-komando/ (ditandai komentar 'PUSAT KOMANDO')
# - output audio ditulis ke folder output/<tokoh>/ bersama
#   (ditandai komentar 'PUSAT KOMANDO')
# - log penjagaan ditulis ke data/log-penjagaan-<tokoh>.json bersama
#   (ditandai komentar 'PUSAT KOMANDO')
# - SUARA PERMANEN tetap terkunci: Oyen MAI_01 speed 110 — tidak ada kontrol UI untuk mengubahnya.
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent 11 — Oyen (Penjaga Konsistensi Tokoh Oyen) — Podcast Meong
================================================================
Dibuat 18 Nov 2026 atas perintah Cipta (tugas harian poin 26).

Tugas: menjaga wajah + suara + sifat + gaya dialog Oyen SELALU SAMA di
setiap konten. Agent ini HANYA mengurus Oyen — Momo diurus Agent 12.

SUARA DAN WAJAH PERMANEN — JANGAN DIUBAH (Cipta, 18 Nov 2026 22:31):
Oyen = kucing oren, mata besar, ekspresif, polos-kaget.
Suara: avocado_v2:MAI_01, speed 110, bahasa id (dialog bisa Inggris),
tinggi, ceria, hangat, target pitch >200 Hz (kisaran 220-350),
pitch sampel permanen 278,0 Hz. Dikunci di tokoh.json — aplikasi ini
TIDAK menyediakan kontrol UI untuk mengubah apa pun di kartu tokoh.
Perubahan hanya lewat edit tokoh.json oleh Muse atas perintah eksplisit
Cipta.

Fitur:
1) Kartu Tokoh Terkunci — avatar, suara, sifat, gaya dialog, voice lock
   EN+ID, pemutar audio sampel permanen. Hanya tampil, tidak bisa diubah.
2) Penjaga Konsistensi — periksa draf (dialog / prompt / deskripsi adegan /
   hasil cek pitch) terhadap kartu terkunci. Verdict LULUS / PERLU
   PERBAIKAN / BELUM CUKUP DATA + daftar penyimpangan + saran perbaikan.
   Mode Gemini (bila env var GEMINI_API_KEY ada, model gemini-2.0-flash)
   dengan verifikasi aturan dasar di kode; tanpa kunci, mode template.
3) Buat Baris Dialog — 1 baris dialog bahasa Inggris 17-25 kata (jumlah
   kata dihitung dan ditampilkan), voice lock yang dipakai, script TTS,
   perintah tts CLI, dan — bila /opt/hatch/bin/tts tersedia — audio TTS
   + cek pitch energy-gated (target >200 Hz).
4) Log Penjagaan — setiap pemeriksaan dan setiap baris dialog dicatat ke
   data/log-penjagaan.json dan ditampilkan sebagai tabel.

Semua output adalah DRAF untuk persetujuan Cipta. Tidak ada yang otomatis
upload / kirim / bayar. Tidak ada layanan berbayar. Telemetri Gradio mati.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime

import gradio as gr

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "oyen")  # PUSAT KOMANDO: aset di agents/oyen/
TOKOH_PATH = os.path.join(BASE, "tokoh.json")
LOG_PATH = os.path.join(  # PUSAT KOMANDO: log ke data/ bersama
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "log-penjagaan-oyen.json")
OUTPUT_DIR = os.path.join(  # PUSAT KOMANDO: folder output/ bersama
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "output", "oyen")
TTS_CLI = "/opt/hatch/bin/tts"
PITCH_SCRIPT = os.path.expanduser("~/workspace/audio-tools/pitch_gated.py")
VENV_PYTHON = os.path.expanduser("~/workspace/audio-tools/python-packages/bin/python")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

with open(TOKOH_PATH, encoding="utf-8") as f:
    TOKOH = json.load(f)

SUARA = TOKOH["suara"]
VOICE_ID = SUARA["voice_id"]
SPEED = SUARA["speed"]
PITCH_MIN = SUARA["pitch_target_min_hz"]
PITCH_MAX = SUARA["pitch_target_max_hz"]
PITCH_SAMPEL = SUARA["pitch_sampel_permanen_hz"]
VOICE_LOCK_EN = TOKOH["voice_lock_en"]
VOICE_LOCK_ID = TOKOH["voice_lock_id"]

LATAR_PILIHAN = [
    ("Pantai", "pantai"),
    ("Studio Podcast", "studio"),
    ("Kustom (tulis sendiri)", "kustom"),
]

# ---------------------------------------------------------------------------
# Utilitas umum
# ---------------------------------------------------------------------------
def hitung_kata(teks):
    """Hitung kata: pisah spasi, abaikan token kosong."""
    return len([w for w in (teks or "").split() if w.strip()])


def _sekarang():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def catat_log(jenis, ringkasan, verdict, pitch=None):
    """Tambah satu entri ke data/log-penjagaan.json. Mengembalikan daftar log."""
    try:
        log = baca_log()
    except Exception:  # noqa: BLE001 — log rusak: mulai baru
        log = []
    log.append({
        "tanggal": _sekarang(),
        "jenis": jenis,
        "ringkasan": (ringkasan or "")[:200],
        "verdict": verdict,
        "pitch_hz": pitch,
    })
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
    except Exception:  # noqa: BLE001 — log gagal ditulis: jangan matikan fitur
        pass
    return log


def baca_log():
    if not os.path.isfile(LOG_PATH):
        return []
    with open(LOG_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def log_ke_tabel():
    """Kembalikan isi log sebagai daftar baris untuk gr.Dataframe."""
    baris = []
    for e in baca_log():
        baris.append([
            e.get("tanggal", ""),
            e.get("jenis", ""),
            e.get("ringkasan", ""),
            e.get("verdict", ""),
            "" if e.get("pitch_hz") is None else str(e.get("pitch_hz")),
        ])
    return baris


# ---------------------------------------------------------------------------
# Penjaga Konsistensi (aturan berbasis kartu terkunci)
# ---------------------------------------------------------------------------
# Sifat yang BERTENTANGAN dengan Oyen (bila Oyen digambarkan begini -> menyimpang).
SIFAT_BERTENTANGAN = [
    "datar", "sinis", "dingin", "murung", "galak", "pemarah", "pendiam",
    "serius", "kaku", "cuek", "sombong", "angkuh", "pemalas", "penakut",
    "suara rendah", "nada rendah", "pelan dan datar", "berbisik pelan",
]
# Ciri wajah yang BERTENTANGAN dengan Oyen (oren, mata besar, ekspresif).
WAJAH_BERTENTANGAN = [
    "abu-abu", "abu abu", "hitam", "putih", "cokelat", "coklat",
    "mata kecil", "mata sipit", "tidak ekspresif", "tanpa ekspresi",
    "sphynx", "tanpa bulu", "botak",
]
# Kata tempat yang dikenal — dipakai untuk cek latar vs judul.
TEMPAT_KATA = {
    "pantai": ["pantai", "beach", "laut", "pasir", "ombak"],
    "studio": ["studio", "ruang podcast", "meja podcast"],
    "dapur": ["dapur", "kitchen"],
    "kolam": ["kolam", "pond"],
    "pasar": ["pasar", "market"],
    "taman": ["taman", "garden"],
    "jalan": ["jalan", "street"],
    "kafe": ["kafe", "cafe", "coffee"],
    "hutan": ["hutan", "forest"],
}


def _tempat_dari_teks(teks):
    rendah = (teks or "").lower()
    ketemu = set()
    for nama, kata_kunci in TEMPAT_KATA.items():
        if any(k in rendah for k in kata_kunci):
            ketemu.add(nama)
    return ketemu


def _cek_pitch_disebut(teks):
    """Cari angka pitch yang disebut di draf. Kembalikan list (angka, konteks)."""
    hasil = []
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*hz", (teks or "").lower()):
        try:
            hasil.append((float(m.group(1).replace(",", ".")), teks[max(0, m.start() - 30):m.end() + 10]))
        except ValueError:
            continue
    for m in re.finditer(r"pitch[^0-9]{0,20}(\d+(?:[.,]\d+)?)", (teks or "").lower()):
        try:
            hasil.append((float(m.group(1).replace(",", ".")), teks[max(0, m.start() - 10):m.end() + 10]))
        except ValueError:
            continue
    return hasil


def cek_aturan_dasar(draf, judul=""):
    """Periksa draf dengan aturan kartu terkunci. Kembalikan list penyimpangan.

    Tiap penyimpangan: (kategori, temuan, saran).
    """
    menyimpang = []
    rendah = (draf or "").lower()

    # 1) Suara: voice_id lain disebut.
    for m in re.finditer(r"(?:avocado_v2:)?mai_(\d+)", rendah):
        if m.group(1) != "01":
            menyimpang.append((
                "suara",
                f"voice_id lain disebut: MAI_{m.group(1)} (bukan MAI_01).",
                "Ganti ke voice_id terkunci Oyen: avocado_v2:MAI_01, speed 110.",
            ))
    if re.search(r"mai_03|momo.*voice|voice.*momo", rendah) and "oyen" in rendah:
        # MAI_03 adalah suara Momo — bila dikaitkan ke Oyen, itu menyimpang.
        if "oyen" in rendah and re.search(r"oyen[^.]{0,60}mai_03|mai_03[^.]{0,60}oyen", rendah):
            menyimpang.append((
                "suara",
                "Suara Momo (MAI_03) dikaitkan ke Oyen.",
                "Oyen HANYA memakai MAI_01. MAI_03 itu suara Momo (Agent 12).",
            ))
    m_speed = re.search(r"speed\s*[:=]?\s*(\d+)", rendah)
    if m_speed and int(m_speed.group(1)) != SPEED:
        menyimpang.append((
            "suara",
            f"Speed {m_speed.group(1)} disebut (terkunci: {SPEED}).",
            f"Pakai speed {SPEED} untuk Oyen — jangan diubah.",
        ))

    # 2) Pitch: angka pitch disebut dan di luar target >200 Hz (220-350).
    for angka, konteks in _cek_pitch_disebut(draf):
        if angka < PITCH_MIN or angka > PITCH_MAX:
            menyimpang.append((
                "suara",
                f"Pitch {angka:g} Hz disebut (di luar target {PITCH_MIN:g}-{PITCH_MAX:g} Hz).",
                "Suara Oyen harus tinggi (>200 Hz, kisaran 220-350). "
                "Generate ulang dengan MAI_01 speed 110, lalu cek pitch lagi; "
                "keputusan akhir tetap telinga Cipta.",
            ))

    # 3) Sifat: Oyen digambarkan dengan sifat yang bertentangan.
    for sifat in SIFAT_BERTENTANGAN:
        if sifat in rendah:
            # Pastikan sifat itu menempel ke Oyen, bukan ke Momo.
            idx = rendah.find(sifat)
            sekitar = rendah[max(0, idx - 40):idx + len(sifat) + 10]
            if "momo" not in sekitar:
                menyimpang.append((
                    "sifat",
                    f"Oyen digambarkan '{sifat}' — bertentangan dengan sifat terkunci "
                    "(polos, kaget, ceria, klaim absurd, mudah jatuh cinta, penasaran).",
                    "Tulis Oyen sebagai kucing oren yang polos, kaget, dan ceria — "
                    "bukan datar/sinis (itu sifat Momo).",
                ))
                break

    # 4) Wajah: Oyen digambarkan dengan ciri wajah yang salah.
    for ciri in WAJAH_BERTENTANGAN:
        if ciri in rendah:
            idx = rendah.find(ciri)
            sekitar = rendah[max(0, idx - 40):idx + len(ciri) + 10]
            if "momo" not in sekitar:
                menyimpang.append((
                    "wajah",
                    f"Wajah Oyen digambarkan '{ciri}' — bertentangan dengan kartu "
                    "(kucing oren, mata besar, ekspresif).",
                    "Pakai gambar avatar tetap avatars/oyen-avatar.jpg sebagai "
                    "Start frame; jangan generate ulang wajah Oyen dari nol.",
                ))
                break

    # 5) Tempat: latar tidak mengikuti judul (bila judul diisi).
    judul_rendah = (judul or "").lower().strip()
    if judul_rendah:
        tempat_judul = _tempat_dari_teks(judul_rendah)
        tempat_draf = _tempat_dari_teks(draf)
        lain = tempat_draf - tempat_judul
        if tempat_judul and lain:
            menyimpang.append((
                "tempat",
                f"Latar di draf ({', '.join(sorted(lain))}) tidak mengikuti judul "
                f"('{judul}', tempat: {', '.join(sorted(tempat_judul))}).",
                "Latar SELALU mengikuti judul (aturan kualitas #4). "
                "Ganti latar draf agar sama dengan tempat di judul.",
            ))

    # 6) Dialog: Oyen tidak bicara / bukan baris Oyen.
    if "oyen" not in rendah and "momo" in rendah:
        menyimpang.append((
            "sifat",
            "Draf hanya menyebut Momo, tidak ada Oyen — ini bukan baris Oyen.",
            "Agent 11 hanya menjaga Oyen. Baris Momo diperiksa Agent 12.",
        ))

    return menyimpang


def _cek_gemini(draf, judul):
    """Minta Gemini menilai draf. Kembalikan teks mentah atau None bila gagal."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=kunci)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "Kamu adalah penjaga konsistensi tokoh Oyen (Podcast Meong). "
            "Kartu tokoh Oyen yang TERKUNCI:\n"
            f"- Nama: Oyen, {TOKOH['deskripsi']}, peran: {TOKOH['peran']}.\n"
            f"- Suara PERMANEN: {VOICE_ID}, speed {SPEED}, bahasa id "
            f"(dialog bisa Inggris), sifat: {SUARA['sifat']}, "
            f"target pitch >{PITCH_MIN:g} Hz (kisaran {PITCH_MIN:g}-{PITCH_MAX:g}), "
            f"pitch sampel permanen {PITCH_SAMPEL:g} Hz.\n"
            f"- Voice lock EN: {VOICE_LOCK_EN}\n"
            f"- Voice lock ID: {VOICE_LOCK_ID}\n"
            f"- Sifat dialog: {', '.join(TOKOH['sifat_dialog'])}. "
            "Hook absurd di kalimat pertama. Lawan bicara utama: Momo "
            "(skeptis, datar-sinis) — baris Oyen merespons Momo.\n"
            f"Judul konten: {judul or '(tidak diisi)'}\n\n"
            "Draf yang harus diperiksa:\n"
            f"{draf}\n\n"
            "Nilai apakah draf ini KONSISTEN dengan kartu terkunci di atas. "
            "Periksa: suara (voice_id/speed/pitch), wajah (oren, mata besar, "
            "ekspresif), tempat (latar harus mengikuti judul bila judul diisi), "
            "sifat (polos/kaget/ceria, bukan datar/sinis — itu sifat Momo). "
            "Jawab dengan format persis ini:\n"
            "VERDICT: LULUS atau PERLU PERBAIKAN\n"
            "PENYIMPANGAN:\n"
            "- [kategori] temuan — saran perbaikan\n"
            "(tulis 'tidak ada' bila tidak ada penyimpangan)\n"
            "SARAN: satu-dua kalimat saran perbaikan bila ada penyimpangan."
        )
        r = model.generate_content(prompt)
        return (r.text or "").strip()
    except Exception as e:  # noqa: BLE001 — Gemini gagal: jatuh ke mode template
        return f"__GEMINI_GAGAL__: {e}"


def periksa_konsistensi(draf, judul=""):
    """Periksa satu draf. Kembalikan (verdict, laporan, tabel_log).

    Verdict: LULUS / PERLU PERBAIKAN / BELUM CUKUP DATA.
    """
    draf = (draf or "").strip()
    judul = (judul or "").strip()
    if not draf or len(draf) < 10 or hitung_kata(draf) < 3:
        verdict = "BELUM CUKUP DATA"
        laporan = (
            "BELUM CUKUP DATA — draf kosong atau terlalu pendek untuk dinilai.\n"
            "Isi draf yang bisa diperiksa: dialog, prompt, deskripsi adegan, "
            "atau hasil cek pitch (mis. 'Oyen MAI_01 speed 110, pitch 278 Hz')."
        )
        catat_log("pemeriksaan", draf or "(kosong)", verdict)
        return verdict, laporan, log_ke_tabel()

    menyimpang = cek_aturan_dasar(draf, judul)
    mode = "template (aturan kartu terkunci)"
    gemini_teks = _cek_gemini(draf, judul)
    if gemini_teks:
        if gemini_teks.startswith("__GEMINI_GAGAL__"):
            mode = "template (aturan kartu terkunci) — Gemini gagal: " + gemini_teks[len("__GEMINI_GAGAL__: "):][:150]
        else:
            mode = "Gemini (gemini-2.0-flash) + verifikasi aturan dasar di kode"
            # Ambil verdict Gemini, tapi aturan dasar di kode tetap berlaku.
            if "PERLU PERBAIKAN" in gemini_teks.upper():
                pass  # verdict akhir ditentukan gabungan di bawah
            # Tarik baris penyimpangan Gemini yang belum tertangkap aturan dasar.
            for baris in gemini_teks.splitlines():
                b = baris.strip()
                if b.startswith("- ") and len(b) > 4:
                    isi = b[2:].strip()
                    if not any(isi[:25].lower() in m[1].lower() for m in menyimpang):
                        kat = "umum"
                        for k in ("suara", "wajah", "tempat", "sifat"):
                            if k in isi.lower()[:30]:
                                kat = k
                                break
                        menyimpang.append((kat, f"(Gemini) {isi}", "Lihat saran Gemini di bawah."))

    if menyimpang:
        verdict = "PERLU PERBAIKAN"
        baris_laporan = [f"⛔ VERDICT: {verdict}  |  Mode: {mode}", ""]
        baris_laporan.append(f"Penyimpangan ditemukan: {len(menyimpang)}")
        for i, (kat, temuan, saran) in enumerate(menyimpang, 1):
            baris_laporan.append(f"{i}. [{kat.upper()}] {temuan}")
            baris_laporan.append(f"   Saran: {saran}")
        if gemini_teks and not gemini_teks.startswith("__GEMINI_GAGAL__"):
            baris_laporan.append("")
            baris_laporan.append("Penilaian Gemini (mentah):")
            baris_laporan.append(gemini_teks)
    else:
        verdict = "LULUS"
        baris_laporan = [f"✅ VERDICT: {verdict}  |  Mode: {mode}", ""]
        baris_laporan.append(
            "Tidak ada penyimpangan terhadap kartu terkunci Oyen: "
            f"suara {VOICE_ID} speed {SPEED}, target pitch >{PITCH_MIN:g} Hz, "
            "wajah oren mata besar ekspresif, sifat polos-kaget-ceria."
        )
        if judul:
            baris_laporan.append(f"Latar mengikuti judul '{judul}' (bila ada tempat di draf).")
        if gemini_teks and not gemini_teks.startswith("__GEMINI_GAGAL__"):
            baris_laporan.append("")
            baris_laporan.append("Penilaian Gemini (mentah):")
            baris_laporan.append(gemini_teks)
    laporan = "\n".join(baris_laporan)
    catat_log("pemeriksaan", draf, verdict)
    return verdict, laporan, log_ke_tabel()


# ---------------------------------------------------------------------------
# Buat Baris Dialog (template + Gemini bila ada)
# ---------------------------------------------------------------------------
# Baris template — SUDAH dihitung: masing-masing 25 kata. Dipilih sesuai tema.
TEMPLATE_BARIS = {
    "bulan_ikan": (
        "Momo, the moon is literally made of fried fish, and I can smell the "
        "crispy deliciousness all the way from our little podcast table tonight!",
        "bulan / ikan goreng",
    ),
    "cinta": (
        "Momo, I fell in love with the prettiest cat at the beach, and my heart "
        "is beating like a drum of pure happiness right now!",
        "jatuh cinta",
    ),
    "makanan": (
        "Momo, I swear this fried chicken is so crispy and delicious that even "
        "the moon is jealous and wants a bite right now, believe me!",
        "makanan / ayam goreng",
    ),
    "pantai": (
        "Momo, the beach sunset looks like melted cheese on warm bread, and I "
        "honestly want to eat the whole sky before it disappears tonight, yum!",
        "pantai / senja",
    ),
    "ekor": (
        "Momo, I just realized my tail has its own opinions, and honestly it "
        "disagrees with everything you say about my brilliant fried fish theory today!",
        "ekor / teori absurd",
    ),
    "respons": (
        "Momo, that is the silliest thing I have ever heard, and I love it so "
        "much I want to shout it from the rooftop now!",
        "merespons baris Momo",
    ),
}

# Kata pengisi untuk menambah jumlah kata bila baris Gemini kekurangan kata.
PENGISI = ["right now", "honestly", "seriously", "believe me", "I swear"]


def _pilih_template(judul, baris_sebelumnya):
    rendah = ((judul or "") + " " + (baris_sebelumnya or "")).lower()
    if (baris_sebelumnya or "").strip():
        return TEMPLATE_BARIS["respons"]
    if any(k in rendah for k in ("bulan", "moon", "ikan", "fish")):
        return TEMPLATE_BARIS["bulan_ikan"]
    if any(k in rendah for k in ("cinta", "love", "pacar", "jodoh", "nikah")):
        return TEMPLATE_BARIS["cinta"]
    if any(k in rendah for k in ("ayam", "chicken", "makan", "food", "goreng", "fried", "bakso", "risol")):
        return TEMPLATE_BARIS["makanan"]
    if any(k in rendah for k in ("pantai", "beach", "sunset", "senja", "laut")):
        return TEMPLATE_BARIS["pantai"]
    return TEMPLATE_BARIS["ekor"]


def _perbaiki_jumlah_kata(teks):
    """Paksa baris ke 17-25 kata bila memungkinkan; kembalikan (teks, catatan)."""
    kata = [w for w in (teks or "").split() if w.strip()]
    n = len(kata)
    if 17 <= n <= 25:
        return " ".join(kata), ""
    if n > 25:
        # Potong kalimat berlebih dari akhir, jaga tetap satu kalimat utuh.
        dipotong = " ".join(kata[:25])
        if not dipotong.endswith(("!", ".", "?")):
            dipotong += "!"
        return dipotong, (
            f"⚠️ Baris awal {n} kata (melebihi 25) — dipotong jadi 25 kata. "
            "Periksa lagi apakah artinya masih utuh sebelum dipakai."
        )
    # n < 17: tambah kata pengisi di akhir sampai 17 kata.
    tambahan = []
    i = 0
    while len(kata) + sum(len(p.split()) for p in tambahan) < 17:
        tambahan.append(PENGISI[i % len(PENGISI)])
        i += 1
    teks_baru = " ".join(kata + [p for p in tambahan])
    if not teks_baru.endswith(("!", ".", "?")):
        teks_baru += "!"
    return teks_baru, (
        f"⚠️ Baris awal hanya {n} kata (kurang dari 17) — ditambah kata pengisi "
        "sampai 17 kata. Periksa lagi apakah masih natural sebelum dipakai."
    )


def _baris_dari_gemini(judul, latar_nama, baris_sebelumnya):
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None, ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=kunci)
        model = genai.GenerativeModel("gemini-2.0-flash")
        konteks = (
            f"Baris Momo sebelumnya: \"{baris_sebelumnya}\"\n"
            "Balas baris itu sebagai Oyen." if (baris_sebelumnya or "").strip()
            else "Ini baris pembuka episode."
        )
        prompt = (
            "Tulis SATU baris dialog bahasa Inggris untuk Oyen, kucing oren "
            "Podcast Meong (polos, kaget, ceria, klaim absurd, mudah jatuh cinta, "
            "penasaran). Baris ini merespons Momo yang skeptis dan datar-sinis.\n"
            f"Judul konten: {judul or '(tanpa judul)'}. Latar: {latar_nama} "
            "(latar mengikuti judul).\n"
            f"{konteks}\n"
            "SYARAT WAJIB: tepat 17-25 kata, diawali 'Momo,', hook absurd di "
            "kalimat pertama, satu kalimat utuh, bahasa Inggris natural dan lucu. "
            "Kembalikan HANYA baris dialognya, tanpa penjelasan, tanpa tanda kutip."
        )
        r = model.generate_content(prompt)
        teks = (r.text or "").strip().strip('"').strip()
        return teks, "Gemini (gemini-2.0-flash)"
    except Exception as e:  # noqa: BLE001 — Gemini gagal: jatuh ke template
        return None, f"Gemini gagal ({e}) — pakai template."


def _tts_tersedia():
    return os.path.isfile(TTS_CLI) and os.access(TTS_CLI, os.X_OK)


def _cek_pitch(mp3_path):
    """Kembalikan (median_hz, pesan) atau (None, pesan)."""
    if not (os.path.isfile(PITCH_SCRIPT) and os.path.isfile(VENV_PYTHON)):
        return None, "alat ukur pitch tidak tersedia di mesin ini"
    if not shutil.which("ffmpeg"):
        return None, "ffmpeg tidak tersedia"
    try:
        wav = mp3_path + ".cek.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3_path, wav],
                       check=True, timeout=120)
        r = subprocess.run([VENV_PYTHON, PITCH_SCRIPT, wav],
                           capture_output=True, text=True, timeout=300)
        os.remove(wav)
        data = json.loads(r.stdout)
        return data.get("gated_median"), "ok"
    except Exception as e:  # noqa: BLE001
        return None, f"gagal ukur pitch: {e}"


def generate_audio_baris(teks):
    """Generate audio TTS baris Oyen + cek pitch. Kembalikan (path, laporan)."""
    if not _tts_tersedia():
        return None, (
            "⚠️ Audio/pitch TIDAK dibuat di mesin ini: TTS CLI "
            "(/opt/hatch/bin/tts) tidak tersedia (mis. saat jalan di Hugging "
            "Face Spaces). Pakai script + perintah TTS di bawah untuk generate "
            "di mesin Muse. Keputusan akhir tetap telinga Cipta — jangan pakai "
            "angka pitch yang tidak terukur."
        )
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = os.path.join(OUTPUT_DIR, f"oyen-baris-{stamp}.mp3")
    cmd = [TTS_CLI, "speak", "--voice", VOICE_ID, "--speed", str(SPEED),
           "--language", "en", "--output", out, "--text-stdin"]
    try:
        r = subprocess.run(cmd, input=teks, capture_output=True,
                           text=True, timeout=180)
    except Exception as e:  # noqa: BLE001
        return None, f"GAGAL generate audio: {e}"
    if r.returncode != 0 or not os.path.isfile(out):
        return None, f"GAGAL generate audio: {r.stderr.strip()[:300]}"
    med, pesan = _cek_pitch(out)
    if med is None:
        return out, f"Audio jadi ({out}), tapi pitch {pesan} — cek telinga Cipta."
    lulus = med > PITCH_MIN
    status = "LULUS" if lulus else "DI BAWAH TARGET (cek telinga Cipta)"
    return out, (
        f"Pitch median (energy-gated): {med:.1f} Hz — target >{PITCH_MIN:g} Hz "
        f"(kisaran {PITCH_MIN:g}-{PITCH_MAX:g}) → {status}. "
        f"Sampel permanen Oyen: {PITCH_SAMPEL:g} Hz."
    )


def buat_baris_dialog(judul, latar_key, latar_kustom, baris_sebelumnya):
    """Buat 1 baris dialog Oyen 17-25 kata + TTS + pitch + log."""
    judul = (judul or "").strip()
    latar_kustom = (latar_kustom or "").strip()
    if latar_key == "kustom":
        latar_nama = latar_kustom or "(latar kustom belum diisi)"
    else:
        latar_nama = dict((v, k) for k, v in LATAR_PILIHAN).get(latar_key, "Studio Podcast")
        if latar_key == "pantai":
            latar_nama = "Pantai"
        elif latar_key == "studio":
            latar_nama = "Studio Podcast"

    mode = "template (tanpa API key Gemini)"
    teks, asal = _baris_dari_gemini(judul, latar_nama, baris_sebelumnya)
    if teks:
        mode = asal
    else:
        teks, tema = _pilih_template(judul, baris_sebelumnya)
        mode = f"template (tema: {tema})" + (f" — {asal}" if asal else "")

    teks, catatan_kata = _perbaiki_jumlah_kata(teks)
    n_kata = hitung_kata(teks)
    peringatan = ""
    if not 17 <= n_kata <= 25:
        peringatan = (
            f"⚠️ PERINGATAN: baris ini {n_kata} kata — DI LUAR target 17-25 kata. "
            "Jangan dipakai sebelum diperbaiki."
        )
    elif catatan_kata:
        peringatan = catatan_kata

    script_tts = f"Oyen: {teks}"
    perintah_tts = (
        f"/opt/hatch/bin/tts speak --voice {VOICE_ID} --speed {SPEED} "
        f"--language en --output oyen-baris.mp3 --text-stdin <<'EOF'\n{teks}\nEOF"
    )
    voice_lock = (
        f"Voice lock dipakai: {VOICE_LOCK_EN}\n"
        f"Suara permanen: {VOICE_ID}, speed {SPEED}, target pitch "
        f">{PITCH_MIN:g} Hz (kisaran {PITCH_MIN:g}-{PITCH_MAX:g}), "
        f"sampel permanen {PITCH_SAMPEL:g} Hz."
    )

    audio_path, laporan_audio = generate_audio_baris(teks)
    pitch = None
    m = re.search(r"Pitch median[^:]*:\s*([\d.]+)\s*Hz", laporan_audio)
    if m:
        try:
            pitch = float(m.group(1))
        except ValueError:
            pitch = None
    verdict_audio = "LULUS" if (pitch is not None and pitch > PITCH_MIN) else (
        "DI BAWAH TARGET" if pitch is not None else "TANPA UKURAN PITCH")
    verdict = f"{n_kata} kata" + (f" | pitch {pitch:.1f} Hz {verdict_audio}" if pitch is not None else " | " + verdict_audio)
    catat_log("baris_dialog", teks, verdict, pitch)

    info = (
        f"Judul: {judul or '(tanpa judul)'} | Latar: {latar_nama} "
        f"(mengikuti judul) | Mode: {mode}\n"
        f"Jumlah kata: {n_kata} (target 17-25) — "
        f"{'✅ DALAM TARGET' if 17 <= n_kata <= 25 else '⛔ DI LUAR TARGET'}\n"
        f"{peringatan}\n"
        f"Audio: {laporan_audio}"
    )
    return teks, info, script_tts, perintah_tts, voice_lock, audio_path, log_ke_tabel()


# ---------------------------------------------------------------------------
# Kartu Tokoh (tampilan)
# ---------------------------------------------------------------------------
def kartu_tokoh_md():
    s = SUARA
    return (
        "# 🐱 OYEN — Kartu Tokoh Terkunci\n\n"
        "🔒 **SUARA DAN WAJAH PERMANEN — JANGAN DIUBAH** (Cipta, 18 Nov 2026 22:31). "
        "Tidak ada kontrol di aplikasi ini untuk mengubah apa pun di kartu ini. "
        "Perubahan hanya lewat edit `tokoh.json` oleh Muse atas perintah eksplisit Cipta.\n\n"
        "| | |\n|---|---|\n"
        f"| Nama | {TOKOH['nama']} |\n"
        f"| Deskripsi | {TOKOH['deskripsi']} |\n"
        f"| Peran | {TOKOH['peran']} |\n"
        f"| Lawan bicara utama | {TOKOH['lawan_bicara_utama']['nama']} — {TOKOH['lawan_bicara_utama']['sifat']} |\n"
        f"| Voice ID (permanen) | `{s['voice_id']}` |\n"
        f"| Speed (permanen) | {s['speed']} |\n"
        f"| Bahasa suara | {s['bahasa']} (dialog bisa bahasa Inggris) |\n"
        f"| Sifat suara | {s['sifat']} |\n"
        f"| Target pitch | >{PITCH_MIN:g} Hz (kisaran {PITCH_MIN:g}-{PITCH_MAX:g}) |\n"
        f"| Pitch sampel permanen | {PITCH_SAMPEL:g} Hz |\n"
        f"| Avatar tetap | `{TOKOH['avatar']}` |\n"
        f"| Sampel audio permanen | `{s['sampel_audio']}` |\n\n"
        f"**Sifat dialog:** {', '.join(TOKOH['sifat_dialog'])}.\n\n"
        f"**Gaya dialog:** {TOKOH['gaya_dialog']}\n\n"
        f"**Voice lock (EN):** {VOICE_LOCK_EN}\n\n"
        f"**Voice lock (ID):** {VOICE_LOCK_ID}\n\n"
        f"**Jumlah kata per baris dialog:** 17-25 kata (per klip 10 detik).\n\n"
        f"**Tugas agent ini:** {TOKOH['tugas']}"
    )


CONTOH_DRAF_BENAR = (
    "Oyen: Momo, the moon is made of fried fish! [angkat satu kaki depan]\n"
    "Suara: avocado_v2:MAI_01, speed 110. Pitch 278 Hz. Latar: pantai (judul: Oyen di Pantai)."
)
CONTOH_DRAF_MENYIMPANG = (
    "Oyen digambarkan datar dan sinis, suaranya rendah. "
    "Voice: avocado_v2:MAI_03, speed 100, pitch 150 Hz. "
    "Latar studio, padahal judulnya 'Oyen di Pantai'."
)

PANDUAN = """# Panduan Agent 11 — Oyen

## Apa tugas agent ini?
Menjaga **wajah + suara + sifat + gaya dialog Oyen SELALU SAMA** di setiap
konten. Agent ini HANYA mengurus Oyen — Momo diurus **Agent 12**. Agent
Avatar Podcast yang lama tetap sebagai workshop bersama (buat adegan
lengkap Oyen + Momo).

## Aturan permanen (Cipta)
- **Suara permanen — jangan diubah** (18 Nov 22:31): Oyen `avocado_v2:MAI_01`,
  speed 110, target pitch >200 Hz (kisaran 220-350), sampel permanen 278,0 Hz.
- **Wajah permanen**: kucing oren, mata besar, ekspresif, polos-kaget.
  Pakai `avatars/oyen-avatar.jpg` sebagai Start frame — jangan generate
  ulang wajah dari nol per adegan.
- **Durasi bebas**, tiap adegan berdiri sendiri (18 Nov 22:31).
- **Latar SELALU mengikuti judul** (aturan kualitas #4).
- **Sifat Oyen**: polos, kaget, ceria, klaim absurd, mudah jatuh cinta,
  penasaran. Datar/sinis itu sifat **Momo**, bukan Oyen.
- **Dialog**: hook absurd di kalimat pertama; 17-25 kata per baris
  (per klip 10 detik); baris Oyen merespons Momo.

## Cara pakai
1. **Kartu Tokoh Terkunci** — patokan. Bila ada yang ragu, bandingkan
   dengan kartu ini.
2. **Penjaga Konsistensi** — tempel draf (dialog / prompt / deskripsi
   adegan / hasil cek pitch) + judul konten, klik "Periksa". Verdict
   LULUS / PERLU PERBAIKAN / BELUM CUKUP DATA. Bila ada penyimpangan,
   perbaiki sesuai saran, lalu periksa ulang sampai LULUS.
3. **Buat Baris Dialog** — isi judul + latar + (opsional) baris Momo
   sebelumnya, klik "Buat Baris Dialog". Hasil: 1 baris Inggris 17-25
   kata + jumlah kata + script TTS + perintah tts CLI + audio + cek pitch
   (bila TTS CLI tersedia di mesin ini).
4. **Log Penjagaan** — semua pemeriksaan dan baris dialog tercatat di
   `data/log-penjagaan.json` (tanggal, jenis, ringkasan, verdict, pitch).

## Mode Gemini vs template
- Bila env var `GEMINI_API_KEY` ada: Gemini `gemini-2.0-flash` ikut
  menilai/menulis, TAPI aturan dasar di kode tetap diverifikasi dan
  menang bila bertentangan.
- Tanpa key: mode template (aturan kartu terkunci saja). Aplikasi tetap
  jalan penuh.

## Batasan (jujur)
- Audio TTS + cek pitch hanya dibuat bila `/opt/hatch/bin/tts` tersedia
  di mesin ini. Di Hugging Face Spaces, aplikasi mengeluarkan spesifikasi
  + script TTS — audio dibuat di mesin Muse.
- Cek pitch memakai metode energy-gated (`pitch_gated.py`); angka pitch
  adalah saringan pertama — keputusan akhir tetap **telinga Cipta**.
- Data di dalam Space gratis hilang bila Space di-rebuild — unduh file
  penting (tokoh.json, sampel audio, log) berkala.
- Semua output adalah DRAF untuk persetujuan Cipta. Tidak ada yang
  otomatis upload/kirim/bayar.
"""


def build_ui():
    with gr.Blocks(title="Agent 11 — Oyen (Penjaga Konsistensi)",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🐱 Agent 11 — Oyen (Penjaga Konsistensi Tokoh)\n"
            "Menjaga wajah + suara + sifat + gaya dialog Oyen SELALU SAMA.\n\n"
            f"🔒 **SUARA PERMANEN — jangan diubah:** `{VOICE_ID}` speed {SPEED} · "
            f"target pitch >{PITCH_MIN:g} Hz · sampel permanen {PITCH_SAMPEL:g} Hz. "
            "Dikunci di `tokoh.json`. Semua output adalah DRAF untuk persetujuan Cipta.")
        with gr.Tab("🔒 Kartu Tokoh Terkunci"):
            with gr.Row():
                gr.Image(value=os.path.join(BASE, TOKOH["avatar"]),
                         label="Avatar tetap OYEN (jangan diganti)",
                         interactive=False)
                gr.Audio(value=os.path.join(BASE, SUARA["sampel_audio"]),
                         label=f"Sampel suara permanen OYEN ({VOICE_ID}, speed {SPEED}) — pitch {PITCH_SAMPEL:g} Hz",
                         type="filepath")
            gr.Markdown(kartu_tokoh_md())
        with gr.Tab("🛡️ Penjaga Konsistensi"):
            gr.Markdown(
                "Tempel draf (dialog / prompt / deskripsi adegan / hasil cek pitch). "
                "Agent memeriksa terhadap kartu terkunci Oyen: suara, wajah, tempat, sifat.")
            judul_cek = gr.Textbox(label="Judul konten (opsional — dipakai untuk cek latar mengikuti judul)",
                                   placeholder="contoh: Oyen di Pantai")
            draf = gr.Textbox(label="Draf yang diperiksa", lines=6,
                              placeholder="contoh: Oyen: Momo, the moon is made of fried fish! Suara MAI_01 speed 110, pitch 278 Hz, latar pantai.")
            with gr.Row():
                btn_cek = gr.Button("🛡️ Periksa Konsistensi", variant="primary")
                btn_contoh_benar = gr.Button("Isi contoh draf benar")
                btn_contoh_salah = gr.Button("Isi contoh draf menyimpang")
            verdict = gr.Textbox(label="Verdict", interactive=False)
            laporan_cek = gr.Textbox(label="Laporan pemeriksaan", lines=14)
            log_tabel_cek = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                label="Log Penjagaan (terbaru di bawah)", value=log_ke_tabel(),
                interactive=False)
            btn_cek.click(periksa_konsistensi, inputs=[draf, judul_cek],
                          outputs=[verdict, laporan_cek, log_tabel_cek])
            btn_contoh_benar.click(lambda: CONTOH_DRAF_BENAR, outputs=draf)
            btn_contoh_salah.click(lambda: CONTOH_DRAF_MENYIMPANG, outputs=draf)
        with gr.Tab("✍️ Buat Baris Dialog"):
            gr.Markdown(
                "Buat 1 baris dialog bahasa Inggris untuk Oyen (17-25 kata). "
                "Suara terkunci otomatis dipakai — tidak bisa diubah.")
            judul_dialog = gr.Textbox(label="Judul konten",
                                      value="The Moon Is Made of Fried Fish")
            with gr.Row():
                latar_dialog = gr.Dropdown(choices=LATAR_PILIHAN, value="pantai",
                                           label="Latar (mengikuti judul)")
                latar_kustom = gr.Textbox(label="Latar kustom (bila pilih Kustom)",
                                          placeholder="contoh: night market with warm lanterns")
            baris_sebelum = gr.Textbox(
                label="Baris Momo sebelumnya (opsional — baris Oyen akan meresponsnya)",
                placeholder="contoh: Momo: Oyen, that's a rock. You've been staring at it too long.")
            btn_buat = gr.Button("✍️ Buat Baris Dialog", variant="primary")
            out_baris = gr.Textbox(label="Baris dialog Oyen (bahasa Inggris)", lines=3)
            out_info = gr.Textbox(label="Jumlah kata + mode + cek audio/pitch", lines=5)
            out_script = gr.Textbox(label="Script TTS", lines=3)
            out_perintah = gr.Textbox(label="Perintah tts CLI", lines=4)
            out_lock = gr.Textbox(label="Voice lock yang dipakai", lines=4)
            out_audio = gr.Audio(label="Audio TTS Oyen (bila TTS CLI tersedia)",
                                 type="filepath")
            log_tabel_dialog = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                label="Log Penjagaan (terbaru di bawah)", value=log_ke_tabel(),
                interactive=False)
            btn_buat.click(
                buat_baris_dialog,
                inputs=[judul_dialog, latar_dialog, latar_kustom, baris_sebelum],
                outputs=[out_baris, out_info, out_script, out_perintah, out_lock,
                         out_audio, log_tabel_dialog])
        with gr.Tab("📋 Log Penjagaan"):
            gr.Markdown(
                "Setiap pemeriksaan (Penjaga Konsistensi) dan setiap baris dialog "
                "yang dibuat dicatat ke `data/log-penjagaan.json`. "
                "Klik \"Muat Ulang Log\" untuk melihat entri terbaru.")
            log_tabel = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                label="Log Penjagaan", value=log_ke_tabel(), interactive=False)
            btn_muat = gr.Button("🔄 Muat Ulang Log")
            btn_muat.click(log_ke_tabel, outputs=log_tabel)
        with gr.Tab("📖 Panduan"):
            gr.Markdown(PANDUAN)
    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
