# Skill: DNS Rebinding — DNS rebinding: memaksa browser menganggap host penyerang sebagai host internal lalu mengakses layanan internal.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 61 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis dNS rebinding: memaksa browser menganggap host penyerang sebagai host internal lalu mengakses layanan internal. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa mengakses layanan internal korban.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `deteksi-takeover-subdomain` — takeover subdomain (keluarga DNS yang berbeda)
- `ssrf-metadata-cloud` (No. 30) — SSRF ke alamat internal (tujuan serupa, vektor berbeda)
- `triase-duplikat` + `laporan-abstrak` — validasi dan pelaporan
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser/perangkat pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyalin, atau memakai data milik pengguna lain — walau terlihat.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pakai jeda antar-permintaan dan hentikan bila target melambat.
6. **Tanpa payload di permukaan publik.** Halaman/file PoC jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus/mengubah data, merusak layanan, menyebar paket/file berbahaya, atau memakai kredensial yang terbaca di luar PoC. Pembuktian HARUS aman, minimal, dan reversibel.
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa mengakses layanan internal korban.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: akun uji sendiri; tanpa mengakses layanan internal korban. Target rebinding hanyalah layanan canary di lab sendiri.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah pengujian DNS/layanan internal in-scope? Catat di log. Rebinding terhadap layanan internal orang lain dilarang.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan domain + layanan canary lab

- Atur domain milik sendiri dengan TTL pendek dan layanan canary di lab sendiri (mis. server HTTP kecil yang mencatat permintaan dan menampilkan nilai canary).
- Catat domain, TTL, dan layanan canary.

**Standar lulus:** Domain + layanan canary lab tercatat.

### Gerbang 2 — Uji resolusi ganda domain sendiri

- Periksa apakah domain sendiri pertama-tama meresolusi ke alamat publik, lalu setelah TTL habis meresolusi ke alamat internal lab — tanpa menyentuh DNS orang lain.
- Catat hasil resolusi tiap tahap.

**Standar lulus:** Hasil resolusi ganda tercatat.

### Gerbang 3 — Buktikan browser mengakses layanan internal lab

- Buka domain sendiri di browser milik sendiri dan periksa apakah skrip di halaman itu berhasil mengakses layanan canary internal lab (nilai canary terbaca).
- Targetnya hanya layanan canary lab sendiri — jangan mengakses layanan internal orang lain.

**Standar lulus:** Akses ke layanan canary lab terbukti atau dinyatakan gagal.

### Gerbang 4 — Serahkan ke triase

- Tulis rantai rebinding + bukti akses canary dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Rantai + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Domain + server DNS milik sendiri | Satu-satunya domain/DNS yang dipakai untuk rebinding; TTL pendek diatur sendiri. |
| Browser milik sendiri + layanan internal lab sendiri | Browser uji dan layanan internal lab (mis. layanan di localhost lab) sebagai target rebinding. |
| Layanan internal lab sendiri (canary) | Layanan canary di jaringan lab yang membuktikan akses terjadi. |
| `~/workspace/catatan/log-bug-bounty.md` | Log konfigurasi DNS, langkah, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [dns-rebinding — No. 61]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- DNS rebinding bergantung pada TTL dan cache DNS browser — hasil yang tidak terulang bisa disebabkan cache, bukan kegagalan teknik. Ulangi pengujian dengan cache dibersihkan sebelum menyatakan gagal.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
