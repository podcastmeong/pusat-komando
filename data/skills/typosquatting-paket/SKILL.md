# Skill: Typosquatting Paket — Typosquatting paket: nama paket yang mirip (salah ketik) dan dipakai untuk menyusup ke rantai pasok perangkat lunak.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 65 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis typosquatting paket: nama paket yang mirip (salah ketik) dan dipakai untuk menyusup ke rantai pasok perangkat lunak. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Deteksi/pelaporan saja; tanpa menyebar paket jahat.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `dependency-confusion` (No. 64) — penyusupan rantai pasok lewat resolusi registry
- `recon-rantai-pasok-cicd` — recon rantai pasok CI/CD
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
11. **Scope guard kandidat ini (WAJIB):** Deteksi/pelaporan saja; tanpa menyebar paket jahat.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: deteksi/pelaporan saja; tanpa menyebar paket jahat. Skill ini mendeteksi typosquatting, bukan melakukannya.

## Langkah + gerbang

### Gerbang 0 — Cek pencantuman rantai pasok dulu

- Baca pasal scope: typosquatting HANYA relevan bila program mencantumkan rantai pasok/dependensi. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pencantuman rantai pasok tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Daftar paket populer yang dipakai target

- Dari manifest/lockfile target in-scope yang tersedia secara sah, daftar paket populer yang dipakai dan versinya.

**Standar lulus:** Daftar paket populer tercatat.

### Gerbang 2 — Cari nama mirip di registry publik

- Untuk tiap paket populer, periksa apakah ada nama mirip (satu huruf beda, huruf tertukar, tanda hubung hilang) yang terdaftar di registry publik.
- Catat nama mirip + pemilik + tanggal terbit + jumlah unduhan.

**Standar lulus:** Daftar nama mirip tercatat.

### Gerbang 3 — Nilai apakah nama mirip itu berbahaya

- Periksa isi paket mirip (read-only, metadata + berkas yang terlihat): apakah isinya meniru paket asli dengan tambahan berbahaya, atau hanya paket lain yang sah dan tidak terkait?
- Jangan mengunduh dan menjalankan paket yang mencurigakan; pemeriksaan metadata saja.

**Standar lulus:** Penilaian tiap nama mirip tercatat (berbahaya/sah/tidak terkait).

### Gerbang 4 — Laporkan deteksi ke triase

- Serahkan nama mirip yang terbukti meniru paket populer dengan isi berbahaya ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Jangan menyebar paket apa pun.

**Standar lulus:** Keputusan triase tercatat; tidak ada paket yang disebar.

## Alat

| Alat | Cara pakai |
|---|---|
| Registry publik (npm/PyPI/dll.) — hanya untuk MEMERIKSA | Periksa nama mirip paket populer; jangan mengunggah paket apa pun. |
| Daftar paket populer target in-scope (bila tersedia secara sah) | Daftar paket yang dipakai target; bandingkan dengan nama mirip di publik. |
| Alat pembanding nama (pemeriksaan ejaan) | Membandingkan nama paket populer dengan nama yang terdaftar di publik. |
| `~/workspace/catatan/log-bug-bounty.md` | Log nama mirip yang ditemukan dan penilaiannya. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [typosquatting-paket — No. 65]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Nama mirip belum tentu jahat — banyak paket sah yang namanya kebetulan mirip. Yang dinilai adalah isi dan niat meniru, bukan kemiripan nama semata. Jangan pernah membuat atau mengunggah paket typosquat, walau 'untuk bukti'.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
