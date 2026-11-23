# Skill: Cheat Sheet HackTricks Android — HackTricks Android Pentesting sebagai rujukan — perintah ADB, bypass SSL pinning, daftar cek celah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 105. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (rujukan)**. Skill rujukan: dipakai sebagai daftar cek saat menguji; pengujian hanya pada aplikasi sendiri / in-scope. Program yang dilayani: semua program sebagai rujukan, bukan sebagai target uji.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat menguji aplikasi Android in-scope dan butuh daftar cek cepat — perintah ADB, pola bypass SSL pinning, dan kelas celah Android dari HackTricks sebagai rujukan langkah pengujian.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Frida/Objection runtime → skill `frida-objection-runtime` (bypass SSL pinning yang dirujuk cheat sheet).
- Bypass SSL pinning → skill `bypass-ssl-pinning` (teknik yang dirujuk cheat sheet).
- Panduan MASTG → skill `panduan-mastg` (acuan pengujian mobile yang melengkapi cheat sheet).
- Komponen Android terekspos → skill `komponen-android-terekspos` (kelas celah yang dirujuk cheat sheet).

## Aturan keras

1. **Hanya program bounty resmi in-scope** — SEMUA (rujukan). Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Rujukan; pengujian hanya pada aplikasi sendiri / in-scope.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

1. Baca pasal scope program sebelum memakai satu pun perintah dari cheat sheet pada target nyata.
2. **Standar lulus:** aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Pilih bagian cheat sheet yang relevan

1. Pilih bagian yang sesuai dengan target uji (mis. ADB, SSL pinning, komponen, penyimpanan lokal) dan catat mengapa bagian itu relevan.
2. **Standar lulus:** bagian + alasan tertulis; bukan memakai seluruh cheat sheet tanpa arah.

### Gerbang 2 — Jalankan daftar cek pada aplikasi sendiri/in-scope

1. Jalankan perintah/cek satu per satu pada perangkat/emulator sendiri; catat hasil tiap cek (temuan/tidak).
2. **Standar lulus:** hasil per cek tercatat. Cek yang tidak relevan dicatat alasannya, bukan dilewati diam-diam.

### Gerbang 3 — Teruskan temuan ke skill yang sesuai

1. Setiap temuan dari daftar cek diteruskan ke skill bounty yang sesuai (mis. SSL pinning → `bypass-ssl-pinning`) untuk pembuktian dan laporan.
2. **Standar lulus:** pemetaan temuan → skill tertulis di log.

## Alat

| Alat | Cara pakai |
|---|---|
| HackTricks – Android Pentesting (rujukan daring) | Daftar cek + perintah rujukan |
| Perangkat/emulator Android sendiri + ADB | Menjalankan cek pada aplikasi sendiri/in-scope |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [cheat-sheet-hacktricks-android] — No. 105
Program: [SEMUA (rujukan)]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Daftar cek HackTricks yang relevan sudah dijalankan pada aplikasi sendiri/in-scope dan hasilnya tercatat per cek.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Cheat sheet adalah RUJUKAN, bukan izin — setiap perintah tetap tunduk pada scope program.
- Pengujian hanya pada aplikasi sendiri / in-scope; jangan menjalankan perintah cheat sheet pada aplikasi lain.
- Perintah yang destruktif atau menyadap pengguna lain tidak dijalankan walau tercantum di cheat sheet.
