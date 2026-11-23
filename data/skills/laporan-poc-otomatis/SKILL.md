# Skill: Laporan PoC Otomatis — Laporan Terstruktur (Ringkasan, Reproduksi, Bukti, Dampak, Perbaikan)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md` butir 50. Isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu draf laporan yang disusun dengan skill ini, dicatat di log, dan lolos triase. Label ini berlaku untuk semua bagian sampai ada kasus nyata yang dicatat.

## Pemicu

Dipakai setiap kali ada temuan yang sudah lewat `skeptic-false-positive-eliminator` (VERIFIED), sudah punya skor CVSS (`penilaian-cvss`), pernyataan dampak bisnis (`artikulasi-dampak-bisnis`), dan lolos cek duplikat + tier (`triase-duplikat`) — dan perlu disusun jadi draf laporan lengkap agar triager bisa memvalidasi dalam hitungan menit. Satu temuan VERIFIED = satu draf laporan. Draf selesai = draf yang lolos semua gerbang di bawah, BUKAN draf yang "kelihatan lengkap".

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A67 Report Writer** | Merakit draf laporan dari bahan yang sudah ada (bukti, skor, dampak); menulis langkah reproduksi + saran perbaikan |
| Dukungan | **A55 Analis Rantai & Pelapor** | Menyediakan rantai serangan langkah-demi-langkah bila temuan berasal dari gabungan celah |
| Audit | **A60 Security Auditor** | Memeriksa tiap klaim bisa ditelusur ke bukti; menolak draf yang klaimnya tanpa bukti |
| Pemimpin | **Muse** | Memutuskan draf maju ke Cipta untuk persetujuan atau dikembalikan |

## Sudah tercakup (jangan diduplikat)

- **Struktur laporan dasar** (judul → ringkasan → langkah repro → bukti → scope → dampak) ada di `laporan-abstrak` — skill ini **memakai struktur itu dan melengkapinya**: langkah reproduksi WAJIB dalam bentuk perintah `curl`/skrip Python yang bisa dijalankan ulang, bukti WAJIB tersensor + ber-reference-ID, dan ditambah bagian **Saran Perbaikan** yang tidak ada di `laporan-abstrak`.
- **Alur abstrak-dulu 0din** (abstrak → jawaban scope ≤3 hari kerja → detail lengkap/PoC) ada di `laporan-abstrak` — tetap berlaku untuk 0din; skill ini menyusun bagian "detail lengkap/PoC"-nya, bukan mengganti alur abstraknya.
- **Verifikasi temuan** ada di `skeptic-false-positive-eliminator` — skill ini TIDAK memverifikasi ulang; hanya merakit bahan yang sudah VERIFIED. Temuan belum VERIFIED = jangan dibuatkan laporan.
- **Skor CVSS** ada di `penilaian-cvss`; **pernyataan dampak** ada di `artikulasi-dampak-bisnis` — skill ini MENYISIPKAN hasil keduanya, bukan menghitung ulang.
- **Cek duplikat + tier hadiah** ada di `triase-duplikat` — draf laporan hanya dibuat SETELAH lolos cek duplikat.
- Alur sesudah skill ini: draf lengkap → tinjau manusia 2–3 menit → persetujuan Cipta → kirim (oleh A69 yang melacak status, sesuai `laporan-abstrak`).

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan dibuatkan laporan.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.** Draf boleh disiapkan; pengiriman hanya setelah Cipta setuju. Berlaku untuk semua program.
6. **Patuhi larangan otomasi program:** huntr "Humans only" (tanpa otomasi pengiriman); **Gray Swan dilewati total** (jangan disentuh).
7. **JANGAN PERNAH mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia 2–3 menit sebelum submit. Satu laporan halusinasi yang terkirim bisa merusak signal score/reputasi akun secara permanen. "Otomatis" di skill ini artinya PERAKITAN drafnya yang dibantu otomasi — pengirimannya SELALU manual + disetujui Cipta.
8. **LLM tidak boleh mengubah bukti.** Bukti HTTP disimpan di file/database di luar memori LLM; hanya reference ID yang diberikan ke LLM saat menyusun laporan, log asli disisipkan secara programatik di akhir. LLM hanya menulis narasi di sekitar bukti, bukan menulis ulang isi bukti.
9. **Sensor PII pada semua bukti** (screenshot/log) SEBELUM laporan disusun — token, kata sandi, email/nomor pribadi, dan data sensitif lain diganti `[REDACTED]`. Bukti tanpa sensor = draf belum selesai.
10. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah. Skor CVSS dan pernyataan dampak disisipkan apa adanya dari skill asalnya.
11. **Pembuat draf tidak boleh meloloskan drafnya sendiri** — A60 yang mengaudit; A67 tidak mengaudit drafnya sendiri.

## Langkah + gerbang

### Gerbang 1 — Kumpulkan bahan (jangan menulis sebelum bahan lengkap)

Kumpulkan, sebelum satu kalimat laporan ditulis:

- [ ] Reference ID bukti sesi bersih dari `skeptic-false-positive-eliminator` (pasangan Request/Response, sudah disensor)
- [ ] Vektor + skor + band CVSS dari `penilaian-cvss` (atau catatan "CVSS tidak cocok" + tier program)
- [ ] Kalimat dampak + paragraf pendukung dari `artikulasi-dampak-bisnis`
- [ ] Hasil cek duplikat + tier hadiah dari `triase-duplikat`
- [ ] Screenshot/log pendukung (sudah disensor) bila ada — tiap file punya nama + reference ID

**Standar lulus:** semua kotak tercentang. Satu bahan hilang = draf BELUM boleh ditulis; kembali ke skill pemilik bahan itu.

### Gerbang 2 — Tulis langkah reproduksi yang bisa dijalankan ulang (curl + Python)

Langkah reproduksi adalah jantung laporan — triager harus bisa mengulang dalam hitungan menit tanpa menebak:

1. Tulis langkah bernomor, dari kondisi awal (akun apa, login sebagai siapa) sampai hasil yang terlihat.
2. Tiap langkah yang berupa permintaan HTTP WAJIB disertai perintah `curl` lengkap (method, URL, header, body) ATAU skrip Python minimal (`requests`) — bukan deskripsi ("lalu kirim permintaan X"). Token/kredensial di perintah diganti placeholder (`$TOKEN_A`, `[REDACTED]`), dengan catatan cara mendapatkannya ("login sebagai akun tes A, salin token dari respons login").
3. Tulis HASIL YANG DIHARAPKAN di tiap langkah kunci ("respons mengembalikan data akun B, status 200") — triager tahu ia berhasil mengulang bila melihat hasil itu.
4. Sertakan langkah **baseline** bila relevan (minta objek yang sama tanpa token → respons berbeda; membuktikan data tidak publik) — sesuai Gerbang 1 `skeptic-false-positive-eliminator`.
5. Uji ulang langkah reproduksi dari sesi bersih (token segar) SEBELUM dimasukkan ke laporan — langkah yang belum diuji ulang = jangan ditulis.

**Standar lulus:** orang ketiga yang hanya membaca laporan bisa mengulang temuan dari nol tanpa bertanya. Langkah yang butuh tebakan = gerbang gagal.

### Gerbang 3 — Rakit bukti (screenshot/log) + saran perbaikan

**Bukti:**
- Sisipkan screenshot/log dengan reference ID, urut sesuai langkah reproduksi. Tiap bukti punya caption satu baris ("Langkah 3: respons mengembalikan data akun B").
- Pastikan sensor PII sudah dilakukan SEBELUM penyisipan (cek ulang tiap file: cari token, email, NIK, kata sandi).
- Bukti yang disisipkan secara programatik dari file asli (bukan diketik ulang LLM) — isi log tidak boleh berubah satu karakter pun dari file sumber.

**Saran perbaikan (wajib ada, per jenis celah — pilih yang sesuai, sesuaikan dengan kode/fitur target):**

| Jenis celah | Saran perbaikan (tulis + cara verifikasi perbaikan) |
|---|---|
| IDOR / BOLA | Periksa kepemilikan objek di server pada SETIAP permintaan (bukan hanya di UI); uji ulang: akun A minta objek akun B → harus 403/404 |
| SSRF | Allowlist URL tujuan + blokir alamat internal/metadata cloud (169.254.169.254); uji ulang: minta URL internal → harus ditolak |
| XSS | Encode output sesuai konteks + Content-Security-Policy; uji ulang: payload tampil sebagai teks, bukan dieksekusi |
| Broken Authentication | Token tidak bisa ditebak + kedaluwarsa setelah logout/ganti kata sandi; uji ulang: token lama → harus ditolak |
| Salah konfigurasi API | Otorisasi per peran di server + jangan kembalikan data berlebih; uji ulang: peran biasa → tidak dapat data/aksi admin |
| CSRF | Token anti-CSRF per sesi + cookie SameSite; uji ulang: permintaan tanpa token → harus ditolak |
| Lainnya | Tulis perbaikan spesifik + SATU cara menguji bahwa perbaikan berhasil (langkah verifikasi) |

- Tiap saran perbaikan WAJIB disertai cara verifikasi ("uji ulang: ...") — saran tanpa cara verifikasi = belum selesai.
- **Standar lulus:** tiap klaim di laporan punya bukti ber-reference-ID; tiap saran perbaikan punya cara verifikasi; tidak ada bukti tanpa sensor.

### Gerbang 4 — Rakit draf lengkap + audit A60 + tinjau manusia

1. Susun draf mengikuti **Format output** di bawah (5 bagian + metadata). Bahasa: Inggris untuk program internasional; simpan salinan Indonesia di log bila perlu.
2. **Audit A60:** A60 memeriksa — (a) tiap klaim bisa ditelusur ke bukti; (b) sensor PII lengkap; (c) skor CVSS + dampak disisipkan apa adanya; (d) langkah reproduksi bisa diulang. Satu cek gagal = draf DITOLAK, kembali ke gerbang yang relevan.
3. **Tinjau manusia 2–3 menit:** draf yang lolos A60 masuk dasbor internal; manusia meninjau pasangan R/R, sensor PII, dan skor sebelum diajukan ke Cipta.
4. **Persetujuan Cipta:** draf hanya dikirim setelah Cipta setuju. Untuk 0din: abstrak dulu (lihat `laporan-abstrak`), draf lengkap ini adalah tahap "detail lengkap/PoC" setelah jawaban scope.
5. **Standar lulus:** draf lolos A60 + tinjauan manusia + persetujuan Cipta. Tanpa ketiganya = BELUM BOLEH KIRIM.

## Alat

| Alat | Cara pakai |
|---|---|
| Template laporan | Format output di bawah — salin strukturnya persis per draf |
| `curl` | Tulis perintah reproduksi lengkap per langkah (Gerbang 2) |
| Skrip Python (`requests`) | Alternatif `curl` bila reproduksi butuh logika (loop, parsing JSON) — skrip minimal, tanpa kredensial asli |
| Penyimpanan bukti | File/database bukti HTTP di luar memori LLM, satu file per temuan, beri reference ID (mis. `FP-2026-11-23-001`); LLM hanya menerima reference ID |
| Sensor PII | Ganti token, kata sandi, email/nomor pribadi, dan data sensitif lain dengan `[REDACTED]` sebelum bukti disimpan/dibagikan |
| `~/workspace/catatan/log-bug-bounty.md` | Catat status draf (draf / audit / tinjau / setuju / terkirim / ditolak / dibayar) |

## Human-in-the-loop

- Draf VERIFIED masuk dasbor internal, **manusia meninjau 2–3 menit sebelum submit** — cek pasangan R/R, sensor PII, dan skor.
- **JANGAN PERNAH auto-submit** ke HackerOne/Bugcrowd atau platform lain. Tidak ada pengecualian.
- Setelah tinjauan manusia: kirim hanya bila **Cipta menyetujui** laporan itu. A69 melacak status pengiriman + pembayaran (sesuai `laporan-abstrak`).

## Format output

Draf laporan lengkap (satu file per temuan, nama `laporan-<program>-<temuan-singkat>.md` di folder kerja temuan; status dicatat di `~/workspace/catatan/log-bug-bounty.md`):

```markdown
# <Judul 1 baris — dampaknya jelas, mis. "IDOR memungkinkan akun gratis membaca data KTP pengguna lain">

## 1. Ringkasan
<2–4 kalimat: celah apa, di mana, dampaknya apa. Sisipkan kalimat dampak dari artikulasi-dampak-bisnis.>

## 2. Keparahan
- CVSS: <vektor lengkap> — Skor <angka> (<band>) [atau: CVSS tidak cocok — tier hadiah program: <tier>]
- Dampak bisnis: <kalimat dampak + paragraf pendukung dari artikulasi-dampak-bisnis>

## 3. Langkah Reproduksi
1. <Kondisi awal: akun/login apa>
   ```bash
   curl -X <METHOD> '<URL>' -H 'Authorization: Bearer $TOKEN_A' ...
   ```
   Hasil yang diharapkan: <...>
2. <Langkah berikutnya + perintah + hasil yang diharapkan>
   (skrip Python bila perlu:)
   ```python
   import requests
   # <langkah reproduksi minimal, tanpa kredensial asli>
   ```

## 4. Bukti
- <Reference ID + caption 1 baris + file screenshot/log yang disensor>
- <Tiap klaim di bagian 1–3 menunjuk ke satu bukti di sini>

## 5. Saran Perbaikan
- <Perbaikan spesifik per jenis celah + cara verifikasi perbaikan (uji ulang: ...)>
```

Status draf di `~/workspace/catatan/log-bug-bounty.md`:

```
- [tanggal] Draf: <nama temuan> | Program: <nama> | Reference ID bukti: <FP-...>
  - Gerbang 1 (bahan lengkap): LULUS/TOLAK — <bahan yang kurang bila tolak>
  - Gerbang 2 (reproduksi bisa diulang): LULUS/TOLAK — <diuji dari sesi bersih? ya/tidak>
  - Gerbang 3 (bukti tersensor + saran perbaikan): LULUS/TOLAK — <jumlah bukti + saran>
  - Gerbang 4 (audit A60 + tinjau manusia + Cipta): <status: draf / audit / tinjau / setuju / terkirim>
  - Verdict akhir: <draf selesai / dikembalikan + alasan>
```

## Batasan yang diketahui

- "Otomatis" di sini = perakitan draf dibantu template + penyisipan bukti programatik. Bukan pengiriman otomatis, bukan penulisan bukti oleh LLM, bukan skor otomatis — semua itu tetap manual + human-in-the-loop.
- Template ini untuk program web/API klasik (huntr dsb.) dan program bounty agen AI yang memakai format laporan serupa — sesuaikan bagian 2–3 dengan format yang diminta program (mis. 0din memakai abstrak dulu; Google memakai pengali kualitas — lihat `laporan-abstrak`).
- Bila program meminta format laporan yang berbeda (form portal, field khusus), isi field itu dari 5 bagian di atas — jangan tulis laporan kedua yang isinya berbeda dari draf ini.
