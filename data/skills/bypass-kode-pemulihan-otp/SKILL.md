# Skill: Bypass Kode Pemulihan OTP — Kode cadangan/backup 2FA yang lemah, tidak kedaluwarsa, atau bisa di-brute-force

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 92. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai kode pemulihan/cadangan 2FA dan ada dugaan kodenya lemah (pendek, berpola), tidak kedaluwarsa, tidak sekali pakai, atau bisa ditebak berulang tanpa batas.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis bypass 2FA → skill `analisis-bypass-2fa` (bypass 2FA umum; skill ini khusus kode pemulihan/backup).
- Perburuan brute-force/rate-limit → skill `perburuan-brute-force-rate-limit` (batas percobaan; skill ini targetnya kode pemulihan).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa melewati 2FA pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian autentikasi/2FA diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan kode pemulihan akun sendiri

1. Buat/lihat kode pemulihan AKUN SENDIRI; catat format (panjang, karakter), jumlah kode, dan aturan yang dinyatakan (sekali pakai, kedaluwarsa).
2. **Standar lulus:** format + aturan tertulis.

### Gerbang 2 — Uji sekali pakai dan kedaluwarsa

1. Pakai satu kode pemulihan milik sendiri, lalu coba pakai kode yang SAMA sekali lagi; amati apakah diterima kedua kalinya.
2. **Standar lulus:** hasil tercatat (sekali pakai ditegakkan/tidak). Sekali pakai ditegakkan = AMAN untuk varian ini.

### Gerbang 3 — Uji batas percobaan (dalam batas wajar)

1. Coba beberapa kode salah pada akun sendiri dan amati apakah ada rate limit/lockout; hentikan jauh sebelum batas yang bisa mengunci akun.
2. Analisis pola kode milik sendiri (apakah berpola/pendek); JANGAN menebak kode orang lain.
3. **Standar lulus:** ada/tidaknya rate limit tercatat + analisis pola kode sendiri.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (pemakaian ulang/batas/kode lemah pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Jalankan alur kode pemulihan akun sendiri |
| Authenticator milik sendiri | Kelola 2FA akun sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-kode-pemulihan-otp] — No. 92
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Kode pemulihan milik akun uji sendiri bisa dipakai lebih dari sekali, atau tidak ada batas percobaan yang berarti, atau polanya lemah.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa melewati 2FA pengguna lain dalam bentuk apa pun.
- Jangan menebak kode pemulihan orang lain; jangan mengunci akun sendiri dengan percobaan berlebihan.
- Kode pemulihan milik sendiri jangan dibagikan ke siapa pun.
