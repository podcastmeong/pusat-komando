# Skill: Pengujian BFLA — Akses Fungsi/Endpoint Khusus Admin dengan Token Pengguna Biasa

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 4 butir 22).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada endpoint/fungsi yang seharusnya hanya untuk peran tinggi (Admin/Moderator) — mis. `/api/admin/users`, `/api/admin/settings`, hapus/ubah peran pengguna, lihat daftar pengguna, ubah konfigurasi — dan perlu dibuktikan apakah token pengguna biasa (Member) atau anonim (Guest) bisa memakainya. Dipakai setelah sesi multi-peran siap (skill `manajemen-sesi-multi-peran`) dan setelah recon mengindeksasi endpoint (skill `pemetaan-permukaan-serangan`). Bedanya dengan BOLA/IDOR: BFLA menguji **fungsi** (apakah peran boleh memanggil fungsi itu sama sekali), bukan **objek** (apakah peran boleh mengakses objek milik orang lain) — pembuktian objek tetap di skill `access-control-differential-analyst`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan pengujian BFLA per endpoint |
| Pengerjaan | **A64 Web Application Tester** | Menguji endpoint admin aplikasi web dengan metode ini |
| Pengerjaan | **A66 API Security Tester** | Menguji endpoint admin API dengan metode ini |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian memenuhi standar lulus sebelum maju ke triase |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- BOLA/IDOR (akses objek milik akun lain) → skill `access-control-differential-analyst` (BFLA di sini hanya fungsi/peran, bukan objek).
- Definisi umum "endpoint admin bisa diakses pengguna biasa" → skill `fondasi-kerentanan-web-api` Gerbang 1.5 (salah konfigurasi API). Skill ini BUKAN definisi itu: skill ini adalah **metodologi pengujian fungsi per peran** (inventaris fungsi admin → uji lintas peran → bukti aksi nyata) yang tidak ada di skill fondasi.
- Sesi multi-peran (Admin/Member/Guest) → skill `manajemen-sesi-multi-peran`.
- Validasi scope program sebelum pengujian → skill `scope-and-safety-guardian`.
- Filter akhir false positive + reproduksibilitas sesi bersih → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu — semua akun uji adalah akun sendiri.** Admin, Member, dan Guest semuanya milik sendiri; jangan pernah memakai akun/kredensial orang lain.
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
13. **Fungsi destruktif TIDAK BOLEH dieksekusi untuk pembuktian.** Bila fungsi admin itu destruktif (hapus pengguna, ubah peran pengguna lain, ubah konfigurasi produksi), JANGAN menjalankannya — catat sebagai "indikasi kuat, butuh validasi manusia" dan serahkan ke A60 + Cipta. Pembuktian BFLA di skill ini hanya untuk fungsi baca (GET/daftar/lihat) dan fungsi tulis non-destruktif terhadap data uji sendiri.
14. **200 OK bukan bukti.** Respons sukses tanpa perubahan status nyata di server = bukan temuan.

## Langkah + gerbang

### Gerbang 1 — Inventarisasi fungsi khusus peran tinggi

1. Dari indeks recon (skill `pemetaan-permukaan-serangan`) + matriks hak akses (skill `manajemen-sesi-multi-peran`), daftarkan fungsi/endpoint yang seharusnya hanya untuk Admin/Moderator: pola URL (`/admin/`, `/api/admin/`, `/manage/`), endpoint yang tidak muncul di UI pengguna biasa, dan fungsi yang disebut di dokumentasi sebagai "admin only".
2. Untuk tiap fungsi catat: metode HTTP, parameter, apakah fungsi baca (GET) atau tulis (POST/PUT/PATCH/DELETE), dan apakah destruktif (Gerbang: fungsi destruktif ditandai dan TIDAK diuji eksekusinya — lihat Aturan keras 13).
3. **Standar lulus:** daftar fungsi admin tercatat dari indeks recon/dokumentasi + tiap fungsi berlabel baca/tulis/destruktif. Fungsi yang dikarang atau ditebak = STOP, jangan diuji.

### Gerbang 2 — Baseline peran: apa yang seharusnya terjadi

1. Untuk tiap fungsi, panggil sebagai Admin (bila akun admin uji tersedia) untuk memastikan fungsi itu ada dan respons pemilik sah seperti apa; panggil sebagai Guest/anonim untuk memastikan mana yang memang publik.
2. Catat respons yang diharapkan dari Member bila kontrol benar: 401/403/404.
3. **Standar lulus:** baseline Admin (bila tersedia) + Guest tercatat per fungsi, dengan raw request/response tersimpan. Tanpa baseline, hasil Member tidak bisa dinilai.

### Gerbang 3 — Uji fungsi sebagai Member (pengguna biasa)

1. Panggil tiap fungsi non-destruktif sebagai Member (token akun Member sendiri), dengan parameter yang sama seperti baseline. Untuk fungsi tulis, operasikan HANYA pada data uji milik sendiri (mis. ubah pengaturan akun Member sendiri lewat endpoint admin — bukan pengaturan orang lain).
2. Klasifikasikan hasil:
   - **Kandidat Temuan:** Member mendapat data/aksi admin yang tidak bisa didapat lewat UI normal dengan peran Member — mis. daftar pengguna lain terbaca, pengaturan admin terbaca, aksi admin berhasil terhadap data uji sendiri.
   - **Aman:** 401/403/404, atau respons sama dengan yang sudah publik di Guest.
   - **Bukan temuan:** 200 tapi isinya data publik / data milik Member sendiri / pesan error generik tanpa data.
3. **Standar lulus:** tiap fungsi punya klasifikasi + nama field/bukti yang membuktikan (PII disensor `[REDACTED]`). Klasifikasi tanpa bukti field = belum terbukti.

### Gerbang 4 — State Verification (untuk fungsi tulis)

1. Untuk fungsi tulis yang lolos Gerbang 3 sebagai Kandidat Temuan: baca ulang state yang diubah dari sesi Admin/pemilik (sesi bersih) dan periksa apakah perubahan itu NYATA terjadi di server.
2. **Perubahan nyata = Kandidat Temuan** (lanjut ke Gerbang 5). **Pesan sukses tapi data tidak berubah (silent drop) = Aman** — server hanya mengembalikan pesan sukses palsu; catat sebagai bukan temuan, jangan laporkan.
3. Bila perubahan ternyata terjadi, kembalikan data ke keadaan semula dari akun pemiliknya (jangan tinggalkan data uji berubah).
4. **Standar lulus:** ada bukti baca-ulang yang menunjukkan status sebelum vs sesudah. Tanpa baca-ulang = belum terbukti, jangan klaim temuan tulis.

### Gerbang 5 — Serahkan ke skeptic gate

1. Kandidat Temuan diserahkan ke skill `skeptic-false-positive-eliminator`: uji ulang dengan sesi HTTP baru (fresh tokens), pastikan reproduksibel konsisten.
2. Gagal direproduksi = TOLAK, catat di log sebagai bukan temuan.
3. Lolos = draf laporan via `triase-duplikat` + `laporan-abstrak` → A60 audit → Cipta setuju → kirim.
4. **Standar lulus:** keputusan akhir tercatat di log dengan pasangan bukti request/response asli (token dan PII disensor).

## Alat

| Alat | Cara pakai |
|---|---|
| Sesi multi-peran (skill `manajemen-sesi-multi-peran`) | Admin (bila tersedia), Member, Guest — semuanya akun sendiri, wadah sesi terpisah. |
| Indeks recon (skill `pemetaan-permukaan-serangan`) | Satu-satunya sumber endpoint/fungsi yang boleh diuji. |
| Matriks hak akses | Dari skill `manajemen-sesi-multi-peran` Gerbang 3 — acuan "seharusnya" per peran. |
| Sesi HTTP bersih (fresh tokens) | Untuk uji ulang reproduksibilitas di Gerbang 5. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap fungsi: baseline peran, hasil Member, verifikasi state, keputusan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Endpoint/fungsi: [metode + URL + peran yang seharusnya]
Jenis fungsi: [baca / tulis non-destruktif / destruktif — destruktif TIDAK diuji eksekusinya]
Baseline Admin: [status + ringkasan, bila akun admin uji tersedia; bila tidak: "tidak tersedia"]
Baseline Guest (anonim): [status + ringkasan]
Uji Member: [status + ringkasan field/aksi yang didapat]
Hasil: [Kandidat Temuan / Aman / Bukan temuan + field yang membuktikan, PII disensor]
Verifikasi state: [tidak berlaku (uji baca) / perubahan NYATA / silent drop + bukti baca-ulang]
Keputusan: [maju ke skeptic gate / Aman-bukan temuan / ditolak / indikasi kuat-butuh validasi manusia + alasan]
Status: [diuji / kandidat / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Skill ini menguji fungsi/peran (BFLA), bukan objek (BOLA/IDOR) — bila satu endpoint gagal di kedua dimensi, pisahkan pembuktiannya: objek di `access-control-differential-analyst`, fungsi di sini.
- Fungsi destruktif tidak bisa dibuktikan tuntas dengan metode aman skill ini — hasilnya mentok di "indikasi kuat" sampai manusia (A60 + Cipta) memutuskan validasi lanjut; jangan pernah mengeksekusi fungsi destruktif demi kelengkapan bukti.
- Bila akun Admin uji tidak tersedia, baseline Admin kosong — keputusan tetap bisa diambil dari perbandingan Member vs Guest + dokumentasi, tapi catat keterbatasan itu di log.
- Skill ini belum diuji pada kasus nyata — label BELUM DIUJI di atas berlaku sampai satu kasus lolos triase.
