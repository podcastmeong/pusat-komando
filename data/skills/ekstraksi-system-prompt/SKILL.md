# Skill: Ekstraksi System Prompt — Memancing Model Membocorkan Instruksi Sistem / Konfigurasi Internal

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 2).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh workflow di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua langkah sampai ada satu kasus nyata yang lolos gerbang QC dan dicatat di log.
>
> **STATUS SKILL: TUNGGU — JANGAN DIPAKAI DULU.** Lihat Gerbang Scope di bawah. Sampai ada program aktif yang secara eksplisit mengizinkan/membayar kategori ini, skill ini hanya arsip referensi, bukan instruksi kerja.

## Gerbang Scope (DI ATAS semua aturan — baca dulu sebelum apa pun)

1. **OUT OF SCOPE di Google AI VRP dan 0din.** Prompt Extraction = N/A untuk Muse Spark (terverifikasi 23 Nov 2026). Jangan kejar kategori ini di kedua program itu.
2. **TIDAK dibayar di Muse/Meta.** Skill `buru-bug-bounty` mencatat "bocor system prompt" sebagai yang TIDAK dibayar di Muse. Jangan kejar di program Muse.
3. **Hanya berlaku untuk program yang secara eksplisit mengizinkan/membayar kategori ini.** Bukti yang diterima: teks scope/panduan hadiah program yang menyebut system prompt extraction sebagai kategori berbayar. Klaim forum atau "katanya dibayar" bukan bukti.
4. **Hanya pada akun tes sendiri.** Pengujian hanya terhadap model/aplikasi yang kita pakai dengan akun kita sendiri.
5. **Bila tidak ada program aktif yang membayarnya, skill ini berstatus "TUNGGU — jangan dipakai dulu".** Kondisi saat skill ditulis (23 Nov 2026): TIDAK ADA program aktif kita yang membayar kategori ini → **skill ini TIDAK BOLEH dipakai.**
6. **Standar lulus gerbang ini:** nama program + kutipan scope yang mengizinkan kategori ini, tertulis di log SEBELUM pengujian apa pun dimulai. Tanpa kutipan scope = gerbang GAGAL = berhenti.

## Pemicu (kapan dipakai)

HANYA bila Gerbang Scope di atas lolos: ada program bounty aktif yang secara eksplisit mengizinkan/membayar system prompt extraction, dan pengujian dilakukan pada akun tes sendiri. Bila gerbang tidak lolos, skill ini tidak dipakai — tidak ada pengecualian.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A63 Format Analyst** | Memeriksa scope program; bila gerbang lolos, menguji teknik ekstraksi pada akun sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan apakah gerbang scope benar-benar lolos; membunuh jalur ini bila tidak |

## Sudah tercakup (jangan diduplikat)

- Prompt injection (menyisipkan instruksi agar model menjalankan perintah yang tidak diinginkan) → skill `buru-bug-bounty`.
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Bukti dampak → skill `triase-duplikat` + `laporan-abstrak`.

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
10. **Jangan pernah mempublikasikan system prompt yang berhasil diekstrak** — isi prompt yang bocor hanya ditulis di draf laporan privat untuk program (dan ke Cipta), tidak di log publik, tidak di media sosial, tidak di permukaan publik mana pun.
11. **Bocornya system prompt saja BELUM tentu dibayar.** Yang dinilai program adalah dampaknya (mis. prompt berisi rahasia/konfigurasi yang memungkinkan penyalahgunaan lebih lanjut). Bocoran tanpa dampak = temuan lemah, jangan kirim.

## Langkah + gerbang

### Gerbang 1 — Verifikasi scope (WAJIB, sebelum teknik apa pun)

1. Baca scope + panduan hadiah program target. Cari penyebutan eksplisit system prompt extraction / prompt extraction sebagai kategori berbayar.
2. Tulis kutipan scope itu di log beserta nama program dan tanggal pengecekan.
3. **Standar lulus:** ada kutipan scope tertulis. Tidak ada kutipan = BERHENTI. Jangan lanjut ke Gerbang 2.

### Gerbang 2 — Tentukan apa yang dicari

1. Tulis dulu: instruksi/konfigurasi apa yang diduga ada di balik model (mis. aturan alat, batasan, identitas), dan kenapa bocornya itu berdampak (rahasia apa yang terungkap, penyalahgunaan apa yang dimungkinkan).
2. **Standar lulus:** target + alasan dampak tertulis. Tanpa alasan dampak = jangan uji.

### Gerbang 3 — Uji dengan langkah minimal, di akun sendiri

1. Ajukan permintaan yang memancing model mengulang/menjelaskan instruksinya, dengan variasi format yang wajar (permintaan langsung, permintaan ringkasan aturan, permintaan melalui konteks tugas). Satu variasi per putaran, catat respons persis.
2. Jangan memakai teknik yang merusak layanan, jangan mengunggah apa pun ke permukaan publik, jangan melibatkan akun/data orang lain.
3. **Standar lulus:** log tiap percobaan (permintaan → respons → berhasil/gagal). Respons yang hanya "saya tidak bisa" = gagal, catat dan variasikan.

### Gerbang 4 — Bedakan bocoran asli dari halusinasi

1. Minta model mengulang bagian yang diduga bocor dengan cara berbeda; cocokkan konsistensinya. Periksa apakah isi yang muncul konsisten di beberapa percobaan dan masuk akal sebagai instruksi sistem (bukan karangan model).
2. **Standar lulus:** isi yang sama muncul konsisten di ≥2 percobaan berbeda dan bisa dijelaskan kenapa itu instruksi sistem, bukan halusinasi. Sekali muncul lalu hilang = belum terbukti.

### Gerbang 5 — Nilai dampak + serahkan ke triase

1. Tulis dampaknya: rahasia/konfigurasi apa yang terungkap dan penyalahgunaan apa yang dimungkinkan. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
2. **Standar lulus:** dampak tertulis + keputusan triase tercatat. Bocoran tanpa dampak = tidak maju.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun tes sendiri pada program target | Satu-satunya akun yang dipakai; jangan memakai akun orang lain. |
| Dokumen scope/panduan hadiah program | Sumber kebenaran gerbang scope — baca teks aslinya, jangan mengandalkan ingatan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log kutipan scope + semua percobaan (permintaan → respons → verdict). |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Program: [nama]
Kutipan scope yang mengizinkan: [teks persis + tanggal dicek]
Target yang dicari: [instruksi/konfigurasi apa]
Percobaan:
  1. [permintaan] → [respons] → [gagal/berhasil]
Dampak bila bocor: [rahasia apa + penyalahgunaan apa]
Keputusan triase: [maju / ditolak + alasan]
Status: [tunggu / diuji / terbukti / dilaporkan / ditolak]
```

Isi system prompt yang berhasil diekstrak TIDAK ditulis di log — hanya di draf laporan privat untuk program.

## Batasan yang diketahui

- Per 23 Nov 2026, tidak ada program aktif kita yang membayar kategori ini — skill ini berstatus TUNGGU.
- Model sering mengarang "system prompt" palsu; Gerbang 4 ada untuk menyaring halusinasi.
