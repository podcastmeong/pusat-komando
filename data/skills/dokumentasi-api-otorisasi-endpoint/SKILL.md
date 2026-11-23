# Skill: Dokumentasi API Otorisasi Endpoint — Membaca dokumentasi API lalu menyusun matriks otorisasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 9. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: akun uji sendiri; tanpa menyentuh data pengguna lain.

## Pemicu (kapan dipakai)

Dipakai sebelum menguji otorisasi API: membaca dokumentasi API target in-scope (OpenAPI/Swagger atau dokumentasi resmi lain) lalu menyusun matriks otorisasi per endpoint — peran mana boleh memanggil endpoint mana — untuk diuji satu per satu dengan akun sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penemuan API/Swagger → skill `penemuan-api-swagger`.
- Kebocoran data respons JSON → skill `kebocoran-data-respons-json-api` (No. 8).
- Kontrol akses diferensial → skill `access-control-differential-analyst`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic, Muse). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Matriks dibuat dari dokumentasi, bukan dari menebak.** Endpoint yang tidak ada di dokumentasi dan tidak diumumkan program jangan dimasukkan sebagai target uji.
12. **Pengujian matriks hanya dengan akun uji sendiri** — tiap sel matriks diuji dengan akun milik sendiri dari peran yang berbeda; jangan memakai akun atau data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + dokumentasi yang tersedia

1. Cari dokumentasi API resmi target in-scope (OpenAPI/Swagger, dokumen developer, atau halaman API resmi). Catat sumbernya.
2. **Standar lulus:** sumber dokumentasi tercatat. Tidak ada dokumentasi = catat dan gunakan pemetaan permukaan (No. 1/11) sebagai gantinya, jangan mengarang endpoint.

### Gerbang 1 — Inventarisasi endpoint

1. Daftar semua endpoint dari dokumentasi: metode, path, parameter, dan deskripsi singkat. Kelompokkan menurut sumber daya (pengguna, pesanan, dokumen, dan sebagainya).
2. **Standar lulus:** daftar endpoint tertulis lengkap dengan metode + path. Endpoint tanpa metode/path jelas = ditandai "belum terverifikasi".

### Gerbang 2 — Susun matriks otorisasi

1. Untuk tiap endpoint, tulis peran mana yang MENURUT dokumentasi boleh memanggilnya (mis. admin, pengguna biasa, tamu) dan operasi apa yang diizinkan (baca/tulis/hapus). Sel yang tidak dijelaskan dokumentasi ditandai "tidak diketahui".
2. **Standar lulus:** matriks tertulis (endpoint × peran). Matriks yang menebak izin tanpa dasar dokumentasi = belum selesai.

### Gerbang 3 — Uji satu per satu (akun sendiri)

1. Uji tiap sel matriks yang meragukan dengan akun sendiri dari peran yang berbeda (akun sendiri semua): apakah peran yang seharusnya ditolak benar-benar ditolak? Satu endpoint per putaran, catat responsnya.
2. **Standar lulus:** hasil uji tiap sel tercatat (diizinkan/ditolak + bukti respons). Sel yang belum diuji = ditandai "belum diuji", bukan diasumsikan aman.

### Gerbang 4 — Serahkan penyimpangan ke triase

1. Sel yang menyimpang dari dokumentasi (peran yang seharusnya ditolak ternyata diizinkan) diserahkan ke A58 sebagai hipotesis dan ke A60 untuk audit.
2. **Standar lulus:** daftar penyimpangan tertulis + hipotesis dirumuskan.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumentasi OpenAPI/Swagger target | Sumber inventarisasi endpoint |
| Akun tes sendiri (beberapa peran) | Pengujian tiap sel matriks |
| curl / klien HTTP | Mengirim request uji per endpoint |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Dokumentasi: [sumber]
Endpoint terinventarisasi: [jumlah]
Penyimpangan matriks: [endpoint + peran + respons]
Scope guard dipatuhi: [ya — Scope guard: akun uji sendiri; tanpa menyentuh data pengguna lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Dokumentasi bisa kedaluwarsa — endpoint yang ada di lapangan tapi tidak di dokumentasi dicatat terpisah dan hanya diuji bila program mengizinkannya.
- Matriks ini adalah peta, bukan bukti kerentanan; bukti datang dari pengujian tiap sel.
