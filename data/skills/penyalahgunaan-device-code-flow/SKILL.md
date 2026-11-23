# Skill: Penyalahgunaan Device Code Flow — Kode perangkat OAuth yang dipancing agar korban mengotorisasi — device code phishing

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 95. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai device code flow OAuth (login perangkat tanpa keyboard) dan ada dugaan alurnya bisa disalahgunakan — mis. kode perangkat tidak kedaluwarsa dengan cepat, atau tidak ada ikatan yang mencegah pemancingan otorisasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perburuan bypass autentikasi → skill `perburuan-bypass-autentikasi` (bypass umum; skill ini khusus device code flow).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa memancing korban nyata.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian alur OAuth diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan device code flow target

1. Minta device code sebagai AKUN SENDIRI; catat masa berlaku kode, apakah kode terikat ke perangkat/peminta, dan pesan verifikasi apa yang ditampilkan ke pengguna.
2. **Standar lulus:** alur + masa berlaku + ikatan kode tertulis.

### Gerbang 2 — Uji masa berlaku dan pemakaian ulang

1. Minta device code milik sendiri, biarkan hingga melewati masa berlaku yang dinyatakan, lalu coba selesaikan; amati apakah masih diterima.
2. Coba selesaikan kode yang sama dua kali (bila sudah berhasil sekali); amati apakah diterima lagi.
3. **Standar lulus:** hasil tiap varian tercatat (diterima/ditolak).

### Gerbang 3 — Uji pemancingan pada diri sendiri (simulasi korban = diri sendiri)

1. Simulasikan pemancingan HANYA terhadap diri sendiri: minta device code, lalu otorisasi dari akun sendiri yang berbeda konteks (perangkat kedua milik sendiri) — amati apakah pesan verifikasi cukup menjelaskan apa yang diotorisasi (nama aplikasi/perangkat).
2. **Standar lulus:** kejelasan pesan verifikasi tercatat (menyebut aplikasi/perangkat/tidak). Pesan yang jelas = mitigasi yang bekerja.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (kedaluwarsa/pemakaian ulang/pesan verifikasi yang menyesatkan pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Minta dan selesaikan device code milik sendiri |
| Dua perangkat/akun milik sendiri | Simulasi peminta vs pengotorisasi — keduanya milik sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [penyalahgunaan-device-code-flow] — No. 95
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Device code milik sendiri masih bisa diselesaikan setelah kedaluwarsa atau dipakai ulang, atau pesan verifikasinya tidak menjelaskan apa yang diotorisasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: akun uji SENDIRI; tanpa memancing korban nyata dalam bentuk apa pun.
- Simulasi pemancingan hanya terhadap diri sendiri (akun/perangkat sendiri).
- Jangan mengirim tautan/kode verifikasi ke orang lain.
