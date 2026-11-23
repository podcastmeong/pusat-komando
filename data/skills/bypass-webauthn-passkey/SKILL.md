# Skill: Bypass WebAuthn Passkey — Kelemahan alur registrasi dan autentikasi passkey — fallback lemah, validasi longgar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 89. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai WebAuthn/passkey dan ada dugaan kelemahan pada alur registrasi atau autentikasi — mis. fallback yang lemah, validasi challenge/origin yang longgar, atau passkey yang bisa didaftarkan tanpa verifikasi yang benar.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis bypass 2FA → skill `analisis-bypass-2fa` (bypass faktor kedua; skill ini khusus WebAuthn/passkey).
- Perburuan bypass autentikasi → skill `perburuan-bypass-autentikasi` (bypass umum; skill ini khusus passkey).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa melewati autentikasi pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian autentikasi diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan alur WebAuthn

1. Petakan alur registrasi dan autentikasi passkey target: challenge, origin/RP ID yang diperiksa, fallback bila passkey gagal, dan apa yang terjadi bila validasi dilewati.
2. **Standar lulus:** alur tertulis (langkah + pemeriksaan tiap langkah). Tanpa peta = jangan menguji acak.

### Gerbang 2 — Uji validasi pada akun sendiri

1. Uji tiap pemeriksaan dengan akun uji SENDIRI: challenge yang dipakai ulang, origin yang salah, credential yang tidak terdaftar — amati mana yang ditolak.
2. **Standar lulus:** hasil tiap varian tercatat (ditolak/diterima). Pemeriksaan yang benar = AMAN.

### Gerbang 3 — Uji fallback

1. Uji jalur fallback (mis. bila passkey gagal, apakah ada cara masuk lain yang lebih lemah) hanya pada akun sendiri; catat apakah fallback melewati passkey tanpa verifikasi yang setara.
2. **Standar lulus:** perilaku fallback tercatat. Tanpa kelemahan fallback = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (varian yang lolos pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri + authenticator uji | Jalankan alur WebAuthn pada akun sendiri |
| curl / klien HTTP | Ulangi permintaan alur dengan variasi challenge/origin |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-webauthn-passkey] — No. 89
Program: [HUNTR, PPLX, MISTRAL, ANTH, MUSE]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Alur WebAuthn pada akun uji sendiri bisa dilewati (validasi longgar atau fallback lemah) sehingga autentikasi berhasil tanpa passkey yang sah.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa melewati autentikasi pengguna lain dalam bentuk apa pun.
- Jangan mendaftarkan passkey ke akun orang lain atau menghapus passkey orang lain.
- Jangan memakai kredensial/passkey milik orang lain sebagai bahan uji.
