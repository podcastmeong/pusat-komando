# Skill: Prioritas Remediasi — Mengurutkan Perbaikan Temuan berdasarkan Risiko (Severity × Eksploitabilitas × Paparan × Dampak Bisnis)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 24 (halaman layanan CHT Security "Penetration Testing", manfaat: rekomendasi jadwal patching), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill PRIORITAS REMEDIASI — mengurutkan temuan yang sudah tervalidasi berdasarkan risiko agar saran perbaikan di laporan tepat sasaran: severity teknis × kemudahan dieksploitasi × paparan (berapa luas celah bisa dijangkau) × dampak bisnis. Skill ini BUKAN skill memperbaiki sistem orang lain dan BUKAN skill menjadwalkan patch untuk organisasi lain: hasilnya adalah SARAN prioritas di dalam laporan bounty — keputusan perbaikan tetap di tangan pemilik sistem.

## Pemicu

Dipakai setiap kali draf laporan butuh bagian "Saran Perbaikan" yang berprioritas — SETELAH severity dihitung (`penilaian-cvss`) dan SEBELUM draf laporan ditulis (`penulisan-laporan-bounty` / `laporan-poc-otomatis`). Dipakai juga saat satu laporan berisi lebih dari satu temuan dan urutan perbaikannya perlu ditetapkan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menghitung prioritas tiap temuan + menyusun jadwal saran perbaikan |
| Audit | **A60 Security Auditor** | Memvalidasi prioritas (harus cocok dengan bukti, bukan tebakan) |
| Pemimpin | **Muse** | Memutuskan prioritas akhir yang dicantumkan di laporan |

## Sudah tercakup (jangan diduplikat)

- Penilaian severity teknis → skill `penilaian-cvss`. Skill ini MEMAKAI skor itu sebagai satu dari empat faktor — bukan menggantinya.
- Saran perbaikan sebagai bagian laporan → skill `laporan-poc-otomatis` (bagian Saran Perbaikan). Skill ini adalah CARA mengurutkan + menjadwalkan saran itu — bukan format laporannya.
- Klasifikasi jenis bug → skill `klasifikasi-jenis-bug`. Skill ini memakai klasifikasi itu sebagai masukan prioritas — bukan mengulanginya.
- Analisis risiko kuantitatif → skill `analisis-risiko-kuantitatif-fair`. Skill ini memakai nilai dolar BILA ADA sebagai satu faktor dampak — bukan menghitungnya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Prioritas dihitung dari bukti pengujian akun sendiri — tanpa data orang lain.
3. **Tanpa data orang lain.** Tanpa memakai data korban dalam perhitungan prioritas.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Perhitungan prioritas tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Daftar prioritas hanya di log internal dan jalur resmi program.
7. **Prioritas harus cocok dengan bukti.** Jangan menaikkan prioritas temuan tanpa bukti (mis. menaikkan karena "terdengar kritis"). Bila bukti lemah, prioritas turun — tulis alasannya.
8. **Validasi human-in-the-loop.** Setiap prioritas harus diperiksa manusia (Muse/A60) sebelum masuk draf laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Prioritas ini bahan draf; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG membesar-besarkan prioritas untuk menekan program. DILARANG menyarankan perbaikan yang merusak sistem (mis. "matikan layanan"). Saran di sini HANYA perbaikan yang aman dan spesifik.

## Langkah + gerbang

### Gerbang 0 — Kumpulkan empat faktor per temuan

1. Untuk tiap temuan tervalidasi, catat empat faktor: (a) Severity teknis — skor CVSS (`penilaian-cvss`); (b) Eksploitabilitas — seberapa mudah dieksploitasi (dari bukti pengujian: butuh autentikasi? butuh kondisi khusus? bisa otomatis?); (c) Paparan — seberapa luas celah bisa dijangkau (satu endpoint? semua pengguna? internet publik?); (d) Dampak bisnis — apa yang dipertaruhkan (data sensitif? uang? reputasi? — lihat `analisis-risiko-kuantitatif-fair` bila ada angkanya).
2. **Standar lulus:** tiap temuan punya empat faktor tertulis. Faktor tanpa bukti = tulis "tidak diketahui" — jangan ditebak.

### Gerbang 1 — Hitung prioritas (P0–P3)

1. Tentukan prioritas dengan aturan: **P0 (segera, hitungan hari)** — severity kritikal + mudah dieksploitasi + paparan luas; **P1 (minggu ini)** — severity tinggi + salah satu dari mudah/paparan luas; **P2 (bulan ini)** — severity sedang + dampak terbatas; **P3 (backlog)** — severity rendah / dampak minimal. Bila faktor bertentangan, faktor yang PALING KUAT (bukti paling solid) yang menentukan — catat alasannya.
2. **Standar lulus:** tiap temuan punya prioritas P0–P3 + alasan per faktor. Prioritas tanpa alasan = belum dihitung.

### Gerbang 2 — Susun jadwal saran perbaikan

1. Untuk tiap temuan, tulis saran perbaikan yang SPESIFIK (komponen apa yang diubah, validasi/kontrol apa yang ditambah) + jadwal yang disarankan sesuai prioritasnya (P0: segera; P1: minggu ini; P2: bulan ini; P3: backlog). Saran generik ("perbaiki keamanan") DILARANG — harus bisa dikerjakan developer dari kalimat itu.
2. **Standar lulus:** tiap temuan punya saran spesifik + jadwal. Saran generik = tulis ulang.

### Gerbang 3 — Serahkan prioritas ke draf laporan

1. Serahkan daftar prioritas + saran perbaikan ke `penulisan-laporan-bounty` / `laporan-poc-otomatis` sebagai bagian Saran Perbaikan. Skill ini BERHENTI di sini.
2. **Standar lulus:** prioritas + saran tercatat di log + diserahkan sebagai bahan draf. Skill ini tidak mencatat "temuan" — hanya "prioritas diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `penilaian-cvss` | Skor severity sebagai faktor (a) |
| `analisis-risiko-kuantitatif-fair` | Nilai dolar sebagai masukan faktor (d) bila ada |
| `klasifikasi-jenis-bug` | Jenis bug sebagai konteks prioritas |
| `penulisan-laporan-bounty` + `laporan-poc-otomatis` | Penerima prioritas + saran sebagai bagian laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log prioritas: temuan → empat faktor → P0–P3 → saran + jadwal |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Temuan: [judul kandidat]
Faktor: [severity: ... — eksploitabilitas: ... — paparan: ... — dampak bisnis: ...]
Prioritas: [P0/P1/P2/P3 — alasan]
Saran perbaikan: [spesifik: ... — jadwal: ...]
Validasi A60: [ya/tidak]
Diserahkan ke draf laporan: [ya/tidak]
Yang TIDAK dilakukan: [tanpa membesar-besarkan prioritas, tanpa saran generik]
Status: [prioritas selesai / diserahkan]
```

## Batasan yang diketahui

- Prioritas P0–P3 adalah SARAN dari hunter — program/pemilik sistem yang memutuskan jadwal sebenarnya. Jangan menyajikan saran sebagai kewajiban atau tenggat yang mengikat.
- Eksploitabilitas dinilai dari pengujian akun sendiri — penyerang sungguhan bisa punya cara yang tidak terlihat dari pengujian kita. Bila ragu, naikkan SATU tingkat dengan alasan tertulis, jangan dua tingkat.
- Faktor "tidak diketahui" menurunkan keyakinan prioritas — catat keyakinan (tinggi/sedang/rendah) tiap prioritas. Prioritas berkeyakinan rendah harus dinyatakan sebagai "perkiraan awal".
- Skill ini tidak membahas manajemen patch organisasi (jadwal rilis, jendela pemeliharaan, rollback) — itu urusan pemilik sistem. Fokus skill ini: prioritas + saran perbaikan dari sisi hunter.
