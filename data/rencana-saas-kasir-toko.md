# Rencana SaaS — Kasir Toko (aplikasi SaaS pertama)

**Status:** KODE V1 SELESAI dibangun 22 Nov 2026 15:03 (28/28 uji end-to-end lolos, termasuk modul logistik) — deploy menunggu Cloudflare staging selesai (login Cloudflare masih berjalan di browser).
**Produk:** Kasir Toko — saat ini dijual sebagai demo statis $59 (sekali bayar). Versi SaaS = aplikasi kasir sungguhan yang jalan di server, pelanggan login dan pakai lewat browser.
**Model (Cipta, 22 Nov 2026 15:09): SaaS ini PER TOKO — aplikasi dan web.** Satu toko = satu akun/workspace sendiri (data terpisah per toko). v1 jalan di web (mobile-friendly, bisa dipakai seperti aplikasi di HP); aplikasi native menyusul bila dibutuhkan.

## Kenapa Kasir Toko dulu

- Produk paling umum (semua toko butuh kasir), harga $59 sudah terbukti di katalog.
- Fitur kasir paling mudah dijadikan SaaS: transaksi, stok, laporan — tanpa fitur aneh.

## Fitur v1 (yang dibangun dulu)

1. Login pelanggan (email + kata sandi; satu akun per toko).
2. Tambah produk + stok (nama, harga, jumlah).
3. Kasir: pilih produk → total otomatis → simpan transaksi → cetak struk.
4. Laporan harian/bulanan (total penjualan, produk terlaris).
5. Data tersimpan di database (tidak hilang bila ganti HP).

## Teknologi (semua gratis di skala kecil)

- Frontend: Cloudflare Pages (sudah staging).
- Backend: Cloudflare Workers (fungsi server, gratis 100 ribu request/hari).
- Database: Cloudflare D1 (gratis, untuk akun + produk + transaksi).
- Dibangun oleh: subagent Muse — kode v1 selesai 22 Nov 2026 15:03 (Worker + D1 + SPA 7 tab, 28/28 uji lolos). Rencana awal pakai Antigravity tidak jadi dipakai untuk v1.

## Harga (USULAN, belum diputuskan)

- Langganan $4,99/bulan, uji coba gratis 7 hari. Versi sekali bayar $59 tetap dijual (file demo statis).
- Bayar lewat PayPal masduki1189 (yang sudah ada). Akses akun dibuat setelah pembayaran terkonfirmasi (v1 manual oleh admin; otomatisasi belakangan).

## Urutan eksekusi

1. Cloudflare login + staging toko selesai (sedang jalan).
2. Agent Antigravity membangun backend Workers + D1 + halaman login/transaksi/laporan untuk Kasir Toko.
3. Uji end-to-end: daftar → login → tambah produk → transaksi → laporan.
4. Deploy ke *.pages.dev, verifikasi, baru laporkan ke Cipta untuk keputusan live.
5. Aplikasi SaaS berikutnya (Faktur & Invoice) setelah Kasir Toko live.
