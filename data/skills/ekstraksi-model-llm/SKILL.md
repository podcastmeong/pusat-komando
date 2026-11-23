# Skill: Ekstraksi Model LLM — Mencuri perilaku/bobot model lewat kueri sistematis pada endpoint model in-scope

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 96. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **MUSE, OAI-S, 0DIN, G-VRP, VK, ANTH**. Skill ini untuk bounty agen AI. Catatan program: Google AI VRP mengecualikan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP tidak tercantum untuk kandidat ini. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat endpoint model in-scope diduga bisa diekstraksi — kueri sistematis yang mereplikasi perilaku (atau sebagian bobot/fungsi) model melebihi penggunaan normal yang diizinkan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Fingerprinting LLM → skill `fingerprinting-llm` (identifikasi model; skill ini ekstraksi perilakunya).
- Injeksi prompt tidak langsung agen → skill `injeksi-prompt-tidak-langsung-agen` (injeksi; skill ini ekstraksi).
- Ekstraksi system prompt → skill `ekstraksi-system-prompt` (STATUS: TUNGGU — jangan dipakai; skill ini tidak mencakup system-prompt-leak).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — MUSE, OAI-S, 0DIN, G-VRP, VK, ANTH. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Hanya endpoint in-scope; tanpa melanggar ketentuan penggunaan model.

## Langkah + gerbang

### Gerbang 0 — Cek scope + ketentuan penggunaan dulu

1. Baca pasal scope DAN ketentuan penggunaan model: apakah ekstraksi/kueri sistematis diizinkan pada endpoint ini? Catat larangan otomasi dan aturan ViKernel (deteksi live-vs-recorded dulu).
2. **Standar lulus:** scope + ketentuan tercatat di log sebelum satu kueri pun dikirim. Bila dilarang = jangan mulai.

### Gerbang 1 — Tentukan apa yang diukur

1. Tentukan target ekstraksi yang terukur: replikasi perilaku pada satu tugas sempit (mis. klasifikasi) dengan kueri milik sendiri, bukan 'mencuri seluruh model'.
2. **Standar lulus:** tugas sempit + metrik keberhasilan tertulis. Tanpa metrik = jangan menguji.

### Gerbang 2 — Kueri sistematis dalam batas yang diizinkan

1. Kirim kueri dalam volume yang diizinkan rate limit program; catat pasangan input-output milik sendiri.
2. **Standar lulus:** jumlah kueri + rate tercatat; tidak ada pelanggaran rate limit.

### Gerbang 3 — Uji replikasi perilaku

1. Latih/uji model pengganti SEDERHANA di lab sendiri memakai pasangan input-output itu; ukur seberapa dekat perilakunya dengan model target pada tugas sempit tersebut.
2. **Standar lulus:** skor kemiripan tercatat (metrik + angka). Tanpa angka = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Endpoint model in-scope | Kueri sistematis dalam batas rate limit |
| Lab sendiri | Model pengganti sederhana untuk mengukur replikasi |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [ekstraksi-model-llm] — No. 96
Program: [MUSE, OAI-S, 0DIN, G-VRP, VK, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Model pengganti yang dilatih dari kueri pada endpoint in-scope mereplikasi perilaku model target pada tugas sempit dengan skor kemiripan yang terukur.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya endpoint in-scope; tanpa melanggar ketentuan penggunaan model.
- Jangan mencoba mengekstrak system prompt (skill `ekstraksi-system-prompt` berstatus TUNGGU — jangan dipakai).
- Volume kueri harus dalam rate limit; kueri massal yang membanjiri endpoint adalah DoS dan dilarang.
