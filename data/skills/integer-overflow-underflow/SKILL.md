# Skill: Integer Overflow & Underflow — Angka Melewati Batas Tipe Data, Nilai Berputar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk program bounty resmi berikut (9 program): Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar kesembilan program itu skill ini tidak boleh dipakai. Program yang relevan untuk skill ini: **HUNTR, Perplexity VDP (PPLX), Mistral VDP, Anthropic (ANTH), Muse** — program lain hanya bila scope tertulisnya menyatakan pengujian logika/angka klasik berlaku. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.

## Pemicu

Dipakai saat target in-scope menghitung dengan angka yang dikendalikan pengguna — saldo, jumlah, harga, kuantitas, batas, penghitung — dan ada dugaan perhitungan itu memakai tipe data berbatas (mis. bilangan bulat 32-bit atau 64-bit, atau bilangan tak bertanda) tanpa pemeriksaan batas: angka sangat besar yang melewati batas maksimum akan "berputar" menjadi angka kecil atau negatif, dan angka negatif yang melewati batas minimum akan berputar menjadi angka besar. Akibatnya saldo minus bisa menjadi besar, biaya bisa menjadi nol, atau jumlah bisa berbalik arah. Dipakai sesudah `fondasi-kerentanan-web-api` dikuasai dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Tanda pemicu: field angka yang menerima nilai sangat besar/negatif tanpa penolakan, perhitungan jumlah × harga, atau saldo yang berubah tidak wajar setelah operasi angka ekstrem.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan field angka dan tipe batas yang diduga |
| Pengerjaan | **A62 Exploit Developer** | Menguji nilai batas pada akun uji sendiri, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kerentanan logika/angka secara umum + standar pembuktian dampak → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian overflow/underflow, bukan mengulang konsepnya).
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Race condition/TOCTOU → sebagian tercakup di `perburuan-kerentanan-spesifik` — bukan skill ini (skill ini soal perhitungan angka, bukan soal urutan waktu permintaan).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Pengujian hanya pada akun uji sendiri dengan nilai canary.
3. **Tanpa data orang lain.** Tanpa mengubah saldo, harga, atau jumlah milik orang lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; uji satu nilai batas per putaran, dengan jeda.
6. **Tanpa payload di permukaan publik.** Nilai uji dan hasilnya jangan disebar — hanya dicatat di log internal.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengubah saldo atau harga nyata, DILARANG memakai nilai hasil overflow/underflow untuk mendapatkan barang/uang nyata, DILARANG membiarkan perubahan angka uji bertahan. Pembuktian HANYA dengan nilai canary pada akun sendiri, lalu KEMBALIKAN atau BATALKAN perubahannya segera.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian logika/angka diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu nilai uji pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali field angka dan perhitungannya

1. Tentukan field angka yang dikendalikan pengguna (jumlah, kuantitas, harga, saldo, batas) dan perhitungan apa yang memakai field itu (penjumlahan, perkalian jumlah × harga, pengurangan saldo).
2. Catat perilaku normal: respons untuk nilai biasa, dan apakah ada pemeriksaan batas (nilai maksimum/minimum yang ditolak).
3. **Standar lulus:** field + perhitungan tertulis beserta batas yang sudah diketahui. Field belum jelas = jangan menebak; petakan dulu lewat `pemetaan-permukaan-serangan`.

### Gerbang 2 — Uji nilai batas (boundary) pada akun sendiri

1. Uji nilai di sekitar batas tipe data yang diduga (mis. di sekitar 2^31-1, 2^32-1, 2^63-1, dan nilai negatif besar) pada SATU field, SATU nilai per uji, dengan nilai canary — amati apakah respons menolak, menerima normal, atau menerima dengan hasil yang berputar (mis. hasil perhitungan menjadi negatif atau nol).
2. Catat saldo/harga akun sendiri SEBELUM dan SESUDAH tiap uji.
3. **Standar lulus:** ada nilai batas yang diterima dengan hasil berputar (bukan sekadar ditolak dan bukan sekadar diterima normal). Semua nilai batas ditolak atau dihitung normal = AMAN, tutup dengan buktinya.

### Gerbang 3 — Buktikan dampak dengan nilai canary, lalu kembalikan/batalkan

1. Dengan nilai batas dari Gerbang 2, buktikan dampak pada akun uji SENDIRI dengan nilai canary: mis. jumlah canary yang setelah perhitungan menjadi nol atau berbalik, atau saldo canary yang berubah tidak wajar.
2. SEGERA kembalikan atau batalkan perubahan itu (batalkan transaksi, kembalikan saldo ke nilai semula, atau minta pengembalian lewat alur yang sah) dan catat pengembaliannya.
3. **Standar lulus:** dampak teramati pada akun sendiri dengan nilai canary DAN perubahan sudah dikembalikan/dibatalkan dengan bukti pengembaliannya. Dampak tanpa pengembalian = BELUM SELESAI, jangan maju ke laporan.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis dampak konkret: perhitungan apa yang berputar, nilai apa yang dihasilkan, dan apa yang bisa dilakukan penyerang dengannya (mis. biaya menjadi nol, saldo menjadi besar) — tulis sesuai bukti Gerbang 3, jangan membesar-besarkan.
2. Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.
3. **Standar lulus:** dampak ditulis konkret (perhitungan + nilai hasil + konsekuensinya), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / curl | Mengirim SATU nilai batas per uji ke field angka akun sendiri |
| Kalkulator nilai batas | Menentukan nilai di sekitar batas tipe data yang diduga (2^31, 2^32, 2^63) |
| Pencatat saldo/harga sebelum-sesudah | Mencatat nilai akun sendiri sebelum dan sesudah tiap uji + bukti pengembalian |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua nilai uji (nilai → hasil perhitungan → dikembalikan/tidak) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur/field angka]
Field + perhitungan: [field — perhitungan yang memakai field itu]
Nilai batas diuji: [nilai — hasil: ditolak / normal / berputar menjadi ...]
Dampak (nilai canary, akun sendiri): [saldo/harga/jumlah berubah menjadi ...]
Dikembalikan/dibatalkan: [ya — nilai semula ... / cara pengembalian ...]
Yang TIDAK dilakukan: [tanpa mengubah saldo/harga nyata, tanpa mengambil barang/uang nyata]
Dampak: [apa yang bisa dilakukan penyerang dengan perhitungan yang berputar]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Banyak sistem memakai bilangan presisi sewenang-wenang atau pemeriksaan batas yang benar — nilai ekstrem akan ditolak atau dihitung normal; itu AMAN, bukan temuan.
- Hasil "berputar" di satu lapisan belum tentu sampai ke saldo/harga akhir (bisa dicek ulang di lapisan lain) — vonis datang dari Gerbang 3, bukan dari Gerbang 2.
- Jangan menguji nilai batas pada transaksi nyata atau dengan uang sungguhan — hanya nilai canary pada akun uji sendiri, lalu kembalikan/batalkan.
