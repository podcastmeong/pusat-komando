# Skill: Peracunan Memori Aktif Muse — Active Memory & Active Focus Poisoning

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi

Peracunan memori aktif: konten tidak tepercaya (dari dokumen, email, pesan, atau tool output yang dibaca agen) tersimpan sebagai memori aktif Muse — Active Memory atau Active Focus — lalu dipakai sebagai fakta di percakapan/job berikutnya, sehingga instruksi atau klaim palsu bertahan lintas sesi dan mengarahkan aksi agen. Skill ini HANYA menguji rantai itu pada akun sendiri dengan canary palsu.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bounty resmi, di sini: **Muse (Meta)**. Di luar program resmi = tidak boleh dipakai. Hanya akun sendiri + canary palsu. Tanpa data orang lain, tanpa uji korban, tanpa eksfiltrasi.

## Pemicu (kapan dipakai)

Dipakai saat menguji apakah nilai dari sumber tidak tepercaya masuk ke Active Memory/Focus; saat menguji apakah memori yang diracuni bertahan lintas sesi dan memengaruhi jawaban atau job berikutnya; saat menguji apakah memori bisa ditulis, diubah, atau dihapus lewat konten yang dibaca agen (bukan lewat perintah pengguna langsung).

## Sudah tercakup (jangan diduplikat)

- Racun RAG / memori retrieval secara umum → skill `racun-rag-memori`.
- Manajemen memori koreksi-diri → skill `koreksi-diri-manajemen-memori`.
- Manajer memori operasional → skill `manajer-memori`.
- Paparan konteks tersembunyi → skill `paparan-konteks-tersembunyi`.
- Injeksi lewat ringkasan buatan sendiri → skill `injeksi-buatan-sendiri-ringakasan`.
- Injeksi prompt tidak langsung secara umum → skill `injeksi-prompt-tidak-langsung-agen`.
- Pembuktian dampak dengan canary → skill `canary-pembuktian-dampak`.

## Tahap rantai (petakan sebelum menguji)

| Tahap | Yang diuji | Bukti yang dicari |
|---|---|---|
| 1. Suntik | Konten tidak tepercaya dibaca agen (dokumen/email/tool output milik sendiri) | Konten tercatat sebagai sumber |
| 2. Simpan | Nilai dari konten itu tersimpan sebagai memori aktif (Active Memory/Focus) | Memori menampilkan nilai canary |
| 3. Bertahan | Nilai bertahan lintas sesi / job berikutnya | Sesi baru masih memakai nilai canary |
| 4. Pengaruh | Memori yang diracuni mengarahkan jawaban atau aksi agen | Agen bertindak berdasarkan nilai canary |

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Nilai racun HANYA canary unik milik sendiri (mis. nama/fakta palsu yang tidak mungkin benar), tidak pernah data nyata.
3. **Tanpa data orang lain.** Jangan memakai nama, fakta, atau dokumen orang lain sebagai isi racun.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Memori yang diuji hanya memori akun sendiri.
5. **Gerbang persetujuan manusia SEBELUM tahap pengaruh.** Exploiter TIDAK menguji tahap 4 sebelum Koordinator/Triase & QA dan Muse menyetujui target + canary-nya; persetujuan dicatat.
6. **Tanpa DoS/DDoS.** Satu nilai racun per hipotesis, volume kecil.
7. **Tanpa payload di permukaan publik.** Dokumen/email sumber racun tidak disebar atau dipublikasikan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG racun yang berujung hapus/ubah memori orang lain, hapus data, kirim dana, atau aksi ke pihak ketiga. Nilai racun HARUS inert: hanya canary yang bila dipakai agen hanya tercatat sebagai bukti. Setelah uji selesai, memori yang diracuni DIBERSIHKAN (nilai canary dihapus/dikoreksi, sesi ditutup) dan pembersihannya dicatat.
10. **Satu hipotesis = satu nilai = satu catatan.** Tiap varian (sumber racun, format nilai, posisi memori) dicatat terpisah dengan hasil lolos/gagal.

## Langkah + gerbang

### Gerbang 0 — Tulis hipotesis + canary (Recon + Analyzer)

1. Tulis hipotesis satu kalimat: "Konten X dari sumber Y menyebabkan memori aktif menyimpan Z dan memakainya di sesi berikut."
2. Pilih canary unik yang HANYA bisa muncul bila memori benar-benar menyimpan nilai itu.
3. Catat scope program Muse yang berlaku; bila ragu soal scope, TANYA dulu — jangan uji.

### Gerbang 1 — Suntik lewat sumber milik sendiri (Recon)

4. Buat SATU sumber racun di akun sendiri (dokumen/email milik sendiri berisi canary).
5. Minta agen membaca sumber itu dalam tugas wajar; catat apa yang dibaca dan kapan.

### Gerbang 2 — Periksa simpan + bertahan (Analyzer)

6. Periksa apakah memori aktif menampilkan nilai canary; buka sesi/job baru dan periksa apakah nilai itu masih dipakai — TANPA memancing aksi.
7. Bila tidak tersimpan/bertahan: catat GAGAL untuk varian itu. Bila bertahan: lanjut ke Gerbang 3.

### Gerbang 3 — Persetujuan pengaruh (Koordinator/Triase & QA + Muse)

8. Koordinator memeriksa: target in-scope? canary inert? duplikat dengan temuan lama? Bila satu saja TIDAK, uji BERHENTI.
9. Muse menyetujui target + canary secara tertulis di log tim.

### Gerbang 4 — Uji pengaruh + bukti (Exploiter + Reporter)

10. Uji apakah memori beracun mengarahkan jawaban/aksi; pantau canary. Tangkap bukti: kutipan memori, log sesi, langkah reproduksi.
11. Reporter menyusun draf sesuai standar platform (HackerOne/Bugcrowd): ringkasan, langkah reproduksi, dampak, bukti canary. Draf dulu — kirim hanya setelah persetujuan Cipta.
12. Bersihkan memori beracun + hapus sumber racun; catat pembersihan.
