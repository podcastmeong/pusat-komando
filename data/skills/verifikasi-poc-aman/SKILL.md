# Skill: Verifikasi PoC Aman — Bukti Tanpa False Positive, Tanpa Merusak

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 7 butir 45 — Zero False-Positive PoC Verification).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu bukti aman per jenis yang lolos gerbang skeptic dan dicatat di log.
>
> Hubungan dengan skill lain: gerbang PENILAIAN zero-FP sudah ada di `skeptic-false-positive-eliminator` (4 gerbang: reproduksibilitas, filter non-security, dampak bisnis, output terstruktur). Skill ini adalah KATALOG CARA membuktikan — teknik bukti aman per jenis kerentanan — yang MENGISI gerbang 1 skeptic dengan bukti, bukan menggantikannya. Tanpa skill ini, butir 45 hanya punya gerbang tanpa teknik buktinya: tidak ada satu pun skill yang menyebut `document.domain` atau DNS callback (dicek 23 Nov 2026, nol hasil di 113 skill).

## Pemicu (kapan dipakai)

Dipakai setiap kali sebuah hipotesis celah harus DIBUKTIKAN sebelum maju ke skeptic/triase — untuk memilih teknik bukti yang aman untuk jenis celah itu, menjalankannya, dan menyimpan buktinya. Dipakai sesudah hipotesis punya label jenis (`fondasi-kerentanan-web-api` / `perburuan-kerentanan-spesifik`) dan sebelum draf laporan dibuat. Satu hipotesis = satu teknik bukti dari katalog di bawah.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Memilih teknik bukti yang aman untuk jenis celah, menjalankannya, menyimpan bukti |
| Audit | **A60 Security Auditor** | Memeriksa bukti lewat `skeptic-false-positive-eliminator` (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan bukti mana yang cukup untuk maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Gerbang penilaian zero-FP (reproduksibilitas bersih, baseline anonim, filter non-security, dampak bisnis) → `skeptic-false-positive-eliminator` — skill ini mengisi gerbang itu dengan bukti, bukan mengulang penilaiannya.
- Standar lulus per jenis kerentanan (apa yang dihitung sebagai bukti) → `fondasi-kerentanan-web-api` + `perburuan-kerentanan-spesifik`.
- Cek duplikat + skor → `triase-duplikat`.

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
11. **Tanpa aksi destruktif — pembuktian harus aman dan read-only.** Bukti yang diizinkan: bukti baca, callback canary, `document.domain`. DILARANG: DROP, DELETE, hapus data, ubah data orang lain, atau perintah yang menulis/menghapus di server.
12. **Bukti tidak boleh mencuri data.** Jangan membaca isi layanan internal, jangan mengunduh data pengguna lain, jangan mengirim cookie/token ke mana pun. Callback canary hanya membuktikan server MENGHUBUNGI alamat itu — isinya tidak diambil.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Pilih teknik bukti dari katalog

Pilih SATU teknik sesuai jenis celah. Jangan memakai teknik jenis lain, jangan memakai payload "bukti" yang lebih kuat dari yang dibutuhkan.

| Jenis celah | Teknik bukti aman | Yang dibuktikan | Yang DILARANG |
|---|---|---|---|
| XSS (reflected/stored/DOM) | Cetak `document.domain` saja (mis. payload yang menampilkan domain halaman) di headless browser / sesi akun kedua milik sendiri | Skrip benar-benar mengeksekusi di konteks halaman itu | Mencuri cookie/token, mengirim data ke server luar, `alert` yang memicu aksi |
| SSRF (blind maupun tidak) | Panggil DNS/HTTP callback canary milik sendiri (Interactsh / server canary sendiri); catat hit-nya saja | Server benar-benar menghubungi URL yang diminta | Meminta `169.254.169.254` (metadata cloud) untuk DIBACA isinya, memanggil layanan internal dan mengambil isinya |
| SQLi / NoSQLi (blind) | Respons boolean/time-based pada data canary milik sendiri; sleep/delay minimal yang masih terukur | Query benar-benar dieksekusi dengan logika penyerang | `DROP`, `DELETE`, `UPDATE` data, membaca tabel pengguna lain |
| SSTI / RCE (dugaan) | Cetak penanda aritmetika / string statis (mis. `7*7` → `49`) — tanpa perintah OS | Template/perintah benar-benar dievaluasi server | Perintah OS apa pun (`id`, `whoami`, baca file), apalagi yang menulis/menghapus |
| IDOR / BOLA / BFLA | Minta objek milik akun B memakai sesi akun A (keduanya milik sendiri); simpan respons yang disensor | Objek orang lain terbaca/diubah tanpa otorisasi | Memakai objek milik pengguna asli mana pun |
| Open Redirect / OAuth | Callback canary milik sendiri sebagai `redirect_uri`; tunjukkan kode/token tiba di canary | Alamat redirect tidak divalidasi | Menukar kode jadi sesi akun orang lain |

**Standar lulus:** teknik yang dipilih ada di katalog di atas dan cocok dengan jenis celahnya. Teknik di luar katalog = jangan jalankan sebelum disetujui Muse.

### Gerbang 2 — Jalankan bukti sekali, dari sesi bersih

1. Jalankan teknik bukti dari sesi HTTP baru + token segar (bukan sesi penemuan pertama).
2. Simpan pasangan Request/Response asli + tangkapan layar/log canary, dengan token dan PII disensor jadi `[REDACTED]` SEBELUM disimpan.
3. **Standar lulus:** bukti berasal dari sesi bersih dan tersimpan dengan sensor PII. Bukti dari sesi penemuan saja = belum cukup (lihat gerbang 1 skeptic).

### Gerbang 3 — Ulangi, lalu serahkan ke skeptic

1. Ulangi Gerbang 2 minimal 1 kali lagi dari sesi bersih yang berbeda. Bukti yang hanya berhasil sekali = belum terbukti.
2. Serahkan bukti ke A60 (`skeptic-false-positive-eliminator`): reproduksibilitas → filter non-security → dampak bisnis → output terstruktur.
3. **Standar lulus:** skeptic memberi verdict VERIFIED dengan reference ID bukti. TOLAK dari skeptic = kembali ke riset, bukan memperbaiki verdict.

## Alat

| Alat | Cara pakai |
|---|---|
| Headless browser (sesi bersih) | Menjalankan bukti XSS (`document.domain`) di sesi akun kedua milik sendiri |
| Server canary sendiri (Interactsh / canary milik sendiri) | Menerima DNS/HTTP callback untuk SSRF, Open Redirect, OAuth — catat hit-nya saja, jangan ambil isinya |
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai dalam semua pengujian |
| Penyimpanan bukti (file per kandidat, reference ID mis. `FP-2026-11-23-001`) | Bukti HTTP disimpan di luar memori LLM; LLM hanya menerima reference ID saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log teknik bukti + reference ID + verdict skeptic |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Jenis celah: [XSS / SSRF / SQLi / SSTI / IDOR / Open Redirect / OAuth]
Teknik bukti: [dari katalog Gerbang 1]
Bukti: [reference ID FP-... + apa yang tercatat: document.domain / hit canary / respons]
Ulangi ke-2: [berhasil/gagal — sesi bersih]
Verdict skeptic: [VERIFIED / TOLAK + alasan]
Status: [terbukti / ditolak]
```

## Batasan yang diketahui

- Katalog ini hanya berisi teknik bukti yang aman dan read-only; celah yang hanya bisa dibuktikan dengan aksi destruktif atau baca data orang lain = TIDAK BISA dibuktikan dengan skill ini — laporkan sebagai tidak terbukti, jangan cari jalan pintas.
- `document.domain` membuktikan eksekusi, bukan dampak pencurian — dampak bisnis tetap dinilai skeptic di gerbang 3.
- Callback canary membuktikan koneksi keluar, bukan isi layanan internal — jangan klaim lebih dari yang terbukti.
