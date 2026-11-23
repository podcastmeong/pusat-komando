# Skill: Mass Assignment API — Mass assignment (auto-binding): field sensitif (mis. is_admin, harga) yang bisa diisi lewat parameter API yang tidak difilter.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 62 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis mass assignment (auto-binding): field sensitif (mis. is_admin, harga) yang bisa diisi lewat parameter API yang tidak difilter. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa mengubah data pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `dokumentasi-api-otorisasi-endpoint` — matriks otorisasi per endpoint (tempat field sensitif ditemukan)
- `access-control-differential-analyst` — perbandingan respons lintas akun (BOLA/IDOR)
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa mengubah data pengguna lain.
12. **Catatan khusus kandidat:** Mass assignment terjadi bila framework mengikat semua parameter permintaan ke objek tanpa daftar field yang diizinkan; bukti harus menunjukkan field sensitif benar-benar tersimpan, bukan hanya diterima di respons.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah pengujian API dan otorisasi in-scope pada target ini? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Inventarisasi field sensitif per endpoint

- Dari dokumentasi API dan respons normal, daftar field sensitif yang seharusnya tidak bisa diisi pengguna (peran, harga, saldo, status verifikasi).
- Catat endpoint + field sensitif + nilai normalnya.

**Standar lulus:** Daftar field sensitif tercatat per endpoint.

### Gerbang 2 — Uji satu field tambahan per permintaan

- Dengan akun peran rendah milik sendiri, kirim permintaan normal ditambah SATU field sensitif (nilai canary) dan periksa apakah server menerimanya.
- Ulangi per field; jangan mengirim banyak field sekaligus.

**Standar lulus:** Hasil tiap field tercatat (diterima/ditolak + respons).

### Gerbang 3 — Buktikan perubahan state pada akun sendiri

- Bila field diterima, buktikan state akun sendiri benar-benar berubah ke nilai canary (mis. peran berubah, harga berubah pada data sendiri) — bukan sekadar status 200.
- Kembalikan nilai canary ke semula setelah bukti didapat.

**Standar lulus:** Perubahan state pada akun sendiri tercatat; tanpa itu = belum terbukti.

### Gerbang 4 — Serahkan ke triase

- Tulis field + endpoint + dampak (apa yang bisa diubah penyerang) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Field + dampak tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater | Kirim satu field tambahan per uji; bandingkan respons. |
| Akun tes sendiri (dua peran bila tersedia) | Akun peran rendah milik sendiri untuk menguji kenaikan peran. |
| Dokumentasi API target (OpenAPI/Swagger) bila tersedia | Daftar field yang didokumentasikan vs field yang diterima server. |
| `~/workspace/catatan/log-bug-bounty.md` | Log field yang diuji, respons, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [mass-assignment-api — No. 62]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Field yang ditolak server atau yang diterima tetapi tidak disimpan bukan temuan. Jangan menguji mass assignment pada data pengguna lain atau pada field yang mengubah dana nyata.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
