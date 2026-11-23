# Skill: Injeksi SQL Kontekstual — Error-Based, Boolean-Blind, Time-Based per Dialek DB

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 28).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis bahwa input pengguna masuk ke query SQL tanpa sanitasi yang cukup — parameter URL/form/JSON/header/cookie yang mengubah hasil query, pesan error DB yang bocor, atau perilaku halaman yang berubah saat input berisi karakter SQL (`'`, `"`, `)`, `OR 1=1`). Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji injeksi SQL per dialek, mendokumentasikan bukti read-only |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan dialek DB dari petunjuk |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep SQLi + standar pembuktian dampak secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian per dialek, bukan mengulang konsepnya).
- Variasi payload secara sistematis (satu dimensi per putaran, log nilai → respons) → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Injeksi NoSQL (operator JSON MongoDB/CouchDB) → skill `injeksi-nosql` (bukan skill ini — sintaks dan dialeknya berbeda).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, atau perintah apa pun yang menghapus/mengubah data. DILARANG dump tabel milik pengguna lain. Pembuktian HARUS aman dan read-only.
11. **Bukti read-only yang diizinkan:** versi DB (`SELECT version()` / `@@VERSION`), nama DB saat ini, hasil boolean-blind (TRUE vs FALSE), dan time-based sleep (tunda beberapa detik, volume kecil, tanpa membanjiri server). Itu saja — cukup untuk membuktikan injeksi.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian injeksi diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja, tanpa skrip agen AI)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali konteks injeksi

1. Tentukan konteks parameter: numerik (`id=1`) atau string (`q='...'`) — uji dengan `'` tunggal dan amati: error DB, halaman kosong, atau respons berubah.
2. Tentukan penutup yang benar: `'`, `"`, `')`, `")`, atau tanpa penutup; catat mana yang mengubah respons.
3. **Standar lulus:** konteks (numerik/string + karakter penutup) tertulis. Tanpa konteks = jangan menebak payload lanjutan; itu tebakan buta.

### Gerbang 2 — Kenali dialek DB

1. Kenali dialek dari petunjuk: pesan error, fungsi yang bekerja, atau stack teknologi target.
2. Penanda per dialek (pakai HANYA untuk identifikasi, semua read-only):

   | Dialek | Fungsi versi | Fungsi tunda | Komentar |
   |---|---|---|---|
   | MySQL | `version()`, `@@version` | `SLEEP(5)` | `-- ` (spasi), `#` |
   | PostgreSQL | `version()` | `pg_sleep(5)` | `--` |
   | MSSQL | `@@VERSION` | `WAITFOR DELAY '0:0:5'` | `--` |
   | Oracle | `SELECT banner FROM v$version` | `DBMS_PIPE.RECEIVE_MESSAGE` | `--` |
   | SQLite | `sqlite_version()` | (tidak ada sleep bawaan — pakai boolean-blind) | `--` |

3. **Standar lulus:** dialek teridentifikasi dengan SATU bukti (error khas atau fungsi versi yang mengembalikan nilai). Dialek belum jelas = uji dengan boolean-blind (Gerbang 4), jangan menebak dialek untuk time-based.

### Gerbang 3 — Error-based (bila error DB bocor)

1. Picu error yang menampilkan isi query: `'` tunggal, `AND 1=CONVERT(int,(SELECT @@VERSION))--` (MSSQL), `AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--` (MySQL), `AND 1=CAST((SELECT version()) AS int)--` (PostgreSQL).
2. **Standar lulus:** respons menampilkan potongan data read-only (mis. versi DB) dari error — BUKAN sekadar "ada error". Error tanpa isi data = belum terbukti, lanjut ke Gerbang 4.

### Gerbang 4 — Boolean-blind (bila tidak ada error dan tidak ada output langsung)

1. Kirim dua kondisi yang hanya berbeda nilai kebenarannya, mis. `AND 1=1` (TRUE) vs `AND 1=2` (FALSE), dan bandingkan respons (isi halaman / status / panjang respons).
2. Bila TRUE dan FALSE menghasilkan respons yang konsisten berbeda → injeksi TERBUKTI. Konfirmasi dengan membalik kondisi (`OR 1=1` vs `OR 1=2`).
3. **Standar lulus:** perbedaan TRUE/FALSE teramati dan terulang minimal 2x dengan nilai berbeda. Perbedaan satu kali yang tidak terulang = belum terbukti (bisa jadi noise/cache).

### Gerbang 5 — Time-based blind (bila boolean juga tidak memberi perbedaan)

1. Pakai fungsi tunda sesuai dialek (Gerbang 2), tunda 5 detik, SATU permintaan per uji, jeda antar uji — jangan membanjiri server (itu DoS).
2. Bandingkan waktu respons: tunda yang diminta vs baseline normal. Konfirmasi dengan tunda berbeda (mis. 2 detik vs 8 detik) agar terbukti respons mengikuti nilai tunda.
3. **Standar lulus:** waktu respons mengikuti nilai tunda pada 2 nilai berbeda, dan baseline tanpa payload kembali normal. Satu tunda saja tanpa konfirmasi = belum terbukti.

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal yang dikumpulkan: versi DB + nama DB saat ini + (bila boolean/time-based) satu nilai read-only yang membuktikan kendali atas query (mis. `SUBSTRING(version(),1,1)='5'`). BERHENTI di situ — jangan lanjut mengekstrak tabel, kolom, atau baris data lain.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (payload persis + respons/waktu persis) + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU payload per uji, amati respons; hanya bila program mengizinkan alat itu |
| Skrip pengujian buatan sendiri (Python/bash) | HANYA bila program mengizinkan otomasi (bukan huntr); satu dimensi per putaran, berhenti otomatis bila respons menunjukkan kerusakan — lihat `rekonstruksi-iterasi-payload` |
| Stopwatch / pengukuran waktu respons | Untuk time-based: catat waktu respons tiap uji + baseline |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload (nilai → respons/waktu → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter]
Konteks: [numerik/string + karakter penutup]
Dialek DB: [MySQL/PostgreSQL/MSSQL/Oracle/SQLite — bukti identifikasi]
Teknik terbukti: [error-based / boolean-blind / time-based]
Payload: [payload persis]
Bukti read-only: [versi DB / perbedaan TRUE-FALSE / waktu respons X dtk vs baseline Y dtk]
Yang TIDAK dilakukan: [tanpa DROP/DELETE/UPDATE, tanpa dump data orang lain]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Tanpa fondasi kerentanan (lihat `fondasi-kerentanan-web-api`), variasi payload mudah jadi tebakan acak yang tidak berdampak.
- WAF/rate-limit bisa mengubah respons dan meniru "perbedaan TRUE/FALSE" — konfirmasi dengan pengulangan sebelum mengklaim terbukti.
- Skill ini tidak membahas injeksi pada ORM/procedure tersimpan yang perilakunya berbeda — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
