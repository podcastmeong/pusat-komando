# Skill: Kepatuhan GDPR, HIPAA, PCI-DSS — Perlindungan Data dalam Pengujian Bounty

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 8 (artikel Edoxi "12 Hacking Skills", No. 11) + batch 14 (artikel Coursera, Regulatory guidelines), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill KEPATUHAN data dalam pengujian bounty: memahami kewajiban perlindungan data yang berlaku saat menguji (GDPR untuk data pribadi, HIPAA untuk data kesehatan, PCI-DSS untuk data pembayaran) dan memastikan pengujian + bukti + laporan TIDAK melanggar kewajiban itu. Skill ini BUKAN nasihat hukum dan BUKAN skill audit compliance organisasi: bila ada keraguan hukum, serahkan ke Muse → Cipta.

## Pemicu

Dipakai setiap kali pengujian menyentuh data yang diatur (data pribadi, data kesehatan, data pembayaran) atau setiap kali temuan kandidat melibatkan data semacam itu — SEBELUM pengujian dilanjutkan dan SEBELUM bukti disimpan. Dipakai juga saat memetakan bobot temuan: temuan yang menyentuh data yang diatur bernilai lebih tinggi bagi program.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A60 Security Auditor** | Menentukan klasifikasi data yang terlibat + aturan perlindungan yang berlaku |
| Pengerjaan | **A58 Vulnerability Researcher** | Menyesuaikan rencana pengujian agar tidak menyentuh data yang diatur di luar akun sendiri |
| Pemimpin | **Muse** | Memutuskan apakah pengujian boleh lanjut, dibatasi, atau dihentikan |

## Sudah tercakup (jangan diduplikat)

- Etika + kerahasiaan data temuan → skill `etika-kerahasiaan-data-bounty`. Skill ini MENAMBAH lensa regulasi (GDPR/HIPAA/PCI-DSS) di atas etika itu — bukan mengulanginya.
- Izin tertulis + batas legal → skill `izin-tertulis-batas-legal`. Skill ini membahas DATA yang diatur, bukan izin pengujian.
- Kebersihan bukti (sensor PII/kredensial) → skill `kebersihan-bukti`. Skill ini menentukan APA yang harus disensor berdasarkan klasifikasi regulasi.
- Penilaian dampak temuan → skill `penilaian-cvss` + `triase-duplikat`. Skill ini memberi BOBOT regulasi pada dampak — bukan mengganti skornya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pengujian HANYA menyentuh data milik akun uji sendiri. Data pribadi/kesehatan/pembayaran orang lain TIDAK BOLEH disentuh dalam bentuk apa pun.
3. **Tanpa data orang lain.** DILARANG membaca, mengunduh, menyimpan, atau memakai data pribadi, rekam medis, atau data kartu pembayaran milik siapa pun.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri target.
6. **Tanpa payload di permukaan publik.** Bukti yang menyentuh data yang diatur HANYA di log internal tersensor + jalur resmi program.
7. **Sensor total untuk data yang diatur.** Bila bukti tanpa sengaja merekam data pribadi/kesehatan/pembayaran: sensor SEBELUM disimpan; bila tidak bisa disensor dengan aman, HAPUS artefak itu dan catat penghapusannya.
8. **Validasi human-in-the-loop.** Setiap keputusan yang menyentuh data yang diatur harus diperiksa manusia (Muse/A60).
9. **Tanpa laporan tanpa persetujuan Cipta.** Laporan yang menyentuh data yang diatur ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengakses, menyalin, atau menyebarkan data pribadi, rekam medis, atau data pembayaran orang lain atas nama pengujian. DILARANG memakai data hasil breach untuk apa pun. Pelanggaran aturan ini = hentikan pengujian segera dan laporkan ke Muse.

## Langkah + gerbang

### Gerbang 0 — Klasifikasikan data yang mungkin terlibat

1. Sebelum pengujian, tentukan: apakah target memproses data pribadi (GDPR), data kesehatan (HIPAA), atau data pembayaran (PCI-DSS)? Catat klasifikasi + dasarnya (dokumentasi publik target, jenis layanan).
2. **Standar lulus:** klasifikasi data tertulis. Tidak tahu klasifikasinya = anggap data itu DIATUR (paling ketat) sampai terbukti sebaliknya.

### Gerbang 1 — Batasi pengujian pada data sendiri

1. Rancang pengujian agar HANYA menyentuh data akun uji sendiri: buat data uji sendiri (nama palsu, kartu uji, rekam uji), jangan pernah memakai data nyata orang lain sebagai masukan uji.
2. **Standar lulus:** rencana pengujian tertulis dengan data uji yang dipakai (semua milik sendiri). Rencana yang butuh data orang lain = DITOLAK, rancang ulang.

### Gerbang 2 — Nilai bobot regulasi temuan kandidat

1. Untuk tiap temuan kandidat, tentukan: apakah temuan itu mengekspos/mengancam data yang diatur? Bila ya, naikkan bobotnya dalam triase dan catat regulasi yang relevan (GDPR / HIPAA / PCI-DSS) + pasal/klausul umum yang dilanggar (tanpa mengklaim sebagai nasihat hukum).
2. **Standar lulus:** tiap temuan kandidat punya bobot regulasi (tidak ada / GDPR / HIPAA / PCI-DSS) + alasan. Temuan tanpa bobot = belum lengkap.

### Gerbang 3 — Sensor + simpan bukti sesuai aturan

1. Terapkan `kebersihan-bukti` dengan standar klasifikasi Gerbang 0: data yang diatur disensor TOTAL (bukan sebagian). Simpan hanya bukti yang sudah tersensor.
2. **Standar lulus:** semua bukti tersensor + tercatat apa yang disensor. Bukti belum tersensor = jangan disimpan, jangan dilampirkan.

### Gerbang 4 — Serahkan ke triase dengan label regulasi

1. Serahkan temuan kandidat + label regulasi ke `triase-duplikat` + `penilaian-cvss`. Skill ini BERHENTI di sini.
2. **Standar lulus:** temuan tercatat di log + label regulasi tercatat. Skill ini tidak mencatat "temuan terbayar" — hanya "temuan + label diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `etika-kerahasiaan-data-bounty` | Aturan etika + kerahasiaan data temuan (dasar skill ini) |
| `kebersihan-bukti` | Aturan sensor bukti sebelum disimpan |
| `izin-tertulis-batas-legal` | Batas legal pengujian (izin + scope) |
| `penilaian-cvss` + `triase-duplikat` | Penerima temuan + label regulasi |
| `~/workspace/catatan/log-bug-bounty.md` | Log kepatuhan: klasifikasi data, bobot regulasi, sensor |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Klasifikasi data: [pribadi/GDPR — kesehatan/HIPAA — pembayaran/PCI-DSS — tidak ada]
Data uji dipakai: [semua milik sendiri: ya/tidak — daftar]
Temuan kandidat: [temuan ... — bobot regulasi: ... — alasan]
Sensor: [disensor total: ya/tidak — apa yang disensor]
Diserahkan ke triase: [ya/tidak — label regulasi]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa akses rekam/kartu siapa pun]
Status: [kepatuhan diperiksa / diserahkan]
```

## Batasan yang diketahui

- Skill ini BUKAN nasihat hukum: GDPR/HIPAA/PCI-DSS adalah kerangka yang kompleks dan berbeda penerapannya per yurisdiksi. Bila ada keraguan hukum yang nyata, hentikan dan serahkan ke Muse → Cipta — jangan menebak.
- Klasifikasi data dari luar bisa salah: target mungkin memproses data yang diatur tanpa menyatakannya secara publik. Prinsipnya: bila ragu, perlakukan sebagai data yang diatur.
- Regulasi berubah dan berbeda per negara (mis. hukum privasi tiap negara bagian AS berbeda-beda). Catat yurisdiksi yang relevan bila diketahui; jangan menggeneralisasi satu aturan ke semua negara.
- Skill ini tidak membahas kepatuhan organisasi secara umum (audit ISO/SOC 2) — lihat `kontrol-framework-keamanan` untuk kerangka kontrol. Skill ini fokus pada PERLINDUNGAN DATA SELAMA PENGUJIAN.
