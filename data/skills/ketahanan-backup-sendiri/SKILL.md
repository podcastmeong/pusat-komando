# Skill: Ketahanan Backup Sendiri — Uji Apakah Backup Bertahan dan Pemulihan Berhasil

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 118. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: menguji pada sistem SENDIRI apakah backup bertahan saat data dirusak dan apakah pemulihan dari backup berhasil — dengan merusak data CANARY milik sendiri, bukan data nyata. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Sistem/backup SENDIRI saja; tanpa menyentuh backup orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **huntr, Perplexity VDP, Mistral VDP**. Skill ini adalah skill LAB/sistem-sendiri: hasil uji dipakai untuk memahami ketahanan backup dan menulis laporan hanya bila program mencantumkan aset/sistem dengan mekanisme backup yang relevan — temuan pada sistem sendiri bukan temuan pada target program kecuali direproduksi pada aset in-scope sesuai pasal scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu menguji ketahanan backup sistem sendiri: apakah backup terpisah dari data utama (tidak ikut rusak saat data utama dirusak), apakah backup terenkripsi/terlindungi dari penghapusan, apakah pemulihan dari backup berhasil penuh, dan berapa lama pemulihan memakan waktu. Dipakai pada sistem + backup MILIK SENDIRI (mesin/VM lab, data canary). Dipakai SEBELUM mengklaim kelemahan backup pada target program — lab membuktikan pola pengujiannya, target in-scope membuktikan relevansinya. Dipakai juga sebagai jaring pengaman internal: setiap uji sabotase lain yang mengubah data harus didahului backup yang teruji skill ini.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Merancang skenario perusakan data canary + uji pemulihan backup |
| Pengerjaan | **A54 Penguji Live** | Menjalankan perusakan canary, memulihkan dari backup, memeriksa integritas |
| Audit | **A60 Security Auditor** | Memvalidasi bukti pemulihan sebelum dicatat sebagai hasil (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan apakah hasil relevan untuk dilaporkan/dipelajari |

## Sudah tercakup (jangan diduplikat)

- Pemulihan/rollback aksi agen sendiri → skill `pemulihan-rollback-agen-sendiri` (rollback aksi agen, bukan pemulihan dari backup sistem).
- Uji ketahanan DoS pada layanan sendiri → skill `ketahanan-dos-lab-sendiri` (ketahanan layanan, bukan backup).
- Pembajakan pembaruan otomatis di lab → skill `pembajakan-pembaruan-otomatis-lab` (snapshot dipakai sebagai pengaman di sana).
- Basis data terekspos / git terekspos → skill `basis-data-terbuka-elasticsearch-mongo-redis`, `git-terekspos` (paparan data, bukan ketahanan backup).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Sistem, backup, dan data yang dirusak/dipulihkan semuanya milik sendiri; data yang dirusak adalah data CANARY yang dibuat khusus untuk uji ini.
3. **Tanpa data orang lain.** Tanpa menyentuh, merusak, menghapus, atau memulihkan backup/data milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Tidak ada korban dalam uji ini — hanya sistem lab sendiri.
5. **Tanpa DoS/DDoS pada target program.** Uji backup hanya pada sistem lab sendiri.
6. **Tanpa payload di permukaan publik.** Skenario dan konfigurasi uji tidak di-host/dibagikan di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim pemulihan/kegagalan diperiksa manusia (Muse/A60) sebelum dicatat sebagai hasil.
8. **Tanpa laporan tanpa persetujuan Cipta.** Hasil ditulis sebagai DRAF/catatan lab dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG merusak data nyata — yang dirusak HANYA data canary yang dibuat untuk uji ini, pada sistem lab yang datanya memang disiapkan untuk dirusak. DILARANG menghapus/mengubah backup yang bukan milik sendiri. DILARANG menguji "ketahanan backup" dengan merusak sistem produksi atau sistem orang lain. SEBELUM merusak data canary, pastikan ada SALINAN KEDUA data penting lab di tempat terpisah (backup dari backup) agar uji tidak pernah menyebabkan kehilangan yang tidak bisa dipulihkan. Setelah uji selesai, sistem lab WAJIB dipulihkan ke kondisi semula dan pemulihannya dicatat.

## Langkah + gerbang

### Gerbang 0 — Cek scope + siapkan sistem, data canary, dan backup ganda

1. Baca pasal scope program yang dituju; catat relevansi aset/sistem. Siapkan sistem lab milik sendiri dengan data CANARY (file/nilai palsu yang unik, mudah dikenali). Buat BACKUP data canary, lalu buat SALINAN KEDUA backup di tempat terpisah. Verifikasi kedua backup bisa dibaca/dipulihkan SEBELUM perusakan apa pun.
2. **Standar lulus:** data canary tercatat + backup + salinan kedua terverifikasi bisa dipulihkan + pasal scope tercatat. Tanpa salinan kedua = jangan mulai.

### Gerbang 1 — Baseline: backup utuh + data canary utuh

1. Catat isi data canary (daftar file + hash/checksum tiap file) dan isi backup (daftar file + checksum). Verifikasi backup sama dengan data canary saat ini. Catat lokasi backup (apakah terpisah dari data utama? apakah bisa diakses dari sistem yang sama?).
2. **Standar lulus:** checksum data canary = checksum backup + lokasi/isolasi backup tercatat. Tanpa checksum, kerusakan tidak terukur.

### Gerbang 2 — Rusak data canary (simulasi kerusakan)

1. Rusak data canary milik sendiri dengan cara yang direncanakan: hapus sebagian file, ubah isi file, atau timpa dengan data acak — HANYA pada data canary di sistem lab. Catat persis apa yang dirusak. JANGAN sentuh backup selama tahap ini.
2. **Standar lulus:** daftar kerusakan tercatat (file apa + bagaimana dirusak). Kerusakan di luar daftar = hentikan uji dan laporkan ke Muse.

### Gerbang 3 — Periksa apakah backup ikut rusak

1. Periksa backup: apakah backup masih utuh (checksum sama seperti Gerbang 1)? Apakah backup bisa dihapus/diubah dari sistem yang sama (mis. backup berada di folder yang sama dan ikut terhapus)? Catat isolasi backup: terpisah/tidak, terlindungi dari hapus/tidak, terenkripsi/tidak.
2. **Standar lulus:** status backup tercatat (utuh/rusak + isolasi + perlindungan). Backup yang ikut rusak = hasil penting — catat persis bagaimana ia ikut rusak.

### Gerbang 4 — Pulihkan dari backup + ukur keberhasilan dan waktu

1. Pulihkan data canary dari backup. Ukur: berapa lama pemulihan, apakah semua file kembali, apakah checksum setelah pemulihan sama dengan checksum Gerbang 1. Bila pemulihan gagal/sebagian, pulihkan dari SALINAN KEDUA Gerbang 0 dan catat kegagalan backup pertama.
2. **Standar lulus:** hasil pemulihan tercatat (penuh/sebagian/gagal + waktu + checksum akhir). Tanpa checksum akhir = pemulihan belum terverifikasi.

### Gerbang 5 — Nilai + tulis hasil

1. Nilai ketahanan backup: isolasi, perlindungan hapus, enkripsi, keberhasilan dan kecepatan pemulihan. Tulis hasil lengkap + relevansi ke aset in-scope program bila ada. Serahkan ke A60 untuk validasi angka.
2. **Standar lulus:** hasil mengikuti format output + angka divalidasi A60. Tanpa validasi = jangan jadikan rujukan.

## Alat

| Alat | Cara pakai |
|---|---|
| Sistem lab milik sendiri + data canary | Satu-satunya sistem/data yang dirusak |
| Backup + salinan kedua backup (lokasi terpisah) | Backup diuji ketahanannya; salinan kedua adalah jaring pengaman |
| Checksum/hash file (mis. sha256sum) | Membuktikan data utuh/rusak/pulih penuh |
| Alat pemulihan backup produk | Menjalankan pemulihan dan mengukur waktunya |
| `~/workspace/catatan/log-bug-bounty.md` | Log baseline, kerusakan, status backup, pemulihan, dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [huntr / Perplexity VDP / Mistral VDP]
Sistem lab: [sistem milik sendiri — data canary saja]
Backup + salinan kedua: [ya — keduanya terverifikasi sebelum uji]
Baseline: [checksum data canary = checksum backup]
Kerusakan: [file canary yang dirusak — daftar persis]
Backup ikut rusak: [tidak — utuh / ya — bagaimana]
Isolasi backup: [terpisah/tidak — terlindungi hapus: ya/tidak — enkripsi: ya/tidak]
Pemulihan: [penuh/sebagian/gagal — waktu ... — checksum akhir sama: ya/tidak]
Dipulihkan dari: [backup pertama / salinan kedua]
Sistem lab kembali normal: [ya]
Keputusan: [pembelajaran lab / maju ke draf — diputuskan A60 + Muse]
Status: [DRAF — menunggu persetujuan Cipta / dicatat sebagai pembelajaran]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program — lab hanya membuktikan pola pengujian; relevansi ke aset in-scope harus dibuktikan terpisah.
- Backup yang tidak pernah diuji pemulihannya belum terbukti bisa memulihkan — uji ini mengukur pemulihan nyata, bukan sekadar keberadaan file backup.
- Uji ini memakai data canary kecil — waktu pemulihan data besar di dunia nyata akan berbeda; catat ukuran data yang diuji.
- Skill ini tidak membahas rollback aksi agen (lihat `pemulihan-rollback-agen-sendiri`) atau ketahanan layanan terhadap beban (lihat `ketahanan-dos-lab-sendiri`).
