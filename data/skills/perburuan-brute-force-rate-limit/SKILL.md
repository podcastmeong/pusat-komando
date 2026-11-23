# Skill: Perburuan Brute-Force & Rate Limit — Pengujian Batas Percobaan Login, OTP, dan Token Reset

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 40, sumber: Claude-BugHunter `hunt-brute-force`, 6 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target punya endpoint login, verifikasi OTP/2FA, reset kata sandi, atau endpoint lain yang menerima tebakan (kode, token).
- Ada sinyal: tidak ada CAPTCHA/lockout setelah banyak percobaan gagal, pesan error berbeda antar percobaan, atau respons lebih lambat untuk input yang benar (timing).
- Dipakai pada akun uji sendiri, SETELAH scope program dibaca dan dipastikan pengujian ini diizinkan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Menguji ada/tidaknya rate limit per endpoint dengan volume minimal |
| Audit | **A60 Security Auditor** | Memeriksa apakah volume pengujian + bukti memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Rate-limit OTP 2FA saja (ruang kunci 10^6, maksimal belasan percobaan) → skill `analisis-bypass-2fa` Teknik C. Skill ini JAUH LEBIH LUAS: login, token reset, credential stuffing, dan enumerasi username/email — OTP hanya satu dari lima area di sini.
- Pacing/ritme request agar tidak terblokir (arah berlawanan: menjaga penguji tetap aman) → skill `pacing-request-aman`. Skill ini menguji APAKAH target membatasi, bukan cara menghindarinya.
- Enumerasi lewat perbedaan respons sebagai teknik umum → sebagian di `access-control-differential-analyst` (diferensial respons lintas akun, bukan brute-force).
- Brute-force secret JWT (HMAC) → skill `manipulasi-jwt` Teknik B (khusus token JWT, bukan endpoint login).
- Rantai ATO menyeluruh → skill `perburuan-pengambilalihan-akun` (skill ini adalah jalur 8 di taksonomi itu).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri. Jangan pernah menebak kata sandi, OTP, atau token milik orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

### PAGAR PALING KETAT — brute-force / rate-limit (bagian dari Aturan keras, WAJIB dibaca sebelum Gerbang 2)

- **Hanya akun uji sendiri.** Semua percobaan memakai kredensial/OTP/token akun milik sendiri. Menebak kredensial akun orang lain, walau "hanya beberapa kali", DILARANG.
- **Hanya target in-scope yang secara eksplisit mengizinkan pengujian ini.** Bila aturan program TIDAK menyebut pengujian brute-force/rate-limit sebagai diizinkan, atau secara eksplisit melarangnya, STOP — jangan uji. Bila ragu, tanyakan ke Muse sebelum mengirim satu pun percobaan.
- **Tanpa uji korban.** Jangan memakai akun/identitas orang lain sebagai bahan tebakan, dan jangan menguji terhadap endpoint yang memengaruhi akun pengguna sungguhan.
- **Tanpa brute-force live tanpa izin program.** Brute-force penuh (menebak sampai dapat) TIDAK PERNAH dilakukan di target live. Yang diuji hanya ADA/TIDAKNYA rate limit.
- **Uji rate-limit dengan volume minimal yang membuktikan ada/tidaknya limit (bukan membanjiri).** Batas: maksimal **20 percobaan gagal berurutan per endpoint per sesi pengujian**, laju rendah (jeda ≥ 2 detik antar percobaan), dan **BERHENTI segera** bila muncul CAPTCHA, lockout, throttling, atau penolakan berulang. Bila setelah 20 percobaan tidak ada limit yang muncul, itu SUDAH cukup sebagai bukti "tidak ada rate limit yang teramati" — jangan lanjutkan ke ratusan/ribuan percobaan.
- **Ruang kunci besar = tidak layak = jangan coba.** Bila target memakai OTP 6 digit acak atau token reset berentropi tinggi, brute-force penuh secara matematis tidak layak dan TIDAK BOLEH dicoba — yang diuji hanya apakah rate-limit ADA atau TIDAK, bukan menebak nilainya sampai dapat.
- **Kode/OTP/token akun uji sendiri tidak boleh ditulis utuh di log.** Catat hanya "diterima/ditolak" + status respons.

## Langkah + gerbang

### Gerbang 1 — Baca aturan program + petakan endpoint tebakan

1. **Baca pasal scope program:** apakah pengujian brute-force/rate-limit diizinkan, dibatasi, atau dilarang? Bila dilarang/tidak disebut = STOP, catat dan tutup.
2. **Petakan endpoint:** login (`/login`, `/api/auth`), verifikasi OTP (`/verify-otp`), reset (`/forgot-password`, `/reset`), dan endpoint lain yang menerima tebakan. Catat parameter + respons sukses vs gagal + header rate-limit (`X-RateLimit-*`, `Retry-After`).
3. **Baseline:** 1 percobaan BENAR (kredensial akun uji sendiri) → sukses; 1 percobaan SALAH → gagal. Simpan raw request/response keduanya (kredensial disensor).

### Gerbang 2 — Uji ada/tidaknya limit per area (satu area = satu putaran, volume minimal)

Uji berurutan; tiap area maksimal 20 percobaan gagal, jeda ≥ 2 detik, berhenti segera bila ada CAPTCHA/lockout/throttling.

**A. Login — tidak ada/lemahnya rate limiting:** kirim ≤ 20 percobaan login gagal (kata sandi salah, akun uji sendiri). Indikator: semua percobaan diproses normal tanpa CAPTCHA/lockout/penundaan progresif = kandidat temuan. Bila CAPTCHA/lockout muncul sebelum 20 = limit ADA, catat dan tutup area ini.

**B. Brute force OTP/2FA (ruang kunci 10^6):** kirim ≤ 20 kode OTP salah (akun uji sendiri). Indikator: tidak ada limit setelah 20 percobaan = kandidat temuan (ruang 10^6 tanpa limit secara teori bisa ditebak — tapi JANGAN menebak sampai dapat; buktinya adalah ketiadaan limit). Detail teknik OTP → `analisis-bypass-2fa`.

**C. Brute force token reset-password:** minta token reset untuk akun uji sendiri, lalu kirim ≤ 20 token salah ke endpoint reset. Indikator: tidak ada limit + token tidak kedaluwarsa cepat = kandidat temuan. Jangan pernah memakai token reset akun orang lain.

**D. Credential stuffing:** uji apakah endpoint login menerima banyak kredensial berbeda tanpa limit — DENGAN BATAS: hanya kredensial akun uji sendiri (beberapa akun uji milik sendiri, bukan daftar bocor). Indikator: tidak ada limit antar-akun = kandidat temuan. Daftar kredensial bocor DILARANG dipakai.

**E. Enumerasi username/email:** kirim ≤ 20 percobaan dengan username/email yang ada vs tidak ada (hanya alamat milik sendiri + alamat canary palsu). Bandingkan pesan error, status code, dan timing. Indikator: perbedaan konsisten (mis. "pengguna tidak ditemukan" vs "kata sandi salah", atau timing berbeda) = kandidat temuan enumerasi.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** ketiadaan limit TERBUKTI dengan ≤ 20 percobaan (semua diproses normal), ATAU enumerasi terbukti lewat perbedaan respons yang konsisten. **TOLAK** = limit muncul sebelum 20 percobaan, atau perbedaan respons tidak konsisten saat diulang.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi area yang sama minimal 2× di sesi berbeda (tetap ≤ 20 percobaan per sesi). Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor kredensial, OTP, dan token pada log HTTP sebelum dilampirkan (`[REDACTED]`); catat jumlah percobaan + jeda + titik berhenti. Bukti tanpa sensor atau tanpa catatan volume = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri (minimal 1, idealnya 2) | Wajib untuk semua area. Semua milik sendiri. |
| Proxy HTTP (Burp/mitmproxy) | Mengirim percobaan berurutan dengan jeda; simpan raw request/response + hitung percobaan. |
| Timer/jeda manual | Jeda ≥ 2 detik antar percobaan; catat waktu tiap percobaan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log aturan program + endpoint + jumlah percobaan + hasil tiap area + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Aturan program soal brute-force/rate-limit: [diizinkan / dibatasi / dilarang / tidak disebut]
Area: [A/B/C/D/E + nama area]
Volume: [jumlah percobaan gagal: ≤20] | [jeda: ≥2 dtk] | [berhenti karena: limit muncul / 20 tercapai]
Indikator teramati: [apa yang terjadi, persis — status code, pesan error, timing, header rate-limit]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - Tidak ada rate limit pada [login/OTP/token reset] memungkinkan [brute-force/enumerasi]`. Isi laporan: Ringkasan (endpoint + ketiadaan limit + volume minimal yang dipakai sebagai bukti); Langkah Reproduksi (akun uji + ≤ 20 percobaan + log HTTP); Rekomendasi Perbaikan (rate limit per IP/akun, lockout progresif, CAPTCHA setelah N gagal, pesan error generik yang sama untuk pengguna ada/tidak ada).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-brute-force`, 6 laporan), bukan pengalaman teruji — tiap area butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Pagar volume (≤ 20 percobaan) adalah batas ETIS tim ini, bukan batas teknis target — bukti "tidak ada limit" dari 20 percobaan sudah cukup untuk laporan; jangan pernah membanjiri untuk "membuktikan lebih kuat".
- Bila program melarang pengujian brute-force, skill ini TIDAK BERLAKU untuk program itu walau endpointnya rentan — catat sebagai "tidak dapat diuji karena aturan program", bukan sebagai temuan.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan rate-limit.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope + pasal larangan brute-force sebelum menguji).

## Alternatives for better results

- Bila hanya OTP 2FA yang dicurigai, pakai langsung `analisis-bypass-2fa` Teknik C (batasnya lebih ketat: belasan percobaan).
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
