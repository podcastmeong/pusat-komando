# Skill: Pengujian iOS — Jailbreak Lab — Pengujian aplikasi iOS: struktur IPA, sandbox iOS, Keychain, dan jailbreak di lab untuk menguji keamanan aplikasi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 51 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis pengujian aplikasi iOS: struktur IPA, sandbox iOS, Keychain, dan jailbreak di lab untuk menguji keamanan aplikasi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya perangkat/aplikasi sendiri; lab sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `sandbox-mobile-root-jailbreak` (No. 43) — sandbox dan jailbreak secara umum
- `struktur-apk-aab-ipa` (No. 42) — struktur IPA
- `owasp-mobile-top-10` (No. 48) — kerangka uji mobile
- `panduan-mastg` (No. 50) — panduan pengujian mobile
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
11. **Scope guard kandidat ini (WAJIB):** Hanya perangkat/aplikasi sendiri; lab sendiri.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya perangkat/aplikasi sendiri; lab sendiri. Jailbreak iOS menembus sandbox — cadangkan dulu dan jangan sentuh data aplikasi lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Jailbreak dan pengujian iOS HANYA pada perangkat/aplikasi milik sendiri atau target in-scope. Catat perangkat + aplikasi di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Perangkat + aplikasi tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan struktur IPA aplikasi uji

- Uraikan IPA aplikasi sendiri / target in-scope: Info.plist, executable, framework, dan aset; catat izin dan skema URL yang didaftarkan.

**Standar lulus:** Peta IPA tercatat.

### Gerbang 2 — Cadangkan, lalu jailbreak perangkat sendiri

- Buat cadangan penuh; jalankan jailbreak yang didokumentasikan untuk model/iOS perangkat sendiri; verifikasi akses sistem file.
- Bila jailbreak gagal atau perangkat tidak stabil, BERHENTI dan pulihkan dari cadangan.

**Standar lulus:** Cadangan dibuat; jailbreak berhasil atau kegagalan + pemulihan tercatat.

### Gerbang 3 — Periksa sandbox dan Keychain aplikasi sendiri

- Periksa direktori data aplikasi sendiri dan entri Keychain milik aplikasi sendiri: apakah token/kata sandi tersimpan tanpa perlindungan memadai?
- Jangan membuka data aplikasi lain di perangkat itu; jangan menyalin nilai token utuh.

**Standar lulus:** Temuan penyimpanan tercatat (jenis + lokasi, tanpa nilai utuh).

### Gerbang 4 — Serahkan ke triase / dokumentasikan

- Bila aplikasi target in-scope, serahkan temuan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Bila latihan, simpan sebagai catatan lab; pulihkan perangkat ke keadaan semula.

**Standar lulus:** Keputusan (laporan atau catatan lab) tercatat; perangkat dipulihkan.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat iOS milik sendiri (di-jailbreak di lab) atau simulator | Satu-satunya perangkat iOS yang diuji. |
| Alat jailbreak resmi untuk model/iOS perangkat sendiri | Hanya alat yang didokumentasikan untuk perangkat itu. |
| Cadangan (backup) perangkat sendiri | Buat cadangan sebelum jailbreak. |
| `~/workspace/catatan/log-bug-bounty.md` | Log perangkat, metode, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-ios-jailbreak-lab — No. 51]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jailbreak bisa membuat perangkat tidak bisa memakai aplikasi tertentu dan membatalkan garansi. Versi iOS dan model perangkat menentukan alat jailbreak yang tersedia — jangan memaksakan alat yang tidak cocok.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
