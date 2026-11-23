# Skill: Kontrol & Framework Keamanan — NIST CSF, ISO 27001, CIS Controls, SOC 2 sebagai Lensa Penilaian

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 14 (artikel Coursera "15 Essential Skills", No. 2 Controls and frameworks), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill KERANGKA KONTROL — memakai framework keamanan (NIST CSF 2.0, ISO 27001, CIS Controls, SOC 2) sebagai lensa untuk menilai postur target in-scope dan memetakan temuan ke kontrol yang gagal. Skill ini BUKAN skill audit compliance organisasi dan BUKAN nasihat sertifikasi: tidak ada klaim "target tidak patuh ISO" tanpa bukti — hanya pemetaan temuan ke kontrol yang relevan.

## Pemicu

Dipakai setiap kali temuan kandidat perlu dipetakan ke kontrol yang gagal (untuk memperkuat argumen dampak di laporan), dan secara berkala untuk menilai postur target dari kontrol yang terlihat dari luar. Dipakai SETELAH temuan tervalidasi (`skeptic-false-positive-eliminator`) dan SEBELUM triase (`triase-duplikat`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Memetakan temuan ke kontrol framework; menyusun penilaian postur |
| Audit | **A60 Security Auditor** | Memvalidasi pemetaan kontrol (kontrol yang dipilih harus cocok dengan bukti) |
| Pemimpin | **Muse** | Memutuskan pemetaan mana yang masuk laporan |

## Sudah tercakup (jangan diduplikat)

- Pemetaan temuan ke ATT&CK + NIST CSF + D3FEND → skill `skill-cybersecurity-anthropic` (Gerbang 1) dan `mitre-attack`. Skill ini menambahkan ISO 27001 + CIS Controls + SOC 2 yang TIDAK dibahas di sana, dan fokus pada KONTROL (bukan taktik serangan).
- Penilaian postur cloud → skill `audit-keamanan-cloud`. Skill ini memakai hasil audit itu sebagai masukan pemetaan kontrol — bukan mengulanginya.
- Kepatuhan data (GDPR/HIPAA/PCI-DSS) → skill `kepatuhan-gdpr-hipaa-pci-dss`. Skill ini membahas KONTROL framework, bukan regulasi data.
- Penilaian severity → skill `penilaian-cvss`. Skill ini memetakan KONTROL yang gagal, bukan skor.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pemetaan kontrol adalah pekerjaan klasifikasi di atas kertas — tidak mengubah apa pun pada target.
3. **Tanpa data orang lain.** Tanpa memakai data korban atau data pihak ketiga dalam pemetaan.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Pemetaan tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Pemetaan kontrol + penilaian postur hanya di log internal dan jalur resmi program.
7. **Pemetaan harus cocok dengan bukti.** Jangan mengklaim target "melanggar ISO 27001" tanpa bukti — tulis "kontrol X (ISO 27001 A.x.x) tidak terlihat bekerja pada temuan ini" dengan bukti yang ada.
8. **Validasi human-in-the-loop.** Setiap pemetaan kontrol harus diperiksa manusia (Muse/A60) sebelum masuk laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Pemetaan ini bahan draf; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai pemetaan framework untuk merencanakan serangan di luar scope bounty. Pemetaan di sini HANYA untuk klasifikasi temuan dan penilaian postur yang sah.

## Langkah + gerbang

### Gerbang 0 — Pilih framework yang relevan dengan temuan

1. Untuk tiap temuan kandidat, tentukan framework yang paling relevan: NIST CSF 2.0 (fungsi Govern/Identify/Protect/Detect/Respond/Recover), ISO 27001 (kontrol Annex A), CIS Controls (safeguard), atau SOC 2 (kriteria Trust Services). Satu temuan bisa dipetakan ke lebih dari satu framework — catat semuanya.
2. **Standar lulus:** tiap temuan punya framework yang dituju + alasan. Framework tanpa alasan = belum dipilih dengan benar.

### Gerbang 1 — Petakan temuan ke kontrol yang gagal

1. Untuk tiap temuan, tentukan kontrol spesifik yang gagal atau tidak ada: mis. NIST CSF PR.AC (manajemen akses), ISO 27001 A.9 (kontrol akses), CIS Control 3 (perlindungan data) / 5 (manajemen akun), SOC 2 CC6 (kontrol akses logis). Cantumkan ID kontrol + nama + bukti temuan yang menunjukkan kegagalannya.
2. **Standar lulus:** tiap temuan punya kontrol + ID + bukti — atau status "tidak terpetakan" dengan alasan. Pemetaan tanpa bukti = belum lulus.

### Gerbang 2 — Nilai postur dari kontrol yang terlihat

1. Dari semua pemetaan putaran ini, susun penilaian postur sederhana: kontrol mana yang berulang kali gagal (pola) vs kontrol yang terlihat bekerja. Pola kegagalan berulang = argumen dampak yang kuat untuk laporan.
2. **Standar lulus:** penilaian postur tertulis (pola kegagalan + kontrol yang bekerja). Tanpa pola = belum ada penilaian postur.

### Gerbang 3 — Serahkan pemetaan ke triase

1. Serahkan pemetaan kontrol sebagai bagian dari paket triase (`triase-duplikat`). Skill ini BERHENTI di sini.
2. **Standar lulus:** pemetaan tercatat di log + masuk paket triase. Skill ini tidak mencatat "temuan" — hanya "pemetaan diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Referensi NIST CSF 2.0 (6 fungsi) | Kerangka fungsi Govern/Identify/Protect/Detect/Respond/Recover |
| Referensi ISO 27001 Annex A | Daftar kontrol (A.5–A.8) untuk pemetaan |
| Referensi CIS Controls v8 | Daftar safeguard (IG1–IG3) untuk pemetaan |
| Referensi SOC 2 Trust Services Criteria | Kriteria CC (keamanan, ketersediaan, integritas, kerahasiaan, privasi) |
| `mitre-attack` + `skill-cybersecurity-anthropic` | Pemetaan taktik serangan sebagai pelengkap pemetaan kontrol |
| `~/workspace/catatan/log-bug-bounty.md` | Log pemetaan: temuan → framework → kontrol, penilaian postur |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Pemetaan kontrol: [temuan ... — framework ... — kontrol ... (ID ...) — bukti: ...]
Penilaian postur: [pola kegagalan: ... — kontrol yang bekerja: ...]
Diserahkan ke triase: [ya/tidak]
Yang TIDAK dilakukan: [tanpa klaim ketidakpatuhan tanpa bukti, tanpa pengujian di skill ini]
Status: [pemetaan selesai / diserahkan]
```

## Batasan yang diketahui

- Pemetaan kontrol dari luar bersifat indikatif: kontrol yang "tidak terlihat bekerja" bisa saja ada tetapi tidak terlihat dari luar. Tulis pemetaan sebagai "kontrol tidak terlihat bekerja pada temuan ini", bukan "target tidak punya kontrol itu".
- Framework punya versi yang berubah (NIST CSF 2.0, CIS v8, ISO 27001:2022). Catat versi yang dipakai tiap putaran; pemetaan putaran lama bisa basi.
- SOC 2 adalah laporan audit, bukan standar kontrol yang bisa dinilai dari luar — pemetaan SOC 2 hanya sebagai bahasa (kriteria CC), bukan sebagai vonis audit.
- Skill ini tidak membahas audit compliance formal atau persiapan sertifikasi. Bila laporan butuh pernyataan compliance formal, serahkan ke Muse → Cipta — jangan mengarangnya.
