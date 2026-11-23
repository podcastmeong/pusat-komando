# Skill: Basis Data Terbuka — Elasticsearch, MongoDB, Redis, dan CouchDB terekspos ke internet tanpa autentikasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 67. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program web/infrastruktur klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat ada dugaan basis data target in-scope terekspos langsung ke internet tanpa autentikasi — mis. port Elasticsearch/MongoDB/Redis yang merespons dari luar, atau layanan yang tercantum dalam scope infrastruktur program.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemindaian port/layanan → skill `pemindaian-port-layanan` (menemukan layanan; skill ini menguji autentikasinya).
- Enumerasi aset cloud → skill `enumerasi-aset-cloud` (bucket terbuka; skill ini untuk basis data).
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
11. **Scope guard kandidat:** Hanya membaca metadata/keberadaan; tanpa mengambil data.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope program: apakah aset infrastruktur/basis data ini in-scope? Banyak program web hanya mencakup aplikasi, bukan basis data yang terekspos.
2. **Standar lulus:** scope tercatat di log sebelum satu koneksi pun dibuat. Tanpa itu = jangan mulai.

### Gerbang 1 — Identifikasi layanan dan versi

1. Sambungkan ke layanan dan baca HANYA metadata yang diungkap layanan itu sendiri saat koneksi (banner, versi, nama klaster/indeks — tanpa isi dokumen).
2. Catat jenis layanan (Elasticsearch/MongoDB/Redis/CouchDB), versi, dan apakah autentikasi diminta.
3. **Standar lulus:** jenis + versi + status autentikasi tertulis. Bila autentikasi diminta = AMAN, tutup dengan buktinya.

### Gerbang 2 — Uji akses baca metadata saja

1. Bila tanpa autentikasi, daftar nama indeks/koleksi/kunci (metadata saja) — JANGAN membuka isi dokumen, baris data, atau nilai kunci.
2. Hitung jumlah indeks/koleksi sebagai ukuran paparan, tanpa membaca isinya.
3. **Standar lulus:** daftar metadata tercatat; TIDAK ADA isi data yang dibaca, disalin, atau disimpan. Satu baris data yang terbaca = pelanggaran scope guard, hentikan dan laporkan ke Muse.

### Gerbang 3 — Uji tulis (hanya bila aman dan diizinkan scope)

1. Tulis HANYA bila scope eksplisit mengizinkan dan hanya ke kunci/indeks canary milik sendiri; bila berhasil, segera hapus.
2. Bila scope tidak mengizinkan uji tulis, cukup buktikan akses baca metadata dan berhenti.
3. **Standar lulus:** hasil uji tulis tercatat (atau alasan tidak diuji), dan setiap canary sudah dihapus.

### Gerbang 4 — Nilai dampak + serahkan ke triase

1. Tulis dampak dari metadata yang terlihat (jumlah indeks/koleksi, nama yang menunjukkan data sensitif — tanpa membuka isinya) dan apa yang bisa dilakukan penyerang.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti metadata + keputusan triase tercatat. Tanpa bukti = belum berhasil.

## Alat

| Alat | Cara pakai |
|---|---|
| klien basis data (mongosh, redis-cli, curl untuk Elasticsearch) | Sambung dan baca metadata layanan; tanpa mengambil isi |
| Pemindai port | Verifikasi port layanan terbuka pada aset in-scope |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [basis-data-terbuka-elasticsearch-mongo-redis] — No. 67
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Basis data in-scope terekspos tanpa autentikasi sehingga metadata (nama indeks/koleksi) bisa dibaca siapa saja.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Scope guard MUTLAK: hanya metadata/keberadaan — jangan pernah membaca, menyalin, atau menyimpan isi data, walau layanan mengizinkannya.
- Nama indeks/koleksi saja sudah cukup sebagai bukti; jangan membuka satu dokumen pun untuk 'memastikan'.
- Bila program tidak mencantumkan aset infrastruktur, temuan ini di luar scope — serahkan ke Muse, jangan laporkan langsung.
