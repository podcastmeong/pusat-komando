# Skill: Perburuan Bypass CAPTCHA — Pengujian Apakah Validasi CAPTCHA Benar-Benar Terjadi di Server

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 41, sumber: Claude-BugHunter `hunt-captcha-bypass`, 6 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target menampilkan CAPTCHA (reCAPTCHA, hCaptcha, Cloudflare Turnstile, atau CAPTCHA buatan sendiri) pada login, pendaftaran, reset kata sandi, atau formulir sensitif.
- Ada sinyal: CAPTCHA hanya muncul di klien, token CAPTCHA terlihat di request, atau alur bisa diselesaikan tanpa menyelesaikan CAPTCHA.
- Dipakai pada akun uji sendiri, setelah alur normal dengan CAPTCHA dipetakan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan alur CAPTCHA + menguji pola bypass satu per satu |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Tidak ada skill CAPTCHA di daftar yang ada — kandidat murni baru. Sebutan CAPTCHA di skill lain hanya insidental (mis. `pacing-request-aman` menyebut CAPTCHA sebagai sinyal terblokir; `uji-live-browser` menyebut Turnstile sebagai penghalang) dan TIDAK mengajarkan pengujian bypass.
- Rate limit / brute-force pada endpoint yang dilindungi CAPTCHA → skill `perburuan-brute-force-rate-limit` (skill itu menguji limit; skill ini menguji apakah CAPTCHA-nya sendiri divalidasi).
- Cloudflare Turnstile yang memblokir pengujian → bukan bypass; bila Turnstile memblokir, catat sebagai penghalang dan serahkan ke Muse/Cipta (jangan memaksa melewatinya).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh alur yang memakai CAPTCHA berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri. Jangan pernah memakai bypass CAPTCHA untuk mengakses atau menguji akun orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Pembuktian bypass cukup sampai request tanpa CAPTCHA valid DITERIMA server (mis. login berhasil / formulir terkirim) pada akun uji sendiri; jangan ubah data apa pun setelahnya.

### PAGAR PALING KETAT — bypass CAPTCHA (bagian dari Aturan keras, WAJIB dibaca sebelum Gerbang 2)

- **Hanya akun uji sendiri.** Semua percobaan memakai akun/formulir milik sendiri.
- **Hanya target in-scope yang secara eksplisit mengizinkan pengujian itu.** Bila aturan program TIDAK menyebut pengujian bypass CAPTCHA sebagai diizinkan, atau secara eksplisit melarangnya, STOP — jangan uji. Bila ragu, tanyakan ke Muse sebelum mengirim satu pun request uji.
- **Tanpa uji korban.** Jangan memakai bypass untuk menguji terhadap akun/formulir pengguna sungguhan.
- **Tanpa brute-force live tanpa izin program.** Bypass CAPTCHA TIDAK BOLEH dipakai sebagai pintu untuk membanjiri endpoint (login/pendaftaran) — pengujian rate-limit tetap memakai pagar volume minimal di `perburuan-brute-force-rate-limit` (≤ 20 percobaan, jeda ≥ 2 detik).
- **Tanpa solver CAPTCHA pihak ketiga / layanan berbayar.** Pengujian hanya membuktikan apakah server memvalidasi CAPTCHA — bukan menyelesaikan CAPTCHA dengan jasa solver, OCR massal, atau otomasi pemecah CAPTCHA. Bila CAPTCHA harus diselesaikan secara sah untuk baseline, selesaikan sendiri secara manual satu kali.
- **Uji dengan volume minimal.** Tiap pola dicoba maksimal 3× (satu kali bukti + dua kali reproduksi). Bila pola gagal 3×, tutup pola itu.

## Langkah + gerbang

### Gerbang 1 — Petakan alur CAPTCHA + catat baseline

1. **Petakan alur:** di endpoint mana CAPTCHA muncul, parameter apa yang dikirim (`g-recaptcha-response`, `h-captcha-response`, `cf-turnstile-response`, atau field buatan sendiri), dan apa respons sukses vs gagal.
2. **Baseline:** selesaikan CAPTCHA secara manual satu kali (akun uji sendiri) → request DITERIMA. Simpan raw request/response (token disensor).
3. **Standar lulus:** parameter CAPTCHA + respons sukses/gagal tercatat. Target tidak memakai CAPTCHA di alur yang diuji = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji pola bypass satu per satu (satu pola = satu putaran, maks 3× per pola)

Uji berurutan pada akun uji sendiri; tiap pola dicoba dari state bersih.

#### Pola A — Field CAPTCHA dihilangkan dari request
Hapus parameter CAPTCHA dari request (atau kirim request tanpa field itu sama sekali). **Terbukti bila:** server tetap menerima request dan melanjutkan alur (login berhasil / formulir terkirim) tanpa CAPTCHA.

#### Pola B — Token CAPTCHA dipakai ulang (tidak sekali pakai)
Ambil token CAPTCHA valid dari baseline (satu kali penyelesaian manual), lalu pakai token yang SAMA untuk request kedua dan ketiga (akun uji sendiri, sesi berbeda). **Terbukti bila:** token lama tetap diterima berulang kali — server tidak menandai token sebagai sudah dipakai.

#### Pola C — Respons CAPTCHA diterima tanpa verifikasi server
Kirim token CAPTCHA palsu/kosong (mis. string acak, `null`, atau nilai dummy) sebagai parameter. **Terbukti bila:** server menerima token palsu dan melanjutkan alur — artinya tidak ada panggilan verifikasi ke penyedia CAPTCHA di sisi server.

#### Pola D — Validasi hanya di klien
Periksa apakah pemeriksaan CAPTCHA hanya berupa JavaScript di klien (tombol submit diblokir di UI tapi request langsung ke API tidak memeriksa CAPTCHA). Kirim request langsung ke endpoint API tanpa melewati UI. **Terbukti bila:** request langsung diterima tanpa token CAPTCHA valid.

#### Pola E — Token CAPTCHA dari konteks lain dipakai ulang
Bila target punya beberapa formulir ber-CAPTCHA, ambil token valid dari formulir A lalu pakai di formulir B. **Terbukti bila:** token lintas-formulir diterima — server tidak mengikat token ke aksi/formulir tertentu.

#### Pola F — Parameter CAPTCHA dimanipulasi
Ubah nilai parameter terkait (mis. `captcha_verified: false` → `true`, hapus flag verifikasi, atau ubah skor/rating CAPTCHA bila dikirim dari klien). **Terbukti bila:** server percaya pada flag dari klien dan melanjutkan alur.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** request tanpa CAPTCHA valid DITERIMA server dan alur sensitif berlanjut (login/pendaftaran/reset berhasil) pada akun uji sendiri. **TOLAK** = server menolak, atau bypass hanya tampak di klien tanpa respons server yang menerima.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pola yang sama minimal 2× dari state bersih (total maks 3× per pola). Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token CAPTCHA dan token sesi pada log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib untuk semua pola. Milik sendiri. |
| Proxy HTTP (Burp/mitmproxy) | Menghapus/mengubah parameter CAPTCHA; simpan raw request/response. |
| Penyelesaian CAPTCHA manual (satu kali, baseline) | Hanya untuk baseline + token valid Pola B/E; selesaikan sendiri, jangan pakai solver pihak ketiga. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta alur CAPTCHA + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint ber-CAPTCHA]
Jenis CAPTCHA: [reCAPTCHA / hCaptcha / Turnstile / buatan sendiri]
Aturan program soal bypass CAPTCHA: [diizinkan / dilarang / tidak disebut]
Pola diuji: [A/B/C/D/E/F + nama pola + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola Bypass CAPTCHA] memungkinkan [alur sensitif] tanpa CAPTCHA valid`. Isi laporan: Ringkasan (jenis CAPTCHA + pola yang lolos); Langkah Reproduksi (akun uji + log HTTP, token disensor); Rekomendasi Perbaikan (verifikasi token di server ke penyedia CAPTCHA setiap request, token sekali pakai + terikat aksi/sesi + kedaluwarsa singkat, jangan percaya flag verifikasi dari klien).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-captcha-bypass`, 6 laporan), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Bila CAPTCHA target adalah Turnstile/penyedia yang memblokir pengujian otomatis, skill ini tidak memaksa melewatinya — catat penghalang dan serahkan ke Muse/Cipta.
- Bypass CAPTCHA saja (tanpa dampak lanjutan) sering dinilai rendah oleh program — rangkai dengan dampaknya (mis. brute-force login tanpa hambatan, pendaftaran massal) lewat `perburuan-brute-force-rate-limit` dan `perangkaian-kerentanan`, tapi tetap dalam pagar volume minimal.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan bypass CAPTCHA.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope + pasal larangan bypass CAPTCHA sebelum menguji).

## Alternatives for better results

- Bila CAPTCHA dilewati lalu endpoint login ternyata tanpa rate limit, pakai `perburuan-brute-force-rate-limit` untuk membuktikan dampak lanjutannya.
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
