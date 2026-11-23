# Skill: Perburuan HTTP Request Smuggling — Desinkronisasi Parser CL/TE

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 51, Claude-BugHunter `hunt-http-smuggling`, 12 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai arsitektur front-end proxy/load balancer + back-end server (dua parser HTTP berbeda).
- Ditemukan endpoint yang menerima `Content-Length` dan/atau `Transfer-Encoding` dari klien.
- Ditemukan respons yang tercampur, cache yang berperilaku aneh, atau request yang "tertinggal" di log.
- Dipakai SETELAH `fondasi-kerentanan-web-api` dikuasai — skill ini hanya menambah kelas smuggling, bukan menggantikan fondasi HTTP.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan deteksi desinkronisasi + pembuktian dampak smuggling |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Race condition via satu paket HTTP/2 (timing, bukan desinkronisasi parser) → skill `serangan-paket-tunggal-http2`. **Smuggling ≠ race:** smuggling soal dua parser yang menafsirkan panjang request secara berbeda; race soal urutan eksekusi. Jangan campur keduanya dalam satu laporan.
- Cache poisoning secara umum (racun cache lewat header lain) → skill `peracunan-cache`. Skill ini hanya memakai cache poisoning sebagai SATU dampak smuggling, bukan mengulang metodologinya.
- "Smuggling" di konteks LLM (ASCII smuggling, token smuggling) → skill `transfer-hunting` / `alat-l1b3rt4s`. Itu soal konten model, bukan parser HTTP — tidak ada hubungannya dengan skill ini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri; request smuggling uji HANYA berisi canary milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau meracuni koneksi bersama. **Smuggling yang memblokir koneksi keep-alive pengguna lain = STOP.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Jangan menyelundupkan request yang mengubah state (POST destruktif, hapus akun, transfer) — buktikan desinkronisasi dengan request baca saja.
11. **Satu koneksi uji, satu desinkronisasi.** Jangan membanjiri server dengan varian smuggling; tiap varian diuji sekali, tunggu respons/timeout, catat, baru lanjut.

## Langkah + gerbang

### Gerbang 1 — Pemetaan arsitektur front-end / back-end

Identifikasi pasangan parser sebelum menguji. Standar lulus: front-end dan back-end teridentifikasi atau dinyatakan "tidak dapat dipetakan" dengan bukti.

1. **Header server:** `Server`, `Via`, `X-Powered-By`, `CF-RAY`/`X-Cache` — tebak front-end (CDN/WAF/proxy) dan back-end (Apache/Nginx/Node/Tomcat).
2. **Perilaku TE/CL:** kirim request normal dengan `Transfer-Encoding: chunked` dan dengan `Content-Length` — apakah server menerima keduanya? Apakah salah satu ditolak/dinormalisasi?
3. **Dukungan HTTP/2:** apakah endpoint melayani H2 (h2c/h2)? Bila ya, catat varian H2.CL dan H2.TE sebagai kandidat.

### Gerbang 2 — Deteksi desinkronisasi (varian uji, satu per satu)

Uji tiap varian dengan request baca (GET) yang disisipkan sebagai "request kedua" yang diselundupkan, berisi canary milik sendiri. Standar lulus tiap varian: desinkronisasi teramati (respons tertunda/tercampur, request kedua dieksekusi sebagai request terpisah) ATAU dinyatakan tidak ada dengan bukti negatif.

| Varian | Pola | Yang diamati |
|---|---|---|
| CL.TE | `Content-Length` + `Transfer-Encoding: chunked` | Front-end pakai CL, back-end pakai TE (atau sebaliknya) |
| TE.CL | `Transfer-Encoding` + `Content-Length` | Kebalikan CL.TE |
| TE obfuscation | `Transfer-Encoding: xchunked`, `Transfer-Encoding : chunked` (spasi), `Transfer-Encoding: chunked\r\nTransfer-Encoding: identity` | Parser yang menormalisasi header secara berbeda |
| H2.CL | HTTP/2 request dengan `Content-Length` yang tidak cocok | Downgrade H2 → HTTP/1.1 di back-end |
| H2.TE | HTTP/2 request dengan `Transfer-Encoding` | Back-end HTTP/1.1 menafsirkan TE dari H2 |

Teknik deteksi aman: kirim request smuggling + request "korban" dari SESI SENDIRI pada koneksi yang sama; bila respons request korban berisi canary dari request smuggling = desinkronisasi terbukti. Gunakan tool `smuggler.py` (PortSwigger) atau skrip `curl --raw` manual — satu varian per koneksi, jeda antar uji.

### Gerbang 3 — Pembuktian dampak (tanpa mengganggu pengguna lain)

Pilih SATU dampak, buktikan dengan sesi sendiri saja:

- **Cache poisoning via smuggling:** request yang diselundupkan membuat cache menyimpan respons beracun untuk URL milik sendiri; buktikan cache key teracuni lalu minta cache dibersihkan (atau tunggu TTL habis). JANGAN meracuni cache URL yang dipakai pengguna lain.
- **Bypass ACL/WAF:** request yang diselundupkan mencapai endpoint internal/admin dari sesi sendiri (bukti: respons 200 pada path yang normalnya 403 — hanya baca, tanpa mengubah state).
- **Hijack request pengguna lain:** JANGAN DIBUKTIKAN secara live. Cukup buktikan desinkronisasi + tunjukkan secara logis bahwa request berikutnya di koneksi yang sama akan dieksekusi sebagai penyerang. Klaim "bisa membajak sesi korban" tanpa bukti live = jelaskan sebagai dampak potensial di laporan, bukan sebagai terbukti.

### Gerbang 4 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = desinkronisasi terbukti + satu dampak (cache poisoning/bypass) terbukti pada sesi sendiri. **TOLAK** = sekadar "server menerima header aneh" tanpa desinkronisasi yang teramati.
2. **Reproduksibilitas:** ulangi varian yang sama minimal 2×; simpan request/response mentah.
3. **Higienitas bukti:** sensor token sesi dan data pribadi sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos keempat gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `smuggler.py` (PortSwigger) / skrip `curl --raw` | Deteksi desinkronisasi CL.TE / TE.CL / H2 |
| Burp Suite Repeater (manual) | Kirim varian satu per satu, amati respons/timeout |
| Dua sesi uji sendiri pada koneksi yang sama | Pembuktian desinkronisasi tanpa melibatkan pengguna lain |
| `~/workspace/catatan/log-bug-bounty.md` | Log varian yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Arsitektur: [front-end] | [back-end] | [HTTP/2 ya/tidak]
Varian diuji: [CL.TE / TE.CL / ... + hasil tiap varian]
Pembuktian dampak: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - HTTP Request Smuggling ([Varian]) menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-http-smuggling`, 12 laporan), bukan pengalaman teruji — tiap varian butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Desinkronisasi sering tidak stabil: hasil bisa berbeda antar koneksi/CDN edge — ulangi 2× sebelum menyimpulkan, dan catat edge/region bila relevan.
- WAF/CDN modern (Cloudflare, Akamai) menormalisasi CL/TE sebelum sampai ke back-end — varian klasik sering sudah mati di sana; fokus pada arsitektur tanpa normalisasi atau pada H2 downgrade.
- Smuggling yang salah sasaran bisa meracuni koneksi bersama — patuhi Aturan keras 5 dan 11: satu varian per koneksi, request baca saja, berhenti bila server merespons aneh.
