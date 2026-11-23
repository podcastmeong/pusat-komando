# Skill: Access Control Differential Analyst — Analisis BOLA/IDOR dengan Perbandingan Respons Lintas Akun Uji

> Dibangun dari riset "Arsitektur Multi-Agent Pemburu Bug Bounty Anti False Positive" (23 Nov 2026, `~/workspace/catatan/referensi-arsitektur-multi-agent-bounty-2026-11-23.md`, bagian 3B dan bagian 2 — Baseline Check, State Verification).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat menguji endpoint API yang punya pengenal objek (id, uuid, account_number, order_id) untuk membuktikan ada/tidaknya BOLA/IDOR — dengan membandingkan respons tiga kondisi (pemilik sah, anonim, lintas akun) dan memverifikasi perubahan status nyata di server. Dipakai setelah recon mengindeksasi endpoint (skill `pemetaan-permukaan-serangan`); jangan dipakai pada endpoint tanpa pengenal objek, dan jangan dipakai untuk menebak ID.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan baseline 3 kondisi + evaluasi diferensial |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai apakah field respons benar berisi data privat |
| Pengerjaan | **A64 Web Application Tester** | Menguji endpoint aplikasi web dengan metode ini |
| Pengerjaan | **A66 API Security Tester** | Menguji endpoint API dengan metode ini |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi IDOR + pembuktian dua akun secara umum → skill `fondasi-kerentanan-web-api` (Gerbang 1, bagian IDOR). Skill ini BUKAN definisi IDOR: skill ini adalah **metodologi diferensial 3 kondisi (A/B/C) + state verification**, yang tidak ada di skill fondasi.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Indeksasi endpoint + parameter valid → skill `pemetaan-permukaan-serangan`.
- Penyusunan draf laporan triase-ready → skill `triase-duplikat` + `laporan-abstrak`.

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
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Jangan tebak ID sensitif.** Hanya uji objek milik dua akun uji sendiri yang sudah diketahui ID-nya dari recon/akun sendiri; jangan brute-force atau menebak ID orang lain.
12. **200 OK bukan bukti.** Respons sukses tanpa perubahan status nyata di server = bukan temuan.

## Langkah + gerbang

### Gerbang 1 — Pilih endpoint dari indeks recon saja

1. Ambil endpoint HANYA dari indeksasi recon (skill `pemetaan-permukaan-serangan`): endpoint API yang menerima pengenal objek — `id`, `uuid`, `account_number`, `order_id`, atau sejenisnya — di URL, parameter, atau body.
2. Catat untuk tiap endpoint: metode HTTP, nama parameter pengenal objek, dan objek milik akun uji mana yang akan dipakai (Object_A milik User_A, Object_B milik User_B).
3. **Standar lulus:** endpoint tercatat di indeks recon + pengenal objeknya jelas + kedua objek uji milik akun sendiri. Endpoint yang dikarang, ditebak, atau di luar indeks = STOP, jangan diuji.

### Gerbang 2 — Baseline 3 kondisi (A / B / C)

Jalankan ketiga kondisi pada endpoint dan objek yang SAMA (Object_A), simpan raw request/response tiap kondisi:

| Kondisi | Permintaan | Yang diharapkan bila kontrol akses benar |
|---|---|---|
| **A — pemilik sah** | User_A (token akun A) → Object_A | Data Object_A lengkap — ini pembanding "yang seharusnya terlihat" |
| **B — anonim** | Tanpa token → Object_A | 401/403/404/objek kosong, atau data yang memang publik |
| **C — lintas akun** | User_B (token akun B) → Object_A | 401/403/404/objek kosong (sama seperti B bila objek itu privat) |

1. Jalankan A dulu untuk memastikan objek ada dan respons pemilik sah seperti apa.
2. Jalankan B untuk memastikan mana bagian respons yang memang publik.
3. Jalankan C — inilah uji intinya.
4. **Standar lulus:** ketiga kondisi dijalankan pada objek yang sama, dengan raw request/response tersimpan. Satu kondisi hilang = baseline tidak lengkap, jangan simpulkan apa-apa.

### Gerbang 3 — Evaluasi diferensial

Bandingkan respons C dengan respons A dan B, field per field:

- **Kandidat Temuan:** C mengembalikan data spesifik User_A yang TIDAK muncul di B — mis. email, transaksi, pengaturan internal, atau isi objek privat milik User_A. Buktikan field respons berisi data privat, bukan sekadar status 200 atau struktur respons yang sama.
- **Aman:** C mengembalikan 401/403/404/objek kosong, atau hanya data yang sama persis dengan yang sudah publik di B.
- **Bukan temuan:** C mengembalikan 200 tapi isinya sama dengan B (data memang publik); C mengembalikan pesan error generik tanpa data; C mengembalikan data milik User_B sendiri (bukan User_A).
- **Standar lulus:** keputusan Kandidat Temuan vs Aman ditulis per field yang berbeda, dengan nama field + isi yang membuktikan data privat (disensor saat dicatat: `[REDACTED]`). Keputusan tanpa menyebut field = belum terbukti.

### Gerbang 4 — State Verification (untuk uji tulis/ubah)

Untuk endpoint yang mengubah data (PUT/PATCH/POST/DELETE), pesan sukses saja TIDAK cukup:

1. Minta perubahan sebagai User_B terhadap Object_A (mis. ubah nama/profil/pengaturan milik User_A).
2. Baca ulang Object_A sebagai User_A (sesi bersih) dan periksa apakah perubahan itu NYATA terjadi di server.
3. **Perubahan nyata = Kandidat Temuan** (lanjut ke Gerbang 5). **Pesan sukses tapi data tidak berubah (silent drop) = Aman** — server hanya mengembalikan pesan sukses palsu; catat sebagai bukan temuan, jangan laporkan.
4. Bila perubahan ternyata terjadi, kembalikan data Object_A ke keadaan semula dari akun pemiliknya (jangan tinggalkan data uji berubah).
5. **Standar lulus:** ada bukti baca-ulang sebagai User_A yang menunjukkan status sebelum vs sesudah. Tanpa baca-ulang = belum terbukti, jangan klaim temuan tulis.

### Gerbang 5 — Serahkan ke skeptic gate

1. Kandidat Temuan yang lolos Gerbang 3 (dan Gerbang 4 bila uji tulis) diserahkan ke skill `skeptic-false-positive-eliminator`: uji ulang dengan sesi HTTP baru (fresh tokens), pastikan reproduksibel konsisten.
2. Gagal direproduksi = TOLAK, catat di log sebagai bukan temuan.
3. Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim.
4. **Standar lulus:** keputusan akhir tercatat di log dengan pasangan bukti request/response asli (token dan PII disensor).

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (User_A dan User_B) | Satu-satunya akun yang dipakai; A pemilik objek, B penguji lintas akun. Keduanya milik sendiri. |
| Canary palsu | Data penanda milik sendiri untuk membuktikan field respons berisi data privat, bukan data orang lain. |
| Indeks recon (skill `pemetaan-permukaan-serangan`) | Satu-satunya sumber endpoint yang boleh diuji — endpoint di luar indeks tidak diuji. |
| Sesi HTTP bersih (fresh tokens) | Untuk uji ulang reproduksibilitas di Gerbang 5. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap endpoint: baseline A/B/C, hasil diferensial, verifikasi state, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Endpoint: [metode + URL + parameter pengenal objek]
Baseline A (pemilik sah User_A → Object_A): [status + ringkasan field yang terlihat]
Baseline B (anonim tanpa token): [status + ringkasan field yang terlihat]
Baseline C (lintas akun User_B → Object_A): [status + ringkasan field yang terlihat]
Hasil diferensial: [Kandidat Temuan / Aman + field yang membuktikan, PII disensor]
Verifikasi state: [tidak berlaku (uji baca) / perubahan NYATA / silent drop + bukti baca-ulang]
Keputusan: [maju ke skeptic gate / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Metode ini hanya menguji kontrol akses berbasis kepemilikan objek (BOLA/IDOR); tidak menguji kerentanan lain (SSRF, XSS, injeksi) — pakai skill fondasi + skill terkait untuk jenis lain.
- Baseline B hanya membedakan "publik vs privat" sejauh respons anonim bisa diamati; bila program menyajikan data berbeda per wilayah/peran, catat konteksnya di log.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
