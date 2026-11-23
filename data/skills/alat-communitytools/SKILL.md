# Skill: Alat CommunityTools — Pantau Skill & Agen Pentest/Bounty dari Transilience

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini ditulis dari ringkasan artikel "Top 43 AI Security Skills" (14 Sep 2026, diringkas 23 Nov 2026) dan belum pernah dipakai dalam perburuan nyata. Semua langkah di bawah adalah rencana pemantauan, bukan prosedur yang sudah terbukti jalan.

## Kapan dipakai (pemicu)

- Saat ada waktu riset yang disisihkan untuk memantau alat baru kategori "Worth watching" dari artikel Top 43 AI Security Skills.
- Saat tim butuh menilai skill dan agen Claude Code open-source untuk pentesting dan bounty.
- Saat muncul skill baru dari lengan komunitas perusahaan keamanan (Transilience) yang patut diawasi.

## Pemilik

**A70 Automation Engineer** — memantau repo, menilai kelayakan skill-skill di dalamnya, dan melaporkan ke Muse. A70 TIDAK memutuskan adopsi sendiri; keputusan adopsi ada di Muse dan Cipta.

## Tentang alat ini

- **Nama:** communitytools
- **Pembuat:** transilienceai
- **Bintang GitHub:** ~530 (per Sep 2026)
- **Deskripsi artikel:** skill dan agen Claude Code open-source untuk pentesting dan bounty dari lengan komunitas perusahaan keamanan. Awasi untuk skill-skillnya.
- **Status:** PANTAU — yang diawasi terutama adalah skill-skill di dalamnya, bukan repo sebagai satu paket. Bukan andalan tim saat ini.

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
10. Jangan install atau jalankan skill/agen dari communitytools sebelum lolos gerbang 1–3 di bawah. Memantau repo (baca daftar skill, rilis, isu) TIDAK sama dengan memakai isinya.
11. Setiap skill di dalam repo dinilai SENDIRI-SENDIRI — satu skill yang lolos gerbang tidak berarti skill lain ikut lolos. Jangan adopsi paket sekaligus tanpa memeriksa tiap skill.

## Langkah + gerbang

### Gerbang 1 — Cek status repo + inventaris skill (tiap pemantauan)

- **Lakukan:** buka repo GitHub communitytools (transilienceai/communitytools), catat tanggal push terakhir, rilis terakhir, dan DAFTAR skill/agen yang ada di dalamnya (nama + satu baris fungsi tiap skill).
- **Standar lulus:** repo masih aktif (push dalam 3 bulan terakhir) dan daftar skill tercatat di log. Bila push terakhir >6 bulan: turunkan status jadi "STALLED — awasi saja", jangan lanjut ke gerbang 2.

### Gerbang 2 — Baca skill sebelum pakai (per skill, sebelum instalasi apa pun)

- **Lakukan:** pilih SATU skill yang paling relevan dengan program kita, baca isi lengkapnya (SKILL.md / prompt / instruksi). Periksa apakah skill itu memerintahkan sesuatu yang melanggar aturan keras (otomasi di program yang melarang, uji korban, payload publik). Pindai dengan SkillSpector bila tersedia — ini WAJIB untuk skill dari pihak ketiga.
- **Standar lulus:** isi skill jelas, tidak ada instruksi tersembunyi atau perintah yang melanggar aturan keras. Bila ada yang mencurigakan: STOP untuk skill itu, laporkan ke Muse, jangan install. Skill lain tetap dinilai terpisah.

### Gerbang 3 — Uji di lingkungan buang (sebelum menyentuh target nyata)

- **Lakukan:** jalankan skill yang lolos gerbang 2 di container/VM yang bisa dibuang, hanya terhadap target lab milik sendiri.
- **Standar lulus:** skill berjalan sesuai klaimnya, output bisa diverifikasi manusia, dan tidak ada trafik keluar yang tidak dijelaskan. Bila gagal: catat penyebabnya, perbaiki atau hentikan — jangan memaksa.

### Gerbang 4 — Uji temuan ke program in-scope

- **Lakukan:** bila gerbang 3 lulus, uji SATU temuan yang dihasilkan skill itu terhadap SATU program in-scope, dengan validasi manusia penuh.
- **Standar lulus:** temuan terverifikasi manual sebagai nyata dan in-scope. Bila tidak: skill itu tetap berstatus pantau.

### Gerbang 5 — Keputusan naik status (per skill)

- **Lakukan:** laporkan hasil gerbang 1–4 ke Muse. Keputusan naik dari "pantau" jadi "andalan" dibuat PER SKILL, bukan per repo — HANYA bila gerbang 4 lulus dan Muse menyetujuinya.
- **Standar lulus:** ada persetujuan tertulis Muse di log, menyebut nama skill yang disetujui. Tanpa itu, status tetap "pantau".

## Status pemantauan — apa yang dipantau dan kapan naik jadi andalan

| Yang dipantau | Sinyal naik | Sinyal turun |
|---|---|---|
| Aktivitas repo (push, rilis, isu) | Rilis baru + skill baru ditambahkan | Push berhenti >6 bulan |
| Inventaris skill di dalam repo | Ada skill baru yang relevan dengan program kita | Tidak ada skill baru yang relevan |
| Hasil uji per skill (gerbang 3) | Skill jalan sesuai klaim di lab | Skill error / tidak sesuai klaim |
| Kesesuaian dengan program kita | Temuan dari satu skill lolos di 1 program in-scope | Tidak ada temuan yang lolos |

**Skill ini (atau satu skill di dalamnya) naik jadi andalan bila:** gerbang 4 lulus untuk skill tersebut (temuan nyata terverifikasi di program in-scope) DAN Muse menyetujui skill itu dengan nama. Sampai saat itu, communitytools tetap repo yang dipantau, bukan alat kerja harian — dan adopsi selalu per skill, tidak pernah sepaket.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| communitytools | GitHub: transilienceai/communitytools | Baca daftar skill di repo; instalasi dan pemakaian mengikuti dokumentasi resmi repo (BELUM DIUJI — jangan jadikan petunjuk di sini sebagai prosedur teruji). Jalankan hanya di container/VM yang bisa dibuang. |
| SkillSpector | GitHub: NVIDIA/SkillSpector | Pindai skill/alat sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. WAJIB untuk skill pihak ketiga. |

## Format output

- **Log pemantauan** ke `~/workspace/catatan/log-bug-bounty.md` — satu baris per pengecekan: tanggal, versi/rilis repo, tanggal push terakhir, status (AKTIF/STALLED), daftar skill baru bila ada, dan catatan singkat.
- **Laporan penilaian** (bila gerbang 2–4 dijalankan) ke file yang sama: nama skill yang dinilai, hasil tiap gerbang (LULUS/GAGAL + bukti), dan rekomendasi per skill (tetap pantau / naik jadi andalan / hentikan pantau).
- **Laporan temuan bounty** mengikuti alur biasa: draf oleh A70 → Muse putuskan → Cipta setuju → baru dikirim. Tanpa persetujuan Cipta, tidak ada laporan yang dikirim.
