# Skill: Enumerasi Aset Cloud — Bucket Terbuka / Salah Konfigurasi AWS S3, GCS, Azure Blob

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 10 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu enumerasi nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih dan perlu diketahui apakah organisasi target punya aset cloud yang terekspos publik — bucket AWS S3, Google Cloud Storage (GCS), atau Azure Blob yang terbuka / salah konfigurasi. Masukan: nama organisasi/produk/domain target. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan enumerasi nama bucket + pengecekan akses read-only, penyerahan ke indeks |
| Pemimpin | **Muse** | Putuskan bucket mana yang dinyatakan temuan dan kapan diserahkan ke Cipta |

## Sudah tercakup (jangan diduplikat)

- **Modul cloud sebagai alat yang dipantau** ada di `alat-cain-agent` (status PANTAU — agen pentest AI + cloud, bukan panduan teknik enumerasi bucket) — skill ini adalah panduan teknik enumerasi aset cloud itu sendiri.
- **Korelasi subdomain → CNAME cloud** memakai `enumerasi-subdomain` dan `probing-http-fingerprint` (deteksi CDN/cloud dari header/CNAME) — skill ini memakai hasilnya, bukan mengulanginya.
- **Payung recon** ada di `pemetaan-permukaan-serangan` — bucket yang ditemukan diserahkan ke indeks aset skill itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Bucket di luar organisasi target / di luar scope = HENTIKAN, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; pengecekan bucket satu per satu, jangan membanjiri endpoint cloud.
4. **Tanpa payload di permukaan publik.** Enumerasi hanya request baca anonim (HEAD/GET status) — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive. **DILARANG menulis, mengunggah, atau menghapus objek apa pun di bucket orang lain.**
6. **DILARANG mengunduh / menyalin / membuka isi data orang lain.** Bila bucket terbuka dan berisi data milik orang lain (dokumen, database, backup, foto), BERHENTI — jangan unduh, jangan baca isinya, jangan simpan. Catat hanya: nama bucket + status akses (terbuka) + JENIS isi secara umum dari listing nama file saja bila listing itu sendiri yang membuktikan keterbukaan (tanpa membuka file). Laporkan segera ke Muse.
7. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar bucket bukan laporan.
8. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
9. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
10. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program). Menebak nama bucket dari nama organisasi adalah aktif — lakukan hanya untuk organisasi target in-scope.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope + nama dasar (wajib, sebelum pengecekan apa pun)

- Apa yang dilakukan: baca aturan program; catat nama organisasi/produk/domain target dan apakah aset cloud dinyatakan in-scope. Buat daftar nama dasar (nama perusahaan, produk, domain tanpa TLD, singkatan) — HANYA dari organisasi target.
- Standar lulus: nama dasar tertulis + status scope cloud tertulis; nama dari organisasi lain = DILARANG ditebak.

### Gerbang 1 — Kandidat bucket dari nama (permutasi)

- Apa yang dilakukan: hasilkan kandidat nama bucket dari nama dasar + pola umum (`<nama>`, `<nama>-assets`, `<nama>-backup`, `<nama>-prod`, `<nama>.com`, dsb.) dan dari CNAME subdomain yang mengarah ke cloud (silangkan `enumerasi-subdomain` — mis. `*.s3.amazonaws.com`, `*.blob.core.windows.net`, `*.storage.googleapis.com`). Catat sumber tiap kandidat.
- Standar lulus: daftar kandidat tertulis + sumber tiap entri; tidak ada kandidat dari nama organisasi lain.

### Gerbang 2 — Cek keterbukaan S3 (read-only)

- Apa yang dilakukan: cek tiap kandidat S3 dengan request anonim read-only (mis. `curl -s -o /dev/null -w "%{http_code}" https://<bucket>.s3.amazonaws.com/` atau alat sejenis seperti `cloud_enum` / `s3scanner` — cek README alat sebelum pakai pertama kali). Klasifikasi: tidak ada (404/NoSuchBucket), privat (403), terbuka-listing (200 + daftar objek), terbuka-baca objek. JANGAN unduh objek.
- Standar lulus: tiap kandidat punya status HTTP + klasifikasi; tidak ada objek yang diunduh; bucket "terbuka" dicatat dengan bukti status/listing-NAMA-file saja.

### Gerbang 3 — Cek keterbukaan GCS + Azure Blob (read-only)

- Apa yang dilakukan: ulangi Gerbang 2 untuk GCS (`https://storage.googleapis.com/<bucket>/`) dan Azure Blob (`https://<akun>.blob.core.windows.net/<container>/` — container ditebak dari nama dasar yang sama). Aturan yang sama: status saja, tanpa unduh.
- Standar lulus: tiap kandidat GCS/Azure punya status + klasifikasi; tidak ada objek yang diunduh; tidak ada akses dengan kredensial apa pun (hanya anonim).

### Gerbang 4 — Verifikasi manual + batasi dampak (human-in-the-loop)

- Apa yang dilakukan: A53 memeriksa tiap bucket "terbuka" secara manual (satu request konfirmasi status). Bila bucket berisi data orang lain: TERAPKAN Aturan keras 6 — berhenti, jangan baca isi, laporkan ke Muse SEGERA. Bila bucket hanya berisi aset publik milik target (gambar/JS/CSS situs) atau kosong: catat sebagai temuan kandidat dengan bukti status.
- Standar lulus: tiap bucket terbuka punya bukti status yang bisa diulang + putusan "berisi data orang lain — STOP" / "aset publik/kosong — kandidat temuan"; tidak ada isi file orang lain yang tersimpan di log mana pun.

### Gerbang 5 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis bucket yang ditemukan (nama, provider, status akses, klasifikasi isi umum) ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Temuan kandidat diserahkan ke Muse → Cipta; pengiriman ke program HANYA setelah Cipta setuju.
- Standar lulus: tiap entri punya provider, status akses, dan klasifikasi; tidak ada nama file sensitif / isi data orang lain di indeks atau log.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Pengecekan status bucket (anonim, read-only) | `curl` (HEAD/GET status) atau `cloud_enum` / `s3scanner` (cek README sebelum pakai) |
| Sumber kandidat dari CNAME/subdomain | `enumerasi-subdomain`, `probing-http-fingerprint` |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |
| Validasi temuan (anti false-positive) | `skeptic-false-positive-eliminator` |

## Format output

### Daftar aset cloud

Simpan di `~/workspace/catatan/cloud-<target>-<tanggal>.md`:

```
- Bucket: <nama> | provider: <S3/GCS/Azure Blob> | sumber kandidat: <permutasi/CNAME>
- Status akses: <tidak ada / privat-403 / terbuka-listing / terbuka-baca>
- Isi (umum saja): <aset publik / kosong / BERISI DATA ORANG LAIN — STOP, tidak dibaca>
- Bukti: <status HTTP + tanggal, tanpa isi file>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Enumerasi aset cloud — <program/target>
- Kandidat diuji: <n> (S3: <n>, GCS: <n>, Azure: <n>)
- Tidak ada: <n> | privat: <n> | terbuka: <n>
- Berisi data orang lain (STOP, dilaporkan): <n>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi cloud_enum (https://github.com/initstring/cloud_enum) dan s3scanner — flag dan pemakaian.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila alat enumerasi bucket tidak tersedia, pengecekan manual dengan `curl` per kandidat tetap sah untuk daftar kecil (<50 kandidat) — catat "cek manual" di log.
- Bila organisasi target memakai nama bucket yang tidak bisa ditebak, andalkan kandidat dari CNAME subdomain (Gerbang 1) — jangan memperluas tebakan ke nama-nama liar di luar organisasi target.
