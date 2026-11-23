# Skill: Gerbang Tujuh Pertanyaan Triase — Validasi Temuan Sebelum Laporan Dibuat

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md` Kategori 4 butir 1 (bug-bounty-triage / triage-validation, 7-Question Gate). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu kandidat yang lolos gerbang ini dan dicatat di log.

## Pemicu (Trigger & Scope)

Dipakai setiap kali ada kandidat temuan yang sudah punya bukti awal (dari `verifikasi-poc-aman`) dan hendak maju ke verifikasi adversarial — **sebelum** `skeptic-false-positive-eliminator`, sebelum cek duplikat (`triase-duplikat`), dan sebelum draf laporan apa pun dibuat. Satu kandidat = satu kali lewat 7 pertanyaan di bawah. Tidak ada jalan pintas, tidak ada "kelihatannya valid".

Skill ini adalah **gerbang pra-triase**: tugasnya memastikan kandidat layak dinilai sama sekali, bukan menilai seberapa besar hadiahnya (itu tugas `triase-duplikat`) dan bukan membantah temuan secara adversarial (itu tugas `skeptic-false-positive-eliminator`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menjalankan 7 pertanyaan, memutuskan LULUS / TOLAK beserta alasan |
| Audit | **A60 Security Auditor** | Memeriksa verdict gerbang; A60 tidak meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan kandidat maju ke skeptic atau dibuang |

## Sudah tercakup (jangan diduplikat)

- **Cek duplikat + skor tier hadiah** ada di `triase-duplikat` — skill ini bukan itu; skill ini berjalan SEBELUM triase-duplikat.
- **Verifikasi adversarial 4 gerbang** (reproduksibilitas bersih, filter non-security, dampak bisnis, output terstruktur) ada di `skeptic-false-positive-eliminator` — skill ini berjalan SEBELUM skeptic, dan tidak mengulang 4 gerbang itu; yang dicek di sini adalah kelayakan dasar kandidat (in-scope, observasi vs asumsi, bukan noise).
- **Parsing aturan scope program** ada di `parsing-scope-program` dan **penegakan scope sebelum eksekusi** ada di `scope-and-safety-guardian` — skill ini MEMAKAI catatan scope dari keduanya untuk menjawab Pertanyaan 1, bukan membuat catatan scope baru.
- **Teknik bukti aman per jenis celah** ada di `verifikasi-poc-aman` — skill ini memakai bukti itu, bukan mengulang cara membuktikannya.
- Alur sesudah skill ini: LULUS → `skeptic-false-positive-eliminator` (4 gerbang) → `triase-duplikat` (cek duplikat + skor) → draf laporan (`laporan-poc-otomatis`) → tinjau manusia → persetujuan Cipta → kirim. TOLAK → catat alasan di log, kembali ke riset/varian.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = TOLAK, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.** LULUS di gerbang ini bukan izin kirim — izin kirim tetap dari Cipta.
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian aman dan read-only; bukti baca, callback canary, `document.domain` — tanpa perintah yang menulis/menghapus di server.
8. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.
9. **Sensor PII/token/kredensial di semua bukti ([REDACTED]) sebelum laporan disusun.** Bukti tanpa sensor = belum boleh maju.
10. **Jangan pernah mengirim laporan otomatis ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia dulu; pengiriman selalu manual + disetujui Cipta.
11. **Satu pertanyaan gagal = TOLAK.** Tidak ada "lolos sebagian". Bedakan jenis penolakan (lihat Gerbang 8): TOLAK PERMANEN (buang) vs TOLAK SEMENTARA (boleh kembali sebagai kandidat baru dengan bukti baru, bukan dengan mengubah verdict).
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Methodology — 7 pertanyaan (langkah + gerbang)

Jawab ketujuh pertanyaan secara berurutan, masing-masing dengan bukti tertulis. Tulis jawaban di tabel kandidat (lihat Format output) sebelum memutuskan.

### Pertanyaan 1 — Apakah program dan asetnya benar-benar in-scope?

- Cek catatan scope program dari `parsing-scope-program`: apakah programnya ada di daftar resmi tim, dan apakah aset/endpoint/fitur yang diuji ada di `in_scope_assets` (bukan di `out_of_scope_assets`)?
- Bila catatan scope belum ada atau sudah basi (aturan program berubah) = jawaban TIDAK — kembali ke `parsing-scope-program` dulu, jangan lanjut.
- **Standar lulus:** nama program + aset tertulis dengan tautan ke sumber resmi program. **Gagal = TOLAK PERMANEN** untuk kandidat ini (jangan uji target out-of-scope dengan harapan "mungkin diterima").

### Pertanyaan 2 — Apakah temuan ini OBSERVASI langsung, bukan asumsi?

- Pisahkan setiap klaim kandidat ke tiga label, dan tulis labelnya:
  - **OBSERVASI** — sesuatu yang benar-benar terlihat di respons/log server (mis. "respons mengembalikan field `email` akun B, status 200").
  - **ASUMSI** — sesuatu yang ditebak tanpa bukti langsung (mis. "server ini pasti memakai database X", "pasti ada 500.000 record").
  - **INFERENSI** — kesimpulan dari observasi (mis. "karena field akun B kembali, berarti tidak ada pemeriksaan kepemilikan") — inferensi BOLEH, asal observasi pendukungnya tertulis.
- Aturan: **inti temuan (apa celahnya) HARUS berupa OBSERVASI**, bukan asumsi. Klaim asumsi boleh ada hanya sebagai konteks, dan WAJIB berlabel ASUMSI — tidak boleh ditulis seolah-olah fakta.
- **Standar lulus:** inti temuan punya minimal satu OBSERVASI dengan reference ID bukti; semua klaim berlabel. **Gagal = TOLAK SEMENTARA** — kembali ke pengujian dan cari observasi yang membuktikan inti temuan.

### Pertanyaan 3 — Apakah temuan teramati dari sesi bersih (bukan artefak sesi penemuan)?

- Ulangi observasi inti dari sesi HTTP baru + token segar, minimal 1 kali (pengulangan penuh 2 kali menjadi tugas `skeptic-false-positive-eliminator` Gerbang 1; di sini cukup satu pengulangan bersih untuk memastikan bukan artefak).
- Lakukan **Baseline Check** bila relevan: minta objek/data yang sama tanpa token (anonim). Bila respons anonim sama dengan respons memakai token, data itu publik — bukan kebocoran.
- **Standar lulus:** observasi inti terulang dari sesi bersih dan baseline anonim terbukti berbeda. **Gagal = TOLAK SEMENTARA** — kembali ke pengujian.

### Pertanyaan 4 — Apakah temuan ini BUKAN noise yang ditolak program (low-hanging noise)?

Tolak langsung bila temuan termasuk salah satu kategori noise di bawah — tanpa lanjut ke pertanyaan 5:

| Noise | Kenapa ditolak |
|---|---|
| Missing SPF / DMARC / DKIM tanpa dampak | Tidak ada skenario eksploitasi nyata yang ditunjukkan; sebagian besar program mengecualikannya eksplisit |
| Clickjacking pada halaman non-sensitif | Tidak ada aksi sensitif yang bisa dibajak (tanpa tombol/aksi berdampak di halaman itu) |
| Missing security headers tanpa skenario eksploitasi nyata | Header hilang saja bukan kerentanan tanpa bukti dampak |
| Info versi server/framework tanpa kerentanan yang menyertainya | Versi saja bukan bukti bisa dieksploitasi |
| Self-XSS | Korban harus menyerang dirinya sendiri |
| Kebocoran data yang memang publik | Termasuk yang lolos dari Baseline Check pertanyaan 3 |
| Respons rate-limit | Bukan kerentanan |
| Halaman error generik | Bukan kebocoran data sensitif |

- **Standar lulus:** temuan bukan salah satu kategori di atas, dan ada skenario eksploitasi nyata yang bisa ditulis dalam 2–3 kalimat. **Gagal = TOLAK PERMANEN** — jangan buang waktu membuktikan noise.

### Pertanyaan 5 — Apakah ada trust boundary yang dilanggar?

- Jawab konkret: batas apa yang dilanggar — antara siapa yang boleh dan siapa yang tidak boleh mengakses/mengubah data atau aksi itu?
- Bila tidak ada trust boundary yang dilanggar (mis. pengguna hanya mengakses datanya sendiri dengan cara yang tidak biasa) = bukan kerentanan keamanan.
- **Standar lulus:** trust boundary tertulis dalam satu kalimat + pihak tak berwenang yang melewatinya disebut. **Gagal = TOLAK PERMANEN.**

### Pertanyaan 6 — Apakah dampaknya nyata dan bisa dijelaskan tanpa mengarang?

- Jawab dengan konkret (bukan "mungkin bisa"): apa yang bisa dicuri / diubah / diakses tanpa sah, oleh siapa, dan apa kerugiannya bagi pemilik program? (Penulisan dampak yang terukur menjadi tugas `artikulasi-dampak-bisnis` sesudah gerbang ini; di sini cukup jawaban singkat yang jujur.)
- Pisahkan TERBUKTI (diukur dari pengujian sendiri) dan ESTIMASI (angka populasi/kerugian — berlabel, bukan fakta).
- **Standar lulus:** ada dampak nyata yang bisa dijelaskan dalam 2–3 kalimat tanpa mengarang. **Gagal = TOLAK SEMENTARA** — kembali ke pengujian atau turunkan klaim dampak ke yang terbukti.

### Pertanyaan 7 — Apakah setiap klaim punya bukti ber-reference-ID yang sudah tersensor?

- Tiap klaim OBSERVASI dan INFERENSI harus menunjuk ke pasangan Request/Response atau bukti lain yang tersimpan dengan reference ID (mis. `FP-2026-11-24-001`).
- Bukti sudah disensor: token, kata sandi, email/nomor pribadi, dan data sensitif lain diganti `[REDACTED]` sebelum disimpan/dibagikan.
- **Standar lulus:** tidak ada klaim tanpa bukti; tidak ada bukti tanpa sensor. **Gagal = TOLAK SEMENTARA** — lengkapi/sensor bukti, lalu ajukan lagi sebagai kandidat baru.

### Gerbang 8 — Verdict

- **LULUS** — ketujuh pertanyaan terjawab YA → kandidat maju ke `skeptic-false-positive-eliminator`.
- **TOLAK PERMANEN** — gagal di Pertanyaan 1, 4, atau 5 → kandidat dibuang; catat alasan di log; jangan ajukan lagi dengan bukti yang sama.
- **TOLAK SEMENTARA** — gagal di Pertanyaan 2, 3, 6, atau 7 → kandidat boleh kembali sebagai kandidat BARU dengan bukti baru; verdict lama tidak diubah.

## Validation Gate (verifikasi deterministik baseline vs exploit)

- Baseline: respons anonim / tanpa token (Pertanyaan 3) HARUS berbeda dari respons exploit; bila sama, temuan bukan kebocoran.
- Exploit: observasi inti HARUS terulang dari sesi bersih + token segar (Pertanyaan 3); satu kali berhasil dari sesi penemuan saja tidak cukup.
- Verdict LULUS hanya sah bila perbandingan baseline-vs-exploit tertulis di tabel kandidat dengan reference ID bukti keduanya.

## Alat

| Alat | Cara pakai |
|---|---|
| Catatan scope program (`parsing-scope-program`) | Sumber jawaban Pertanyaan 1 — daftar `in_scope_assets` / `out_of_scope_assets` + tautan resmi |
| Sesi HTTP bersih (`curl` / skrip Python, sesi baru + token segar) | Pengulangan observasi inti (Pertanyaan 3) + Baseline Check anonim |
| Penyimpanan bukti (file per kandidat, reference ID mis. `FP-2026-11-24-001`) | Bukti HTTP di luar memori LLM; LLM hanya menerima reference ID |
| Sensor PII | Ganti token, kata sandi, email/nomor pribadi, dan data sensitif lain dengan `[REDACTED]` sebelum bukti disimpan/dibagikan |
| `~/workspace/catatan/log-bug-bounty.md` | Catat verdict tiap kandidat (lihat Format output) |

## Human-in-the-loop

- A60 mengaudit verdict gerbang sebelum kandidat maju ke skeptic. Bila A60 tidak setuju satu jawaban, kandidat dikembalikan — bukan dinegosiasi.
- LULUS di gerbang ini bukan izin kirim laporan. Draf VERIFIED tetap ditinjau manusia 2–3 menit dan hanya dikirim bila **Cipta menyetujui**.

## Format output

Catat setiap kandidat di `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Kandidat: <nama temuan singkat> | Program: <nama> | Reference ID bukti: <FP-...>
  - Q1 (in-scope): YA/TIDAK — <program + aset + sumber resmi>
  - Q2 (observasi vs asumsi): YA/TIDAK — <inti temuan = OBSERVASI + reference ID; daftar klaim ASUMSI bila ada>
  - Q3 (sesi bersih + baseline): YA/TIDAK — <pengulangan bersih + hasil baseline anonim>
  - Q4 (bukan noise): YA/TIDAK — <kategori noise bila ditolak / skenario eksploitasi 2–3 kalimat>
  - Q5 (trust boundary): YA/TIDAK — <batas yang dilanggar + pihak tak berwenang>
  - Q6 (dampak nyata): YA/TIDAK — <apa yang dicuri/diubah + kerugian, TERBUKTI vs ESTIMASI>
  - Q7 (klaim berbukti + tersensor): YA/TIDAK — <jumlah klaim / jumlah bukti ber-reference-ID>
  - Verdict akhir: LULUS / TOLAK PERMANEN / TOLAK SEMENTARA — <alasan satu kalimat>
```

Hanya kandidat berstatus **LULUS** yang diteruskan ke A60 (`skeptic-false-positive-eliminator`). Kandidat TOLAK berhenti di sini — dicatat, tidak dihapus dari log, tidak dikirim ke mana pun.

## Batasan yang diketahui

- Gerbang ini menilai kelayakan dasar, bukan keparahan — skor CVSS (`penilaian-cvss`) dan tier hadiah (`triase-duplikat`) tetap diputuskan sesudahnya.
- Daftar noise di Pertanyaan 4 adalah daftar umum program web/API klasik; program tertentu bisa mengecualikan lebih banyak (cek aturan program di catatan scope — bila program menyebut pengecualian lain, pengecualian itu yang menang).
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar) — terapkan 7 pertanyaan yang sama pada outcome-nya, tapi jangan paksakan kategori noise web klasik bila outcome-nya berupa aksi agen.
