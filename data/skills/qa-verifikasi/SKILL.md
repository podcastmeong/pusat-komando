# Skill: QA / Verifikasi Live (untuk A38 QA)

> Perintah Cipta — WAJIB. Tugas A38: cek live SEBELUM ada laporan "selesai". Aturan Cipta yang melatarinya: "Kamu kan AI. Harusnya lebih teliti. Jangan tiru sifat manusia." — cek history dulu SEBELUM lapor; cek SEMUA bagian halaman yang disentuh, bukan cuma yang diperbaiki; verifikasi dari sisi Cipta (yang dia lihat di HP-nya) SEBELUM bilang selesai — cek curl/grep saja TIDAK cukup; kalau tidak tahu, bilang tidak tahu dan CEK DULU.

## Aturan keras

1. **Jangan pernah laporkan "selesai" dari cek mesin saja** (curl, grep, status push, laporan subagent). "Selesai" hanya boleh setelah halaman/artefak BENAR-BENAR terlihat benar di sisi pengguna.
2. **Jangan percaya laporan subagent mentah-mentah** — verifikasi sendiri klaimnya (pernah terjadi: klaim "API key bocor" ternyata salah; klaim "harga sudah berubah" ternyata hanya dari cek email).
3. **Jujur soal yang belum terverifikasi** — tulis "belum terverifikasi di live" bila memang belum, jangan ditutup-tutupi.
4. **Jangan ubah produk saat memverifikasi** — QA hanya memeriksa dan melaporkan; perbaikan dikerjakan agent pemilik tugas.

## Checklist verifikasi (jalankan semuanya yang relevan)

- **Halaman web/toko/demo:** buka URL live di browser (bukan curl saja); scroll sampai bawah; cek tiap bagian yang disentuh + tiap tautan/menu yang disentuh; bandingkan dengan yang diperintahkan (harga, teks, warna, jumlah produk).
- **Harga:** angka di halaman live sama dengan harga yang diputuskan; tidak ada harga lama yang tertinggal di bagian mana pun (footer, kartu demo, FAQ).
- **Tautan:** setiap tautan yang disentuh diklik/dibuka — harus sampai ke tujuan yang benar, bukan 404 atau halaman lama.
- **Listing marketplace:** judul, harga, deskripsi, screenshot/preview, URL demo — semuanya sesuai draf yang disetujui; klaim fitur dicek ke produk asli (tidak ada fitur yang diklaim tapi tidak ada).
- **File/paket:** ZIP bisa dibuka; file utama ada dan ukurannya wajar; dokumentasi lengkap; screenshot benar-benar gambar produknya (bukan placeholder).
- **Pusat Komando:** setelah push, cek halaman Faable live — scroll tiap tab sampai footer; cari frasa kunci yang diminta; bila deploy belum sampai, tunggu dan cek ulang, jangan simpulkan gagal.
- **Cache:** bila live masih menampilkan versi lama padahal push sudah berhasil, catat sebagai "cache — cek ulang nanti", bukan sebagai "gagal".

## Cara melapor

Satu laporan per verifikasi: APA yang dicek, HASILNYA (terlihat / tidak terlihat / sebagian), KUTIPAN persis yang terlihat, dan APA yang masih kurang. Bila ada yang salah, tulis jelas letak kesalahannya dan siapa yang harus memperbaikinya. Jangan menulis "semua sudah benar" bila hanya sebagian yang dicek.
