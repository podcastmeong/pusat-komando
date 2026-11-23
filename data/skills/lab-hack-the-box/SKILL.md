# Skill: Lab Hack The Box — Platform latihan legal Hack The Box — mesin rentan, tantangan, dan jalur belajar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 69. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: platform latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat membutuhkan latihan legal sebelum menguji program nyata — menyelesaikan mesin rentan atau tantangan Hack The Box untuk melatih teknik yang akan dipakai di bounty, atau saat tim butuh bukti latihan atas satu teknik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Jalur belajar TryHackMe → skill `jalur-belajar-tryhackme` (platform latihan lain).
- Lab PortSwigger Academy → skill `lab-portswigger-academy` (latihan web).
- Lab aplikasi rentan mobile → skill `lab-aplikasi-rentan-mobile` (latihan mobile).
- Kurikulum minggu pertama mobile → skill `kurikulum-minggu-pertama-mobile` (rencana belajar mobile).

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
11. **Scope guard kandidat:** Platform latihan; tanpa target nyata.

## Langkah + gerbang

### Gerbang 0 — Pastikan ini latihan, bukan target nyata

1. Konfirmasi aktivitas hanya di dalam platform Hack The Box (mesin/tantangan resmi) — bukan terhadap sistem di luar platform.
2. **Standar lulus:** nama mesin/tantangan + jalur belajar tercatat di log sebelum mulai.

### Gerbang 1 — Pilih mesin/tantangan sesuai teknik yang dilatih

1. Pilih mesin/tantangan yang melatih teknik yang dibutuhkan tim (mis. enumerasi web, privesc Linux, Active Directory) dan catat tujuannya.
2. **Standar lulus:** teknik target + mesin/tantangan tertulis; bukan sekadar bermain tanpa tujuan.

### Gerbang 2 — Selesaikan dengan metode yang terdokumentasi

1. Kerjakan mesin/tantangan langkah demi langkah; catat perintah/metode yang berhasil dan yang gagal.
2. Jangan menyalin write-up orang lain mentah-mentah — tulis ulang dengan pemahaman sendiri.
3. **Standar lulus:** langkah penyelesaian + pelajaran tercatat; flag/bukti penyelesaian dicatat.

### Gerbang 3 — Petakan pelajaran ke skill bounty

1. Tulis teknik apa dari latihan ini yang bisa dipakai di program nyata, dan skill bounty mana yang memakainya (atau ajukan skill baru bila belum ada).
2. **Standar lulus:** pemetaan teknik → skill bounty tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Platform Hack The Box (VPN lab + mesin/tantangan) | Latihan legal di lingkungan lab |
| Catatan latihan | Dokumentasi langkah + pelajaran |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [lab-hack-the-box] — No. 69
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Latihan legal di Hack The Box untuk menguasai teknik sebelum dipakai di program bounty nyata.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya mesin/tantangan resmi Hack The Box — jangan pernah memakai teknik latihan terhadap sistem nyata di luar platform.
- Write-up orang lain hanya rujukan; pemahaman sendiri yang dicatat.
- Tidak ada temuan bounty dari lab ini — hasilnya adalah keterampilan, bukan laporan.
