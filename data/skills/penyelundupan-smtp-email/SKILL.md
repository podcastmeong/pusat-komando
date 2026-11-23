# Skill: Penyelundupan SMTP (Email Smuggling) — SMTP smuggling: menyelundupkan email lewat perbedaan parsing server SMTP sehingga spoofing lolos validasi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 60 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis sMTP smuggling: menyelundupkan email lewat perbedaan parsing server SMTP sehingga spoofing lolos validasi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa mengirim email palsu ke korban.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `perburuan-tls-dns-email-spoofing` — spoofing TLS/DNS/email secara umum
- `analisis-batas-kepercayaan` — perbedaan parsing sebagai titik kepercayaan
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa mengirim email palsu ke korban.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: akun uji sendiri; tanpa mengirim email palsu ke korban. Penerima setiap email uji adalah alamat sendiri.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah pengujian email/SPF/DKIM/DMARC in-scope pada target ini? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan validasi email target

- Catat validasi yang dipakai target: SPF, DKIM, DMARC, dan cara server SMTP mem-parse batas pesan (akhir DATA, baris kosong, pemisah header).
- Catat juga alamat pengirim yang diizinkan dan yang ditolak.

**Standar lulus:** Daftar validasi + perilaku parsing tercatat.

### Gerbang 2 — Kirim email uji ke alamat sendiri

- Kirim email uji dari akun sendiri ke alamat sendiri melewati server target, dengan satu variasi parsing per uji (mis. pemisah yang tidak biasa di antara dua pesan).
- Periksa apakah email sampai, dan bagaimana header validasi (SPF/DKIM/DMARC) tercatat pada email yang sampai.

**Standar lulus:** Hasil tiap varian tercatat (sampai/tidak + hasil validasi).

### Gerbang 3 — Buktikan spoofing lolos validasi

- Bila satu varian membuat email dengan pengirim yang dipalsukan lolos validasi dan sampai ke alamat sendiri, itu bukti inti: catat varian + header validasi yang menunjukkan lolos.
- Jangan mengirim email palsu ke alamat orang lain — penerima uji hanya alamat sendiri.

**Standar lulus:** Bukti spoofing lolos (varian + header) tercatat, atau semua varian dinyatakan gagal.

### Gerbang 4 — Serahkan ke triase

- Tulis varian + header validasi + dampak (pengirim apa yang bisa dipalsukan) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Varian + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun email uji sendiri (pengirim + penerima milik sendiri) | Satu-satunya alamat yang dipakai; email uji hanya dikirim ke alamat sendiri. |
| Server SMTP target in-scope | Satu-satunya server yang diuji; baca pasal scope dulu. |
| Klien SMTP / skrip pengirim di mesin sendiri | Mengirim email uji dengan format yang bervariasi; satu varian per uji. |
| `~/workspace/catatan/log-bug-bounty.md` | Log varian, hasil validasi, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [penyelundupan-smtp-email — No. 60]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Perbedaan parsing SMTP adalah celah implementasi, bukan celah protokol semata — satu server yang lolos belum tentu berarti server lain lolos. Jangan memakai email uji untuk menipu siapa pun.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
