# Skill: PowerShell Windows untuk Bounty — PowerShell/Command Prompt Windows untuk pengujian bounty: enumerasi, jaringan, dan otomasi di lingkungan Windows.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 39 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis powerShell/Command Prompt Windows untuk pengujian bounty: enumerasi, jaringan, dan otomasi di lingkungan Windows. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Pengetahuan dasar; tanpa perintah destruktif di luar lab.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `terminal-linux-kali` (No. 38) — padanan Linux
- `eskalasi-hak-akses-windows` (No. 37) — privesc Windows yang memakai perintah ini
- `otomasi-python-bash-bounty` (No. 34) — otomasi lintas platform
- `triase-duplikat` — validasi temuan
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
11. **Scope guard kandidat ini (WAJIB):** Pengetahuan dasar; tanpa perintah destruktif di luar lab.
12. **Catatan khusus kandidat:** Skill dasar ini melayani SEMUA program karena PowerShell adalah alat kerja di lingkungan Windows — isinya adalah perintah dan disiplin, bukan teknik serangan.

## Langkah + gerbang

### Gerbang 0 — Kenali lingkungan kerja

- Periksa versi PowerShell, kebijakan eksekusi, dan pengguna saat ini; pastikan bekerja di mesin/lab sendiri.
- Catat lingkungan kerja di log.

**Standar lulus:** Lingkungan kerja tercatat; tidak ada perintah yang menyentuh sistem orang lain.

### Gerbang 1 — Enumerasi file dan proses di mesin sendiri

- Kuasai pencarian file dan teks, daftar proses/layanan, dan pemeriksaan jaringan di mesin sendiri.
- Latih pola: cari file konfigurasi di lab sendiri dan catat yang relevan.

**Standar lulus:** Perintah enumerasi berjalan lancar di lab sendiri.

### Gerbang 2 — Jaringan dan permintaan HTTP

- Uji konektivitas dan kirim permintaan HTTP ke endpoint in-scope dengan akun uji sendiri (Invoke-WebRequest/curl).
- Catat respons dan header yang relevan.

**Standar lulus:** Permintaan ke target in-scope tercatat dengan responsnya.

### Gerbang 3 — Otomasi kecil yang sopan

- Tulis skrip kecil untuk tugas berulang (mis. memeriksa sekumpulan header) dengan jeda antar-permintaan dan batas total — hanya bila program mengizinkan otomasi; huntr "Humans only" = tanpa skrip.
- Uji skrip di lab dulu sebelum menyentuh target.

**Standar lulus:** Skrip lolos uji lab; pasal otomasi program tercatat.

### Gerbang 4 — Disiplin tanpa perintah destruktif

- Jangan menjalankan perintah hapus/format/ubah registry di luar lab; bila ragu, uji di lab atau tanyakan ke Muse.
- Setiap perintah yang menyentuh target program dicatat di log.

**Standar lulus:** Tidak ada perintah destruktif di luar lab; semua perintah ke target tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| PowerShell / Command Prompt di mesin/lab Windows sendiri | Lingkungan kerja utama; semua perintah di mesin sendiri atau lab. |
| Cmdlet dasar (Get-ChildItem, Select-String, Get-Process, Test-NetConnection, Invoke-WebRequest) | Rujukan perintah harian; tanpa perintah destruktif di luar lab. |
| Skrip PowerShell kecil | Otomasi tugas berulang di lab; dengan jeda dan batas bila menyentuh target. |
| `~/workspace/catatan/log-bug-bounty.md` | Log perintah penting dan hasil kerja. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [powershell-windows-bounty — No. 39]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Kebijakan eksekusi PowerShell sering memblokir skrip — itu pengaman, bukan halangan yang harus dilompati dengan cara yang merusak. Jangan menjalankan skrip PowerShell dari sumber yang tidak tepercaya.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
