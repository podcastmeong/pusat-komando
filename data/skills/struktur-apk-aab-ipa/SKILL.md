# Skill: Struktur APK / AAB / IPA — Struktur APK/AAB Android (AndroidManifest.xml, DEX/Dalvik, aset) dan IPA iOS — peta isi aplikasi sebelum dibedah.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 42 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis struktur APK/AAB Android (AndroidManifest.xml, DEX/Dalvik, aset) dan IPA iOS — peta isi aplikasi sebelum dibedah. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi sendiri / target in-scope.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `dekompilasi-aplikasi-mobile` — dekompilasi APK (langkah setelah struktur dipetakan)
- `pipeline-redteam-apk` — alur red-team APK (skill ini mendalami langkah pemetaan strukturnya)
- `owasp-mobile-top-10` (No. 48) — kerangka uji mobile
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi sendiri / target in-scope.
12. **Catatan khusus kandidat:** Peta struktur adalah langkah pertama sebelum dekompilasi mendalam: manifest memberi tahu permukaan aplikasi tanpa perlu membaca seluruh kode.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi yang dibedah adalah aplikasi sendiri atau aplikasi target in-scope; membedah aplikasi orang lain di luar program dilarang.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Aplikasi yang dibedah tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan isi paket

- Uraikan paket: manifest, file DEX/Dalvik, aset, resource, dan pustaka; catat versi, izin yang diminta, dan komponen yang diekspor.
- Jangan mengubah isi paket pada tahap ini — hanya membaca.

**Standar lulus:** Peta isi paket tercatat (manifest + komponen + izin).

### Gerbang 2 — Inventarisasi permukaan dari manifest

- Dari manifest, daftar: Activity/Service/Receiver/Provider yang diekspor, deep link yang didaftarkan, dan izin berbahaya yang diminta.
- Tiap permukaan dicatat sebagai hipotesis uji (lihat No. 98 komponen terekspos bila relevan).

**Standar lulus:** Daftar permukaan dari manifest tercatat.

### Gerbang 3 — Lacak secret dan endpoint di dalam paket

- Cari string menarik di dalam paket (URL API, kunci, token) — hanya untuk dicatat sebagai hipotesis, tanpa memakai kunci/token itu di luar PoC.
- Bila menemukan kredensial, jangan menggunakannya untuk mengakses layanan lain; catat keberadaannya saja.

**Standar lulus:** Daftar string menarik tercatat; tidak ada kredensial yang dipakai.

### Gerbang 4 — Serahkan hipotesis ke skill uji

- Teruskan tiap hipotesis ke skill uji yang sesuai (Frida No. 45, SSL pinning No. 46, data lokal No. 47) atau ke A60 audit → triase bila sudah cukup bukti.

**Standar lulus:** Hipotesis diteruskan + keputusan tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| APK/AAB/IPA milik sendiri atau target in-scope | Satu-satunya berkas aplikasi yang dibedah. |
| Alat pembaca arsip + penampil manifest (jadx/apktool dan sejenisnya) | Memetakan isi paket tanpa mengubahnya. |
| Perangkat/emulator sendiri | Tempat aplikasi diuji setelah strukturnya dipetakan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log struktur yang ditemukan dan hipotesis. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [struktur-apk-aab-ipa — No. 42]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- APK/AAB/IPA yang diunduh dari sumber tidak resmi bisa mengandung malware — hanya bedah paket dari sumber resmi program atau aplikasi sendiri. Jangan mendistribusikan ulang isi paket yang dibedah.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
