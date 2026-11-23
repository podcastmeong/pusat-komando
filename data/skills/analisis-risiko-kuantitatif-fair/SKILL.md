# Skill: Analisis Risiko Kuantitatif FAIR — Menilai Nilai Temuan dalam Dolar (Loss Event Frequency × Loss Magnitude)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 17 (artikel Hack The Box "How to launch a bug bounty program", bagian pelaporan kesuksesan + analisis risiko kuantitatif FAIR Institute), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill ANALISIS KUANTITATIF risiko memakai kerangka FAIR (Factor Analysis of Information Risk): menilai nilai temuan dalam dolar dari dua sisi — Loss Event Frequency (seberapa sering peristiwa kerugian bisa terjadi) dan Loss Magnitude (seberapa besar kerugian per peristiwa) — untuk memperkuat argumen dampak di laporan. Skill ini BUKAN penilaian severity teknis (lihat `penilaian-cvss`) dan BUKAN nasihat keuangan: angka yang dihasilkan adalah PERKIRAAN dengan asumsi yang dinyatakan secara terbuka, bukan klaim pasti.

## Pemicu

Dipakai setiap kali temuan kandidat berdampak besar dan perlu argumen nilai-dolar di laporan (mis. temuan yang mengekspos data banyak pengguna, atau yang memungkinkan kerugian finansial langsung). Dipakai SETELAH severity CVSS dihitung (`penilaian-cvss`) dan SEBELUM draf laporan (`penulisan-laporan-bounty`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menghitung frekuensi + magnitudo + nilai risiko dengan asumsi tertulis |
| Audit | **A60 Security Auditor** | Memvalidasi asumsi + perhitungan sebelum masuk draf laporan |
| Pemimpin | **Muse** | Memutuskan angka mana yang boleh dicantumkan di laporan |

## Sudah tercakup (jangan diduplikat)

- Penilaian severity teknis → skill `penilaian-cvss`. Skill ini MENAMBAH nilai dolar di atas skor teknis — bukan menggantinya.
- Manajemen risiko operasi kualitatif → skill `manajemen-risiko-bounty`. Skill ini KUANTITATIF (angka dolar) — bukan skala rendah/sedang/tinggi.
- Argumen dampak di laporan → skill `penulisan-laporan-bounty` (Gerbang 2: buktikan rantai dampak). Skill ini menyediakan ANGKA untuk argumen itu — bukan menulis laporannya.
- Bobot regulasi temuan → skill `kepatuhan-gdpr-hipaa-pci-dss`. Denda regulasi bisa masuk sebagai salah satu komponen Loss Magnitude di sini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Perhitungan memakai data publik + dampak pada akun sendiri sebagai dasar — tanpa data orang lain.
3. **Tanpa data orang lain.** DILARANG memakai data korban atau data hasil breach sebagai dasar perhitungan.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Perhitungan tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Perhitungan + angka hanya di log internal dan jalur resmi program.
7. **Asumsi harus dinyatakan.** Setiap angka WAJIB disertai asumsi + sumbernya. Angka tanpa asumsi = jangan cantumkan di laporan.
8. **Validasi human-in-the-loop.** Setiap perhitungan harus diperiksa manusia (Muse/A60) sebelum masuk draf laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Angka FAIR ini bahan draf; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG membesar-besarkan angka untuk menekan program. DILARANG mengklaim kerugian yang tidak terbukti sebagai fakta. Angka di sini HANYA perkiraan berbasis asumsi terbuka.

## Langkah + gerbang

### Gerbang 0 — Tentukan skenario kerugian (loss event)

1. Tulis skenario kerugian SATU kalimat: bila celah ini dieksploitasi, apa yang terjadi? (mis. "penyerang membaca data N pengguna" / "penyerang mengambil alih akun dan melakukan transaksi"). Tentukan batas skenario: berapa pengguna/akun yang terdampak dalam skenario ini (dari data publik target + bukti pengujian akun sendiri — JANGAN dari data orang lain).
2. **Standar lulus:** skenario tertulis + batas dampak tertulis. Skenario tanpa batas = terlalu kabur, persempit dulu.

### Gerbang 1 — Perkirakan Loss Event Frequency (LEF)

1. Perkirakan seberapa sering peristiwa ini bisa terjadi per tahun: dari Threat Event Frequency (seberapa sering penyerang mencoba — dari tren publik + `intelijen-ancaman-berkala`) × Vulnerability (probabilitas upaya berhasil — dari bukti pengujian sendiri: mudah/sulit dieksploitasi?). Nyatakan sebagai rentang (mis. 0,1–1 kali/tahun), bukan satu angka palsu-presisi.
2. **Standar lulus:** LEF tertulis sebagai rentang + asumsi + sumber. LEF tanpa asumsi = belum lulus.

### Gerbang 2 — Perkirakan Loss Magnitude (LM)

1. Perkirakan kerugian per peristiwa dalam dolar, dari komponen yang relevan: biaya respons insiden, denda regulasi (lihat `kepatuhan-gdpr-hipaa-pci-dss`), kehilangan pelanggan/reputasi, biaya perbaikan. Pakai angka publik bila ada (mis. biaya rata-rata breach $4,4 juta menurut IBM 2025 — sebagai PEMBANDING, bukan sebagai angka temuan ini). Nyatakan sebagai rentang + komponennya.
2. **Standar lulus:** LM tertulis sebagai rentang + komponen + sumber pembanding. LM tanpa komponen = belum lulus.

### Gerbang 3 — Hitung nilai risiko + uji sensitivitas

1. Nilai risiko tahunan = LEF × LM (pakai ujung bawah dan ujung atas rentang → hasil juga rentang). Uji sensitivitas: bila satu asumsi berubah (mis. jumlah pengguna terdampak setengahnya), seberapa besar hasil berubah? Catat asumsi mana yang paling memengaruhi hasil.
2. **Standar lulus:** nilai risiko sebagai rentang + uji sensitivitas + asumsi paling berpengaruh. Nilai tanpa sensitivitas = belum lengkap.

### Gerbang 4 — Serahkan angka ke draf laporan

1. Serahkan rentang nilai + asumsi + sensitivitas ke `penulisan-laporan-bounty` untuk dicantumkan sebagai argumen dampak (dengan bahasa "perkiraan berdasarkan asumsi X"). Skill ini BERHENTI di sini.
2. **Standar lulus:** angka + asumsi tercatat di log + diserahkan sebagai bahan draf. Skill ini tidak mencatat "temuan" — hanya "angka diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `penilaian-cvss` | Skor teknis sebagai dasar sebelum menghitung nilai dolar |
| `intelijen-ancaman-berkala` | Tren ancaman sebagai dasar Threat Event Frequency |
| `kepatuhan-gdpr-hipaa-pci-dss` | Komponen denda regulasi dalam Loss Magnitude |
| Data publik (biaya breach IBM, jumlah pengguna target) | Pembanding + dasar batas dampak — HANYA sumber publik |
| `~/workspace/catatan/log-bug-bounty.md` | Log FAIR: skenario, LEF, LM, nilai risiko, asumsi |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Temuan: [judul kandidat]
Skenario kerugian: [...] | Batas dampak: [...]
LEF: [rentang .../tahun — asumsi: ... — sumber: ...]
LM: [rentang $... — komponen: ... — pembanding: ...]
Nilai risiko tahunan: [rentang $... — sensitivitas: ... — asumsi paling berpengaruh: ...]
Diserahkan ke draf laporan: [ya/tidak]
Yang TIDAK dilakukan: [tanpa membesar-besarkan angka, tanpa data orang lain]
Status: [perhitungan selesai / diserahkan]
```

## Batasan yang diketahui

- FAIR adalah perkiraan, bukan ramalan: LEF dan LM bergantung pada asumsi yang sering tidak bisa diverifikasi penuh dari luar. Selalu sajikan sebagai RENTANG dengan asumsi terbuka — jangan pernah menyajikan satu angka tunggal seolah pasti.
- Biaya breach rata-rata industri (mis. IBM $4,4 juta) adalah PEMBANDING, bukan angka temuan ini — target kecil tidak mengalami kerugian sebesar rata-rata industri. Sesuaikan dengan skala target.
- Program bounty menilai temuan dari dampak TEKNIS yang terbukti, bukan dari angka FAIR — angka ini memperkuat argumen, bukan menggantikan bukti. Bila bukti teknis lemah, angka besar tidak menyelamatkannya.
- Skill ini tidak membahas asuransi siber atau transfer risiko. Bila laporan butuh bahasa asuransi, serahkan ke Muse → Cipta.
