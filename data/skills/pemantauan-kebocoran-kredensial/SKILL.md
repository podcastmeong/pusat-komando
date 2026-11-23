# Skill: Pemantauan Kebocoran Kredensial — Memantau data breach publik untuk domain target

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 12. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya data breach publik; tanpa memakai kredensial orang lain.

## Pemicu (kapan dipakai)

Dipakai saat memeriksa apakah kredensial atau secret yang terkait dengan domain target in-scope sudah bocor di data breach PUBLIK (layanan pemantau breach, arsip publik, repositori publik). Tujuannya: memahami permukaan target dan menemukan secret terekspos — bukan untuk memakai kredensial siapa pun.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Dorking & secret di GitHub → skill `dorking-secret-github`.
- Direktori .git terekspos → skill `git-terekspos` (No. 68, keluarga HACKING).
- Jejak digital perusahaan → skill `jejak-digital-perusahaan-publik` (No. 16).

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
11. **Hanya sumber breach PUBLIK.** Jangan membeli, mengunduh, atau mengakses dump breach yang tidak publik.
12. **DILARANG memakai kredensial orang lain** — kredensial yang ditemukan hanya dicatat keberadaannya (layanan + jenis + tanggal breach bila diketahui) dan dilaporkan; jangan pernah login dengan kredensial itu, jangan menguji apakah kredensial itu masih aktif.

## Langkah + gerbang

### Gerbang 0 — Cek scope + sumber yang diizinkan

1. Tetapkan domain target in-scope dan daftar sumber breach publik yang akan dipakai. Catat sumbernya.
2. **Standar lulus:** domain + sumber tercatat. Sumber yang tidak publik = jangan dipakai.

### Gerbang 1 — Cari kebocoran untuk domain target

1. Cari di sumber breach publik: apakah domain target muncul dalam breach yang diketahui? Catat breach-nya (nama layanan, tanggal bila diketahui, jenis data yang bocor menurut sumber publik).
2. **Standar lulus:** daftar breach tertulis atau "tidak ditemukan" tercatat. Pencarian tanpa sumber = tidak bisa dipakai sebagai bukti.

### Gerbang 2 — Periksa secret terekspos di sumber publik

1. Periksa sumber publik terkait target (repositori publik, dokumen publik, arsip) apakah ada secret yang terekspos (API key, token, kata sandi) yang terkait dengan domain target. Catat jenis dan lokasinya saja.
2. **Standar lulus:** tiap secret tercatat dengan jenis + lokasi publiknya (tanpa menyalin nilai utuhnya ke log).

### Gerbang 3 — Nilai dan laporkan

1. Nilai: apakah kebocoran/secret itu masih relevan (masih dipakai target?) dan apa dampaknya bila masih aktif. Jangan menguji keaktifannya dengan login. Serahkan ke A60 untuk audit.
2. **Standar lulus:** penilaian tertulis + draf mengikuti format output, dan status triase diputuskan A60.

## Alat

| Alat | Cara pakai |
|---|---|
| Layanan pemantau breach publik | Mencari breach yang terkait domain target |
| Pencarian repositori/dokumen publik | Memeriksa secret terekspos di sumber publik |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Domain target: [domain in-scope]
Breach ditemukan: [nama + tanggal + jenis data — dari sumber publik]
Secret terekspos: [jenis + lokasi publik — tanpa nilai utuh]
Scope guard dipatuhi: [ya — Scope guard: hanya data breach publik; tanpa memakai kredensial orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak 'breach' yang beredar adalah gabungan data lama atau data palsu — verifikasi dari sumber publik yang kredibel sebelum mengklaim.
- Menemukan kredensial bocor bukan izin memakainya; memakai kredensial orang lain adalah pelanggaran aturan keras.
