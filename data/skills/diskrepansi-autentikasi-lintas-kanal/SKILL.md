# Skill: Diskrepansi Autentikasi Lintas Kanal — Bandingkan Otorisasi Fungsi yang Sama di Web, API Mobile, dan Endpoint Versi Lama

> Dibangun dari riset "Skill Langka High/Critical & Anti False Positive" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`, Bagian 2 — Trust Boundary & Feature Interaction Mapping, butir Cross-Channel Auth Discrepancy).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat satu fungsi yang sama bisa dijangkau lewat lebih dari satu kanal — aplikasi web, API mobile, dan/atau endpoint versi lama (`/api/v1/` vs `/api/v2/`) — dan perlu dibuktikan apakah otorisasinya sama kuat di semua kanal. Dipakai setelah recon mengindeksasi endpoint per kanal (skill `pemetaan-permukaan-serangan`, `perburuan-shadow-api-spa`, `penemuan-api-swagger`) dan setelah sesi multi-peran siap (skill `manajemen-sesi-multi-peran`). Jangan dipakai bila fungsi itu hanya ada di satu kanal — tidak ada yang bisa dibandingkan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan matriks kanal × peran + evaluasi diferensial |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai apakah selisih otorisasi antar kanal benar berdampak |
| Pengerjaan | **A64 Web Application Tester** | Menguji kanal aplikasi web |
| Pengerjaan | **A66 API Security Tester** | Menguji kanal API mobile + endpoint versi lama |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perbandingan lintas akun pada SATU endpoint (baseline A/B/C pemilik–anonim–lintas akun) → skill `access-control-differential-analyst`. Skill ini BUKAN itu: skill ini membandingkan otorisasi fungsi yang SAMA lintas KANAL/VERSI (web vs mobile vs `/api/v1` vs `/api/v2`), dengan peran dan objek yang sama — dimensi yang tidak ada di skill diferensial.
- Penemuan endpoint lama/tak terdokumentasi dari bundle SPA + verifikasi liveness read-only → skill `perburuan-shadow-api-spa`. Skill itu secara eksplisit MENYERAHKAN pengujian otorisasi endpoint shadow ke skill lain — skill inilah yang mengujinya, setelah liveness terbukti.
- Inventarisasi endpoint dari spesifikasi resmi (termasuk spesifikasi v1 vs v2) → skill `penemuan-api-swagger`.
- Pengujian fungsi admin per peran pada satu kanal → skill `pengujian-bfla` (BFLA di sini hanya fungsi/peran, bukan kanal).
- Sesi multi-peran (Admin/Member/Guest) → skill `manajemen-sesi-multi-peran` (skill ini hanya MENYIAPKAN sesinya; perbandingan lintas kanal tetap di sini).
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.

## Signal (sinyal yang memicu perburuan)

Sinyal berikut menandakan satu fungsi patut diuji lintas kanal — satu sinyal cukup untuk masuk ke Probe Steps, makin banyak sinyal makin tinggi prioritas:

1. **Versi ganda hidup bersamaan:** aplikasi memakai `/api/v2/...` tapi `/api/v1/...` masih merespons (ditemukan lewat `perburuan-shadow-api-spa` atau `penemuan-api-swagger`) — endpoint lama sering luput dari perbaikan otorisasi.
2. **Fitur baru di atas middleware lama:** fitur yang baru rilis memakai ulang middleware autentikasi/otorisasi lama (terlihat dari pola path, header, atau respons error yang sama dengan endpoint lama) — middleware lama mungkin tidak mengenal peran/cek baru yang dipakai fitur itu.
3. **Kanal mobile lebih longgar:** API mobile menerima token/sesi yang berbeda dari web (mis. token perangkat, sesi panjang tanpa 2FA, header kustom) — kanal mobile sering dibuat dengan asumsi "klien tepercaya".
4. **Respons otorisasi berbeda antar kanal:** permintaan yang sama (peran + objek yang sama) ditolak di web (403) tapi diterima di mobile/v1, atau sebaliknya — selisih ini adalah inti temuan.
5. **Cek baru hanya di satu kanal:** perbaikan keamanan terbaru (mis. cek peran baru, verifikasi 2FA, pembatasan perangkat) hanya terlihat di satu kanal — kanal lain yang belum diperbaiki adalah kandidat.
6. **Dokumentasi kanal tidak konsisten:** spesifikasi/dokumentasi menyebut batasan peran yang berbeda per kanal, atau satu kanal tidak terdokumentasi sama sekali.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun/peran uji milik sendiri.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only; untuk uji tulis, operasikan HANYA pada data uji milik sendiri dan kembalikan ke keadaan semula.
12. **Jangan mengarang pasangan lintas kanal.** Pasangan fungsi lintas kanal harus berasal dari indeks recon / bundle / spesifikasi (path + bukti asal tercatat); menebak `/api/v1/admin` hanya karena ada `/api/v2/admin` = tebakan, bukan pasangan — dilarang diuji sebagai fakta.
13. **200 OK bukan bukti.** Respons sukses tanpa perubahan status nyata di server (uji tulis) atau tanpa data privat yang terbukti (uji baca) = bukan temuan.
14. **Jangan memakai token/sesi kanal lain milik orang lain.** Token mobile/web yang dipakai harus milik akun uji sendiri di kanal itu; jangan mencuri, menebak, atau memakai ulang token sesi pengguna lain.

## Probe Steps (langkah pengujian)

### Gerbang 1 — Pasangkan fungsi yang sama lintas kanal

1. Ambil daftar endpoint/fungsi HANYA dari indeks recon (`pemetaan-permukaan-serangan`), inventaris shadow AKTIF (`perburuan-shadow-api-spa`), atau spesifikasi resmi (`penemuan-api-swagger`).
2. Untuk tiap fungsi, cari pasangannya di kanal lain: fungsi yang sama (operasi + resource yang sama) di web, di API mobile, dan di `/api/v1/` bila ada. Catat untuk tiap pasangan: kanal, metode + path lengkap, versi API, jenis token/sesi yang dipakai kanal itu, dan sumber buktinya (indeks/bundle baris/spesifikasi).
3. Tandai pasangan yang TIDAK punya pasangan lintas kanal — fungsi satu kanal saja tidak diuji di skill ini (serahkan ke `access-control-differential-analyst` / `pengujian-bfla` bila relevan).
4. **Standar lulus:** tiap pasangan tercatat dengan kanal + path + versi + sumber bukti asal. Pasangan tanpa sumber bukti = STOP, jangan diuji.

### Gerbang 2 — Bangun matriks kanal × peran

1. Dari matriks hak akses (skill `manajemen-sesi-multi-peran` Gerbang 3), salin hak yang SEHARUSNYA berlaku per peran untuk fungsi itu — hak yang sama dipakai sebagai acuan di SEMUA kanal, kecuali dokumentasi resmi menyatakan perbedaan antar kanal secara eksplisit (bila begitu, catat perbedaannya sebagai "perbedaan terdokumentasi", bukan temuan).
2. Buat matriks kanal × peran: baris = kanal (web / mobile / v1 / v2), kolom = peran (Admin / Member / Guest), sel = boleh baca / boleh tulis / tidak boleh + respons yang diharapkan bila kontrol benar (401/403/404).
3. Siapkan wadah sesi terpisah per peran DAN per kanal (sesi web ≠ sesi mobile — jangan campur cookie/token antar kanal dalam satu wadah; lihat `manajemen-sesi-multi-peran` Gerbang 2).
4. **Standar lulus:** matriks tertulis sebelum satu pun pengujian lintas kanal dimulai + tiap sel punya respons yang diharapkan. Pengujian tanpa matriks = menebak-nebak, jangan jalan.

### Gerbang 3 — Baseline per kanal (metode diferensial per kanal)

Untuk tiap kanal, jalankan baseline 3 kondisi dari `access-control-differential-analyst` pada fungsi dan objek yang SAMA (objek milik akun uji sendiri):

| Kondisi | Permintaan | Yang diharapkan bila kontrol benar |
|---|---|---|
| **A — pemilik sah** | Pemilik (token kanal itu) → objek sendiri | Data/aksi lengkap — pembanding "yang seharusnya terlihat" |
| **B — anonim** | Tanpa token → objek yang sama | 401/403/404/objek kosong, atau data yang memang publik |
| **C — lintas akun** | Akun uji kedua (token kanal itu) → objek akun pertama | 401/403/404/objek kosong (sama seperti B bila objek itu privat) |

1. Jalankan A → B → C di tiap kanal, simpan raw request/response tiap kondisi per kanal.
2. **Standar lulus:** ketiga kondisi dijalankan di SETIAP kanal pada objek yang sama, dengan raw request/response tersimpan. Satu kanal tanpa baseline lengkap = kanal itu belum bisa dibandingkan, jangan simpulkan apa-apa darinya.

### Gerbang 4 — Evaluasi diferensial lintas kanal

Bandingkan hasil kondisi C (dan B) ANTAR kanal, field per field dan status per status:

- **Kandidat Temuan:** peran/objek yang DITOLAK di satu kanal (mis. web mengembalikan 403) tapi DITERIMA di kanal lain (mis. `/api/v1/` atau mobile mengembalikan 200 + data privat / aksi berhasil) — dengan peran, objek, dan parameter yang sama persis. Inilah diskrepansi otorisasi lintas kanal.
- **Aman:** semua kanal menolak dengan cara yang setara (401/403/404/objek kosong), atau semua kanal mengembalikan hanya data yang sama persis dengan yang sudah publik di B.
- **Bukan temuan:** selisih dijelaskan oleh perbedaan yang TERDOKUMENTASI antar kanal (mis. kanal mobile memang dirancang read-only sehingga responsnya berbeda, atau v1 memang sudah diumumkan tidak lagi menegakkan cek X karena fiturnya dipensiunkan — dengan tautan dokumentasi tercatat); selisih hanya pada pesan error/status tanpa data/aksi (mis. 401 vs 403 tanpa isi berbeda); kanal yang satu mengembalikan data milik akun penguji sendiri, bukan akun lain.
- **Standar lulus:** keputusan Kandidat Temuan vs Aman vs Bukan temuan ditulis per pasangan kanal, dengan nama field + isi yang membuktikan (PII disensor `[REDACTED]`) + tautan dokumentasi bila diklaim "perbedaan terdokumentasi". Keputusan tanpa menyebut field = belum terbukti.

### Gerbang 5 — State Verification (untuk uji tulis lintas kanal)

Untuk pasangan yang mengubah data (PUT/PATCH/POST/DELETE) dan lolos Gerbang 4 sebagai Kandidat Temuan:

1. Minta perubahan lewat kanal yang longgar sebagai akun uji kedua terhadap objek akun pertama (HANYA data uji milik sendiri).
2. Baca ulang objek itu sebagai pemilik lewat kanal yang ketat (sesi bersih) dan periksa apakah perubahan itu NYATA terjadi di server.
3. **Perubahan nyata = Kandidat Temuan** (lanjut ke Gerbang 6). **Pesan sukses tapi data tidak berubah (silent drop) = Aman** — server hanya mengembalikan pesan sukses palsu; catat sebagai bukan temuan, jangan laporkan.
4. Bila perubahan ternyata terjadi, kembalikan data objek ke keadaan semula dari akun pemiliknya (jangan tinggalkan data uji berubah).
5. **Standar lulus:** ada bukti baca-ulang sebagai pemilik yang menunjukkan status sebelum vs sesudah. Tanpa baca-ulang = belum terbukti, jangan klaim temuan tulis.

### Gerbang 6 — Execution Gate (gerbang akhir sebelum triase)

Kandidat Temuan hanya LOLOS ke triase bila SEMUA syarat ini terpenuhi — satu gagal = TOLAK:

1. **Selisih nyata:** peran/objek yang sama ditolak di ≥1 kanal dan diterima di ≥1 kanal lain, dengan raw request/response tersimpan per kanal (Gerbang 3–4).
2. **Bukan perbedaan terdokumentasi:** tidak ada dokumentasi resmi yang menyatakan perbedaan otorisasi antar kanal itu disengaja (bila ada, itu Bukan temuan — catat tautannya).
3. **Dampak terbukti:** uji baca → field respons berisi data privat milik akun lain (disensor); uji tulis → perubahan state NYATA terverifikasi baca-ulang + sudah dikembalikan (Gerbang 5).
4. **Reproduksibel:** uji ulang dengan sesi HTTP baru (fresh tokens) di kedua kanal memberi hasil yang sama — lihat skill `skeptic-false-positive-eliminator`. Gagal direproduksi = TOLAK.
5. **Bukan artefak sesi:** sesi di kedua kanal terbukti hidup saat pengujian (bukan token kedaluwarsa yang disalahartikan sebagai 403 = aman — lihat `manajemen-sesi-multi-peran` Gerbang 4).

Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim. Tidak lolos = catat alasan di log, kembali ke Gerbang 1 (pasangan lain).

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri per peran (Admin, Member, Guest) | Satu-satunya akun yang dipakai; semuanya milik sendiri, di tiap kanal. |
| Wadah sesi terpisah per peran DAN per kanal | Isolasi sesi; token web tidak pernah dipakai di kanal mobile dan sebaliknya. |
| Canary palsu unik per akun | Data penanda milik sendiri untuk membuktikan kebocoran antar akun dari isi respons. |
| Indeks recon + inventaris shadow AKTIF + spesifikasi resmi | Satu-satunya sumber pasangan lintas kanal (`pemetaan-permukaan-serangan`, `perburuan-shadow-api-spa`, `penemuan-api-swagger`). |
| Matriks hak akses | Dari skill `manajemen-sesi-multi-peran` Gerbang 3 — acuan "seharusnya" per peran, sama di semua kanal. |
| Sesi HTTP bersih (fresh tokens) | Untuk uji ulang reproduksibilitas di Gerbang 6. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap pasangan: baseline per kanal, hasil diferensial, verifikasi state, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Fungsi: [operasi + resource yang sama di semua kanal]
Pasangan lintas kanal: [web: metode + path | mobile: metode + path | v1: metode + path | v2: metode + path + sumber bukti tiap kanal]
Matriks kanal × peran: [per kanal × per peran: boleh baca / boleh tulis / tidak boleh + respons yang diharapkan]
Baseline per kanal: [per kanal: A pemilik / B anonim / C lintas akun — status + ringkasan field]
Hasil diferensial lintas kanal: [Kandidat Temuan / Aman / Bukan temuan + kanal yang longgar vs kanal yang ketat + field yang membuktikan, PII disensor]
Perbedaan terdokumentasi: [tidak ada / ada — tautan dokumentasi]
Verifikasi state: [tidak berlaku (uji baca) / perubahan NYATA + sudah dikembalikan / silent drop + bukti baca-ulang]
Reproduksibilitas: [lolos sesi bersih / gagal + alasan]
Keputusan: [maju ke triase / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini hanya menguji otorisasi fungsi yang sama lintas kanal/versi; tidak menguji kerentanan lain (SSRF, XSS, injeksi) — pakai skill fondasi + skill terkait untuk jenis lain.
- Bila kanal mobile memakai token yang tidak bisa dibuat sendiri (mis. butuh perangkat terdaftar), pengujian kanal itu terbatas pada apa yang bisa dibuktikan dari kanal yang sesinya tersedia — catat keterbatasan itu di log, jangan meminjam perangkat/akun orang lain.
- Perbedaan respons antar kanal kadang disebabkan perbedaan format error/versi, bukan otorisasi — Gerbang 4 memaksa pembuktian lewat field/aksi, bukan lewat status saja.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Pengujian memakai akun sendiri di program target dan pencatatan di file log di atas.

## Websites

- Referensi riset Bagian 2: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`
- Pembuktian diferensial per kanal: `~/workspace/tmp/pusat-komando-push/data/skills/access-control-differential-analyst/SKILL.md`
- Penemuan endpoint lama: `~/workspace/tmp/pusat-komando-push/data/skills/perburuan-shadow-api-spa/SKILL.md`
- Inventarisasi spesifikasi: `~/workspace/tmp/pusat-komando-push/data/skills/penemuan-api-swagger/SKILL.md`
- Sesi multi-peran: `~/workspace/tmp/pusat-komando-push/data/skills/manajemen-sesi-multi-peran/SKILL.md`
- Validasi + laporan: `~/workspace/tmp/pusat-komando-push/data/skills/triase-duplikat/SKILL.md`, `~/workspace/tmp/pusat-komando-push/data/skills/laporan-abstrak/SKILL.md`

## Alternatives for better results

- Bila pasangan lintas kanal tidak ditemukan (fungsi hanya ada di satu kanal): lanjutkan dengan `access-control-differential-analyst` (lintas akun) atau `pengujian-bfla` (lintas peran) pada kanal itu.
- Bila endpoint lama ternyata TIDAK AKTIF (sama dengan baseline 404): itu hasil yang sah dari `perburuan-shadow-api-spa` — jangan memaksa dengan menebak path lain.
- Bila selisih antar kanal ternyata soal urutan langkah alur kerja, bukan otorisasi: lanjutkan dengan `pelompakan-alur-state-machine`.
