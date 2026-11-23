# Skill: Zip Slip — Zip Slip: entri arsip dengan path traversal (../) yang menulis file di luar folder ekstraksi saat diekstrak server.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 32 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis zip Slip: entri arsip dengan path traversal (../) yang menulis file di luar folder ekstraksi saat diekstrak server. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Lab/akun uji sendiri; tanpa menulis di luar direktori uji.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `bypass-unggah-file` — bypass unggah file umum
- `traversal-jalur-lfi` — traversal jalur / LFI
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
11. **Scope guard kandidat ini (WAJIB):** Lab/akun uji sendiri; tanpa menulis di luar direktori uji.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: lab/akun uji sendiri; tanpa menulis di luar direktori uji. Bukti Zip Slip adalah lokasi penulisan, bukan isi file yang merusak.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah unggah arsip dan ekstraksi server in-scope? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan alur unggah arsip

- Catat endpoint unggah arsip, format yang diterima, dan apa yang dilakukan server setelah unggah (ekstrak otomatis, pratinjau isi, impor).

**Standar lulus:** Alur unggah → ekstraksi tercatat.

### Gerbang 2 — Uji dengan entri canary jinak

- Unggah arsip berisi satu entri dengan nama traversal yang menunjuk ke direktori uji sendiri dan berisi teks canary unik — tanpa menimpa file sistem, tanpa file yang bisa dieksekusi, tanpa menunjuk ke luar direktori uji.
- Periksa apakah file canary muncul di direktori uji yang dituju.

**Standar lulus:** File canary muncul di direktori uji yang dituju, atau ekstraksi aman tercatat.

### Gerbang 3 — Buktikan penulisan di luar folder ekstraksi

- Buktikan file canary tertulis di luar folder ekstraksi yang semestinya (lokasi persis tercatat) — itu inti Zip Slip.
- Jangan menulis ke lokasi sistem atau menimpa file yang ada; bila satu-satunya jalur traversal menunjuk ke lokasi sensitif, BERHENTI dan serahkan ke Muse.

**Standar lulus:** Lokasi penulisan di luar folder ekstraksi tercatat; tidak ada file sistem yang disentuh.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (file apa yang bisa ditulis di mana) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Bersihkan file canary dari direktori uji.

**Standar lulus:** Dampak ditulis konkret + keputusan triase tercatat; file canary dibersihkan.

## Alat

| Alat | Cara pakai |
|---|---|
| Pembuat arsip (zip) di mesin sendiri | Buat arsip uji dengan entri bernama canary; hanya di mesin/lab sendiri. |
| Akun tes sendiri + direktori uji sendiri | Satu-satunya akun dan direktori yang dipakai; file canary unik. |
| `~/workspace/catatan/log-bug-bounty.md` | Log arsip uji, respons server, dan hasil pemeriksaan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [unggah-zip-slip — No. 32]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Server yang mengekstrak arsip dengan pustaka yang sudah menormalisasi jalur biasanya aman — entri traversal yang ditolak atau dinormalisasi bukan temuan. Jangan pernah mengunggah arsip traversal ke layanan produksi yang dipakai pengguna lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
