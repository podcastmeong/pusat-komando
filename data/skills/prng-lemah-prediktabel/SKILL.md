# Skill: PRNG Lemah & Prediktabel — Seed Mudah Ditebak, Kunci dan Token Bisa Direkonstruksi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk program bounty resmi berikut (9 program): Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar kesembilan program itu skill ini tidak boleh dipakai. Program yang relevan untuk skill ini: **HUNTR, Perplexity VDP (PPLX), Mistral VDP, Anthropic (ANTH)** — program lain hanya bila scope tertulisnya menyatakan pengujian kriptografi klasik berlaku. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.

## Pemicu

Dipakai saat target in-scope menghasilkan nilai yang seharusnya acak — kunci enkripsi, token sesi, token reset kata sandi, kode sekali pakai, pengenal (ID) yang tidak bisa ditebak, atau angka undian — dengan pembangkit bilangan acak yang lemah atau seed yang mudah ditebak, misalnya waktu sistem (detik/milidetik saat proses berjalan), pengenal proses, atau nilai awal yang kecil dan bisa dienumerasi. Dipakai sesudah `fondasi-kerentanan-web-api` dikuasai dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Tanda pemicu: token yang polanya berurutan atau berdekatan, token yang berubah mengikuti jam, nilai acak yang terulang setelah restart, atau kode yang memakai pembangkit acak non-kriptografis untuk keperluan keamanan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan sumber keacakan dan pola seed target |
| Pengerjaan | **A62 Exploit Developer** | Menguji prediksi di lab pada sistem sendiri, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kerentanan kriptografi secara umum + standar pembuktian dampak → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian PRNG lemah, bukan mengulang konsepnya).
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Kerentanan kriptografi lain (kolisi hash, padding oracle) → skill masing-masing — bukan skill ini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Rekonstruksi hanya dilakukan atas token/kunci akun uji sendiri atau sistem/aplikasi sendiri.
3. **Tanpa data orang lain.** Tanpa merekonstruksi kunci, token, atau sesi milik orang lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; enumerasi seed dilakukan secukupnya dan dengan jeda.
6. **Tanpa payload di permukaan publik.** Token/kunci hasil rekonstruksi jangan disebar — hanya dicatat di log internal.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG merekonstruksi kunci/token milik orang lain, DILARANG memakai token hasil rekonstruksi untuk masuk ke akun orang lain, DILARANG mengubah atau membocorkan kunci/token apa pun. Pembuktian HANYA pada akun uji sendiri, dan berhenti di situ.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian kriptografi/PRNG diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu token uji pun diminta. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali sumber keacakan target

1. Tentukan nilai acak apa yang dihasilkan target (token sesi, token reset, kunci, kode sekali pakai) dan dari mana keacakannya berasal — dari dokumentasi, kode yang tersedia, atau pola nilai yang teramati.
2. Amati pola: apakah token berurutan, berdekatan, berulang, atau berubah mengikuti waktu? Catat beberapa sampel token dari akun uji sendiri beserta waktu pembuatannya.
3. **Standar lulus:** jenis nilai acak + dugaan sumber keacakan tertulis beserta sampel. Bila token tampak acak kuat (panjang, tanpa pola, tidak berkorelasi dengan waktu) = AMAN, tutup dengan buktinya.

### Gerbang 2 — Uji hipotesis seed di lab sendiri

1. Di lab sendiri, bangun replika pola pembangkitan yang diduga (mis. seed = waktu sistem saat token dibuat) dan periksa apakah replika itu menghasilkan nilai yang sama dengan token akun uji sendiri.
2. Uji dengan beberapa sampel: replika harus cocok pada lebih dari satu token, bukan satu kebetulan.
3. **Standar lulus:** replika lab menghasilkan nilai yang sama dengan token akun uji sendiri pada minimal 2 sampel dengan waktu berbeda. Satu kecocokan = belum terbukti (bisa jadi kebetulan).

### Gerbang 3 — Buktikan prediksi token baru milik sendiri

1. Dengan model seed dari Gerbang 2, prediksi token berikutnya yang akan dibuat untuk akun uji SENDIRI, lalu minta target membuat token itu dan bandingkan dengan prediksi.
2. Uji HANYA pada akun uji sendiri. Jangan pernah memprediksi atau memakai token milik orang lain.
3. **Standar lulus:** prediksi cocok dengan token nyata akun sendiri minimal 2x berturut-turut. Prediksi yang hanya cocok sekali = belum terbukti.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis dampak konkret: nilai apa yang bisa diprediksi penyerang (token reset, token sesi, kunci) dan apa yang bisa dilakukan dengannya atas akun yang tokennya bisa diprediksi — tulis sesuai bukti Gerbang 3, jangan membesar-besarkan.
2. Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.
3. **Standar lulus:** dampak ditulis konkret (nilai yang bisa diprediksi + konsekuensinya), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / curl | Meminta token untuk akun uji sendiri dan mencatat waktu pembuatannya |
| Lab replika (skrip sendiri di lingkungan sendiri) | Menguji hipotesis seed terhadap token akun sendiri; hanya bila program mengizinkan otomasi |
| Pencatat waktu + sampel token | Mencatat waktu pembuatan tiap token dan nilai tokennya untuk analisis pola |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua sampel token (waktu → nilai → prediksi → cocok/tidak) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur yang menghasilkan nilai acak]
Nilai acak: [token sesi / token reset / kunci / kode sekali pakai]
Dugaan sumber keacakan: [waktu sistem / seed kecil / PRNG non-kriptografis — bukti pola]
Bukti prediksi (akun sendiri): [prediksi vs token nyata — cocok 2x atau lebih]
Yang TIDAK dilakukan: [tanpa merekonstruksi kunci/token orang lain, tanpa memakai token orang lain]
Dampak: [nilai apa yang bisa diprediksi + apa yang bisa dilakukan dengannya]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Pola yang "kelihatan berurutan" belum tentu bisa diprediksi — vonis datang dari Gerbang 3 (prediksi yang cocok berulang), bukan dari kesan pola di Gerbang 1.
- Banyak sistem memakai pembangkit acak kriptografis yang kuat di balik tampilan yang sederhana; jangan klaim lemah hanya dari panjang token yang pendek.
- Bila seed memakai entropi yang tidak bisa diamati dari luar (mis. dari perangkat keras), prediksi dari luar tidak mungkin — catat sebagai batas, jangan memaksakan hipotesis.
