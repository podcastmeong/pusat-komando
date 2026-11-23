# Skill: Kursus Reverse Engineering Android 101 — Android App Reverse Engineering 101 (Maddie Stone, gratis) — alur RE Android dari nol sampai analisis biner

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 104. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: kursus latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat membutuhkan alur belajar RE Android yang terstruktur dari nol — mengikuti kursus gratis Android App Reverse Engineering 101 (Maddie Stone) sampai analisis biner, sebagai fondasi sebelum menguji program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Bahasa Smali Android → skill `bahasa-smali-android` (teknik Smali yang diajarkan kursus).
- Dekompilasi aplikasi mobile → skill `dekompilasi-aplikasi-mobile` (teknik decompile yang diajarkan kursus).
- Lab UnCrackable Android → skill `lab-uncrackable-android` (latihan RE setelah kursus).
- Kurikulum minggu pertama mobile → skill `kurikulum-minggu-pertama-mobile` (rencana belajar yang memakai kursus ini).

## Aturan keras

1. **Hanya program bounty resmi in-scope** — SEMUA (latihan). Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Kursus latihan; tanpa target nyata.

## Langkah + gerbang

### Gerbang 0 — Pastikan ini belajar, bukan target nyata

1. Konfirmasi semua praktik kursus hanya memakai aplikasi latihan/contoh kursus di emulator sendiri.
2. **Standar lulus:** modul kursus + tujuan belajar tercatat di log sebelum mulai.

### Gerbang 1 — Ikuti modul berurutan

1. Ikuti modul kursus berurutan (dasar APK → decompile → Smali → analisis biner); catat konsep kunci tiap modul.
2. **Standar lulus:** modul + konsep kunci tertulis.

### Gerbang 2 — Praktikkan tiap modul di lab sendiri

1. Praktikkan tiap modul pada aplikasi latihan di emulator sendiri; catat apa yang berhasil dan apa yang belum dipahami.
2. **Standar lulus:** hasil praktik per modul tercatat.

### Gerbang 3 — Petakan pelajaran ke skill bounty

1. Tulis teknik apa yang dikuasai dan skill bounty mana yang memakainya; catat modul yang perlu diulang.
2. **Standar lulus:** pemetaan teknik → skill bounty tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Kursus Android App Reverse Engineering 101 (gratis) | Materi belajar RE Android |
| Emulator Android sendiri + aplikasi latihan | Praktik tiap modul |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [kursus-reverse-engineering-android-101] — No. 104
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Modul kursus selesai dengan praktik di lab sendiri dan konsep kunci terdokumentasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aplikasi latihan/contoh kursus di emulator sendiri — jangan mempraktikkan teknik kursus pada aplikasi nyata di luar program.
- Kursus gratis saja; jangan membeli materi berbayar tanpa persetujuan Cipta.
- Tidak ada temuan bounty dari kursus ini — hasilnya adalah keterampilan, bukan laporan.
