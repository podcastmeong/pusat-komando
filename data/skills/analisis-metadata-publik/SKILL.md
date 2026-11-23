# Skill: Analisis Metadata Publik — Metadata dokumen publik yang membocorkan informasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 17. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya dokumen publik; tanpa data pribadi.

## Pemicu (kapan dipakai)

Dipakai saat memeriksa dokumen PUBLIK milik target in-scope (foto, PDF, dokumen Office yang dipublikasikan target sendiri): apakah metadata-nya (EXIF foto, metadata PDF/Office) membocorkan pengguna, perangkat, lokasi, atau jalur internal yang seharusnya tidak publik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Jejak digital perusahaan → skill `jejak-digital-perusahaan-publik` (No. 16).
- Pemantauan kebocoran kredensial → skill `pemantauan-kebocoran-kredensial` (No. 12).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Hanya dokumen PUBLIK** — dokumen yang target publikasikan sendiri atau yang tersedia bebas di sumber publik. Jangan mengakses dokumen yang tidak publik atau yang diperoleh tanpa izin.
12. **Tanpa data pribadi.** Bila metadata memuat data pribadi seseorang (nama, lokasi rumah, perangkat pribadi), catat HANYA jenis kebocorannya (mis. 'EXIF memuat koordinat') dan laporkan — jangan menyalin, menyebarkan, atau memakai data pribadi itu.

## Langkah + gerbang

### Gerbang 0 — Cek scope + dokumen yang akan diperiksa

1. Tetapkan dokumen publik target in-scope yang akan diperiksa (URL/sumber publik) dan baca pasal scope.
2. **Standar lulus:** daftar dokumen + sumber tercatat. Dokumen yang tidak publik = jangan diperiksa.

### Gerbang 1 — Ekstrak metadata

1. Unduh salinan dokumen publik dan ekstrak metadata-nya (EXIF foto; properti PDF/Office: pembuat, perangkat lunak, jalur file, riwayat revisi bila ada). Simpan di lingkungan terkendali milik sendiri.
2. **Standar lulus:** metadata tiap dokumen tercatat. Dokumen tanpa metadata = dicatat "tidak ada metadata".

### Gerbang 2 — Nilai kebocoran

1. Periksa tiap field metadata: apakah membocorkan informasi sensitif (nama pengguna internal, perangkat, lokasi, jalur direktori internal, versi perangkat lunak)? Bedakan informasi yang memang wajar publik dari yang seharusnya tidak publik.
2. **Standar lulus:** tiap field sensitif tercatat dengan jenisnya (bukan nilai utuh bila berupa data pribadi). Tidak ada kebocoran = catat "bersih pada dokumen ini".

### Gerbang 3 — Nilai dampak + tulis draf

1. Tulis metadata apa yang bocor dan apa yang bisa dilakukan dengan informasi itu (mis. jalur internal membantu penebakan struktur server). Serahkan ke A60 untuk audit.
2. **Standar lulus:** dampak ditulis konkret, draf mengikuti format output, dan status triase diputuskan A60.

## Alat

| Alat | Cara pakai |
|---|---|
| exiftool / penampil metadata | Mengekstrak EXIF dan metadata PDF/Office dari dokumen publik |
| Salinan dokumen publik | Satu-satunya dokumen yang diperiksa |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Dokumen diperiksa: [URL/sumber publik]
Metadata sensitif: [field + jenis kebocoran — tanpa nilai pribadi utuh]
Dampak: [apa yang bisa dilakukan dengan info itu]
Scope guard dipatuhi: [ya — Scope guard: hanya dokumen publik; tanpa data pribadi.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Metadata sering dibersihkan otomatis saat dokumen diunggah ke platform — ketiadaan metadata pada satu salinan bukan bukti dokumen aslinya bersih.
- Jalur file internal di metadata adalah petunjuk, bukan bukti kerentanan — gabungkan dengan temuan lain sebelum mengklaim dampak.
