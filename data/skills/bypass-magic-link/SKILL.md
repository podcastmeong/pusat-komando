# Skill: Bypass Magic Link — Token login via email yang bisa ditebak, dipakai ulang, atau tanpa kedaluwarsa

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 90. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai magic link (tautan login via email) dan ada dugaan tokennya bisa ditebak, dipakai ulang setelah dipakai, atau tidak kedaluwarsa.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Alur reset kata sandi/ATO → skill `alur-reset-kata-sandi-ato` (alur pemulihan; skill ini khusus magic link).
- Perburuan bypass autentikasi → skill `perburuan-bypass-autentikasi` (bypass umum; skill ini khusus magic link).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL, ANTH, MUSE. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Akun uji sendiri; tanpa memakai token milik orang lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian autentikasi diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan alur magic link

1. Minta magic link ke AKUN SENDIRI; catat format token, panjang, masa berlaku yang dinyatakan, dan apakah tautan sekali pakai.
2. **Standar lulus:** format token + aturan kedaluwarsa/pemakaian tertulis.

### Gerbang 2 — Uji pemakaian ulang dan kedaluwarsa

1. Pakai magic link milik sendiri dua kali (setelah berhasil dipakai sekali); amati apakah pemakaian kedua masih diterima.
2. Uji tautan lama milik sendiri setelah masa berlaku yang dinyatakan; amati apakah masih diterima.
3. **Standar lulus:** hasil tiap varian tercatat (diterima/ditolak). Sekali pakai + kedaluwarsa ditegakkan = AMAN.

### Gerbang 3 — Uji ketertebakan (hanya pola, tanpa menyerang akun lain)

1. Analisis pola token dari BEBERAPA magic link milik sendiri (apakah berurutan, pendek, atau memakai nilai yang bisa ditebak); JANGAN menebak token akun orang lain.
2. **Standar lulus:** analisis pola tercatat. Pola acak yang kuat = tidak terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (pemakaian ulang/kedaluwarsa/pola pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Email milik sendiri | Terima magic link akun sendiri |
| Browser milik sendiri | Buka tautan dan amati hasil autentikasi |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-magic-link] — No. 90
Program: [HUNTR, PPLX, MISTRAL, ANTH, MUSE]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Magic link milik akun uji sendiri bisa dipakai ulang setelah dipakai, atau masih diterima setelah kedaluwarsa, atau tokennya berpola sehingga bisa ditebak.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa memakai token milik orang lain dalam bentuk apa pun.
- Jangan menebak atau mencoba token akun orang lain, walau polanya tampak lemah.
- Jangan membagikan magic link milik sendiri ke siapa pun selama pengujian.
