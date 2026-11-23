# Skill: Serangan Padding Oracle — Pesan Error Dekripsi Membocorkan Isi Pesan Terenkripsi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk program bounty resmi berikut (9 program): Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar kesembilan program itu skill ini tidak boleh dipakai. Program yang relevan untuk skill ini: **HUNTR, Perplexity VDP (PPLX), Mistral VDP, Anthropic (ANTH)** — program lain hanya bila scope tertulisnya menyatakan pengujian kriptografi klasik berlaku. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.

## Pemicu

Dipakai saat target in-scope mengembalikan pesan error (atau perilaku yang berbeda) ketika dekripsi gagal karena padding salah — misalnya respons "padding tidak valid" berbeda dari respons "dekripsi gagal" atau "token tidak valid", atau waktu respons/isi halaman berbeda antara padding benar dan padding salah. Perbedaan itu adalah oracle: penyerang bisa memakai perbedaan respons untuk mengupas isi pesan terenkripsi sedikit demi sedikit tanpa mengetahui kuncinya. Dipakai sesudah `fondasi-kerentanan-web-api` dikuasai dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Tanda pemicu: endpoint menerima token/ciphertext (cookie terenkripsi, token sesi terenkripsi, parameter terenkripsi) dan merespons berbeda saat ciphertext diubah.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan endpoint dan skema padding target |
| Pengerjaan | **A62 Exploit Developer** | Menguji oracle di lab dan pada ciphertext sendiri, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kerentanan kriptografi secara umum + standar pembuktian dampak → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian padding oracle, bukan mengulang konsepnya).
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Kerentanan kriptografi lain (kolisi hash, PRNG lemah) → skill masing-masing — bukan skill ini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Ciphertext yang diuji adalah milik sendiri atau yang dihasilkan untuk akun uji sendiri.
3. **Tanpa data orang lain.** Tanpa mendekripsi data pengguna lain, tanpa membaca isi pesan terenkripsi milik orang lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pengujian oracle dilakukan secukupnya, dengan jeda, dan berhenti bila rate-limit muncul.
6. **Tanpa payload di permukaan publik.** Ciphertext dan hasil dekripsi jangan disebar — hanya dicatat di log internal.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mendekripsi data pengguna lain, DILARANG memakai isi hasil dekripsi untuk masuk ke akun orang lain, DILARANG mengubah ciphertext milik orang lain. Pembuktian HANYA pada ciphertext sendiri, dan berhenti di situ.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian kriptografi/padding oracle diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu ciphertext uji pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali endpoint dan skema enkripsinya

1. Tentukan endpoint yang menerima ciphertext (cookie/token/parameter terenkripsi), skema yang diduga (mis. enkripsi blok dengan padding PKCS#7 — mode CBC adalah pola klasik yang rentan), dan apa yang terjadi bila ciphertext diubah.
2. Catat respons normal: respons untuk ciphertext valid milik akun uji sendiri.
3. **Standar lulus:** endpoint + bentuk ciphertext + respons normal tertulis. Skema belum jelas = cari bukti dulu (dokumentasi/respons); jangan menebak skema untuk langkah berikutnya.

### Gerbang 2 — Uji apakah ada oracle (padding benar vs padding salah)

1. Ubah satu byte ciphertext milik sendiri (mis. byte terakhir blok terakhir) dan kirim ke endpoint; bandingkan responsnya dengan respons untuk ciphertext yang tidak diubah.
2. Ulangi dengan beberapa perubahan berbeda dan catat: apakah respons membedakan "padding salah" dari "dekripsi gagal" atau "token tidak valid" (pesan berbeda, status berbeda, isi halaman berbeda, atau waktu respons berbeda)?
3. **Standar lulus:** perbedaan respons antara padding salah dan kesalahan lain teramati dan terulang minimal 2x dengan perubahan berbeda. Tanpa perbedaan yang konsisten = TIDAK ADA oracle, tutup dengan buktinya.

### Gerbang 3 — Buktikan oracle bisa mengupas isi ciphertext sendiri

1. Dengan oracle dari Gerbang 2, kupas ciphertext MILIK SENDIRI sedikit demi sedikit — satu byte per satu putaran, memakai perbedaan respons sebagai penanda benar/salah — sampai sebagian kecil isi plaintext milik sendiri berhasil ditebak dan diverifikasi (cocok dengan isi yang memang diketahui milik sendiri).
2. Kerjakan secukupnya saja untuk membuktikan oracle bekerja (beberapa byte cukup); jangan mengupas seluruh pesan bila tidak perlu, dan jangan pernah menyentuh ciphertext orang lain.
3. **Standar lulus:** minimal beberapa byte plaintext milik sendiri berhasil ditebak lewat oracle dan cocok dengan isi yang diketahui. Oracle yang terdeteksi tapi tidak bisa mengupas satu byte pun = belum terbukti, catat kenapa.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis dampak konkret: isi apa yang bisa dibocorkan oracle (mis. isi token sesi terenkripsi, data di cookie terenkripsi) dan apa yang bisa dilakukan dengannya — tulis sesuai bukti Gerbang 3, jangan membesar-besarkan.
2. Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.
3. **Standar lulus:** dampak ditulis konkret (isi yang bisa dibocorkan + konsekuensinya), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / curl | Mengirim ciphertext milik sendiri yang diubah dan mencatat perbedaan respons |
| Lab replika (skrip sendiri di lingkungan sendiri) | Menguji logika oracle terhadap ciphertext sendiri; hanya bila program mengizinkan otomasi |
| Pencatat respons (status, isi, waktu) | Membandingkan respons padding salah vs kesalahan lain |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua uji oracle (ciphertext diubah → respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint yang menerima ciphertext]
Skema enkripsi: [diduga — bukti identifikasi]
Oracle terdeteksi: [ya — perbedaan respons: pesan/status/isi/waktu — atau "TIDAK ADA"]
Bukti pengupasan (ciphertext sendiri): [byte plaintext milik sendiri yang berhasil ditebak + cocok dengan isi yang diketahui]
Yang TIDAK dilakukan: [tanpa mendekripsi data pengguna lain, tanpa memakai isi hasil dekripsi untuk akun lain]
Dampak: [isi apa yang bisa dibocorkan oracle + konsekuensinya]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Perbedaan respons bisa berasal dari hal lain (rate-limit, cache, WAF) — konfirmasi dengan pengulangan sebelum mengklaim ada oracle.
- Banyak sistem modern memakai enkripsi terautentikasi (mis. mode GCM) yang tidak punya padding oracle — bila target memakainya, oracle tidak ada; tutup sebagai AMAN dengan buktinya.
- Pengupasan penuh satu pesan bisa butuh banyak permintaan; kerjakan secukupnya untuk bukti, jangan membanjiri server (aturan keras 5).
