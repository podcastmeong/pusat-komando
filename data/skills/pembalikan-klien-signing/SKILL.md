# Skill: Pembalikan Klien & Signing — Rekonstruksi Penandatanganan Request (PAGAR PALING KETAT)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 61, Agentic-Bug-Hunter `client-reverse` — request-signing / anti-bot token reversal), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## ⚠️ PAGAR PALING KETAT — BACA DULU SEBELUM MEMAKAI SKILL INI

Skill ini menyentuh rekayasa balik klien (aplikasi Android, JS browser, klien desktop) — area yang rawan keluar dari scope dan rawan disalahartikan sebagai upaya mengakali perlindungan anti-bot/anti-otomasi.

1. **HANYA bila scope program secara EKSPLISIT mengizinkan pengujian API di balik klien tersebut.** Bila scope hanya mencantumkan "website" tanpa menyebut aplikasi mobile/API-nya, JANGAN membalik klien mobile-nya. Bila scope melarang pengujian anti-bot/anti-otomasi, JANGAN pakai skill ini.
2. **HANYA akun uji sendiri.** Semua request replay memakai sesi/akun uji MILIK SENDIRI. **DILARANG menguji dengan sesi/akun korban, dan DILARANG mereplay request yang berisi data orang lain.**
3. **Tanpa uji korban.** Segala bentuk pengujian terhadap akun/sesi orang lain DILARANG, tanpa pengecualian.
4. **Tanpa follow-up yang pernah diblokir.** Bila sebuah teknik replay / endpoint / akun pernah diblokir (WAF, deteksi bot, pemblokiran perangkat, peringatan program), JANGAN pernah mengulanginya dalam bentuk apa pun — jangan ganti device ID, jangan ganti signature, jangan ganti jalur untuk mengakali blokir tersebut.
5. **Jangan membobol perlindungan untuk tujuan selain pengujian API in-scope.** Rekonstruksi signing HANYA untuk menguji API di belakangnya (mencari IDOR, BOLA, logika bisnis) — BUKAN untuk melewati paywall, mengotomasi penyalahgunaan, membuat bot, atau mengakali lisensi/pembayaran.
6. **Jangan mendistribusikan hasil rekayasa balik.** Kode signing yang direkonstruksi, kunci yang diekstrak, dan token yang dihasilkan HANYA dipakai di sesi uji sendiri dan dicatat di log internal — JANGAN dibagikan ke publik, jangan dimasukkan utuh ke laporan (cukup deskripsikan metodenya), jangan dipakai di luar program ini.

## Pemicu (kapan dipakai)

- API target in-scope hanya bisa diakses lewat klien (Android/JS/desktop) yang menandatangani/mengenkripsi request-nya, sehingga Burp tidak bisa langsung me-replay.
- Ditemukan signature, enkripsi, token status, device binding, atau logika anti-otomasi yang memblokir replay request.
- Dipakai SETELAH `analisis-statis-js` / `dekompilasi-aplikasi-mobile` (analisis statis) menunjukkan di mana letak pemblokirannya — skill ini adalah langkah LANJUTAN (rekonstruksi), bukan langkah pertama.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menangkap traffic + merekonstruksi signing/enkripsi |
| Audit | **A60 Security Auditor** | Memeriksa izin scope + apakah pagar ketat dipatuhi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase — Muse berhak MELARANG rekonstruksi kapan saja |

## Sudah tercakup (jangan diduplikat)

- **Analisis statis file JS** (bedah kode, cari endpoint/secret) → skill `analisis-statis-js`. Skill ini TIDAK mengulang analisis statis — hanya rekonstruksi signing agar replay bisa berjalan.
- **Dekompilasi APK statis** (ekstraksi endpoint/secret dari APK) → skill `dekompilasi-aplikasi-mobile`. Skill ini TIDAK mengulang bedah statis APK — hanya rekonstruksi signing/enkripsi klien mobile.
- **Pipeline APK ujung-ke-ujung** (akuisisi, Frida runtime, intent injection) → skill `pipeline-redteam-apk`. Skill ini fokus pada signing/request, bukan pipeline mobile.

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN scope secara eksplisit mengizinkan pengujian API/klien tersebut.** Verifikasi dan catat kutipan scope-nya sebelum mulai.
2. **Hanya akun sendiri + canary palsu.** Replay HANYA dengan sesi/akun uji sendiri; request yang direplay HANYA berisi data uji sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang membanjiri API dengan replay.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).** Rekonstruksi signing TIDAK BOLEH berjalan otomatis tanpa pengawasan — tiap langkah diputuskan manusia.
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — replay HANYA request baca atau request yang mengubah data MILIK SENDIRI. JANGAN mereplay request yang mengubah/menghapus data orang lain.
11. **Tanpa follow-up yang pernah diblokir.** Teknik replay / endpoint / perangkat yang pernah diblokir = JANGAN PERNAH diulang.
12. **Jangan mendistribusikan hasil rekayasa balik** (lihat Pagar 6 di atas).

## Langkah + gerbang

### Gerbang 0 — Verifikasi izin (STOP bila tidak ada)

1. Baca pasal scope program. Pastikan API/klien yang akan dibalik tercantum in-scope dan pengujian anti-bot/anti-otomasi tidak dilarang.
2. Salin kutipan scope-nya ke log. Bila tidak ada izin eksplisit → STOP.

### Gerbang 1 — Packet-first: tangkap traffic nyata (observasi dulu)

Prinsip: **observasi dulu, reverse hanya pada titik yang memblokir.** Jangan membalik seluruh aplikasi — hanya titik yang menghalangi replay.

1. Tangkap traffic klien (Android: proxy + sertifikat uji sendiri; browser: DevTools/Burp; desktop: proxy sistem) saat klien melakukan SATU aksi biasa dengan AKUN UJI SENDIRI.
2. Catat request mentah: method, path, header (termasuk header signature/token/device), body (termasuk field terenkripsi).
3. Replay request mentah itu apa adanya via Burp/curl — apakah server menerimanya? Bila YA, tidak perlu reverse — langsung uji API-nya (lihat Gerbang 4). Bila TIDAK (401/403/ditolak), lanjut ke Gerbang 2.

### Gerbang 2 — Analisis titik pemblokiran

Identifikasi APA yang membuat replay gagal, dengan analisis statis (lihat `analisis-statis-js` / `dekompilasi-aplikasi-mobile`):

| Titik pemblokiran | Yang dicari |
|---|---|
| Signature (HMAC/dll.) | Header signature dihitung dari apa (method + path + body + timestamp + secret)? Di mana secret-nya (hardcoded di klien / diambil dari server saat login)? |
| Enkripsi body | Algoritme + kunci apa (AES-GCM, RSA)? Kunci dari mana (hardcoded / handshake)? |
| Token status | Token sekali pakai / nonce yang berubah tiap request? Dari mana token itu didapat (endpoint token)? |
| Device binding | Apakah request terikat device ID / sertifikat perangkat? Apakah device ID bisa dibuat untuk perangkat uji sendiri? |
| Logika anti-otomasi | Apakah ada tantangan (CAPTCHA, proof-of-work, attestation) yang harus dilewati? Bila ya — STOP: jangan mengakali tantangan anti-bot; catat sebagai batas dan pindah ke jalur lain. |

### Gerbang 3 — Rekonstruksi signing/enkripsi (hanya titik yang memblokir)

1. Tulis ulang fungsi signing/enkripsi dalam skrip lokal (Python/Node) — HANYA fungsi yang diperlukan untuk membuat SATU request valid dari sesi uji sendiri.
2. Uji skrip itu: hasilkan request yang ditandatangani untuk aksi BACA milik sendiri → kirim → apakah server menerimanya (200)? Bila ya, replay stabil tercapai.
3. **Batasan rekonstruksi:** jangan mengekstrak kunci privat perangkat / sertifikat hardware; jangan membalik attestation (SafetyNet/Play Integrity/App Attest) — bila titik pemblokirannya adalah attestation perangkat, STOP dan catat sebagai batas (bukan kegagalan — itu di luar pagar skill ini).
4. Simpan skrip rekonstruksi di log internal saja; JANGAN lampirkan utuh ke laporan — deskripsikan metodenya saja (Pagar 6).

### Gerbang 4 — Pengujian API di belakangnya (tujuan sebenarnya skill ini)

Dengan replay yang stabil, uji API seperti biasa dengan skill perburuan yang sesuai (IDOR/BOLA, logika bisnis, otorisasi) — TETAP dengan akun uji sendiri dan data sendiri. Temuan yang dihasilkan dilaporkan lewat skill perburuan itu, BUKAN lewat skill ini. Skill ini hanya membuka jalannya.

### Gerbang 5 — Gerbang validasi (sebelum maju ke skill perburuan)

1. **Replay stabil terbukti:** request yang direkonstruksi diterima server (200) pada aksi baca milik sendiri, minimal 2×.
2. **Pagar dipatuhi:** tidak ada data orang lain, tidak ada tantangan anti-bot yang diakali, tidak ada attestation yang dibobol, tidak ada follow-up yang pernah diblokir.
3. **Higienitas bukti:** sensor token, signature, kunci, dan device ID sebelum dicatat (`[REDACTED]`). JANGAN catat kunci signing utuh di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Burp Suite / mitmproxy + sertifikat uji sendiri | Tangkap traffic klien (akun uji sendiri) |
| `analisis-statis-js` / `dekompilasi-aplikasi-mobile` | Analisis statis titik pemblokiran |
| Python/Node (skrip lokal) | Rekonstruksi fungsi signing/enkripsi untuk sesi sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log titik pemblokiran + hasil rekonstruksi (tanpa kunci utuh) |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + API/klien in-scope]
Izin scope: [kutipan scope yang mengizinkan pengujian API/klien ini]
Titik pemblokiran: [signature / enkripsi / token / device binding / anti-otomasi + lokasi]
Rekonstruksi: [fungsi yang ditulis ulang + hasil uji replay (200 ya/tidak)]
API yang diuji sesudahnya: [skill perburuan yang dipakai + temuan]
Keputusan gerbang: [lolos / ditolak / STOP-batas + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter `client-reverse`), bukan pengalaman teruji — skill ini butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Pagar skill ini adalah yang paling ketat bersama `serangan-kredensial-spray`.** Bila ada keraguan apakah suatu langkah melanggar pagar — ANGGAP MELANGGAR, berhenti, dan tanyakan ke Muse.
- Attestation perangkat (SafetyNet/Play Integrity/App Attest) dan tantangan anti-bot (CAPTCHA/proof-of-work) adalah BATAS skill ini — jangan diakali; catat sebagai batas dan pindah jalur.
- Rekonstruksi signing bukan temuan bounty dengan sendirinya — nilainya ada pada API yang berhasil diuji sesudahnya. Bila setelah replay stabil tidak ditemukan apa-apa di API, hasilnya tetap "tidak ada temuan" — jangan laporkan rekonstruksinya sebagai temuan.
- Kunci/secret yang ditemukan hardcoded di klien JANGAN dipakai di luar sesi uji dan JANGAN didistribusikan — bila kunci itu sendiri adalah temuan (mis. secret global yang membocorkan data), laporkan keberadaannya lewat `dorking-secret-github` / skill yang sesuai, tanpa melampirkan nilainya.
