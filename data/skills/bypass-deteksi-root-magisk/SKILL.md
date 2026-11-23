# Skill: Bypass Deteksi Root Magisk — Melewati cek root aplikasi dengan modul Magisk (Shamiko/Zygisk) atau skrip Frida

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 99. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program yang mencantumkan aplikasi mobile; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat aplikasi Android in-scope menolak berjalan di perangkat root dan ada dugaan cek root-nya bisa dilewati — dengan modul Magisk (Shamiko/Zygisk) atau skrip Frida — sehingga proteksi aplikasi gugur.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Frida/Objection runtime → skill `frida-objection-runtime` (instrumentasi runtime; skill ini penerapannya pada cek root).
- Sandbox mobile root/jailbreak → skill `sandbox-mobile-root-jailbreak` (sandbox dan root; skill ini bypass deteksinya).
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
11. **Scope guard kandidat:** Hanya perangkat/aplikasi sendiri; lab sendiri.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aplikasi Android ini eksplisit in-scope dan apakah pengujian di perangkat root diizinkan?
2. **Standar lulus:** aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Petakan cek root aplikasi

1. Pada perangkat/emulator SENDIRI, jalankan aplikasi dan catat cek root apa yang dilakukan (file su, build tags, Magisk, SafetyNet/Play Integrity) dan kapan aplikasi menolak.
2. **Standar lulus:** daftar cek root + titik penolakan tertulis.

### Gerbang 2 — Uji bypass satu cek

1. Terapkan SATU teknik bypass (modul Magisk Shamiko/Zygisk atau skrip Frida) pada perangkat sendiri; amati cek mana yang lolos dan mana yang tetap menolak.
2. **Standar lulus:** hasil per cek tercatat (lolos/tetap menolak). Semua cek tetap menolak = belum terbukti.

### Gerbang 3 — Buktikan aplikasi berjalan + serahkan ke triase

1. Bila semua cek lolos, buktikan aplikasi berjalan penuh di perangkat root milik sendiri (fitur sensitif bisa diakses) — hanya akun/data sendiri.
2. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator Android sendiri (root) | Lingkungan uji bypass |
| Magisk + modul Shamiko/Zygisk | Sembunyikan root dari aplikasi |
| Frida | Lewati cek root lewat instrumentasi runtime |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-deteksi-root-magisk] — No. 99
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Cek root aplikasi in-scope berhasil dilewati di perangkat sendiri sehingga aplikasi berjalan penuh di perangkat root.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya perangkat/aplikasi SENDIRI; lab sendiri. Jangan memakai bypass ini pada aplikasi di luar scope.
- Jangan memakai bypass untuk mengakses data pengguna lain atau memalsukan integritas perangkat di layanan nyata.
- Bila aplikasi adalah mobile banking/finansial, dampak dilaporkan apa adanya; jangan melakukan transaksi nyata.
