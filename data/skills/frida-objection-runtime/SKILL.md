# Skill: Frida & Objection — Instrumentasi Runtime — Instrumentasi runtime Frida & Objection: menyuntikkan JavaScript ke proses berjalan, memodifikasi fungsi real-time (mis. lewati cek root/biometrik).

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 45 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis instrumentasi runtime Frida & Objection: menyuntikkan JavaScript ke proses berjalan, memodifikasi fungsi real-time (mis. lewati cek root/biometrik). Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi sendiri / target in-scope; lab sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `pipeline-redteam-apk` — Frida disebut di alur pipeline; skill ini adalah skill Frida/Objection khusus
- `bypass-ssl-pinning` (No. 46) — bypass pinning memakai skrip Frida
- `bypass-deteksi-root-magisk` — bypass deteksi root (pendalaman)
- `owasp-mobile-top-10` (No. 48) — kerangka uji mobile
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi sendiri / target in-scope; lab sendiri.
12. **Catatan khusus kandidat:** Frida mengaitkan fungsi saat aplikasi berjalan — skrip pengamat dulu sebelum skrip pengubah, satu fungsi per uji, agar penyebab perubahan jelas.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi yang diinstrumentasi adalah aplikasi sendiri atau target in-scope, dan perangkatnya milik sendiri. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Aplikasi + perangkat tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Pasang Frida di perangkat sendiri

- Pasang frida-server yang cocok dengan arsitektur perangkat sendiri; verifikasi Frida melihat proses aplikasi uji.
- Jangan memasang frida-server di perangkat orang lain.

**Standar lulus:** Frida terpasang dan melihat proses aplikasi uji.

### Gerbang 2 — Amati fungsi tanpa mengubahnya dulu

- Tulis skrip pengamat (observer) yang hanya mencatat pemanggilan fungsi dan argumennya — tanpa mengubah perilaku aplikasi.
- Catat fungsi menarik: cek root, cek biometrik, validasi sertifikat, dan penyimpanan token.

**Standar lulus:** Daftar fungsi menarik tercatat dari pengamatan pasif.

### Gerbang 3 — Ubah perilaku fungsi secara minimal di lab

- Ubah SATU fungsi per uji (mis. fungsi cek root mengembalikan 'tidak di-root') pada aplikasi sendiri dan amati apakah perilaku aplikasi berubah seperti hipotesis.
- Jangan mengubah fungsi yang memproses dana, mengirim data, atau mengubah data pengguna lain.

**Standar lulus:** Perubahan perilaku tercatat per fungsi; fungsi dana/data tidak disentuh.

### Gerbang 4 — Buktikan dampak + serahkan ke triase

- Tulis fungsi apa yang diubah dan dampaknya (mis. cek root dilewati sehingga fitur yang semestinya terkunci terbuka) lalu serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Fungsi + dampak tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator milik sendiri (di-root bila perlu) | Satu-satunya perangkat tempat Frida berjalan. |
| Frida + Objection (versi resmi) | Server Frida di perangkat; skrip JavaScript untuk hooking fungsi. |
| Aplikasi sendiri / target in-scope | Satu-satunya aplikasi yang diinstrumentasi. |
| `~/workspace/catatan/log-bug-bounty.md` | Log skrip, fungsi yang di-hook, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [frida-objection-runtime — No. 45]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Skrip Frida dari sumber tidak tepercaya bisa berbahaya — tulis skrip sendiri atau telaah tiap baris skrip yang dipakai. Jangan memakai Frida untuk melewati pembayaran, lisensi, atau autentikasi pengguna lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
