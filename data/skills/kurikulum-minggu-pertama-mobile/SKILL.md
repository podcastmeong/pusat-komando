# Skill: Kurikulum Minggu Pertama Mobile — Rencana belajar mobile minggu pertama — emulator, JADX-GUI + ADB, DIVA/InjuredAndroid, MASTG

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 107. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: kurikulum latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat memulai belajar pengujian mobile dari nol — mengikuti kurikulum minggu pertama: (1) instal emulator Android Studio/Genymotion; (2) instal JADX-GUI + ADB; (3) unduh DIVA/InjuredAndroid, selesaikan 3–5 tantangan pertama sambil membaca MASTG.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Lab aplikasi rentan mobile → skill `lab-aplikasi-rentan-mobile` (DIVA; dipakai langkah 3 kurikulum).
- Lab InjuredAndroid CTF → skill `lab-injuredandroid-ctf` (tantangan langkah 3 kurikulum).
- Panduan MASTG → skill `panduan-mastg` (bacaan pendamping kurikulum).
- Lab MobileHackingLab → skill `lab-mobilehackinglab` (alternatif perangkat lab bila emulator lokal bermasalah).

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
11. **Scope guard kandidat:** Kurikulum latihan; tanpa target nyata.

## Langkah + gerbang

### Gerbang 0 — Siapkan lingkungan (hari 1–2)

1. Instal emulator Android Studio/Genymotion di perangkat sendiri; pastikan emulator jalan dan ADB terhubung.
2. **Standar lulus:** emulator jalan + `adb devices` menampilkan perangkat; bila emulator lokal bermasalah, pakai `lab-mobilehackinglab` sebagai alternatif dan catat.

### Gerbang 1 — Siapkan alat analisis (hari 2–3)

1. Instal JADX-GUI + ADB; pastikan keduanya bisa membuka APK latihan dan terhubung ke emulator.
2. **Standar lulus:** JADX-GUI membuka APK latihan + ADB terhubung; keduanya tercatat.

### Gerbang 2 — Selesaikan 3–5 tantangan pertama (hari 3–7)

1. Unduh DIVA/InjuredAndroid; selesaikan 3–5 tantangan pertama sambil membaca bagian MASTG yang relevan; catat metode tiap tantangan.
2. **Standar lulus:** minimal 3 tantangan selesai + langkah tiap tantangan tercatat.

### Gerbang 3 — Evaluasi minggu pertama

1. Tulis teknik apa yang dikuasai, apa yang belum dipahami, dan rencana minggu kedua (skill bounty mana yang dilatih berikutnya).
2. **Standar lulus:** evaluasi + rencana minggu kedua tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Emulator Android Studio/Genymotion | Perangkat lab minggu pertama |
| JADX-GUI + ADB | Analisis APK + interaksi perangkat |
| DIVA / InjuredAndroid + MASTG | Aplikasi latihan + bacaan pendamping |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [kurikulum-minggu-pertama-mobile] — No. 107
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Kurikulum minggu pertama selesai: emulator jalan, alat terpasang, minimal 3 tantangan pertama selesai, evaluasi tertulis.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aplikasi latihan (DIVA/InjuredAndroid) di emulator sendiri — jangan memakai tekniknya terhadap aplikasi nyata di luar program.
- Bila satu alat gagal terpasang, catat kendalanya dan pakai alternatif (mis. MobileHackingLab) — jangan berhenti tanpa catatan.
- Tidak ada temuan bounty dari kurikulum ini — hasilnya adalah keterampilan, bukan laporan.
