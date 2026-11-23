# Skill: Pengujian WebView Mobile — Kerentanan WebView aplikasi mobile: JavaScript bridge, akses file, dan interaksi WebView–aplikasi native.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 57 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis kerentanan WebView aplikasi mobile: JavaScript bridge, akses file, dan interaksi WebView–aplikasi native. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi sendiri / target in-scope.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `struktur-apk-aab-ipa` (No. 42) — menemukan WebView dari struktur aplikasi
- `frida-objection-runtime` (No. 45) — mengamati interaksi WebView–native saat berjalan
- `owasp-mobile-top-10` (No. 48) — kerangka uji mobile
- `panduan-mastg` (No. 50) — panduan pengujian mobile
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi sendiri / target in-scope.
12. **Catatan khusus kandidat:** WebView adalah browser di dalam aplikasi: bridge JavaScript yang diekspos ke halaman web mana pun dan akses file yang diizinkan adalah dua pola celah utamanya.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi yang diuji adalah aplikasi sendiri atau target in-scope. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Aplikasi tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Temukan WebView dan konfigurasinya

- Dari struktur aplikasi dan perilaku, catat WebView yang dipakai, apakah JavaScript diaktifkan, apakah bridge JavaScript diekspos ke halaman web, dan apakah akses file diizinkan.
- Catat tiap pengaturan beserta lokasinya di kode.

**Standar lulus:** Daftar WebView + konfigurasi tercatat.

### Gerbang 2 — Uji bridge JavaScript dari halaman canary

- Muat halaman canary milik sendiri di WebView aplikasi sendiri dan periksa apakah bridge JavaScript dapat dipanggil dari halaman itu (mis. membaca nilai canary dari sisi native).
- Jangan memuat halaman penyerang sungguhan; halaman canary milik sendiri saja.

**Standar lulus:** Hasil uji bridge tercatat (dapat dipanggil/tidak + apa yang terbaca).

### Gerbang 3 — Uji akses file dan skema dari WebView

- Periksa apakah WebView dapat membaca file lokal aplikasi sendiri atau memuat skema berbahaya (file://, intent://) — hanya file aplikasi sendiri.
- Bila akses file terbuka, buktikan dengan membaca file canary milik sendiri, bukan file sensitif.

**Standar lulus:** Hasil uji akses file/skema tercatat.

### Gerbang 4 — Serahkan ke triase

- Tulis konfigurasi WebView + bukti (bridge apa yang terekspos, file apa yang terbaca) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Konfigurasi + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator milik sendiri | Satu-satunya perangkat tempat aplikasi uji berjalan. |
| Aplikasi sendiri / target in-scope yang memakai WebView | Satu-satunya aplikasi yang diuji. |
| Proksi (Burp/ZAP) + sertifikat CA di perangkat sendiri | Mengamati lalu lintas WebView aplikasi sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log WebView yang ditemukan, konfigurasi, dan hasil uji. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-webview-mobile — No. 57]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Bridge yang hanya diekspos ke halaman tepercaya aplikasi sendiri (bukan ke halaman web umum) belum tentu celah — bukti harus menunjukkan halaman canary yang tidak tepercaya dapat memanggilnya.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
