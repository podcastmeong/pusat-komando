# Skill: Dekompilasi Aplikasi Mobile — Ekstrak Endpoint & Secret dari APK/IPA

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 18. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat program bounty in-scope mencakup aplikasi mobile (Android APK / iOS IPA) dan aplikasi itu harus dibedah untuk mengekstrak endpoint API, hardcoded keys, dan logika bisnis — sebelum pengujian apa pun. Dipakai pada tahap recon teknis; hasilnya masuk ke indeks aset (`pemetaan-permukaan-serangan`). Bukan untuk bounty agen AI — ini teknik web/API klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Mendapatkan salinan aplikasi yang sah, mendekompilasi, mencatat temuan |
| Audit | **A60 Security Auditor** | Memvalidasi temuan sebelum masuk indeks (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Putuskan aplikasi mana yang dibedah dan kapan temuan masuk indeks |

## Sudah tercakup (jangan diduplikat)

- **Analisis biner umum** sudah disinggung sebagai tool di `mcp-security-hub` (Ghidra dkk.) — itu daftar tool; skill ini adalah WORKFLOW khusus aplikasi mobile (APK/IPA, manifest, resource, kode aplikasi), bukan analisis biner sembarang.
- **Analisis file JS aplikasi web** ada di `analisis-statis-js` — skill itu untuk JS yang dimuat browser; skill ini untuk kode aplikasi mobile (DEX/Swift/Obj-C). Jangan campur keduanya.
- **Inventaris endpoint hasil bedah** masuk ke `pemetaan-permukaan-serangan` — skill ini menyerahkan hasilnya ke sana, bukan menggantikan indeksnya.
- **Pengujian endpoint hasil dekompilasi** BUKAN bagian skill ini — itu lewat `rekonstruksi-iterasi-payload` setelah endpoint masuk indeks.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja) — DAN aplikasi mobilenya harus secara tertulis in-scope di aturan program. Aplikasi mobile yang tidak disebut in-scope = jangan dibedah.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Dekompilasi dilakukan lokal pada salinan aplikasi; tidak ada serangan jaringan di skill ini.
4. **Tanpa payload di permukaan publik.** Dekompilasi hanya MEMBACA — tidak mengirim payload, tidak mengubah/menghapus data.
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Temuan dekompilasi bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Aplikasi hanya dari sumber yang sah.** Salinan APK/IPA HANYA dari toko resmi (Google Play / App Store) dengan akun sendiri, atau dari program bounty itu sendiri (bila program menyediakannya). JANGAN mengunduh APK dari situs pihak ketiga, JANGAN membedah aplikasi hasil curian/bocoran, dan JANGAN mendistribusikan ulang salinan aplikasi.
10. **Secret yang ditemukan DISENSOR di log (`[REDACTED]`) dan TIDAK dipakai untuk mengakses apa pun** — hanya dicatat sebagai temuan pemetaan (jenis secret + lokasi file). Memakai kunci orang lain untuk mengakses layanan = pelanggaran.
11. **Jangan membedah aplikasi orang lain di luar program.** Bila aplikasi ternyata bukan milik target in-scope (mis. SDK pihak ketiga di dalam aplikasi), catat sebagai pihak ketiga dan jangan bedah lebih dalam tanpa persetujuan Muse.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan aplikasi mobile tertulis in-scope di aturan program (baca halaman scope, catat URL + tanggal cek) dan programnya adalah program web/API klasik.
2. Pastikan salinan aplikasi bisa didapat dari sumber sah (toko resmi / program) — bila tidak bisa, tulis "tidak dapat diperoleh secara sah" dan STOP.
3. **Standar lulus:** scope tertulis; sumber sah tercatat. Satu gagal = STOP, jangan lanjut.

### Gerbang 1 — Dapatkan + simpan salinan

1. Unduh/install aplikasi dari toko resmi dengan akun sendiri; ambil salinan APK (Android) atau IPA (iOS) ke folder kerja lokal (satu folder per aplikasi + versi + tanggal). Catat nama aplikasi, versi, dan sumber unduhan.
2. **Standar lulus:** salinan tersimpan lokal dengan versi tercatat; tidak ada salinan dari situs pihak ketiga. Tanpa versi tercatat, jangan lanjut — temuan tanpa versi tidak bisa direproduksi.

### Gerbang 2 — Uraikan paket (tanpa menjalankan kode berbahaya)

1. Android: uraikan APK (mis. dengan apktool — pilih tool yang tersedia) menjadi manifest, resource, dan kode DEX; lalu ubah DEX menjadi kode yang bisa dibaca (mis. dengan jadx).
2. iOS: uraikan IPA (arsip zip) menjadi app bundle; bedah file konfigurasi (Info.plist), resource, dan string di dalam biner.
3. **Standar lulus:** manifest/konfigurasi terbaca (nama paket, izin, activity/service yang didaftarkan); kode berhasil diuraikan atau, bila gagal, kegagalannya tercatat dengan alasannya. Jangan menjalankan kode aplikasi hasil uraian — hanya dibaca.

### Gerbang 3 — Ekstrak endpoint, secret, dan logika bisnis

1. Cari secara sistematis di hasil uraian: URL dasar API + path endpoint, kunci/secret yang ter-hardcode, skema deep link/URL scheme, izin + komponen yang diekspor, dan logika bisnis yang relevan (cek peran di sisi klien, validasi harga/kuantitas di klien, token yang disimpan).
2. Untuk tiap temuan catat: file + lokasi, jenis temuan, dan nilai persisnya (kecuali secret — sensor jadi `[REDACTED]`).
3. Bedakan: endpoint yang TERAMATI dipakai aplikasi (cocok dengan lalu lintas saat aplikasi dipakai sebagai pengguna asli) vs endpoint yang HANYA ADA DI KODE (belum teramati).
4. **Standar lulus:** tiap temuan punya file + lokasi; secret tersensor; tiap endpoint punya status TERAMATI/HANYA DI KODE. Temuan tanpa lokasi = belum dicatat.

### Gerbang 4 — Serahkan ke indeks + audit

1. Serahkan daftar endpoint + temuan ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`), dengan catatan otorisasi tiap endpoint (bila belum diketahui, tulis "otorisasi belum diketahui" dan entri = BELUM DIPETAKAN).
2. A60 mengaudit: tiap temuan bisa dilacak ke file hasil uraian; secret tersensor; tidak ada salinan dari sumber tidak sah.
3. **Standar lulus:** audit A60 lolos; indeks diperbarui; entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji.

## Alat

| Alat | Cara pakai |
|---|---|
| apktool + jadx (Android — pilih yang tersedia) | Uraikan APK → manifest/resource/DEX → kode terbaca. Ambil cara pakai dari dokumentasi resminya, jangan mengarang flag. |
| Tool uraian IPA (unzip + pemeriksa plist — pilih yang tersedia) | Uraikan IPA → app bundle → Info.plist + string biner. |
| Toko resmi (Google Play / App Store) | Satu-satunya sumber salinan aplikasi (selain dari program itu sendiri). |
| `mcp-security-hub` | Pembanding: analisis biner (Ghidra) bila kode native perlu dibaca lebih dalam. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi dekompilasi. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Dekompilasi aplikasi mobile — <program/aplikasi versi> — <tanggal>
- Sumber salinan: <toko resmi/program> | versi: <...>
- Alat: <apktool/jadx/... + versi>
- Temuan: <n> endpoint, <n> secret [REDACTED], <n> deep link, <n> logika bisnis
- Per temuan: <file:lokasi> | <jenis> | <nilai> | <status: TERAMATI/HANYA DI KODE>
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; dekompilasi dilakukan lokal pada salinan aplikasi.

### Websites

- Dokumentasi apktool (apktool.org) dan jadx (github.com/skylot/jadx) — cara uraikan APK.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila aplikasi memakai obfuscation berat (nama kelas/metode acak): prioritaskan string URL dan file konfigurasi (manifest/plist) yang tidak ter-obfuscate; catat bagian yang tidak terbaca sebagai "belum terpetakan".
- Bila tidak ada salinan sah yang bisa diperoleh (mis. iOS tanpa akses IPA): catat sebagai keterbatasan, andalkan pengamatan lalu lintas aplikasi sebagai pengguna asli lewat proxy (`mcp-burp-official`) — jangan mengunduh dari situs pihak ketiga.
- Bila aplikasi ternyata hanya membungkus website (WebView): pakai `crawling-browser-headless` + `analisis-statis-js` untuk bagian webnya, bukan dekompilasi.
