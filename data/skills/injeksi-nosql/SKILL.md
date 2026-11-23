# Skill: Injeksi NoSQL — Manipulasi Operator JSON pada MongoDB/CouchDB

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 29).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target memakai database NoSQL (MongoDB/CouchDB) dan input pengguna diteruskan ke query dalam bentuk JSON/objek — tanda-tandanya: endpoint menerima body JSON, login/pencarian memakai parameter yang diteruskan mentah, atau respons berubah saat nilai JSON diganti operator (`$ne`, `$gt`, `$regex`). Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji operator NoSQL, mendokumentasikan bukti read-only |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan bentuk query dari petunjuk |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian operator NoSQL, bukan mengulang konsepnya).
- Variasi payload secara sistematis (satu dimensi per putaran, log nilai → respons) → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Injeksi SQL klasik (dialek MySQL/PostgreSQL/MSSQL) → skill `injeksi-sql-kontekstual` (bukan skill ini — sintaks dan mesinnya berbeda).
- Eksekusi perintah OS via `$where`/JavaScript → bila terbukti bisa eksekusi perintah, pembuktiannya mengikuti skill `injeksi-perintah-rce` (hanya echo canary, tanpa baca/tulis file).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Khususnya: JANGAN pakai `$regex` yang berat/rakus (mis. `.*.*.*`) berulang-ulang — itu membanjiri DB.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai operator tulis (`$set`, `$unset`, `$push`, `$pull`, `$inc`) atau perintah hapus/ubah dokumen apa pun. DILARANG membaca dokumen milik pengguna lain. Pembuktian HARUS aman dan read-only.
11. **Bukti read-only yang diizinkan:** login/pencarian yang lolos memakai akun SENDIRI dengan operator, perbedaan respons boolean-blind via `$regex` pada data canary SENDIRI, dan `$where` yang hanya mengembalikan nilai canary (tanpa eksekusi perintah berbahaya). Itu saja.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian injeksi diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali bentuk input

1. Tentukan bagaimana input diteruskan: body JSON mentah (`{"username": "..."}`), query string (`?user=...`), atau form yang diubah jadi objek di server.
2. Uji penanda: kirim nilai JSON sebagai string vs sebagai objek — bila server menerima objek JSON di tempat yang semestinya string, itu permukaan injeksi.
3. **Standar lulus:** bentuk input (JSON mentah / query string / form) + contoh permintaan normal tertulis. Tanpa bentuk input = jangan menebak operator.

### Gerbang 2 — Uji operator perbandingan (MongoDB)

1. Uji operator satu per satu pada akun/data SENDIRI saja, mis. pada endpoint login/pencarian:

   | Operator | Contoh payload (nilai field) | Arti |
   |---|---|---|
   | `$ne` | `{"username": {"$ne": null}, "password": {"$ne": null}}` | tidak sama dengan null |
   | `$gt` / `$lt` | `{"age": {"$gt": 0}}` | lebih besar / lebih kecil dari |
   | `$in` | `{"role": {"$in": ["user", "admin"]}}` | salah satu dari daftar |
   | `$regex` | `{"username": {"$regex": "^a"}}` | cocok pola awal |
   | `$or` | `{"$or": [{"username": "akun-sendiri"}]}` | salah satu kondisi |
   | `$where` | `{"$where": "this.username == 'akun-sendiri'"}` | ekspresi JavaScript |

2. Untuk login bypass: uji HANYA terhadap akun SENDIRI (apakah login berhasil tanpa kata sandi yang benar, memakai akun sendiri). Jangan pernah menguji login ke akun orang lain.
3. **Standar lulus:** satu operator mengubah hasil secara konsisten (lolos vs gagal) pada akun/data sendiri. Operator yang tidak mengubah apa-apa = permukaan itu tidak rentan terhadap operator itu, catat dan lanjut.

### Gerbang 3 — Boolean-blind via `$regex` (bila tidak ada output langsung)

1. Tebak karakter demi karakter HANYA pada data canary SENDIRI (mis. token/username canary yang dibuat sendiri), mis. `{"field-canary": {"$regex": "^a"}}` lalu `^b`, `^c` — bandingkan respons TRUE vs FALSE.
2. Batasi jumlah percobaan (maks. puluhan, bukan ratusan) dan beri jeda — jangan membanjiri DB.
3. **Standar lulus:** perbedaan TRUE/FALSE teramati dan terulang pada 2 karakter berbeda, dan yang ditebak adalah data canary sendiri. Menebak data orang lain = DILARANG, berhenti.

### Gerbang 4 — `$where` JavaScript (bila tersedia, hati-hati)

1. `$where` mengeksekusi JavaScript di server — perlakukan sebagai permukaan RCE: uji HANYA dengan ekspresi yang mengembalikan nilai canary tanpa efek samping, mis. `{"$where": "this.username == 'akun-sendiri'"}`.
2. DILARANG memakai `$where` untuk memanggil fungsi sistem, membaca file, atau mengakses jaringan. Bila `$where` terbukti mengeksekusi, pembuktian lanjutan mengikuti skill `injeksi-perintah-rce` (hanya echo canary).
3. **Standar lulus:** `$where` terbukti dievaluasi (respons berubah mengikuti ekspresi) tanpa satu pun efek samping. Ekspresi dengan efek samping = pelanggaran, hentikan uji.

### Gerbang 5 — CouchDB (bila targetnya CouchDB)

1. CouchDB memakai Mango query (`{"selector": {...}}`) — uji operator yang sama (`$ne`, `$gt`, `$regex`) di dalam `selector`, plus parameter `_find`.
2. Periksa juga endpoint `/_all_docs` dan `/_find` yang terekspos tanpa autentikasi — bila bisa dibaca, itu temuan tersendiri (keterbukaan data), tapi JANGAN membaca dokumen milik orang lain; cukup buktikan endpoint merespons pada database canary sendiri.
3. **Standar lulus:** sama seperti Gerbang 2–3, pada selector CouchDB, hanya dengan data sendiri.

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal: login/pencarian lolos pada akun sendiri tanpa kredensial semestinya, atau boolean-blind yang membuktikan kendali query pada data canary sendiri. BERHENTI di situ — jangan lanjut mengekstrak dokumen lain.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (payload JSON persis + respons persis) + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU payload JSON per uji, amati respons; hanya bila program mengizinkan alat itu |
| Skrip pengujian buatan sendiri (Python/bash) | HANYA bila program mengizinkan otomasi (bukan huntr); satu operator per putaran — lihat `rekonstruksi-iterasi-payload` |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload JSON (nilai → respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Bentuk input: [body JSON / query string / form]
Mesin NoSQL: [MongoDB / CouchDB — bukti]
Operator terbukti: [$ne / $gt / $regex / $where / ...]
Payload: [JSON persis]
Bukti read-only: [login akun sendiri lolos / perbedaan TRUE-FALSE pada data canary sendiri]
Yang TIDAK dilakukan: [tanpa operator tulis, tanpa baca dokumen orang lain, tanpa $regex berat]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Banyak aplikasi memakai ORM/ODM yang mengubah objek sebelum query — operator bisa diblokir di lapisan itu walau DB-nya rentan; hasil negatif pada satu endpoint bukan berarti seluruh aplikasi aman.
- `$where` yang dievaluasi tidak selalu berarti RCE penuh — bedakan "ekspresi dievaluasi" dari "perintah OS dieksekusi" sebelum mengklaim dampak.
- Skill ini tidak membahas injeksi pada database NoSQL lain (Cassandra, Redis, Elasticsearch) — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
