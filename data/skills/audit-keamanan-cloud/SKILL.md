# Skill: Audit Keamanan Cloud — Menilai Postur AWS/Azure/GCP In-Scope (IAM, Storage, Enkripsi, Logging)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 8 (artikel Edoxi "12 Hacking Skills") + batch 10 (artikel Champlain "16 Cybersecurity Skills"), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill AUDIT konfigurasi cloud — menilai postur keamanan aset cloud milik target in-scope (AWS, Azure, GCP) dari informasi yang tersedia secara publik/pasif: kebijakan IAM, keterbukaan storage, enkripsi, dan logging. Skill ini BUKAN skill eksploitasi cloud dan BUKAN skill menyerang infrastruktur cloud orang lain: tidak ada akses dengan kredensial apa pun, tidak ada perubahan konfigurasi, tidak ada pengunduhan data.

## Pemicu

Dipakai saat target in-scope diketahui memakai cloud (AWS/Azure/GCP) dan perlu dinilai apakah konfigurasi cloud-nya punya celah yang terlihat dari luar — sebelum atau sesudah enumerasi aset (`enumerasi-aset-cloud`). Dipakai SETELAH scope cloud target dipastikan in-scope (`recon-pantau-program` + `scope-and-safety-guardian`). Hasilnya: daftar temuan kandidat konfigurasi (mis. storage publik, IAM terlalu longgar, enkripsi mati, logging tidak ada) yang diserahkan ke triase — bukan laporan final.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Mengumpulkan sinyal konfigurasi cloud dari sumber publik/pasif; menyusun daftar temuan kandidat |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai apakah tiap sinyal benar-benar celah (bukan konfigurasi yang disengaja) |
| Audit | **A60 Security Auditor** | Memvalidasi tiap temuan kandidat sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Enumerasi bucket terbuka (S3/GCS/Azure Blob) → skill `enumerasi-aset-cloud`. Skill ini MEMAKAI hasil enumerasi itu sebagai satu dari empat pilar audit — bukan mengulang teknik menebak nama bucket.
- Serangan IAM Entra → skill `serangan-cloud-iam-entra`. Skill ini menilai KEBIJAKAN IAM dari luar (prinsip least privilege yang dilanggar secara terlihat), bukan mengeksekusi serangan IAM.
- SSRF metadata cloud → skill `ssrf-metadata-cloud`. Skill ini tidak membahas SSRF.
- Rekayasa balik arsitektur cloud target → skill `pemetaan-permukaan-serangan` (indeks aset). Skill ini menilai KONFIGURASI tiap aset cloud yang sudah terpetakan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Aset cloud di luar organisasi target / di luar scope = HENTIKAN.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa kredensial apa pun.** Audit hanya dari informasi publik/pasif (header, CNAME, dokumentasi publik, status endpoint anonim). DILARANG memakai kredensial bocor, token, atau kunci apa pun.
4. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih.
5. **Tanpa payload di permukaan publik.** Pengecekan hanya request baca anonim (HEAD/GET status) — tidak mengirim payload eksploitasi.
6. **Tanpa aksi destruktif.** DILARANG menulis, mengubah, atau menghapus konfigurasi, objek, atau data apa pun di cloud orang lain.
7. **DILARANG mengunduh / menyalin / membuka isi data orang lain.** Bila aset cloud terbuka dan berisi data milik orang lain: BERHENTI, jangan baca isinya, laporkan segera ke Muse.
8. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar temuan kandidat bukan laporan.
9. **Patuhi larangan otomasi program** — huntr "Humans only"; Gray Swan dilewati total.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengubah konfigurasi cloud target, menghapus data, atau memakai celah konfigurasi untuk mengakses data orang lain. Audit di sini HANYA membaca sinyal konfigurasi dari luar.

## Langkah + gerbang

### Gerbang 0 — Pastikan scope cloud + catat provider yang dipakai target

1. Baca aturan program: apakah aset cloud dinyatakan in-scope? Catat provider (AWS/Azure/GCP) + layanan yang terlihat dipakai target (dari dokumentasi publik, header, CNAME).
2. **Standar lulus:** status scope cloud tertulis + daftar provider/layanan tertulis. Scope tidak jelas = tanya Muse dulu, jangan mulai.

### Gerbang 1 — Pilar 1: IAM + kontrol akses

1. Periksa sinyal IAM dari luar: apakah ada endpoint/API yang bisa diakses tanpa autentikasi padahal seharusnya butuh login? Apakah ada kebijakan publik yang menunjukkan akses berlebihan (mis. bucket/policy publik, URL bertanda tangan yang bocor di tempat publik)?
2. Nilai dengan prinsip least privilege: akses yang terlihat LEBIH LUAS dari yang dibutuhkan fungsinya = kandidat temuan. Akses yang memang disengaja publik (aset statis situs) = BUKAN temuan.
3. **Standar lulus:** tiap sinyal IAM punya verdict (kandidat / bukan temuan) + alasan. Sinyal tanpa alasan = belum lulus.

### Gerbang 2 — Pilar 2: keterbukaan storage + enkripsi

1. Silangkan hasil `enumerasi-aset-cloud`: bucket/container yang terbuka — apakah isinya aset publik yang disengaja atau data yang seharusnya privat? Periksa juga sinyal enkripsi: apakah endpoint memakai TLS yang valid (lihat `perburuan-tls-dns-email-spoofing`), apakah ada indikasi data sensitif dikirim tanpa enkripsi?
2. **Standar lulus:** tiap aset storage punya klasifikasi (publik-disengaja / terbuka-seharusnya-privat / privat) + status TLS tercatat.

### Gerbang 3 — Pilar 3: logging + visibilitas

1. Nilai dari luar: apakah target punya halaman status/advisory yang menunjukkan mereka memantau insiden? Apakah ada sinyal bahwa logging tidak jalan (mis. tidak ada respons terhadap percobaan akses yang tercatat di log publik)? Catatan: ini penilaian TIDAK LANGSUNG — jangan klaim "logging mati" tanpa bukti; tulis sebagai "tidak ada bukti logging terlihat dari luar".
2. **Standar lulus:** penilaian logging ditulis sebagai observasi dengan tingkat keyakinan (bukti langsung / tidak langsung / tidak ada bukti) — bukan klaim mutlak.

### Gerbang 4 — Pilar 4: compliance + rangkum skor postur

1. Petakan tiap temuan kandidat ke standar yang relevan (mis. GDPR untuk data pribadi, PCI-DSS untuk data pembayaran, HIPAA untuk data kesehatan — lihat `kepatuhan-gdpr-hipaa-pci-dss`): temuan yang menyentuh data yang diatur = bobot lebih tinggi.
2. Susun skor postur sederhana per pilar (kuat / lemah / tidak dapat dinilai) + daftar temuan kandidat terurut. Serahkan ke A60 untuk validasi.
3. **Standar lulus:** skor per pilar tertulis + daftar temuan kandidat terurut + validasi A60. Tanpa validasi = belum boleh jadi draf laporan.

### Gerbang 5 — Serahkan ke triase (bukan dieksekusi di sini)

1. Serahkan temuan kandidat yang lolos A60 ke `triase-duplikat` + `penilaian-cvss`. Skill ini BERHENTI di sini.
2. **Standar lulus:** tiap temuan kandidat tercatat di log + status triase tercatat. Skill ini tidak mencatat "temuan terbayar" — hanya "kandidat diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `enumerasi-aset-cloud` | Hasil enumerasi bucket sebagai masukan Pilar 2 |
| `perburuan-tls-dns-email-spoofing` | Status TLS/sertifikat endpoint target |
| `enumerasi-subdomain` + `probing-http-fingerprint` | Deteksi layanan cloud dari CNAME/header |
| `curl` (HEAD/GET status anonim) | Pengecekan status endpoint, maks 5 req/detik |
| `kepatuhan-gdpr-hipaa-pci-dss` | Pemetaan temuan ke standar yang relevan |
| `~/workspace/catatan/log-bug-bounty.md` | Log audit cloud: scope, sinyal per pilar, skor, temuan kandidat |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Scope cloud: [in-scope: ya/tidak — provider: AWS/Azure/GCP]
Pilar 1 IAM: [sinyal ... — verdict: kandidat/bukan temuan — alasan]
Pilar 2 storage + enkripsi: [aset ... — klasifikasi — TLS: ...]
Pilar 3 logging: [observasi ... — keyakinan: langsung/tidak langsung/tidak ada bukti]
Pilar 4 compliance: [temuan ... → standar ... — bobot]
Skor postur: [IAM: ... | storage: ... | logging: ... | compliance: ...]
Temuan kandidat diserahkan: [daftar terurut — ke triase: ya/tidak]
Yang TIDAK dilakukan: [tanpa kredensial, tanpa ubah konfigurasi, tanpa unduh data orang lain]
Status: [audit selesai / menunggu validasi A60 / diserahkan ke triase]
```

## Batasan yang diketahui

- Audit dari luar hanya melihat PERMUKAAN: konfigurasi internal (kebijakan IAM lengkap, enkripsi at-rest, aturan logging) tidak bisa dinilai pasti dari luar. Tulis verdict sebagai "terlihat dari luar", bukan fakta internal.
- Aset yang memang disengaja publik (gambar/JS/CSS situs, dokumentasi) BUKAN temuan — bedakan dengan teliti sebelum mencatat kandidat.
- Provider cloud memperbarui layanan dan default keamanan secara berkala; yang "terbuka" tahun lalu bisa sudah tertutup hari ini. Verifikasi ulang status tiap putaran, jangan pakai hasil lama.
- Skill ini tidak membahas eksploitasi celah cloud. Bila temuan kandidat butuh pembuktian aktif, pembuktian itu mengikuti skill pengujian yang sesuai dan scope program.
