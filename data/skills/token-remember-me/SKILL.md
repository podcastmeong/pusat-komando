# Skill: Token Remember Me — Token 'remember me' yang persisten — bisa ditebak, tidak kedaluwarsa, atau tidak diinvalidasi saat ganti kata sandi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 93. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai token 'remember me' (atau cookie persisten serupa) dan ada dugaan tokennya bisa ditebak, tidak pernah kedaluwarsa, atau tetap hidup setelah kata sandi diganti / logout.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perburuan manajemen sesi → skill `perburuan-manajemen-sesi` (sesi umum; skill ini khusus token remember-me).
- Manipulasi JWT → skill `manipulasi-jwt` (bila tokennya JWT; skill ini perilaku siklus hidup token).
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

1. Baca pasal scope: apakah target dan pengujian sesi diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan token remember-me akun sendiri

1. Login ke AKUN SENDIRI dengan 'remember me' aktif; catat cookie/token yang dibuat (nama, format, panjang) dan masa berlakunya.
2. **Standar lulus:** format token + masa berlaku tertulis.

### Gerbang 2 — Uji invalidasi saat ganti kata sandi dan logout

1. Ganti kata sandi AKUN SENDIRI, lalu coba memakai token remember-me lama; amati apakah masih diterima.
2. Logout dari AKUN SENDIRI, lalu coba memakai token lama; amati apakah masih diterima.
3. **Standar lulus:** hasil tiap varian tercatat (masih diterima/ditolak). Invalidasi ditegakkan = AMAN.

### Gerbang 3 — Uji ketertebakan dan kedaluwarsa (hanya token sendiri)

1. Analisis pola dari beberapa token milik sendiri (apakah berurutan/pendek/berpola); uji token lama milik sendiri setelah masa berlaku yang dinyatakan.
2. **Standar lulus:** analisis pola + hasil kedaluwarsa tercatat. Token acak + kedaluwarsa ditegakkan = tidak terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (token lama yang tetap hidup / pola lemah pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Login, ganti kata sandi, logout pada akun sendiri |
| curl / klien HTTP | Pakai token lama dan amati respons |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [token-remember-me] — No. 93
Program: [HUNTR, PPLX, MISTRAL, ANTH, MUSE]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Token remember-me milik akun uji sendiri tetap diterima setelah kata sandi diganti atau setelah logout, atau tidak kedaluwarsa, atau polanya bisa ditebak.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa memakai token milik orang lain dalam bentuk apa pun.
- Jangan menebak token akun orang lain walau polanya tampak lemah.
- Setelah pengujian, hapus semua token uji dan login ulang dengan kredensial sendiri.
