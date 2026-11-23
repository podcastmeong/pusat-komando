# Skill: Bypass Pertanyaan Keamanan — Jawaban pertanyaan keamanan (KBA) yang bisa ditebak atau dicari dari sumber publik

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 91. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai pertanyaan keamanan (KBA) pada alur pemulihan akun dan ada dugaan jawabannya bisa ditebak atau ditemukan dari sumber publik — sehingga alur pemulihan bisa dilewati tanpa verifikasi yang benar.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Alur reset kata sandi/ATO → skill `alur-reset-kata-sandi-ato` (alur pemulihan; skill ini khusus pertanyaan keamanan).
- Perburuan bypass autentikasi → skill `perburuan-bypass-autentikasi` (bypass umum; skill ini khusus KBA).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL, ANTH. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Akun uji sendiri; tanpa memulihkan akun orang lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian alur pemulihan diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan alur KBA pada akun sendiri

1. Jalankan alur pemulihan AKUN SENDIRI sampai langkah pertanyaan keamanan; catat pertanyaan apa yang ditanyakan, berapa percobaan yang diizinkan, dan apakah ada kunci (lockout) setelah gagal.
2. **Standar lulus:** alur + pertanyaan + batas percobaan tertulis.

### Gerbang 2 — Uji kekuatan jawaban (hanya akun sendiri)

1. Uji apakah jawaban bisa ditebak dari informasi publik TENTANG AKUN SENDIRI (jawaban yang sengaja dibuat mudah ditebak saat pendaftaran akun uji) atau apakah pertanyaan punya jawaban yang umum.
2. Uji apakah percobaan gagal dibatasi (rate limit/lockout) dengan mencoba jawaban salah pada akun sendiri dalam batas yang wajar.
3. **Standar lulus:** hasil tercatat (jawaban mudah ditebak/tidak + batas percobaan ada/tidak).

### Gerbang 3 — Buktikan pemulihan lewat KBA lemah (akun sendiri)

1. Pulihkan AKUN SENDIRI memakai jawaban yang mudah ditebak/dari sumber publik tentang diri sendiri; catat langkahnya.
2. **Standar lulus:** pemulihan akun sendiri lewat KBA lemah terbukti (atau tidak). Tanpa itu = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Jalankan alur pemulihan akun sendiri |
| Sumber publik tentang diri sendiri | Bahan uji ketertebakan jawaban akun sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-pertanyaan-keamanan] — No. 91
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Alur pemulihan akun uji sendiri bisa dilewati lewat jawaban pertanyaan keamanan yang mudah ditebak atau tersedia di sumber publik.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa memulihkan akun orang lain dalam bentuk apa pun.
- Jangan mencari atau memakai jawaban keamanan milik orang lain; bahan uji hanya informasi publik tentang diri sendiri.
- Jangan melewati batas percobaan secara agresif — patuhi rate limit program.
