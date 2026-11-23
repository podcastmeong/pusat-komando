# Skill: Raptor — Berpikir Adversarial dalam Rantai Serang (Bukan Sekadar Menjalankan Tool)

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026), bukan pengalaman teruji. Raptor belum pernah diinstal/dijalankan tim; skill ini mengatur CARA BERPIKIR ala Raptor, bukan instalasi buta.

## Pemicu (kapan dipakai)

- Ada temuan tunggal (mis. satu injeksi lolos) yang perlu dikembangkan jadi RANTAI SERANG end-to-end: dari titik masuk → eskalasi → dampak nyata.
- A56 perlu memetakan permukaan serang sebuah target (program in-scope) sebelum memilih varian prompt untuk diuji.
- Ada banyak temuan kecil yang diduga punya akar penyebab yang sama dan perlu analisis silang.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56 Red Team** | Petakan permukaan serang, rangkai rantai serang, tulis bukti tiap tahap |
| Pendukung | **A52 Generator Varian** | Sediakan varian prompt untuk tiap tahap rantai |
| Pemeriksa | **A60 Security Auditor** | Periksa rantai sebelum naik ke draf laporan |
| Pemimpin | **Muse** | Putuskan rantai mana yang dikembangkan, bunuh jalur buntu |

## Sumber

- Repo: **gadievron/raptor** — https://github.com/gadievron/raptor (lisensi MIT; ~3,8k bintang). RAPTOR = Recursive Autonomous Penetration Testing and Observation Robot. Dibuat oleh Gadi Evron, Daniel Cuthbert, Thomas Dullien (Halvar Flake), Michael Bargury, John Cartwright.
- PENTING: Raptor BUKAN 50 file skill — ini konfigurasi/framework Claude Code yang membuat agen berpikir adversarial, plus alur kerja agen otonom (`/agentic`): pindai (Semgrep, CodeQL) → dedup temuan → validasi tiap temuan lewat tahap eksploitasi → buat PoC untuk yang terkonfirmasi → tulis patch → analisis silang antar-temuan.
- Prinsip yang kita adopsi: **berpikir dalam rantai serang, bukan temuan terisolasi.** Tool menemukan SQLi lalu berhenti; Raptor memetakan permukaan serang, menelusuri aliran data, memvalidasi apakah temuan bisa dieksploitasi, lalu mencari akar penyebab bersama.
- Instal (bila diputuskan): `git clone https://github.com/gadievron/raptor.git`, `pip install -r requirements.txt`, `pip install semgrep`, Claude Code wajib. Proyek masih berstatus eksperimental/beta menurut pembuatnya.
- Peran model terpisah di Raptor: peran `analysis` (menyelidiki temuan) vs peran `code` (menulis exploit/patch) — kita tiru pembagian ini: A56 analisis, A62 exploit/PoC, jangan dicampur dalam satu kepala.

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — rantai yang dirangkai AI bukan rantai sampai manusia memverifikasi tiap tahap.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**
11. **Otonomi Raptor TIDAK berarti otonomi tanpa pengawasan.** Alur `/agentic` yang otonom TIDAK dijalankan otomatis di program bounty — tiap tahap rantai dijalankan manual dengan persetujuan Muse, karena program bounty melarang otomasi tertentu. Raptor dipakai sebagai CARA BERPIKIR, bukan sebagai mesin yang dibiarkan jalan sendiri.
12. **PoC hanya untuk temuan terkonfirmasi.** Jangan buat PoC untuk dugaan yang belum terbukti.

## Langkah + gerbang

### Gerbang 0 — Cek scope (standar lulus: program + target in-scope tertulis di log)

1. Tulis program + target di `~/workspace/catatan/log-bug-bounty.md`.

### Gerbang 1 — Petakan permukaan serang (standar lulus: daftar titik masuk + aliran data tertulis, bukan sekadar "coba prompt X")

1. Untuk target (agen/model/program): daftarkan semua titik masuk yang bisa dimasuki instruksi dari luar (email, kalender, dokumen, tool-output, undangan, file yang dibaca agen).
2. Telusuri aliran data: dari titik masuk, ke mana instruksi itu mengalir? Alat apa yang bisa dipanggil agen sesudahnya? Data apa yang bisa keluar?
3. Hasilnya: peta permukaan serang tertulis — ini dasar memilih varian, bukan tebakan.

### Gerbang 2 — Rangkai rantai serang (standar lulus: rantai punya minimal 2 tahap yang saling terkait + dampak akhir yang konkret)

1. Ambil satu temuan lolos → tanyakan: "sesudah ini lolos, apa yang bisa dilakukan agen selanjutnya?" (mis. baca email → panggil tool → kirim data ke luar).
2. Tiap tahap rantai harus punya bukti sendiri; tahap tanpa bukti = rantai putus di situ, jangan diklaim lanjut.
3. Bedakan peran: A56 merangkai + menganalisis; A62 yang membuat PoC (bila perlu dan diizinkan program).

### Gerbang 3 — Validasi tiap tahap (standar lulus: tiap tahap diuji ulang secara terpisah dan hasilnya dicatat; tahap yang gagal dicoret, bukan ditambal dengan klaim)

1. Uji tiap tahap satu per satu di akun sendiri.
2. Dedup: bila dua temuan ternyata satu akar penyebab, gabungkan jadi satu — jangan laporkan dua kali (lihat skill `triase-duplikat`).

### Gerbang 4 — Analisis silang + draf laporan (standar lulus: akar penyebab bersama ditulis; draf ikut format `laporan-abstrak`)

1. Cari akar penyebab bersama dari semua temuan di target yang sama.
2. Serahkan ke A60 untuk diperiksa; hanya rantai terverifikasi yang masuk draf laporan.
3. Jangan kirim sebelum Cipta setuju.

## Alat

| Alat | Repo / cara pakai |
|---|---|
| Raptor (framework berpikir adversarial) | https://github.com/gadievron/raptor — `git clone https://github.com/gadievron/raptor.git`; dipakai sebagai metodologi, BUKAN dijalankan otomatis |
| Semgrep | `pip install semgrep` — pindai pola di kode (program web klasik saja) |
| CodeQL | Opsional, dianjurkan repo Raptor |
| Skill transfer-hunting | Rantai yang lolos di 1 program diuji ke semua program (adaptasi minimal) |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per rantai: tanggal | program | peta permukaan serang (ringkas) | tahap rantai + bukti per tahap | akar penyebab | status (kandidat / terverifikasi A60).
- Peta permukaan serang + rantai ditulis sebagai bagian draf laporan (format skill `laporan-abstrak`); jangan kirim sebelum Cipta setuju.

## Batasan yang diketahui (BELUM DIUJI)

- Raptor belum pernah diinstal/dijalankan tim; proyek berstatus eksperimental/beta menurut pembuatnya dan tidak membuktikan sendiri bahwa patch/PoC-nya benar.
- Raptor dirancang untuk audit kode/aplikasi, bukan khusus bounty agen AI — pemetaan ke program kita (Muse, OpenAI, 0din, Google AI VRP, ViKernel) adalah adaptasi yang belum teruji.
- Alur otonom penuh Raptor TIDAK boleh dipakai di program bounty yang melarang otomasi — skill ini sengaja membatasi Raptor menjadi cara berpikir manual.
