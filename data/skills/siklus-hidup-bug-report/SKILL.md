# Skill: Siklus Hidup Bug Report — Template Laporan QA, Severity vs Priority, dan Alur Open sampai Closed

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 15 (skill menulis bug report) + batch 16 (artikel Medium "Bug Report" Fauzan Ahmat Rahmawan) + batch 18 (artikel Logique "Cara Membuat Bug Report"), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill TEMPLATE + SIKLUS bug report gaya QA yang dipakai di dalam perburuan bounty: (a) menulis bug report yang jelas (judul, langkah reproduksi, aktual vs ekspektasi, bukti, lingkungan, severity + priority); (b) memahami siklus hidup bug (Open → Assigned → Fixing → Re-Test → Closed, dengan loop Re-Open); (c) membedakan severity (ditentukan penemu) dari priority (ditentukan bersama). Skill ini MELENGKAPI skill laporan bounty (`penulisan-laporan-bounty`, `laporan-poc-otomatis`) dengan disiplin QA — bukan menggantikannya: laporan ke program tetap mengikuti format program, template di sini dipakai untuk DRAF internal + lampiran bukti.

## Pemicu

Dipakai setiap kali temuan kandidat perlu didokumentasikan sebagai bug report internal yang rapi — SEBELUM draf laporan bounty ditulis. Dipakai juga saat menindaklanjuti status temuan yang sudah disubmit (apakah sudah diperbaiki? perlu re-test? perlu Re-Open?).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A67 Report Writer** | Menulis bug report internal dari bahan temuan; melacak status siklus hidup |
| Audit | **A60 Security Auditor** | Memvalidasi isi bug report (judul, langkah, severity) sebelum jadi draf laporan |
| Pemimpin | **Muse** | Memutuskan severity + priority yang dicantumkan dan kapan Re-Open diajukan |

## Sudah tercakup (jangan diduplikat)

- Struktur laporan bounty per platform → skill `penulisan-laporan-bounty`. Skill ini menambah TEMPLATE QA (aktual vs ekspektasi, lingkungan, severity vs priority) sebagai draf internal — format akhir ke program tetap ikut skill itu.
- Laporan PoC terstruktur (reproduksi curl/Python + saran perbaikan) → skill `laporan-poc-otomatis`. Skill ini tidak mengulang struktur PoC itu.
- Struktur dasar laporan (judul → ringkasan → repro → bukti → scope → dampak) → skill `laporan-abstrak`. Skill ini memakai struktur itu dan menambahkan disiplin QA di dalamnya.
- Triase + duplikat → skill `triase-duplikat`. Skill ini tidak memutuskan duplikat — hanya mendokumentasikan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Bug report HANYA dari pengujian akun sendiri. Tanpa data orang lain.
3. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
4. **Tanpa DoS/DDoS.** Jangan membanjiri target.
5. **Tanpa payload di permukaan publik.** Bug report internal hanya di log internal dan jalur resmi program.
6. **Judul spesifik atau jangan tulis.** Judul umum ("Landing page error", "Aplikasi rusak") DILARANG — judul harus menyebut fitur + gejala spesifik.
7. **Langkah reproduksi harus bisa dijalankan ulang.** Bila langkah tidak bisa diulang oleh orang lain, bug report belum selesai — lengkapi dulu.
8. **Validasi human-in-the-loop.** Bug report harus diperiksa manusia (Muse/A60) sebelum jadi draf laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Bug report ini draf internal; pengiriman ke program tetap lewat Muse → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengarang langkah reproduksi, dampak, atau angka. DILARANG memakai bug report untuk menekan atau menipu program. Dokumentasi di sini HANYA fakta terverifikasi.

## Langkah + gerbang

### Gerbang 0 — Tulis judul yang spesifik

1. Judul = fitur + gejala spesifik. BAIK: "Error muncul ketika menambahkan produk ke daftar favorit". BURUK: "Landing page error" (tidak menjelaskan masalahnya: tidak bisa diakses? layout rusak? atau apa). Uji judul: apakah orang yang belum melihat bug-nya bisa menebak fitur + gejalanya dari judul saja? Bila tidak, tulis ulang.
2. **Standar lulus:** judul spesifik + lulus uji tebak. Judul umum = tulis ulang.

### Gerbang 1 — Tulis langkah reproduksi + aktual vs ekspektasi

1. Langkah reproduksi: urutan bernomor dari awal sampai bug muncul, runtut agar mudah diulang (contoh: Buka contohwebsite.com → Search iPhone 11 Pro → Pilih produk → Tekan tombol "add to favorites"). Satu langkah = satu tindakan.
2. Actual result: apa yang benar-benar terjadi (contoh: pesan "Error" muncul, produk tidak masuk daftar favorit). Expected behaviour: apa yang seharusnya terjadi (contoh: pesan "Successfully added to your list" muncul, produk ada di daftar favorit).
3. **Standar lulus:** langkah bernomor lengkap + aktual vs ekspektasi tertulis. Langkah yang tidak bisa diulang = lengkapi dulu.

### Gerbang 2 — Lampirkan bukti + detail lingkungan + dampak

1. Bukti visual: screenshot atau rekaman layar + pesan error/log bila ada. Bukti menghemat waktu penerima dan menghilangkan alasan "tidak bisa direproduksi".
2. Lingkungan: OS (versi), browser/perangkat (versi), versi aplikasi. Dampak: berapa banyak pengguna terpengaruh / berapa kerugian yang ditimbulkan — kuantifikasi bila bisa (angka, bukan "banyak").
3. **Standar lulus:** bukti terlampir + lingkungan lengkap + dampak terkuantifikasi (atau ditulis "tidak dapat dikuantifikasi" dengan alasan).

### Gerbang 3 — Tentukan severity (penemu) vs priority (bersama)

1. Severity — ditentukan PENEMU (yang menemukan + mengetahui bug): Critical (kerusakan parah/sistem tidak berfungsi, flow tidak berjalan, stopper pengetesan), High (dampak serius, bukan stopper), Medium (dampak terbatas, masalah kecil — contoh: download berhasil tapi format file tidak rapi), Low (typo, perbedaan UI, dampak minimal).
2. Priority — ditentukan BERSAMA (penemu + developer + business analyst, dalam konteks bounty: hunter + triager + program) berdasarkan urgensi + dampak ke pengguna/bisnis/fungsionalitas: Critical (segera, kerusakan serius/fungsi kritis terhambat), Major (signifikan, perlu segera tapi tidak mengancam fungsi utama), Medium (signifikan tapi tidak segera mengancam fungsi utama), Low (tidak urgent, tidak ganggu fungsionalitas). Catatan: severity dan priority TIDAK SELALU sama — bug severity High bisa priority Low (dan sebaliknya); tulis keduanya secara terpisah dengan alasan masing-masing.
3. **Standar lulus:** severity + priority tertulis terpisah + alasan masing-masing. Hanya satu dari keduanya = belum lengkap.

### Gerbang 4 — Lacak siklus hidup (Open → Closed, dengan Re-Open)

1. Status bug mengikuti 5 fase: (1) Open/New — QA/hunter menemukan bug; (2) Assigned — developer/program memverifikasi temuan memang bug; (3) Fixing — developer memperbaiki; (4) Re-Test — QA/hunter menguji ulang memastikan perbaikan sesuai; (5) Closed — berhasil diperbaiki + dicek ulang. Bila setelah Re-Test masih tidak sesuai → Re-Open, iterasi kembali dari fase 2.
2. Catat status tiap temuan yang disubmit dan tindak lanjuti: bila program menyatakan sudah diperbaiki, lakukan Re-Test pada akun sendiri (bila diizinkan scope) sebelum menutup.
3. **Standar lulus:** tiap temuan yang disubmit punya status siklus tercatat + tanggal perubahan status. Temuan tanpa status = belum dilacak.

### Gerbang 5 — Serahkan bug report ke draf laporan

1. Serahkan bug report internal (judul + langkah + aktual/ekspektasi + bukti + lingkungan + severity/priority) ke `penulisan-laporan-bounty` sebagai bahan draf laporan program. Skill ini BERHENTI di sini.
2. **Standar lulus:** bug report tercatat di log + diserahkan sebagai bahan draf. Skill ini tidak mengirim laporan ke program.

## Alat

| Alat | Cara pakai |
|---|---|
| Bahan temuan tervalidasi | Masukan bug report — HANYA fakta terverifikasi |
| `penulisan-laporan-bounty` + `laporan-poc-otomatis` | Penerima bug report sebagai bahan draf laporan program |
| `triase-duplikat` + `penilaian-cvss` | Severity/priority diselaraskan dengan triase + skor |
| `~/workspace/catatan/log-bug-bounty.md` | Log bug report: judul, langkah, status siklus, severity/priority |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Judul: [fitur + gejala spesifik]
Langkah reproduksi: [1. ... 2. ... 3. ...]
Actual: [...] | Expected: [...]
Bukti: [screenshot/rekaman/log — ID referensi]
Lingkungan: [OS ... — browser/perangkat ... — versi aplikasi ...]
Dampak: [pengguna terpengaruh: ... — kerugian: ...]
Severity: [Critical/High/Medium/Low — alasan] | Priority: [Critical/Major/Medium/Low — alasan]
Status siklus: [Open/Assigned/Fixing/Re-Test/Closed/Re-Open — tanggal]
Validasi A60: [ya/tidak]
Status: [bug report selesai / diserahkan sebagai bahan draf]
```

## Batasan yang diketahui

- Template QA ini dibuat untuk bug fungsional umum — untuk temuan keamanan, format program (`penulisan-laporan-bounty`) tetap yang utama; template ini melengkapi, bukan mengganti.
- Severity dan priority memakai skala yang berbeda antar sumber (batch 16: Critical/High/Medium/Low; batch 18: low/medium/major/critical). Skill ini memakai KEDUA skala secara eksplisit dan terpisah — jangan mencampuradukkannya dalam satu nilai.
- Status siklus setelah submit bergantung pada respons program — bila program tidak memberi kabar, status tetap di fase terakhir yang diketahui; jangan menebak status.
- Re-Test setelah perbaikan hanya dilakukan bila scope program mengizinkan pengujian ulang. Bila tidak diizinkan, catat "Re-Test tidak dilakukan — di luar scope" dan tutup berdasarkan konfirmasi program saja.
