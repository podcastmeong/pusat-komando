# Skill: Membaca Scope dari Sisi Penyelenggara — Memahami Cara Program Berpikir, Jebakan "Beg Bounty", dan Kematangan Program

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 17 (artikel Hack The Box "How to launch a bug bounty program — a security leader's guide"), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill MEMBACA SCOPE dari sisi penyelenggara: memahami mengapa scope program ditulis seperti itu, mengenali jebakan "Beg Bounty" (daftar out-of-scope yang terlalu luas sehingga klaim low-risk terpotong), menilai kematangan program sebelum ikut, dan membedakan pengujian di test instance vs live app. Skill ini BUKAN skill melanggar scope dan BUKAN skill mencari celah aturan: memahami cara penyelenggara berpikir dipakai untuk MEMILIH program yang sehat dan MEMATUHI scope-nya — bukan untuk mengakali.

## Pemicu

Dipakai setiap kali program baru dipertimbangkan untuk diikuti, dan setiap kali scope program berubah — SEBELUM pengujian apa pun dimulai. Dipakai juga saat temuan ditolak sebagai "out-of-scope" dan perlu dipahami apakah penolakan itu wajar atau pola "Beg Bounty".

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Membaca + menganalisis scope program; menilai kematangan program |
| Audit | **A60 Security Auditor** | Memvalidasi penilaian scope + kematangan sebelum jadi keputusan ikut/tidak |
| Pemimpin | **Muse** | Memutuskan program diikuti atau dilewati berdasarkan penilaian ini |

## Sudah tercakup (jangan diduplikat)

- Penegakan scope sebelum eksekusi → skill `scope-and-safety-guardian`. Skill ini MEMBACA dan MENILAI scope sebelum diputuskan ikut — gerbang itu MENEGAKKANNYA saat eksekusi. Berbeda fase.
- Pemantauan program (scope/hadiah/deadline) → skill `recon-pantau-program`. Skill itu MEMANTAU perubahan; skill ini MENAFSIRKAN maksud + jebakan di balik tulisan scope.
- Posisi bounty dalam manajemen risiko penyelenggara → dibahas di skill ini sebagai konteks (bounty hanya SATU kontrol, tidak menggantikan kontrol lain) — bukan sebagai skill terpisah.
- Triase + penolakan temuan → skill `triase-duplikat`. Skill ini menganalisis POLA penolakan (apakah "Beg Bounty"?) — bukan memutuskan satu temuan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Analisis scope adalah pekerjaan membaca dokumen publik program — tidak menyentuh target.
3. **Tanpa data orang lain.** Tanpa memakai data korban atau data pihak ketiga.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Analisis scope tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Analisis scope hanya di log internal.
7. **Memahami scope ≠ mengakali scope.** Bila scope melarang sesuatu, larangan itu DIPATUHI — memahami alasan di baliknya tidak membuat larangan itu boleh dilanggar.
8. **Validasi human-in-the-loop.** Penilaian kematangan + keputusan ikut/tidak harus diperiksa manusia (Muse/A60).
9. **Tanpa laporan tanpa persetujuan Cipta.** Keputusan ikut program baru tetap lewat Muse → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai pemahaman tentang penyelenggara untuk memanipulasi program, menekan triager, atau menguji aset out-of-scope. Pemahaman di sini HANYA untuk memilih program yang sehat dan mematuhi aturannya.

## Langkah + gerbang

### Gerbang 0 — Baca scope secara harfiah + catat strukturnya

1. Baca halaman program: target + URL/lokasi spesifik, kategori (website, API, mobile, IoT), daftar aset out-of-scope, fungsionalitas out-of-scope, jenis kerentanan yang diterima/ditolak, cara submit, cara perusahaan merespons. Catat SEMUANYA secara harfiah — jangan menafsirkan dulu.
2. **Standar lulus:** ringkasan scope harfiah tertulis. Ringkasan yang menafsirkan sebelum mencatat = ulangi.

### Gerbang 1 — Deteksi pola "Beg Bounty"

1. Periksa tanda-tanda program "Beg Bounty" (meminta temuan tapi memangkas pembayaran lewat scope): daftar out-of-scope yang sangat panjang/umum; hampir semua kategori low/medium dinyatakan out-of-scope; hadiah jauh di bawah program sejenis untuk temuan yang sama; respons lambat/tidak jelas; tidak ada kejelasan tentang test instance vs live. Satu tanda = waspada; dua atau lebih = program kemungkinan tidak sehat.
2. **Standar lulus:** tiap tanda punya verdict (ada/tidak ada) + kutipan dari halaman program. Tanda tanpa kutipan = belum terbukti.

### Gerbang 2 — Nilai kematangan program (4 pertanyaan)

1. Nilai 4 pertanyaan kematangan penyelenggara: (1) apakah ada strategi manajemen risiko sebagai dasar keputusan keamanan? (2) apakah ada proses secure development? (3) apakah developer + security engineer cukup terampil dan menjaga skill? (4) apakah metrik keamanan dicatat, dilaporkan, dianalisis? Jawab dari bukti publik (laporan, blog, riwayat program, transparansi). Semua ya → program matang, boleh dipertimbangkan; ada yang tidak → catat kekurangannya sebagai risiko (lihat `manajemen-risiko-bounty`).
2. **Standar lulus:** tiap pertanyaan punya jawaban + bukti publik. Jawaban tanpa bukti = dugaan, tulis sebagai dugaan.

### Gerbang 3 — Bedakan test instance vs live app

1. Tentukan apakah program menyediakan test instance/sandbox atau mengharuskan pengujian di live app. Bila live: syaratnya lebih ketat (jangan ganggu pengguna sah) — catat batasan tambahannya. Bila test instance: catat bahwa temuan di test instance belum tentu melindungi live app (hunter bisa tetap menargetkan live — JANGAN lakukan itu bila live out-of-scope).
2. **Standar lulus:** jenis lingkungan tertulis (test/live) + batasan tambahannya. Tidak jelas = tanya lewat jalur resmi program, jangan menebak.

### Gerbang 4 — Putuskan ikut / lewati + serahkan

1. Gabungkan hasil Gerbang 1–3: program sehat + matang + scope jelas → rekomendasikan IKUT (dengan catatan risiko). Program "Beg Bounty" atau tidak matang → rekomendasikan LEWATI dengan alasan tertulis. Serahkan rekomendasi ke Muse → Cipta untuk keputusan akhir.
2. **Standar lulus:** rekomendasi tertulis (ikut/lewati) + alasan + validasi A60. Rekomendasi tanpa validasi = belum boleh dipakai.

## Alat

| Alat | Cara pakai |
|---|---|
| Halaman aturan program resmi | Sumber utama scope — baca harfiah, kutip saat menilai |
| `recon-pantau-program` | Data program (hadiah, deadline, riwayat perubahan scope) |
| `manajemen-risiko-bounty` | Penerima risiko program yang ditemukan di sini |
| `scope-and-safety-guardian` | Gerbang penegakan scope saat eksekusi (setelah diputuskan ikut) |
| `~/workspace/catatan/log-bug-bounty.md` | Log analisis scope: ringkasan, pola Beg Bounty, kematangan, rekomendasi |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama — URL aturan]
Scope harfiah: [target ... — out-of-scope ... — diterima/ditolak ...]
Beg Bounty: [tanda ... — verdict: ada/tidak — kutipan: ...]
Kematangan: [(1) ... (2) ... (3) ... (4) ... — bukti: ...]
Lingkungan: [test instance / live — batasan tambahan: ...]
Rekomendasi: [IKUT/LEWATI — alasan]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa mengakali scope, tanpa menguji out-of-scope]
Status: [analisis selesai / diserahkan ke Muse]
```

## Batasan yang diketahui

- Kematangan program dinilai dari bukti PUBLIK — program bisa matang secara internal tanpa mempublikasikannya, dan sebaliknya. Tulis penilaian sebagai "berdasarkan bukti publik", bukan vonis mutlak.
- Pola "Beg Bounty" adalah penilaian, bukan fakta hukum: program dengan scope ketat bisa saja sah (mis. memang hanya mencari temuan kritis). Bedakan "scope ketat yang jujur" dari "scope yang memangkas pembayaran" — lihat hadiah + respons program sebagai pembanding.
- Scope program bisa berubah sewaktu-waktu. Analisis ini berlaku untuk tanggal dibaca — periksa ulang sebelum putaran baru bila ada perubahan (lihat `recon-pantau-program`).
- Skill ini tidak membahas cara MENJADI penyelenggara program (membuat program bounty sendiri) — itu di luar perburuan. Bila Cipta meminta itu suatu hari, itu tugas terpisah.
