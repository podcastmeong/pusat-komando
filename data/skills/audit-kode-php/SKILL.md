# Skill: Audit Kode PHP — Audit kode PHP: pola rawan (include, eval, unserialize, query mentah) dan cara membaca alur backend PHP.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 41 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis audit kode PHP: pola rawan (include, eval, unserialize, query mentah) dan cara membaca alur backend PHP. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya kode target in-scope / kode sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `kopilot-analisis-kode` — rumusan hipotesis dari kode secara umum
- `analisis-statis-js` — analisis statis untuk JavaScript (padanan bahasa lain)
- `injeksi-sql-kontekstual` — SQLi yang sering ditemukan lewat audit PHP
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
11. **Scope guard kandidat ini (WAJIB):** Hanya kode target in-scope / kode sendiri.
12. **Catatan khusus kandidat:** Audit kode menemukan kerentanan dari alur input, bukan dari keberadaan fungsi rawan semata: include/eval/unserialize hanya celah bila input pengguna yang tidak disanitasi benar-benar mencapainya.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan kode yang diaudit adalah kode target in-scope atau kode sendiri; audit kode di luar scope dilarang.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Batas kode yang diaudit tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Inventarisasi titik masuk input

- Daftar semua titik masuk input pengguna (parameter GET/POST, cookie, header, unggahan file) dan ke mana tiap input mengalir.
- Catat alur input → fungsi → output untuk tiap titik masuk.

**Standar lulus:** Daftar titik masuk + alur tercatat.

### Gerbang 2 — Cari pola rawan

- Cari pola rawan: include/require dengan variabel, eval, unserialize pada input pengguna, query SQL mentah (tanpa prepared statement), dan output tanpa escaping.
- Untuk tiap pola, catat file, baris, dan apakah input pengguna benar-benar mencapai pola itu tanpa sanitasi.

**Standar lulus:** Daftar pola rawan tercatat dengan bukti alur input yang mencapai pola itu.

### Gerbang 3 — Rumuskan hipotesis + konfirmasi live (bila in-scope)

- Untuk pola terkuat, rumuskan hipotesis kerentanan (jenis + dampak) lalu konfirmasikan secara live dengan akun uji sendiri dan data canary — tanpa data orang lain dan tanpa perintah destruktif.
- Bila tidak ada akses live ke target, hipotesis tetap dicatat sebagai temuan audit kode (bukan temuan live) dan diserahkan apa adanya.

**Standar lulus:** Hipotesis terkonfirmasi live atau dicatat sebagai temuan audit kode + keputusan triase.

### Gerbang 4 — Serahkan ke triase

- Tulis pola + alur + bukti (kutipan kode secukupnya, tanpa membocorkan kode proprietari di luar laporan) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Laporan audit berisi pola + alur + bukti; keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Kode sumber PHP target in-scope / kode sendiri | Satu-satunya kode yang diaudit; jangan mengaudit kode yang bukan in-scope. |
| Pencarian teks (grep) + pembaca kode | Melacak alur input → fungsi rawan → output. |
| Akun tes sendiri + data canary palsu | Untuk mengonfirmasi hipotesis audit secara live, hanya di target in-scope. |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang ditemukan, hipotesis, dan hasil konfirmasi. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [audit-kode-php — No. 41]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jangan menyalin kode sumber target secara luas ke dalam laporan atau log — kutip secukupnya untuk membuktikan alur. Audit kode tanpa akses live tetap berharga bila alurnya lengkap dan dapat diikuti triase.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
