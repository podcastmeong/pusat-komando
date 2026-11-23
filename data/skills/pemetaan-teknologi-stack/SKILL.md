# Skill: Pemetaan Teknologi Stack — Memetakan stack teknologi target dari fingerprint

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 11. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pasif; tanpa pemindaian agresif di luar scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu tahu teknologi apa yang dipakai target in-scope (framework, versi, CDN, library, bahasa backend) dari fingerprint pasif — agar pola uji yang dipilih tepat sasaran. Dipakai setelah pemetaan permukaan awal, sebelum pengujian kerentanan spesifik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis header HTTP → skill `analisis-header-http-keamanan` (No. 10).
- Analisis statis JS → skill `analisis-statis-js`.
- Kerentanan per framework → skill `perburuan-framework-*`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic, Muse). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Pasif saja.** Gunakan header, isi halaman, dan petunjuk yang diumumkan target sendiri; jangan memakai pemindaian agresif atau brute-force fingerprint di luar scope.
12. **Versi yang terdeteksi adalah dugaan sampai terkonfirmasi** — jangan mengklaim 'versi X rentan' hanya dari fingerprint; konfirmasi lewat perilaku atau dokumentasi resmi.

## Langkah + gerbang

### Gerbang 0 — Cek scope + target

1. Tetapkan target in-scope dan baca pasal scope. Catat host/halaman yang akan dipetakan.
2. **Standar lulus:** target tertulis. Tanpa itu = jangan mulai.

### Gerbang 1 — Kumpulkan fingerprint pasif

1. Dari respons normal target in-scope, kumpulkan petunjuk: header Server/X-Powered-By, cookie khas framework, pola URL, nama file statis, meta generator, dan library JavaScript yang dimuat halaman.
2. **Standar lulus:** daftar petunjuk tertulis dengan sumber tiap petunjuk (header/isi halaman). Petunjuk tanpa sumber = jangan dipakai.

### Gerbang 2 — Identifikasi stack

1. Cocokkan petunjuk dengan teknologi yang dikenal: framework web, bahasa backend, CDN, server web, library JS, dan versi bila terlihat. Tulis tingkat keyakinan tiap identifikasi (pasti/kemungkinan/dugaan).
2. **Standar lulus:** tabel stack tertulis dengan tingkat keyakinan. Identifikasi tanpa tingkat keyakinan = belum selesai.

### Gerbang 3 — Pilih pola uji yang tepat

1. Berdasarkan stack yang teridentifikasi, pilih pola uji yang relevan (mis. kerentanan khas framework itu) dan serahkan ke A58 sebagai hipotesis — beserta stack yang mendasarinya.
2. **Standar lulus:** daftar pola uji tertulis + stack pendukungnya. Stack yang tidak menghasilkan pola uji = dicatat "belum ada pola uji yang relevan".

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP (request normal) | Membaca header dan isi halaman |
| Browser milik sendiri | Melihat library dan sumber daya yang dimuat halaman |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Target: [host in-scope]
Stack teridentifikasi: [teknologi + versi + keyakinan]
Pola uji yang dipilih: [pola + alasan]
Scope guard dipatuhi: [ya — Scope guard: pasif; tanpa pemindaian agresif di luar scope.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Fingerprint bisa sengaja disamarkan (header dihapus, versi disembunyikan) — ketiadaan petunjuk bukan bukti ketiadaan teknologi.
- Jangan mengandalkan satu petunjuk saja; gabungkan beberapa petunjuk sebelum menyimpulkan stack.
