# Skill: Pelarian VM Hypervisor — Keluar dari mesin virtual ke host — kelas temuan bernilai tinggi di program virtualisasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 86. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**. Skill ini untuk program yang eksplisit mencantumkan hypervisor/virtualisasi; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat program in-scope eksplisit mencantumkan hypervisor/virtualisasi dan ada dugaan celah yang memungkinkan tamu VM keluar ke host — kelas temuan bernilai tinggi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Eksploitasi memori buffer overflow → skill `eksploitasi-memori-buffer-overflow` (dasar eksploitasi memori; skill ini konteks hypervisor).
- Pivoting/tunneling → skill `pivoting-tunneling` (loncatan antar-host; skill ini keluar dari VM ke host).
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
11. **Scope guard kandidat:** Hanya bila program eksplisit mencantumkan hypervisor.

## Langkah + gerbang

### Gerbang 0 — Cek scope eksplisit hypervisor

1. Baca pasal scope: apakah hypervisor (nama + versi + komponen: perangkat virtual, hypercall) eksplisit in-scope? Tanpa pencantuman eksplisit = JANGAN UJI.
2. **Standar lulus:** komponen hypervisor + pasal scope tercatat di log sebelum mulai.

### Gerbang 1 — Pahami batas VM

1. Pelajari arsitektur hypervisor target (perangkat virtual yang diekspos ke tamu, hypercall, isolasi memori) dari dokumentasi publik.
2. **Standar lulus:** batas VM + permukaan perangkat virtual tertulis.

### Gerbang 2 — Uji dengan PoC aman di lab sendiri

1. Bangun lab sendiri (host + VM tamu) dengan hypervisor in-scope; uji SATU primitif pelarian dengan penanda canary milik sendiri, tanpa muatan berbahaya.
2. **Standar lulus:** hasil primitif tercatat (berhasil/gagal + bukti penanda). Tanpa penanda = belum terbukti.

### Gerbang 3 — Buktikan pelarian + serahkan ke triase

1. Bila primitif berhasil, buktikan dampak minimal yang aman (mis. membaca penanda canary di host dari dalam tamu) — jangan mengakses data host lain atau sistem lain.
2. Serahkan ke A60 audit → draf laporan → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab virtualisasi sendiri (host + VM tamu) | Lingkungan uji hypervisor |
| Alat debugging hypervisor | Amati perangkat virtual dan hypercall |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pelarian-vm-hypervisor] — No. 86
Program: [HUNTR, PPLX, MISTRAL]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Primitif pelarian VM berhasil membaca penanda canary di host dari dalam VM tamu lab sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- SCOPE GUARD MUTLAK: hanya bila program eksplisit mencantumkan hypervisor — tanpa itu, jangan uji.
- PoC hanya memakai penanda canary milik sendiri; tanpa muatan berbahaya, tanpa akses data host lain.
- Jangan menyebar PoC pelarian ke publik sebelum program menutup/memperbaiki temuan.
