# Skill: Spionase Permukaan Agen AI — Inventarisasi permukaan agen AI sebelum berburu

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 1. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya permukaan program in-scope; tanpa data orang lain.

## Pemicu (kapan dipakai)

Dipakai di AWAL setiap perburuan agen AI, sebelum satu pun uji injeksi atau eksploitasi dijalankan. Dipakai saat perlu peta H0: jalur baca data apa saja yang dimiliki agen (email, kalender, dokumen, halaman, repo), konektor apa saja yang terpasang, dan komponen apa saja yang bisa dibaca atau ditulis agen. Tanpa peta ini, pengujian berikutnya adalah tebakan buta.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Inventarisasi endpoint web/API umum → skill `pemetaan-permukaan-serangan` (skill ini khusus permukaan AGEN AI: jalur baca data + konektor, bukan endpoint web biasa).
- Enumerasi subdomain/teknologi → skill `enumerasi-subdomain`, `pemetaan-teknologi-stack` (No. 11 keluarga ini).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Anthropic). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Google AI VRP secara eksplisit mengecualikan prompt injection langsung, jailbreak, halusinasi, dan system-prompt-leak** — skill ini hanya MEMETAKAN permukaan; bila peta mengarah ke area yang dikecualikan Google AI VRP, arahkan pengujian ke Muse/OpenAI Safety/0din/ViKernel/Anthropic, bukan Google AI VRP.
12. **Hanya baca konfigurasi/dokumentasi permukaan yang disediakan program** — jangan memancing agen membaca data pribadi orang lain untuk 'melengkapi peta'.

## Langkah + gerbang

### Gerbang 0 — Cek scope + definisi permukaan

1. Baca pasal scope program: aset agen AI mana yang in-scope (nama agen, versi, konektor yang tercantum)? Catat batasnya.
2. **Standar lulus:** daftar aset in-scope tertulis sebelum pemetaan dimulai. Tanpa itu = jangan mulai.

### Gerbang 1 — Inventarisasi jalur baca data

1. Dari dokumentasi resmi program dan antarmuka agen yang in-scope, catat tiap jalur baca data: email, kalender, dokumen/drive, halaman web, repo/kode, basis data, pesan/chat. Untuk tiap jalur catat: sumber datanya, apakah agen bisa membaca saja atau juga menulis, dan apakah ada filter/persetujuan.
2. **Standar lulus:** tabel jalur baca data lengkap dengan kemampuan baca/tulis tiap jalur. Jalur yang tidak terdokumentasi = ditandai "belum terverifikasi", bukan diasumsikan ada.

### Gerbang 2 — Inventarisasi konektor dan komponen

1. Catat tiap konektor/integrasi yang terpasang pada agen in-scope (nama konektor, layanan yang dihubungkan, izin yang diminta) dan tiap komponen yang bisa dipanggil agen (alat/tool, fungsi, API internal).
2. **Standar lulus:** daftar konektor + komponen tertulis beserta izinnya. Konektor yang izinnya tidak jelas = ditandai untuk diklarifikasi, bukan diasumsikan aman atau berbahaya.

### Gerbang 3 — Petakan aliran data (H0)

1. Gambar aliran sederhana: data masuk dari jalur mana → diproses komponen apa → keluar ke mana (tampilan, pengiriman, penulisan). Tandai titik di mana data dari sumber yang tidak tepercaya (email masuk, dokumen pihak ketiga, halaman web) bisa masuk ke alur agen.
2. **Standar lulus:** diagram/alur tertulis dengan titik masuk data tak tepercaya ditandai. Tanpa alur = belum ada peta, jangan lanjut ke pengujian.

### Gerbang 4 — Prioritaskan permukaan untuk diuji

1. Urutkan permukaan dari yang paling berisiko: jalur yang membaca data tak tepercaya + bisa menulis/mengirim tanpa persetujuan berada di atas. Serahkan prioritas ke A58 untuk dirumuskan menjadi hipotesis pengujian.
2. **Standar lulus:** daftar prioritas tertulis + hipotesis pertama dirumuskan. Peta yang tidak menghasilkan prioritas = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumentasi resmi program + antarmuka agen in-scope | Sumber utama peta permukaan; baca dulu sebelum alat apa pun |
| Catatan peta (tabel + diagram alur) | Disimpan bersama log; dipakai semua skill pengujian berikutnya |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Peta permukaan (H0): [jalur baca data + konektor + komponen]
Aliran data tak tepercaya: [titik masuk yang ditandai]
Prioritas uji: [permukaan #1 yang dipilih A58]
Scope guard dipatuhi: [ya — Scope guard: hanya permukaan program in-scope; tanpa data orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Peta yang dibuat dari dokumentasi saja bisa kedaluwarsa bila agen diperbarui — perbarui peta tiap kali program mengumumkan perubahan (lihat skill `pemantauan-perubahan-target`, No. 19).
- Skill ini tidak membuktikan kerentanan apa pun; pembuktian dilakukan skill pengujian lain dengan canary milik sendiri.
