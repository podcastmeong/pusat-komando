# Skill: Lab PortSwigger Academy — Web Security Academy gratis — lab per kelas kerentanan web dengan penjelasan interaktif

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 70. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**. Skill latihan: platform latihan SAJA, tanpa target nyata. Program yang dilayani: semua program sebagai bekal latihan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat membutuhkan latihan web gratis per kelas kerentanan — menyelesaikan lab PortSwigger Web Security Academy untuk melatih teknik (SQLi, XSS, SSRF, dsb.) sebelum menguji program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian/lab di lingkungan terkendali milik sendiri dan mencatat hasilnya |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penguasaan Burp Suite Community → skill `penguasaan-burp-suite-community` (alat yang dipakai di lab ini).
- Lab Hack The Box → skill `lab-hack-the-box` (platform latihan lain).
- Injeksi SQL kontekstual → skill `injeksi-sql-kontekstual` (teknik yang dilatih di lab SQLi).
- Deteksi CSRF → skill `deteksi-csrf` (teknik yang dilatih di lab CSRF).

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

1. Konfirmasi aktivitas hanya di lab resmi PortSwigger Academy — bukan terhadap sistem di luar platform.
2. **Standar lulus:** nama lab + kelas kerentanan tercatat di log sebelum mulai.

### Gerbang 1 — Baca materi, pilih lab

1. Baca penjelasan kelas kerentanan di Academy, lalu pilih lab yang sesuai dengan tingkat (Apprentice/Practitioner/Expert).
2. **Standar lulus:** kelas + tingkat lab tertulis; tujuan latihan jelas.

### Gerbang 2 — Selesaikan lab dengan metode sendiri

1. Kerjakan lab langkah demi langkah memakai Burp Suite Community; catat payload/metode yang berhasil dan yang gagal.
2. Bila mentok, baca kembali penjelasan Academy sebelum melihat solusi.
3. **Standar lulus:** lab selesai (atau alasan kegagalan tercatat) + langkah penyelesaian didokumentasikan.

### Gerbang 3 — Petakan pelajaran ke skill bounty

1. Tulis teknik apa yang dikuasai dan skill bounty mana yang memakainya; catat perbedaan antara lab dan target nyata (mis. WAF, rate limit).
2. **Standar lulus:** pemetaan teknik → skill bounty tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| PortSwigger Web Security Academy | Lab gratis per kelas kerentanan |
| Burp Suite Community | Alat pengujian di lab |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [lab-portswigger-academy] — No. 70
Program: [SEMUA (latihan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Latihan web gratis di PortSwigger Academy untuk menguasai kelas kerentanan sebelum dipakai di program bounty nyata.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya lab resmi Academy — jangan memakai teknik lab terhadap sistem nyata di luar platform.
- Solusi lab hanya dibaca bila sudah mentok; pemahaman sendiri yang dicatat.
- Tidak ada temuan bounty dari lab ini — hasilnya adalah keterampilan, bukan laporan.
