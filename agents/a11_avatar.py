# ======================================================================
# PUSAT KOMANDO — salinan dari agent-avatar-podcast (Agent Avatar Podcast).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Perubahan dari aslinya:
# - aset (voice_config.json, avatars/, latar/, samples/) dipindah ke
#   agents/avatar/ di pusat-komando/ (ditandai komentar 'PUSAT KOMANDO')
# - output audio/naskah ditulis ke folder output/avatar/ bersama
#   (ditandai komentar 'PUSAT KOMANDO')
# - SUARA PERMANEN tetap terkunci: Oyen MAI_01 speed 110, Momo MAI_03
#   speed 100 — tidak ada kontrol UI untuk mengubahnya.
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent Avatar Podcast — Podcast Meong
=====================================
Tahap 1 (18 Nov 2026): dua agent AI avatar kucing Oyen & Momo yang ACTING
podcast sesuai dialog — tinggal ganti latar tempat. Tiap adegan berdiri
sendiri (tidak perlu sambungan), durasi bebas.

TUGAS AVATAR (Cipta, 18 Nov 22:38): acting membuat konten untuk kepentingan
kita — episode podcast, promosi, pemasaran, jualan, edukasi, dan lain-lain.
Latar tempat SELALU disesuaikan dengan judul (aturan kualitas #4).

SUARA PERMANEN — JANGAN DIUBAH (Cipta, 18 Nov 22:31):
Oyen = avocado_v2:MAI_01 (tinggi, speed 110), Momo = avocado_v2:MAI_03
(rendah, speed 100). Suara dikunci di voice_config.json, TIDAK ada kontrol
UI untuk mengubahnya. Perubahan hanya lewat edit file atas perintah
eksplisit Cipta. Tokoh bisa BERAPA PUN: tiap tokoh punya gambar avatar
tetap + suara terkunci sendiri (wajah + suara dikunci permanen per tokoh;
suara antar-tokoh harus berbeda jelas).

Cara kerja:
- Masukkan dialog (satu baris = satu giliran bicara, format "Nama: teks").
- Pilih tujuan (episode / promo produk / jualan / edukasi) + latar tempat.
- Aplikasi mengeluarkan: prompt Flow terkunci per adegan, naskah lengkap,
  script TTS + audio per baris (bila /opt/hatch/bin/tts tersedia di mesin
  ini), dan cek pitch per baris (Oyen >200 Hz, Momo <200 Hz).
- Di Hugging Face Spaces (tanpa tts CLI), aplikasi mengeluarkan spesifikasi
  suara terkunci + script TTS yang bisa dijalankan Muse lewat CLI.

Model: Google Gemini free tier (gemini-4-hydrogen), API key HANYA dari env var
GEMINI_API_KEY. Tanpa key, aplikasi tetap jalan mode template. Tidak ada
layanan berbayar. Telemetri Gradio dimatikan.
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
                      "avatar")  # PUSAT KOMANDO: aset di agents/avatar/
CONFIG_PATH = os.path.join(BASE, "voice_config.json")
TTS_CLI = "/opt/hatch/bin/tts"
PITCH_SCRIPT = os.path.expanduser("~/workspace/audio-tools/pitch_gated.py")
VENV_PYTHON = os.path.expanduser("~/workspace/audio-tools/python-packages/bin/python")
OUTPUT_DIR = os.path.join(  # PUSAT KOMANDO: folder output/ bersama
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "output", "avatar")
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = json.load(f)

# Tokoh aktif saja yang bisa dipakai di dialog; slot kosong tidak bisa dipilih.
TOKOH_AKTIF = {k: v for k, v in CONFIG["tokoh"].items() if v.get("status") == "aktif"}
NAMA_KE_KEY = {v["nama"].lower(): k for k, v in TOKOH_AKTIF.items()}

LATAR = CONFIG["latar"]

# ---------------------------------------------------------------------------
# Tujuan adegan — memengaruhi gaya dialog + saran latar (latar tetap ikut judul)
# ---------------------------------------------------------------------------
TUJUAN = {
    "episode": {
        "label": "Episode podcast",
        "gaya_en": "Natural comedic podcast conversation, hook in the first line, "
                   "one joke or funny reaction per turn, warm and conversational.",
        "gaya_id": "Percakapan podcast komedi yang natural, hook di kalimat pertama, "
                   "satu lelucon atau reaksi lucu per giliran, hangat dan santai.",
        "saran_latar": "Studio Podcast — atau latar apa pun yang mengikuti judul episode.",
    },
    "promo": {
        "label": "Promo produk",
        "gaya_en": "Upbeat promotional acting: the speaker presents the product benefit "
                   "clearly and enthusiastically, shows the product with a paw gesture, "
                   "ends with a clear call to action, keeps the cat-podcast charm.",
        "gaya_id": "Acting promosi yang bersemangat: pembicara menyampaikan manfaat "
                   "produk dengan jelas dan antusias, menunjukkan produk dengan gestur kaki, "
                   "diakhiri ajakan yang jelas, tetap dengan gaya podcast kucing.",
        "saran_latar": "Studio Podcast — meja dengan produk yang dipromosikan terlihat jelas.",
    },
    "jualan": {
        "label": "Jualan",
        "gaya_en": "Persuasive sales acting: name the benefit and the price advantage, "
                   "answer one likely objection with humor, end with a clear call to buy "
                   "and where to buy it.",
        "gaya_id": "Acting jualan yang persuasif: sebut manfaat dan keunggulan harga, "
                   "jawab satu keberatan yang mungkin muncul dengan humor, akhiri dengan "
                   "ajakan membeli yang jelas dan di mana membelinya.",
        "saran_latar": "Studio Podcast — produk + label harga terlihat di meja bila ada.",
    },
    "edukasi": {
        "label": "Edukasi",
        "gaya_en": "Clear educational acting: explain one simple idea per turn, plain "
                   "language, friendly teacher tone, one concrete example, no jargon.",
        "gaya_id": "Acting edukasi yang jelas: jelaskan satu ide sederhana per giliran, "
                   "bahasa polos, nada guru yang ramah, satu contoh konkret, tanpa jargon.",
        "saran_latar": "Studio Podcast — suasana tenang; papan tulis/buku boleh terlihat.",
    },
}

# Rumus anti-kaku dari desain.md §6 (wajib di setiap prompt video).
RUMUS_ANTI_KAKU = (
    "handheld camera style, smooth gimbal movement, slight organic camera shake, "
    "cinematic tracking shot, subtle facial micro-expressions, natural breathing, "
    "slow blink, ear twitch, head tilt, whiskers moving gently, shot on 35mm lens, "
    "shallow depth of field, warm ambient lighting, natural motion blur, "
    "photorealistic, hyper-detailed"
)

AUDIO_LOCK_TEMPLATE = (
    "Audio & Voice Lock (tempel identik di setiap adegan, jangan diubah): "
    "{locks} Recorded close-mic with clean, studio-grade vocal clarity and "
    "consistent pitch. Background ambience remains steady, zero sudden volume "
    "shifts, no background music."
)

DISCLAIMER = (
    "\n\n---\n⚠️ SUARA PERMANEN — jangan diubah. Semua output adalah DRAF untuk "
    "persetujuan Cipta. Adegan berdiri sendiri, durasi bebas."
)


def _tokoh(key):
    return TOKOH_AKTIF[key]


def parse_dialog(teks):
    """Ubah teks dialog menjadi daftar baris.

    Format per baris:  Nama: kalimat dialog  [aksi opsional dalam kurung siku]
    Contoh: Oyen: Halo, Momo! [angkat satu kaki depan]
    Mengembalikan (baris, galat). baris = list dict {tokoh, nama, teks, aksi}.
    """
    baris, galat = [], []
    for i, mentah in enumerate((teks or "").splitlines(), 1):
        s = mentah.strip()
        if not s:
            continue
        m = re.match(r"^([^:]+):\s*(.+)$", s)
        if not m:
            galat.append(f"Baris {i}: tidak ada 'Nama: dialog' — lewati: {s[:60]}")
            continue
        nama = m.group(1).strip()
        isi = m.group(2).strip()
        key = NAMA_KE_KEY.get(nama.lower())
        if not key:
            aktif = ", ".join(v["nama"] for v in TOKOH_AKTIF.values())
            galat.append(
                f"Baris {i}: tokoh '{nama}' tidak dikenal / belum aktif. "
                f"Tokoh aktif: {aktif}."
            )
            continue
        aksi = ""
        ma = re.search(r"\[(.+?)\]\s*$", isi)
        if ma:
            aksi = ma.group(1).strip()
            isi = isi[: ma.start()].strip()
        if not isi:
            galat.append(f"Baris {i}: dialog kosong setelah nama tokoh.")
            continue
        baris.append({"tokoh": key, "nama": _tokoh(key)["nama"],
                      "teks": isi, "aksi": aksi})
    return baris, galat


def _deskripsi_tokoh_en(key):
    t = _tokoh(key)
    return (
        f"{t['nama']}, {t['deskripsi']}, photorealistic AI cat, facing the camera, "
        f"sitting at a podcast table with a black podcast microphone on a boom arm "
        f"in front, same face, same fur colour, same body size in every scene."
    )


def _voice_lock(teks_bahasa):
    locks = []
    for key, t in TOKOH_AKTIF.items():
        locks.append(t["voice_lock_en"] if teks_bahasa == "en" else t["voice_lock_id"])
    return AUDIO_LOCK_TEMPLATE.format(locks=" ".join(locks))


def buat_prompt_flow(baris, judul, tujuan, latar_key, latar_kustom, durasi, bahasa):
    """Satu prompt Flow terkunci per baris dialog (satu adegan berdiri sendiri)."""
    if not baris:
        return "Isi dialog dulu (format 'Nama: kalimat')."
    latar = LATAR.get(latar_key)
    latar_en = (latar_kustom.strip() if latar_kustom and latar_kustom.strip()
                else (latar["deskripsi_en"] if latar else "podcast studio"))
    nama_latar = latar["nama"] if latar else "Kustom"
    tj = TUJUAN[tujuan]
    gaya = tj["gaya_en"] if bahasa == "en" else tj["gaya_id"]
    out = []
    out.append(f"# Prompt Flow terkunci — {judul or '(tanpa judul)'}")
    out.append(f"Tujuan: {tj['label']} | Latar: {nama_latar} (mengikuti judul) | "
               f"Durasi: {durasi or 'bebas'} | Bahasa dialog: "
               f"{'Inggris' if bahasa == 'en' else 'Indonesia'}")
    out.append("Aturan avatar: tiap adegan berdiri sendiri, tidak perlu sambungan. "
               "Satu pembicara per adegan; yang diam mulutnya tertutup, hanya bereaksi "
               "(kedip, angguk). NO human, only cats. 180-Degree Rule: jangan pindah "
               "sisi kamera antar adegan.")
    out.append("")
    for i, b in enumerate(baris, 1):
        t = _tokoh(b["tokoh"])
        aksi = f" Action: {b['aksi']}." if b["aksi"] else ""
        out.append(f"## Adegan {i} — {b['nama']} (SUARA PERMANEN: "
                   f"{t['suara']['voice_id']}, speed {t['suara']['speed']})")
        out.append(
            f"{_deskripsi_tokoh_en(b['tokoh'])} Setting: {latar_en}. "
            f"{RUMUS_ANTI_KAKU}. {gaya} "
            f"{b['nama']} speaks the full sentence without stopping, mouth moving "
            f"until the very last word:{aksi} \"{b['teks']}\""
        )
        out.append("")
    out.append(_voice_lock(bahasa))
    out.append(
        "Master frame: pakai gambar avatar tetap di folder avatars/ "
        "(oyen-avatar.jpg / momo-avatar.jpg) sebagai Start frame di Flow — "
        "jangan generate ulang tokoh dari nol per adegan."
    )
    return "\n".join(out)


def buat_naskah(baris, judul, tujuan, latar_key, durasi, bahasa):
    if not baris:
        return "Isi dialog dulu (format 'Nama: kalimat')."
    nama_latar = LATAR.get(latar_key, {}).get("nama", "Kustom")
    tj = TUJUAN[tujuan]
    baris_md = ["# Naskah Avatar Podcast — " + (judul or "(tanpa judul)"),
                f"Tujuan: {tj['label']} | Latar: {nama_latar} (mengikuti judul) | "
                f"Durasi: {durasi or 'bebas'} | Bahasa: "
                f"{'Inggris' if bahasa == 'en' else 'Indonesia'}",
                "",
                "| # | Tokoh | Dialog | Aksi |",
                "|---|-------|--------|------|"]
    for i, b in enumerate(baris, 1):
        baris_md.append(f"| {i} | {b['nama']} | {b['teks']} | {b['aksi'] or '-'} |")
    baris_md.append("")
    baris_md.append("**Suara permanen (jangan diubah):**")
    for key, t in TOKOH_AKTIF.items():
        baris_md.append(
            f"- {t['nama']}: {t['suara']['voice_id']}, speed {t['suara']['speed']}, "
            f"target pitch {t['suara']['pitch_target_hz']} Hz "
            f"(sampel permanen: {t['suara']['pitch_sampel_permanen_hz']} Hz).")
    baris_md.append("")
    baris_md.append("Aturan: satu pembicara per adegan; yang diam mulut tertutup; "
                    "adegan berdiri sendiri, tidak perlu sambungan.")
    return "\n".join(baris_md)


def buat_script_tts(baris, bahasa):
    """Script untuk /opt/hatch/bin/tts synthesize-script + pemetaan speaker."""
    if not baris:
        return "", ""
    nama_file = {}
    for key, t in TOKOH_AKTIF.items():
        nama_file[t["nama"]] = t["suara"]["voice_id"]
    lines = []
    for b in baris:
        lines.append(f"{b['nama']}: {b['teks']}")
    script = "\n".join(lines)
    perintah = ["# Jalankan di mesin Muse (lokal), contoh:",
                "  /opt/hatch/bin/tts synthesize-script \\"]
    for nama, vid in nama_file.items():
        perintah.append(f"    --speaker {nama}={vid} \\")
    perintah.append("    --script naskah-avatar.txt --output audio-avatar.mp3")
    perintah.append(f"# Bahasa: {'en' if bahasa == 'en' else 'id'}; "
                    "speed per tokoh sudah dikunci di voice_config.json "
                    "(Oyen 110, Momo 100) — pakai --speed per baris bila generate "
                    "satu-satu dengan 'speak'.")
    return script, "\n".join(perintah)


# ---------------------------------------------------------------------------
# Audio lokal (hanya bila tts CLI tersedia di mesin ini) + cek pitch
# ---------------------------------------------------------------------------
def _tts_tersedia():
    return os.path.isfile(TTS_CLI) and os.access(TTS_CLI, os.X_OK)


def _cek_pitch(mp3_path):
    """Kembalikan (median_hz, mean_hz, pesan) atau (None, None, pesan)."""
    if not (os.path.isfile(PITCH_SCRIPT) and os.path.isfile(VENV_PYTHON)):
        return None, None, "alat ukur pitch tidak tersedia di mesin ini"
    if not shutil.which("ffmpeg"):
        return None, None, "ffmpeg tidak tersedia"
    try:
        wav = mp3_path + ".cek.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3_path, wav],
                       check=True, timeout=120)
        r = subprocess.run([VENV_PYTHON, PITCH_SCRIPT, wav],
                           capture_output=True, text=True, timeout=300)
        os.remove(wav)
        data = json.loads(r.stdout)
        return data.get("gated_median"), data.get("gated_mean"), "ok"
    except Exception as e:  # noqa: BLE001 — tampilkan apa adanya
        return None, None, f"gagal ukur pitch: {e}"


def _target_pitch(key):
    t = _tokoh(key)
    target = t["suara"]["pitch_target_hz"]
    if target.startswith(">"):
        return ("min", float(target[1:].split()[0]))
    if target.startswith("<"):
        return ("max", float(target[1:].split()[0]))
    return (None, None)


def generate_audio_lokal(baris, bahasa):
    """Generate audio per baris dengan suara terkunci (hanya bila tts CLI ada).

    Mengembalikan (path_audio_gabungan, daftar_file, laporan_cek).
    """
    if not baris:
        return None, [], "Isi dialog dulu."
    if not _tts_tersedia():
        return None, [], (
            "⚠️ TTS CLI (/opt/hatch/bin/tts) TIDAK tersedia di mesin ini "
            "(mis. saat jalan di Hugging Face Spaces). Audio TIDAK dibuat di sini. "
            "Pakai spesifikasi suara terkunci + script TTS di bawah: jalankan "
            "script itu di mesin Muse, atau minta Muse generate audionya. "
            "Suara tetap terkunci: " + ", ".join(
                f"{t['nama']} {t['suara']['voice_id']} speed {t['suara']['speed']}"
                for t in TOKOH_AKTIF.values()) + "."
        )
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = os.path.join(OUTPUT_DIR, "audio", stamp)
    os.makedirs(folder, exist_ok=True)
    files, laporan = [], []
    for i, b in enumerate(baris, 1):
        t = _tokoh(b["tokoh"])
        out = os.path.join(folder, f"baris-{i:02d}-{b['tokoh']}.mp3")
        cmd = [TTS_CLI, "speak", "--voice", t["suara"]["voice_id"],
               "--speed", str(t["suara"]["speed"]),
               "--language", bahasa, "--output", out, "--text-stdin"]
        try:
            r = subprocess.run(cmd, input=b["teks"], capture_output=True,
                               text=True, timeout=180)
            if r.returncode != 0 or not os.path.isfile(out):
                laporan.append(f"Baris {i} ({b['nama']}): GAGAL generate audio "
                               f"— {r.stderr.strip()[:200]}")
                continue
        except Exception as e:  # noqa: BLE001
            laporan.append(f"Baris {i} ({b['nama']}): GAGAL — {e}")
            continue
        files.append(out)
        med, _mean, pesan = _cek_pitch(out)
        if med is None:
            laporan.append(f"Baris {i} ({b['nama']}): audio jadi, pitch {pesan}.")
            continue
        arah, ambang = _target_pitch(b["tokoh"])
        if arah == "min":
            lulus = med > ambang
            ket = f"target >{ambang:g} Hz"
        elif arah == "max":
            lulus = med < ambang
            ket = f"target <{ambang:g} Hz"
        else:
            lulus, ket = True, "tanpa target"
        laporan.append(f"Baris {i} ({b['nama']}): pitch median {med:.1f} Hz "
                       f"({ket}) — {'LULUS' if lulus else 'DI BAWAH/DI ATAS TARGET, cek telinga'}")
    gabungan = None
    if files and shutil.which("ffmpeg"):
        try:
            daftar = os.path.join(folder, "concat.txt")
            sunyi = os.path.join(folder, "sunyi-04.mp3")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                            "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.4",
                            "-q:a", "9", "-acodec", "libmp3lame", sunyi],
                           check=True, timeout=60)
            with open(daftar, "w", encoding="utf-8") as f:
                for p in files:
                    f.write(f"file '{p}'\nfile '{sunyi}'\n")
            gabungan = os.path.join(folder, "audio-gabungan.mp3")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                            "-safe", "0", "-i", daftar, "-c", "copy", gabungan],
                           check=True, timeout=120)
        except Exception as e:  # noqa: BLE001
            laporan.append(f"Audio gabungan gagal dirakit: {e}")
            gabungan = None
    return gabungan, files, "\n".join(laporan) if laporan else "Tidak ada baris."


def proses_adegan(dialog_teks, judul, tujuan, latar_key, latar_kustom, durasi, bahasa):
    baris, galat = parse_dialog(dialog_teks)
    pesan_galat = ("\n".join("⚠️ " + g for g in galat) + "\n\n") if galat else ""
    if not baris:
        return (pesan_galat + "Tidak ada baris dialog yang valid.",
                "", None, [], "Tidak ada baris dialog yang valid.",
                "", "")
    prompt = buat_prompt_flow(baris, judul, tujuan, latar_key, latar_kustom,
                              durasi, bahasa)
    naskah = buat_naskah(baris, judul, tujuan, latar_key, durasi, bahasa)
    script, perintah = buat_script_tts(baris, bahasa)
    gabungan, files, laporan = generate_audio_lokal(baris, bahasa)
    script_path = os.path.join(OUTPUT_DIR, "naskah-avatar.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    unduhan = [script_path] + files
    return (pesan_galat + prompt, pesan_galat + naskah, gabungan, unduhan,
            pesan_galat + laporan, perintah)


# ---------------------------------------------------------------------------
# Tokoh & suara permanen
# ---------------------------------------------------------------------------
def tabel_tokoh():
    baris = ["# Tokoh & Suara Permanen — JANGAN DIUBAH",
             "",
             "Suara tiap tokoh dikunci PERMANEN (Cipta, 18 Nov 2026 22:31). "
             "Aplikasi ini TIDAK menyediakan kontrol untuk mengubah suara. "
             "Perubahan hanya lewat edit `voice_config.json` oleh Muse atas "
             "perintah eksplisit Cipta.",
             "",
             "| Tokoh | Status | Gambar avatar | Suara terkunci | Speed | Target pitch | Sampel permanen |",
             "|-------|--------|---------------|----------------|-------|--------------|-----------------|"]
    for key, t in CONFIG["tokoh"].items():
        s = t.get("suara") or {}
        baris.append(
            f"| {t['nama']} | {t['status']} | {t.get('avatar') or '-'} | "
            f"{s.get('voice_id', '-')} | {s.get('speed', '-')} | "
            f"{s.get('pitch_target_hz', '-')} Hz | "
            f"{s.get('pitch_sampel_permanen_hz', '-') or '-'} Hz |")
    baris.append("")
    baris.append("**Slot kosong** (Bang Mpus, Bang Abu, Si Abu): disiapkan tempatnya. "
                 "Untuk mengaktifkan, lihat panduan 'Tambah Tokoh Baru' di bawah — "
                 "gambar avatar tetap + voice_id yang JELAS berbeda + sampel audio "
                 "+ cek pitch.")
    return "\n".join(baris)


def draft_tokoh_baru(nama, deskripsi, voice_id, speed, sifat):
    nama = (nama or "").strip()
    voice_id = (voice_id or "").strip()
    if not nama:
        return "Isi nama tokoh dulu."
    if not voice_id:
        return ("Isi voice_id yang akan dipakai (contoh: avocado_v2:MAI_01). "
                "Pilih suara yang JELAS berbeda dari tokoh yang sudah aktif.")
    dipakai = {t["suara"]["voice_id"]: t["nama"]
               for t in TOKOH_AKTIF.values() if t.get("suara")}
    if voice_id in dipakai:
        return (f"⛔ voice_id {voice_id} SUDAH dipakai {dipakai[voice_id]}. "
                "Suara antar-tokoh harus berbeda jelas — pilih voice_id lain.")
    try:
        speed_i = int(speed)
        if not 1 <= speed_i <= 200:
            raise ValueError
    except ValueError:
        return "Speed harus angka 1–200."
    key = re.sub(r"[^a-z0-9]+", "-", nama.lower()).strip("-")
    draft = {
        key: {
            "nama": nama,
            "status": "aktif (setelah sampel + cek pitch lulus)",
            "peran": (deskripsi or "").strip(),
            "deskripsi": (deskripsi or "").strip(),
            "avatar": f"avatars/{key}-avatar.jpg",
            "suara": {
                "voice_id": voice_id,
                "speed": speed_i,
                "bahasa": "id",
                "sifat": (sifat or "").strip(),
                "pitch_target_hz": "ditentukan setelah cek pitch sampel",
                "sampel_audio": f"samples/sampel-suara-{key}-permanen.mp3",
                "pitch_sampel_permanen_hz": None,
            },
        }
    }
    return (
        "DRAF entri tokoh baru (BELUM aktif — ini hanya draf, bukan penguncian):\n\n"
        "```json\n" + json.dumps(draft, ensure_ascii=False, indent=2) + "\n```\n\n"
        "Checklist sebelum tokoh ini dikunci permanen:\n"
        "1. Buat gambar avatar tetap → simpan sebagai "
        f"`avatars/{key}-avatar.jpg` (wajah menghadap kamera, mic podcast, "
        "fotorealistik, sesuai desain.md).\n"
        "2. Generate sampel suara permanen dengan voice_id + speed di atas "
        "(kalimat yang sama seperti sampel Oyen/Momo agar pitch bisa "
        "dibandingkan).\n"
        "3. Ukur pitch sampel (pitch_gated.py) — pastikan JELAS berbeda dari "
        "Oyen (278 Hz) dan Momo (153 Hz).\n"
        "4. Setelah 1–3 lulus, Muse menambahkan entri ini ke voice_config.json "
        "dan mengubah status menjadi 'aktif'.\n"
        "5. Simpan sampel audio sebagai patokan permanen di folder samples/."
    )


# ---------------------------------------------------------------------------
# Poles dialog (Gemini bila ada key, template bila tidak)
# ---------------------------------------------------------------------------
def poles_dialog(teks):
    if not (teks or "").strip():
        return "Isi dialog dulu."
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if kunci:
        try:
            import google.generativeai as genai
            genai.configure(api_key=kunci)
            model = genai.GenerativeModel("gemini-4-hydrogen")
            r = model.generate_content(
                "Kamu membantu menulis dialog podcast kucing Podcast Meong "
                "(Oyen = oren, ceria, tinggi; Momo = abu-abu, tenang, datar). "
                "Perbaiki dialog berikut agar natural, lucu, dan enak diucapkan, "
                "tanpa mengubah arti dan tanpa mengganti nama pembicara. "
                "Kembalikan dialog hasil perbaikan saja, format 'Nama: kalimat' "
                "per baris, satu giliran bicara per baris.\n\n" + teks)
            return (r.text or "").strip() or "Gemini mengembalikan teks kosong."
        except Exception as e:  # noqa: BLE001
            return f"Gemini gagal ({e}) — pakai checklist template di bawah.\n\n" + _tips_template()
    return _tips_template()


def _tips_template():
    return (
        "Mode template (tanpa API key Gemini) — checklist poles dialog:\n"
        "1. Hook di kalimat pertama — kejutan, pertanyaan, atau klaim absurd.\n"
        "2. Satu giliran bicara = satu kalimat utuh, jangan dua pembicara sekaligus.\n"
        "3. Tiap jawaban merespons kalimat sebelumnya (rantai dialog, bukan kalimat lepas).\n"
        "4. Tambah aksi tubuh dalam [kurung siku], mis. [angkat satu kaki depan] — "
        "aksi harus nyambung dengan isi kalimat.\n"
        "5. Satu lelucon/reaksi lucu per giliran; bahasa lisan natural (sih, kan, deh).\n"
        "6. Akhiri dengan punchline atau ajakan (follow / beli / coba)."
    )


def saran_latar(tujuan):
    return f"**Saran latar untuk tujuan '{TUJUAN[tujuan]['label']}':** {TUJUAN[tujuan]['saran_latar']} Latar tetap mengikuti judul episode/konten (aturan kualitas #4)."


CONTOH_DIALOG = """Oyen: Momo, the moon is made of fried fish. I can smell it all the way from here, crispy and delicious.
Momo: Oyen, that's a rock. You've been staring at it too long. Your brain is more fried than any fish.
Oyen: Then explain the smell. And why is it crispy? Admit it, Momo. The moon is a giant fish."""

PANDUAN = """# Panduan Agent Avatar Podcast

## Apa tugas avatar? (Cipta, 18 Nov 22:38)
Avatar Oyen & Momo bertugas **ACTING membuat konten untuk kepentingan kita** —
bukan hanya episode podcast. Mereka juga membantu **pemasaran, promosi, jualan,
edukasi, dan lain-lain**. Di tab "Buat Adegan", pilih **tujuan** per adegan:
episode podcast / promo produk / jualan / edukasi — tujuan memengaruhi gaya
dialog dan saran latar. **Latar tempat SELALU disesuaikan dengan judul**
(aturan kualitas #4): latar mengikuti judul konten, bukan sebaliknya.

## Aturan avatar (Cipta)
- **Durasi BEBAS** — berapa pun boleh; adegan **TIDAK PERLU sambungan**,
  tiap adegan berdiri sendiri.
- **Suara KONSISTEN dan STABIL** — kriteria keberhasilan. Bila suara berubah
  antar-adegan, avatar gagal.
- **SUARA PERMANEN — jangan diubah** (18 Nov 22:31): Oyen MAI_01 speed 110,
  Momo MAI_03 speed 100. Dikunci di `voice_config.json`; tidak ada kontrol UI
  untuk mengubahnya.
- **Tokoh bisa BERAPA PUN**: tiap tokoh punya gambar avatar tetap + suara
  terkunci sendiri. Oyen & Momo tokoh pertama; Bang Mpus, Bang Abu, Si Abu
  disiapkan slotnya.

## Cara pakai
1. Tulis dialog di tab "Buat Adegan", satu baris per giliran:
   `Oyen: kalimat...` atau `Momo: kalimat... [aksi tubuh]`.
2. Pilih tujuan, latar, bahasa, durasi (bebas, mis. "26 detik" / "bebas").
3. Klik "Buat Adegan" → dapat prompt Flow terkunci per adegan + naskah +
   script TTS. Bila aplikasi jalan di mesin Muse (lokal), audio per baris
   ikut dibuat + dicek pitch-nya (Oyen >200 Hz, Momo <200 Hz).
4. Bawa prompt Flow + gambar avatar tetap (`avatars/`) ke Flow sebagai
   Start frame. Jangan generate ulang tokoh dari nol per adegan.

## Menambah tokoh baru
Isi form di tab "Tokoh & Suara Permanen" → aplikasi memberi draf JSON +
checklist. Aktivasi (oleh Muse): gambar avatar tetap → sampel suara permanen
(kalimat yang sama seperti sampel Oyen/Momo) → cek pitch (harus JELAS berbeda
dari 278 Hz Oyen dan 153 Hz Momo) → entri masuk `voice_config.json`.

## Batasan (jujur)
- Audio TTS hanya dibuat bila `/opt/hatch/bin/tts` tersedia di mesin ini.
  Di Hugging Face Spaces, aplikasi mengeluarkan spesifikasi + script TTS —
  audio dibuat di mesin Muse.
- Mulut di halaman demo bergerak mengikuti volume audio (bukan lip-sync
  sesungguhnya). Avatar real-time (Live2D/VRM) adalah tahap 2, bila tahap 1
  terbukti.
- Data di dalam Space gratis hilang bila Space di-rebuild — unduh file
  penting (voice_config.json, sampel audio) berkala.
- Semua output adalah DRAF untuk persetujuan Cipta. Tidak ada yang otomatis
  upload/kirim/bayar.
"""


def build_ui():
    with gr.Blocks(title="Agent Avatar Podcast — Oyen & Momo",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🐱 Agent Avatar Podcast — Oyen & Momo\n"
            "Avatar acting podcast sesuai dialog — tinggal ganti latar tempat. "
            "Durasi bebas, tiap adegan berdiri sendiri.\n\n"
            "🔒 **SUARA PERMANEN — jangan diubah:** Oyen `avocado_v2:MAI_01` speed 110 · "
            "Momo `avocado_v2:MAI_03` speed 100. Dikunci di `voice_config.json`.")
        with gr.Tab("🎬 Buat Adegan"):
            with gr.Row():
                judul = gr.Textbox(label="Judul adegan / konten",
                                   value="The Moon Is Made of Fried Fish")
                tujuan = gr.Radio(choices=[(v["label"], k) for k, v in TUJUAN.items()],
                                  value="episode", label="Tujuan adegan")
            with gr.Row():
                latar = gr.Dropdown(choices=[(v["nama"], k) for k, v in LATAR.items()],
                                    value="pantai", label="Latar tempat (mengikuti judul)")
                bahasa = gr.Radio(choices=[("Indonesia", "id"), ("Inggris", "en")],
                                  value="en", label="Bahasa dialog")
                durasi = gr.Textbox(label="Durasi (bebas)", value="26 detik")
            latar_kustom = gr.Textbox(
                label="Latar kustom (opsional — bila tidak ada di pilihan, tulis deskripsi Inggrisnya)",
                placeholder="contoh: night market with warm lanterns, wooden stalls...")
            saran = gr.Markdown(saran_latar("episode"))
            tujuan.change(saran_latar, inputs=tujuan, outputs=saran)
            dialog = gr.Textbox(label="Dialog — satu baris per giliran (format: Nama: kalimat [aksi])",
                                lines=6, value=CONTOH_DIALOG)
            with gr.Row():
                btn_buat = gr.Button("🎬 Buat Adegan", variant="primary")
                btn_poles = gr.Button("✨ Poles Dialog (Gemini bila ada key)")
            poles_out = gr.Textbox(label="Hasil poles dialog / checklist", lines=6)
            btn_poles.click(poles_dialog, inputs=dialog, outputs=poles_out)
            out_prompt = gr.Textbox(label="Prompt Flow terkunci per adegan", lines=14)
            out_naskah = gr.Textbox(label="Naskah lengkap", lines=10)
            out_audio = gr.Audio(label="Audio gabungan (bila TTS CLI tersedia)",
                                 type="filepath")
            out_files = gr.File(label="Unduhan: script TTS + audio per baris",
                                file_count="multiple")
            out_cek = gr.Textbox(label="Cek suara (pitch per baris)", lines=6)
            out_perintah = gr.Textbox(label="Perintah TTS (bila audio tidak dibuat di sini)",
                                      lines=5)
            btn_buat.click(
                proses_adegan,
                inputs=[dialog, judul, tujuan, latar, latar_kustom, durasi, bahasa],
                outputs=[out_prompt, out_naskah, out_audio, out_files, out_cek,
                         out_perintah])
        with gr.Tab("🔒 Tokoh & Suara Permanen"):
            gr.Markdown(tabel_tokoh())
            with gr.Row():
                gr.Audio(value=os.path.join(BASE, "samples",
                                            "sampel-suara-oyen-permanen.mp3"),
                         label="Sampel permanen OYEN (MAI_01, speed 110) — pitch median 278,0 Hz",
                         type="filepath")
                gr.Audio(value=os.path.join(BASE, "samples",
                                            "sampel-suara-momo-permanen.mp3"),
                         label="Sampel permanen MOMO (MAI_03, speed 100) — pitch median 153,3 Hz",
                         type="filepath")
            gr.Markdown("### ➕ Tambah Tokoh Baru (draf — aktivasi tetap lewat file config)")
            with gr.Row():
                nb_nama = gr.Textbox(label="Nama tokoh baru", placeholder="Bang Mpus")
                nb_voice = gr.Textbox(label="voice_id yang diusulkan",
                                      placeholder="avocado_v2:MAI_02")
                nb_speed = gr.Textbox(label="Speed (1–200)", value="100")
            nb_desk = gr.Textbox(label="Deskripsi tokoh (wajah, peran, sifat)",
                                 placeholder="Kucing abu-abu belang, host, santai tapi sinis")
            nb_sifat = gr.Textbox(label="Sifat suara", placeholder="sedang, hangat, pelan")
            btn_tokoh = gr.Button("📝 Buat Draf Tokoh Baru")
            out_tokoh = gr.Textbox(label="Draf + checklist aktivasi", lines=14)
            btn_tokoh.click(draft_tokoh_baru,
                            inputs=[nb_nama, nb_desk, nb_voice, nb_speed, nb_sifat],
                            outputs=out_tokoh)
        with gr.Tab("📖 Panduan"):
            gr.Markdown(PANDUAN)
    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
