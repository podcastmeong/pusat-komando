# Skill: Lab UnCrackable Android — OWASP UnCrackable Apps Level 1–4 — reverse engineering + bypass deteksi root dan debugging

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 103. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: platform latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat membutuhkan latihan reverse engineering Android yang bertingkat — menyelesaikan OWASP UnCrackable Apps Level 1–4 (bypass deteksi root dan debugging) untuk melatih RE sebelum menguji program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Lab InjuredAndroid CTF → skill `lab-injuredandroid-ctf` (CTF flag; skill ini RE bertingkat).
- Bahasa Smali Android → skill `bahasa-smali-android` (teknik yang dilatih di level lanjut).
- Bypass deteksi root Magisk → skill `bypass-deteksi-root-magisk` (teknik bypass yang dilatih di sini).
- Panduan MASTG → skill `panduan-mastg` (acuan pengujian mobile).

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
11. **Scope guard kandidat:** Lab saja; aplikasi latihan, bukan target nyata.

## Langkah + gerbang

### Gerbang 0 — Pastikan ini latihan, bukan target nyata

1. Konfirmasi aktivitas hanya di aplikasi UnCrackable di emulator sendiri — bukan terhadap aplikasi nyata.
2. **Standar lulus:** level + tujuan latihan tercatat di log sebelum mulai.

### Gerbang 1 — Pilih level sesuai kemampuan

1. Mulai dari Level 1 dan naik bertingkat; catat teknik yang dilatih tiap level (decompile, bypass root, bypass debug, bypass native).
2. **Standar lulus:** level + teknik target tertulis.

### Gerbang 2 — Selesaikan level dengan metode sendiri

1. Kerjakan level langkah demi langkah (decompile, analisis Smali, Frida, patching) sampai secret/flag level didapat; catat metode yang berhasil dan gagal.
2. **Standar lulus:** flag + langkah penyelesaian tercatat per level.

### Gerbang 3 — Petakan pelajaran ke skill bounty

1. Tulis teknik apa yang dikuasai dan skill bounty mana yang memakainya.
2. **Standar lulus:** pemetaan teknik → skill bounty tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Emulator Android sendiri + aplikasi UnCrackable | Lingkungan latihan RE |
| Alat decompile + Frida | Analisis dan bypass di lab |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [lab-uncrackable-android] — No. 103
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Level UnCrackable selesai (flag didapat) dengan langkah yang terdokumentasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aplikasi latihan UnCrackable di emulator sendiri — jangan memakai tekniknya terhadap aplikasi nyata di luar program.
- Tidak ada temuan bounty dari lab ini — hasilnya adalah keterampilan, bukan laporan.
