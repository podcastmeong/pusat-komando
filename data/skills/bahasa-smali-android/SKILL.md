# Skill: Bahasa Smali Android — Smali (assembly Android) — membaca dan mengubah logika kode secara permanen di APK hasil decompile

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 101. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program yang mencantumkan aplikasi mobile; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat analisis APK in-scope butuh membaca atau mengubah logika di tingkat Smali — mis. memahami cek keamanan yang tidak terlihat di decompile Java, atau membuktikan suatu cek bisa diubah secara permanen.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Dekompilasi aplikasi mobile → skill `dekompilasi-aplikasi-mobile` (decompile APK; skill ini membaca/mengubah Smali-nya).
- Struktur APK/AAB/IPA → skill `struktur-apk-aab-ipa` (isi APK; skill ini bahasa Smali di dalamnya).
- Frida/Objection runtime → skill `frida-objection-runtime` (ubah perilaku saat jalan; skill ini ubah permanen di Smali).
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
11. **Scope guard kandidat:** Hanya APK sendiri / target in-scope; lab sendiri.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aplikasi Android ini eksplisit in-scope dan apakah modifikasi APK diizinkan untuk pembuktian?
2. **Standar lulus:** aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Decompile dan temukan logika target

1. Decompile APK milik sendiri/in-scope; temukan metode Smali yang relevan (mis. cek root, cek lisensi, validasi token) dan catat logikanya.
2. **Standar lulus:** metode + logika Smali tertulis (nama metode + alur).

### Gerbang 2 — Baca dan pahami, jangan ubah dulu

1. Baca Smali sampai alur logika dipahami (kondisi, lompatan, pemanggilan); catat hipotesis kelemahan sebelum mengubah apa pun.
2. **Standar lulus:** hipotesis tertulis sebelum modifikasi. Tanpa hipotesis = jangan mengubah.

### Gerbang 3 — Uji modifikasi di lab sendiri

1. Ubah SATU kondisi Smali pada salinan APK di lab sendiri (mis. balikkan hasil cek), bangun ulang, dan jalankan di emulator sendiri; amati apakah perilaku berubah sesuai hipotesis.
2. **Standar lulus:** hasil tercatat (perilaku berubah/tidak + bukti). Tanpa perubahan = belum terbukti.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (logika Smali + modifikasi lab yang mengubah perilaku) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator Android sendiri | Lingkungan uji APK hasil modifikasi |
| Alat decompile (apktool, JADX) | Baca dan ubah Smali |
| ADB | Pasang dan jalankan APK lab |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bahasa-smali-android] — No. 101
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Modifikasi satu kondisi Smali pada salinan APK di lab sendiri mengubah perilaku cek keamanan sesuai hipotesis.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya APK sendiri / target in-scope; lab sendiri. Jangan memodifikasi APK orang lain.
- APK hasil modifikasi hanya dipakai di emulator/perangkat sendiri; jangan disebar atau dipasang di perangkat orang lain.
- Jangan memakai modifikasi untuk melewati pembayaran/lisensi di layanan nyata.
