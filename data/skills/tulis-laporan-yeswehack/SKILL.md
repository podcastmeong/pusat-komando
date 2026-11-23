# Skill: Tulis Laporan YesWeHack — Struktur 7 Seksi (Draf Hanya dari Fakta Terverifikasi)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah format pelaporan dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 69; YesWeHack Claude Kit, skill `write`, https://www.yeswehack.com/learn-bug-bounty/triager-grade-reports-claude-code), bukan pengalaman teruji sampai ada laporan berformat ini yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Temuan sudah terkonfirmasi (lolos `gerbang-tujuh-pertanyaan-triase` + `skeptic-false-positive-eliminator`) dan akan dilaporkan ke YesWeHack (atau platform yang menerima struktur ini).
- Draf laporan perlu disusun dari fakta yang sudah diverifikasi — bukan dari ingatan atau dugaan.
- Dipakai SETELAH bukti lengkap; skill ini menulis laporan, bukan mencari bukti.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menyusun draf 7 seksi dari fakta terverifikasi |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Struktur laporan umum (abstrak + ringkasan) → skill `laporan-abstrak`.
- Laporan PoC terstruktur (repro curl/Python + saran perbaikan) → skill `laporan-poc-otomatis`.
- Skor keparahan → skill `penilaian-cvss`; artikulasi dampak bisnis → skill `artikulasi-dampak-bisnis`.
- Simulasi triase pra-kirim (verdict READY/NEEDS FIXES/DO NOT SUBMIT) → skill `simulasi-triase-pra-kirim` — jalankan SEBELUM mengirim draf dari skill ini.
- Katalog jebakan per kelas (ambang bukti minimum) → skill `jebakan-per-kelas-kerentanan` — cek kelas temuan di sana SEBELUM menulis seksi PoC/Impact.
- Skill ini HANYA format khusus YesWeHack + aturan anti-karangnya. YesWeHack sebagai platform tidak disebut di satu pun skill yang ada sebelum skill ini dibuat.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan program YesWeHack yang dituju in-scope sebelum draf ditulis.
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

### Gerbang 1 — Kumpulkan fakta dulu, tulis kemudian (aturan anti-karang)

**Prinsip inti YesWeHack: draf HANYA dari fakta terverifikasi — jangan isi celah dengan karangan.** Sebelum menulis satu seksi pun, kumpulkan: langkah reproduksi yang sudah dijalankan, log HTTP mentah (reference ID saja yang diberikan ke LLM saat menyusun), screenshot/log tersensor, dan keputusan gerbang triase. Bila ada fakta yang KURANG (mis. dampak belum terbukti, langkah repro ada yang belum dijalankan ulang): **TANYAKAN / lengkapi dulu — jangan dikarang.** Standar lulus: daftar fakta per seksi tertulis; tiap klaim di draf bisa dilacak ke satu fakta di daftar itu. Klaim tanpa fakta = HAPUS dari draf, bukan dipertahankan.

### Gerbang 2 — Tulis 7 seksi (aturan per seksi)

| # | Seksi | Aturan |
|---|---|---|
| 1 | Description | Apa kerentanannya, di mana, dalam 1–2 paragraf. Tanpa klaim dampak di sini — dampak punya seksi sendiri. |
| 2 | Discovery | BAGAIMANA ditemukan (alur penemuan, bukan sekadar "saya menguji X"). Tulis apa yang diamati, bukan apa yang diasumsikan. |
| 3 | PoC | Langkah reproduksi lengkap yang bisa dijalankan ulang triager (cek ambang bukti minimum kelasnya di `jebakan-per-kelas-kerentanan` dulu). |
| 4 | Exploitation | Apa yang BISA dilakukan penyerang dengan kerentanan ini — hanya yang sudah dibuktikan atau yang mengikuti langsung dari PoC. Jangan ekstrapolasi. |
| 5 | Impact | Dampak nyata yang terbukti. **TOLAK menulis seksi ini bila dampak belum terbukti** — kosongkan dan tandai "dampak belum terbukti, butuh bukti tambahan", jangan tulis dampak teoretis. |
| 6 | Remediation | Saran perbaikan konkret (bukan "perbaiki keamanannya"). Satu saran per akar masalah. |
| 7 | References | Tautan/dokumen pendukung: halaman program, dokumentasi, writeup relevan. Tanpa referensi karangan. |

**Judul:** format `<kelas> in <lokasi> via <param/header>`, maksimal 100 karakter. Contoh pola: `IDOR in /api/orders via order_id`. **CVSS 3.1:** hanya metrik Base — TANPA Temporal/Environmental, agar skor tidak menggelembung. Standar lulus: ketujuh seksi ada; seksi 5 kosong bila dampak belum terbukti (bukan diisi teori); judul ≤100 karakter mengikuti format.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** tiap klaim dampak di seksi 5 punya bukti PoC. Klaim tanpa bukti = hapus.
2. **Reproduksibilitas deterministik — standar lulus:** PoC di seksi 3 sudah diulang minimal **3 kali** (perilaku LLM probabilistik) atau 1× deterministik untuk web klasik. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya draf yang lolos ketiga gerbang di atas yang diteruskan ke `simulasi-triase-pra-kirim` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar fakta terverifikasi (per seksi) | Dibuat di Gerbang 1; tiap klaim draf dilacak ke sini |
| Log HTTP mentah + screenshot tersensor | Bukti PoC; berikan hanya reference ID ke LLM saat menyusun |
| `jebakan-per-kelas-kerentanan` | Cek ambang bukti minimum kelas temuan sebelum menulis PoC/Impact |
| `simulasi-triase-pra-kirim` | Simulasi triager atas draf sebelum kirim |
| `~/workspace/catatan/log-bug-bounty.md` | Log draf + keputusan gerbang |

## Format output

Tulis draf ke `~/workspace/catatan/log-bug-bounty.md` (atau file draf laporan) dengan format:

```
# <kelas> in <lokasi> via <param/header>  (≤100 karakter)
## 1. Description
[..]
## 2. Discovery
[..]
## 3. PoC
[langkah reproduksi + reference ID log/screenshot]
## 4. Exploitation
[..]
## 5. Impact
[dampak terbukti — ATAU "dampak belum terbukti, butuh bukti tambahan"]
## 6. Remediation
[..]
## 7. References
[..]
CVSS 3.1 (Base saja): [skor + vektor]
Status: [draf / siap-triase / dikirim / ditolak]
```

## Batasan yang diketahui

- Format ini dari riset (YesWeHack Claude Kit), bukan pengalaman teruji — butuh satu laporan berformat ini yang lolos triase sebelum label BELUM DIUJI dicabut.
- Aturan "tanya bila bukti kurang, jangan karang" adalah inti skill ini — draf yang mengarang fakta adalah penyebab laporan AI ditolak (lihat `aturan-laporan-selalu-aktif`).
- CVSS hanya Base — bila platform tujuan meminta Temporal/Environmental, itu pengecualian yang dicatat, bukan default.
