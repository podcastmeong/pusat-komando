# Skill: Penemuan API & Swagger — Dokumentasi API Terekspos (OpenAPI/Swagger)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 16. Belum pernah dipakai dalam perburuan nyata oleh tim; daftar path dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target diduga mengekspos dokumentasi API-nya (OpenAPI/Swagger) di path yang umum — `/swagger.json`, `/api-docs`, `/v1/openapi.yaml`, `/openapi.json`, `/docs`, `/redoc` — atau saat endpoint API perlu diinventarisasi dari spesifikasi resmi, bukan dari tebakan. Dipakai pada tahap recon teknis; hasilnya masuk ke indeks aset (`pemetaan-permukaan-serangan`). Bukan untuk bounty agen AI — ini teknik web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Memeriksa path dokumentasi API, mem-parse spesifikasi, menyusun inventaris endpoint |
| Pengerjaan | **A59 Threat Hunter** | Mencocokkan spesifikasi dengan yang teramati di JS/crawl |
| Pemimpin | **Muse** | Putuskan target mana yang diperiksa dan kapan inventaris dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Inventaris endpoint dari dokumentasi resmi** sudah disinggung di `pemetaan-permukaan-serangan` langkah 5 dan `rekonstruksi-iterasi-payload` Gerbang 1 ("OpenAPI/Swagger bila tersedia") — keduanya MENGASUMSIKAN dokumentasi sudah ditemukan; skill ini adalah CARA MENEMUKAN dan MEM-PARSE-nya. Jangan duplikat langkah inventarisasinya — skill ini menyerahkan hasilnya ke sana.
- **Endpoint yang teramati dari crawl/JS** ada di `crawling-browser-headless` dan `analisis-statis-js` — skill ini melengkapinya dengan spesifikasi resmi; selisih antara spesifikasi dan yang teramati dicatat, bukan diabaikan.
- **GraphQL** BUKAN bagian skill ini — lihat `introspeksi-graphql`.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Path dokumentasi di luar scope = jangan diperiksa.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Periksa daftar path umum SATU per satu dengan jeda (rate limit ≤5 req/detik); jangan membanjiri server dengan brute-force path massal.
4. **Tanpa payload di permukaan publik.** Penemuan ini hanya MEMBACA dokumentasi — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Inventaris API bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Jangan mengarang endpoint dari spesifikasi lain.** Endpoint yang masuk indeks harus berasal dari spesifikasi target itu sendiri atau dari pengamatan langsung; jangan menyalin path dari dokumentasi program lain.
10. **Jangan memakai kredensial dari spesifikasi.** Bila spesifikasi berisi contoh token/kunci, SENSOR (`[REDACTED]`) dan JANGAN dipakai untuk mengakses apa pun — hanya dicatat sebagai temuan pemetaan.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web/API klasik in-scope dan targetnya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. **Standar lulus:** scope tertulis; target diketahui punya API (dari crawl, JS, atau dokumentasi program). Bila target tidak punya API sama sekali, skill ini tidak dipakai — tulis "tidak berlaku" di log.

### Gerbang 1 — Periksa path dokumentasi umum

1. Periksa SATU per satu path yang umum (dengan jeda): `/swagger.json`, `/swagger.yaml`, `/api-docs`, `/api/docs`, `/openapi.json`, `/openapi.yaml`, `/v1/openapi.yaml`, `/v2/api-docs`, `/docs`, `/redoc`, `/graphql` (bila yang ini yang merespons, serahkan ke `introspeksi-graphql`, jangan lanjut di sini).
2. Catat tiap path: status HTTP, jenis konten, dan apakah isinya spesifikasi OpenAPI/Swagger yang valid atau halaman dokumentasi lain.
3. Periksa juga tautan dokumentasi dari halaman utama aplikasi, footer, dan dari file JS (`analisis-statis-js` — string `/api-docs`, `swagger`).
4. **Standar lulus:** tiap path tercatat status + isinya; path yang 404 dicatat sebagai tidak ada, bukan diulang-ulang. Satu path valid = lanjut ke Gerbang 2; tidak ada yang valid = tulis "tidak ditemukan" dan lanjut ke Gerbang 3 (cek silang).

### Gerbang 2 — Parse spesifikasi + susun inventaris

1. Unduh salinan spesifikasi ke folder kerja lokal (satu file per target + tanggal); parse sebagai OpenAPI/Swagger (JSON/YAML).
2. Untuk tiap operasi dalam spesifikasi catat: metode, path, parameter (query/path/body/header), skema respons, dan catatan otorisasi yang tertulis di spesifikasi (skema security apa — jenisnya saja, bukan nilai token).
3. Tandai operasi yang sensitif (admin, hapus, ubah peran, baca data massal) — tandai saja, JANGAN diuji di skill ini.
4. **Standar lulus:** tiap operasi punya metode + path + parameter + catatan otorisasi tertulis; spesifikasi tersimpan lokal; contoh token/kunci tersensor. Operasi tanpa catatan otorisasi = BELUM DIPETAKAN.

### Gerbang 3 — Cek silang dengan yang teramati

1. Bandingkan inventaris spesifikasi dengan endpoint yang teramati dari `crawling-browser-headless` dan `analisis-statis-js`: mana yang ada di keduanya, mana yang hanya di spesifikasi (mungkin endpoint lama/tersembunyi), mana yang hanya teramati (mungkin tidak terdokumentasi).
2. Endpoint yang hanya ada di spesifikasi dicatat dengan status "SPESIFIKASI SAJA — belum teramati"; endpoint yang hanya teramati dicatat "TERAMATI SAJA — tidak terdokumentasi".
3. **Standar lulus:** selisih tercatat lengkap; tidak ada endpoint spesifikasi yang langsung dinyatakan "aktif" tanpa pengecekan — statusnya tetap "spesifikasi saja" sampai ada pengamatan atau pengujian yang membuktikannya.

### Gerbang 4 — Serahkan ke indeks

1. Serahkan inventaris ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`).
2. **Standar lulus:** indeks diperbarui; entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji; operasi sensitif ditandai dan belum diuji.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser / curl (permintaan HTTP biasa) | Memeriksa path dokumentasi satu per satu; simpan responsnya. |
| Parser OpenAPI (mis. pustaka OpenAPI/Swagger di Python/Node — pilih yang tersedia) | Parse spesifikasi JSON/YAML jadi daftar operasi; ambil cara pakai dari dokumentasinya, jangan mengarang. |
| `crawling-browser-headless` + `analisis-statis-js` | Sumber pembanding Gerbang 3. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi penemuan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Penemuan API/Swagger — <program/target> — <tanggal>
- Path diperiksa: <n> path (daftar + status HTTP tiap path)
- Spesifikasi ditemukan: <ya/tidak> | <path + versi OpenAPI> | <file lokal tersimpan>
- Operasi di spesifikasi: <n> operasi (<n> sensitif, ditandai saja)
- Cek silang: <n> di keduanya, <n> spesifikasi saja, <n> teramati saja
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; pemeriksaan dilakukan lewat HTTP biasa.

### Websites

- Spesifikasi OpenAPI (spec.openapis.org) — format yang di-parse.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila tidak ada path dokumentasi yang merespons: jangan brute-force ribuan path — andalkan `crawling-browser-headless` + `analisis-statis-js` untuk inventaris endpoint, dan catat "dokumentasi tidak terekspos".
- Bila spesifikasi yang ditemukan ternyata milik layanan pihak ketiga (bukan target): jangan masukkan ke indeks target — catat sebagai temuan terpisah dan tanya Muse.
- Bila spesifikasi versi lama (v1) dan aplikasi sudah v2: catat versi + tanggal spesifikasi; endpoint v1 yang tidak teramati tetap berstatus "spesifikasi saja".
