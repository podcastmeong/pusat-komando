# Skill: Inspeksi Data Lokal Mobile — Inspeksi /data/data/<paket>/, SharedPreferences, SQLite, dan Keychain iOS: token/kata sandi yang tersimpan plaintext tanpa enkripsi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 47 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis inspeksi /data/data/<paket>/, SharedPreferences, SQLite, dan Keychain iOS: token/kata sandi yang tersimpan plaintext tanpa enkripsi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi/perangkat sendiri; tanpa data pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `adb-android-debug-bridge` (No. 44) — menarik file data lewat ADB
- `sandbox-mobile-root-jailbreak` (No. 43) — akses ke direktori data aplikasi
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi/perangkat sendiri; tanpa data pengguna lain.
12. **Catatan khusus kandidat:** Yang dicari adalah data sensitif yang tersimpan tanpa enkripsi — token sesi aktif, kata sandi, kunci API. Pengaturan tampilan yang tersimpan plaintext bukan temuan.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi dan perangkat yang diperiksa adalah milik sendiri atau target in-scope. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Aplikasi + perangkat tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan lokasi penyimpanan aplikasi

- Daftar lokasi data aplikasi sendiri: SharedPreferences, berkas SQLite, cache, dan (iOS) Keychain — catat jalur tiap lokasi.
- Jangan membuka data aplikasi lain di perangkat itu.

**Standar lulus:** Daftar lokasi penyimpanan tercatat.

### Gerbang 2 — Periksa token dan kredensial yang tersimpan

- Periksa tiap lokasi: apakah token sesi, kata sandi, atau kunci API tersimpan plaintext (tanpa enkripsi)?
- Catat JENIS data yang tersimpan plaintext dan lokasinya — jangan menyalin nilai token/kunci utuh ke log atau laporan; cukup catat jenis + lokasi + panjang/karakter awal yang disamarkan.

**Standar lulus:** Daftar data plaintext tercatat (jenis + lokasi, tanpa nilai utuh).

### Gerbang 3 — Nilai apakah data itu sensitif dan dapat dipakai

- Nilai: apakah data plaintext itu cukup untuk mengakses akun (token sesi aktif) atau hanya data non-sensitif (pengaturan tampilan)?
- Bila token aktif tersimpan plaintext, buktikan dengan memakai token itu HANYA pada akun sendiri untuk mengakses data sendiri — lalu segera cabut/putar token itu.

**Standar lulus:** Penilaian sensitivitas tercatat; token yang dipakai untuk bukti segera dicabut.

### Gerbang 4 — Serahkan ke triase

- Tulis lokasi + jenis data + dampak (tanpa nilai token utuh) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Temuan tercatat tanpa nilai sensitif utuh + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator milik sendiri (di-root bila perlu) | Satu-satunya perangkat yang diperiksa. |
| ADB / alat berkas perangkat | Menarik file SharedPreferences, SQLite, dan berkas data aplikasi sendiri. |
| Pembaca SQLite + penampil teks | Membaca isi basis data dan preferensi aplikasi sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log berkas yang diperiksa dan temuan — tanpa menyalin token utuh. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [inspeksi-data-lokal-mobile — No. 47]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jangan pernah menyalin token atau kata sandi utuh ke log, laporan, atau chat. Bila token sendiri dipakai untuk bukti, cabut/putar segera setelah bukti didapat.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
