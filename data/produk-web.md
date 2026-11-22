# Produk Web — 4 Produk (Keputusan Cipta 22 Nov 2026 17:02)

> Keputusan Cipta (WA 17:02, dicatat di `~/workspace/catatan/keputusan.md`):
> 1. Demo web · 2. Pembuatan web (belum termasuk hosting dan domain) ·
> 3. Pembuatan web + free hosting · 4. Penyewaan web + hosting.
> Dokumen ini sumber racikan produk + price list-nya di Pusat Komando.
> Harga lain yang sudah disetujui TIDAK diubah di sini
> (eBook $4,99 · aplikasi $29/$59/$99 · video promo $19/$39/$69 · game · POD · musik).
> Riset model sewa: `~/workspace/research_notes/jasa-website-dikelola-agency-20261122-0948/report.md`.

## Ringkasan price list

| # | Produk | Harga | Satuan |
|---|---|---|---|
| 1 | Demo web (website jadi, dijual apa adanya) | **$29 / $49 / $79** | sekali bayar, per website |
| 2 | Pembuatan web (custom, belum termasuk hosting dan domain) | **$99 / $299 / $599** | sekali bayar, per website |
| 3 | Pembuatan web + free hosting | **$119 / $319 / $619** | sekali bayar, per website |
| 4 | Penyewaan web + hosting (WaaS / sewa website) | **Rp29.000 / Rp39.000 / Rp49.000** | per bulan — **DRAFT**, lihat §4 |

Aturan harga (Cipta 22 Nov 13:33): **nama dan angka tingkat TIDAK PERNAH ditulis
di mana pun** (toko, catatan, Komando). Saat upload/tayang: langsung harga saja.

---

## 1. Demo web — $29 / $49 / $79 (sekali bayar)

Website jadi yang dijual apa adanya, berdasarkan 15 template demo yang sudah ada
di repo toko (`~/workspace/tmp/podcastmeong.github.io/demo-website/`).

Stok demo (15, judul dari `<title>` masing-masing `index.html`):

| Folder | Demo |
|---|---|
| `bisnis` | Kiki Barbershop & Salon — Website + Booking |
| `blog-ai` | Blog Kiki Cerdas — Blog + Chatbot & Rekomendasi Artikel |
| `blog` | Roti Manis Ibu Sari — Blog Toko Roti Rumahan |
| `booking-cerdas` | Kiki Futsal Arena — Booking + Prediksi Permintaan |
| `booking` | Salon Cantik Ayu — Booking / Reservasi |
| `company-profile` | CV Sinar Jaya Distributor — Distributor Sembako |
| `katalog-whatsapp` | Toko Hijab Kirana — Katalog Produk & Order WhatsApp |
| `landing-page` | Sepatu Kinclong — Jasa Cuci Sepatu (Landing Page) |
| `portofolio` | Raka Prasetyo Photography — Portofolio Fotografer |
| `restoran` | Kafe Senja — Menu Digital & Reservasi |
| `sekolah` | SDN Harapan Bangsa 01 — Website Sekolah |
| `sistem-aplikasi` | PT Kiki Distribusi — Website + Dashboard Admin |
| `sistem-bisnis` | PT Kiki Digital — Website + Dashboard Internal |
| `website-ai` | Kiki Laundry — Website + Chatbot Otomatis |
| `website-cerdas` | Sembako Kiki Jaya — Website + AI Prediksi Permintaan |

**Termasuk:** file website sesuai demo; panduan instalasi; login admin default
di dalam panduan (aturan 22 Nov 13:28); garansi perbaikan bug 30–60 hari.
**Tidak termasuk:** domain, hosting, pemasangan ke hosting pembeli, ubah desain
di luar demo, source code bebas lisensi ulang — beli demo TIDAK otomatis berarti
punya hak cipta, source code, atau hak jual ulang (tergantung lisensi; lisensi
ikut pasar — Cipta 22 Nov 13:30–13:31).
**Dasar harga pasar:** template HTML dasar $9–$29, standar $29–$59,
premium $59–$99 (ThemeForest terlaris $59–$89).

---

## 2. Pembuatan web — $99 / $299 / $599 (sekali bayar)

Jasa pembuatan website custom sesuai pesanan. **Belum termasuk hosting dan domain:**
hosting + domain TIDAK termasuk — pelanggan bayar sendiri atau bawa sendiri.

**Termasuk:** website custom sesuai pesanan; 2 muka website (customer + admin,
rincian di `data/target-dan-strategi.md` § "Keputusan harga & hak pembeli");
akun admin khusus pembeli (dikirim lewat email + panduan pemilik situs, pembeli
ganti password saat login pertama — aturan 22 Nov 13:28); 1 revisi kecil;
pengerjaan 7 hari kalender; garansi perbaikan bug 30 hari (Pemula) / 60 hari
(Profesional).
**Tidak termasuk:** domain, hosting, SSL berbayar, penulisan konten dari nol,
halaman tambahan di luar paket, redesign besar, iklan, SEO lanjutan.
**Dasar harga pasar:** Fiverr Pro — landing page $150–$300, situs 5–7 halaman
$400–$950, ~10 halaman $1.000–$2.500.

---

## 3. Pembuatan web + free hosting — $119 / $319 / $619 (sekali bayar)

Sama seperti produk 2 (custom, 7 hari kalender, 1 revisi kecil, garansi bug
30/60 hari, 2 muka website, akun admin khusus pembeli), **ditambah hosting
gratis termasuk dalam harga pembuatan**:

- Hosting di Cloudflare Pages (gratis, boleh komersial) — lihat §5.
- Subdomain gratis `namatoko.pages.dev` (atau subdomain di bawah domain kita
  bila sudah ada) — ini yang dimaksud bahasa promo **"free domain"**:
  subdomain gratis, **BUKAN domain .com** — tulis jelas di promo, jangan
  pernah klaim .com gratis.
- Form kontak / keranjang / pembayaran memakai layanan pihak ketiga
  (WhatsApp order, payment link) — Pages statis, tanpa server/database bawaan.

**Tidak termasuk:** domain berbayar (.com/.id/dll — pelanggan beli sendiri bila
mau; kita belum bisa belikan — Cipta 22 Nov 16:45 "beli saat ini belum bisa"),
biaya domain/hosting berbayar apa pun, konten dari nol, halaman tambahan,
redesign besar, iklan, SEO lanjutan.

---

## 4. Penyewaan web + hosting — Rp29.000–Rp49.000/bulan (DRAFT)

Model **Website as a Service (WaaS)** / **sewa website**: kami buatkan website,
kami hosting di domain/hosting kami, kami yang pegang pengelolaan, dashboard,
dan maintenance. Pelanggan hanya memakai websitenya; mau ubah isi, minta ke kami.
Nama global: Website as a Service (WaaS), managed website, subscription website,
website rental/leasing. Nama di Indonesia: sewa website, langganan website,
website siap pakai.

**Berlangganan = sewa** (Cipta 22 Nov 16:56): bayar tiap bulan, website hidup
selama bayar, berhenti bayar → website dimatikan. Website TIDAK jadi milik
pelanggan (kecuali ada opsi beli putus — lihat kontrak di bawah).

### Tier sewa — DRAFT (di dalam rentang Rp29–50 ribu/bulan yang diputuskan Cipta)

| Tier | Harga/bulan | Isi |
|---|---|---|
| Sewa Dasar | **Rp29.000** | 1 website statis dari template demo (§1); subdomain gratis; hosting + SSL termasuk; tanpa jatah update konten |
| Sewa Standar | **Rp39.000** | Sewa Dasar + 1 permintaan update konten/bulan |
| Sewa Plus | **Rp49.000** | Sewa Standar + 1 permintaan update konten/bulan lagi (total 2/bulan) |

**Termasuk di semua tier:** hosting Cloudflare Pages gratis (biaya Rp0 buat
kita); subdomain gratis; SSL; backup; monitoring uptime; dukungan lewat
DM/email. **Tidak termasuk:** domain berbayar, redesign, halaman baru,
penulisan konten dari nol, iklan, SEO lanjutan, update di luar jatah
(dikenakan per permintaan — harga per permintaan BELUM diputuskan, lihat
pertanyaan terbuka).
**Dasar harga pasar Indonesia (riset 22 Nov):** sewa template Rp29 ribu/bln
(KawanSistem), Rp50 ribu/bln (BangunWeb), Rp69 ribu/bln (Wanoh), Rp99–149
ribu/bln (M-One); maintenance saja Rp275 ribu–Rp3 jt/bln. Harga kita sengaja
di ujung bawah pasar (Cipta 22 Nov 16:55: "jasanya jangan mahal") — hidup
karena hosting gratis + build pakai template yang dipakai ulang.

### Kontrak — WAJIB jelas sejak hari pertama

- **Domain (bila pelanggan punya domain sendiri) + konten (teks, foto, logo,
  data bisnis) milik pelanggan.** Desain/template/kode milik penyedia (kami).
- **Berhenti bayar → website dimatikan** setelah masa tenggang yang tertulis
  di perjanjian. Konten pelanggan tetap milik pelanggan dan bisa diekspor.
- **Opsi beli putus (buyout):** pelanggan boleh membeli website jadi miliknya
  — harga buyout BELUM diputuskan (lihat pertanyaan terbuka).
- **Jatah update tertulis** (1–2 permintaan/bulan sesuai tier) — jangan janji
  "unlimited", kalau tidak dukungan memakan margin.
- Minimum masa langganan mengikuti pasar (umumnya 12 bulan) — BELUM diputuskan,
  lihat pertanyaan terbuka.

---

## 5. Hosting & domain — yang dipakai semua produk web

- **Hosting: Cloudflare Pages (gratis).** Boleh dipakai komersial (beda dengan
  GitHub Pages yang melarang jualan). Batas resmi Free (19 Nov 2026):
  100 proyek/akun · 500 build/bulan (dipakai bersama semua proyek) ·
  20.000 file/situs · 25 MiB/file · 100 domain kustom/proyek ·
  bandwidth/request aset statis tidak terbatas. Tanpa SLA/dukungan.
  Statis saja — form/bayar butuh pihak ketiga.
- **Domain: kita BELUM punya domain berbayar.** Yang ada `podcastmeong.github.io`
  dan nanti `*.pages.dev` (gratis). Pelanggan sewa/pembuatan+hosting dapat
  **subdomain gratis**. Domain berbayar (.com dsb) ditunda sampai ada pemasukan
  (Cipta 22 Nov 16:45).
- **Google:** website di subdomain gratis tetap bisa masuk Google — daftarkan
  ke Google Search Console (gratis) atau tunggu Google menemukannya lewat
  tautan. Toko kita sudah terdaftar di Search Console.
- **Batas skala:** 1 proyek = 1 website pelanggan → maks. 100 pelanggan per
  akun Cloudflare gratis. Lewat dari itu: Workers for Platforms, atau pola
  akun per klien (lihat §6).

---

## 6. Catatan risiko — ketentuan Cloudflare §2.2.1(a) (PENTING)

Ketentuan Cloudflare (Self-Serve Subscription Agreement, 12 Sep 2025)
§2.2.1(a) melarang — tanpa izin tertulis Cloudflare — **"rent, lease, loan,
export, or sell access to the Services to any third party, or sign up for the
Services on behalf of a third party"**. Meng-hosting puluhan website klien di
SATU akun Cloudflare milik kami lalu menagih bulanan dapat dibaca sebagai
menjual akses layanan — **statusnya abu-abu, belum ada jawaban resmi
Cloudflare untuk skenario agensi persis ini**.

**Pola aman (menurut diskusi komunitas Cloudflare):** tiap klien punya akun
Cloudflare sendiri dan mengundang kami sebagai developer — atau naik ke produk
yang dirancang untuk skala (Workers for Platforms) saat pelanggan membesar.
**Keputusan operasional:** mulai kecil dulu di akun kita (Cipta 22 Nov 16:53),
pindah ke pola akun per klien begitu ramai. Risiko konsentrasi: bila satu akun
ditangguhkan, semua website di akun itu mati bersamaan.
**Larangan lain yang berlaku:** dilarang memproses/mengumpulkan info kartu
kredit di properti Free (§2.2.1(h)) — checkout pelanggan HARUS via pihak
ketiga (payment gateway / marketplace / WhatsApp order), bukan form kartu di
halaman website itu sendiri.

---

## 7. Pemilik & penanggung jawab

- Pemilik produk: **A14 (Web Dev)** — dibantu A32 (Build) untuk pembuatan,
  A37 (Marketplace) untuk penayangan di marketplace, A25 (Sales) untuk
  penawaran, A26/A27 (CS + pesan masuk) untuk dukungan pelanggan sewa.
- Stok demo produk 1 & bahan sewa produk 4: 15 demo di repo toko
  (`demo-website/`, lihat §1).
- Pendaftaran Master Database: `WEB-001` s.d. `WEB-004` di tabel PRODUCTS
  (`agents/master_database.py`, SEED_PRODUCTS).

---

## 8. Pertanyaan terbuka (butuh keputusan Cipta — jangan ditebak)

1. Tier sewa produk 4 (Rp29/39/49 ribu) masih **DRAFT** — setujui tier + isi
   tiap tier, atau ubah?
2. Harga **buyout** produk 4 (pelanggan membeli website jadi miliknya)?
3. Harga per permintaan update konten di luar jatah tier sewa?
4. Minimum masa langganan produk 4 (pasar umumnya 12 bulan)?
5. ~~Produk 3 (pembuatan + free hosting) harganya sama persis dengan produk 2
   ($99/$299/$599) atau ada selisih karena hosting termasuk?~~ — **DIPUTUSKAN
   22 Nov 17:11: produk 3 = $119/$319/$619 (naik $20/tier dari produk 2,
   karena kita juga mengeluarkan jasa hosting/pengelolaan).**
6. Kapan pindah dari satu akun Cloudflare ke pola akun per klien
   (ambang jumlah pelanggan)?
7. Apakah produk 4 mulai ditawarkan sekarang, atau menunggu staging
   Cloudflare toko-oyen selesai dulu?

---

## Sumber

- Keputusan Cipta 22 Nov 2026 17:02 (4 produk web) + 16:45 (domain berbayar
  belum bisa dibeli) + 16:53 ("buat baru aja lalu sewakan") + 16:55 (harga
  sewa jangan mahal; promo "free domain") + 16:56 (berlangganan = sewa) —
  `~/workspace/catatan/keputusan.md`.
- Riset WaaS/sewa website 22 Nov 2026 (nama, cara kerja, harga global +
  Indonesia, isi bulanan, contoh sukses, batas Cloudflare):
  `~/workspace/research_notes/jasa-website-dikelola-agency-20261122-0948/report.md`.
- Harga demo web + jasa web yang berlaku:
  `data/target-dan-strategi.md` § "Keputusan harga & hak pembeli".
- Syarat 2 muka website + cara kasih admin/password:
  `data/target-dan-strategi.md`; riset
  `~/workspace/research_notes/platform-kdp-printful/website-2-muka.md` dan
  `cara-kasih-admin-password-pembeli.md`.
