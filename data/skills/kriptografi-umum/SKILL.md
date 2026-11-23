# Skill: Kriptografi Umum — Menilai Implementasi Enkripsi, Hashing, Tanda Tangan, dan TLS In-Scope

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 8 (artikel Edoxi "12 Hacking Skills", No. 10) + batch 10 (artikel Champlain, Cryptography + Encryption) + batch 12 (artikel Kamsib, Cryptography), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill PENILAIAN kriptografi — kerangka umum untuk menilai implementasi kripto pada target in-scope: algoritma enkripsi (simetris + asimetris), hashing, tanda tangan digital/PKI, manajemen kunci, dan konfigurasi TLS. Skill ini BUKAN skill memecahkan enkripsi yang kuat dan BUKAN skill menyerang kripto di luar scope: tidak ada brute-force terhadap kunci produksi, tidak ada dekripsi data orang lain, tidak ada serangan terhadap implementasi yang sudah terbukti aman.

## Pemicu

Dipakai saat target in-scope memakai kripto yang terlihat dari luar (TLS, token bertanda tangan, hash, enkripsi pesan) dan perlu dinilai apakah implementasinya lemah — atau saat temuan kandidat menyentuh kripto dan perlu dipetakan ke kerangka yang benar. Dipakai SEBELUM memilih skill serangan kripto spesifik (`serangan-kolisi-hash`, `prng-lemah-prediktabel`, `serangan-padding-oracle`). Hasilnya: peta penilaian kripto target + temuan kandidat yang diserahkan ke skill yang sesuai.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai tiap primitif kripto target dari sinyal yang terlihat; memetakan ke skill serangan yang sesuai |
| Audit | **A60 Security Auditor** | Memvalidasi penilaian sebelum jadi hipotesis pengujian (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan hipotesis kripto mana yang diuji |

## Sudah tercakup (jangan diduplikat)

- Collision attack (MD5/SHA-1) → skill `serangan-kolisi-hash`. Skill ini MEMETAKAN ke sana bila hash lama terdeteksi — bukan mengulang tekniknya.
- PRNG lemah → skill `prng-lemah-prediktabel`. Skill ini memetakan ke sana bila seed/pembangkit acak dicurigai lemah.
- Padding oracle → skill `serangan-padding-oracle`. Skill ini memetakan ke sana bila error padding bocor.
- Spoofing TLS/DNS/email → skill `perburuan-tls-dns-email-spoofing`. Skill ini menilai KONFIGURASI TLS (versi, cipher, sertifikat), bukan spoofing-nya.
- Enkripsi sebagai bagian audit cloud → skill `audit-keamanan-cloud` (Pilar 2). Skill ini adalah penilaian kripto MENDALAM, bukan sekadar sinyal.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pengujian kripto hanya terhadap data/token milik akun uji sendiri.
3. **Tanpa data orang lain.** DILARANG mendekripsi, membaca, atau memakai data terenkripsi milik orang lain.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri endpoint kripto target.
6. **Tanpa brute-force kunci produksi.** DILARANG mencoba memecahkan kunci enkripsi/tanda tangan target dengan brute-force — hanya menilai KELEMAHAN IMPLEMENTASI yang terlihat (algoritma usang, konfigurasi lemah, kesalahan pemakaian).
7. **Tanpa payload di permukaan publik.** Temuan kripto hanya di log internal dan jalur resmi program.
8. **Validasi human-in-the-loop.** Setiap penilaian kripto harus diperiksa manusia (Muse/A60) sebelum jadi hipotesis.
9. **Tanpa laporan tanpa persetujuan Cipta.** Temuan kripto ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memalsukan tanda tangan untuk mengakses akun/sistem orang lain. DILARANG memakai kelemahan kripto untuk membaca atau mengubah data orang lain. Penilaian di sini HANYA untuk menemukan dan melaporkan kelemahan implementasi.

## Langkah + gerbang

### Gerbang 0 — Inventarisasi primitif kripto target

1. Catat semua kripto yang terlihat pada target: versi + cipher TLS, algoritma hash yang dipakai (di URL/token), format token bertanda tangan, dan petunjuk manajemen kunci dari dokumentasi publik.
2. **Standar lulus:** inventaris tertulis (primitif + di mana terlihat + sumber). Tanpa inventaris = jangan mulai.

### Gerbang 1 — Nilai algoritma: usang vs aman

1. Untuk tiap primitif, tentukan: apakah algoritmanya masih dianggap aman (mis. SHA-256, AES-GCM, TLS 1.2+ dengan cipher kuat) atau sudah usang/lemah (MD5, SHA-1, DES, RC4, TLS 1.0/1.1, cipher NULL/EXPORT)? Rujuk daftar algoritma usang yang diakui industri — jangan menilai dari opini.
2. **Standar lulus:** tiap primitif punya verdict (aman / usang / tidak dapat dinilai) + referensi. Verdict tanpa referensi = belum lulus.

### Gerbang 2 — Nilai pemakaian: kunci, IV, tanda tangan

1. Periksa sinyal pemakaian yang salah: kunci yang sama dipakai ulang di tempat berbeda? IV/nonce yang berulang atau bisa ditebak? Tanda tangan yang tidak memverifikasi isi dengan benar? Token yang bisa diubah tanpa merusak tanda tangan? Semua pengujian HANYA pada token/data akun sendiri.
2. **Standar lulus:** tiap sinyal pemakaian punya verdict (kandidat / bukan temuan) + bukti dari akun sendiri. Dugaan tanpa bukti = catat sebagai "dugaan, belum terbukti".

### Gerbang 3 — Nilai TLS: versi, cipher, sertifikat

1. Periksa konfigurasi TLS endpoint target: versi minimum, daftar cipher, validitas + rantai sertifikat, HSTS. Catat kelemahan konfigurasi (mis. masih menerima TLS 1.0, cipher lemah, sertifikat kedaluwarsa/self-signed pada layanan produksi).
2. **Standar lulus:** laporan TLS tertulis (versi + cipher + sertifikat + HSTS). Tanpa data TLS = gerbang ini dilewati dengan status "tidak dapat dinilai".

### Gerbang 4 — Petakan ke skill serangan + serahkan hipotesis

1. Untuk tiap temuan kandidat, tentukan skill pengujian yang sesuai: hash usang → `serangan-kolisi-hash`; PRNG lemah → `prng-lemah-prediktabel`; error padding → `serangan-padding-oracle`; kelemahan TLS → `perburuan-tls-dns-email-spoofing`; kelemahan lain → rumuskan hipotesis satu kalimat.
2. Serahkan hipotesis ke A58/A60 untuk validasi, lalu ke skill pengujian. Skill ini BERHENTI di sini.
3. **Standar lulus:** tiap temuan kandidat punya skill tujuan (atau hipotesis tertulis) + validasi A60. Temuan tanpa tujuan = belum bisa dieksekusi.

## Alat

| Alat | Cara pakai |
|---|---|
| `openssl s_client` / pemeriksa TLS | Membaca versi TLS + cipher + sertifikat endpoint (pasif, tanpa login) |
| Token/data akun uji sendiri | Bahan uji pemakaian kripto — HANYA milik sendiri |
| `serangan-kolisi-hash`, `prng-lemah-prediktabel`, `serangan-padding-oracle` | Skill serangan kripto spesifik (tujuan pemetaan) |
| `perburuan-tls-dns-email-spoofing` | Lanjutan untuk kelemahan TLS |
| `~/workspace/catatan/log-bug-bounty.md` | Log penilaian kripto: inventaris, verdict, hipotesis |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Inventaris kripto: [primitif ... — lokasi terlihat — sumber]
Gerbang 1 algoritma: [primitif ... — verdict: aman/usang/tidak dapat dinilai — referensi]
Gerbang 2 pemakaian: [sinyal ... — verdict: kandidat/bukan temuan — bukti akun sendiri]
Gerbang 3 TLS: [versi ... — cipher ... — sertifikat ... — HSTS: ...]
Pemetaan: [temuan ... → skill ... | hipotesis: ...]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa brute-force kunci, tanpa dekripsi data orang lain]
Status: [penilaian selesai / hipotesis diserahkan]
```

## Batasan yang diketahui

- Penilaian dari luar tidak bisa melihat kunci dan implementasi internal: verdict "aman" dari luar bukan jaminan internal aman, dan "usang" harus dikonfirmasi dengan bukti perilaku (bukan sekadar nama algoritma di dokumentasi).
- Algoritma yang "usang" secara umum bisa saja masih dipakai secara aman dalam konteks tertentu (mis. MD5 untuk checksum non-keamanan) — nilai KONTEKS pemakaian, bukan sekadar nama.
- Standar kripto berubah: algoritma yang aman hari ini bisa dinyatakan lemah besok. Rujuk sumber standar terbaru tiap putaran, jangan pakai daftar usang dari ingatan.
- Skill ini tidak membahas kriptografi kuantum atau serangan kripto tingkat lanjut di luar tiga skill serangan yang dirujuk. Bila temuan membutuhkan analisis kripto mendalam, serahkan ke A58 + Muse sebelum melangkah.
