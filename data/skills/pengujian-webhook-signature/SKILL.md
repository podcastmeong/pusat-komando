# Skill: Pengujian Webhook Signature — Verifikasi signature webhook yang lemah/tidak ada, replay event, dan SSRF lewat URL webhook

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 81. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope menerima atau mengirim webhook dan ada dugaan signature tidak diverifikasi (atau rahasianya lemah), event bisa di-replay, atau URL webhook bisa dipakai untuk SSRF.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- SSRF metadata cloud → skill `ssrf-metadata-cloud` (SSRF umum; skill ini lewat URL webhook).
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
11. **Scope guard kandidat:** Akun uji sendiri; tanpa memicu aksi pada sistem korban.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah fitur webhook target in-scope dan pengujiannya diizinkan?
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Inventarisasi webhook

1. Daftar webhook yang bisa dikonfigurasi/diterima akun sendiri: URL tujuan, event, dan cara signature dibuat/diverifikasi (dokumentasi + perilaku nyata).
2. **Standar lulus:** daftar webhook + mekanisme signature tertulis.

### Gerbang 2 — Uji verifikasi signature

1. Kirim event canary ke endpoint webhook milik sendiri TANPA signature, dengan signature salah, dan dengan signature lama; amati mana yang diterima.
2. **Standar lulus:** hasil tiap varian tercatat (diterima/ditolak). Signature yang divalidasi benar = AMAN.

### Gerbang 3 — Uji replay dan URL webhook

1. Replay event canary yang sama dua kali; amati apakah event kedua diproses lagi (tanpa perlindungan replay).
2. Bila URL webhook bisa diatur, arahkan ke server canary milik sendiri dan periksa apakah server target memanggilnya (SSRF lewat webhook) — hanya server canary milik sendiri sebagai tujuan.
3. **Standar lulus:** hasil replay + hasil pemanggilan URL canary tercatat.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Kirim event webhook dengan variasi signature |
| Server canary milik sendiri | Tujuan URL webhook untuk membuktikan pemanggilan |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-webhook-signature] — No. 81
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Event webhook canary diterima tanpa signature yang valid, atau event yang sama diproses dua kali, atau URL webhook memanggil server canary milik sendiri.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun dan webhook milik sendiri; jangan memicu aksi pada sistem korban atau mengirim event palsu ke pihak ketiga.
- Jangan memakai URL webhook untuk mengakses layanan internal korban; tujuan uji hanya server canary milik sendiri.
- Jangan memicu aksi nyata (pembayaran, pengiriman) lewat replay event.
