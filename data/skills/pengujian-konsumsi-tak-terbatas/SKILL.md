# Skill: Pengujian Konsumsi Tak Terbatas — Pengukuran Terbatas DoS/DoW pada Aplikasi LLM (TERKUNCI — Hanya Setelah Program Pembayar Terverifikasi)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` kandidat gabungan G3; OWASP LLM06:2026 Unbounded Consumption; Wraith Academy Modul 09, "Unbounded Consumption"), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

> **PERINGATAN — BACA SEBELUM MEMAKAI SKILL INI:**
> 1. **Posisi tim saat ini adalah DoS tidak dibayar.** Skill `buru-bug-bounty` mencatat DoS dalam daftar "JANGAN buang waktu pada yang TIDAK dibayar", dan `pacing-request-aman` menegaskan banjir request = DoS, bukan pengujian.
> 2. **Wraith menyebut DoS masuk scope 0din — klaim ini BELUM terverifikasi dari sumber primer 0din.** Jangan percaya klaim itu tanpa verifikasi.
> 3. **Skill ini HANYA boleh dipakai setelah program in-scope yang benar-benar membayar kategori ini terverifikasi** dari sumber primer program itu (halaman scope program / platform bounty-nya), dicatat sumbernya di log, dan disetujui Cipta. Sampai saat itu, skill ini TERKUNCI: dipakai untuk memahami ancaman dan merancang pengukuran terbatas, BUKAN untuk menguji target live.
> 4. **Jangan klaim kategori ini berbayar.** Jangan tulis angka hadiah untuk kategori ini sebelum verifikasi butir 3 selesai.

## Pemicu (kapan dipakai)

- Program in-scope yang membayar unbounded consumption/DoS SUDAH terverifikasi dari sumber primer (Gerbang 1 lolos) — dan hanya untuk program itu.
- Ada hipotesis bahwa aplikasi LLM target tidak membatasi konsumsi (token, penalaran, rantai tool, ingestion) sehingga satu input bisa menghabiskan biaya/ketersediaan secara tidak proporsional.
- Dipakai untuk PENGUKURAN TERBATAS, bukan untuk menjatuhkan layanan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Memverifikasi program pembayar + menjalankan pengukuran terbatas |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pacing/ritme pengujian agar penguji tidak terblokir dan tidak membebani target → skill `pacing-request-aman`. Skill itu adalah KEBALIKAN arah skill ini (menjaga ritme, bukan menguji konsumsi) — baca dan patuhi batasnya sebelum memakai skill ini.
- Penjaga scope dan larangan DoS/stress testing → skill `scope-and-safety-guardian` + `buru-bug-bounty`.
- Rantai pemanggilan tool / penyalahgunaan tool → skill `penyalahgunaan-tool-agen` (itu soal tool yang disalahgunakan; skill ini soal RANTAI tool tanpa batas yang menghabiskan token/biaya).
- Skill ini HANYA menguji konsumsi tak terbatas sebagai kerentanan — tidak ada skill lain yang melakukannya (grep "unbounded" di seluruh skill = nol hasil sebelum skill ini dibuat).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). **DAN hanya bila program itu terverifikasi membayar kategori ini dari sumber primer** (Gerbang 1). Tanpa verifikasi itu, skill ini TERKUNCI.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — **aturan ini berlaku PENUH secara default dan hanya dilonggarkan sebatas pengukuran terbatas di Gerbang 2 SETELAH Gerbang 1 lolos.** Dilarang keras pengujian yang mengganggu ketersediaan layanan, menjatuhkan layanan, atau menghabiskan kuota token secara berlebihan — bahkan setelah Gerbang 1 lolos.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Verifikasi program pembayar (KUNCI — tanpa ini, STOP)

Sebelum pengujian apa pun: buktikan dari SUMBER PRIMER program (halaman scope program / platform bounty-nya, bukan dari Wraith, bukan dari artikel sekunder) bahwa kategori unbounded consumption / DoS / denial-of-wallet DIBAYAR oleh program in-scope tersebut. Catat: nama program, kutipan pasal scope-nya, URL sumber primer, tanggal cek. Bila sumber primer tidak menyebut kategori ini, atau hanya menyebutnya sebagai out-of-scope → **STOP. Skill TERKUNCI. Jangan menguji.** Bila verifikasi lolos → catat juga batasan program (mis. hanya pengukuran, larangan volume tertentu) dan patuhi batasan itu sebagai aturan tambahan. Standar lulus: kutipan sumber primer tercatat + persetujuan Cipta atas pemakaian skill ini untuk program itu.

### Gerbang 2 — Pengukuran terbatas (bukan serangan)

"When the attack is the bill": yang diuji adalah apakah SATU input wajar bisa memicu konsumsi yang tidak proporsional. Lima pola dari riset — uji SATU pola per putaran, dengan batas keras:

| # | Pola | Yang diukur | Batas keras pengukuran |
|---|---|---|---|
| U1 | Token floods (input raksasa) | Apakah input besar diterima tanpa batas token? | SATU input, ukuran wajar (jangan banjir berulang); hentikan bila respons mulai lambat |
| U2 | Generation runaway (penalaran mendalam / output tak berujung) | Apakah model menghasilkan output tanpa batas berhenti? | SATU prompt; hentikan (stop) segera setelah runaway teramati — jangan biarkan berjalan |
| U3 | Tool-call storms (rantai pemanggilan tool rekursif) | Apakah tool memanggil tool tanpa batas? | SATU rantai; hitung kedalaman panggilan, hentikan di ambang yang sudah ditentukan sebelum uji |
| U4 | Ingestion amplification (unggahan yang mengembang saat diproses) | Apakah satu unggahan kecil memicu pemrosesan besar? | SATU unggahan kecil milik sendiri |
| U5 | Model extraction (ekstraksi bertahap) | Apakah output bisa dipakai merekonstruksi model? | Pengukuran pasif atas output yang sudah diterima — tanpa banjir query |

Aturan pengukuran: (a) tentukan AMBANG BERHENTI sebelum uji (jumlah request, token, detik) dan berhenti di ambang itu walau belum terbukti; (b) ukur dari SATU akun uji sendiri, jangan dari banyak akun paralel; (c) catat metrik (token masuk/keluar, jumlah tool call, durasi) — metrik adalah bukti, bukan volume serangannya; (d) kenapa rate limit klasik gagal mendeteksinya: rate limit menghitung JUMLAH request, bukan BIAYA per request — satu request mahal lolos dari rate limit. Standar lulus: metrik tercatat + ambang berhenti dipatuhi + layanan tidak terganggu.

### Gerbang 3 — Bedakan temuan DoW dari pemakaian berat yang sah

Temuan DoW valid bila: satu input/aksi WAJAR (bukan banjir) memicu konsumsi yang TIDAK PROPORSIONAL (mis. satu prompt → ribuan tool call / token berlipat / biaya jauh di atas pemakaian normal) DAN tidak ada batas/circuit breaker yang menahannya. BUKAN temuan bila: konsumsi besar itu memang pemakaian yang diminta pengguna (mis. pengguna meminta ringkasan dokumen besar), atau ada batas yang bekerja (token cap, circuit breaker per agen, rate limit berbasis biaya). Standar lulus: perbandingan konsumsi normal vs konsumsi pemicu tercatat dengan angka.

### Gerbang 4 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** Valid = konsumsi tidak proporsional terbukti dengan metrik + tidak ada kontrol yang menahan + program tujuan terverifikasi membayar kategori ini (Gerbang 1). **TOLAK** = sekadar "respons lambat", pemakaian berat yang sah, atau program tidak membayar kategori ini.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengukuran minimal **3 kali** dengan input yang sama. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos keempat gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `peta-rute-program-ai-bounty` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `recon-pantau-program` | Verifikasi program pembayar dari sumber primer (Gerbang 1) |
| `pacing-request-aman` | Batas ritme + kondisi berhenti — patuhi sebelum dan selama pengukuran |
| Metrik konsumsi (token, tool call, durasi) | Bukti utama skill ini — catat per pengujian |
| Akun uji sendiri (satu akun) | Wajib — jangan pakai banyak akun paralel |
| `~/workspace/catatan/log-bug-bounty.md` | Log verifikasi program + metrik + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Program pembayar terverifikasi: [program + kutipan pasal scope + URL sumber primer + tanggal cek, atau "BELUM TERVERIFIKASI — skill TERKUNCI"]
Pola: [U1–U5 + deskripsi input]
Metrik: [token masuk/keluar] | [tool call: n] | [durasi: ..] | [pembanding normal: ..]
Ambang berhenti: [ditentukan sebelum uji: .. — dipatuhi ya/tidak]
Kontrol yang ada: [token cap / circuit breaker / rate limit berbasis biaya — ada/tidak + bukti]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [terkunci / diukur / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP LLM06:2026 + Wraith Modul 09), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Skill ini TERKUNCI sampai Gerbang 1 lolos.** Klaim Wraith bahwa DoS masuk scope 0din belum terverifikasi dari sumber primer 0din — jangan jadikan dasar pengujian.
- Pengukuran terbatas BUKAN serangan DoS — bila ambang berhenti dilanggar, pengukuran itu sendiri menjadi pelanggaran Aturan keras 5; hentikan dan catat.
- Rate limit klasik (jumlah request) tidak mendeteksi DoW (biaya per request) — kontrol yang dicari adalah batas token, circuit breaker per agen, dan rate limit berbasis biaya.
