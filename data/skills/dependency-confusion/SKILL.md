# Skill: Dependency Confusion — Dependency confusion: paket internal yang dibajak lewat registry publik karena namespace/resolusi tidak diprioritaskan.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 64 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis dependency confusion: paket internal yang dibajak lewat registry publik karena namespace/resolusi tidak diprioritaskan. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya bila program mencantumkan rantai pasok; tanpa menyebar paket jahat.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `recon-rantai-pasok-cicd` — recon rantai pasok CI/CD
- `typosquatting-paket` (No. 65) — penyusupan rantai pasok lewat nama mirip
- `dorking-secret-github` — pencarian secret di repo publik
- `triase-duplikat` + `laporan-abstrak` — validasi dan pelaporan
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser/perangkat pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyalin, atau memakai data milik pengguna lain — walau terlihat.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pakai jeda antar-permintaan dan hentikan bila target melambat.
6. **Tanpa payload di permukaan publik.** Halaman/file PoC jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus/mengubah data, merusak layanan, menyebar paket/file berbahaya, atau memakai kredensial yang terbaca di luar PoC. Pembuktian HARUS aman, minimal, dan reversibel.
11. **Scope guard kandidat ini (WAJIB):** Hanya bila program mencantumkan rantai pasok; tanpa menyebar paket jahat.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya bila program mencantumkan rantai pasok; tanpa menyebar paket jahat. Pembuktian dependency confusion TIDAK PERNAH memakai unggahan paket — pemeriksaan nama + konfigurasi resolver sudah cukup.

## Langkah + gerbang

### Gerbang 0 — Cek pencantuman rantai pasok dulu

- Baca pasal scope: dependency confusion HANYA bila program mencantumkan rantai pasok/dependensi sebagai in-scope. Tanpa pencantuman = jangan diuji.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pencantuman rantai pasok tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Inventarisasi nama paket internal

- Dari manifest/lockfile target in-scope yang tersedia secara sah, daftar nama paket internal (namespace perusahaan) beserta versi dan sumber registry yang dipakai.
- Jangan mengambil daftar dependensi dari sumber yang bukan hak target.

**Standar lulus:** Daftar paket internal tercatat.

### Gerbang 2 — Periksa keberadaan nama yang sama di registry publik

- Periksa (read-only) apakah nama paket internal itu juga terdaftar di registry publik, dan versi mana yang akan dipilih resolver bila kedua sumber tersedia.
- Jangan mengunggah paket apa pun ke registry publik — pemeriksaan saja.

**Standar lulus:** Hasil pemeriksaan tiap nama tercatat (ada/tidak di publik + versi).

### Gerbang 3 — Nilai urutan resolusi

- Nilai apakah konfigurasi resolver target memprioritaskan registry internal atau tidak (dari dokumentasi/konfigurasi yang tersedia secara sah). Bila tidak ada bukti konfigurasi, catat sebagai hipotesis yang belum terkonfirmasi — bukan temuan.
- Jangan membuktikan dengan mengunggah paket jahat; pembuktian lewat unggahan DILARANG.

**Standar lulus:** Penilaian resolusi tercatat; tidak ada paket yang diunggah.

### Gerbang 4 — Serahkan ke triase

- Bila ada nama internal yang juga ada di publik DAN bukti konfigurasi resolver tidak memprioritaskan internal, serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Bila tidak, tutup dengan buktinya.

**Standar lulus:** Keputusan triase tercatat; tidak ada paket yang disebar.

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar dependensi aplikasi target in-scope (bila tersedia secara sah) | Satu-satunya daftar yang diperiksa; dari manifest/lockfile yang sah. |
| Registry publik (npm/PyPI/dll.) — hanya untuk MEMERIKSA keberadaan nama paket | Periksa apakah nama paket internal juga ada di registry publik; jangan mengunggah paket apa pun. |
| Akun tes sendiri | Satu-satunya akun yang dipakai. |
| `~/workspace/catatan/log-bug-bounty.md` | Log nama paket, hasil pemeriksaan, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [dependency-confusion — No. 64]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Nama paket internal yang juga ada di registry publik belum tentu celah — yang menentukan adalah urutan resolusi. Jangan pernah mengunggah paket ke registry publik untuk 'membuktikan' celah ini.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
