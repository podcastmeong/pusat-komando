# Skill: Mutation XSS (mXSS) — Mutation XSS (mXSS): markup yang bermutasi saat diparse ulang (innerHTML) sehingga filter lolos dan skrip jalan.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 29 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis mutation XSS (mXSS): markup yang bermutasi saat diparse ulang (innerHTML) sehingga filter lolos dan skrip jalan. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa menyerang pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `verifikasi-xss`, `pelacakan-taint-xss-dom` — XSS dasar dan pelacakan taint DOM
- `analisis-statis-js` — menemukan titik innerHTML/parse ulang di kode target
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa menyerang pengguna lain.
12. **Catatan khusus kandidat:** mXSS terjadi karena sanitizer memeriksa markup dalam satu bentuk, tetapi browser mem-parse ulang markup itu menjadi bentuk lain; bukti harus menunjukkan kedua tahap parse, bukan hanya bahwa markup lolos filter.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope program: apakah pengujian XSS diizinkan pada target ini? Catat di log sebelum menguji.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Temukan titik parse ulang

- Baca kode target dan cari titik di mana markup yang sudah dibersihkan diparse ulang: penugasan innerHTML, insertAdjacentHTML, document.write, atau parser DOM yang dipakai ulang.
- Catat titik parse ulang + sanitizer/filter yang dipakai sebelum titik itu.

**Standar lulus:** Minimal satu titik parse ulang tercatat dengan sanitizer yang mendahuluinya.

### Gerbang 2 — Uji markup yang bermutasi

- Kirim markup yang lolos filter pada parse pertama tetapi berubah bentuk saat diparse ulang (mis. markup bersarang yang 'diperbaiki' browser menjadi bentuk berbahaya), lalu amati hasil parse ulang di DevTools.
- Bila markup tidak bermutasi, catat dan tutup hipotesis itu.

**Standar lulus:** Hasil parse ulang tercatat; mutasi teramati atau hipotesis ditutup.

### Gerbang 3 — Buktikan eksekusi pada sesi sendiri

- Bila mutasi terjadi, buktikan skrip canary milik sendiri dieksekusi saat markup dirender di sesi akun sendiri — tanpa skrip yang menyerang pengguna lain dan tanpa aksi di luar akun sendiri.
- Kembalikan state akun sendiri ke semula setelah bukti didapat.

**Standar lulus:** Eksekusi skrip canary teramati pada sesi sendiri dan tercatat langkah-demi-langkah.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (markup apa, filter apa yang lolos, eksekusi apa yang terjadi) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Dampak ditulis konkret + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri + DevTools | Amati hasil parse ulang markup; hanya di sesi/akun sendiri. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai. |
| `~/workspace/catatan/log-bug-bounty.md` | Log markup uji, hasil mutasi, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [xss-mutasi-mxss — No. 29]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Sanitizer yang berbeda (DOMPurify, filter server, filter klien) bermutasi dengan cara berbeda — satu pola mXSS yang bekerja pada satu sanitizer belum tentu bekerja pada yang lain. Jangan memakai pola mXSS yang disalin mentah tanpa memahami titik parse ulangnya.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
