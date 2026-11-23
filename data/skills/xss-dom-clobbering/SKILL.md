# Skill: DOM Clobbering — DOM clobbering: elemen HTML yang menimpa variabel global JavaScript sehingga alur aplikasi berubah dan XSS terjadi.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 28 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis dOM clobbering: elemen HTML yang menimpa variabel global JavaScript sehingga alur aplikasi berubah dan XSS terjadi. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Akun uji sendiri; tanpa menyerang pengguna lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `verifikasi-xss`, `pelacakan-taint-xss-dom` — XSS dasar dan pelacakan taint DOM
- `analisis-statis-js` — membaca kode JavaScript target untuk menemukan variabel global yang bisa ditimpa
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
11. **Scope guard kandidat ini (WAJIB):** Akun uji sendiri; tanpa menyerang pengguna lain.
12. **Catatan khusus kandidat:** DOM clobbering memanfaatkan fakta bahwa elemen HTML dengan atribut id/name tertentu otomatis menjadi properti global window; serangan berhasil bila aplikasi membaca variabel itu tanpa memeriksa tipenya.

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu

- Baca pasal scope program: apakah pengujian XSS diizinkan pada target ini? Catat di log sebelum menguji.
- Perplexity VDP: dalam laporan jangan pakai kata "prompt injection"/"hallucination"/"model safety".

**Standar lulus:** Pasal scope tercatat di log. Tanpa itu = jangan mulai.

### Gerbang 1 — Temukan variabel global yang dipakai aplikasi

- Baca kode JavaScript target (statis) dan cari variabel global yang dibaca tanpa deklarasi aman — mis. variabel yang dipakai untuk URL, konfigurasi, atau alur tampilan.
- Catat nama variabel, file sumber, dan apa yang terjadi bila nilainya berubah.

**Standar lulus:** Minimal satu variabel global kandidat tercatat dengan lokasi kode dan dampak hipotetisnya.

### Gerbang 2 — Uji penimpaan dengan markup jinak

- Sisipkan markup jinak (elemen dengan id/name sama dengan nama variabel) lewat field yang mengizinkan HTML, lalu periksa di DevTools apakah variabel global benar-benar tertimpa.
- Bila variabel tidak tertimpa, catat dan tutup hipotesis itu — jangan memaksa dengan markup lain tanpa hipotesis baru.

**Standar lulus:** Hasil penimpaan tercatat (tertimbang/tidak) dengan bukti dari DevTools.

### Gerbang 3 — Buktikan perubahan alur, bukan sekadar penimpaan

- Tunjukkan bahwa penimpaan mengubah alur aplikasi (mis. URL yang dimuat, konfigurasi yang dipakai) pada sesi akun sendiri — penimpaan tanpa perubahan alur bukan temuan.
- Bila perubahan alur mencapai eksekusi skrip, buktikan dengan skrip canary milik sendiri (mis. mengubah teks halaman akun sendiri), bukan dengan skrip berbahaya.

**Standar lulus:** Perubahan alur teramati pada akun sendiri dan tercatat langkah-demi-langkah.

### Gerbang 4 — Serahkan ke triase

- Tulis dampak konkret (alur apa yang berubah, apa yang bisa dilakukan penyerang atas nama korban yang login) — bukan dugaan umum.
- Serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Dampak ditulis konkret + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Browser milik sendiri + DevTools | Periksa variabel global dan perilaku DOM; hanya di sesi/akun sendiri. |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis variabel, markup pemicu, dan hasil uji. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [xss-dom-clobbering — No. 28]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Banyak variabel global tampak bisa ditimpa tapi aplikasi sudah memeriksa tipenya atau memakai deklarasi yang aman — penimpaan saja tanpa perubahan alur bukan temuan. Jangan menguji markup clobbering pada halaman yang dilihat pengguna lain.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
