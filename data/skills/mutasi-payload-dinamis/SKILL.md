# Skill: Mutasi Payload Dinamis — Adaptasi Payload dari Respons WAF

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 7 butir 46 — Dynamic Payload Mutation).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu mutasi yang lolos WAF dan terbukti di log.

## Pemicu (kapan dipakai)

Dipakai saat sebuah payload dasar DIBLOKIR atau DINETRALISIR oleh WAF/filter (respons 403, 406, 419, payload terpantul tapi tidak mengeksekusi, atau karakter kunci dihapus/di-encode) dan hipotesis celahnya masih kuat — untuk mengubah payload secara adaptif berdasarkan APA yang diblokir, bukan menebak variasi acak. Dipakai sesudah `rekonstruksi-iterasi-payload` (variasi satu dimensi per putaran) — skill ini menambah loop adaptif berbasis respons WAF di atasnya. Hanya untuk program web/API klasik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Membaca respons WAF, memilih keluarga mutasi, menjalankan putaran adaptif, mencatat log |
| Audit | **A60 Security Auditor** | Memeriksa bukti mutasi yang lolos sebelum jadi draf laporan |
| Pemimpin | **Muse** | Memutuskan mutasi mana yang dikembangkan jadi temuan dan kapan berhenti |

## Sudah tercakup (jangan diduplikat)

- Variasi payload sistematis satu dimensi per putaran + log nilai → respons → verdict → `rekonstruksi-iterasi-payload` — skill ini memakai kerangka log itu, dan menambah PEMILIHAN mutasi berdasarkan respons WAF (bukan variasi buta).
- Pembuktian dampak + bukti aman → `verifikasi-poc-aman` + `skeptic-false-positive-eliminator`.
- Validasi temuan + laporan triage-ready → `triase-duplikat` + `laporan-abstrak`.

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
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
11. **Tanpa aksi destruktif.** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) — tanpa DROP, DELETE, atau hapus data.
12. **Mutasi payload tidak boleh dipakai untuk melewati batas scope atau menyerang di luar target in-scope.** Mutasi hanya mengubah CARA payload yang sama disampaikan ke endpoint yang sama dan sudah in-scope — bukan cara masuk ke endpoint/parameter/program lain, bukan cara melewati autentikasi/otorisasi yang di luar scope.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Baca respons WAF, klasifikasikan blokirnya

1. Kirim payload dasar SEKALI dan simpan respons persis (status, body, header). Klasifikasikan apa yang diblokir:
   - **Kata kunci diblokir** (mis. `script`, `SELECT`, `../` ditolak / dihapus) → keluarga mutasi: encoding & pengaburan kata kunci.
   - **Karakter diblokir** (mis. `<`, `>`, `"`, `'`, spasi, `/` dihapus/di-encode) → keluarga mutasi: encoding karakter & pengganti sintaks.
   - **Pola diblokir** (mis. `<script` ditolak tapi `<svg` lolos; `union select` ditolak tapi varian lain belum dicoba) → keluarga mutasi: pergantian tag/konteks & fragmentasi.
   - **Semua diblokir / respons generik tanpa petunjuk** → JANGAN menebak membabi buta; catat sebagai buntu sementara, kembali ke riset (baca dokumentasi filter bila ada) atau pindah hipotesis.
2. **Standar lulus:** klasifikasi blokir tertulis (keluarga mutasi yang dipilih + alasan dari respons). Tanpa klasifikasi = jangan mutasi; itu tebakan acak.

### Gerbang 2 — Pilih keluarga mutasi, satu keluarga per putaran

Pilih SATU keluarga per putaran, sesuai klasifikasi Gerbang 1. Jangan mencampur dua keluarga dalam satu putaran — bila lolos, tidak ketahuan keluarga mana yang berhasil.

| Keluarga mutasi | Teknik | Contoh pemakaian |
|---|---|---|
| URL encoding | Encode sebagian/semua karakter kunci (`%3C`, double-encoding `%253C`) | WAF memeriksa bentuk mentah, server men-decode |
| Unicode normalization | Karakter Unicode yang dinormalisasi server jadi karakter kunci (mis. bentuk lebar/overlong) | WAF tidak menormalisasi, server menormalisasi |
| Fragmentasi payload | Pecah payload jadi potongan yang digabung server/browser (mis. string concat, tag terpisah) | WAF memeriksa pola utuh, server merangkai potongan |
| Pengganti sintaks | Ganti karakter yang diblokir dengan yang setara (tab/`${IFS}` ganti spasi; backtick; komentar SQL `/**/`) | Satu karakter diblokir, yang setara tidak |
| Pergantian konteks/tag | Ganti tag/fungsi dengan yang setara (`<svg onload>` ganti `<script>`; fungsi SQL lain) | Satu pola diblokir, konteks lain belum |
| Case & whitespace | Ubah kapitalisasi / tambah whitespace yang diabaikan parser | Filter case-sensitive |

**Standar lulus:** satu keluarga dipilih per putaran + alasan dari klasifikasi Gerbang 1. Dua keluarga sekaligus = putaran tidak valid.

### Gerbang 3 — Jalankan putaran adaptif, maksimal 5 putaran per hipotesis

1. Kirim mutasi, simpan respons, nilai: lolos (payload mengeksekusi / mencapai dampak) / masih diblokir (klasifikasi baru?) / berubah (respons berbeda — baca ulang, reklasifikasi).
2. Bila masih diblokir dan klasifikasinya berubah → putaran berikutnya memakai keluarga yang cocok dengan klasifikasi BARU. Bila klasifikasinya sama → jangan ulangi keluarga yang sama; pilih keluarga lain atau berhenti.
3. **Batas keras: maksimal 5 putaran per hipotesis.** Sesudah 5 putaran belum lolos → hipotesis DINYATAKAN BUNTU untuk jalur ini, catat di log + memori (`koreksi-diri-manajemen-memori`), pindah hipotesis. Jangan memutar tanpa batas — itu membanjiri target dan membuang tenaga.
4. **Standar lulus:** log lengkap tiap putaran (mutasi → respons → klasifikasi → verdict) dan jumlah putaran ≤ 5. Putaran tanpa log = tidak terjadi.

### Gerbang 4 — Mutasi lolos → buktikan dampak, serahkan ke triase

1. Mutasi yang lolos LANGSUNG dibuktikan dampaknya dengan teknik aman (`verifikasi-poc-aman`: `document.domain` untuk XSS, callback canary untuk SSRF) — "lolos WAF" saja BUKAN temuan; temuan = dampak terbukti.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** bukti dampak aman tersimpan + keputusan triase tercatat di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Skrip pengujian kecil (Python/bash) | Mengirim satu mutasi per putaran + mencatat respons; hanya bila program mengizinkan otomasi; berhenti otomatis bila respons menunjukkan kerusakan |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log klasifikasi blokir + mutasi per putaran + verdict + keputusan triase |
| Memori pengujian (`koreksi-diri-manajemen-memori`) | Simpan mutasi yang gagal + klasifikasi WAF-nya agar tidak diulang di target/program yang sama |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter]
Payload dasar: [nilai] → Respons WAF: [status/body singkat] → Klasifikasi blokir: [kata kunci/karakter/pola/generik]
Putaran mutasi:
  1. [keluarga: teknik] [nilai] → [respons] → [lolos/masih diblokir/berubah]
  2. [keluarga: teknik] [nilai] → [respons] → [lolos/masih diblokir/berubah]
  (maksimal 5)
Dampak terbukti: [apa yang terjadi + teknik bukti aman yang dipakai]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / buntu / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Mutasi hanya mengakali FILTER, bukan memperbaiki hipotesis yang salah — bila celahnya memang tidak ada, 5 putaran tidak akan menciptakannya.
- WAF yang sama di program berbeda bisa berperilaku berbeda — mutasi yang lolos di satu program belum tentu lolos di program lain; catat per program.
- Unicode normalization dan fragmentasi bergantung pada perilaku parser server — hasil tidak bisa ditebak dari respons WAF saja; bukti akhir tetap dari eksekusi/dampak, bukan dari "kelihatan lolos".
