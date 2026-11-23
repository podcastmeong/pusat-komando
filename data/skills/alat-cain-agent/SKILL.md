# Skill: Alat Cain-Agent — Pantau Agen Pentest AI + Cloud

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini ditulis dari ringkasan artikel "Top 43 AI Security Skills" (14 Sep 2026, diringkas 23 Nov 2026) dan belum pernah dipakai dalam perburuan nyata. Semua langkah di bawah adalah rencana pemantauan, bukan prosedur yang sudah terbukti jalan.

## Kapan dipakai (pemicu)

- Saat ada waktu riset yang disisihkan untuk memantau alat baru kategori "Worth watching" dari artikel Top 43 AI Security Skills.
- Saat tim butuh menilai apakah agen pentest AI dengan modul cloud layak diadopsi untuk perburuan bounty.
- Saat muncul kebutuhan pentest permukaan cloud (AWS, Azure, GCP, Aliyun/Tencent/Huawei) yang tidak tercakup alat yang sudah dipakai.

## Pemilik

**A70 Automation Engineer** — memantau repo, menilai kelayakan, dan melaporkan ke Muse. A70 TIDAK memutuskan adopsi sendiri; keputusan adopsi ada di Muse dan Cipta.

## Tentang alat ini

- **Nama:** cain-agent
- **Pembuat:** cdxiaodong
- **Bintang GitHub:** ~950 (per Sep 2026)
- **Deskripsi artikel:** "real-world AI penetration testing engineer" — agen AI pentest dengan modul cloud (AWS, Azure, GCP, Aliyun/Tencent/Huawei).
- **Status:** PANTAU — agen AI + permukaan cloud adalah taruhan yang layak diawasi. Bukan andalan tim saat ini.

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
10. Jangan install atau jalankan cain-agent sebelum lolos gerbang 1–3 di bawah. Memantau repo (baca README, rilis, isu) TIDAK sama dengan memakai alatnya.

## Langkah + gerbang

### Gerbang 1 — Cek status repo (tiap pemantauan)

- **Lakukan:** buka repo GitHub cain-agent (cdxiaodong/cain-agent), catat tanggal push terakhir, rilis terakhir, jumlah isu terbuka, dan apakah README masih menjelaskan modul cloud yang sama.
- **Standar lulus:** repo masih aktif (push dalam 3 bulan terakhir) dan README/dokumentasi masih tersedia. Bila push terakhir >6 bulan: turunkan status jadi "STALLED — awasi saja", jangan lanjut ke gerbang 2.

### Gerbang 2 — Baca sebelum pakai (sebelum instalasi apa pun)

- **Lakukan:** baca README, lisensi, dan daftar dependensi/modul cloud. Periksa apa yang dilakukan alat terhadap kredensial cloud dan data target. Pindai dengan SkillSpector bila tersedia (aturan supply-chain: skill/MCP/alat dari sumber anonim bisa berisi injeksi — cek dulu sebelum pakai).
- **Standar lulus:** tidak ada perilaku mencurigakan (eksfiltrasi kredensial, panggilan ke server tak dikenal, instruksi tersembunyi). Bila ada yang mencurigakan: STOP, laporkan ke Muse, jangan install.

### Gerbang 3 — Uji di lingkungan buang (sebelum menyentuh target nyata)

- **Lakukan:** jalankan cain-agent di container/VM yang bisa dibuang, hanya terhadap target milik sendiri (lab lokal / akun cloud sendiri, tanpa data orang lain).
- **Standar lulus:** alat berjalan tanpa error fatal, output-nya bisa dibaca dan diverifikasi manusia, dan tidak ada trafik keluar yang tidak dijelaskan. Bila gagal: catat penyebabnya, perbaiki atau hentikan — jangan memaksa.

### Gerbang 4 — Uji temuan ke program in-scope

- **Lakukan:** bila gerbang 3 lulus, uji SATU temuan yang dihasilkan alat terhadap SATU program in-scope, dengan validasi manusia penuh (human-in-the-loop).
- **Standar lulus:** temuan terverifikasi manual sebagai nyata dan in-scope. Bila tidak: alat tetap berstatus pantau, jangan jadikan andalan.

### Gerbang 5 — Keputusan naik status

- **Lakukan:** laporkan hasil gerbang 1–4 ke Muse. Keputusan naik dari "pantau" jadi "andalan" HANYA bila gerbang 4 lulus dan Muse menyetujuinya.
- **Standar lulus:** ada persetujuan tertulis Muse di log. Tanpa itu, status tetap "pantau".

## Status pemantauan — apa yang dipantau dan kapan naik jadi andalan

| Yang dipantau | Sinyal naik | Sinyal turun |
|---|---|---|
| Aktivitas repo (push, rilis, isu) | Rilis baru + perbaikan bug aktif | Push berhenti >6 bulan |
| Modul cloud (AWS/Azure/GCP/Aliyun/Tencent/Huawei) | Modul cloud terbukti jalan di lab sendiri | Modul cloud dihapus / tidak jalan |
| Hasil uji di lab (gerbang 3) | Temuan nyata terverifikasi | Hanya temuan palsu / error |
| Kesesuaian dengan program kita | Temuan lolos di 1 program in-scope | Tidak ada temuan yang lolos |

**Skill ini naik jadi andalan bila:** gerbang 4 lulus (temuan nyata terverifikasi di program in-scope) DAN Muse menyetujui. Sampai saat itu, cain-agent tetap alat yang dipantau, bukan alat kerja harian.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| cain-agent | GitHub: cdxiaodong/cain-agent | Baca README di repo; instalasi dan pemakaian mengikuti dokumentasi resmi repo (BELUM DIUJI — jangan jadikan petunjuk di sini sebagai prosedur teruji). Jalankan hanya di container/VM yang bisa dibuang. |
| SkillSpector | GitHub: NVIDIA/SkillSpector | Pindai skill/alat sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. |

## Format output

- **Log pemantauan** ke `~/workspace/catatan/log-bug-bounty.md` — satu baris per pengecekan: tanggal, versi/rilis repo, tanggal push terakhir, status (AKTIF/STALLED), dan catatan singkat.
- **Laporan penilaian** (bila gerbang 2–4 dijalankan) ke file yang sama: hasil tiap gerbang (LULUS/GAGAL + bukti), dan rekomendasi (tetap pantau / naik jadi andalan / hentikan pantau).
- **Laporan temuan bounty** mengikuti alur biasa: draf oleh A70 → Muse putuskan → Cipta setuju → baru dikirim. Tanpa persetujuan Cipta, tidak ada laporan yang dikirim.
