# Skill: Alat DorkAgent — Pantau Google Dorking Otomatis Bertenaga LLM

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini ditulis dari ringkasan artikel "Top 43 AI Security Skills" (14 Sep 2026, diringkas 23 Nov 2026) dan belum pernah dipakai dalam perburuan nyata. Semua langkah di bawah adalah rencana pemantauan, bukan prosedur yang sudah terbukti jalan.

## Kapan dipakai (pemicu)

- Saat ada waktu riset yang disisihkan untuk memantau alat baru kategori "Worth watching" dari artikel Top 43 AI Security Skills.
- Saat tim butuh menilai apakah Google dorking otomatis bertenaga LLM layak dipakai untuk hunt dan pentest.
- Saat muncul kebutuhan recon permukaan web yang sempit dan terfokus (bukan sapu jagat).

## Pemilik

**A70 Automation Engineer** — memantau repo, menilai kelayakan, dan melaporkan ke Muse. A70 TIDAK memutuskan adopsi sendiri; keputusan adopsi ada di Muse dan Cipta.

## Tentang alat ini

- **Nama:** DorkAgent
- **Pembuat:** yee-yore
- **Bintang GitHub:** ~320 (per Sep 2026)
- **Deskripsi artikel:** Google dorking otomatis bertenaga LLM untuk hunt dan pentest. Scope sempit, dikerjakan bersih — agen fokus seperti ini yang benar-benar menghasilkan temuan.
- **Status:** PANTAU — layak diawasi karena fokus sempit dan bersih. Bukan andalan tim saat ini.

## Aturan keras

1. Hanya program bounty resmi in-scope (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. Hanya akun sendiri + canary palsu.
3. Tanpa data orang lain.
4. Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).
5. Tanpa DoS/DDoS.
6. Tanpa payload di permukaan publik.
7. Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).
8. Tanpa laporan tanpa persetujuan Cipta.
9. Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. Jangan install atau jalankan DorkAgent sebelum lolos gerbang 1–3 di bawah. Memantau repo (baca README, rilis, isu) TIDAK sama dengan memakai alatnya.
11. Dorking hanya terhadap target in-scope. Hasil dork yang menyingkap data orang lain TIDAK BOLEH disimpan, disebar, atau dipakai — laporkan ke Muse dan hapus.

## Langkah + gerbang

### Gerbang 1 — Cek status repo (tiap pemantauan)

- **Lakukan:** buka repo GitHub DorkAgent (yee-yore/DorkAgent), catat tanggal push terakhir, rilis terakhir, dan isu terbuka.
- **Standar lulus:** repo masih aktif (push dalam 3 bulan terakhir) dan dokumentasi masih tersedia. Bila push terakhir >6 bulan: turunkan status jadi "STALLED — awasi saja", jangan lanjut ke gerbang 2.

### Gerbang 2 — Baca sebelum pakai (sebelum instalasi apa pun)

- **Lakukan:** baca README dan daftar query/dork yang dihasilkan. Periksa apakah alat mengirim query ke layanan pihak ketiga dan data apa yang dikirim. Pindai dengan SkillSpector bila tersedia.
- **Standar lulus:** tidak ada perilaku mencurigakan (eksfiltrasi data, panggilan ke server tak dikenal). Bila ada yang mencurigakan: STOP, laporkan ke Muse, jangan install.

### Gerbang 3 — Uji di lingkungan buang (sebelum menyentuh target nyata)

- **Lakukan:** jalankan DorkAgent di container/VM yang bisa dibuang, hanya dengan query terhadap domain/target milik sendiri atau program in-scope.
- **Standar lulus:** alat berjalan, query yang dihasilkan relevan dan sempit (bukan sapu jagat), dan tidak ada trafik keluar yang tidak dijelaskan. Bila gagal: catat penyebabnya, perbaiki atau hentikan.

### Gerbang 4 — Uji temuan ke program in-scope

- **Lakukan:** bila gerbang 3 lulus, uji SATU temuan hasil dorking terhadap SATU program in-scope, dengan validasi manusia penuh.
- **Standar lulus:** temuan terverifikasi manual sebagai nyata dan in-scope. Bila tidak: alat tetap berstatus pantau.

### Gerbang 5 — Keputusan naik status

- **Lakukan:** laporkan hasil gerbang 1–4 ke Muse. Keputusan naik dari "pantau" jadi "andalan" HANYA bila gerbang 4 lulus dan Muse menyetujuinya.
- **Standar lulus:** ada persetujuan tertulis Muse di log. Tanpa itu, status tetap "pantau".

## Status pemantauan — apa yang dipantau dan kapan naik jadi andalan

| Yang dipantau | Sinyal naik | Sinyal turun |
|---|---|---|
| Aktivitas repo (push, rilis, isu) | Rilis baru + perbaikan aktif | Push berhenti >6 bulan |
| Kualitas dork yang dihasilkan | Dork sempit, relevan, menghasilkan temuan | Dork berisik / sapu jagat |
| Hasil uji di lab (gerbang 3) | Temuan nyata terverifikasi | Hanya noise / error |
| Kesesuaian dengan program kita | Temuan lolos di 1 program in-scope | Tidak ada temuan yang lolos |

**Skill ini naik jadi andalan bila:** gerbang 4 lulus (temuan nyata terverifikasi di program in-scope) DAN Muse menyetujui. Sampai saat itu, DorkAgent tetap alat yang dipantau, bukan alat kerja harian.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| DorkAgent | GitHub: yee-yore/DorkAgent | Baca README di repo; instalasi dan pemakaian mengikuti dokumentasi resmi repo (BELUM DIUJI — jangan jadikan petunjuk di sini sebagai prosedur teruji). Jalankan hanya di container/VM yang bisa dibuang. |
| SkillSpector | GitHub: NVIDIA/SkillSpector | Pindai skill/alat sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. |

## Format output

- **Log pemantauan** ke `~/workspace/catatan/log-bug-bounty.md` — satu baris per pengecekan: tanggal, versi/rilis repo, tanggal push terakhir, status (AKTIF/STALLED), dan catatan singkat.
- **Laporan penilaian** (bila gerbang 2–4 dijalankan) ke file yang sama: hasil tiap gerbang (LULUS/GAGAL + bukti), dan rekomendasi (tetap pantau / naik jadi andalan / hentikan pantau).
- **Laporan temuan bounty** mengikuti alur biasa: draf oleh A70 → Muse putuskan → Cipta setuju → baru dikirim. Tanpa persetujuan Cipta, tidak ada laporan yang dikirim.
