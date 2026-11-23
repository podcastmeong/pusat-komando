# Skill: Komponen Android Terekspos — Exported Activity, Service, Broadcast Receiver, dan Content Provider yang membocorkan data

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 98. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program yang mencantumkan aplikasi mobile; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat aplikasi Android in-scope diduga mengekspos komponen (Activity/Service/Receiver/Provider dengan `exported=true`) yang bisa dipanggil aplikasi lain — membuka layar sensitif tanpa login, memicu aksi, atau membaca data lewat Content Provider. Pendalaman dari langkah enumerasi komponen di `pipeline-redteam-apk`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pipeline redteam APK → skill `pipeline-redteam-apk` (alur redteam APK; skill ini pendalaman enumerasi komponennya).
- Struktur APK/AAB/IPA → skill `struktur-apk-aab-ipa` (isi APK; skill ini komponen yang terekspos).
- Deep link & intent hijacking → skill `deep-link-intent-hijacking` (intent; skill ini komponen exported).
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
11. **Scope guard kandidat:** Hanya aplikasi sendiri / target in-scope.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aplikasi Android ini (nama + versi) eksplisit in-scope?
2. **Standar lulus:** aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Enumerasi komponen dari AndroidManifest.xml

1. Baca AndroidManifest.xml APK milik sendiri/in-scope: daftar komponen dengan `exported=true` (Activity, Service, Broadcast Receiver, Content Provider) beserta intent-filter dan permission-nya.
2. **Standar lulus:** daftar komponen terekspos tertulis (nama + jenis + permission).

### Gerbang 2 — Uji pemanggilan komponen dari aplikasi uji sendiri

1. Dari aplikasi uji milik sendiri, panggil SATU komponen terekspos (mis. buka Exported Activity, kirim broadcast, query Content Provider) dengan data canary milik sendiri.
2. **Standar lulus:** hasil pemanggilan tercatat (berhasil/ditolak + apa yang terjadi). Komponen yang menolak = AMAN.

### Gerbang 3 — Buktikan dampak pada data/layar sendiri

1. Buktikan dampak HANYA pada akun/data sendiri: layar sensitif terbuka tanpa login, atau Content Provider mengembalikan data milik sendiri tanpa otorisasi.
2. **Standar lulus:** dampak tercatat (layar/data apa + tanpa login). Tanpa dampak = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator Android sendiri | Lingkungan uji aplikasi Android |
| ADB | Panggil komponen dan baca log |
| Aplikasi uji milik sendiri | Pemanggil komponen terekspos |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [komponen-android-terekspos] — No. 98
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Komponen Android terekspos pada aplikasi in-scope bisa dipanggil aplikasi uji sendiri dan membuka layar sensitif atau data milik sendiri tanpa login.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya aplikasi sendiri / target in-scope; jangan menguji aplikasi lain di perangkat.
- Hanya data/akun sendiri yang diakses lewat komponen; tanpa data pengguna lain.
- Jangan memicu aksi destruktif lewat komponen (hapus/kirim) — bila komponen hanya bisa dibuktikan lewat aksi destruktif, serahkan ke Muse.
