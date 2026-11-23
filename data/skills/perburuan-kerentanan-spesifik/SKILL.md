# Skill: Perburuan Kerentanan Spesifik — Business Logic, Race Condition & OAuth/SSO

> Dibangun dari riset ketiga "Dua Perspektif Skill Bug Bounty AI" (23 Nov 2026, `~/workspace/catatan/referensi-dua-perspektif-skill-bug-bounty-ai-2026-11-23.md`, Perspektif 1 — Vulnerability-Specific Hunting Modules).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata per kategori yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis celah pada alur bisnis, kondisi balapan, atau login OAuth/SSO di program bounty resmi in-scope, dan hipotesis itu harus dibuktikan dampaknya sebelum maju ke triase. Dipakai sesudah fondasi (`fondasi-kerentanan-web-api`) dikuasai — skill ini hanya menambah 3 kategori yang belum tercakup di sana, bukan menggantikannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan 3 kategori ini pada tiap hipotesis dan pengujian |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar lulus kategori itu |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- IDOR, SSRF, XSS, Broken Auth, dan salah konfigurasi API → skill `fondasi-kerentanan-web-api` (jangan ulangi kelimanya di sini).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
11. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "kelihatan rentan" tanpa pembuktian dampak = tidak maju ke triase.
12. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.

## Langkah + gerbang

### Gerbang 1 — Kuasai 3 kategori ini

Pelajari dan hafalkan definisi, cara mengenali, dan cara membuktikan dampak tiap kategori di bawah. A58 wajib bisa menjelaskan ketiganya dengan contoh sebelum menguji.

#### 1. Business Logic Flaws (celah logika bisnis)

- **Definisi:** alur kerja yang bisa disalahgunakan dalam aturan main aplikasi — bukan karena input tidak divalidasi, melainkan karena logika bisnisnya sendiri tidak menegakkan aturan yang dimaksud. Contoh: manipulasi harga/jumlah (harga atau kuantitas diubah di permintaan dan diterima server), lompat langkah state machine (langkah wajib dilewati, mis. langsung ke "bayar" tanpa "konfirmasi" atau ke status selesai tanpa persetujuan), penyalahgunaan kupon/referral (kupon sekali pakai dipakai berulang, referral diklaim sendiri, diskon ditumpuk melebihi batas).
- **Cara mengenali:** petakan alur kerja sebagai state machine (langkah → langkah, siapa boleh pindah, apa syaratnya). Cari langkah yang diasumsikan klien (browser/aplikasi) yang menegakkannya padahal server tidak memeriksa ulang; cari angka yang menentukan nilai (harga, jumlah, diskon, saldo) yang dikirim dari klien dan dipercaya server; cari batasan "sekali pakai" atau "maksimal" yang hanya dicek di tampilan.
- **Cara membuktikan dampak:** buktikan dengan perubahan state nyata pada akun sendiri — mis. harga akhir yang dibayar benar-benar berubah, status pesanan benar-benar melompat ke langkah yang seharusnya tidak bisa dicapai, kupon benar-benar memberi diskon kedua kali / referral benar-benar tercatat. Simpan respons server + state sebelum/sesudah (saldo, status pesanan, riwayat kupon).
- **Standar lulus:** ada bukti perubahan state nyata pada akun sendiri (angka/status sebelum vs sesudah) + langkah reproduksi persis. Sekadar "parameter harga bisa diubah di permintaan" tanpa perubahan state yang diterima server = belum terbukti.

#### 2. Race Condition (kondisi balapan)

- **Definisi:** dua (atau lebih) permintaan bersamaan yang mengubah resource yang sama, dan server memprosesnya tanpa penguncian/pengecekan atomik sehingga hasilnya melanggar aturan. Contoh: double-spend (saldo yang sama dibelanjakan dua kali sebelum saldo diperbarui), kupon dipakai dua kali secara bersamaan, stok yang sama terjual melebihi jumlah yang ada.
- **Cara mengenali:** cari operasi yang membaca lalu menulis resource yang sama dalam dua langkah terpisah (cek saldo → kurangi saldo; cek kupon → tandai terpakai; cek stok → kurangi stok). Bila ada jeda antara "cek" dan "tulis", permintaan bersamaan bisa menyelinap di antaranya. Tanda lain: tidak ada kunci (lock), token sekali pakai, atau pengecekan ulang atomik di sisi server.
- **Cara membuktikan dampak:** buktikan dengan reproduksi deterministik — kirim permintaan bersamaan dengan konkurensi minimal (cukup 2 permintaan, tambah sedikit saja bila 2 belum cukup) dan tunjukkan resource yang sama benar-benar terpakai dua kali (mis. saldo terpotong sekali tapi dua pesanan berhasil, atau kupon yang sama memberi diskon dua kali). Ulangi dari state bersih untuk memastikan hasilnya bisa diulang, bukan kebetulan sekali jalan.
- **Standar lulus:** ada bukti reproduksi deterministik (hasil yang sama dari state bersih, minimal 2 kali percobaan berhasil) + bukti resource ganda terpakai (dua pesanan/diskon dari satu saldo/kupon). Sekali berhasil tanpa pengulangan = belum terbukti. **Batasan keras:** hanya akun sendiri, batasi jumlah permintaan, patuhi rate limit program — jangan kirim banjir permintaan (itu DoS, bukan pembuktian).

#### 3. OAuth/SSO Misconfiguration (salah konfigurasi OAuth/SSO)

- **Definisi:** celah pada alur login pihak ketiga — server tidak memvalidasi dengan benar bagian-bagian alur OAuth/OpenID Connect, sehingga penyerang bisa masuk sebagai orang lain atau membajak sesi. Contoh: validasi `redirect_uri` lemah (token/kode dikirim ke alamat penyerang), parameter `state` tidak diperiksa (serangan CSRF pada alur login), penanganan token salah (token tidak divalidasi tanda tangan/penerbit/kedaluwarsa, atau token akun lain diterima), kebingungan IdP (server tidak memeriksa IdP mana yang mengeluarkan token, sehingga token dari IdP lain / akun lain diterima).
- **Cara mengenali:** amati alur login lengkap (permintaan otorisasi → callback → penukaran kode → sesi). Periksa: apakah `redirect_uri` di callback harus sama persis dengan yang didaftarkan; apakah `state` yang kembali sama dengan yang dikirim dan terikat ke sesi; apakah token/kode divalidasi (penerbit, audiens, tanda tangan, kedaluwarsa); apakah ada lebih dari satu IdP dan apakah server membedakan token dari tiap IdP.
- **Cara membuktikan dampak:** buktikan dengan akun sendiri di kedua sisi (IdP + aplikasi) — mis. kode/token dari akun sendiri A dipakai untuk masuk sebagai akun sendiri B, atau callback dengan `redirect_uri`/`state` yang dimanipulasi benar-benar menghasilkan sesi login yang sah, atau token dari IdP lain benar-benar diterima aplikasi. Simpan permintaan callback + token + sesi yang terbentuk.
- **Standar lulus:** ada bukti sesi login yang terbentuk lewat alur yang dimanipulasi, dengan kedua akun (IdP + aplikasi) milik sendiri + langkah reproduksi persis. Sekadar "parameter `state` tidak ada" tanpa sesi yang terbentuk = belum terbukti.

### Gerbang 2 — Nilai hipotesis dengan kategori ini

1. Setiap hipotesis dinilai: kategorinya apa (salah satu dari 3 di atas, atau kategori fondasi — bila fondasi, pakai skill `fondasi-kerentanan-web-api`)? Cara pembuktian dampaknya apa (sesuai standar lulus kategori itu)?
2. **Standar lulus:** tiap hipotesis yang maju punya label kategori + rencana pembuktian dampak. Hipotesis tanpa label kategori dan tanpa rencana bukti = ditolak, jangan diuji.

### Gerbang 3 — Buktikan dampak, serahkan ke triase

1. Pengujian memakai `rekonstruksi-iterasi-payload` (variasi terarah, satu dimensi per putaran); bukti memakai standar lulus tiap kategori di Gerbang 1. Untuk Race Condition, tetap dalam batas konkurensi minimal + rate limit (lihat Gerbang 1.2).
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri | Wajib untuk membuktikan OAuth/SSO (akun IdP vs akun aplikasi, keduanya milik sendiri) dan Business Logic Flaws lintas akun bila relevan. |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian. |
| Skrip pengujian kecil (Python/bash) | Hanya untuk Race Condition: mengirim 2 permintaan bersamaan (konkurensi minimal). Hanya bila program mengizinkan otomasi; patuhi rate limit; berhenti otomatis bila respons menunjukkan kerusakan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + kategori + bukti dampak + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint/fitur]
Jenis kerentanan: [Business Logic Flaws / Race Condition / OAuth-SSO Misconfiguration]
Cara mengenali: [tanda yang ditemukan]
Pembuktian dampak: [langkah + bukti, sesuai standar lulus kategori itu]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini hanya mencakup 3 kategori dari riset Perspektif 1; tiap kategori punya varian yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Business Logic Flaws sangat bergantung pada aturan main tiap aplikasi — tidak ada daftar cek universal; pemetaan state machine per target wajib dibuat sebelum menguji.
- Race Condition yang hanya berhasil sekali tanpa reproduksi deterministik = belum terbukti; jangan laporkan sebagai temuan.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik di atas — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.
