# Skill: Injeksi Template Klien CSTI — Client-Side Template Injection — injeksi ekspresi template di sisi klien hingga eksekusi kode

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 80. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat aplikasi web in-scope memakai framework template sisi klien (Angular, Vue, dan sejenisnya) dan input pengguna diduga dirender sebagai ekspresi template — sehingga ekspresi canary dievaluasi oleh browser.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi template SSTI → skill `injeksi-template-ssti` (sisi server; skill ini sisi klien).
- XSS DOM clobbering / mXSS → skill `xss-dom-clobbering`, `xss-mutasi-mxss` (varian XSS; skill ini lewat template klien).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL, ANTH. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Akun uji sendiri; tanpa menyerang pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian injeksi template diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu payload pun dikirim.

### Gerbang 1 — Identifikasi framework template klien

1. Tentukan framework (Angular/Vue/dll.) dan sintaks ekspresinya dari kode/DOM halaman; catat cara input dirender (interpolasi, binding).
2. **Standar lulus:** framework + sintaks + jalur input-ke-template tertulis. Tanpa jalur = jangan menebak.

### Gerbang 2 — Uji ekspresi canary

1. Kirim ekspresi aritmetika canary yang TIDAK BERBAHAYA (mis. ekspresi yang mengevaluasi ke angka) lewat input milik sendiri dan amati apakah hasilnya dirender sebagai nilai hasil, bukan teks mentah.
2. **Standar lulus:** hasil tercatat (dievaluasi sebagai ekspresi / dirender sebagai teks). Teks mentah = tidak terbukti.

### Gerbang 3 — Uji eskalasi ke eksekusi (terbatas, aman)

1. Bila ekspresi dievaluasi, uji apakah ekspresi bisa mengakses objek/fungsi di luar template (sandbox escape) — hanya dengan ekspresi baca-tulis canary milik sendiri, tanpa memanggil aksi sensitif.
2. **Standar lulus:** tingkat eskalasi tercatat (hanya evaluasi / bisa akses objek / tidak bisa). Jangan memanggil aksi destruktif lewat template.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Periksa DOM dan hasil evaluasi ekspresi template |
| curl / klien HTTP | Kirim input canary dan baca respons |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [injeksi-template-klien-csti] — No. 80
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Ekspresi template canary dievaluasi oleh framework klien pada input milik akun uji sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun dan data sendiri; jangan menyerang pengguna lain.
- Ekspresi uji harus tidak berbahaya: aritmetika dan pembacaan canary saja; jangan memanggil aksi sensitif, pengiriman data, atau penghapusan lewat template.
- Evaluasi ekspresi saja (tanpa eskalasi) tetap temuan — nilailah dampak apa adanya.
