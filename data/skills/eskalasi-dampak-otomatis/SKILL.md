# Skill: Eskalasi Dampak Otomatis — Uji Rantai Lanjutan dari Temuan Rendah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md` Kategori 4 butir 2 (Impact Chaining / Eskalasi Dampak Otomatis). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu temuan rendah yang terbukti tereskalasi dan dicatat di log.

## Pemicu (Trigger & Scope)

Dipakai setiap kali ada temuan yang sudah berstatus VERIFIED (lolos `skeptic-false-positive-eliminator`) tetapi dampaknya sendiri RENDAH — terlalu kecil untuk dibayar atau dinilai rendah di triase — dan diduga bisa menjadi pintu masuk rantai lanjutan ke dampak yang lebih besar. Dipakai sesudah triase awal memberi skor rendah, SEBELUM memutuskan melaporkan temuan itu apa adanya atau membuangnya. Satu temuan rendah = satu kali lewat katalog rantai di bawah.

"Otomatis" di sini artinya **sistematis dan terpicu otomatis oleh skor rendah** — setiap temuan rendah WAJIB dicek terhadap katalog rantai, bukan hanya bila seseorang teringat. Bukan otomasi tanpa pengawasan: tiap langkah eskalasi dijalankan dan divalidasi dengan human-in-the-loop.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55 Analis Rantai & Pelapor** | Memetakan temuan rendah ke katalog rantai, menjalankan uji eskalasi |
| Pengerjaan | **A62 Exploit Developer** | Menjalankan teknik bukti aman untuk tiap langkah eskalasi |
| Audit | **A60 Security Auditor** | Memeriksa tiap langkah eskalasi sudah terbukti sendiri + dampak akhir nyata |
| Pemimpin | **Muse** | Memutuskan rantai mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Perangkaian temuan yang masing-masing sudah VERIFIED** ada di `perangkaian-kerentanan` — skill itu HANYA menggabungkan temuan yang masing-masing sudah terbukti sendiri ("satu mata rantai yang belum terbukti = rantai belum ada"). Skill ini adalah **kebalikannya**: berangkat dari SATU temuan rendah dan secara aktif MENGUJI apakah rantai lanjutan ada — mata rantai lanjutan di sini belum terbukti, dan tugas skill ini adalah membuktikannya atau membuktikan tidak ada. Bila eskalasi terbukti, hasil akhirnya diserahkan ke `perangkaian-kerentanan` untuk dirangkai sebagai laporan rantai.
- **Teknik bukti aman per jenis celah** ada di `verifikasi-poc-aman` — tiap langkah eskalasi memakai teknik dari katalog itu (mis. `document.domain` untuk XSS, callback canary untuk redirect/SSRF), bukan teknik baru.
- **Verifikasi adversarial + skor + draf laporan** ada di `skeptic-false-positive-eliminator`, `penilaian-cvss`, `artikulasi-dampak-bisnis`, `triase-duplikat`, `laporan-poc-otomatis` — hasil eskalasi yang terbukti masuk kembali ke alur itu (skor dihitung dari dampak AKHIR, bukan dampak awal).
- **Rantai injeksi prompt di program bounty agen AI** ada di `transfer-hunting` — skill ini untuk rantai web/API klasik.
- Alur sesudah skill ini: eskalasi TERBUKTI → `perangkaian-kerentanan` (rangkai + buktikan ujung-ke-ujung) → `penilaian-cvss` + `artikulasi-dampak-bisnis` (dari dampak akhir) → `triase-duplikat` → draf laporan → tinjau manusia → persetujuan Cipta → kirim. Eskalasi GAGAL (tidak ada rantai) → temuan rendah dilaporkan apa adanya atau dibuang, sesuai keputusan triase.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Rantai yang butuh korban memakai akun KEDUA MILIK SENDIRI sebagai korban; jangan pernah melibatkan pengguna asli.
4. **Tanpa DoS/DDoS.** Tanpa payload di permukaan publik.
5. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).** Tiap langkah eskalasi yang berhasil HARUS ditinjau manusia sebelum langkah berikutnya dijalankan.
6. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
8. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian eskalasi harus aman dan read-only: bukti baca, callback canary, `document.domain` — tanpa perintah yang menulis/menghapus di server.
9. **Jangan membesar-besarkan severity.** Hanya dampak AKHIR yang TERBUKTI yang boleh diklaim; rantai yang berhenti di tengah jalan = belum terbukti, jangan klaim dampak akhirnya.
10. **Sensor PII/token/kredensial di semua bukti ([REDACTED]) sebelum laporan disusun.**
11. **Jangan pernah mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia dulu; pengiriman selalu manual + disetujui Cipta.
12. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, jangan menguji payload injeksi.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Methodology & Payloads — katalog rantai eskalasi

Cek temuan rendah terhadap SETIAP pola di bawah yang titik awalnya cocok. Pola dicatat sebagai hipotesis dulu ("diduga bisa tereskalasi"), lalu diuji langkah demi langkah (Gerbang 2). Pola yang titik awalnya tidak cocok = lewati, jangan dipaksakan.

| # | Temuan rendah (titik awal) | Rantai lanjutan yang diuji | Dampak akhir bila terbukti |
|---|---|---|---|
| 1 | Open Redirect | Open Redirect + manipulasi `redirect_uri` OAuth → `authorization code` korban tiba di alamat penyerang → tukar kode jadi sesi korban | Account Takeover (ATO) |
| 2 | Open Redirect | Open Redirect + tautan reset kata sandi → token reset korban bocor lewat parameter `redirect` / `Referer` ke alamat penyerang | Account Takeover (ATO) |
| 3 | SVG File Upload | SVG terunggah + dieksekusi sebagai skrip saat dilihat → Stored XSS → skrip jalan di sesi admin yang membuka berkas → aksi admin (ubah peran, baca data) | Stored XSS + eskalasi ke admin |
| 4 | SVG / HTML File Upload | Berkas terunggah + disajikan tanpa `Content-Disposition: attachment` dan tanpa `Content-Security-Policy` ketat → eksekusi skrip di origin aplikasi | Stored XSS di origin utama |
| 5 | Self-XSS | Self-XSS + CSRF (tanpa token anti-CSRF) → CSRF memaksa browser korban mengirim payload Self-XSS ke akunnya sendiri | Stored XSS di akun korban |
| 6 | CORS misconfiguration | CORS longgar + IDOR → respons berisi objek milik pengguna lain bisa dibaca lintas situs | Pencurian data lintas situs |
| 7 | Subdomain Takeover | Subdomain diambil alih + cookie sesi tanpa atribut `Domain` yang ketat → skrip di subdomain membaca/mengirim cookie | Pembajakan sesi |
| 8 | Cache Poisoning | Respons beracun tersimpan di CDN + payload XSS di dalamnya → dieksekusi ke semua pengunjung | Stored XSS lewat cache |
| 9 | Reflected XSS (butuh klik) | Reflected XSS + Open Redirect / halaman tepercaya sebagai umpan → korban mengklik tautan dari domain tepercaya | XSS dengan kepercayaan domain |
| 10 | Info disclosure kecil | Kebocoran token/CSRF/nonce + endpoint sensitif tanpa otorisasi tambahan → token dipakai untuk aksi tanpa sah | Eskalasi ke aksi tanpa sah |

Catatan: pola 5–8 juga muncul sebagai pasangan di `perangkaian-kerentanan` — bedanya, di sana kedua mata rantai sudah VERIFIED; di sini hanya titik awalnya yang VERIFIED dan mata rantai lanjutannya masih hipotesis yang harus diuji.

## Langkah + gerbang

### Gerbang 1 — Petakan temuan rendah ke katalog

1. Tulis temuan rendah + dampaknya sendiri + skor triase awalnya (dari `triase-duplikat`).
2. Cocokkan titik awalnya dengan kolom pertama katalog di atas. Tulis SEMUA pola yang cocok sebagai hipotesis eskalasi, plus prasyarat tiap pola (mis. pola 1 butuh `redirect_uri` yang tidak divalidasi ketat; pola 3 butuh SVG dieksekusi saat dibuka admin).
3. Urutkan hipotesis dari yang paling mungkin (prasyarat sudah terlihat ada) ke yang paling spekulatif.
4. **Standar lulus:** daftar hipotesis tertulis dengan prasyarat tiap pola. Tidak ada pola yang cocok = eskalasi selesai dengan hasil TIDAK ADA RANTAI — temuan dilaporkan apa adanya atau dibuang sesuai triase.

### Gerbang 2 — Uji tiap langkah eskalasi dengan bukti aman

1. Untuk hipotesis pertama, uji langkah lanjutan SATU PER SATU, memakai teknik bukti aman dari `verifikasi-poc-aman`:
   - Pola 1–2: callback canary milik sendiri sebagai `redirect_uri` / alamat redirect; tunjukkan kode/token tiba di canary — JANGAN menukar kode jadi sesi akun orang lain (penukaran hanya pada akun kedua milik sendiri).
   - Pola 3–4: unggah SVG berisi skrip yang hanya mencetak `document.domain` di sesi akun kedua milik sendiri; tunjukkan skrip jalan saat berkas dibuka — JANGAN mencuri cookie/token atau memicu aksi destruktif.
   - Pola 5: CSRF dari akun penyerang (milik sendiri) ke akun korban (milik sendiri) yang mengirim payload Self-XSS yang hanya mencetak `document.domain`.
   - Pola 6–10: teknik bukti aman sesuai jenis langkahnya (callback canary / sesi akun kedua / respons yang disensor).
2. **BERHENTI di langkah yang gagal.** Bila satu langkah eskalasi tidak terbukti, hipotesis itu GAGAL — jangan menambal langkah yang gagal dengan asumsi. Catat langkah yang gagal + buktinya, lalu lanjut ke hipotesis berikutnya.
3. Tiap langkah yang berhasil HARUS ditinjau manusia sebelum langkah berikutnya dijalankan.
4. **Standar lulus per hipotesis:** semua langkah eskalasi terbukti dengan bukti aman + reference ID. Satu langkah gagal = hipotesis gagal.

### Gerbang 3 — Buktikan dampak AKHIR, bukan tiap langkahnya saja

1. Jalankan rantai lengkap dari langkah pertama sampai dampak akhir, memakai akun sendiri di kedua sisi (penyerang + korban — keduanya milik sendiri).
2. Buktikan dampak AKHIR-nya: untuk ATO, tunjukkan sesi akun korban benar-benar terbentuk; untuk Stored XSS ke admin, tunjukkan skrip jalan di sesi akun kedua milik sendiri yang berperan sebagai admin.
3. **Standar lulus:** ada bukti dampak akhir nyata pada akun sendiri + langkah reproduksi persis dari langkah 1. Rantai yang berhenti di tengah jalan = belum terbukti.

### Gerbang 4 — Nilai ulang, serahkan ke perangkaian + triase

1. Nilai ulang: dampak akhir vs dampak temuan rendah awal — bila dampak akhir tidak lebih besar dari temuan awal, laporkan temuan awalnya saja, jangan klaim rantai.
2. Catat jumlah interaksi korban yang dibutuhkan (0-klik / 1-klik / lebih) dengan jujur — itu memengaruhi tier hadiah.
3. Serahkan rantai yang terbukti ke `perangkaian-kerentanan` (dirangkai sebagai laporan rantai) → `penilaian-cvss` + `artikulasi-dampak-bisnis` (dihitung dari dampak AKHIR) → `triase-duplikat` → draf laporan → tinjau manusia → persetujuan Cipta → kirim.
4. **Standar lulus:** keputusan tercatat di log dengan alasan + jumlah klik/interaksi korban tertulis jujur + dampak akhir vs awal dibandingkan.

## Validation Gate (verifikasi deterministik baseline vs exploit)

- Baseline: tiap langkah eskalasi dibandingkan dengan perilaku normal tanpa payload (mis. `redirect_uri` ke domain tepercaya → kode TIDAK bocor; SVG tanpa skrip → tidak ada eksekusi). Bila perilaku exploit sama dengan baseline, langkah itu bukan celah.
- Exploit: rantai lengkap HARUS terulang dari sesi bersih + token segar, minimal 1 kali pengulangan penuh sesudah pembuktian pertama; dampak akhir HARUS teramati pada akun sendiri, bukan sekadar pesan sukses dari server (silent drop).
- Verdict TERBUKTI hanya sah bila perbandingan baseline-vs-exploit tiap langkah tertulis di log dengan reference ID bukti.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (penyerang + korban) | Wajib — kedua sisi rantai memakai akun milik sendiri |
| Server canary sendiri (Interactsh / canary milik sendiri) | Menerima DNS/HTTP callback untuk redirect/OAuth — catat hit-nya saja, jangan ambil isinya |
| Headless browser (sesi bersih) | Menjalankan bukti XSS (`document.domain`) di sesi akun kedua milik sendiri |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis eskalasi + langkah yang gagal/berhasil + bukti dampak akhir + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur]
Temuan rendah awal: [nama + reference ID bukti + skor triase awal]
Hipotesis eskalasi: [nomor pola katalog + rantai yang diduga]
Langkah eskalasi:
  - Langkah 1: [apa yang diuji] — TERBUKTI/GAGAL — [reference ID bukti]
  - Langkah 2: [apa yang diuji] — TERBUKTI/GAGAL — [reference ID bukti]
Dampak akhir terbukti: [apa yang terjadi pada akun sendiri / BELUM TERBUKTI — berhenti di langkah X]
Interaksi korban: [0-klik / 1-klik / lebih — jelaskan]
Dampak akhir vs awal: [lebih besar / sama — bila sama, laporkan temuan awal saja]
Keputusan: [maju ke perangkaian-kerentanan / laporkan temuan awal / dibuang + alasan]
Status: [tereskalasi / tidak ada rantai / ditolak]
```

## Batasan yang diketahui

- Eskalasi yang butuh interaksi korban dinilai lebih rendah oleh sebagian program — catat jujur, jangan sembunyikan.
- Dua temuan pada target/program yang berbeda umumnya TIDAK bisa dirangkai jadi satu laporan.
- Katalog di atas tidak lengkap — pola baru yang ditemukan di lapangan ditambahkan ke katalog dengan nomor baru + dicatat tanggalnya, bukan dipakai diam-diam.
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome — gunakan `transfer-hunting` untuk rantai prompt AI, bukan skill ini.
