# Skill: Analisis Bypass 2FA / MFA — Pengujian Autentikasi Dua Faktor (Manipulasi Respons, Kebocoran OTP, Rate-Limit)

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 4 butir 25).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target memakai autentikasi dua faktor / multi-faktor (kode OTP via email/SMS/aplikasi authenticator, atau langkah verifikasi kedua setelah kata sandi) dan perlu dibuktikan apakah langkah kedua itu bisa dilewati atau dimanipulasi. Dipakai pada akun uji sendiri, setelah login tahap pertama berhasil. Jangan dipakai untuk membobol 2FA akun orang lain, dan jangan dipakai untuk menebak kode OTP akun orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan teknik 2FA di bawah |
| Pengerjaan | **A64 Web Application Tester** | Menguji alur 2FA aplikasi web dengan metode ini |
| Pengerjaan | **A66 API Security Tester** | Menguji endpoint verifikasi 2FA API dengan metode ini |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi umum Broken Authentication (login bisa dilewati) → skill `fondasi-kerentanan-web-api` Gerbang 1.4. Skill ini BUKAN definisi itu: skill ini adalah **metodologi bypass 2FA per teknik** (manipulasi respons, kebocoran OTP, rate-limit) yang tidak ada di skill fondasi.
- Alur reset kata sandi / pengambilalihan akun → skill `alur-reset-kata-sandi-ato` (2FA di sini hanya langkah verifikasi kedua, bukan reset kata sandi).
- Sesi multi-peran → skill `manajemen-sesi-multi-peran`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun uji adalah akun sendiri.** Pengujian 2FA hanya pada akun uji milik sendiri; jangan pernah menguji 2FA akun/kredensial orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.
13. **Jangan brute-force kode OTP akun orang lain.** Pengujian rate-limit (Teknik C) hanya pada kode OTP akun uji sendiri, dengan jumlah percobaan TERBATAS (maksimal belasan, bukan ratusan/ribuan), laju rendah, dan BERHENTI segera bila akun terkunci atau server menolak berulang. Bila target memakai OTP 6 digit acak, brute-force penuh secara matematis tidak layak dan TIDAK BOLEH dicoba — yang diuji hanya apakah rate-limit ADA atau TIDAK, bukan menebak kodenya sampai dapat.
14. **Kode OTP akun uji sendiri tidak boleh ditulis utuh di log.** Catat hanya "kode diterima/ditolak" + 2 karakter terakhir bila perlu membedakan percobaan.
15. **Jangan menonaktifkan 2FA akun lain atau mengubah pengaturan keamanan akun orang lain.** Pembuktian bypass hanya berupa sesi login yang terbentuk pada akun sendiri.

## Langkah + gerbang

### Gerbang 1 — Petakan alur 2FA + catat baseline

1. Login akun uji sendiri sampai langkah 2FA dan petakan alurnya: endpoint verifikasi kode (`/verify-otp`, `/api/2fa/verify`, atau sejenis), parameter yang dikirim (kode, token sesi sementara, user_id), respons sukses vs gagal, dan apa yang terjadi setelah sukses (token sesi penuh diterbitkan).
2. Catat baseline: kode BENAR → sukses + sesi penuh terbentuk; kode SALAH → gagal + tidak ada sesi penuh. Simpan raw request/response keduanya (kode disensor).
3. **Standar lulus:** endpoint verifikasi + parameter + respons sukses/gagal tercatat. Alur 2FA tidak ditemukan (target tidak pakai 2FA) = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji teknik satu per satu (satu teknik = satu putaran)

Uji berurutan pada akun uji sendiri; tiap teknik dicoba dari state bersih (login ulang sampai langkah 2FA).

#### Teknik A — Manipulasi respons (response manipulation)
Ubah respons verifikasi di sisi klien (mis. lewat proxy: ubah `{"success": false}` menjadi `{"success": true}`, atau ubah status/kode respons) lalu lanjutkan alur dan lihat apakah aplikasi memberi sesi penuh. Variasi: ubah parameter permintaan (`verified: false` → `true`, `otp_verified: 0` → `1`, hapus parameter kode) dan lihat apakah server percaya. **Terbukti bila:** sesi penuh terbentuk padahal kode yang dimasukkan salah/tidak ada — dibuktikan dengan endpoint profil yang mengembalikan data akun sendiri dalam sesi itu.

#### Teknik B — Kebocoran kode OTP di respons API
Periksa SEMUA respons selama alur 2FA (permintaan kirim kode, halaman verifikasi, respons error, header, body JSON): apakah kode OTP / token verifikasi ikut terkirim ke klien (di body, header, atau JavaScript)? Periksa juga apakah kode yang sama bisa dipakai ulang (replay) atau apakah kode untuk akun A bisa dipakai di akun B (keduanya akun sendiri). **Terbukti bila:** kode OTP terbaca dari respons API (bukan dari email/SMS yang memang jalurnya) lalu dipakai untuk login tanpa mengakses email/SMS; atau kode yang sama berhasil dipakai dua kali / lintas akun sendiri.

#### Teknik C — Rate-limit bypass pada kode verifikasi
Uji apakah ada batas percobaan kode salah: kirim kode salah berulang dalam jumlah TERBATAS (maksimal belasan percobaan, jeda antar percobaan, patuhi Aturan keras 13) dan amati apakah server mengunci/memblokir. Variasi yang diuji (satu per satu, dari state bersih): tambah header `X-Forwarded-For` berbeda, ganti IP/proxy (bila tersedia), ubah parameter pengenal (user_id/session) antar percobaan, atau minta kode baru lalu coba kode lama. **Terbukti bila:** server tidak pernah mengunci setelah percobaan salah berulang (tidak ada rate-limit sama sekali) ATAU salah satu variasi mereset hitungan percobaan sehingga percobaan salah bisa dilanjutkan tanpa batas. Sekadar "belasan percobaan salah belum mengunci" tanpa bukti variasi yang mereset hitungan = indikasi, bukan bukti — catat jumlah percobaan + batas yang teramati, jangan klaim lebih.

#### Teknik D — Lewati langkah (step skipping) & token sesi sementara
Coba akses halaman/endpoint setelah 2FA (dashboard, `/api/profile`) langsung dengan token sesi sementara dari langkah pertama (sebelum 2FA), tanpa menyelesaikan verifikasi. Coba juga memanggil endpoint verifikasi dengan parameter kosong / tanpa parameter kode. **Terbukti bila:** endpoint setelah 2FA mengembalikan data akun sendiri dengan token sementara yang belum terverifikasi, atau verifikasi kosong menghasilkan sesi penuh.

4. **Standar lulus per teknik:** ada hasil per teknik (berhasil/gagal + status + isi respons). Teknik tanpa hasil = belum diuji, jangan diklaim.

### Gerbang 3 — Buktikan sesi penuh terbentuk (read-only)

1. Untuk teknik yang berhasil di Gerbang 2, buktikan dampaknya: dengan sesi yang terbentuk lewat bypass, panggil endpoint profil dan endpoint baca milik akun sendiri — tunjukkan sesi itu benar-benar sesi login penuh (bukan halaman error / redirect login).
2. Jangan ubah data apa pun dengan sesi bypass itu; setelah pembuktian, logout dan hapus sesi.
3. **Standar lulus:** ada bukti sesi penuh (respons profil akun sendiri dalam sesi bypass) + langkah reproduksi persis. Sekadar "respons verifikasi bisa diubah di klien" tanpa sesi penuh yang terbentuk = belum terbukti (server mungkin tetap memeriksa di sisi server).

### Gerbang 4 — Serahkan ke skeptic gate

1. Kandidat Temuan diserahkan ke skill `skeptic-false-positive-eliminator`: uji ulang dengan sesi HTTP baru (fresh tokens), pastikan reproduksibel konsisten.
2. Gagal direproduksi = TOLAK, catat di log sebagai bukan temuan.
3. Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim.
4. **Standar lulus:** keputusan akhir tercatat di log dengan pasangan bukti request/response asli (kode OTP dan token disensor).

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri dengan 2FA aktif | Satu-satunya akun yang diuji; 2FA diaktifkan oleh pemilik akun (kita) sendiri. |
| Proxy pencegat (mis. Burp — lihat skill `mcp-burp-official`/`mcp-burp-ultra`) | Mengubah respons/permintaan verifikasi (Teknik A/D); hanya pada lalu lintas akun sendiri. |
| Akun uji kedua milik sendiri | Untuk uji lintas akun pada Teknik B (kode akun A dipakai di akun B — keduanya milik sendiri). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap teknik: alur 2FA, hasil, bukti sesi, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint verifikasi 2FA]
Alur 2FA: [endpoint + parameter + respons sukses/gagal baseline — kode disensor]
Teknik A (manipulasi respons): [berhasil/gagal + bukti sesi]
Teknik B (kebocoran OTP di respons): [berhasil/gagal + lokasi kebocoran + bukti]
Teknik C (rate-limit bypass): [jumlah percobaan salah + apakah terkunci + variasi yang mereset hitungan + bukti]
Teknik D (lewati langkah / token sementara): [berhasil/gagal + bukti]
Pembuktian sesi penuh: [respons profil dalam sesi bypass + langkah reproduksi]
Keputusan: [maju ke skeptic gate / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Manipulasi respons di sisi klien (Teknik A) sering gagal karena server tetap memeriksa di sisi server — hasil "gagal" adalah hasil valid, catat sebagai Aman.
- Teknik C tidak membuktikan kode bisa ditebak: OTP 6 digit acak tetap tidak layak ditebak meski tanpa rate-limit; yang dilaporkan adalah ketiadaan rate-limit itu sendiri (dengan dampak yang dinilai apa adanya, jangan dibesar-besarkan — lihat Aturan keras di skill fondasi: jangan membesar-besarkan severity).
- Bila target memakai kunci keamanan fisik (WebAuthn/FIDO2) sebagai faktor kedua, teknik di skill ini sebagian besar tidak berlaku — catat jenis faktor kedua di Gerbang 1 dan uji hanya yang relevan.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome, bukan trik autentikasi klasik — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
