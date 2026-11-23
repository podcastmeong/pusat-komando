# Skill: Sandbox Mobile, Root & Jailbreak — Sandbox mobile: cara sistem mengisolasi data tiap aplikasi, dan cara menembus batasan lewat Rooting (Android) / Jailbreak (iOS).

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 43 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis sandbox mobile: cara sistem mengisolasi data tiap aplikasi, dan cara menembus batasan lewat Rooting (Android) / Jailbreak (iOS). Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya perangkat/emulator sendiri; tanpa perangkat korban.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Menjalankan pengujian di lab/perangkat/browser milik sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `pengujian-ios-jailbreak-lab` (No. 51) — pengujian iOS di lab jailbreak
- `bypass-deteksi-root-magisk` — bypass deteksi root (pendalaman)
- `adb-android-debug-bridge` (No. 44) — interaksi perangkat setelah root
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
11. **Scope guard kandidat ini (WAJIB):** Hanya perangkat/emulator sendiri; tanpa perangkat korban.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya perangkat/emulator sendiri; tanpa perangkat korban. Root/jailbreak adalah pengubah sistem — cadangkan dulu, dan pahami bahwa perangkat yang di-root lebih rentan.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Root/jailbreak HANYA pada perangkat/emulator milik sendiri. Jangan pernah me-root atau men-jailbreak perangkat orang lain.
- Catat perangkat + metode yang akan dipakai di log sebelum memulai.

**Standar lulus:** Perangkat sendiri + metode tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Pahami sandbox sebelum menembusnya

- Pelajari isolasi bawaan: tiap aplikasi punya UID/direktori sendiri di Android; sandbox iOS membatasi akses file antar-aplikasi.
- Catat data apa yang terlindungi sandbox dan mengapa menembusnya relevan untuk pengujian.

**Standar lulus:** Model sandbox tercatat + alasan pengujian.

### Gerbang 2 — Cadangkan, lalu root/jailbreak perangkat sendiri

- Buat cadangan penuh perangkat sendiri; jalankan prosedur root/jailbreak yang didokumentasikan untuk perangkat itu; verifikasi hak akses baru hanya di perangkat sendiri.
- Bila prosedur gagal atau perangkat menunjukkan tanda tidak stabil, BERHENTI dan pulihkan dari cadangan.

**Standar lulus:** Cadangan dibuat; root/jailbreak berhasil atau kegagalan + pemulihan tercatat.

### Gerbang 3 — Uji batas sandbox yang sudah ditembus

- Dengan hak baru, periksa data aplikasi sendiri (lihat No. 47) dan komponen yang sebelumnya tidak terjangkau — hanya aplikasi sendiri / target in-scope.
- Jangan mengakses data aplikasi milik orang lain di perangkat itu.

**Standar lulus:** Hasil pemeriksaan sandbox tercatat; hanya aplikasi sendiri yang diperiksa.

### Gerbang 4 — Pulihkan dan dokumentasikan

- Pulihkan perangkat ke keadaan semula bila pengujian selesai; tulis metode + hasil + risiko (mis. perangkat yang di-root tidak lagi aman untuk mobile banking) di log.

**Standar lulus:** Perangkat dipulihkan (atau status akhirnya tercatat) + dokumentasi lengkap.

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat/emulator Android/iOS milik sendiri | Satu-satunya perangkat yang di-root/di-jailbreak. |
| Alat root/jailbreak resmi untuk perangkat sendiri | Hanya alat yang didokumentasikan untuk model perangkat sendiri; tanpa alat dari sumber tidak tepercaya. |
| Cadangan (backup) perangkat sendiri | Buat cadangan sebelum mengubah sistem perangkat. |
| `~/workspace/catatan/log-bug-bounty.md` | Log perangkat, metode, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [sandbox-mobile-root-jailbreak — No. 43]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Root/jailbreak bisa membatalkan garansi dan membuat perangkat tidak bisa memakai aplikasi tertentu (mis. mobile banking menolak perangkat root). Jangan memakai perangkat yang di-root untuk aktivitas keuangan pribadi.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
