# Skill: Injeksi CSS Ekfiltrasi — CSS yang disuntikkan membocorkan isi halaman lewat selector/atribut

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 79. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat input pengguna diduga bisa menyuntikkan CSS ke halaman target (mis. profil, tema, atau konten yang dirender dengan CSS kustom) dan CSS itu bisa membocorkan isi halaman lewat selector/atribut.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- XSS DOM clobbering / mXSS → skill `xss-dom-clobbering`, `xss-mutasi-mxss` (eksekusi skrip; skill ini ekfiltrasi lewat CSS tanpa skrip).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa menyerang pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian injeksi CSS diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu payload pun dikirim.

### Gerbang 1 — Temukan titik injeksi CSS

1. Cari input yang nilainya dirender sebagai CSS atau memengaruhi gaya halaman (tema kustom, profil, editor konten) pada akun sendiri.
2. **Standar lulus:** titik injeksi tertulis (input + tempat CSS dirender). Tanpa titik = jangan menebak.

### Gerbang 2 — Uji injeksi CSS canary

1. Suntikkan CSS canary tidak berbahaya (mis. aturan yang mengubah warna elemen milik sendiri) dan amati apakah CSS diterapkan.
2. **Standar lulus:** hasil tercatat (diterapkan/tidak + bukti visual/DOM). CSS tidak diterapkan = tidak terbukti.

### Gerbang 3 — Uji ekfiltrasi pada data sendiri

1. Dengan CSS yang membocorkan nilai atribut lewat selector, uji HANYA terhadap data milik AKUN SENDIRI (mis. token canary palsu yang sengaja ditaruh di halaman sendiri) dan periksa apakah nilainya bisa ditebak karakter demi karakter.
2. **Standar lulus:** ekfiltrasi terhadap data canary sendiri terbukti (atau tidak). Jangan pernah menguji terhadap data pengguna lain.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Periksa CSS yang diterapkan dan DOM halaman |
| Halaman uji milik sendiri | Tempat CSS canary dan data canary ditaruh |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [injeksi-css-ekfiltrasi] — No. 79
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [CSS canary yang disuntikkan diterapkan dan berhasil membocorkan nilai canary milik sendiri lewat selector/atribut.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya data canary milik sendiri yang dipakai sebagai target ekfiltrasi; jangan menyerang pengguna lain.
- CSS injection tanpa ekfiltrasi yang terbukti masih bisa dilaporkan sebagai injeksi — nilailah dampak apa adanya.
- Jangan menyuntikkan CSS yang merusak tampilan pengguna lain atau halaman publik.
