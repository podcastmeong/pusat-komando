# Skill: Perburuan Framework Next.js — Server Actions, Middleware Bypass & Cache ISR

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 53, Claude-BugHunter `hunt-nextjs`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target teridentifikasi memakai Next.js (header `x-powered-by: Next.js`, `/_next/static/`, `__NEXT_DATA__`, RSC payload `/_next/data/`).
- Ditemukan Server Actions, middleware auth, halaman ISR, atau endpoint `/_next/image` (Image Optimization).
- Dipakai SETELAH framework teridentifikasi via fingerprint (`probing-http-fingerprint`) — jangan menebak framework.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprint + pengujian pola khas Next.js |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- SSRF secara umum → skill `ssrf-oast` (bila ada) / `fondasi-kerentanan-web-api`. Skill ini HANYA SSRF via `/_next/image` (Image Optimization), bukan SSRF umum.
- Cache poisoning secara umum → skill `peracunan-cache`. Skill ini HANYA poisoning cache ISR (revalidate/on-demand), bukan cache poisoning umum.
- Kelas kerentanan umum (XSS, IDOR) → skill `fondasi-kerentanan-web-api`.
- Lihat juga skill framework lain bila target memakai banyak stack: `perburuan-framework-aspnet`, `perburuan-framework-laravel`, `perburuan-framework-nodejs`, `perburuan-framework-springboot`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan. **Jangan memicu revalidasi ISR berulang-ulang** (itu membebani origin).
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Server Actions yang diuji HANYA yang bersifat baca atau yang mengubah data MILIK SENDIRI (mis. ubah nama profil akun uji sendiri); JANGAN memanggil Server Action yang mengubah data orang lain atau menghapus data.

## Langkah + gerbang

### Gerbang 1 — Fingerprint Next.js

Standar lulus: framework + versi terkonfirmasi atau dinyatakan "bukan Next.js" dengan bukti.

1. Header/artefak: `x-powered-by: Next.js`, path `/_next/static/`, `__NEXT_DATA__` di HTML, RSC payload (`text/x-component`).
2. Build ID: ekstrak `buildId` dari `__NEXT_DATA__` — catat untuk analisis route.
3. Route mapping: petakan halaman (App Router `app/` vs Pages Router `pages/`) dari struktur `/_next/data/<buildId>/...`.

### Gerbang 2 — Pola khas (uji satu per satu, read-only / data sendiri)

| Pola | Cara uji aman | Indikator |
|---|---|---|
| Eksekusi Server Actions | Identifikasi Server Action dari RSC payload / form `action` (ID action + argumen). Panggil action itu langsung via POST dengan argumen MILIK SENDIRI (mis. action baca data / ubah profil sendiri) tanpa melalui UI — apakah server mengeksekusi tanpa cek otorisasi UI? | Action sensitif tereksekusi tanpa otorisasi yang semestinya = kandidat |
| Bypass auth middleware via path aset statis | Middleware Next.js sering tidak berjalan pada path tertentu (`/_next/static/`, `/_next/image`, file publik). Uji path yang dilindungi (mis. `/dashboard`) dengan variasi: `/dashboard` vs `/_next/static/../dashboard`, trailing slash, encoded path (`%2e%2e`), header `x-middleware-rewrite`. | Halaman terproteksi terbuka lewat variasi path = kandidat |
| Poisoning cache ISR | Uji halaman ISR milik sendiri: kirim request dengan header yang memengaruhi cache key (mis. `x-forwarded-host`, query aneh) lalu periksa apakah respons beracun tersimpan dan disajikan ke sesi kedua MILIK SENDIRI. JANGAN meracuni cache halaman yang dipakai pengguna lain. | Respons beracun tersimpan + tersaji ke sesi sendiri = kandidat |
| SSRF Image Optimization | `GET /_next/image?url=<URL-canary-milik-sendiri>` — apakah server mengambil URL eksternal? Uji HANYA ke server canary milik sendiri (atau `https://example.com` untuk bukti fetch). Periksa apakah URL internal (`http://169.254.169.254/`, `http://localhost/`) difilter — JANGAN meminta URL internal bila ada indikasi SSRF: cukup tunjukkan fetch eksternal berhasil + dokumentasikan bahwa filter internal tidak teruji demi keamanan, atau uji dengan canary yang mencatat percobaan akses. | Server mengambil URL eksternal yang tidak ada di allowlist = kandidat |

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = Server Action tereksekusi tanpa otorisasi / halaman terproteksi terbuka / cache ISR teracuni (sesi sendiri) / image optimizer mengambil URL eksternal. **TOLAK** = sekadar "Next.js terdeteksi" atau "buildId terlihat".
2. **Reproduksibilitas:** ulangi minimal 2×; simpan request/response mentah (RSC payload + header).
3. **Higienitas bukti:** sensor token sesi dan data pribadi sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `probing-http-fingerprint` | Fingerprint framework + buildId dari `__NEXT_DATA__` |
| Burp Suite Repeater | Panggil Server Actions langsung, variasi path middleware, uji `/_next/image` |
| Server canary milik sendiri | Satu-satunya tujuan SSRF Image Optimization |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Framework: [Next.js + buildId + bukti fingerprint]
Pola diuji: [Server Actions / middleware bypass / ISR / image SSRF + hasil]
Pembuktian: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola Next.js] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-nextjs`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku middleware dan ISR sangat bergantung pada versi Next.js dan konfigurasi deployment (Vercel vs self-hosted) — pola yang bekerja di satu versi bisa sudah diperbaiki di versi lain; catat versi/buildId di setiap temuan.
- SSRF via `/_next/image` pada deployment Vercel modern umumnya sudah dibatasi allowlist domain — jangan klaim SSRF hanya dari "URL eksternal diambil"; tunjukkan bahwa URL di luar allowlist (atau URL internal) bisa diambil, atau nyatakan batas pembuktian dengan jujur.
- Server Actions yang diekspos tanpa otorisasi sering hanya "baca" — dampaknya dinilai dari DATA apa yang bisa dibaca/ditulis, bukan dari sekadar "action bisa dipanggil".
