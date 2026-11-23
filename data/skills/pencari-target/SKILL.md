# Skill: Pencari Target (untuk A48 Pencari Target)

> Perintah Cipta 23 Nov 2026 — "Orangnya diperbanyak. Semakin banyak orangnya, semakin banyak kesempatan dan kemungkinan terjadi." Target $5.000 s.d. 30 Nov 2026. Masalah: penawaran hanya jalan bila ada antrean toko — A25/A45/A46/A47 butuh 20 toko valid setiap hari. A48 menjaga antrean itu tidak pernah kosong.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A48 Pencari Target** | Riset + verifikasi toko target; jaga antrean ≥20 toko/hari |
| Pemakai antrean | **A25, A45, A46, A47** | Ambil toko dari antrean untuk ditawari (jangan ambil dari luar antrean tanpa verifikasi A48) |

## Aturan keras

1. **Target harian:** antrean selalu ≥20 toko VALID untuk esok hari (siapkan malam sebelumnya bila perlu). Toko yang sudah ditawari JANGAN masuk antrean lagi.
2. **AKTIF dan VALID (keduanya wajib):** ada postingan terbaru (maks ~2 minggu terakhir); ada kontak yang bisa dihubungi (DM terbuka / email / nomor WA di profil); toko benar-benar jualan (bukan akun pribadi, bukan akun mati, bukan akun bot).
3. **Jenis toko:** UMKM / petshop / toko kelontong / kuliner / fashion / jasa lokal — yang paling butuh video promo + website. Utamakan toko yang BELUM punya video promo dan BELUM punya website.
4. **JANGAN ambil toko dari grup terbuka** (risiko ban — aturan UMKM 23 Nov 2026). Ambil dari Google Maps, pencarian IG/TikTok, dan riset komunitas (`~/workspace/riset-komunitas-umkm-2026-11-23.md`).
5. **JANGAN tawarkan langsung** — A48 hanya riset + verifikasi + antrean. Penawaran dikirim A25/A45/A46/A47.
6. **Satu toko satu baris data:** nama toko, jenis usaha, akun IG/TikTok/Threads, alamat email (bila ada), kota, tanggal verifikasi, status (baru / sudah ditawari / menolak / tertarik).

## Cara verifikasi (cek sebelum masuk antrean)

1. Buka profil toko: ada foto produk + deskripsi usaha yang jelas?
2. Postingan terbaru: ada dalam 2 minggu terakhir? (bila tidak — TOLAK, akun mati)
3. Kontak: DM terbuka ATAU email di bio ATAU nomor WA di profil? (bila tidak ada ketiganya — TOLAK, tidak bisa dihubungi)
4. Sudah punya video promo / website? (bila sudah lengkap — prioritas RENDAH, catat tapi antre belakangan)
5. Catat alasan bila toko ditolak (mati / tanpa kontak / bukan toko) — supaya tidak dicek ulang besok.

## File kerja

- **Antrean utama (repo): `data/leads.json`** — daftar target yang dipakai A25/A45/A46/A47 setiap hari.
- Daftar pet shop Jaksel (15 toko + draf WA) sudah ada di `~/workspace/goals/daily-oyen-60-second-podcast-videos/files/oyen-podcast/daftar-target-petshop-10.md` — pakai sebagai antrean awal, jangan duplikasi (dan pindahkan yang terverifikasi ke `data/leads.json`).
- Riset komunitas UMKM: `~/workspace/riset-komunitas-umkm-2026-11-23.md` (jangan posting promo terbuka di grup — risiko ban).

## Bukti + lapor

- Setiap toko baru yang masuk antrean dicatat di `data/leads.json` (lengkap dengan tanggal verifikasi).
- Satu baris `data/log-eksekusi.jsonl` per hari: berapa toko baru terverifikasi, berapa ditolak + alasannya, sisa antrean untuk besok.
