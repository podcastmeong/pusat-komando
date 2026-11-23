# Skill: Eskalator Rantai ABC — Pola Eskalasi Lanjutan dari Sinyal Low/Informational

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` Bagian 3 (A → B → C Chaining Escalator, 24 Nov 2026). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu rantai yang lolos triase dan dicatat di log.
>
> Skill ini adalah **katalog pola lanjutan** untuk `eskalasi-dampak-otomatis` (pola 11–13, melanjutkan katalog pola 1–10 di sana) — BUKAN skill chaining yang berdiri sendiri. Dipakai bersama skill itu: tiap pola di sini dicek lewat Gerbang 1–4 `eskalasi-dampak-otomatis`, dan rantai yang terbukti diserahkan ke `perangkaian-kerentanan` untuk dirangkai sebagai laporan.

## Pemicu (kapan dipakai)

Dipakai setiap kali ada temuan VERIFIED (lolos `skeptic-false-positive-eliminator`) yang dampaknya sendiri RENDAH — IDOR read-only, S3 bucket listing, CORS reflects-origin, atau debug/error endpoint — dan temuan itu cocok dengan kolom "Sinyal Awal" pada salah satu pola di bawah. Dipakai SEBELUM temuan rendah itu dilaporkan apa adanya atau dibuang: satu sinyal = satu kali cek terhadap pola yang cocok. Bila tidak ada pola yang cocok, eskalasi selesai dengan hasil TIDAK ADA RANTAI.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55 Analis Rantai & Pelapor** | Memetakan sinyal rendah ke pola 11–13, menjalankan uji eskalasi |
| Pengerjaan | **A62 Exploit Developer** | Menjalankan teknik bukti aman untuk tiap langkah eskalasi |
| Audit | **A60 Security Auditor** | Memeriksa tiap langkah eskalasi sudah terbukti sendiri + dampak akhir nyata |
| Pemimpin | **Muse** | Memutuskan rantai mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Eskalasi umum dari temuan rendah + katalog pola 1–10** → `eskalasi-dampak-otomatis`. Skill ini HANYA menambah pola 11–13; gerbang kerja (petakan → uji langkah → buktikan dampak akhir → nilai ulang), Validation Gate baseline-vs-exploit, dan format log mengikuti skill itu.
- **Perangkaian temuan yang masing-masing sudah VERIFIED** → `perangkaian-kerentanan`. Rantai yang terbukti lewat pola di sini diserahkan ke sana untuk dirangkai sebagai laporan rantai.
- **Teknik uji tulis IDOR (PUT/PATCH/POST/DELETE lintas akun + state verification + kembalikan data)** → `access-control-differential-analyst` Gerbang 4. Pola 11 di bawah HANYA menambah aturan pemicunya (IDOR read-only VERIFIED wajib memicu uji tulis sebelum ditutup); langkah tekniknya TIDAK diulang di sini — jalankan Gerbang 4 skill itu.
- **Audit CORS lengkap (uji pantulan Origin + kredensial + bukti baca lintas-origin di browser)** → `audit-cors`. Rantai CORS dari riset Bagian 3 SUDAH tercakup penuh di sana (Langkah 2–3) dan sebagai pola 6 `eskalasi-dampak-otomatis` — karena itu rantai CORS TIDAK dijadikan pola baru di skill ini (lihat "Butir yang ditolak" di bawah).
- **Bedah JS bundle + sensor secret** → `analisis-statis-js` (Gerbang 3–4). Pola 12 memakai teknik itu; yang baru di sini hanyalah rangkaiannya (listing S3 → bundle JS → client_secret → SSO).
- **Enumerasi bucket cloud + klasifikasi keterbukaan (read-only, tanpa unduh objek)** → `enumerasi-aset-cloud`. Pola 12 berangkat dari hasil skill itu; aturan larangan unduh objek di sana TETAP berlaku.
- **OAuth/SSO misconfiguration (redirect_uri, state, validasi token)** → `perburuan-kerentanan-spesifik` §3. Pola 12 BUKAN itu — pola 12 soal client_secret yang bocor di kode publik, bukan soal validasi alur OAuth.
- **Teknik bukti aman per jenis celah** → `verifikasi-poc-aman`. Tiap langkah eskalasi memakai teknik dari katalog itu, bukan teknik baru.
- **Verifikasi adversarial + skor + draf laporan** → `skeptic-false-positive-eliminator`, `penilaian-cvss`, `artikulasi-dampak-bisnis`, `triase-duplikat`, `laporan-poc-otomatis` — hasil eskalasi yang terbukti masuk kembali ke alur itu (skor dihitung dari dampak AKHIR, bukan dampak awal).
- **Rantai injeksi prompt di program bounty agen AI** → `transfer-hunting` — skill ini untuk rantai web/API klasik.
- Alur sesudah skill ini: eskalasi TERBUKTI → `perangkaian-kerentanan` (rangkai + buktikan ujung-ke-ujung) → `penilaian-cvss` + `artikulasi-dampak-bisnis` (dari dampak akhir) → `triase-duplikat` → draf laporan → tinjau manusia → persetujuan Cipta → kirim. Eskalasi GAGAL → temuan rendah dilaporkan apa adanya atau dibuang, sesuai keputusan triase.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Rantai yang butuh korban memakai akun KEDUA MILIK SENDIRI sebagai korban; jangan pernah melibatkan pengguna asli.
4. **Tanpa DoS/DDoS.** Tanpa payload di permukaan publik.
5. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).** Tiap langkah eskalasi yang berhasil HARUS ditinjau manusia sebelum langkah berikutnya dijalankan.
6. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
8. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian eskalasi harus aman dan read-only — kecuali uji tulis Pola 11 yang dibatasi ketat di bawah (hanya objek canary milik sendiri, dikembalikan ke semula; DELETE hanya pada objek canary sekali-pakai yang dibuat khusus untuk uji itu).
9. **Kredensial / cloud key yang ditemukan JANGAN dipakai untuk mengakses apa pun dan JANGAN ditulis utuh** — hanya pola + lokasi + `[REDACTED]`. Ini berlaku mutlak untuk client_secret (Pola 12) dan API key / kredensial cloud (Pola 13). Memakai secret temuan untuk login/mengakses = pelanggaran, walau terhadap akun sendiri.
10. **Jangan membesar-besarkan severity.** Hanya dampak AKHIR yang TERBUKTI yang boleh diklaim; rantai yang berhenti di tengah jalan = belum terbukti, jangan klaim dampak akhirnya. Khusus Pola 12 dan 13, dampak akhir (pembajakan SSO / akses infrastruktur cloud) TIDAK BOLEH diklaim terbukti — yang terbukti hanyalah eksposurnya (lihat Execution Gate tiap pola).
11. **Sensor PII/token/kredensial di semua bukti ([REDACTED]) sebelum laporan disusun.**
12. **Jangan pernah mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia dulu; pengiriman selalu manual + disetujui Cipta.
13. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, jangan menguji payload injeksi.
14. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Katalog pola eskalasi (lanjutan pola 1–10 `eskalasi-dampak-otomatis`)

Setiap pola ditulis dalam struktur riset Bagian 3: **Signal → Probe Steps → Execution Gate**. Satu sinyal rendah = cek SEMUA pola yang titik awalnya cocok; pola yang titik awalnya tidak cocok = lewati, jangan dipaksakan.

### Pola 11 — IDOR Read-Only → uji tulis pada endpoint yang sama → manipulasi penuh data akun korban

| Bagian | Isi |
|---|---|
| **Signal (A)** | IDOR read-only VERIFIED: akun uji B bisa MEMBACA objek milik akun uji A (lolos `access-control-differential-analyst` Gerbang 2–3 + `skeptic-false-positive-eliminator`). Dampak sendiri rendah — hanya baca. |
| **Probe Steps (B)** | 1. Ambil endpoint yang SAMA persis (metode GET yang bocor) dari indeks recon. 2. Uji metode tulis pada endpoint itu sebagai akun B terhadap objek milik akun A, SATU PER SATU: PUT, lalu PATCH, lalu DELETE — memakai teknik `access-control-differential-analyst` Gerbang 4 (bukan teknik baru). 3. Uji tulis HANYA pada objek canary milik sendiri: PUT/PATCH mengubah field canary, lalu baca-ulang sebagai akun A untuk state verification; DELETE hanya pada objek canary sekali-pakai yang dibuat khusus untuk uji itu (bukan objek nyata), dan tidak ada objek nyata yang boleh dihapus. 4. Bila perubahan nyata terjadi, kembalikan data objek ke keadaan semula dari akun pemiliknya (kecuali objek canary sekali-pakai yang memang dibuat untuk dihapus). 5. BERHENTI di metode yang gagal — metode itu GAGAL, jangan ditambal asumsi; lanjut ke metode berikutnya. |
| **Execution Gate (C)** | TERBUKTI hanya bila: baca-ulang sebagai akun A (sesi bersih) menunjukkan perubahan NYATA di server (bukan sekadar pesan sukses — silent drop = GAGAL) + langkah reproduksi persis tercatat + objek canary dikembalikan ke semula. Dampak akhir yang boleh diklaim: manipulasi penuh data akun korban (Account Takeover bila field yang diubah menguasai akun — mis. ganti email/password/role — dibuktikan pada akun kedua milik sendiri, bukan diduga). Satu metode tulis terbukti = pola TERBUKTI; lanjut ke `perangkaian-kerentanan`. |

### Pola 12 — S3 Bucket Listing → ekstrak JS bundles, cari client_secret OAuth → pembajakan alur SSO / OAuth

| Bagian | Isi |
|---|---|
| **Signal (A)** | S3 bucket listing VERIFIED: bucket target berstatus terbuka-listing (lolos `enumerasi-aset-cloud` Gerbang 2–4) dan listing nama file menunjukkan bundle JS aplikasi (`*.js`, `*.js.map`, chunk) sebagai aset publik milik target. Dampak sendiri rendah — hanya daftar nama file. |
| **Probe Steps (B)** | 1. Pastikan dulu bucket TIDAK berisi data orang lain: bila listing menunjukkan dokumen/database/backup/foto milik pengguna, BERHENTI — terapkan `enumerasi-aset-cloud` Aturan keras 6 (jangan unduh, jangan baca isi, laporkan ke Muse). Pola ini HANYA jalan bila isi bucket adalah aset publik milik target (JS/CSS/gambar situs). 2. Ambil HANYA file JS bundle / source map yang merupakan kode aplikasi publik — file yang sama yang juga disajikan situs target ke semua pengunjung — dan bedah dengan `analisis-statis-js` (cari pola `client_secret`, `clientSecret`, `oauth`, kunci API). 3. Untuk tiap kandidat secret catat: file + baris + jenis secret — nilainya DISENSOR (`[REDACTED]`), jangan pernah ditulis utuh. 4. Periksa konteks: apakah nilai itu benar secret rahasia (dipakai di alur token server-side) atau nilai publik yang memang boleh terekspos (mis. `client_id` publik, kunci publishable) — yang kedua = BUKAN temuan, tutup. 5. JANGAN menukar authorization code dengan secret temuan, JANGAN login/mengakses apa pun dengan secret itu (Aturan keras 9). |
| **Execution Gate (C)** | TERBUKTI hanya untuk klaim **"client_secret rahasia terekspos di kode publik"**: pola nilai + file + baris tercatat (tersensor) + bukti bundle itu disajikan publik oleh target + A60 memastikan nilainya bukan kunci publik. Dampak akhir "pembajakan alur SSO/OAuth" TIDAK BOLEH diklaim terbukti lewat pola ini — pembuktiannya butuh memakai secret temuan, dan itu DILARANG. Dampak akhir ditulis sebagai dampak yang DIARTIKULASIKAN (secret rahasia di kode publik = siapa pun bisa membacanya; per spesifikasi OAuth, client_secret confidential tidak boleh dikirim ke klien) dan A60 yang memutuskan apakah eksposur itu sendiri layak maju ke triase sebagai temuan. Bila tidak ada secret rahasia di bundle = pola GAGAL, tutup. |

### Pola 13 — Debug / Error Endpoint → cari kebocoran variabel lingkungan (.env / stack trace) → ekstraksi kunci API / kredensial infrastruktur cloud

| Bagian | Isi |
|---|---|
| **Signal (A)** | Debug / error endpoint VERIFIED: endpoint target (mis. halaman error, halaman debug, endpoint status/health yang terlalu cerewet) mengembalikan respons yang mengandung jejak internal — stack trace, nama variabel lingkungan, potongan konfigurasi — pada permintaan biasa. Dampak sendiri rendah/informational — hanya kebocoran jejak. |
| **Probe Steps (B)** | 1. Catat endpoint + respons persis yang membocorkan jejak (permintaan read-only biasa, sesi sendiri; jangan brute-force jalur di luar endpoint itu dan jangan memicu error sengaja dalam jumlah besar — patuhi rate limit). 2. Periksa respons itu sendiri apakah sudah mengandung nilai sensitif: pola kunci API (`AKIA...`, `sk-...`, `xox...`, dsb.), kredensial cloud, string koneksi database, token internal. Bila respons hanya berisi nama variabel TANPA nilai = catat sebagai kandidat lemah, jangan klaim kebocoran kredensial. 3. Bila endpoint memuat daftar variabel lingkungan, periksa HANYA apa yang sudah dikembalikan server dalam respons itu — jangan memanggil endpoint lain / jalur file (`/.env`, traversal) untuk "melengkapi" kebocoran; itu ranah `traversal-jalur-lfi`, bukan pola ini. 4. Untuk tiap kandidat kunci catat: pola + lokasi respons — nilainya DISENSOR (`[REDACTED]`), jangan pernah ditulis utuh. 5. JANGAN memakai kunci temuan untuk mengakses layanan apa pun (Aturan keras 9) — termasuk JANGAN memanggil API cloud dengan kunci itu untuk "membuktikan ia aktif". |
| **Execution Gate (C)** | TERBUKTI hanya untuk klaim **"kunci API / kredensial cloud terekspos lewat respons debug/error"**: pola kunci + lokasi respons tercatat (tersensor) + bukti endpoint mengembalikannya pada permintaan biasa + A60 memastikan polanya cocok dengan format kunci layanan yang diklaim. Dampak akhir "akses infrastruktur cloud" TIDAK BOLEH diklaim terbukti — pembuktiannya butuh memakai kunci temuan, dan itu DILARANG. Dampak akhir ditulis sebagai dampak yang DIARTIKULASIKAN (kunci cloud di respons publik = siapa pun bisa membacanya dan kunci itu mengontrol layanan X menurut dokumentasi layanan) dan A60 yang memutuskan apakah eksposur itu sendiri layak maju ke triase. Bila respons hanya berisi nama variabel tanpa nilai, atau hanya stack trace tanpa secret = pola GAGAL sebagai kebocoran kredensial (tetap boleh dicatat sebagai info disclosure rendah bila triase memintanya). |

## Butir yang ditolak (tidak dibuat jadi pola baru)

| Rantai riset Bagian 3 | Alasan ditolak |
|---|---|
| CORS Reflects Origin → uji dengan `Access-Control-Allow-Credentials: true` → pencurian data terautentikasi lintas domain | SUDAH TERCUKUP PENUH. `audit-cors` Langkah 2 sudah menguji pantulan Origin DENGAN kredensial dan Langkah 3 sudah membuktikan pembacaan lintas-origin di browser dengan `credentials: "include"`; `eskalasi-dampak-otomatis` pola 6 sudah mencatat varian CORS + IDOR. Membuat pola keempat = duplikat (perintah Cipta "Yang sama g usah"). Bila sinyalnya CORS reflects-origin, jalankan `audit-cors`, bukan skill ini. |

## Langkah + gerbang (cara memakai katalog ini)

### Gerbang 1 — Petakan sinyal ke pola 11–13

1. Tulis sinyal rendah + dampaknya sendiri + skor triase awalnya (dari `triase-duplikat`).
2. Cocokkan sinyalnya dengan kolom Signal pola 11–13. Tulis SEMUA pola yang cocok sebagai hipotesis eskalasi, plus prasyarat tiap pola (mis. Pola 11 butuh endpoint yang sama menerima metode tulis; Pola 12 butuh bundle JS sebagai aset publik di bucket; Pola 13 butuh respons debug/error yang sudah mengandung jejak).
3. Urutkan hipotesis dari yang paling mungkin (prasyarat sudah terlihat ada) ke yang paling spekulatif.
4. **Standar lulus:** daftar hipotesis tertulis dengan prasyarat tiap pola. Tidak ada pola yang cocok = eskalasi selesai dengan hasil TIDAK ADA RANTAI — temuan dilaporkan apa adanya atau dibuang sesuai triase.

### Gerbang 2 — Uji tiap langkah eskalasi dengan bukti aman

1. Untuk hipotesis pertama, jalankan Probe Steps polanya SATU PER SATU, memakai teknik bukti aman dari skill yang didelegasikan (Pola 11 → `access-control-differential-analyst` Gerbang 4; Pola 12 → `analisis-statis-js`; Pola 13 → pembacaan respons itu sendiri).
2. **BERHENTI di langkah yang gagal.** Bila satu langkah eskalasi tidak terbukti, hipotesis itu GAGAL — jangan menambal langkah yang gagal dengan asumsi. Catat langkah yang gagal + buktinya, lalu lanjut ke hipotesis berikutnya.
3. Tiap langkah yang berhasil HARUS ditinjau manusia sebelum langkah berikutnya dijalankan.
4. **Standar lulus per hipotesis:** semua langkah eskalasi terbukti dengan bukti aman + reference ID, dan Execution Gate polanya terpenuhi. Satu langkah gagal = hipotesis gagal.

### Gerbang 3 — Buktikan dampak AKHIR, bukan tiap langkahnya saja

1. Pola 11: jalankan rantai lengkap dari langkah pertama sampai dampak akhir, memakai akun sendiri di kedua sisi (penyerang + korban — keduanya milik sendiri); buktikan dampak AKHIR-nya (perubahan nyata pada akun kedua milik sendiri).
2. Pola 12 dan 13: dampak akhir TIDAK dibuktikan lewat pemakaian secret/kunci temuan (dilarang) — yang dibuktikan adalah eksposurnya + artikulasi dampaknya; A60 memutuskan kelayakan triase (lihat Execution Gate tiap pola).
3. **Standar lulus:** ada bukti dampak akhir nyata pada akun sendiri (Pola 11) ATAU bukti eksposur tersensor + putusan A60 (Pola 12–13) + langkah reproduksi persis dari langkah 1. Rantai yang berhenti di tengah jalan = belum terbukti.

### Gerbang 4 — Nilai ulang, serahkan ke perangkaian + triase

1. Nilai ulang: dampak akhir vs dampak sinyal awal — bila dampak akhir tidak lebih besar dari sinyal awal, laporkan sinyal awalnya saja, jangan klaim rantai.
2. Catat jumlah interaksi korban yang dibutuhkan (0-klik / 1-klik / lebih) dengan jujur — itu memengaruhi tier hadiah.
3. Serahkan rantai yang terbukti ke `perangkaian-kerentanan` (dirangkai sebagai laporan rantai) → `penilaian-cvss` + `artikulasi-dampak-bisnis` (dihitung dari dampak AKHIR — untuk Pola 12–13 dari dampak eksposur yang diartikulasikan, dengan catatan jujur bahwa pemakaian kuncinya tidak dibuktikan) → `triase-duplikat` → draf laporan → tinjau manusia → persetujuan Cipta → kirim.
4. **Standar lulus:** keputusan tercatat di log dengan alasan + jumlah klik/interaksi korban tertulis jujur + dampak akhir vs awal dibandingkan.

## Validation Gate (verifikasi deterministik baseline vs exploit)

- Baseline: tiap langkah eskalasi dibandingkan dengan perilaku normal tanpa payload (mis. GET sebagai pemilik sah → data sendiri; bundle JS tanpa secret → tidak ada temuan; endpoint error normal → tidak ada jejak env). Bila perilaku exploit sama dengan baseline, langkah itu bukan celah.
- Exploit: rantai lengkap HARUS terulang dari sesi bersih + token segar, minimal 1 kali pengulangan penuh sesudah pembuktian pertama; dampak akhir HARUS teramati pada akun sendiri (Pola 11) atau eksposur HARUS teramati ulang pada respons segar (Pola 12–13), bukan sekadar pesan sukses dari server (silent drop).
- Verdict TERBUKTI hanya sah bila perbandingan baseline-vs-exploit tiap langkah tertulis di log dengan reference ID bukti.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (penyerang + korban) | Wajib untuk Pola 11 — kedua sisi rantai memakai akun milik sendiri |
| Objek canary milik sendiri | Wajib untuk Pola 11 — satu-satunya objek yang diubah/dihapus dalam uji tulis; DELETE hanya pada objek canary sekali-pakai |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian |
| Server canary sendiri | Bila diperlukan untuk membuktikan alur terkait (catat hit-nya saja, jangan ambil isinya) |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis eskalasi + langkah yang gagal/berhasil + bukti dampak akhir atau eksposur + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur]
Sinyal awal: [nama + reference ID bukti + skor triase awal]
Hipotesis eskalasi: [nomor pola (11/12/13) + rantai yang diduga]
Langkah eskalasi:
  - Langkah 1: [apa yang diuji] — TERBUKTI/GAGAL — [reference ID bukti]
  - Langkah 2: [apa yang diuji] — TERBUKTI/GAGAL — [reference ID bukti]
Dampak akhir terbukti: [apa yang terjadi pada akun sendiri / eksposur tersensor + putusan A60 / BELUM TERBUKTI — berhenti di langkah X]
Interaksi korban: [0-klik / 1-klik / lebih — jelaskan]
Dampak akhir vs awal: [lebih besar / sama — bila sama, laporkan sinyal awal saja]
Keputusan: [maju ke perangkaian-kerentanan / laporkan sinyal awal / dibuang + alasan]
Status: [tereskalasi / tidak ada rantai / ditolak]
```

## Batasan yang diketahui

- Eskalasi yang butuh interaksi korban dinilai lebih rendah oleh sebagian program — catat jujur, jangan sembunyikan.
- Dua temuan pada target/program yang berbeda umumnya TIDAK bisa dirangkai jadi satu laporan.
- Katalog pola 11–13 tidak lengkap — pola baru yang ditemukan di lapangan ditambahkan ke katalog dengan nomor baru + dicatat tanggalnya, bukan dipakai diam-diam.
- Pola 12 dan 13 sengaja TIDAK membuktikan dampak akhir lewat pemakaian secret/kunci temuan — klaim maksimalnya adalah eksposur. Bila suatu program secara eksplisit mengizinkan pembuktian pemakaian kunci terhadap akun sendiri dan Cipta menyetujuinya secara tertulis untuk kasus itu, putusan itu dicatat di log sebagai pengecualian per-kasus — bukan sebagai perubahan aturan skill ini.
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome — gunakan `transfer-hunting` untuk rantai prompt AI, bukan skill ini.

### Available connectors

Tidak ada konektor khusus untuk skill ini; pengujian memakai curl/klien HTTP, dua akun uji sendiri, dan log `~/workspace/catatan/log-bug-bounty.md`.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi target (endpoint API dan alur OAuth/SSO yang diuji).

### Alternatives for better results

- Bila endpoint Pola 11 hanya menerima metode tulis lewat antarmuka web (bukan API langsung), uji tetap dilakukan lewat antarmuka itu dengan akun sendiri, dan baca-ulang state tetap wajib — pesan sukses UI saja bukan bukti.
- Bila bundle JS Pola 12 hanya tersedia lewat situs (bukan bucket), jalankan `analisis-statis-js` langsung pada bundle situs — pola ini tetap berlaku selama bundle itu kode aplikasi publik; yang berubah hanya sumber Signal-nya (bukan listing S3).
- Bila respons debug Pola 13 hanya berisi nama variabel tanpa nilai, jangan memaksakan klaim kebocoran kredensial — catat sebagai info disclosure rendah dan serahkan ke triase apa adanya.
