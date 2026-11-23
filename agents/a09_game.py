# ======================================================================
# PUSAT KOMANDO — salinan dari agent-produksi-game-aplikasi (Agent 9 Produksi Game & Aplikasi).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
"""Agent Produksi Game & Aplikasi — Podcast Meong.

Agent AI gratis kesembilan: generator ide game/aplikasi, kerangka kode,
naskah toko, dan pelacak produksi. Model Gemini free tier (bila ada key),
selebihnya template lokal. Semua output adalah DRAF/prototipe untuk
persetujuan Cipta — tidak ada yang diterbitkan otomatis.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "data"  # PUSAT KOMANDO: folder data bersama
DATA_FILE = BASE_DIR / "game_data.json"  # PUSAT KOMANDO

# ---------------------------------------------------------------- Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
_model = None
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-4-hydrogen")
    except Exception:
        _model = None


def mode_ai():
    """True bila mode AI Gemini aktif, False bila mode template lokal."""
    return _model is not None


def tanya_ai(prompt, fallback):
    """Tanya Gemini; bila tidak ada key / gagal, pakai fallback template."""
    if _model is not None:
        try:
            resp = _model.generate_content(prompt)
            teks = (resp.text or "").strip()
            if teks:
                return teks
        except Exception:
            pass
    return fallback


# ---------------------------------------------------------------- Pengetahuan
BRAND = "Podcast Meong — Oyen (kucing oren) & Momo (kucing abu-abu), komedi absurd, target global."
GAME_PERTAMA = (
    '"Oyen Tangkap Ikan" (HTML5, tangkap ikan goreng jatuh, 3 nyawa, level naik, PWA) '
    "— game pertama yang sedang dibuat."
)
TEKNOLOGI = "Game web HTML5/Canvas (tanpa aset berbayar), PWA (bisa diinstal dari browser), aplikasi web (Gradio/Python atau HTML statis)."

DISTRIBUSI_GRATIS = (
    "itch.io (bagi hasil bisa 0%), website sendiri (podcastmeong.github.io), "
    "Game Jolt, F-Droid (khusus open source)."
)
DISTRIBUSI_BERBAYAR = (
    "Google Play Store ($25 sekali bayar, komisi ~15% untuk $1 juta pertama/tahun), "
    "Steam ($100 per game)."
)
MONETISASI = (
    "Harga tetap, bayar seikhlasnya, donasi, iklan, pembelian di dalam aplikasi. "
    "Tidak ada janji penghasilan — yang menentukan laku atau tidak adalah yang memakainya, "
    "jadi tetap butuh promosi."
)

STATUS_PRODUKSI = ["ide", "prototipe", "diuji", "diterbitkan"]
JENIS_PROYEK = ["game", "aplikasi"]

GENRE_GAME = {
    "tangkap": {
        "nama": "Tangkap (Catch)",
        "mekanik": "Objek jatuh dari atas; pemain menggerakkan karakter kiri-kanan untuk menangkap yang benar dan menghindari yang salah.",
        "kesulitan": "Mudah — cocok sebagai game pertama.",
    },
    "lari": {
        "nama": "Lari / Lompat (Runner)",
        "mekanik": "Karakter berlari otomatis; pemain melompat atau menghindar tepat waktu. Kecepatan naik tiap level.",
        "kesulitan": "Sedang — butuh tuning kecepatan dan jarak rintangan.",
    },
    "teka-teki": {
        "nama": "Teka-teki (Puzzle)",
        "mekanik": "Pemain memecahkan susunan/pola (cocokkan 3, geser balok, atau jawab cepat). Santai, tanpa tekanan waktu keras.",
        "kesulitan": "Sedang — butuh desain level yang adil dan makin menantang.",
    },
    "masak": {
        "nama": "Masak / Layan (Time Management)",
        "mekanik": "Pemain melayani pesanan secepat mungkin sebelum pelanggan kesal. Kombinasi kecepatan + ingatan.",
        "kesulitan": "Sedang — butuh keseimbangan jumlah pesanan dan waktu.",
    },
    "balap": {
        "nama": "Balap (Racing)",
        "mekanik": "Pemain berpindah jalur untuk mengumpulkan bonus dan menghindari rintangan. Kecepatan naik tiap putaran.",
        "kesulitan": "Sedang — butuh variasi trek dan rintangan.",
    },
    "petualangan": {
        "nama": "Petualangan (Adventure)",
        "mekanik": "Pemain menjelajah beberapa area, mengumpulkan benda, dan menyelesaikan misi kecil. Ada cerita ringan.",
        "kesulitan": "Sulit — butuh peta, dialog, dan misi yang dirancang matang.",
    },
}

# ---------------------------------------------------------------- Data proyek
def muat_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []


def simpan_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def tabel_proyek():
    data = muat_data()
    if not data:
        return "Belum ada proyek. Tambahkan game/aplikasi pertama di bawah."
    baris = ["| Nama | Jenis | Status | Catatan |", "|---|---|---|---|"]
    for p in data:
        baris.append(
            "| {n} | {j} | {s} | {c} |".format(
                n=p.get("nama", "-"), j=p.get("jenis", "-"),
                s=p.get("status", "-"), c=p.get("catatan", "-"),
            )
        )
    ringkas = {}
    for p in data:
        ringkas[p.get("status", "?")] = ringkas.get(p.get("status", "?"), 0) + 1
    total = "Ringkasan: " + ", ".join(
        "{s}: {n}".format(s=s, n=n) for s, n in sorted(ringkas.items())
    )
    return "\n".join(baris) + "\n\n" + total


def tambah_proyek(nama, jenis, status, catatan):
    nama = (nama or "").strip()
    if not nama:
        return "Nama proyek wajib diisi.", tabel_proyek()
    if jenis not in JENIS_PROYEK:
        return "Jenis harus 'game' atau 'aplikasi'.", tabel_proyek()
    if status not in STATUS_PRODUKSI:
        return "Status tidak dikenal.", tabel_proyek()
    data = muat_data()
    if any(p.get("nama", "").lower() == nama.lower() for p in data):
        return "Proyek '{n}' sudah ada.".format(n=nama), tabel_proyek()
    data.append({
        "nama": nama, "jenis": jenis, "status": status,
        "catatan": (catatan or "").strip(),
    })
    simpan_data(data)
    return "Proyek '{n}' ditambahkan (status: {s}).".format(n=nama, s=status), tabel_proyek()


def ubah_status(nama, status_baru):
    nama = (nama or "").strip()
    if status_baru not in STATUS_PRODUKSI:
        return "Status baru tidak dikenal.", tabel_proyek()
    data = muat_data()
    for p in data:
        if p.get("nama", "").lower() == nama.lower():
            p["status"] = status_baru
            simpan_data(data)
            return "Status '{n}' diubah menjadi {s}.".format(n=nama, s=status_baru), tabel_proyek()
    return "Proyek '{n}' tidak ditemukan.".format(n=nama), tabel_proyek()


def hapus_proyek(nama):
    nama = (nama or "").strip()
    data = muat_data()
    baru = [p for p in data if p.get("nama", "").lower() != nama.lower()]
    if len(baru) == len(data):
        return "Proyek '{n}' tidak ditemukan.".format(n=nama), tabel_proyek()
    simpan_data(baru)
    return "Proyek '{n}' dihapus.".format(n=nama), tabel_proyek()


# ---------------------------------------------------------------- Generator ide game
def ide_game(tema, genre, pemain):
    tema = (tema or "").strip()
    genre = (genre or "").strip().lower()
    pemain = (pemain or "").strip() or "semua umur"
    if not tema:
        return "Tema game wajib diisi (contoh: ikan goreng, kolam, pasar malam)."
    g = GENRE_GAME.get(genre, GENRE_GAME["tangkap"])
    draf = """# Ide Game: {tema} — {genre_nama}

**Brand:** {brand}
**Target pemain:** {pemain}
**Status:** DRAF — menunggu persetujuan Cipta.

## Konsep
Game kasual bertema "{tema}" dibintangi Oyen & Momo (Podcast Meong). Satu sesi 1–3 menit,
mudah dipahami dalam 10 detik pertama, sulit dikuasai — cocok dimainkan di HP maupun laptop.

## Cara Main
{mekanik}
Misi tiap sesi: kumpulkan skor sebanyak mungkin sebelum nyawa habis.

## Kontrol
- Keyboard: panah kiri/kanan atau A/D untuk bergerak, spasi untuk aksi (bila ada).
- Sentuh (HP): seret jari kiri-kanan; ketuk untuk aksi.
- Satu tombol Jeda + tombol Suara (mute).

## Level & Skor
- 3 nyawa. Salah tangkap / tabrakan = nyawa berkurang 1.
- Tangkap benar = +10 poin; kombo beruntun = bonus +5 per kombo.
- Level naik tiap 100 poin: kecepatan dan jumlah objek naik.
- Skor tertinggi tersimpan di perangkat (localStorage).

## Arah Seni & Suara
- Visual: warna hangat khas Podcast Meong (oranye, krem lembut), karakter digambar Canvas/SVG
  tanpa aset berbayar; animasi sederhana (goyang, lompat, ekspresi kaget).
- Suara: efek WebAudio sederhana (tangkap, salah, naik level) + tombol mute. Tanpa file audio eksternal.
- Dialog: sedikit, lucu, gaya Oyen & Momo (komedi absurd, kalimat pendek).

## Perkiraan Kesulitan Pembuatan
{kesulitan}

## Distribusi & Monetisasi (usulan)
- Gratis: {dist_gratis}
- Berbayar: {dist_bayar}
- Monetisasi: {monetisasi}

## Catatan ATM (Amati–Tiru–Modifikasi)
Ide ini dirancang sebagai karya sendiri — amati game sejenis, tiru polanya, lalu modifikasi
tema, karakter, dan aturannya. JANGAN menjiplak game/aplikasi orang lain mentah-mentah
(nama, aset, level, atau kode yang sama persis).
""".format(
        tema=tema, genre_nama=g["nama"], brand=BRAND, pemain=pemain,
        mekanik=g["mekanik"], kesulitan=g["kesulitan"],
        dist_gratis=DISTRIBUSI_GRATIS, dist_bayar=DISTRIBUSI_BERBAYAR,
        monetisasi=MONETISASI,
    )
    prompt = (
        "Kamu asisten produksi game Podcast Meong (Oyen & Momo, komedi absurd, target global). "
        "Kembangkan ide game berikut menjadi konsep yang lebih kaya dan orisinal, tetap Bahasa Indonesia, "
        "tetap sederhana dan bisa dibuat dengan HTML5/Canvas. Jangan menjiplak game yang sudah ada; "
        "jangan janjikan penghasilan.\n\n" + draf
    )
    return tanya_ai(prompt, draf)


# ---------------------------------------------------------------- Generator ide aplikasi
def ide_aplikasi(tujuan, pengguna, fitur_utama):
    tujuan = (tujuan or "").strip()
    pengguna = (pengguna or "").strip() or "penggemar Podcast Meong"
    fitur_utama = (fitur_utama or "").strip() or "katalog episode & eBook"
    if not tujuan:
        return "Tujuan aplikasi wajib diisi (contoh: katalog episode, toko eBook, pengingat upload)."
    draf = """# Ide Aplikasi: {tujuan}

**Brand:** {brand}
**Pengguna:** {pengguna}
**Status:** DRAF — menunggu persetujuan Cipta.

## Tujuan
{tujuan}

## Fitur Utama
- {fitur}
- Pencarian & filter sederhana.
- Tampilan bersih, cepat dibuka di HP (responsif), tanpa login wajib.
- Tautan ke toko/layanan yang sudah ada (KaryaKarsa, Zazzle, Lynk.id, Mayar).

## Daftar Layar
1. Beranda — ringkasan & jalan pintas.
2. Daftar Isi — episode / produk / konten (kartu + gambar).
3. Detail — deskripsi lengkap + tombol aksi (tonton/beli/baca).
4. Tentang — profil Podcast Meong & tautan akun.

## Teknologi (gratis)
{teknologi}
- Hosting gratis: GitHub Pages (statis) atau Hugging Face Spaces (Gradio/Python).
- Data: file JSON lokal; tanpa basis data berbayar.

## Langkah Berikutnya
1. Setujui konsep + nama aplikasi.
2. Buat prototipe 1 layar (Beranda) dan uji di HP.
3. Tambah layar lain satu per satu; terbitkan gratis di website sendiri.

## Distribusi & Monetisasi (usulan)
- Gratis: website sendiri (podcastmeong.github.io), PWA (instal dari browser).
- Berbayar: Google Play Store ($25 sekali bayar) bila sudah terbukti dipakai.
- Monetisasi: {monetisasi}
""".format(
        tujuan=tujuan, brand=BRAND, pengguna=pengguna, fitur=fitur_utama,
        teknologi=TEKNOLOGI, monetisasi=MONETISASI,
    )
    prompt = (
        "Kamu asisten produksi aplikasi Podcast Meong (Oyen & Momo, komedi absurd). "
        "Kembangkan ide aplikasi berikut menjadi rancangan yang lebih lengkap dan praktis, "
        "tetap Bahasa Indonesia, teknologi gratis saja. Jangan janjikan penghasilan.\n\n" + draf
    )
    return tanya_ai(prompt, draf)


# ---------------------------------------------------------------- Kerangka kode
KERANGKA_GAME_HTML5 = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Game Tangkap — Kerangka (Podcast Meong)</title>
<style>
  body { margin: 0; background: #faf8f5; font-family: sans-serif; text-align: center; }
  canvas { background: #f0dfc2; display: block; margin: 0 auto; touch-action: none; }
  button { padding: 10px 20px; font-size: 16px; margin: 8px; }
</style>
</head>
<body>
<h1>Tangkap Ikan!</h1>
<p>Skor: <span id="skor">0</span> | Nyawa: <span id="nyawa">3</span></p>
<canvas id="game" width="360" height="540"></canvas>
<p><button id="mulai">Mulai</button> <button id="suara">Suara: Nyala</button></p>
<script>
// Kerangka game HTML5/Canvas — titik awal, kembangkan sendiri.
// Aturan: pemain (x) bergerak kiri-kanan; benda jatuh; tangkap = +10, salah = -1 nyawa.
const cvs = document.getElementById('game');
const ctx = cvs.getContext('2d');
let pemainX = 160, skor = 0, nyawa = 3, jalan = false, benda = [];
let bunyiNyala = true;

function acak(min, maks) { return min + Math.random() * (maks - min); }
function buatBenda() {
  benda.push({ x: acak(20, 340), y: -20, cepat: acak(2, 4), baik: Math.random() > 0.25 });
}
function bunyi(frek) {
  if (!bunyiNyala) return;
  try {
    const a = new (window.AudioContext || window.webkitAudioContext)();
    const o = a.createOscillator(); o.frequency.value = frek;
    o.connect(a.destination); o.start(); o.stop(a.currentTime + 0.08);
  } catch (e) { /* suara opsional */ }
}
function gambar() {
  ctx.clearRect(0, 0, 360, 540);
  // pemain: kotak oren (ganti dengan gambar Oyen)
  ctx.fillStyle = '#e8862e'; ctx.fillRect(pemainX, 500, 60, 30);
  for (const b of benda) {
    ctx.fillStyle = b.baik ? '#2e7d32' : '#c0392b';
    ctx.beginPath(); ctx.arc(b.x, b.y, 12, 0, Math.PI * 2); ctx.fill();
  }
}
function langkah() {
  if (!jalan) return;
  if (Math.random() < 0.02) buatBenda();
  for (const b of benda) {
    b.y += b.cepat;
    if (b.y > 500 && b.y < 530 && Math.abs(b.x - (pemainX + 30)) < 35) {
      if (b.baik) { skor += 10; bunyi(660); } else { nyawa -= 1; bunyi(180); }
      b.y = 9999;
    }
    if (b.y > 540 && b.baik) { nyawa -= 1; b.y = 9999; }
  }
  benda = benda.filter(b => b.y < 600);
  document.getElementById('skor').textContent = skor;
  document.getElementById('nyawa').textContent = nyawa;
  if (nyawa <= 0) { jalan = false; alert('Game over! Skor: ' + skor); }
  gambar();
  requestAnimationFrame(langkah);
}
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft' || e.key === 'a') pemainX = Math.max(0, pemainX - 20);
  if (e.key === 'ArrowRight' || e.key === 'd') pemainX = Math.min(300, pemainX + 20);
});
let sentuhX = null;
cvs.addEventListener('touchstart', e => { sentuhX = e.touches[0].clientX; });
cvs.addEventListener('touchmove', e => {
  const x = e.touches[0].clientX;
  if (sentuhX !== null) pemainX = Math.max(0, Math.min(300, pemainX + (x - sentuhX)));
  sentuhX = x; e.preventDefault();
});
document.getElementById('mulai').onclick = () => {
  if (jalan) return;
  skor = 0; nyawa = 3; benda = []; jalan = true; langkah();
};
document.getElementById('suara').onclick = e => {
  bunyiNyala = !bunyiNyala;
  e.target.textContent = 'Suara: ' + (bunyiNyala ? 'Nyala' : 'Mati');
};
gambar();
</script>
</body>
</html>
"""

KERANGKA_APLIKASI_WEB = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aplikasi Katalog — Kerangka (Podcast Meong)</title>
<style>
  body { margin: 0; font-family: sans-serif; background: #faf8f5; color: #3b3631; }
  header { background: #c07a54; color: #fff; padding: 16px; text-align: center; }
  main { max-width: 640px; margin: 0 auto; padding: 16px; }
  .kartu { background: #fff; border: 1px solid #e7e0d6; border-radius: 12px;
           padding: 12px; margin: 10px 0; }
  input { width: 100%; padding: 10px; font-size: 16px; box-sizing: border-box; }
  button { padding: 8px 14px; font-size: 15px; margin-top: 8px; }
</style>
</head>
<body>
<header><h1>Katalog Podcast Meong</h1></header>
<main>
  <input id="cari" type="search" placeholder="Cari episode / produk...">
  <div id="daftar"></div>
</main>
<script>
// Kerangka aplikasi web statis — titik awal, kembangkan sendiri.
// Data disimpan di array lokal; ganti dengan data asli (episode, eBook, produk).
const DATA = [
  { judul: 'Episode: Bulan Ikan Goreng', jenis: 'Video', tautan: 'https://podcastmeong.github.io/' },
  { judul: 'eBook: Si Oyen Penjaga Kolam Ikan', jenis: 'eBook', tautan: 'https://karyakarsa.com/podcast-meong/si-oyen-penjaga-kolam-ikan' },
  { judul: 'Kaos Oyen & Momo', jenis: 'POD', tautan: 'https://www.zazzle.com/store/podcast_meong' },
];
const daftar = document.getElementById('daftar');
const cari = document.getElementById('cari');
function tampilkan(kata) {
  const k = (kata || '').toLowerCase();
  daftar.innerHTML = '';
  for (const item of DATA) {
    if (k && !(item.judul.toLowerCase().includes(k) || item.jenis.toLowerCase().includes(k))) continue;
    const div = document.createElement('div');
    div.className = 'kartu';
    div.innerHTML = '<strong></strong> <span></span><br><a target="_blank" rel="noopener">Buka</a>';
    div.querySelector('strong').textContent = item.judul;
    div.querySelector('span').textContent = '· ' + item.jenis;
    div.querySelector('a').href = item.tautan;
    daftar.appendChild(div);
  }
  if (!daftar.children.length) daftar.innerHTML = '<p>Tidak ditemukan.</p>';
}
cari.addEventListener('input', () => tampilkan(cari.value));
tampilkan('');
</script>
</body>
</html>
"""


def kerangka_kode(jenis):
    if jenis == "game-html5":
        return (
            "Kerangka game HTML5/Canvas (salin ke file index.html lalu buka di browser). "
            "Ini titik awal yang bisa dikembangkan — ganti kotak oren dengan gambar Oyen, "
            "tambah level dan suara sesuai rancangan.\n\n" + KERANGKA_GAME_HTML5
        )
    if jenis == "aplikasi-web":
        return (
            "Kerangka aplikasi web statis (salin ke file index.html lalu buka di browser). "
            "Ini titik awal yang bisa dikembangkan — ganti DATA dengan katalog asli.\n\n"
            + KERANGKA_APLIKASI_WEB
        )
    return "Pilih jenis kerangka: 'game-html5' atau 'aplikasi-web'."


# ---------------------------------------------------------------- Naskah toko
def naskah_toko(nama, jenis, deskripsi, platform):
    nama = (nama or "").strip()
    jenis = (jenis or "").strip().lower()
    deskripsi = (deskripsi or "").strip()
    platform = (platform or "").strip().lower()
    if not nama:
        return "Nama game/aplikasi wajib diisi."
    if not deskripsi:
        deskripsi = "Game/aplikasi santai dari Podcast Meong, dibintangi Oyen & Momo."
    if platform == "itch.io":
        harga = "Usulan: gratis atau bayar seikhlasnya (itch.io membiarkan pembeli membayar lebih). Donasi diaktifkan."
        tag = "cats, casual, html5, cute, funny, indonesia, 2d, family-friendly"
    elif platform == "play-store":
        harga = "Usulan: gratis dengan pembelian di dalam aplikasi, atau harga tetap Rp15.000. Catatan: akun developer Play Store $25 sekali bayar."
        tag = "cats, casual, family, funny, offline"
    else:
        harga = "Usulan: gratis di website sendiri; tautan donasi (Saweria/Trakteer) di halaman game."
        tag = "podcast-meong, oyen, momo, kucing"
    draf = """# Naskah Toko: {nama}

**Platform:** {platform}
**Jenis:** {jenis}
**Status:** DRAF — menunggu persetujuan Cipta.

## Judul
{nama} — Game Santai Oyen & Momo | Podcast Meong

## Deskripsi
{deskripsi}

Mainkan sebagai Oyen, si kucing oren, bersama Momo. Santai, lucu, dan bisa dimainkan
di HP maupun laptop — tanpa instalasi berat, langsung main dari browser.

Fitur:
- Kontrol mudah: keyboard dan sentuh
- Level makin menantang, skor tertinggi tersimpan
- Gratis dimainkan, tanpa iklan mengganggu

Dari Podcast Meong — podcast komedi kucing Oyen & Momo.
Tonton episodenya di YouTube @Podcastmeong dan TikTok @podcast_kucing.

## Tag
{tag}

## Harga & Monetisasi (usulan)
{harga}

Catatan jujur: tidak ada janji penghasilan. Yang menentukan laku atau tidak adalah
yang memakainya — tetap butuh promosi.
""".format(
        nama=nama, platform=platform or "itch.io", jenis=jenis or "game",
        deskripsi=deskripsi, tag=tag, harga=harga,
    )
    prompt = (
        "Kamu penulis naskah toko game/aplikasi Podcast Meong (Oyen & Momo). "
        "Rapikan dan buat naskah toko berikut lebih menarik untuk platform "
        + (platform or "itch.io")
        + ", tetap Bahasa Indonesia/Inggris seperlunya, jujur, tanpa janji penghasilan.\n\n" + draf
    )
    return tanya_ai(prompt, draf)


# ---------------------------------------------------------------- Antarmuka
def bangun_ui():
    import gradio as gr

    with gr.Blocks(title="Agent Produksi Game & Aplikasi — Podcast Meong",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🎮 Agent Produksi Game & Aplikasi — Podcast Meong\n"
            "Ide, rancangan, kerangka kode, dan naskah toko untuk game & aplikasi. "
            "Semua output adalah **DRAF/prototipe untuk persetujuan Cipta** — "
            "tidak ada yang diterbitkan otomatis.\n\n"
            "Mode: **{mode}** — {ket}\n\n"
            "Game pertama: {game1}".format(
                mode="AI Gemini" if mode_ai() else "Template lokal",
                ket="Gemini free tier aktif." if mode_ai()
                else "Isi GEMINI_API_KEY untuk mode AI; semua generator tetap jalan dengan template.",
                game1=GAME_PERTAMA,
            )
        )
        with gr.Tabs():
            with gr.Tab("🎮 Ide Game"):
                gr.Markdown(
                    "Buat konsep game baru. Prinsip ATM: amati game sejenis, tiru polanya, "
                    "modifikasi tema/karakter/aturan — **jangan jiplak mentah-mentah**."
                )
                tema = gr.Textbox(label="Tema game", placeholder="contoh: ikan goreng, kolam, pasar malam")
                genre = gr.Dropdown(
                    choices=list(GENRE_GAME.keys()),
                    value="tangkap", label="Genre",
                )
                pemain = gr.Textbox(label="Target pemain", value="semua umur")
                btn_game = gr.Button("Buat Ide Game")
                out_game = gr.Markdown(label="Konsep game")
                btn_game.click(ide_game, [tema, genre, pemain], out_game, api_name="ide_game")

            with gr.Tab("📱 Ide Aplikasi"):
                gr.Markdown("Buat rancangan aplikasi baru (web — gratis).")
                tujuan = gr.Textbox(label="Tujuan aplikasi", placeholder="contoh: katalog episode dan eBook")
                pengguna = gr.Textbox(label="Pengguna", value="penggemar Podcast Meong")
                fitur = gr.Textbox(label="Fitur utama", value="katalog episode & eBook")
                btn_app = gr.Button("Buat Ide Aplikasi")
                out_app = gr.Markdown(label="Rancangan aplikasi")
                btn_app.click(ide_aplikasi, [tujuan, pengguna, fitur], out_app, api_name="ide_aplikasi")

            with gr.Tab("💻 Kerangka Kode"):
                gr.Markdown(
                    "Kerangka awal yang bisa dikembangkan — bukan produk jadi. "
                    "Salin ke file `index.html` lalu buka di browser untuk menguji."
                )
                jenis_kode = gr.Radio(
                    choices=[("Game HTML5/Canvas", "game-html5"),
                             ("Aplikasi web statis", "aplikasi-web")],
                    value="game-html5", label="Jenis kerangka",
                )
                btn_kode = gr.Button("Buat Kerangka Kode")
                out_kode = gr.Code(label="Kerangka kode", language="html")
                btn_kode.click(kerangka_kode, jenis_kode, out_kode, api_name="kerangka_kode")

            with gr.Tab("🏪 Naskah Toko"):
                gr.Markdown(
                    "Judul, deskripsi, tag, dan saran harga/monetisasi untuk itch.io, "
                    "Play Store, atau website sendiri."
                )
                nama_toko = gr.Textbox(label="Nama game/aplikasi", placeholder="contoh: Oyen Tangkap Ikan")
                jenis_toko = gr.Textbox(label="Jenis", value="game")
                desk_toko = gr.Textbox(label="Deskripsi singkat", lines=3,
                                       placeholder="contoh: Tangkap ikan goreng yang jatuh bersama Oyen!")
                platform = gr.Dropdown(
                    choices=["itch.io", "play-store", "website"],
                    value="itch.io", label="Platform",
                )
                btn_toko = gr.Button("Buat Naskah Toko")
                out_toko = gr.Markdown(label="Naskah toko")
                btn_toko.click(naskah_toko, [nama_toko, jenis_toko, desk_toko, platform],
                               out_toko, api_name="naskah_toko")

            with gr.Tab("📊 Pelacak Produksi"):
                gr.Markdown(
                    "Status tiap game/aplikasi: ide → prototipe → diuji → diterbitkan. "
                    "Data tersimpan di `data.json` (lokal)."
                )
                out_tabel = gr.Markdown(value=tabel_proyek(), label="Daftar proyek")
                nama_p = gr.Textbox(label="Nama proyek")
                jenis_p = gr.Dropdown(choices=JENIS_PROYEK, value="game", label="Jenis")
                status_p = gr.Dropdown(choices=STATUS_PRODUKSI, value="ide", label="Status")
                catatan_p = gr.Textbox(label="Catatan", placeholder="contoh: kerangka sudah jadi, menunggu uji")
                pesan_p = gr.Textbox(label="Pesan", interactive=False)
                btn_tambah = gr.Button("Tambah Proyek")
                btn_tambah.click(tambah_proyek, [nama_p, jenis_p, status_p, catatan_p],
                                 [pesan_p, out_tabel], api_name="tambah_proyek")
                status_baru = gr.Dropdown(choices=STATUS_PRODUKSI, value="prototipe",
                                          label="Status baru")
                btn_ubah = gr.Button("Ubah Status")
                btn_ubah.click(ubah_status, [nama_p, status_baru],
                               [pesan_p, out_tabel], api_name="ubah_status")
                btn_hapus = gr.Button("Hapus Proyek")
                btn_hapus.click(hapus_proyek, nama_p,
                                [pesan_p, out_tabel], api_name="hapus_proyek")
                btn_muat = gr.Button("Muat Ulang Tabel")
                btn_muat.click(lambda: tabel_proyek(), None, out_tabel, api_name="muat_tabel")
    return demo


if __name__ == "__main__":
    demo = bangun_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
