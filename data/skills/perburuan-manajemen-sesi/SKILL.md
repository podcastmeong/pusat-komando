# Skill: Perburuan Manajemen Sesi — Siklus Hidup Sesi (Fixation, Invalidasi, Entropi, JWT sebagai Sesi)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 49, sumber: Claude-BugHunter `hunt-session`, 18 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai sesi berbasis cookie/token untuk menjaga status login pengguna.
- Ada sinyal: session ID tidak berubah setelah login, sesi lama tetap berlaku setelah logout/ganti kata sandi/ganti email, atau session ID tampak pendek/berpola.
- Dipakai pada akun uji sendiri; pengujian siklus hidup sesi selalu memakai dua akun uji milik sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Menguji siklus hidup sesi satu tahap per putaran |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Manipulasi JWT (alg none, secret lemah, JWK/JKU, key confusion, klaim tidak divalidasi) → skill `manipulasi-jwt`. Skill itu soal KRIPTOGRAFI token JWT. Skill ini soal SIKLUS HIDUP sesi secara menyeluruh — JWT di sini hanya satu varian (JWT yang dipakai sebagai sesi tanpa expiry/revocation).
- Mengelola banyak sesi multi-peran sebagai PERKAKAS pengujian (wadah sesi per peran, matriks hak akses) → skill `manajemen-sesi-multi-peran`. Skill itu adalah perkakas, bukan pengujian cacat sesi.
- Perbandingan hak akses lintas akun (diferensial respons) → skill `access-control-differential-analyst`.
- Rantai ATO menyeluruh → skill `perburuan-pengambilalihan-akun` (sesi di sini adalah jalur 3 di taksonomi itu).
- Reset kata sandi / token reset → skill `alur-reset-kata-sandi-ato`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh alur sesi berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri (minimal dua akun: Akun A dan Akun B). Jangan pernah menguji sesi, fixation, atau invalidasi terhadap akun orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Khusus sesi: pembuktian cukup sampai sesi akun uji lain dipakai/diperiksa keberlakuannya — JANGAN mengubah data, kata sandi, atau pengaturan lewat sesi yang diuji, dan segera logout setelah pembuktian.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Petakan siklus hidup sesi + catat baseline

1. **Petakan siklus:** (a) session ID sebelum login (anonim) vs sesudah login; (b) apa yang terjadi saat logout; (c) apa yang terjadi saat ganti kata sandi; (d) apa yang terjadi saat ganti email; (e) masa berlaku sesi (expiry) dan apakah ada revocation.
2. **Baseline:** login Akun A → catat session ID + cookie (`Domain`, `Path`, `Secure`, `HttpOnly`, `SameSite`); logout → catat apakah session ID lama masih berlaku. Simpan raw request/response (token disensor).
3. **Standar lulus:** peta siklus hidup sesi + atribut cookie tercatat. Target tidak memakai sesi (stateless murni tanpa sesi) = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji cacat siklus hidup sesi satu per satu (satu pola = satu putaran)

Uji berurutan pada akun uji sendiri; tiap pola dicoba dari state bersih.

#### Pola A — Session fixation (ID tidak diregenerasi saat login)
Ambil session ID anonim (sebelum login) untuk Akun A, lalu login dengan session ID itu (tetapkan cookie sebelum login). **Terbukti bila:** session ID yang sama tetap berlaku SETELAH login dan memberi sesi penuh — artinya penyerang yang menetapkan session ID bisa memakai sesi korban. Pembuktian hanya dengan akun uji sendiri.

#### Pola B — Invalidasi tidak tuntas saat logout
Login Akun A, catat session ID, lalu logout. Coba pakai session ID lama untuk mengakses endpoint profil. **Terbukti bila:** session ID lama masih memberi akses setelah logout.

#### Pola C — Invalidasi tidak tuntas saat ganti kata sandi / ganti email
Login Akun A di dua sesi (browser berbeda), catat kedua session ID. Ganti kata sandi (akun uji sendiri) dari sesi pertama, lalu coba sesi kedua. Ulangi untuk ganti email. **Terbukti bila:** sesi lain tetap berlaku setelah ganti kata sandi/email — artinya sesi lama tidak dicabut saat kredensial berubah.

#### Pola D — Session ID dapat diprediksi atau berentropi rendah
Kumpulkan beberapa session ID (login-logout berulang, akun uji sendiri, minimal 5 sampel) dan analisis polanya: berurutan, berbasis waktu, atau entropi rendah. **Terbukti bila:** session ID berikutnya dapat ditebak dari sampel yang ada (pola deterministik teramati). Jangan menebak session ID akun orang lain — cukup buktikan prediktabilitas dari sampel akun uji sendiri.

#### Pola E — JWT yang dipakai sebagai sesi tanpa expiry / revocation
Bila sesi memakai JWT, periksa klaim `exp` dan apakah ada mekanisme revocation: ubah `exp` (bila tidak ditandatangani dengan benar — lihat `manipulasi-jwt`), atau pakai token lama setelah logout/ganti kata sandi. **Terbukti bila:** token JWT lama tetap diterima setelah logout/ganti kata sandi, atau token tanpa `exp` diterima tanpa batas waktu.

#### Pola F — Sesi tidak terikat pada konteks (IP / User-Agent / perangkat)
Login Akun A, lalu pakai session ID yang sama dari konteks berbeda (IP/User-Agent berbeda, bila memungkinkan). **Terbukti bila:** sesi dipakai dari konteks yang sangat berbeda tanpa tantangan tambahan — catat sebagai temuan pendukung (nilainya lebih rendah; banyak aplikasi sengaja tidak mengikat sesi).

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** sesi akun uji lain dapat dipakai/difiksasi, ATAU sesi lama tetap berlaku setelah logout/ganti kredensial, ATAU session ID terbukti dapat diprediksi. **TOLAK** = sesi diregenerasi dengan benar di semua tahap, atau prediktabilitas tidak terbukti dari sampel.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pola yang sama minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor session ID/token sesi pada log HTTP sebelum dilampirkan (`[REDACTED]` — lampirkan hanya 4 karakter terakhir bila perlu membedakan sesi). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (Akun A / Akun B) + dua wadah sesi | Wajib untuk semua pola; pakai `manajemen-sesi-multi-peran` untuk wadah sesi per peran. |
| Proxy HTTP (Burp/mitmproxy) | Menetapkan/menggunakan session ID; simpan raw request/response. |
| Koleksi session ID (minimal 5 sampel) | Untuk Pola D; hanya dari akun uji sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta siklus sesi + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alur sesi]
Siklus sesi: [ID sebelum login: ... | ID sesudah login: sama/berbeda] | [logout: dicabut/tidak] | [ganti kata sandi: dicabut/tidak] | [ganti email: dicabut/tidak] | [expiry: ...]
Pola diuji: [A/B/C/D/E/F + nama pola + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Alur Sesi] - [Cacat Siklus Hidup Sesi] menyebabkan [sesi lama tetap berlaku / fixation / prediksi session ID]`. Isi laporan: Ringkasan (tahap siklus yang cacat); Langkah Reproduksi (akun uji + log HTTP, session ID disensor); Rekomendasi Perbaikan (regenerasi session ID saat login dan saat perubahan hak; cabut semua sesi saat logout/ganti kata sandi/ganti email; session ID acak berentropi tinggi dari generator aman; JWT sesi wajib `exp` singkat + daftar pencabutan).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-session`, 18 laporan), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Pola F (sesi tidak terikat konteks) sering dianggap perilaku yang disengaja — perlakukan sebagai temuan pendukung, bukan temuan utama.
- Session ID/token sesi TIDAK BOLEH ditulis utuh di log — sensor selalu, lampirkan maksimal 4 karakter terakhir bila perlu membedakan sesi.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan manajemen sesi.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila sesi memakai JWT dan fokusnya kriptografi token, pakai `manipulasi-jwt`.
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
- Bila butuh wadah sesi multi-peran untuk pengujian, pakai `manajemen-sesi-multi-peran`.
