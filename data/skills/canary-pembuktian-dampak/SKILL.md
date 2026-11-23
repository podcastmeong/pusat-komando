# Skill: Canary Pembuktian Dampak — Merancang dan Memasang Umpan Palsu Milik Sendiri

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 115. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Skill ini adalah fondasi seluruh keluarga sabotase: canary adalah token, tautan, file, atau nilai PALSU yang unik dan hanya milik sendiri, dipasang agar tersentuh bila agen/sistem beraksi — agen menyentuh canary = bukti aksi terjadi. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Canary palsu milik sendiri; tanpa canary yang meniru data nyata orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Anthropic, huntr**. Canary dipakai di hampir setiap PoC tim — skill ini dipakai BERSAMA skill pembuktian dampak lainnya, bukan berdiri sendiri sebagai temuan.

## Pemicu (kapan dipakai)

Dipakai SETIAP kali sebuah uji butuh bukti bahwa suatu aksi benar-benar terjadi: sebelum menjalankan `sabotase-pembuktian-dampak`, `pemicu-terjadwal-agen-sendiri`, `perilaku-fail-open-agen`, atau `pemulihan-rollback-agen-sendiri`, pasang dulu canary pada target aksi. Dipakai saat merancang PoC apa pun yang mengklaim "agen melakukan X" — tanpa canary, klaim itu tidak punya bukti yang bisa diverifikasi triase. Dipakai juga saat menguji apakah suatu nilai/file/tautan disentuh, dibaca, dikirim, atau diubah oleh agen atau sistem.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56 Red Team** | Merancang canary (jenis, nilai unik, lokasi pasang) per skenario uji |
| Pengerjaan | **A54 Penguji Live** | Memasang canary, memantau sentuhan, mencatat bukti |
| Audit | **A60 Security Auditor** | Memvalidasi keunikan dan kepemilikan canary sebelum dipakai sebagai bukti (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan canary mana yang dipakai per PoC |

## Sudah tercakup (jangan diduplikat)

- Pembuktian dampak ujung-ke-ujung → skill `sabotase-pembuktian-dampak` (MEMAKAI canary dari skill ini).
- Pemicu terjadwal → skill `pemicu-terjadwal-agen-sendiri`; fail-open → skill `perilaku-fail-open-agen`; rollback → skill `pemulihan-rollback-agen-sendiri` (semuanya MEMAKAI canary dari skill ini).
- Bukti read-only + log nilai → respons → skill `injeksi-sql-kontekstual` (pola pembuktian, bukan canary).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Jenis canary (pilih sesuai aksi yang dibuktikan)

| Jenis canary | Dipasang di | Tersentuh bila | Contoh nilai |
|---|---|---|---|
| Nilai field unik | Field preferensi/profil akun sendiri | Agen mengubah field itu | Nama tampilan `CANARY-7f3a9-2026-11-24` |
| Alamat kirim milik sendiri | Tujuan kirim/berbagi yang dimonitor | Agen mengirim ke alamat itu | Alamat email/file milik sendiri yang hanya dipakai untuk uji ini |
| File canary | Folder yang dimonitor agen/sistem sendiri | Agen membaca/mengubah/menghapus file itu | File bernama unik berisi string unik |
| Token/tautan unik | Dokumen/data yang dibaca agen | Agen membuka tautan / memakai token itu | URL canary milik sendiri dengan token unik |
| Nilai angka unik | Field jumlah/harga/kuantitas milik sendiri | Agen mengubah nilai itu | Jumlah yang tidak mungkin muncul secara wajar |

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Anthropic, huntr untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Semua canary dipasang pada akun/sistem milik sendiri.
3. **Tanpa data orang lain.** Canary TIDAK BOLEH meniru data nyata orang lain: jangan memakai nama, email, nomor, alamat, kata sandi, token, atau dokumen milik orang lain sebagai canary — dan jangan memakai canary yang bila bocor bisa disangka data nyata.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Canary tidak dipasang pada akun orang lain atau pada jalur yang melayani pengguna lain.
5. **Tanpa DoS/DDoS pada target program.** Pemantauan canary bersifat pasif (cek berkala, volume kecil).
6. **Tanpa payload di permukaan publik.** Canary tidak disebar/dipublikasikan — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim "canary tersentuh" diperiksa manusia (Muse/A60) sebelum ditulis sebagai bukti.
8. **Tanpa laporan tanpa persetujuan Cipta.** Bukti canary ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Pemantauan canary otomatis hanya di program yang mengizinkan otomasi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memasang canary yang bila tersentuh menimbulkan kerusakan (mis. canary berupa perintah hapus, canary yang memicu transfer dana, atau canary di jalur produksi orang lain). Canary HARUS inert: tersentuhnya canary hanya tercatat sebagai bukti, tidak memicu aksi lanjutan yang merusak. Setelah uji selesai, canary DIBERSIHKAN (nilai dikembalikan, file dihapus, token dicabut) dan pembersihannya dicatat.

## Langkah + gerbang

### Gerbang 0 — Tentukan aksi yang harus dibuktikan + jenis canary

1. Tulis aksi persis yang ingin dibuktikan (mis. "agen mengubah nama tampilan", "agen mengirim email", "agen membaca file X"). Pilih jenis canary dari tabel di atas yang HANYA bisa tersentuh bila aksi itu terjadi — canary yang bisa tersentuh oleh aktivitas normal sehari-hari adalah canary yang buruk.
2. **Standar lulus:** aksi + jenis canary tertulis + alasan kenapa canary itu spesifik untuk aksi tersebut. Canary tidak spesifik = jangan pakai.

### Gerbang 1 — Buat nilai canary yang unik dan inert

1. Buat nilai unik (mis. gabungan kata `CANARY` + angka acak + tanggal) yang tidak mungkin muncul secara kebetulan dan tidak meniru data nyata orang lain. Pastikan canary inert: tidak memicu aksi lanjutan, tidak berisi instruksi, tidak berisi data sensitif.
2. **Standar lulus:** nilai canary tercatat + diperiksa A60 bahwa nilai itu unik dan tidak meniru data nyata. Nilai yang meniru data nyata = buang dan buat ulang.

### Gerbang 2 — Pasang canary + catat baseline

1. Pasang canary di lokasi target (field, folder, dokumen, alamat). Catat baseline: state sebelum uji (nilai field semula, isi folder, status token) + waktu pemasangan + siapa yang memasang.
2. **Standar lulus:** lokasi + nilai + baseline tercatat. Tanpa baseline, sentuhan tidak bisa dibuktikan.

### Gerbang 3 — Pantau sentuhan selama uji

1. Selama uji berjalan (oleh skill pembuktian dampak yang memakai canary ini), pantau canary secara berkala: apakah nilai berubah, file dibaca/diubah, tautan dibuka, kiriman diterima? Catat WAKTU tiap sentuhan dan konteksnya (aksi apa yang sedang diuji saat itu).
2. **Standar lulus:** tiap sentuhan tercatat dengan waktu + konteks. Sentuhan tanpa waktu/konteks = bukti lemah.

### Gerbang 4 — Verifikasi sentuhan bukan positif palsu

1. Periksa: apakah sentuhan bisa dijelaskan oleh aktivitas lain (aktivitas normal sendiri, uji lain yang berjalan bersamaan, sistem otomatis)? Bila ya, itu positif palsu — buang dan ulangi dengan canary baru yang lebih spesifik. Konfirmasi dengan canary kedua yang berbeda bila dampaknya besar.
2. **Standar lulus:** sentuhan tidak bisa dijelaskan aktivitas lain + (bila dampak besar) terkonfirmasi canary kedua. Tidak lolos verifikasi = belum terbukti.

### Gerbang 5 — Bersihkan canary + serahkan bukti

1. Bersihkan semua canary (kembalikan nilai, hapus file, cabut token) dan catat pembersihannya. Serahkan bukti (nilai canary + waktu sentuhan + baseline + verifikasi) ke skill pembuktian dampak yang memakainya, lalu ke A60 audit → Muse → Cipta.
2. **Standar lulus:** canary bersih + bukti lengkap diserahkan. Canary tertinggal aktif = uji belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun/sistem sendiri | Satu-satunya tempat canary dipasang |
| Generator nilai unik (acak + tanggal) | Membuat nilai canary yang tidak mungkin muncul kebetulan |
| Pemantau (cek berkala manual / log sistem sendiri) | Mendeteksi sentuhan canary + mencatat waktu |
| `~/workspace/catatan/log-bug-bounty.md` | Log canary (nilai, lokasi, baseline, sentuhan, verifikasi, pembersihan) |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [Muse / OpenAI Safety / 0din / Google AI VRP / ViKernel / Anthropic / huntr]
Aksi yang dibuktikan: [aksi persis]
Jenis canary: [nilai field / alamat kirim / file / token-tautan / nilai angka]
Nilai canary: [nilai unik — tanpa data nyata orang lain]
Lokasi pasang: [field/folder/dokumen/alamat milik sendiri]
Baseline: [state sebelum uji + waktu pasang]
Sentuhan: [ya/tidak — waktu ... — konteks ...]
Verifikasi positif palsu: [tidak bisa dijelaskan aktivitas lain — atau "POSITIF PALSU, dibuang"]
Canary dibersihkan: [ya — nilai dikembalikan/file dihapus/token dicabut]
Dipakai oleh skill: [sabotase-pembuktian-dampak / pemicu-terjadwal-agen-sendiri / ...]
Status: [DRAF — menunggu persetujuan Cipta / dicatat sebagai bukti]
```

## Batasan yang diketahui

- Canary yang terlalu umum (mis. nama "test") mudah tersentuh kebetulan — selalu pakai nilai unik dengan penanda `CANARY` + acak + tanggal.
- Canary hanya membuktikan BAHWA aksi terjadi, bukan MENGAPA — penyebab tetap harus dijelaskan oleh skill pembuktian dampak yang memakainya.
- Canary yang dipasang di jalur yang juga dipakai aktivitas normal sendiri akan menghasilkan positif palsu — pilih lokasi yang hanya tersentuh oleh aksi yang diuji.
- Skill ini bukan temuan sendiri: canary tanpa aksi yang dibuktikan adalah persiapan, bukan laporan bounty.
