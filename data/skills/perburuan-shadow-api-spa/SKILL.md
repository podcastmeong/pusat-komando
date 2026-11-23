# Skill: Perburuan Shadow API & SPA — Endpoint Lama, Tak Terdokumentasi & Beta dari Bundle JavaScript

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`), Kategori 2, butir hunt-shadow-api & hunt-spa-api. Belum pernah dipakai dalam perburuan nyata oleh tim; pola dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target adalah SPA (React, Vue, Angular, atau sejenisnya) dan bundle JavaScript-nya sudah dibedah (`analisis-statis-js`) — lalu ada endpoint/rute berstatus KODE SAJA (ada di kode, belum teramati dipanggil) yang dicurigai masih aktif di backend: endpoint API lama (v1), rute tak terdokumentasi, atau fitur beta yang belum dipublikasikan tapi masih merespons. Dipakai pada tahap recon lanjutan, SETELAH `analisis-statis-js` dan SEBELUM pengujian otorisasi. Bukan untuk bounty agen AI — ini teknik web/API klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Mengumpulkan bundle + chunk, mengklasifikasi shadow, memverifikasi liveness |
| Pengerjaan | **A53 Recon Program** | Memasukkan shadow terverifikasi ke indeks aset |
| Audit | **A60 Security Auditor** | Memvalidasi klasifikasi + bukti liveness sebelum masuk indeks |
| Pemimpin | **Muse** | Putuskan bundle mana yang diburu dan kapan inventaris shadow dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Ekstraksi endpoint dari file JS (AST parsing, source map, pola `fetch`/`axios`)** ada di `analisis-statis-js` — skill ini MENGAMBIL daftar KODE SAJA dari sana sebagai bahan mentah, bukan mengulang pembedahannya. Jangan parse ulang file yang sama dengan cara yang sama.
- **Pemetaan rute teramati + DOM saat crawl** ada di `crawling-browser-headless` — skill ini HANYA untuk yang TIDAK teramati saat crawl (shadow), bukan rute yang sudah terlihat dipakai.
- **Endpoint dari dokumentasi resmi** ada di `penemuan-api-swagger` — shadow adalah kebalikannya: endpoint yang TIDAK ada di dokumentasi. Selisih spesifikasi vs teramati di Gerbang 3 skill itu dicatat sebagai petunjuk, bukan sebagai hasil akhir skill ini.
- **URL/endpoint lama dari arsip (Wayback Machine / CommonCrawl)** ada di `penambangan-data-historis` — sumbernya arsip, bukan bundle SPA. Keduanya saling melengkapi: endpoint lama yang muncul di KEDUA sumber naik prioritas, tapi tetap diverifikasi lewat gerbang skill ini.
- **Pengujian otorisasi pada endpoint shadow yang terbukti aktif** BUKAN bagian skill ini — itu lewat `access-control-differential-analyst` (IDOR/BOLA) dan `pengujian-bfla` (fungsi per peran), setelah liveness terbukti.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Trigger & Scope

- **Trigger:** target SPA in-scope; hasil `analisis-statis-js` berisi ≥1 endpoint/rute berstatus KODE SAJA, ATAU bundle memuat chunk lazy-load yang belum dibedah, ATAU ada petunjuk fitur beta (string `beta`, `featureFlag`, `experiment`, `preview`, versi API ganda `v1`/`v2`).
- **Scope:** hanya endpoint/rute yang KUTIPANNYA berasal dari bundle/chunk target in-scope itu sendiri (file + baris tercatat). Dilarang menebak path dari pola nama (mis. menebak `/api/v1/admin` hanya karena ada `/api/v2/admin`) — tebakan bukan shadow, dan tidak masuk inventaris sebagai fakta.
- **Di luar scope:** endpoint yang sudah TERAMATI saat crawl (itu milik `crawling-browser-headless`); endpoint dari arsip saja tanpa jejak di bundle (itu milik `penambangan-data-historis` sampai ada jejak bundle-nya); endpoint dari dokumentasi resmi (itu milik `penemuan-api-swagger`).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Bundle/endpoint di luar scope = jangan diunduh, jangan dibedah, jangan diprobe.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Probe liveness SATU per satu dengan jeda (rate limit ≤5 req/detik, lihat `scope-and-safety-guardian`); jangan membanjiri server dengan probe massal atau brute-force path.
4. **Tanpa payload di permukaan publik.** Tahap ini hanya MEMBACA (probe baca read-only) — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive. Larang memanggil endpoint shadow yang mengubah/menghapus data di skill ini — tandai saja sebagai "tulis/hapus, belum dipanggil".
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Inventaris shadow bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Jangan mengarang endpoint.** Endpoint shadow harus dikutip dari bundle/chunk + baris; endpoint hasil tebakan ditulis sebagai "dugaan — belum terverifikasi", bukan fakta, dan tidak masuk indeks sebagai fakta.
10. **Jangan memakai feature flag / beta gate milik orang lain.** Mengaktifkan fitur beta hanya pada sesi/akun tes sendiri (bila flag-nya terlihat di kode dan bisa diubah di sisi klien sendiri); jangan mengubah flag, peran, atau akses akun lain, dan jangan memaksa masuk ke fitur beta yang butuh undangan/allowlist orang lain.
11. **Secret yang ditemukan DISENSOR di log (`[REDACTED]`) dan TIDAK dipakai untuk mengakses apa pun** — hanya dicatat sebagai temuan pemetaan (jenis secret + lokasi file/baris).

## Methodology & Payloads

### Klasifikasi shadow (dipakai di Gerbang 2)

| Kelas | Tanda di bundle | Prioritas uji |
|---|---|---|
| Legacy / v1 | Path `/api/v1/...` sementara aplikasi memakai `/api/v2/...`; string `deprecated`, `legacy`, `oldApi` | Tinggi — endpoint lama sering luput dari perbaikan otorisasi |
| Undocumented | Path `/api/...` yang tidak ada di spesifikasi OpenAPI dan tidak teramati saat crawl | Tinggi — tidak ada yang menjaganya |
| Beta / feature-flag | Path di balik cek `if (flags.betaX)` / `isBetaUser` / `experiment`; rute `/beta/...`, `/preview/...` | Sedang — aktif tapi mungkin butuh flag; uji hanya dengan flag sesi sendiri |
| Admin / internal | Path `/admin/...`, `/internal/...`, `/ops/...` yang hanya muncul di chunk admin | Tinggi — tandai, JANGAN probe tulis; probe baca hanya dengan akun tes sendiri |
| Kode mati (dugaan) | String path tanpa pemanggilan `fetch`/router di sekitarnya, atau di chunk yang tidak pernah dimuat | Rendah — tetap dicatat, verifikasi terakhir |

### Pola pengujian (bukan payload eksploitasi — probe baca)

- **Probe liveness read-only:** `GET` (atau metode baca yang dipakai kode) dengan token akun tes sendiri, tanpa body yang mengubah state; bila endpoint butuh parameter, pakai ID/canary milik sendiri.
- **Pembanding baseline:** respons probe dibandingkan dengan baseline (request yang sama ke path yang pasti 404, mis. `/api/v9/tidak-ada-canary`) — lihat Validation Gate.
- **Chunk lazy-load:** periksa peta chunk (`webpackChunk`, `import()` dinamis, file `.chunk.js`) — chunk yang hanya dimuat pada rute tertentu sering menyembunyikan endpoint admin/beta; catat chunk mana memuat endpoint mana.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web/API klasik in-scope dan targetnya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. Pastikan ada bahan mentah: hasil `analisis-statis-js` (daftar KODE SAJA) ATAU bundle/chunk SPA yang belum dibedah penuh.
3. **Standar lulus:** scope tertulis; daftar KODE SAJA tersedia dengan file + baris; bila tidak ada satu pun kandidat KODE SAJA dan tidak ada chunk yang belum dibedah, skill ini tidak dipakai — tulis "tidak berlaku" di log.

### Gerbang 1 — Kumpulkan bundle lengkap (termasuk chunk malas)

1. Kumpulkan SEMUA file JS yang dimuat aplikasi, termasuk chunk lazy-load: dari log jaringan `crawling-browser-headless` (semua `.js`/`.chunk.js` yang teramati) + dari peta `import()` dinamis di bundle utama (nama chunk yang dirujuk kode tapi belum termuat saat crawl).
2. Muat tiap chunk yang dirujuk dengan menjelajahi rute terkait sebagai pengguna asli (akun tes sendiri) — jangan mengunduh chunk dengan tebakan URL; URL chunk harus berasal dari bundle atau log jaringan.
3. Serahkan file baru ke `analisis-statis-js` untuk diekstrak endpoint-nya (jangan bedah di sini).
4. **Standar lulus:** tiap chunk tercatat (dimuat/diruujuk-tapi-belum-dimuat/tidak ditemukan); endpoint baru dari chunk tercatat dengan file + baris. Chunk yang tidak bisa dimuat dicatat alasannya, bukan ditebak isinya.

### Gerbang 2 — Klasifikasi shadow

1. Untuk tiap endpoint/rute KODE SAJA, tentukan kelasnya dari tabel klasifikasi di atas (legacy / undocumented / beta / admin-internal / kode mati) berdasarkan konteks kode di sekitarnya: versi path, string `deprecated`/`beta`/`flag`, lokasi chunk, dan pemakaian di router.
2. Catat juga: versi API yang dipakai aplikasi saat ini (untuk membedakan v1 lama vs v2 aktif), nama feature flag bila ada (nama flag-nya saja, bukan nilainya untuk akun lain), dan apakah endpoint berada di chunk admin/beta.
3. **Standar lulus:** tiap kandidat punya kelas + alasan klasifikasi (kutipan kode) tertulis; kandidat tanpa alasan = "belum diklasifikasi", bukan ditebak kelasnya. Urutkan prioritas: legacy + undocumented + admin-internal dulu.

### Gerbang 3 — Verifikasi liveness (probe baca, baseline vs probe)

1. Ambil BASELINE dulu: request ke path yang pasti tidak ada di API yang sama (`/api/v9/tidak-ada-canary`) dengan token akun tes sendiri — simpan status + panjang body + pola responsnya.
2. Probe tiap kandidat prioritas tinggi SATU per satu, metode baca saja, token akun tes sendiri, parameter canary milik sendiri. JANGAN probe endpoint tulis/hapus — tandai "tulis/hapus, belum dipanggil" dan serahkan ke Muse.
3. Nilai tiap respons terhadap baseline (lihat Validation Gate): respons yang berbeda bermakna dari baseline = AKTIF; sama dengan baseline (404 generik) = TIDAK AKTIF / tidak terbukti; redirect ke login = butuh otorisasi (catat, jangan paksa).
4. **Standar lulus:** tiap kandidat prioritas tinggi punya verdict (AKTIF / TIDAK AKTIF / BUTUH OTORISASI / TULIS-HAPUS-BELUM-DIPROBE) + bukti responsnya. Kandidat tanpa perbandingan baseline = belum diuji.

### Gerbang 4 — Serahkan ke indeks + audit

1. Serahkan endpoint shadow AKTIF ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`), dengan kelas + bukti liveness + catatan otorisasi (token/peran apa — bila belum diketahui, tulis "otorisasi belum diketahui" dan entri = BELUM DIPETAKAN).
2. A60 mengaudit: tiap entri bisa dilacak ke bundle + baris dan ke bukti probe; tidak ada dugaan sebagai fakta; tidak ada endpoint tulis/hapus yang dipanggil di skill ini; secret tersensor.
3. **Standar lulus:** audit A60 lolos; indeks diperbarui; endpoint AKTIF dengan otorisasi belum diketahui = BELUM DIPETAKAN dan tidak boleh diuji otorisasinya sebelum dicatat.

## Validation Gate

Verifikasi deterministik baseline vs probe — WAJIB sebelum endpoint shadow dinyatakan AKTIF:

1. **Baseline tercatat** (status + panjang body + hash ringkas respons 404-canary) SEBELUM probe apa pun.
2. **Probe dibedakan dari baseline** pada minimal SATU dimensi yang bermakna: status berbeda (mis. 200/401/403 vs 404 baseline), ATAU struktur body berbeda (bukan sekadar panjang), ATAU pesan error menyebut resource/parameter itu.
3. **Ulangi sekali** untuk kandidat yang dinyatakan AKTIF: probe kedua dengan parameter canary berbeda harus memberi respons yang konsisten (bukan kebetulan sekali jalan).
4. **Yang TIDAK lolos gate:** respons identik dengan baseline (= tidak aktif); respons 404 dengan body yang sama persis (= tidak terbukti); probe yang memakai data orang lain (= batal, hapus dari log, laporkan ke Muse). Satu gate gagal = verdict TIDAK AKTIF / BELUM TERBUKTI, bukan AKTIF.

## Alat

| Alat | Cara pakai |
|---|---|
| `analisis-statis-js` | Ekstraksi endpoint dari bundle + chunk (Gerbang 1); sumber daftar KODE SAJA (Gerbang 0). |
| `crawling-browser-headless` | Log jaringan (daftar chunk yang dimuat) + memuat chunk lewat navigasi sebagai pengguna asli. |
| Browser / curl (permintaan HTTP biasa) | Probe liveness read-only satu per satu; simpan responsnya. |
| `penemuan-api-swagger` | Pembanding: mana yang tidak ada di spesifikasi (undocumented). |
| `penambangan-data-historis` | Pembanding: endpoint lama yang juga muncul di arsip naik prioritas. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi perburuan shadow. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Perburuan shadow API/SPA — <program/target> — <tanggal>
- Bundle + chunk: <n> file (baru: <n> chunk lazy-load dimuat, <n> belum dimuat)
- Kandidat KODE SAJA: <n> (legacy: <n>, undocumented: <n>, beta: <n>, admin/internal: <n>, kode mati: <n>)
- Baseline: <status + panjang body + hash ringkas>
- Verdict liveness: <n> AKTIF, <n> TIDAK AKTIF, <n> BUTUH OTORISASI, <n> TULIS-HAPUS-BELUM-DIPROBE
- Per endpoint AKTIF: <metode path> | <kelas> | <file:baris> | <bukti probe vs baseline> | <otorisasi: diketahui/belum>
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; pembedahan dilakukan lokal pada salinan bundle, probe lewat HTTP biasa.

### Websites

- Halaman aturan program resmi (sumber scope Gerbang 0).
- Dokumentasi framework SPA target (cara chunk lazy-load dimuat — untuk melacak `import()` dinamis).

### Alternatives for better results

- Bila bundle ter-obfuscate berat dan kelas tidak bisa ditentukan: catat sebagai "belum diklasifikasi", serahkan ke Muse — jangan menebak kelas dari nama variabel acak.
- Bila endpoint beta butuh flag yang tidak dimiliki akun tes: catat sebagai "BUTUH OTORISASI / flag beta", jangan mencoba flag akun lain atau memaksa allowlist.
- Bila semua kandidat ternyata TIDAK AKTIF (sama dengan baseline): itu hasil yang sah — tulis "tidak ada shadow aktif", jangan menaikkan volume probe untuk memaksa hasil.
