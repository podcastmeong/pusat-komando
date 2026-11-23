# Skill: Jalur Belajar TryHackMe — TryHackMe (Pre-Security & Jr Penetration Tester): konsep jaringan dari nol + simulasi interaktif di browser.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 55 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis tryHackMe (Pre-Security & Jr Penetration Tester): konsep jaringan dari nol + simulasi interaktif di browser. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Platform latihan; tanpa target nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `lab-hack-the-box` / `lab-portswigger-academy` — platform latihan lain
- `pemetaan-jaringan-osi-tcpip` — konsep jaringan yang dipelajari di TryHackMe
- `terminal-linux-kali` (No. 38) — perintah yang dipakai di lab TryHackMe
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
11. **Scope guard kandidat ini (WAJIB):** Platform latihan; tanpa target nyata.
12. **Catatan khusus kandidat:** TryHackMe adalah kurikulum belajar, bukan tempat berburu: nilai jalur ini adalah konsep jaringan dan alur pengujian yang dipelajari dari nol sampai bisa.

## Langkah + gerbang

### Gerbang 0 — Tegaskan: platform latihan

- TryHackMe HANYA latihan. Room dan mesinnya adalah target latihan; teknik yang dipelajari baru dipakai ke target program lewat skill yang sesuai dan setelah cek scope.
- Catat batas ini di log.

**Standar lulus:** Batas latihan tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Selesaikan jalur Pre-Security

- Pelajari konsep dasar: jaringan, web, Linux, dan keamanan — catat konsep yang baru dipahami tiap room.

**Standar lulus:** Ringkasan Pre-Security tercatat.

### Gerbang 2 — Selesaikan jalur Jr Penetration Tester

- Pelajari alur pengujian: enumerasi, eksploitasi dasar, dan privesc di mesin latihan; catat pola tiap room.

**Standar lulus:** Ringkasan Jr Penetration Tester tercatat.

### Gerbang 3 — Petakan pola ke skill bounty

- Untuk tiap pola yang dikuasai, tulis skill bounty mana yang memakai pola itu; pola tanpa skill padanan dicatat sebagai usulan.

**Standar lulus:** Pemetaan pola → skill tercatat.

### Gerbang 4 — Dokumentasikan pelajaran

- Tulis ringkasan pelajaran dan rencana latihan berikutnya di log sebagai bekal sebelum menguji target nyata.

**Standar lulus:** Ringkasan pelajaran tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun TryHackMe sendiri (gratis) | Akun latihan milik sendiri. |
| Browser + mesin lab/VM TryHackMe | Ruang latihan yang disediakan platform; tanpa target di luar platform. |
| Catatan belajar sendiri | Ringkasan tiap jalur/room yang diselesaikan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log jalur yang diselesaikan dan pola yang dipelajari. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [jalur-belajar-tryhackme — No. 55]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jangan memakai mesin TryHackMe untuk menguji target di luar platform, dan jangan mengklaim penyelesaian room sebagai temuan bounty.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
