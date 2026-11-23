# Skill: Terminal Linux (Kali) — Terminal Linux (Kali/Parrot): perintah dasar, manajemen file, proses, jaringan, dan piping untuk kerja bounty.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 38 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis terminal Linux (Kali/Parrot): perintah dasar, manajemen file, proses, jaringan, dan piping untuk kerja bounty. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Pengetahuan dasar; tanpa perintah destruktif di luar lab.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `otomasi-python-bash-bounty` (No. 34) — skrip Bash di atas perintah dasar ini
- `powershell-windows-bounty` (No. 39) — padanan Windows
- `jalur-belajar-tryhackme` — latihan konsep jaringan dari nol
- `terminal-linux-kali` adalah fondasi — skill lain mengasumsikan perintah di sini sudah dikuasai
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
12. **Catatan khusus kandidat:** Skill dasar ini melayani SEMUA program karena terminal adalah alat kerja, bukan teknik serangan — tetapi perintah yang sama bisa destruktif bila dijalankan di tempat yang salah; disiplin lokasi adalah isi skill ini.

## Langkah + gerbang

### Gerbang 0 — Kenali lingkungan kerja

- Periksa distribusi, pengguna saat ini, dan direktori kerja; pastikan bekerja di mesin/lab sendiri, bukan di sistem target.
- Catat lingkungan kerja di log.

**Standar lulus:** Lingkungan kerja tercatat; tidak ada perintah yang menyentuh sistem orang lain.

### Gerbang 1 — Manajemen file dan pencarian

- Kuasai navigasi direktori, membaca file, mencari teks (grep), dan menemukan file (find) — semua read-only terhadap target.
- Latih pola: cari file konfigurasi di lab sendiri, baca isinya, catat yang relevan.

**Standar lulus:** Perintah file + pencarian berjalan lancar di lab sendiri.

### Gerbang 2 — Proses dan jaringan

- Periksa proses yang berjalan, port yang mendengarkan, dan koneksi aktif di mesin sendiri; pahami apa yang normal sebelum menilai target.
- Gunakan curl untuk menguji endpoint in-scope dengan akun uji sendiri.

**Standar lulus:** Proses + port mesin sendiri terpetakan; curl ke target in-scope tercatat.

### Gerbang 3 — Piping menjadi alur kerja

- Gabungkan perintah dengan pipe (mis. keluaran enumerasi → grep → simpan ke file log) agar hasil kerja tersimpan dan dapat diulang.
- Simpan alur yang sering dipakai sebagai skrip kecil (lihat No. 34) — dengan jeda dan batas bila menyentuh target.

**Standar lulus:** Alur kerja tersimpan dan dapat diulang dari log.

### Gerbang 4 — Disiplin tanpa perintah destruktif

- Hafalkan daftar larangan: jangan menjalankan perintah hapus/format/menulis di luar lab; bila ragu, jalankan dulu di lab atau tanyakan ke Muse.
- Setiap perintah yang menyentuh target program dicatat di log beserta alasannya.

**Standar lulus:** Tidak ada perintah destruktif di luar lab; semua perintah ke target tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Terminal Linux (Kali/Parrot) di mesin/lab sendiri | Lingkungan kerja utama; semua perintah dijalankan di mesin sendiri atau lab. |
| Perintah dasar (ls, cd, cat, grep, find, ps, netstat/ss, curl) | Rujukan perintah harian; tanpa perintah destruktif di luar lab. |
| Piping dan redirect (|, >, >>) | Menggabungkan perintah kecil menjadi alur kerja. |
| `~/workspace/catatan/log-bug-bounty.md` | Log perintah penting dan hasil kerja. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [terminal-linux-kali — No. 38]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Perintah destruktif (hapus massal, format, penulisan ke file sistem) tidak pernah menjadi bagian dari pengujian bounty. Bila sebuah perintah tidak dipahami sepenuhnya, jangan menjalankannya terhadap target — uji dulu di lab.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
