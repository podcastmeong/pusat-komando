# Skill: Pelarian Sandbox Browser — Keluar dari sandbox browser ke proses sistem — kelas temuan bernilai tinggi di program browser

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 85. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program yang eksplisit mencantumkan browser; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat program in-scope eksplisit mencantumkan browser (atau komponennya: renderer, sandbox, IPC) dan ada dugaan celah yang memungkinkan proses renderer keluar dari sandbox ke proses sistem.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pengujian ekstensi browser → skill `pengujian-ekstensi-browser` (ekstensi; skill ini sandbox browser itu sendiri).
- Eksploitasi memori buffer overflow → skill `eksploitasi-memori-buffer-overflow` (dasar eksploitasi memori; skill ini konteks sandbox).
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
11. **Scope guard kandidat:** Hanya bila program eksplisit mencantumkan browser.

## Langkah + gerbang

### Gerbang 0 — Cek scope eksplisit browser

1. Baca pasal scope: apakah browser (nama + versi + komponen: renderer/sandbox/IPC) eksplisit in-scope? Tanpa pencantuman eksplisit = JANGAN UJI.
2. **Standar lulus:** komponen browser + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Pahami batas sandbox

1. Pelajari arsitektur sandbox browser target (proses renderer vs broker, kebijakan IPC, batas sistem yang berlaku) dari dokumentasi publik.
2. **Standar lulus:** batas sandbox + permukaan IPC tertulis.

### Gerbang 2 — Uji dengan PoC aman di lingkungan sendiri

1. Bangun PoC yang menguji SATU primitif pelarian (mis. akses sumber daya di luar sandbox) di browser in-scope pada perangkat sendiri; PoC hanya membaca penanda canary milik sendiri, tanpa muatan berbahaya.
2. **Standar lulus:** hasil primitif tercatat (berhasil/gagal + bukti penanda). Tanpa penanda = belum terbukti.

### Gerbang 3 — Buktikan pelarian + serahkan ke triase

1. Bila primitif berhasil, buktikan dampak minimal yang aman (mis. membaca file canary milik sendiri di luar sandbox) — jangan mengakses data pengguna lain atau sistem lain.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim. Kelas temuan ini bernilai tinggi; laporkan dengan bukti yang rapi.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser in-scope di perangkat sendiri | Lingkungan uji sandbox |
| Alat debugging browser | Amati proses renderer, IPC, dan crash |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pelarian-sandbox-browser] — No. 85
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Primitif pelarian sandbox berhasil membaca penanda canary milik sendiri di luar sandbox browser in-scope.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: hanya bila program eksplisit mencantumkan browser — tanpa itu, jangan uji.
- PoC hanya memakai penanda canary milik sendiri; tanpa muatan berbahaya, tanpa akses data orang lain.
- Jangan menyebar PoC pelarian ke publik sebelum program menutup/memperbaiki temuan.
