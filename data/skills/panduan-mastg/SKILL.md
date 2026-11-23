# Skill: Panduan MASTG — OWASP MASTG (Mobile Application Security Testing Guide) sebagai acuan pengujian mobile dari dasar sampai lanjut.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 50 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **SEMUA (latihan)**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis oWASP MASTG (Mobile Application Security Testing Guide) sebagai acuan pengujian mobile dari dasar sampai lanjut. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Acuan pengujian; tanpa target di luar program.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan pola dan alat uji |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `owasp-mobile-top-10` (No. 48) — kerangka sepuluh kelas yang dirinci MASTG
- `lab-aplikasi-rentan-mobile` (No. 49) — lab yang dipakai bersama panduan ini
- `struktur-apk-aab-ipa` (No. 42), `frida-objection-runtime` (No. 45), `bypass-ssl-pinning` (No. 46), `inspeksi-data-lokal-mobile` (No. 47) — skill uji yang dirujuk MASTG
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
11. **Scope guard kandidat ini (WAJIB):** Acuan pengujian; tanpa target di luar program.
12. **Catatan khusus kandidat:** MASTG adalah panduan, bukan daftar temuan: nilainya ada pada teknik pengujian dan kriteria lulusnya, yang dipakai untuk menguji aplikasi nyata lewat skill-skill uji.

## Langkah + gerbang

### Gerbang 0 — Cek edisi dan scope dulu

- Catat edisi MASTG yang dipakai dan program + aplikasi target di log. MASTG adalah acuan — pengujian tetap tunduk pada pasal scope program.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Edisi MASTG + program + aplikasi tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Pilih kategori MASTG yang relevan

- Pilih kategori pengujian yang relevan untuk aplikasi target (mis. penyimpanan data, kriptografi, autentikasi, komunikasi jaringan, interaksi platform).
- Kategori yang tidak relevan dicatat alasannya.

**Standar lulus:** Daftar kategori terpilih tercatat.

### Gerbang 2 — Ikuti teknik pengujian MASTG per kategori

- Untuk tiap kategori, ikuti teknik pengujian yang ditulis MASTG (alat + langkah + kriteria lulus) memakai skill uji yang sesuai.
- Catat hasil tiap teknik: lulus/gagal + bukti.

**Standar lulus:** Hasil tiap teknik tercatat dengan bukti.

### Gerbang 3 — Kumpulkan temuan per kategori

- Kumpulkan teknik yang gagal (temuan) beserta bukti dari skill ujinya; teknik yang lulus dicatat buktinya.
- Jangan melaporkan kategori sebagai temuan — laporkan teknik spesifik yang gagal.

**Standar lulus:** Daftar temuan per teknik tercatat.

### Gerbang 4 — Serahkan ke triase

- Serahkan tiap temuan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Tiap temuan punya keputusan triase sendiri.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumen OWASP MASTG (edisi terbaru, sumber resmi OWASP) | Acuan utama; catat edisi yang dipakai. |
| Daftar periksa MASTG (MASVS + teknik pengujian) | Lembar kerja pengujian per kategori. |
| Aplikasi sendiri / target in-scope + perangkat/emulator sendiri | Satu-satunya aplikasi dan perangkat yang diuji. |
| `~/workspace/catatan/log-bug-bounty.md` | Log bagian MASTG yang dipakai dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [panduan-mastg — No. 50]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- MASTG diperbarui berkala — edisi yang dipakai harus dicatat agar hasil dapat ditelusuri. Jangan menyalin isi MASTG secara luas ke laporan; rujuk bagian dan edisinya saja.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
