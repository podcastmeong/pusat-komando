# Skill: Second-Order SQLi — Second-order SQLi: payload tersimpan dulu, dieksekusi belakangan di konteks lain — lolos saat injeksi langsung terblokir.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 27 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis second-order SQLi: payload tersimpan dulu, dieksekusi belakangan di konteks lain — lolos saat injeksi langsung terblokir. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa merusak data.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `injeksi-sql-kontekstual` — injeksi SQL langsung (first-order) per dialek; skill ini menambah varian tersimpan
- `fondasi-kerentanan-web-api` — konsep SQLi umum
- `rekonstruksi-iterasi-payload` — variasi payload satu dimensi per putaran
- `triase-duplikat` + `skeptic-false-positive-eliminator` — validasi temuan
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa merusak data.
12. **Catatan khusus kandidat:** Second-order berbeda dari first-order karena payload tidak dieksekusi di permintaan yang sama: bukti harus menunjukkan rantai simpan → pakai, bukan hanya bahwa payload tersimpan.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

- Baca pasal scope: apakah pengujian injeksi diizinkan pada target ini? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
- Catat pasal scope + aturan otomasi di log sebelum satu payload pun dikirim.

**Standar lulus:** Pasal scope + aturan otomasi tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan alur simpan-lalu-pakai

- Inventarisasi field yang menyimpan input pengguna (nama tampilan, profil, komentar, alamat) dan tempat nilai itu dipakai lagi (halaman profil, laporan, pencarian, ekspor).
- Catat pasangan simpan → pakai: field mana disimpan di mana, lalu dibaca di endpoint apa. Tanpa pasangan ini, second-order tidak bisa diuji.

**Standar lulus:** Minimal satu pasangan simpan → pakai tercatat dengan endpoint dan parameternya.

### Gerbang 2 — Simpan penanda jinak, amati eksekusi

- Simpan penanda jinak yang tidak berbahaya (mis. nilai canary unik) lewat field simpan, lalu buka konteks pemakaian dan periksa apakah penanda itu muncul/diproses di sana.
- Bila penanda tidak muncul di konteks pemakaian, alur itu bukan second-order — tutup dan pindah ke pasangan berikutnya.

**Standar lulus:** Penanda canary terlacak dari penyimpanan sampai pemakaian, atau pasangan dinyatakan bukan alur second-order.

### Gerbang 3 — Uji injeksi read-only di konteks pemakaian

- Di konteks pemakaian, uji perbedaan perilaku dengan kondisi benar/salah (boolean-blind) atau tunda kecil (time-based) memakai data canary sendiri — tanpa DROP/DELETE/UPDATE/INSERT.
- Konfirmasi perbedaan yang teramati terulang minimal 2x dengan nilai berbeda.

**Standar lulus:** Perbedaan TRUE/FALSE atau waktu respons yang mengikuti nilai tunda teramati 2x. Tanpa pengulangan = belum terbukti.

### Gerbang 4 — Buktikan dampak read-only, serahkan ke triase

- Bukti maksimal: versi/nama DB saat ini atau satu nilai read-only yang membuktikan kendali atas query di konteks pemakaian. BERHENTI di situ — jangan mengekstrak tabel, kolom, atau baris lain.
- Serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Ada bukti reproduksi (payload tersimpan persis + langkah pemicu + respons) + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater | Kirim payload tersimpan lalu picu eksekusinya di konteks lain; satu payload per uji. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai; nilai canary unik agar jejaknya terlacak. |
| Pengukur waktu respons / stopwatch | Untuk varian time-based second-order: catat waktu respons tiap uji + baseline. |
| `~/workspace/catatan/log-bug-bounty.md` | Log nilai yang disimpan, tempat eksekusi, dan hasil tiap uji. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [sqli-second-order — No. 27]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- WAF yang memblokir injeksi langsung sering tidak memeriksa nilai yang sudah tersimpan — itu sebabnya second-order lolos. Sebaliknya, banyak 'temuan' second-order ternyata hanya nilai yang ditampilkan kembali tanpa dieksekusi sebagai SQL; bukti eksekusi (boolean/time-based) wajib ada.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
