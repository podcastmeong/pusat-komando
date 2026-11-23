# Skill: SSRF Bypass — Parser & Filter — Bypass filter SSRF lewat perbedaan parser URL (encoding, redirect, skema) untuk mencapai alamat internal yang diblokir.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 63 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis bypass filter SSRF lewat perbedaan parser URL (encoding, redirect, skema) untuk mencapai alamat internal yang diblokir. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya target in-scope; tanpa mengakses layanan internal korban.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `ssrf-oast` — SSRF dasar dengan out-of-band interaction
- `ssrf-metadata-cloud` (No. 30) — SSRF ke metadata cloud (tujuan yang sering dituju bypass ini)
- `analisis-batas-kepercayaan` — perbedaan parser sebagai titik kepercayaan
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
11. **Scope guard kandidat ini (WAJIB):** Hanya target in-scope; tanpa mengakses layanan internal korban.
12. **Catatan khusus kandidat:** Filter SSRF dan parser URL sering tidak sepakat tentang apa arti sebuah URL; bukti bypass harus menunjukkan varian yang lolos filter DAN mencapai alamat internal, bukan hanya varian yang tidak diblokir.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah SSRF in-scope pada target ini? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan filter SSRF target

- Uji filter dengan URL jinak: alamat apa yang diblokir (pesan error apa), skema apa yang diizinkan, dan apakah redirect diikuti?
- Catat aturan filter yang teramati.

**Standar lulus:** Aturan filter tercatat.

### Gerbang 2 — Buktikan SSRF dasar dulu (OAST)

- Sebelum bypass, buktikan server melakukan permintaan ke URL canary milik sendiri (lihat No. 30 Gerbang 2). Bila SSRF dasar tidak ada, bypass tidak ada artinya.
- Catat bukti OAST.

**Standar lulus:** Bukti SSRF dasar tercatat. Tanpa itu = jangan lanjut ke bypass.

### Gerbang 3 — Uji varian bypass satu per satu

- Uji SATU varian per putaran (encoding berbeda, redirect lewat URL canary sendiri, skema alternatif, representasi alamat yang berbeda) menuju alamat internal canary lab sendiri — bukan layanan internal korban.
- Catat varian mana yang lolos filter dan mana yang tetap diblokir.

**Standar lulus:** Hasil tiap varian tercatat (lolos/diblokir + respons).

### Gerbang 4 — Buktikan jangkauan internal + serahkan ke triase

- Bila satu varian lolos, buktikan responsnya menunjukkan jangkauan internal (perbedaan status/panjang/waktu vs alamat yang tidak ada) tanpa memakai kredensial apa pun yang terbaca.
- Tulis varian + bukti dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Varian + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater | Kirim satu varian URL per uji; amati respons server. |
| Server canary milik sendiri (OAST/collaborator) | Menerima interaksi out-of-band untuk membuktikan server melakukan permintaan. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai. |
| `~/workspace/catatan/log-bug-bounty.md` | Log varian URL, respons, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [ssrf-bypass-parser-filter — No. 63]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jangan memakai varian bypass untuk mengakses layanan internal korban atau memakai kredensial yang terbaca. Varian yang lolos filter tetapi tidak mencapai alamat internal bukan temuan.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
