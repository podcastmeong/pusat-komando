# Skill: Pemetaan Alur Autentikasi — Memetakan alur login, SSO, MFA, dan pemulihan sebelum menguji

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 18. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pemetaan saja; pengujian hanya akun uji sendiri.

## Pemicu (kapan dipakai)

Dipakai sebelum menguji autentikasi: memetakan alur login, SSO, MFA, dan pemulihan akun target in-scope — menemukan titik lemah tanpa menyerang. Pemetaan saja; pengujian tiap titik dilakukan skill terkait dengan akun sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Bypass 2FA/MFA → skill `analisis-bypass-2fa`.
- Reset kata sandi/ATO → skill `alur-reset-kata-sandi-ato`.
- Manipulasi JWT/sesi → skill `manipulasi-jwt` dan `perburuan-manajemen-sesi`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic, Muse). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Pemetaan saja di skill ini.** Jangan menguji bypass, brute-force, atau pemulihan akun di sini — tiap pengujian memakai skill terkait + akun uji sendiri.
12. **Jangan memetakan alur akun orang lain.** Alur yang dipetakan adalah alur umum yang disediakan target untuk semua pengguna, diuji dengan akun sendiri; jangan memakai akun atau data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + target

1. Tetapkan target in-scope (aplikasi/situs) dan baca pasal scope: apakah pengujian autentikasi diizinkan?
2. **Standar lulus:** target + izin tercatat sebelum pemetaan dimulai.

### Gerbang 1 — Petakan alur login

1. Dengan akun sendiri, lalui dan catat alur login: metode yang tersedia (kata sandi, SSO, magic link, passkey), langkah-langkahnya, pesan error yang muncul, dan apa yang terjadi pada kredensial salah.
2. **Standar lulus:** diagram/langkah alur login tertulis. Langkah yang tidak teramati = ditandai "belum terverifikasi".

### Gerbang 2 — Petakan MFA dan SSO

1. Catat alur MFA (jenis faktor, kapan diminta, apa yang terjadi bila faktor gagal) dan SSO (penyedia identitas, parameter state, redirect) — hanya dari alur akun sendiri.
2. **Standar lulus:** alur MFA + SSO tertulis. Alur yang tidak bisa diamati dengan akun sendiri = ditandai, bukan ditebak.

### Gerbang 3 — Petakan alur pemulihan

1. Catat alur pemulihan akun (lupa kata sandi, kode pemulihan, pertanyaan keamanan): langkah-langkahnya, token/ tautan yang dikirim, dan masa berlakunya — hanya untuk akun sendiri.
2. **Standar lulus:** alur pemulihan tertulis. Titik yang tampak lemah ditandai sebagai kandidat, bukan vonis.

### Gerbang 4 — Serahkan kandidat titik lemah

1. Serahkan peta + daftar kandidat titik lemah ke A58 untuk dirumuskan menjadi hipotesis pengujian (skill terkait). Jangan menguji di skill ini.
2. **Standar lulus:** daftar kandidat tertulis + hipotesis pertama dirumuskan.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri + akun tes sendiri | Melalui alur autentikasi dan mencatat langkahnya |
| Catatan alur (diagram/langkah) | Peta yang diserahkan ke A58 |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Target: [aplikasi in-scope]
Alur terpetakan: [login + MFA + SSO + pemulihan]
Kandidat titik lemah: [titik + alasan]
Scope guard dipatuhi: [ya — Scope guard: pemetaan saja; pengujian hanya akun uji sendiri.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Alur autentikasi sering berbeda antar-peran (pengguna biasa vs admin) — petakan per peran yang dimiliki akun sendiri, jangan menggeneralisasi.
- Pesan error yang berbeda antara 'pengguna tidak ada' dan 'kata sandi salah' adalah petunjuk enumerasi — catat, jangan dieksploitasi di skill ini.
