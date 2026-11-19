# LAPORAN — Pusat Komando Podcast Meong

**Tanggal:** 18 Nov 2026 · **Status:** selesai, teruji lokal, siap deploy (belum di-deploy — butuh akun Hugging Face + API key Gemini pemilik).

## Yang dibuat

Folder `~/workspace/your_files/oyen-podcast/pusat-komando/`:

- `app.py` (±700 baris) — satu aplikasi Gradio: header aturan SOP + tab
  **Papan Handoff** + 9 tab agent + tab Agent 2 (FastAPI) yang dibuatkan
  antarmuka Gradio dari fungsi aslinya.
- `agents/` — salinan 9 `app.py` agent asli (a01, a02, a03, a05, a06, a07,
  a08, a09, a10; total ±6.300 baris). Satu-satunya perubahan dari aslinya:
  path data dialihkan ke folder `data/` bersama (ditandai komentar
  "PUSAT KOMANDO"). Agent aslinya tidak diubah dan tetap bisa dipakai terpisah.
- `data/` — folder data bersama: `leads.json` (15 lead), `lomba.json`
  (25 lomba), `keuangan_data.json` (baseline Rp0), `riwayat_tema.json`,
  `progres.json`, `handoff.json` (antrean kosong), `handoff-templates/`
  (6 template skema SOP), `terjemahan/` (kosong — dibuat saat pertama dipakai).
- `output/` — folder draf Agent 5 (kosong — diisi saat draf dibuat).
- `requirements.txt` — gradio==6.32.0, google-generativeai==0.8.6,
  google-genai>=1.0, fastapi>=0.115, uvicorn>=0.30.
- `README.md` — cara jalan lokal + deploy ke 1 Space (ZeroGPU).

## Cara kerja Papan Handoff

- Membaca `data/` bersama: brief riset layak (Agent 10), draf terbaru
  (`output/`), lead (Agent 2), tenggat lomba ≤ 14 hari (Agent 6), uang masuk
  (Agent 7), progres terjemah (Agent 8), proyek game (Agent 9).
- Antrean handoff mengikuti skema template SOP (`sop-agent/handoff/`),
  status `draf → diperiksa → disetujui / ditolak → selesai`.
- Aksi cepat: brief Riset (10) → Produksi (5); draf Produksi (5) →
  Penjualan (2) / Terjemah (8). Semua item baru berstatus `draf`.

## Hasil uji (Python 3.12.3, mode template, tanpa API key)

- `py_compile app.py` + 9 modul agent — **OK**.
- Impor 9 modul + bangun 8 UI Gradio — **OK**, 0 tab error; semua path data
  terverifikasi mengarah ke `data/` bersama.
- Uji fungsi: **24/24 lolos** — satu panggilan per agent (Asisten jawab,
  Penjualan template + rencana 15 lead, Pertumbuhan ringkasan + aksi,
  Produksi draf puisi, Lomba tabel + pengingat, Keuangan ringkasan,
  Terjemah template, Game ide + tabel, Riset nilai + simpan) + alur handoff
  lengkap (brief 10→5 sebagai HO-001, draf 5→2 HO-002, draf 5→8 HO-003,
  ubah status → diperiksa, papan menampilkan antrean).
- Uji server live: **HTTP 200**; API Gradio `tampilkan_papan` (memuat tenggat
  AdArena dari data lama) dan `tambah_handoff` (HO-001 tersimpan dengan skema
  SOP) — **lolos**.
- Dua bug ditemukan & diperbaiki: (1) `sorted()` pada pasangan
  (tanggal, dict) gagal bila tanggal sama — sortir pakai kunci tanggal;
  (2) pengembalian list mentah ke Dropdown ID menimbulkan peringatan
  "value not in choices" — diganti `gr.update(choices=...)`; setelah
  perbaikan, log server bersih (0 peringatan).
- Artefak uji dibersihkan: data uji (riset, handoff, draf tanggal 2099)
  dihapus; `handoff.json` kembali `[]`; `output/` kosong; folder agent
  asli tidak tertulisi (mtime data lama tidak berubah); server uji dimatikan.

## Batasan (jujur)

- Space gratis tidur bila lama tak dipakai; data `data/` hilang bila Space
  di-rebuild — unduh berkala.
- Gemini free tier ada kuota harian; tanpa key / kuota habis → mode template.
- Mode AI belum teruji end-to-end tanpa key.
- Agent 2 hanya fungsi intinya yang dipakai (endpoint FastAPI tidak ikut).
- Bila satu modul agent gagal dimuat, tabnya menampilkan pesan error dan
  8 tab lain tetap jalan.

## Yang masih butuh pemilik (deploy)

1. **Akun Hugging Face** (gratis) — langkah lengkap di `README.md`;
   hardware **ZeroGPU** (maks 2 Space gratis; aplikasi ini cuma butuh 1).
2. **API key Gemini gratis** dari https://aistudio.google.com/apikey
   (opsional — tanpa key, mode template tetap jalan).

## Pembaruan 18 Nov 2026 — Riset Konten (Agent 10)

Perintah Cipta 18 Nov 22:44: Agent 10 ditambah riset konten. Perubahan
diterapkan ke `agents/a10_riset.py` (salinan yang sama dengan
`agent-riset-produk/app.py`; perbedaan tetap hanya header + path
`DATA_FILE`): tab baru **🎬 Riset Konten** (topik + platform + tujuan
viral/jualan/edukasi → hook, format, pola terverifikasi Goldy & Sapi,
skor 0–10 + verdict, langkah verifikasi), hasil disimpan ke
`data/riset.json` dengan jenis `"konten"`, dan Log Riset kini
menampilkan kolom "Jenis". Tab muncul otomatis di Pusat Komando karena
memakai `build_ui()` yang sama. Uji pembaruan: `py_compile` OK, uji
fungsi 40/40 lolos (20 per salinan), server live aplikasi agent 10
HTTP 200 + API `/nilai_konten` lolos. Detail lengkap di
`agent-riset-produk/LAPORAN.md`.

## Pembaruan 18 Nov 2026 — Penyelarasan Semua Agent

- **SOP Kerja Sama Agent AI v1.2 BERLAKU** (disetujui Cipta 18 Nov 2026 21:41): semua output agent adalah DRAF untuk persetujuan Cipta; tidak ada yang otomatis upload / kirim / transfer / bayar; dilarang mengarang data, ayat, hadis, atau angka pasar — bila data kurang, tulis "belum cukup data"; tidak ada janji penghasilan.
- **Tugas Harian Wajib kini 25 poin**: Agent 1 selalu standby dan fast respon ke customer; Agent 2, 3, 5, 6, 7, 8 kerja tiap hari + wajib laporan; Agent 9 produksi minimal 1 aplikasi/game per hari + wajib laporan; Agent 10 riset tiap minggu + wajib laporan. Semua laporan agent masuk ke laporan malam 20:00.
- **Suara avatar Oyen & Momo PERMANEN**: Oyen `avocado_v2:MAI_01` speed 110, Momo `avocado_v2:MAI_03` speed 100 — tidak boleh diubah tanpa perintah eksplisit Cipta.
- **Tokoh avatar bisa berapa pun**: tiap tokoh punya wajah + suara terkunci permanen sendiri; suara antar-tokoh harus berbeda jelas.
- **Fokus gratis dulu**: tanpa langganan berbayar (tanpa HF PRO $9/bln, Play Store $25, Steam $100) sampai ada pemasukan.
- **Cek pasar berkala tiap Senin** (~07:42 WIB): tren, peluang produk, dan perubahan aturan platform — riset jangan pakai data lama.
- **Khusus aplikasi ini**: Pusat Komando kini berisi **10 agent** — Agent Avatar Podcast ditambahkan sebagai tab 11 pada 18 Nov 2026 (salinan a11_avatar.py, aset di agents/avatar/, output ke output/avatar/, suara permanen tetap terkunci). Tab Riset Konten Agent 10 terverifikasi masih ada. Papan Handoff tetap menjadi antrean kerja bersama; data di data/ hilang bila Space di-rebuild — unduh berkala.

## Pembaruan 18 Nov 2026 — Agent 11 Oyen + Agent 12 Momo

- **Tugas Harian Wajib kini 26 poin** (dirumuskan ulang Cipta 18 Nov 2026 23:19): poin 26 — **Agent 11 (Oyen) dan Agent 12 (Momo)** menjaga, membantu, dan membuat setiap pembuatan konten agar stabil, konsisten, dan suara tidak berubah. Keduanya kerja tiap hari + wajib laporan (masuk laporan malam 20:00).
- **Agent 11 Oyen** (folder `agent-11-oyen/`, modul Pusat Komando `agents/a11_oyen.py`, aset di `agents/oyen/`): hanya mengurus Oyen — wajah `oyen-avatar.jpg` + suara permanen `avocado_v2:MAI_01` speed 110, target pitch >200 Hz (sampel permanen 278,0 Hz). Fitur: Kartu Tokoh Terkunci, Penjaga Konsistensi (verdict LULUS / PERLU PERBAIKAN / BELUM CUKUP DATA), Pembuat Baris Dialog 17–25 kata + TTS + cek pitch energy-gated, Log Penjagaan (`data/log-penjagaan-oyen.json`).
- **Agent 12 Momo** (folder `agent-12-momo/`, modul Pusat Komando `agents/a12_momo.py`, aset di `agents/momo/`): hanya mengurus Momo — wajah `momo-avatar.jpg` + suara permanen `avocado_v2:MAI_03` speed 100, target pitch <200 Hz (sampel permanen 153,3 Hz). Fitur sama seperti Agent 11; log di `data/log-penjagaan-momo.json`.
- **Pusat Komando kini 11 agent bernomor + workshop Avatar Podcast (12 tab)**: tab baru "11 · Oyen" dan "12 · Momo"; tab "11 · Avatar Podcast" yang lama diubah menjadi tab tanpa nomor "Avatar Podcast" (workshop bersama, tetap ada). NAMA_AGENT diperbarui (11: Oyen, 12: Momo); header/footer jumlah agent diperbarui.
- **SOP Kerja Sama Agent AI kini v1.3** (18 Nov 2026): tabel peran agent + daftar folder + riwayat versi ditambah Agent 11 dan 12.
- **Suara dan wajah TIDAK BOLEH diubah** tanpa perintah eksplisit Cipta — tidak ada kontrol UI untuk itu di kedua agent baru. Semua output adalah DRAF untuk persetujuan Cipta.
