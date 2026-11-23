# Skill: Respons Insiden & Forensik — Penanganan Bukti dan Analisis Akar Masalah untuk Laporan Bounty

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 8 (artikel Edoxi "12 Hacking Skills", No. 9) + batch 10 (artikel Champlain, Incident Response + Computer Forensics) + batch 11 (artikel Clarusway, DFIR), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill RESPONS INSIDEN + FORENSIK dari sisi hunter: (a) menangani bukti temuan dengan benar (menjaga rantai bukti, menyimpan artefak, mencatat timeline); (b) menganalisis akar masalah dari artefak pengujian SENDIRI (log, respons, rekaman sesi uji); (c) memakai analisis itu untuk memperkuat laporan (dampak + saran perbaikan). Skill ini BUKAN skill forensik terhadap sistem orang lain dan BUKAN skill investigasi insiden di organisasi lain: tidak ada akses ke sistem, log, atau data milik siapa pun di luar akun uji sendiri dan lab sendiri.

## Pemicu

Dipakai setiap kali ada temuan kandidat yang butuh bukti kuat sebelum triase — atau setiap kali artefak pengujian sendiri (log sesi, respons server, rekaman) perlu dianalisis untuk memahami akar masalah celah. Dipakai SETELAH pengujian (`skeptic-false-positive-eliminator`) dan SEBELUM penulisan laporan (`penulisan-laporan-bounty`). Dipakai juga saat triager meminta bukti tambahan atau mempertanyakan akar masalah.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Mengumpulkan + menjaga bukti temuan; menyusun timeline insiden uji |
| Pengerjaan | **A58 Vulnerability Researcher** | Menganalisis akar masalah dari artefak sendiri; merumuskan saran perbaikan |
| Audit | **A60 Security Auditor** | Memvalidasi rantai bukti + analisis akar sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan bukti mana yang cukup untuk maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Validasi temuan (anti false-positive) → skill `skeptic-false-positive-eliminator`. Skill ini MEMAKAI hasil validasi itu — bukan mengulanginya.
- Penulisan laporan bounty → skill `penulisan-laporan-bounty` + `laporan-poc-otomatis`. Skill ini menyiapkan BAHAN bukti + analisis akar untuk laporan — bukan menulis laporannya.
- Analisis malware di lab → skill `analisis-malware-lab`. Skill ini menganalisis artefak PENGUJIAN (log/respons), bukan sampel malware.
- Kebersihan bukti (sensor PII/kredensial) → skill `kebersihan-bukti`. Skill ini memakai aturan sensor itu di semua artefak.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu + lab sendiri.** Artefak yang dianalisis HANYA dari pengujian akun sendiri atau lab sendiri. Tanpa data orang lain.
3. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
4. **Tanpa DoS/DDoS.** Jangan membanjiri target untuk "menghasilkan log".
5. **Tanpa payload di permukaan publik.** Bukti + analisis hanya di log internal dan jalur resmi program.
6. **Rantai bukti dijaga.** Setiap artefak dicatat: kapan diambil, dari pengujian apa, hash-nya bila berupa file. Artefak tanpa asal = tidak bisa dipakai sebagai bukti.
7. **Sensor sebelum simpan.** PII/kredensial/token apa pun yang tanpa sengaja terekam di artefak WAJIB disensor sebelum disimpan di log (lihat `kebersihan-bukti`).
8. **Validasi human-in-the-loop.** Analisis akar masalah harus diperiksa manusia (Muse/A60) sebelum masuk draf laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Analisis forensik ini bahan draf; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengakses sistem, log, atau data milik orang lain atas nama "forensik". DILARANG memakai artefak insiden orang lain. Forensik di sini HANYA atas artefak pengujian sendiri.

## Langkah + gerbang

### Gerbang 0 — Kumpulkan artefak pengujian sendiri

1. Kumpulkan semua artefak dari sesi pengujian yang relevan: langkah reproduksi, respons server, screenshot/rekaman, log sesi, timestamp tiap langkah. Beri tiap artefak ID referensi + hash bila berupa file.
2. **Standar lulus:** daftar artefak tertulis (ID + asal + waktu). Artefak tanpa asal tercatat = buang, jangan dipakai.

### Gerbang 1 — Susun timeline insiden uji

1. Urutkan artefak secara kronologis: apa yang dilakukan, apa respons sistem, kapan tepatnya. Tandai titik di mana perilaku menyimpang dari yang diharapkan (anomali) — lihat `analisis-anomali`.
2. **Standar lulus:** timeline tertulis dengan titik anomali ditandai. Timeline tanpa titik anomali = belum ada bahan analisis akar.

### Gerbang 2 — Analisis akar masalah

1. Untuk tiap anomali di timeline, tanyakan: komponen apa yang seharusnya mencegah ini? Kontrol apa yang gagal atau tidak ada? Apakah ini kesalahan konfigurasi, logika, atau validasi? Bedakan FAKTA (apa yang teramati) dari TEORI (dugaan penyebab) — teori ditulis sebagai "dugaan, perlu bukti tambahan".
2. Rumuskan saran perbaikan yang spesifik (bukan generik): komponen apa yang diubah, validasi apa yang ditambah, kontrol apa yang dipasang.
3. **Standar lulus:** tiap anomali punya analisis akar (fakta vs teori dipisah) + saran perbaikan spesifik. Analisis tanpa saran perbaikan = belum lengkap.

### Gerbang 3 — Validasi rantai bukti + sensor

1. Periksa tiap artefak: apakah masih bisa ditelusur ke pengujian asal? Apakah ada PII/kredensial yang harus disensor? Sensor dulu, lalu serahkan ke A60 untuk validasi.
2. **Standar lulus:** semua artefak tersensor + tervalidasi A60. Artefak belum tervalidasi = belum boleh masuk draf laporan.

### Gerbang 4 — Serahkan bahan ke laporan (bukan dieksekusi di sini)

1. Serahkan paket bahan (timeline + analisis akar + saran perbaikan + artefak tersensor) ke `penulisan-laporan-bounty`. Skill ini BERHENTI di sini.
2. **Standar lulus:** paket bahan tercatat di log + penerima tercatat. Skill ini tidak mencatat "temuan" — hanya "bahan laporan diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Artefak pengujian sendiri (log, respons, rekaman) | Bahan mentah analisis — kumpulkan dengan ID + hash |
| `analisis-anomali` | Menandai titik penyimpangan di timeline |
| `kebersihan-bukti` | Aturan sensor PII/kredensial/token di artefak |
| `skeptic-false-positive-eliminator` | Validasi temuan sebelum analisis forensik dimulai |
| `~/workspace/catatan/log-bug-bounty.md` | Log forensik: artefak, timeline, analisis akar, saran perbaikan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Temuan: [judul kandidat]
Artefak: [ID — asal pengujian — waktu — hash]
Timeline: [waktu — aksi — respons — anomali: ya/tidak]
Analisis akar: [anomali ... — fakta: ... — teori: ... — saran perbaikan: ...]
Sensor: [PII/kredensial disensor: ya/tidak — apa]
Validasi A60: [ya/tidak]
Paket diserahkan ke: [penulisan-laporan-bounty — tanggal]
Yang TIDAK dilakukan: [tanpa akses sistem/log/data orang lain]
Status: [bahan siap / menunggu validasi / diserahkan]
```

## Batasan yang diketahui

- Analisis akar dari luar hanya bisa sampai pada DUGAN yang kuat — penyebab pasti di dalam kode target tidak bisa diketahui tanpa akses ke kode itu. Tulis teori sebagai teori, jangan klaim sebagai fakta internal.
- Timeline bergantung pada ketelitian pencatatan saat pengujian: bila langkah pengujian tidak dicatat waktunya, timeline jadi perkiraan — nyatakan itu dengan jujur.
- Bukti yang lemah (screenshot tanpa konteks, log tanpa timestamp) melemahkan laporan — kumpulkan artefak dengan disiplin sejak awal pengujian, bukan setelahnya.
- Skill ini tidak membahas investigasi insiden di organisasi lain atau respons insiden sebagai penyedia layanan. Bila program meminta bantuan respons insiden di luar bounty, itu di luar skill ini.
