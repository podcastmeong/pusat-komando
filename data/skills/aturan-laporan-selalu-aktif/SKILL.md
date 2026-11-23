# Skill: Aturan Laporan Selalu Aktif — Lapisan Disiplin Persisten Anti-Karang (Adaptasi Hook YesWeHack ke Muse)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah mekanisme disiplin dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 72; YesWeHack Claude Kit, lapisan always-on SessionStart hook, https://www.yeswehack.com/learn-bug-bounty/triager-grade-reports-claude-code), bukan pengalaman teruji sampai mekanisme ini terbukti mencegah karangan dalam kerja nyata dan dicatat di log. Label ini berlaku untuk semua bagian.

> **ADAPTASI — BACA DULU:** mekanisme aslinya adalah **hook plugin Claude Code (SessionStart)** yang menyuntikkan aturan otomatis setiap sesi dimulai/dilanjutkan/diringkas. **Muse tidak memakai plugin Claude Code dan tidak punya hook SessionStart yang sama.** Adaptasi ke Muse (Gerbang 1) memakai padanan yang tersedia: (1) file instruksi persisten di workspace yang dibaca di awal tiap sesi kerja bounty; (2) skill ini dibaca PERTAMA di setiap sesi bounty sebagai checklist pembuka; (3) gerbang pra-kirim wajib yang tidak bisa dilewati. Bila runtime Muse di kemudian hari menyediakan hook/instruksi persisten yang setara, pasang aturan ini di sana dan perbarui skill ini — jangan klaim adaptasi ini sama dengan hook aslinya.

## Pemicu (kapan dipakai)

- Setiap sesi kerja bounty dimulai — skill ini dibaca PERTAMA, sebelum skill lain dipanggil.
- Setiap kali sesi dilanjutkan atau diringkas (compaction) — baca ulang skill ini, karena ringkasan bisa menghilangkan aturan disiplin.
- Setiap kali draf laporan ditulis atau diperiksa — aturan di sini berlaku selama investigasi, penulisan draf, DAN cek akhir, bukan hanya saat skill tertentu dijalankan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Membaca skill ini di awal sesi + menegakkan aturannya selama kerja |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Format laporan 7 seksi + aturan anti-karang per seksi → skill `tulis-laporan-yeswehack`.
- Simulasi triase + daftar cek AI-slop → skill `simulasi-triase-pra-kirim`.
- Katalog jebakan per kelas → skill `jebakan-per-kelas-kerentanan`.
- Seluruh skill lain bersifat on-demand (dipicu/dipanggil). **Skill ini satu-satunya yang bertipe MEKANISME (lapisan persisten), bukan konten** — ia menjawab masalah berulang yang disebut YesWeHack sebagai penyebab laporan AI ditolak: asisten mengarang fakta saat tidak diawasi. Tidak ada skill lain yang menjawab masalah itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan program yang dikerjakan in-scope sebelum sesi dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Pasang lapisan persisten (adaptasi hook ke Muse)

Mekanisme asli (Claude Code): hook SessionStart menyuntikkan aturan anti-karang otomatis setiap sesi dimulai/dilanjutkan/diringkas. Padanan untuk Muse — lakukan ketiganya, karena tidak ada satu pun yang otomatis:

1. **File instruksi persisten:** salin empat aturan anti-karang (Gerbang 2) ke `~/workspace/catatan/aturan-laporan-anti-karang.md` — file ini dibaca di awal tiap sesi kerja bounty, sebelum pekerjaan lain. Bila file belum ada, buat dari Gerbang 2 di bawah.
2. **Skill ini dibaca pertama:** setiap sesi kerja bounty dibuka dengan membaca skill ini (bukan dipanggil bila ingat — WAJIB pertama). Catat "aturan-laporan-selalu-aktif dibaca" di log sesi.
3. **Gerbang pra-kirim wajib:** tidak ada laporan yang dikirim tanpa melewati `simulasi-triase-pra-kirim` (verdict READY) + audit A60 + persetujuan Cipta — gerbang ini tidak bisa dilewati dengan alasan "sudah yakin".

Standar lulus: file persisten ada + skill ini tercatat dibaca di awal sesi + gerbang pra-kirim tidak pernah dilewati.

### Gerbang 2 — Empat aturan anti-karang (berlaku di SEMUA tahap kerja)

Aturan ini menempel selama investigasi, penulisan draf, dan cek akhir:

| # | Aturan | Pelanggaran yang dicegah |
|---|---|---|
| A1 | Jangan validasi lead yang belum terbukti | Menyatakan "temuan" dari hipotesis yang belum diuji; menaikkan lead mentah menjadi laporan |
| A2 | Jangan tulis dampak teoretis | Dampak "mungkin/secara teori" di seksi Impact tanpa bukti PoC (lihat `tulis-laporan-yeswehack` seksi 5) |
| A3 | Jangan tambah boilerplate | Paragraf generik yang bisa ditempel ke laporan apa pun (AI-slop S2 di `simulasi-triase-pra-kirim`) |
| A4 | Draf hanya dari fakta terverifikasi | Mengisi celah bukti dengan karangan — bila fakta kurang, TANYAKAN/lengkapi dulu, jangan dikarang |

Setiap kali satu aturan dilanggar (oleh diri sendiri maupun oleh draf yang dibaca): hentikan pekerjaan itu, perbaiki pelanggaran, catat ke log sesi ("pelanggaran A2 diperbaiki di draf X"). Standar lulus: nol pelanggaran A1–A4 yang dibiarkan di draf final.

### Gerbang 3 — Pemeriksaan ulang pasca-ringkas (compaction)

Setelah sesi diringkas/dilanjutkan (compaction): baca ulang skill ini + file `~/workspace/catatan/aturan-laporan-anti-karang.md` SEBELUM melanjutkan pekerjaan. Alasan: ringkasan bisa menghilangkan aturan disiplin dan menyisipkan instruksi dari ringkasan itu sendiri (lihat pola injeksi ringkasan buatan sendiri — kandidat 3, kelompok lain). Periksa juga: apakah ada klaim di ringkasan yang tidak punya fakta pendukung — bila ada, tandai "belum terverifikasi" dan verifikasi ulang sebelum dipakai. Standar lulus: skill + file persisten dibaca ulang pasca-ringkas; klaim tanpa fakta ditandai.

## Alat

| Alat | Cara pakai |
|---|---|
| `~/workspace/catatan/aturan-laporan-anti-karang.md` | File instruksi persisten (Gerbang 1.1) — dibuat dari Gerbang 2 bila belum ada |
| Skill ini (dibaca pertama tiap sesi) | Checklist pembuka sesi bounty |
| `simulasi-triase-pra-kirim` | Gerbang pra-kirim wajib (Gerbang 1.3) |
| `~/workspace/catatan/log-bug-bounty.md` | Log pembacaan sesi + pelanggaran A1–A4 yang diperbaiki |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Sesi: [tanggal + target/program]
Aturan dibaca di awal sesi: [ya — file persisten + skill ini]
Pelanggaran A1–A4: [tidak ada / A2 diperbaiki di draf X: ..]
Pasca-ringkas: [dibaca ulang ya/tidak — klaim tanpa fakta: ..]
Gerbang pra-kirim: [simulasi READY + audit A60 + persetujuan Cipta — ya/tidak]
Status: [disiplin-terjaga / ada-pelanggaran-diperbaiki]
```

## Batasan yang diketahui

- Mekanisme ini dari riset (YesWeHack Claude Kit), bukan pengalaman teruji — adaptasi ke Muse (file persisten + baca-pertama + gerbang pra-kirim) belum terbukti sama efektifnya dengan hook otomatis aslinya; label BELUM DIUJI berlaku sampai ada bukti kerja nyata.
- Adaptasi ini TIDAK otomatis — ia bergantung pada disiplin membaca di awal sesi. Bila ada runtime Muse yang menyediakan hook/instruksi persisten setara SessionStart, pasang aturan ini di sana dan perbarui skill ini.
- Skill ini tidak menggantikan validasi isi (`gerbang-tujuh-pertanyaan-triase`, `skeptic-false-positive-eliminator`, `simulasi-triase-pra-kirim`) — ia menjaga agar validasi itu benar-benar dijalankan.
