# Skill: Pengujian Ekstensi Browser — Keamanan ekstensi browser: izin berlebih, komunikasi dengan halaman web, dan kebocoran data lewat ekstensi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 59 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis keamanan ekstensi browser: izin berlebih, komunikasi dengan halaman web, dan kebocoran data lewat ekstensi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya ekstensi target in-scope / ekstensi sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `analisis-statis-js` — membaca kode JavaScript ekstensi
- `audit-kode-php` (No. 41) — audit kode (pendekatan audit, bahasa berbeda)
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
11. **Scope guard kandidat ini (WAJIB):** Hanya ekstensi target in-scope / ekstensi sendiri.
12. **Catatan khusus kandidat:** Izin ekstensi yang berlebih baru menjadi temuan bila dibuktikan data atau fungsi yang bisa dijangkau pihak yang tidak semestinya — daftar izin saja bukan temuan.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan ekstensi yang diuji adalah ekstensi target in-scope atau ekstensi sendiri. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Ekstensi tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Baca manifest dan izin

- Baca manifest ekstensi: izin yang diminta (tabs, cookies, storage, host mana), skrip konten yang disuntikkan, dan halaman latar yang dipakai.
- Tandai izin yang berlebih dibanding fungsi ekstensi yang dinyatakan.

**Standar lulus:** Daftar izin + penilaian keberlebihannya tercatat.

### Gerbang 2 — Lacak komunikasi ekstensi

- Periksa komunikasi ekstensi: pesan antara halaman web dan ekstensi, permintaan jaringan yang dikirim ekstensi, dan data apa yang dikirim.
- Catat endpoint + data yang dikirim ekstensi.

**Standar lulus:** Daftar komunikasi + data tercatat.

### Gerbang 3 — Uji halaman web canary terhadap ekstensi

- Buka halaman canary milik sendiri di browser uji dan periksa apakah halaman itu dapat memanggil fungsi ekstensi atau membaca data lewat ekstensi (mis. membaca nilai canary dari penyimpanan ekstensi).
- Jangan memakai halaman penyerang sungguhan; halaman canary milik sendiri saja.

**Standar lulus:** Hasil uji halaman canary tercatat.

### Gerbang 4 — Serahkan ke triase

- Tulis izin berlebih + bukti komunikasi/kebocoran dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Temuan + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Ekstensi browser target in-scope / ekstensi sendiri | Satu-satunya ekstensi yang diuji. |
| Browser uji milik sendiri (profil terpisah) | Tempat ekstensi dipasang dan diuji; profil terpisah dari browser utama. |
| Pembaca paket ekstensi (arsip CRX/XPI) | Menguraikan isi ekstensi untuk dibaca manifest dan kodenya. |
| `~/workspace/catatan/log-bug-bounty.md` | Log manifest, izin, dan hasil uji. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-ekstensi-browser — No. 59]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Pasang ekstensi uji hanya di profil browser terpisah milik sendiri; jangan memasang ekstensi yang tidak tepercaya di browser utama. Jangan menguji ekstensi yang dipakai pengguna lain tanpa scope.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
