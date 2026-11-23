# Skill: Analisis Anomali — Membaca Pola dan Penyimpangan pada Sistem, Log, dan Perilaku

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 13 (ringkasan ethical hacking, "Kriptografi dan analisis anomali"), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill ANALISIS ANOMALI — membaca pola dan penyimpangan pada sistem yang diuji secara sah: membandingkan perilaku yang teramati dengan baseline yang diharapkan, menandai penyimpangan, dan mengubah penyimpangan itu menjadi hipotesis pengujian. Objek analisis HANYA: respons terhadap permintaan akun sendiri, log sesi pengujian sendiri, dan perilaku sistem di lab sendiri. Skill ini BUKAN skill memata-matai pengguna lain dan BUKAN skill membaca log milik siapa pun.

## Pemicu

Dipakai setiap kali ada perilaku sistem yang "terasa aneh" selama pengujian, atau secara sistematis saat memeriksa hasil pengujian: bandingkan apa yang terjadi dengan apa yang seharusnya terjadi. Dipakai SETELAH pemetaan alur (`cara-kerja-aplikasi-web`) dan SEBELUM merumuskan hipotesis pengujian. Dipakai juga di dalam `respons-insiden-forensik` (Gerbang 1) untuk menandai titik anomali di timeline.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menetapkan baseline + menandai penyimpangan; merumuskan hipotesis dari anomali |
| Audit | **A60 Security Auditor** | Memvalidasi bahwa anomali benar-benar penyimpangan (bukan perilaku normal yang salah paham) |
| Pemimpin | **Muse** | Memutuskan anomali mana yang jadi hipotesis pengujian |

## Sudah tercakup (jangan diduplikat)

- Deteksi drift perilaku agen → skill `deteksi-agen-nakal`. Skill itu khusus DRIFT AGEN dari waktu ke waktu; skill ini umum — anomali pada sistem/log/respons apa pun.
- Anomali perilaku model lab → skill `racun-data-model-pelatihan` (butir c). Skill itu khusus perilaku MODEL; skill ini umum.
- Deteksi anomali login akun sendiri → skill `serangan-okta-idp` (butir kebijakan password). Skill itu khusus ambang login; skill ini umum.
- Penanda titik anomali di timeline forensik → skill `respons-insiden-forensik`. Skill ini adalah METODE menandai anomali itu — dipakai bersama, bukan duplikat.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu + lab sendiri.** Anomali yang dianalisis HANYA dari interaksi akun sendiri atau lab sendiri. Tanpa data orang lain.
3. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
4. **Tanpa DoS/DDoS.** Jangan membanjiri target untuk "memancing anomali".
5. **Tanpa payload di permukaan publik.** Daftar anomali + hipotesis hanya di log internal dan jalur resmi program.
6. **Anomali ≠ temuan.** Penyimpangan dari baseline adalah HIPOTESIS, bukan bukti celah. Jangan mengklaim temuan hanya dari satu anomali tanpa validasi.
7. **Validasi human-in-the-loop.** Setiap anomali yang jadi hipotesis harus diperiksa manusia (Muse/A60) — banyak anomali ternyata perilaku normal.
8. **Tanpa laporan tanpa persetujuan Cipta.** Anomali yang berujung temuan tetap lewat jalur draf → Cipta.
9. **Patuhi larangan otomasi program** — huntr "Humans only"; Gray Swan dilewati total.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai analisis anomali untuk mengintip perilaku pengguna lain, membaca log orang lain, atau mengeksploitasi penyimpangan untuk mengakses data orang lain. Analisis di sini HANYA atas interaksi akun sendiri.

## Langkah + gerbang

### Gerbang 0 — Tetapkan baseline yang diharapkan

1. Sebelum mencari anomali, tulis baseline: apa yang SEHARUSNYA terjadi pada tiap langkah alur (dari `cara-kerja-aplikasi-web` + dokumentasi publik target)? Baseline mencakup: status respons yang diharapkan, waktu respons yang wajar, isi respons yang konsisten, dan perilaku sesi yang normal.
2. **Standar lulus:** baseline tertulis per langkah alur. Tanpa baseline = tidak ada pembanding, jangan mencari anomali.

### Gerbang 1 — Amati + catat perilaku teramati

1. Jalani alur dengan akun sendiri dan catat perilaku teramati per langkah: status, isi, waktu, dan perubahan sesi. Catat APA ADANYA — tanpa menafsirkan dulu.
2. **Standar lulus:** catatan perilaku teramati per langkah. Catatan tanpa baseline tandingan = belum bisa dinilai.

### Gerbang 2 — Bandingkan + tandai penyimpangan

1. Bandingkan teramati vs baseline, tandai penyimpangan dalam 5 jenis: (a) status berbeda (mis. 200 padahal seharusnya 403); (b) isi berbeda (data yang seharusnya tidak ada, muncul); (c) waktu berbeda jauh (terlalu cepat/lambat tanpa alasan); (d) sesi berbeda (token tidak berubah padahal seharusnya berubah, atau sebaliknya); (e) urutan berbeda (langkah bisa dilewati/dibalik).
2. Beri tiap penyimpangan tingkat kecurigaan (rendah/sedang/tinggi) + alasan.
3. **Standar lulus:** tiap penyimpangan punya jenis + tingkat + alasan. Penyimpangan tanpa jenis = belum diklasifikasikan.

### Gerbang 3 — Saring anomali palsu + rumuskan hipotesis

1. Untuk tiap penyimpangan tingkat SEDANG/TINGGI, periksa dulu penjelasan normalnya: apakah ini caching? Apakah ini perilaku yang memang didokumentasikan? Apakah ini terjadi juga di akun lain yang sejenis (milik sendiri)? Bila ada penjelasan normal → coret dengan alasan. Bila tidak ada → rumuskan hipotesis satu kalimat + skill pengujian yang sesuai.
2. Serahkan hipotesis ke A60 untuk validasi. Skill ini BERHENTI di sini.
3. **Standar lulus:** tiap penyimpangan punya verdict (coret + alasan / hipotesis + skill) + validasi A60. Penyimpangan tanpa verdict = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| `cara-kerja-aplikasi-web` | Peta alur + baseline perilaku yang diharapkan |
| Akun uji sendiri + log sesi pengujian sendiri | Satu-satunya sumber perilaku teramati |
| `respons-insiden-forensik` | Pemakai hasil skill ini (penanda anomali di timeline) |
| `skeptic-false-positive-eliminator` | Penyaring hipotesis anomali sebelum jadi temuan |
| `~/workspace/catatan/log-bug-bounty.md` | Log anomali: baseline, teramati, penyimpangan, hipotesis |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Baseline: [langkah ... — diharapkan: ...]
Teramati: [langkah ... — terjadi: ...]
Penyimpangan: [jenis (a/b/c/d/e) — tingkat: rendah/sedang/tinggi — alasan]
Saring: [coret: ... + alasan normal | hipotesis: ... — skill: ...]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa data/log orang lain, anomali bukan klaim temuan]
Status: [analisis selesai / hipotesis diserahkan]
```

## Batasan yang diketahui

- Baseline dari luar bisa salah: dokumentasi publik bisa kedaluwarsa dan perilaku "normal" bisa tidak terdokumentasi. Bila baseline diragukan, nyatakan keraguannya — jangan memaksakan verdict anomali.
- Satu anomali bisa punya banyak penjelasan normal (caching, A/B testing, perbedaan region, beban server). Selalu cari penjelasan normal dulu sebelum merumuskan hipotesis.
- Anomali waktu (terlalu cepat/lambat) adalah sinyal paling lemah — jaringan dan beban server mengubah waktu respons tanpa ada celah. Jangan jadikan waktu sebagai satu-satunya bukti.
- Skill ini tidak membahas deteksi anomali otomatis (machine learning atas log besar) — itu pekerjaan alat SIEM/defender, bukan hunter. Analisis di sini manual, atas interaksi akun sendiri.
