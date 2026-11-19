# LAPORAN — Sistem Koordinasi Antar-Agent (Pusat Komando)

**Tanggal:** 19 Nov 2026 · **Status:** SELESAI + teruji · **Lokasi:**
`~/workspace/your_files/oyen-podcast/pusat-komando/`

## 1. Yang dibangun

### 1.1 Modul baru `agents/koordinasi.py` — message bus antar-agent
- **Pesan** (`dari_agent`, `ke_agent`, `jenis`, `prioritas`, `ringkasan`,
  `isi`, `status`, `sumber`, `kunci`) tersimpan di `data/koordinasi.json`.
  Status: `baru → dibaca → dikerjakan → selesai / ditolak` (transisi
  divalidasi; `selesai`/`ditolak` terminal, tidak bisa diubah lagi).
- **Dedupe:** pesan aturan memakai `kunci` — tidak dibuat duplikat bila
  pesan aktif dengan kunci yang sama sudah ada, dan tidak dibuat bila
  handoff yang sama sudah ada di `handoff.json`.
- **Inbox/outbox per agent** + papan status (jumlah pesan baru/dikerjakan/
  selesai per agent) + log aktivitas (maks 200 entri).
- **Fungsi:** `kirim_pesan`, `ubah_status_pesan`, `daftar_pesan`,
  `inbox`, `outbox`, `ringkasan_status`, `evaluasi_rute`,
  `jalankan_siklus_harian`, `teks_papan`, `tabel_pesan`, `tabel_aturan`,
  `teks_log`. Semua fungsi menerima `data_dir` opsional (dipakai unit test
  agar tidak menyentuh data asli). Tanpa panggilan eksternal, tanpa API key.

### 1.2 Tabel aturan rute otomatis (R1–R13)

| ID | Aturan | Dari → Ke | Jenis | Prioritas | Pemicu |
|----|--------|-----------|-------|-----------|---------|
| R1 | Brief layak → Produksi | 10 → 5 | product-brief | normal | `riset.json` verdict "Layak dicoba", belum ada handoff/pesan untuk ide itu |
| R2 | Draf baru → Penjualan + Terjemah | 5 → 2, 8 | draft-approval | normal | File baru di `output/`, belum ada handoff/pesan untuk file itu |
| R3 | Tenggat lomba ≤7 hari → Produksi | 6 → 5 | contest-entry | tinggi | `lomba.json`: tenggat 0–7 hari, status baru/dicek, AI "diizinkan" |
| R4 | Payout jatuh tempo → Muse | 7 → Muse | finance-entry | tinggi | `keuangan_data.json`: pengingat payout ≤7 hari / pemasukan "menunggu" |
| R5 | Email penting → agent terkait | 13 → terkait | pemberitahuan | tinggi | Log Agent 13: email prioritas Tinggi. Lomba→6, Keuangan→7, Affiliate/Bisnis→2, Promo→3, Penting→Muse |
| R6 | Verdict PERLU PERBAIKAN → Produksi | 11/12 → 5 | permintaan-perbaikan | normal | Log penjagaan Oyen/Momo ada verdict "PERLU PERBAIKAN" |
| R7 | Game/aplikasi selesai → Penjualan + Keuangan | 9 → 2, 7 | pemberitahuan | normal | `game_data.json` proyek status "selesai"/"diterbitkan" |
| R8 | Terjemahan selesai → Penjualan | 8 → 2 | translation-job | normal | `terjemah_progress.json` ada buku/bagian "selesai" |
| R9 | Ringkasan siklus → Muse | Sistem → Muse | laporan-harian | normal | Setiap Siklus Harian selesai |
| R10 | Pesan mendesak → eskalasi ke Muse | Sistem → Muse | eskalasi | mendesak | Pesan berprioritas "mendesak" dibuat (salinan otomatis ke Muse) |
| R11 | Spesifikasi selesai → Bangun | 9A → 9B | product-brief | normal | `produksi_game.json` ada proyek status "spesifikasi-selesai", belum ada pesan bus untuk proyek itu |
| R12 | Uji lolos → Jualan | 9B → 9C | draft-approval | normal | `produksi_game.json` ada proyek status "diuji-lolos", belum ada pesan bus untuk proyek itu |
| R13 | Siap jual → Penjualan | 9C → 2 | draft-approval | normal | `produksi_game.json` ada proyek status "siap-jual", belum ada pesan bus untuk proyek itu |

### 1.3 Siklus Harian
Satu kali jalan memeriksa data bersama sesuai urutan ketergantungan:
1. Riset (10) → 2. Produksi (5) → 3. Lomba (6) → 4. Keuangan (7) →
5. Email (13) → 6. Penjaga (11/12) → 7. Game (9) → 8. Terjemah (8),
lalu ringkasan diposting ke Muse (R9). Mode template. Siklus **tidak**
membuat entri `handoff.json` otomatis dan **tidak** mengirim/mengunggah
apa pun — handoff tetap dibuat Muse lewat Papan Handoff setelah diperiksa
(SOP bagian 5).

### 1.4 Tab baru "🔄 Koordinasi" di `app.py`
Tab ke-2 (setelah Papan Handoff). Isi: papan status per agent, tabel pesan
dengan saring (per agent penerima + status), form kirim pesan manual,
ubah status pesan, tabel aturan rute R1–R13, tombol "Jalankan Siklus
Harian" + laporan, log aktivitas. Pusat Komando kini **18 tab**
(12 agent bernomor + 3 tim Agent 9 + workshop Avatar Podcast + Koordinasi). Header/footer
`app.py` diperbarui. 13 tab lama tidak diubah isinya.

### 1.5 File yang diubah/dibuat
- **Baru:** `agents/koordinasi.py` (31 KB), `data/koordinasi.json`
  (dibuat otomatis saat Siklus Harian pertama dijalankan),
  `LAPORAN-KOORDINASI.md` (file ini).
- **Diubah:** `app.py` (tambah tab + pembungkus; 13 tab lama utuh),
  `README.md` (catatan pembaruan di bawah).
- **Tidak diubah:** semua modul agent di `agents/`, `data/handoff.json`,
  SOP v1.3, tugas agent di `daftar-agent-ai.md`.

## 2. Cara pakai
1. Buka Pusat Komando → tab **🔄 Koordinasi**.
2. Klik **"Jalankan Siklus Harian"** — bus memeriksa semua data bersama
   dan memposting pengingat (DRAF) ke agent yang bersangkutan.
3. Buka inbox agent di tabel pesan (saring per agent) → ubah status
   `baru → dibaca → dikerjakan → selesai` saat ditindaklanjuti.
4. Kirim pesan manual bila perlu (mis. Muse meneruskan catatan ke agent).
5. Handoff resmi tetap dibuat lewat tab **🏠 Papan Handoff** setelah Muse
   memeriksa isi pesan — bus tidak menggantikan Papan Handoff.

## 3. Hasil uji
| Uji | Hasil |
|-----|-------|
| `py_compile` `koordinasi.py` + `app.py` | OK |
| Unit test bus + rute (`/tmp/test_koordinasi.py`) | **43/43 lulus, 0 gagal** — kirim/dedupe, transisi status (termasuk penolakan transisi ilegal + status terminal), eskalasi R10, R1–R8 (termasuk idempotensi tiap aturan + kasus "BELUM CUKUP DATA" R4/R7/R8), Siklus Harian end-to-end + idempotensi siklus kedua, ringkasan/inbox/outbox |
| Unit test bus + rute + tim 9A/9B/9C (`pusat-komando/tests/test_koordinasi.py`, 19 Nov 2026) | **76/76 lulus, 0 gagal** — file test lama di `/tmp` hilang (ephemeral), jadi suite dibuat ulang dari deskripsi cakupan di atas: 47 test area warisan + 29 test baru (R11–R13 termasuk idempotensi + pendaftaran aturan, alur pipa 9A→9B→9C termasuk gagal uji, impor modul tim, `build_app()` memuat 18/18 tab, template `game-pipeline.json` valid, standar buku panduan: spesifikasi tanpa panduan ditolak, uji gagal bila panduan tidak lengkap). Semua test memakai data_dir sementara — tidak menyentuh data asli. |
| `build_app()` (tanpa API key) | OK — modul koordinasi termuat (`KOORD loaded: True`) |
| Server Gradio (port 7861) | **HTTP 200** |
| `/config` | Tab "🔄 Koordinasi" ada; 4 API terdaftar (`segarkan_koordinasi`, `kirim_pesan_koordinasi`, `ubah_status_pesan_koordinasi`, `jalankan_siklus_harian`); 689 komponen |
| Uji UI headless (Playwright Chromium) | **15/15 tab ter-mount** (termasuk Koordinasi sebagai tab ke-2); Papan Koordinasi, Aturan Rute, Siklus Harian terlihat; tombol "Jalankan Siklus Harian" diklik lewat UI dan laporan tampil; **0 console error** |
| Siklus pertama di data asli (via UI) | 0 pesan aturan baru (data masih kosong — jujur, bukan dikarang); ringkasan R9 diposting ke Muse sebagai KB-001; `data/koordinasi.json` terbentuk |

**Catatan uji headless:** batasan lama "halaman besar hanya me-mount 9 tab
di Chromium headless VM ini" **tidak terulang** kali ini — 15/15 tab
ter-mount dan terklik. Tetap dicatat sebagai batasan yang pernah terjadi.

**Catatan lingkungan uji:** Gradio tidak terpasang di VM ini, jadi untuk
pengujian dipasang `gradio==6.32.0` + `google-generativeai==0.8.6` +
`google-genai>=1.0` ke venv `~/workspace/audio-tools/python-packages/`,
plus `pandas` dipasang paksa (`--ignore-installed`, karena pip menganggap
pandas sistem 2.1.4 sudah memenuhi syarat padahal binernya tidak cocok
dengan numpy 2.5.4 venv — error `numpy.dtype size changed`). Server
dijalankan dengan semua variabel proxy dikosongkan (sesuai kebiasaan VM
ini). Instalasi ini hanya untuk pengujian lokal; deploy Space/VM memakai
`requirements.txt` seperti biasa.

## 4. BATASAN JUJUR
- **Agent adalah aplikasi pasif — koordinasi berjalan lewat bus + aturan
  + Muse, bukan obrolan otonom antar-agent secara live.** Pesan dibaca
  saat seseorang membuka tab Koordinasi atau menjalankan Siklus Harian.
  Tidak ada agent yang "bangun sendiri" lalu membalas pesan.
- **Bus tidak menggantikan Muse.** Rantai komando tetap Cipta → Muse →
  agent (SOP v1.3). Bus hanya mencatat dan mengingatkan; pemeriksaan mutu
  dan penerusan sebagai handoff resmi tetap dilakukan Muse.
- **Tidak ada aksi keluar otomatis.** Pesan bus tidak pernah mengunggah,
  mengirim, mendaftar lomba, membayar, atau mentransfer. Semua output
  tetap DRAF; keputusan akhir di tangan Cipta.
- **Butuh Space/VM live untuk pemakaian nyata.** Selama Pusat Komando
  belum live (HF ZeroGPU terkunci sampai akun 30 hari — 15 Des 2026; jalur
  Oracle sedang disiapkan), bus hanya bisa dipakai dari server lokal.
- **Data hilang bila Space di-rebuild** (`data/koordinasi.json` sama
  seperti `data/` lainnya) — unduh berkala.
- **Siklus tidak bisa memeriksa isi yang belum ada datanya.** Bila
  `game_data.json`, `terjemah_progress.json`, atau data payout kosong,
  siklus menulis "BELUM CUKUP DATA" — bukan menebak.
- **Aturan rute membaca data bersama, bukan isi tab agent.** Bila sebuah
  agent menyimpan datanya di tempat lain (bukan `data/` bersama), aturan
  yang bersangkutan tidak akan melihatnya.

## 5. TIM 9A/9B/9C DI BAWAH AGENT 9 (19 Nov 2026)

Perintah Cipta: "tambah 3 tim Agent 9" + "langsung hubungkan dengan wadah".

- **9A Rancang** (`agents/a09a_rancang.py`): menulis spesifikasi tiap aplikasi/game
  dari antrean — daftar fitur, data contoh, kriteria demo lolos, dan isi
  buku panduan penggunaan (standar produk: setiap aplikasi berisi buku
  panduan — cara memakai tiap fitur, Bahasa Indonesia).
  Status: antrean → spesifikasi-selesai.
- **9B Bangun** (`agents/a09b_bangun.py`): verifikasi 5 butir (fitur jalan,
  tanpa error, data contoh benar, responsif HP, buku panduan ada dan
  lengkap). Semua lolos → diuji-lolos;
  ada yang gagal → status tetap + catatan perbaikan untuk 9A.
- **9C Jualan** (`agents/a09c_jualan.py`): listing toko (deskripsi, fitur,
  harga "bisa negosiasi", tautan demo) + draf penawaran gaya WA + tandai
  sudah di Toko Aplikasi. Status: diuji-lolos → siap-jual → di-toko.
- Data bersama: `data/produksi_game.json` (17 proyek per 19 Nov 2026 —
  3 aplikasi selesai, 12 antrean, 1 siap-jual, 4 di-toko). Pembantu bersama:
  `agents/a09_pipa.py`. Semua output tim adalah DRAF (SOP v1.3).
- Aturan rute baru: **R11** spesifikasi selesai 9A→9B, **R12** uji lolos
  9B→9C, **R13** siap jual 9C→2 (Penjualan). Ketiganya idempotent
  (kunci dedupe) dan menulis "BELUM CUKUP DATA" bila
  `produksi_game.json` kosong. Siklus Harian langkah 7 kini menjalankan
  R7 + R11–R13.
- Pendaftaran di wadah: 3 tab baru di `app.py` (tepat setelah tab Agent 9),
  `NAMA_AGENT` + dropdown memakai urutan eksplisit `_URUTAN_AGENT`
  (kunci campuran int + str tidak bisa di-`sorted()`), jenis handoff baru
  `game-pipeline` + template `data/handoff-templates/game-pipeline.json`,
  seksi alur produksi di Papan Handoff. Pusat Komando kini **18 tab**.
- Uji: `pusat-komando/tests/test_koordinasi.py` — **76/76 lolos**
  (47 area warisan dibuat ulang + 29 baru, termasuk 2 test standar buku panduan). Verifikasi R11–R13 terhadap
  salinan data asli: R11 0, R12 0, R13 1 (Oyen Tangkap Ikan siap-jual → 9C→2).
  Uji headless + server HTTP belum diulang setelah penambahan tim.
