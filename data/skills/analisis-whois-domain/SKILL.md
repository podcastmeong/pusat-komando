# Skill: Analisis WHOIS Domain — Data WHOIS/registrasi domain sebagai titik awal recon

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 23. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya data registrasi publik.

## Pemicu (kapan dipakai)

Dipakai sebagai titik awal recon target: membaca data WHOIS/registrasi domain target in-scope — pemilik organisasi, nameserver, tanggal registrasi dan kedaluwarsa — dari data registrasi publik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis DNS pasif → skill `analisis-dns-pasif` (No. 13).
- Jejak digital perusahaan → skill `jejak-digital-perusahaan-publik` (No. 16).
- Pemantauan sertifikat baru → skill `pemantauan-sertifikat-baru` (No. 24).

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
11. **Hanya data registrasi PUBLIK.** Gunakan layanan WHOIS publik; jangan mencoba mengakses data registrasi yang disembunyikan (privacy protection) atau data pribadi pendaftar.
12. **Data WHOIS bukan bukti kepemilikan mutlak** — data bisa kedaluwarsa, memakai privacy protection, atau memakai nama organisasi yang berbeda dari merek; verifikasi dengan sumber lain sebelum mengklaim.

## Langkah + gerbang

### Gerbang 0 — Cek scope + domain target

1. Tetapkan domain target in-scope dan baca pasal scope. Catat domainnya.
2. **Standar lulus:** domain tertulis. Tanpa itu = jangan mulai.

### Gerbang 1 — Ambil data WHOIS

1. Ambil data WHOIS domain dari layanan WHOIS publik: pendaftar (registrar), tanggal dibuat/diperbarui/kedaluwarsa, nameserver, dan organisasi pendaftar bila dipublikasikan.
2. **Standar lulus:** data WHOIS tercatat dengan sumber + tanggal pengambilan. Data tanpa tanggal = tidak bisa dipakai sebagai bukti.

### Gerbang 2 — Nilai data registrasi

1. Nilai: apakah domain sudah lama terdaftar (menunjukkan kestabilan) atau baru (perlu kewaspadaan)? Apakah nameserver mengarah ke penyedia yang dikenal? Apakah ada petunjuk organisasi atau layanan terkait?
2. **Standar lulus:** penilaian tertulis per item. Penilaian tanpa data WHOIS persis = belum selesai.

### Gerbang 3 — Kaitkan dengan recon lain

1. Kaitkan hasil WHOIS dengan DNS pasif (No. 13) dan jejak perusahaan (No. 16): apakah nameserver cocok dengan data DNS? Apakah organisasi cocok dengan perusahaan target? Serahkan ketidakcocokan ke A58 sebagai pertanyaan, bukan vonis.
2. **Standar lulus:** kaitan tertulis + pertanyaan lanjut (bila ada) diserahkan.

## Alat

| Alat | Cara pakai |
|---|---|
| Layanan WHOIS publik | Mengambil data registrasi domain |
| Data DNS pasif (No. 13) | Pembanding nameserver dan organisasi |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Domain: [domain in-scope]
Data WHOIS: [registrar + tanggal + nameserver + organisasi bila publik]
Kaitan: [cocok/tidak dengan DNS + jejak perusahaan]
Scope guard dipatuhi: [ya — Scope guard: hanya data registrasi publik.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak domain memakai privacy protection sehingga data pemilik disembunyikan — itu normal, bukan temuan.
- Tanggal kedaluwarsa yang dekat bukan kerentanan; jangan mengklaim 'domain akan kedaluwarsa' sebagai temuan bounty.
