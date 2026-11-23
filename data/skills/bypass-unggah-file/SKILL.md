# Skill: Bypass Unggah File — Polyglot, MIME, Double Extension & Traversal Nama File

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 35).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target punya fitur unggah file (avatar, dokumen, lampiran, impor) dengan filter jenis file — dan diduga filter itu bisa dilewati sehingga file dengan jenis yang dilarang diterima/disimpan/ditayangkan server. Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji bypass filter unggah, mendokumentasikan bukti penyimpanan/penayangan |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan filter yang dipakai target |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi/unggah file secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH bypass filter, bukan mengulang konsepnya).
- Isi XML pada file SVG/DOCX/XLSX (XXE) → skill `injeksi-xxe` (skill ini khusus FILTER unggahnya; bila file SVG lolos filter, isi XML-nya mengikuti skill itu).
- Traversal pada parameter PEMBACAAN file → skill `traversal-jalur-lfi` (skill ini khusus traversal pada NAMA FILE saat unggah).
- Eksekusi perintah bila file yang diunggah dieksekusi server → skill `injeksi-perintah-rce` (pembuktian perintah mengikuti allowlist skill itu).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan mengunggah file raksasa atau banyak file sekaligus untuk membanjiri penyimpanan server.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengunggah webshell yang berfungsi, skrip yang mengeksekusi perintah, atau file apa pun yang mengeksekusi kode di server. DILARANG menimpa/menghapus file yang sudah ada di server. DILARANG mengunggah file yang menyerang pengguna lain (mis. SVG berisi skrip yang jalan di browser korban).
11. **File bukti HARUS inert (tidak mengeksekusi apa pun).** File uji hanya berisi teks canary, mis. `CANARY-UNIK-123` — tanpa kode yang dieksekusi, tanpa skrip, tanpa perintah. Bukti bypass = file dengan ekstensi/jenis yang dilarang DITERIMA + DISIMPAN/DITAYANGKAN server, bukan dieksekusi.
12. **Jangan memicu eksekusi.** Bila file yang diunggah ternyata dieksekusi server (mis. file `.php` yang diunggah lalu bisa diakses sebagai halaman), JANGAN membukanya untuk mengeksekusi — cukup catat URL penyimpanan + respons header sebagai bukti penyimpanan, lalu hentikan uji dan laporkan ke Muse. Pembuktian eksekusi (bila scope mengizinkan) hanya mengikuti skill `injeksi-perintah-rce` dengan allowlist perintahnya.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian bypass unggah file diizinkan pada target ini? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu file pun diunggah. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan filter unggah

1. Tentukan apa yang diperiksa server: ekstensi nama file, `Content-Type`/MIME, isi/magic bytes, ukuran, atau kombinasi. Uji dengan file yang sah (mis. `.png` asli) sebagai baseline, lalu file yang jelas dilarang (mis. `.php` berisi teks canary) untuk melihat pesan penolakan.
2. **Standar lulus:** jenis filter tertulis (ekstensi / MIME / magic bytes / kombinasi) + pesan penolakan persis tercatat. Filter belum jelas = uji satu dimensi per putaran (Gerbang 2–4) dan catat mana yang mengubah hasil.

### Gerbang 2 — Bypass berbasis ekstensi

1. Uji SATU variasi per putaran, selalu dengan file inert berisi teks canary:
   - **Double extension:** `canary.php.png`, `canary.png.php`, `canary.php;.png`
   - **Variasi huruf:** `canary.PHP`, `canary.PhP`, `canary.pHp`
   - **Ekstensi ganda/aneh:** `canary.php5`, `canary.phtml`, `canary.php.`, `canary.php%00.png` (null byte — hanya pada target lama yang masih rentan; catat bila diblokir)
   - **Tanpa ekstensi / ekstensi kosong:** `canary`, `canary.`
2. **Standar lulus:** file dengan ekstensi yang semestinya dilarang DITERIMA server (respons sukses + URL/path penyimpanan dikembalikan). File ditolak = variasi itu gagal, catat dan lanjut.

### Gerbang 3 — Bypass berbasis MIME-type & magic bytes

1. Uji manipulasi `Content-Type`: kirim file `.php` (isi teks canary) dengan header `Content-Type: image/png` — bila diterima, filter hanya memeriksa MIME.
2. Uji polyglot sederhana yang INERT: file yang diawali magic bytes gambar yang sah (mis. header PNG) diikuti teks canary — tanpa kode yang dieksekusi. Bila server memeriksa magic bytes saja, file ini lolos sebagai "gambar" walau ekstensinya dilarang.
3. **Standar lulus:** file diterima saat MIME/magic bytes dimanipulasi, padahal ekstensi/isinya semestinya dilarang — dengan bukti respons sukses + URL penyimpanan. File tetap ditolak = filter memeriksa isi dengan benar pada dimensi itu.

### Gerbang 4 — Traversal pada nama file (penulisan di luar direktori unggah)

1. Uji nama file berisi traversal, mis. `../../canary-uji.txt` atau `..%2f..%2fcanary-uji.txt`, dengan isi teks canary. Periksa apakah file tersimpan di luar direktori unggah yang dimaksud (respons menyebutkan path, atau file bisa diakses dari jalur di luar direktori unggah).
2. DILARANG memakai traversal nama file untuk menimpa file yang sudah ada (mis. menargetkan nama file aplikasi/config yang ada) — target penulisan HANYA nama file canary baru yang tidak menimpa apa pun.
3. **Standar lulus:** file canary tersimpan di jalur di luar direktori unggah yang dimaksud, tanpa menimpa file apa pun. File tersimpan di tempat yang benar = tidak ada traversal, catat dan lanjut.

### Gerbang 5 — Periksa apa yang terjadi pada file yang lolos

1. Periksa bagaimana server memperlakukan file yang lolos: apakah ditayangkan kembali (URL bisa diakses), apakah `Content-Type` respons mengikuti file, apakah file dijalankan sebagai skrip (JANGAN memicu eksekusi — lihat aturan 12), dan apakah file tampil ke pengguna lain (bila ya, itu temuan tersendiri: stored XSS via SVG — laporkan polanya, tapi JANGAN mengunggah SVG berisi skrip; buktinya cukup file SVG inert yang ditayangkan dengan `Content-Type: image/svg+xml`).
2. **Standar lulus:** perlakuan server terhadap file yang lolos tertulis (disimpan saja / ditayangkan / dijalankan — tanpa eksekusi yang dipicu). Perlakuan tidak diperiksa = bukti belum lengkap.

### Gerbang 6 — Buktikan dampak, serahkan ke triase

1. Tulis dampak sesuai yang TERBUKTI: filter mana yang dilewati + apa yang terjadi pada file (disimpan/ditayangkan). Jangan klaim "bisa RCE via unggah" bila hanya penyimpanan yang terbukti — tulis "bypass filter terbukti (file dilarang diterima + disimpan); eksekusi tidak diuji, sesuai aturan aman".
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (file uji persis + respons/URL penyimpanan persis) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU file uji per putaran dengan nama/MIME yang divariasikan; hanya bila program mengizinkan alat itu |
| File uji inert (teks canary) | Satu file per variasi; isi hanya `CANARY-UNIK-123`, tanpa kode yang dieksekusi |
| Pemeriksa magic bytes (`file`, `xxd`) | Memastikan header file uji sesuai yang dimaksud sebelum diunggah |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua file uji (nama/MIME/isi → respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint unggah]
Filter yang dipakai target: [ekstensi / MIME / magic bytes / kombinasi]
Teknik bypass terbukti: [double extension / variasi huruf / MIME / polyglot inert / traversal nama file]
File uji: [nama file + Content-Type + isi canary persis]
Bukti: [respons sukses + URL/path penyimpanan + perlakuan server]
Dampak terbukti: [file dilarang diterima + disimpan/ditayangkan]
Yang TIDAK dilakukan: [tanpa webshell, tanpa eksekusi, tanpa menimpa file, tanpa skrip di SVG]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Filter yang memeriksa isi file secara mendalam (mis. mem-parse ulang gambar) akan menolak polyglot — hasil negatif pada satu teknik bukan berarti semua teknik gagal; uji tiap gerbang.
- File yang diterima tapi disimpan dengan nama acak/ekstensi dipaksa aman (mis. selalu `.png`) belum tentu temuan — yang dihitung adalah file dilarang yang TETAP bisa disimpan/ditayangkan sebagai jenis yang dilarang.
- Skill ini tidak membahas bypass filter pada unggah file yang langsung dieksekusi sebagai template/kode oleh server — itu mengikuti skill `injeksi-template-ssti` / `injeksi-perintah-rce` bila scope mengizinkan.
