# Skill: Perburuan Framework Laravel — Debug Mode, Telescope/Horizon & Signed URL

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 53, Claude-BugHunter `hunt-laravel`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target teridentifikasi memakai Laravel (cookie `laravel_session` / `XSRF-TOKEN`, header `X-Powered-By` PHP + struktur route khas, error page Ignition).
- Ditemukan error page Laravel yang menampilkan detail, atau path `/telescope`, `/horizon`, `/_ignition`.
- Dipakai SETELAH framework teridentifikasi via fingerprint (`probing-http-fingerprint`) — jangan menebak framework.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprint + pengujian pola khas Laravel |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Kelas kerentanan umum (SQLi, XSS, IDOR) → skill `fondasi-kerentanan-web-api`. Skill ini HANYA pola khas Laravel.
- Lihat juga skill framework lain bila target memakai banyak stack: `perburuan-framework-aspnet`, `perburuan-framework-nextjs`, `perburuan-framework-nodejs`, `perburuan-framework-springboot`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG:** mengeksekusi RCE via Ignition atau memodifikasi data lewat Telescope/Horizon — buktikan keterbukaan dashboard/error page dengan akses baca saja, tanpa menjalankan aksi apa pun di dalamnya.

## Langkah + gerbang

### Gerbang 1 — Fingerprint Laravel

Standar lulus: framework terkonfirmasi atau dinyatakan "bukan Laravel" dengan bukti.

1. Cookie: `laravel_session`, `XSRF-TOKEN`; header `Set-Cookie` dengan enkripsi Laravel.
2. Error page: halaman error Ignition (tampilan khas dengan stack trace, file `.env` yang dirujuk) — picu error 404/500 pada path uji sendiri.
3. Path khas: `/telescope`, `/horizon`, `/_ignition/execute-solution`, `/vendor/`.

### Gerbang 2 — Pola khas (uji satu per satu, read-only)

| Pola | Cara uji aman | Indikator |
|---|---|---|
| Kebocoran debug mode | Picu error pada path uji sendiri; periksa apakah `APP_DEBUG=true` (stack trace lengkap, nilai `.env` seperti `APP_KEY`, kredensial DB/mail tampil). | Nilai sensitif tampil di error page = kandidat kritis (sensor sebelum dicatat) |
| Dashboard Telescope tanpa auth | `GET /telescope`, `GET /telescope/requests` tanpa login. | 200 + daftar request/job/log terlihat = kandidat (STOP: jangan baca isi request pengguna lain — cukup buktikan dashboard terbuka) |
| Dashboard Horizon tanpa auth | `GET /horizon`, `GET /horizon/api/jobs` tanpa login. | 200 + daftar job/queue terlihat = kandidat |
| Ignition RCE | Periksa `/_ignition/execute-solution` — JANGAN mengeksekusi solusi. Cukup periksa apakah endpoint merespons (mis. 200/405) tanpa auth dan apakah debug mode aktif (prasyarat RCE). Klaim RCE hanya sebagai dampak potensial bila endpoint + debug mode keduanya terbukti. | Endpoint terbuka + debug aktif = kandidat (tanpa eksekusi) |
| Manipulasi signed URL | Ambil signed URL milik SESI SENDIRI (mis. tautan unduh/verifikasi email sementara), ubah parameter (ID, expiry) dan periksa apakah signature masih diterima. | Parameter yang diubah tetap diterima = kandidat |

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = nilai sensitif bocor / dashboard terbuka / signed URL bisa dimanipulasi — dengan bukti pada sesi sendiri. **TOLAK** = sekadar "Laravel terdeteksi" atau "path /telescope mengembalikan 404".
2. **Reproduksibilitas:** ulangi minimal 2×; simpan request/response mentah.
3. **Higienitas bukti:** sensor `APP_KEY`, kredensial DB/mail, token sesi, dan data pengguna lain sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `probing-http-fingerprint` | Fingerprint framework dari cookie/header/error page |
| Burp Suite Repeater | Akses path Telescope/Horizon/Ignition, manipulasi signed URL sesi sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Framework: [Laravel + bukti fingerprint]
Pola diuji: [debug / Telescope / Horizon / Ignition / signed URL + hasil]
Pembuktian: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola Laravel] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-laravel`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Telescope/Horizon di produksi yang benar biasanya sudah di-gate oleh auth/gate — keterbukaan tanpa auth adalah salah konfigurasi, bukan perilaku default; jangan klaim sebelum menguji langsung.
- Ignition RCE HANYA dibuktikan sebagai "endpoint terbuka + debug aktif" — eksekusi RCE live DILARANG (Aturan keras 10).
- `APP_KEY` yang bocor lewat error page sering sudah dirotasi — verifikasi relevansinya (mis. apakah signed URL masih bisa dibuat dengan kunci itu pada sesi sendiri) sebelum mengklaim dampak.
