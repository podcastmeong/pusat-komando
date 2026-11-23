# Skill: Serangan Okta-as-IdP — Tenant Discovery, Push Fatigue & Spray per-Protokol

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 54, Claude-BugHunter `okta-attack`, 8 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program bounty enterprise in-scope secara EKSPLISIT mencantumkan organisasi Okta target (atau aplikasi yang memakai Okta sebagai IdP).
- Ditemukan subdomain Okta (`<tenant>.okta.com`, `<tenant>.oktapreview.com`) atau aplikasi yang me-redirect ke Okta untuk login.
- Dipakai SETELAH scope diverifikasi — skill ini HANYA bagian Okta-spesifik; rantai federasi umum ditangani skill lain (lihat "Sudah tercakup").

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan discovery + pengujian alur autentikasi Okta |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Rantai serangan federasi identitas enterprise (SAML/OIDC, confused deputy STS, AssumeRole, manipulasi assertion lintas IdP) → skill `serangan-cloud-iam-entra`.** Skill ini TIDAK mengulang bagian itu — bila temuanmu adalah manipulasi assertion SAML/OIDC atau rantai federasi Entra–Okta, pakai skill tersebut. Skill ini hanya menambah: tenant discovery Okta, enumerasi user, analisis alur autentikasi Okta (enumerasi faktor, push fatigue, bypass SMS), dan spray per-protokol Okta.
- **Metodologi password spray secara umum** (pipeline wordlist → breach → OSINT → spray, taktik lockout umum) → skill `serangan-kredensial-spray`. Skill ini hanya menambah perilaku spray KHUSUS Okta (endpoint `/api/v1/authn`, lockout per-protokol, perbedaan respons antar faktor).
- **Discovery tenant M365** → skill `mcp-osint`. Skill ini hanya discovery tenant OKTA, bukan M365.

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN organisasi Okta tercantum eksplisit.** Bila program hanya mencantumkan aplikasi web tanpa menyebut Okta/IdP, JANGAN sentuh endpoint Okta — itu di luar scope.
2. **Hanya akun sendiri + canary palsu.** Pengujian autentikasi HANYA pada akun uji milik sendiri (atau akun uji yang disediakan program). **DILARANG menguji akun karyawan/pengguna lain — termasuk sekadar memeriksa apakah sebuah username terdaftar.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).** Push fatigue dan SMS bypass TIDAK BOLEH diuji dengan mengirim push/SMS ke perangkat orang lain — hanya ke perangkat/faktor MILIK SENDIRI.
5. **Tanpa DoS / resource exhaustion** — dilarang membanjiri endpoint auth. Spray dibatasi jumlah percobaan kecil (lihat Gerbang 3) dan dihentikan segera bila ada tanda lockout.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Jangan mengubah faktor autentikasi, menonaktifkan MFA, atau mereset password akun mana pun.
11. **Spray HANYA bila scope program secara eksplisit mengizinkan pengujian kredensial.** Bila scope diam atau melarang, spray = DILARANG — cukup laporkan temuan enumerasi/faktor yang terbukti dari analisis alur.

## Langkah + gerbang

### Gerbang 1 — Tenant discovery Okta (pasif)

Standar lulus: tenant teridentifikasi atau dinyatakan "tidak ditemukan" dengan bukti.

1. Dari domain target: cari subdomain Okta (`<tenant>.okta.com`) lewat CT log / `mcp-osint` / halaman login yang me-redirect ke Okta.
2. Dari halaman login Okta: catat `orgUrl`, logo/brand, dan apakah self-service registration aktif.
3. Periksa endpoint publik: `GET https://<tenant>.okta.com/api/v1/org` (info organisasi, biasanya publik) — catat tanpa menyentuh data pengguna.

### Gerbang 2 — Analisis alur autentikasi (akun uji sendiri)

Uji dengan akun uji MILIK SENDIRI pada tenant in-scope. Standar lulus tiap sub-alur: perilaku teramati ATAU dinyatakan tidak ada dengan bukti.

1. **Enumerasi user:** apakah respons login berbeda antara username yang ada vs tidak ada (pesan error, timing, kode status pada `/api/v1/authn`)? Uji HANYA dengan username akun uji sendiri + username palsu yang jelas-jelas bukan milik siapa pun (mis. `tidak-ada-xyz123@...`). JANGAN memakai daftar username karyawan.
2. **Enumerasi faktor:** setelah login akun uji sendiri, apakah API mengembalikan daftar faktor (push, SMS, TOTP, WebAuthn) tanpa otorisasi tambahan? Catat faktor apa saja yang terdaftar untuk AKUN SENDIRI.
3. **Push fatigue:** analisis kebijakan push pada tenant — apakah ada pembatasan jumlah push (number matching / throttling)? Uji HANYA dengan mengirim push ke PERANGKAT SENDIRI, maksimal 3×, dan catat apakah ada number matching atau penolakan setelah percobaan berulang. **JANGAN mengirim push ke perangkat orang lain.**
4. **Bypass SMS:** apakah faktor SMS bisa dilewati/diganti (mis. fallback ke email, atau enroll faktor baru tanpa verifikasi kuat) pada AKUN SENDIRI? Uji hanya pada akun sendiri.
5. **Kebijakan password:** apakah ada lockout, CAPTCHA, atau deteksi anomali setelah percobaan gagal pada akun sendiri? Catat ambang yang teramati (berhenti sebelum lockout permanen).

### Gerbang 3 — Spray per-protokol Okta (hanya bila Aturan keras 11 terpenuhi)

1. **Mode:** endpoint `/api/v1/authn` (primary auth), OAuth `/oauth2/v1/token` (resource owner password grant), dan O365-style bila tenant memakai federasi — satu mode per putaran.
2. **Wordlist:** HANYA password generik yang lemah + password akun uji sendiri yang sengaja dibuat lemah untuk pengujian (mis. `Perusahaan2024!` sebagai password akun uji sendiri). **DILARANG memakai password hasil breach karyawan atau menebak password akun orang lain.**
3. **Disiplin lockout:** maksimal 1 percobaan per akun uji per 10 menit; total maksimal 5 percobaan per akun uji; berhenti segera bila respons menunjukkan lockout/CAPTCHA. Spray ke BANYAK akun = DILARANG — uji hanya 1–2 akun uji milik sendiri.
4. **Deteksi keberhasilan:** login berhasil pada akun uji sendiri dengan password lemah yang sengaja dipasang = bukti kebijakan password lemah (bukan "pembobolan").

### Gerbang 4 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = enumerasi user/faktor terbukti / push tanpa number matching terbukti pada perangkat sendiri / kebijakan password lemah terbukti pada akun sendiri. **TOLAK** = sekadar "tenant Okta ditemukan" atau "endpoint /api/v1/authn merespons".
2. **Reproduksibilitas:** ulangi minimal 2×; simpan respons mentah (dengan token disensor).
3. **Higienitas bukti:** sensor token sesi, nomor telepon, dan data akun sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos keempat gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `mcp-osint` (CT log, subdomain) | Tenant discovery pasif |
| Akun uji sendiri + perangkat/faktor sendiri | Satu-satunya subjek pengujian autentikasi |
| Burp Suite Repeater / `curl` | Uji `/api/v1/authn`, `/oauth2/v1/token`, enumerasi faktor |
| `serangan-kredensial-spray` | Metodologi spray umum (dipakai sebagai referensi, bukan diulang) |
| `~/workspace/catatan/log-bug-bounty.md` | Log alur yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + organisasi Okta in-scope]
Tenant: [orgUrl + bukti discovery]
Alur diuji: [enumerasi user / enumerasi faktor / push / SMS / spray + hasil]
Pembuktian: [apa yang dibuktikan pada akun/perangkat sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Organisasi Okta] - [Kelas: Enumerasi / Push Fatigue / Kebijakan Password] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `okta-attack`, 8 laporan), bukan pengalaman teruji — tiap alur butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Skill ini sengaja TIDAK mengulang rantai federasi** yang sudah ada di `serangan-cloud-iam-entra` — bila temuanmu menyentuh SAML/OIDC lintas IdP, pindah ke skill itu.
- Push fatigue dan SMS bypass hanya bisa dibuktikan pada perangkat/faktor sendiri — dampak terhadap korban hanya bisa diklaim sebagai analisis (kebijakan tanpa number matching + tidak ada throttling), bukan bukti live.
- Okta secara default punya proteksi (threat insight, lockout, CAPTCHA adaptif) — banyak tenant sudah aman; jangan klaim sebelum menguji langsung pada akun sendiri.
