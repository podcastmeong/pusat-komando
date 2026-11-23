# Skill: Daftar-Tolak-Selalu — Daftar Hitam Otomatis Pola Sampah (Tanpa Probing)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` Bagian 1 (Always-Reject List). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu kandidat yang ditolak gerbang ini dan dicatat di log.

## Pemicu (Trigger & Scope)

Dipakai untuk SETIAP kandidat temuan segera sesudah program dan asetnya dipastikan in-scope (catatan scope dari `parsing-scope-program` / `scope-and-safety-guardian`) dan **SEBELUM** probing apa pun, sebelum `gerbang-tujuh-pertanyaan-triase`, sebelum `skeptic-false-positive-eliminator`, dan sebelum draf laporan apa pun. Satu kandidat = satu kali pencocokan terhadap daftar di bawah. Tidak ada jalan pintas, tidak ada "pola ini mungkin pengecualian".

Skill ini adalah **filter pola nol-probing**: tugasnya membuang pola sampah dengan pencocokan pola + satu langkah konfirmasi murah — BUKAN dengan menguji eksploitasi. Bila pola cocok, kandidat dibuang tanpa satu pun request eksploitasi dikirim. Skill ini TIDAK menilai dampak (itu tugas `gerbang-sinyal-dampak` + `skeptic-false-positive-eliminator`) dan TIDAK memberi skor (itu tugas `triase-duplikat`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Mencocokkan kandidat terhadap daftar, memutuskan TOLAK / LANJUT beserta alasan |
| Audit | **A60 Security Auditor** | Memeriksa verdict penolakan; A60 tidak meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan kandidat yang lolos daftar ini maju ke gerbang tujuh pertanyaan |

## Sudah tercakup (jangan diduplikat)

- **Daftar noise umum** (missing SPF/DMARC/DKIM, clickjacking non-sensitif, missing security headers, info versi, Self-XSS, data publik, rate-limit, halaman error generik) ada di `gerbang-tujuh-pertanyaan-triase` Pertanyaan 4 dan `skeptic-false-positive-eliminator` Gerbang 2 — daftar di bawah ini HANYA berisi pola yang **BELUM ADA** di kedua daftar itu. Jangan menyalin kategori dari sana ke sini.
- **Gerbang dampak per jenis sinyal** (mis. Open Redirect hanya valid pada alur sensitif + bocor token) ada di `gerbang-sinyal-dampak` — skill ini berjalan SEBELUM gerbang itu dan tidak mengulang tabel sinyalnya. Pola di sini ditolak TANPA probing; sinyal di sana ditolak HANYA sesudah probing membuktikan dampak tidak ada.
- **Temuan di kode pengujian / contoh / dokumentasi** dicegah di hulu oleh `kebersihan-worktree` (direktori test/benchmark/docs disingkirkan SEBELUM pemindaian repo lokal) — daftar ini adalah jaring pengaman kedua bila temuan semacam itu tetap lolos ke triase.
- Alur sesudah skill ini: LANJUT (tidak ada pola yang cocok) → `gerbang-tujuh-pertanyaan-triase` (7 pertanyaan) → `gerbang-sinyal-dampak` (syarat eskalasi per jenis) → `skeptic-false-positive-eliminator` (4 gerbang) → `triase-duplikat` (cek duplikat + skor) → draf laporan → tinjau manusia → persetujuan Cipta → kirim. TOLAK → catat alasan di log, kembali ke riset/varian, tanpa probing lanjutan.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = TOLAK, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.** LANJUT di daftar ini bukan izin kirim — izin kirim tetap dari Cipta.
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Daftar ini tidak butuh probing sama sekali — bila satu pola butuh request eksploitasi untuk memastikannya, itu BUKAN pola daftar ini; serahkan ke `gerbang-sinyal-dampak`.
8. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.
9. **Sensor PII/token/kredensial di semua bukti ([REDACTED]) sebelum laporan disusun.**
10. **Jangan pernah mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia dulu; pengiriman selalu manual + disetujui Cipta.
11. **Pola yang cocok = TOLAK PERMANEN.** Tidak ada "lolos sebagian", tidak ada pengecualian diam-diam. Kandidat yang ditolak boleh kembali HANYA sebagai kandidat BARU bila pola penolaknya terbukti salah terpasang (mis. kode yang dikira mati ternyata terpanggil) — dengan bukti baru, bukan dengan mengubah verdict.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Methodology — Signal, langkah konfirmasi, dan Execution Gate per pola

Cocokkan kandidat terhadap SETIAP pola di bawah, berurutan. Langkah konfirmasi tiap pola adalah pemeriksaan murah (baca kode / hitung prasyarat / pindai kata kunci) — BUKAN probing eksploitasi. Bila satu pola cocok dan terkonfirmasi = TOLAK PERMANEN, berhenti, jangan lanjut ke pola berikutnya.

### Pola 1 — Dead code (celah di kode yang tidak pernah dieksekusi)

- **Signal:** dugaan kerentanan berada di kode yang tidak terjangkau dari input mana pun yang bisa dijangkau penyerang — mis. fungsi yang tidak pernah dipanggil, cabang (branch) yang kondisinya tidak pernah benar, berkas yang tidak diimpor/dirujuk modul mana pun, atau kode di balik feature flag yang mati / tidak pernah diaktifkan di deployment in-scope.
- **Langkah konfirmasi (bukan probing):**
  1. Telusur call graph / rujukan: dari titik masuk (endpoint, handler, rute) yang in-scope, adakah jalur pemanggilan sampai ke fungsi/berkas yang diduga rentan? Catat jalurnya (atau ketiadaan jalur) dengan file + baris.
  2. Periksa feature flag / kondisi cabang: apakah kondisi yang mengaktifkan kode itu bisa benar di deployment in-scope (bukan hanya "bisa benar di teori")?
  3. Bila ragu, minta `kopilot-analisis-kode` membuktikan keterjangkauan dengan kutipan kode — jawaban tanpa kutipan = belum terbukti terjangkau.
- **Execution Gate:** **TOLAK PERMANEN bila** tidak ada jalur dari titik masuk in-scope ke kode itu, atau kondisi pengaktifnya tidak pernah benar di deployment in-scope. **LANJUT bila** ada satu jalur keterjangkauan tertulis (file + baris pemanggil) — kandidat diteruskan ke `gerbang-tujuh-pertanyaan-triase`, bukan langsung lolos sebagai temuan.

### Pola 2 — Source map tanpa kredensial

- **Signal:** source map (`.js.map`) terekspos dan bisa diunduh, dan itu SATU-SATUNYA isi temuan — tidak ada kredensial, rahasia, atau endpoint sensitif yang ditunjukkan dari dalamnya.
- **Langkah konfirmasi (bukan probing):**
  1. Pulihkan kode dari source map (cara di `analisis-statis-js` Gerbang 1) dan pindai isinya untuk kredensial/rahasia: kunci API, token, kata sandi, `client_secret`, URL internal, endpoint admin yang tidak ada di bundle publik.
  2. Bandingkan dengan bundle publik: apakah source map membongkar sesuatu yang TIDAK ada di bundle `.js` yang sama (yang juga publik)?
- **Execution Gate:** **TOLAK PERMANEN bila** source map tidak mengandung kredensial/rahasia apa pun, atau isinya sama dengan yang sudah terlihat di bundle publik. **LANJUT bila** ada kredensial/rahasia nyata atau endpoint sensitif yang hanya terlihat lewat source map — kandidat diteruskan ke `gerbang-sinyal-dampak` (baris S3/listing tidak berlaku; yang berlaku adalah pembuktian rahasia itu aktif, seperti Baris 5 Debug Endpoint). Source map yang berisi rahasia BUKAN pola ini — jangan tolak.

### Pola 3 — Bug butuh 4+ prasyarat tidak realistis

- **Signal:** eksploitasi dugaan temuan menuntut BANYAK kondisi yang harus benar serentak, dan kondisi-kondisi itu di luar kendali penyerang serta tidak umum terjadi.
- **Langkah konfirmasi (bukan probing):**
  1. Tulis DAFTAR prasyarat, satu per baris, masing-masing dengan jawaban: apakah penyerang bisa memaksakan kondisi ini (YA/TIDAK) dan apakah kondisi ini umum terjadi di deployment in-scope (YA/TIDAK)?
  2. Hitung prasyarat yang TIDAK BISA dipaksakan penyerang DAN tidak umum terjadi. Contoh prasyarat tidak realistis: admin harus membuka berkas tertentu pada saat tertentu; korban harus memakai browser versi yang sudah tidak didukung; konfigurasi langka yang bukan bawaan; dua kejadian waktu yang harus bersamaan dalam hitungan milidetik tanpa alat bantu; korban harus sudah login sebagai peran yang hampir tidak ada.
  3. Prasyarat yang REALISTIS (mis. "korban mengklik satu tautan" = 1-klik; "penyerang punya akun biasa" = akun sendiri) TIDAK dihitung — catat jujur, jangan digelembungkan supaya lolos ambang.
- **Execution Gate:** **TOLAK PERMANEN bila** jumlah prasyarat tidak realistis **≥ 4**. **LANJUT bila** jumlahnya 0–3 — kandidat diteruskan ke `gerbang-tujuh-pertanyaan-triase`, dengan daftar prasyaratnya dilampirkan supaya penilai berikutnya tidak menghitung ulang dari nol. Ambang 4 adalah aturan riset (bukan hukum alam): bila program tertentu menyatakan ambang lain secara tertulis di aturan programnya, ambang program itu yang menang — catat sumbernya di log.

## Gerbang Akhir — Verdict

- **LANJUT** — tidak satu pun pola cocok (atau pola yang dicurigai gagal terkonfirmasi) → kandidat maju ke `gerbang-tujuh-pertanyaan-triase`.
- **TOLAK PERMANEN** — satu pola cocok dan terkonfirmasi → kandidat dibuang; catat pola + bukti konfirmasi di log; jangan ajukan lagi dengan bukti yang sama. Satu-satunya jalan kembali: kandidat BARU dengan bukti bahwa pola penolaknya salah terpasang (mis. jalur keterjangkauan yang sebelumnya terlewat, dengan kutipan kode).

## Alat

| Alat | Cara pakai |
|---|---|
| Call graph / pencarian rujukan kode (`grep` / `rg`, peta dari `kopilot-analisis-kode` Gerbang 1) | Konfirmasi Pola 1: ada/tidak ada jalur dari titik masuk ke kode yang diduga rentan |
| Pemulih source map (cara di `analisis-statis-js` Gerbang 1) + pindai kata kunci rahasia | Konfirmasi Pola 2: ada/tidak ada kredensial di source map |
| Daftar prasyarat tertulis (format di bawah) | Konfirmasi Pola 3: hitung prasyarat tidak realistis |
| `~/workspace/catatan/log-bug-bounty.md` | Catat verdict tiap kandidat (lihat Format output) |

## Human-in-the-loop

- A60 mengaudit verdict penolakan sebelum kandidat dibuang dari antrean. Bila A60 tidak setuju satu pencocokan pola, kandidat dikembalikan ke antrean — bukan dinegosiasi.
- LANJUT di daftar ini bukan izin kirim laporan. Draf VERIFIED tetap ditinjau manusia 2–3 menit dan hanya dikirim bila **Cipta menyetujui**.

## Format output

Catat setiap kandidat di `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Kandidat: <nama temuan singkat> | Program: <nama>
  - Pola 1 (dead code): COCOK/TIDAK — <jalur keterjangkauan ada/tidak + file:baris>
  - Pola 2 (source map tanpa kredensial): COCOK/TIDAK — <rahasia ditemukan/tidak + isi yang dipindai>
  - Pola 3 (4+ prasyarat tidak realistis): COCOK/TIDAK — <jumlah prasyarat tidak realistis>/daftar:
      1. <prasyarat> — bisa dipaksakan: YA/TIDAK — umum terjadi: YA/TIDAK
  - Verdict akhir: LANJUT / TOLAK PERMANEN — <pola penolak bila ditolak / alasan satu kalimat>
```

Kandidat TOLAK berhenti di sini — dicatat, tidak dihapus dari log, tidak dikirim ke mana pun. Kandidat LANJUT diteruskan ke `gerbang-tujuh-pertanyaan-triase` dengan catatan pola di atas dilampirkan.

## Batasan yang diketahui

- Daftar di atas hanya berisi pola dari riset Bagian 1 — pola sampah baru yang ditemukan di lapangan ditambahkan dengan nomor baru + dicatat tanggalnya, bukan dipakai diam-diam. Pola baru wajib menyebut Signal, langkah konfirmasi, dan Execution Gate-nya, dan wajib diperiksa dulu apakah pola itu sudah ada di `gerbang-tujuh-pertanyaan-triase` Q4 atau `skeptic-false-positive-eliminator` Gerbang 2 (bila sudah ada, JANGAN ditambahkan di sini).
- Ambang "4+ prasyarat" adalah aturan riset — program tertentu bisa menetapkan ambang lain; aturan program tertulis menang.
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome — terapkan daftar ini pada outcome-nya (mis. rantai prompt yang butuh 4+ kondisi tidak realistis = tolak), tapi jangan paksakan Pola 1–2 bila outcome-nya bukan kode.
