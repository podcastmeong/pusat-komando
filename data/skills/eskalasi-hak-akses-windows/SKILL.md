# Skill: Eskalasi Hak Akses Windows — Privilege escalation Windows: token impersonation, layanan lemah, AlwaysInstallElevated, dan kerentanan lokal.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 37 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis privilege escalation Windows: token impersonation, layanan lemah, AlwaysInstallElevated, dan kerentanan lokal. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya bila program eksplisit mencantumkan aset infra; lab sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `powershell-windows-bounty` (No. 39) — perintah Windows untuk enumerasi
- `eskalasi-hak-akses-linux` (No. 36) — padanan Linux
- `jalur-belajar-tryhackme` / `lab-hack-the-box` — lab privesc legal
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
11. **Scope guard kandidat ini (WAJIB):** Hanya bila program eksplisit mencantumkan aset infra; lab sendiri.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya bila program eksplisit mencantumkan aset infra; lab sendiri. Selalu bedakan salah konfigurasi dari fitur yang disengaja.

## Langkah + gerbang

### Gerbang 0 — Cek scope eksplisit dulu

- Baca pasal scope: privesc HANYA bila program secara eksplisit mencantumkan aset infrastruktur Windows sebagai in-scope. Tanpa pencantuman eksplisit = hanya lab sendiri.
- Catat pasal scope di log sebelum enumerasi apa pun.

**Standar lulus:** Pasal scope eksplisit tercatat, atau batas lab-saja dicatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Enumerasi sebagai pengguna biasa

- Enumerasi: layanan dengan izin lemah, tugas terjadwal, kunci registry (mis. AlwaysInstallElevated), token yang bisa dipersonifikasi, dan file sensitif yang bisa dibaca — tanpa mengubah apa pun.
- Catat tiap temuan dengan jalur dan izinnya.

**Standar lulus:** Daftar enumerasi tercatat tanpa perubahan apa pun.

### Gerbang 2 — Nilai tiap jalur, pilih yang paling aman

- Nilai tiap jalur: salah konfigurasi atau fitur disengaja? Reversibel? Pilih satu jalur yang paling aman dan paling jelas salah konfigurasinya.

**Standar lulus:** Satu jalur terpilih dengan alasan keamanan + reversibilitasnya.

### Gerbang 3 — Buktikan kenaikan hak di lab / aset in-scope

- Jalankan jalur terpilih di lab sendiri (atau aset in-scope eksplisit) dan buktikan hak naik lewat file canary milik administrator di lab.
- Jangan mengubah kata sandi, menambah pengguna, atau mengubah konfigurasi sistem.

**Standar lulus:** Kenaikan hak terbukti lewat canary; tidak ada perubahan konfigurasi sistem.

### Gerbang 4 — Serahkan ke triase

- Tulis jalur persis (konfigurasi apa yang salah, langkah apa yang membuktikan) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Jalur + bukti tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Mesin lab Windows milik sendiri / VM terisolasi | Tempat utama pengujian privesc; akun pengguna biasa milik sendiri. |
| PowerShell + alat enumerasi Windows di lab | Enumerasi layanan, tugas terjadwal, registry, dan token. |
| Akun uji sendiri | Akun pengguna biasa milik sendiri sebagai titik awal. |
| `~/workspace/catatan/log-bug-bounty.md` | Log jalur yang ditemukan dan hasil uji. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [eskalasi-hak-akses-windows — No. 37]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- AlwaysInstallElevated, layanan lemah, dan token impersonation adalah pola klasik — tetapi di lingkungan yang dikelola dengan benar semuanya sudah dikunci. Jangan menguji privesc pada mesin Windows milik orang lain tanpa scope eksplisit.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
