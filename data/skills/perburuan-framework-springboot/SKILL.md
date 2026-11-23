# Skill: Perburuan Framework Spring Boot — Actuator, SpEL & Konsol H2

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 53, Claude-BugHunter `hunt-springboot`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target teridentifikasi memakai Spring Boot (header `X-Application-Context`, cookie `JSESSIONID`, error page Whitelabel, path `/actuator`, `/error` dengan JSON `{"timestamp":...,"status":...}`).
- Ditemukan endpoint `/actuator/*`, konsol H2 (`/h2-console`), atau error yang menyebut SpEL / Spring Expression Language.
- Dipakai SETELAH framework teridentifikasi via fingerprint (`probing-http-fingerprint`) — jangan menebak framework.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprint + pengujian pola khas Spring Boot |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi template SSTI secara umum → skill `injeksi-template-ssti`. Skill ini HANYA injeksi SpEL (Spring Expression Language) — sintaks dan konteksnya berbeda dari SSTI template engine.
- Kelas kerentanan umum (SQLi, XSS, IDOR) → skill `fondasi-kerentanan-web-api`.
- Lihat juga skill framework lain bila target memakai banyak stack: `perburuan-framework-aspnet`, `perburuan-framework-laravel`, `perburuan-framework-nextjs`, `perburuan-framework-nodejs`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan. **JANGAN memanggil endpoint `/actuator/shutdown`** (itu mematikan aplikasi) — cukup periksa apakah endpoint itu TERBUKA (merespons tanpa auth), jangan mengeksekusinya.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG:** menjalankan query di konsol H2 yang mengubah/membaca data (gunakan hanya `SELECT 1` / buktikan halaman login konsol terbuka), mengunduh heapdump penuh bila berisi kredensial (cukup buktikan endpoint merespons + header `Content-Type`/`Content-Length`), dan mengeksekusi SpEL yang memanggil perintah sistem — buktikan SpEL dengan ekspresi read-only (`7*7`).

## Langkah + gerbang

### Gerbang 1 — Fingerprint Spring Boot

Standar lulus: framework + versi teridentifikasi atau dinyatakan "bukan Spring Boot" dengan bukti.

1. Header/cookie: `X-Application-Context`, `JSESSIONID`, Whitelabel Error Page (HTML khas Spring).
2. Error JSON: `{"timestamp":...,"status":404,"error":"Not Found","path":"..."}`.
3. Endpoint khas: `GET /actuator`, `GET /actuator/health`, `GET /h2-console`.

### Gerbang 2 — Pola khas (uji satu per satu, read-only)

| Pola | Cara uji aman | Indikator |
|---|---|---|
| Endpoint Actuator terbuka | `GET /actuator`, lalu tiap endpoint: `/actuator/env`, `/actuator/configprops`, `/actuator/heapdump`, `/actuator/mappings`, `/actuator/beans`, `/actuator/shutdown` (HANYA GET/HEAD untuk memeriksa keterbukaan — JANGAN POST ke shutdown). | `env`/`configprops` mengembalikan properti sensitif (kredensial, kunci) = kandidat kritis; `heapdump` merespons 200 = kandidat (jangan unduh isinya bila besar/berisi secret — cukup header + ukuran); `shutdown` merespons tanpa auth = kandidat (jangan dieksekusi) |
| Injeksi SpEL | Cari input yang dievaluasi sebagai SpEL (parameter pencarian/filter, template, pesan error yang menggema ekspresi). Uji ekspresi read-only: `#{7*7}`, `${7*7}` pada input MILIK SENDIRI. | Output `49` = SpEL injection terbukti (read-only) |
| Konsol H2 terbuka | `GET /h2-console` tanpa auth; periksa apakah halaman login konsol terbuka dan apakah bisa login dengan kredensial default/lemah yang diketahui publik (HANYA bila konsol itu milik target in-scope dan tidak ada data produksi di belakangnya — bila ragu, cukup buktikan halaman terbuka). | Konsol terbuka + login anonim/default berhasil = kandidat |
| Spring4Shell (CVE-2022-22965) | Periksa versi Spring dari error page/header/`/actuator/info` — bila versi rentan (Spring Framework 5.3.0–5.3.17, 5.2.0–5.2.19, atau Spring Boot terkait) DAN aplikasi memakai data binding pada objek non-primitif, catat sebagai kandidat. **JANGAN mengirim payload Spring4Shell (classloader manipulation) ke server target** — buktikan hanya lewat versi + kondisi binding yang teramati. | Versi rentan + data binding terkonfirmasi = kandidat (dampak potensial, tanpa exploit live) |

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = properti sensitif bocor via Actuator / SpEL read-only terbukti / konsol H2 terbuka / versi rentan + binding terkonfirmasi. **TOLAK** = sekadar "Spring Boot terdeteksi" atau "endpoint /actuator/health terbuka" (health biasanya memang publik dan bukan temuan).
2. **Reproduksibilitas:** ulangi minimal 2×; simpan request/response mentah.
3. **Higienitas bukti:** sensor kredensial, kunci, token, dan data pengguna lain sebelum dilampirkan (`[REDACTED]`). JANGAN melampirkan isi heapdump.

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `probing-http-fingerprint` | Fingerprint framework + versi dari header/error page |
| Burp Suite Repeater / `curl` | Akses endpoint Actuator, uji SpEL read-only, periksa konsol H2 |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Framework: [Spring Boot + versi + bukti fingerprint]
Pola diuji: [Actuator / SpEL / H2 / Spring4Shell + hasil]
Pembuktian: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola Spring Boot] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-springboot`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- `/actuator/health` dan `/actuator/info` yang terbuka umumnya BUKAN temuan — fokus pada `env`, `heapdump`, `shutdown`, `mappings`, `configprops`.
- Spring4Shell HANYA diklaim dari versi + kondisi binding — tanpa exploit live, triase bisa meminta bukti lebih; siapkan analisis kondisi binding (parameter yang terikat ke objek) sebagai bukti pendukung.
- Heapdump bisa berisi kredensial dan data pengguna — JANGAN mengunduh atau menyimpan isinya; cukup buktikan endpoint merespons.
