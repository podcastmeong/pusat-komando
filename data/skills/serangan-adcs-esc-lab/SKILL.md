# Skill: Serangan ADCS ESC Lab — Template sertifikat Active Directory yang salah konfigurasi (ESC1–ESC8) hingga penerbitan sertifikat istimewa

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 84. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan aset infrastruktur; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai HANYA di lab sendiri (atau infra in-scope eksplisit) untuk mempelajari serangan ADCS — memahami bagaimana template sertifikat yang salah konfigurasi (ESC1–ESC8) memungkinkan penerbitan sertifikat istimewa, agar celah serupa bisa dikenali di program nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Eskalasi hak akses Windows → skill `eskalasi-hak-akses-windows` (privesc lokal; skill ini lewat sertifikat AD).
- Analisis Active Directory lewat MCP → skill `analisis-active-directory-lewat-mcp` (pemetaan AD; skill ini serangan template sertifikat).
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
11. **Scope guard kandidat:** Lab sendiri / infra in-scope eksplisit saja.

## Langkah + gerbang

### Gerbang 0 — Konfirmasi lab sendiri / infra in-scope eksplisit

1. Pastikan SEMUA sistem adalah lab AD milik sendiri (domain controller lab, CA lab) atau infra yang eksplisit in-scope. Bila ada sistem nyata = JANGAN MULAI.
2. **Standar lulus:** daftar sistem lab + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Enumerasi template sertifikat lab

1. Daftar template sertifikat di CA lab: siapa yang bisa mendaftar, apakah SAN bisa ditentukan pendaftar, dan EKU apa yang diizinkan.
2. Petakan template ke kelas ESC1–ESC8 berdasarkan konfigurasinya.
3. **Standar lulus:** daftar template + pemetaan ESC tertulis.

### Gerbang 2 — Uji penerbitan sertifikat di lab

1. Minta sertifikat dari satu template yang dicurigai memakai akun lab sendiri; periksa EKU/SAN sertifikat yang diterbitkan.
2. **Standar lulus:** hasil penerbitan tercatat (diterbitkan/ditolak + isi sertifikat). Template yang menolak = hasil yang dicatat.

### Gerbang 3 — Uji pemakaian sertifikat (lab saja)

1. Bila sertifikat istimewa diterbitkan di lab, uji autentikasinya terhadap layanan lab sendiri dan catat hasilnya.
2. **Standar lulus:** hasil autentikasi tercatat; pelajaran dan mitigasi (template aman) dipetakan ke skill bounty yang relevan.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab Active Directory sendiri (DC + CA lab) | Domain dan otoritas sertifikat lab |
| Alat enumerasi template sertifikat | Daftar template dan konfigurasinya di lab |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [serangan-adcs-esc-lab] — No. 84
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Template sertifikat lab memungkinkan penerbitan sertifikat istimewa (kelas ESC) oleh akun lab sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: lab sendiri / infra in-scope eksplisit SAJA — tanpa AD nyata, tanpa sertifikat milik orang lain.
- Sertifikat lab tidak boleh dipakai di luar lab; cabut/hapus setelah selesai.
- Hasil lab adalah pembelajaran; temuan bounty hanya bila program eksplisit mencantumkan aset infra dan celah yang sama terbukti di sana.
