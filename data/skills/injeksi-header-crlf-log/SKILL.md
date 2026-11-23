# Skill: Injeksi Header CRLF/Log — Menyisipkan baris baru lewat header/input sehingga log teracuni atau respons terbelah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 76. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat input pengguna (header, parameter, atau nilai yang dicatat ke log) diduga diteruskan tanpa sanitasi ke header respons atau berkas log — sehingga karakter baris baru (CRLF) bisa membelah respons atau meracuni log.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi SQL kontekstual → skill `injeksi-sql-kontekstual` (injeksi ke query; skill ini injeksi ke header/log).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa meracuni log produksi.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian injeksi header diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu payload pun dikirim.

### Gerbang 1 — Temukan titik yang memantulkan input ke header/log

1. Cari parameter/header yang nilainya muncul kembali di header respons (mis. Location, Set-Cookie) atau yang diketahui dicatat ke log (mis. User-Agent, nama).
2. **Standar lulus:** titik injeksi tertulis (parameter + tempat pantulannya). Tanpa titik = jangan menebak.

### Gerbang 2 — Uji CRLF dengan pola identifikasi

1. Kirim nilai canary berisi penanda baris baru yang TIDAK BERBAHAYA (mis. nilai dengan `%0d%0a` + header canary bernama jelas seperti `X-Canary-Test`) dan amati apakah respons terbelah (header baru muncul) atau log mencatat baris palsu milik sendiri.
2. **Standar lulus:** hasil tercatat (terbelah/tidak + bukti header/log). Pola yang tidak mengubah respons = tidak terbukti.

### Gerbang 3 — Buktikan dampak terbatas + serahkan ke triase

1. Tulis dampak konkret: header apa yang bisa disisipkan (mis. Set-Cookie canary) atau baris log palsu apa yang bisa dibuat — tanpa meracuni log produksi dengan data menyesatkan tentang orang lain.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Kirim nilai canary CRLF dan baca header respons |
| Log milik sendiri (bila tersedia) | Periksa baris log yang tercatak dari aksi sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [injeksi-header-crlf-log] — No. 76
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Input canary dengan CRLF berhasil membelah header respons atau menyisipkan baris log palsu milik sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Tanpa meracuni log produksi: hanya baris canary milik sendiri yang jelas-jelas penanda uji; jangan menyisipkan baris yang meniru aktivitas pengguna lain atau menyembunyikan jejak.
- Jangan menyisipkan header Set-Cookie yang menimpa sesi pengguna lain; uji hanya pada sesi sendiri.
- Satu respons terbelah pada header canary sudah cukup; jangan lanjut ke eksploitasi lanjutan.
