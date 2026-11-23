# Skill: Penyalahgunaan Refresh Token — Replay refresh token, rotasi yang tidak ditegakkan, dan token lama yang tetap hidup setelah logout

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 94. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai refresh token (OAuth/OIDC atau sesi API) dan ada dugaan token bisa di-replay, rotasi tidak ditegakkan, atau token lama tetap hidup setelah logout.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perburuan manajemen sesi → skill `perburuan-manajemen-sesi` (sesi umum; skill ini khusus siklus refresh token).
- Manipulasi JWT → skill `manipulasi-jwt` (bila tokennya JWT; skill ini perilaku rotasi/replay).
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

1. Baca pasal scope: apakah target dan pengujian token diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Petakan alur refresh token akun sendiri

1. Login ke AKUN SENDIRI; catat access token + refresh token yang diterbitkan, masa berlakunya, dan apakah rotasi dinyatakan (refresh token baru tiap pemakaian).
2. **Standar lulus:** alur + aturan rotasi tertulis.

### Gerbang 2 — Uji replay dan rotasi

1. Pakai refresh token milik sendiri untuk meminta access token baru, lalu pakai refresh token LAMA yang sama sekali lagi; amati apakah masih diterima (rotasi tidak ditegakkan) atau ditolak.
2. **Standar lulus:** hasil replay tercatat (diterima/ditolak). Rotasi ditegakkan = AMAN untuk varian ini.

### Gerbang 3 — Uji invalidasi setelah logout

1. Logout dari AKUN SENDIRI, lalu coba memakai refresh token lama; amati apakah masih diterima.
2. **Standar lulus:** hasil tercatat (masih diterima/ditolak). Invalidasi ditegakkan = AMAN.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (replay/rotasi/invalidasi pada akun sendiri) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Tukar refresh token dan uji replay/rotasi |
| Akun uji sendiri | Satu-satunya akun yang tokennya diuji |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [penyalahgunaan-refresh-token] — No. 94
Program: [HUNTR, PPLX, MISTRAL, ANTH, MUSE]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Refresh token milik akun uji sendiri bisa di-replay setelah dipakai, atau rotasi tidak ditegakkan, atau token lama tetap hidup setelah logout.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji SENDIRI; tanpa memakai token milik orang lain dalam bentuk apa pun.
- Jangan membagikan refresh token milik sendiri ke siapa pun; cabut semua token uji setelah selesai.
- Jangan memakai refresh token untuk mengakses data pengguna lain.
