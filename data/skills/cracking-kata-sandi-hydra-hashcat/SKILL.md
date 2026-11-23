# Skill: Cracking Kata Sandi — Hydra & Hashcat — Password cracking: Hydra (online, SSH/FTP/RDP) dan Hashcat (offline, hash) untuk menguji kekuatan kata sandi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 52 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis password cracking: Hydra (online, SSH/FTP/RDP) dan Hashcat (offline, hash) untuk menguji kekuatan kata sandi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya hash/kredensial sendiri atau lab; tanpa menyerang akun orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `serangan-kredensial-spray` — batas yang sama: akun uji sendiri saja
- `eskalasi-hak-akses-linux` (No. 36) / `eskalasi-hak-akses-windows` (No. 37) — privesc yang kadang memakai hash lokal lab
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
11. **Scope guard kandidat ini (WAJIB):** Hanya hash/kredensial sendiri atau lab; tanpa menyerang akun orang lain.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya hash/kredensial SENDIRI atau lab; tanpa menyerang akun orang lain. Batasnya sama seperti skill serangan-kredensial-spray: akun uji sendiri saja.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu: hanya milik sendiri

- Cracking HANYA untuk hash/kredensial milik sendiri atau lab sendiri. Jangan pernah memecahkan hash atau menyerang akun orang lain; jangan menguji Hydra terhadap layanan yang bukan lab sendiri tanpa scope eksplisit.
- Catat batas ini di log sebelum alat apa pun dijalankan.

**Standar lulus:** Batas milik-sendiri/lab tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Uji offline dulu (Hashcat) dengan hash sendiri

- Buat hash dari kata sandi sendiri di lab (atau pakai hash lab resmi); jalankan Hashcat offline dengan wordlist kecil dan aturan dasar.
- Catat mode hash, wordlist, dan waktu yang dipakai — tanpa menulis kata sandi hasil pecahan secara utuh di log.

**Standar lulus:** Hasil Hashcat lab tercatat (berhasil/gagal + waktu).

### Gerbang 2 — Uji online (Hydra) hanya ke layanan lab sendiri

- Jalankan Hydra hanya terhadap layanan lab milik sendiri dengan akun uji sendiri; pakai daftar kecil, jeda antar-percobaan, dan hentikan bila layanan membatasi.
- Jangan menjalankan Hydra terhadap layanan produksi atau akun orang lain.

**Standar lulus:** Hasil Hydra lab tercatat; layanan membatasi = berhenti.

### Gerbang 3 — Nilai kekuatan, bukan membobol

- Tulis penilaian: kata sandi sendiri/lab itu lemah (mudah dipecahkan) atau kuat (tahan terhadap wordlist + aturan yang dipakai).
- Bila kata sandi akun nyata terbukti lemah, ganti kata sandi itu segera — jangan menulisnya di laporan.

**Standar lulus:** Penilaian kekuatan tercatat; kata sandi lemah yang nyata segera diganti.

### Gerbang 4 — Serahkan bila program meminta bukti

- Bila program bounty meminta bukti kebijakan kata sandi yang lemah pada layanan in-scope, serahkan temuan (kebijakan + bukti, tanpa kata sandi utuh) ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Keputusan triase tercatat; tidak ada kata sandi utuh di laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Hashcat (offline) + hash milik sendiri / hash lab | Satu-satunya hash yang dipecahkan; hash dibuat dari kata sandi sendiri di lab. |
| Hydra (online) + layanan lab sendiri | Satu-satunya layanan yang diuji; layanan lab milik sendiri dengan akun uji sendiri. |
| Wordlist publik + aturan (rules) Hashcat | Wordlist umum; tanpa wordlist berisi data pribadi orang lain. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hash/layanan yang diuji, metode, dan hasil — tanpa menulis kata sandi yang berhasil dipecahkan secara utuh bila itu kata sandi akun nyata. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [cracking-kata-sandi-hydra-hashcat — No. 52]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hashcat offline terhadap hash sendiri adalah cara yang sah mengukur kekuatan kata sandi. Hydra online terhadap layanan orang lain adalah serangan brute-force — jangan pernah dilakukan. Kata sandi yang berhasil dipecahkan tidak ditulis utuh di mana pun.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
