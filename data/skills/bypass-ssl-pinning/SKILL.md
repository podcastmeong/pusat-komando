# Skill: Bypass SSL Pinning — Bypass SSL pinning: melewati validasi sertifikat aplikasi (skrip Frida atau modifikasi network_security_config.xml) agar proksi bisa menyadap.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 46 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis bypass SSL pinning: melewati validasi sertifikat aplikasi (skrip Frida atau modifikasi network_security_config.xml) agar proksi bisa menyadap. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya aplikasi sendiri / target in-scope; tanpa menyadap pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `frida-objection-runtime` (No. 45) — skrip Frida untuk bypass pinning
- `penguasaan-burp-suite-community` (No. 26) / `owasp-zap-pengujian-web` (No. 25) — proksi yang menerima lalu lintas setelah pinning dilewati
- `owasp-mobile-top-10` (No. 48) — kerangka uji mobile
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
11. **Scope guard kandidat ini (WAJIB):** Hanya aplikasi sendiri / target in-scope; tanpa menyadap pengguna lain.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya aplikasi sendiri / target in-scope; tanpa menyadap pengguna lain. Bypass pinning adalah kunci untuk menguji, bukan tujuan — tujuannya adalah apa yang terlihat di lalu lintas setelah kunci itu dibuka.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Pastikan aplikasi yang diuji adalah aplikasi sendiri atau target in-scope, dan perangkatnya milik sendiri. Catat di log.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Aplikasi + perangkat tercatat + dasar scope-nya. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan validasi sertifikat aplikasi

- Periksa apakah aplikasi memakai pinning (sertifikat disematkan, network_security_config, atau pustaka pinning) dan metode pinning apa yang dipakai.
- Catat metode pinning + titik validasinya.

**Standar lulus:** Metode pinning tercatat.

### Gerbang 2 — Lewati pinning pada aplikasi sendiri

- Terapkan SATU metode bypass per uji (skrip Frida yang mengubah hasil validasi, atau konfigurasi jaringan aplikasi sendiri yang mengizinkan CA pengguna) pada aplikasi sendiri.
- Verifikasi proksi menerima lalu lintas aplikasi sendiri.

**Standar lulus:** Bypass berhasil (proksi menerima lalu lintas sendiri) atau metode dinyatakan gagal dan dicatat.

### Gerbang 3 — Amati lalu lintas sendiri, cari kebocoran

- Periksa lalu lintas aplikasi sendiri: token/kata sandi plaintext, data sensitif tanpa enkripsi, atau endpoint yang tidak memakai TLS.
- Jangan menyadap lalu lintas pengguna lain; jangan menyimpan kredensial yang terlihat di luar bukti.

**Standar lulus:** Temuan lalu lintas tercatat; tidak ada data pengguna lain yang disadap.

### Gerbang 4 — Serahkan ke triase

- Tulis metode bypass + temuan lalu lintas (bila ada) dan serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Metode + temuan tercatat + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator milik sendiri | Satu-satunya perangkat tempat bypass dilakukan. |
| Frida / Objection atau berkas konfigurasi aplikasi sendiri | Skrip bypass pinning, atau modifikasi network_security_config.xml pada aplikasi sendiri. |
| Proksi (Burp/ZAP) + sertifikat CA di perangkat sendiri | Menerima lalu lintas aplikasi sendiri setelah pinning dilewati. |
| `~/workspace/catatan/log-bug-bounty.md` | Log metode bypass, lalu lintas yang diamati, dan temuan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [bypass-ssl-pinning — No. 46]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Sebagian aplikasi memakai pinning ganda (sertifikat + validasi tambahan) sehingga satu skrip bypass tidak cukup — catat metode yang gagal sebagai informasi, bukan kegagalan. Jangan memasang CA proksi di perangkat orang lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
