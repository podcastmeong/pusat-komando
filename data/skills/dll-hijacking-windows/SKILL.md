# Skill: DLL Hijacking Windows — Aplikasi memuat DLL dari lokasi yang bisa ditulis sehingga kode berjalan atas nama aplikasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 72. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang mencantumkan aplikasi Windows; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat aplikasi Windows in-scope diduga memuat DLL dari direktori yang bisa ditulis (mis. direktori kerja aplikasi, PATH) tanpa verifikasi — sehingga DLL canary bisa dimuat dan kode berjalan atas nama aplikasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Eskalasi hak akses Windows → skill `eskalasi-hak-akses-windows` (privesc lokal; skill ini tentang pemuatan DLL aplikasi).
- Pengujian aplikasi Electron → skill `pengujian-electron-desktop` (aplikasi desktop; skill ini khusus Windows DLL).
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
11. **Scope guard kandidat:** Lab sendiri / aplikasi in-scope; tanpa menyebar DLL jahat.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah aplikasi Windows ini eksplisit in-scope? Bila hanya lab sendiri, konfirmasi aplikasi uji adalah milik sendiri.
2. **Standar lulus:** aplikasi + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Identifikasi urutan pencarian DLL

1. Pantau DLL apa yang dicari aplikasi saat jalan (mis. dengan Process Monitor di lab sendiri): nama DLL, urutan direktori yang dicari, dan direktori mana yang bisa ditulis.
2. **Standar lulus:** nama DLL + direktori yang bisa ditulis tertulis. Tanpa direktori yang bisa ditulis = tidak rentan lewat jalur ini.

### Gerbang 2 — Uji dengan DLL canary di lab sendiri

1. Letakkan DLL canary TIDAK BERBAHAYA (hanya menulis penanda ke file log milik sendiri, tanpa muatan jahat) di direktori yang bisa ditulis, lalu jalankan aplikasi dan periksa apakah DLL dimuat.
2. **Standar lulus:** bukti pemuatan DLL canary (penanda di log) tercatat. Tanpa penanda = tidak terbukti.

### Gerbang 3 — Nilai dampak + serahkan ke triase

1. Tulis dampak: kode apa yang bisa berjalan atas nama aplikasi bila DLL diganti (privilege aplikasi, akses file aplikasi) — tanpa pernah memakai DLL berbahaya.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat. Tanpa bukti = belum berhasil.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/lab Windows sendiri | Lingkungan uji aplikasi Windows |
| Process Monitor | Pantau pencarian dan pemuatan DLL |
| DLL canary tidak berbahaya | Penanda pemuatan saja, tanpa muatan jahat |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [dll-hijacking-windows] — No. 72
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Aplikasi Windows in-scope memuat DLL dari direktori yang bisa ditulis sehingga DLL canary dimuat atas nama aplikasi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya DLL canary tidak berbahaya — JANGAN PERNAH membuat atau menyebar DLL jahat.
- Hanya lab sendiri / aplikasi in-scope; jangan menaruh DLL di direktori aplikasi orang lain.
- Bila aplikasi berjalan dengan hak tinggi, dampak lebih besar — catat hak aplikasi apa adanya, jangan membesar-besarkan.
