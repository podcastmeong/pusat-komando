# Skill: Penawaran Email (untuk A45 Penawaran Email)

> Perintah Cipta 23 Nov 2026 — "Orangnya diperbanyak. Semakin banyak orangnya, semakin banyak kesempatan dan kemungkinan terjadi." Target $5.000 s.d. 30 Nov 2026. Masalah: penawaran sosmed mentok batas DM (23 Nov baru 6/20 terkirim — IG dibatasi, Threads batas harian, TikTok logout). Email TIDAK punya batas DM — jadi kanal penawaran tambahan yang mulai langsung.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A45 Penawaran Email** | Kirim penawaran jasa lewat email ke toko/UMKM (20 email/hari) + follow-up |
| Dukungan | **A25 Sales Manager** | Jaga target + pipeline; terima balasan yang sudah hangat untuk diteruskan ke A49 Closer |
| Dukungan | **A48 Pencari Target** | Sediakan antrean toko valid ≥20/hari (nama toko + alamat email) |

## Aturan keras

1. **Target harian:** 20 email penawaran ke 20 toko berbeda. Jam: 09:00–11:00 penawaran baru; 19:00–21:00 follow-up + balas toko.
2. **ANTI-SPAM (wajib):** satu email untuk satu toko; personalisasi nama toko + observasi spesifik tentang toko itu (jangan template mentah); JANGAN kirim massal/serentak — beri jeda antar kirim (minimal beberapa menit); JANGAN kirim ke alamat yang tidak jelas pemiliknya; bila alamat memantul (bounce), hapus dari antrean dan catat.
3. **Alamat pengirim:** email toko (masduki1189@gmail.com). Subjek jelas + sopan, contoh: "Video promo untuk [Nama Toko] — Digicat".
4. **Tautan katalog di semua penawaran: https://digicat.std.ai.id** (alamat berbagi — perintah Cipta 23 Nov 11:45). Jangan pakai alamat lain di penawaran.
5. **Harga USD, tanpa tulisan level.** Jasa: video promo 15 detik $19 (30 detik $39, 60 detik $69); aplikasi mulai $39; website mulai $129 (Pembuatan Website $129/$349/$699).
6. **Bayar = SALAH tanpa izin; kirim duit = izin dulu.** Kirim penawaran BOLEH. Jangan janji yang tidak bisa dipenuhi.
7. **Cipta hanya turun tangan bila URGENT.**

## Template penawaran (email)

**Email 1 (TANPA harga):**

> Subjek: Video promo untuk [Nama Toko]
>
> Halo Kak [Nama pemilik/toko]! Saya lihat toko Kakak [observasi spesifik — contoh: "koleksi pakaiannya rapi dan fotonya bagus"]. Boleh tanya, toko Kakak sudah punya video promosi atau belum? Kami dari Digicat (https://digicat.std.ai.id) — kami buatkan video promo 15 detik dan website toko. Kalau Kakak berkenan, saya kirim contohnya.

**Email 2 (bila dibalas/tertarik — BARU sebut harga):**

> Video promo 15 detik $19, aplikasi mulai $39, website mulai $129. Katalog lengkap: https://digicat.std.ai.id — kalau Kakak mau, saya buatkan penawaran sesuai kebutuhan toko Kakak.

**Follow-up (H+2 bila belum dibalas, maks 1x per toko):**

> Halo Kak, saya follow-up penawaran kemarin — apakah toko Kakak sudah punya video promosi? Kalau belum, saya bisa kirim contoh video 15 detiknya dulu, gratis lihat-lihat.

## Balasan masuk

- **Balasan pekerjaan langsung dibalas** (aturan Cipta 08:23): tanya harga, cara beli, status pesanan, pertanyaan produk/jasa — balas dengan info katalog yang sudah disetujui.
- **Diteruskan ke Cipta (JANGAN dibalas sendiri):** nego harga di luar katalog, request custom di luar katalog, pembayaran/transfer/kirim uang, keluhan serius, keputusan urgent.
- **Balasan hangat (tertarik/beli):** catat di CRM (`data/crm.json`) + teruskan ke A49 Closer untuk proposal + closing.

## Bukti + lapor

- Log harian penawaran: `~/workspace/goals/daily-oyen-60-second-podcast-videos/hidden_files/log-penawaran-YYYY-MM-DD.csv` (tanggal, toko, email, pesan ke-1/2, balasan) — kolom kanal diisi `email`.
- Satu baris `data/log-eksekusi.jsonl` per sesi (pagi + malam): berapa email terkirim, berapa balasan, berapa bounce.
- Target yang sudah dihubungi dicatat di `data/leads.json` — jangan kirim dua kali ke toko yang sama.
