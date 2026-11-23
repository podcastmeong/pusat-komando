# Skill: Pembajakan WebSocket CSWSH — Cross-Site WebSocket Hijacking — halaman lain membuka koneksi WebSocket korban tanpa validasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 78. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope memakai WebSocket untuk data/aksi sensitif dan ada dugaan handshake WebSocket tidak memvalidasi Origin — sehingga halaman di origin lain bisa membuka koneksi memakai sesi korban.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menjalankan pengujian eksploitasi dan mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis WebSocket/gRPC → skill `analisis-websocket-grpc` (pemetaan komunikasi; skill ini menguji hijacking-nya).
- Deteksi CSRF → skill `deteksi-csrf` (CSRF klasik; skill ini khusus WebSocket).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa membajak sesi pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah target dan pengujian WebSocket diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu koneksi pun dibuat.

### Gerbang 1 — Identifikasi endpoint WebSocket dan data yang lewat

1. Catat URL WebSocket, pesan yang dipertukarkan, dan apakah koneksi memakai cookie sesi (kredensial otomatis terkirim browser).
2. **Standar lulus:** endpoint + jenis pesan + mekanisme autentikasi tertulis.

### Gerbang 2 — Uji validasi Origin pada handshake

1. Kirim handshake WebSocket dengan header Origin lain (milik sendiri) memakai sesi akun sendiri; amati apakah server menerima koneksi.
2. **Standar lulus:** hasil tercatat (diterima/ditolak + Origin yang dipakai). Handshake yang ditolak = AMAN.

### Gerbang 3 — PoC lintas-origin di browser sendiri

1. Buat halaman PoC milik sendiri di origin canary yang membuka WebSocket ke target memakai sesi login akun sendiri; periksa apakah pesan dari akun sendiri bisa dibaca/dikirim lewat halaman itu.
2. Hanya data/akun sendiri yang dipakai; setelah berhasil, tutup koneksi dan catat.
3. **Standar lulus (gerbang utama):** tanpa pesan akun sendiri yang berhasil dibaca/dikirim lewat origin lain = BELUM BERHASIL.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti PoC ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien WebSocket | Kirim handshake dengan Origin lain |
| Halaman PoC milik sendiri (origin canary) | Buka WebSocket lintas-origin dengan sesi sendiri |
| Browser milik sendiri | Tempat PoC dijalankan |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pembajakan-websocket-cswsh] — No. 78
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Handshake WebSocket dengan Origin lain diterima dan pesan akun uji sendiri bisa dibaca/dikirim lewat halaman origin canary.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Tanpa membajak sesi pengguna lain — PoC hanya memakai sesi akun sendiri.
- Halaman PoC jangan di-host di tempat umum; hanya di lingkungan terkendali milik sendiri.
- Bila WebSocket hanya membawa data publik/tidak sensitif, nilailah dampak apa adanya; jangan membesar-besarkan.
