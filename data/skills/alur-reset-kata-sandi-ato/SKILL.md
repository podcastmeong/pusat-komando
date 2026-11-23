# Skill: Alur Reset Kata Sandi & Account Takeover (ATO) — Host Header Injection, Token Reset, Kebocoran via Referer

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 4 butir 26).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target punya alur "lupa kata sandi" (minta tautan reset → email berisi token reset → atur kata sandi baru) dan perlu dibuktikan apakah alur itu bisa dipakai untuk mengambil alih akun. Dipakai HANYA pada akun uji sendiri — token reset yang diuji adalah token milik akun sendiri. Jangan dipakai untuk mereset/mengambil alih akun orang lain dalam bentuk apa pun.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan teknik reset/ATO di bawah |
| Pengerjaan | **A64 Web Application Tester** | Menguji alur reset aplikasi web dengan metode ini |
| Pengerjaan | **A66 API Security Tester** | Menguji endpoint reset API dengan metode ini |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi umum "reset kata sandi bisa dipakai untuk akun lain" → skill `fondasi-kerentanan-web-api` Gerbang 1.4 (Broken Authentication). Skill ini BUKAN definisi itu: skill ini adalah **metodologi reset/ATO per teknik** (Host Header Injection, token dapat diprediksi, kebocoran via Referer) yang tidak ada di skill fondasi.
- Bypass 2FA pada langkah verifikasi → skill `analisis-bypass-2fa` (reset di sini hanya alur lupa-kata-sandi, bukan langkah 2FA).
- Sesi multi-peran (akun A vs akun B, keduanya milik sendiri) → skill `manajemen-sesi-multi-peran`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun uji adalah akun sendiri.** Alur reset hanya diminta untuk akun uji milik sendiri; token reset yang diuji adalah token milik akun sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.
13. **JANGAN PERNAH meminta reset untuk akun orang lain, dan JANGAN PERNAH memakai token reset orang lain.** Pembuktian ATO di skill ini dilakukan dengan DUA akun sendiri: akun korban simulasi adalah akun uji milik sendiri (akun B), dan penyerang simulasi adalah akun uji milik sendiri juga (akun A) — keduanya milik kita, jadi "pengambilalihan" yang dibuktikan adalah atas akun sendiri.
14. **Jangan benar-benar mengambil alih akun simulasi sampai tidak bisa kembali.** Bila teknik terbukti bisa mereset kata sandi akun B (milik sendiri), JANGAN lanjut mengubah kata sandinya sampai tidak bisa login kembali — cukup buktikan token reset valid (token diterima di endpoint reset / halaman atur kata sandi terbuka untuk akun B), lalu hentikan dan kembalikan akun B ke keadaan semula. Pembuktian berhenti di "token valid + halaman reset terbuka", bukan di "kata sandi berhasil diubah".
15. **Token reset TIDAK BOLEH ditulis utuh di log/skill.** Catat hanya "token diterima/ditolak" + 4 karakter terakhir bila perlu membedakan percobaan.
16. **Host Header Injection hanya dengan host yang kita kendalikan** (domain/canary milik sendiri) — jangan arahkan tautan reset ke domain orang lain.

## Langkah + gerbang

### Gerbang 1 — Petakan alur reset + catat baseline

1. Minta reset untuk akun uji sendiri (akun B) dan petakan alurnya: endpoint minta reset, isi email reset (tautan + token + masa berlaku), endpoint pakai token (`/reset-password?token=...`), parameter yang dikirim saat atur kata sandi baru, dan apa yang terjadi setelah berhasil.
2. Catat baseline: tautan reset akun B yang sah → halaman atur kata sandi terbuka untuk akun B; token salah/kedaluwarsa → ditolak.
3. **Standar lulus:** endpoint + format token + masa berlaku tercatat. Target tidak punya alur reset = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji teknik satu per satu (satu teknik = satu putaran)

Uji berurutan; tiap teknik memakai akun uji sendiri dan token reset milik sendiri yang baru diminta (token sekali pakai — minta token baru per teknik).

#### Teknik A — Host Header Injection (tautan reset mengarah ke host penyerang)
Saat meminta reset untuk akun B (milik sendiri), ubah header `Host` (dan variasi `X-Forwarded-Host`, `X-Forwarded-For`, `Origin`) ke domain yang kita kendalikan (canary milik sendiri), lalu periksa isi email reset: apakah tautan reset memakai host yang kita kirim? **Terbukti bila:** tautan reset di email akun B (milik sendiri) mengarah ke host yang kita kendalikan — artinya server memakai header Host tanpa validasi untuk membangun tautan. Jangan klik tautan itu untuk mereset akun lain; cukup buktikan host-nya.

#### Teknik B — Token reset dapat diprediksi / tidak acak
Minta beberapa token reset berturut-turut untuk akun sendiri dan analisis polanya: apakah token berurutan (angka naik), berbasis waktu (timestamp), berbasis data akun (hash dari email/username tanpa secret), atau terlalu pendek? Coba tebak token berikutnya dari pola yang teramati — hanya untuk akun sendiri, dengan percobaan TERBATAS (belasan, bukan ribuan). **Terbukti bila:** token berikutnya berhasil ditebak dari pola dan diterima endpoint reset (halaman atur kata sandi terbuka untuk akun sendiri). Token acak panjang yang tidak berpola = Aman untuk teknik ini, catat sebagai Aman.

#### Teknik C — Kebocoran token via header Referer
Buka tautan reset akun sendiri (di browser uji), lalu dari halaman reset itu klik tautan keluar / muat sumber daya pihak ketiga (bila halaman reset memuatnya), dan periksa apakah token reset ikut terkirim di header `Referer` ke pihak ketiga. Periksa juga: apakah token reset tersimpan di riwayat/log yang bisa diakses (mis. token muncul di URL yang tercatat di analytics pihak ketiga yang dimuat halaman). **Terbukti bila:** token reset akun sendiri teramati terkirim ke pihak ketiga lewat `Referer` (di log proxy milik sendiri) — artinya siapa pun yang mengendalikan pihak ketiga itu bisa memakai token tersebut.

#### Teknik D — Token tidak terikat ke akun / tidak kedaluwarsa / bisa dipakai ulang
Uji satu per satu pada akun sendiri: (1) token reset akun A dipakai untuk mereset akun B (keduanya milik sendiri) — apakah diterima? (2) token yang sudah dipakai sekali — apakah bisa dipakai kedua kali? (3) token lama yang sudah lewat masa berlaku — apakah masih diterima? (4) minta reset untuk akun A, lalu ubah parameter `email`/`user_id` di endpoint pakai-token menjadi akun B — apakah server memakai parameter itu tanpa memeriksa tokennya milik siapa? **Terbukti bila:** salah satu variasi membuat halaman atur kata sandi terbuka untuk akun yang bukan pemilik token (keduanya akun sendiri) — berhenti di titik itu sesuai Aturan keras 14, jangan ubah kata sandinya.

4. **Standar lulus per teknik:** ada hasil per teknik (terbukti/tidak + status + isi respons). Teknik tanpa hasil = belum diuji, jangan diklaim.

### Gerbang 3 — Buktikan token valid (berhenti sebelum ubah kata sandi)

1. Untuk teknik yang terbukti di Gerbang 2, buktikan dampaknya dengan batas Aturan keras 14: tunjukkan endpoint reset menerima token (halaman atur kata sandi terbuka / respons "token valid") untuk akun yang seharusnya tidak bisa — JANGAN kirim permintaan ubah kata sandi sampai selesai.
2. Setelah pembuktian, batalkan token yang dipakai (minta token baru untuk menimpa yang lama, atau biarkan kedaluwarsa) dan pastikan akun B masih bisa login dengan kata sandi lamanya.
3. **Standar lulus:** ada bukti "token diterima + halaman reset terbuka untuk akun yang salah" + bukti akun B masih bisa login normal sesudahnya. Mengubah kata sandi akun simulasi sampai tidak bisa kembali = pelanggaran Aturan keras 14.

### Gerbang 4 — Serahkan ke skeptic gate

1. Kandidat Temuan diserahkan ke skill `skeptic-false-positive-eliminator`: uji ulang dengan sesi HTTP baru (fresh tokens), pastikan reproduksibel konsisten.
2. Gagal direproduksi = TOLAK, catat di log sebagai bukan temuan.
3. Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim.
4. **Standar lulus:** keputusan akhir tercatat di log dengan pasangan bukti request/response asli (token reset dan PII disensor).

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (akun A "penyerang simulasi", akun B "korban simulasi") | Keduanya milik sendiri; akun B tidak pernah benar-benar diambil alih sampai tidak bisa kembali. |
| Akses email akun uji sendiri | Membaca email reset milik akun sendiri (untuk Teknik A: memeriksa host di tautan). |
| Domain/canary milik sendiri | Hanya untuk Teknik A (host tujuan injeksi yang kita kendalikan). |
| Proxy pencegat (lihat skill `mcp-burp-official`/`mcp-burp-ultra`) | Mengamati header `Referer` (Teknik C) dan mengubah parameter (Teknik D); hanya pada lalu lintas akun sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap teknik: alur reset, hasil, bukti token valid, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint reset]
Alur reset: [endpoint minta reset + format token + masa berlaku — token disensor]
Teknik A (Host Header Injection): [tautan memakai host injeksi? + host yang teramati]
Teknik B (token dapat diprediksi): [pola teramati + token berikutnya bisa ditebak? + bukti]
Teknik C (kebocoran via Referer): [token terkirim ke pihak ketiga? + tujuan + bukti log proxy]
Teknik D (token tidak terikat/kedaluwarsa/pakai ulang): [variasi yang diterima + bukti halaman reset terbuka]
Pembuktian (berhenti sebelum ubah kata sandi): [token diterima + akun B masih bisa login normal]
Keputusan: [maju ke skeptic gate / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Pembuktian di skill ini sengaja berhenti di "token valid + halaman reset terbuka" (Aturan keras 14) — triager mungkin meminta bukti ubah kata sandi penuh; bila itu terjadi, keputusan lanjut ada di A60 + Cipta (manusia), bukan di agen — jangan lanjut sendiri.
- Teknik A hanya bermakna bila email reset benar-benar dikirim dengan tautan berbasis Host; bila server memakai host tetap dari konfigurasi, hasilnya Aman — catat sebagai Aman.
- Token reset yang pendek tapi acak (CSPRNG) tetap aman meski pendek — yang dinilai adalah keacakan/pola, bukan panjang semata.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome, bukan trik reset klasik — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
