# Skill: QC eBook Sebelum Dipasarkan (untuk A16 eBook Publisher + A04 Quality Control, diverifikasi A38 QA)

> Perintah Cipta 23 Nov 2026 — PELAJARAN dari produk cacat: eBook Nuh yang dijual di Gumroad + Payhip ternyata isinya cerita Ayub (file 3,1 MB tertukar), dan detail 11 eBook di toko tampil bahasa Inggris padahal pembeli Indonesia. Cacat ketahuan SETELAH produk dipasarkan — Cipta yang menemukan ("Buat ulang. Tarik yang cacat"). Skill ini memastikan: TIDAK ADA eBook yang dipasarkan sebelum isinya diperiksa.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A16 eBook Publisher** | Menulis, menyunting, menyiapkan eBook; WAJIB menjalankan gerbang ini SEBELUM kirim ke Cipta untuk "Setuju" dan SEBELUM terbit di platform mana pun |
| Pengawasan isi | **A04 Quality Control** | Memeriksa hasil gerbang A16; menolak bila ada satu cek gagal |
| Verifikasi live | **A38 QA** | Memeriksa listing live setelah terbit (judul, harga, tautan, file yang diunduh) — dari sisi Cipta, bukan curl saja |

## Aturan keras

1. **TIDAK ADA eBook yang diunggah/didaftar/dijual sebelum gerbang ini LULUS.** "Setuju" Cipta atas naskah BUKAN pengganti gerbang ini — persetujuan isi naskah dan pemeriksaan file jadi adalah dua hal berbeda.
2. **Satu cek gagal = CACAT = TIDAK BOLEH PASAR.** Jangan perbaiki diam-diam lalu loloskan; tulis verdict CACAT + alasannya, perbaiki file, lalu jalankan gerbang dari awal.
3. **QC tidak memeriksa dirinya sendiri.** A16 yang membuat file TIDAK BOLEH meloloskan filenya sendiri — A04 yang memutuskan lolos/tolak.
4. **Cek ISI file, bukan nama file.** Nama file "nabi-nuh.pdf" tidak membuktikan isinya Nuh — yang membuktikan adalah teks di dalamnya.
5. **eBook "Cuan dengan AI" JANGAN PERNAH diterbitkan** sampai cara-cara di dalamnya TERBUKTI menghasilkan uang (aturan lama, tetap berlaku).

## Gerbang pra-pasar (semua wajib LULUS)

Jalankan di file PDF final yang akan diunggah (bukan draf .md):

### 1. Bahasa benar (cek "tertuka r bahasa")
- Ekstrak teks: `pdftotext <file.pdf> - | head` + hitung kata.
- Judul dan isi HARUS bahasa Indonesia. Kata Inggris yang diizinkan HANYA: judul referensi di daftar pustaka, nama platform, dan istilah yang memang tidak ada padanan Indonesianya.
- Bila isi utama berbahasa Inggris atau campur acak = CACAT.

### 2. Cerita benar — tidak tertukar (cek "tertuka r cerita")
- Hitung kemunculan nama tokoh utama: `pdftotext <file.pdf> - | grep -ci "Nuh"` (ganti dengan nama tokoh buku itu).
- Nama tokoh buku ini HARUS dominan (puluhan kali). Nama tokoh buku LAIN (mis. "Ayub" di file Nuh) HARUS 0x — atau bila muncul, hanya sebagai perbandingan singkat, bukan sebagai isi cerita.
- **Contoh nyata (23 Nov 2026):** file Nuh yang benar = "Nuh" 91x, "Ayub" 0x. File cacat yang sempat terjual = isinya Ayub. Bila hitungan terbalik (tokoh lain lebih banyak dari tokoh buku) = CACAT, tarik file itu.
- Cek juga judul di halaman pertama PDF sama dengan judul produk.

### 3. Isi lengkap + valid
- Jumlah halaman sesuai rencana (seri nabi: 20 halaman).
- Ayat Al-Quran + hadis sudah dicek ke sumber sahih (aturan lama penerbitan-ebook poin 4).
- Tidak ada halaman kosong, teks terpotong, atau gambar rusak.

### 4. Data toko + platform cocok dengan file
- Judul produk, harga, dan deskripsi di toko (index.html, objek `id`) sama dengan file — bahasa Indonesia.
- Tautan beli mengarah ke produk yang benar di platform (bukan produk buku lain).
- Setelah diunggah: unduh file dari platform, ulangi cek 1–2 pada file yang diunduh (bukan file lokal) — yang dijual adalah file di platform, bukan file di laptop.

## Alat

- `pdftotext <file.pdf> -` — ekstrak teks PDF (sudah terpasang di /usr/bin/pdftotext).
- `pdftotext <file.pdf> - | grep -ci "NamaTokoh"` — hitung kemunculan nama tokoh.
- `pdftotext <file.pdf> - | grep -ci "Ayub\|Yunus\|Yusuf\|Musa\|Ibrahim"` — deteksi nama buku lain (sesuaikan daftarnya).

## Format verdict (tulis ke `data/log-eksekusi.jsonl` + `~/workspace/catatan/keputusan.md`)

```
QC eBook <Judul> — <tanggal jam>: Bahasa <LULUS/CACAT: ...>; Cerita <LULUS/CACAT: <Tokoh> Nx, tokoh lain 0x>; Lengkap <...>; Data toko <...>. STATUS: LULUS (boleh pasar) / CACAT (<alasan> — tarik/perbaiki).
```

## Bukti + lapor

- Setiap eBook yang lolos gerbang: satu baris `data/log-eksekusi.jsonl` (ts, agent A16/A04, task, status, bukti = angka hitungan tokoh + halaman).
- Setiap CACAT: tulis juga ke `~/workspace/catatan/keputusan.md` di hari yang sama (apa cacatnya, di mana ketahuan, apa perbaikannya) — supaya tidak terulang.
