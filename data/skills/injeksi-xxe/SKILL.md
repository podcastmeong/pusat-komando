# Skill: Injeksi XXE — XML External Entity pada Unggah File & Endpoint XML/SOAP

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 32).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target mem-parse XML dari input pengguna — endpoint SOAP/XML, impor XML, atau unggah file berbasis XML/ZIP: SVG, DOCX, XLSX, PPTX, dan file konfigurasi XML. Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji definisi entitas eksternal + callback OAST, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan permukaan XML (endpoint vs unggah file) |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian XXE per permukaan, bukan mengulang konsepnya).
- Penyiapan server canary OAST + bukti callback → skill `ssrf-oast` (skill ini memakai canary itu untuk XXE blind; jangan ulangi cara menyiapkan canary di sini).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Bypass filter unggah file (polyglot, MIME, double extension) → skill `bypass-unggah-file` (skill ini khusus isi XML-nya; bila file SVG/DOCX ditolak filter, bypass filter mengikuti skill itu).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.** Server canary (OAST) milik sendiri; satu ID unik per uji.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** DILARANG memakai Billion Laughs / entity expansion (amplifikasi entitas) — itu serangan kehabisan memori.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG membaca file sensitif server (`/etc/passwd`, `.env`, `win.ini`, konfigurasi, kredensial) via entitas eksternal, DILARANG menulis file ke server, DILARANG SSRF lanjutan ke layanan internal lewat entitas eksternal (kecuali callback canary sendiri). Pembuktian HARUS aman.
11. **Bukti aman yang diizinkan:** (a) callback DNS/HTTP ke canary OAST milik sendiri dari entitas eksternal; (b) error-based yang mengembalikan isi file CANARY MILIK SENDIRI yang ditempatkan atas izin program; (c) pemantulan kembali entitas internal yang TIDAK sensitif (mis. string canary yang didefinisikan sendiri di DTD). Itu saja.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian XXE diizinkan pada target dan permukaan ini (endpoint XML? unggah SVG/DOCX?)? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan permukaan XML

1. Cari permukaan: endpoint yang menerima `Content-Type: application/xml` / `text/xml` (termasuk SOAP), impor XML, dan unggah file berbasis XML/ZIP:
   - **SVG:** file XML murni — sisipkan DOCTYPE + entitas langsung di file.
   - **DOCX/XLSX/PPTX:** arsip ZIP berisi XML — sisipkan DOCTYPE + entitas di `word/document.xml` / `xl/worksheets/sheet1.xml`, lalu zip ulang.
   - **SOAP:** sisipkan DOCTYPE di envelope SOAP.
2. **Standar lulus:** daftar permukaan XML tertulis dengan format file/endpoint tiap permukaan. Permukaan yang tidak mem-parse XML (mis. file hanya disimpan tanpa diproses) = bukan XXE, jangan diuji lanjut.

### Gerbang 2 — Uji entitas internal (deteksi parser, tanpa akses luar)

1. Definisikan entitas internal yang TIDAK sensitif dan amati apakah dipantulkan, mis.:

   ```xml
   <?xml version="1.0"?>
   <!DOCTYPE uji [ <!ENTITY canary "CANARY-UNIK-123"> ]>
   <uji>&canary;</uji>
   ```

2. Bila respons menampilkan `CANARY-UNIK-123` → parser memproses DTD/entitas. Bila tidak → parser mungkin menolak DTD, lanjut ke Gerbang 3 (blind) sebelum menyimpulkan aman.
3. **Standar lulus:** hasil pemantulan entitas internal tercatat (ya/tidak + respons persis). Entitas internal yang dipantulkan = parser rentan terhadap DTD, bukti awal yang sah.

### Gerbang 3 — Uji entitas eksternal blind via callback canary (bukti utama)

1. Siapkan canary OAST milik sendiri (lihat `ssrf-oast`), satu ID unik per uji. Kirim definisi entitas eksternal yang mengarah ke canary:

   ```xml
   <?xml version="1.0"?>
   <!DOCTYPE uji [ <!ENTITY xxe SYSTEM "https://<id-unik>.canary-milik-sendiri/uji-xxe-1"> ]>
   <uji>&xxe;</uji>
   ```

2. Periksa log canary: apakah ada hit dari server target saat file/permintaan diproses? Untuk blind XXE, hit canary ADALAH buktinya — isi respons tidak perlu kembali.
3. Variasikan bila tidak ada hit: parameter entity (`%`) untuk out-of-band exfiltration KE CANARY SENDIRI SAJA, perubahan Content-Type, dan penempatan DOCTYPE di tiap permukaan (Gerbang 1) — satu variasi per putaran.
4. **Standar lulus (gerbang utama):** hit canary tercatat dengan ID unik yang cocok + waktu hit mengikuti waktu pengiriman. Tanpa hit = BELUM BERHASIL — catat kenapa gagal, variasikan, ulangi.

### Gerbang 4 — Error-based (HANYA dengan file canary sendiri, bila program mengizinkan)

1. Bila program mengizinkan penempatan file canary di server (mis. lewat fitur unggah yang sah): baca kembali file canary itu via entitas eksternal, mis. `<!ENTITY xxe SYSTEM "file:///jalur/canary-milik-sendiri.txt">`, dan amati apakah isinya kembali di respons/error.
2. DILARANG memakai gerbang ini untuk membaca file sistem (`/etc/passwd`, `.env`, `win.ini`) atau file aplikasi/config apa pun yang bukan canary sendiri.
3. **Standar lulus:** isi file canary sendiri kembali persis di respons/error. File selain canary sendiri = pelanggaran, hentikan uji.

### Gerbang 5 — Buktikan dampak, serahkan ke triase

1. Tulis dampak sesuai yang TERBUKTI: XXE terbukti via callback canary (blind) atau via pemantulan entitas. Jangan klaim "bisa membaca file server" bila hanya callback canary yang terbukti — tulis "parser memproses entitas eksternal; dampak baca file belum dibuktikan (dan tidak diuji, sesuai aturan aman)".
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (file/payload XML persis + log canary/respons persis) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Server canary OAST milik sendiri (lihat `ssrf-oast`) | Bukti callback untuk XXE blind; satu ID unik per uji |
| Editor XML + ZIP (zip/unzip) | Sisipkan DOCTYPE/entitas ke SVG (langsung) atau DOCX/XLSX (di XML dalam ZIP, lalu zip ulang) |
| Permintaan HTTP manual / Burp Repeater | Kirim XML ke endpoint SOAP/XML; hanya bila program mengizinkan alat itu |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload XML (nilai → hit canary/respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint / jenis file unggah]
Permukaan XML: [endpoint SOAP/XML / SVG / DOCX / XLSX]
Payload: [XML/DOCTYPE persis — atau jalur file uji]
Bukti: [hit canary: waktu + ID unik / pemantulan entitas internal / isi file canary sendiri]
Dampak terbukti: [XXE blind via callback / pemantulan entitas — sesuai bukti]
Yang TIDAK dilakukan: [tanpa baca file sensitif, tanpa Billion Laughs, tanpa SSRF ke internal]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Parser modern sering menonaktifkan DTD/entitas eksternal secara default — hasil negatif pada satu permukaan bukan berarti permukaan XML lain aman; uji tiap permukaan di Gerbang 1.
- DOCX/XLSX yang di-zip ulang harus tetap valid (struktur ZIP + `[Content_Types].xml` utuh) — file rusak yang ditolak server bukan bukti aman.
- Skill ini tidak membahas XXE pada parser non-XML (mis. YAML/JSON dengan fitur serupa) — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
