# Skill: Deteksi CSRF — Ketiadaan Token Anti-CSRF / Cookie SameSite Lemah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 40 (CSRF Detection). Jangan klaim metode ini terbukti sampai ada satu aksi sensitif yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat target web klasik in-scope punya aksi sensitif yang mengubah state (ganti email/kata sandi, transfer, hapus data, ubah pengaturan) dan ada dugaan aksi itu bisa dipicu dari situs lain tanpa token anti-CSRF yang valid. Dipakai SETELAH `pemetaan-permukaan-serangan` menginventarisasi endpoint — skill ini menguji pertahanan CSRF tiap aksi sensitif, bukan menginventarisasi ulang.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menguji token + atribut cookie tiap aksi sensitif |
| Pengerjaan | **A54 Penguji Live** | Menjalankan PoC lintas-origin di browser milik sendiri |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Inventarisasi endpoint + otorisasi** → `pemetaan-permukaan-serangan` langkah 5. Skill ini menguji pertahanan CSRF endpoint itu.
- **CSRF pada alur login OAuth (parameter `state` tidak diperiksa)** → `perburuan-kerentanan-spesifik` (bagian OAuth/SSO). Skill ini untuk CSRF UMUM pada aksi sensitif aplikasi, bukan alur OAuth.
- **Pembuktian dampak umum + laporan triage-ready** → `triase-duplikat` + `laporan-abstrak`.
- **Gerbang false-positive akhir sebelum laporan** → `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan.
5. **Tanpa payload di permukaan publik.** Halaman PoC jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only sebisa mungkin: pilih aksi sensitif yang REVERSIBEL dan tidak merusak (mis. ganti nama tampilan/nilai preferensi milik sendiri, bukan hapus akun/data); JANGAN pernah menguji CSRF pada aksi hapus permanen atau transfer dana nyata — bila satu-satunya aksi sensitif bersifat destruktif, buktikan lewat permintaan yang DITOLAK/diubah ke nilai canary yang aman, atau serahkan ke Muse sebelum menguji.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik CSRF klasik.

## Yang dicari (definisi singkat)

- **Ketiadaan token anti-CSRF:** aksi state-changing (POST/PUT/DELETE, atau GET yang mengubah state) berhasil tanpa token anti-CSRF, atau token tidak divalidasi server (token kosong/salah/statis tetap diterima, token tidak terikat sesi).
- **Cookie SameSite lemah:** cookie sesi memakai `SameSite=None` (tanpa `Secure` lebih parah lagi) atau tidak mengatur `SameSite` sama sekali di server lama — sehingga browser mengirim cookie sesi pada permintaan lintas-situs dan CSRF menjadi mungkin. Catatan: browser modern memperlakukan cookie tanpa `SameSite` sebagai `Lax` secara default — jadi "tidak ada atribut SameSite" saja BUKAN bukti otomatis; yang menentukan adalah perilaku nyata di Langkah 3.
- **Pertahanan lain yang perlu dicatat:** validasi header `Origin`/`Referer` oleh server, dan header `fetch` kustom (mis. `X-Requested-With`) yang memaksa preflight CORS — bila server memeriksa salah satunya dengan benar, CSRF klasik bisa gagal walau tanpa token.
- **Bukan temuan (umumnya):** aksi yang hanya membaca data (GET tanpa efek samping), aksi yang memakai token Bearer di header `Authorization` (token itu tidak otomatis dikirim browser lintas-situs), dan aksi yang sudah dilindungi token anti-CSRF yang divalidasi dengan benar.

## Langkah + gerbang

### Langkah 1 — Inventarisasi aksi sensitif

Dari indeks `pemetaan-permukaan-serangan`, daftar aksi yang mengubah state milik pengguna: ganti email/kata sandi/nama, ubah pengaturan, kirim/transfer, buat/hapus konten. Untuk tiap aksi catat metode, endpoint, parameter, dan apakah butuh autentikasi. Pilih SATU aksi yang reversibel dan aman untuk PoC (lihat aturan keras 9).

**Standar lulus:** daftar aksi tertulis dengan metode + endpoint + reversibel/tidaknya; aksi destruktif ditandai "JANGAN diuji tanpa keputusan Muse".

### Langkah 2 — Uji token anti-CSRF

Untuk aksi terpilih, periksa: (a) apakah formulir/permintaan normal menyertakan token anti-CSRF; (b) ulangi permintaan TANPA token — apakah server tetap menjalankannya? (c) ulangi dengan token salah/statis/milik sesi lain — apakah diterima? (d) apakah token terikat ke sesi (token sesi A dipakai sesi B → ditolak?).

**Standar lulus:** hasil tiap varian tercatat (tanpa token / token salah / token sesi lain → diterima/ditolak). Bila token divalidasi benar = AMAN, tutup dengan buktinya.

### Langkah 3 — Periksa atribut cookie + pertahanan lain

Baca header `Set-Cookie` sesi: `SameSite` (None/Lax/Strict/tidak ada), `Secure`, `HttpOnly`. Catat juga apakah server memvalidasi `Origin`/`Referer` (kirim permintaan dengan `Origin` lain → ditolak?) dan apakah ada header kustom wajib.

**Standar lulus:** atribut cookie tercatat persis + hasil uji validasi Origin/Referer tercatat. Atribut saja bukan vonis — vonis datang dari Langkah 4.

### Langkah 4 — Buktikan dengan PoC lintas-origin di browser sendiri

Buat halaman PoC milik sendiri di origin canary (bukan origin target) yang secara otomatis mengirim permintaan aksi sensitif (form auto-submit / `fetch` dengan kredensial) memakai sesi login akun sendiri. Buka halaman itu di browser milik sendiri, lalu periksa apakah state akun sendiri benar-benar berubah ke nilai canary yang aman (mis. nama tampilan berubah menjadi nilai canary).

**Standar lulus (gerbang utama): tanpa perubahan state nyata pada akun sendiri lewat halaman origin lain = BELUM BERHASIL.** Token yang "kelihatan tidak ada" tanpa PoC, atau PoC yang diblokir browser/server, = GAGAL — catat kenapa gagal dan tutup. Setelah PoC berhasil, KEMBALIKAN state akun sendiri ke nilai semula dan catat pengembaliannya.

### Langkah 5 — Nilai dampak + tulis draf

Tulis aksi apa yang bisa dilakukan situs penyerang atas nama korban yang sedang login (aksi persis dari Langkah 4, bukan dugaan). Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (aksi + nilai yang berubah), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Ulangi permintaan tanpa token / token salah / Origin lain; baca `Set-Cookie` |
| Halaman PoC milik sendiri (origin canary) | Form auto-submit / `fetch` lintas-origin dengan kredensial sesi sendiri; hanya di lingkungan terkendali milik sendiri |
| Browser milik sendiri (`uji-live-browser`) | Tempat halaman PoC dijalankan dan perubahan state diperiksa |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua aksi + hasil uji token/cookie + bukti PoC + keputusan triase |

## Format output

Log setiap aksi ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Aksi sensitif: [METODE path — aksi + nilai canary yang diubah]
Token anti-CSRF: [ada/tidak — tanpa token: diterima/ditolak — token salah: diterima/ditolak]
Cookie sesi: [SameSite: ... | Secure: ... | HttpOnly: ...]
Validasi Origin/Referer: [ada/tidak — hasil uji]
Bukti PoC lintas-origin: [state akun sendiri berubah ke nilai canary lewat halaman origin lain — atau "TIDAK ADA"]
State dikembalikan: [ya — nilai semula ... / tidak perlu]
Dampak: [aksi apa yang bisa dilakukan situs lain atas nama korban]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Cookie tanpa atribut `SameSite` di browser modern diperlakukan sebagai `Lax` — jangan klaim "SameSite lemah" hanya dari ketiadaan atribut; buktikan lewat PoC Langkah 4.
- CSRF pada aksi GET yang mengubah state tetap CSRF — tapi banyak program menilainya lebih rendah bila aksinya sepele; nilai dampak apa adanya, jangan membesar-besarkan.
- Bila satu-satunya aksi sensitif bersifat destruktif (hapus akun, transfer dana), JANGAN uji PoC penuh — serahkan ke Muse untuk keputusan (aturan keras 9).

### Available connectors

Tidak ada konektor khusus untuk skill ini; permintaan HTTP dikirim dengan curl/klien HTTP dan PoC dijalankan di browser milik sendiri.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi target (alur fitur tempat aksi sensitif berada).

### Alternatives for better results

- Bila token anti-CSRF ada tapi tidak terikat sesi (token statis yang sama untuk semua pengguna), uji dengan token dari sesi lain milik sendiri — bila diterima, itu tetap celah walau token "ada".
- Bila PoC form auto-submit diblokir karena `SameSite=Lax` pada cookie, coba varian GET (bila aksi menerima GET) — `Lax` masih mengirim cookie pada navigasi GET tingkat atas; catat hasil tiap varian secara terpisah.
