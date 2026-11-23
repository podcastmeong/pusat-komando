# Skill: Pass-the-Hash Lab — Memakai hash NTLM yang tertangkap untuk mengautentikasi tanpa mengetahui kata sandi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 83. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan aset infrastruktur; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai HANYA di lab sendiri untuk mempelajari pass-the-hash — memahami bagaimana hash NTLM bisa dipakai langsung sebagai kredensial autentikasi, agar celah serupa bisa dikenali di program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- SMB relay NTLM lab → skill `smb-relay-ntlm-lab` (relay sesi; skill ini memakai hash langsung).
- Cracking kata sandi Hydra/Hashcat → skill `cracking-kata-sandi-hydra-hashcat` (memecahkan hash; skill ini memakai hash tanpa memecahkannya).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Lab sendiri saja; tanpa hash milik orang lain.

## Langkah + gerbang

### Gerbang 0 — Konfirmasi lab sendiri

1. Pastikan SEMUA sistem adalah lab milik sendiri (VM lab, jaringan terisolasi). Bila ada sistem nyata = JANGAN MULAI.
2. **Standar lulus:** daftar sistem lab tercatat di log sebelum mulai.

### Gerbang 1 — Siapkan akun dan hash lab

1. Buat akun lab sendiri di VM lab; ekstrak hash NTLM akun lab itu dari VM lab sendiri (bukan dari sistem mana pun di luar lab).
2. **Standar lulus:** akun lab + sumber hash tertulis; hash berasal dari lab sendiri.

### Gerbang 2 — Uji autentikasi dengan hash

1. Autentikasi ke layanan lab (mis. SMB) memakai hash tersebut tanpa kata sandi; amati apakah diterima.
2. **Standar lulus:** hasil tercatat (diterima/ditolak + layanan yang diuji). Hash yang ditolak = hasil yang dicatat.

### Gerbang 3 — Catat mitigasi yang bekerja

1. Catat kontrol apa yang menggagalkan pass-the-hash di lab (mis. Credential Guard, pembatasan akun) sebagai pelajaran untuk pengujian program nyata.
2. **Standar lulus:** mitigasi + hasil tercatat; pelajaran dipetakan ke skill bounty yang relevan.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab VM sendiri (jaringan terisolasi) | Sistem sumber hash dan target autentikasi lab |
| Alat autentikasi NTLM | Autentikasi memakai hash di lab |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pass-the-hash-lab] — No. 83
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Autentikasi dengan hash NTLM akun lab sendiri berhasil (atau ditolak oleh kontrol) pada layanan lab.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: lab sendiri SAJA — tanpa hash milik orang lain, tanpa sistem nyata.
- Hash lab tidak boleh dipakai di luar lab; hapus materi lab setelah selesai bila berisi hash.
- Hasil lab adalah pembelajaran; temuan bounty hanya bila program eksplisit mencantumkan aset infra dan celah yang sama terbukti di sana.
