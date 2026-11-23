# Skill: Metode Belajar 70-20-10 — Praktik, Komunitas, dan Teori untuk Skill Bounty yang Terus Naik

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 21 (artikel Medium "BUG-BOUNTY SERIES 5" Krisna Wahyu Andriawan), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill METODE BELAJAR untuk tim bounty: rasio 70–20–10 (70% praktik langsung, 20% belajar dari komunitas, 10% teori/referensi), belajar dari write-up + laporan publik, dan target realistis + konsistensi jangka panjang. Skill ini BUKAN skill pengujian: tidak ada langkah menyerang di sini — hasilnya adalah rencana belajar + catatan pelajaran yang dipakai putaran berikutnya.

## Pemicu

Dipakai secara berkala (tiap awal pekan/putaran) untuk menyusun rencana belajar tim, dan setiap kali putaran berakhir tanpa temuan (evaluasi kegagalan sebagai proses belajar). Dipakai SETELAH putaran selesai — hasilnya masuk ke rencana putaran berikutnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **Semua tim bounty A51–A70** | Menjalankan porsi belajar masing-masing sesuai rasio |
| Audit | **A60 Security Auditor** | Memvalidasi catatan pelajaran (pelajaran harus dari fakta putaran, bukan opini) |
| Pemimpin | **Muse** | Menyusun rencana belajar putaran berikutnya + menetapkan target realistis |

## Sudah tercakup (jangan diduplikat)

- Kurikulum belajar ethical hacker → skill `jalur-belajar-ethical-hacker-maraton`. Skill ini adalah METODE RASIO belajar (70-20-10) — bukan kurikulumnya.
- Platform lab (HTB/TryHackMe/PortSwigger) → skill `lab-hack-the-box`, `jalur-belajar-tryhackme`, `lab-portswigger-academy`, `lab-pentesterlab`. Skill ini memakai lab-lab itu sebagai porsi 70% — bukan mengulang panduannya.
- Threat intel + CVE → skill `intelijen-ancaman-berkala` + `pemantauan-cve-breach-nyata`. Skill ini memakai hasil keduanya sebagai bahan porsi 20% (belajar dari laporan publik) — bukan mengulang pemantauannya.
- Konsistensi/maraton → dibahas di skill ini sebagai TARGET + EVALUASI (bukan sekadar slogan).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Belajar di sini HANYA untuk program itu.
2. **Hanya akun sendiri + canary palsu.** Praktik belajar (porsi 70%) HANYA di lab sendiri, platform latihan legal, atau program in-scope dengan akun sendiri.
3. **Tanpa data orang lain.** Belajar dari write-up publik HANYA memakai informasi publik — tanpa data korban.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba, termasuk atas nama "belajar".
5. **Tanpa DoS/DDoS.** Praktik belajar tidak membanjiri target apa pun.
6. **Tanpa payload di permukaan publik.** Catatan belajar hanya di log internal.
7. **Pelajaran harus dari fakta.** Setiap pelajaran yang dicatat harus merujuk ke kejadian nyata putaran (teknik apa yang gagal + kenapa) — bukan opini umum.
8. **Validasi human-in-the-loop.** Rencana belajar + target realistis harus diperiksa manusia (Muse/A60).
9. **Tanpa laporan tanpa persetujuan Cipta.** Pelajaran yang berujung temuan tetap lewat jalur draf → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai write-up publik untuk meniru serangan terhadap korban atau target di luar scope. Belajar di sini HANYA untuk teknik yang sah di program in-scope.

## Langkah + gerbang

### Gerbang 0 — Evaluasi putaran lalu (bahan belajar)

1. Tinjau putaran lalu: teknik apa yang dicoba, mana yang gagal + kenapa, mana yang hampir berhasil, apa yang tidak diketahui tim saat itu. Tulis 3–5 pelajaran faktual (bukan opini).
2. **Standar lulus:** daftar pelajaran tertulis dengan rujukan kejadian. Pelajaran tanpa rujukan = opini, buang.

### Gerbang 1 — Susun rencana 70-20-10 putaran ini

1. Bagi waktu belajar putaran ini dengan rasio: **70% Praktik Langsung** (hunting di program in-scope + lab/vulnerable environment — latih teknik yang akan dipakai); **20% Belajar dari Komunitas** (diskusi sesama hunter, membaca write-up + laporan publik yang relevan dengan target); **10% Teori dan Referensi** (dokumentasi teknis, artikel riset, paper keamanan).
2. **Standar lulus:** rencana tertulis dengan alokasi 70-20-10 + topik tiap porsi. Rencana tanpa alokasi = belum tersusun.

### Gerbang 2 — Belajar dari write-up + laporan publik (porsi 20%)

1. Pilih 2–3 write-up/laporan publik yang relevan dengan target putaran ini. Untuk tiap write-up, catat: teknik apa yang dipakai, kondisi apa yang membuatnya berhasil, apakah kondisi itu ada di target kita, dan skill apa yang perlu dilatih untuk menirunya SECARA SAH.
2. **Standar lulus:** tiap write-up punya catatan teknik + kondisi + relevansi dengan target. Write-up tanpa relevansi = bacaan bebas, bukan bahan belajar putaran.

### Gerbang 3 — Tetapkan target realistis + jaga konsistensi

1. Tetapkan target putaran ini yang REALISTIS (contoh: 1 bug valid per bulan — bukan 10 temuan per minggu). Tetapkan juga sikap terhadap hasil: status "duplicate"/"informational" BUKAN kegagalan — itu data belajar. Evaluasi setiap kegagalan sebagai proses belajar (Gerbang 0 putaran berikutnya).
2. **Standar lulus:** target tertulis + sikap terhadap duplicate/informational tertulis. Target tanpa batas realistis = akan mengecewakan tim, turunkan.

### Gerbang 4 — Serahkan rencana belajar ke putaran

1. Serahkan rencana 70-20-10 + catatan write-up + target ke koordinator putaran. Skill ini BERHENTI di sini.
2. **Standar lulus:** rencana tercatat di log. Skill ini tidak mencatat "temuan" — hanya "rencana belajar diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Lab legal (HTB, TryHackMe, PortSwigger, PentesterLab) | Porsi 70% — praktik teknik sebelum dipakai di program nyata |
| Write-up + laporan publik | Porsi 20% — bahan belajar teknik yang terbukti berhasil |
| Dokumentasi teknis + paper keamanan | Porsi 10% — teori pendukung |
| `jalur-belajar-ethical-hacker-maraton` | Kurikulum jangka panjang sebagai konteks rencana ini |
| `~/workspace/catatan/log-bug-bounty.md` | Log belajar: pelajaran putaran lalu, rencana 70-20-10, target |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal/putaran) dengan format:

```
Tanggal putaran: [YYYY-MM-DD]
Pelajaran putaran lalu: [pelajaran ... — rujukan kejadian: ...]
Rencana 70-20-10: [70%: ... | 20%: ... | 10%: ...]
Write-up dipelajari: [judul/sumber ... — teknik ... — relevansi: ...]
Target putaran: [realistis: ... — sikap duplicate/informational: ...]
Yang TIDAK dilakukan: [tanpa meniru serangan ke korban, tanpa belajar dari data breach]
Status: [rencana diserahkan]
```

## Batasan yang diketahui

- Rasio 70-20-10 adalah PANDUAN, bukan hukum: bila putaran ini butuh lebih banyak teori (teknik baru yang belum dipahami), porsi teori boleh naik — catat alasannya, jangan kaku.
- Write-up publik sering menyembunyikan detail penting (langkah yang dihilangkan, kondisi khusus target). Jangan menganggap write-up sebagai resep yang bisa disalin mentah — sesuaikan dengan target kita.
- Belajar dari kegagalan hanya bekerja bila kegagalan DICATAT dengan jujur. Putaran yang "gagal total" tanpa catatan pelajaran = waktu yang terbuang dua kali.
- Skill ini tidak membahas motivasi personal atau manajemen waktu manusia — itu urusan Cipta dan tim manusia. Untuk agen, "konsistensi" berarti: rencana belajar dijalankan tiap putaran tanpa terlewat.
