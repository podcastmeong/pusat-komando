# Skill: Upload SVG XSS — Upload file SVG berisi JavaScript yang dieksekusi saat dibuka — stored XSS lewat file gambar.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 31 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis upload file SVG berisi JavaScript yang dieksekusi saat dibuka — stored XSS lewat file gambar. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa file berbahaya di luar PoC.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `bypass-unggah-file` — bypass unggah file umum (polyglot, MIME, ekstensi ganda)
- `verifikasi-xss` — XSS dasar
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa file berbahaya di luar PoC.
12. **Catatan khusus kandidat:** SVG adalah XML sehingga bisa memuat skrip; celahnya ada bila server menerima SVG dan menyajikannya sebagai gambar yang bisa dieksekusi, bukan bila server hanya menyimpan file.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah unggah file dan XSS in-scope pada target ini? Catat di log sebelum menguji.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan alur unggah dan penyajian

- Catat endpoint unggah, jenis file yang diterima, dan cara file disajikan kembali (URL langsung, pratinjau, unduhan, content-type, content-disposition).
- Periksa apakah SVG disajikan dengan content-type image/svg+xml dan tanpa header yang memblokir eksekusi skrip.

**Standar lulus:** Alur unggah → penyajian tercatat dengan header penyajian file.

### Gerbang 2 — Unggah SVG canary jinak

- Unggah SVG yang hanya berisi skrip canary milik sendiri (mis. mengubah teks halaman akun sendiri) — tanpa skrip yang mencuri data atau menyerang pengguna lain.
- Catat apakah unggahan diterima, di mana file disimpan, dan URL penyajiannya.

**Standar lulus:** File SVG canary diterima dan URL penyajiannya tercatat, atau penolakan tercatat.

### Gerbang 3 — Buktikan eksekusi saat dibuka di sesi sendiri

- Buka URL file SVG di browser milik sendiri dalam sesi akun sendiri dan periksa apakah skrip canary dieksekusi.
- Bila file dipaksa unduh atau disajikan dengan header yang memblokir skrip, itu bukan temuan — catat dan tutup.

**Standar lulus:** Eksekusi skrip canary teramati pada sesi sendiri, atau pemblokiran tercatat.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (siapa yang membuka file, skrip apa yang jalan) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Hapus file uji dari akun sendiri setelah bukti didapat.

**Standar lulus:** Dampak ditulis konkret + keputusan triase tercatat; file uji dihapus.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri | Buka file SVG hasil unggahan di sesi akun sendiri dan amati eksekusinya. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai; file SVG hanya berisi skrip canary milik sendiri. |
| `~/workspace/catatan/log-bug-bounty.md` | Log file yang diunggah, respons server, dan hasil eksekusi. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [unggah-svg-xss — No. 31]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak aplikasi menyajikan SVG dengan content-disposition attachment atau content-type yang aman — itu pemblokiran yang sah, bukan temuan. Jangan mengunggah SVG berisi skrip berbahaya ke layanan yang dipakai pengguna lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
