# Skill: Cara Kerja Aplikasi Web — Request/Response, Autentikasi, dan Manajemen Sesi sebagai Fondasi Pengujian

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 9 (artikel Cyber Academy "Skill Penting Pentester", No. 3) + batch 23 (ringkasan etis-legal, cara kerja aplikasi & web), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill FONDASI — memahami cara kerja aplikasi web target in-scope sebelum menguji: anatomi request/response HTTP, alur autentikasi, otorisasi, dan siklus hidup sesi. Skill ini BUKAN skill pengujian: tidak ada langkah menyerang di sini — hasilnya adalah PETA alur aplikasi yang dipakai skill pengujian lain sebagai dasar hipotesis.

## Pemicu

Dipakai pada tahap awal perburuan tiap target web in-scope — SETELAH pemetaan permukaan (`pemetaan-permukaan-serangan`) dan SEBELUM pengujian kerentanan apa pun. Dipakai juga saat temuan kandidat perlu dijelaskan lewat alur aplikasinya (mis. "di langkah mana dari alur login celah ini terjadi").

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Memetakan alur aplikasi target dari interaksi akun sendiri; menyusun peta request/response |
| Pengerjaan | **A58 Vulnerability Researcher** | Menandai titik-titik alur yang layak diuji (validasi, auth, sesi) |
| Audit | **A60 Security Auditor** | Memvalidasi peta alur sebelum dipakai sebagai dasar hipotesis |
| Pemimpin | **Muse** | Memutuskan alur mana yang jadi prioritas pengujian |

## Sudah tercakup (jangan diduplikat)

- Pemetaan permukaan serangan → skill `pemetaan-permukaan-serangan`. Skill ini MEMAKAI indeks aset itu dan menambahkan ALUR di atasnya — bukan mengulang enumerasi.
- Manajemen sesi (serangan) → skill `perburuan-manajemen-sesi`. Skill ini menjelaskan SIKLUS HIDUP sesi normal (buat → pakai → perbarui → akhiri) sebagai fondasi — bukan teknik serangannya.
- Otorisasi diferensial → skill `access-control-differential-analyst`. Skill ini menjelaskan MODEL otorisasi aplikasi (peran, izin, batas) sebagai fondasi — bukan teknik pengujiannya.
- Intersepsi traffic (Burp/ZAP) → skill `mcp-burp-*` + `owasp-zap-pengujian-web`. Skill ini memakai hasil intersepsi sebagai bahan peta — bukan mengulang cara memakai tool-nya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pemetaan alur HANYA lewat interaksi akun uji sendiri. Tanpa data orang lain.
3. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
4. **Tanpa DoS/DDoS.** Pemetaan alur memakai request normal secukupnya, patuhi rate limit program.
5. **Tanpa payload di permukaan publik.** Peta alur + hipotesis hanya di log internal dan jalur resmi program.
6. **Tanpa kredensial orang lain.** Jangan memakai sesi/token milik siapa pun untuk memetakan alur.
7. **Validasi human-in-the-loop.** Peta alur harus diperiksa manusia (Muse/A60) sebelum jadi dasar hipotesis.
8. **Tanpa laporan tanpa persetujuan Cipta.** Peta alur ini bahan kerja internal; temuan yang lahir darinya tetap lewat jalur draf → Cipta.
9. **Patuhi larangan otomasi program** — huntr "Humans only"; Gray Swan dilewati total.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai pemahaman alur aplikasi untuk mengakses data/fitur milik orang lain. Pemahaman di sini HANYA untuk merumuskan hipotesis pengujian yang sah atas akun sendiri.

## Langkah + gerbang

### Gerbang 0 — Petakan endpoint + alur utama dari akun sendiri

1. Dengan akun uji sendiri, jalani alur utama aplikasi: daftar/masuk, navigasi fitur kunci, dan keluar. Catat tiap endpoint yang dilewati (URL + metode HTTP) + tujuannya.
2. **Standar lulus:** daftar endpoint alur utama tertulis. Alur tanpa endpoint tercatat = belum terpetakan.

### Gerbang 1 — Bedah request/response tiap langkah

1. Untuk tiap langkah alur, catat: apa yang dikirim klien (parameter, header, body, cookie/token), apa yang dibalas server (status, body, header keamanan, cookie baru). Tandai di mana validasi input, autentikasi, dan otorisasi TERLIHAT terjadi (mis. respons 401/403, pesan error validasi).
2. **Standar lulus:** tiap langkah punya catatan request/response + titik kontrol yang terlihat. Langkah tanpa catatan = belum dibedah.

### Gerbang 2 — Petakan siklus hidup sesi

1. Lacak satu sesi dari awal sampai akhir: bagaimana sesi dibuat (login → token/cookie apa), bagaimana sesi dipakai (apa yang dikirim tiap request), bagaimana sesi diperbarui (refresh/rotasi?), bagaimana sesi diakhiri (logout → apakah token benar-benar mati?). Uji HANYA pada sesi akun sendiri.
2. **Standar lulus:** siklus sesi tertulis (buat → pakai → perbarui → akhiri) + bukti dari sesi sendiri. Siklus yang terputus (mis. tidak tahu cara sesi berakhir) = catat sebagai "belum diketahui".

### Gerbang 3 — Tandai titik uji + serahkan hipotesis

1. Dari peta alur, tandai titik yang layak diuji: input yang tidak tervalidasi dengan jelas, transisi peran (mis. user biasa → admin), pergantian sesi, dan pemanggilan API yang sensitif. Untuk tiap titik, rumuskan hipotesis satu kalimat + skill pengujian yang sesuai.
2. Serahkan hipotesis ke A58/A60 untuk validasi. Skill ini BERHENTI di sini — pengujian mengikuti skill pengujian itu.
3. **Standar lulus:** tiap titik uji punya hipotesis + skill tujuan + validasi A60. Titik tanpa hipotesis = belum bisa dieksekusi.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Satu-satunya akun untuk menjalani alur aplikasi |
| `mcp-burp-*` / `owasp-zap-pengujian-web` | Intersepsi request/response untuk bahan peta (baca saja di tahap ini) |
| `pemetaan-permukaan-serangan` | Indeks aset sebagai dasar peta alur |
| `perburuan-manajemen-sesi` + `access-control-differential-analyst` | Skill pengujian lanjutan untuk titik yang ditandai |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta alur: endpoint, request/response, siklus sesi, titik uji |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Target + program: [nama — program]
Alur utama: [langkah 1 → endpoint ... | langkah 2 → endpoint ...]
Request/response: [langkah ... — dikirim: ... — dibalas: ... — kontrol terlihat: ...]
Siklus sesi: [buat: ... — pakai: ... — perbarui: ... — akhiri: ...]
Titik uji: [titik ... — hipotesis: ... — skill: ...]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa data/sesi orang lain, tanpa serangan di skill ini]
Status: [peta selesai / hipotesis diserahkan]
```

## Batasan yang diketahui

- Peta alur dari luar hanya melihat PERMUKAAN: logika di dalam server (aturan bisnis, validasi server-side yang tidak terlihat) tidak bisa diketahui pasti — tandai asumsi sebagai asumsi.
- Aplikasi berubah: endpoint dan alur bisa berubah tanpa pemberitahuan. Perbarui peta tiap putaran; jangan memakai peta lama tanpa verifikasi ulang.
- Alur yang membutuhkan peran khusus (admin, mitra) tidak bisa dipetakan penuh dari akun uji biasa — catat sebagai "tidak dapat dipetakan dari akun ini", jangan memaksakan akses peran lain.
- Skill ini tidak membahas GraphQL secara mendalam — lihat `introspeksi-graphql` bila target memakai GraphQL. Untuk API REST, peta di skill ini sudah cukup sebagai fondasi.
