# Skill: Eksploitasi EternalBlue (SMB) — Lab — Eksploitasi layanan jaringan usang (mis. EternalBlue pada SMB) dengan Metasploit sebagai pola eksploitasi layanan jaringan.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 53 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis eksploitasi layanan jaringan usang (mis. EternalBlue pada SMB) dengan Metasploit sebagai pola eksploitasi layanan jaringan. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Lab sendiri saja; tanpa menyerang sistem nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `metasploit-framework` (No. 40) — framework yang dipakai untuk pola ini
- `pivoting-tunneling` (No. 54) — langkah lanjutan setelah satu host lab ditembus
- `terminal-linux-kali` (No. 38) — lingkungan kerja lab
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
11. **Scope guard kandidat ini (WAJIB):** Lab sendiri saja; tanpa menyerang sistem nyata.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: lab sendiri saja; tanpa menyerang sistem nyata. EternalBlue adalah pola eksploitasi layanan jaringan usang — nilai skill ini adalah polanya, bukan menjalankan exploit ke sistem nyata.

## Langkah + gerbang

### Gerbang 0 — Tegaskan: lab sendiri SAJA

- EternalBlue HANYA di lab sendiri (VM Windows lama milik sendiri yang tidak ditambal, di jaringan terisolasi). Tanpa menyerang sistem nyata dalam bentuk apa pun.
- Catat batas ini di log sebelum modul apa pun dijalankan.

**Standar lulus:** Batas lab-saja tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan VM lab yang rentan

- Bangun VM lab Windows lama yang tidak ditambal dari media resmi; isolasi jaringannya dari sistem lain; buat snapshot sebelum pengujian.
- Catat versi OS + status tambalan VM lab.

**Standar lulus:** VM lab siap + terisolasi + snapshot dibuat.

### Gerbang 2 — Konfirmasi layanan SMB di lab

- Periksa layanan SMB berjalan di VM lab dan versinya cocok dengan modul yang akan dipakai (lihat No. 40 Gerbang 1–2).
- Bila layanan tidak cocok, BERHENTI — jangan memaksa modul.

**Standar lulus:** Layanan SMB lab terkonfirmasi cocok atau pengujian dihentikan.

### Gerbang 3 — Jalankan modul exploit di lab

- Jalankan modul exploit SMB di VM lab dengan payload paling tidak invasif (pembuktian sesi); amati hasilnya di lab.
- Pulihkan VM dari snapshot setelah pengujian.

**Standar lulus:** Hasil modul di lab tercatat; VM dipulihkan dari snapshot.

### Gerbang 4 — Dokumentasikan pola sebagai pembelajaran

- Tulis pola eksploitasi layanan jaringan (identifikasi layanan → kecocokan modul → bukti sesi) sebagai catatan lab; pola ini dipakai ke target program HANYA bila program mencantumkan layanan jaringan in-scope dan lewat skill No. 40.

**Standar lulus:** Dokumentasi pola tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Metasploit Framework langsung (msfconsole) | Modul exploit SMB yang sudah diketahui; hanya di lab. |
| VM lab milik sendiri (Windows lama yang tidak ditambal, terisolasi) | Satu-satunya target; jaringan lab terisolasi tanpa akses ke sistem nyata. |
| Snapshot VM lab | Pulihkan VM ke keadaan semula setelah pengujian. |
| `~/workspace/catatan/log-bug-bounty.md` | Log modul, target lab, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [eksploitasi-eternalblue-smb-lab — No. 53]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- VM lab harus benar-benar terisolasi: SMB yang terekspos ke jaringan nyata bisa diserang pihak lain. Jangan pernah memindai atau mengeksploitasi SMB di jaringan yang bukan milik sendiri.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
