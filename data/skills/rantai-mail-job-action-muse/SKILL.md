# Skill: Rantai Mail-Job-Action Muse — Uji 0-Klik dari Email ke Aksi Agen

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi

Rantai mail→job→action: sebuah email (atau pesan) yang diterima agen Muse berisi instruksi tersembunyi, yang lalu dibaca sebagai konteks kerja, diubah menjadi job/tugas, dan dieksekusi sebagai aksi (kirim, ubah, hapus, panggil tool) — tanpa klik atau persetujuan pengguna. Hipotesis H-M10 dan turunannya menguji apakah rantai ini bisa dipicu 0-klik pada akun sendiri. Skill ini HANYA memetakan dan menguji rantai itu pada akun sendiri dengan canary palsu.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bounty resmi, di sini: **Muse (Meta)**. Di luar program resmi = tidak boleh dipakai. Hanya akun sendiri + canary palsu. Tanpa data orang lain, tanpa uji korban, tanpa eksfiltrasi.

## Pemicu (kapan dipakai)

Dipakai saat menguji apakah instruksi di dalam email/pesan yang masuk bisa menjadi job lalu aksi tanpa persetujuan; saat memetakan jalur email → ringkasan → job → tool call di Muse; saat menguji varian H-M10 (format email berbeda, lampiran, undangan kalender, balasan berantai).

## Sudah tercakup (jangan diduplikat)

- Spoofing pengirim / SPF-DKIM-DMARC → skill `perburuan-tls-dns-email-spoofing`.
- Penyelundupan SMTP / header email → skill `penyelundupan-smtp-email`.
- Injeksi lewat undangan kalender → skill `injeksi-undangan-kalender`.
- Injeksi prompt tidak langsung secara umum → skill `injeksi-prompt-tidak-langsung-agen`.
- Injeksi lewat ringkasan buatan sendiri → skill `injeksi-buatan-sendiri-ringakasan`.
- Pembuktian dampak dengan canary → skill `canary-pembuktian-dampak`.

## Tahap rantai (petakan sebelum menguji)

| Tahap | Yang diuji | Bukti yang dicari |
|---|---|---|
| 1. Masuk | Email tiba di inbox akun sendiri, berisi instruksi tersembunyi (teks putih, lampiran, metadata) | Email terkirim ke akun sendiri, isi tercatat |
| 2. Baca | Agen membaca email sebagai konteks (ringkasan, kutipan, pencarian) | Agen mengutip isi email tanpa diminta |
| 3. Job | Instruksi berubah menjadi job/tugas yang dijadwalkan atau diantrekan | Job tercatat dengan sumber = email itu |
| 4. Aksi | Job dieksekusi sebagai aksi (kirim/ubah/panggil tool) tanpa klik pengguna | Canary tersentuh = aksi terjadi |

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Email uji hanya dikirim ke akun sendiri; aksi uji hanya menyentuh canary milik sendiri.
3. **Tanpa data orang lain.** Jangan memakai nama, email, atau dokumen orang lain sebagai isi uji.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Rantai tidak diuji pada akun atau jalur yang melayani pengguna lain.
5. **Gerbang persetujuan manusia SEBELUM tahap aksi.** Exploiter TIDAK menjalankan tahap 4 sebelum Koordinator/Triase & QA dan Muse menyetujui target + canary-nya; persetujuan dicatat.
6. **Tanpa DoS/DDoS.** Uji satu email per hipotesis, volume kecil, jeda wajar.
7. **Tanpa payload di permukaan publik.** Email uji tidak disebar; lampiran uji tidak dipublikasikan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG rantai yang berujung hapus data, kirim dana, kirim ke pihak ketiga, atau ubah akun orang lain. Aksi uji HARUS inert: hanya menyentuh canary milik sendiri, dan setelah uji selesai canary DIBERSIHKAN (nilai dikembalikan, job dibatalkan, jejak dihapus) dan pembersihannya dicatat.
10. **Satu hipotesis = satu rantai = satu catatan.** Tiap varian (format email, posisi instruksi, jenis lampiran) dicatat terpisah dengan hasil lolos/gagal.

## Langkah + gerbang

### Gerbang 0 — Tulis hipotesis + canary (Recon + Analyzer)

1. Tulis hipotesis satu kalimat: "Email berisi X di posisi Y menyebabkan agen melakukan Z tanpa klik."
2. Pilih canary yang HANYA tersentuh bila aksi Z terjadi (mis. nilai field unik di akun sendiri).
3. Catat scope program Muse yang berlaku; bila ragu soal scope, TANYA dulu — jangan uji.

### Gerbang 1 — Kirim email uji ke akun sendiri (Recon)

4. Kirim SATU email uji ke akun sendiri dari alamat yang dikuasai sendiri.
5. Catat header, isi persis, dan waktu kirim. Jangan kirim ulang dengan variasi lain sebelum hasil pertama dicatat.

### Gerbang 2 — Amati baca + job (Analyzer)

6. Amati apakah agen mengutip/membaca email itu dan apakah muncul job dari isinya — TANPA memancing aksi.
7. Bila tidak ada job: catat GAGAL untuk varian itu, lanjut ke varian berikut. Bila ada job: lanjut ke Gerbang 3.

### Gerbang 3 — Persetujuan aksi (Koordinator/Triase & QA + Muse)

8. Koordinator memeriksa: target in-scope? canary inert? duplikat dengan temuan lama? Bila satu saja TIDAK, uji BERHENTI.
9. Muse menyetujui target + canary secara tertulis di log tim.

### Gerbang 4 — Uji aksi + bukti (Exploiter + Reporter)

10. Biarkan/uji job sampai ke aksi; pantau canary. Tangkap bukti: request/response, langkah reproduksi, tangkapan layar/log.
11. Reporter menyusun draf sesuai standar platform (HackerOne/Bugcrowd): ringkasan, langkah reproduksi, dampak, bukti canary. Draf dulu — kirim hanya setelah persetujuan Cipta.
12. Bersihkan canary + batalkan job sisa; catat pembersihan.
