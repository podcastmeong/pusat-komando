# Skill: Perangkaian Kerentanan — Gabung Temuan Kecil Jadi Dampak Kritis

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 7 butir 44 — Vulnerability Chaining).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu rantai yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada dua (atau lebih) temuan kecil yang masing-masing sudah terbukti sendiri, tetapi dampak masing-masing terlalu kecil untuk dibayar — dan gabungannya diduga menghasilkan dampak kritis (mis. Open Redirect + OAuth Misconfiguration = Account Takeover; Self-XSS + CSRF = eksekusi skrip di akun korban). Dipakai sesudah tiap temuan lolos `verifikasi-poc-aman` dan `skeptic-false-positive-eliminator` secara sendiri-sendiri — skill ini hanya merangkai, bukan membuktikan temuan mentah. Untuk rantai injeksi prompt di program bounty agen AI, pakai `transfer-hunting` (A55) — skill ini untuk rantai web/API klasik.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55 Analis Rantai & Pelapor** | Memetakan pasangan temuan, merangkai rantai, membuktikan dampak ujung-ke-ujung |
| Audit | **A60 Security Auditor** | Memeriksa tiap mata rantai sudah terbukti sendiri + dampak gabungan nyata |
| Pemimpin | **Muse** | Memutuskan rantai mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pembuktian tiap temuan secara sendiri-sendiri → `verifikasi-poc-aman` (bukti aman per jenis) + `skeptic-false-positive-eliminator` (gerbang zero-FP).
- Variasi payload untuk satu temuan → `rekonstruksi-iterasi-payload` + `mutasi-payload-dinamis`.
- Rantai injeksi prompt antar program AI (varian lolos → rantai end-to-end lintas program) → `transfer-hunting` — skill ini BUKAN itu; jangan campur keduanya.
- Kategori tiap temuan (Business Logic, OAuth/SSO, IDOR, XSS, SSRF) → `perburuan-kerentanan-spesifik` + `fondasi-kerentanan-web-api`.

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
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
11. **Chaining hanya menggabungkan temuan yang masing-masing sudah terbukti sendiri.** Satu mata rantai yang belum terbukti = rantai belum ada. Jangan menambal mata rantai yang lemah dengan asumsi.
12. **Tanpa aksi destruktif.** Pembuktian rantai harus aman dan read-only: bukti baca, callback canary, `document.domain` — tanpa DROP, DELETE, atau hapus data apa pun.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Inventarisasi temuan terbukti

1. Kumpulkan semua temuan yang sudah berstatus VERIFIED (lolos `skeptic-false-positive-eliminator`) pada target yang sama. Untuk tiap temuan catat: jenis, titik masuk, prasyarat (butuh login? butuh interaksi korban? butuh parameter apa?), dan dampaknya sendiri.
2. **Standar lulus:** daftar temuan VERIFIED tertulis dengan prasyarat tiap temuan. Temuan yang belum VERIFIED tidak masuk daftar — jangan merangkai dari dugaan.

### Gerbang 2 — Cari pasangan yang saling melengkapi

1. Cari pasangan (atau tiga serangkai) yang prasyaratnya saling mengisi: temuan A memberi apa yang dibutuhkan temuan B. Pola yang dicari:
   - **Open Redirect + OAuth Misconfiguration = Account Takeover:** redirect mengarahkan `authorization code` ke alamat penyerang, lalu kode itu ditukar jadi sesi korban.
   - **Self-XSS + CSRF = Stored XSS di akun korban:** CSRF memaksa browser korban mengirim payload Self-XSS ke akunnya sendiri, sehingga skrip jalan di sesi korban.
   - **CORS misconfiguration + IDOR = pencurian data lintas situs:** CORS membocorkan respons, IDOR memberi objek milik orang lain.
   - **Subdomain Takeover + cookie tanpa Domain yang ketat = pembajakan sesi:** skrip di subdomain yang diambil alih membaca/mengirim cookie sesi.
   - **Cache Poisoning + XSS = Stored XSS lewat cache:** respons beracun tersimpan di CDN dan dieksekusi ke semua pengunjung.
2. Untuk tiap pasangan tulis rantai lengkap: langkah 1 → langkah 2 → dampak akhir, plus prasyarat yang masih hilang (mis. butuh korban mengklik tautan = 1-klik, catat jujur — jangan sembunyikan interaksi korban).
3. **Standar lulus:** tiap pasangan punya diagram rantai tertulis (langkah → langkah → dampak) + prasyarat yang hilang dicatat. Pasangan tanpa dampak akhir yang lebih besar dari tiap bagiannya = bukan rantai, jangan lanjut.

### Gerbang 3 — Buktikan rantai ujung-ke-ujung

1. Jalankan rantai lengkap dari langkah pertama sampai dampak akhir, memakai akun sendiri di kedua sisi (penyerang + korban — keduanya milik sendiri). Tiap langkah memakai bukti aman sesuai `verifikasi-poc-aman` (mis. `document.domain` untuk XSS, callback canary untuk SSRF/redirect).
2. Buktikan dampak AKHIR-nya, bukan tiap langkahnya saja: untuk ATO, tunjukkan sesi akun korban benar-benar terbentuk; untuk XSS lewat CSRF, tunjukkan skrip jalan di sesi akun kedua milik sendiri.
3. **Standar lulus:** ada bukti dampak akhir nyata pada akun sendiri (sesi terbentuk / skrip jalan di sesi kedua / data terbaca) + langkah reproduksi persis dari langkah 1. Rantai yang berhenti di tengah jalan = belum terbukti.

### Gerbang 4 — Nilai, serahkan ke triase

1. Nilai rantai: dampak akhir vs dampak tiap bagian — bila dampak akhir tidak lebih besar dari bagian terbesarnya, laporkan bagiannya saja, jangan klaim rantai. Catat jumlah interaksi korban yang dibutuhkan (0-klik / 1-klik / lebih) karena itu memengaruhi tier hadiah.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan + jumlah klik/interaksi korban tertulis jujur.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (penyerang + korban) | Wajib — kedua sisi rantai memakai akun milik sendiri |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log inventaris temuan VERIFIED + diagram rantai + bukti dampak akhir + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur]
Rantai: [temuan A] + [temuan B] → [dampak akhir]
Mata rantai (masing-masing VERIFIED): [A: reference ID bukti] | [B: reference ID bukti]
Langkah reproduksi: [1 → 2 → dampak akhir]
Interaksi korban: [0-klik / 1-klik / lebih — jelaskan]
Dampak akhir terbukti: [apa yang terjadi pada akun sendiri]
Keputusan triase: [maju / ditolak + alasan]
Status: [dirangkai / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Rantai yang butuh interaksi korban dinilai lebih rendah oleh sebagian program — catat jujur, jangan sembunyikan.
- Dua temuan pada target/program yang berbeda umumnya TIDAK bisa dirangkai jadi satu laporan.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar) — gunakan `transfer-hunting` untuk rantai prompt AI, bukan skill ini.
