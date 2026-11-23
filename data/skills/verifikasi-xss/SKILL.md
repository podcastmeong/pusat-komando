# Skill: Verifikasi XSS — Pastikan Payload Benar-Benar Mengeksekusi JS di Headless Browser

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 37 (Reflected & Stored XSS Verification). Jangan klaim metode ini terbukti sampai ada satu payload yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat ada hipotesis XSS (dari `fondasi-kerentanan-web-api`, `pelacakan-taint-xss-dom`, atau temuan pemetaan) dan payload harus DIBUKTIKAN mengeksekusi JavaScript — bukan sekadar terpantul di HTML respons. Dipakai untuk tiga varian: reflected (parameter terpantul di respons), stored (payload tersimpan lalu dieksekusi saat dilihat akun lain), dan DOM (aliran sudah dipetakan `pelacakan-taint-xss-dom`).

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memilih konteks + payload canary, menjalankan uji |
| Pengerjaan | **A54 Penguji Live** | Menjalankan verifikasi di headless browser / browser task (`uji-live-browser`) |
| Audit | **A60 Security Auditor** | Mengaudit bukti eksekusi + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Definisi + standar bukti XSS secara umum** (eksekusi di akun/sesi kedua milik sendiri) → `fondasi-kerentanan-web-api` (bagian XSS). Skill ini menambah PROSEDUR verifikasinya: konteks injeksi, payload per konteks, dan pembuktian di headless browser.
- **Aliran DOM source→sink** → `pelacakan-taint-xss-dom`. Skill ini membuktikan eksekusinya, bukan menemukan alirannya.
- **Vektor output AI yang dirender** (payload lahir dari jawaban model) → `output-tidak-aman`. Skill ini untuk XSS KLASIK di aplikasi web (input langsung ditampilkan), bukan output AI.
- **Katalog teknik bukti aman lintas jenis celah** (satu baris XSS: cetak `document.domain`) → `verifikasi-poc-aman` (Fase 7 butir 45). Skill itu memberi TEKNIK bukti generik; skill ini memberi PROSEDUR verifikasi khusus XSS (konteks injeksi, alur reflected vs stored, variasi WAF) — keduanya dipakai bersama, bukan duplikat.
- **Variasi payload sistematis saat WAF memblokir** → `rekonstruksi-iterasi-payload`. Skill ini memakai variasinya, bukan menulis ulang metodenya.
- **Gerbang false-positive akhir sebelum laporan** → `skeptic-false-positive-eliminator`. Setiap klaim BERHASIL di sini wajib lewat gerbang itu sebelum jadi draf laporan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan.
5. **Tanpa payload di permukaan publik.** Payload dan halaman pemicu jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap klaim eksekusi harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only: bukti eksekusi cukup mencetak `document.domain` / alert canary di browser/sesi sendiri — JANGAN mencuri cookie/sesi orang lain, JANGAN menjalankan aksi atas nama akun lain.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik XSS klasik.
11. **Self-XSS umumnya TIDAK dibayar.** Payload yang hanya mengeksekusi di akun/sesi yang memasukkannya sendiri BUKAN temuan yang layak lapor. Bukti yang dihitung: payload yang dimasukkan di akun/sesi pertama **dieksekusi saat dilihat akun/sesi kedua milik sendiri** (akun korban = akun sendiri yang kedua, data canary palsu).

## Langkah + gerbang

### Langkah 1 — Tentukan varian dan konteks injeksi

Tentukan dulu variannya: reflected (input terpantul di respons yang sama), stored (input tersimpan di server lalu dirender di halaman lain), atau DOM (aliran dari `pelacakan-taint-xss-dom`). Lalu petakan KONTEKS tempat input muncul di halaman: isi elemen HTML, nilai atribut, string di dalam `<script>`, URL, atau komentar. Konteks menentukan payload — payload yang benar di satu konteks gagal total di konteks lain.

**Standar lulus:** varian + konteks tertulis (mis. "stored, konteks nilai atribut `value=\"...\"`"); payload yang dipilih merujuk ke konteks itu. Tanpa konteks = jangan uji.

### Langkah 2 — Pilih payload canary minimal per konteks

Pakai payload canary yang HANYA membuktikan eksekusi, tanpa efek samping: mis. payload yang memanggil server canary milik sendiri dengan ID unik, atau mencetak `document.domain`. Contoh per konteks (sesuaikan dengan konteks Langkah 1):

- Konteks isi HTML: tag yang mengeksekusi saat dirender (mis. `<img src=x onerror=...>`).
- Konteks atribut: keluar dari atribut dulu (tutup kutip), lalu sisipkan event handler.
- Konteks string JS: keluar dari string dulu, lalu sisipkan pernyataan.

**Standar lulus:** payload tercatat persis + ID canary unik per uji (satu ID tidak dipakai dua uji); payload tidak mengandung aksi destruktif, tidak membaca/mengirim cookie atau data sesi ke mana pun kecuali canary milik sendiri.

### Langkah 3 — Uji di headless browser (bukan sekadar baca HTML)

Jalankan payload di headless browser / browser task milik sendiri (`uji-live-browser`). **Pantulan di HTML respons BUKAN bukti** — payload yang tampil sebagai teks, ter-encode (`&lt;`), atau diblokir WAF adalah GAGAL. Bukti hanya salah satu dari: (a) hit canary tercatat dari eksekusi skrip, atau (b) efek eksekusi teramati dan terdokumentasi di browser (mis. `document.domain` tercetak).

- **Reflected:** kirim payload lewat parameter, muat URL hasil di headless browser, periksa eksekusi.
- **Stored:** simpan payload dari akun pertama milik sendiri, lalu buka halaman penampil dari akun kedua milik sendiri, periksa eksekusi.
- **DOM:** muat halaman dengan source yang berisi payload (mis. fragment `#`), periksa eksekusi tanpa round-trip server.

**Standar lulus (gerbang utama): tanpa bukti eksekusi = BELUM BERHASIL.** Refleksi tanpa eksekusi, canary yang tidak pernah dipanggil, atau eksekusi hanya di akun yang memasukkan payload (self-XSS) = GAGAL — catat kenapa gagal, lalu variasikan dan ulangi dari Langkah 2.

### Langkah 4 — Variasikan bila diblokir

Bila payload diblokir WAF/filter (ter-encode, terpotong, ditolak), variasikan secara sistematis memakai `rekonstruksi-iterasi-payload` (encoding, fragmentasi, konteks lain). Catat tiap variasi + hasilnya; jangan mengulang payload yang sama persis berkali-kali.

**Standar lulus:** tiap variasi tercatat (payload + hasil); maksimal variasi wajar per target — bila semua konteks gagal, tutup sebagai GAGAL dan serahkan ke Muse, jangan menghantam target tanpa henti.

### Langkah 5 — Gerbang false-positive + tulis draf

Serahkan klaim BERHASIL ke `skeptic-false-positive-eliminator` (cek sesi bersih, deterministik, bukan kebetulan). Yang lolos ditulis sebagai draf laporan ke A60, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (apa yang didapat penyerang bila korbannya sungguhan — mis. aksi atas nama korban, pencurian sesi), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Headless browser / browser task (`uji-live-browser`) | Tempat payload dijalankan dan eksekusi diamati; JANGAN nilai dari HTML mentah saja |
| Server canary milik sendiri | Endpoint HTTP(S) yang mencatat setiap hit (waktu, IP, path/ID unik); satu ID unik per uji |
| Dua akun/sesi uji sendiri | Wajib untuk stored XSS: akun penyimpan + akun penampil; keduanya milik sendiri, data canary palsu |
| `rekonstruksi-iterasi-payload` | Variasi payload saat WAF/filter memblokir |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua uji + bukti + keputusan triase |

## Format output

Log setiap uji ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Varian: [reflected / stored / DOM]
Konteks injeksi: [isi HTML / atribut / string JS / ...]
Payload: [payload persis + ID canary unik]
Bukti eksekusi: [log canary tercatat / document.domain tercetak — atau "TIDAK ADA"]
Akun penampil: [akun kedua milik sendiri — atau "hanya akun sendiri (self-XSS)"]
Dampak: [apa yang didapat penyerang bila korban sungguhan]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Refleksi ≠ eksekusi: sebagian besar kandidat XSS gagal di gerbang ini karena encoding konteks — itu normal, catat dan lanjut.
- Stored XSS butuh halaman penampil yang benar-benar dirender akun kedua; bila akun kedua tidak bisa melihat konten itu (hak akses berbeda), buktinya belum lengkap — catat batasnya, jangan diklaim berhasil.

### Available connectors

Tidak ada konektor khusus untuk skill ini; headless browser dipakai lewat `uji-live-browser`.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi target (alur fitur tempat payload disimpan/ditampilkan).

### Alternatives for better results

- Bila headless browser tidak bisa dipakai, uji di browser task biasa milik sendiri dengan akun yang sama — yang penting eksekusi diamati di browser sungguhan, bukan dari HTML mentah.
- Bila WAF memblokir semua variasi di satu konteks, pindah konteks (mis. dari isi HTML ke atribut) sebelum menambah variasi di konteks yang sama.
