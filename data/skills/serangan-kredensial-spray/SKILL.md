# Skill: Serangan Kredensial Spray — Satu Password ke Banyak Akun (PAGAR PALING KETAT)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 60, Agentic-Bug-Hunter `credential-attack` / `password-spray-methodology`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## ⚠️ PAGAR PALING KETAT — BACA DULU SEBELUM MEMAKAI SKILL INI

Skill ini adalah skill PALING SENSITIF di antara semua skill bounty. Pelanggaran pagar di bawah ini bukan sekadar "temuan ditolak" — melainkan bisa berarti akun hunter diblokir, program menutup akses, atau konsekuensi hukum.

1. **HANYA akun uji sendiri.** Spray HANYA boleh menguji akun yang MILIK SENDIRI (akun uji yang dibuat untuk pengujian, atau akun uji yang disediakan program). **DILARANG KERAS menguji akun korban — akun karyawan, pengguna, atau siapa pun yang bukan milik sendiri — termasuk sekadar "mengecek apakah password ini cocok dengan akun itu".**
2. **HANYA bila scope program secara EKSPLISIT mengizinkan pengujian kredensial.** Bila scope diam, ambigu, atau melarang pengujian kredensial/brute force/spray — skill ini DILARANG dipakai. "Tidak dilarang" ≠ "diizinkan". Harus ada kalimat eksplisit yang mengizinkan.
3. **Tanpa uji korban.** Segala bentuk pengujian terhadap akun orang lain DILARANG, tanpa pengecualian.
4. **Tanpa follow-up yang pernah diblokir.** Bila sebuah teknik spray / akun / endpoint pernah diblokir (lockout, CAPTCHA, pemblokiran IP, peringatan program), JANGAN pernah mengulanginya dalam bentuk apa pun — jangan ganti IP, jangan ganti user-agent, jangan ganti mode untuk mengakali blokir tersebut.
5. **Berhenti saat ada tanda lockout.** Satu tanda lockout/CAPTCHA/pemblokiran = BERHENTI SELURUHNYA, catat, laporkan ke Muse. Jangan "coba sekali lagi".
6. **Jangan memakai password hasil breach terhadap akun nyata.** Wordlist hanya dari kosakata perusahaan yang PUBLIK + password akun uji sendiri yang sengaja dibuat lemah. DILARANG memakai password hasil breach yang dikaitkan dengan orang tertentu.

## Pemicu (kapan dipakai)

- Scope program secara EKSPLISIT mengizinkan pengujian kredensial (kalimat izin tertulis di scope).
- Ada hipotesis kebijakan password lemah / tidak ada lockout pada endpoint login in-scope.
- Dipakai SETELAH `fondasi-kerentanan-web-api` dikuasai dan SETELAH izin eksplisit diverifikasi di scope — bukan sebelumnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan pipeline spray + mencatat setiap percobaan |
| Audit | **A60 Security Auditor** | Memeriksa izin scope + apakah pagar ketat dipatuhi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase — Muse berhak MELARANG spray kapan saja |

## Sudah tercakup (jangan diduplikat)

- **Brute force satu akun + rate limiting** (login, OTP, token reset, enumerasi) → kandidat 40 (`perburuan-brute-force-rate-limit`, kelompok lain) dan `analisis-bypass-2fa` (rate-limit OTP saja). Skill ini BUKAN brute force satu akun — melainkan spray: satu password ke banyak akun uji sendiri dengan penghindaran lockout + pipeline wordlist/breach/OSINT.
- **Spray per-protokol Okta** (endpoint `/api/v1/authn`, lockout per-protokol Okta) → skill `serangan-okta-idp`. Skill ini metodologi spray UMUM; bila targetnya Okta, pakai skill itu untuk detail protokolnya.
- **Pemeriksaan breach secara umum** → gunakan hanya sebagai input wordlist (langkah 2 di bawah), bukan sebagai skill tersendiri.

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN scope secara eksplisit mengizinkan pengujian kredensial.** Verifikasi kalimat izinnya dan catat kutipannya di log sebelum mulai. Tanpa kutipan izin = DILARANG.
2. **Hanya akun sendiri + canary palsu.** Hanya akun uji milik sendiri. **LARANGAN MENGUJI AKUN KORBAN — mutlak, tanpa pengecualian.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — spray yang membanjiri endpoint login = pelanggaran. Patuhi batas percobaan di Gerbang 3.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).** Spray TIDAK BOLEH berjalan otomatis tanpa pengawasan — tiap putaran diputuskan manusia.
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Jangan mengubah password, menonaktifkan MFA, atau mereset akun mana pun.
11. **Tanpa follow-up yang pernah diblokir.** Teknik/akun/endpoint yang pernah diblokir = JANGAN PERNAH diulang.
12. **Catat SEMUA percobaan.** Tiap percobaan spray (waktu, mode, akun uji, hasil) dicatat di log — tanpa catatan, spray dianggap tidak terjadi dan temuannya TOLAK.

## Langkah + gerbang

### Gerbang 0 — Verifikasi izin eksplisit (STOP bila tidak ada)

1. Baca pasal scope program. Cari kalimat yang secara eksplisit mengizinkan pengujian kredensial / password spraying / brute force.
2. Salin kutipan kalimat izin itu ke log. Bila tidak ditemukan kalimat eksplisit → STOP. Skill ini tidak dipakai.
3. Konfirmasi ke Muse bahwa izin sudah diverifikasi sebelum putaran pertama.

### Gerbang 1 — Pipeline 4 tahap (persiapan, tanpa menyentuh endpoint login)

| Tahap | Yang dilakukan | Batasan |
|---|---|---|
| 1. Generasi wordlist | Susun daftar password kandidat dari kosakata perusahaan yang PUBLIK (nama produk, slogan, nama kota kantor, musim) + pola umum (`Perusahaan2024!`, `Welcome123`). | HANYA kosakata publik + pola umum. DILARANG memakai password yang dikaitkan dengan orang tertentu. |
| 2. Pengecekan breach | Periksa apakah password kandidat muncul di breach publik (mis. HaveIBeenPwned, tanpa mengaitkan ke individu). | Hanya untuk menilai "password ini umum/lemah" — BUKAN untuk mengambil password milik seseorang. |
| 3. OSINT karyawan | Kumpulkan daftar AKUN UJI SENDIRI yang akan dipakai (akun uji yang dibuat untuk pengujian). | **DILARANG mengumpulkan daftar username/email karyawan atau pengguna nyata untuk dijadikan target spray.** Target spray = akun uji sendiri saja. |
| 4. Spray | Jalankan spray sesuai Gerbang 2–3. | Lihat batas di bawah. |

### Gerbang 2 — Pemilihan mode

| Mode | Endpoint | Catatan |
|---|---|---|
| Form HTTP | Form login web in-scope | Mode paling umum; amati respons (error generik vs spesifik) |
| OAuth | `/oauth2/token` (resource owner password grant) | Bila tersedia; catat perbedaan respons antar mode |
| O365 / Entra | Endpoint login Microsoft in-scope | Hanya bila tenant tercantum eksplisit di scope |
| Okta | `/api/v1/authn` | Detail protokol di `serangan-okta-idp` — pakai skill itu |

Satu mode per putaran; jangan menjalankan banyak mode bersamaan.

### Gerbang 3 — Taktik rate-limit & lockout (batas keras)

1. **Jumlah percobaan:** maksimal 1 password per akun uji per putaran; maksimal 3 password per akun uji per hari; maksimal 5 akun uji per program. Total maksimal 15 percobaan per hari.
2. **Jeda:** minimal 10 menit antar percobaan pada akun yang sama; jeda acak 5–15 menit antar akun.
3. **Berhenti segera bila:** respons menunjukkan lockout, CAPTCHA, penundaan paksa, atau pemblokiran IP. BERHENTI SELURUHNYA, catat, laporkan ke Muse. Jangan ganti IP/user-agent/mode untuk mengakali.
4. **Jangan memakai tool spray otomatis** (Burp Intruder cluster bomb, Hydra, dsb.) tanpa pengawasan — tiap percobaan dikirim manual atau satu per satu dengan jeda, dan dicatat.

### Gerbang 4 — Deteksi keberhasilan + gerbang validasi laporan

1. **Deteksi keberhasilan:** login BERHASIL pada akun uji sendiri dengan password lemah dari wordlist = bukti kebijakan password lemah / tidak ada lockout yang efektif. Catat: password yang berhasil (itu password akun uji sendiri yang sengaja lemah), waktu, mode.
2. **Dampak keamanan nyata:** Valid = login berhasil pada akun uji sendiri + password itu berasal dari wordlist generik (bukan password yang sengaja dibuat untuk pengujian itu saja — bila password berhasil adalah password yang dipasang khusus untuk pengujian, dampaknya lemah; yang kuat adalah password generik dari Tahap 1 yang ternyata cocok). **TOLAK** = tidak ada login yang berhasil, atau keberhasilan hanya karena password yang dipasang sendiri untuk pengujian.
3. **Reproduksibilitas:** keberhasilan harus bisa diulang 1× (login kedua dengan password yang sama) — tanpa mengulang spray penuh.
4. **Higienitas bukti:** sensor password akun uji dan token sesi sebelum dilampirkan (`[REDACTED]`). JANGAN lampirkan password yang berhasil secara utuh — cukup sebutkan polanya (mis. "password generik berbasis nama perusahaan + tahun").

Hanya temuan yang lolos keempat gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `curl` / Burp Suite Repeater (manual) | Satu percobaan per kirim, dengan jeda; JANGAN Intruder otomatis tanpa pengawasan |
| Wordlist dari kosakata publik | Tahap 1 pipeline; tanpa password milik orang tertentu |
| Akun uji sendiri (maks. 5 per program) | Satu-satunya target spray |
| `serangan-okta-idp` | Detail spray per-protokol Okta (bila targetnya Okta) |
| `~/workspace/catatan/log-bug-bounty.md` | Log SEMUA percobaan (waktu, mode, akun uji, hasil) + kutipan izin scope |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint login]
Izin scope: [kutipan kalimat eksplisit yang mengizinkan pengujian kredensial]
Mode: [form HTTP / OAuth / O365 / Okta]
Percobaan: [waktu | mode | akun uji | password (pola saja) | hasil] — satu baris per percobaan
Keberhasilan: [akun uji + pola password + bukti login berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint Login] - Password Spray dengan [Pola Password] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter `credential-attack`), bukan pengalaman teruji — skill ini butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Pagar skill ini adalah yang paling ketat di antara semua skill bounty.** Bila ada keraguan apakah suatu langkah melanggar pagar — ANGGAP MELANGGAR, berhenti, dan tanyakan ke Muse.
- Kebanyakan program MODERN melarang pengujian kredensial secara eksplisit atau diam — dalam praktiknya skill ini akan lebih sering TIDAK dipakai daripada dipakai. Itu benar dan diharapkan: "melewati spray" adalah keputusan yang valid dan sering kali keputusan yang tepat.
- Keberhasilan spray pada akun uji sendiri membuktikan kebijakan password lemah — tetapi dampak yang diklaim harus proporsional: satu akun uji yang berhasil ≠ "seluruh pengguna bisa dibobol". Nyatakan dengan jujur berapa akun uji yang berhasil dan dari berapa percobaan.
