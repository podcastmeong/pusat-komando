# Skill: Inferensi Keanggotaan Model — Menentukan apakah data tertentu dipakai melatih model, dari respons model terhadap kueri

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 97. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **MUSE, OAI-S, 0DIN, G-VRP, VK, ANTH**. Skill ini untuk bounty agen AI. Catatan program: Google AI VRP mengecualikan halusinasi dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat ada dugaan model in-scope bisa mengungkapkan apakah suatu data dipakai dalam pelatihannya — lewat perbedaan respons terhadap data yang diduga anggota vs bukan anggota.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Fingerprinting LLM → skill `fingerprinting-llm` (identifikasi model; skill ini inferensi keanggotaan data).
- Ekstraksi model LLM → skill `ekstraksi-model-llm` (ekstraksi perilaku; skill ini keanggotaan data latih).
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
11. **Scope guard kandidat:** Hanya data sendiri sebagai sampel uji; tanpa data orang lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + ketentuan penggunaan dulu

1. Baca pasal scope DAN ketentuan penggunaan model: apakah pengujian inferensi keanggotaan diizinkan pada endpoint ini? Catat aturan ViKernel (deteksi live-vs-recorded dulu).
2. **Standar lulus:** scope + ketentuan tercatat di log sebelum satu kueri pun dikirim.

### Gerbang 1 — Siapkan sampel milik sendiri

1. Siapkan dua kelompok sampel HANYA dari data milik sendiri: (a) data yang diketahui dipakai melatih model (bila ada, mis. data yang sengaja diserahkan sendiri), (b) data sendiri yang pasti TIDAK dipakai melatih.
2. **Standar lulus:** kedua kelompok sampel tertulis + asal tiap sampel. Tanpa kelompok pembanding = jangan menguji.

### Gerbang 2 — Ukur respons model

1. Kirim kedua kelompok sampel sebagai kueri ke endpoint in-scope; catat metrik respons (mis. confidence/loss/kelancaran jawaban) per sampel.
2. **Standar lulus:** metrik per sampel tercatat untuk kedua kelompok.

### Gerbang 3 — Uji pemisahan anggota vs bukan anggota

1. Uji apakah metrik memisahkan kedua kelompok secara konsisten (mis. ambang yang mengklasifikasi anggota vs bukan anggota di atas peluang acak); ulangi dengan sampel berbeda milik sendiri.
2. **Standar lulus:** akurasi pemisahan tercatat (angka + jumlah sampel). Akurasi setara acak = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Endpoint model in-scope | Kueri sampel milik sendiri |
| Lembar hitung | Metrik respons + akurasi pemisahan |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [inferensi-keanggotaan-model] — No. 97
Program: [MUSE, OAI-S, 0DIN, G-VRP, VK, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Metrik respons model memisahkan data latih milik sendiri dari data non-latih milik sendiri dengan akurasi di atas peluang acak yang terukur.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: hanya data SENDIRI sebagai sampel uji; tanpa data orang lain dalam bentuk apa pun.
- Jangan memakai data pribadi orang lain untuk menguji apakah data itu ada dalam pelatihan model.
- Akurasi setara acak bukan temuan — jangan membesar-besarkan.
