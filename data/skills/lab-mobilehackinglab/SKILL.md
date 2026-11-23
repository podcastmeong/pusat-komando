# Skill: Lab MobileHackingLab — Lab gratis berbasis browser dengan perangkat Android di cloud untuk latihan pengujian mobile

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 106. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: platform latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat membutuhkan perangkat Android lab tanpa emulator lokal — memakai MobileHackingLab (lab gratis berbasis browser, perangkat Android di cloud) untuk latihan pengujian mobile sebelum menguji program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Lab aplikasi rentan mobile → skill `lab-aplikasi-rentan-mobile` (lab lokal; skill ini lab cloud).
- Lab InjuredAndroid CTF → skill `lab-injuredandroid-ctf` (aplikasi latihan yang bisa dipakai di lab ini).
- Panduan MASTG → skill `panduan-mastg` (acuan pengujian mobile yang dipakai saat latihan).
- Kurikulum minggu pertama mobile → skill `kurikulum-minggu-pertama-mobile` (rencana belajar yang memakai lab ini).

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
11. **Scope guard kandidat:** Lab saja; tanpa target nyata.

## Langkah + gerbang

### Gerbang 0 — Pastikan ini latihan, bukan target nyata

1. Konfirmasi aktivitas hanya di perangkat lab MobileHackingLab — bukan terhadap sistem di luar platform.
2. **Standar lulus:** nama lab/sesi + tujuan latihan tercatat di log sebelum mulai.

### Gerbang 1 — Pilih perangkat dan aplikasi latihan

1. Pilih perangkat Android lab dan aplikasi latihan yang tersedia; catat teknik yang dilatih.
2. **Standar lulus:** perangkat + aplikasi + teknik target tertulis.

### Gerbang 2 — Kerjakan latihan di perangkat lab

1. Kerjakan latihan langkah demi langkah di perangkat lab; catat metode yang berhasil dan yang gagal.
2. **Standar lulus:** langkah penyelesaian + pelajaran tercatat.

### Gerbang 3 — Petakan pelajaran ke skill bounty

1. Tulis teknik apa yang dikuasai dan skill bounty mana yang memakainya.
2. **Standar lulus:** pemetaan teknik → skill bounty tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| MobileHackingLab (lab cloud berbasis browser) | Perangkat Android lab untuk latihan |
| Catatan latihan | Dokumentasi langkah + pelajaran |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [lab-mobilehackinglab] — No. 106
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Latihan di MobileHackingLab selesai dengan langkah yang terdokumentasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya perangkat lab MobileHackingLab — jangan memakai teknik latihan terhadap sistem nyata di luar platform.
- Jangan mengunggah data pribadi atau kredensial nyata ke perangkat lab cloud.
- Tidak ada temuan bounty dari lab ini — hasilnya adalah keterampilan, bukan laporan.
