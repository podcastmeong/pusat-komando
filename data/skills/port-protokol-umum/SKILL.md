# Skill: Port Protokol Umum — Rujukan port & protokol standar dan informasi yang diungkap tiap layanan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 5. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: rujukan; pemindaian hanya pada aset in-scope.

## Pemicu (kapan dipakai)

Dipakai sebagai rujukan saat merencanakan atau menafsirkan pemindaian: port apa yang biasa dipakai layanan apa (SSH 22, HTTP 80, HTTPS 443, DNS 53, SMB 445, RDP 3389, dan lainnya), dan informasi apa yang biasanya diungkap tiap layanan (banner, versi, nama host). Dipakai sebelum dan sesudah pemindaian, bukan sebagai pengganti skill pemindaian.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemindaian port/layanan → skill `pemindaian-port-layanan`.
- Nmap Scripting Engine → skill `nmap-nse-scripting` (No. 14).
- Penemuan perangkat → skill `penemuan-perangkat-jaringan` (No. 6).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (SEMUA — kesembilan program (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr)). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Rujukan ini BUKAN izin memindai.** Mengetahui bahwa port 22 biasanya SSH tidak memberi izin memindai port 22 pada host mana pun — pemindaian hanya pada aset in-scope (lihat No. 4).
12. **Port non-standar ada di mana-mana** — layanan bisa berjalan di port apa pun; jangan menyimpulkan 'tidak ada layanan' hanya karena port standarnya tertutup.

## Langkah + gerbang

### Gerbang 0 — Kuasai rujukan port umum

1. Hafal dan catat tabel port/protokol standar: 22 SSH, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 445 SMB, 3306 MySQL, 3389 RDP, 5432 PostgreSQL, 6379 Redis, 8080 HTTP alternatif — beserta TCP/UDP dan informasi yang biasa diungkap tiap layanan.
2. **Standar lulus:** tabel rujukan tertulis dan bisa dipakai tanpa menebak saat menafsirkan hasil pindaian.

### Gerbang 1 — Petakan port ke aset in-scope

1. Untuk tiap aset in-scope, tulis port mana yang RELEVAN diuji berdasarkan layanan yang diumumkan program (bukan semua port sekaligus tanpa alasan).
2. **Standar lulus:** daftar port per aset tertulis dengan alasan. Pemindaian tanpa daftar port = tebakan buta.

### Gerbang 2 — Tafsirkan hasil pindaian

1. Saat hasil pindaian (dari skill pemindaian) tersedia, tafsirkan tiap port terbuka: layanan apa yang kemungkinan berjalan, banner/versi apa yang terungkap, dan apakah itu sesuai dengan yang diumumkan program.
2. **Standar lulus:** tiap port terbuka ditafsirkan (layanan + bukti banner/versi) atau ditandai "tidak dikenal — perlu verifikasi lanjut". Port terbuka tanpa tafsiran = belum selesai.

### Gerbang 3 — Serahkan ke pengujian lanjut

1. Port/layanan yang menarik (versi lama, layanan tak terduga, banner yang membocorkan informasi) diserahkan ke A58 sebagai kandidat hipotesis, dengan catatan port dan buktinya.
2. **Standar lulus:** daftar kandidat tertulis + hipotesis pertama dirumuskan.

## Alat

| Alat | Cara pakai |
|---|---|
| Tabel port/protokol standar (catatan skill ini) | Rujukan saat merencanakan dan menafsirkan pemindaian |
| Hasil pemindaian dari skill `pemindaian-port-layanan` | Bahan yang ditafsirkan di Gerbang 2 |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Port relevan per aset: [aset + port + alasan]
Port terbuka + tafsiran: [port + layanan + banner/versi]
Scope guard dipatuhi: [ya — Scope guard: rujukan; pemindaian hanya pada aset in-scope.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Daftar ini tidak lengkap — layanan baru dan port kustom selalu muncul; bila menemui port yang tidak ada di tabel, catat dan cari rujukannya, jangan ditebak.
- Port terbuka saja BUKAN kerentanan; yang dinilai adalah apa yang diungkap dan bisa dilakukan layanan itu.
