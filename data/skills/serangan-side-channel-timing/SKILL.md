# Skill: Serangan Side-Channel Timing — Membedakan respons benar/salah dari waktu proses tanpa melihat isi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 87. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat ada dugaan perbandingan rahasia (token, kata sandi, kode) dilakukan tanpa waktu konstan, atau respons benar/salah bisa dibedakan dari waktu proses — sehingga nilai rahasia bisa ditebak dari pengukuran waktu.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perburuan brute-force/rate-limit → skill `perburuan-brute-force-rate-limit` (tebakan berulang; skill ini memakai waktu sebagai sinyal).
- Analisis bypass 2FA → skill `analisis-bypass-2fa` (bila celahnya pada kode OTP).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa mengukur data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengukuran waktu diizinkan? Perhatikan rate limit program — pengukuran butuh banyak permintaan.
2. **Standar lulus:** scope + batas rate tercatat di log sebelum mulai.

### Gerbang 1 — Identifikasi titik perbandingan rahasia

1. Cari endpoint yang membandingkan nilai rahasia milik AKUN SENDIRI (token reset, kode OTP sendiri, kata sandi sendiri) dan catat apakah responsnya membedakan benar/salah.
2. **Standar lulus:** titik perbandingan tertulis (endpoint + nilai rahasia milik sendiri yang dibandingkan).

### Gerbang 2 — Ukur baseline dan perbedaan waktu

1. Ukur waktu respons untuk nilai benar vs salah milik sendiri, berulang kali (minimal 10x tiap nilai), dengan jeda sesuai rate limit; hitung rata-rata dan sebarannya.
2. **Standar lulus:** data waktu tercatat (rata-rata benar vs salah + jumlah sampel). Perbedaan yang tidak konsisten = belum terbukti (bisa jadi noise jaringan).

### Gerbang 3 — Buktikan penebakan karakter (hanya nilai sendiri)

1. Bila perbedaan waktu konsisten, buktikan satu karakter nilai rahasia MILIK SENDIRI bisa ditebak dari waktu (mis. karakter pertama token canary sendiri) — dan hanya itu.
2. **Standar lulus:** satu karakter canary sendiri berhasil ditebak dari waktu dan terkonfirmasi. Tanpa itu = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (data waktu + penebakan karakter canary) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Klien HTTP + pengukur waktu | Ukur waktu respons berulang dengan presisi |
| Lembar hitung | Rata-rata, sebaran, dan uji konsistensi perbedaan waktu |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [serangan-side-channel-timing] — No. 87
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Waktu respons untuk nilai benar vs salah milik sendiri berbeda konsisten, dan satu karakter token canary sendiri berhasil ditebak dari waktu.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya nilai rahasia milik sendiri yang diukur/ditebak; tanpa mengukur data pengguna lain.
- Patuhi rate limit program — pengukuran yang membanjiri server adalah DoS dan dilarang.
- Noise jaringan bisa meniru perbedaan waktu; klaim hanya bila perbedaan konsisten dan terulang.
