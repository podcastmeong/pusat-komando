# Skill: Simulasi Triase Pra-Kirim — Triager Senior yang Ketat atas Draf Sendiri (PELENGKAP, Bukan Pengganti)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah simulasi triase dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 71; YesWeHack Claude Kit, skill `triage`, https://www.yeswehack.com/learn-bug-bounty/triager-grade-reports-claude-code), bukan pengalaman teruji sampai ada draf yang lolos simulasi ini lalu lolos triase nyata dan dicatat di log. Label ini berlaku untuk semua bagian.

> **POSISI SKILL INI: PELENGKAP, BUKAN PENGGANTI.** Fungsi "validasi sebelum laporan" sudah tercakup oleh `gerbang-tujuh-pertanyaan-triase` (7 pertanyaan) dan `skeptic-false-positive-eliminator` (default TOLAK, 4 gerbang). Skill ini TIDAK menggantikan keduanya — jalankan keduanya DULU. Bagian yang benar-benar baru di skill ini hanyalah: (a) daftar cek deteksi AI-slop pada draf sendiri, dan (b) taksonomi verdict tiga tingkat READY / NEEDS FIXES / DO NOT SUBMIT beserta perbaikan berprioritas. Jangan memakai skill ini sebagai satu-satunya validasi.

## Pemicu (kapan dipakai)

- Draf laporan sudah melewati `gerbang-tujuh-pertanyaan-triase` + `skeptic-false-positive-eliminator` dan akan disimulasikan sekali lagi dari sudut pandang triager senior yang ketat — SEBELUM kirim.
- Draf ditulis dengan bantuan AI dan perlu diperiksa apakah ciri tulisan LLM (AI-slop) bocor ke dalamnya.
- Dipakai sebagai langkah terakhir sebelum audit A60 + persetujuan Cipta.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menjalankan simulasi + memberi verdict + daftar perbaikan berprioritas |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Validasi 7 pertanyaan sebelum laporan → skill `gerbang-tujuh-pertanyaan-triase` — jalankan DULU, jangan diulang di sini.
- Filter penolakan default-TOLAK 4 gerbang → skill `skeptic-false-positive-eliminator` — jalankan DULU, jangan diulang di sini.
- Ambang bukti minimum + pola auto-close + jebakan overclaim per kelas → skill `jebakan-per-kelas-kerentanan` — dipakai di langkah 3 simulasi ini (bukan diulang).
- Format laporan YesWeHack 7 seksi → skill `tulis-laporan-yeswehack`.
- **Bagian baru skill ini (satu-satunya yang belum ada):** (a) daftar cek deteksi AI-slop pada draf sendiri; (b) taksonomi verdict tiga tingkat + perbaikan berprioritas Critical/Major/Minor.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan program tujuan in-scope sebelum simulasi.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya bukti dari akun uji milik sendiri.
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

### Langkah 1 — Prasyarat (bukan bagian simulasi)

Pastikan draf sudah lolos `gerbang-tujuh-pertanyaan-triase` DAN `skeptic-false-positive-eliminator`. Bila belum → kembali ke kedua skill itu; simulasi ini tidak boleh dipakai untuk menutupi kegagalan di sana. Standar lulus: kedua verdict pendahulu tercatat "lolos" di log.

### Langkah 2 — Daftar cek deteksi AI-slop pada draf sendiri [BAGIAN BARU]

Baca draf sebagai triager yang curiga draf ini ditulis LLM. Tandai tiap temuan slop — ciri tulisan LLM yang bocor ke laporan dan merusak kredibilitas hunter:

| # | Ciri AI-slop | Contoh | Perbaikan |
|---|---|---|---|
| S1 | Klaim tak berdasar | "Penyerang bisa mengambil alih seluruh sistem" tanpa PoC yang membuktikannya | Hapus klaim, atau buktikan dulu (lihat `jebakan-per-kelas-kerentanan`) |
| S2 | Boilerplate generik | Paragraf pembuka/penutup yang bisa ditempel ke laporan apa pun ("Keamanan adalah prioritas...") | Hapus; ganti dengan fakta spesifik temuan ini |
| S3 | Dampak teoretis | Dampak yang "mungkin terjadi" / "secara teori" tanpa rantai bukti | Pindahkan ke "dampak belum terbukti" atau hapus (aturan `tulis-laporan-yeswehack` seksi 5) |
| S4 | Detail yang dikarang untuk mengisi celah | Versi, parameter, atau langkah yang tidak ada di log pengujian | Hapus; tandai sebagai "butuh verifikasi" dan verifikasi dulu |
| S5 | Nada terlalu yakin pada hal yang belum diuji | "Terbukti rentan di semua endpoint" dari satu endpoint yang diuji | Turunkan ke yang teruji ("terbukti di endpoint X") |
| S6 | Pengulangan tanpa informasi baru | Seksi yang mengulang seksi lain dengan kata berbeda | Gabung/hapus |

Standar lulus: nol temuan slop tersisa di draf (tiap temuan S1–S6 sudah diperbaiki atau dihapus). Draf dengan slop yang dibiarkan = verdict otomatis NEEDS FIXES (bukan READY).

### Langkah 3 — Cek berurutan (validasi scope → reproduksibilitas PoC → gotchas per kelas)

1. **Validasi scope:** program + aset + kelas temuan benar-benar in-scope (cek ulang `parsing-scope-program` — jangan percaya ingatan).
2. **Reproduksibilitas PoC:** jalankan ulang PoC dari draf (minimal 3× untuk LLM, 1× deterministik untuk web klasik) — PoC yang tidak bisa dijalankan ulang dari drafnya sendiri = draf gagal.
3. **Gotchas per kelas:** cocokkan dengan `jebakan-per-kelas-kerentanan` — ambang bukti minimum, pola auto-close, jebakan overclaim.

Standar lulus: ketiga cek lolos. Satu cek gagal = NEEDS FIXES (bila bisa diperbaiki) atau DO NOT SUBMIT (bila tidak bisa).

### Langkah 4 — Verdict tiga tingkat [BAGIAN BARU] + perbaikan berprioritas

| Verdict | Arti | Syarat |
|---|---|---|
| READY | Kirim — draf layak triase | Langkah 1–3 lolos, nol slop, bukti lengkap |
| NEEDS FIXES | Perbaiki dulu, simulasi ulang | Ada kekurangan yang BISA diperbaiki (bukti kurang, slop, klaim berlebih) — sertakan daftar perbaikan berprioritas |
| DO NOT SUBMIT | Jangan kirim — draf ini akan ditolak | Temuan tidak valid / out-of-scope / duplikat / dampak tidak terbukti dan tidak bisa dibuktikan — kirim = buang kredibilitas |

Daftar perbaikan berprioritas (bila NEEDS FIXES): **Critical** (tanpanya laporan ditolak: bukti minimum tidak terpenuhi, out-of-scope, klaim karangan); **Major** (menurunkan peluang dibayar: slop S1/S3/S5, PoC sulit direproduksi, judul tidak mengikuti format); **Minor** (kosmetik: boilerplate, pengulangan, format CVSS). Perbaiki Critical dulu, simulasi ulang; Major/Minor boleh diperbaiki dalam satu putaran. Standar lulus: verdict tercatat + alasan + daftar perbaikan (bila ada).

## Alat

| Alat | Cara pakai |
|---|---|
| `gerbang-tujuh-pertanyaan-triase` | Prasyarat — jalankan dulu |
| `skeptic-false-positive-eliminator` | Prasyarat — jalankan dulu |
| `jebakan-per-kelas-kerentanan` | Cek gotchas per kelas (Langkah 3.3) |
| Daftar cek AI-slop S1–S6 di atas | Bagian baru skill ini |
| `~/workspace/catatan/log-bug-bounty.md` | Log verdict + daftar perbaikan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Draf: [judul laporan + program tujuan]
Prasyarat: [gerbang-tujuh: lolos] [skeptic: lolos]
AI-slop: [S1: tidak ada / diperbaiki: ..] [S2: ..] [S3: ..] [S4: ..] [S5: ..] [S6: ..]
Cek berurutan: [scope: lolos/gagal] [repro PoC: lolos/gagal] [gotchas: lolos/gagal]
Verdict: [READY / NEEDS FIXES / DO NOT SUBMIT + alasan]
Perbaikan: [Critical: ..] [Major: ..] [Minor: ..]
Status: [disimulasi / diperbaiki-simulasi-ulang / siap-kirim / jangan-kirim]
```

## Batasan yang diketahui

- Simulasi ini dari riset (YesWeHack Claude Kit, skill `triage`), bukan pengalaman teruji — butuh draf yang lolos simulasi lalu lolos triase nyata sebelum label BELUM DIUJI dicabut.
- Simulasi bukan triase nyata — triager manusia bisa menolak hal yang lolos simulasi (mis. duplikat yang tidak terlihat dari luar). Verdict READY bukan jaminan dibayar.
- Skill ini PELENGKAP `gerbang-tujuh-pertanyaan-triase` + `skeptic-false-positive-eliminator` — jangan dipakai sendirian sebagai satu-satunya validasi.
