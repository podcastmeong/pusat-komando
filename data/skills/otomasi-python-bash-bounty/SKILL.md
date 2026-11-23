# Skill: Otomasi Python & Bash untuk Bounty — Menulis alat bantu otomatis dengan Python dan Bash: skrip enumerasi, pengujian berulang, dan modifikasi skrip eksploitasi yang ada.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 34 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis menulis alat bantu otomatis dengan Python dan Bash: skrip enumerasi, pengujian berulang, dan modifikasi skrip eksploitasi yang ada. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Otomasi hanya pada target in-scope; patuhi rate limit program.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `rekonstruksi-iterasi-payload` — variasi payload satu dimensi per putaran
- `terminal-linux-kali` (No. 38) — perintah dasar tempat skrip berjalan
- `powershell-windows-bounty` (No. 39) — otomasi di lingkungan Windows
- `triase-duplikat` — validasi temuan hasil otomasi
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
11. **Scope guard kandidat ini (WAJIB):** Otomasi hanya pada target in-scope; patuhi rate limit program.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: otomasi hanya pada target in-scope; patuhi rate limit program. huntr 'Humans only' = tanpa otomasi — skill ini TIDAK BOLEH dipakai terhadap target huntr.

## Langkah + gerbang

### Gerbang 0 — Cek pasal otomasi tiap program dulu

- Baca pasal scope SETIAP program yang dilayani: huntr "Humans only" = TANPA otomasi sama sekali — jangan jalankan skrip apa pun terhadap target huntr; Gray Swan dilewati total.
- Untuk program yang mengizinkan otomasi, catat batasnya (rate limit, jumlah permintaan, jam pengujian) di log sebelum skrip ditulis.

**Standar lulus:** Pasal otomasi tiap program tercatat. Program yang melarang = skrip tidak dijalankan ke target itu.

### Gerbang 1 — Tulis skrip yang sopan dan terbatas

- Satu skrip = satu tugas kecil (enumerasi endpoint, pengujian satu parameter, pengecekan satu header).
- Wajib ada: jeda antar-permintaan, batas total permintaan, berhenti otomatis bila respons menunjukkan error/rate-limit/kerusakan, dan log tiap permintaan.

**Standar lulus:** Skrip punya jeda + batas + penghentian otomatis; tanpa itu jangan dijalankan.

### Gerbang 2 — Uji skrip di lab / target canary dulu

- Jalankan skrip terhadap lab sendiri atau endpoint canary milik sendiri; periksa laju, log, dan perilaku berhentinya sebelum menyentuh target program.
- Perbaiki skrip sampai perilakunya sopan dan dapat diprediksi.

**Standar lulus:** Skrip lolos uji lab dengan log yang rapi.

### Gerbang 3 — Jalankan terhadap target in-scope, pantau terus

- Jalankan skrip hanya pada target in-scope yang mengizinkan otomasi; pantau log selama berjalan; hentikan segera bila ada tanda beban atau error.
- Simpan semua hasil mentah untuk ditelaah manual — skrip tidak memutuskan temuan.

**Standar lulus:** Hasil mentah tersimpan; tidak ada tanda beban pada target.

### Gerbang 4 — Telaah manual + serahkan temuan

- Telaah tiap hasil mentah secara manual; hanya hasil yang terkonfirmasi manual yang maju ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.
- Jangan mengirim hasil mentah otomasi sebagai laporan.

**Standar lulus:** Temuan terkonfirmasi manual + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Python 3 (pustaka standar + requests bila diizinkan) | Skrip enumerasi dan pengujian berulang; tanpa pustaka yang membanjiri target. |
| Bash + alat baris perintah (curl, jq) | Rantai perintah kecil untuk pengujian berulang dan pengolahan hasil. |
| Pembatas laju (rate limiter) + jeda | Setiap skrip wajib punya jeda antar-permintaan dan batas total permintaan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log skrip yang dijalankan, target, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [otomasi-python-bash-bounty — No. 34]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Skrip yang baik berhenti sendiri saat target melambat — skrip yang terus memaksa saat rate-limit muncul adalah perilaku DoS dan bisa berujung banned. Modifikasi skrip eksploitasi yang ada hanya untuk memahami polanya; jangan menjalankan eksploitasi lengkap tanpa gerbang skill yang relevan.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
