# Manifest Upload Marketplace — A43 (MANIFEST, BUKAN EKSEKUSI)

**Status: MANIFEST — belum ada yang diunggah.** Dibuat A43 (agent baru, 22 Nov 2026).
Upload ke Gumroad/Payhip butuh browser + login — A43 tidak punya browser, jadi file ini
adalah daftar kerja untuk parent (browser). **Jangan klaim produk sudah live** sebelum
URL listing-nya terverifikasi.

**Target:** Gumroad (utama — toko sudah live, eksekusi selesai penuh 22 Nov 06:28) /
Payhip (cerminan kedua — 6 eBook sudah live). **Terbitkan hanya setelah Cipta setuju
harga + isi persisnya.**

**Aturan harga (DRAF — tier per produk belum pernah diputuskan Cipta):**
- Aplikasi: **$29 / $59 / $99 + $25 APK** (tabel USD yang disetujui; tier per produk DRAF,
  aturan: $29 sederhana, $59 menengah, $99 kompleks — sama dengan spesifikasi A42).
- Demo website: tier DRAF **$29 / $59 / $99** (usulan A43 dari kompleksitas; **BUKAN**
  harga jasa website $99/$299/$599 — demo website dan jasa website dipisah, keputusan Cipta;
  harga demo masih menunggu keputusan final).
- Per produk: ZIP berisi `index.html` (+ file test/aset bila ada — test TIDAK ikut dijual,
  hanya bukti uji) + deskripsi jujur + screenshot ASLI + tautan demo live terverifikasi
  (`https://podcastmeong.github.io/<direktori>/`).

**Langkah sebelum upload (parent):** (1) buat ZIP per produk; (2) screenshot tiap produk
dari demo live; (3) verifikasi demo live HTTP 200; (4) upload sebagai DRAF; (5) terbitkan
setelah Cipta setuju harga + isi.

## A. 15 demo website — `~/workspace/tmp/podcastmeong.github.io/demo-website/`

Semua direktori terverifikasi berisi `index.html` (22 Nov 2026).

| # | Produk (direktori) | File | Tier DRAF | Harga DRAF | Platform | Status |
|---|---|---|---|---|---|---|
| 1 | demo-website/bisnis/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 2 | demo-website/blog/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 3 | demo-website/blog-ai/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 4 | demo-website/booking/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 5 | demo-website/booking-cerdas/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 6 | demo-website/company-profile/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 7 | demo-website/katalog-whatsapp/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 8 | demo-website/landing-page/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 9 | demo-website/portofolio/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 10 | demo-website/restoran/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 11 | demo-website/sekolah/ | index.html | Sederhana | $29 | Gumroad / Payhip | Menunggu upload |
| 12 | demo-website/sistem-aplikasi/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 13 | demo-website/sistem-bisnis/ | index.html | Kompleks | $99 | Gumroad / Payhip | Menunggu upload |
| 14 | demo-website/website-ai/ | index.html | Menengah | $59 | Gumroad / Payhip | Menunggu upload |
| 15 | demo-website/website-cerdas/ | index.html | Kompleks | $99 | Gumroad / Payhip | Menunggu upload |

Demo website: 7 × $29 + 6 × $59 + 2 × $99.

## B. 61 aplikasi — `~/workspace/tmp/podcastmeong.github.io/aplikasi-*/`

Semua direktori terverifikasi berisi `index.html` (22 Nov 2026). Kolom "File tambahan"
hanya mencatat file test yang ada (bukti uji, TIDAK ikut dijual).

### B1. $99 — Kompleks (11)

| # | Produk (direktori) | File | File tambahan | Harga DRAF | Platform | Status |
|---|---|---|---|---|---|---|
| 1 | aplikasi-accounting | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 2 | aplikasi-akuntansi-distributor | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 3 | aplikasi-apotek | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 4 | aplikasi-audit-internal | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 5 | aplikasi-distribusi-hasil-tani | index.html | tests/ | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 6 | aplikasi-klinik | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 7 | aplikasi-koperasi | index.html | test_aplikasi_koperasi.py | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 8 | aplikasi-pajak | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 9 | aplikasi-penjualan-distributor | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 10 | aplikasi-penjualan-properti | index.html | test_penjualan_properti.py | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 11 | aplikasi-penggajian | index.html | — | $99 (+$25 APK) | Gumroad / Payhip | Menunggu upload |

### B2. $59 — Menengah (31)

| # | Produk (direktori) | File | File tambahan | Harga DRAF | Platform | Status |
|---|---|---|---|---|---|---|
| 12 | aplikasi-anggaran-perusahaan | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 13 | aplikasi-bengkel-mobil | index.html | test_mobil.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 14 | aplikasi-bengkel-motor | index.html | test_motor.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 15 | aplikasi-booking-servis | index.html | test_booking.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 16 | aplikasi-crm | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 17 | aplikasi-delivery-makanan | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 18 | aplikasi-delivery-surat | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 19 | aplikasi-estimasi-biaya-perbaikan | index.html | test_estimasi.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 20 | aplikasi-evaluasi-kinerja | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 21 | aplikasi-faktur-invoice | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 22 | aplikasi-gudang-mandiri | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 23 | aplikasi-hrd | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 24 | aplikasi-komunikasi-internal-tim | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 25 | aplikasi-kurir | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 26 | aplikasi-mekanik-komisi | index.html | test_mekanik.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 27 | aplikasi-pelatihan-karyawan | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 28 | aplikasi-pembayaran-sekolah | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 29 | aplikasi-pembelian | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 30 | aplikasi-pemesanan-makanan | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 31 | aplikasi-pencatatan-produksi | index.html | tests/ | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 32 | aplikasi-pengawasan-proyek | index.html | test_pengawasan.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 33 | aplikasi-pengiriman | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 34 | aplikasi-pinjaman-kredit | index.html | test_aplikasi_pinjaman_kredit.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 35 | aplikasi-piutang-hutang | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 36 | aplikasi-rab | index.html | test_rab.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 37 | aplikasi-rekrutmen | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 38 | aplikasi-rental-kendaraan | index.html | test_rental.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 39 | aplikasi-salesman | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 40 | aplikasi-servis-kendaraan | index.html | test_servis.py | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 41 | aplikasi-toko-online | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 42 | aplikasi-ujian-online | index.html | — | $59 (+$25 APK) | Gumroad / Payhip | Menunggu upload |

### B3. $29 — Sederhana (19)

| # | Produk (direktori) | File | File tambahan | Harga DRAF | Platform | Status |
|---|---|---|---|---|---|---|
| 43 | aplikasi-absensi-pekerja-proyek | index.html | test_absensi.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 44 | aplikasi-absensi-siswa | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 45 | aplikasi-anggaran-bulanan | index.html | test_aplikasi_anggaran_bulanan.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 46 | aplikasi-arus-kas | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 47 | aplikasi-barcode-scanner | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 48 | aplikasi-cuti-izin | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 49 | aplikasi-data-karyawan | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 50 | aplikasi-jadwal-shift | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 51 | aplikasi-ocr | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 52 | aplikasi-ojek | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 53 | aplikasi-panen | index.html | test_aplikasi_panen.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 54 | aplikasi-patungan | index.html | test_aplikasi_patungan.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 55 | aplikasi-pencatat-utang-piutang-pribadi | index.html | test_pencatat_utang_piutang.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 56 | aplikasi-piutang | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 57 | aplikasi-rekap | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 58 | aplikasi-riwayat-kendaraan | index.html | test_riwayat.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 59 | aplikasi-stok-pakan | index.html | test_aplikasi_stok_pakan.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 60 | aplikasi-stok-spare-part | index.html | test_sparepart.py | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |
| 61 | aplikasi-taksi | index.html | — | $29 (+$25 APK) | Gumroad / Payhip | Menunggu upload |

**Rekap:** 15 demo website + 61 aplikasi = **76 produk**. Aplikasi: 11 × $99 + 31 × $59 + 19 × $29.
Tier/harga di manifest ini SAMA dengan spesifikasi A42 (`data/a42-spesifikasi-harga-toko.md`)
— satu sumber tier DRAF untuk toko + marketplace, supaya tidak bentrok.

## C. Catatan eksekusi (untuk parent / browser)

1. **ZIP belum dibuat** — tiap produk perlu di-ZIP (`index.html` + aset) sebelum upload;
   manifest ini baru daftar + harga, bukan paket siap upload.
2. **Demo live belum diverifikasi ulang** — cek HTTP 200 tiap `https://podcastmeong.github.io/<direktori>/`
   sebelum tautan demo ditulis di listing.
3. **Screenshot asli** — jangan pakai gambar stok/buatan untuk preview produk.
4. **Urutan usul:** Gumroad dulu (sudah live), Payhip sebagai cerminan; atau batch 10 produk/hari
   supaya tidak mentok batasan akun.
5. **Setelah upload:** isi kolom Status + URL listing live di manifest ini + satu baris
   ke `data/log-eksekusi.jsonl` per batch. Produk tanpa URL live = BELUM selesai.
