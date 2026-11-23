# Skill: Serangan Kolisi Hash — Dua Input Berbeda, Hash Sama, Tanda Tangan Dipalsukan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk program bounty resmi berikut (9 program): Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar kesembilan program itu skill ini tidak boleh dipakai. Program yang relevan untuk skill ini: **HUNTR, Perplexity VDP (PPLX), Mistral VDP, Anthropic (ANTH)** — program lain hanya bila scope tertulisnya menyatakan pengujian kriptografi klasik berlaku. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.

## Pemicu

Dipakai saat target in-scope memakai fungsi hash yang sudah rusak atau lemah terhadap kolisi — terutama MD5 dan SHA-1 — untuk hal yang bergantung pada keunikan hash: verifikasi tanda tangan digital, validasi integritas file/dokumen, sertifikat, deduplikasi, atau pencocokan identitas berbasis hash. Dipakai sesudah `fondasi-kerentanan-web-api` dikuasai dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Tanda pemicu: target menyebut MD5/SHA-1 di dokumentasi atau responsnya, menerima file yang keasliannya hanya dicek lewat hash, atau membandingkan dua artefak semata-mata dari nilai hashnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan algoritma hash dan alur verifikasi target |
| Pengerjaan | **A62 Exploit Developer** | Menguji kolisi di lab pada artefak sendiri, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kerentanan kriptografi secara umum + standar pembuktian dampak → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian kolisi hash, bukan mengulang konsepnya).
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- Injeksi dan kerentanan web klasik lainnya → skill masing-masing (mis. `injeksi-sql-kontekstual`, `deteksi-csrf`) — bukan skill ini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** File/input uji adalah milik sendiri, dibuat di lab sendiri.
3. **Tanpa data orang lain.** Tanpa memalsukan tanda tangan, sertifikat, atau dokumen milik pihak lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pembuatan kolisi dilakukan di lab sendiri, bukan di server target.
6. **Tanpa payload di permukaan publik.** Artefak kolisi jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memalsukan tanda tangan digital atau sertifikat nyata untuk dipakai, DILARANG mengganti artefak asli dengan artefak kolisi di sistem apa pun, DILARANG mengunggah artefak kolisi ke target. Pembuktian kolisi HANYA pada artefak sendiri di lab sendiri, dan berhenti di situ.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian kriptografi/kolisi hash diizinkan pada target ini? Apakah otomasi/skrip dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu artefak uji pun dibuat. Tanpa itu = jangan mulai.

### Gerbang 1 — Kenali algoritma hash dan alur verifikasi

1. Tentukan algoritma hash yang dipakai target (MD5, SHA-1, atau yang lebih kuat) dari dokumentasi, respons, atau perilaku verifikasi.
2. Petakan alur yang bergantung pada hash itu: apa yang diverifikasi (tanda tangan, integritas file, identitas), siapa yang percaya pada hash, dan apa yang terjadi bila dua artefak berbeda lolos sebagai "sama".
3. **Standar lulus:** algoritma + alur verifikasi tertulis. Algoritma belum jelas = jangan menebak; cari bukti dulu (dokumentasi/respons). Bila target memakai SHA-256 atau lebih kuat tanpa kelemahan kolisi praktis yang diketahui, tutup sebagai AMAN dengan buktinya.

### Gerbang 2 — Buat pasangan kolisi di lab sendiri

1. Di lab sendiri, buat dua file/input SENDIRI yang berbeda isinya tetapi menghasilkan nilai hash yang sama menurut algoritma target, memakai perkakas riset kolisi yang sudah dikenal publik untuk algoritma itu.
2. Catat perbedaan isi kedua artefak (mis. satu artefak jinak, satu artefak berisi muatan canary yang jelas-jelas palsu dan tidak berbahaya) dan nilai hash keduanya yang identik.
3. **Standar lulus:** dua artefak sendiri yang berbeda isi tetapi hash-nya identik, dengan nilai hash tercatat persis. Tanpa pasangan kolisi yang terverifikasi di lab = belum terbukti, jangan maju.

### Gerbang 3 — Uji apakah verifikasi target tertipu oleh kolisi (hanya in-scope, hanya artefak sendiri)

1. Periksa logika verifikasi target terhadap pasangan kolisi dari Gerbang 2: apakah target memperlakukan kedua artefak sebagai identik (mis. menerima artefak kedua sebagai pengganti artefak pertama yang sudah ditandatangani/diverifikasi)?
2. Uji HANYA dengan artefak sendiri dan akun uji sendiri, di endpoint in-scope. Jangan pernah mengunggah artefak kolisi ke sistem produksi atau menggantikan artefak orang lain.
3. **Standar lulus:** ada bukti bahwa target menerima artefak kedua sebagai artefak pertama (atau sebaliknya) berdasarkan hash saja. Bila target memeriksa isi selain hash (mis. memeriksa struktur/isi dokumen) dan menolak artefak kedua = AMAN, tutup dengan buktinya.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis dampak konkret: artefak apa yang bisa diganti tanpa terdeteksi, dan apa konsekuensinya (mis. dokumen yang sudah ditandatangani bisa ditukar isinya). Jangan membesar-besarkan — tulis sesuai bukti Gerbang 3.
2. Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.
3. **Standar lulus:** dampak ditulis konkret (artefak + alur yang tertipu), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Perkakas riset kolisi hash publik (untuk MD5/SHA-1) | Membuat pasangan kolisi dari file sendiri di lab sendiri; hanya bila program mengizinkan |
| Utilitas hash (cek nilai hash file) | Memverifikasi kedua artefak menghasilkan hash identik |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua artefak uji (hash → hasil verifikasi → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alur verifikasi + algoritma hash]
Algoritma hash: [MD5 / SHA-1 / lainnya — bukti identifikasi]
Artefak kolisi (lab sendiri): [deskripsi dua artefak sendiri + nilai hash identik]
Hasil uji verifikasi: [target menerima artefak kedua sebagai artefak pertama — atau "DITOLAK"]
Yang TIDAK dilakukan: [tanpa pemalsuan tanda tangan/sertifikat nyata, tanpa unggah artefak kolisi ke target]
Dampak: [artefak apa yang bisa ditukar tanpa terdeteksi + konsekuensinya]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Kolisi praktis hanya diketahui untuk algoritma yang sudah rusak (MD5, SHA-1); SHA-256 dan yang lebih kuat tidak punya serangan kolisi praktis — jangan klaim kolisi di sana tanpa bukti.
- Banyak sistem memeriksa lebih dari hash (isi, struktur, metadata) sehingga kolisi hash saja belum tentu cukup — vonis datang dari Gerbang 3, bukan dari Gerbang 2.
- Pembuatan kolisi bisa berat secara komputasi; lakukan di lab sendiri dan jangan membebani server target.
