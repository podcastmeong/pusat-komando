# Spesifikasi Harga Toko — A42 (SPESIFIKASI UNTUK PARENT, BUKAN EKSEKUSI)

**Status: SPESIFIKASI — belum dieksekusi.** Dibuat A42 (agent baru, 22 Nov 2026).
Edit harga aplikasi toko HANYA bisa lewat artifact `toko-aplikasi` — A42 tidak punya
artifact tools, jadi file ini adalah instruksi kerja untuk parent (artifact.edit →
artifact.export → salin ke repo → commit → push → verifikasi live dari sisi Cipta).
**Jangan edit file repo `toko.html` langsung** — edit itu akan tertimpa export artifact
berikutnya (insiden "balik hijau" 20 Nov 2026).

**Dasar keputusan:** hapus tier Basic/Professional/Business di katalog aplikasi; SATU harga
per aplikasi dari tabel USD yang disetujui — **aplikasi $29 / $59 / $99 + $25 untuk APK** —
tanpa menyebut nama level di tampilan toko. **Tier per produk di bawah ini DRAF**
(belum pernah diputuskan Cipta) — tetapkan sebagai draf, tayang setelah Cipta setuju.

## 1. Blok harga Basic/Professional/Business yang HARUS DIHAPUS (katalog aplikasi)

Nomor baris merujuk **salinan repo `~/workspace/tmp/podcastmeong.github.io/toko.html`**
(terverifikasi grep 22 Nov 2026) — **WAJIB dikonfirmasi ulang di artifact `toko-aplikasi`
sebelum edit**, karena salinan repo bisa berbeda dari artifact:

| # | Lokasi (repo toko.html) | Isi yang dihapus |
|---|---|---|
| 1 | L983 | Paragraf pembuka: "Semua aplikasi di katalog tersedia dalam tiga paket — Basic, Professional, dan Business…" |
| 2 | L994–1004 | Pilihan paket `qname` Basic / Professional / Business (bagian katalog aplikasi) |
| 3 | L1110 | `qnote` tambahan harga: "+Rp500.000, +Rp1.000.000, atau +Rp1.500.000 di atas harga dasar paket" + contoh harga (Basic Rp999.000 dst) |
| 4 | L1117, L1136 | Patokan request khusus 3 tingkat + contoh hitung "harga dasar paket pilihan Anda + biaya tambahan… Misalnya paket Basic (Rp…)" |
| 5 | L1371 | Hint formulir: "Patokan biaya tambahannya di atas harga dasar (Basic Rp499.…)" |
| 6 | L1515 | "Beli Sekali (sekali bayar per aplikasi): Basic Rp4…" (dua cara beli per paket) |
| 7 | L1527 | FAQ custom: "Beli Sekali: Basic Rp499.000 / Professional Rp999.000 / Business…" |
| 8 | L1886 | Note JS data: "Harga: beli sekali Basic Rp999.000 / Professional Rp1.499.000 / Business Rp2.499.000…" |
| 9 | L1891–1893 | Data JS paket beli sekali: Basic Rp999.000 / Professional Rp1.499.000 / Business Rp2.499.000 |
| 10 | L1896–1898 | Data JS paket **berlangganan**: Basic Rp199.000 / Professional Rp399.000 / Business Rp749.000 (tier juga dihapus — lihat catatan) |
| 11 | L2734, L2737 | Patokan biaya request khusus: "di atas harga dasar (Basic Rp499.000 / Professional Rp999.000 / Business Rp1.999.000)" |
| 12 | L3644–3646 | Data JS paket beli sekali (set kedua): Basic Rp499.000 / Professional Rp999.000 / Business Rp1.999.000 |
| 13 | L3650–3652 | Data JS paket berlangganan (set kedua): Basic Rp49.000 / Professional Rp99.000 / Business Rp199.000 |

**Catatan berlangganan (butuh keputusan Cipta bila dipertahankan):** tabel USD yang disetujui
hanya mengatur harga **beli sekali** ($29/$59/$99 + $25 APK). Spesifikasi ini menghapus
SEMUA tier Basic/Pro/Business termasuk blok berlangganan, sesuai perintah hapus blok harga
tersebut. Bila Cipta mau mempertahankan model berlangganan, harganya harus diputuskan
terpisah — jangan mengarang angka langganan baru.

**Yang diganti:** tiap kartu aplikasi di katalog menampilkan **SATU harga** (tabel §2) +
catatan "+$25 untuk file APK Android" bila relevan. Tidak ada lagi pilihan paket,
tidak ada lagi label Basic/Professional/Business di bagian aplikasi.

## 2. Penetapan harga per aplikasi — TABEL USD (DRAF, belum diputuskan Cipta)

Aturan tier (DRAF, disusun A42 22 Nov 2026 dari kompleksitas nama/fungsi):
- **$29 — Sederhana:** satu fungsi utama (absensi, pencatat, rekap, stok sederhana).
- **$59 — Menengah:** operasional beberapa modul/fitur (kasir/toko, booking, delivery, HRD, gudang).
- **$99 — Kompleks:** multi-modul / multi-user / laporan keuangan (akuntansi, distributor, klinik, apotek).
- **+$25** untuk file APK Android (tambahan di luar harga, sama untuk semua tier).

### $99 — Kompleks (11 aplikasi)

| Aplikasi (direktori) | Harga |
|---|---|
| aplikasi-accounting | $99 (+$25 APK) |
| aplikasi-akuntansi-distributor | $99 (+$25 APK) |
| aplikasi-apotek | $99 (+$25 APK) |
| aplikasi-audit-internal | $99 (+$25 APK) |
| aplikasi-distribusi-hasil-tani | $99 (+$25 APK) |
| aplikasi-klinik | $99 (+$25 APK) |
| aplikasi-koperasi | $99 (+$25 APK) |
| aplikasi-pajak | $99 (+$25 APK) |
| aplikasi-penjualan-distributor | $99 (+$25 APK) |
| aplikasi-penjualan-properti | $99 (+$25 APK) |
| aplikasi-penggajian | $99 (+$25 APK) |

### $59 — Menengah (31 aplikasi)

| Aplikasi (direktori) | Harga |
|---|---|
| aplikasi-anggaran-perusahaan | $59 (+$25 APK) |
| aplikasi-bengkel-mobil | $59 (+$25 APK) |
| aplikasi-bengkel-motor | $59 (+$25 APK) |
| aplikasi-booking-servis | $59 (+$25 APK) |
| aplikasi-crm | $59 (+$25 APK) |
| aplikasi-delivery-makanan | $59 (+$25 APK) |
| aplikasi-delivery-surat | $59 (+$25 APK) |
| aplikasi-estimasi-biaya-perbaikan | $59 (+$25 APK) |
| aplikasi-evaluasi-kinerja | $59 (+$25 APK) |
| aplikasi-faktur-invoice | $59 (+$25 APK) |
| aplikasi-gudang-mandiri | $59 (+$25 APK) |
| aplikasi-hrd | $59 (+$25 APK) |
| aplikasi-komunikasi-internal-tim | $59 (+$25 APK) |
| aplikasi-kurir | $59 (+$25 APK) |
| aplikasi-mekanik-komisi | $59 (+$25 APK) |
| aplikasi-pelatihan-karyawan | $59 (+$25 APK) |
| aplikasi-pembayaran-sekolah | $59 (+$25 APK) |
| aplikasi-pembelian | $59 (+$25 APK) |
| aplikasi-pemesanan-makanan | $59 (+$25 APK) |
| aplikasi-pencatatan-produksi | $59 (+$25 APK) |
| aplikasi-pengawasan-proyek | $59 (+$25 APK) |
| aplikasi-pengiriman | $59 (+$25 APK) |
| aplikasi-pinjaman-kredit | $59 (+$25 APK) |
| aplikasi-piutang-hutang | $59 (+$25 APK) |
| aplikasi-rab | $59 (+$25 APK) |
| aplikasi-rekrutmen | $59 (+$25 APK) |
| aplikasi-rental-kendaraan | $59 (+$25 APK) |
| aplikasi-salesman | $59 (+$25 APK) |
| aplikasi-servis-kendaraan | $59 (+$25 APK) |
| aplikasi-toko-online | $59 (+$25 APK) |
| aplikasi-ujian-online | $59 (+$25 APK) |

### $29 — Sederhana (19 aplikasi)

| Aplikasi (direktori) | Harga |
|---|---|
| aplikasi-absensi-pekerja-proyek | $29 (+$25 APK) |
| aplikasi-absensi-siswa | $29 (+$25 APK) |
| aplikasi-anggaran-bulanan | $29 (+$25 APK) |
| aplikasi-arus-kas | $29 (+$25 APK) |
| aplikasi-barcode-scanner | $29 (+$25 APK) |
| aplikasi-cuti-izin | $29 (+$25 APK) |
| aplikasi-data-karyawan | $29 (+$25 APK) |
| aplikasi-jadwal-shift | $29 (+$25 APK) |
| aplikasi-ocr | $29 (+$25 APK) |
| aplikasi-ojek | $29 (+$25 APK) |
| aplikasi-panen | $29 (+$25 APK) |
| aplikasi-patungan | $29 (+$25 APK) |
| aplikasi-pencatat-utang-piutang-pribadi | $29 (+$25 APK) |
| aplikasi-piutang | $29 (+$25 APK) |
| aplikasi-rekap | $29 (+$25 APK) |
| aplikasi-riwayat-kendaraan | $29 (+$25 APK) |
| aplikasi-stok-pakan | $29 (+$25 APK) |
| aplikasi-stok-spare-part | $29 (+$25 APK) |
| aplikasi-taksi | $29 (+$25 APK) |

**Total: 61 aplikasi (11 × $99 + 31 × $59 + 19 × $29).** Daftar direktori terverifikasi
di `~/workspace/tmp/podcastmeong.github.io/aplikasi-*/` (61 direktori, masing-masing ada
`index.html`).

## 3. JANGAN SENTUH

| Item | Alasan / lokasi repo |
|---|---|
| Harga website/jasa website **$99 / $299 / $599** (Basic/Professional/Business) | Harga jasa pembuatan website — BUKAN harga aplikasi; demo website dan jasa website dipisah (keputusan Cipta). Lokasi repo: L4059–4066. |
| Blok demo website L1210–1231 ("Setiap demo website kami adalah produk yang dijual…" + qname Basic/Professional/Business) | Harga demo website masih MENUNGGU keputusan (model Rp0/25rb/75rb/150rb vs gratis) — jangan hapus/ubah dalam tugas ini. |
| Tombol Payhip eBook | Jalur penjualan eBook — di luar cakupan A42. |
| Jumpnav 9 tautan kamar | Menu toko wajib 9 tautan kamar, tanpa pil Jasa (pelajaran 20 Nov 2026). |
| Palet navy (#14263d, #8fb4d9) | Desain toko saat ini navy/biru soft, BUKAN hijau. |
| Harga sistem custom (L4073: Basic Rp4.900.000 dst) | Di luar cakupan katalog aplikasi. |
| Harga lain yang sudah disetujui (eBook $4,99, game $2,99/$4,99/$5,99, video promo $19/$39/$69, skill $12) | Bukan tugas A42. |

## 4. Langkah eksekusi untuk parent (artifact)

1. Buka artifact `toko-aplikasi`; konfirmasi tiap blok §1 ada di artifact (nomor baris repo bisa bergeser).
2. `artifact.edit`: hapus blok §1; ganti harga tiap kartu aplikasi dengan SATU harga §2 + "+$25 APK".
3. `artifact.export` → salin ke repo → commit → push.
4. Verifikasi live dari sisi Cipta (A38 QA): 0× "Basic/Professional/Business" di bagian aplikasi;
   tiap aplikasi 1 harga; §3 tidak berubah. Cek grep/curl saja TIDAK cukup.
5. Bila tier per produk (§2) belum disetujui Cipta: tayangkan sebagai DRAF dulu atau tahan —
   jangan klaim sudah diputuskan.
