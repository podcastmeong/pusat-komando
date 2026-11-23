# Skill: Misconfig Firebase — Realtime Database/Firestore terbuka, API key terekspos, dan aturan keamanan longgar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 66. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat aplikasi target in-scope memakai Firebase (Realtime Database, Firestore, Storage, atau Auth) dan ada dugaan aturan keamanan longgar — mis. database bisa dibaca tanpa autentikasi, API key terekspos di kode klien, atau aturan baca/tulis mengizinkan siapa saja.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kebocoran data API secara umum → skill `kebocoran-data-respons-json-api` (bila ada di toko; bila belum, catat di log).
- Audit konfigurasi cloud/IAM → skill `serangan-cloud-iam-entra` (untuk sisi IAM, bukan aturan Firebase).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Gerbang false-positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL, ANTH, MUSE. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Hanya aplikasi in-scope; tanpa membaca data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope program: apakah aplikasi dan backend Firebase-nya in-scope? Apakah pengujian konfigurasi diizinkan?
2. **Standar lulus:** scope + pasal otomasi tercatat di log sebelum satu permintaan pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Identifikasi pemakaian Firebase

1. Periksa aplikasi (web/APK in-scope): cari konfigurasi Firebase di kode klien (nama proyek, URL database, bucket Storage) dan endpoint `*.firebaseio.com` / `firestore.googleapis.com` yang dipanggil.
2. Catat layanan yang dipakai: Realtime Database, Firestore, Storage, Auth.
3. **Standar lulus:** layanan Firebase yang dipakai tertulis dengan bukti pemanggilan (URL endpoint + konteks fitur). Tanpa bukti = jangan menebak.

### Gerbang 2 — Uji aturan baca tanpa autentikasi

1. Minta satu dokumen/kunci milik AKUN UJI SENDIRI tanpa token autentikasi (mis. path data milik akun sendiri). Amati: ditolak (aturan benar) atau dikembalikan (aturan longgar).
2. Bila dikembalikan, ulangi dengan kunci canary palsu milik sendiri untuk memastikan bukan data statis publik.
3. **Standar lulus:** hasil baca tanpa autentikasi tercatat (ditolak/dikembalikan) beserta path yang diuji. Jangan pernah meminta data pengguna lain.

### Gerbang 3 — Uji aturan tulis dan API key

1. Uji apakah tulis tanpa autentikasi ditolak (coba tulis nilai canary ke path milik akun sendiri saja; bila berhasil, segera hapus/kembalikan).
2. Periksa apakah API key yang terekspos di klien bisa dipakai memanggil layanan berbayar/terbatas tanpa autentikasi pengguna.
3. **Standar lulus:** hasil uji tulis + penyalahgunaan API key tercatat; setiap nilai canary yang tertulis sudah dihapus/dikembalikan.

### Gerbang 4 — Nilai dampak + serahkan ke triase

1. Tulis dampak konkret: data apa (milik akun sendiri) yang bisa dibaca/ditulis orang tanpa login, dan apa yang bisa dilakukan penyerang karenanya.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah + keputusan triase tercatat. Tanpa bukti = belum berhasil.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Minta dokumen/kunci Firebase tanpa dan dengan autentikasi; baca respons |
| Browser milik sendiri | Periksa pemanggilan Firebase di aplikasi web in-scope |
| Akun tes sendiri | Satu-satunya akun yang datanya dibaca/ditulis dalam pengujian |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [firebase-misconfig] — No. 66
Program: [HUNTR, PPLX, MISTRAL, ANTH, MUSE]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Aturan Firebase longgar sehingga data akun uji sendiri bisa dibaca/ditulis tanpa autentikasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Aturan Firebase bisa berbeda per path/koleksi — satu path yang terbuka bukan bukti seluruh database terbuka; uji per path yang relevan.
- API key Firebase di kode klien pada umumnya BUKAN rahasia; yang dinilai adalah apa yang bisa dilakukan dengan key itu tanpa autentikasi, bukan keberadaan key-nya.
- Jangan mengambil atau menyimpan data pengguna lain walau aturan database mengizinkannya.
