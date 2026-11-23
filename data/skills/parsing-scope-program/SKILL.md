# Skill: Parsing Scope Program — Ubah Aturan Program Jadi Catatan Scope Terstruktur (untuk A53 Recon Program + A59 Threat Hunter)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md` Fase 1 butir 1 (Scope Parsing & Validation), 23 Nov 2026.

## Pemicu

Dipakai **setiap kali ada program bounty baru yang lolos gerbang slogan** (Aman, Gratis, Valid, Potensi, Peluang, AI boleh ikut) **atau setiap kali aturan/scope program aktif berubah** — SEBELUM tim mana pun menguji target program itu. Skill ini menghasilkan catatan scope terstruktur yang dipakai `scope-and-safety-guardian` sebagai daftar `in_scope_assets` di Gerbang 1–2. Tanpa catatan scope dari skill ini, **tidak ada eksekusi** (guardian tidak punya daftar untuk divalidasi).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Parse aturan program baru → tulis catatan scope terstruktur |
| Pengerjaan | **A59 Threat Hunter** | Parse ulang bila scope/aturan program aktif berubah; catat perubahan hari itu juga |
| Konsumen | **Semua tim bounty A51–A70** | Pakai catatan scope ini lewat `scope-and-safety-guardian` sebelum eksekusi |
| Pemimpin | **Muse** | Putuskan program mana yang dieksekusi; putuskan bila aturan program ambigu |

## Sudah tercakup (jangan diduplikat)

- **Penemuan + validasi program baru** (nama, hadiah, slogan 6 unsur, tanggal tutup) ada di **`recon-pantau-program`** — skill itu memutuskan program layak dicatat sebagai kandidat; skill ini **mengurai aturan program yang sudah lolos itu menjadi daftar aset/metode terstruktur**.
- **Penegakan scope sebelum eksekusi** ada di **`scope-and-safety-guardian`** (Gerbang 1–2) — guardian MEMAKAI daftar `in_scope_assets` yang dihasilkan skill ini, bukan membuatnya. Bila catatan scope belum ada atau sudah basi, guardian GAGAL dan eksekusi HENTIKAN.
- **Cek duplikat + skor temuan** ada di **`triase-duplikat`** — bukan bagian skill ini.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Program di luar daftar resmi tim (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja) = JANGAN di-parse untuk eksekusi.
2. **Hanya akun sendiri + canary palsu.** Scope yang di-parse tidak boleh dipakai untuk menyentuh data orang lain atau menguji korban.
3. **Tanpa data orang lain; tanpa uji korban; tanpa DoS/DDoS.** Parsing adalah pekerjaan baca dokumen — tidak ada request pengujian ke target selama parsing.
4. **Tanpa payload di permukaan publik.** Contoh/payload apa pun dari dokumen program jangan di-host di permukaan publik.
5. **Validasi human-in-the-loop.** Catatan scope yang ambigu (aturan bertentangan, wildcard tidak jelas, metode di perbatasan larangan) HARUS ditandai AMBIGU dan diputuskan Muse/Cipta — jangan ditebak sendiri.
6. **Tanpa laporan tanpa persetujuan Cipta.** Skill ini tidak mengirim laporan apa pun.
7. **Patuhi larangan otomasi program.** huntr "Humans only" → challenge huntr JANGAN di-parse untuk eksekusi agen AI (hanya jalur audit kode OSV). **Gray Swan dilewati total** (perintah Cipta 23 Nov 18:35).
8. **Larang aksi destruktif (DROP, DELETE, hapus data).** Bila dokumen program mengizinkan metode destruktif sekalipun, pembuktian tim tetap harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive — izin program bukan izin merusak.
9. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Untuk program agen AI (Muse, OpenAI Safety, Google AI VRP, 0din, ViKernel), yang di-parse adalah aturan hasil/outcome program itu, bukan teknik web klasik.
10. **Satu sumber resmi per fakta.** Setiap baris catatan scope wajib menunjuk ke sumber resmi (tautan halaman program / dokumen resmi). Tanpa sumber resmi = BELUM TERVERIFIKASI, jangan dipakai eksekusi.

## Langkah + gerbang

### Langkah 1 — Kumpulkan dokumen aturan program

- Ambil dokumen resmi program dari sumbernya: halaman program (HackerOne/Bugcrowd/halaman resmi), file `scope.json`/JSON, `SECURITY.md`/Markdown, atau PDF aturan program. Simpan salinan lokal + tautan sumber + tanggal ambil.
- **Standar lulus:** minimal satu dokumen/sumber resmi tersimpan; tanggal ambil tercatat. Tidak ada sumber resmi = GAGAL, jangan lanjut.

### Langkah 2 — Urai jadi catatan scope terstruktur

- Dari dokumen Langkah 1, isi SEMUA kolom berikut (kosong = tulis "TIDAK DISEBUTKAN", jangan dikarang):
  - `in_scope_assets`: daftar persis aset (domain, URL, IP, aplikasi, model) — termasuk wildcard (`*.contoh.com`) dan pengecualiannya.
  - `out_of_scope_assets`: daftar persis yang dilarang (termasuk subdomain/endpoint yang disebut eksplisit).
  - `metode_diizinkan`: metode pengujian yang disebut boleh.
  - `metode_dilarang`: metode yang disebut dilarang (DoS, spam, akses data pengguna, dsb.).
  - `larangan_otomasi`: apakah AI/otomasi dilarang (contoh: huntr "Humans only") — bila YA, tulis "AGEN AI DILARANG" dan HENTIKAN parsing untuk eksekusi.
  - `safe_harbor`: ada/tidak + syaratnya.
  - `tier_hadiah`: tier + kisaran hadiah per kategori (bila dipublikasikan).
  - `tanggal_tutup`: tanggal tutup program + tanggal STOP kerja (1 hari sebelumnya).
  - `ambiguitas`: bagian aturan yang bertentangan/tidak jelas, ditandai AMBIGU.
- **Standar lulus:** semua kolom terisi atau ditandai "TIDAK DISEBUTKAN"; tiap baris punya sumber (tautan/bagian dokumen). Satu kolom diisi dari dugaan = GAGAL.

### Langkah 3 — Filter target: tandai in-scope vs out-of-scope

- Untuk tiap target yang direncanakan tim, cocokkan dengan `in_scope_assets` dan `out_of_scope_assets` (perhatikan wildcard dan pengecualian). Tulis daftar `target_lolos` (in-scope) dan `target_ditolak` (out-of-scope + alasan + sumber aturannya).
- **Standar lulus:** tiap target punya verdict LOLOS/DITOLAK + alasan + sumber. Target tanpa verdict = GAGAL.

### Gerbang 4 — Serahkan ke guardian + catat

- Simpan catatan scope ke `~/workspace/catatan/log-bug-bounty.md` (entri baru, format di bawah) dan beri tahu Muse agar `scope-and-safety-guardian` bisa memakainya. Bila ada AMBIGU, sampaikan ke Muse untuk diputuskan sebelum eksekusi.
- **Standar lulus:** catatan scope tertulis + AMBIGU (bila ada) sudah diteruskan ke Muse. Eksekusi hanya jalan setelah guardian lolos memakai catatan ini.

## Alat

- Dokumen resmi program (halaman program / JSON / Markdown / PDF) + salinan lokalnya.
- Log: `~/workspace/catatan/log-bug-bounty.md` (wajib) + `~/workspace/catatan/keputusan.md` (ringkasan bila ada keputusan baru hari itu juga).
- Skill konsumen: `scope-and-safety-guardian` (penegakan), `recon-pantau-program` (pemantauan perubahan).

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md`, satu entri per program (baru atau berubah):

```
## [YYYY-MM-DD HH:MM WIB] Catatan Scope — [Program] — [A53/A59]
- Sumber resmi: [tautan + tanggal ambil]
- in_scope_assets: [daftar persis]
- out_of_scope_assets: [daftar persis]
- metode_diizinkan: [daftar]
- metode_dilarang: [daftar]
- larangan_otomasi: [YA — AGEN AI DILARANG / TIDAK]
- safe_harbor: [ada/tidak + syarat]
- tier_hadiah: [tier + kisaran]
- tanggal_tutup: [tanggal] — STOP kerja: [tanggal - 1 hari]
- target_lolos: [daftar + alasan]
- target_ditolak: [daftar + alasan + sumber aturan]
- ambiguitas: [bagian AMBIGU + diteruskan ke Muse: YA/TIDAK]
- Keputusan: SIAP DIEKSEKUSI (guardian boleh pakai) / DITAHAN (alasan)
```

Bila `larangan_otomasi: YA` atau program = Gray Swan: keputusan DITAHAN, jangan teruskan ke eksekusi agen AI.
