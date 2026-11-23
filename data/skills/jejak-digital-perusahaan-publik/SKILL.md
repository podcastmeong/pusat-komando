# Skill: Jejak Digital Perusahaan Publik — Jejak digital perusahaan dari sumber publik

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 16. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya sumber publik perusahaan; tanpa data pribadi karyawan.

## Pemicu (kapan dipakai)

Dipakai saat memahami permukaan target perusahaan dari sumber publik: domain, teknologi yang dipakai, lowongan pekerjaan, dan dokumen publik — untuk memahami apa saja yang dimiliki perusahaan sebelum berburu. Tanpa data pribadi karyawan dan tanpa doxxing.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis WHOIS/domain → skill `analisis-whois-domain` (No. 23).
- Pemetaan teknologi/stack → skill `pemetaan-teknologi-stack` (No. 11).
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
11. **Hanya sumber publik PERUSAHAAN.** Jangan mengumpulkan data pribadi karyawan (nama pribadi, email pribadi, nomor telepon pribadi, media sosial pribadi) — itu doxxing dan dilarang.
12. **Jangan menghubungi karyawan atau pihak perusahaan** untuk menggali informasi — pengumpulan hanya dari sumber publik yang sudah tersedia.

## Langkah + gerbang

### Gerbang 0 — Cek scope + perusahaan target

1. Tetapkan perusahaan target in-scope (nama + domain) dan baca pasal scope. Catat sumber publik yang akan dipakai.
2. **Standar lulus:** perusahaan + sumber tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Kumpulkan jejak dari sumber publik

1. Kumpulkan dari sumber publik perusahaan: domain dan subdomain yang diumumkan, teknologi yang terlihat dipakai, lowongan pekerjaan yang menyebut teknologi/produk, dokumen publik (laporan, presentasi, panduan publik).
2. **Standar lulus:** daftar jejak tertulis dengan sumber tiap item. Jejak tanpa sumber = jangan dipakai.

### Gerbang 2 — Petakan permukaan perusahaan

1. Susun peta: aset digital apa yang dimiliki perusahaan (situs, aplikasi, API, layanan), teknologi apa yang dipakai, dan area mana yang in-scope menurut program.
2. **Standar lulus:** peta permukaan tertulis + batas in-scope ditandai. Aset yang tidak in-scope = ditandai "di luar scope".

### Gerbang 3 — Serahkan prioritas

1. Serahkan peta ke A58 untuk diprioritaskan menjadi hipotesis pengujian. Jangan lanjut menguji dari peta ini tanpa gerbang skill pengujian terkait.
2. **Standar lulus:** daftar prioritas tertulis. Peta tanpa prioritas = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| Pencarian web (sumber publik) | Mengumpulkan jejak perusahaan dari sumber publik |
| Dokumen publik perusahaan | Laporan/panduan publik yang menyebut teknologi/aset |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Perusahaan: [nama + domain in-scope]
Jejak publik: [domain/teknologi/lowongan/dokumen + sumber]
Peta permukaan: [aset + batas in-scope]
Scope guard dipatuhi: [ya — Scope guard: hanya sumber publik perusahaan; tanpa data pribadi karyawan.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Lowongan pekerjaan bisa menyebut teknologi lama yang sudah tidak dipakai — verifikasi teknologi dari fingerprint (No. 11) sebelum mengklaim.
- Jejak digital perusahaan berubah cepat (akuisisi, layanan baru); catat tanggal pengumpulan.
