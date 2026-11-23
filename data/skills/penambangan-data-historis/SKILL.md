# Skill: Penambangan Data Historis — Wayback Machine / CommonCrawl: URL Lama, Parameter Usang, Endpoint yang Sudah Dihapus dari Navigasi tapi Masih Aktif

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 12 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu penambangan nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih dan perlu diketahui URL/endpoint lama target yang sudah tidak ada di navigasi sekarang — dari arsip Wayback Machine dan CommonCrawl — karena endpoint lama sering masih aktif dan luput dari pengujian. Masukan: domain in-scope. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menarik arsip (Wayback CDX + CommonCrawl), filter, dedup, penyerahan ke indeks |
| Pengerjaan | **A59 Threat Hunter** | Menilai parameter/endpoint usang mana yang menarik untuk fase parameter mining |
| Pemimpin | **Muse** | Putuskan endpoint historis mana yang diteruskan ke probing/pengujian |

## Sudah tercakup (jangan diduplikat)

- **Wayback sebagai alat** disebut satu baris di `mcp-osint` (Gerbang 2, tanpa langkah teknik) — skill ini adalah panduan langkah-demi-langkah penambangan arsip.
- **Payung recon** ada di `pemetaan-permukaan-serangan` — endpoint historis yang ditemukan diserahkan ke indeks aset skill itu.
- **Probing status hidup endpoint historis** ada di `probing-http-fingerprint` — skill ini berhenti di daftar URL historis; liveness check adalah langkah terpisah.
- **Parameter mining / fuzzing atas parameter usang** adalah Fase 3 butir 15 — skill ini hanya MENGINVENTARISASI parameter usang, bukan mengujinya.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Domain di luar scope = HENTIKAN, jangan ditambang arsipnya.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; query arsip secukupnya (CDX/CommonCrawl adalah layanan publik bersama — jangan membanjiri).
4. **Tanpa payload di permukaan publik.** Penambangan ini hanya MEMBACA arsip — tidak mengirim payload, tidak mengubah/menghapus data.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar URL historis bukan laporan.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program). Query ke arsip (Wayback/CommonCrawl) adalah pasif — TIDAK menyentuh server target; satu-satunya sentuhan aktif adalah liveness check di Gerbang 5, dan itu memakai `probing-http-fingerprint`.
10. **URL lama ≠ endpoint aktif.** Arsip membuktikan URL itu PERNAH ada, bukan masih aktif — jangan laporkan endpoint historis sebagai temuan sebelum liveness check membuktikan masih merespons.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope + domain (wajib, sebelum query arsip apa pun)

- Apa yang dilakukan: baca aturan program; catat domain in-scope yang akan ditambang arsipnya (apex + subdomain in-scope dari `enumerasi-subdomain`).
- Standar lulus: domain tertulis; arsip domain DI LUAR scope = DILARANG ditambang.

### Gerbang 1 — Wayback Machine via CDX API

- Apa yang dilakukan: tarik daftar URL dari CDX API Wayback (`http://web.archive.org/cdx/search/cdx?url=<domain>/*&output=json&fl=original,statuscode,mimetype,timestamp&collapse=urlkey&limit=<batas>` — cek dokumentasi CDX sebelum pakai pertama kali). Simpan mentah + tanggal tarikan. Batasi jumlah hasil bila arsip sangat besar (filter per tahun/subdomain dulu).
- Standar lulus: ada daftar mentah Wayback + jumlah entri + tanggal tarikan; tiap entri punya URL + statuscode arsip + timestamp.

### Gerbang 2 — CommonCrawl index

- Apa yang dilakukan: query CommonCrawl Index API untuk domain yang sama (`https://index.commoncrawl.org/CC-MAIN-<terbaru>-index?url=<domain>/*&output=json` — cek indeks terbaru yang tersedia sebelum pakai). Gabungkan dengan hasil Gerbang 1, dedup berdasarkan URL.
- Standar lulus: ada daftar mentah CommonCrawl + jumlah entri + nama indeks CC yang dipakai; duplikat terhadap Wayback dihapus; URL yang hanya dari satu arsip dicatat sumbernya.

### Gerbang 3 — Filter: URL lama, parameter usang, endpoint hilang dari navigasi

- Apa yang dilakukan: dari daftar gabungan, saring (a) URL dengan query string/parameter (`?` — kumpulkan nama parameter unik), (b) path API/admin/lama (`/api/`, `/admin`, `/v1/`, `/old/`, `/beta/`, file `.php/.asp/.jsp` lama, dsb.), (c) URL yang TIDAK muncul di indeks aktif saat ini (bandingkan dengan hasil `pemetaan-permukaan-serangan` / crawl aktif — yang tidak ada di navigasi sekarang = "hilang dari navigasi"). Buang aset statis murni (gambar/CSS/JS) dari daftar prioritas — simpan terpisah bila perlu.
- Standar lulus: tiap URL punya klasifikasi (parameter-usang / endpoint-lama / hilang-dari-navigasi); daftar parameter unik tercatat; aset statis terpisah dari daftar prioritas.

### Gerbang 4 — Dedup + bandingkan dengan indeks aktif

- Apa yang dilakukan: dedup akhir (normalisasi: buang fragment `#`, urutkan parameter query); bandingkan tiap URL dengan indeks aset aktif — tandai "sudah ada di indeks aktif" vs "hanya di arsip". Yang hanya di arsip adalah kandidat endpoint terlupakan.
- Standar lulus: tidak ada duplikat (setelah normalisasi); tiap URL punya status "di indeks aktif" / "hanya di arsip"; daftar parameter usang final tertulis.

### Gerbang 5 — Liveness check (via probing, bukan dari skill ini)

- Apa yang dilakukan: serahkan kandidat "hanya di arsip" ke `probing-http-fingerprint` (SATU request GET/HEAD per URL, rate ≤5 req/detik) untuk membuktikan masih merespons atau sudah mati. Skill ini TIDAK melakukan liveness check sendiri.
- Standar lulus: tiap kandidat punya hasil liveness (hidup + status / mati) dari probing; kandidat tanpa hasil liveness dicatat "belum dicek", bukan sebagai temuan.

### Gerbang 6 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis URL historis + parameter usang + hasil liveness ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Endpoint yang TERBUKTI masih hidup diteruskan sebagai kandidat pengujian; parameter usang diteruskan sebagai masukan Fase 3 butir 15 (parameter mining) — belum diuji di sini.
- Standar lulus: tiap entri punya sumber arsip (Wayback/CommonCrawl + timestamp), klasifikasi, dan status liveness; tidak ada endpoint "hanya di arsip, belum dicek" yang lolos sebagai kandidat uji.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Arsip URL Wayback | CDX API Wayback Machine (`web.archive.org/cdx/search/cdx`) |
| Arsip URL CommonCrawl | CommonCrawl Index API (`index.commoncrawl.org`) |
| Koleksi URL historis (bila tersedia) | `waybackurls` / `gau` (cek README sebelum pakai) — pembungkus CDX/CommonCrawl, bukan sumber baru |
| Liveness check endpoint historis | `probing-http-fingerprint` |
| Sumber daftar aktif (pembanding) | `pemetaan-permukaan-serangan`, `enumerasi-subdomain` |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |

## Format output

### Daftar URL historis

Simpan di `~/workspace/catatan/historis-<target>-<tanggal>.md`:

```
- URL: <alamat lengkap> | sumber: <Wayback <timestamp> / CommonCrawl <indeks>>
- Klasifikasi: <parameter-usang / endpoint-lama / hilang-dari-navigasi>
- Parameter: <daftar nama parameter, bila ada>
- Status indeks aktif: <sudah ada / hanya di arsip>
- Liveness: <hidup <status> / mati / belum dicek>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Penambangan data historis — <program/target>
- Wayback: <n> URL | CommonCrawl: <n> URL | gabungan setelah dedup: <n>
- Parameter unik: <n> | endpoint hilang-dari-navigasi: <n>
- Liveness: hidup <n> | mati <n> | belum dicek <n>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Wayback CDX API (https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md).
- CommonCrawl Index API (https://index.commoncrawl.org).
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila CDX API membatasi hasil, tarik per subdomain/per tahun secara terpisah dan gabungkan — catat pembagian tarikan di log.
- Bila CommonCrawl tidak punya data untuk domain kecil, hasil Wayback saja sudah cukup — catat "CommonCrawl: tidak ada data" dan lanjut, jangan memaksa.
