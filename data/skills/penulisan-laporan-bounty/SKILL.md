# Skill: Penulisan Laporan Bounty — Template per Platform & Nada Manusiawi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 58, Agentic-Bug-Hunter `report-writing` + Claude-BugHunter `report-writing`), bukan pengalaman teruji sampai ada laporan yang dibayar memakai template ini dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebuah temuan sudah lolos triase (`gerbang-tujuh-pertanyaan-triase` + `skeptic-false-positive-eliminator`) dan siap ditulis menjadi laporan.
- Perlu memilih template + nada yang tepat untuk platform tujuan (HackerOne, Bugcrowd, Intigriti, Immunefi).
- Dipakai SETELAH PoC terverifikasi (`verifikasi-poc-aman`, `laporan-poc-otomatis`) — skill ini menulis laporannya, bukan membuktikan temuannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menyusun draf laporan dari fakta terverifikasi |
| Audit | **A60 Security Auditor** | Memeriksa draf: fakta terverifikasi, dampak tidak menggelembung, CVSS benar |
| Pemimpin | **Muse** | Memutuskan draf mana yang maju ke persetujuan Cipta |

## Sudah tercakup (jangan diduplikat)

- **Struktur laporan PoC** (repro berupa curl/Python + saran perbaikan, perakitan draf otomatis) → skill `laporan-poc-otomatis`. Skill ini TIDAK mengulang perakitan PoC — hanya template per platform + nada + formula dampak.
- **Struktur laporan abstrak** (untuk program abstrak-dulu seperti 0din) → skill `laporan-abstrak`. Skill ini untuk platform laporan penuh (HackerOne/Bugcrowd/Intigriti/Immunefi), bukan abstrak.
- **Skor CVSS saja** → skill `penilaian-cvss`. Skill ini memakai skor itu di dalam template, bukan menghitung ulang metodenya.
- **Taksonomi VRT khusus Bugcrowd + sanggahan OOS** → skill `pelaporan-bugcrowd-vrt`. Skill ini template UMUM Bugcrowd; bila perlu berargumen soal kategori VRT atau klausul OOS, pakai skill itu.
- **Format khusus YesWeHack** (7 seksi + aturan anti-karang) → bukan bagian skill ini; bila targetnya YesWeHack, pakai panduan format platform itu (bila sudah ada sebagai skill, ikuti skill tersebut).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan program tujuan laporan adalah program in-scope yang sama dengan tempat temuan diuji.
2. **Hanya akun sendiri + canary palsu.** Semua bukti dalam laporan berasal dari akun uji sendiri.
3. **Tanpa data orang lain.** Sensor token, data pribadi, dan data pengguna lain sebelum melampirkan (`[REDACTED]`).
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — jangan klaim dampak DoS bila tidak diuji (dan jangan mengujinya).
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf boleh disiapkan; pengiriman HANYA setelah Cipta setuju. Berlaku untuk semua platform.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — jangan klaim dampak destruktif yang tidak dibuktikan secara aman.
11. **JANGAN PERNAH mengirim laporan otomatis ke platform mana pun.** Draf ditinjau manusia 2–3 menit sebelum submit (lihat `laporan-poc-otomatis` Aturan 7). Satu laporan halusinasi yang terkirim bisa merusak signal score/reputasi akun secara permanen.
12. **Draf HANYA dari fakta terverifikasi.** Jangan mengarang langkah reproduksi, dampak, atau angka. Bila bukti kurang, TANYAKAN / lengkapi dulu — jangan isi celah dengan karangan. Jangan tulis seksi Impact bila dampak belum terbukti.

## Langkah + gerbang

### Gerbang 1 — Pilih template per platform

| Platform | Struktur yang diharapkan | Catatan nada |
|---|---|---|
| HackerOne | Summary → Steps to Reproduce → Impact → Supporting Material (screenshot/video/log) | Langsung, faktual; severity diisi dari CVSS; lampirkan PoC yang bisa dijalankan ulang |
| Bugcrowd | Summary → Vulnerability details → Steps → Impact → Remediation (opsional) + VRT category | Pilih kategori VRT yang paling cocok (bila ragu, lihat `pelaporan-bugcrowd-vrt`); paragraf severity di awal bila default VRT meremehkan |
| Intigriti | Title → Description → Steps → Impact → Proof (video/screenshot) | Mirip HackerOne; tekankan reproduksibilitas |
| Immunefi (Web3) | Title → Project → Vulnerability details → PoC (Foundry, fork lokal) → Impact (jumlah terukur) | Angka WAJIB: jumlah dana yang berisiko + PoC yang bisa dijalankan; tanpa angka = kemungkinan besar ditolak |

### Gerbang 2 — Formula judul + pernyataan dampak

**Formula judul:** `[Kelas Kerentanan] in [Lokasi/Komponen] via [Parameter/Header/Fungsi]` — maksimal 100 karakter, spesifik, tanpa kata "critical" yang menggelembung.

- Baik: `Stored XSS in comment field via profile bio allows session hijack`
- Buruk: `Critical vulnerability in website` (tidak spesifik, menggelembung)

**Pernyataan dampak (impact-first):** paragraf pertama laporan HARUS menjawab: apa yang bisa dilakukan penyerang, terhadap siapa, dan seberapa besar — dalam 2–3 kalimat, tanpa jargon yang tidak perlu.

- Baik: "Penyerang tanpa login bisa mencuri sesi admin dengan mengirim tautan ke halaman komentar — satu klik admin, sesi diambil alih, seluruh data pengguna bisa diakses."
- Buruk: "Terdapat kerentanan XSS yang memungkinkan eksekusi skrip arbitrer yang dapat berdampak pada kerahasiaan, integritas, dan ketersediaan sistem." (generik, tidak ada skenario konkret)

### Gerbang 3 — Panduan keputusan severity + penangkal downgrade

1. **Tentukan severity dari DAMPAK, bukan dari kelas.** XSS stored di halaman admin ≠ XSS reflected di halaman publik. Pakai `penilaian-cvss` untuk skor, lalu cocokkan dengan tabel severity platform.
2. **Buktikan rantai dampak, bukan dampak teoritis.** "Bisa ATO" harus didukung langkah reproduksi sampai ke ATO pada akun uji sendiri — bila rantai berhenti di tengah, nyatakan dengan jujur sampai mana yang terbukti.
3. **Penangkal downgrade:** bila triager menurunkan severity, siapkan argumen berbasis FAKTA (bukan emosi): kutip langkah reproduksi yang menunjukkan dampak, bandingkan dengan laporan serupa yang dibayar (bila ada), dan tawarkan PoC tambahan — jangan berdebat tanpa bukti baru.
4. **Jangan menggelembung:** klaim massal butuh cara memperoleh ID/korban; klaim dana butuh angka likuiditas nyata; klaim RCE butuh eksekusi yang terbukti aman (bukan sekadar "payload terkirim"). Lihat `skeptic-false-positive-eliminator` dan `gerbang-sinyal-dampak`.

### Gerbang 4 — Checklist pra-pengiriman (wajib dicentang semua)

- [ ] Judul mengikuti formula + < 100 karakter
- [ ] Paragraf pertama = pernyataan dampak (impact-first)
- [ ] Langkah reproduksi lengkap + bisa dijalankan ulang oleh triager (akun uji sendiri, tanpa kredensial korban)
- [ ] CVSS 3.1 Base saja (tanpa Temporal/Environmental agar skor tidak menggelembung) — lihat `penilaian-cvss`
- [ ] Semua bukti disensor (`[REDACTED]` untuk token/data pribadi)
- [ ] Tidak ada klaim tanpa bukti; tidak ada boilerplate AI (lihat daftar cek AI-slop di bawah)
- [ ] Template sesuai platform tujuan (Gerbang 1)
- [ ] Draf ditinjau manusia 2–3 menit + disetujui Cipta (Aturan keras 8 dan 11)

**Daftar cek AI-slop (ciri tulisan LLM yang merusak kredibilitas):** klaim tanpa dasar ("sangat kritis", "dampak besar" tanpa angka), boilerplate generik ("kerentanan ini dapat berdampak pada kerahasiaan, integritas, dan ketersediaan"), dampak teoretis yang ditulis seolah terbukti, langkah reproduksi yang tidak bisa dijalankan ulang. Bila satu ciri ditemukan, perbaiki sebelum kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `laporan-poc-otomatis` | Perakitan draf PoC (repro curl/Python + saran perbaikan) |
| `penilaian-cvss` | Skor CVSS 3.1 Base |
| `artikulasi-dampak-bisnis` | Terjemahan dampak teknis ke risiko bisnis |
| `triase-duplikat` | Cek duplikat sebelum kirim |
| `pelaporan-bugcrowd-vrt` | Argumen VRT + sanggahan OOS khusus Bugcrowd |
| `~/workspace/catatan/log-bug-bounty.md` | Log draf laporan + keputusan gerbang |

## Format output

Tulis draf laporan ke file draf (bukan langsung ke platform) dengan format:

```
Platform: [HackerOne / Bugcrowd / Intigriti / Immunefi]
Judul: [<kelas> in <lokasi> via <param/header> — <100 karakter]
Dampak (paragraf pertama): [2–3 kalimat impact-first]
Langkah reproduksi: [langkah bernomor, bisa dijalankan ulang]
CVSS: [skor Base 3.1 + vektor]
Bukti: [daftar lampiran, semua disensor]
Checklist pra-kirim: [semua tercentang ya/tidak]
Status: [draf / ditinjau / disetujui Cipta / terkirim / dibayar / ditolak]
```

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter + Claude-BugHunter `report-writing`), bukan pengalaman teruji — template ini butuh satu laporan yang dibayar sebelum label BELUM DIUJI dicabut.
- Tiap platform mengubah format/ekspektasinya dari waktu ke waktu — periksa panduan pelaporan terbaru platform tujuan sebelum memakai template ini mentah-mentah.
- Nada "manusiawi" bukan berarti santai — tetap faktual, spesifik, dan tanpa basa-basi; triager menilai bukti, bukan gaya bahasa.
- Severity akhir ditentukan triager, bukan hunter — tugas skill ini adalah menyajikan dampak seterang mungkin dengan bukti, bukan memaksakan angka.
