# Skill: Fuzzing Direktori File — Menebak folder/file tersembunyi dengan ffuf/Gobuster

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 7. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya target in-scope; jeda antar-request; tanpa DoS.

## Pemicu (kapan dipakai)

Dipakai saat target web in-scope diduga punya folder/file tersembunyi (mis. /admin, /backup.zip, .env, direktori cadangan) yang tidak tertaut dari halaman mana pun. Dipakai setelah pemetaan permukaan web, dengan wordlist dan jeda antar-request.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemetaan permukaan web → skill `pemetaan-permukaan-serangan`.
- Direktori .git terekspos → skill `git-terekspos` (No. 68, keluarga HACKING).
- Penemuan API/Swagger → skill `penemuan-api-swagger`.

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
11. **Hanya target in-scope, dengan jeda antar-request.** Atur rate dan jeda agar tidak membanjiri server; volume kecil, berhenti bila server menunjukkan tanda kewalahan (itu DoS).
12. **Temuan file sensitif (mis. .env, backup berisi kredensial) TIDAK BOLEH diunduh isinya di luar bukti minimal** — catat keberadaan + status responsnya saja, jangan memakai kredensial yang mungkin ada di dalamnya di luar PoC, dan laporkan segera.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi

1. Baca pasal scope: apakah fuzzing direktori diizinkan pada target ini? Apakah otomasi dilarang (huntr 'Humans only' = uji manual saja)? Catat aturannya.
2. **Standar lulus:** izin fuzzing + aturan otomasi tercatat sebelum satu request pun dikirim.

### Gerbang 1 — Siapkan wordlist + baseline

1. Pilih wordlist yang sesuai (umum, lalu spesifik bila perlu) dan tentukan baseline: ukuran/status respons halaman yang TIDAK ada (404) pada target ini, agar hasil bisa dibedakan dari noise.
2. **Standar lulus:** baseline 404 tercatat (status + ukuran respons). Tanpa baseline = hasil fuzzing tidak bisa ditafsirkan.

### Gerbang 2 — Jalankan fuzzing dengan jeda

1. Jalankan ffuf/Gobuster (atau manual bila otomasi dilarang) pada target in-scope dengan jeda antar-request. Catat tiap respons yang BERBEDA dari baseline (status, ukuran, atau isi yang berbeda).
2. **Standar lulus:** daftar kandidat path tertulis dengan status + ukuran respons. Jalankan dalam volume kecil; hentikan bila server melambat.

### Gerbang 3 — Verifikasi tiap kandidat

1. Kunjungi tiap kandidat secara manual dan periksa isinya: apakah benar-benar ada dan relevan (halaman admin? file backup? file konfigurasi?) atau hanya false positive (halaman error kustom yang mengembalikan 200)?
2. **Standar lulus:** tiap kandidat berstatus terverifikasi/false positive dengan buktinya. Kandidat yang tidak diverifikasi = jangan dilaporkan.

### Gerbang 4 — Nilai dampak + tulis draf

1. Untuk kandidat terverifikasi, tulis apa yang terungkap dan dampaknya (tanpa mengunduh isi sensitif di luar bukti minimal). Serahkan ke A60 untuk audit.
2. **Standar lulus:** dampak ditulis konkret, draf mengikuti format output, dan status triase diputuskan A60.

## Alat

| Alat | Cara pakai |
|---|---|
| ffuf / Gobuster | Fuzzing direktori/file — hanya bila program mengizinkan otomasi |
| Wordlist (umum) | Daftar kata path yang ditebak |
| curl / browser milik sendiri | Verifikasi manual tiap kandidat |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Target: [program + host in-scope]
Baseline 404: [status + ukuran]
Kandidat terverifikasi: [path + status + isi singkat]
Scope guard dipatuhi: [ya — Scope guard: hanya target in-scope; jeda antar-request; tanpa DoS.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Halaman error kustom sering mengembalikan 200 untuk semua path — selalu bandingkan dengan baseline, jangan percaya status saja.
- Wordlist besar + tanpa jeda = membanjiri server; itu DoS dan dilarang.
