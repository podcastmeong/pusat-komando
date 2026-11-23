# Skill: Pengujian Electron Desktop — Keamanan aplikasi desktop Electron: Node integration, context isolation, dan preload script sebagai permukaan serangan.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 58 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis keamanan aplikasi desktop Electron: Node integration, context isolation, dan preload script sebagai permukaan serangan. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya bila program mencantumkan aplikasi desktop.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `owasp-mobile-top-10` (No. 48) — kerangka uji (pendekatan per kelas, untuk mobile)
- `audit-kode-php` (No. 41) — audit kode (pendekatan audit, bahasa berbeda)
- `analisis-statis-js` — membaca kode JavaScript aplikasi Electron
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
11. **Scope guard kandidat ini (WAJIB):** Hanya bila program mencantumkan aplikasi desktop.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya bila program mencantumkan aplikasi desktop. Electron yang konfigurasinya aman (Node integration mati + context isolation aktif) bukan temuan walau memakai Electron.

## Langkah + gerbang

### Gerbang 0 — Cek pencantuman program dulu

- Baca pasal scope: aplikasi desktop HANYA diuji bila program secara eksplisit mencantumkan aplikasi desktop itu. Tanpa pencantuman = jangan diuji.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pencantuman program tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan konfigurasi Electron

- Periksa konfigurasi jendela aplikasi: Node integration (aktif/tidak), context isolation (aktif/tidak), sandbox, dan preload script yang dimuat.
- Catat tiap pengaturan beserta file sumbernya.

**Standar lulus:** Daftar konfigurasi tercatat.

### Gerbang 2 — Nilai kombinasi konfigurasi

- Nilai kombinasi yang berbahaya: Node integration aktif + context isolation mati adalah kombinasi klasik yang memberi halaman web akses Node; preload script yang mengekspos API berbahaya adalah pola kedua.
- Catat kombinasi + hipotesis dampaknya.

**Standar lulus:** Kombinasi berbahaya + hipotesis tercatat.

### Gerbang 3 — Buktikan eksekusi di aplikasi sendiri

- Buktikan hipotesis dengan halaman canary milik sendiri yang dimuat aplikasi uji: apakah skrip canary dapat memanggil API Node yang semestinya tidak tersedia?
- Jangan menjalankan perintah sistem yang merusak; bukti cukup berupa pembacaan nilai canary.

**Standar lulus:** Bukti eksekusi canary tercatat atau hipotesis ditutup.

### Gerbang 4 — Serahkan ke triase

- Tulis konfigurasi + bukti dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Konfigurasi + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Aplikasi desktop Electron target in-scope (bila dicantumkan program) | Satu-satunya aplikasi yang diuji; tanpa pencantuman program = jangan diuji. |
| Kode sumber / paket aplikasi (bila tersedia secara sah) | Satu-satunya kode yang diaudit. |
| Mesin lab sendiri (Windows/macOS/Linux) | Tempat aplikasi uji dijalankan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log konfigurasi, hipotesis, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-electron-desktop — No. 58]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak aplikasi Electron modern sudah mengaktifkan context isolation secara default — klaim 'Electron = rentan' tanpa memeriksa konfigurasi adalah klaim yang salah. Jangan menguji aplikasi desktop di luar program.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
