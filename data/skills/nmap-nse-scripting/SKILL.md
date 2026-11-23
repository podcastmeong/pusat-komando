# Skill: Nmap NSE Scripting — Nmap Scripting Engine: enumerasi lanjutan di atas pemindaian dasar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 14. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya aset in-scope; skrip non-destruktif saja.

## Pemicu (kapan dipakai)

Dipakai setelah pemindaian port dasar menemukan layanan pada aset in-scope: memakai Nmap Scripting Engine (NSE) untuk enumerasi lanjutan — versi layanan, banner, informasi yang diumumkan layanan, dan kerentanan yang sudah dikenal — tanpa skrip destruktif.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemindaian port/layanan dasar → skill `pemindaian-port-layanan`.
- Port/protokol umum → skill `port-protokol-umum` (No. 5).
- Penguasaan Burp/ZAP → skill `penguasaan-burp-suite-community` (No. 26) dan `owasp-zap-pengujian-web` (No. 25).

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
11. **Hanya aset in-scope, skrip non-destruktif saja.** Gunakan kategori skrip yang aman (mis. default/safe/version) dan JANGAN menjalankan skrip yang mengubah keadaan target (brute-force, exploit, DoS, atau skrip yang menulis data).
12. **Batasi kecepatan dan jumlah skrip** — jalankan skrip yang relevan dengan layanan yang ditemukan, bukan semua skrip sekaligus; hentikan bila target melambat.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi

1. Baca pasal scope: apakah pemindaian Nmap/NSE diizinkan pada aset ini? Apakah otomasi dilarang? Catat aturannya dan daftar aset + port yang boleh dipindai (dari No. 4 dan 5).
2. **Standar lulus:** izin + daftar aset/port tercatat sebelum satu skrip pun dijalankan.

### Gerbang 1 — Pilih skrip yang relevan

1. Dari layanan yang ditemukan pemindaian dasar, pilih skrip NSE yang relevan dan non-destruktif per layanan (mis. skrip banner/versi untuk layanan itu). Tulis daftar skrip + alasannya.
2. **Standar lulus:** daftar skrip tertulis dengan alasan per layanan. Skrip tanpa alasan = jangan dijalankan.

### Gerbang 2 — Jalankan skrip dengan batas

1. Jalankan NSE pada aset in-scope dengan skrip terpilih, kecepatan terbatas, dan jeda. Simpan output mentah di lingkungan terkendali milik sendiri.
2. **Standar lulus:** output tersimpan + tiap layanan tercatat hasil skripnya. Hentikan bila target melambat atau menunjukkan tanda kewalahan.

### Gerbang 3 — Tafsirkan hasil dan serahkan

1. Tafsirkan hasil: versi layanan yang terkonfirmasi, informasi yang diumumkan, dan kerentanan dikenal yang ditandai skrip (verifikasi klaim skrip sebelum meneruskannya — skrip bisa salah). Serahkan kandidat ke A58.
2. **Standar lulus:** daftar temuan tertulis dengan bukti output skrip + status verifikasi. Klaim skrip yang belum diverifikasi = ditandai "belum terverifikasi".

## Alat

| Alat | Cara pakai |
|---|---|
| Nmap + NSE (skrip safe/default/version) | Enumerasi lanjutan non-destruktif pada aset in-scope |
| Hasil `pemindaian-port-layanan` | Dasar pemilihan skrip |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Aset + port: [daftar in-scope]
Skrip dijalankan: [nama skrip + layanan]
Temuan: [versi/informasi/kerentanan dikenal + status verifikasi]
Scope guard dipatuhi: [ya — Scope guard: hanya aset in-scope; skrip non-destruktif saja.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Output NSE bisa memuat false positive (mis. versi yang ditebak dari banner) — selalu verifikasi sebelum mengklaim.
- Skrip kategori brute/exploit/dos TIDAK BOLEH dijalankan di skill ini.
