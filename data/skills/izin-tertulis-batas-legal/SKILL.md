# Skill: Izin Tertulis & Batas Legal — Garis yang Membedakan Ethical Hacker dari Kriminal

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 7 (FAQ), 24 Nov 2026. Pemeriksaan izin ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill scope/gate — mengatur IZIN SEBELUM PENGUJIAN APA PUN — BUKAN skill pengujian: skill ini tidak memberi langkah untuk menemukan atau mengeksploitasi kerentanan. Skill ini bukan nasihat hukum; bila ada keraguan hukum, serahkan ke Muse/Cipta sebelum langkah apa pun.

## Pemicu

Dipakai SEBELUM pengujian apa pun dimulai, setiap kali target atau program berganti, setiap kali scope program berubah, dan setiap kali ada keraguan apakah suatu target masih diizinkan. Dipakai juga saat membedakan ethical hacker dari cyber criminal dalam diskusi tim — pembedanya adalah izin + niat, bukan teknik yang dipakai (tekniknya bisa sama persis).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Penjaga izin | **Muse** | Memutuskan izin sah/tidak untuk tiap target; menghentikan pengujian bila izin tidak jelas |
| Pengerjaan | **A59 Threat Hunter, A58 Vulnerability Researcher** | Membuktikan izin tertulis sebelum menguji; mencatat bukti izin di log |
| Audit | **A60 Security Auditor** | Memvalidasi bukti izin sebelum pengujian maju (A60 tidak meloloskan izin untuk temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan eskalasi ke Cipta bila izin diragukan atau dicabut |

## Sudah tercakup (jangan diduplikat)

- Etika + kerahasiaan data temuan → skill `etika-kerahasiaan-data-bounty`. Skill ini TIDAK mengulang aturan penanganan data — skill ini mengatur IZIN MASUKNYA pengujian (sebelum data apa pun tersentuh).
- Pemantauan program (scope/hadiah/deadline) → skill `recon-pantau-program`. Skill ini memakai scope yang dipantau skill itu sebagai BUKTI izin; cara memantaunya tetap di sana.
- Pola pikir penyerang → skill `pola-pikir-penyerang-analitis`. Skill ini tidak mengatur pola pikir — skill ini mengatur BATAS tempat pola pikir itu boleh diterapkan.
- Sertifikasi (EC-Council) sebagai rujukan kredibilitas → sudah dicatat di skill `etika-kerahasiaan-data-bounty`. Skill ini tidak mengulang pembahasan sertifikasi.

## Prinsip izin

1. **Izin + niat adalah pembedanya.** Ethical hacker bekerja DENGAN izin tertulis dan resmi dari pemilik sistem/perusahaan, dengan niat meningkatkan keamanan dan melindungi data. Cyber criminal bekerja TANPA izin, demi keuntungan pribadi, merugikan orang lain, dan melanggar hukum. Tekniknya bisa sama — izin dan niatnya yang berbeda.
2. **Legal dan etis kuncinya izin.** Ethical hacking itu legal dan etis — kuncinya IZIN: hanya bekerja setelah mendapat izin tertulis dan resmi; patuhi hukum siber + standar etika profesional.
3. **Scope program = izin tertulis.** Untuk bounty, scope resmi program adalah izin tertulisnya: target in-scope = diizinkan; target out-of-scope = TIDAK diizinkan, meskipun secara teknis bisa dijangkau.
4. **Izin yang tidak jelas = tidak ada izin.** Bila ragu apakah suatu target diizinkan, perlakukan sebagai TIDAK diizinkan sampai Muse/Cipta memastikan. Jangan menebak izin.
5. **Izin bisa dicabut.** Izin yang sudah ada bisa berakhir (program tutup, scope berubah, akun dicabut). Periksa ulang sebelum tiap pengujian, bukan sekali di awal saja.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pengujian hanya di akun dan data milik sendiri atau canary palsu — dan tetap harus di dalam izin program.
3. **Tanpa data orang lain.** Jangan menyentuh, menyimpan, atau memakai data pengguna lain, meskipun targetnya in-scope.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan atau akun yang bukan milik sendiri DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan, meskipun targetnya in-scope.
6. **Tanpa payload di permukaan publik.** Bukti izin, catatan scope, dan draf jangan di-host atau dibagikan di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Bukti izin harus diperiksa Muse/A60 sebelum pengujian — jangan serahkan keputusan izin ke otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data apa pun — termasuk data target in-scope. DILARANG memakai izin program untuk mengakses akun siapa pun, memeras, mengancam, atau memperoleh keuntungan di luar hadiah bounty resmi.

## Langkah + gerbang

### Gerbang 0 — Buktikan izin tertulis

1. Sebelum pengujian apa pun: catat bukti izin — (a) nama program (satu dari sembilan resmi); (b) teks scope yang mengizinkan target itu (kutip atau ringkas + sumber); (c) tanggal scope dibaca; (d) jalur laporan resmi program.
2. **Standar lulus:** keempat bukti tercatat di log + diperiksa A60. Tanpa bukti izin = jangan lanjut ke pengujian apa pun.

### Gerbang 1 — Petakan batas scope

1. Tulis batasnya secara eksplisit: target APA SAJA yang diizinkan, target apa yang DILARANG, teknik apa yang dilarang program (mis. DoS, social engineering terhadap karyawan, pengujian akun orang lain), dan kapan program tutup.
2. **Standar lulus:** daftar batas tertulis; agent bisa menyebutkan satu target yang dilarang program tanpa membaca catatan. Batas yang kabur = tanyakan ke Muse sebelum lanjut.

### Gerbang 2 — Periksa izin masih berlaku

1. Sebelum tiap sesi pengujian: periksa ulang apakah scope berubah, program masih buka, dan akun masih aktif. Program yang akan tutup: BERHENTI 1 hari sebelumnya (aturan tim).
2. **Standar lulus:** tanggal pemeriksaan terakhir tercatat. Pemeriksaan lebih dari 7 hari lalu = periksa ulang sekarang.

### Gerbang 3 — Hentikan bila ragu

1. Bila di tengah pengujian muncul keraguan (target ternyata di luar scope, scope berubah, izin dicabut, atau ada data orang lain yang tersentuh): BERHENTI SEGERA, catat posisi terakhir, laporkan ke Muse. Jangan melanjutkan "sedikit lagi".
2. **Standar lulus:** penghentian + laporan ke Muse tercatat. Pengujian yang dilanjutkan dalam keraguan = pelanggaran — laporkan juga bila itu terjadi.

### Gerbang 4 — Serahkan bukti izin bersama temuan

1. Setiap draf laporan temuan WAJIB melampirkan bukti izin (Gerbang 0) — supaya triase dan program bisa melihat bahwa pengujian dilakukan dengan izin.
2. **Standar lulus:** draf tanpa bukti izin = DITOLAK triase, lengkapi dulu.

## Alat

| Alat | Cara pakai |
|---|---|
| Halaman scope resmi tiap program | Sumber bukti izin (Gerbang 0) — baca langsung dari program, bukan dari ringkasan pihak ketiga |
| Skill `recon-pantau-program` | Pemantauan perubahan scope/hadiah/deadline (Gerbang 2) |
| Skill `etika-kerahasiaan-data-bounty` | Aturan penanganan data setelah izin terbukti |
| `~/workspace/catatan/log-bug-bounty.md` | Log bukti izin + batas scope + pemeriksaan ulang + penghentian + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [satu dari sembilan program resmi]
Target: [nama target]
Bukti izin: [teks scope yang mengizinkan + sumber + tanggal dibaca]
Batas scope: [diizinkan: ... / dilarang: ... / teknik dilarang: ... / tutup: ...]
Pemeriksaan terakhir: [tanggal]
Keraguan/penghentian: [tidak ada / ada — kapan + kenapa + laporan ke Muse]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Skill ini mengatur pembuktian izin, bukan memberi nasihat hukum. Bila suatu temuan berpotensi menyentuh wilayah hukum (mis. data anak, kesehatan, keuangan, atau yurisdiksi lain), serahkan ke Muse/Cipta sebelum langkah apa pun.
- Scope program bisa berubah tanpa pemberitahuan panjang — karena itu Gerbang 2 (periksa ulang tiap sesi) wajib, bukan opsional.
- Sertifikasi (mis. EC-Council) tidak wajib untuk bounty, tetapi sangat disarankan sebagai kredibilitas profesional — skill ini mencatat itu sebagai fakta, bukan sebagai syarat untuk menguji.
- Izin program TIDAK mencakup pengujian terhadap karyawan program, pengguna lain, atau sistem di luar scope — meskipun tekniknya sama dengan yang diizinkan.

### Available connectors

Tidak ada konektor khusus untuk skill ini; bukti izin dicatat manual di log dan divalidasi A60/Muse.

### Websites

- Halaman scope + kebijakan disclosure resmi tiap program (sumber bukti izin — satu-satunya sumber yang sah).
- Kode etik EC-Council sebagai rujukan standar etika profesional (hanya rujukan — bukan isi skill ini).

### Alternatives for better results

- Bila scope program ditulis dalam bahasa yang sulit dipahami, ringkas dengan kata sendiri dan minta A60 memeriksa ringkasan itu — ringkasan yang salah sama berbahayanya dengan tidak membaca scope.
- Bila dua program punya aturan yang bertentangan untuk target serupa, ikuti aturan yang PALING ketat — lebih aman berhenti daripada melanggar.
- Bila program tidak punya scope tertulis sama sekali, perlakukan sebagai TIDAK ADA IZIN: jangan uji sampai ada izin tertulis yang jelas.
