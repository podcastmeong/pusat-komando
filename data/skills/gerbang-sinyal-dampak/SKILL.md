# Skill: Gerbang Sinyal-Dampak — Sinyal Rendah Hanya Lolos Bila Dampak Nyatanya Terbukti

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` Bagian 1 (Signal-to-Impact Gate). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu kandidat yang lolos gerbang ini dan dicatat di log.

## Pemicu (Trigger & Scope)

Dipakai setiap kali ada kandidat temuan yang sudah LULUS `gerbang-tujuh-pertanyaan-triase` tetapi sinyalnya masih RENDAH — yaitu temuan yang "kelihatan ada celah" namun dampaknya belum terbukti — **sebelum** `skeptic-false-positive-eliminator` dan **sebelum** `eskalasi-dampak-otomatis`. Satu kandidat = satu kali lewat tabel sinyal di bawah. Tidak ada jalan pintas, tidak ada "kelihatannya berdampak".

Skill ini adalah **gerbang eskalasi**: tugasnya membuang sinyal yang tidak memenuhi syarat eskalasi nyata, supaya tenaga tidak habis untuk membuktikan rantai yang dari awal tidak punya ujung. Skill ini TIDAK menilai seberapa besar hadiahnya (itu tugas `triase-duplikat`) dan TIDAK membantah temuan secara adversarial (itu tugas `skeptic-false-positive-eliminator`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menjalankan tabel sinyal, memutuskan LULUS / TOLAK beserta alasan |
| Audit | **A60 Security Auditor** | Memeriksa verdict gerbang; A60 tidak meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan kandidat maju ke skeptic atau dibuang |

## Sudah tercakup (jangan diduplikat)

- **Daftar noise umum** (missing headers, info versi, Self-XSS, data publik, rate-limit, halaman error generik, SPF/DMARC/DKIM, clickjacking non-sensitif) ada di `gerbang-tujuh-pertanyaan-triase` Pertanyaan 4 dan `skeptic-false-positive-eliminator` Gerbang 2 — skill ini TIDAK mengulang daftar itu. Tabel di bawah hanya berisi sinyal yang **LOLOS** kedua daftar itu tetapi masih belum membuktikan dampak — sinyal yang butuh pembuktian dampak spesifik per jenis, bukan sekadar "bukan noise".
- **Dampak bisnis generik + trust boundary** ada di `skeptic-false-positive-eliminator` Gerbang 3 dan `gerbang-tujuh-pertanyaan-triase` Pertanyaan 5–6 — skill ini TIDAK mengulang pertanyaan generik itu. Yang ditambahkan di sini adalah **syarat eskalasi nyata per jenis sinyal** (mis. Open Redirect hanya valid pada alur sensitif + bocor token/kode), yang tidak ada di kedua skill itu.
- **Katalog rantai eskalasi** (apa yang diuji SESUDAH temuan rendah terbukti) ada di `eskalasi-dampak-otomatis` — skill ini berjalan SEBELUM eskalasi: sinyal yang gagal di sini tidak pernah sampai ke eskalasi, karena tidak ada yang bisa dirangkai dari sinyal tanpa dampak.
- **Teknik bukti aman per jenis celah** ada di `verifikasi-poc-aman` — Probe Steps di bawah MEMAKAI teknik itu, bukan mengulang caranya.
- Alur sesudah skill ini: LULUS → `skeptic-false-positive-eliminator` (4 gerbang) → `triase-duplikat` (cek duplikat + skor) → draf laporan (`laporan-poc-otomatis`) → tinjau manusia → persetujuan Cipta → kirim. TOLAK → catat alasan di log, kembali ke riset/varian. Bila temuan LULUS tetapi triase memberi skor rendah, barulah `eskalasi-dampak-otomatis` mencoba rantai lanjutan.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = TOLAK, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.** LULUS di gerbang ini bukan izin kirim — izin kirim tetap dari Cipta.
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian aman dan read-only; bukti baca, callback canary, `document.domain` — tanpa perintah yang menulis/menghapus di server.
8. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, tanpa payload.
9. **Jangan membesar-besarkan severity.** Hanya dampak yang TERBUKTI lewat Probe Steps yang boleh diklaim; "mungkin bisa" = belum terbukti = TOLAK.
10. **Satu sinyal gagal = TOLAK.** Tidak ada "lolos sebagian". Bedakan jenis penolakan (lihat Gerbang Akhir): TOLAK PERMANEN (buang) vs TOLAK SEMENTARA (boleh kembali sebagai kandidat baru dengan bukti baru, bukan dengan mengubah verdict).
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Methodology — tabel sinyal, Probe Steps, dan Execution Gate

Untuk tiap kandidat, cocokkan sinyalnya dengan SATU baris tabel di bawah. Jalankan Probe Steps baris itu, lalu terapkan Execution Gate-nya. Sinyal yang tidak ada di tabel = bukan sinyal rendah yang dikenal — serahkan ke A60 untuk diputuskan baris baru atau langsung ke `skeptic-false-positive-eliminator`; jangan mengarang syarat eskalasi sendiri.

### Baris 1 — Open Redirect

- **Signal:** ada parameter (`next`, `redirect`, `return`, `url`, atau sejenisnya) yang mengarahkan browser ke domain luar yang dipilih penyerang — redirect-nya sendiri terbukti terjadi (respons 302 / Location ke domain luar).
- **Probe Steps:**
  1. Ganti alamat redirect dengan callback canary milik sendiri pada alur BIASA (mis. redirect sesudah login biasa). Catat: apakah ada data sensitif yang ikut terkirim ke canary? (Biasanya tidak.)
  2. Ulangi pada alur SENSITIF: (a) `redirect_uri` OAuth / OpenID Connect — minta authorization code dengan `redirect_uri` = canary milik sendiri; (b) tautan reset kata sandi — minta token reset dengan parameter `redirect` / `Referer` mengarah ke canary milik sendiri.
  3. Periksa canary: apakah `authorization code`, token reset, atau token sesi benar-benar TIBA di canary? Simpan hit canary + pasangan Request/Response dengan reference ID.
- **Execution Gate:** **LULUS hanya bila** redirect terjadi pada alur sensitif (OAuth `redirect_uri` ATAU reset kata sandi) **DAN** kode/token TERBUKTI tiba di canary. **TOLAK PERMANEN bila** redirect hanya mengarahkan ke situs luar tanpa membocorkan kode/token apa pun (Open Redirect telanjang — "korban bisa diarahkan ke situs phishing" saja bukan dampak yang dibayar). Bila alur sensitif belum sempat diuji = **TOLAK SEMENTARA** — uji dulu, jangan loloskan dari dugaan.

### Baris 2 — CORS Reflects Origin

- **Signal:** server merefleksikan header `Origin` penyerang ke `Access-Control-Allow-Origin` (respons mengandung origin penyerang).
- **Probe Steps:**
  1. Kirim permintaan lintas situs dari origin milik sendiri dengan kredensial (sesi akun kedua milik sendiri): cek apakah `Access-Control-Allow-Credentials: true` ikut dikembalikan.
  2. Baca respons lintas situs itu: apakah berisi data terautentikasi (data akun, token, isi yang hanya muncul bila login)?
- **Execution Gate:** **LULUS hanya bila** `Allow-Credentials: true` **DAN** data terautentikasi TERBUKTI terbaca lintas situs. **TOLAK PERMANEN bila** origin direfleksikan tanpa `Allow-Credentials: true` (refleksi saja tanpa kredensial tidak mencuri apa pun).

### Baris 3 — IDOR Read-Only

- **Signal:** objek milik akun lain terbaca dengan mengubah pengenal (ID di URL/parameter) memakai sesi akun sendiri.
- **Probe Steps:**
  1. Buktikan dengan DUA akun sendiri (akun A meminta objek milik akun B) — satu akun saja TIDAK cukup.
  2. Periksa isi objek yang terbaca: apakah berisi data sensitif (bukan data publik / data yang memang dibagikan)?
  3. Catat: uji tulis (PUT / PATCH / DELETE) pada endpoint yang sama adalah tugas `eskalasi-dampak-otomatis` SESUDAH temuan ini lolos — bukan syarat lolos di sini.
- **Execution Gate:** **LULUS bila** data sensitif akun lain TERBUKTI terbaca oleh akun yang tidak berhak. **TOLAK PERMANEN bila** yang terbaca hanya data publik atau data milik sendiri yang diakses dengan cara tidak biasa. Read-only yang terbukti BUKAN alasan tolak — jangan menuntut eskalasi tulis sebagai syarat lolos.

### Baris 4 — Kebocoran token / CSRF / nonce kecil

- **Signal:** respons server mengandung token, CSRF token, nonce, atau nilai sekali pakai yang terlihat bisa dipakai ulang.
- **Probe Steps:**
  1. Ambil nilai yang bocor itu dan PAKAI untuk satu aksi tanpa sah pada akun kedua milik sendiri (mis. token CSRF korban dipakai dari sesi penyerang untuk mengubah data akun korban — keduanya milik sendiri).
  2. Verifikasi perubahan status nyata di server (State Verification), bukan sekadar pesan sukses.
- **Execution Gate:** **LULUS hanya bila** nilai yang bocor TERBUKTI dipakai untuk aksi tanpa sah. **TOLAK PERMANEN bila** nilai itu hanya terlihat di respons tetapi tidak bisa dipakai untuk aksi apa pun (mis. sudah kedaluwarsa, terikat sesi lain, atau hanya nilai acak tanpa fungsi).

### Baris 5 — Debug / Error Endpoint (kebocoran variabel lingkungan)

- **Signal:** endpoint debug / halaman error mengembalikan stack trace, variabel lingkungan, atau isi konfigurasi.
- **Probe Steps:**
  1. Baca isi yang bocor: apakah ada kunci API, kredensial infrastruktur cloud, `.env`, atau rahasia nyata — atau hanya nama file / nomor baris / jejak tumpukan tanpa rahasia?
  2. Bila ada rahasia: buktikan rahasia itu AKTIF (mis. kunci API dipakai untuk membaca data canary milik sendiri — jangan dipakai pada data orang lain).
- **Execution Gate:** **LULUS hanya bila** rahasia nyata TERBUKTI bocor (dan bila diuji, terbukti aktif). **TOLAK PERMANEN bila** yang bocor hanya stack trace / nama file / pesan error tanpa rahasia.

### Baris 6 — S3 Bucket Listing / penyimpanan terbuka

- **Signal:** bucket / penyimpanan cloud bisa di-listing dari luar (daftar objek terlihat).
- **Probe Steps:**
  1. Periksa isi listing: apakah ada berkas sensitif (cadangan database, kunci, JS bundle berisi `client_secret` OAuth) — atau hanya berkas publik (gambar, aset statis)?
  2. Bila ada berkas sensitif: unduh SALINAN-nya saja (read-only) dan buktikan isinya sensitif (mis. `client_secret` terbaca); jangan ubah/hapus isi bucket.
- **Execution Gate:** **LULUS hanya bila** berkas sensitif TERBUKTI bisa diakses (bukan sekadar listing terlihat). **TOLAK PERMANEN bila** listing hanya menampilkan berkas publik. Bila ada `client_secret` yang terbukti, eskalasi ke pembajakan SSO/OAuth menjadi tugas `eskalasi-dampak-otomatis`.

### Baris yang SUDAH diputuskan di skill lain (jangan probe ulang)

| Sinyal | Sudah diputuskan di | Keputusan |
|---|---|---|
| Source map tanpa kredensial | `daftar-tolak-selalu` | TOLAK PERMANEN — tidak sampai ke gerbang ini |
| Dead code (celah di kode tak tereksekusi) | `daftar-tolak-selalu` | TOLAK PERMANEN — tidak sampai ke gerbang ini |
| Bug butuh 4+ prasyarat tidak realistis | `daftar-tolak-selalu` | TOLAK PERMANEN — tidak sampai ke gerbang ini |
| Missing headers / info versi / Self-XSS / data publik / rate-limit / error generik | `gerbang-tujuh-pertanyaan-triase` Q4, `skeptic-false-positive-eliminator` Gerbang 2 | TOLAK PERMANEN — tidak sampai ke gerbang ini |

## Gerbang Akhir — Verdict

- **LULUS** — sinyal cocok dengan satu baris tabel DAN Execution Gate baris itu terpenuhi dengan bukti ber-reference-ID → kandidat maju ke `skeptic-false-positive-eliminator`.
- **TOLAK PERMANEN** — Execution Gate gagal karena syarat eskalasi tidak ada (mis. Open Redirect telanjang tanpa alur sensitif; CORS tanpa credentials) → kandidat dibuang; catat alasan di log; jangan ajukan lagi dengan bukti yang sama.
- **TOLAK SEMENTARA** — Probe Steps belum lengkap (alur sensitif belum diuji, canary belum diperiksa) → kandidat boleh kembali sebagai kandidat BARU dengan bukti baru; verdict lama tidak diubah.

## Validation Gate (verifikasi deterministik baseline vs exploit)

- Baseline: perilaku normal tanpa payload HARUS berbeda dari perilaku exploit (mis. `redirect_uri` ke domain tepercaya → kode TIDAK bocor; respons tanpa kredensial → data TIDAK terbaca lintas situs). Bila perilaku exploit sama dengan baseline, langkah itu bukan celah.
- Exploit: bukti dampak (kode/token tiba di canary, data terbaca lintas situs) HARUS terulang dari sesi bersih + token segar, minimal 1 kali pengulangan sesudah pembuktian pertama.
- Verdict LULUS hanya sah bila perbandingan baseline-vs-exploit tertulis di log dengan reference ID bukti keduanya.

## Alat

| Alat | Cara pakai |
|---|---|
| Server canary sendiri (Interactsh / canary milik sendiri) | Menerima callback untuk Open Redirect / OAuth / reset kata sandi — catat hit-nya saja, jangan ambil isinya |
| Dua akun uji sendiri (penyerang + korban) | Wajib — kedua sisi pembuktian memakai akun milik sendiri |
| Sesi HTTP bersih (`curl` / skrip Python, sesi baru + token segar) | Pengulangan bukti dampak (Validation Gate) |
| Penyimpanan bukti (file per kandidat, reference ID mis. `FP-2026-11-24-001`) | Bukti HTTP di luar memori LLM; LLM hanya menerima reference ID |
| Sensor PII | Ganti token, kata sandi, email/nomor pribadi, dan data sensitif lain dengan `[REDACTED]` sebelum bukti disimpan/dibagikan |
| `~/workspace/catatan/log-bug-bounty.md` | Catat verdict tiap kandidat (lihat Format output) |

## Human-in-the-loop

- A60 mengaudit verdict gerbang sebelum kandidat maju ke skeptic. Bila A60 tidak setuju satu jawaban, kandidat dikembalikan — bukan dinegosiasi.
- LULUS di gerbang ini bukan izin kirim laporan. Draf VERIFIED tetap ditinjau manusia 2–3 menit dan hanya dikirim bila **Cipta menyetujui**.

## Format output

Catat setiap kandidat di `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Kandidat: <nama temuan singkat> | Program: <nama> | Reference ID bukti: <FP-...>
  - Sinyal: <baris tabel: Open Redirect / CORS / IDOR Read-Only / Token bocor / Debug endpoint / S3 listing>
  - Probe Steps: <langkah yang dijalankan + hasil tiap langkah + reference ID bukti>
  - Execution Gate: LULUS/TOLAK — <syarat eskalasi yang terpenuhi / tidak terpenuhi>
  - Baseline vs exploit: <perbedaan perilaku + reference ID bukti baseline dan exploit>
  - Verdict akhir: LULUS / TOLAK PERMANEN / TOLAK SEMENTARA — <alasan satu kalimat>
```

Hanya kandidat berstatus **LULUS** yang diteruskan ke A60 (`skeptic-false-positive-eliminator`). Kandidat TOLAK berhenti di sini — dicatat, tidak dihapus dari log, tidak dikirim ke mana pun.

## Batasan yang diketahui

- Tabel di atas tidak lengkap — baris baru yang ditemukan di lapangan ditambahkan dengan nomor baru + dicatat tanggalnya, bukan dipakai diam-diam. Baris baru wajib menyebut Signal, Probe Steps, dan Execution Gate-nya, bukan sekadar nama kerentanan.
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar) — terapkan gerbang ini pada outcome-nya, tapi jangan paksakan baris web klasik bila outcome-nya berupa aksi agen.
