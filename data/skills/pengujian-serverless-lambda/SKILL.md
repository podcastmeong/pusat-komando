# Skill: Pengujian Serverless Lambda — Misconfig serverless — environment variable terekspos, IAM berlebih, endpoint tanpa otorisasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 75. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan aset serverless; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai serverless (Lambda, API Gateway, dan sejenisnya) dan ada dugaan environment variable terekspos, peran IAM berlebih, atau endpoint tanpa otorisasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Serangan cloud IAM → skill `serangan-cloud-iam-entra` (IAM; skill ini khusus serverless).
- Dokumentasi API/otorisasi endpoint → skill `dokumentasi-api-otorisasi-endpoint` (matriks otorisasi endpoint; skill ini menambah sisi serverless).
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
11. **Scope guard kandidat:** Hanya aset in-scope; tanpa membaca data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aset serverless ini eksplisit in-scope? Banyak program tidak mencakup infrastruktur cloud.
2. **Standar lulus:** aset + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Inventarisasi endpoint dan fungsi

1. Daftar endpoint API Gateway / fungsi Lambda yang terekspos beserta pemicunya (HTTP, antrean, terjadwal) dari dokumentasi/sumber yang diizinkan scope.
2. **Standar lulus:** daftar endpoint + pemicu tertulis.

### Gerbang 2 — Uji otorisasi endpoint

1. Panggil tiap endpoint sensitif tanpa token dan dengan akun uji berperang rendah; catat mana yang merespons tanpa otorisasi yang benar.
2. Hanya data milik akun sendiri yang dipakai; jangan memicu fungsi yang mengubah data orang lain.
3. **Standar lulus:** hasil per endpoint tercatat (ditolak/diterima).

### Gerbang 3 — Uji paparan konfigurasi

1. Periksa apakah respons error atau endpoint debug membocorkan environment variable, nama peran IAM, atau konfigurasi internal — catat JENIS paparannya saja.
2. Jangan memakai kredensial yang terbaca di luar PoC; jangan memanggil layanan cloud dengan kredensial itu.
3. **Standar lulus:** paparan tercatat (jenis + lokasi); tidak ada kredensial yang dipakai.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Panggil endpoint serverless dengan variasi otorisasi |
| Dokumentasi target | Daftar endpoint dan pemicu fungsi |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-serverless-lambda] — No. 75
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Endpoint serverless in-scope bisa diakses tanpa otorisasi, atau konfigurasinya membocorkan environment variable / peran IAM.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aset in-scope; jangan memanggil fungsi serverless di luar scope.
- Jangan memakai kredensial/IAM yang terbaca di luar PoC.
- Jangan memicu fungsi yang menimbulkan biaya besar atau mengubah data (hindari pemicu destruktif; bila ragu, serahkan ke Muse).
