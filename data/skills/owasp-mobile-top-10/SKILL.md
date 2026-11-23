# Skill: OWASP Mobile Top 10 — Pemetaan OWASP Mobile Top 10 per kelas kerentanan (autentikasi lemah, kriptografi buruk, kebocoran data) sebagai kerangka uji mobile.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 48 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis pemetaan OWASP Mobile Top 10 per kelas kerentanan (autentikasi lemah, kriptografi buruk, kebocoran data) sebagai kerangka uji mobile. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi in-scope; tanpa data pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `panduan-mastg` (No. 50) — panduan pengujian mobile yang memuat Top 10 ini
- `struktur-apk-aab-ipa` (No. 42) — pemetaan struktur sebelum uji per kelas
- `frida-objection-runtime` (No. 45), `bypass-ssl-pinning` (No. 46), `inspeksi-data-lokal-mobile` (No. 47) — skill uji per kelas
- `lab-aplikasi-rentan-mobile` (No. 49) — lab untuk melatih tiap kelas
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi in-scope; tanpa data pengguna lain.
12. **Catatan khusus kandidat:** Top 10 adalah kerangka pemetaan, bukan temuan: tiap kelas harus dibuktikan dengan pengujian dari skill yang sesuai sebelum dilaporkan.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi yang diuji adalah aplikasi in-scope; catat program + aplikasi di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Program + aplikasi tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan Top 10 ke aplikasi target

- Untuk tiap kelas Top 10, tulis apakah kelas itu relevan untuk aplikasi target dan hipotesisnya (mis. autentikasi lemah → alur login apa yang diuji).
- Kelas yang tidak relevan dicatat alasannya, bukan diabaikan diam-diam.

**Standar lulus:** Matriks sepuluh kelas tercatat dengan hipotesis atau alasan tidak relevan.

### Gerbang 2 — Uji kelas demi kelas dengan skill yang sesuai

- Uji tiap kelas dengan skill yang sesuai (mis. kriptografi buruk → No. 47; komunikasi tidak aman → No. 46; autentikasi lemah → alur login akun sendiri).
- Satu kelas per putaran; catat hasil tiap kelas.

**Standar lulus:** Hasil tiap kelas tercatat dengan skill yang dipakai.

### Gerbang 3 — Kumpulkan temuan per kelas

- Kumpulkan kelas yang terbukti bermasalah; tiap temuan harus punya bukti dari skill ujinya, bukan hanya dari pemetaan.
- Kelas yang aman dicatat buktinya (pengujian apa yang menunjukkan aman).

**Standar lulus:** Daftar kelas bermasalah + bukti tercatat; kelas aman tercatat buktinya.

### Gerbang 4 — Serahkan ke triase

- Serahkan tiap temuan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim; satu laporan per temuan, bukan satu laporan untuk sepuluh kelas.

**Standar lulus:** Tiap temuan punya keputusan triase sendiri.

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar OWASP Mobile Top 10 (edisi terbaru) | Kerangka sepuluh kelas kerentanan mobile sebagai daftar periksa. |
| Aplikasi sendiri / target in-scope + perangkat/emulator sendiri | Satu-satunya aplikasi dan perangkat yang diuji. |
| Matriks pemetaan (kelas → hipotesis → skill uji → hasil) | Lembar kerja pemetaan tiap kelas ke pengujian nyata. |
| `~/workspace/catatan/log-bug-bounty.md` | Log pemetaan dan hasil tiap kelas. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [owasp-mobile-top-10 — No. 48]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Edisi OWASP Mobile Top 10 berubah dari waktu ke waktu — catat edisi yang dipakai di log agar pemetaan dapat ditelusuri. Jangan melaporkan 'aplikasi rentan terhadap Top 10' tanpa bukti per kelas.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
