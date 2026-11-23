# Skill: Ketahanan Kanal Penjualan (untuk A25 Sales Manager)

> Perintah Cipta 23 Nov 2026 — Masalah: penawaran hari ini 6/20. TikTok logout sendiri, Threads kena batas harian, IG dibatasi. Tidak ada yang mengecek kanal sebelum jam kirim, dan tidak ada jalur cadangan — target hilang begitu satu kanal mati. Skill ini memastikan penawaran tetap jalan walau satu kanal tumbang.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A25 Sales Manager** | Mengelola pipeline, penawaran, target penjualan; menjalankan cek pra-penerbangan + fallback di bawah |
| Dukungan | **A26 Customer Service** | Membalas toko yang merespons penawaran; follow-up jam 19:00–21:00 |

## Aturan keras

1. **Target harian:** 20 toko valid + 1 balasan; mingguan 1 closing; bulanan (Des 2026) Rp10.000.000.
2. **Jam:** 09:00–11:00 penawaran baru; 19:00–21:00 follow-up + balas toko.
3. **Kanal:** Instagram, TikTok, Threads (DM) + email. **WhatsApp TIDAK dipakai** untuk penjualan/pemasaran/promo/penawaran — termasuk follow-up/closing (sangat high risk, rawan blokir). Facebook NANTI.
4. **Batas per kanal:** maks ~10 DM/hari/akun, jeda ≥3 menit antar DM. Jangan tembak sekaligus — akun kena batasi.
5. **Akun yang JANGAN dipakai DM:** @meongcast (dibatasi sejak 21 Nov), @meongcast.id (cadangan, masih pemanasan — JANGAN DM dulu).
6. **Isi pesan:** Pesan 1 TANPA harga; Pesan 2 harga USD + https://digicat.std.ai.id/ (tanpa `?v=`). Fokus kebutuhan customer — bila customer bercerita, dengarkan masalahnya, cari solusinya, lalu tawarkan produk yang menjawab kebutuhan itu.
7. **Cipta hanya turun tangan bila URGENT.** A25 yang MENGIRIM penawaran (aturan 21 Nov 11:43).

## Cek pra-penerbangan — WAJIB sebelum jam 09:00

Jangan kirim penawaran sebelum cek ini selesai:

1. **TikTok:** sesi masih login? Bila logout sendiri (pernah 23 Nov 09:37) → catat, alihkan kuota TikTok hari itu ke email; jangan paksa login ulang (hanya Cipta bisa login Google bila verifikasi diminta).
2. **Threads:** cek batas harian — bila kemarin sudah kena batas, mulai dari email dulu, Threads belakangan.
3. **Instagram:** cek akun masih bisa DM (bukan dibatasi). @meongcast dibatasi → pakai akun lain yang sehat.
4. **Email:** pastikan daftar target hari ini punya alamat email (dari Google Maps / riset UMKM) sebagai cadangan tiap toko.
5. Tulis hasil cek ke `data/log-eksekusi.jsonl` (kanal mana hidup/mati, kuota dialihkan ke mana).

## Fallback — bila kanal mati di tengah jalan

- **Satu kanal mati:** kuotanya dialihkan ke email (kirim penawaran via email ke toko yang sama) atau ke kanal lain yang masih sehat. Target 20/hari TIDAK BOLEH turun karena satu kanal mati.
- **Semua DM mati:** hari itu penuh via email + follow-up toko lama (jam 19:00–21:00).
- **Akun kena batasi saat mengirim:** BERHENTI di akun itu hari itu juga; jangan pindah akun lalu tembak lagi dengan pola sama — catat, alihkan ke email, laporkan ke log.

## Follow-up (19:00–21:00)

- Balas semua toko yang merespons (maks 1 hari tunggu).
- Toko yang belum merespons 2 hari: kirim Pesan 2 (harga + tautan toko) bila belum dikirim.
- Toko yang menolak: catat alasannya di `data/leads.json` — jangan ditawari produk yang sama lagi.

## Bukti + lapor

- Log harian penawaran: `~/workspace/goals/daily-oyen-60-second-podcast-videos/hidden_files/log-penawaran-YYYY-MM-DD.csv` (tanggal, toko, kanal, pesan ke-1/2, balasan).
- Satu baris `data/log-eksekusi.jsonl` per sesi (pagi + malam): berapa terkirim per kanal, berapa balasan, kanal apa yang mati + fallback-nya.
