# Skill: OWASP ZAP — Pengujian Web — OWASP ZAP (gratis, open-source): spider, active scan, pemindaian API, dan otomatisasi sebagai alternatif Burp.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 25 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH, MUSE**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis oWASP ZAP (gratis, open-source): spider, active scan, pemindaian API, dan otomatisasi sebagai alternatif Burp. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya target in-scope; tanpa pemindaian destruktif.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `penguasaan-burp-suite-community` (No. 26) — alat proxy alternatif; skill ini ZAP, bukan Burp
- `fuzzing-direktori-file` — enumerasi direktori pelengkap spider ZAP
- `analisis-header-http-keamanan` — membaca header yang ditemukan ZAP
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
11. **Scope guard kandidat ini (WAJIB):** Hanya target in-scope; tanpa pemindaian destruktif.
12. **Catatan khusus kandidat:** ZAP adalah alternatif gratis Burp: konteks dan kebijakan scan-nya yang membedakan pemindaian sah dari pemindaian liar. Jangan pernah menjalankan active scan ZAP terhadap host yang tidak tercantum di scope.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

- Baca pasal scope program: apakah pemindaian aktif diizinkan pada target ini? Apakah otomasi dilarang (huntr "Humans only" = ZAP dipakai manual sebagai proxy, tanpa active scan otomatis)?
- Catat pasal scope + aturan otomasi di log sebelum satu permintaan scan pun dikirim.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety" — bingkai temuan sebagai aksi tanpa izin via grant yang dipakai ulang.

**Standar lulus:** Pasal scope + aturan otomasi tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Siapkan konteks dan scope ZAP

- Buat konteks ZAP berisi hanya host/path in-scope; masukkan semua host di luar scope ke daftar exclude.
- Atur kebijakan active scan: matikan pemindai yang destruktif atau menulis data (mis. pemindai yang mengirim form berbahaya) bila targetnya layanan produksi.
- Jalankan spider pasif dulu (crawl lewat proxy) untuk memetakan permukaan tanpa memicu active scan.

**Standar lulus:** Konteks berisi hanya target in-scope; pemindai destruktif dimatikan; peta spider tercatat.

### Gerbang 2 — Spider + pemindaian pasif

- Jalankan spider (tradisional dan/atau AJAX bila aplikasi SPA) pada target in-scope; catat endpoint, parameter, dan teknologi yang teridentifikasi.
- Biarkan pemindai pasif ZAP menandai masalah (header hilang, cookie tanpa atribut aman, respons yang membocorkan informasi).
- Tandai tiap temuan pasif sebagai hipotesis, bukan vonis — butuh konfirmasi manual.

**Standar lulus:** Daftar endpoint + parameter in-scope tercatat; temuan pasif dikelompokkan per kelas.

### Gerbang 3 — Active scan terkendali (bila diizinkan)

- Jalankan active scan hanya pada endpoint in-scope yang sudah dipetakan, dengan jeda antar-permintaan dan intensitas rendah; hentikan bila respons menunjukkan kesalahan atau perlambatan.
- Untuk tiap alert active scan, ulangi permintaan pemicunya secara manual (Repeater/manual request) dan periksa apakah alert dapat direproduksi.
- Buang alert yang hanya berasal dari pola generik tanpa bukti (mis. alert yang muncul pada setiap halaman).

**Standar lulus:** Setiap alert yang diteruskan punya langkah reproduksi manual yang tercatat; scan berhenti bila target menunjukkan tanda beban.

### Gerbang 4 — Konfirmasi manual + buktikan dampak read-only

- Pilih alert dengan bukti terkuat; konfirmasikan dengan akun uji sendiri dan data canary palsu — tanpa membaca data pengguna lain dan tanpa mengubah data.
- Buktikan dampak seminimal mungkin (mis. nilai canary terbaca/berubah pada akun sendiri) lalu kembalikan ke nilai semula.
- Serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Ada bukti reproduksi langkah-demi-langkah + keputusan triase tercatat. Tanpa bukti = belum berhasil.

## Alat

| Alat | Cara pakai |
|---|---|
| OWASP ZAP (gratis, open-source) | Spider, active scan, pemindaian API, dan otomatisasi — atur konteks, scope, dan kebijakan scan sebelum memindai. |
| Browser / proxy ZAP | Arahkan lalu lintas browser uji lewat proxy ZAP; simpan sesi dan riwayat permintaan. |
| ZAP API / CLI (zap-cli, automation framework) | Jalankan spider dan active scan dari baris perintah; hanya bila program mengizinkan otomasi. |
| `~/workspace/catatan/log-bug-bounty.md` | Log konfigurasi scan, temuan, dan keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [owasp-zap-pengujian-web — No. 25]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- ZAP Community gratis — tidak ada dukungan scan otomatis penuh seperti Burp Professional; active scan bisa menghasilkan false positive pada aplikasi SPA/AJAX bila spider AJAX tidak dipakai. Alert ZAP bukan temuan sampai dikonfirmasi manual.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
