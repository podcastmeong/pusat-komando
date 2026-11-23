# Skill: Analisis Header HTTP Keamanan — Menganalisis header keamanan HTTP sebagai peta permukaan pasif

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 10. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pasif (hanya membaca header); tanpa eksploitasi.

## Pemicu (kapan dipakai)

Dipakai saat memetakan permukaan target in-scope dari luar secara pasif: membaca header respons HTTP (HSTS, CSP, X-Frame-Options, dan lainnya) untuk menilai postur keamanan tanpa mengirim satu pun payload. Dipakai di awal pemetaan web.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemetaan teknologi/stack → skill `pemetaan-teknologi-stack` (No. 11).
- Clickjacking → skill `perburuan-clickjacking`.
- Pembuktian dampak header yang hilang → skill pengujian terkait (bukan skill ini — skill ini hanya analisis pasif).

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
11. **Pasif saja — hanya membaca header respons normal.** Jangan mengirim payload, jangan memaksa error, jangan menguji bypass header di skill ini; pengujian aktif dilakukan skill lain dengan gerbangnya sendiri.
12. **Header yang hilang BUKAN otomatis kerentanan** — yang dinilai adalah apakah ketiadaannya benar-benar membuka celah yang bisa dibuktikan; jangan mengklaim temuan dari daftar header saja.

## Langkah + gerbang

### Gerbang 0 — Cek scope + target

1. Tetapkan target in-scope (host + halaman) dan baca pasal scope. Catat URL yang akan dibaca headernya.
2. **Standar lulus:** target tertulis. Tanpa itu = jangan mulai.

### Gerbang 1 — Baca header respons

1. Kirim request normal (GET halaman utama dan beberapa halaman kunci) dan catat semua header keamanan: Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, serta header kustom yang relevan.
2. **Standar lulus:** tabel header tercatat persis (nama + nilai) per halaman. Header yang tidak ada = dicatat "tidak ada", bukan diasumsikan.

### Gerbang 2 — Nilai tiap header

1. Untuk tiap header, nilai: ada/tidak, nilainya kuat atau lemah (mis. CSP yang longgar, HSTS tanpa includeSubDomains/max-age pendek, X-Frame-Options yang mengizinkan framing). Catat juga header yang saling bertentangan.
2. **Standar lulus:** penilaian tiap header tertulis dengan alasan. Penilaian tanpa nilai header persis = belum selesai.

### Gerbang 3 — Kaitkan dengan permukaan lain

1. Kaitkan hasil header dengan peta permukaan (No. 1, 11): mis. CSP longgar + endpoint yang menerima input pengguna = kandidat uji lanjut; X-Frame-Options hilang + halaman sensitif = kandidat clickjacking.
2. **Standar lulus:** daftar kandidat uji lanjut tertulis (atau "tidak ada kandidat" bila header sudah kuat). Daftar ini diserahkan ke A58.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP (request normal) | Membaca header respons tanpa payload |
| Browser milik sendiri | Memeriksa header + perilaku framing bila perlu |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Target: [host + halaman]
Header tercatat: [nama + nilai per halaman]
Kandidat uji lanjut: [header lemah + kaitannya]
Scope guard dipatuhi: [ya — Scope guard: pasif (hanya membaca header); tanpa eksploitasi.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Beberapa header hanya dikirim pada respons tertentu (mis. hanya di halaman login) — periksa beberapa halaman kunci, jangan hanya halaman utama.
- CSP yang terlihat ketat bisa punya celah (mis. 'unsafe-inline') — nilai isinya, bukan sekadar keberadaannya.
