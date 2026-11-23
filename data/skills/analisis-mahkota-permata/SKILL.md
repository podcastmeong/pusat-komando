# Skill: Analisis Mahkota Permata — Merumuskan Aset Paling Berharga SEBELUM Satu Pun Request Dikirim

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: Bagian 5 "Business Logic & Race Condition Synthesizer" di `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` (Crown Jewel Analysis, jawaban AI lain diteruskan Cipta 24 Nov 2026 00:05 WIB). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai satu analisis mahkota permata terbukti mengarahkan temuan yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai PALING AWAL pada setiap target bounty web/API klasik in-scope — SEBELUM satu pun request pengujian dikirim, dan sebelum hipotesis apa pun ditulis. Dipakai sesudah indeks aset selesai (`pemetaan-permukaan-serangan`) dan sebelum `perburuan-kerentanan-spesifik` dijalankan. Bila agen sudah mengirim request pengujian tanpa tabel mahkota permata = pelanggaran prosedur: berhenti, buat tabelnya dulu, baru lanjut.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menyusun tabel mahkota permata per target + mengaitkan tiap hipotesis ke satu permata |
| Pengerjaan | **A59 Threat Hunter** | Menemukan aset bernilai dari arsitektur/JS/dokumentasi target |
| Audit | **A60 Security Auditor** | Memeriksa apakah peringkat permata beralasan dan hipotesis benar-benar menargetkan permata itu |
| Pemimpin | **Muse** | Menyetujui tabel mahkota permata sebelum pengujian dimulai; memutuskan permata mana yang diburu dulu |

## Sudah tercakup (jangan diduplikat)

- **Inventarisasi aset & endpoint teknis** ada di `pemetaan-permukaan-serangan` — skill ini TIDAK mengulang inventarisasi; ia mengambil indeks itu sebagai bahan mentah dan hanya menambahkan LAPISAN NILAI (aset mana yang paling berharga bila dimanipulasi).
- **Definisi + cara mengenali + standar bukti Business Logic Flaws dan Race Condition** ada di `perburuan-kerentanan-spesifik` — skill ini tidak mengulang ketiganya; ia menentukan PERMATA mana yang diburu dengan kategori-kategori itu.
- **Titik yang dipercaya server tanpa verifikasi** ada di `analisis-batas-kepercayaan` — itu peta kepercayaan, bukan peta nilai; jangan campur keduanya.
- **Eskalasi dari temuan rendah yang sudah ada** ada di `eskalasi-dampak-otomatis` — arahnya berlawanan: skill itu berangkat dari temuan, skill ini berangkat dari NILAI ASET sebelum ada temuan.
- **Penilaian severity setelah temuan terbukti** ada di `penilaian-cvss` + `artikulasi-dampak-bisnis` — skill ini menilai nilai aset SEBELUM pengujian, bukan severity sesudah temuan.

## Signal

Sinyal bahwa sebuah aset adalah "mahkota permata" — aset yang bila dimanipulasi memberi dampak bisnis nyata dan bernilai high/critical di triase:

| # | Signal | Contoh aset |
|---|---|---|
| 1 | **Nilai uang langsung** — aset adalah saldo, kredit, atau alat bayar yang bisa dikuras/digandakan | Saldo kredit akun, dompet, poin yang bisa ditukar uang, kupon bernilai uang |
| 2 | **Hasil yang dipercaya pihak ketiga** — output aset dipakai orang lain sebagai kebenaran (keputusan bisnis, peringkat, sertifikat) | Hasil survei komersial, hasil voting/pemilihan, skor/sertifikasi, peringkat produk |
| 3 | **Batas antar-tenant** — satu aset memisahkan data/uang dua pelanggan berbeda; jebolnya berarti data/uang bercampur | Data antar-tenant SaaS, saldo antar-organisasi, dokumen antar-perusahaan |
| 4 | **Kelangkaan yang dijual** — aset adalah slot/jatah terbatas yang diperebutkan dan bernilai bila direbut | Slot reservasi, kursi/kuota terbatas, stok edisi terbatas, antrean prioritas |
| 5 | **Keputusan yang tidak bisa dibatalkan** — sekali berubah, dampaknya menyebar dan sulit ditarik kembali | Status persetujuan/pembayaran, pengumuman hasil, transfer dana yang sudah jalan |

Aset yang tidak cocok dengan satu pun signal di atas = BUKAN mahkota permata; catat sebagai aset biasa dan jangan jadikan prioritas utama.

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
10. **Larang aksi destruktif (DROP, DELETE, hapus data)** — pembuktian aman dan read-only.
11. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
12. **Tidak ada request pengujian sebelum tabel mahkota permata disetujui Muse.** Request yang sudah telanjur dikirim tanpa tabel = hentikan pengujian, buat tabelnya, catat pelanggaran di log.
13. **Tidak ada hipotesis tanpa permata.** Setiap hipotesis yang maju ke `perburuan-kerentanan-spesifik` wajib menyebut SATU permata dari tabel; hipotesis yang tidak menargetkan permata = ditolak atau diturunkan prioritasnya.

## Probe Steps

### Langkah 1 — Ambil indeks aset sebagai bahan mentah

Ambil indeks dari `pemetaan-permukaan-serangan` (subdomain, endpoint, layanan, arsitektur). Jangan memetakan ulang — bila indeks belum ada atau belum SIAP UJI, kembali ke skill itu dulu.

**Standar lulus:** indeks tersedia + tiap entri punya metode, parameter, dan catatan otorisasi.

### Langkah 2 — Daftarkan kandidat permata

Untuk tiap aset/endpoint di indeks, tanyakan: "Bila aset ini dimanipulasi, siapa yang dirugikan dan berapa besar?" Cocokkan dengan tabel Signal di atas. Tulis kandidat dengan kolom: aset/endpoint | signal yang cocok (#1–#5) | siapa yang dirugikan | apa yang bisa dilakukan penyerang (satu kalimat).

**Standar lulus:** tiap kandidat punya kelima kolom terisi; kandidat tanpa signal yang cocok = dibuang dari daftar, bukan dipaksakan masuk.

### Langkah 3 — Beri peringkat (skor nilai)

Beri tiap kandidat skor 1–3 pada tiga dimensi, lalu jumlahkan:

| Dimensi | 1 | 2 | 3 |
|---|---|---|---|
| **Nilai** — berapa besar nilai uang/kepercayaan yang dipertaruhkan | Kecil (kosmetik, preferensi) | Sedang (diskon, poin, data non-sensitif) | Besar (uang, saldo, hasil resmi yang dipercaya pihak ketiga) |
| **Jangkauan** — berapa banyak pihak yang kena bila dimanipulasi | Hanya akun sendiri | Satu tenant/organisasi lain | Banyak tenant/pengguna atau publik |
| **Tidak-terbalikkan** — seberapa sulit menarik kembali dampaknya | Mudah dibatalkan admin | Bisa dibatalkan dengan usaha | Praktis tidak bisa ditarik (uang sudah pindah, hasil sudah diumumkan) |

**Standar lulus:** tiap kandidat punya 3 skor + total (3–9); peringkat diurutkan dari total tertinggi; 2 kandidat dengan total sama diurutkan berdasarkan Nilai dulu, lalu Jangkauan.

### Langkah 4 — Bekukan tabel + kaitkan hipotesis

Tulis tabel mahkota permata final (peringkat 1 = prioritas pertama) dan serahkan ke Muse untuk disetujui. Sesudah disetujui, tiap hipotesis di `perburuan-kerentanan-spesifik` WAJIB menuliskan nomor permata yang ditargetkannya.

**Standar lulus:** tabel disetujui Muse + tidak ada hipotesis yang maju tanpa nomor permata.

## Execution Gate

| Gerbang | Syarat lulus | Bila gagal |
|---|---|---|
| G1 — Indeks siap | Indeks dari `pemetaan-permukaan-serangan` berstatus SIAP UJI | Kembali ke pemetaan; jangan lanjut |
| G2 — Tabel lengkap | Tiap kandidat punya 5 kolom Langkah 2 + 3 skor Langkah 3 | Lengkapi dulu; tabel setengah jadi = belum boleh dipakai |
| G3 — Persetujuan sebelum request | Muse menyetujui tabel SEBELUM request pengujian pertama | HENTIKAN semua pengujian sampai disetujui |
| G4 — Hipotesis terikat permata | Tiap hipotesis menyebut nomor permata dari tabel | Hipotesis ditolak / turun prioritas |
| G5 — Audit | A60 memeriksa alasan peringkat sebelum hipotesis peringkat 1 diuji | Perbaiki peringkat; jangan uji permata yang peringkatnya belum diaudit |

## Alat

| Alat | Cara pakai |
|---|---|
| Indeks aset (`pemetaan-permukaan-serangan`) | Bahan mentah Langkah 1 — jangan petakan ulang |
| Dokumentasi/OpenAPI + JS target | Sumber kandidat permata (fitur bernilai uang/kepercayaan/kelangkaan) |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai bila analisis butuh melihat fitur sebagai pengguna |
| `~/workspace/catatan/log-bug-bounty.md` | Log tabel mahkota permata + keputusan peringkat per tanggal |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + target]
Tabel mahkota permata (disetujui Muse: [ya/belum]):
  #1 | [aset/endpoint] | signal: [#n — nama] | dirugikan: [siapa] | bila dimanipulasi: [satu kalimat]
      Nilai: [1-3] | Jangkauan: [1-3] | Tidak-terbalikkan: [1-3] | Total: [3-9]
  #2 | [aset/endpoint] | ...
Aset biasa (bukan permata): [daftar singkat — jangan diburu dulu]
Hipotesis yang maju: [hipotesis] → permata #[n]
Status: [tabel disetujui / menunggu persetujuan / ditolak — alasan]
```

## Available connectors

Tidak ada konektor khusus untuk skill ini. Analisis memakai indeks aset + dokumentasi target dan pencatatan di file log di atas.

## Websites

- Referensi riset Bagian 5: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`
- Indeks aset: `~/workspace/tmp/pusat-komando-push/data/skills/pemetaan-permukaan-serangan/SKILL.md`
- Kategori pembuktian: `~/workspace/tmp/pusat-komando-push/data/skills/perburuan-kerentanan-spesifik/SKILL.md`

## Alternatives for better results

- Bila target ternyata tidak punya aset bernilai uang/kepercayaan (mis. hanya konten statis), catat "tidak ada mahkota permata" dan serahkan ke Muse — jangan memaksakan peringkat pada aset kosmetik.
- Bila satu permata ternyata menargetkan dua signal sekaligus (mis. saldo antar-tenant), catat kedua signalnya — itu menaikkan prioritas, bukan alasan membuat dua baris untuk aset yang sama.

## Batasan yang diketahui

- Peringkat adalah penilaian SEBELUM pengujian — permata peringkat 1 bisa ternyata tidak rentan; itu bukan kegagalan analisis, itu hasil yang dicatat dan peringkat berikutnya yang diburu.
- Skill ini tidak membuktikan kerentanan apa pun — pembuktian tetap memakai `perburuan-kerentanan-spesifik` (business logic / race condition) dan `serangan-paket-tunggal-http2` (race condition presisi waktu).
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome pada agennya — pakai skill ini hanya bila targetnya punya aset bisnis bernilai (saldo, hasil, data tenant), bukan untuk menilai trik terhadap model.
