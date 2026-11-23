# Skill: Scope & Safety Guardian — Gerbang Kepatuhan Sebelum Tool Jaringan Dijalankan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-arsitektur-multi-agent-bounty-2026-11-23.md` bagian 3A + komponen 1, dan aturan program di `buru-bug-bounty/SKILL.md` (23 Nov 2026).

## Pemicu

Dipakai **sebelum tool jaringan apa pun dijalankan** dalam perburuan bug bounty — sebelum recon aktif, sebelum satu request HTTP dikirim, sebelum payload apa pun diuji. Bila skill ini belum lolos, **tidak ada eksekusi**.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **Semua tim bounty A51–A70** (Tim 1 Muse, Tim 2 OpenAI, Tim 3 0din, Tim 4 Google AI VRP, Tim 5 ViKernel) | Jalankan gerbang ini sebelum setiap eksekusi jaringan |
| Pemimpin | **Muse** | Putuskan pengiriman semua laporan; penanggung jawab akhir kepatuhan |

## Sudah tercakup (jangan diduplikat)

- Aturan scope program, daftar target, dan tanggal tutup tersebar di **`buru-bug-bounty`** (skill induk perburuan) — skill ini tidak mengulang daftar programnya, hanya **menegakkannya**.
- Pemantauan perubahan scope, hadiah, dan deadline program ada di **`recon-pantau-program`** (A53/A59) — skill itu **menemukan dan memantau** program; skill ini adalah **gerbang penegakan SEBELUM eksekusi**, bukan penemuan program.
- Bila scope/aturan program berubah, `recon-pantau-program` yang memperbarui catatannya; skill ini yang memblokir eksekusi yang melanggar catatan terbaru itu.

## Aturan keras

1. **Hanya program bounty resmi yang in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr (jalur audit kode OSV saja). Di luar daftar ini = HENTIKAN.
2. **Hanya akun sendiri + canary palsu.** Uji hanya dengan akun milik kita sendiri (`test_account_1` / `test_account_2` atau akun milik tim). Tanpa data orang lain — jangan pernah baca, ubah, atau hapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests) — DIBLOKIR** dalam bentuk apa pun. Playbook skenario korban di `buru-bug-bounty` butuh persetujuan Cipta dulu; tanpa persetujuan itu, langkah tersebut tidak boleh dijalankan.
4. **Tanpa DoS/DDoS dan tanpa metode destruktif.** Larang stress testing, larang metode `DELETE`/`DROP`, larang ubah/hapus data apa pun (kecuali data akun uji sendiri yang memang dibuat untuk diuji).
5. **Tanpa payload di permukaan publik.** Perintah/j payload uji jangan di-host di permukaan publik (halaman web publik, repo publik, postingan publik).
6. **Validasi human-in-the-loop.** Laporan tidak dikirim otomatis; draf VERIFIED ditinjau manusia (Muse → Cipta) sebelum submit. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program.** huntr: "Humans only — automated tooling gets you banned" → jangan ikut challenge-nya dengan agen AI. **Gray Swan dilewati total** (perintah Cipta 23 Nov 18:35).
8. **Google AI VRP: payload injeksi DIBLOKIR.** Tim 4 analisis format saja, tanpa file payload — jangan diulang, diparafrasa, atau dicari jalan lain.
9. **Rate limit maks 5 permintaan/detik**, kecuali program secara eksplisit mengizinkan lebih. Larang pemindaian massal tanpa jeda.
10. **Berhenti 1 hari sebelum program tutup.** ViKernel S1–3 STOP **15 Jan 2027**, S4 STOP **14 Feb 2027**. Program tanpa tanggal tutup (Muse, OpenAI, 0din, Google AI VRP) tetap dipantau tiap minggu oleh `recon-pantau-program`.
11. **Sertakan header identifikasi peneliti** (`X-Bug-Bounty-Researcher: <handle>`) bila program mewajibkannya.
12. **Slogan Cipta = gerbang eksekusi:** Aman + Gratis + Valid + Potensi + Peluang + AI boleh ikut. Satu unsur gagal = jangan eksekusi.

## Langkah + gerbang

Jalankan berurutan sebelum setiap sesi eksekusi jaringan. **Satu gerbang gagal = HENTIKAN, catat di log, jangan lanjut.**

### Gerbang 1 — Baca scope + aturan program target

- Baca scope dan aturan program target (halaman resmi / dokumen program) sampai paham apa yang dinilai dan apa yang dilarang.
- **Standar lulus:** nama program, daftar `in_scope_assets`, metode yang diizinkan/dilarang, dan tanggal tutup tercatat; sumbernya tautan resmi. Tanpa sumber resmi = GAGAL.

### Gerbang 2 — Validasi target vs `in_scope_assets`

- Cocokkan target (URL/IP/metode HTTP yang akan dipakai) dengan daftar `in_scope_assets` program.
- **Standar lulus:** target persis ada di daftar in-scope DAN metodenya tidak masuk daftar larangan program. **Tidak cocok = HENTIKAN.**

### Gerbang 3 — Validasi akun + data

- Pastikan yang disentuh hanya akun uji sendiri (`test_account_1`/`test_account_2` atau akun milik tim) dan data canary palsu.
- **Standar lulus:** tidak ada data pengguna lain, tidak ada uji korban, tidak ada payload di permukaan publik. Satu saja terlanggar = HENTIKAN.

### Gerbang 4 — Validasi metode + laju

- Pastikan metode bukan destruktif (`DELETE`/`DROP`/ubah-hapus data) dan bukan DoS/stress testing; tetapkan jeda agar laju ≤ 5 permintaan/detik (kecuali program mengizinkan lebih, dengan bukti tertulis aturannya).
- **Standar lulus:** metode aman + laju dalam batas + jeda antar permintaan tercatat. Pelanggaran = HENTIKAN.

### Gerbang 5 — Validasi tenggat + header

- Pastikan hari ini bukan 1 hari sebelum tutup program (ViKernel S1–3: STOP 15 Jan 2027; S4: STOP 14 Feb 2027) dan sertakan header `X-Bug-Bounty-Researcher: <handle>` bila diwajibkan program.
- **Standar lulus:** masih dalam masa kerja program + header terpasang bila wajib. Lewat tenggat = HENTIKAN.

### Gerbang 6 — Catat keputusan gerbang

- Tulis hasil tiap gerbang (LOLOS/GAGAL + alasan) ke log sebelum eksekusi dimulai.
- **Standar lulus:** log gerbang tertulis; eksekusi hanya jalan bila keenam gerbang LOLOS.

## Alat

- Dokumen scope/aturan program target (halaman resmi program).
- Daftar `in_scope_assets` program (dari `buru-bug-bounty` / catatan recon terbaru).
- Log: `~/workspace/catatan/log-bug-bounty.md` (wajib) + `~/workspace/catatan/keputusan.md` (ringkasan hari itu juga, bila ada keputusan baru).

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` sebelum eksekusi, satu entri per sesi:

```
## [YYYY-MM-DD HH:MM WIB] Gerbang Scope & Safety — [Program] — [Tim]
- Target: [URL/IP + metode HTTP]
- Gerbang 1 (scope dibaca): LOLOS/GAGAL — [catatan]
- Gerbang 2 (target in-scope): LOLOS/GAGAL — [catatan]
- Gerbang 3 (akun/data sendiri): LOLOS/GAGAL — [catatan]
- Gerbang 4 (metode + laju ≤5/detik): LOLOS/GAGAL — [catatan]
- Gerbang 5 (tenggat + header): LOLOS/GAGAL — [catatan]
- Keputusan: LANJUT / HENTIKAN — [alasan bila HENTIKAN]
```

Bila HENTIKAN: jangan jalankan tool jaringan apa pun untuk target itu; catat alasan dan (bila relevan) laporkan ke Muse.
