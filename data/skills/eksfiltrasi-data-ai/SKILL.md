# Skill: Eksfiltrasi Data via AI — Data Exfiltration lewat Celah Akses Konteks, RAG, atau Integrasi Sistem

> Dibangun dari riset kedua "Untuk lolos dan menghasilkan di program bug bounty menggunakan AI" (23 Nov 2026, `~/workspace/catatan/referensi-skill-bug-bounty-ai-2026-11-23.md`, Bagian 2).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh workflow di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua langkah sampai ada satu kasus nyata yang lolos gerbang QC dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target adalah aplikasi AI yang punya akses ke konteks, dokumen (RAG), atau integrasi sistem (email, Drive, kalender, database) dan diduga data bisa keluar lewat celah akses — mis. agen membaca dokumen yang bukan haknya lalu menampilkannya, konteks dari satu sumber bocor ke jawaban untuk pihak lain, atau integrasi dipakai untuk mengirim data keluar. Ini permukaan Google AI VRP S2 ($15rb, sensitive data exfiltration) dan ViKernel S2 ($500).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Memetakan jalur data, menyiapkan canary palsu, menguji eksfiltrasi, mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan varian mana yang dikembangkan jadi rantai (lihat `transfer-hunting`) |

## Sudah tercakup (jangan diduplikat)

- Prompt injection (konten tertanam yang membuat agen bertindak) → skill `buru-bug-bounty` (skill ini fokus pada JALUR KELUARNYA DATA, bukan pada isi injeksinya).
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
11. **Hanya canary palsu yang boleh keluar.** Data yang dieksfiltrasi dalam pengujian HARUS string canary buatan sendiri (mis. kode unik yang tidak ada artinya) — tidak pernah data asli, tidak pernah data orang lain, tidak pernah kredensial sungguhan.
12. **Bukti = canary sampai di luar.** Klaim "data bisa bocor" tanpa canary yang benar-benar keluar = belum berhasil.

## Langkah + gerbang

### Gerbang 1 — Petakan jalur data

1. Catat semua sumber data yang bisa dijangkau aplikasi AI pada akun sendiri: dokumen/RAG, email, Drive, kalender, database, integrasi lain. Untuk tiap sumber catat: siapa pemiliknya, siapa yang boleh membacanya, dan lewat jalur apa agen mengaksesnya.
2. Tandai batas kepercayaan: data dari sumber mana yang dipercaya agen tanpa verifikasi, dan data mana yang bisa dipengaruhi pihak luar (mis. isi dokumen, isi email).
3. **Standar lulus:** peta sumber data tertulis dengan pemilik + jalur akses tiap sumber. Sumber tanpa catatan pemilik = belum dipetakan.

### Gerbang 2 — Tanam canary palsu

1. Buat string canary unik yang tidak ada artinya (mis. `CANARY-<kode-acak>`), simpan di SATU sumber data milik sendiri (satu dokumen, satu email, satu file). Catat di mana canary ditanam dan siapa saja yang berhak membacanya.
2. Jangan menanam canary di data orang lain atau di permukaan publik.
3. **Standar lulus:** canary tercatat (lokasi + siapa yang berhak baca). Tanpa canary tercatat, hasil uji tidak bisa dinilai.

### Gerbang 3 — Rumuskan hipotesis jalur keluar

1. Tulis hipotesis dalam format: "Saya menduga canary di [sumber A] bisa keluar lewat [jalur B: jawaban agen / email terkirim / ringkasan / tool output] karena [celah akses]."
2. Jalur keluar yang dicari: agen menampilkan konteks yang bukan hak penanya; agen mengirim data ke destinasi yang dikendalikan penyerang; ringkasan/ekspor yang menyertakan data dari sumber yang tidak semestinya terbaca.
3. **Standar lulus:** hipotesis menyebut sumber, jalur keluar, dan celah akses yang diduga. Hipotesis tanpa jalur keluar spesifik = dugaan kosong.

### Gerbang 4 — Uji dengan langkah minimal

1. Minta agen melakukan tugas normal yang melewati jalur yang diduga (bertanya soal dokumen, minta ringkasan, minta kirim sesuatu). Destinasi selalu canary/akun sendiri. Satu variasi per putaran; catat respons persis.
2. Periksa: apakah canary muncul di tempat yang tidak semestinya (jawaban, email keluar, file ekspor)?
3. **Standar lulus:** log tiap percobaan (permintaan → respons → canary muncul di mana?). Canary tidak muncul = gagal, catat dan variasikan.

### Gerbang 5 — Buktikan eksfiltrasi

1. Bukti yang diterima: string canary yang ditanam di sumber A muncul di tempat B yang tidak berhak membacanya (jawaban untuk konteks lain, email ke alamat penyerang-milik-sendiri, ekspor, tool output) — disertai log/transkrip langkah reproduksi persis.
2. Berhenti menguji jalur itu begitu berhasil; kembangkan jadi rantai end-to-end (lihat `transfer-hunting`) dan uji ke program lain.
3. **Standar lulus:** ada bukti canary keluar + langkah reproduksi yang bisa diulang orang lain. Tanpa canary yang keluar = belum berhasil.

### Gerbang 6 — Serahkan ke triase

1. Serahkan bukti ke A61/A68 (`triase-duplikat`): skor per tier program (Google S2 $15rb, ViKernel S2 $500) + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
2. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai; canary adalah satu-satunya "data sensitif" dalam pengujian. |
| Aplikasi AI target (dalam scope) | Diamati sebagai pengguna asli: sumber data apa yang dijangkau, lewat jalur apa. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta jalur data, lokasi canary, dan semua percobaan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi AI]
Sumber data: [dokumen/RAG/integrasi + pemiliknya]
Canary: [kode canary + lokasi tanam + siapa yang berhak baca]
Hipotesis jalur keluar: [sumber → jalur → celah]
Percobaan:
  1. [langkah] → [respons] → [canary muncul di mana?]
Bukti eksfiltrasi: [canary sampai di luar + file log/transkrip]
Dampak: [kategori hadiah yang cocok, mis. Google S2 $15rb]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

Nilai canary itu sendiri boleh ditulis di log (canary palsu, tidak ada artinya) — tetapi JANGAN pernah menulis data asli atau kredensial sungguhan di log mana pun.

## Batasan yang diketahui

- Bila aplikasi AI tidak punya akses ke sumber data lain selain milik penanya sendiri, tidak ada eksfiltrasi yang bisa dibuktikan — skill ini tidak berlaku, jangan dipaksakan.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.
