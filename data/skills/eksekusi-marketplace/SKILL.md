# Skill: Eksekusi 20 Marketplace (untuk Tim Produksi A11–A19)

> Perintah Cipta 22 Nov 2026 — WAJIB. Eksekusi SEMUA 20 marketplace, satu-satu dari no. 1; kalau selesai lanjut next. Yang bisa dikerjakan dulu; berhenti hanya bila benar-benar mentok. Diserahkan ke Tim Produksi. Skill ini adalah bekal kerja tim — baca sebelum mengerjakan marketplace mana pun.

## Aturan keras (tidak boleh dilanggar)

1. **Jangan bayar apa pun** — termasuk biaya pendaftaran, ujian, listing, dan langganan. Bila sebuah marketplace mewajibkan pembayaran untuk daftar, LAPORKAN dan lewati.
2. **Jangan kirim email/pesan ke pihak mana pun** tanpa persetujuan Cipta atas teks persisnya.
3. **Pakai hanya akun Cipta yang sudah ada** (masduki1189@gmail.com / ciptabintanglestari@gmail.com). Jangan buat akun dengan data yang tidak benar.
4. **Jangan sertakan kredensial/kunci/token** apa pun dalam listing atau paket.
5. **Jujur soal produk** — jangan klaim fitur yang tidak ada di produk. Tiga contoh nyata yang sudah diperbaiki: aplikasi Faktur TIDAK punya diskon per baris; PPN tetap 11% (bukan bisa diubah); tidak ada tombol/layout cetak (cetak via browser). Periksa klaim draf ke kode/file produk sebelum upload.
6. **Labeli karya AI sebagai AI** di marketplace yang memintanya (Creative Market, dan semua yang sejenis).
7. **DRAF dulu, live belakangan** — listing dibuat draf; terbit hanya setelah Cipta menyetujui harga + isi persisnya.
8. **Harga patokan tidak diubah tanpa persetujuan Cipta:** skill $12 · aplikasi $29/$59/$99 · game $2,99/$4,99/$5,99 · eBook nabi $4,99 · Rindu $5 · video promo $19/$39/$69 · website $99/$299/$599 · POD $2,99/$7,99/$14,99 · musik $5/$19/$29.

## Cara kerja satu marketplace (urutannya selalu sama)

1. **Riset syarat seller** di situs resminya: pendaftaran, verifikasi identitas, komisi, payout, kategori yang diterima, batasan produk. Catat sumber + tanggal riset.
2. **Cek kecocokan produk** dengan kategori marketplace itu. Bila tidak cocok (contoh: produk HTML bukan aset Unity; produk skill bukan Actor Apify), LAPORKAN alasannya dan lewati — jangan dipaksakan.
3. **Siapkan paket listing** dari draf yang sudah ada (lihat peta file di bawah) atau buat baru: deskripsi (Inggris bila marketplace internasional), harga, screenshot/preview asli, dokumentasi (bila wajib), URL demo live yang sudah diverifikasi.
4. **Periksa klaim ke produk asli** (buka file/kode produk, jangan percaya draf mentah-mentah).
5. **Buat listing sebagai DRAF** (atau siapkan semua file + teks bila butuh browser). Laporkan: apa yang siap, harga yang diusulkan, dan apa yang butuh Cipta.
6. **Terbitkan hanya setelah Cipta setuju** harga + isi persisnya. Setelah live, catat tautan listing + tanggal di `data/marketplace-20-eksekusi.md` dan `~/workspace/marketplace-20-status.md`.
7. **Bila mentok** (pendaftaran tutup, butuh badan usaha/kartu kredit/kemitraan, verifikasi hanya pemilik bisa), catat alasannya, laporkan, dan LANJUT ke nomor berikutnya — jangan berhenti di satu nomor.

## Urutan eksekusi (satu-satu)

1 Swarms → 11 Codester → 14/16 Creative Market + PromptBase → 2 Agensi.io → 4, 5, 18, 20 (riset) → 9, 10 (pantau pembukaan) → 3, 6, 7, 8, 12, 15, 19 (butuh keputusan/berkas Cipta). Status terbaru selalu di `data/marketplace-20-eksekusi.md`.

## Peta file (baca sebelum mengerjakan nomornya)

- Rencana + status lengkap: `data/marketplace-20-eksekusi.md` dan `~/workspace/marketplace-20-status.md`
- Referensi syarat/komisi/payout per marketplace: `data/skills/eksekusi-marketplace/referensi-20-marketplace.md`
- No. 1 Swarms — paket skill: `~/workspace/skill-pusat-komando-swarms/` (baca `PUBLISH.md`; publish lewat `POST /api/v1/publish/product` type `prompt`, butuh `SWARMS_API_KEY` dari akun Cipta; TIDAK ada endpoint khusus skill)
- No. 9–12 — draf listing: `~/workspace/marketplace-9-12/` (envato/codecanyon/codester-draf-listing.md + `codester-paket/` berisi ZIP, dokumentasi EN, 6 screenshot, preview 800×400, icon 200×200)
- No. 14 — draf + harga: `~/workspace/creative-market-14-16/` (draf-listing-cm.md, shop-request-cm.md, kekurangan-cm.md)
- No. 16 — draf + harga: `~/workspace/promptbase-14-16/` (draf-listing-promptbase.md, kekurangan-promptbase.md)
- No. 15 Etsy — kata kunci + draf: `~/workspace/research_notes/strategi-11-platform/etsy-gratis-langkah-1.md`
- No. 13 Gumroad / No. 17 Payhip — sudah LIVE; isi produk, jangan daftar ulang
- Aturan persetujuan (WAJIB dibaca): `data/aturan-persetujuan.md` — apa yang boleh jalan sendiri, apa yang butuh "Setuju" Cipta
- 27 Aturan Wajib: `data/aturan-wajib-27-poin.md`

## Pembagian tugas dalam Tim Produksi

- **A13 App Developer** — listing aplikasi (Codester, CodeCanyon, Envato, Agensi.io bila perlu): paket ZIP, dokumentasi, screenshot, demo live.
- **A18 Game Developer** — listing game (itch.io, Codester, Unity bila diputuskan port).
- **A15 POD Designer** — listing ilustrasi POD (Creative Market).
- **A16 eBook Publisher** — listing eBook (Etsy, Creative Market cover, Payhip, Gumroad).
- **A11 + A12** — video preview + gambar preview/icon untuk listing (ukuran sesuai syarat tiap marketplace).
- **A17 Creative Writer** — deskripsi listing (Inggris), teks Shop Request, teks prompt (PromptBase).
- **A14 Web Developer** — URL demo live + halaman demo bersih (tanpa harga lama yang bentrok).
- **A19 Content Producer** — koordinasi urutan 1→20, update status di komando tiap ada kemajuan.
- **A32 Build** (bukan Produksi, tapi pendukung) — membangun paket/artefak yang dibutuhkan listing. **A31 Publish** — mengunggah produk yang sudah disetujui ke platform penjualan.

## Yang butuh Cipta (hanya ini — selebihnya tim yang kerjakan)

- Masuk Google masduki1189 (satu ketukan, di aplikasi Muse) — API key Swarms (no. 1).
- Setuju teks + harga + bahasa UI — Codester (no. 11).
- Setuju harga — Creative Market (no. 14) + PromptBase (no. 16).
- Setuju teks balasan $12 ke Joeri — Agensi.io (no. 2).
- Jawab pertanyaan keamanan Fiverr — no. 19.
- Putuskan: port game jadi template Unity? Buka toko Etsy? — no. 12, 15.
