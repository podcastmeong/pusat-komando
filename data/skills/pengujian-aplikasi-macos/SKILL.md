# Skill: Pengujian Aplikasi macOS — Keychain, TCC, entitlements, dan auto-update sebagai permukaan aplikasi macOS

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 71. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan aplikasi macOS; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat program in-scope mencantumkan aplikasi macOS dan ada dugaan celah pada Keychain, izin TCC, entitlements, atau mekanisme auto-update (temuan tim: celah auto-update Mac bernilai $1rb).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pengujian aplikasi Electron → skill `pengujian-electron-desktop` (aplikasi desktop lintas platform).
- Pengujian ekstensi browser → skill `pengujian-ekstensi-browser` (permukaan browser, bukan aplikasi macOS).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Hanya bila program mencantumkan aplikasi macOS.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aplikasi macOS ini (nama + versi) eksplisit in-scope? Tanpa pencantuman eksplisit = jangan uji.
2. **Standar lulus:** nama aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Inventarisasi permukaan

1. Periksa entitlements, Info.plist, helper tool, dan kanal auto-update aplikasi di perangkat sendiri.
2. Periksa item Keychain yang dibuat aplikasi dan izin TCC yang dimintanya.
3. **Standar lulus:** daftar permukaan (entitlements, helper, auto-update, Keychain, TCC) tertulis.

### Gerbang 2 — Uji satu permukaan

1. Pilih satu permukaan (mis. auto-update: apakah kanal pembaruan memverifikasi tanda tangan? Keychain: apakah item bisa dibaca aplikasi lain?).
2. Uji di perangkat sendiri dengan aplikasi in-scope; catat perilaku nyata.
3. **Standar lulus:** hasil uji satu permukaan tercatat (rentan/aman + bukti perilaku).

### Gerbang 3 — Buktikan dampak aman + serahkan ke triase

1. Buktikan dampak tanpa merusak perangkat atau data (mis. pembaruan palsu ditolak/diterima di lab sendiri; akses Keychain hanya item milik sendiri).
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat macOS sendiri | Lingkungan uji aplikasi macOS |
| Alat inspeksi (codesign, plutil, Keychain Access) | Baca entitlements, plist, dan item Keychain milik sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-aplikasi-macos] — No. 71
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Aplikasi macOS in-scope punya celah pada Keychain, TCC, entitlements, atau auto-update.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aplikasi macOS yang eksplisit in-scope; jangan menguji aplikasi lain di perangkat sendiri.
- Jangan membajak kanal pembaruan aplikasi orang lain; uji hanya pada aplikasi in-scope di perangkat sendiri.
- Jangan membaca item Keychain milik aplikasi lain atau pengguna lain.
