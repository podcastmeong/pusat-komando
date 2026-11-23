# Skill: Kebocoran Data Respons JSON API — Mencari kebocoran data pada respons JSON API

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 8. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: akun uji sendiri; tanpa membaca data pengguna lain.

## Pemicu (kapan dipakai)

Dipakai saat menguji API target in-scope dengan akun sendiri: memeriksa apakah respons JSON mengandung field berlebih, pesan error verbose, atau data pengguna lain yang ikut terkirim. Dipakai pada endpoint yang sudah dipetakan (lihat No. 9), bukan pada endpoint acak.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Matriks otorisasi endpoint → skill `dokumentasi-api-otorisasi-endpoint` (No. 9).
- Penemuan API/Swagger → skill `penemuan-api-swagger`.
- Mass assignment → skill `mass-assignment-api` (No. 62, keluarga HACKING).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic, Muse, OpenAI Safety). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Akun uji sendiri saja.** Bila respons mengandung data pengguna lain, BERHENTI membaca isinya, catat HANYA bahwa data pihak lain ikut terkirim (jenis field + endpoint), dan laporkan — jangan membuka, menyimpan, atau memakai data itu.
12. **Jangan memancing kebocoran dengan ID/parameter milik orang lain** — uji hanya dengan ID dan data milik akun sendiri.

## Langkah + gerbang

### Gerbang 0 — Cek scope + endpoint yang akan diuji

1. Pilih endpoint dari matriks otorisasi (No. 9) dan baca pasal scope: apakah pengujian API diizinkan pada endpoint ini?
2. **Standar lulus:** endpoint + izin tercatat sebelum satu request pun dikirim.

### Gerbang 1 — Kirim request normal akun sendiri

1. Kirim request normal memakai akun sendiri dan simpan respons JSON lengkap (milik sendiri). Catat semua field yang dikembalikan.
2. **Standar lulus:** respons akun sendiri tersimpan + daftar field tercatat.

### Gerbang 2 — Cari field berlebih dan error verbose

1. Periksa: field sensitif yang tidak dibutuhkan klien (hash kata sandi, token internal, ID internal, flag admin)? Pesan error yang membocorkan struktur internal (nama tabel, query, stack trace)? Bandingkan respons antar-peran akun sendiri bila ada lebih dari satu peran milik sendiri.
2. **Standar lulus:** tiap field mencurigakan tercatat dengan nama field + jenis isinya (bukan nilai utuh bila sensitif). Tidak ada field berlebih = catat "bersih pada endpoint ini".

### Gerbang 3 — Uji apakah data pihak lain ikut terkirim

1. HANYA dengan data milik sendiri sebagai pemicu (mis. membuat dua akun sendiri dan memeriksa apakah respons akun A memuat data akun B milik sendiri) — bila data akun lain (bukan milik sendiri) muncul, BERHENTI dan ikuti aturan keras 11.
2. **Standar lulus:** hasil uji tercatat; bila data pihak lain terlihat, hanya jenis field + endpoint yang dicatat, isinya TIDAK dibaca lebih jauh.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis field apa yang bocor, siapa yang bisa melihatnya, dan langkah reproduksi. Serahkan ke A60 untuk audit.
2. **Standar lulus:** dampak ditulis konkret, draf mengikuti format output, dan status triase diputuskan A60.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP / Burp Repeater | Mengirim request API akun sendiri dan membaca respons JSON |
| Akun tes sendiri (dua akun bila perlu) | Satu-satunya akun yang datanya dipakai |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Endpoint: [METODE path]
Field berlebih: [nama field + jenis isi]
Data pihak lain ikut terkirim: [ya/tidak — hanya jenis field bila ya]
Scope guard dipatuhi: [ya — Scope guard: akun uji sendiri; tanpa membaca data pengguna lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Respons JSON sering memuat field internal yang tidak sensitif (ID internal, timestamp) — bedakan field yang benar-benar sensitif dari yang sekadar berlebih.
- Error verbose bisa berubah-ubah antar-deploy; konfirmasi dengan pengulangan sebelum mengklaim terbukti.
