# Skill: Traversal Jalur & LFI — Baca File Server via Manipulasi Jalur Direktori

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 34).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada parameter yang menentukan file/jalur yang dibaca server — `file=`, `page=`, `template=`, `lang=`, `include=`, unduh file, atau pratinjau dokumen — dan nilai parameter itu diduga diteruskan ke filesystem tanpa validasi. Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji traversal jalur + wrapper, mendokumentasikan bukti canary |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan permukaan file |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi/akses file secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian traversal + wrapper, bukan mengulang konsepnya).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Traversal pada NAMA FILE saat unggah → skill `bypass-unggah-file` (skill ini khusus parameter PEMBACAAN file; traversal saat unggah mengikuti skill itu).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

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
10. **LARANGAN DESTRUKTIF + LARANGAN BACA FILE SENSITIF — MUTLAK.** DILARANG menghapus/mengubah/menulis file apa pun via traversal. DILARANG membaca file sensitif di luar akun uji sendiri: `/etc/passwd`, `win.ini`, `.env`, file konfigurasi, kredensial, kunci privat, database, dan file milik pengguna lain. Menyebut nama file-file itu sebagai "target klasik penyerang" di laporan TIDAK berarti boleh membacanya — jangan pernah mengirim permintaan untuk membacanya.
11. **Bukti yang diizinkan:** HANYA file canary yang ditempatkan sendiri (mis. file yang diunggah lewat fitur sah, lalu dibaca kembali via traversal) bila program mengizinkan — atau perbedaan perilaku/error yang membuktikan traversal tanpa membaca isi file apa pun. Itu saja.
12. **DILARANG log poisoning dan RFI.** Menulis ke file log server lalu memicu log itu (log poisoning) adalah penulisan ke server = DILARANG. Remote File Inclusion (memasukkan file dari URL luar) DILARANG kecuali scope program secara eksplisit mengizinkannya — dan bila diizinkan, file remote itu hanya file canary milik sendiri yang tidak mengeksekusi apa pun.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian traversal/LFI diizinkan pada target ini? Apakah penempatan file canary diizinkan (untuk bukti Gerbang 3)? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + izin penempatan canary + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan permukaan pembacaan file

1. Cari permukaan: parameter file/halaman/template/bahasa, fitur unduh/pratinjau, dan endpoint yang mengembalikan isi file. Untuk tiap permukaan catat: nilai normalnya, dan apakah respons berisi isi file atau hanya error.
2. **Standar lulus:** daftar permukaan tertulis dengan nilai normal + jenis respons tiap permukaan. Permukaan yang tidak membaca file dari disk = bukan LFI, jangan diuji lanjut.

### Gerbang 2 — Uji traversal dasar (tanpa membaca isi file sensitif)

1. Uji apakah server mengikuti `../` keluar dari direktori yang dimaksud — dengan target yang TIDAK sensitif dan TIDAK berisi data orang lain. Cara aman: arahkan traversal ke file canary yang SUDAH ditempatkan sendiri (lihat Gerbang 3), atau amati perbedaan perilaku: respons berubah antara `file=normal` vs `file=../normal` vs `file=../../normal` (error berbeda / status berbeda / isi berbeda pada file yang sama).
2. Variasikan encoding SATU per satu: `../`, `..%2f`, `..%5c`, `....//`, `..;/`, dan (bila perlu) absolute path ke file canary sendiri.
3. **Standar lulus:** perbedaan perilaku yang konsisten mengikuti jumlah `../` (mis. file yang sama terbaca dari kedalaman berbeda, atau error berubah pola mengikuti traversal). Perbedaan satu kali yang tidak terulang = belum terbukti.

### Gerbang 3 — Bukti dengan file canary sendiri (bukti utama, bila program mengizinkan)

1. Tempatkan file canary lewat fitur yang sah (mis. unggah avatar/dokumen sebagai akun sendiri) dengan isi unik, mis. `CANARY-UNIK-123` di `canary-uji.txt`. Catat jalur penyimpanannya bila terlihat.
2. Baca kembali file canary itu via traversal dari parameter uji, mis. `file=../../../../jalur/unggahan/canary-uji.txt` (sesuaikan kedalaman dari Gerbang 2).
3. **Standar lulus:** isi `CANARY-UNIK-123` kembali persis di respons. Itu membuktikan traversal + pembacaan file di luar direktori yang dimaksud — TANPA membaca satu pun file sensitif. Bila program TIDAK mengizinkan penempatan canary, bukti berhenti di Gerbang 2 (perbedaan perilaku) + Gerbang 4 (wrapper, bila ada).

### Gerbang 4 — Wrapper PHP (HANYA bila target PHP, dan hanya pada file canary sendiri)

1. Bila target memakai PHP, uji wrapper pada file canary sendiri: `php://filter/convert.base64-encode/resource=<jalur-canary-sendiri>` — respons base64 yang di-decode berisi `CANARY-UNIK-123` = bukti.
2. DILARANG memakai wrapper pada file apa pun selain canary sendiri. DILARANG `php://input`, `data://`, dan `expect://` — semuanya mengeksekusi input = di luar skill ini (ikuti `injeksi-perintah-rce` bila scope mengizinkan, dengan allowlist perintahnya).
3. **Standar lulus:** isi canary sendiri kembali (langsung atau base64) via wrapper. Wrapper pada file lain = pelanggaran, hentikan uji.

### Gerbang 5 — Buktikan dampak, serahkan ke triase

1. Tulis dampak sesuai yang TERBUKTI: traversal terbukti karena file canary sendiri terbaca dari luar direktori yang dimaksud. Jangan klaim "bisa membaca /etc/passwd / .env" bila hanya canary yang terbukti — tulis "pembacaan file di luar direktori terbukti pada file canary sendiri; pembacaan file sensitif tidak diuji, sesuai aturan aman".
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (payload traversal persis + isi canary yang kembali persis) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU payload traversal per uji, amati respons; hanya bila program mengizinkan alat itu |
| Fitur unggah yang sah (akun sendiri) | Menempatkan file canary untuk bukti Gerbang 3; hanya bila program mengizinkan |
| Decoder base64 | Memeriksa hasil `php://filter` pada file canary sendiri |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload traversal (nilai → respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter file]
Permukaan: [parameter file/halaman/template/bahasa — nilai normal]
Payload traversal: [payload persis + encoding yang dipakai]
Bukti: [isi canary sendiri kembali persis / perbedaan perilaku mengikuti jumlah ../]
Wrapper: [php://filter pada canary sendiri — bila dipakai]
Dampak terbukti: [file canary sendiri terbaca dari luar direktori yang dimaksud]
Yang TIDAK dilakukan: [tanpa baca /etc/passwd, .env, win.ini, config; tanpa log poisoning; tanpa RFI]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Filter traversal (blokir `../` mentah) sering bisa dilewati encoding — tapi setiap variasi tetap memakai target canary sendiri, bukan file sensitif.
- LFI pada aplikasi yang hanya mengembalikan error tanpa isi file tetap bisa dibuktikan via Gerbang 2 (perbedaan perilaku) — catat sebagai "traversal terindikasi, pembacaan isi belum terbukti" bila canary tidak bisa ditempatkan.
- Skill ini tidak membahas traversal pada penulisan file (path traversal saat menyimpan/unggah) — itu mengikuti skill `bypass-unggah-file`.
