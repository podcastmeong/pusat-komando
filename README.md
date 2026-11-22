---
title: Pusat Komando Podcast Meong
emoji: 🐱
colorFrom: orange
colorTo: yellow
sdk: gradio
sdk_version: 6.32.0
app_file: app.py
pinned: false
---

# Pusat Komando Podcast Meong — v2.0

**Versi 2.0** (21 Nov 2026). v1 = sistem 14 agent bernomor. v2.0 = **30 Agent
Bintang** (A01–A30) + **Mesin Eksekusi** + **Dashboard Agent** dalam **SATU Space
Gradio**, berbagi satu folder `data/` — supaya output satu agent langsung bisa
dipakai agent lain lewat **Papan Handoff**, tanpa antre lewat Muse. Dibangun
atas keputusan Cipta 18 Nov 2026 (Opsi A — "Pusat Komando").

14 agent lama (a01–a14) kini **pasif non-job**: modul + data tetap utuh sebagai
mesin (engine/pustaka) yang dipakai 30 Agent Bintang; tab UI mereka dihapus.

| Tab | Isi |
|---|---|
| 0 · Command Center | CEO Agent (Muse) + 8 direktorat + Approval Center (pemetaan 3.0) |
| B · 30 Agent | 30 Agent Bintang A01–A30 + job description + contoh draf |
| C · Dashboard Agent | Pergerakan agent, antrean kerja, pekerjaan terkendala, target 30 hari Gemini, platform per agent, tombol Jalankan Mesin Eksekusi |
| 🏠 Papan Handoff | Antrean kerja bersama + ringkasan lintas agent |
| 🔄 Koordinasi | Message bus antar-agent (`data/koordinasi.json`) |

## Cara kerja Papan Handoff

Papan membaca folder `data/` bersama dan menampilkan: brief riset yang layak
(Agent 10), draf produksi terbaru (folder `output/`), lead penjualan,
tenggat lomba ≤ 14 hari, uang masuk, progres terjemah, dan proyek game.

Antrean handoff memakai **skema yang sama dengan template SOP**
(`data/handoff-templates/`, dari `sop-agent/handoff/`):
`id · jenis · dari_agent · ke_agent · ringkasan · isi · status`
dengan status `draf → diperiksa → disetujui / ditolak → selesai`.
Keputusan akhir selalu di tangan Cipta.

Aksi cepat di Papan:
- **Kirim Brief → Agent 5**: brief riset berverdict "Layak dicoba" dari
  Agent 10 menjadi item `product-brief` untuk Agent 5.
- **Kirim Draf → Agent 2 / Agent 8**: draf dari folder `output/` menjadi
  item `draft-approval` untuk Penjualan atau Terjemah.

## Aturan yang berlaku (SOP Kerja Sama Agent AI, berlaku 18 Nov 2026)

- Semua output agent adalah **DRAF** untuk persetujuan Cipta.
- **Tidak ada** yang otomatis upload / kirim / transfer / bayar.
- Dilarang mengarang data pasar, ayat, hadis, atau angka; bila data kurang,
  tulis **"belum cukup data"**. Tidak ada janji penghasilan.
- Fokus **gratis dulu** — tanpa layanan berbayar.

## Jalankan lokal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Opsional (AI penuh): export GEMINI_API_KEY="kunci-gratis-dari-aistudio"
# Tanpa key, semua agent jalan mode template lokal.
python app.py
# Buka http://127.0.0.1:7860
```

Catatan VM: `pip install` butuh variabel proxy lingkungan; `import gradio`
GAGAL bila variabel proxy aktif (bug httpx dengan entri IPv6 di `NO_PROXY`) —
jalankan server dengan semua variabel proxy dikosongkan. Di Hugging Face
Spaces masalah ini tidak ada.

## Deploy ke Hugging Face Spaces (1 Space saja)

1. Buat akun Hugging Face (gratis) di https://huggingface.co/join
2. Buat Space baru: SDK **Gradio**, Hardware **ZeroGPU** (akun gratis:
   maks 2 Space Gradio di ZeroGPU; bila pembuatan meminta PRO, pilih ZeroGPU).
3. Unggah isi folder ini (`app.py`, `requirements.txt`, folder `agents/`,
   folder `data/`). Jangan unggah `.venv`.
4. Di Settings → Variables and secrets, tambahkan Secret
   `GEMINI_API_KEY` = API key gratis dari https://aistudio.google.com/apikey
   (opsional — tanpa key, mode template tetap jalan).
5. Space akan build otomatis; buka tautannya saat status Running.

## Batasan gratis (jujur)

- Space gratis **tidur** bila lama tidak dipakai dan bangun lagi saat dibuka.
- Data di folder `data/` (termasuk `handoff.json`) **hilang bila Space
  di-rebuild** — unduh berkala lewat Files di halaman Space.
- Gemini free tier ada kuota harian; bila habis, agent jatuh ke mode template.
- Mode AI belum teruji end-to-end tanpa key (kode memanggil Gemini dengan
  fallback template bila gagal).
- Agent 2 aslinya layanan FastAPI (Oracle); di sini hanya fungsi intinya yang
  dipakai lewat tab Gradio — endpoint API FastAPI-nya tidak ikut.

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

## Pembaruan 20 Nov 2026 — Agent 4 Penjualan Harian

- **Agent 4 diaktifkan kembali** atas perintah Cipta ("Exsekusi / Buatkan"),
  mengisi slot Agent 4 yang dulu dihapus. Total agent menjadi **13
  (slot 1–13 penuh) + Muse = 14**. Modul: `agents/a04_penjualan_harian.py`,
  data: `data/penjualan_toko.json` (log awal: 10 pet shop Jakarta Selatan,
  sudah ada draf, BELUM ada yang dikirim).
- **Tugas:** penjualan harian ke toko-toko (alur kerja 4 Cipta) — cari
  minimal 15 toko/hari (nomor HP dari Google Maps), verifikasi nomor, buat
  draf penawaran personal dari katalog baru, catat hasil + follow-up.
- **Dibantu Agent 2 untuk memasarkan:** draf memakai generator promosi
  Agent 2 (WA outreach/follow-up, DM IG, email, caption); toko terverifikasi
  Agent 4 masuk sebagai lead Agent 2 (`leads.json`); lead baru Agent 2
  bisa diambil Agent 4 untuk penawaran harian.
- **Aturan keras:** agent TIDAK PERNAH mengirim pesan — Cipta menyetujui
  draf persisnya dulu, lalu mengirim sendiri dari WA-nya.
- **Deploy:** kode baru ini ada di folder lokal Pusat Komando. Cara Faable
  mengambil update TIDAK tercatat di repo ini — sinkronisasi ulang ke
  Faable (dashboard Faable / GitHub App) masih perlu dilakukan manual;
  JANGAN anggap sudah live di Faable sebelum dicek di
  https://pusat-komando-972u7.faable.link/.

## Pembaruan 19 Nov 2026 — Sistem Koordinasi Antar-Agent

- **Tab baru "🔄 Koordinasi" (tab ke-2, setelah Papan Handoff):** message bus
  antar-agent di `data/koordinasi.json` — pesan berstatus baru → dibaca →
  dikerjakan → selesai/ditolak, inbox/outbox per agent, log aktivitas.
- **Aturan rute otomatis R1–R13:** brief layak 10→5; draf baru 5→2+8; tenggat
  lomba ≤7 hari 6→5; payout 7→Muse; email penting 13→agent terkait;
  verdict PERLU PERBAIKAN 11/12→5; game selesai 9→2+7; terjemah selesai
  8→2; spesifikasi selesai 9A→9B; uji lolos 9B→9C; siap jual 9C→2;
  ringkasan siklus → Muse; pesan mendesak dieskalasi otomatis ke Muse.
  Duplikat dicegah (kunci dedupe + cek handoff yang sudah ada).
- **Siklus Harian:** satu tombol memeriksa data bersama sesuai urutan
  ketergantungan (riset → produksi → penjualan/terjemah → lomba/keuangan →
  email → penjaga → game → terjemah), mode template, tanpa panggilan
  eksternal. Siklus tidak membuat handoff otomatis dan tidak mengirim/
  mengunggah apa pun.
- **Pusat Komando kini 18 tab** (12 agent bernomor + 3 tim Agent 9
  (9A Rancang, 9B Bangun, 9C Jualan) + workshop Avatar Podcast
  + Koordinasi). Detail: `LAPORAN-KOORDINASI.md`. Uji: unit test 76/76
  (47 area warisan dibuat ulang — file `/tmp` hilang — + 29 baru R11–R13
  & tim 9A/9B/9C), `build_app()` memuat 18/18 tab (cek config; uji
  headless + server HTTP belum diulang setelah penambahan tim).
- **Batasan jujur:** agent tetap aplikasi pasif — bus bukan obrolan live;
  rantai komando tetap Cipta → Muse → agent; butuh Space/VM live untuk
  pemakaian nyata.

## Pembaruan 21 Nov 2026 — Pusat Komando v2.0

- **30 Agent Bintang A01–A30** (tab B): job description dari Share ChatGPT
  #18/#19 + Share Gemini #1, dipetakan ke 14 mesin lama + Muse + Pusat
  Komando. Strategi SESUAI ChatGPT + Gemini: jadwal harian alur Gemini #1
  (06:00 riset, 08:00 produksi, 11/15/19 distribusi, CS sepanjang hari,
  21:00 audit) dalam bingkai 06:00–21:00 ChatGPT #18; KPI gemini_kpi;
  target 30 hari Gemini (15 produk, 30 konten, 1000 followers baru,
  5–10 lomba, Rp500rb–Rp2jt) sebagai tolok ukur Dashboard.
- **Mesin Eksekusi** (`agents/mesin_eksekusi.py`, CLI
  `python -m agents.mesin_eksekusi`): menjalankan fungsi kerja NYATA tiap
  agent Bintang sesuai job description-nya (bukan sekadar contoh()) dengan
  argumen dari tugas antrean; bila argumen tidak cukup, memanggil contoh()
  dan mencatat mode="contoh". Semua output DRAF; tidak pernah kirim/bayar/
  publikasi/submit/upload. Jalan hanya saat dipicu (tombol/CLI).
- **14 agent lama (a01–a14) menjadi PASIF NON-JOB** (pekerjaan dicabut atas
  perintah Cipta 21 Nov 2026): modul + data tetap utuh sebagai mesin yang
  dipakai 30 Bintang; 21 tab UI lama dihapus; aplikasi kini **5 tab**
  (0 Command Center, B 30 Agent, C Dashboard Agent, Papan Handoff,
  Koordinasi). Dashboard menampilkan hitungan utama 30 Bintang + 14 mesin
  pasif terpisah (bukan 44 agent). KOREKSI 22 Nov 2026: no 1–10 sudah jadi A31–A40; no 11–14 DIGANTI agen pintar (Oyen Pintar, Momo Pintar, A27-pintar, A28-Upwork-pintar) — hitungan roster tetap 40 agent (A01–A40), bukan 44.
- **Kendala harus diinfokan:** pekerjaan yang tidak bisa jalan (platform
  belum terhubung, data tidak ada, butuh login/keputusan Cipta, error)
  berstatus "terkendala" di antrean + audit log, lengkap dengan penyebab
  dan apa yang dibutuhkan dari Cipta — tampil terpisah di Dashboard.
- **Pemetaan platform** (`data/agents.json`, key "platform" per agent):
  21 platform terhubung + 6 belum terhubung dipetakan ke agent Bintang
  yang job description-nya mencakup platform itu; tampil di Dashboard.
- **Konflik ChatGPT vs Gemini yang dicatat** (diutamakan yang tercatat di
  agents.json): (1) jadwal rinci 12 baris ChatGPT #18 tidak tercatat di
  agents.json — dipakai 5 slot Gemini; (2) KPI ChatGPT per-agent tidak
  tercatat — dipakai gemini_kpi; (3) Gemini bilang "6 divisi" padahal
  isinya 5 divisi + Agent 0 — dipakai yang nyata.
- **Batasan jujur:** mesin hanya menjalankan draf; distribusi (posting/
  upload/kirim) tetap butuh persetujuan Cipta atas isi persisnya; jendela
  30 hari belum punya tanggal mulai tercatat sehingga realisasi target
  ditampilkan sebagai total tercatat, bukan hitungan dalam jendela.
