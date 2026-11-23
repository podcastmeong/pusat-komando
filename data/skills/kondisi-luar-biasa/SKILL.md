# Skill: Kondisi Luar Biasa — Edge-Case Logika Aplikasi (Overflow, Null/NaN, Timeout Parsial & Gagal Rollback)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`), Kategori 2, butir hunt-exceptional-conditions. Belum pernah dipakai dalam perburuan nyata oleh tim; nilai batas dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat ada hipotesis celah logika bisnis yang hanya muncul pada kondisi luar biasa — nilai di batas tipe data, nilai kosong/aneh, atau transaksi yang tidak selesai utuh — dan hipotesis itu harus dibuktikan dampaknya sebelum maju ke triase. Dipakai sesudah fondasi (`fondasi-kerentanan-web-api`) dan sesudah `perburuan-kerentanan-spesifik` dikuasai — skill ini menambah 4 keluarga edge-case yang belum tercakup di keduanya, bukan menggantikannya. Bukan untuk bounty agen AI — ini teknik web/API klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan 4 keluarga edge-case pada tiap hipotesis dan pengujian |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar lulus keluarga itu |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Business Logic Flaws umum** (manipulasi harga/jumlah, lompat langkah state machine, penyalahgunaan kupon/referral) → skill `perburuan-kerentanan-spesifik` Gerbang 1.1. Skill ini BUKAN itu: skill ini hanya untuk 4 keluarga edge-case di bawah, yang cara mengenalinya (nilai batas/tipe/transaksi) berbeda dari logika bisnis biasa.
- **Race Condition** (dua permintaan bersamaan memakai resource yang sama) → skill `perburuan-kerentanan-spesifik` Gerbang 1.2. Timeout parsial di skill ini adalah SATU alur yang tidak selesai utuh, bukan dua permintaan yang berlomba — jangan campur keduanya. Bila temuannya butuh konkurensi, pakai skill race condition itu.
- **IDOR, SSRF, XSS, Broken Auth, salah konfigurasi API** → skill `fondasi-kerentanan-web-api` (jangan ulangi kelimanya di sini).
- **Variasi payload secara sistematis** → skill `rekonstruksi-iterasi-payload` (satu dimensi per putaran).
- **Validasi temuan + laporan triage-ready** → skill `triase-duplikat` + `laporan-abstrak`.

## Trigger & Scope

- **Trigger:** ada endpoint/fitur in-scope yang menerima angka, field yang bisa kosong, atau alur multi-langkah bertransaksi (keranjang → bayar → konfirmasi; transfer → catat → notifikasi) — dan salah satu dari 4 keluarga di bawah diduga tidak ditangani server.
- **Scope:** HANYA data, akun, dan transaksi milik akun tes sendiri. Pengujian edge-case dilakukan pada alur milik sendiri (keranjang sendiri, saldo sendiri, pesanan sendiri) dengan nilai terkecil yang masih membuktikan hipotesis.
- **Di luar scope:** memicu edge-case pada transaksi/data pengguna lain; memaksa kegagalan basis data (mematikan koneksi, membanjiri dengan timeout); menguji rollback dengan merusak state produksi. Bila sebuah keluarga hanya bisa dibuktikan dengan merusak data orang lain atau produksi, keluarga itu = TIDAK DAPAT DIBUKTIKAN secara aman — catat, jangan uji.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Satu permintaan edge-case sekali jalan, rate limit ≤5 req/detik; JANGAN mengirim banjir permintaan timeout/lambat untuk memaksa kegagalan (itu DoS, bukan pembuktian).
6. **Tanpa payload di permukaan publik.** Nilai uji adalah nilai edge-case yang valid secara format (angka batas, null, string kosong) pada field milik sendiri — bukan payload eksploitasi, bukan injeksi.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
11. **Picu edge-case HANYA pada data/akun uji sendiri.** Jangan rusak state transaksi pengguna lain; jangan picu rollback gagal pada data produksi; jangan memaksa timeout pada transaksi yang melibatkan pihak lain. Bila pengujian berisiko menyentuh state orang lain, HENTIKAN dan serahkan ke Muse.
12. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "kelihatan rentan" tanpa pembuktian dampak = tidak maju ke triase.
13. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.
14. **Berhenti otomatis bila respons menunjukkan kerusakan.** Bila satu uji edge-case mengembalikan error massal, state rusak, atau saldo/angka yang tidak bisa dijelaskan — HENTIKAN pengujian pada fitur itu, catat state sebelum/sesudah, laporkan ke Muse. Jangan mengulang untuk "memastikan" dengan merusak lebih jauh.

## Methodology & Payloads

### 4 keluarga edge-case (dipakai di Gerbang 1)

#### 1. Integer overflow / underflow & nilai batas

- **Definisi:** field angka yang disimpan dalam tipe berhingga (mis. int32: maks 2.147.483.647; int64; unsigned) dan server tidak memeriksa batas — nilai di atas maks "meluber" menjadi negatif/nol, atau nilai negatif diterima untuk jumlah/harga/saldo.
- **Cara mengenali:** cari field angka yang menentukan nilai (jumlah, kuantitas, harga, saldo, poin, stok) dan dikirim dari klien; periksa apakah server menolak nilai di luar akal (negatif, nol, sangat besar) atau menerimanya diam-diam.
- **Nilai uji (SATU dimensi per putaran, nilai milik sendiri):** 0, -1, -999, 2.147.483.647 (batas int32), 2.147.483.648 (satu di atas batas), 9.223.372.036.854.775.807 (batas int64) — mulai dari yang paling kecil/aman (0, -1) dan naik hanya bila yang kecil ditolak dengan benar; JANGAN langsung memakai nilai terbesar pada transaksi bernilai uang.
- **Cara membuktikan dampak:** buktikan dengan perubahan state nyata pada akun sendiri — mis. kuantitas negatif benar-benar menambah saldo, harga akhir benar-benar menjadi negatif/nol dan transaksi tetap jalan, stok benar-benar bertambah lewat underflow. Simpan respons server + state sebelum/sesudah (saldo, kuantitas, status pesanan).
- **Standar lulus:** ada bukti perubahan state nyata pada akun sendiri (angka/status sebelum vs sesudah) + langkah reproduksi persis. Sekadar "nilai besar diterima di permintaan" tanpa perubahan state yang diterima server = belum terbukti.

#### 2. Penanganan null / NaN / tipe kosong

- **Definisi:** field yang dikirim sebagai `null`, `NaN`, string kosong, array kosong, atau tipe yang salah (string untuk angka, angka untuk boolean) dan server tidak menanganinya — field yang seharusnya wajib jadi terlewat, pengecekan dilewati, atau nilai default yang berbahaya dipakai.
- **Cara mengenali:** cari field wajib dalam alur (harga, jumlah, ID pemilik, persetujuan) yang pengecekannya mungkin hanya di klien; cari field yang bila kosong mengubah makna (mis. `discount: null` diartikan "tanpa batas", `role: null` diartikan "admin default").
- **Nilai uji (SATU dimensi per putaran, data milik sendiri):** `null`, string kosong `""`, array kosong `[]`, objek kosong `{}`, `NaN`, 0 untuk field yang seharusnya wajib isi — satu nilai sekali jalan, jangan gabungkan beberapa field aneh sekaligus (bila digabung, tidak jelas mana yang menyebabkan efek).
- **Cara membuktikan dampak:** buktikan dengan perubahan state nyata pada akun sendiri — mis. field harga `null` benar-benar membuat total menjadi 0 dan pesanan tetap dibuat, field persetujuan `null` benar-benar melompati langkah wajib, atau `role: null` benar-benar memberi akses yang seharusnya tidak ada. Simpan request + respons + state sebelum/sesudah.
- **Standar lulus:** ada bukti perubahan state nyata pada akun sendiri + langkah reproduksi persis + nilai persis yang memicunya (satu nilai, bukan gabungan). Sekadar "server mengembalikan 500 untuk null" = BUKAN temuan (error saja, tanpa dampak bisnis).

#### 3. Timeout transaksi parsial

- **Definisi:** alur multi-langkah (mis. potong saldo → buat pesanan → kirim notifikasi) yang tidak atomik — bila satu langkah lambat/gagal di tengah (timeout), langkah sebelumnya sudah terlanjur terjadi dan tidak dibatalkan, sehingga state menjadi setengah jadi: saldo terpotong tapi pesanan tidak ada, atau pesanan ada tapi pembayaran tidak tercatat.
- **Cara mengenali:** cari alur yang terdiri dari 2+ langkah berurutan yang saling bergantung, terutama yang memanggil layanan pihak ketiga (pembayaran, notifikasi, stok) di tengah alur; cari langkah yang tidak punya kompensasi (tidak ada pembatalan otomatis bila langkah berikutnya gagal).
- **Nilai uji (SATU alur sekali jalan, akun sendiri):** jalankan alur normal milik sendiri SEKALI dengan kondisi yang memperlambat SATU langkah yang sah (mis. nilai yang membuat langkah tengah memakan waktu, atau membatalkan alur di titik yang disediakan aplikasi sendiri seperti tombol "batal" di tengah alur) — JANGAN mematikan koneksi, membanjiri server, atau memutus paksa dari luar untuk memaksa timeout.
- **Cara membuktikan dampak:** buktikan dengan state yang tidak konsisten pada akun sendiri — mis. saldo terpotong tapi pesanan tidak tercatat, atau pesanan tercatat ganda dari satu pembayaran. Simpan state sebelum (saldo, daftar pesanan) + respons tiap langkah + state sesudah.
- **Standar lulus:** ada bukti state setengah jadi yang bertahan (bukan sesaat) pada akun sendiri + langkah reproduksi persis + bukti langkah yang gagal vs langkah yang sudah terjadi. State yang pulih sendiri dalam hitungan detik (retry otomatis berhasil) = belum terbukti — catat sebagai "pulih otomatis".

#### 4. Kegagalan rollback basis data

- **Definisi:** alur yang seharusnya membatalkan SEMUA langkah bila satu langkah gagal (transaksi basis data), tapi rollback-nya tidak jalan — sebagian langkah tetap tersimpan sehingga state menjadi tidak konsisten (mis. kupon terpakai tapi pesanan gagal; poin terpotong tapi hadiah tidak keluar).
- **Cara mengenali:** cari alur yang secara dokumen/nalar harus atomik (pakai kupon + buat pesanan; potong poin + beri hadiah; transfer + catat mutasi) — lalu cari cara yang sah untuk menggagalkan langkah AKHIR alur itu pada data sendiri (mis. memasukkan data tidak valid pada langkah terakhir yang disediakan aplikasi, atau membatalkan di titik yang disediakan aplikasi).
- **Nilai uji (SATU alur sekali jalan, akun sendiri):** jalankan alur milik sendiri sampai langkah terakhir, lalu gagalkan langkah terakhir dengan cara yang disediakan aplikasi (input tidak valid pada field terakhir, batalkan di konfirmasi akhir) — JANGAN merusak basis data, mematikan layanan, atau memaksa kegagalan dari luar.
- **Cara membuktikan dampak:** buktikan dengan state yang tidak konsisten pada akun sendiri — mis. kupon/poin sudah terpotong padahal pesanan/hadiah gagal, dan potongan itu TIDAK kembali setelah menunggu wajar. Simpan state sebelum (saldo kupon/poin) + respons langkah gagal + state sesudah (setelah jeda wajar, mis. 5 menit, untuk memberi kesempatan rollback otomatis).
- **Standar lulus:** ada bukti langkah awal tetap tersimpan padahal langkah akhir gagal (state sebelum vs sesudah setelah jeda wajar) + langkah reproduksi persis. Potongan yang kembali sendiri setelah jeda = rollback jalan, BUKAN temuan — catat sebagai "rollback berfungsi".

## Langkah + gerbang

### Gerbang 1 — Kuasai 4 keluarga ini

Pelajari dan hafalkan definisi, cara mengenali, dan cara membuktikan dampak tiap keluarga di atas. A58 wajib bisa menjelaskan keempatnya dengan contoh sebelum menguji.

### Gerbang 2 — Nilai hipotesis dengan keluarga ini

1. Setiap hipotesis dinilai: keluarganya apa (salah satu dari 4 di atas, atau kategori `perburuan-kerentanan-spesifik` / fondasi — bila itu, pakai skill tersebut)? Nilai uji persisnya apa (satu nilai, satu dimensi)? Cara pembuktian dampaknya apa (sesuai standar lulus keluarga itu)?
2. Periksa keamanan hipotesis SEBELUM menguji: apakah pengujian hanya menyentuh data/akun/transaksi sendiri? Bila ada risiko menyentuh state orang lain atau produksi — TOLAK hipotesis itu, catat alasannya, jangan uji.
3. **Standar lulus:** tiap hipotesis yang maju punya label keluarga + nilai uji persis + rencana pembuktian dampak + pernyataan keamanan ("hanya data sendiri"). Hipotesis tanpa label keluarga, tanpa nilai uji persis, atau tanpa pernyataan keamanan = ditolak, jangan diuji.

### Gerbang 3 — Buktikan dampak, serahkan ke triase

1. Pengujian memakai `rekonstruksi-iterasi-payload` (variasi terarah, satu dimensi per putaran); bukti memakai standar lulus tiap keluarga di atas. Untuk keluarga 3 dan 4, beri jeda wajar sebelum menilai state akhir (rollback/retry otomatis butuh waktu) dan catat waktu tunggunya.
2. Ulangi dari state bersih untuk memastikan hasilnya bisa diulang, bukan kebetulan sekali jalan — minimal 2 kali percobaan berhasil untuk keluarga 1 dan 2; untuk keluarga 3 dan 4, satu reproduksi dari state bersih + bukti state bertahan sudah cukup bila pengulangan berisiko merusak state sendiri (catat bila hanya sekali).
3. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
4. **Standar lulus:** keputusan triase tercatat di log dengan alasan; tidak ada temuan yang maju tanpa bukti state sebelum/sesudah pada akun sendiri.

## Validation Gate

Verifikasi deterministik baseline vs edge-case — WAJIB sebelum edge-case dinyatakan rentan:

1. **Baseline tercatat:** alur yang SAMA dengan nilai NORMAL pada akun sendiri harus berhasil (atau memberi respons yang diharapkan). Bila baseline saja gagal, pengujian tidak valid — perbaiki alurnya dulu, jangan simpulkan celah.
2. **Satu dimensi berbeda:** antara baseline dan uji edge-case, HANYA satu nilai/satu langkah yang diubah. Bila dua hal diubah sekaligus, hasilnya tidak bisa diatribusikan — ulangi dengan satu perubahan.
3. **Dampak nyata pada akun sendiri:** ada perubahan state yang merugikan/menguntungkan secara nyata (saldo, status pesanan, kupon/poin, akses) — bukan sekadar status HTTP atau pesan error yang berbeda.
4. **Dapat diulang dari state bersih:** hasil yang sama dari state bersih (minimal 2 kali untuk keluarga 1–2; 1 kali + bukti bertahan untuk keluarga 3–4 bila pengulangan berisiko).
5. **Yang TIDAK lolos gate:** error 500 tanpa perubahan state (= bukan temuan bisnis); hasil sekali jalan tanpa pengulangan (keluarga 1–2); state yang pulih sendiri setelah jeda wajar (= rollback/retry berfungsi); pengujian yang menyentuh data orang lain (= batal, hapus dari log, laporkan ke Muse). Satu gate gagal = BELUM TERBUKTI.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri | Bila relevan: akun kedua milik sendiri untuk membuktikan efek lintas akun (mis. `role: null` pada akun kedua) — keduanya milik sendiri. |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian. |
| Browser / curl (permintaan HTTP biasa) | Menjalankan alur milik sendiri + mengirim nilai edge-case satu per satu; simpan request + respons + state sebelum/sesudah. |
| `rekonstruksi-iterasi-payload` | Variasi terarah satu dimensi per putaran. |
| `perburuan-kerentanan-spesifik` | Rujukan kategori business logic / race condition bila hipotesis ternyata masuk ke sana. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + keluarga + nilai uji + bukti dampak + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint/fitur]
Keluarga edge-case: [Integer Overflow / Null-NaN / Timeout Parsial / Gagal Rollback]
Nilai uji: [nilai persis, satu dimensi] | Baseline: [nilai normal + hasil baseline]
Cara mengenali: [tanda yang ditemukan]
Pembuktian dampak: [state sebelum → state sesudah pada akun sendiri + langkah reproduksi persis]
Pengulangan: [n kali dari state bersih + hasil]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini hanya mencakup 4 keluarga edge-case dari riset Kategori 2; tiap keluarga punya varian yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Keluarga 3 dan 4 sangat bergantung pada cara aplikasi menangani kegagalan — tidak ada daftar cek universal; pemetaan alur multi-langkah per target wajib dibuat sebelum menguji.
- Nilai batas integer bergantung pada tipe data server (int32 vs int64 vs desimal) — bila tipe tidak diketahui, mulai dari nilai kecil/aman (0, -1) dan naik bertahap; jangan langsung memakai nilai terbesar pada transaksi bernilai uang.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik di atas — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.

### Available connectors

Tidak ada konektor khusus untuk skill ini; pengujian dilakukan lewat HTTP biasa pada alur milik sendiri.

### Websites

- Halaman aturan program resmi (sumber scope Gerbang 0).
- Dokumentasi tipe data bahasa/framework server target (batas int32/int64 — untuk memilih nilai uji keluarga 1).

### Alternatives for better results

- Bila server menolak semua nilai edge-case dengan validasi yang benar (400 + pesan jelas + tanpa perubahan state): itu hasil yang sah — tulis "ditangani dengan benar", jangan menaikkan nilai untuk memaksa.
- Bila keluarga 3/4 hanya bisa dibuktikan dengan merusak data orang lain atau produksi: jangan uji — catat sebagai "tidak dapat dibuktikan secara aman" dan serahkan ke Muse.
- Bila efek edge-case ternyata butuh dua permintaan bersamaan untuk muncul: itu race condition — pakai `perburuan-kerentanan-spesifik` Gerbang 1.2, bukan skill ini.
