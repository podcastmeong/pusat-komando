# Skill: Etika & Kerahasiaan Data dalam Bounty — Standar Etika Profesional untuk Menangani Temuan dan Data

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 5, 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill standar/metode — mengatur CARA temuan dan data ditangani — BUKAN skill pengujian: skill ini tidak memberi langkah untuk menemukan atau mengeksploitasi kerentanan. Kerangka etikanya mengikuti standar etika profesional gaya EC-Council (kode etik peretas etis: legalitas, kerahasiaan, responsible disclosure, tidak merugikan pihak lain); sertifikasi seperti EC-Council disebut di sini HANYA sebagai rujukan kredibilitas, bukan sebagai isi skill — skill ini tidak mengajarkan materi sertifikasi dan tidak menjanjikan sertifikasi apa pun.

## Pemicu

Dipakai setiap kali perburuan menyentuh data apa pun di luar data canary milik sendiri: temuan yang menampilkan data pengguna lain, data internal program, PII (nama, email, nomor telepon, alamat, kredensial, token), atau data yang secara tidak sengaja terungkap selama pengujian. Dipakai juga SEBELUM laporan ditulis (memutuskan data apa yang boleh masuk laporan dan apa yang wajib disamarkan/dihapus), SEBELUM bukti PoC disimpan atau dibagikan, dan setiap kali ada keraguan apakah suatu data boleh disimpan, dipakai, atau diteruskan. Bila tidak ada data pihak lain yang tersentuh sama sekali, skill ini cukup dibaca sebagai pengingat — tetapi keputusan "tidak ada data pihak lain" itu sendiri wajib dicatat di log.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Menerapkan standar etika pada setiap temuan yang ditangani; memutuskan klasifikasi data temuan |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai apakah data dalam temuan termasuk PII/data sensitif; menyamarkan data sebelum masuk draf laporan |
| Audit | **A60 Security Auditor** | Memvalidasi keputusan etika + penyamaran data sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase dan data apa yang boleh diteruskan ke program |

## Sudah tercakup (jangan diduplikat)

- Mekanik penanganan token/PII/kredensial di dalam bukti PoC (cara menyamarkan, menyimpan, dan menghapus token serta kredensial dari bukti) → skill `kebersihan-bukti`. Skill ini TIDAK mengulang mekanik itu — skill ini mengatur KEPUTUSAN etikanya (data apa yang boleh disimpan/dipakai/dilaporkan), sedangkan `kebersihan-bukti` mengatur CARA membersihkannya.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Pemantauan program bounty (scope/hadiah/deadline program) → skill `recon-pantau-program`. Skill ini tidak memantau program — skill ini mengatur penanganan data temuan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Data yang dipakai dalam pengujian hanyalah akun dan data milik sendiri atau data canary palsu yang dibuat untuk pengujian.
3. **Tanpa data orang lain.** Data pengguna lain, data internal program, atau data pihak ketiga yang terungkap selama pengujian TIDAK BOLEH disimpan, disalin, dipakai, atau dibagikan di luar PoC minimal yang dibutuhkan untuk membuktikan temuan — dan PoC itu sendiri wajib disamarkan (lihat Langkah 3).
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan atau akun yang bukan milik sendiri DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan, termasuk lewat pengumpulan data massal.
6. **Tanpa payload di permukaan publik.** Bukti, tangkapan layar, dan draf laporan yang memuat data temuan jangan di-host atau dibagikan di tempat umum — hanya di lingkungan terkendali milik sendiri dan jalur resmi program.
7. **Validasi human-in-the-loop.** Setiap keputusan etika (boleh/tidak suatu data disimpan atau dilaporkan) harus diperiksa manusia (Muse/A60) sebelum dijalankan — jangan serahkan keputusan etika ke otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta. Laporan yang memuat data pihak lain wajib ditandai eksplisit di drafnya.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data apa pun — termasuk data temuan. DILARANG memakai data temuan untuk mengakses akun siapa pun, memeras, mengancam, atau memperoleh keuntungan di luar hadiah bounty resmi. DILARANG menyimpan salinan data temuan setelah laporan selesai — hapus sesuai Langkah 5.

## Langkah + gerbang

### Gerbang 0 — Cek scope + kebijakan disclosure program dulu

1. Baca pasal scope dan kebijakan disclosure program target: apakah responsible disclosure diwajibkan, berapa tenggat embargo, apakah data temuan boleh disertakan dalam laporan, dan lewat jalur apa laporan dikirim.
2. **Standar lulus:** pasal scope + kebijakan disclosure + jalur laporan tercatat di log sebelum data temuan apa pun ditangani. Tanpa itu = jangan lanjut.

### Gerbang 1 — Klasifikasikan data yang tersentuh

1. Untuk setiap data yang muncul selama pengujian, klasifikasikan: (a) data canary milik sendiri — bebas dipakai; (b) PII pengguna lain (nama, email, telepon, alamat, foto) — sensitif; (c) kredensial/token/kunci — sangat sensitif; (d) data internal program (konfigurasi, data bisnis) — rahasia program; (e) data publik yang memang ditampilkan target untuk umum — bukan temuan.
2. **Standar lulus:** setiap data tercatat dengan klasifikasinya. Data yang tidak terklasifikasi = perlakukan sebagai sangat sensitif sampai A60 memutuskan lain.

### Gerbang 2 — Minimalkan: berhenti di bukti minimal

1. Begitu temuan terbukti, BERHENTI mengumpulkan data. Ambil hanya bukti minimal yang menunjukkan kerentanan itu ada (mis. satu baris yang membuktikan akses, bukan seluruh daftar). Jangan mengunduh, mengekspor, atau menyalin kumpulan data.
2. **Standar lulus:** bukti yang disimpan hanya yang dibutuhkan untuk reproduksi temuan; jumlah data yang disimpan tercatat (mis. "1 baris, 2 kolom"). Bila bukti yang ada sudah melebihi kebutuhan = hapus kelebihannya sekarang dan catat penghapusannya.

### Gerbang 3 — Samarkan sebelum masuk laporan

1. Samarkan semua PII/kredensial/token dalam bukti dan draf laporan (nama → inisial, email → sebagian disensor, token/kredensial → hapus seluruhnya dan ganti penanda seperti `[TOKEN-DIHAPUS]`). Mekanik penyamaran dan penyimpanannya mengikuti skill `kebersihan-bukti` — jangan buat cara sendiri.
2. **Standar lulus:** draf laporan diperiksa A60 dan TIDAK memuat satu pun PII/kredensial/token utuh milik pihak lain. Satu nilai utuh yang lolos = draf DITOLAK, ulangi gerbang ini.

### Gerbang 4 — Responsible disclosure lewat jalur resmi

1. Kirim laporan HANYA lewat jalur resmi program (platform bounty atau alamat disclosure yang ditetapkan program), dalam tenggat embargo yang berlaku. Jangan umumkan temuan di media sosial, forum, atau kanal publik sebelum program mengizinkan — embargo berlaku sampai program menyatakan temuan selesai ditangani atau memberi izin publikasi.
2. **Standar lulus:** bukti pengiriman lewat jalur resmi + status embargo tercatat. Laporan yang bocor ke publik sebelum izin = pelanggaran etika — laporkan ke Muse segera.

### Gerbang 5 — Hapus data temuan setelah selesai

1. Setelah laporan dikirim (atau ditolak triase), hapus semua salinan data pihak lain dari mesin kerja, bukti, dan draf — sisakan hanya log keputusan (apa yang ditemukan, klasifikasi datanya, kapan dihapus) tanpa isi datanya. Konfirmasi penghapusan dicatat di log.
2. **Standar lulus:** tidak ada lagi salinan data pihak lain yang tersimpan; catatan penghapusan (tanggal + apa yang dihapus) ada di log. Data yang masih tersimpan setelah laporan selesai = pelanggaran — hapus dan laporkan ke Muse.

### Gerbang 6 — Serahkan ke triase

1. Serahkan draf (yang sudah disamarkan) ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.
2. **Standar lulus:** keputusan triase tercatat + persetujuan Cipta tercatat. Tanpa keduanya = belum berhasil, jangan maju ke pengiriman.

## Alat

| Alat | Cara pakai |
|---|---|
| Kebijakan scope + disclosure tiap program | Sumber kebenaran untuk Gerbang 0 dan 4 — baca sebelum menangani data |
| Skill `kebersihan-bukti` | Mekanik menyamarkan/menyimpan/menghapus token, PII, dan kredensial dalam bukti PoC |
| Daftar klasifikasi data (Gerbang 1) | Templat klasifikasi a–e di atas; salin ke log tiap temuan |
| `~/workspace/catatan/log-bug-bounty.md` | Log klasifikasi data + keputusan etika + penyamaran + penghapusan + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [satu dari sembilan program resmi]
Temuan: [judul singkat — tanpa data pihak lain]
Data yang tersentuh: [klasifikasi per data: canary sendiri / PII / kredensial-token / internal program / publik]
Bukti minimal: [apa yang disimpan — jumlah + jenis, mis. "1 baris, 2 kolom"]
Penyamaran: [apa yang disensor/dihapus — mengikuti kebersihan-bukti; "tidak ada data pihak lain" bila tidak ada]
Jalur disclosure: [jalur resmi program + status embargo]
Data dihapus: [ya — tanggal ... / tidak ada data pihak lain yang disimpan]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Skill ini mengatur keputusan etika, bukan memberi nasihat hukum. Bila suatu temuan menyentuh data yang berpotensi melanggar hukum (mis. data anak, data kesehatan, data keuangan), serahkan ke Muse/Cipta sebelum langkah apa pun — jangan putuskan sendiri.
- Kebijakan disclosure berbeda-beda per program (tenggat embargo, data yang boleh dilampirkan). Selalu baca kebijakan program target — jangan menggeneralisasi dari satu program ke program lain.
- Sertifikasi (mis. EC-Council) disebut hanya sebagai rujukan kredibilitas kerangka etika ini; skill ini tidak mengajarkan materi sertifikasi dan tidak menggantikan pelatihan etika formal.
- Bila program tidak punya kebijakan disclosure tertulis, perlakukan sebagai embargo penuh: jangan publikasikan apa pun sampai program memberi izin eksplisit.

### Available connectors

Tidak ada konektor khusus untuk skill ini; keputusan etika dicatat manual di log dan divalidasi A60/Muse.

### Websites

- Halaman aturan dan kebijakan disclosure resmi tiap program (sumber scope + tenggat embargo + jalur laporan).
- Kode etik EC-Council sebagai rujukan kerangka etika profesional (hanya rujukan — bukan isi skill ini).

### Alternatives for better results

- Bila ragu apakah suatu data termasuk PII atau bukan, perlakukan sebagai PII sampai A60 memutuskan lain — lebih aman menyamarkan berlebihan daripada membocorkan satu nilai.
- Bila temuan menampilkan data dalam jumlah besar sebelum sempat dihentikan, catat jumlah dan jenisnya secara jujur di log, hapus segera, dan laporkan ke Muse — menyembunyikan insiden lebih buruk daripada melaporkannya.
