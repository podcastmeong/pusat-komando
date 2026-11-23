# Skill: HTTP Method Override Bypass — HTTP verb tampering / method override (X-HTTP-Method-Override, _method) untuk melewati kontrol akses berbasis metode.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 33 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis hTTP verb tampering / method override (X-HTTP-Method-Override, _method) untuk melewati kontrol akses berbasis metode. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa mengubah data pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `perburuan-bypass-autentikasi` — bypass autentikasi umum
- `perburuan-manajemen-sesi` — manajemen sesi
- `fondasi-kerentanan-web-api` — dasar HTTP/metode
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
12. **Catatan khusus kandidat:** Kontrol akses yang hanya memeriksa metode HTTP (bukan peran pengguna) rapuh bila framework mendukung override metode; bukti harus menunjukkan aksi yang semestinya ditolak benar-benar terjadi.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope: apakah pengujian kontrol akses in-scope pada target ini? Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan kontrol akses berbasis metode

- Catat endpoint yang perilakunya berbeda per metode (mis. GET boleh dibaca peran rendah, DELETE hanya admin) dan cara server memeriksa metode.
- Catat juga apakah aplikasi memakai parameter _method atau header X-HTTP-Method-Override.

**Standar lulus:** Daftar endpoint + aturan metode tercatat.

### Gerbang 2 — Uji varian override pada akun peran rendah

- Dengan akun peran rendah milik sendiri, kirim permintaan dengan metode override (header dan parameter, satu varian per uji) menuju aksi yang semestinya ditolak.
- Bandingkan respons dengan permintaan normal tanpa override.

**Standar lulus:** Hasil tiap varian tercatat (diterima/ditolak + respons).

### Gerbang 3 — Buktikan aksi yang semestinya ditolak berhasil

- Bila varian override diterima, buktikan aksi itu benar-benar terjadi pada data milik sendiri (nilai canary berubah) — bukan sekadar status 200.
- Kembalikan nilai canary ke semula setelah bukti didapat.

**Standar lulus:** Perubahan state pada data sendiri tercatat; tanpa itu = belum terbukti.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (aksi apa yang lolos, peran apa yang seharusnya ditolak) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Dampak ditulis konkret + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater | Kirim satu varian metode per uji; bandingkan respons. |
| Akun tes sendiri (dua peran bila tersedia) | Akun peran rendah + akun peran tinggi milik sendiri untuk membandingkan kontrol akses. |
| `~/workspace/catatan/log-bug-bounty.md` | Log varian metode, respons, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [http-method-override-bypass — No. 33]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak framework mengabaikan header override bila tidak dikonfigurasi — varian yang diabaikan bukan temuan. Jangan menguji override pada aksi destruktif atau data pengguna lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
