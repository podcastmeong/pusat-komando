# Skill: Cek Konsistensi Toko (untuk A42 Penanggung Jawab Toko Digicat + A32 Build, diverifikasi A38 QA)

> Perintah Cipta 23 Nov 2026 — Masalah: 162 dari 196 produk tautan belinya masih Gmail (bukan platform), 6 game belum ada harga, URL Rindu beda antara data toko dan yang live, detail 11 eBook sempat tampil Inggris. Data toko dan platform bisa melenceng diam-diam. Skill ini adalah rutinitas cek silang toko vs platform — supaya yang dipasarkan cocok dengan yang dijual.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A42 Penanggung Jawab Toko Digicat** | Menjaga 1 harga per produk, data toko cocok dengan platform; menjalankan cek ini rutin |
| Pengerjaan | **A32 Build** | Memperbaiki data toko di repo bila cek menemukan selisih |
| Pengawasan | **A38 QA** | Verifikasi live dari sisi Cipta (buka toko di browser, klik tautan beli, bandingkan harga) sebelum laporan "selesai" |

## Aturan keras

1. **Repo adalah SATU-SATUNYA sumber toko** (`podcastmeong/digistore-ai`, file `index.html`). Artifact toko STALE (187 produk) — JANGAN PERNAH export artifact menimpa repo.
2. **Jangan ubah harga tanpa persetujuan.** Harga sudah disetujui Cipta (aplikasi $29/$59/$99 + APK $25; game $2,99/$4,99/$5,99; eBook $4,99; bundle 3 $11,99 / 9 $24,99; video promo $19/$39/$69). A42 menjaga, bukan mengubah.
3. **Satu selisih = CACAT** untuk produk itu: tautan beli salah, harga kosong/salah, demo mati, deskripsi beda bahasa. Produk cacat TIDAK BOLEH dilaporkan "live benar" — perbaiki dulu, cek ulang, baru lapor.
4. **Alamat toko stabil:** https://digistore-ai.pages.dev/ — tanpa `?v=` selamanya (poin 33). Tautan `?v=` lama tetap hidup (200) tapi jangan pernah dikirim lagi.

## Rutinitas cek (harian, sebelum jam kerja)

Jalankan di repo lokal `~/workspace/digistore-ai/` (pastikan `git pull` dulu):

### 1. Hitung produk + tautan beli
- Ekstrak array `PRODUCTS` dari `index.html` (JSON satu baris — parse dengan penghitung kurung).
- Hitung: total produk per ruangan; tautan beli Gmail vs platform (Zazzle/Payhip/Gumroad/KaryaKarsa/Fiverr/Swarms).
- Target: 0 tautan Gmail untuk produk yang SUDAH live di platform. Tautan Gmail hanya boleh untuk produk yang memang belum ada di platform — dan itu harus tercatat, bukan dibiarkan.

### 2. Harga lengkap
- Semua produk HARUS punya harga. Daftar produk tanpa harga (saat ini 6 game: oyen-lari, kuis-cerita-nabi, memori-kartu-oyen, oyen-tangkap-ikan-2, tebak-kata-oyen, masak-bersama-momo) = CACAT sampai Cipta menetapkan harganya.

### 3. Tautan beli + demo hidup
- Setiap tautan beli platform dan tautan demo: cek HTTP 200 + judul produk cocok (bukan produk lain, bukan halaman error).
- Contoh nyata: URL Rindu pernah beda antara data toko dan yang live — cek ini yang menangkapnya.

### 4. Bahasa cocok
- Deskripsi + detail produk di toko bahasa Indonesia (`id`); bila masih ada detail Inggris untuk produk Indonesia = CACAT (pelajaran 11 eBook, 23 Nov).

### 5. Jumlah + ruangan cocok
- Jumlah produk di toko = jumlah di data (saat ini 196: aplikasi 132, web 19, pod 14, ebook 12, game 9, prompt 8, video 1, skill 1); 11 ruangan lengkap.

## Perbaikan bila ketemu selisih

1. Perbaiki di repo (bukan artifact) → commit → push → tunggu deploy Cloudflare Pages ~20–30 dtk.
2. Verifikasi live dari sisi Cipta (A38): buka https://digistore-ai.pages.dev/ di browser, cek bagian yang diperbaiki + SEMUA bagian yang disentuh.
3. Catat di `data/log-eksekusi.jsonl` (apa selisihnya, di mana, sudah diperbaiki jam berapa).

## Bukti + lapor

- Laporan cek harian: tanggal, total produk, Gmail vs platform, produk tanpa harga, tautan mati, selisih bahasa — + satu baris `data/log-eksekusi.jsonl`.
- Bila ada produk cacat yang sudah telanjur dipasarkan: laporkan ke Cipta dengan nama produk + cacatnya + perbaikannya — jangan diam-diam diperbaiki tanpa kabar.
