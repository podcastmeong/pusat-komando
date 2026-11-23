# Skill: Pacing Request Aman — Delay, Jitter & Backoff Agar Tidak Terblokir Sendiri (untuk A54 Penguji Live + A70 Automation Engineer)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md` Fase 1 butir 2 (Rate-Limit & WAF Evasion Awareness), 23 Nov 2026.

## Pemicu

Dipakai **setiap kali sesi pengujian mengirim request berurutan ke satu target** — recon aktif, probing, fuzzing, atau pengujian varian. Skill ini mengatur KECEPATAN request supaya tim tidak memicu rate-limit, tidak diblokir WAF, dan tidak memblokir IP sendiri. Dipakai BERSAMA `scope-and-safety-guardian` (yang menetapkan batas laju) — guardian menetapkan batasnya, skill ini menjalankan pacing-nya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Terapkan pacing di setiap sesi pengujian live |
| Pengerjaan | **A70 Automation Engineer** | Terapkan pacing di skrip/otomasi pengujian; pastikan skrip berhenti otomatis saat kena blokir |
| Konsumen | **Semua tim bounty A51–A70** | Patuhi pacing ini di setiap request berurutan |
| Pemimpin | **Muse** | Putuskan bila target memblokir dan sesi harus dipindah/dihentikan |

## Sudah tercakup (jangan diduplikat)

- **Batas laju** (maks 5 permintaan/detik, kecuali program mengizinkan lebih) ada di **`scope-and-safety-guardian`** Gerbang 4 — skill ini TIDAK mengubah batas itu, hanya menjalankan pacing DI BAWAH batas itu.
- **Larangan DoS/stress testing** ada di **`scope-and-safety-guardian`** + **`buru-bug-bounty`** — skill ini menegakkannya lewat jeda dan kondisi berhenti, bukan mengulang larangannya.
- **Bukti pertahanan IP datacenter** (skor IP, trajektori, dsb.) ada di **`buru-bug-bounty`** (riset pola CAPTCHA 23 Nov 18:05) — skill ini memakai pelajarannya (IP datacenter mudah diblokir → pacing lebih hati-hati), bukan mengulang risetnya.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Pacing hanya untuk target yang sudah lolos `scope-and-safety-guardian`.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Pacing ini untuk MENGHINDARI beban berlebih, bukan untuk menyerang ketersediaan. Banjir request = DoS, bukan pengujian.
4. **DILARANG membypass/mengelabui rate-limit atau WAF.** Yang diizinkan di skill ini HANYA: melambat, memberi jeda, backoff, dan BERHENTI saat diblokir. Dilarang: memutar IP/proxy untuk lolos blokir, memalsukan header/identitas untuk lolos WAF, memecah payload untuk mengelabui filter, atau teknik evasion lain. "WAF evasion awareness" di riset artinya SADAR akan WAF dan menghindarinya dengan bersikap sopan — bukan menembusnya. `buru-bug-bounty` juga melarang buang waktu "lewati rate-limit".
5. **Tanpa payload di permukaan publik.** Tanpa uji korban; tanpa laporan tanpa persetujuan Cipta.
6. **Patuhi larangan otomasi program.** huntr "Humans only" → jangan ikut challenge-nya dengan agen AI. **Gray Swan dilewati total** (perintah Cipta 23 Nov 18:35).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Sertakan header identifikasi peneliti** (`X-Bug-Bounty-Researcher: <handle>`) bila program mewajibkannya — jangan menyamar sebagai lalu lintas biasa.
10. **Blokir = BERHENTI, bukan diakali.** Sekali kena 429/403/WAF-block, sesi itu BERHENTI (lihat Gerbang 3). Mencoba lagi dari IP/sesi lain untuk lolos blokir = pelanggaran aturan 4.

## Langkah + gerbang

### Gerbang 1 — Tetapkan anggaran laju sebelum sesi

- Baca batas dari `scope-and-safety-guardian` (default maks **5 permintaan/detik**; bila program mengizinkan lebih, pakai angka program + bukti tertulis aturannya). Tetapkan untuk sesi ini: jeda dasar antar request (minimal **0,2 detik** pada batas 5/detik — dan LEBIH LAMBAT bila target sensitif), total request maksimum sesi, dan jeda antar batch.
- **Standar lulus:** angka laju + jeda dasar + total maksimum tercatat sebelum request pertama. Tanpa angka = GAGAL, jangan mulai.

### Gerbang 2 — Kirim dengan delay + jitter (pola sopan)

- Antar request beri jeda dasar + **jitter acak ±50%** dari jeda dasar (contoh: jeda dasar 1 detik → jeda nyata 0,5–1,5 detik), supaya pola request tidak terlihat seperti mesin berinterval tetap. Jangan kirim batch paralel besar; bila perlu paralel, total laju gabungan tetap di bawah batas Gerbang 1. Catat tiap respons: status HTTP, header `Retry-After` bila ada, dan waktu respons.
- **Standar lulus:** tidak ada dua request berurutan tanpa jeda; laju nyata ≤ batas; log respons tercatat. Satu pelanggaran = HENTIKAN sesi.

### Gerbang 3 — Deteksi blokir + backoff + berhenti

- Tanda kena rate-limit/WAF: **429** (dengan/tanpa `Retry-After`), **403** mendadak setelah sebelumnya 200, halaman challenge/CAPTCHA, respons kosong/timeout berulang, atau pesan "blocked / rate limited". Begitu SATU tanda muncul: **HENTIKAN pengiriman segera**. Tunggu minimal sesuai `Retry-After` (bila ada) atau **minimal 10 menit** (bila tidak ada), lalu coba SATU request uji. Bila masih diblokir → **sesi SELESAI hari itu**: catat blokir di log, laporkan ke Muse, JANGAN pindah IP/sesi untuk mengulang (aturan keras 4 & 10). Bila request uji lolos → lanjut dengan jeda dasar DIGANDAKAN.
- **Standar lulus:** blokir terdeteksi dari respons (bukan dugaan) + jeda backoff ditaati + keputusan lanjut/berhenti tercatat. Mengulang tanpa jeda atau pindah IP = GAGAL + pelanggaran.

### Gerbang 4 — Catat laju + hasil sesi

- Tulis ringkasan sesi ke log (format di bawah): laju yang dipakai, jumlah request, respons blokir (bila ada), dan keputusan akhir.
- **Standar lulus:** ringkasan tertulis; sesi tanpa catatan = belum selesai.

## Alat

- Batas laju program dari `scope-and-safety-guardian` (Gerbang 4) + dokumen program.
- Skrip pengujian (Python/bash) — WAJIB berisi jeda + jitter + penghentian otomatis saat respons 429/403 (A70 yang memastikan).
- Log: `~/workspace/catatan/log-bug-bounty.md` (wajib).

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md`, satu entri per sesi pengujian:

```
## [YYYY-MM-DD HH:MM WIB] Pacing Request — [Program] — [Target] — [Tim]
- Batas laju: [5 req/detik / angka program + sumber]
- Jeda dasar + jitter: [mis. 1 detik ±50%]
- Total request sesi: [jumlah]
- Respons blokir: [tidak ada / 429 jam HH:MM + Retry-After: ... / 403 / CAPTCHA]
- Backoff: [tidak perlu / tunggu ... menit + 1 request uji: LOLOS/BLOKIR]
- Keputusan: LANJUT (jeda digandakan) / SELESAI HARI ITU — [alasan]
```
