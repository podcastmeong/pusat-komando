# Skill: Koreksi Diri & Manajemen Memori — Jangan Ulangi Pengujian Gagal, Hubungkan Petunjuk Antar Sub-Agen

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 7 butir 47 — Self-Correction & Memory Management).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu kasus nyata di mana memori mencegah pengulangan pengujian gagal dan dicatat di log.
>
> Hubungan dengan skill lain: `manajer-memori` (DIFY-02) menyimpan memori Digistore — keputusan/progres/kesalahan proyek toko — lewat dataset Dify, BUKAN memori pengujian bounty. Skill ini adalah memori PENGUJIAN bounty: apa yang sudah diuji, apa yang gagal, petunjuk apa yang ditemukan, dan siapa (sub-agen mana) yang memegangnya. Keduanya tidak saling menggantikan; jangan simpan memori pengujian bounty ke dataset Dify Digistore, dan jangan simpan keputusan toko ke memori pengujian ini.

## Pemicu (kapan dipakai)

Dipakai (a) SEBELUM pengujian apa pun dimulai — cek memori apakah endpoint/payload/hipotesis ini sudah pernah diuji dan gagal; (b) SESUDAH tiap pengujian — simpan hasilnya (berhasil/gagal + kenapa); (c) saat sebuah temuan/petunjuk dari satu sub-agen diduga berhubungan dengan pekerjaan sub-agen lain — hubungkan petunjuknya sebelum pengujian dilanjutkan. Dipakai oleh semua tim bounty (A51–A70) pada program web/API klasik maupun bounty agen AI — memori pengujian berlaku untuk keduanya, yang berbeda hanya isi catatannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **Semua sub-agen tim bounty (A51–A70)** | Cek memori sebelum menguji; simpan hasil sesudah menguji; menautkan petunjuk ke sub-agen lain |
| Penjaga memori | **Muse (pemimpin tim)** | Menjaga satu sumber memori pengujian, menyelesaikan konflik catatan, menghapus catatan yang terbukti salah |
| Audit | **A60 Security Auditor** | Memeriksa klaim "sudah diuji" sebelum sebuah hipotesis dinyatakan buntu atau duplikat |

## Sudah tercakup (jangan diduplikat)

- Memori keputusan/progres/kesalahan proyek Digistore → `manajer-memori` (DIFY-02, dataset Dify) — BUKAN memori pengujian bounty.
- Log hipotesis + bukti + keputusan triase → `~/workspace/catatan/log-bug-bounty.md` — skill ini memakai log itu sebagai SUMBER, dan menambah indeks yang bisa dicari + tautan antar sub-agen di atasnya.
- Cek duplikat terhadap laporan publik/CVE → `triase-duplikat` (A68) — skill ini mencegah duplikat INTERNAL (pengujian yang sama diulang tim sendiri), bukan duplikat publik.

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
10. **Jangan menyimpan rahasia di memori pengujian** — kata sandi, OTP, API key, token sesi, dan data sensitif TIDAK PERNAH disimpan (sama seperti `manajer-memori`).
11. **Memori adalah catatan, bukan bukti.** Klaim "sudah terbukti" di memori tetap harus bisa ditelusur ke pasangan Request/Response atau reference ID bukti di log — memori tanpa reference ID = kabar burung, jangan dipakai untuk memutuskan triase.
12. **Jangan diam-diam menimpa catatan lama.** Bila informasi baru bertentangan dengan memori lama, laporkan + catat keduanya dengan tanggal; yang memutuskan mana yang benar adalah Muse, bukan sub-agen yang menemukan konfliknya.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu — aturan memori pengujian ini sendiri berlaku untuk keduanya.

## Langkah + gerbang

### Gerbang 1 — Cek memori SEBELUM menguji

1. Sebelum pengujian baru, cari di memori pengujian dengan 3 kunci: (a) target + endpoint, (b) jenis celah/hipotesis, (c) payload/mutasi yang akan dipakai.
2. Bila ditemukan catatan GAGAL untuk kombinasi yang sama (endpoint + jenis + payload/mutasi yang sama) → JANGAN ulangi; pilih varian lain (`rekonstruksi-iterasi-payload` / `mutasi-payload-dinamis`) atau pindah hipotesis. Bila ditemukan catatan BERHASIL → pakai sebagai titik awal, jangan mulai dari nol.
3. **Standar lulus:** ada bukti pencarian memori tercatat (kunci yang dicari + hasil: ditemukan/tidak) sebelum pengujian dimulai. Pengujian tanpa cek memori = pelanggaran prosedur — catat sebagai kesalahan di log.

### Gerbang 2 — Simpan hasil SESUDAH menguji (satu catatan = satu pengujian)

1. Setiap pengujian yang selesai — berhasil, gagal, ATAU buntu — disimpan di hari yang sama dengan format di bawah. Pengujian yang tidak disimpan = tidak terjadi.
2. Isi catatan: target + endpoint + parameter, hipotesis + jenis celah, payload/mutasi yang dipakai, respons/klasifikasi (mis. klasifikasi blokir WAF), verdict (berhasil/gagal/buntu), KENAPA (penyebab yang diketahui — filter apa, asumsi mana yang salah), sub-agen yang menguji, tanggal, reference ID bukti bila ada.
3. **Standar lulus:** tiap pengujian punya satu catatan lengkap dengan kolom KENAPA terisi. Catatan tanpa KENAPA = belum selesai disimpan — "gagal" tanpa alasan akan diulang orang lain.

### Gerbang 3 — Koreksi diri: dari gagal jadi aturan

1. Saat sebuah pengujian gagal, tulis koreksinya sebagai aturan baru yang bisa dipakai tim: "JANGAN [ulangi X] KARENA [penyebab]; COBA [Y] SEBAGAI GANTI". Satu kegagalan = satu aturan (prinsip anti-ulang).
2. Aturan baru dicatat di memori + di log hari itu, dan dibaca ulang sebelum pengujian berikutnya pada target/jenis yang sama.
3. **Standar lulus:** tiap kegagalan yang tercatat punya aturan koreksi pasangannya. Kegagalan tanpa aturan koreksi = akan terulang.

### Gerbang 4 — Hubungkan petunjuk antar sub-agen

1. Saat menyimpan catatan, beri TAG petunjuk yang mungkin relevan untuk sub-agen lain (mis. `butuh-akun-admin` → A58/access-control; `filter-WAF-keras` → A62/mutasi; `diduga-duplikat-publik` → A68; `dampak-bisnis-besar` → A61).
2. Sebelum memulai giliran kerja, tiap sub-agen membaca catatan ber-tag yang ditujukan ke perannya + catatan terbaru dari sub-agen lain pada target yang sama. Petunjuk yang menghubungkan dua temuan kecil jadi kandidat rantai → serahkan ke A55 (`perangkaian-kerentanan`).
3. **Standar lulus:** tiap catatan punya tag peran bila relevan; tiap sub-agen mencatat apa yang dibacanya dari memori sebelum bekerja. Petunjuk yang tidak dibaca siapa pun = petunjuk yang hilang.

## Alat

| Alat | Cara pakai |
|---|---|
| Memori pengujian: file indeks di `~/workspace/catatan/memori-pengujian-bounty.md` (satu baris per pengujian + tag; bila volume membesar, pindah ke vector database — sampai saat itu file ini SATU-SATUNYA sumber, jangan buat salinan kedua) | Cek sebelum menguji (Gerbang 1), simpan sesudah menguji (Gerbang 2), baca tag peran (Gerbang 4) |
| `~/workspace/catatan/log-bug-bounty.md` | Sumber detail tiap pengujian; memori pengujian hanya indeks + ringkasan + tautan ke log (bukan salinan penuh) |
| Vector database (RENCANA — belum ada) | Bila memori pengujian melewati ~200 catatan dan pencarian file sudah lambat, ajukan ke Muse untuk pindah ke vector database (simpan embedding konteks temuan agar pencarian berdasarkan kemiripan, bukan kata kunci saja). Sampai diputuskan, JANGAN membangunnya sendiri |

## Format output

Tulis ke `~/workspace/catatan/memori-pengujian-bounty.md` (satu baris per pengujian) dengan format:

```
- [tanggal] [program] [endpoint + parameter] | Hipotesis: [jenis celah] | Payload/mutasi: [nilai singkat] | Hasil: [berhasil/gagal/buntu] | Kenapa: [penyebab] | Aturan koreksi: [jangan X karena Y; coba Z] | Oleh: [Axx] | Tag: [peran lain yang relevan] | Bukti: [reference ID FP-... / —]
```

Dan ringkasan koreksi harian ke `~/workspace/catatan/log-bug-bounty.md`:

```
Koreksi diri [tanggal]: [aturan baru dari kegagalan hari ini, satu baris per aturan]
```

## Batasan yang diketahui

- Sampai vector database diputuskan dan dibangun, pencarian memori masih berbasis kata kunci di file — pencarian berdasarkan kemiripan makna belum bisa; catat kata kunci yang konsisten (nama endpoint, jenis celah, keluarga mutasi) agar pencarian berhasil.
- Memori pengujian hanya sebaik disiplin tim yang mengisinya — satu sub-agen yang tidak menyimpan = satu lubang yang akan diulang orang lain. Muse memeriksa kelengkapan memori tiap laporan malam.
- Jangan simpan memori pengujian ke dataset Dify Digistore (`manajer-memori`) — dataset itu untuk keputusan/progres toko, bukan pengujian bounty.
