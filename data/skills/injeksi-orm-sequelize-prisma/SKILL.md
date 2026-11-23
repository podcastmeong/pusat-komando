# Skill: Injeksi ORM Sequelize/Prisma — Manipulasi objek query ORM sehingga filter otorisasi lolos dan data bocor

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 77. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai ORM (Sequelize, Prisma, atau sejenisnya) dan ada dugaan objek query dari input pengguna diteruskan tanpa filter — mis. parameter JSON berisi operator ORM (`$gt`, `$ne`, dan sejenisnya) yang mengubah filter otorisasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi SQL kontekstual → skill `injeksi-sql-kontekstual` (SQL mentah; skill ini injeksi lewat objek ORM).
- Injeksi NoSQL → skill `injeksi-nosql` (operator JSON MongoDB; pola serupa, target berbeda).
- Mass assignment API → skill `mass-assignment-api` (field yang bisa diisi; skill ini operator query).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa membaca data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian injeksi diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu payload pun dikirim.

### Gerbang 1 — Identifikasi ORM dan cara query dibangun

1. Tentukan ORM dari petunjuk (error, stack, dokumentasi) dan cara input pengguna masuk ke objek query (parameter JSON, query string yang diparse sebagai objek).
2. **Standar lulus:** ORM + jalur input-ke-query tertulis. Tanpa jalur = jangan menebak operator.

### Gerbang 2 — Uji operator dengan akun sendiri

1. Kirim objek query canary memakai operator ORM pada filter milik AKUN SENDIRI (mis. filter yang seharusnya membatasi ke data sendiri) dan amati apakah filter lolos — mis. data sendiri yang seharusnya tersembunyi menjadi terlihat, atau sebaliknya.
2. **Standar lulus:** hasil tercatat (filter lolos/tidak + bukti pada data sendiri). Tanpa perubahan pada data sendiri = belum terbukti.

### Gerbang 3 — Buktikan batas otorisasi terlampaui (hanya data sendiri sebagai pembanding)

1. Buktikan bahwa operator mengubah hasil query melewati filter otorisasi — dengan membandingkan hasil sebelum/sesudah pada data MILIK SENDIRI saja. Jangan pernah membaca data pengguna lain walau filter lolos.
2. **Standar lulus:** perbandingan sebelum/sesudah tercatat; TIDAK ADA data pengguna lain yang dibaca.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Kirim objek query JSON dengan operator ORM canary |
| Dokumentasi ORM (Sequelize/Prisma) | Rujukan operator yang sah untuk diuji |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [injeksi-orm-sequelize-prisma] — No. 77
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Operator ORM pada input berhasil melewati filter otorisasi pada data milik akun uji sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya data milik sendiri yang dipakai sebagai pembanding; jangan membaca data pengguna lain walau filter lolos.
- Jangan memakai operator untuk menghapus/mengubah data (tanpa UPDATE/DELETE lewat ORM).
- ORM yang berbeda punya operator berbeda — uji sesuai ORM yang teridentifikasi, jangan menebak operator ORM lain.
