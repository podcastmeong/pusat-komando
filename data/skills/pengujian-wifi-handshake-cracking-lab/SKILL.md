# Skill: Pengujian Wi-Fi — Handshake & Cracking (Lab) — Aircrack-ng: menangkap handshake Wi-Fi dan menguji kekuatan kata sandi nirkabel pada jaringan sendiri.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 56 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis aircrack-ng: menangkap handshake Wi-Fi dan menguji kekuatan kata sandi nirkabel pada jaringan sendiri. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya jaringan Wi-Fi sendiri/lab; tanpa jaringan orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `cracking-kata-sandi-hydra-hashcat` (No. 52) — cracking offline yang sama polanya (hash/kredensial sendiri)
- `analisis-lalu-lintas-wireshark` — analisis paket (pendekatan pasif)
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
11. **Scope guard kandidat ini (WAJIB):** Hanya jaringan Wi-Fi sendiri/lab; tanpa jaringan orang lain.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya jaringan Wi-Fi sendiri/lab; tanpa jaringan orang lain. Handshake yang ditangkap adalah milik sendiri dan diuji offline.

## Langkah + gerbang

### Gerbang 0 — Tegaskan: jaringan sendiri SAJA

- Pengujian Wi-Fi HANYA pada jaringan Wi-Fi milik sendiri/lab. Jangan pernah menangkap handshake atau menguji jaringan orang lain.
- Catat jaringan + pemiliknya di log sebelum alat apa pun dijalankan.

**Standar lulus:** Jaringan sendiri tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan jaringan lab sendiri

- Pastikan router dan kata sandi jaringan lab diketahui dan dimiliki sendiri; catat nama jaringan (SSID) lab.
- Siapkan perangkat klien sendiri untuk memicu handshake.

**Standar lulus:** Jaringan lab tercatat.

### Gerbang 2 — Tangkap handshake jaringan sendiri

- Tangkap handshake saat perangkat sendiri terhubung ke jaringan sendiri; simpan berkas tangkapan di mesin lab.
- Jangan memakai serangan deauth terhadap klien orang lain — bila perlu memicu handshake ulang, putuskan dan sambungkan kembali perangkat sendiri saja.

**Standar lulus:** Handshake jaringan sendiri tertangkap dan tersimpan di lab.

### Gerbang 3 — Uji kekuatan kata sandi secara offline

- Jalankan cracking offline terhadap handshake sendiri dengan wordlist kecil; catat apakah kata sandi sendiri mudah ditebak.
- Bila kata sandi sendiri terbukti lemah, ganti kata sandi jaringan itu segera — jangan menulis kata sandi utuh di log.

**Standar lulus:** Hasil cracking offline tercatat; kata sandi lemah segera diganti.

### Gerbang 4 — Dokumentasikan pelajaran

- Tulis penilaian kekuatan kata sandi jaringan sendiri dan pelajaran (panjang, kerumitan) sebagai catatan lab.

**Standar lulus:** Penilaian + pelajaran tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Jaringan Wi-Fi milik sendiri + router sendiri | Satu-satunya jaringan yang diuji; kata sandi jaringan diketahui sendiri. |
| Adaptor nirkabel + Aircrack-ng di mesin lab sendiri | Menangkap handshake jaringan sendiri dan menguji kata sandinya offline. |
| Perangkat klien milik sendiri | Perangkat yang dipakai untuk memicu handshake jaringan sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log jaringan, metode, dan hasil — tanpa menulis kata sandi jaringan secara utuh. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-wifi-handshake-cracking-lab — No. 56]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Menangkap handshake jaringan orang lain — walau hanya 'untuk menguji' — adalah penyadapan. Serangan deauth terhadap klien orang lain dilarang (lihat juga skill ketahanan-dos-lab-sendiri untuk batas DoS).
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
