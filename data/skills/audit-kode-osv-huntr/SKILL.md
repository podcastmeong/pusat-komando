# Skill: Audit Kode OSV huntr — Code-Audit Only

> BELUM DIUJI — dibangun 24 Nov 2026 dari perintah Cipta ("Ok buat", 24 Nov 06:45, Blok F / T23). Skill ini memandu audit kode sumber terbuka (OSV) saja, bukan pengalaman teruji. HANYA UNTUK BOUNTY (program resmi saja — huntr). LARANGAN DESTRUKTIF: dilarang merusak, menghapus, atau mengubah data apa pun; dilarang menjalankan payload terhadap sistem live milik orang lain; dilarang eksfiltrasi data.

## Ruang lingkup (ketat)

- **Code-audit only.** Kerja T23 adalah membaca + menganalisis kode (repo open-source yang tercatat di OSV / proyek yang jadi target huntr), menemukan celah di kode, dan menyusun laporan dengan bukti dari kode + PoC lokal.
- **BUKAN** pengujian live terhadap layanan huntr, **BUKAN** otomasi agen terhadap platform huntr, **BUKAN** tantangan/arena huntr.
- Perhatikan aturan huntr yang berlaku ("Humans only" untuk sebagian jalur): sebelum laporan apa pun dikirim, Koordinator T23 (A165) WAJIB memeriksa ulang aturan pengiriman huntr yang berlaku saat itu. Bila aturannya melarang pengiriman berbasis AI, temuan dicatat + diserahkan ke Muse/Cipta untuk diputuskan jalurnya — jangan kirim diam-diam.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr). Di luar scope = JANGAN.
2. **Hanya kode publik + PoC lokal di lingkungan sendiri.** Uji payload HANYA di salinan kode lokal / lab sendiri, tidak pernah terhadap sistem live orang lain.
3. **Setujui target SEBELUM Exploiter berjalan** — Koordinator T23 (A165) menyetujui repo + file + versi yang diaudit; tanpa persetujuan itu, tidak ada pengujian.
4. **Satu repo, satu versi, satu temuan per audit** — catat commit hash / versi rilis yang diaudit; temuan tanpa versi = tidak bisa direproduksi = tidak dilaporkan.
5. **Bukti minimal:** (a) lokasi kode (file + baris + commit/versi), (b) alur data yang rentan (sumber → sink), (c) PoC lokal + outputnya, (d) dampak + perbaikan yang disarankan.
6. **Cek duplikat dulu** — periksa OSV + laporan huntr publik yang relevan sebelum menyusun laporan; duplikat dicatat, bukan dikirim.
7. **Tidak ada DoS, tidak ada uji korban, tidak ada data orang lain, tidak ada bypass EDR, tidak ada IoT/SCADA/OT.**

## Alur kerja T23 (5 peran)

| Peran | Agent | Tugas |
|---|---|---|
| Recon | A161 | Petakan repo + versi target OSV; kumpulkan advisory OSV terkait |
| Analyzer | A162 | Baca kode, petakan alur data sumber → sink, kelompokkan fungsi paling rentan |
| Exploiter | A163 | Rancang + uji PoC LOKAL dari temuan Analyzer (bukan eksekusi live); validasi benar-benar bisa dieksploitasi, hindari false positive |
| Reporter | A164 | Susun draf laporan huntr + bukti kode + PoC lokal + langkah reproduksi |
| Koordinator/Triase & QA | A165 | Pimpin tim, jadwalkan giliran, cek duplikat + validitas + aturan kirim huntr sebelum laporan disusun |

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | T23 (A161–A165) | Audit kode OSV untuk huntr |
| Pemimpin | Muse | Putuskan temuan mana yang dilaporkan + jalurnya |
