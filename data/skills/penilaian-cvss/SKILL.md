# Skill: Penilaian CVSS v3.1 / v4.0 — Hitung Tingkat Keparahan Akurat dan Objektif

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md` butir 48; spesifikasi FIRST (CVSS v3.1 dan v4.0). Isi di bawah ini adalah ringkasan riset + spesifikasi, bukan pengalaman teruji sampai ada satu temuan yang skornya dicatat di log dan lolos triase. Label ini berlaku untuk semua bagian sampai ada kasus nyata yang dicatat.

## Pemicu

Dipakai setiap kali ada temuan berstatus **VERIFIED** dari `skeptic-false-positive-eliminator` yang butuh skor keparahan sebelum masuk triase — sebelum cek duplikat (`triase-duplikat`) dan sebelum draf laporan (`laporan-poc-otomatis`). Satu temuan = satu vektor + satu skor. Tanpa vektor dan skor = temuan belum siap triase.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Memilih nilai tiap metrik dari bukti, menghitung skor lewat kalkulator FIRST, menulis vektor + skor + alasan per metrik |
| Audit | **A60 Security Auditor** | Memeriksa tiap nilai metrik terhadap bukti; menolak skor yang tidak bisa ditelusur ke bukti |
| Pemimpin | **Muse** | Memutuskan temuan maju ke triase atau dikembalikan untuk bukti tambahan |

## Sudah tercakup (jangan diduplikat)

- **Skor per tier hadiah program** ada di `triase-duplikat` — skill ini **bukan** penggantinya. Tier hadiah (mis. 0din Low/Medium/High/Severe) tetap diputuskan di `triase-duplikat` SETELAH skor CVSS dihitung di sini.
- **"Skor CVSS" disebut** di `skeptic-false-positive-eliminator` (Gerbang 4) dan `mcp-shodan` (Gerbang 4, membaca skor CVSS dari data CVE yang sudah ada) — keduanya **tidak memberi cara** memilih nilai metrik, menyusun vektor, atau membedakan v3.1 dan v4.0. Skill ini adalah **cara menghitungnya langkah demi langkah**.
- **Dampak bisnis** (apa yang dicuri/diubah, berapa banyak) ditulis di `artikulasi-dampak-bisnis` — skill ini hanya mengubah dampak yang SUDAH TERBUKTI itu menjadi metrik C/I/A. Jangan menilai dampak di sini; pakai hasil `artikulasi-dampak-bisnis`.
- Alur sesudah skill ini: skor CVSS → `artikulasi-dampak-bisnis` (bila belum ditulis) → `triase-duplikat` (cek duplikat + tier hadiah) → draf laporan (`laporan-poc-otomatis`) → tinjau manusia → persetujuan Cipta → kirim.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan dinilai, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.**
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya — hanya dampak yang TERBUKTI di sesi bersih yang boleh masuk metrik C/I/A. Triase yang menentukan tier hadiah, bukan skor ini.
8. **Skor dihitung kalkulator, bukan dikarang.** Skor akhir HARUS berasal dari kalkulator resmi FIRST (lihat Alat). Jangan pernah menulis angka skor dari perkiraan atau hafalan. Vektor + skor + tautan kalkulator dicatat bersama.
9. **Satu nilai metrik = satu bukti.** Tiap nilai metrik harus bisa ditelusur ke pasangan Request/Response atau bukti lain yang tersimpan (reference ID dari `skeptic-false-positive-eliminator`). Nilai tanpa bukti = nilai itu TIDAK BOLEH dipakai; pakai nilai yang lebih rendah yang terbukti, dan catat kekurangannya.
10. **CVSS tidak cocok untuk semua program.** Untuk bounty agen AI (Muse, OpenAI Safety, Google AI VRP, 0din) yang menilai HASIL/outcome (aksi nyata/data keluar), CVSS sering tidak pas — bila begitu, tulis "CVSS tidak cocok — pakai tier hadiah program" dan serahkan ke `triase-duplikat`. Jangan memaksakan skor CVSS ke temuan agen AI.
11. **Pembuat temuan tidak boleh meloloskan skornya sendiri** — A60 yang mengaudit.

## Langkah + gerbang

### Gerbang 1 — Pilih versi: v3.1 atau v4.0

- Tanya dulu: **versi apa yang dipakai program?** Bila program menyebut versi tertentu (mis. HackerOne memakai v3.1), pakai versi itu. Bila program tidak menyebut, **default v4.0** (versi terbaru FIRST, terbit 1 Nov 2023) dan tulis versinya eksplisit di laporan.
- Jangan campur: satu temuan = satu versi. Bila triager meminta versi lain, hitung ulang dari Gerbang 2 dengan metrik versi itu — jangan konversi angka skor secara kasar.
- **Standar lulus:** versi tertulis (v3.1 atau v4.0) + alasan pemilihannya, sebelum satu metrik pun dinilai.

### Gerbang 2 — Nilai metrik exploitability dari bukti (bukan dari dugaan)

Isi tiap metrik hanya dari apa yang TERBUKTI saat reproduksi bersih:

**CVSS v3.1 — 8 metrik dasar (Base):**

| Metrik | Nilai | Artinya (ringkas) |
|---|---|---|
| Attack Vector (AV) | Network (N) / Adjacent (A) / Local (L) / Physical (P) | Seberapa jauh penyerang bisa berada. Web/API lewat internet = N |
| Attack Complexity (AC) | Low (L) / High (H) | H hanya bila penyerang harus mengalahkan pengamanan bawaan atau kondisi khusus di luar kendalinya |
| Privileges Required (PR) | None (N) / Low (L) / High (H) | Akses apa yang harus dimiliki dulu. Akun pengguna biasa = L; tanpa login = N |
| User Interaction (UI) | None (N) / Required (R) | Apakah korban harus bertindak (klik tautan, buka halaman)? |
| Scope (S) | Unchanged (U) / Changed (C) | C bila dampak melewati batas otoritas komponen rentan (mis. dari aplikasi ke data pengguna lain / sistem lain) |
| Confidentiality (C) / Integrity (I) / Availability (A) | None (N) / Low (L) / High (H) | Dampak pada kerahasiaan / keutuhan / ketersediaan — lihat Gerbang 3 |

**CVSS v4.0 — 11 metrik dasar (Base), semua wajib:**

| Metrik | Nilai | Bedanya dari v3.1 |
|---|---|---|
| Attack Vector (AV) | Network (N) / Adjacent (A) / Local (L) / Physical (P) | Sama |
| Attack Complexity (AC) | Low (L) / High (H) | Di v4.0 HANYA soal mengalahkan pengamanan bawaan — kondisi situasional pindah ke AT |
| Attack Requirements (AT) | None (N) / Present (P) | BARU. P bila sukses bergantung kondisi di luar kendali penyerang (race condition, posisi man-in-the-middle, konfigurasi non-default). Kebanyakan IDOR/injeksi/XSS = N |
| Privileges Required (PR) | None (N) / Low (L) / High (H) | Akun pengguna biasa = L. Reflected XSS dan CSRF = N (korban yang bekerja, bukan penyerang) |
| User Interaction (UI) | None (N) / Passive (P) / Active (A) | BARU tiga nilai. P = korban cukup memakai situs seperti biasa (lihat halaman berisi payload tersimpan, CSRF). A = korban harus bertindak sengaja (klik tautan crafted untuk reflected XSS) |
| Vulnerable System C/I/A (VC / VI / VA) | None (N) / Low (L) / High (H) | Dampak pada sistem yang berisi celah |
| Subsequent System C/I/A (SC / SI / SA) | None (N) / Low (L) / High (H) | Dampak pada sistem LAIN di luar sistem rentan — PENGGANTI Scope v3.1 |

- Kaidah umum: **bila ragu antara dua nilai, pilih yang lebih rendah** dan catat keraguannya. Skor yang terlalu rendah bisa dikoreksi triager ke atas; skor yang dibesarkan merusak kredibilitas.
- **Standar lulus:** tiap metrik exploitability punya nilai + satu kalimat alasan yang menunjuk ke bukti (reference ID). Metrik tanpa alasan bukti = gerbang gagal.

### Gerbang 3 — Nilai metrik dampak (C/I/A) hanya dari dampak yang terbukti

- **High (H)** hanya bila terbukti: kebocoran TOTAL data sensitif, atau penyerang bisa mengubah data apa pun / data yang akibatnya langsung serius, atau layanan mati total.
- **Low (L)** bila terbukti ada dampak tapi terbatas: sebagian data bocor, perubahan terbatas, atau gangguan sebagian.
- **None (N)** bila tidak ada dampak pada aspek itu — jangan isi L "untuk jaga-jaga".
- Di v4.0, pisahkan: dampak pada sistem rentan (VC/VI/VA) vs dampak pada sistem lain (SC/SI/SA). Dampak di luar sistem rentan HARUS masuk SC/SI/SA, bukan digabung ke VC/VI/VA.
- **Larangan:** jangan menilai dampak dari "yang MUNGKIN terjadi" (mis. "bisa saja ada 500.000 record") — hanya dari yang terbukti di sesi bersih. Angka populasi potensial ditulis di `artikulasi-dampak-bisnis` sebagai ESTIMASI berlabel, bukan sebagai dasar metrik C/I/A.
- **Standar lulus:** tiap metrik C/I/A punya nilai + bukti dampaknya. Bila dampak belum terbukti, kembali ke pengujian — jangan lanjut ke Gerbang 4.

### Gerbang 4 — Hitung skor di kalkulator FIRST, tulis vektor + band

1. Masukkan semua nilai metrik ke kalkulator resmi FIRST:
   - v3.1: `https://www.first.org/cvss/calculator/3.1`
   - v4.0: `https://www.first.org/cvss/calculator/4.0`
2. Salin **vektor lengkap** persis dari kalkulator, contoh:
   - v3.1: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
   - v4.0: `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`
3. Catat **skor + band keparahan** (sama di v3.1 dan v4.0): None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 · Critical 9.0–10.0.
4. Di v4.0, skor dari metrik dasar saja disebut **CVSS-B** (Base). Metrik Threat (Exploit Maturity: E) dan Environmental HANYA dipakai bila program memintanya — default jangan ditambah, dan bila ditambah tulis label lengkapnya (mis. CVSS-BTE).
5. **Uji kewarasan (sanity check):** bandingkan skor dengan contoh sejenis yang dikenal (mis. IDOR baca data akun lain biasanya Medium–High, bukan Critical; RCE tanpa autentikasi biasanya Critical). Bila skor jauh dari kewajaran, periksa lagi tiap metrik — hampir selalu ada satu metrik yang salah nilai.
6. **Standar lulus:** vektor + skor + band + alasan per metrik tercatat di log; A60 menyetujui tiap nilai. Skor tanpa vektor = tidak sah.

## Alat

| Alat | Cara pakai |
|---|---|
| Kalkulator CVSS FIRST v3.1 | `https://www.first.org/cvss/calculator/3.1` — satu-satunya sumber angka skor v3.1 |
| Kalkulator CVSS FIRST v4.0 | `https://www.first.org/cvss/calculator/4.0` — satu-satunya sumber angka skor v4.0 |
| Spesifikasi FIRST | `https://www.first.org/cvss/` — rujukan bila ragu arti satu metrik; spesifikasi yang menang atas ingatan |
| Bukti sesi bersih | Pasangan Request/Response + reference ID dari `skeptic-false-positive-eliminator` — dasar tiap nilai metrik |
| `~/workspace/catatan/log-bug-bounty.md` | Catat vektor + skor + alasan per metrik + verdict A60 |

## Human-in-the-loop

- A60 mengaudit tiap nilai metrik sebelum skor dipakai di draf laporan. Bila A60 tidak setuju satu nilai, skor dihitung ulang — bukan dinegosiasi.
- Skor CVSS adalah **usulan untuk triager**, bukan keputusan hadiah. Tier hadiah tetap diputuskan triager/program (`triase-duplikat`).

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per temuan) dengan format:

```
- [tanggal] Temuan: <nama singkat> | Program: <nama> | Reference ID bukti: <FP-...>
  - Versi CVSS: <3.1 / 4.0> — <alasan pilih versi>
  - Vektor: <vektor lengkap dari kalkulator>
  - Skor: <angka> (<band: None/Low/Medium/High/Critical>) — <CVSS-B bila v4.0 dasar saja>
  - Alasan per metrik:
    - AV:<nilai> — <alasan + bukti>
    - AC:<nilai> — <alasan + bukti>
    - (AT:<nilai> — <alasan + bukti>) [v4.0]
    - PR:<nilai> — <alasan + bukti>
    - UI:<nilai> — <alasan + bukti>
    - (S:<nilai> — <alasan + bukti>) [v3.1] / (VC/VI/VA + SC/SI/SA — <alasan + bukti>) [v4.0]
  - Catatan keraguan: <metrik yang dipilih nilai rendah karena ragu + apa yang kurang>
  - Audit A60: SETUJU / TOLAK — <alasan>
  - Atau: CVSS tidak cocok — <alasan> → pakai tier hadiah program (triase-duplikat)
```

## Batasan yang diketahui

- Skill ini hanya menghitung skor **Base** (CVSS-B di v4.0). Metrik Threat/Environmental/Supplemental tidak dibahas rinci — bila program memintanya, baca spesifikasi FIRST dan catat sebagai tambahan, bukan sebagai pengganti skor dasar.
- CVSS mengukur keparahan TEKNIS, bukan nilai bisnis. Skor Critical pada sistem yang tidak penting tetap kalah penting dari skor Medium pada sistem inti — itulah gunanya `artikulasi-dampak-bisnis` dan tier hadiah program.
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome — skill ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI kecuali program itu sendiri meminta skor CVSS.
