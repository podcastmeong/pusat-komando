# Skill: Output Tidak Aman — XSS/SSRF lewat Jawaban AI yang Dirender

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-dua-perspektif-skill-bug-bounty-ai-2026-11-23.md`, Perspektif 2 (Insecure Output Handling). Jangan klaim metode ini terbukti sampai ada satu uji end-to-end yang lolos gerbang di bawah.

## Pemicu

Dipakai saat menguji aplikasi AI (chatbot, agen, asisten berkode) yang menampilkan jawaban model ke pengguna: ada dugaan jawaban AI dirender tanpa sanitasi sehingga penyerang bisa menyelipkan payload lewat inputnya sendiri. Vektornya adalah **output AI**, bukan input yang langsung ditampilkan — itu yang membedakan skill ini dari XSS klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Merancang input pemicu + payload, menjalankan uji render |
| Pengerjaan | **A65 Mobile Security Tester** | Uji render di permukaan mobile/aplikasi (bila targetnya aplikasi mobile) |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan pengiriman laporan; semua laporan butuh persetujuan Cipta |

## Sudah tercakup (jangan diduplikat)

- **Definisi + pembuktian XSS klasik** → `fondasi-kerentanan-web-api`. Skill ini khusus vektor **output AI** (payload lahir dari jawaban model, bukan dari input yang langsung di-echo).
- **Isi injeksi prompt** (cara membuat model menuruti instruksi penyerang) → `buru-bug-bounty`. Skill ini mulai dari titik model sudah menghasilkan payload — fokusnya di **render**, bukan di injeksinya.
- **Validasi + laporan** (cek duplikat, skor keparahan, format laporan triase-ready) → `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Server canary milik sendiri, data uji palsu. Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target atau canary dengan permintaan.
5. **Tanpa payload di permukaan publik.** Payload dan halaman pemicu jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap klaim berhasil harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Google AI VRP: payload injeksi DIBLOKIR.** Tim 4 analisis format saja — jangan menyiapkan, memparafrasa, atau mencari jalan lain untuk payload injeksi Google.

## Langkah + gerbang

### Langkah 1 — Petakan cara render

Pahami cara aplikasi menampilkan jawaban agen: apakah Markdown dirender otomatis? Apakah tautan/gambar dimuat otomatis (tanpa klik pengguna)? Apakah ada sanitasi (tag/URL apa yang dibuang)? Catat hasil observasi ini — tanpa peta render, payload yang dibuat hanya tebakan.

**Standar lulus:** tertulis, untuk target itu, (a) Markdown dirender atau tidak, (b) gambar/tautan dimuat otomatis atau perlu klik, (c) ada/tidaknya sanitasi yang teramati.

### Langkah 2 — Buat input pemicu

Buat input yang membuat jawaban agen mengandung payload yang diinginkan:

- **Uji SSRF:** jawaban berisi tautan/gambar Markdown yang mengarah ke server canary milik sendiri, mis. `![x](https://canary-milik-sendiri/unik-id)`. Pertanyaannya: apakah server aplikasi mengambil URL itu (prefetch/proxy/thumbnail) saat jawaban dirender?
- **Uji XSS:** jawaban berisi payload skrip (mis. lewat HTML yang lolos sanitasi atau lewat atribut tautan/gambar). Pertanyaannya: apakah payload dieksekusi di browser yang melihat jawaban itu?

**Standar lulus:** input tercatat persis (teks lengkap), payload tercatat persis, dan hipotesisnya satu kalimat: "Saya menduga X terjadi karena Y."

### Langkah 3 — Uji render HANYA di browser/sesi milik sendiri

Jalankan uji di browser/sesi milik sendiri. **Self-XSS (payload hanya menyerang diri sendiri) umumnya TIDAK dibayar** — bukti yang dihitung adalah payload yang dibuat di satu akun/sesi milik sendiri **dieksekusi saat dilihat akun/sesi kedua milik sendiri** (akun korban = akun sendiri yang kedua, data canary palsu).

**Standar lulus:** dua akun/sesi milik sendiri dipakai (pembuat + penonton); tidak ada browser, akun, atau sesi orang lain yang terlibat.

### Langkah 4 — Kumpulkan bukti pengambilan/eksekusi

- **SSRF:** log server canary tercatat (waktu, IP peminta, path/ID unik) — membuktikan server aplikasi benar-benar mengambil URL itu.
- **XSS:** eksekusi teramati di sesi penonton (mis. callback canary dari eksekusi skrip, atau efek yang terlihat dan terdokumentasi) — bukan sekadar payload tampil sebagai teks.

**Standar lulus (gerbang utama): tanpa bukti pengambilan/eksekusi = BELUM BERHASIL.** Payload yang hanya tampil sebagai teks, atau canary yang tidak pernah dipanggil, adalah gagal — catat kenapa gagal, lalu variasikan format/permukaan dan ulangi dari Langkah 2.

### Langkah 5 — Nilai dampak + tulis draf

Tulis apa yang akan didapat penyerang bila korbannya sungguhan (mis. pencurian sesi, aksi atas nama korban, akses jaringan internal lewat SSRF). Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (bukan "bisa berbahaya"), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

- **Server canary milik sendiri** — endpoint HTTP(S) yang mencatat setiap permintaan (waktu, IP, path/ID unik) dan tidak menyimpan data apa pun selain log akses itu. Satu ID unik per uji, supaya satu hit tidak tertukar dengan uji lain.
- **Dua akun/sesi uji sendiri** — akun pembuat payload + akun penonton; keduanya milik sendiri, data canary palsu.
- **Browser/sesi milik sendiri** — tempat render diuji; jangan pernah memakai browser pengguna lain.

## Format output

Log setiap uji ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Cara render: [Markdown dirender? tautan/gambar dimuat otomatis? sanitasi teramati?]
Payload: [input pemicu + payload persis di jawaban AI]
Bukti pengambilan/eksekusi: [log canary tercatat / eksekusi teramati — atau "TIDAK ADA"]
Dampak: [apa yang didapat penyerang bila korban sungguhan]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```
