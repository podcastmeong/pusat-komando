# Skill: ADB — Android Debug Bridge — ADB: shell perangkat, instal APK, tarik/dorong file, logcat, dan perintah dasar interaksi Android lewat terminal.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 44 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis aDB: shell perangkat, instal APK, tarik/dorong file, logcat, dan perintah dasar interaksi Android lewat terminal. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya perangkat/emulator sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `struktur-apk-aab-ipa` (No. 42) — peta isi APK yang dipasang lewat ADB
- `frida-objection-runtime` (No. 45) — instrumentasi runtime setelah perangkat terhubung ADB
- `inspeksi-data-lokal-mobile` (No. 47) — membaca data aplikasi lewat ADB
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
11. **Scope guard kandidat ini (WAJIB):** Hanya perangkat/emulator sendiri.
12. **Catatan khusus kandidat:** ADB memberi akses shell penuh ke perangkat — kekuatan itu hanya dipakai pada perangkat sendiri; menghubungkan ADB ke perangkat orang lain adalah akses tanpa izin.

## Langkah + gerbang

### Gerbang 0 — Cek perangkat dulu

- Pastikan perangkat yang terhubung adalah milik sendiri (periksa serial + model); jangan menghubungkan ADB ke perangkat orang lain.
- Catat perangkat di log.

**Standar lulus:** Perangkat sendiri terverifikasi + tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Hubungkan dan verifikasi akses

- Aktifkan USB debugging di perangkat sendiri, hubungkan, dan verifikasi perangkat terdaftar (adb devices) serta shell merespons.
- Bila perangkat meminta otorisasi, setujui hanya di perangkat sendiri.

**Standar lulus:** Perangkat terdaftar dan shell merespons.

### Gerbang 2 — Instal dan kelola APK uji

- Pasang APK aplikasi sendiri / target in-scope lewat ADB; catat paket yang terpasang dan versinya.
- Jangan memasang APK dari sumber tidak tepercaya.

**Standar lulus:** APK uji terpasang + tercatat.

### Gerbang 3 — Tarik file dan baca logcat

- Tarik file data aplikasi sendiri (lihat No. 47) dan baca logcat untuk mencari kebocoran informasi — hanya aplikasi sendiri / target in-scope.
- Jangan menarik file milik aplikasi lain di perangkat itu.

**Standar lulus:** File + log yang relevan tercatat; hanya aplikasi sendiri yang diperiksa.

### Gerbang 4 — Putuskan sambungan dengan aman

- Matikan USB debugging bila tidak dipakai; cabut perangkat; catat hasil pengujian di log.

**Standar lulus:** Perangkat diputus + USB debugging dimatikan + log lengkap.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator Android milik sendiri + kabel/USB debugging | Satu-satunya perangkat yang dihubungkan; aktifkan USB debugging hanya di perangkat sendiri. |
| ADB (platform-tools resmi) | Perintah shell, instal, tarik/dorong file, dan logcat. |
| Terminal di mesin sendiri | Tempat perintah ADB dijalankan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log perangkat, perintah, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [adb-android-debug-bridge — No. 44]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Logcat bisa berisi token dan data sensitif aplikasi sendiri — jangan menyalin logcat mentah ke laporan; kutip hanya baris yang membuktikan temuan dan samarkan token.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
