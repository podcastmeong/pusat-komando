# Skill: Perburuan Clickjacking — Pengujian UI Redressing via X-Frame-Options / CSP frame-ancestors

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 42, sumber: Claude-BugHunter `hunt-clickjacking`, 6 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target punya halaman dengan aksi sensitif (hapus akun, ganti email/kata sandi, transfer, setujui pembayaran, ubah pengaturan keamanan) yang dimuat lewat GET tanpa token anti-CSRF yang terikat aksi.
- Ada sinyal: respons halaman tidak mengirim `X-Frame-Options` maupun CSP `frame-ancestors`, atau salah satunya bernilai longgar (`ALLOW-FROM` domain lain, `frame-ancestors *`).
- Dipakai untuk membuktikan halaman BISA di-frame, bukan untuk menjebak pengguna sungguhan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memeriksa header framing + membangun PoC framing yang aman |
| Audit | **A60 Security Auditor** | Memeriksa apakah PoC + dampak memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Tidak ada skill clickjacking/UI-redressing di daftar yang ada — kandidat murni baru. Sebutan clickjacking di skill lain hanya: daftar noise di `gerbang-tujuh-pertanyaan-triase` (clickjacking pada halaman non-sensitif = ditolak) dan `daftar-tolak-selalu`, serta batas teknis di `analisis-postmessage` (bila target tidak bisa di-frame, pembuktian lintas-origin lewat iframe tidak bisa jalan). Ketiganya TIDAK mengajarkan cara menguji dan membuktikan clickjacking.
- CSRF (tidak adanya token anti-CSRF / cookie SameSite lemah) → skill `deteksi-csrf`. Clickjacking berbeda: ini soal halaman yang bisa di-frame, bukan soal request yang bisa dipalsukan — walau keduanya bisa dirangkai.
- XSS via output yang dirender → skill `output-tidak-aman` dan `verifikasi-xss`.
- Analisis PostMessage lintas-origin → skill `analisis-postmessage`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh halaman yang diuji berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri. Jangan pernah menguji clickjacking terhadap sesi/akun orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.** PoC framing HANYA di-host di lingkungan uji sendiri (file lokal / server canary milik sendiri), JANGAN di-host di permukaan publik dan JANGAN dibagikan tautannya ke siapa pun kecuali ke A60/Muse/Cipta sebagai bukti.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

### PAGAR KHUSUS — pembuktian dampak clickjacking (bagian dari Aturan keras)

- **Pembuktian dampak HANYA dengan PoC framing yang aman pada halaman uji sendiri.** PoC hanya memuat iframe halaman target dalam sesi AKUN UJI SENDIRI, dengan tombol umpan yang bila diklik hanya memicu aksi yang TIDAK merusak pada akun uji sendiri (mis. klik tombol yang membuka dialog konfirmasi, atau aksi yang bisa dibatalkan).
- **Jangan pernah menyelesaikan aksi destruktif lewat PoC.** Bila tombol yang di-frame adalah aksi destruktif (hapus akun, transfer dana, ganti kata sandi), pembuktian BERHENTI pada: iframe termuat + tombol sensitif terlihat/terjangkau di posisi umpan + klik uji TIDAK diselesaikan (atau diselesaikan hanya bila aksinya aman dan bisa dibatalkan pada akun uji sendiri). Tulis di log: "klik tidak diselesaikan — aksi destruktif".
- **Jangan libatkan browser/korban lain.** Tidak ada pengguna sungguhan yang diarahkan ke PoC; tidak ada tautan PoC yang disebar.

## Langkah + gerbang

### Gerbang 1 — Periksa header framing + petakan halaman sensitif

1. **Periksa header tiap halaman sensitif:** kirim GET ke halaman aksi sensitif (dalam sesi akun uji sendiri) dan catat `X-Frame-Options` dan CSP `frame-ancestors`. Catat juga bila halaman memakai `Content-Security-Policy` tanpa `frame-ancestors`.
2. **Petakan halaman sensitif:** halaman dengan tombol/aksi berdampak (hapus, ganti email/kata sandi, transfer, setujui, ubah pengaturan keamanan). Halaman tanpa aksi berdampak = bukan kandidat (lihat `gerbang-tujuh-pertanyaan-triase` — clickjacking non-sensitif ditolak).
3. **Standar lulus:** daftar halaman sensitif + nilai header framing tiap halaman tercatat. Semua halaman sensitif sudah terlindungi (`DENY`/`SAMEORIGIN`/`frame-ancestors 'self'`) = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji framing + bangun PoC aman (satu halaman = satu putaran)

1. **Uji framing minimal:** buat file HTML lokal (bukan publik) berisi `<iframe src="https://target/halaman-sensitif">` lalu buka di browser sendiri dalam sesi akun uji sendiri. **Terbukti bisa di-frame bila:** halaman termuat di dalam iframe tanpa diblokir browser.
2. **Bangun PoC aman:** tambahkan lapisan umpan di atas iframe (tombol palsu "Klaim Hadiah" yang posisinya tepat di atas tombol sensitif target, iframe dibuat transparan). Klik umpan dalam sesi akun uji sendiri.
3. **Uji varian header:** bila `X-Frame-Options: ALLOW-FROM` dipakai, uji apakah origin lain tetap bisa mem-frame; bila CSP `frame-ancestors` memakai wildcard/`https:` longgar, uji dari origin canary milik sendiri.
4. **Standar lulus tiap halaman:** iframe termuat + tombol sensitif terjangkau di posisi umpan. Bila browser memblokir framing = aman, catat dan tutup halaman itu.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** halaman dengan AKSI SENSITIF terbukti bisa di-frame DAN tombol aksinya bisa diposisikan di bawah umpan (PoC aman). **TOLAK** = halaman bisa di-frame tapi tidak ada aksi sensitif di dalamnya (clickjacking non-sensitif), atau framing diblokir browser.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi uji framing minimal 2× (sesi baru + browser bersih). Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** screenshot PoC memakai akun uji sendiri (nama/email disensor bila terlihat); file PoC disimpan di lingkungan uji sendiri dan TIDAK di-host publik; tautan PoC tidak disebar. Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib; semua pengujian dalam sesi akun uji sendiri. |
| File HTML lokal (PoC framing) | Hanya di mesin sendiri / server canary milik sendiri; jangan host publik. |
| Browser sendiri + proxy HTTP | Memeriksa header framing + memuat PoC; simpan raw response header. |
| `~/workspace/catatan/log-bug-bounty.md` | Log header framing per halaman + hasil PoC + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + halaman sensitif]
Header framing: [X-Frame-Options: ...] | [CSP frame-ancestors: ...]
Aksi sensitif di halaman: [hapus akun / ganti email / transfer / ...]
PoC: [iframe termuat: ya/tidak] | [tombol sensitif terjangkau di posisi umpan: ya/tidak] | [klik diselesaikan: tidak — aksi destruktif / ya — aksi aman dan bisa dibatalkan]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Halaman] - Tidak ada perlindungan framing memungkinkan clickjacking pada [aksi sensitif]`. Isi laporan: Ringkasan (header yang hilang + aksi yang bisa dibajak); Langkah Reproduksi (PoC lokal, akun uji sendiri, screenshot disensor); Rekomendasi Perbaikan (kirim `X-Frame-Options: DENY` atau `SAMEORIGIN` + CSP `frame-ancestors 'self'`, dan tambahkan token anti-CSRF yang terikat aksi).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-clickjacking`, 6 laporan), bukan pengalaman teruji — tiap halaman butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Clickjacking pada halaman non-sensitif hampir selalu ditolak program (lihat `gerbang-tujuh-pertanyaan-triase` + `daftar-tolak-selalu`) — jangan buang waktu membuktikan framing pada halaman tanpa aksi berdampak.
- Perlindungan framing yang benar (`DENY`/`SAMEORIGIN`/`frame-ancestors 'self'`) membuat halaman tidak bisa diuji lewat iframe — itu hasil "aman", bukan kegagalan.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan clickjacking.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila halaman sensitif juga tanpa token anti-CSRF, rangkai dengan `deteksi-csrf` (dua vektor, satu aksi).
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
