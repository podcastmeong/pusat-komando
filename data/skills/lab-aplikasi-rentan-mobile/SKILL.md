# Skill: Lab Aplikasi Rentan Mobile — Lab aplikasi rentan: DIVA, InsecureBankv2, dan OWASP MASTG Hacking Playground di emulator untuk latihan legal.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 49 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis lab aplikasi rentan: DIVA, InsecureBankv2, dan OWASP MASTG Hacking Playground di emulator untuk latihan legal. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Lab saja; aplikasi latihan, bukan target nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `panduan-mastg` (No. 50) — panduan yang dipakai bersama lab ini
- `lab-injuredandroid-ctf`, `lab-uncrackable-android`, `lab-mobilehackinglab` — lab mobile lain
- `owasp-mobile-top-10` (No. 48) — kerangka kelas yang dilatih di lab
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
11. **Scope guard kandidat ini (WAJIB):** Lab saja; aplikasi latihan, bukan target nyata.
12. **Catatan khusus kandidat:** Lab rentan adalah tempat belajar yang aman: DIVA, InsecureBankv2, dan MASTG Hacking Playground sengaja dibuat rentan agar pola kerentanan bisa dipelajari tanpa melanggar scope.

## Langkah + gerbang

### Gerbang 0 — Tegaskan: lab saja

- Lab ini HANYA latihan. Aplikasi lab bukan target nyata; teknik yang dipelajari di sini baru dipakai ke target program lewat skill uji yang sesuai dan setelah cek scope.
- Catat batas ini di log.

**Standar lulus:** Batas lab-saja tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan emulator + aplikasi lab

- Pasang emulator, unduh aplikasi lab dari sumber resmi, pasang lewat ADB, dan verifikasi aplikasi lab berjalan.
- Catat versi emulator + aplikasi lab.

**Standar lulus:** Emulator + aplikasi lab berjalan.

### Gerbang 2 — Selesaikan tantangan satu per satu

- Pilih satu tantangan (mis. satu kerentanan di DIVA); baca petunjuk tantangannya, uji dengan alat lab, dan catat langkah + pola yang berhasil.
- Satu tantangan per putaran; jangan melompat sebelum pola tantangan itu dipahami.

**Standar lulus:** Tiap tantangan tercatat (langkah + pola + hasil).

### Gerbang 3 — Petakan pola lab ke skill nyata

- Untuk tiap pola yang dikuasai, tulis skill bounty mana yang memakai pola itu (mis. pola penyimpanan tidak aman → No. 47).
- Pola yang belum punya skill padanannya dicatat sebagai usulan, bukan dipakai mentah.

**Standar lulus:** Pemetaan pola → skill tercatat.

### Gerbang 4 — Dokumentasikan pelajaran

- Tulis ringkasan pelajaran (pola yang dikuasai, kesalahan yang dibuat, waktu yang dipakai) di log sebagai bekal sebelum menguji target nyata.

**Standar lulus:** Ringkasan pelajaran tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Emulator Android milik sendiri (Android Studio/Genymotion) | Tempat lab berjalan; tanpa perangkat nyata orang lain. |
| Aplikasi lab resmi: DIVA, InsecureBankv2, OWASP MASTG Hacking Playground | Unduh hanya dari sumber resmi proyeknya. |
| ADB + alat analisis (jadx, Frida) | Alat yang dipakai di dalam lab. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tantangan lab yang diselesaikan dan pelajaran. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [lab-aplikasi-rentan-mobile — No. 49]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jangan memakai kredensial atau data apa pun dari aplikasi lab di luar lab. Jangan mengklaim temuan lab sebagai temuan bounty — temuan bounty hanya dari target program in-scope.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
