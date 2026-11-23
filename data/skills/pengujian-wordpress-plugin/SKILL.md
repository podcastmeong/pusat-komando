# Skill: Pengujian WordPress Plugin — Kerentanan plugin/tema WordPress — injeksi, otorisasi, dan upload pada instalasi in-scope

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 74. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan instalasi WordPress; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope adalah instalasi WordPress (atau plugin/tema tertentu) dan ada dugaan celah pada plugin/tema — pola umum: injeksi, otorisasi lemah, atau upload file.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi SQL kontekstual → skill `injeksi-sql-kontekstual` (bila celahnya SQLi di plugin).
- Bypass unggah file → skill `bypass-unggah-file` (bila celahnya upload di plugin).
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
11. **Scope guard kandidat:** Hanya instalasi in-scope; tanpa merusak situs.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah instalasi WordPress / plugin / tema ini eksplisit in-scope? Catat versi yang tercakup.
2. **Standar lulus:** target + versi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Identifikasi plugin/tema dan versi

1. Enumerasi plugin/tema aktif dan versinya dari sumber yang diizinkan scope (header, halaman, endpoint publik) — tanpa pemindaian agresif.
2. Bandingkan dengan kerentanan yang diketahui publik untuk versi itu; catat kandidat.
3. **Standar lulus:** daftar plugin/tema + versi + kandidat kerentanan tertulis.

### Gerbang 2 — Uji satu kandidat pada instalasi sendiri/in-scope

1. Pilih satu kandidat; uji dengan akun uji sendiri (peran rendah bila menguji otorisasi) dan nilai canary.
2. Untuk upload: hanya file canary tidak berbahaya; untuk injeksi: hanya pola identifikasi read-only.
3. **Standar lulus:** hasil uji tercatat (rentan/aman + bukti). Tanpa bukti = belum terbukti.

### Gerbang 3 — Buktikan dampak aman + serahkan ke triase

1. Tulis dampak konkret (apa yang bisa dilakukan peran rendah / penyerang tanpa login) tanpa merusak situs atau data.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP + browser milik sendiri | Uji endpoint plugin/tema dengan akun uji sendiri |
| Daftar kerentanan publik (WPScan dan sejenisnya) | Rujukan versi rentan — verifikasi sendiri, jangan percaya mentah |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-wordpress-plugin] — No. 74
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Plugin/tema WordPress in-scope rentan (injeksi, otorisasi lemah, atau upload) pada versi yang diuji.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya instalasi in-scope; jangan menguji situs WordPress lain.
- Jangan merusak situs: tanpa menghapus/mengubah konten, tanpa mengunggah file berbahaya, tanpa mengubah pengguna lain.
- Kerentanan publik untuk suatu versi BUKAN bukti — harus diverifikasi sendiri pada target in-scope.
