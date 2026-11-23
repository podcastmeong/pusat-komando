# Skill: Kopilot Analisis Kode — AI sebagai Kopilot untuk Analisis Kode & Logika Kompleks

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 1).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh workflow di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua langkah sampai ada satu kasus nyata yang lolos gerbang QC dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target punya source code yang bisa dibaca (repo open-source, kode aplikasi hasil vibe coding, kode yang diunggah ke ruang kerja, atau potongan kode dari program bounty) dan analisis manual terlalu lambat karena logikanya rumit — terutama alur autentikasi, otorisasi, dan logika bisnis. Dipakai SEBELUM menulis payload apa pun: tugas skill ini adalah menemukan HIPOTESIS celah, bukan membuktikan celahnya (pembuktian memakai skill `rekonstruksi-iterasi-payload`, `triase-duplikat`, dan `laporan-abstrak`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mengarahkan kopilot AI membaca kode, merumuskan hipotesis celah, mencatatnya |
| Audit | **A60 Security Auditor** | Memvalidasi hipotesis sebelum jadi target pengujian (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan hipotesis mana yang dilanjutkan ke pengujian |

## Sudah tercakup (jangan diduplikat)

- Checklist review kode langkah-demi-langkah → skill `skill-trail-of-bits` (bukan skill ini). Skill ini soal **WORKFLOW mengarahkan kopilot AI**, bukan checklist-nya.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Prompt injection → skill `buru-bug-bounty`.
- Pemakaian skill/agen keamanan siap pakai (Agentic-Bug-Hunter, 43 skill) → skill `mesin-agentic-bug-hunter` (dibuat tim lain).

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
10. **Kode yang dianalisis harus legal dibaca** — repo publik, kode milik sendiri, atau kode yang program bounty izinkan untuk diaudit. Jangan membaca kode hasil curian/bocoran.
11. **AI tidak memutuskan.** Kopilot boleh mengusulkan hipotesis; A58 + A60 yang memutuskan hipotesis mana yang diuji. Hipotesis AI tanpa validasi manusia = belum ada apa-apa.

## Langkah + gerbang

### Gerbang 0 — Tentukan pertanyaan, bukan "cari bug"

1. Tulis SATU pertanyaan sempit sebelum membuka kode, mis. "Di mana token sesi dibuat dan apa yang terjadi bila dua sesi bersamaan?" atau "Fungsi apa yang memutuskan apakah pengguna boleh membaca dokumen orang lain?"
2. **Standar lulus:** pertanyaan tertulis, satu kalimat, menyebut fungsi/alur yang dicari. Tanpa pertanyaan = jangan mulai; "cari bug apa saja" selalu menghasilkan temuan generik yang ditolak triage.

### Gerbang 1 — Petakan dulu, baca kemudian

1. Minta kopilot membuat peta: daftar file/fungsi yang relevan dengan pertanyaan, alur data (input → proses → output), dan titik kepercayaan (trust boundary: mana data dari pengguna, mana dari sistem).
2. **Standar lulus:** peta berisi ≤10 file/fungsi inti + alur data tertulis. Bila peta menyebut >20 file, pertanyaan terlalu luas — persempit dan ulangi Gerbang 0.

### Gerbang 2 — Chunking kode

1. Bagi kode jadi potongan kecil (satu fungsi / satu alur per potongan). Jangan menempel seluruh repo sekaligus — konteks besar membuat kopilot mengarang.
2. Untuk tiap potongan, tanyakan hal yang sama: "Apa asumsi keamanan di sini? Apa yang terjadi bila input ini jahat/kosong/ganda?"
3. **Standar lulus:** tiap potongan punya catatan asumsi + skenario input jahat. Potongan tanpa catatan = belum dianalisis.

### Gerbang 3 — Telusur alur autentikasi & otorisasi

1. Telusuri ujung-ke-ujung: login → token/sesi dibuat → token dicek di tiap endpoint → hak akses diputuskan di mana.
2. Tandai titik rawan yang umum: cek otorisasi hanya di frontend, ID yang bisa ditebak/diubah, token yang tidak kedaluwarsa, peran yang dicek sekali lalu dipercaya selamanya.
3. **Standar lulus:** ada diagram alur tertulis (minimal daftar langkah bernomor) + daftar titik rawan dengan lokasi file/baris. Tanpa lokasi persis, hipotesis tidak bisa diuji.

### Gerbang 4 — Tanya jawab iteratif (bukan sekali tanya)

1. Untuk tiap titik rawan, ajukan pertanyaan lanjutan ke kopilot: "Buktikan dengan kutip kode baris X–Y", "Apa yang terjadi bila langkah ini dilewati?", "Apakah ada jalur lain yang sampai ke fungsi yang sama tanpa melewati cek ini?"
2. Tolak jawaban yang tidak mengutip kode. Minta kopilot membedakan "ada di kode" vs "saya duga".
3. **Standar lulus:** tiap hipotesis didukung kutipan kode (file + baris) dan skenario input konkret. Hipotesis tanpa kutipan = dugaan, buang.

### Gerbang 5 — Rumuskan hipotesis teruji

1. Tulis hipotesis dalam format: "Saya menduga [fungsi X di file Y] bisa [dampak Z] karena [alasan dari kode], diuji dengan [langkah konkret]."
2. Serahkan ke A60 untuk validasi. Hipotesis yang lolos A60 baru diteruskan ke `rekonstruksi-iterasi-payload` untuk pengujian.
3. **Standar lulus:** hipotesis punya lokasi kode, dampak, dan langkah uji. Hipotesis yang hanya berbunyi "mungkin rentan" = GAGAL, tulis ulang.

## Alat

| Alat | Cara pakai |
|---|---|
| LLM/agen AI apa pun yang tersedia (ChatGPT, DeepSeek, Gemini, Claude, Copilot) | Kopilot pembaca kode — beri potongan kode + pertanyaan sempit, minta kutipan baris. Jangan percaya jawaban tanpa kutipan. |
| Repo/kode target (publik atau milik sendiri) | Sumber yang dibaca; catat file + baris tiap temuan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua hipotesis + hasil validasi A60. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Hipotesis: [satu kalimat: fungsi + dampak + alasan]
Lokasi kode: [file:baris]
Kutipan pendukung: [potongan kode relevan]
Langkah uji yang diusulkan: [1. ... 2. ...]
Validasi A60: [lolos / ditolak + alasan]
Status: [hipotesis / diuji / temuan / ditolak]
```

Hipotesis TIDAK dikirim sebagai laporan. Yang dikirim hanya temuan yang sudah terbukti lewat pengujian + audit A60 + persetujuan Cipta (lihat `laporan-abstrak`).

## Batasan yang diketahui

- Kopilot AI mudah mengarang celah yang tidak ada di kode (halusinasi) — karena itu Gerbang 4 mewajibkan kutipan baris.
- Skill ini tidak menggantikan pemahaman dasar kerentanan — tanpa fondasi (lihat `fondasi-kerentanan-web-api`), hipotesis kopilot tidak bisa dinilai benar/salah.
