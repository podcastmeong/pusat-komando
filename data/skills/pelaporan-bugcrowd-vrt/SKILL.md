# Skill: Pelaporan Bugcrowd VRT — Kategori, Override Severity & Sanggahan OOS

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 59, Claude-BugHunter `bugcrowd-reporting`), bukan pengalaman teruji sampai ada laporan Bugcrowd yang dibayar memakai taktik ini dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Laporan ditujukan ke program di platform Bugcrowd.
- Kategori VRT (Vulnerability Rating Taxonomy) yang tersedia tidak ada yang cocok persis dengan temuan.
- Severity default VRT meremehkan dampak yang sudah terbukti.
- Triager menolak laporan dengan alasan klausul out-of-scope (mis. rate limiting pada auth) padahal dampaknya nyata.
- Dipakai BERSAMA `penulisan-laporan-bounty` (template umum) — skill ini HANYA taktik khusus Bugcrowd, bukan pengganti penulisan laporan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Memilih kategori VRT + menulis paragraf severity + sanggahan OOS |
| Audit | **A60 Security Auditor** | Memeriksa argumen VRT/severity/OOS berbasis fakta, bukan emosi |
| Pemimpin | **Muse** | Memutuskan draf mana yang maju ke persetujuan Cipta |

## Sudah tercakup (jangan diduplikat)

- **Template laporan umum per platform** (HackerOne, Bugcrowd, Intigriti, Immunefi) + formula judul + pernyataan dampak → skill `penulisan-laporan-bounty`. Skill ini TIDAK mengulang template itu — hanya mekanisme VRT dan sanggahan OOS Bugcrowd.
- **Skor CVSS saja** → skill `penilaian-cvss`.
- **Simulasi triase pra-kirim / validasi temuan** → skill `gerbang-tujuh-pertanyaan-triase` dan `skeptic-false-positive-eliminator`. Skill ini dipakai SETELAH temuan lolos kedua gerbang itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Bugcrowd; program yang sama dengan tempat temuan diuji). Pastikan program tujuan adalah program Bugcrowd in-scope sebelum menulis.
2. **Hanya akun sendiri + canary palsu.** Semua bukti berasal dari akun uji sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — jangan klaim dampak destruktif yang tidak dibuktikan secara aman.
11. **JANGAN PERNAH mengirim laporan otomatis ke Bugcrowd.** Draf ditinjau manusia 2–3 menit + disetujui Cipta sebelum submit.
12. **Argumen severity/OOS HANYA berbasis fakta yang sudah terbukti.** Jangan membesar-besarkan severity atau menyerang klausul OOS tanpa bukti langkah reproduksi yang menunjukkan dampak nyata.

## Langkah + gerbang

### Gerbang 1 — Strategi pencarian & fallback kategori VRT

Bugcrowd memakai VRT — tiap laporan wajib memilih satu kategori. Bila tidak ada yang cocok persis:

1. **Cari dari dampak, bukan dari nama kelas.** Tanyakan: "apa yang bisa dilakukan penyerang?" — lalu cari kategori VRT yang menggambarkan DAMPAK itu (mis. temuan rantai open-redirect → ATO masuk kategori pengambilalihan akun, bukan sekadar "open redirect").
2. **Fallback berlapis:** (a) kategori paling dekat secara teknis; (b) bila dua kategori sama dekat, pilih yang severity default-nya lebih tinggi DAN jelaskan alasannya di laporan; (c) bila benar-benar tidak ada, pilih kategori umum ("Other" / "Insufficient ...") dan tulis penjelasan eksplisit di paragraf pertama mengapa kategori itu dipilih.
3. **Catat pilihan + alasan** di draf — triager menilai apakah hunter memahami taksonomi atau asal pilih.

### Gerbang 2 — Override severity manual

Bila severity default VRT meremehkan dampak yang terbukti:

1. **Tulis paragraf permintaan severity sebagai BAGIAN PERTAMA isi laporan** (sebelum langkah reproduksi), dengan format:
   - Severity yang diminta (P1–P4) + alasannya dalam 2–3 kalimat berbasis fakta.
   - Bukti dampak yang mendukung (langkah reproduksi yang menunjukkan rantai sampai ke dampak).
   - Perbandingan: kategori VRT yang dipilih memberi default P3, tetapi dampak yang terbukti (sebutkan konkret) setara P1/P2 karena [alasan faktual].
2. **Jangan meminta severity tanpa bukti baru.** Permintaan yang hanya berisi "menurut saya ini kritis" tanpa langkah reproduksi = diabaikan triager.
3. **Sertakan CVSS 3.1 Base** (lihat `penilaian-cvss`) sebagai pendukung angka — tetapi ingat keputusan akhir ada di triager.

### Gerbang 3 — Template sanggahan klausul out-of-scope (OOS)

Bila laporan ditolak dengan alasan klausul OOS, sanggah HANYA bila ada bukti dampak yang membuat klausul itu tidak berlaku. Template sanggahan:

```
Terima kasih atas peninjauannya. Saya memahami laporan ini awalnya
dinilai masuk klausul out-of-scope [nama klausul, mis. "rate limiting
pada autentikasi"]. Namun bukti berikut menunjukkan klausul itu tidak
berlaku pada kasus ini:

1. [Langkah reproduksi singkat yang menunjukkan dampak — bukan sekadar
   keberadaan kelemahan, melainkan rantai sampai ke dampak konkret
   pada akun uji sendiri.]
2. [Mengapa dampak ini berbeda dari yang dimaksud klausul OOS —
   mis. bukan sekadar "tidak ada rate limit", melainkan "tidak ada
   rate limit + enumerasi user + bypass lockout = ATO akun uji".]
3. [Bukti pendukung: log / screenshot / video, semua disensor.]

Saya mohon peninjauan ulang berdasarkan bukti di atas.
```

Aturan sanggahan:
- **Satu sanggahan per laporan, berbasis bukti baru atau sudut pandang yang belum dipertimbangkan.** Mengirim sanggahan yang sama berulang-ulang tanpa bukti baru merusak reputasi akun.
- **Bila triager tetap menolak setelah satu sanggahan berbasis bukti, TERIMA dan catat** — jangan berdebat lebih lanjut. Pindah ke temuan berikutnya.
- **Contoh klausul OOS yang sering disalahpahami:** rate limiting pada auth (tidak berlaku bila dirantai ke ATO/brute force yang terbukti); missing security headers (tidak berlaku bila header itu adalah satu-satunya pertahanan pada endpoint sensitif dan terbukti bisa dieksploitasi); "informational" (tidak berlaku bila ada rantai dampak konkret).

### Gerbang 4 — Checklist pra-pengiriman khusus Bugcrowd

- [ ] Kategori VRT dipilih + alasan tercatat (Gerbang 1)
- [ ] Paragraf permintaan severity (bila override) ada di bagian pertama laporan (Gerbang 2)
- [ ] Template umum dari `penulisan-laporan-bounty` sudah diikuti (judul, impact-first, repro, CVSS)
- [ ] Semua bukti disensor (`[REDACTED]`)
- [ ] Draf ditinjau manusia 2–3 menit + disetujui Cipta

## Alat

| Alat | Cara pakai |
|---|---|
| `penulisan-laporan-bounty` | Template laporan umum + formula judul + pernyataan dampak |
| `penilaian-cvss` | Skor CVSS 3.1 Base pendukung override severity |
| Dokumentasi VRT Bugcrowd (publik) | Daftar kategori + severity default terbaru — periksa sebelum memilih |
| `~/workspace/catatan/log-bug-bounty.md` | Log pilihan VRT + sanggahan OOS + keputusan gerbang |

## Format output

Tulis draf laporan Bugcrowd ke file draf dengan format:

```
Platform: Bugcrowd
Program: [nama program]
Kategori VRT: [kategori + alasan pilih]
Severity diminta: [P1–P4 + alasan 2–3 kalimat, bila override]
Judul: [<kelas> in <lokasi> via <param/header> — <100 karakter]
Dampak (paragraf pertama): [2–3 kalimat impact-first]
Langkah reproduksi: [langkah bernomor, bisa dijalankan ulang]
CVSS: [skor Base 3.1 + vektor]
Sanggahan OOS: [bila ada — pakai template Gerbang 3]
Status: [draf / ditinjau / disetujui Cipta / terkirim / dibayar / ditolak / disanggah]
```

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `bugcrowd-reporting`), bukan pengalaman teruji — taktik ini butuh satu laporan Bugcrowd yang dibayar sebelum label BELUM DIUJI dicabut.
- VRT diperbarui berkala oleh Bugcrowd — kategori dan severity default bisa berubah; periksa dokumentasi VRT terbaru sebelum memilih, jangan mengandalkan hafalan.
- Override severity dan sanggahan OOS hanya bekerja bila didukung bukti — tanpa bukti, keduanya diabaikan dan bisa menurunkan kredibilitas hunter bila dipakai berlebihan.
- Keputusan triager bersifat final setelah satu sanggahan berbasis bukti — jangan menghabiskan waktu berdebat; pindah ke temuan berikutnya.
