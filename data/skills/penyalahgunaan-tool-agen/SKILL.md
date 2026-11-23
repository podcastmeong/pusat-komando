# Skill: Penyalahgunaan Tool / Agen — Tool Misuse & Agent Abuse

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 2).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh workflow di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua langkah sampai ada satu kasus nyata yang lolos gerbang QC dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target adalah aplikasi/agen AI yang punya akses tool, API, atau kemampuan beraksi (mengirim email/pesan, membaca file, mengubah data, memanggil API) dan diduga agen bisa dibuat melakukan tindakan berisiko DI LUAR otoritas semestinya — mis. beraksi tanpa konfirmasi pengguna, melewati batas otorisasi tool, atau menyetujui permintaannya sendiri. Ini permukaan utama Google AI VRP S1 ($20rb, rogue actions) dan OpenAI Safety P1 ($5.500–$7.500).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Memetakan tool/izin agen, menguji penyalahgunaan, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan varian mana yang dikembangkan jadi rantai (lihat `transfer-hunting`) |

## Sudah tercakup (jangan diduplikat)

- Prompt injection (konten tertanam yang membuat agen bertindak) → skill `buru-bug-bounty` (skill ini fokus pada PENYALAHGUNAAN TOOL/IZIN-nya, bukan pada isi injeksinya).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.
- Bukti dampak → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR.** Tim 4 Google hanya melakukan analisis format, tanpa file payload (lihat `buru-bug-bounty`). Skill ini untuk Tim 4 hanya dipakai sebagai analisis format — pengujian payload injeksi Google JANGAN diulang.
11. **Aksi yang diuji harus bisa dibatalkan/tidak merusak.** Jangan menghapus, jangan mengubah konfigurasi permanen, jangan mengirim ke alamat asli. Destinasi aksi selalu alamat/canary milik sendiri.
12. **Bukti = aksi tanpa approval.** Klaim "agen bisa disalahgunakan" tanpa bukti aksi nyata = belum berhasil.

## Langkah + gerbang

### Gerbang 1 — Inventarisasi tool & izin agen

1. Catat semua tool/API yang bisa dipakai agen pada akun sendiri: nama tool, apa yang bisa dilakukannya, izin apa yang diminta, dan kapan konfirmasi pengguna muncul (atau tidak muncul).
2. Tandai tool berisiko tinggi: kirim (email/pesan), baca (file/dokumen), ubah/hapus, panggil API eksternal, dan tool yang mengubah izin sendiri.
3. **Standar lulus:** daftar tool tertulis dengan izin + titik konfirmasi tiap tool. Tool tanpa catatan izin = belum diinventarisasi.

### Gerbang 2 — Petakan jalur approval

1. Untuk tiap tool berisiko, uji sebagai pengguna normal: tindakan apa yang memicu konfirmasi, apa yang lolos tanpa konfirmasi, dan apa yang terjadi bila pengguna menolak.
2. Catat aturan egress/approval: destinasi mana yang diizinkan diam-diam, ambang apa yang memicu deteksi.
3. **Standar lulus:** ada peta "tindakan → butuh konfirmasi? ya/tidak" per tool. Tanpa peta ini, pengujian buta.

### Gerbang 3 — Rumuskan hipotesis penyalahgunaan

1. Tulis hipotesis dalam format: "Saya menduga agen bisa [tindakan berisiko] tanpa [konfirmasi/otorisasi yang semestinya] karena [celah pada jalur approval/izin]."
2. Contoh pola yang dicari: agen menyetujui permintaannya sendiri; izin connector diubah dari ask menjadi allow; API dipanggil langsung melewati approval; egress lewat destinasi yang di-allowlist.
3. **Standar lulus:** hipotesis menyebut tool, tindakan, dan celah jalur approval yang diduga. Hipotesis tanpa celah spesifik = dugaan kosong.

### Gerbang 4 — Uji dengan langkah minimal

1. Uji hipotesis dengan langkah paling kecil yang bisa membuktikan: minta agen melakukan tindakan itu dalam kondisi yang diduga melewati approval. Destinasi selalu canary/akun sendiri.
2. Satu variasi per putaran; catat respons + apa yang sebenarnya terjadi (apakah aksi benar-benar jalan, atau hanya dijanjikan).
3. **Standar lulus:** log tiap percobaan (permintaan → respons → aksi benar terjadi? ya/tidak). Agen yang hanya "berjanji" tanpa beraksi = GAGAL.

### Gerbang 5 — Buktikan aksi tanpa approval

1. Bukti yang diterima: aksi nyata terjadi (email terkirim ke canary, file terbaca/terkirim, API terpanggil, izin berubah) TANPA konfirmasi pengguna yang semestinya — disertai log/transkrip langkah reproduksi persis.
2. Berhenti menguji jalur itu begitu berhasil; kembangkan jadi rantai end-to-end (lihat `transfer-hunting`) dan uji ke program lain.
3. **Standar lulus:** ada bukti aksi nyata + langkah reproduksi yang bisa diulang orang lain. Tanpa aksi nyata = belum berhasil.

### Gerbang 6 — Serahkan ke triase

1. Serahkan bukti ke A61/A68 (`triase-duplikat`): skor per tier program (Google S1 $20rb, OpenAI P1) + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
2. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai; destinasi semua aksi uji. |
| Agen/aplikasi AI target (dalam scope) | Diamati sebagai pengguna asli: tool apa yang ada, kapan konfirmasi muncul. |
| `~/workspace/catatan/log-bug-bounty.md` | Log inventarisasi tool, peta approval, dan semua percobaan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi/agen]
Tool yang diuji: [nama tool + izinnya]
Jalur approval normal: [tindakan → butuh konfirmasi?]
Hipotesis: [tindakan tanpa approval karena celah apa]
Percobaan:
  1. [langkah] → [respons] → [aksi terjadi? ya/tidak]
Bukti aksi tanpa approval: [apa yang terjadi + file log/transkrip]
Dampak: [kategori hadiah yang cocok, mis. Google S1 $20rb]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Pola "agen menyetujui permintaannya sendiri" sudah dicatat di `buru-bug-bounty` sebagai teknik yang bisa bikin jebol — skill ini adalah playbook langkah-demi-langkah untuk mengujinya secara sistematis, bukan pengulangan daftar teknik.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.
