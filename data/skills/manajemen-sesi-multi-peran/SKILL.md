# Skill: Manajemen Sesi Multi-Peran — Kelola Akun Admin, Member & Guest Sekaligus untuk Perbandingan Hak Akses

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 4 butir 20).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai sebelum pengujian kontrol akses apa pun (BOLA/IDOR, BFLA, JWT, OAuth) pada program web/API klasik: saat target punya lebih dari satu peran (Admin, Member, Guest/anonim) dan pengujian butuh membandingkan apa yang boleh dilakukan tiap peran pada endpoint/fitur yang sama. Skill ini adalah **prasyarat operasional** — sesi multi-peran disiapkan dulu di sini, baru skill pengujian (`access-control-differential-analyst`, `pengujian-bfla`, `manipulasi-jwt`) yang memakai sesi-sesi itu. Jangan dipakai untuk membuat akun orang lain, dan jangan dipakai di luar program bounty resmi in-scope.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menyiapkan + memelihara inventaris sesi multi-peran |
| Pengerjaan | **A64 Web Application Tester** | Memakai sesi multi-peran untuk pengujian aplikasi web |
| Pengerjaan | **A66 API Security Tester** | Memakai sesi multi-peran untuk pengujian API |
| Audit | **A60 Security Auditor** | Memeriksa isolasi sesi + kebersihan token sebelum pengujian maju |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pembuktian BOLA/IDOR dengan baseline 3 kondisi → skill `access-control-differential-analyst` (skill ini hanya MENYIAPKAN sesinya; pembuktian diferensial tetap di sana).
- Pembuktian BFLA (endpoint admin diakses peran biasa) → skill `pengujian-bfla`.
- Manipulasi token JWT → skill `manipulasi-jwt`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun uji adalah akun sendiri.** Admin, Member, dan Guest semuanya akun milik sendiri yang dibuat untuk pengujian; jangan pernah memakai akun/kredensial orang lain.
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
13. **Jangan pernah menyimpan kata sandi atau token utuh di log/skill.** Token dicatat hanya sebagai sidik (`[TOKEN_REDACTED: <4 karakter terakhir>]`); kata sandi tidak pernah ditulis di mana pun.
14. **Satu peran = satu wadah sesi terpisah.** Jangan campur cookie/token antar peran dalam satu profil browser atau satu header HTTP.

## Langkah + gerbang

### Gerbang 1 — Daftarkan peran + buat akun uji sendiri

1. Baca dokumentasi/UI target dan daftarkan peran yang ada: Admin, Member (pengguna biasa), Guest/anonim, plus peran khusus bila ada (Moderator, Penjual, dsb.). Untuk tiap peran catat: cara mendapatkannya (registrasi sendiri / undangan / dibuat admin) dan apa yang seharusnya boleh dilakukan peran itu menurut dokumentasi.
2. Buat akun uji sendiri untuk tiap peran yang bisa dibuat sendiri. Bila peran Admin tidak bisa dibuat sendiri (butuh undangan admin asli), catat sebagai **peran tidak tersedia** — jangan meminjam atau merebut akun admin orang lain; pengujian BFLA tetap bisa jalan dengan membandingkan Member vs Guest dan menguji endpoint admin dari sisi Member (lihat skill `pengujian-bfla`).
3. Beri tiap akun uji nama yang jelas (`test_admin_1`, `test_member_1`, `test_member_2`, `test_guest`) dan data canary palsu yang unik per akun (mis. nama/email canary berbeda) supaya kebocoran antar akun bisa dibuktikan dari isi respons.
4. **Standar lulus:** matriks peran tercatat (peran × cara dapat × hak yang seharusnya) + tiap akun uji yang tersedia adalah milik sendiri + canary per akun berbeda. Akun yang bukan milik sendiri = STOP.

### Gerbang 2 — Siapkan wadah sesi terpisah per peran

1. Untuk tiap peran, siapkan wadah sesi yang terisolasi: profil browser terpisah, container/tab terpisah, atau klien HTTP terpisah dengan cookie jar sendiri. Jangan pernah memakai satu profil browser untuk dua peran bergantian tanpa membersihkan cookie/token di antaranya.
2. Login tiap peran di wadahnya masing-masing dan simpan penanda sesi: jenis token (cookie sesi / JWT / Bearer), masa berlaku, dan cara refresh-nya (bila ada).
3. Uji isolasi: minta endpoint profil (`/me`, `/api/profile`, atau sejenis) dari tiap wadah dan pastikan responsnya cocok dengan peran wadah itu (Admin melihat profil admin, Member melihat profil member). Bila satu wadah mengembalikan profil peran lain, sesi tercampur — bersihkan semua wadah dan ulangi.
4. **Standar lulus:** tiap wadah mengembalikan profil perannya sendiri + tidak ada token yang dipakai di dua wadah. Isolasi gagal = STOP, jangan lanjut ke pengujian.

### Gerbang 3 — Buat matriks hak akses (peran × endpoint/fitur)

1. Dari indeks recon (skill `pemetaan-permukaan-serangan`), daftarkan endpoint/fitur yang akan diuji dan tandai hak yang seharusnya per peran: boleh baca / boleh tulis / tidak boleh (menurut dokumentasi/UI).
2. Untuk tiap sel matriks yang "tidak boleh", catat juga respons yang diharapkan bila kontrol benar (401/403/404).
3. **Standar lulus:** matriks tertulis sebelum satu pun pengujian kontrol akses dimulai. Pengujian tanpa matriks = menebak-nebak, jangan jalan.

### Gerbang 4 — Pelihara sesi selama pengujian

1. Sebelum tiap batch pengujian, periksa tiap sesi masih hidup (panggil endpoint profil; bila 401, login ulang di wadahnya dan catat waktu refresh). Jangan memakai token kedaluwarsa lalu menyimpulkan "403 = aman" — token mati dan akses ditolak adalah dua hal berbeda.
2. Bila satu peran logout sendiri / sesi dicabut server setelah pengujian peran lain (mis. ganti kata sandi), catat dan siapkan ulang sesi itu sebelum melanjutkan.
3. Setelah pengujian selesai, logout semua sesi uji dan hapus token dari wadah (jangan tinggalkan sesi aktif).
4. **Standar lulus:** log sesi mencatat waktu login/refresh tiap peran + tidak ada kesimpulan yang diambil dari token kedaluwarsa. Kesimpulan dari sesi mati = batal, uji ulang dengan sesi hidup.

### Gerbang 5 — Serahkan sesi ke skill pengujian

1. Skill pengujian (`access-control-differential-analyst`, `pengujian-bfla`) memakai wadah sesi dari Gerbang 2 dan matriks dari Gerbang 3 apa adanya — tidak membuat sesi baru sendiri.
2. Bila skill pengujian menemukan kandidat temuan, uji ulang dengan sesi segar (login ulang di wadah bersih) sesuai skill `skeptic-false-positive-eliminator` sebelum maju ke triase.
3. **Standar lulus:** kandidat temuan direproduksi dengan sesi segar + matriks hak akses terlampir di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri per peran (Admin, Member, Guest, + peran khusus) | Satu-satunya akun yang dipakai; semuanya milik sendiri. |
| Profil browser / container / cookie jar terpisah per peran | Isolasi sesi; satu peran tidak pernah berbagi cookie/token dengan peran lain. |
| Canary palsu unik per akun | Data penanda milik sendiri untuk membuktikan kebocoran antar akun dari isi respons. |
| Indeks recon (skill `pemetaan-permukaan-serangan`) | Satu-satunya sumber endpoint/fitur untuk matriks hak akses. |
| `~/workspace/catatan/log-bug-bounty.md` | Log matriks peran, status sesi, dan hasil isolasi. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi]
Matriks peran: [Admin: cara dapat + hak seharusnya; Member: ...; Guest: ...; peran khusus: ...]
Akun uji: [test_admin_1 / test_member_1 / test_member_2 / test_guest — semuanya milik sendiri]
Isolasi sesi: [LOLOS/GAGAL + bukti endpoint profil per wadah]
Matriks hak akses: [endpoint/fitur × peran: boleh baca / boleh tulis / tidak boleh + respons yang diharapkan]
Status sesi: [tiap peran: hidup sejak HH:MM / refresh terakhir HH:MM / logout setelah selesai]
Keputusan: [siap dipakai skill pengujian / STOP + alasan]
```

## Batasan yang diketahui

- Peran Admin sering tidak bisa dibuat sendiri; bila begitu, pengujian BFLA terbatas pada apa yang bisa dibuktikan dari sisi Member/Guest — jangan memaksakan akses admin dengan akun orang lain.
- Skill ini hanya mengelola sesi dan matriks; skill ini sendiri TIDAK membuktikan kerentanan apa pun — pembuktian ada di skill pengujian masing-masing.
- Bila target memakai SSO pihak ketiga untuk login, sesi peran terikat pada akun IdP masing-masing — siapkan akun IdP uji sendiri per peran juga (metode OAuth/SSO ada di skill `perburuan-kerentanan-spesifik` Gerbang 1.3).
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
