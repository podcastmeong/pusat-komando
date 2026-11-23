# Skill: Perburuan Framework Node.js — Prototype Pollution, Trust Proxy & SSTI Template Engine

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 53, Claude-BugHunter `hunt-nodejs`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target teridentifikasi memakai Node.js (header `X-Powered-By: Express`, cookie `connect.sid`, error stack `node_modules`, `at Object.<anonymous>`).
- Ditemukan endpoint yang menerima JSON bertingkat (merge objek) atau memakai template engine (EJS, Pug, Handlebars, Nunjucks).
- Dipakai SETELAH framework teridentifikasi via fingerprint (`probing-http-fingerprint`) — jangan menebak framework.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprint + pengujian pola khas Node.js |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- SSTI secara umum (identifikasi engine, payload generik) → skill `injeksi-template-ssti`. Skill ini HANYA SSTI pada template engine Node.js (EJS/Pug/Handlebars/Nunjucks) dan rantainya ke RCE — bukan mengulang identifikasi SSTI umum.
- Kelas kerentanan umum (SQLi, XSS, IDOR) → skill `fondasi-kerentanan-web-api`.
- Lihat juga skill framework lain bila target memakai banyak stack: `perburuan-framework-aspnet`, `perburuan-framework-laravel`, `perburuan-framework-nextjs`, `perburuan-framework-springboot`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan. **Prototype pollution yang meracuni `Object.prototype` secara global = DILARANG bila memengaruhi pengguna lain;** uji HANYA di endpoint yang terisolasi per-request atau buktikan lewat respons sesi sendiri tanpa meracuni state global.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG:** RCE live via prototype pollution / SSTI (mis. `child_process.exec`) — buktikan polusi/SSTI dengan canary read-only (mis. properti `__proto__.canary` terbaca kembali di respons sesi sendiri, atau output template `7*7=49`), bukan eksekusi perintah.

## Langkah + gerbang

### Gerbang 1 — Fingerprint Node.js / Express

Standar lulus: runtime + template engine teridentifikasi atau dinyatakan "bukan Node.js" dengan bukti.

1. Header/cookie: `X-Powered-By: Express`, `connect.sid`, `set-cookie` dengan `Path=/; HttpOnly`.
2. Error stack: `node_modules`, `at Object.<anonymous>`, `Error: Cannot find module`.
3. Template engine: error page yang menyebut EJS/Pug/Handlebars/Nunjucks, atau pola render khas di respons.

### Gerbang 2 — Pola khas (uji satu per satu, read-only / sesi sendiri)

| Pola | Cara uji aman | Indikator |
|---|---|---|
| Prototype pollution | Kirim JSON bertingkat dengan kunci `__proto__` / `constructor.prototype` berisi canary (`{"__proto__": {"canary": "POLLUTED-OWN-TEST"}}`) ke endpoint merge/update MILIK SENDIRI. Periksa apakah `Object.prototype.canary` terbaca kembali di respons SESI SENDIRI. Bila endpoint memakai merge rekursif tanpa proteksi, polusi terjadi. **STOP bila polusi memengaruhi state global bersama** — laporkan sebagai kandidat tanpa mengulang. | Canary terbaca kembali dari `Object.prototype` = kandidat |
| Prototype pollution → RCE (rantai) | JANGAN eksekusi RCE. Tunjukkan rantai secara logis: polusi terbukti + library yang memakai properti terpolusi (mis. `exec`, `spawn` option) ada di stack — cukup sebagai analisis dampak di laporan, bukan bukti live. | Polusi + jalur ke eksekusi teridentifikasi di kode publik/dokumentasi = kandidat (dampak potensial) |
| Salah konfigurasi trust proxy Express | Uji apakah aplikasi mempercayai `X-Forwarded-For` / `X-Forwarded-Proto` dari klien: kirim request dengan `X-Forwarded-For: <IP-canary>` dan `X-Forwarded-Proto: https` ke endpoint yang memakai IP untuk rate-limit/allowlist (mis. login, reset password) dari SESI SENDIRI. | Rate-limit/allowlist bisa dilewati dengan header palsu = kandidat |
| SSTI template engine Node.js | Identifikasi engine dulu (lihat `injeksi-template-ssti`), lalu uji payload read-only khas engine: EJS `<%= 7*7 %>`, Pug `#{7*7}`, Handlebars `{{7*7}}`, Nunjucks `{{7*7}}` — pada input MILIK SENDIRI. | Output `49` di respons = SSTI terbukti (read-only); lanjutkan ke analisis RCE hanya sebagai dampak potensial, tanpa eksekusi |

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = polusi canary terbaca kembali / trust proxy dilewati / SSTI read-only terbukti — dengan bukti pada sesi sendiri. **TOLAK** = sekadar "Express terdeteksi" atau "JSON diterima".
2. **Reproduksibilitas:** ulangi minimal 2×; simpan request/response mentah.
3. **Higienitas bukti:** sensor token sesi dan data pribadi sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `probing-http-fingerprint` | Fingerprint runtime + template engine |
| Burp Suite Repeater | Kirim JSON `__proto__`, header `X-Forwarded-*`, payload SSTI read-only |
| `injeksi-template-ssti` | Identifikasi engine + payload generik (dipakai sebagai referensi, bukan diulang) |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Framework: [Node.js/Express + template engine + bukti fingerprint]
Pola diuji: [prototype pollution / trust proxy / SSTI + hasil]
Pembuktian: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola Node.js] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-nodejs`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Prototype pollution pada aplikasi modern sering sudah dicegah (Object.freeze, merge yang aman, `__proto__` difilter) — jangan klaim sebelum canary terbaca kembali.
- Trust proxy hanya berdampak bila aplikasi BENAR-BENAR memakai IP dari header untuk keputusan keamanan (rate-limit, allowlist, logging) — bila IP hanya dipakai untuk logging, dampaknya rendah dan kemungkinan besar ditolak triase.
- SSTI → RCE pada template engine Node.js adalah dampak potensial yang TIDAK dibuktikan live — jelaskan rantai secara logis di laporan, jangan eksekusi perintah.
