# Skill: Kebersihan Bukti — Kelola Token, PII & Kredensial dalam Bukti PoC secara Aman

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md` Kategori 4 butir 3 (evidence-hygiene). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu laporan yang buktinya dikelola dengan skill ini, dicatat di log, dan lolos triase.

## Pemicu (Trigger & Scope)

Dipakai setiap kali bukti PoC ditangkap, disimpan, dibagikan antar agent, atau dirakit menjadi draf laporan — yaitu di seluruh rantai `verifikasi-poc-aman` (tangkap) → `skeptic-false-positive-eliminator` (nilai) → `laporan-poc-otomatis` (rakit). Dipakai juga setiap kali bukti mengandung token sesi, kredensial, atau PII — yang hampir selalu terjadi pada bukti HTTP nyata. Satu temuan = satu paket bukti yang dikelola dari tangkap sampai laporan terkirim.

Skill ini adalah **pengelola bukti**, bukan penilai temuan: ia tidak memutuskan temuan valid atau tidak (itu tugas skeptic + gerbang tujuh pertanyaan), dan tidak menyusun narasi laporan (itu tugas `laporan-poc-otomatis`). Tugasnya: bukti yang sampai ke triager tetap bisa direproduksi, tetapi tidak membocorkan rahasia apa pun.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menangkap bukti dengan sensor + menyimpan sesuai Gerbang 1–2 |
| Pengerjaan | **A67 Report Writer** | Merakit bukti ke draf laporan sesuai format platform (Gerbang 3–4) |
| Audit | **A60 Security Auditor** | Memeriksa sensor + format sebelum draf maju ke tinjauan manusia; A60 tidak meloloskan buktinya sendiri |
| Pemimpin | **Muse** | Memutuskan paket bukti maju ke draf laporan atau dikembalikan |

## Sudah tercakup (jangan diduplikat)

- **Kewajiban sensor `[REDACTED]`** sudah disebut di `skeptic-false-positive-eliminator` (Gerbang 4), `verifikasi-poc-aman` (Gerbang 2), dan `laporan-poc-otomatis` (Gerbang 3, aturan keras 9) — skill ini **bukan** pengulangan kewajiban itu. Skill ini adalah **cara melaksanakannya tanpa merusak reproduktibilitas**: siklus hidup token/kredensial, pemisahan salinan mentah vs tersensor, pemetaan placeholder, minimisasi PII, dan format per platform — semua hal yang tidak diatur di ketiga skill itu.
- **LLM tidak boleh mengubah bukti** (bukti disimpan di luar memori LLM, hanya reference ID yang diberikan) sudah diatur di `skeptic-false-positive-eliminator` dan `laporan-poc-otomatis` — skill ini MEMAKAI aturan itu; penyimpanan bukti di sini mengikuti aturan yang sama.
- **Struktur laporan** (judul → ringkasan → langkah repro → bukti → dampak → saran perbaikan) ada di `laporan-poc-otomatis` — skill ini hanya menyiapkan BAHAN bukti + format platform untuk struktur itu.
- Alur sesudah skill ini: paket bukti bersih → `laporan-poc-otomatis` (rakit draf) → tinjau manusia 2–3 menit → persetujuan Cipta → kirim (oleh A69 yang melacak status, sesuai `laporan-abstrak`).

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan tangkap bukti, jangan buat laporan.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.**
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian aman dan read-only.
8. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.
9. **Sensor PII/token/kredensial di semua bukti ([REDACTED]) sebelum laporan disusun.** Bukti tanpa sensor = paket bukti belum selesai.
10. **Jangan pernah mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia dulu; pengiriman selalu manual + disetujui Cipta.
11. **Salinan mentah bukti TIDAK PERNAH keluar dari mesin kerja.** Hanya salinan tersensor yang masuk draf laporan, dasbor internal, atau dibagikan antar agent. Salinan mentah tidak di-commit ke repo, tidak dikirim lewat chat, tidak diunggah ke platform.
12. **Token/kredensial yang tertangkap dalam bukti WAJIB dirotasi/dicabut sesudah pengujian selesai** (lihat Gerbang 2) — token yang dipakai untuk bukti adalah token sekali pakai untuk pengujian, bukan token yang dibiarkan hidup.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Tangkap seminimal mungkin (minimisasi)

1. Sebelum menangkap, tanyakan: **apa bukti paling kecil yang membuktikan klaim ini?** Tangkap hanya itu. Jangan mengunduh respons lengkap bila satu field sudah cukup; jangan menyimpan seluruh riwayat sesi bila satu pasangan Request/Response sudah cukup.
2. Pakai **data canary palsu** untuk semua nilai sensitif yang bisa dipalsukan (nama, email, nomor identitas, isi pesan) — bukti yang berisi data palsu tidak perlu disensor seketat bukti berisi data nyata.
3. Jangan pernah menangkap: kata sandi pengguna lain, token sesi pengguna lain, isi lengkap layanan internal, atau data pengguna lain dalam jumlah besar. Bila respons server mengembalikan data orang lain melebihi yang dibutuhkan, **potong responsnya** ke bagian yang membuktikan klaim, dan sensor sisanya.
4. **Standar lulus:** tiap file bukti hanya berisi yang dibutuhkan untuk klaimnya + memakai data canary bila memungkinkan. Bukti yang berisi data berlebih = potong dulu sebelum lanjut.

### Gerbang 2 — Pisahkan mentah vs tersensor + kelola siklus hidup rahasia

1. Simpan **dua salinan** untuk tiap bukti:
   - **Mentah** — pasangan Request/Response asli, lengkap. Disimpan di file lokal di luar memori LLM, dengan reference ID (mis. `FP-2026-11-24-001`). TIDAK PERNAH dibagikan, di-commit, atau diunggah. LLM hanya menerima reference ID, bukan isinya.
   - **Tersensor** — salinan yang sama dengan semua rahasia diganti (lihat tabel sensor di bawah). Inilah yang dipakai antar agent, di dasbor internal, dan di draf laporan.
2. **Tabel sensor — ganti sebelum disimpan/dibagikan:**

   | Yang disensor | Diganti dengan |
   |---|---|
   | Token sesi / Bearer / JWT | `[REDACTED]` |
   | Kata sandi / secret / kunci API | `[REDACTED]` |
   | Email / nomor telepon / nama pribadi | `[REDACTED]` |
   | NIK / nomor identitas / nomor rekening / kartu | `[REDACTED]` |
   | Cookie sesi (nilai lengkap) | `[REDACTED]` |
   | Alamat canary pribadi (bila tidak boleh diketahui publik) | `[REDACTED]` |

3. **Redaksi yang menjaga reproduktibilitas** — sensor tidak boleh membuat langkah reproduksi mustahil diikuti:
   - Pakai **placeholder konsisten** di langkah reproduksi, bukan `[REDACTED]` mentah: `$TOKEN_A` (token akun penyerang), `$TOKEN_B` (token akun korban), `$SESSION_COOKIE`, dan tulis CARA mendapatkannya ("login sebagai akun tes A, salin token dari respons login").
   - Satu placeholder = satu nilai yang sama di seluruh laporan; jangan pakai `$TOKEN_A` untuk dua token berbeda.
   - Simpan **log redaksi** (file terpisah, tidak masuk laporan): reference ID bukti + daftar field yang disensor + placeholder yang dipakai. Log ini memungkinkan audit internal tanpa membuka salinan mentah.
4. **Siklus hidup token/kredensial:**
   - Token yang dipakai untuk bukti dibuat FRESH per sesi pengujian (jangan pakai ulang token lama).
   - Sesudah pengujian selesai, **cabut/rotasi** token dan kredensial yang tertangkap dalam bukti (logout, ganti kata sandi akun tes, cabut token API) — supaya bukti yang tersimpan tidak bisa dipakai untuk masuk kembali.
   - Kredensial akun tes TIDAK PERNAH ditulis di file bukti, log, atau skill — hanya di penyimpanan kredensial yang disetujui.
5. **Standar lulus:** tiap bukti punya salinan mentah (lokal, tak dibagikan) + salinan tersensor (yang dibagikan) + log redaksi; semua token pengujian sudah dicabut/dirotasi sesudah pengujian. Satu bukti tanpa pasangan tersensor = gerbang gagal.

### Gerbang 3 — Format sesuai standar platform

Sesuaikan paket bukti dengan format platform tempat laporan akan dikirim. Tabel di bawah adalah **titik awal default (BELUM DIUJI — wajib diverifikasi ke halaman pengiriman program yang bersangkutan sebelum merakit draf, karena format platform berubah)**:

| Platform | Klasifikasi keparahan | Yang wajib ada di paket bukti | Catatan format |
|---|---|---|---|
| **HackerOne** | CVSS v3.1 (kalkulator FIRST) + rating HackerOne | Judul dampak-jelas; langkah reproduksi bernomor; pasangan Request/Response tersensor; screenshot ber-caption; bagian Impact | Markdown didukung; kirim lewat form platform, bukan email; jangan kirim laporan otomatis |
| **Bugcrowd** | VRT (Vulnerability Rating Taxonomy) + CVSS | Klasifikasi VRT yang tepat; langkah reproduksi; bukti tersensor; prioritas P1–P5 mengikuti VRT | Isi field klasifikasi VRT dari taksonomi Bugcrowd yang berlaku — jangan menebak kategorinya |
| **Intigriti** | CVSS + CWE | Nomor CWE yang sesuai; langkah reproduksi; bukti tersensor | CWE yang salah = triase lambat; bila ragu antara dua CWE, tulis keduanya dengan alasan |
| **Immunefi** | Klasifikasi Immunefi (dampak langsung pada dana/aset) | Bukti dampak pada dana (jumlah yang TERBUKTI dari pengujian sendiri, berlabel TERBUKTI vs ESTIMASI); PoC langkah-demi-langkah | Fokus pada dampak dana langsung; program smart contract sering meminta PoC yang bisa dijalankan ulang di testnet/fork |

- Bila program memakai **0din**: berlaku alur abstrak-dulu (`laporan-abstrak`) — paket bukti di sini dipakai untuk tahap "detail lengkap/PoC" sesudah jawaban scope, bukan untuk abstrak.
- Bila program meminta format lain (form portal, field khusus), isi field itu dari paket bukti yang sama — jangan tulis laporan kedua yang isinya berbeda dari draf.
- **Standar lulus:** platform tujuan tertulis + klasifikasinya (CVSS/VRT/CWE/Immunefi) terisi dari bukti + semua bukti dalam paket sudah tersensor. Platform belum diverifikasi ke halaman resminya = gerbang gagal.

### Gerbang 4 — Audit paket bukti (A60) sebelum dirakit

1. A60 memeriksa paket bukti: (a) tiap klaim di draf punya bukti ber-reference-ID; (b) sensor lengkap — cari token, email, NIK, kata sandi di tiap file tersensor; (c) placeholder konsisten di seluruh laporan; (d) klasifikasi platform sesuai tabel Gerbang 3; (e) token pengujian sudah dicabut/dirotasi.
2. Satu cek gagal = paket DITOLAK, kembali ke gerbang yang relevan. A60 tidak meloloskan paket buktinya sendiri.
3. **Standar lulus:** paket lolos A60 + siap dirakit oleh A67 (`laporan-poc-otomatis`) + ditinjau manusia 2–3 menit sebelum diajukan ke Cipta.

## Validation Gate (verifikasi deterministik baseline vs exploit)

- Baseline: salinan tersensor HARUS tetap bisa dibaca triager untuk membedakan respons normal (baseline anonim) dari respons exploit — redaksi tidak boleh menghapus status HTTP, struktur respons, atau field yang membuktikan perbedaan itu. Bila redaksi menghapus bukti perbedaan baseline-vs-exploit, redaksi itu salah — buat ulang dengan placeholder, bukan penghapusan.
- Exploit: langkah reproduksi dari paket bukti HARUS bisa diulang orang ketiga dari nol memakai placeholder + cara mendapatkan token (Gerbang 2) — langkah yang butuh tebakan = paket belum selesai.
- Verdict paket SELESAI hanya sah bila A60 mengonfirmasi kedua cek di atas di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Penyimpanan bukti (file per temuan, reference ID mis. `FP-2026-11-24-001`) | Salinan mentah lokal + salinan tersensor; LLM hanya menerima reference ID |
| Sensor PII (ganti manual / skrip sensor) | Ganti token, kata sandi, email/nomor pribadi, dan data sensitif lain dengan `[REDACTED]` sebelum bukti disimpan/dibagikan |
| Log redaksi (file terpisah per temuan) | Daftar field yang disensor + placeholder yang dipakai — untuk audit internal, tidak masuk laporan |
| Kalkulator CVSS FIRST | `https://www.first.org/cvss/calculator/3.1` dan `/4.0` — skor untuk HackerOne/Intigriti (lihat `penilaian-cvss`) |
| Taksonomi VRT Bugcrowd / daftar CWE / klasifikasi Immunefi | Rujukan klasifikasi Gerbang 3 — baca dari sumber resmi platform yang berlaku saat itu |
| `~/workspace/catatan/log-bug-bounty.md` | Catat status paket bukti (ditangkap / tersensor / diaudit / siap dirakit) |

## Human-in-the-loop

- A60 mengaudit paket bukti sebelum dirakit menjadi draf. Manusia meninjau draf VERIFIED 2–3 menit sebelum submit — cek pasangan R/R, sensor PII, dan skor.
- **JANGAN PERNAH auto-submit** ke HackerOne/Bugcrowd atau platform lain. Tidak ada pengecualian.
- Setelah tinjauan manusia: kirim hanya bila **Cipta menyetujui** laporan itu.

## Format output

Catat setiap paket bukti di `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Paket bukti: <nama temuan singkat> | Program: <nama> | Platform tujuan: <HackerOne/Bugcrowd/Intigriti/Immunefi/lainnya>
  - Reference ID bukti: <FP-... — jumlah file: mentah X / tersensor X>
  - Gerbang 1 (minimisasi): LULUS/TOLAK — <data berlebih dipotong? data canary dipakai?>
  - Gerbang 2 (mentah vs tersensor + rotasi token): LULUS/TOLAK — <log redaksi ada? token dicabut?>
  - Gerbang 3 (format platform): LULUS/TOLAK — <klasifikasi: CVSS/VRT/CWE/Immunefi + tautan halaman program yang diverifikasi>
  - Gerbang 4 (audit A60): LULUS/TOLAK — <cek sensor + placeholder + klasifikasi>
  - Verdict akhir: <paket selesai / dikembalikan + alasan>
```

## Batasan yang diketahui

- Tabel format platform di Gerbang 3 adalah titik awal dari riset, BUKAN spesifikasi resmi platform — format dan taksonomi berubah; halaman pengiriman program yang bersangkutan selalu menang atas tabel ini.
- Skill ini mengatur bukti PoC web/API klasik. Untuk bukti bounty agen AI (transkrip agen, log tool-call), prinsip yang sama berlaku (sensor kredensial/PII, pisahkan mentah vs tersensor, jaga reproduktibilitas) tetapi format platformnya mengikuti program agen AI itu sendiri.
- Sensor `[REDACTED]` melindungi isi bukti, bukan metadata file (nama file, tanggal, ukuran) — jangan menulis nama file yang berisi token atau nama pengguna asli.
