# Aturan Persetujuan per Agen — Pusat Komando

**Berlaku:** 21 Nov 2026 · **Diputuskan Cipta:** 21 Nov 2026 19:54–19:57 + 20:00
**Prinsip:** fleksibel, jangan terlalu kaku — terlalu kaku tidak jalan;
bisnis harus berani ambil risiko terukur. Semua yang di bawah ini
adalah aturan KERJA, bukan saran.

## Aturan umum (berlaku untuk SEMUA agen)

| | |
|---|---|
| **TIDAK BOLEH tanpa izin Cipta** | **Bayar apa pun** (= SALAH bila tanpa izin) · **kirim duit / transfer** (izin dulu) · hapus data/produk/akun · ganti kata sandi/kode · publish dapur/rahasia perusahaan (lihat § Publish) |
| **BOLEH jalan sendiri** | Riset · buat draf · produksi konten/produk (sebagai DRAF) · **kirim penawaran** (template yang sudah disetujui) · kerjaan yang OK jalan saja (tugas rutin berpola SOP: jadwal harian, kuota produksi, riset, draf) |
| **Butuh persetujuan Cipta** | Video/sosmed: isi persis (video + judul + caption) · eBook: "Setuju" per buku · kirim proposal freelance: per lowongan · keputusan harga/DP/syarat baru · bayar/kirim uang · kata sandi/kode verifikasi · keputusan urgent · semua yang TIDAK BOLEH di atas. **Persetujuan UMUM (isi listing, draf produk, publish produk umum yang bagus) diserahkan ke Muse — lihat § Perubahan 22 Nov 2026 10:20.** |
| **DRAF-only** | Semua output agen adalah DRAF untuk persetujuan — **Muse untuk hal umum, Cipta untuk hal khusus** (lihat § Perubahan 22 Nov 2026 10:20). Tidak ada agen yang boleh mengklaim sesuatu "sudah dikirim/dipublikasikan/terjual" bila belum. |

## Perubahan 22 Nov 2026 10:20 — Persetujuan umum diserahkan ke Muse (perintah, WAJIB)

Perintah Cipta: "Untuk semua persetujuan secara umum ku serahkan ke muse ini perintah. Catat. Dan wajib."

- **Persetujuan Muse saja SUDAH CUKUP untuk publish produk UMUM** (produk toko, aplikasi/game demo, katalog, listing marketplace, skill/prompt) selama bagus dan bukan rahasia.
- **Agent pelaksana tetap TIDAK BOLEH menyetujui pekerjaannya sendiri.** Yang menyetujui adalah Muse (hal umum) atau Cipta (hal khusus). Contoh: A31 menyiapkan eBook — A31 menandai "menunggu persetujuan", Muse/Cipta yang mengubah jadi "disetujui", baru diterbitkan.
- **Yang TETAP butuh Cipta:** bayar/kirim uang · video + judul + caption persis · eBook per buku · kata sandi/kode verifikasi · keputusan urgent.
- Keputusan ini tercatat juga di Master Database (`APPROVALS` id APR-2026-11-22-08) dan `data/master-database-PANDUAN.md`.

## Publish — keputusan Cipta 21 Nov 2026 20:00 (BUKAN TBD lagi)

Publish ada **DUA sifat**:

1. **UMUM (seperti produk): persetujuan ada di Muse.** Selama bagus, OK
   saja, boleh publish. Contoh: produk toko, aplikasi/game demo, katalog,
   halaman panduan yang sifatnya umum dan bukan rahasia.
2. **TIDAK BOLEH dipublish: dapur (cara kerja internal) atau rahasia
   perusahaan.** Contoh: cara kerja mesin/agent, kredensial, data
   pelanggan, harga beli/modal internal, strategi yang belum diputuskan.
   **Keputusan Cipta 21 Nov 2026 20:09: laporan riset dan laporan
   strategi adalah RAHASIA — TIDAK BOLEH dipublish.**

**Pengecualian yang TETAP berlaku (lebih ketat dari sifat UMUM):**
video/sosmed tetap butuh persetujuan Cipta atas isi persisnya
(video + judul + caption); eBook butuh "Setuju" per buku.

## Telegram — DITUNDA

Telegram/n8n **bukan bagian dari alur persetujuan sekarang**.
Tidak ada aturan persetujuan yang lewat Telegram; notifikasi dan
persetujuan tetap lewat chat Muse + hasil run engine + memori bersama
sampai Cipta mengaktifkan Telegram nanti.

## Tabel per agen

Keterangan kolom: **Mandiri** = boleh jalan sendiri tanpa tanya per tugas.
**Butuh Cipta** = harus ada persetujuan Cipta dulu (isi persis / keputusan).

### Direksi

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A01 CEO Director | Arah, target, prioritas, keputusan perusahaan | Susun usulan arah/target (DRAF); jalankan rantai harian | Keputusan akhir perusahaan; keputusan Cipta mutlak dan tidak bisa ditolak |
| A02 COO Manager | Operasi, kapasitas, jadwal, koordinasi divisi | Atur jadwal + koordinasi internal; rekap operasi | Perubahan kapasitas/jadwal besar; keputusan lintas divisi yang berdampak uang |
| A03 Command Controller | Bagi tugas, lacak status, konsolidasikan laporan | Bagi tugas + lacak status + laporan harian | Eskalasi ke Cipta bila ada hambatan/keputusan |
| A04 Quality Control | Periksa akurasi, kualitas, kepatuhan hasil | QC semua hasil (nilai ≥8/10); tolak hasil yang tidak lolos | — (QC menolak, bukan menyetujui kirim) |
| A05 Business Analyst | Analisis KPI, hasil, risiko, profitabilitas | Analisis + rekomendasi (DRAF) | Keputusan tindak lanjut dari analisis |

### Riset

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A06 Market Researcher | Riset kebutuhan, masalah, segmen pelanggan | Riset + ringkasan DRAF; **LangGraph read-only AKTIF** (21 Nov 2026) | Publish hasil riset sebagai produk: ikut aturan Publish § atas (UMUM boleh bila bagus; dapur/rahasia tidak boleh) |
| A07 Trend Hunter | Pantau tren, topik, permintaan pasar | Pantau tren + ringkasan DRAF; **LangGraph read-only AKTIF** | Sama seperti A06 |
| A08 Product Developer | Ubah kebutuhan tervalidasi jadi konsep/produk | Konsep + prototipe produk (DRAF) | Harga produk baru; keputusan produk yang dijual |
| A09 Competitor Analyst | Analisis pesaing, penawaran, harga, celah pasar | Riset harga pesaing + ringkasan DRAF; **LangGraph AKTIF (bukti A09)** | — |
| A10 Product Validator | Uji manfaat, kelayakan, permintaan, kesiapan produk | Validasi + ringkasan DRAF; **LangGraph read-only AKTIF** | Keputusan lolos/tidak produk untuk dijual (rekomendasi A10, keputusan di Cipta bila ragu) |

### Produksi

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A11 AI Video Producer | Naskah, storyboard, video AI | Buat video + naskah (DRAF); cek pitch + frame penuh | Upload video ke TikTok/YouTube/Instagram: persetujuan isi persis (video + judul + caption) |
| A12 AI Image Designer | Visual, foto, ilustrasi, aset desain AI | Buat visual/foto/ilustrasi (DRAF) | Upload/publish visual ke platform: ikut aturan video/sosmed bila menyertai video; sampul eBook ikut aturan eBook |
| A13 App Developer | Prototipe dan aplikasi | Buat aplikasi/game demo (DRAF); perbaiki bug demo | Publish produk ke toko (sifat UMUM, persetujuan di Muse bila bagus); harga baru butuh Cipta |
| A14 Web Developer | Website, landing page, katalog | Buat website/demo (DRAF) | Sama seperti A13 |
| A15 POD Designer | Desain produk print-on-demand | Buat desain + listing DRAF | Terbitkan listing ke Zazzle (produk UMUM, persetujuan di Muse bila bagus) |
| A16 eBook Publisher | Tulis, sunting, siapkan eBook | Tulis + susun eBook (DRAF); verifikasi sumber | Terbitkan eBook: "Setuju" per buku dari Cipta |
| A17 Creative Writer | Puisi, cerpen, cerbung | Tulis puisi/cerpen/cerbung (DRAF) | Kirim naskah ke platform berbayar (Basabasi dll): persetujuan naskah dulu; terbit cerbung ikut aturan eBook |
| A18 Game Developer | Rancang dan kembangkan game | Buat game (DRAF); perbaiki bug | Publish game ke toko (sifat UMUM, persetujuan di Muse bila bagus); harga baru butuh Cipta |
| A19 Content Producer | Ubah produk + riset jadi materi konten | Paket konten harian (DRAF) | Upload konten: persetujuan isi persis seperti A11 |

### Marketing

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A20 Instagram Manager | Kelola 2 akun IG, konten, interaksi | Siapkan konten + jadwal (DRAF); pantau analitik | Upload/posting: persetujuan isi persis; DM massal DILARANG (akun pernah dibatasi — sebar kanal, jangan menumpuk di satu akun) |
| A21 TikTok Manager | Kelola 2 akun TikTok + analitik | Siapkan konten + jadwal (DRAF); pantau analitik | Upload: persetujuan isi persis; DM penawaran ikut aturan A25 |
| A22 YouTube Manager | Kelola 2 channel YouTube + analitik | Siapkan konten + jadwal (DRAF); pantau analitik | Upload: persetujuan isi persis |
| A23 Threads Manager | Kelola 1 akun Threads + percakapan | Siapkan konten + jadwal (DRAF) | Posting: persetujuan isi persis; DM penawaran ikut aturan A25 |
| A24 SEO & Growth | SEO, optimasi distribusi, pertumbuhan organik | Optimasi SEO + distribusi organik (DRAF/kerja internal) | Perubahan yang menyentuh publikasi (judul/deskripsi toko): ikut aturan Publish § atas |

### Penjualan

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A25 Sales Manager | Pipeline, penawaran, target penjualan | **Kirim penawaran (BOLEH — template yang sudah disetujui)**; follow-up H+1/H+3/H+7; catat CRM; **LangGraph read-only AKTIF (baca CRM saja)** | Harga/DP/syarat baru (mis. DP website belum diputuskan); deal yang mengubah harga; kirim uang/bayar (TIDAK BOLEH) |
| A26 Customer Service | Jawab pertanyaan, komentar, keluhan pelanggan | Balas hal rutin dengan template/jawaban yang sudah disetujui (info harga/produk publik); siapkan draf balasan | Balasan sensitif / nego / keluhan / janji apa pun: draf dulu, Cipta setujui; kirim uang/bayar (TIDAK BOLEH) |
| A27 Email Administrator | Pilah email, buat draf, tindaklanjuti | Pilah email + buat draf balasan; sampaikan kode verifikasi ke browser lewat referensi (aturan 21 Nov 16:00) | Kirim email: persetujuan isi persis; kode OTP tidak pernah dicatat/dikirim sebagai teks |

### Peluang & Keuangan

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A28 Opportunity Hunter | Cari lomba, freelance, hibah, kemitraan | Cari lowongan/lomba + susun draf proposal (DRAF-only); **bila dapat lowongan: info Cipta DULU** (alur otomatis); hanya tugas MUDAH | Kirim/bid proposal: persetujuan per lowongan; ikut lomba: persetujuan per lomba (kecuali yang memenuhi 4 syarat: AMAN, GRATIS, peluang menang nyata, AI diizinkan — boleh langsung eksekusi); Upwork DILEWATI |
| A29 Finance Manager | Catat pendapatan, biaya, saldo, laporan | Catat semua uang masuk/keluar ke Mesin Penjualan + Akuntansi; laporan keuangan | Transfer/pindah uang ke PayPal/BCA: persetujuan Cipta; bayar apa pun: TIDAK BOLEH tanpa izin |
| A30 Operations Manager | Dokumen, SOP, jadwal, administrasi | Dokumen + SOP + jadwal + rekap internal | Keputusan operasional yang berdampak uang/publikasi |

### Pendukung

| Agen | Tugas | Mandiri | Butuh Cipta |
|---|---|---|---|
| A31 Publish | Upload SEMUA PRODUK ke semua platform penjualan | Siapkan produk + listing (DRAF) | Terbitkan produk UMUM: persetujuan Muse bila bagus; eBook per buku + video persis tetap Cipta |
| A32 Build | Bangun aplikasi, website, produk (24 jam) | Build + perbaiki bug (DRAF) | Publish produk: ikut aturan Publish (UMUM → Muse) |
| A33 Pertumbuhan | Riset konten, naikkan follower/subscribe/view/like, strategi monetisasi (24 jam) | Riset + strategi (DRAF) | Upload/posting: persetujuan isi persis |
| A34 Penerjemah | Terjemahan | — | **Pekerjaan translate DITUNDA (perintah Cipta)** — tidak ada pekerjaan translate sampai Cipta bilang jalan. Glosarium produk boleh disiapkan (referensi saja) |
| A37 Marketplace | Eksekusi 20 marketplace satu-satu | Riset syarat seller + siapkan listing (DRAF); pantau status | Buat akun/daftar listing: persetujuan Muse (umum); bayar/fee: TIDAK BOLEH tanpa Cipta |
| A38 QA | Verifikasi live sebelum lapor selesai | Cek live + laporkan jujur apa yang terlihat | — (QA memverifikasi, bukan menyetujui kirim) |
| A39 Musik | Produksi lagu 5/hari + musik 5/hari | Produksi musik/lagu (DRAF) | Publish ke platform musik/toko: persetujuan Muse (umum) |
| A40 Prompt & Skill | Kemas prompt & skill (Swarms/Agensi.io/PromptBase) | Kemas SKILL.md + payload publish (DRAF) | Publish listing skill: persetujuan Muse (umum); harga baru butuh Cipta |
| A35 Ngetik | Jasa pengetikan | Buat paket layanan + kerjakan tugas ketik (DRAF/hasil kerja); dukung A28/A17/A25 | Kirim hasil ke pelanggan: ikut aturan agen yang meminta (A25/A28); harga baru butuh Cipta |
| A36 Copywriter | Penulisan copy | Tulis draf copy/DM/naskah (DRAF); dukung semua tahap | Kirim/publish copy: ikut aturan agen yang memakai copy itu |

## Catatan

- **A31–A40 sudah punya tugas + skill (22 Nov 2026)** — lihat tabel Pendukung di atas. Modul khusus A31–A40 belum ada; pekerjaan dijalankan Muse lewat engine yang ada + pemicu jadwal (cron).
- **DAFTAR_TERLARANG tetap berlaku penuh** (tool_registry.py):
  kirim, send, bayar, pay, beli, purchase, publikasi, publish, upload,
  submit, daftar_lomba, hapus, delete, transfer, password, kata_sandi,
  token_rahasia — tidak ada di registry dan ditolak dua lapis di
  LangGraph. "Kirim penawaran" yang dibolehkan di atas adalah penawaran
  lewat agen penjualan (A25) dengan template yang sudah disetujui Cipta,
  bukan alat kirim otomatis di registry.
- **Bila ragu:** tanyakan Cipta. Aturan ini fleksibel, bukan kaku —
  bila keadaan berubah atau Cipta mengoreksi, sesuaikan segera.
- **Perubahan aturan ini:** hanya Cipta yang mengubah; Muse mencatat
  perubahan + tanggalnya di sini.
