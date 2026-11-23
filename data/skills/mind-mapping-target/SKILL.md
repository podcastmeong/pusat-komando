# Skill: Mind Mapping Target — Memvisualisasikan Struktur Aplikasi dan Attack Surface untuk Prioritas Pengujian

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 21 (artikel Medium "BUG-BOUNTY SERIES 5", tips produktivitas No. 4 Mind Mapping), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill PEMETAAN VISUAL — membuat mind map target in-scope (pusat = target, cabang = fitur/endpoint/komponen, ranting = titik uji) untuk memahami struktur aplikasi, menentukan area prioritas pengujian, dan mengidentifikasi attack surface yang terlewat. Skill ini BUKAN skill pengujian: tidak ada langkah menyerang di sini — hasilnya adalah peta visual + daftar prioritas yang dipakai skill pengujian lain.

## Pemicu

Dipakai pada tahap awal perburuan tiap target — SETELAH pemetaan permukaan (`pemetaan-permukaan-serangan`) dan peta alur (`cara-kerja-aplikasi-web`), SEBELUM pengujian dimulai. Dipakai juga di tengah putaran bila target ternyata lebih besar dari perkiraan dan prioritas perlu disusun ulang.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menyusun mind map target dari indeks aset + peta alur |
| Pengerjaan | **A58 Vulnerability Researcher** | Menandai cabang prioritas + titik uji pada peta |
| Audit | **A60 Security Auditor** | Memvalidasi peta (cabang yang tidak ada buktinya dicoret) |
| Pemimpin | **Muse** | Memutuskan prioritas cabang yang diuji duluan |

## Sudah tercakup (jangan diduplikat)

- Pemetaan permukaan serangan → skill `pemetaan-permukaan-serangan`. Skill ini MEMVISUALISASIKAN indeks itu sebagai mind map — bukan mengulang enumerasi.
- Peta alur aplikasi → skill `cara-kerja-aplikasi-web`. Skill ini memakai peta alur sebagai salah satu cabang mind map — bukan mengulang pembedahan request/response.
- Analisis mahkota permata (aset paling berharga) → skill `analisis-mahkota-permata`. Skill ini memakai hasilnya untuk menandai cabang prioritas — bukan mengulang analisisnya.
- Prioritas perburuan → skill `buru-bug-bounty` (induk). Skill ini memberi MASUKAN visual (cabang prioritas) ke prioritas itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Mind map disusun dari indeks aset + peta alur yang sudah ada — tidak ada pengumpulan baru atas data orang lain.
3. **Tanpa data orang lain.** Tanpa memasukkan data pengguna atau data pihak ketiga ke dalam peta.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Penyusunan peta tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Mind map hanya di log internal.
7. **Cabang tanpa bukti = coret.** Setiap cabang/ranting harus merujuk ke aset/alur yang sudah terpetakan — jangan menambahkan cabang dari tebakan.
8. **Validasi human-in-the-loop.** Mind map + prioritas harus diperiksa manusia (Muse/A60) sebelum dipakai.
9. **Tanpa laporan tanpa persetujuan Cipta.** Peta ini bahan kerja internal; temuan yang lahir darinya tetap lewat jalur draf → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai mind map untuk merencanakan serangan di luar scope bounty. Peta di sini HANYA untuk prioritas pengujian yang sah.

## Langkah + gerbang

### Gerbang 0 — Tentukan pusat + cabang utama

1. Pusat mind map = target (nama + program). Cabang utama = fitur/area besar aplikasi (mis. autentikasi, profil, pembayaran, API, admin) dari indeks aset + peta alur. Tulis dalam bentuk daftar berjenjang (teks) — format visual opsional, isi yang penting.
2. **Standar lulus:** pusat + cabang utama tertulis dengan sumber (indeks/peta alur). Cabang tanpa sumber = coret.

### Gerbang 1 — Uraikan ranting: endpoint + komponen per cabang

1. Untuk tiap cabang utama, uraikan ranting: endpoint, komponen, dan teknologi yang terlihat (dari `pemetaan-permukaan-serangan` + `cara-kerja-aplikasi-web`). Tandai ranting yang belum terpetakan penuh sebagai "belum diketahui" — jangan diisi tebakan.
2. **Standar lulus:** tiap cabang punya ranting + sumber. Ranting tanpa sumber = tandai "belum diketahui".

### Gerbang 2 — Tandai titik uji + area prioritas

1. Pada tiap ranting, tandai titik uji yang sudah diketahui (dari `cara-kerja-aplikasi-web` Gerbang 3) + tandai cabang prioritas: cabang yang memegang data sensitif/uang (lihat `analisis-mahkota-permata`) = prioritas tinggi; cabang yang sudah sering diuji tanpa hasil = prioritas turun.
2. **Standar lulus:** tiap cabang punya prioritas (tinggi/sedang/rendah) + alasan. Cabang tanpa prioritas = belum dinilai.

### Gerbang 3 — Periksa celah peta: cabang yang terlewat

1. Periksa peta secara keseluruhan: apakah ada area aplikasi yang tidak muncul di cabang mana pun? (mis. fitur lupa password, halaman bantuan, API lama). Area yang terlewat = kandidat recon tambahan — catat sebagai "butuh pemetaan" dan serahkan ke `pemetaan-permukaan-serangan`, jangan langsung diuji.
2. **Standar lulus:** daftar area terlewat tertulis (atau "tidak ada" dengan alasan). Tanpa pemeriksaan ini = peta belum lengkap.

### Gerbang 4 — Serahkan peta + prioritas ke perburuan

1. Serahkan mind map (teks berjenjang) + prioritas cabang ke koordinator putaran. Skill ini BERHENTI di sini.
2. **Standar lulus:** peta tercatat di log + prioritas tercatat. Skill ini tidak mencatat "temuan" — hanya "peta + prioritas diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `pemetaan-permukaan-serangan` | Indeks aset sebagai bahan cabang/ranting |
| `cara-kerja-aplikasi-web` | Peta alur sebagai bahan cabang/ranting |
| `analisis-mahkota-permata` | Penanda cabang prioritas (aset paling berharga) |
| Format teks berjenjang | Cara menulis mind map (pusat → cabang → ranting) — tanpa tool khusus |
| `~/workspace/catatan/log-bug-bounty.md` | Log mind map: struktur, prioritas, area terlewat |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Mind map:
  [Target]
  ├── [Cabang 1 — prioritas: ...] (sumber: ...)
  │   ├── [Ranting ... — titik uji: ...]
  │   └── [Ranting ... — belum diketahui]
  └── [Cabang 2 — prioritas: ...] (sumber: ...)
Area terlewat: [... — butuh pemetaan: ya/tidak]
Prioritas pengujian: [urutan cabang #1, #2, ... + alasan]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa cabang dari tebakan, tanpa pengujian di skill ini]
Status: [peta selesai / diserahkan]
```

## Batasan yang diketahui

- Mind map hanya sebagus bahan bakunya: bila indeks aset atau peta alur tidak lengkap, peta ini juga tidak lengkap. Perbarui peta bila bahan baku bertambah — jangan memakai peta lama yang sudah basi.
- Format teks berjenjang cukup untuk tim ini — tidak perlu tool mind-mapping khusus. Bila suatu hari dibutuhkan visual, itu keputusan terpisah.
- Prioritas cabang bersifat perkiraan awal: pengujian nyata bisa membuktikan cabang prioritas rendah ternyata menyimpan temuan. Tinjau ulang prioritas tiap putaran (lihat `intelijen-ancaman-berkala` + umpan balik putaran).
- Skill ini tidak membahas pemetaan arsitektur infrastruktur (jaringan/server) — lihat `audit-keamanan-cloud` + `pemetaan-permukaan-serangan` untuk itu. Fokus skill ini: struktur APLIKASI dan attack surface-nya.
