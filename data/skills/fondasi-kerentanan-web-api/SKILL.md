# Skill: Fondasi Kerentanan Web, API & Cloud — yang Wajib Dikuasai agar Lolos Triage

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 3).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan fondasi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata per jenis kerentanan yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai SEBELUM pengujian program web/API klasik (mis. huntr) dan setiap kali output AI (hipotesis, payload, atau laporan) harus dinilai benar/salah: tanpa fondasi ini, output AI mudah meleset, low, atau invalid dan ditolak triage. Dipakai juga sebagai bahan belajar A58 sebelum memakai `kopilot-analisis-kode` dan `rekonstruksi-iterasi-payload` — fondasi dulu, alat kemudian.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan fondasi ini pada tiap hipotesis dan pengujian |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar di skill ini |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Bukti dampak → skill `triase-duplikat` + `laporan-abstrak`.
- Cara mengarahkan kopilot AI membaca kode → skill `kopilot-analisis-kode`.
- Cara memvariasikan payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Catatan: XSS/SQLi klasik TIDAK relevan untuk bounty agen AI (program AI menilai hasil/outcome, bukan trik klasik) — skill ini untuk program web/API klasik (huntr) dan sebagai fondasi penilaian.

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
10. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "kelihatan rentan" tanpa pembuktian dampak = tidak maju ke triase.
11. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.

## Langkah + gerbang

### Gerbang 1 — Kuasai 5 jenis kerentanan inti

Pelajari dan hafalkan definisi, cara mengenali, dan cara membuktikan dampak tiap jenis di bawah. A58 wajib bisa menjelaskan kelimanya dengan contoh sebelum menguji program web klasik.

#### 1. IDOR (Insecure Direct Object Reference)

- **Definisi:** pengguna bisa mengakses objek milik orang lain hanya dengan mengubah pengenal di permintaan (mis. ID di URL/parameter) karena server tidak memeriksa kepemilikan.
- **Cara mengenali:** endpoint menerima ID objek (angka, UUID, nama file) dan mengembalikan data tanpa memeriksa apakah peminta berhak atas objek itu.
- **Cara membuktikan dampak:** dengan DUA akun sendiri (akun A dan akun B), minta objek milik akun B memakai sesi akun A. Bukti = data akun B terbaca/terubah oleh akun A. Satu akun saja TIDAK cukup membuktikan IDOR.
- **Standar lulus:** ada bukti dua akun + respons yang menunjukkan data akun lain terbaca. Tanpa akun kedua = belum terbukti.

#### 2. SSRF (Server-Side Request Forgery)

- **Definisi:** server bisa dipancing meminta URL yang dipilih penyerang, sehingga mencapai layanan internal yang seharusnya tidak bisa diakses dari luar.
- **Cara mengenali:** ada parameter yang berisi URL/alamat (mis. ambil gambar dari URL, webhook, pratinjau tautan) dan server yang mengambilnya.
- **Cara membuktikan dampak:** arahkan server ke alamat internal/canary milik sendiri dan tunjukkan server benar-benar menghubunginya (respons berisi isi layanan internal atau log canary tercatat). Sekadar "parameter URL diterima" bukan bukti.
- **Standar lulus:** ada bukti server menghubungi alamat yang diminta (isi respons internal atau hit canary). Tanpa bukti koneksi = belum terbukti.

#### 3. XSS (Cross-Site Scripting)

- **Definisi:** input penyerang ditampilkan ke pengguna lain tanpa penyaringan sehingga skrip penyerang jalan di browser korban.
- **Cara mengenali:** input (komentar, nama, profil) yang tampil kembali di halaman tanpa encoding.
- **Cara membuktikan dampak:** tunjukkan input yang dimasukkan di satu sesi/akun dieksekusi saat dilihat sesi/akun lain milik sendiri (mis. alert/pesan uji muncul di akun kedua). Self-XSS (hanya menyerang diri sendiri) umumnya TIDAK dibayar.
- **Standar lulus:** ada bukti eksekusi di akun/sesi kedua milik sendiri. Hanya di akun sendiri = belum cukup.

#### 4. Broken Authentication (autentikasi rusak)

- **Definisi:** celah pada proses login/sesi — mis. token sesi bisa ditebak, sesi tidak kedaluwarsa, reset kata sandi bisa dipakai untuk akun lain, atau login bisa dilewati.
- **Cara mengenali:** amati alur login, pembuatan token, dan apa yang terjadi pada token lama setelah logout/ganti kata sandi.
- **Cara membuktikan dampak:** tunjukkan akses ke akun sendiri TANPA kredensial yang semestinya (mis. token lama masih berlaku setelah logout, atau token akun lain bisa dipakai). Tunjukkan langkah reproduksi persis.
- **Standar lulus:** ada bukti akses tanpa kredensial semestinya + langkah reproduksi. Dugaan "token kelihatan lemah" tanpa pembuktian = belum terbukti.

#### 5. Salah konfigurasi API

- **Definisi:** API tidak memeriksa otorisasi/rate/batasan dengan benar — mis. endpoint admin bisa diakses pengguna biasa, data berlebih dikembalikan (excessive data exposure), atau batasan (limit/kuota) bisa dilewati.
- **Cara mengenali:** bandingkan apa yang dikembalikan API dengan apa yang ditampilkan UI; periksa endpoint yang tidak ada di UI; uji peran berbeda pada endpoint yang sama.
- **Cara membuktikan dampak:** tunjukkan data/aksi yang didapat lewat API dan tidak bisa didapat lewat UI normal dengan peran yang sama. Bukti = respons API persis + perbandingan peran.
- **Standar lulus:** ada bukti respons API + bukti peran yang sama tidak bisa mendapatkannya lewat UI. Tanpa perbandingan peran = belum terbukti.

### Gerbang 2 — Nilai output AI dengan fondasi ini

1. Setiap hipotesis atau payload dari AI dinilai: jenis kerentanannya apa (salah satu dari 5 di atas, atau bukan apa-apa)? Cara pembuktian dampaknya apa (sesuai standar lulus jenis itu)?
2. **Standar lulus:** tiap hipotesis yang maju punya label jenis kerentanan + rencana pembuktian dampak. Hipotesis tanpa label jenis dan tanpa rencana bukti = ditolak, jangan diuji.

### Gerbang 3 — Buktikan dampak, serahkan ke triase

1. Pengujian memakai `rekonstruksi-iterasi-payload`; bukti memakai standar lulus tiap jenis di Gerbang 1.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun tes sendiri | Wajib untuk membuktikan IDOR dan XSS (akun A vs akun B, keduanya milik sendiri). |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian. |
| LLM/agen AI | Membantu menjelaskan kode dan mengusulkan hipotesis — dinilai dengan Gerbang 2, bukan diterima mentah. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + jenis kerentanan + bukti dampak + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint/fitur]
Jenis kerentanan: [IDOR / SSRF / XSS / Broken Auth / Salah konfigurasi API]
Cara mengenali: [tanda yang ditemukan]
Pembuktian dampak: [langkah + bukti, sesuai standar lulus jenis itu]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Fondasi ini ringkasan dari riset, bukan kurikulum lengkap — tiap jenis kerentanan punya varian yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik di atas — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.
