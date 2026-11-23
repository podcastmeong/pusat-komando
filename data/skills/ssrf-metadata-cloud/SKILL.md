# Skill: SSRF ke Metadata Cloud — SSRF ke endpoint metadata cloud (169.254.169.254): membaca kredensial sementara dan konfigurasi internal dari server.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 30 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis sSRF ke endpoint metadata cloud (169.254.169.254): membaca kredensial sementara dan konfigurasi internal dari server. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya target in-scope; tanpa memakai kredensial yang terbaca di luar PoC.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `ssrf-oast` — SSRF dasar dengan out-of-band interaction
- `ssrf-bypass-parser-filter` (No. 63) — bypass filter SSRF lewat perbedaan parser
- `analisis-batas-kepercayaan` — memetakan titik yang dipercaya server tanpa verifikasi
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
11. **Scope guard kandidat ini (WAJIB):** Hanya target in-scope; tanpa memakai kredensial yang terbaca di luar PoC.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: tanpa memakai kredensial yang terbaca di luar PoC. Kredensial sementara yang terbaca adalah bukti keberadaan jangkauan, bukan alat untuk dipakai lanjut.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah SSRF in-scope pada target ini? Apakah metadata cloud termasuk aset yang boleh dibuktikan? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat, termasuk batas pembuktian metadata. Tanpa itu = jangan mulai.

### Gerbang 1 — Temukan parameter pemuat URL

- Inventarisasi parameter yang membuat server mengambil URL (pratinjau tautan, impor dari URL, webhook, pemuat gambar jarak jauh, PDF dari URL).
- Catat parameter + endpoint + format URL yang diterima.

**Standar lulus:** Minimal satu parameter pemuat URL tercatat.

### Gerbang 2 — Buktikan server melakukan permintaan (OAST)

- Arahkan parameter ke URL canary milik sendiri dan periksa apakah server canary menerima interaksi (DNS/HTTP) — ini membuktikan SSRF tanpa menyentuh alamat internal.
- Bila tidak ada interaksi, parameter itu bukan SSRF — tutup dan pindah ke parameter berikutnya.

**Standar lulus:** Interaksi out-of-band dari server target ke canary milik sendiri tercatat, atau parameter dinyatakan bukan SSRF.

### Gerbang 3 — Uji jangkauan internal secara minimal

- Bila Gerbang 2 terbukti, uji satu alamat metadata cloud standar untuk memastikan jangkauan internal — cukup buktikan responsnya berbeda dari respons untuk alamat yang tidak ada (status/panjang/waktu).
- JANGAN memakai kredensial sementara apa pun yang terbaca di luar pembuktian keberadaan; jangan mengunduh, menyimpan, atau memakai kredensial itu untuk mengakses layanan lain; jangan membaca konfigurasi internal lebih jauh.

**Standar lulus:** Perbedaan respons terhadap alamat internal tercatat; tidak ada kredensial yang dipakai atau disimpan.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (endpoint apa, jangkauan apa yang terbukti) tanpa melampirkan kredensial apa pun; serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Dampak ditulis konkret tanpa kredensial + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater | Kirim satu kandidat URL per uji; amati respons server. |
| Server canary milik sendiri (OAST/collaborator) | Menerima interaksi out-of-band untuk membuktikan server melakukan permintaan — tanpa data orang lain. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai. |
| `~/workspace/catatan/log-bug-bounty.md` | Log URL yang diuji, respons, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [ssrf-metadata-cloud — No. 30]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Respons SSRF sering kali hanya menampilkan error generik — perbedaan status/panjang/waktu respons sudah cukup sebagai bukti jangkauan bila konsisten dan terulang. Jangan memaksa membaca isi metadata lengkap bila program tidak memintanya.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
