# Skill: Perburuan gRPC — Refleksi Skema, Dekode Protobuf & Otorisasi Level Metode RPC

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`), Kategori 2, butir hunt-grpc. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool, flag, dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target memakai gRPC (format biner Protobuf, bukan JSON) dan endpoint gRPC-nya sudah masuk indeks aset lewat `analisis-websocket-grpc` — lalu skemanya perlu diungkap (refleksi), pesan binernya perlu dibaca (dekode Protobuf), dan otorisasi tiap metode RPC perlu diuji (apakah metode yang seharusnya admin/berbayar bisa dipanggil peran rendah?). Dipakai pada tahap pengujian, SETELAH pemetaan gRPC selesai. Bukan untuk bounty agen AI — ini teknik web/API klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menjalankan refleksi + dekode, menguji otorisasi per metode RPC |
| Pengerjaan | **A59 Threat Hunter** | Mencocokkan skema hasil refleksi dengan file `.proto`/JS |
| Audit | **A60 Security Auditor** | Memvalidasi skema + bukti otorisasi sebelum maju ke triase |
| Pemimpin | **Muse** | Putuskan metode RPC mana yang diuji dan kapan temuan maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Pemetaan metode gRPC (rekam lalu lintas, daftar layanan + metode dari `.proto`/path HTTP/2, tandai metode tulis/hapus)** ada di `analisis-websocket-grpc` Gerbang 1–3 — skill ini MENGAMBIL peta itu sebagai bahan mentah, bukan mengulang perekamannya. Jangan petakan ulang metode yang sudah terpetakan.
- **Analisis file JS yang memuat string `.proto`/endpoint gRPC** ada di `analisis-statis-js` — itu sumber penemuan endpoint-nya; skill ini bekerja pada endpoint yang sudah ditemukan.
- **Pengujian otorisasi HTTP/REST secara umum** ada di `access-control-differential-analyst` (metodologi diferensial 3 kondisi A/B/C) dan `pengujian-bfla` (fungsi per peran) — skill ini MENERAPKAN metodologi diferensial itu ke metode RPC gRPC (bukan HTTP), dengan format pesan Protobuf; jangan duplikat metodologinya, pakai sebagai rujukan dan catat adaptasi gRPC-nya.
- **GraphQL introspection** ada di `introspeksi-graphql` — itu padanan GraphQL dari refleksi; jangan campur skema GraphQL dan skema gRPC dalam satu inventaris.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Trigger & Scope

- **Trigger:** peta gRPC dari `analisis-websocket-grpc` berisi ≥1 layanan + metode; ATAU target diketahui memakai gRPC (dari JS: string `.proto`/`grpc`, dari crawl: lalu lintas HTTP/2 ke path `/paket.Layanan/Metode`).
- **Scope:** hanya layanan + metode gRPC pada endpoint in-scope yang tercatat di indeks aset. Refleksi hanya pada server refleksi target in-scope itu sendiri; dekode hanya pada pesan dari sesi akun tes sendiri.
- **Di luar scope:** metode gRPC yang mengubah/menghapus data — HANYA diuji bila Gerbang 3 lolos dan ada persetujuan manusia (lihat Aturan keras poin 5); streaming dua arah yang membanjiri server (itu DoS, bukan pengujian); memecah enkripsi/TLS untuk membaca lalu lintas gRPC (bila terenkripsi dan tidak bisa dibaca, andalkan refleksi + `.proto`, catat "isi pesan tidak teramati").

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Endpoint gRPC di luar scope = jangan direfleksi, jangan dipanggil.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Panggilan gRPC manual, rate limit ≤5 req/detik (lihat `scope-and-safety-guardian`); JANGAN membanjiri metode streaming dengan pesan massal; satu panggilan per metode per kondisi uji (lihat Gerbang 3).
4. **Tanpa payload di permukaan publik.** Pengujian otorisasi memakai request yang valid secara format (pesan Protobuf yang sah) dengan konteks otorisasi yang diubah — bukan payload eksploitasi, bukan injeksi.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive. Metode RPC yang mengubah/menghapus data HANYA dipanggil bila: (a) datanya milik akun tes sendiri, (b) aksinya reversibel atau berupa canary palsu, (c) ada persetujuan manusia tercatat di log. Tanpa ketiganya = tandai saja, jangan panggil.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Temuan gRPC bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Refleksi yang dimatikan BUKAN kerentanan.** Bila server tidak mengaktifkan refleksi, itu konfigurasi normal — catat "refleksi nonaktif", lanjut lewat `.proto`/pengamatan, jangan laporkan sebagai temuan.
10. **Bila rekaman/dekode mengandung data pengguna lain, HENTIKAN, sensor, dan laporkan ke Muse** — jangan dibaca lanjut, jangan disimpan utuh. Simpan hanya struktur pesannya (nama field + nomor field + jenis), bukan isinya.
11. **Jangan mengarang skema.** Layanan/metode/field harus berasal dari refleksi, file `.proto`, atau pengamatan path HTTP/2 — hasil tebakan ditulis sebagai "dugaan — belum terverifikasi", bukan fakta.

## Methodology & Payloads

### Refleksi skema gRPC (server reflection)

- Bila server mengaktifkan refleksi (`grpc.reflection.v1alpha.ServerReflection`): daftar layanan (`list`), lalu deskripsikan tiap layanan + metode (`describe`) — ambil nama layanan, nama metode, jenis panggilan (unary / server-streaming / client-streaming / bidi), dan definisi pesan request/response.
- Bila refleksi nonaktif: rekonstruksi dari file `.proto` (bila ada, dari `analisis-statis-js` / `dekompilasi-aplikasi-mobile`) atau dari path HTTP/2 yang teramati (`/paket.Layanan/Metode`) — catat sumber tiap metode sebagai "refleksi" / "proto" / "pengamatan".
- Bandingkan hasil refleksi dengan peta `analisis-websocket-grpc`: metode yang ada di refleksi tapi tidak di peta = shadow RPC (serahkan daftarnya ke `perburuan-shadow-api-spa` untuk klasifikasi, jangan uji langsung).

### Dekode pesan Protobuf (wire format)

- Pesan Protobuf adalah biner: tiap field = pasangan (nomor field + wire type) + nilai. Wire type yang umum: 0 = varint (int/bool/enum), 1 = 64-bit, 2 = length-delimited (string/bytes/pesan bersarang/repeated), 5 = 32-bit.
- Dekode pesan dari sesi sendiri (request/response yang direkam `analisis-websocket-grpc`) dengan tool dekode (mis. `protoc --decode_raw` atau klien gRPC yang menampilkan JSON) — catat per pesan: nomor field, wire type, dan nilai (sensor bila sensitif).
- Field yang tidak dikenal (nomor field tanpa nama di skema) dicatat sebagai "field tak dikenal #N (wire type T)" — jangan ditebak namanya; field tak dikenal yang membawa data sensitif ditandai saja.
- Pesan yang tidak bisa didekode (terenkripsi/kompres tak dikenal) dicatat "tidak terdekode + alasannya", bukan ditebak isinya.

### Uji otorisasi level metode RPC (diferensial, adaptasi gRPC)

- Terapkan metodologi diferensial `access-control-differential-analyst` (3 kondisi A/B/C) ke SATU metode RPC sekali jalan: (A) token peran rendah/akun tes sendiri memanggil metode yang seharusnya butuh peran lebih tinggi; (B) tanpa token; (C) token akun tes sendiri yang lain (dua akun sendiri) untuk objek milik akun lain.
- Mulai dari metode BACA (unary read) — metode tulis/hapus hanya bila Aturan keras poin 5 terpenuhi.
- Untuk streaming: uji dengan SATU pesan streaming saja (bukan banjir); server-streaming yang mengembalikan data orang lain = HENTIKAN sesuai Aturan keras poin 10.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web/API klasik in-scope dan endpoint gRPC-nya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. Pastikan ada peta gRPC dari `analisis-websocket-grpc` (layanan + metode tercatat) atau bukti target memakai gRPC.
3. **Standar lulus:** scope tertulis; peta gRPC tersedia; bila target hanya HTTP/REST biasa, skill ini tidak dipakai — tulis "tidak berlaku" di log.

### Gerbang 1 — Refleksi skema

1. Coba refleksi pada endpoint gRPC in-scope (klien gRPC, mis. grpcurl — pilih satu yang tersedia; ambil cara pakai dari dokumentasi resminya, jangan mengarang flag): daftar layanan, lalu deskripsikan tiap layanan + metode + pesan request/response.
2. Bila refleksi nonaktif, rekonstruksi dari `.proto`/pengamatan dan catat sumber tiap metode; bila tidak ada `.proto` DAN tidak ada pengamatan, metode itu = "belum terpetakan", bukan ditebak.
3. Cek silang dengan peta `analisis-websocket-grpc` + file `.proto` (A59): selisih dicatat (metode baru dari refleksi, metode di peta yang tidak ada di refleksi).
4. **Standar lulus:** tiap metode punya layanan + jenis panggilan + pesan request/response + sumber (refleksi/proto/pengamatan) tertulis; refleksi nonaktif dicatat sebagai konfigurasi, bukan temuan. Metode tanpa sumber = belum terpetakan.

### Gerbang 2 — Dekode pesan Protobuf

1. Ambil 1–2 pasang pesan request/response per metode dari sesi akun tes sendiri (dari rekaman `analisis-websocket-grpc`); dekode ke bentuk terbaca (field + nomor + wire type + nilai, sensor bila sensitif).
2. Petakan field ke skema Gerbang 1: field mana yang membawa ID objek, token, peran, atau data sensitif (jenisnya saja, bukan isinya).
3. **Standar lulus:** tiap metode yang akan diuji punya minimal satu pesan terdekode dengan field kuncinya terpetakan; pesan yang tidak terdekode dicatat alasannya. Metode tanpa pesan terdekode = belum siap diuji (kecuali metodenya read sederhana yang pesannya sudah jelas dari skema).

### Gerbang 3 — Uji otorisasi per metode RPC

1. Pilih 1–3 metode prioritas (metode baca yang sensitif dulu: baca data pengguna, daftar resource, konfigurasi; lalu metode admin bila ada) — SATU metode sekali jalan.
2. Untuk tiap metode, kirim request yang sama persis (pesan Protobuf yang sama, dari dekode Gerbang 2) dalam 3 kondisi: (A) token peran rendah (akun tes sendiri), (B) tanpa token, (C) token akun tes kedua untuk objek milik akun pertama — patuhi rate limit, satu panggilan per kondisi.
3. Simpan respons tiap kondisi (status gRPC + pesan, sensor bila sensitif). Metode tulis/hapus HANYA bila Aturan keras poin 5 terpenuhi; bila tidak, tandai "tulis/hapus, belum diuji — butuh persetujuan manusia".
4. **Standar lulus:** tiap metode yang diuji punya respons 3 kondisi tercatat; tidak ada metode tulis/hapus yang dipanggil tanpa persetujuan manusia tercatat. Metode tanpa 3 kondisi = belum diuji.

### Gerbang 4 — Validation Gate + serahkan ke triase

1. Terapkan Validation Gate di bawah pada tiap metode yang menunjukkan perbedaan respons antar kondisi.
2. Metode yang lolos gate diserahkan ke `triase-duplikat` (cek duplikat) → A60 audit → draf laporan (A67) → Cipta setuju → kirim. Metode yang tidak lolos gate = "belum terbukti", bukan temuan.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan; tidak ada metode yang maju tanpa lolos gate.

## Validation Gate

Verifikasi deterministik baseline vs exploit — WAJIB sebelum metode RPC dinyatakan rentan:

1. **Baseline tercatat:** kondisi (C) yang sah — akun pemilik objek memanggil metodenya sendiri — harus BERHASIL (atau memberi respons yang diharapkan pemilik). Bila baseline saja gagal, pengujian tidak valid — perbaiki request-nya dulu, jangan simpulkan celah.
2. **Perbedaan deterministik:** kondisi (A) atau (B) memberi respons yang SAMA dengan baseline (data yang sama / aksi yang sama) padahal seharusnya ditolak (UNAUTHENTICATED / PERMISSION_DENIED) — dan perbedaan itu terulang pada pengulangan kedua dari state bersih.
3. **Bukti dampak:** respons berisi data/aksi milik akun lain (canary palsu akun tes kedua) atau perubahan state nyata pada akun sendiri — sekadar "status bukan 403" tanpa data/aksi = belum terbukti.
4. **Yang TIDAK lolos gate:** respons error generik yang sama di semua kondisi; hasil sekali jalan tanpa pengulangan; data pengguna lain yang tidak sengaja terbaca (= hentikan, sensor, laporkan — bukan bukti). Satu gate gagal = BELUM TERBUKTI.

## Alat

| Alat | Cara pakai |
|---|---|
| Klien gRPC (mis. grpcurl / BloomRPC — pilih satu yang tersedia) | Refleksi (`list`/`describe`) + panggil metode BACA untuk konfirmasi + uji otorisasi. Ambil cara pakai dari dokumentasi resminya, jangan mengarang flag. |
| Dekoder Protobuf (mis. `protoc --decode_raw` atau tampilan JSON klien gRPC) | Dekode pesan biner dari sesi sendiri ke field + nomor + wire type. |
| File `.proto` / definisi layanan (bila tersedia) | Pembanding skema Gerbang 1; sumber dari `analisis-statis-js` / `dekompilasi-aplikasi-mobile`. |
| `analisis-websocket-grpc` | Peta metode + rekaman lalu lintas (bahan mentah Gerbang 0–2). |
| `access-control-differential-analyst` + `pengujian-bfla` | Metodologi diferensial + uji per peran yang diterapkan di Gerbang 3. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi perburuan gRPC. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Perburuan gRPC — <program/target> — <tanggal>
- Refleksi: <aktif/nonaktif> | layanan: <n> | metode: <n> (sumber: refleksi <n> / proto <n> / pengamatan <n>)
- Metode baru dari refleksi (shadow RPC): <n> → diserahkan ke perburuan-shadow-api-spa
- Pesan terdekode: <n> metode (per metode: <field kunci: nomor + wire type>)
- Uji otorisasi: <n> metode (per metode: <layanan/metode> | <A: status+ringkasan> | <B: status+ringkasan> | <C: status+ringkasan>)
- Lolos Validation Gate: <n> metode (bukti dampak: <...>)
- Tulis/hapus belum diuji: <n> metode (alasan: butuh persetujuan manusia)
- Keputusan triase: [maju/ditolak + alasan]
- Audit A60: [lolos/ditolak + alasan]
- Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; refleksi, dekode, dan pemanggilan dilakukan lewat klien gRPC lokal.

### Websites

- Dokumentasi gRPC (grpc.io) — refleksi server + format `.proto`.
- Dokumentasi Protocol Buffers (protobuf.dev) — wire format + tipe field.
- Dokumentasi klien gRPC yang dipakai (grpcurl/BloomRPC) — cara pakai flag-nya.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila refleksi nonaktif dan tidak ada `.proto`: petakan dari path HTTP/2 teramati saja dan catat metode yang belum terkonfirmasi sebagai "belum terpetakan" — jangan menebak skema.
- Bila pesan terenkripsi (TLS) dan tidak bisa didekode: andalkan refleksi + `.proto`; catat "isi pesan tidak teramati (terenkripsi)" — jangan mencoba memecah enkripsi.
- Bila metode yang sensitif ternyata hanya tersedia lewat streaming dua arah: uji dengan satu pesan saja; bila server menuntut aliran berlanjut, hentikan dan catat sebagai "belum teruji — butuh streaming", jangan membanjiri.
