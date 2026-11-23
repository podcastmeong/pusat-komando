# Skill: Git Terekspos — Direktori .git/.svn terekspos di web sehingga riwayat repo dan secret bisa diunduh

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 68. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target web in-scope diduga mengekspos direktori `.git/` (atau `.svn/`) — mis. URL `/.git/HEAD` atau `/.git/config` merespons 200, atau file `/.git/logs/HEAD` bisa diunduh.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Fuzzing direktori/file → skill `fuzzing-direktori-file` (menemukan path tersembunyi; skill ini menguji isi `.git`).
- Pencarian secret di kode publik → skill `dorking-secret-github` (repo publik; skill ini untuk repo yang terekspos lewat web target).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Hanya target in-scope; tanpa memakai secret yang ditemukan di luar PoC.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope program: apakah target web ini in-scope dan apakah pengunduhan riwayat repo diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Konfirmasi keterpaparan

1. Minta `/.git/HEAD`, `/.git/config`, dan `/.git/logs/HEAD` pada target in-scope. Catat status HTTP dan isi yang dikembalikan.
2. **Standar lulus:** minimal satu file `.git` merespons 200 dengan isi repo yang valid. Bila semua 404/403 = tidak terekspos, tutup dengan buktinya.

### Gerbang 2 — Unduh riwayat secukupnya

1. Unduh objek Git yang diperlukan untuk membuktikan keterpaparan (HEAD, config, log, dan objek yang dirujuk) — secukupnya untuk PoC, bukan seluruh repo bila tidak perlu.
2. Catat commit yang mengandung informasi sensitif (nama file + jenisnya), tanpa menyalin isi secret ke log.
3. **Standar lulus:** riwayat berhasil dibaca dan daftar file sensitif tercatat (nama + commit). Isi secret TIDAK ditulis di log.

### Gerbang 3 — Buktikan dampak tanpa memakai secret

1. Tunjukkan bahwa riwayat berisi kredensial/kode sensitif (mis. jenis secret + file + commit) — CUKUP sebagai bukti; JANGAN memakai secret itu untuk login, mengakses layanan, atau menguji sistem lain.
2. Bila secret itu kunci API internal, cukup sebut jenis + lokasinya; jangan memanggil layanan dengan kunci tersebut.
3. **Standar lulus:** dampak tertulis tanpa satu pun secret yang dipakai di luar PoC. Secret yang dipakai = pelanggaran, hentikan dan laporkan ke Muse.

### Gerbang 4 — Serahkan ke triase

1. Serahkan draf (bukti keterpaparan + daftar file sensitif tanpa isi secret) ke A60 audit → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat. Tanpa bukti = belum berhasil.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Minta file .git dan periksa status/isi |
| Git (git clone / git log / git show di salinan lokal) | Baca riwayat repo yang diunduh secukupnya |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [git-terekspos] — No. 68
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Direktori .git target in-scope terekspos sehingga riwayat repo bisa diunduh siapa saja.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Secret yang ditemukan TIDAK BOLEH dipakai di luar PoC — tidak untuk login, tidak untuk mengakses layanan, tidak untuk menguji sistem lain.
- Jangan menulis isi secret (nilai kunci/token/kata sandi) di log atau laporan; cukup jenis + file + commit.
- Hapus salinan repo yang diunduh setelah laporan selesai bila berisi data sensitif.
