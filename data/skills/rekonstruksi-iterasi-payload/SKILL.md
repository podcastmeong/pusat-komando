# Skill: Rekonstruksi & Iterasi Payload — Memetakan Endpoint, Merangkai Skrip Otomasi, dan Memvariasikan Payload secara Sistematis

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 1).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh workflow di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua langkah sampai ada satu kasus nyata yang lolos gerbang QC dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat sudah ada hipotesis celah (dari `kopilot-analisis-kode` atau dari riset manual) pada program web/API klasik dan hipotesis itu harus DIBUKTIKAN dengan pengujian nyata: memetakan endpoint, merangkai skrip otomasi pengujian, dan memvariasikan payload secara terarah dan sistematis. Dipakai untuk program web/API klasik (mis. huntr) — BUKAN untuk payload injeksi Google AI VRP (payload injeksi Google DIBLOKIR, lihat `buru-bug-bounty`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Memetakan endpoint, menulis skrip pengujian, memvariasikan payload, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan varian mana yang dikembangkan jadi rantai (lihat `transfer-hunting`) |

## Sudah tercakup (jangan diduplikat)

- Variasi format prompt/tool-output untuk program AI → skill `buru-bug-bounty` + `transfer-hunting` (skill ini untuk payload pengujian web/API klasik, bukan varian prompt AI).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Prompt injection → skill `buru-bug-bounty`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **huntr = "Humans only".** Challenge huntr TIDAK BOLEH diuji dengan otomasi/skrip agen AI (otomasi = banned). Untuk huntr, skill ini hanya berlaku pada jalur audit kode OSV yang mengizinkan bantuan alat — bila ragu, tanya dulu, jangan jalankan skrip.
11. **Satu payload lolos → transfer dulu.** Ikuti `transfer-hunting`: uji payload yang lolos ke semua program lain sebelum menulis varian baru.
12. **Jangan merusak.** Jangan menghapus, mengubah konfigurasi permanen, atau mengunci akun. Uji dengan langkah minimal.

## Langkah + gerbang

### Gerbang 1 — Petakan endpoint

1. Inventarisasi endpoint dari sumber yang sah: dokumentasi API program, OpenAPI/Swagger bila tersedia, dan pengamatan sebagai pengguna asli (bukan scanning agresif di luar scope).
2. Untuk tiap endpoint catat: metode, parameter, autentikasi yang dibutuhkan, dan data apa yang dikembalikan.
3. **Standar lulus:** daftar endpoint tertulis dengan parameter + otorisasi tiap endpoint. Endpoint tanpa catatan otorisasi = belum dipetakan.

### Gerbang 2 — Tentukan permukaan uji

1. Dari peta endpoint + hipotesis, pilih 1–3 endpoint yang paling mungkin membuktikan dampak. Tulis untuk tiap endpoint: input apa yang dikendalikan penyerang, dan dampak apa yang membuktikan celah (bukan sekadar error).
2. **Standar lulus:** tiap endpoint uji punya pasangan "input penyerang → dampak yang diharapkan". Tanpa dampak yang jelas = jangan uji; itu cuma kebisingan scanner.

### Gerbang 3 — Rangkai skrip otomasi (bila program mengizinkan)

1. Tulis skrip kecil yang mengulang SATU pengujian dasar dengan parameter berbeda (bukan scanner buta). Skrip hanya mengirim permintaan yang sama seperti pengguna asli, dengan nilai parameter yang divariasikan.
2. Simpan skrip + daftar nilai uji di folder kerja; jangan menjalankan skrip yang belum dibaca manusia.
3. **Standar lulus:** skrip dibaca dan disetujui A62/manusia sebelum jalan; skrip berhenti otomatis bila respons menunjukkan kerusakan/error tak terduga. Skrip tanpa batas berhenti = jangan jalankan.

### Gerbang 4 — Variasikan payload secara terarah

1. Variasikan SATU dimensi per putaran (mis. satu parameter, satu encoding, satu urutan langkah). Catat tiap variasi: nilai yang dikirim, respons yang diterima, berhasil/gagal.
2. Bila satu variasi lolos → BERHENTI menambah variasi baru; kembangkan variasi yang lolos itu (lihat `transfer-hunting`) dan dokumentasikan bukti.
3. **Standar lulus:** log variasi lengkap (nilai → respons → verdict) untuk tiap putaran. Variasi tanpa log = tidak terjadi.

### Gerbang 5 — Buktikan dampak, bukan error

1. Temuan hanya BERHASIL bila ada dampak nyata yang cocok dengan kategori berbayar program (baca scope + tier hadiah di `triase-duplikat`): data yang terbaca/diubah, aksi yang terjadi tanpa otorisasi, atau batas yang dilewati — BUKAN sekadar pesan error atau status 500.
2. Simpan bukti: respons persis, tangkapan layar/log, dan langkah reproduksi yang bisa diulang orang lain.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah + dampak tertulis. Tanpa bukti = belum berhasil, jangan maju ke laporan.

### Gerbang 6 — Serahkan ke triase

1. Serahkan bukti ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
2. **Standar lulus:** keputusan triase tercatat di log dengan alasan. Temuan yang gagal triase kembali ke Gerbang 4 dengan catatan kenapa gagal.

## Alat

| Alat | Cara pakai |
|---|---|
| Skrip pengujian buatan sendiri (Python/bash) | Mengulang satu pengujian dasar dengan parameter bervariasi; hanya bila program mengizinkan otomasi. Simpan di folder kerja program, bukan di permukaan publik. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian. |
| LLM/agen AI | Membantu merangkai skrip dan mengusulkan variasi — manusia membaca skrip sebelum menjalankannya. |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua variasi (nilai → respons → verdict) dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Hipotesis: [dari kopilot-analisis-kode / riset]
Variasi yang diuji:
  1. [nilai] → [respons] → [gagal/berhasil]
  2. [nilai] → [respons] → [gagal/berhasil]
Dampak terbukti: [apa yang terjadi + kenapa ini kategori berbayar]
Bukti: [file log/screenshot]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Tanpa fondasi kerentanan (lihat `fondasi-kerentanan-web-api`), variasi payload mudah jadi tebakan acak yang tidak berdampak.
- Skrip otomasi dilarang di sebagian program — selalu cek larangan otomasi program SEBELUM menjalankan skrip apa pun.
