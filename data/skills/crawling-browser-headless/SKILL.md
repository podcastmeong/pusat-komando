# Skill: Crawling Browser Headless — Render Aplikasi JS Modern & Petakan DOM + Alur Navigasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 13. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target adalah aplikasi web modern (React, Vue, Angular, atau SPA lain) yang konten dan rutenya baru muncul setelah JavaScript di-render — crawler HTTP biasa (yang hanya membaca HTML awal) tidak melihat apa-apa. Dipakai pada tahap recon teknis, SEBELUM pengujian: hasilnya adalah peta DOM + alur navigasi yang masuk ke indeks aset (`pemetaan-permukaan-serangan`), bukan temuan kerentanan. Bukan untuk bounty agen AI — di Muse, OpenAI, 0din, Google AI VRP, dan ViKernel yang dinilai adalah HASIL/outcome pada agennya, bukan crawling web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Menjalankan crawl headless, memetakan DOM + alur navigasi |
| Pengerjaan | **A53 Recon Program** | Memasukkan hasil crawl ke indeks aset |
| Pemimpin | **Muse** | Putuskan target mana yang di-crawl dan kapan peta dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Inventaris aset & endpoint** hasil akhirnya ada di `pemetaan-permukaan-serangan` — skill ini adalah CARA mengisi indeks itu untuk aplikasi JS modern, bukan pengganti indeksnya. Semua rute/endpoint hasil crawl WAJIB masuk indeks sebelum diuji.
- **Crawl HTTP sederhana** (tanpa render JS) sudah tercakup sebagai tool di `mcp-security-hub` (katana) — skill ini beda: render penuh di browser headless untuk SPA, bukan crawl HTTP mentah.
- **Uji live lewat browser** ada di `uji-live-browser` — skill itu menguji SATU alur secara manual lewat browser task; skill ini memetakan SELURUH aplikasi secara sistematis. Jangan campur keduanya.
- **Penjaga scope & rate limit** ada di `scope-and-safety-guardian` — skill ini memakai batasnya, bukan menulis ulang.
- **Analisis file JS hasil crawl** (endpoint tersembunyi, token) ada di `analisis-statis-js` — skill ini hanya MENGUMPULKAN file JS-nya; pembedahannya skill itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Target di luar scope = HENTIKAN, jangan di-crawl.
2. **Hanya akun sendiri + canary palsu.** Crawl hanya sebagai pengguna yang login dengan akun tes sendiri; tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** (lihat `scope-and-safety-guardian`); crawl satu target dalam satu sesi; jeda antar halaman; tanpa crawl paralel massal.
4. **Tanpa payload di permukaan publik.** Crawling hanya MENGAMATI dan MENCATAT — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Peta crawl bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja; crawl otomatis pada challenge huntr DILARANG); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Bila program melarang otomasi, crawl otomatis DILARANG** — lakukan pemetaan manual setara (klik alur sebagai pengguna asli) atau jangan jalankan sama sekali; bila ragu, tanya Muse dulu.
10. **Jangan crawl di luar indeks.** Hanya URL/rute yang tercatat di indeks aset yang boleh dijelajahi; jangan menebak path atau mengikuti tautan ke domain di luar scope.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web klasik in-scope dan targetnya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. Cek larangan otomasi program dan catat statusnya di log.
3. **Standar lulus:** scope tertulis; status larangan otomasi tercatat; target adalah SPA/aplikasi JS (bukan situs statis — bila statis, pakai katana di `mcp-security-hub`, bukan skill ini). Satu gagal = STOP.

### Gerbang 1 — Siapkan browser headless

1. Siapkan browser headless (Playwright atau Puppeteer — pilih satu yang tersedia di lab; jangan memasang keduanya) dengan profil bersih, tanpa ekstensi pihak ketiga yang tidak dikenal.
2. Atur: viewport desktop standar, JavaScript aktif, blokir permintaan ke domain pihak ketiga di luar scope, dan simpan log jaringan (request/response) selama crawl.
3. Login HANYA dengan akun tes sendiri bila aplikasi butuh login; jangan simpan kredensial di skrip crawl (baca dari sesi login manual, bukan dari file berisi kata sandi).
4. **Standar lulus:** satu halaman uji in-scope berhasil di-render (DOM terisi setelah JS jalan, bukan HTML kosong); log jaringan tercatat. Bila render gagal, catat errornya, jangan lanjut.

### Gerbang 2 — Crawl alur navigasi sebagai pengguna asli

1. Jelajahi aplikasi mengikuti alur pengguna sungguhan: halaman utama → login → dashboard → tiap menu/fitur → form → halaman admin (bila akun tes punya akses itu). Klik tautan dan tombol, isi form dengan data canary palsu saja.
2. Untuk tiap halaman catat: URL/rute, judul, komponen utama, form + field-nya, dan aksi yang tersedia (tombol/endpoint yang dipanggil).
3. **Standar lulus:** tiap rute in-scope yang terlihat di navigasi tercatat dengan field + aksinya; rute yang tidak bisa dijangkau dicatat sebagai "belum terpetakan" dengan alasannya, bukan ditebak.

### Gerbang 3 — Petakan DOM + panggil API yang teramati

1. Dari log jaringan selama crawl, catat SEMUA request yang dibuat aplikasi: metode, path API, parameter, dan header otorisasi yang dipakai (jenis tokennya saja — JANGAN salin nilai token ke log).
2. Petakan hubungan DOM → API: elemen/form mana yang memanggil endpoint mana.
3. Kumpulkan daftar file JS yang dimuat untuk diserahkan ke `analisis-statis-js` (jangan bedah di sini).
4. **Standar lulus:** tiap endpoint teramati punya metode + parameter + catatan otorisasi; file JS terkumpul dengan URL sumbernya; tidak ada nilai token/rahasia tertulis di log (bila tertulis, sensor jadi `[REDACTED]`).

### Gerbang 4 — Bekukan peta + serahkan ke indeks

1. Serahkan peta DOM + alur navigasi + daftar endpoint teramati ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`).
2. **Standar lulus:** indeks diperbarui (tiap entri punya metode, parameter, otorisasi); entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji. Peta yang belum masuk indeks = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| Playwright ATAU Puppeteer (pilih satu) | Browser headless untuk render SPA + merekam log jaringan. Ambil cara instalasi/pakai dari dokumentasi resminya saat setup — jangan mengarang flag. |
| katana (via `mcp-security-hub`) | Pembanding crawl HTTP mentah — untuk memastikan rute yang hanya muncul setelah render JS memang tidak terlihat tanpa browser. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `analisis-statis-js` | Lanjutan: bedah file JS yang dikumpulkan Gerbang 3. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi crawl. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Crawl headless — <program/target> — <tanggal>
- Alat: <Playwright/Puppeteer + versi> | larangan otomasi program: <diizinkan/dilarang + sumber>
- Rute terpetakan: <n> rute (daftar: <rute> — <form/aksi>)
- Endpoint teramati: <n> endpoint (metode + path + parameter + otorisasi)
- File JS dikumpulkan: <n> file → diserahkan ke analisis-statis-js
- Belum terpetakan: <n> rute (alasan)
- Indeks: <path file indeks aset>
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; browser headless dijalankan lokal.

### Websites

- Dokumentasi Playwright (playwright.dev) dan Puppeteer (pptr.dev) — cara setup browser headless.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila target situs statis / server-rendered: jangan pakai browser headless — pakai katana di `mcp-security-hub` (lebih ringan, lebih cepat).
- Bila crawl mentok (bot-check/CAPTCHA): berhenti, catat sebagai "belum terpetakan", dan serahkan ke Muse — jangan memaksa dengan pemindaian agresif atau solver CAPTCHA pihak ketiga. Lihat playbook CAPTCHA di `uji-live-browser`.
- Bila file JS ter-obfuscate dan endpoint tak terlihat: serahkan daftar file ke `analisis-statis-js`, jangan menebak endpoint.
