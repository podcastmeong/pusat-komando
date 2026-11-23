# Skill: Penguasaan Burp Suite Community — Penguasaan Burp Suite Community (gratis): proxy, Repeater, Intruder, Scanner, dan ekstensi — fondasi wajib pemula.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 26 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis penguasaan Burp Suite Community (gratis): proxy, Repeater, Intruder, Scanner, dan ekstensi — fondasi wajib pemula. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya target in-scope; edisi Community tanpa scan otomatis penuh.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `owasp-zap-pengujian-web` (No. 25) — alternatif gratis bila Burp tidak tersedia
- `mcp-burp-repeater`, `mcp-burp-*` — integrasi Burp lewat MCP (bukan pengganti penguasaan manual)
- `fondasi-kerentanan-web-api` — konsep kerentanan yang diuji lewat Burp
- `triase-duplikat` + `laporan-abstrak` — validasi dan pelaporan temuan
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
11. **Scope guard kandidat ini (WAJIB):** Hanya target in-scope; edisi Community tanpa scan otomatis penuh.
12. **Catatan khusus kandidat:** Edisi Community tidak punya Scanner otomatis penuh seperti Professional — kekurangan itu diatasi dengan pengujian manual di Repeater, bukan dengan mengklaim hasil scan otomatis yang tidak ada.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

- Baca pasal scope program dan aturan otomasi (huntr "Humans only" = semua pengujian Burp manual: Repeater dan Intruder manual, tanpa skrip agen AI).
- Pastikan target proxy hanya host in-scope: atur scope Burp dan aktifkan intercept hanya untuk target itu.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope + aturan otomasi tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan proxy dan peta situs

- Arahkan browser uji lewat proxy Burp; jelajahi aplikasi dengan akun uji sendiri sampai Site Map terisi endpoint dan parameter in-scope.
- Tandai scope di Target; gunakan filter agar riwayat hanya menampilkan target in-scope.
- Periksa riwayat permintaan: catat parameter menarik (ID, token, harga, peran) sebagai daftar hipotesis.

**Standar lulus:** Site Map berisi hanya target in-scope; daftar parameter hipotesis tercatat.

### Gerbang 2 — Uji manual dengan Repeater

- Pilih satu parameter; ubah satu dimensi per putaran di Repeater (nilai → respons), catat tiap perubahan.
- Gunakan Decoder/Comparer untuk membandingkan respons (panjang, status, isi) dan menemukan perbedaan yang konsisten.
- Jangan menebak banyak parameter sekaligus — satu dimensi per putaran agar penyebab perbedaan jelas.

**Standar lulus:** Perbedaan respons yang konsisten teramati dan tercatat per parameter.

### Gerbang 3 — Intruder terkendali (bila diizinkan)

- Intruder hanya bila program mengizinkan otomasi; pakai payload list kecil, jeda antar-permintaan, dan hentikan bila rate-limit/error muncul.
- Jangan memakai Intruder untuk brute-force kredensial akun orang lain — hanya enumerasi parameter/identifikasi pada akun uji sendiri.
- Catat posisi payload, daftar yang dipakai, dan hasil tiap putaran.

**Standar lulus:** Hasil Intruder tercatat; tidak ada brute-force terhadap akun orang lain; scan berhenti saat rate-limit muncul.

### Gerbang 4 — Konfirmasi + buktikan dampak read-only

- Konfirmasikan temuan kandidat dengan permintaan manual ulang (minimal 2x) memakai akun uji sendiri dan data canary palsu.
- Buktikan dampak seminimal mungkin, kembalikan state ke semula, lalu serahkan ke A60 audit → triase → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Ada bukti reproduksi langkah-demi-langkah + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Burp Suite Community (gratis) | Proxy, Repeater, Intruder, Decoder, Comparer; Scanner otomatis terbatas di edisi Community — jangan klaim kemampuan Pro. |
| Browser uji + sertifikat CA Burp | Pasang CA Burp hanya di browser/profil uji milik sendiri, bukan di browser utama; hapus setelah sesi selesai. |
| Ekstensi Burp (BApp Store, gratis) | Hanya ekstensi dari sumber resmi; catat ekstensi yang dipakai di log. |
| `~/workspace/catatan/log-bug-bounty.md` | Log setiap pengujian, payload, dan keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [penguasaan-burp-suite-community — No. 26]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Burp Community membatasi kecepatan Intruder dan tidak menyediakan scan aktif penuh. Sertifikat CA Burp hanya dipasang di profil browser uji; jangan memasangnya di perangkat atau browser orang lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
