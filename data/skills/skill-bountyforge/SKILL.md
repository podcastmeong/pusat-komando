# Skill: BountyForge — Audit Paralel Smart Contract + Web/API

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026), bukan pengalaman teruji. Repo BountyForge belum pernah di-clone/dijalankan tim; URL repo di bawah ini diambil dari catatan referensi dan BELUM diverifikasi langsung (pencarian web tidak menemukan konfirmasi repo Gabson0x/bountyforge). Verifikasi URL sebelum clone.

## Pemicu (kapan dipakai)

- Ada program bounty in-scope yang mencakup smart contract (EVM, Move, Solana, TRON) atau web/API, dan perlu diaudit dengan banyak agen paralel.
- A62 butuh audit yang luas (banyak agen menyerang target yang sama dari sudut berbeda) untuk satu target kontrak/API.
- Ada target kontrak yang sudah diaudit manual dan perlu putaran kedua dengan agen paralel untuk mencari yang terlewat.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Jalankan agen paralel, kumpulkan temuan, saring duplikat |
| Pemeriksa | **A60 Security Auditor** | Periksa temuan sebelum naik ke draf laporan |
| Pemimpin | **Muse** | Putuskan target + jumlah agen paralel; bunuh putaran yang buntu |

## Sumber

- Repo: **Gabson0x/bountyforge** — https://github.com/Gabson0x/bountyforge (~400 bintang, sangat aktif menurut artikel). ⚠️ URL BELUM TERVERIFIKASI — cek dulu repo itu ada dan isinya sesuai sebelum clone.
- Konsep: agen paralel Claude untuk audit smart contract (EVM, Move, Solana, TRON) + web/API. Mirip arah "serang rame-rame" tim kita (banyak agen menyerang target yang sama bersamaan).
- Prinsip yang kita adopsi: **paralel dengan sudut berbeda, bukan paralel dengan tugas yang sama.** Tiap agen diberi sudut serang berbeda (mis. agen 1: kontrol akses, agen 2: matematika/presisi, agen 3: logika bisnis, agen 4: integrasi eksternal) supaya hasilnya tidak duplikat satu sama lain.

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun — termasuk jangan menjalankan banyak agen paralel yang menghantam layanan live secara bersamaan.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain. Jangan deploy kontrak berisi payload ke mainnet/testnet publik.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — temuan agen paralel bukan temuan sampai manusia memverifikasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**
11. **Audit smart contract HANYA di kode yang diberikan program / repo in-scope, di lingkungan lokal.** Jangan audit kontrak live milik orang lain yang tidak in-scope.
12. **Paralel ≠ otomatis tanpa batas.** Jumlah agen paralel dibatasi Muse per putaran; tiap agen bekerja di salinan lokal, bukan menghantam layanan live bersamaan.

## Langkah + gerbang

### Gerbang 0 — Cek scope + verifikasi repo (standar lulus: program in-scope tertulis; URL repo terverifikasi ada + isinya sesuai)

1. Tulis program + target (kontrak/API) di `~/workspace/catatan/log-bug-bounty.md`.
2. Verifikasi URL repo BountyForge; bila tidak ditemukan/tidak sesuai → BERHENTI, pakai metode manual (skill `skill-trail-of-bits`) dan catat di log bahwa repo tidak terverifikasi.

### Gerbang 1 — Bagi sudut serang (standar lulus: tiap agen paralel punya sudut berbeda yang tertulis; tidak ada dua agen dengan tugas yang sama)

1. Tentukan 2–5 sudut serang sesuai target (contoh kontrak: kontrol akses, matematika/presisi, logika bisnis, integrasi/oracle, DoS gas — catat: DoS gas HANYA dianalisis di kode lokal, TIDAK diuji di jaringan live).
2. Tiap agen menerima: target + sudutnya + aturan keras skill ini.

### Gerbang 2 — Jalankan paralel di lokal (standar lulus: semua agen bekerja di salinan lokal; tidak ada permintaan ke layanan live yang tidak diizinkan program)

1. Jalankan agen paralel pada kode lokal (repo kontrak / spesifikasi API program).
2. Tiap agen mencatat temuannya + bukti (file, baris, alasan).

### Gerbang 3 — Gabung + dedup (standar lulus: daftar temuan gabungan tanpa duplikat; tiap temuan punya bukti + agen penemunya)

1. Gabungkan semua temuan; hapus duplikat (temuan yang sama dari agen berbeda = SATU temuan, catat semua agen penemunya).
2. Saring false positive: uji tiap temuan di kode lokal (apakah benar-benar bisa terjadi?).
3. Lihat skill `triase-duplikat` untuk pemeriksaan duplikat terhadap laporan yang sudah ada.

### Gerbang 4 — Verifikasi A60 + draf laporan (standar lulus: A60 memeriksa tiap temuan; draf ikut format `laporan-abstrak`)

1. Serahkan daftar temuan ke A60; hanya yang disetujui yang masuk draf laporan.
2. Jangan kirim sebelum Cipta setuju.

## Alat

| Alat | Repo / cara pakai |
|---|---|
| BountyForge (agen paralel audit) | https://github.com/Gabson0x/bountyforge — ⚠️ URL BELUM TERVERIFIKASI, cek dulu sebelum clone |
| Slither (analisis statis EVM) | `pip install slither-analyzer` lalu `slither <target>` — di kode lokal |
| Foundry (forge/cast) | `forge test`, `cast call` — uji lokal, bukan jaringan live |
| Skill triase-duplikat | Cek duplikat temuan sebelum draf laporan |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per putaran: tanggal | program | target | sudut serang per agen | temuan gabungan (tanpa duplikat) | status (kandidat / terverifikasi A60).
- Draf laporan: ikut format skill `laporan-abstrak`; jangan kirim sebelum Cipta setuju.
- Bila repo BountyForge tidak terverifikasi, tulis di log: "BountyForge BELUM TERVERIFIKASI — audit dilakukan manual" beserta tanggal pengecekan.

## Batasan yang diketahui (BELUM DIUJI)

- Repo belum terverifikasi keberadaannya; seluruh cara pakai di atas adalah adaptasi dari deskripsi artikel, bukan pengalaman menjalankan tool-nya.
- Audit smart contract hanya relevan bila ada program in-scope yang mencakup kontrak — saat ini program utama kita adalah bounty agen AI; skill ini cadangan untuk program web/contract klasik.
- Agen paralel yang tidak dibatasi bisa menghasilkan banyak duplikat (pelajaran XBOW: ~20% duplikat dari ~1.060 laporan) — Gerbang 3 wajib, bukan opsional.
