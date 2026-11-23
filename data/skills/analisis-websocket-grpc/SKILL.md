# Skill: Analisis WebSocket & gRPC — Pemetaan Komunikasi Real-Time & Protokol Biner

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 19. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target memakai komunikasi di luar HTTP biasa — WebSocket (notifikasi live, chat, kolaborasi real-time) atau gRPC (panggilan prosedur biner, sering di balik aplikasi mobile dan layanan internal) — dan komunikasi itu perlu dipetakan: pesan apa yang dipertukarkan, metode apa yang tersedia, dan data apa yang mengalir. Dipakai pada tahap recon teknis; hasilnya masuk ke indeks aset (`pemetaan-permukaan-serangan`). Bukan untuk bounty agen AI — ini teknik web/API klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Merekam lalu lintas WebSocket/gRPC, memetakan pesan + metode |
| Pengerjaan | **A59 Threat Hunter** | Menganalisis skema pesan (proto) dan mencocokkan dengan JS/kode |
| Pemimpin | **Muse** | Putuskan target mana yang dipetakan dan kapan peta dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Pemetaan HTTP/REST biasa** ada di `pemetaan-permukaan-serangan`, `penemuan-api-swagger`, dan `crawling-browser-headless` — skill ini HANYA untuk lalu lintas non-HTTP (WebSocket + gRPC). Jangan campur peta HTTP dan peta real-time dalam satu daftar tanpa label.
- **Rekam lalu lintas lewat proxy Burp** ada di `mcp-burp-official` / `mcp-burp-ultra` Gerbang 2 — itu perekam HTTP-nya; skill ini adalah WORKFLOW memetakan pesan WebSocket dan metode gRPC dari rekaman itu (plus perekaman khusus gRPC yang tidak ditangkap proxy HTTP biasa).
- **Analisis file JS yang memuat URL WebSocket** ada di `analisis-statis-js` — skill itu menemukan alamat endpoint-nya; skill ini memetakan ISI komunikasinya.
- **Pengujian celah pada pesan/metode yang dipetakan** BUKAN bagian skill ini — itu lewat `rekonstruksi-iterasi-payload` + `access-control-differential-analyst`, setelah peta selesai.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Endpoint WebSocket/gRPC di luar scope = jangan direkam, jangan dipetakan.
2. **Hanya akun sendiri + canary palsu.** Rekam hanya sesi milik akun tes sendiri; tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Rekam lalu lintas pemakaian normal sebagai pengguna asli saja; jangan membanjiri koneksi dengan pesan massal; rate limit ≤5 req/detik untuk panggilan gRPC yang dipicu manual.
4. **Tanpa payload di permukaan publik.** Pemetaan ini hanya MENGAMATI dan MENCATAT — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive. Larang memanggil metode gRPC yang mengubah/menghapus data di skill ini — pemetaan hanya memakai panggilan BACA.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Peta komunikasi bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Bila rekaman mengandung data pengguna lain, HENTIKAN, sensor, dan laporkan ke Muse** — jangan dibaca lanjut, jangan disimpan utuh. Simpan hanya struktur pesannya (nama field + jenis), bukan isinya.
10. **Bila program melarang otomasi, perekaman otomatis massal DILARANG** — lakukan pemetaan manual (pakai aplikasi sebagai pengguna asli, rekam satu alur sekali jalan) atau jangan jalankan; bila ragu, tanya Muse dulu.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web/API klasik in-scope dan targetnya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. Pastikan target benar-benar memakai WebSocket dan/atau gRPC (dari file JS: string `ws://`/`wss://`/`.proto`, dari crawl: koneksi WebSocket di log jaringan, atau dari dokumentasi program).
3. **Standar lulus:** scope tertulis; jenis komunikasi tertulis (WebSocket saja / gRPC saja / keduanya) dengan bukti penemunya. Bila target hanya HTTP biasa, skill ini tidak dipakai — tulis "tidak berlaku" di log.

### Gerbang 1 — Rekam lalu lintas sebagai pengguna asli

1. Pakai aplikasi sebagai pengguna asli dengan akun tes sendiri (login, buka fitur real-time, kirim pesan/chat/notifikasi canary palsu) sambil merekam lalu lintas: untuk WebSocket, rekam lewat log jaringan browser headless (`crawling-browser-headless`) atau proxy yang mendukung WebSocket (`mcp-burp-official`); untuk gRPC, rekam lewat proxy yang mendukung HTTP/2 atau dari file `.proto`/definisi layanan bila tersedia.
2. Simpan rekaman mentah ke folder kerja lokal (satu file per sesi + tanggal); catat alur pengguna yang dilakukan saat merekam.
3. **Standar lulus:** rekaman tersimpan dengan alur tercatat; tidak ada data pengguna lain di rekaman (bila ada, sensor/hentikan sesuai Aturan Keras poin 9). Rekaman tanpa alur tercatat = belum bisa dipetakan.

### Gerbang 2 — Petakan pesan WebSocket

1. Dari rekaman, susun daftar jenis pesan: arah (klien→server / server→klien), nama/jenis pesan, field + jenis datanya, dan pemicu (aksi pengguna apa yang mengirimnya).
2. Tandai pesan yang membawa data sensitif (token, ID pengguna lain, isi pribadi) — tandai saja, JANGAN salin isinya ke log (tulis jenis datanya saja).
3. **Standar lulus:** tiap jenis pesan punya arah + field + pemicu tertulis; tidak ada isi sensitif tertulis di log. Pesan tanpa pemicu = "belum dipetakan", bukan ditebak.

### Gerbang 3 — Petakan metode gRPC

1. Dari rekaman dan/atau file `.proto`/definisi layanan yang tersedia, susun daftar layanan + metode: nama layanan, nama metode, jenis panggilan (unary / streaming server / streaming klien / dua arah), pesan request/response + field-nya.
2. Bila tidak ada file `.proto`, rekonstruksi nama metode dari path HTTP/2 yang teramati (`/paket.Layanan/Metode`) — catat sebagai "hasil pengamatan", bukan dari spesifikasi.
3. Tandai metode yang mengubah data (tulis/menghapus) — tandai saja, JANGAN dipanggil di skill ini (hanya metode baca yang boleh dipanggil untuk konfirmasi, dan hanya dengan data canary).
4. **Standar lulus:** tiap metode punya layanan + jenis panggilan + pesan request/response tertulis; metode tulis/hapus ditandai dan belum dipanggil.

### Gerbang 4 — Serahkan ke indeks + audit

1. Serahkan peta pesan WebSocket + metode gRPC ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`), dengan catatan otorisasi tiap pesan/metode (token/peran apa — bila belum diketahui, tulis "otorisasi belum diketahui" dan entri = BELUM DIPETAKAN).
2. A60 mengaudit: tiap entri bisa dilacak ke rekaman; tidak ada isi sensitif di log; tidak ada metode tulis/hapus yang dipanggil di skill ini.
3. **Standar lulus:** audit A60 lolos; indeks diperbarui; entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser headless / proxy WebSocket (via `crawling-browser-headless`, `mcp-burp-official`) | Merekam lalu lintas WebSocket selama pemakaian normal. |
| Proxy HTTP/2 atau klien gRPC (mis. grpcurl / BloomRPC — pilih satu yang tersedia) | Memeriksa metode gRPC dan memanggil metode BACA untuk konfirmasi. Ambil cara pakai dari dokumentasi resminya, jangan mengarang flag. |
| File `.proto` / definisi layanan (bila tersedia dari JS, aplikasi mobile, atau dokumentasi) | Sumber nama layanan + metode Gerbang 3; bila tidak ada, rekonstruksi dari pengamatan. |
| `analisis-statis-js` + `dekompilasi-aplikasi-mobile` | Sumber penemuan endpoint WebSocket/gRPC dan file `.proto`. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi pemetaan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Analisis WebSocket & gRPC — <program/target> — <tanggal>
- Jenis: <WebSocket/gRPC/keduanya> (bukti: <...>)
- Rekaman: <path file rekaman> | alur yang direkam: <...>
- Pesan WebSocket: <n> jenis (per jenis: <arah> | <nama> | <field> | <pemicu>)
- Metode gRPC: <n> metode (per metode: <layanan/metode> | <jenis panggilan> | <request/response>)
- Metode tulis/hapus: <n> (ditandai saja, tidak dipanggil)
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; perekaman dilakukan lewat browser/proxy lokal.

### Websites

- Dokumentasi gRPC (grpc.io) — jenis panggilan dan format `.proto`.
- Dokumentasi WebSocket (RFC 6455 / MDN) — format frame dan pesan.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila lalu lintas gRPC terenkripsi dan tidak bisa dibaca: andalkan file `.proto` dari `dekompilasi-aplikasi-mobile` atau string di `analisis-statis-js`; catat "isi pesan tidak teramati (terenkripsi)" — jangan mencoba memecah enkripsi.
- Bila WebSocket hanya dipakai untuk notifikasi satu arah: petakan pesannya saja (Gerbang 2), jangan memaksakan pemetaan dua arah.
- Bila tidak ada tool gRPC yang tersedia: petakan dari path HTTP/2 teramati + `.proto` saja, dan catat metode yang belum terkonfirmasi sebagai "belum terpetakan".
