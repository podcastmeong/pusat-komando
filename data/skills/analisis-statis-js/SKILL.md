# Skill: Analisis Statis JS — Bedah File .js & Source Map (AST Parsing)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 14. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat sudah ada daftar file JavaScript target (dari `crawling-browser-headless` atau dari `pemetaan-permukaan-serangan` langkah 4) dan file-file itu harus dibedah untuk menemukan endpoint tersembunyi, rute admin, parameter tak terdokumentasi, dan token/konfigurasi — sebelum pengujian apa pun. Dipakai juga saat aplikasi memuat source map (`.js.map`) yang terekspos: source map membongkar kode asli di balik bundle yang ter-minify. Bukan untuk bounty agen AI — ini teknik web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Mengumpulkan + membedah file JS dan source map, mencatat temuan |
| Audit | **A60 Security Auditor** | Memvalidasi temuan sebelum masuk indeks (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Putuskan file mana yang dibedah dan kapan temuan masuk indeks |

## Sudah tercakup (jangan diduplikat)

- **Langkah pengumpulan JS + pencatatan temuan kasar** sudah ada di `pemetaan-permukaan-serangan` langkah 4 — skill ini adalah PEMBEDAHAN MENDALAM-nya (AST parsing, source map, pola pencarian sistematis), bukan pengganti langkah itu. Temuan skill ini WAJIB kembali ke indeks aset di sana.
- **Analisis kode sumber repo** (bukan JS hasil unduhan dari browser) ada di `kopilot-analisis-kode` — skill itu membaca kode yang legal dibaca dari repo; skill ini membedah file JS yang DIMUAT aplikasi target saat berjalan. Jangan campur keduanya.
- **Panen endpoint dari JS lewat Burp MCP** sudah ada sebagai tool di `mcp-burp-ultra` Gerbang 2 — itu panen otomatis lewat proxy; skill ini adalah analisis statis mandiri (AST + source map + pola) yang hasilnya bisa dicek silang dengan panen Burp. Bila keduanya ada, pakai keduanya dan catat selisihnya.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak` — skill ini hanya menemukan HIPOTESIS, bukan membuktikan celah.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). File JS di luar scope = jangan diunduh, jangan dibedah.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Unduh file JS yang teramati saat memakai aplikasi sebagai pengguna asli saja; jangan membanjiri server dengan permintaan unduhan massal (rate limit ≤5 req/detik).
4. **Tanpa payload di permukaan publik.** Analisis ini hanya MEMBACA kode — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Temuan analisis JS bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Secret yang ditemukan DISENSOR di log (`[REDACTED]`) dan TIDAK dipakai untuk mengakses apa pun** — hanya dicatat sebagai temuan pemetaan (jenis secret + lokasi file/baris). Memakai secret orang lain untuk login/mengakses = pelanggaran.
10. **Jangan mengarang endpoint.** Endpoint yang ditemukan harus dikutip dari file + baris; endpoint hasil tebakan dari pola nama ditulis sebagai "dugaan — belum terverifikasi", bukan fakta, dan tidak masuk indeks sebagai fakta.

## Langkah + gerbang

### Gerbang 0 — Kumpulkan file JS yang legal dianalisis

1. Ambil daftar file JS dari hasil `crawling-browser-headless` Gerbang 3 atau dari `pemetaan-permukaan-serangan` langkah 4 — hanya file yang dimuat aplikasi target in-scope saat dipakai sebagai pengguna asli.
2. Unduh salinannya ke folder kerja lokal (satu folder per target + tanggal); catat URL sumber + tanggal unduh tiap file.
3. **Standar lulus:** tiap file punya URL sumber tercatat; tidak ada file dari domain di luar scope. File tanpa sumber = jangan dibedah.

### Gerbang 1 — Pulihkan source map bila ada

1. Untuk tiap file `.js`, cek apakah ada source map: komentar `//# sourceMappingURL=...` di akhir file, atau coba URL yang sama dengan akhiran `.map`.
2. Bila source map ditemukan dan bisa diunduh, pulihkan kode aslinya (nama file, nama fungsi, struktur direktori asli) — ini sering membongkar rute dan logika yang hilang di bundle minify.
3. **Standar lulus:** tiap file tercatat status source map-nya (ada/tidak ada/404); source map yang ada dipulihkan dan disimpan bersama file aslinya. Source map yang tidak ada BUKAN kegagalan — lanjut ke Gerbang 2 dengan bundle minify.

### Gerbang 2 — Parse AST + cari pola (bukan grep buta)

1. Parse tiap file menjadi AST (mis. dengan parser JS seperti Acorn/Babel — pilih satu yang tersedia; jangan menulis parser sendiri) agar pencarian memahami struktur kode, bukan sekadar teks.
2. Cari secara sistematis lewat AST + pola string: pemanggilan `fetch`/`axios`/`XMLHttpRequest` (URL + metode + body), definisi rute/router (path + komponen), string yang mengandung `/api/`, `/admin/`, `/internal/`, kunci konfigurasi, dan pemakaian `localStorage`/`sessionStorage`/cookie.
3. Untuk tiap temuan catat: file + baris/konteks, jenis temuan (endpoint/rute admin/parameter/token/konfigurasi), dan nilai persisnya (kecuali secret — sensor).
4. **Standar lulus:** tiap file punya daftar temuan dengan file + baris; tidak ada temuan tanpa lokasi; secret tersensor. Pencarian hanya-grep tanpa AST dicatat sebagai "pencarian dangkal" dan hasilnya ditandai belum lengkap.

### Gerbang 3 — Bedakan endpoint nyata vs string mati

1. Untuk tiap endpoint/rute kandidat, tentukan statusnya: (a) TERAMATI — sudah terlihat dipanggil saat crawl/pemakaian asli; (b) KODE SAJA — ada di kode tapi belum terlihat dipanggil (mungkin rute admin, fitur lama, atau kode mati); (c) DUGAN — hasil tebakan pola, bukan kutipan kode.
2. Hanya (a) dan (b) yang diteruskan; (c) ditulis terpisah sebagai dugaan dan TIDAK masuk indeks sebagai fakta.
3. **Standar lulus:** tiap kandidat punya status (a)/(b)/(c) tertulis; tidak ada dugaan yang lolos sebagai fakta ke indeks.

### Gerbang 4 — Serahkan ke indeks + audit

1. Serahkan daftar endpoint/rute/parameter hasil Gerbang 3 ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`), dengan catatan otorisasi tiap endpoint (token/peran apa — bila belum diketahui, tulis "otorisasi belum diketahui" dan entri = BELUM DIPETAKAN).
2. A60 mengaudit: tiap temuan bisa dilacak ke file + baris; secret tersensor; tidak ada dugaan sebagai fakta.
3. **Standar lulus:** audit A60 lolos; indeks diperbarui; entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji.

## Alat

| Alat | Cara pakai |
|---|---|
| Parser JS (Acorn atau Babel — pilih satu) | Parse file JS jadi AST; ambil cara pakai dari dokumentasi resminya, jangan mengarang API. |
| Tool pemulih source map (mis. `source-map` / shuji — pilih yang tersedia) | Pulihkan kode asli dari `.js.map`; bila tidak ada tool, catat dan lanjut manual. |
| `crawling-browser-headless` | Sumber daftar file JS (Gerbang 0). |
| `mcp-burp-ultra` Gerbang 2 | Pembanding: panen endpoint JS lewat Burp — cek silang hasilnya dengan Gerbang 2 skill ini. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi analisis. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Analisis statis JS — <program/target> — <tanggal>
- File dibedah: <n> file (.js + .js.map bila ada)
- Source map: <n> ditemukan/dipulihkan, <n> tidak ada
- Temuan: <n> endpoint, <n> rute admin, <n> parameter, <n> secret [REDACTED]
- Per temuan: <file:baris> | <jenis> | <nilai> | <status: TERAMATI/KODE SAJA/DUGAAN>
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; analisis dilakukan lokal pada salinan file.

### Websites

- Dokumentasi Acorn (acornjs.org) / Babel (babeljs.io) — cara parse AST.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila file JS ter-obfuscate berat dan AST tidak membantu: catat sebagai "belum terpetakan", serahkan ke Muse — jangan menebak endpoint dari nama variabel acak.
- Bila tidak ada source map dan bundle sangat besar: prioritaskan file yang memuat string `/api/` atau `fetch` (Gerbang 2), jangan bedah semua file sekaligus.
- Bila targetnya kode repo (bukan JS hasil unduhan browser): pakai `kopilot-analisis-kode`, bukan skill ini.
