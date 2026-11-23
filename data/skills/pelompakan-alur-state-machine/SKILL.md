# Skill: Pelompakan Alur State Machine — Uji Lompat Langkah & Webhook Konfirmasi Tanpa Validasi Sesi

> Dibangun dari riset "Skill Langka High/Critical & Anti False Positive" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`, Bagian 2 — Trust Boundary & Feature Interaction Mapping, butir State-Machine & Workflow Skipping).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target punya alur kerja bertahap (langkah A → langkah B → langkah C) dan perlu dibuktikan apakah langkah B bisa dipanggil langsung tanpa menyelesaikan langkah A — mis. langsung memukul endpoint `PUT /study-status`, atau memanggil webhook konfirmasi pembayaran tanpa melewati validasi sesi peserta. Dipakai setelah alur kerja target dipetakan dari UI/dokumentasi/recon, dan setelah sesi multi-peran siap (skill `manajemen-sesi-multi-peran`). Jangan dipakai pada endpoint yang memang dirancang satu langkah (tidak ada alur) — tidak ada yang bisa dilompati.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Memetakan state machine + menjalankan uji lompat langkah |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai apakah lompatan benar mengubah state dan berdampak |
| Pengerjaan | **A64 Web Application Tester** | Menguji lompat langkah di alur aplikasi web |
| Pengerjaan | **A66 API Security Tester** | Menguji lompat langkah + webhook di endpoint API |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi Business Logic Flaws + contoh "lompat langkah state machine" + standar bukti dampak (perubahan state nyata pada akun sendiri) → skill `perburuan-kerentanan-spesifik` Gerbang 1.1. Skill ini BUKAN definisi itu: skill ini adalah **METODOLOGI SISTEMATIS** yang tidak ada di sana — pemetaan state machine lengkap (matriks transisi), enumerasi tiap lompatan yang mungkin, dan probe webhook konfirmasi — dengan standar lulus per gerbang. Standar bukti dampak tetap memakai `perburuan-kerentanan-spesifik` (jangan ulangi definisinya di sini).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Pembuktian BOLA/IDOR pada satu endpoint → skill `access-control-differential-analyst` (skill ini menguji URUTAN langkah, bukan kepemilikan objek).
- Pengujian fungsi admin per peran → skill `pengujian-bfla`.
- Sesi multi-peran → skill `manajemen-sesi-multi-peran`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- **Webhook sebagai parameter SSRF** (URL webhook yang diambil server) → skill `fondasi-kerentanan-web-api` — itu soal SSRF, BUKAN soal webhook konfirmasi yang memutar state. Probe webhook di skill ini hanya soal validasi sesi/tanda tangan pada endpoint callback, bukan SSRF.

## Signal (sinyal yang memicu perburuan)

Sinyal berikut menandakan satu alur patut diuji lompat langkahnya — satu sinyal cukup untuk masuk ke Probe Steps, makin banyak sinyal makin tinggi prioritas:

1. **Alur bertahap yang terlihat di UI:** pendaftaran → konfirmasi → pembayaran → selesai; studi/peserta berpindah status langkah demi langkah; checkout bertahap (keranjang → alamat → bayar → konfirmasi).
2. **Endpoint per langkah terpisah:** tiap langkah punya endpoint sendiri (mis. `PUT /study-status`, `POST /confirm`, `POST /payment/confirm`) — endpoint langkah akhir bisa dipanggil langsung bila server tidak memeriksa langkah sebelumnya.
3. **Validasi hanya di klien:** tombol langkah B baru aktif setelah langkah A di UI, tapi tidak ada bukti server memeriksa ulang — langkah yang "diasumsikan klien yang menegakkan" adalah kandidat utama.
4. **Webhook konfirmasi terekspos:** ada endpoint callback/webhook (mis. konfirmasi pembayaran dari payment gateway) yang mengubah state — patut diuji apakah endpoint itu memeriksa tanda tangan penyedia, mengikat ke sesi/transaksi peserta, dan menolak replay/pemalsuan.
5. **Status bisa ditebak/dipaksa:** nilai status berikutnya terlihat di respons API atau di kode klien (mis. enum status `pending → confirmed → completed`) sehingga penyerang tahu persis nilai apa yang harus dikirim untuk melompat.
6. **Tanpa token sekali pakai antar langkah:** tidak ada token/nonce yang mengikat langkah B ke penyelesaian langkah A (tidak ada `step_token`, `session_id` alur, atau pengecekan urutan di server).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun/peran uji dan semua transaksi/alur uji milik sendiri.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only.
12. **Uji lompat langkah HANYA pada alur/transaksi akun uji sendiri.** Jangan mengubah state pesanan, pembayaran, status studi, atau pendaftaran pengguna lain — alur orang lain tidak pernah disentuh, sekalipun endpoint-nya terlihat bisa.
13. **Bila lompat langkah berhasil mengubah state, segera kembalikan/laporkan + jangan ulangi.** Kembalikan state alur uji sendiri ke keadaan semula dari akun pemiliknya (batalkan pesanan uji / kembalikan status / laporkan ke log hari itu juga); jangan mengulangi lompatan yang sudah terbukti demi "bukti tambahan".
14. **Webhook: hanya transaksi milik sendiri, hanya callback yang sah milik sendiri.** Uji webhook HANYA dengan transaksi/alur milik akun uji sendiri; jangan memalsukan tanda tangan penyedia (signature) — yang diuji adalah apakah endpoint MEMERIKSA tanda tangan/sesi atau tidak (kirim callback tanpa tanda tangan / dengan tanda tangan salah / dengan payload yang diubah pada field milik sendiri, lalu amati apakah state tetap berubah). Jangan replay callback transaksi orang lain, jangan memalsukan callback untuk transaksi orang lain.
15. **200 OK bukan bukti.** Respons sukses tanpa perubahan state nyata di server = bukan temuan (silent drop).
16. **Jangan memakai token/nonce alur milik orang lain.** Token langkah, `session_id` alur, atau nonce yang dipakai harus milik sesi uji sendiri.

## Probe Steps (langkah pengujian)

### Gerbang 1 — Petakan state machine alur

1. Jalani alur SEKALI secara normal sebagai pengguna sah (akun uji sendiri) dan catat tiap langkah: endpoint yang dipanggil, metode + path, parameter/body yang dikirim, respons server, dan status alur sebelum vs sesudah tiap langkah.
2. Susun peta state machine: daftar state (mis. `draft → pending → confirmed → completed`), daftar transisi (state asal → endpoint → state tujuan), siapa yang boleh memicu tiap transisi (peran), dan apa syaratnya (langkah sebelumnya selesai? token langkah? sesi peserta valid? pembayaran lunas?).
3. Tandai transisi yang syaratnya TIDAK TERTULIS di respons server/dokumentasi — syarat yang hanya terlihat di UI klien (tombol nonaktif, langkah disembunyikan) dicatat sebagai "diasumsikan klien" dan menjadi kandidat lompatan.
4. **Standar lulus:** peta state machine tertulis (state + transisi + pemicu + syarat per transisi) dari SATU alur normal yang dijalani sendiri. Alur yang tidak pernah dijalani normal = tidak ada peta = STOP, jangan menguji lompatan.

### Gerbang 2 — Enumerasi lompatan (matriks transisi)

1. Dari peta Gerbang 1, buat matriks lompatan: untuk tiap transisi (langkah B), daftarkan semua state awal yang BUKAN prasyaratnya (mis. dari `draft` langsung ke `completed`, dari `pending` langsung ke `completed` tanpa `confirmed`).
2. Untuk tiap lompatan catat: endpoint langkah B, parameter yang dibutuhkan (ambil dari pengamatan alur normal — jangan dikarang), dan state yang diharapkan bila server menegakkan urutan (harus ditolak: 400/403/409 atau pesan "langkah sebelumnya belum selesai").
3. Urutkan prioritas: lompatan yang mengubah nilai (status pembayaran, status studi/peserta, status pesanan ke selesai) dulu; lompatan antar state baca saja terakhir.
4. **Standar lulus:** matriks lompatan tertulis sebelum satu pun lompatan diuji + tiap lompatan punya respons yang diharapkan bila kontrol benar. Lompatan yang diuji tanpa masuk matriks = menebak-nebak, jangan jalan.

### Gerbang 3 — Uji lompat langkah (satu per satu, akun sendiri)

1. Siapkan alur uji BARU milik akun sendiri pada state awal yang diinginkan (mis. alur baru di state `draft`/`pending` — jangan memakai alur yang sudah berjalan setengah jalan milik orang lain; bila perlu, buat alur uji baru dari awal).
2. Panggil endpoint langkah B LANGSUNG dari state awal itu — tanpa menjalankan langkah A — dengan parameter yang sama seperti pada alur normal, memakai sesi akun uji sendiri.
3. Klasifikasikan hasil per lompatan:
   - **Kandidat Temuan:** server menerima lompatan dan state alur uji BERUBAH ke state tujuan (dibuktikan dengan baca-ulang state — lihat Gerbang 4).
   - **Aman:** server menolak (400/403/409/pesan urutan langkah) dan state tidak berubah.
   - **Bukan temuan:** 200/pesan sukses tapi state TIDAK berubah saat dibaca ulang (silent drop); lompatan hanya mengubah tampilan/field yang memang boleh diubah dari state itu.
4. Uji SATU lompatan per satu, satu alur uji per lompatan bila memungkinkan; jangan menumpuk beberapa lompatan dalam satu alur uji (hasilnya tidak bisa diatribusikan).
5. **Standar lulus:** tiap lompatan di matriks punya klasifikasi + bukti respons + bukti baca-ulang state. Lompatan tanpa baca-ulang state = belum terbukti.

### Gerbang 4 — State Verification + rollback (wajib untuk tiap Kandidat Temuan)

1. Baca ulang state alur uji dari sesi bersih (akun pemilik) dan bandingkan sebelum vs sesudah lompatan — perubahan NYATA di server adalah syarat Kandidat Temuan (standar bukti dampak dari `perburuan-kerentanan-spesifik` Gerbang 1.1).
2. **Bila perubahan ternyata terjadi, SEGERA kembalikan state ke semula** dari akun pemiliknya (batalkan pesanan uji / kembalikan status / hubungi alur pembatalan normal) dan catat waktu rollback di log. Jangan tinggalkan alur uji dalam state hasil lompatan.
3. **Jangan ulangi lompatan yang sudah terbukti** — satu bukti perubahan nyata + rollback sudah cukup; pengulangan hanya menambah risiko state yang tidak bisa dikembalikan.
4. **Standar lulus:** ada bukti baca-ulang sebelum vs sesudah + bukti rollback (state kembali semula) TERCATAT. Tanpa bukti rollback = Kandidat Temuan belum lengkap, jangan maju ke triase.

### Gerbang 5 — Probe webhook konfirmasi (alur pembayaran/konfirmasi)

Gerbang ini HANYA bila alur memakai webhook/callback konfirmasi (mis. payment gateway memberi tahu server bahwa pembayaran lunas). Bila tidak ada webhook, lewati gerbang ini dan tulis "tidak berlaku".

1. Identifikasi endpoint webhook dari dokumentasi/recon (path + parameter yang diharapkan + cara penyedia menandatangani callback, bila didokumentasikan). Catat juga: apakah endpoint itu memeriksa tanda tangan penyedia, mengikat callback ke sesi/transaksi peserta, dan menolak replay — menurut dokumentasi.
2. Buat transaksi/alur uji BARU milik akun uji sendiri (mis. pesanan/pembayaran uji yang memang belum lunas) dan catat state-nya sebelum probe.
3. Uji SATU per satu, dari yang paling ringan, HANYA pada transaksi milik sendiri:
   - **(a) Tanpa tanda tangan:** kirim callback konfirmasi tanpa header/parameter tanda tangan penyedia — amati apakah state berubah.
   - **(b) Tanda tangan salah:** kirim callback dengan tanda tangan yang jelas salah (nilai acak milik sendiri) — amati apakah state berubah.
   - **(c) Payload diubah (field milik sendiri):** kirim callback dengan tanda tangan yang sah milik sendiri BILA tersedia dari transaksi sendiri, tapi ubah field milik sendiri (mis. jumlah/status) — amati apakah server memakai nilai dari callback tanpa memeriksa ke penyedia.
   - **(d) Replay callback sendiri:** kirim ulang callback ASLI dari transaksi milik sendiri yang sudah diproses — amati apakah state berubah dua kali / efek ganda (tanpa idempotency).
   - JANGAN memalsukan tanda tangan penyedia, JANGAN replay callback transaksi orang lain, JANGAN memalsukan callback untuk transaksi orang lain.
4. Klasifikasikan seperti Gerbang 3 (Kandidat Temuan bila state transaksi sendiri berubah tanpa validasi yang seharusnya ada; Aman bila ditolak; Bukan temuan bila pesan sukses tapi state tidak berubah).
5. Bila state berubah, lakukan rollback seperti Gerbang 4 (batalkan/kembalikan transaksi uji sendiri) dan jangan ulangi.
6. **Standar lulus:** tiap probe webhook punya klasifikasi + bukti respons + bukti baca-ulang state + bukti rollback bila state berubah. Probe tanpa baca-ulang = belum terbukti.

### Gerbang 6 — Execution Gate (gerbang akhir sebelum triase)

Kandidat Temuan (lompat langkah dan/atau webhook) hanya LOLOS ke triase bila SEMUA syarat ini terpenuhi — satu gagal = TOLAK:

1. **Perubahan state nyata:** ada bukti baca-ulang sebelum vs sesudah yang menunjukkan state alur/transaksi milik sendiri benar-benar berubah (Gerbang 4/5) — bukan sekadar 200 OK.
2. **Urutan/validasi memang dilewati:** lompatan dilakukan dari state yang BUKAN prasyarat (matriks Gerbang 2), atau webhook diterima tanpa tanda tangan/sesi yang seharusnya diperiksa (Gerbang 5) — dengan raw request/response tersimpan.
3. **Rollback selesai:** state alur/transaksi uji sudah dikembalikan ke semula dan buktinya tercatat; tidak ada alur uji yang tertinggal dalam state hasil lompatan.
4. **Hanya akun/transaksi sendiri:** tidak ada state, pesanan, pembayaran, atau pendaftaran orang lain yang disentuh — bila ternyata tersentuh, STOP, laporkan ke Muse + Cipta segera, jangan maju ke triase.
5. **Reproduksibel (bila aman):** uji ulang dengan alur uji BARU milik sendiri memberi hasil yang sama — lihat skill `skeptic-false-positive-eliminator`. Bila uji ulang berisiko (state sulit dikembalikan), cukup SATU bukti + rollback, dan catat alasan tidak diulang di log; A60 yang memutuskan.
6. **Bukan perilaku terdokumentasi:** tidak ada dokumentasi resmi yang menyatakan lompatan/webhook tanpa validasi itu disengaja (bila ada, itu Bukan temuan — catat tautannya).

Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim. Tidak lolos = catat alasan di log, kembali ke Gerbang 2 (lompatan lain).

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri + alur/transaksi uji milik sendiri | Satu-satunya akun dan alur yang dipakai; tiap lompatan memakai alur uji baru bila memungkinkan. |
| Peta state machine + matriks lompatan | Dari Gerbang 1–2 — satu-satunya daftar lompatan yang boleh diuji. |
| Sesi HTTP bersih (fresh tokens) | Untuk baca-ulang state + uji ulang reproduksibilitas. |
| Canary palsu | Nilai penanda milik sendiri di parameter alur uji, supaya perubahan state bisa dibuktikan milik alur uji sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap alur: peta state machine, matriks lompatan, hasil uji, verifikasi state, rollback, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Alur: [nama alur + program/target]
Peta state machine: [state: daftar | transisi: asal → endpoint → tujuan + pemicu + syarat per transisi]
Matriks lompatan: [n lompatan terdaftar — tiap lompatan: dari state X langsung ke langkah B + respons yang diharapkan]
Uji lompat langkah: [per lompatan: endpoint + state awal + status + hasil baca-ulang state + klasifikasi]
Verifikasi state + rollback: [sebelum vs sesudah + rollback selesai HH:MM / tidak berlaku]
Probe webhook: [tidak berlaku / per probe (a)–(d): hasil + baca-ulang state + rollback]
Perilaku terdokumentasi: [tidak ada / ada — tautan dokumentasi]
Keputusan: [maju ke triase / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini hanya menguji URUTAN langkah dan validasi webhook konfirmasi; tidak menguji kepemilikan objek (BOLA/IDOR — lihat `access-control-differential-analyst`) atau fungsi per peran (BFLA — lihat `pengujian-bfla`).
- Peta state machine hanya seakurat pengamatan satu alur normal + dokumentasi; transisi yang hanya terjadi di kondisi langka (mis. timeout, refund) mungkin tidak terpetakan — catat sebagai "belum terpetakan", jangan ditebak.
- Lompatan yang berhasil tapi state-nya sulit/tidak bisa dikembalikan (mis. pembayaran sudah diteruskan) TIDAK BOLEH diuji ulang — satu bukti + laporan segera ke Muse/Cipta; jangan mengambil risiko demi bukti kedua.
- Webhook penyedia yang memakai tanda tangan kuat dan tidak bisa diuji tanpa memalsukannya = mentok di "indikasi, butuh validasi manusia" — jangan pernah memalsukan tanda tangan penyedia.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Pengujian memakai akun sendiri di program target dan pencatatan di file log di atas.

## Websites

- Referensi riset Bagian 2: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`
- Definisi + standar bukti dampak lompat langkah: `~/workspace/tmp/pusat-komando-push/data/skills/perburuan-kerentanan-spesifik/SKILL.md` (Gerbang 1.1)
- Sesi multi-peran: `~/workspace/tmp/pusat-komando-push/data/skills/manajemen-sesi-multi-peran/SKILL.md`
- Validasi + laporan: `~/workspace/tmp/pusat-komando-push/data/skills/triase-duplikat/SKILL.md`, `~/workspace/tmp/pusat-komando-push/data/skills/laporan-abstrak/SKILL.md`

## Alternatives for better results

- Bila yang ditemukan adalah selisih otorisasi antar kanal/versi, bukan urutan langkah: lanjutkan dengan `diskrepansi-autentikasi-lintas-kanal`.
- Bila lompatan ternyata soal objek milik akun lain (bukan urutan): lanjutkan dengan `access-control-differential-analyst`.
- Bila alur memakai race condition (dua permintaan bersamaan pada resource yang sama), bukan lompat langkah: lanjutkan dengan `perburuan-kerentanan-spesifik` Gerbang 1.2.
