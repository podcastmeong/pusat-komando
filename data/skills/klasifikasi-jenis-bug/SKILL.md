# Skill: Klasifikasi Jenis Bug — Taksonomi 9 Jenis Bug untuk Triase Hunter (Mana yang Dibayar, Mana yang Tidak)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 19 (artikel Vascomm "9 Jenis Bug dalam Software Development dan Cara Mengatasinya"), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill KLASIFIKASI — taksonomi 9 jenis bug yang dipakai saat triase untuk menentukan: jenis bug apa ini, apakah jenis ini umumnya dibayar program bounty, dan prioritas apa yang pantas. Skill ini BUKAN skill pengujian: tidak ada langkah menyerang di sini — klasifikasi dilakukan ATAS temuan kandidat yang sudah ada.

## Pemicu

Dipakai setiap kali temuan kandidat perlu diklasifikasikan sebelum triase — SETELAH validasi (`skeptic-false-positive-eliminator`) dan SEBELUM `triase-duplikat`. Dipakai juga saat memilah banyak kandidat: mana yang diteruskan, mana yang dicoret karena jenisnya tidak dibayar program.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Mengklasifikasikan tiap temuan kandidat ke 1 dari 9 jenis; menentukan kelayakan bounty |
| Audit | **A60 Security Auditor** | Memvalidasi klasifikasi (jenis yang dipilih harus cocok dengan bukti) |
| Pemimpin | **Muse** | Memutuskan kandidat mana yang diteruskan berdasarkan klasifikasi |

## Taksonomi 9 jenis bug (dengan nilai bounty)

| # | Jenis | Ciri | Nilai bounty |
|---|---|---|---|
| 1 | Fungsional | Aplikasi tidak bekerja sesuai fungsi (tombol login tidak berfungsi, fitur utama hasil salah) | Umumnya RENDAH / sering out-of-scope — kecuali fungsionalitas keamanan |
| 2 | Performa | Aplikasi lambat, boros resource, loading tidak wajar | Umumnya RENDAH / tidak dibayar — kecuali DoS (dan DoS DIBLOKIR di sini) |
| 3 | Usabilitas | UI sulit/membingungkan; cacat desain interaksi, bukan kesalahan teknis | Umumnya TIDAK DIBAYAR |
| 4 | Kompatibilitas | Hanya jalan di satu tempat (browser/perangkat tertentu) | Umumnya TIDAK DIBAYAR |
| 5 | Keamanan | Kerentanan kode yang bisa dieksploitasi (SQLi, XSS, dsb.) | PALING BERBAYAR — fokus utama perburuan |
| 6 | Sintaks | Kesalahan ketik/tanda baca; kode tidak bisa dikompilasi/dijalankan | TIDAK DIBAYAR (tertangkap compiler) |
| 7 | Logika | PALING SULIT dideteksi; kode jalan tanpa error tapi hasil salah (kalkulator harusnya menjumlah malah mengurang) | BERBAYAR bila berdampak keamanan (business logic flaw) |
| 8 | Tingkat Unit | Kesalahan pada unit kode terkecil (fungsi/metode); bisa jadi dasar masalah besar saat integrasi | Tergantung dampak — diteruskan bila terbukti berdampak |
| 9 | Tingkat Sistem | Interaksi antar komponen/modul tidak berjalan baik; sulit direplikasi; bisa menyebabkan kegagalan total/downtime | BERBAYAR bila terbukti + berdampak keamanan |

## Sudah tercakup (jangan diduplikat)

- Triase + duplikat → skill `triase-duplikat`. Skill ini memberi KLASIFIKASI JENIS sebagai masukan triase — bukan memutuskan duplikat.
- Penilaian severity → skill `penilaian-cvss`. Skill ini mengklasifikasikan JENIS, bukan skor.
- Bug logika bisnis → skill `perburuan-kerentanan-spesifik` + `pelompakan-alur-state-machine`. Skill ini mengklasifikasikan bug logika sebagai JENIS — pengujian logikanya tetap di skill itu.
- Siklus hidup + template bug report → skill `siklus-hidup-bug-report`. Skill ini mengklasifikasikan JENIS bug — bukan menulis laporannya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Klasifikasi adalah pekerjaan di atas kertas atas temuan yang sudah ada.
3. **Tanpa data orang lain.** Tanpa memakai data korban atau data pihak ketiga.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Klasifikasi tidak mengirim request ke target. (Bug performa yang mengarah ke DoS TIDAK diuji — DoS diblokir.)
6. **Tanpa payload di permukaan publik.** Klasifikasi hanya di log internal dan jalur resmi program.
7. **Klasifikasi harus cocok dengan bukti.** Satu temuan = satu jenis utama (+ satu jenis sekunder bila benar-benar tumpang tindih). Jangan memaksakan jenis "keamanan" pada bug fungsional agar terlihat dibayar.
8. **Validasi human-in-the-loop.** Setiap klasifikasi harus diperiksa manusia (Muse/A60) sebelum jadi keputusan teruskan/coret.
9. **Tanpa laporan tanpa persetujuan Cipta.** Klasifikasi ini bahan triase internal; temuan tetap lewat jalur draf → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengklasifikasikan ulang bug non-keamanan sebagai keamanan untuk menipu program. Klasifikasi di sini HANYA jujur berdasarkan bukti.

## Langkah + gerbang

### Gerbang 0 — Klasifikasikan tiap temuan kandidat

1. Untuk tiap temuan kandidat, tentukan jenis utamanya dari 9 taksonomi di atas + alasan (ciri mana yang cocok dengan bukti). Bila tumpang tindih, tambah jenis sekunder.
2. **Standar lulus:** tiap temuan punya jenis utama + alasan. Jenis tanpa alasan = belum diklasifikasikan.

### Gerbang 1 — Tentukan kelayakan bounty per jenis

1. Terapkan tabel nilai bounty: jenis Keamanan + Logika (berdampak keamanan) + Sistem (terbukti + berdampak keamanan) → TERUSKAN. Jenis Fungsional/Performa/Usabilitas/Kompatibilitas/Sintaks → umumnya CORET, kecuali ada bukti dampak keamanan yang jelas (bila ada, tulis buktinya dan teruskan sebagai pengecualian). Jenis Unit → teruskan hanya bila terbukti berdampak.
2. **Standar lulus:** tiap temuan punya verdict (teruskan/coret) + alasan berdasarkan tabel. Verdict tanpa alasan = belum diputuskan.

### Gerbang 2 — Perhatikan pola: bug logika + bug sistem

1. Untuk temuan jenis Logika dan Sistem, catat pola khususnya: bug logika paling sulit dideteksi (kode jalan tanpa error, hasil salah) — periksa dengan `analisis-anomali` (hasil vs yang diharapkan). Bug sistem sulit direplikasi — catat kondisi replikasi selengkap mungkin (`siklus-hidup-bug-report`).
2. **Standar lulus:** temuan Logika/Sistem punya catatan pola + kondisi replikasi. Tanpa itu = belum siap triase.

### Gerbang 3 — Serahkan ke triase

1. Serahkan temuan yang lolos (teruskan) + klasifikasinya ke `triase-duplikat`. Yang dicoret dicatat di log dengan alasan (bukan dihapus tanpa jejak). Skill ini BERHENTI di sini.
2. **Standar lulus:** tiap temuan punya status akhir (diteruskan/dicoret + alasan) tercatat di log. Skill ini tidak mencatat "temuan" — hanya "klasifikasi diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Tabel taksonomi 9 jenis (di atas) | Acuan klasifikasi + nilai bounty |
| `analisis-anomali` | Membantu mengklasifikasikan bug Logika (hasil vs diharapkan) |
| `siklus-hidup-bug-report` | Kondisi replikasi untuk bug Sistem yang sulit direplikasi |
| `triase-duplikat` + `penilaian-cvss` | Penerima temuan yang lolos klasifikasi |
| `~/workspace/catatan/log-bug-bounty.md` | Log klasifikasi: temuan → jenis → verdict → alasan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Temuan: [judul kandidat]
Jenis: [utama: ... — sekunder: ... — alasan: ...]
Kelayakan bounty: [teruskan/coret — alasan berdasarkan tabel]
Pola khusus: [logika/sistem — catatan pola + kondisi replikasi]
Validasi A60: [ya/tidak]
Diserahkan ke triase: [ya/tidak — atau dicoret: alasan]
Yang TIDAK dilakukan: [tanpa mengklasifikasikan ulang demi pembayaran]
Status: [klasifikasi selesai / diserahkan]
```

## Batasan yang diketahui

- Taksonomi ini dibuat untuk bug software UMUM — batas antar jenis bisa kabur (mis. bug fungsional yang ternyata berdampak keamanan). Bila ragu, klasifikasikan berdasarkan DAMPAK KEAMANAN yang terbukti, bukan berdasarkan gejala permukaan.
- Nilai bounty per jenis adalah KECENDERUNGAN umum, bukan aturan program: tiap program punya kebijakan sendiri. Selalu periksa aturan program (`membaca-scope-penyelenggara`) — scope program menang atas tabel ini.
- Bug Performa yang mengarah ke DoS TIDAK diuji di sini (DoS diblokir). Jangan memakai klasifikasi ini sebagai alasan untuk menguji DoS.
- Skill ini tidak membahas cara memperbaiki tiap jenis bug (itu pekerjaan developer) — hanya klasifikasi + kelayakan bounty dari sisi hunter.
