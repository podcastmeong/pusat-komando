# ======================================================================
# PUSAT KOMANDO — salinan dari agent-12-momo (Agent 12 Momo).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Perubahan dari aslinya:
# - aset (tokoh.json, avatars/, samples/, latar/) dipindah ke
#   agents/momo/ di pusat-komando/ (ditandai komentar 'PUSAT KOMANDO')
# - output audio ditulis ke folder output/<tokoh>/ bersama
#   (ditandai komentar 'PUSAT KOMANDO')
# - log penjagaan ditulis ke data/log-penjagaan-<tokoh>.json bersama
#   (ditandai komentar 'PUSAT KOMANDO')
# - SUARA PERMANEN tetap terkunci: Momo MAI_03 speed 100 — tidak ada kontrol UI untuk mengubahnya.
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent 12 — Momo (Penjaga Konsistensi Tokoh) — Podcast Meong
============================================================
Aplikasi Gradio mandiri. Satu tokoh saja: Momo.

TUGAS (Cipta, 18 Nov 2026 23:19): menjaga konsistensi tokoh Momo — wajah +
suara terkunci — memeriksa setiap konten sebelum produksi.

SUARA + WAJAH PERMANEN — JANGAN DIUBAH (Cipta, 18 Nov 2026 22:31):
Momo = avocado_v2:MAI_03 (rendah, speed 100), target pitch <200 Hz,
pitch sampel permanen 153,3 Hz. Dikunci di tokoh.json; TIDAK ada kontrol
UI untuk mengubahnya. Perubahan hanya lewat edit file atas perintah
eksplisit Cipta.

Fitur:
1) Kartu Tokoh Terkunci — tampilkan avatar, suara, sifat, voice lock,
   pemutar audio sampel permanen. Tanpa kontrol ubah.
2) Penjaga Konsistensi — periksa draf (dialog / prompt / deskripsi adegan /
   hasil cek pitch) terhadap kartu terkunci. Verdict LULUS / PERLU
   PERBAIKAN / BELUM CUKUP DATA + daftar penyimpangan + saran perbaikan.
   Mode Gemini (bila env var GEMINI_API_KEY ada, model gemini-4-hydrogen),
   tapi aturan dasar tetap diverifikasi di kode. Tanpa key: mode template.
3) Buat Baris Dialog — 1 baris dialog bahasa Inggris 17–25 kata (dihitung
   dan ditampilkan jumlah katanya), voice lock, script TTS, perintah tts
   CLI. Bila /opt/hatch/bin/tts tersedia, audio ikut dibuat + pitch diukur
   (energy-gated, target <200 Hz).
4) Log Penjagaan — setiap pemeriksaan dan baris dialog dicatat ke
   data/log-penjagaan.json dan ditampilkan sebagai tabel.

Semua output adalah DRAF untuk persetujuan Cipta. Tidak ada layanan
berbayar. Telemetri Gradio dimatikan. API key HANYA dari env var
GEMINI_API_KEY.
"""
import json
import os
import re
import shutil
import subprocess

# Quirk mesin Muse (18 Nov 2026): NO_PROXY bawaan berisi entri IPv6 dalam
# kurung ([::1], [fd8b:...]) yang membuat httpx (dipakai Gradio) gagal impor
# dengan "Invalid port". Bersihkan entri berkutung sebelum impor gradio.
# Ini hanya memengaruhi proses aplikasi ini, bukan sistem.
for _var in ("NO_PROXY", "no_proxy"):
    _val = os.environ.get(_var, "")
    if "[" in _val:
        _bersih = ",".join(p for p in _val.split(",") if "[" not in p.strip())
        os.environ[_var] = _bersih or "localhost,127.0.0.1"

import gradio as gr  # noqa: E402

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "momo")  # PUSAT KOMANDO: aset di agents/momo/
TOKOH_PATH = os.path.join(BASE, "tokoh.json")
LOG_PATH = os.path.join(  # PUSAT KOMANDO: log ke data/ bersama
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "log-penjagaan-momo.json")
TTS_CLI = "/opt/hatch/bin/tts"
PITCH_SCRIPT = os.path.expanduser("~/workspace/audio-tools/pitch_gated.py")
VENV_PYTHON = os.path.expanduser("~/workspace/audio-tools/python-packages/bin/python")
OUTPUT_DIR = os.path.join(  # PUSAT KOMANDO: folder output/ bersama
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "output", "momo")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

with open(TOKOH_PATH, encoding="utf-8") as f:
    TOKOH = json.load(f)

SUARA = TOKOH["suara"]
VOICE_ID = SUARA["voice_id"]
SPEED = SUARA["speed"]
PITCH_TARGET_MAX = 200.0  # target pitch Momo: <200 Hz
PITCH_SAMPEL = SUARA["pitch_sampel_permanen_hz"]

DISCLAIMER = (
    "\n\n---\n🔒 SUARA + WAJAH PERMANEN — jangan diubah. "
    "Semua output adalah DRAF untuk persetujuan Cipta."
)

# ---------------------------------------------------------------------------
# Utilitas umum
# ---------------------------------------------------------------------------
def hitung_kata(teks):
    """Jumlah kata: token dipisah spasi, tanda baca di ujung kata diabaikan."""
    return len([w for w in re.split(r"\s+", (teks or "").strip()) if w])


def _muat_log():
    try:
        with open(LOG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _catat_log(jenis, ringkasan, verdict, pitch_hz=None):
    from datetime import datetime

    log = _muat_log()
    log.append({
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jenis": jenis,
        "ringkasan": (ringkasan or "")[:200],
        "verdict": verdict,
        "pitch_hz": pitch_hz,
    })
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return log


def _log_ke_tabel(log=None):
    log = log if log is not None else _muat_log()
    if not log:
        return [["(belum ada entri)", "", "", "", ""]]
    return [[e.get("tanggal", ""), e.get("jenis", ""), e.get("ringkasan", ""),
             e.get("verdict", ""),
             ("" if e.get("pitch_hz") is None else str(e.get("pitch_hz")))]
            for e in reversed(log)]


# ---------------------------------------------------------------------------
# Fitur 2 — Penjaga Konsistensi (aturan berbasis kartu terkunci)
# ---------------------------------------------------------------------------
# Kata/kalimat yang bertentangan dengan sifat Momo (datang dari draf yang
# menggambarkan Momo — bukan Oyen).
SIFAT_BERTENTANGAN = [
    "ceria", "riang", "semangat", "antusias", "hyper", "hiperaktif",
    "excited", "cheerful", "energetic", "suara tinggi", "nada tinggi",
    "high pitch", "high-pitched", "melengking", "tertawa terbahak",
    "berteriak", "screaming", "shouting happily",
]
WAJAH_SALAH = [
    "oren", "orange", "kucing oren", "mata biru", "blue eyes",
    "kucing kecil", "tubuh kecil", "kurus", "berbulu panjang",
]
# Kata kunci latar -> label latar. Dipakai untuk cek "latar mengikuti judul".
LATAR_KATA = {
    "pantai": "Pantai", "beach": "Pantai", "sunset beach": "Pantai",
    "studio": "Studio Podcast", "podcast studio": "Studio Podcast",
    "kolam": "Kolam", "pond": "Kolam",
    "dapur": "Dapur", "kitchen": "Dapur",
    "pasar": "Pasar", "market": "Pasar",
    "hutan": "Hutan", "forest": "Hutan",
    "bulan": "Bulan / luar angkasa", "moon": "Bulan / luar angkasa",
    "angkasa": "Bulan / luar angkasa", "space": "Bulan / luar angkasa",
}


def _latar_dari_teks(teks):
    rendah = (teks or "").lower()
    ketemu = []
    for kata, label in LATAR_KATA.items():
        if kata in rendah and label not in ketemu:
            ketemu.append(label)
    return ketemu


def _aturan_dasar(draf, judul=""):
    """Periksa draf dengan aturan berbasis kartu terkunci.

    Mengembalikan (penyimpangan, catatan_ok). penyimpangan = list dict
    {kategori, temuan, saran}. Aturan ini SELALU jalan — juga di mode Gemini.
    """
    menyimpang, ok = [], []
    teks = draf or ""
    rendah = teks.lower()

    # 1) Suara: voice_id lain disebut.
    for vid in sorted(set(re.findall(r"MAI_\d+", teks, flags=re.IGNORECASE))):
        if vid.upper() != VOICE_ID.split(":")[-1].upper():
            menyimpang.append({
                "kategori": "Suara",
                "temuan": f"voice_id {vid} disebut — bukan suara Momo.",
                "saran": f"Ganti dengan voice_id permanen Momo: {VOICE_ID} "
                         f"(speed {SPEED}).",
            })
    if "mai_01" in rendah or "oyen" in rendah and "suara oyen" in rendah:
        if not any(m["kategori"] == "Suara" for m in menyimpang):
            menyimpang.append({
                "kategori": "Suara",
                "temuan": "Suara Oyen (MAI_01) disebut untuk Momo.",
                "saran": f"Momo memakai {VOICE_ID}, speed {SPEED}. "
                         "Suara Oyen (MAI_01) hanya untuk Oyen.",
            })
    if re.search(r"\bvoice_id\b", rendah) and VOICE_ID.lower() in rendah:
        ok.append("voice_id Momo benar (avocado_v2:MAI_03).")

    # 2) Suara: speed lain disebut.
    for m in re.finditer(r"speed\s*[:=]?\s*(\d+)", rendah):
        if int(m.group(1)) != SPEED:
            menyimpang.append({
                "kategori": "Suara",
                "temuan": f"speed {m.group(1)} disebut — bukan speed Momo.",
                "saran": f"Speed permanen Momo: {SPEED}.",
            })

    # 3) Suara: angka pitch disebut dan di luar target <200 Hz.
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*hz", rendah):
        nilai = float(m.group(1).replace(",", "."))
        if nilai >= PITCH_TARGET_MAX:
            menyimpang.append({
                "kategori": "Suara",
                "temuan": f"Pitch {nilai:g} Hz disebut — di atas target "
                          f"Momo (<{PITCH_TARGET_MAX:g} Hz).",
                "saran": "Cek telinga Cipta yang memutuskan; bila suara "
                         "terdengar tinggi, generate ulang dengan "
                         f"{VOICE_ID} speed {SPEED}.",
            })
        else:
            ok.append(f"Pitch {nilai:g} Hz masih di bawah target "
                      f"<{PITCH_TARGET_MAX:g} Hz.")

    # 4) Sifat: Momo digambarkan bertentangan dengan karakternya.
    for kata in SIFAT_BERTENTANGAN:
        if kata in rendah:
            menyimpang.append({
                "kategori": "Sifat",
                "temuan": f"Momo digambarkan '{kata}' — bertentangan dengan "
                          "sifatnya (rendah, tenang, datar-sinis).",
                "saran": "Momo itu skeptis, datar, sinis tapi sayang. "
                         "Ceria / suara tinggi itu sifat Oyen, bukan Momo.",
            })
            break

    # 5) Wajah: Momo digambarkan dengan ciri yang salah.
    for kata in WAJAH_SALAH:
        if kata in rendah:
            menyimpang.append({
                "kategori": "Wajah",
                "temuan": f"Momo digambarkan '{kata}' — bukan ciri Momo "
                          "(abu-abu besar British Shorthair, mata "
                          "hijau/kuning).",
                "saran": "Pakai gambar avatar tetap avatars/momo-avatar.jpg "
                         "sebagai patokan wajah; jangan generate ulang "
                         "tokoh dari nol.",
            })
            break

    # 6) Tempat: latar tidak mengikuti judul (bila judul diisi).
    if (judul or "").strip():
        latar_judul = _latar_dari_teks(judul)
        latar_draf = _latar_dari_teks(teks)
        if latar_judul and latar_draf:
            beda = [l for l in latar_draf if l not in latar_judul]
            if beda:
                menyimpang.append({
                    "kategori": "Tempat",
                    "temuan": f"Judul mengarah ke latar {', '.join(latar_judul)}, "
                              f"tapi draf memakai latar {', '.join(beda)}.",
                    "saran": "Latar SELALU mengikuti judul (aturan kualitas "
                             "#4). Ganti latar draf agar sama dengan judul.",
                })
            else:
                ok.append("Latar draf mengikuti judul.")
    return menyimpang, ok


def _cek_gemini(draf, judul=""):
    """Minta Gemini menilai draf terhadap kartu terkunci. Kembalikan teks
    penilaian atau None bila tidak ada key / gagal."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=kunci)
        model = genai.GenerativeModel("gemini-4-hydrogen")
        prompt = (
            "Kamu penjaga konsistensi tokoh Momo (Podcast Meong). Kartu terkunci Momo:\n"
            f"- Nama: {TOKOH['nama']}; {TOKOH['deskripsi']}; peran: {TOKOH['peran']}.\n"
            f"- Suara permanen: {VOICE_ID}, speed {SPEED}, bahasa id "
            f"(dialog bisa Inggris), sifat suara: {SUARA['sifat']}.\n"
            f"- Target pitch <{PITCH_TARGET_MAX:g} Hz; pitch sampel permanen "
            f"{PITCH_SAMPEL} Hz.\n"
            f"- Sifat dialog: {TOKOH['sifat_dialog']}\n"
            f"- Lawan bicara utama: {TOKOH['lawan_bicara']}\n"
            f"- Voice lock EN: {TOKOH['voice_lock_en']}\n"
            f"- Voice lock ID: {TOKOH['voice_lock_id']}\n\n"
            f"Judul konten: {judul or '(tidak diisi)'}\n\n"
            "Draf yang diperiksa:\n" + draf + "\n\n"
            "Tugas: sebutkan PENYIMPANGAN dari kartu terkunci di atas, "
            "per kategori (Suara / Wajah / Tempat / Sifat). Bila tidak ada "
            "penyimpangan, tulis 'TIDAK ADA PENYIMPANGAN'. "
            "Jawab singkat, daftar bernomor, bahasa Indonesia."
        )
        r = model.generate_content(prompt)
        return (r.text or "").strip() or None
    except Exception as e:  # noqa: BLE001 — tampilkan apa adanya
        return f"[Gemini gagal: {e}]"


def cek_konsistensi(draf, judul=""):
    """Fitur 2. Mengembalikan (verdict_md, tabel_log)."""
    draf = (draf or "").strip()
    judul = (judul or "").strip()
    if len(draf) < 20:
        verdict = ("## ⏳ BELUM CUKUP DATA\n\n"
                   "Draf terlalu pendek / kosong — tidak cukup data untuk "
                   "menilai konsistensi Momo. Isi draf (dialog / prompt / "
                   "deskripsi adegan / hasil cek pitch) minimal satu kalimat "
                   "lengkap, lalu periksa lagi.")
        _catat_log("cek_konsistensi", draf or "(kosong)", "BELUM CUKUP DATA")
        return verdict, _log_ke_tabel()

    menyimpang, ok = _aturan_dasar(draf, judul)
    mode = "template (tanpa API key Gemini)"
    penilaian_gemini = _cek_gemini(draf, judul)
    if penilaian_gemini is not None:
        mode = "Gemini (gemini-4-hydrogen) + verifikasi aturan dasar di kode"

    if menyimpang:
        verdict_status = "PERLU PERBAIKAN"
        emoji = "⚠️"
    else:
        verdict_status = "LULUS"
        emoji = "✅"

    baris = [f"## {emoji} {verdict_status}",
             f"**Mode:** {mode} | **Judul:** {judul or '(tidak diisi)'}",
             ""]
    if menyimpang:
        baris.append(f"**Penyimpangan ditemukan: {len(menyimpang)}**")
        baris.append("")
        baris.append("| # | Kategori | Temuan | Saran perbaikan |")
        baris.append("|---|----------|--------|-----------------|")
        for i, m in enumerate(menyimpang, 1):
            baris.append(f"| {i} | {m['kategori']} | {m['temuan']} | "
                         f"{m['saran']} |")
        baris.append("")
    else:
        baris.append("Tidak ada penyimpangan dari kartu terkunci Momo "
                     "menurut aturan dasar.")
        baris.append("")
    if ok:
        baris.append("**Yang sudah benar:**")
        for o in ok:
            baris.append(f"- {o}")
        baris.append("")
    if penilaian_gemini:
        baris.append("**Penilaian Gemini:**")
        baris.append("")
        baris.append(penilaian_gemini)
        baris.append("")
    baris.append("Aturan dasar di kode SELALU diverifikasi — penilaian "
                 "Gemini tidak bisa membatalkan penyimpangan aturan dasar.")
    verdict = "\n".join(baris) + DISCLAIMER
    _catat_log("cek_konsistensi",
               f"{judul} — {draf[:120]}" if judul else draf[:150],
               verdict_status)
    return verdict, _log_ke_tabel()


# ---------------------------------------------------------------------------
# Fitur 3 — Buat Baris Dialog (mode template + Gemini)
# ---------------------------------------------------------------------------
# Bank baris template Momo (Inggris). Tiap baris merespons klaim absurd Oyen
# dengan logika + sindiran kering, punchline kering di akhir. Jumlah kata
# diverifikasi di runtime (harus 17–25); baris di luar rentang tidak dipakai.
BANK_BARIS = [
    # (kata kunci pemilih, baris)
    (("moon", "bulan", "fish", "ikan"),
     "Oyen, the moon is a rock. It is not fried, not fish, and not dinner. "
     "Please stop licking the telescope and come back inside now."),
    (("beach", "pantai", "sunset", "senja", "crab", "kepiting"),
     "Oyen, the beach is for sitting quietly and judging the waves, not for "
     "shouting at crabs. Sit down, breathe slowly, and watch the sunset."),
    (("food", "makan", "fridge", "kulkas", "eat", "lapar", "hungry"),
     "Oyen, you have already eaten twice today. The fridge is not a "
     "restaurant, and I am not taking orders from a cat in a hat."),
    (("love", "cinta", "pacar", "pacaran", "dating", "girlfriend"),
     "Oyen, falling in love does not require a speech, a song, and "
     "fireworks. Just say hello, be normal, and stop practicing in the mirror."),
    (("viral", "money", "uang", "rich", "kaya", "follower"),
     "Oyen, going viral is not a plan. It is luck with better lighting. Make "
     "something honest, post it daily, and let the internet decide slowly."),
    ((),
     "Oyen, that is not how the world works, and you know it. I have "
     "explained this three times already, yet here we are again."),
    ((),
     "Fine. Believe whatever you want, Oyen. I will be over here, quietly "
     "being right, while reality does its slow, patient work."),
    ((),
     "No, Oyen. The answer is still no. It was no yesterday, it is no "
     "today, and it will be no tomorrow, cute face or not."),
]

# Baris template yang lolos rentang kata, dihitung sekali saat impor.
BANK_VALID = [(kunci, teks) for kunci, teks in BANK_BARIS
              if 17 <= hitung_kata(teks) <= 25]


def _pilih_template(judul, baris_sebelumnya):
    gabung = f"{judul or ''} {baris_sebelumnya or ''}".lower()
    for kunci, teks in BANK_VALID:
        if kunci and any(k in gabung for k in kunci):
            return teks
    umum = [t for k, t in BANK_VALID if not k]
    if not umum:
        return None
    idx = abs(hash(gabung)) % len(umum)
    return umum[idx]


def _baris_gemini(judul, latar_nama, baris_sebelumnya):
    """Minta Gemini satu baris dialog Momo 17–25 kata. Kembalikan teks atau
    None bila tidak ada key / gagal / di luar rentang setelah 2 percobaan."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None, "tanpa API key"
    try:
        import google.generativeai as genai

        genai.configure(api_key=kunci)
        model = genai.GenerativeModel("gemini-4-hydrogen")
        prompt = (
            "Tulis SATU baris dialog bahasa Inggris untuk Momo, kucing "
            "abu-abu besar British Shorthair yang skeptis, datar, sinis tapi "
            "sayang (Podcast Meong). Momo merespons klaim absurd Oyen "
            "(kucing oren, ceria, polos) dengan logika + sindiran kering, "
            "punchline kering di akhir. Gaya suara: "
            f"{TOKOH['voice_lock_en']}\n"
            f"Judul konten: {judul or '(tidak diisi)'}; latar: {latar_nama}.\n"
            f"Baris sebelumnya (Oyen): {baris_sebelumnya or '(tidak ada)'}\n"
            "SYARAT KERAS: baris HARUS 17–25 kata (hitung sendiri sebelum "
            "menjawab), SATU kalimat utuh, tanpa nama pembicara di depan, "
            "tanpa tanda kutip. Kembalikan baris itu saja."
        )
        for _ in range(2):
            r = model.generate_content(prompt)
            teks = (r.text or "").strip().strip('"').strip()
            if teks and 17 <= hitung_kata(teks) <= 25:
                return teks, "Gemini (gemini-4-hydrogen)"
        return None, "Gemini mengembalikan baris di luar 17–25 kata (2x coba)"
    except Exception as e:  # noqa: BLE001
        return None, f"Gemini gagal: {e}"


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
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3_path,
                        wav], check=True, timeout=120)
        r = subprocess.run([VENV_PYTHON, PITCH_SCRIPT, wav],
                           capture_output=True, text=True, timeout=300)
        os.remove(wav)
        data = json.loads(r.stdout)
        return data.get("gated_median"), data.get("gated_mean"), "ok"
    except Exception as e:  # noqa: BLE001
        return None, None, f"gagal ukur pitch: {e}"


def generate_audio_momo(teks):
    """Generate audio TTS Momo bila tts CLI ada. Kembalikan
    (path_audio_atau_None, laporan_pitch)."""
    if not _tts_tersedia():
        return None, (
            "⚠️ TTS CLI (/opt/hatch/bin/tts) TIDAK tersedia di mesin ini "
            "(mis. saat jalan di Hugging Face Spaces). Audio TIDAK dibuat di "
            "sini — pakai script TTS + perintah CLI di bawah, jalankan di "
            "mesin Muse. Suara tetap terkunci: "
            f"{VOICE_ID}, speed {SPEED}. Telinga Cipta yang memutuskan."
        )
    from datetime import datetime

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = os.path.join(OUTPUT_DIR, "audio", stamp)
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, "momo-baris.mp3")
    cmd = [TTS_CLI, "speak", "--voice", VOICE_ID, "--speed", str(SPEED),
           "--language", "en", "--output", out, "--text-stdin"]
    try:
        r = subprocess.run(cmd, input=teks, capture_output=True, text=True,
                           timeout=180)
        if r.returncode != 0 or not os.path.isfile(out):
            return None, (f"GAGAL generate audio — "
                          f"{r.stderr.strip()[:200]}")
    except Exception as e:  # noqa: BLE001
        return None, f"GAGAL generate audio — {e}"
    med, _mean, pesan = _cek_pitch(out)
    if med is None:
        return out, f"Audio jadi ({out}), pitch {pesan} — cek telinga Cipta."
    status = ("LULUS" if med < PITCH_TARGET_MAX
              else "DI ATAS TARGET — cek telinga Cipta")
    return out, (f"Pitch median (energy-gated): {med:.1f} Hz — target "
                 f"<{PITCH_TARGET_MAX:g} Hz (sampel permanen {PITCH_SAMPEL} "
                 f"Hz) — {status}. Telinga Cipta yang memutuskan.")


def buat_baris_dialog(judul, latar_key, latar_kustom, baris_sebelumnya):
    """Fitur 3. Mengembalikan (hasil_md, audio_path, laporan_pitch,
    tabel_log)."""
    judul = (judul or "").strip()
    latar = TOKOH["latar"].get(latar_key)
    if latar_kustom and latar_kustom.strip():
        latar_nama = f"Kustom: {latar_kustom.strip()}"
    elif latar:
        latar_nama = latar["nama"]
    else:
        latar_nama = "Studio Podcast"

    teks, mode = _baris_gemini(judul, latar_nama, baris_sebelumnya)
    if teks is None:
        teks = _pilih_template(judul, baris_sebelumnya)
        mode = ("template (tanpa API key Gemini)"
                if mode == "tanpa API key"
                else f"template (fallback: {mode})")
    n_kata = hitung_kata(teks)
    peringatan = ""
    if not 17 <= n_kata <= 25:
        peringatan = (f"\n\n⚠️ **PERINGATAN: baris ini {n_kata} kata — DI LUAR "
                     "rentang 17–25 kata.** Jangan dipakai apa adanya; "
                     "minta Muse perbaiki dulu.")

    audio_path, laporan_pitch = generate_audio_momo(teks)
    pitch_hz = None
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*Hz", laporan_pitch)
    if m and "median" in laporan_pitch:
        pitch_hz = float(m.group(1).replace(",", "."))

    script_tts = f"Momo: {teks}"
    perintah_cli = (
        "# Jalankan di mesin Muse (lokal):\n"
        f"  /opt/hatch/bin/tts speak --voice {VOICE_ID} --speed {SPEED} "
        f"--language en --output momo-baris.mp3 --text-stdin <<'EOF'\n"
        f"{teks}\nEOF"
    )
    hasil = "\n".join([
        f"# Baris Dialog — Momo ({latar_nama})",
        f"**Judul:** {judul or '(tidak diisi)'}",
        "",
        f"**Dialog (Inggris):** {teks}",
        "",
        f"**Jumlah kata: {n_kata}** — rentang wajib 17–25 kata: "
        f"{'✅ DALAM RENTANG' if 17 <= n_kata <= 25 else '❌ DI LUAR RENTANG'}",
        peringatan,
        "",
        f"**Mode:** {mode}",
        "",
        "**Voice lock yang dipakai (EN):**",
        TOKOH["voice_lock_en"],
        "",
        "**Script TTS:**",
        "```",
        script_tts,
        "```",
        "",
        "**Perintah tts CLI:**",
        "```bash",
        perintah_cli,
        "```",
        "",
        "**Cek pitch:**",
        laporan_pitch,
    ]) + DISCLAIMER
    _catat_log("buat_dialog",
               f"{judul} — {teks[:120]}" if judul else teks[:150],
               "LULUS" if 17 <= n_kata <= 25 else "PERLU PERBAIKAN",
               pitch_hz)
    return hasil, audio_path, laporan_pitch, _log_ke_tabel()


# ---------------------------------------------------------------------------
# Fitur 1 — Kartu Tokoh Terkunci
# ---------------------------------------------------------------------------
def kartu_tokoh_md():
    s = SUARA
    return "\n".join([
        "# 🐱 Kartu Tokoh Terkunci — Momo",
        "",
        "🔒 **SUARA + WAJAH PERMANEN — JANGAN DIUBAH.** Kartu ini dikunci "
        "18 Nov 2026 atas perintah Cipta. Aplikasi ini TIDAK menyediakan "
        "kontrol untuk mengubah apa pun di bawah ini. Perubahan hanya lewat "
        "edit `tokoh.json` oleh Muse atas perintah eksplisit Cipta.",
        "",
        "| | |",
        "|---|---|",
        f"| **Nama** | {TOKOH['nama']} |",
        f"| **Peran** | {TOKOH['peran']} |",
        f"| **Penampilan** | {TOKOH['deskripsi']} |",
        f"| **voice_id** | `{s['voice_id']}` |",
        f"| **Speed** | {s['speed']} |",
        f"| **Bahasa** | {s['bahasa']} (dialog bisa Inggris) |",
        f"| **Sifat suara** | {s['sifat']} |",
        f"| **Target pitch** | {s['pitch_target_hz']} Hz |",
        f"| **Pitch sampel permanen** | {s['pitch_sampel_permanen_hz']} Hz |",
        f"| **Avatar** | `{TOKOH['avatar']}` |",
        f"| **Sampel audio** | `{TOKOH['sampel_audio']}` |",
        "",
        f"**Sifat dialog:** {TOKOH['sifat_dialog']}",
        "",
        f"**Lawan bicara utama:** {TOKOH['lawan_bicara']}",
        "",
        "**Voice lock (EN):**",
        f"> {TOKOH['voice_lock_en']}",
        "",
        "**Voice lock (ID):**",
        f"> {TOKOH['voice_lock_id']}",
        "",
        "**Latar yang tersedia:** Pantai (`latar/latar-pantai.jpg`), "
        "Studio Podcast (`latar/latar-studio.jpg`), atau kustom mengikuti "
        "judul konten.",
    ])


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
def build_ui():
    with gr.Blocks(title="Agent 12 — Momo (Penjaga Konsistensi)",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🐱 Agent 12 — Momo (Penjaga Konsistensi Tokoh)\n"
            "Penjaga konsistensi tokoh Momo — wajah + suara terkunci — "
            "memeriksa setiap konten sebelum produksi.\n\n"
            "🔒 **SUARA PERMANEN:** Momo `avocado_v2:MAI_03` speed 100 · "
            "target pitch <200 Hz (sampel permanen 153,3 Hz). "
            "Semua output adalah DRAF untuk persetujuan Cipta.")

        with gr.Tab("🔒 Kartu Tokoh Terkunci"):
            with gr.Row():
                gr.Image(os.path.join(BASE, TOKOH["avatar"]),
                         label="Avatar Momo (tetap — jangan diganti)",
                         height=320)
                gr.Audio(os.path.join(BASE, TOKOH["sampel_audio"]),
                         label="Sampel suara permanen Momo (153,3 Hz)")
            gr.Markdown(kartu_tokoh_md())

        with gr.Tab("🛡️ Penjaga Konsistensi"):
            gr.Markdown(
                "Tempel draf (dialog / prompt / deskripsi adegan / hasil cek "
                "pitch). Aplikasi memeriksa draf terhadap kartu terkunci "
                "Momo. Bila input kosong atau tidak cukup data → "
                "**BELUM CUKUP DATA**.")
            judul_cek = gr.Textbox(label="Judul konten (opsional — untuk cek latar mengikuti judul)",
                                   placeholder="cth. Oyen Pacaran di Pantai")
            draf = gr.Textbox(label="Draf yang diperiksa",
                              lines=8,
                              placeholder="cth. Momo: ... / Prompt Flow: ... / Hasil cek pitch: 153,3 Hz ...")
            tombol_cek = gr.Button("Periksa Konsistensi", variant="primary")
            verdict = gr.Markdown()
            gr.Markdown("### 📋 Log Penjagaan (terbaru di atas)")
            log_tabel_cek = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                value=_log_ke_tabel(), interactive=False)
            tombol_cek.click(fn=cek_konsistensi,
                             inputs=[draf, judul_cek],
                             outputs=[verdict, log_tabel_cek])

        with gr.Tab("💬 Buat Baris Dialog"):
            gr.Markdown(
                "Buat 1 baris dialog Momo (bahasa Inggris, 17–25 kata) yang "
                "merespons Oyen. Jumlah kata dihitung dan ditampilkan. Bila "
                "tts CLI tersedia di mesin ini, audio ikut dibuat + pitch "
                "diukur (target <200 Hz).")
            judul_dialog = gr.Textbox(label="Judul konten",
                                      value="The Moon Is Made of Fried Fish")
            with gr.Row():
                latar_dd = gr.Dropdown(
                    choices=[("Pantai", "pantai"),
                             ("Studio Podcast", "studio")],
                    value="pantai", label="Latar (mengikuti judul)")
                latar_kustom = gr.Textbox(
                    label="Latar kustom (opsional, bila bukan Pantai/Studio)",
                    placeholder="cth. Kolam ikan saat senja")
            baris_sebelum = gr.Textbox(
                label="Baris sebelumnya — Oyen (opsional)",
                placeholder="cth. Momo, the moon is made of fried fish!",
                lines=2)
            tombol_buat = gr.Button("Buat Baris Dialog Momo", variant="primary")
            hasil_dialog = gr.Markdown()
            audio_dialog = gr.Audio(label="Audio TTS Momo (bila dibuat di mesin ini)")
            laporan_pitch = gr.Textbox(label="Laporan pitch", lines=3)
            gr.Markdown("### 📋 Log Penjagaan (terbaru di atas)")
            log_tabel_dialog = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                value=_log_ke_tabel(), interactive=False)
            tombol_buat.click(fn=buat_baris_dialog,
                              inputs=[judul_dialog, latar_dd, latar_kustom,
                                      baris_sebelum],
                              outputs=[hasil_dialog, audio_dialog,
                                       laporan_pitch, log_tabel_dialog])

        with gr.Tab("📋 Log Penjagaan"):
            gr.Markdown(
                "Setiap pemeriksaan (Penjaga Konsistensi) dan setiap baris "
                "dialog yang dibuat dicatat ke `data/log-penjagaan.json`.")
            log_tabel = gr.Dataframe(
                headers=["Tanggal", "Jenis", "Ringkasan", "Verdict", "Pitch (Hz)"],
                value=_log_ke_tabel(), interactive=False)
            tombol_muat = gr.Button("Muat Ulang Log")
            tombol_muat.click(fn=lambda: _log_ke_tabel(), outputs=[log_tabel])
    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
