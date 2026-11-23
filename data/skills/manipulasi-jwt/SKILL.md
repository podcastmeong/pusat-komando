# Skill: Manipulasi JWT — Pengujian Token JSON Web Token (alg none, Secret Lemah, JWK/JKU, Key Confusion)

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 4 butir 23).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat target memakai JWT (JSON Web Token) sebagai token sesi/autentikasi — terlihat dari token `eyJ...` (header.payload.signature, base64url) di cookie atau header `Authorization: Bearer` — dan perlu dibuktikan apakah server memvalidasi token itu dengan benar. Dipakai setelah sesi multi-peran siap (skill `manajemen-sesi-multi-peran`) supaya ada token Member dan token Admin/pembanding. Jangan dipakai pada token yang bukan JWT (token opaque/session-id acak), dan jangan dipakai untuk memalsukan identitas orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mempelajari + menerapkan teknik JWT di bawah |
| Pengerjaan | **A64 Web Application Tester** | Menguji JWT aplikasi web dengan metode ini |
| Pengerjaan | **A66 API Security Tester** | Menguji JWT API dengan metode ini |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi umum Broken Authentication (token bisa ditebak, sesi tidak kedaluwarsa) → skill `fondasi-kerentanan-web-api` Gerbang 1.4. Skill ini BUKAN definisi itu: skill ini adalah **metodologi manipulasi JWT per teknik** (alg none, secret lemah, JWK/JKU, key confusion) yang tidak ada di skill fondasi.
- Sesi multi-peran + token pembanding (Member vs Admin) → skill `manajemen-sesi-multi-peran`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun uji adalah akun sendiri.** Token yang dimanipulasi adalah token akun uji sendiri; jangan pernah memakai token/kredensial orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan kirim payload.**
11. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
12. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.
13. **Brute-force secret JWT HANYA terhadap secret akun uji sendiri.** Brute-force hanya boleh memakai daftar kata umum terhadap token akun sendiri, dengan laju rendah dan berhenti begitu server menolak berulang (rate-limit). Jangan brute-force secret akun/prod orang lain, jangan menyerang kunci produksi.
14. **Jangan pernah memalsukan identitas orang lain.** Token yang dimodifikasi hanya boleh mengklaim peran/data akun uji sendiri (mis. Member sendiri → klaim `role: admin` pada akun sendiri untuk menguji apakah server percaya klaim itu — buktinya adalah akses baca ke data/fungsi admin, bukan data orang lain). Bila teknik berhasil, JANGAN dipakai untuk membaca/mengubah data pengguna lain.
15. **Jangan menyimpan token utuh di log/skill.** Token dicatat terpotong (`eyJ...[REDACTED]...<4 karakter terakhir signature>`).

## Langkah + gerbang

### Gerbang 1 — Bedah token + catat baseline

1. Ambil token JWT akun Member sendiri (dari cookie/header sesi) dan bedah ketiga bagiannya: header (`alg`, `kid`, `jku`, `x5u`), payload (`sub`, `role`, `exp`, `iss`, `aud`), signature. Catat algoritma dan klaim apa saja yang menentukan hak akses (biasanya `role`, `sub`, `admin`).
2. Tentukan endpoint pembanding yang membedakan peran: satu endpoint baca yang hanya boleh Admin (mis. `/api/admin/users`) + satu endpoint profil (`/me`) untuk memastikan token masih dikenali sebagai siapa.
3. Baseline: panggil kedua endpoint dengan token Member asli — catat status + isi (seharusnya: profil = data Member sendiri; endpoint admin = 401/403).
4. **Standar lulus:** struktur token terbedah + klaim penentu hak akses teridentifikasi + baseline Member tercatat. Token bukan JWT atau klaim hak akses tidak ada di token = STOP, teknik ini tidak berlaku.

### Gerbang 2 — Uji teknik satu per satu (satu teknik = satu putaran)

Uji berurutan; tiap teknik memakai token Member sendiri yang dimodifikasi, lalu dipanggil ke endpoint pembanding dari Gerbang 1. Berhenti dan catat begitu satu teknik terbukti — jangan lanjut menguji teknik lain dengan token palsu yang sudah berhasil.

#### Teknik A — alg: none (hilangkan signature)
Ubah header `alg` menjadi `none`, hapus bagian signature (token jadi `header.payload.`), lalu panggil endpoint pembanding. **Terbukti bila:** server menerima token tanpa signature dan mengembalikan data/aksi yang seharusnya butuh autentikasi.

#### Teknik B — Weak secret brute-forcing (tebak secret HMAC)
Bila `alg` adalah HS256/HS384/HS512, coba tebak secret dengan daftar kata umum (secret lemah seperti `secret`, `password`, nama aplikasi) — hanya terhadap token akun sendiri, laju rendah, berhenti bila server menolak berulang. Tanda-tanda secret lemah: secret bisa ditebak dari repo publik/dokumentasi target sendiri (bukan dari akun orang lain). **Terbukti bila:** secret ditemukan, token baru ditandatangani dengan secret itu (klaim peran diubah pada akun sendiri), dan server menerimanya di endpoint pembanding.

#### Teknik C — JWK/JKU header injection (suntik kunci sendiri)
Bila server membaca kunci dari header (`jku` = URL kunci, `jwk` = kunci di dalam header, `x5u` = URL sertifikat), arahkan ke kunci yang kita kendalikan (server canary milik sendiri, bukan permukaan publik) dan tandatangani token dengan kunci itu. **Terbukti bila:** server mengambil kunci dari URL/kunci yang kita tunjuk dan menerima token yang ditandatangani kunci itu di endpoint pembanding. Jangan arahkan `jku`/`x5u` ke URL publik yang tidak kita kendalikan.

#### Teknik D — Key confusion RS256 → HS256 (kunci publik dipakai sebagai secret HMAC)
Bila `alg` adalah RS256 (asimetris) dan kunci publik server bisa didapat (endpoint `/.well-known/`, dokumentasi, atau respons server), coba tandatangani token dengan `alg: HS256` memakai kunci publik itu sebagai secret HMAC. **Terbukti bila:** server memvalidasi token HS256 dengan kunci publiknya sendiri dan menerima klaim peran yang diubah (pada akun sendiri) di endpoint pembanding.

#### Teknik E — Klaim tidak divalidasi (kedaluwarsa / penerbit / audiens)
Uji satu per satu: token kedaluwarsa (`exp` sudah lewat) — apakah masih diterima? `iss`/`aud` diubah — apakah masih diterima? `kid` diubah ke nilai tak dikenal / path traversal — apakah server error dengan cara yang membocorkan info? **Terbukti bila:** token yang seharusnya ditolak (kedaluwarsa/penerbit salah) tetap diterima di endpoint pembanding.

5. **Standar lulus per teknik:** ada hasil per teknik (diterima/ditolak + status + isi respons endpoint pembanding). Teknik tanpa hasil = belum diuji, jangan diklaim.

### Gerbang 3 — Buktikan dampak dengan peran sendiri (read-only)

1. Untuk teknik yang "diterima" server di Gerbang 2, buktikan dampaknya secara read-only: panggil endpoint baca admin sebagai Member dengan token termanipulasi dan tunjukkan data/fungsi admin benar-benar terbaca (bukan sekadar 200 kosong). Untuk fungsi tulis, JANGAN eksekusi aksi destruktif — cukup buktikan token diterima di endpoint baca, atau pada fungsi tulis non-destruktif terhadap data uji sendiri.
2. Kembalikan klaim ke keadaan semula: jangan tinggalkan token palsu aktif; logout sesi uji setelah pembuktian.
3. **Standar lulus:** ada bukti baca (field admin terbaca, PII disensor) + langkah reproduksi persis. Sekadar "server menerima token" tanpa data/aksi yang terbukti = belum terbukti.

### Gerbang 4 — Serahkan ke skeptic gate

1. Kandidat Temuan diserahkan ke skill `skeptic-false-positive-eliminator`: uji ulang dengan sesi HTTP baru (fresh tokens), pastikan reproduksibel konsisten.
2. Gagal direproduksi = TOLAK, catat di log sebagai bukan temuan.
3. Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim.
4. **Standar lulus:** keputusan akhir tercatat di log dengan pasangan bukti request/response asli (token disensor).

## Alat

| Alat | Cara pakai |
|---|---|
| Token JWT akun uji sendiri (Member + Admin bila tersedia) | Satu-satunya token yang dimanipulasi; semuanya milik sendiri. |
| Pembedah JWT (decoder base64url / pustaka JWT lokal) | Membaca header + payload tanpa mengirim apa pun ke server. |
| Daftar kata umum untuk secret lemah | Hanya untuk Teknik B, hanya terhadap token akun sendiri, laju rendah. |
| Server canary milik sendiri | Hanya untuk Teknik C (host kunci JWK/JKU yang kita kendalikan); bukan permukaan publik. |
| Kunci publik server (bila dipublikasikan target sendiri) | Hanya untuk Teknik D; diambil dari sumber resmi target. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap teknik: token terbedah (disensor), hasil, bukti dampak, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint pembanding]
Token baseline: [alg + klaim penentu hak akses + exp/iss/aud — token disensor]
Teknik A (alg none): [diterima/ditolak + status + isi]
Teknik B (weak secret): [diterima/ditolak + secret ditemukan? + status — JANGAN tulis secret utuh bila itu secret produksi; bila secret akun uji sendiri, tulis "ditemukan (disensor)"]
Teknik C (JWK/JKU injection): [diterima/ditolak + status]
Teknik D (key confusion RS256→HS256): [diterima/ditolak + status]
Teknik E (klaim tidak divalidasi): [kedaluwarsa/iss/aud: diterima/ditolak + status]
Pembuktian dampak (read-only): [field admin terbaca / aksi non-destruktif + bukti, PII disensor]
Keputusan: [maju ke skeptic gate / Aman-bukan temuan / ditolak + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini hanya untuk JWT; token opaque/session-id tidak tercakup — untuk itu pakai skill `fondasi-kerentanan-web-api` (Broken Authentication) dan `manajemen-sesi-multi-peran`.
- Teknik B (brute-force secret) hanya bermakna bila secret memang lemah; secret kuat yang tidak bisa ditebak = Aman untuk teknik itu, bukan kegagalan pengujian — catat sebagai Aman.
- Teknik C butuh server yang benar-benar membaca `jku`/`jwk`/`x5u` dari header; kebanyakan server modern mengabaikannya — hasil "ditolak/diabaikan" adalah hasil valid, catat sebagai Aman.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome, bukan trik token klasik — gunakan skill ini sebagai fondasi penilaian, bukan sebagai daftar target program AI.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
