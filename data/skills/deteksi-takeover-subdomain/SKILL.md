# Skill: Deteksi Takeover Subdomain — Verifikasi CNAME ke Layanan yang Sudah Tidak Diklaim

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 41 (Subdomain Takeover Detection). Jangan klaim metode ini terbukti sampai ada satu subdomain yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat enumerasi subdomain (dari `pemetaan-permukaan-serangan` langkah 2) menemukan subdomain in-scope yang CNAME-nya mengarah ke layanan pihak ketiga (GitHub Pages, Heroku, S3, Vercel, Netlify, Azure, Shopify, dan sejenisnya) dan ada dugaan layanan itu sudah tidak diklaim pemiliknya — sehingga siapa pun bisa mendaftarkan dan mengambil alih subdomain tersebut.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Enumerasi subdomain + pemeriksaan CNAME dan fingerprint layanan |
| Pengerjaan | **A58 Vulnerability Researcher** | Menilai klaimabilitas + menyiapkan bukti |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan apakah klaim percobaan diizinkan (gerbang Langkah 4) dan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Enumerasi subdomain** → `pemetaan-permukaan-serangan` langkah 2. Skill ini memeriksa CNAME subdomain yang SUDAH dienumerasi, bukan mengenumerasi ulang.
- **Pembuktian dampak umum + laporan triage-ready** → `triase-duplikat` + `laporan-abstrak`.
- **Gerbang false-positive akhir sebelum laporan** → `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Subdomain di luar scope = jangan sentuh, walau kelihatan bisa diambil alih.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target atau layanan pihak ketiga dengan permintaan.
5. **Tanpa payload di permukaan publik.** Halaman placeholder klaim (bila diizinkan) hanya berisi teks penanda yang tidak berbahaya — jangan pasang konten yang meniru pemilik asli, memungut data pengunjung, atau menampilkan iklan.
6. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Jangan menghapus/mengubah konfigurasi DNS atau layanan milik target; jangan mengklaim lalu menahan (hold hostage) subdomain — bila klaim percobaan diizinkan dan berhasil, pasang HANYA placeholder tidak berbahaya dan segera laporkan + lepaskan/serahkan sesuai arahan pemilik/program.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan takeover subdomain.
11. **Klaim percobaan HANYA dengan izin eksplisit.** Mengklaim subdomain (mendaftarkan layanan pihak ketiga atas nama subdomain target) HANYA boleh dilakukan bila (a) aturan program secara eksplisit mengizinkan pembuktian dengan klaim, DAN (b) Muse menyetujuinya untuk kasus itu. Tanpa keduanya, bukti cukup berupa fingerprint layanan + catatan DNS (Langkah 3) — JANGAN mengklaim.

## Layanan pihak ketiga yang umum (acuan — periksa fingerprint masing-masing)

| Layanan | Tanda tidak diklaim (contoh pola respons) |
|---|---|
| GitHub Pages | 404 "There isn't a GitHub Pages site here" |
| Heroku | "No such app" / "There's nothing here, yet" |
| AWS S3 | `NoSuchBucket` |
| Vercel | 404 "DEPLOYMENT_NOT_FOUND" |
| Netlify | "Not Found — Request ID: ..." |
| Azure | NXDOMAIN / halaman default Azure |
| Shopify | "Sorry, this shop is currently unavailable" |
| Fastly / Tumblr / WordPress.com | Pesan layanan tidak ditemukan masing-masing |

Daftar ini acuan awal — fingerprint BERUBAH seiring waktu; yang menentukan adalah respons AKTUAL yang teramati dan didokumentasikan, bukan hafalan pola di atas. Bila pola tidak dikenali, catat respons persisnya dan serahkan ke Muse.

## Langkah + gerbang

### Langkah 1 — Kumpulkan CNAME subdomain in-scope

Dari hasil enumerasi `pemetaan-permukaan-serangan`, ambil semua subdomain in-scope yang masih hidup maupun yang DNS-nya mengarah ke pihak ketiga. Untuk tiap subdomain, catat catatan DNS-nya (`dig`/`nslookup`: CNAME, A, NS) dengan keluaran persis.

**Standar lulus:** tiap subdomain punya catatan DNS tercatat; subdomain tanpa catatan DNS = belum diperiksa.

### Langkah 2 — Saring CNAME ke layanan pihak ketiga

Tandai subdomain yang CNAME-nya mengarah ke layanan pihak ketiga (daftar acuan di atas atau layanan sejenis). Subdomain yang mengarah ke infrastruktur milik target sendiri (IP/server sendiri) BUKAN kandidat takeover — tutup dengan alasannya.

**Standar lulus:** daftar kandidat tertulis dengan layanan tujuan masing-masing; kandidat tanpa layanan tujuan = belum disaring.

### Langkah 3 — Periksa fingerprint "tidak diklaim"

Untuk tiap kandidat, minta URL-nya lewat HTTPS dan catat respons persis: kode status, isi halaman, header. Cocokkan dengan fingerprint "tidak diklaim" layanan itu (mis. GitHub Pages 404 "There isn't a GitHub Pages site here"). Bila layanan menjawab normal (situs aktif milik target) = TIDAK RENTAN, tutup dengan buktinya. Bila respons ambigu (error umum, timeout) = "belum dapat disimpulkan", jangan ditebak.

**Standar lulus (gerbang bukti tanpa klaim):** tiap kandidat punya respons tercatat (status + isi + header) dan penilaian: TIDAK RENTAN / KANDIDAT (fingerprint cocok) / BELUM DAPAT DISIMPULKAN. Fingerprint yang cocok + catatan DNS = bukti yang cukup untuk draf TANPA klaim.

### Langkah 4 — Gerbang klaim percobaan (HANYA bila diizinkan)

Bila aturan program mengizinkan pembuktian dengan klaim DAN Muse menyetujui kasus itu, daftarkan layanan pihak ketiga atas nama subdomain target memakai akun sendiri, pasang HANYA placeholder teks tidak berbahaya (mis. "Subdomain ini sedang diuji keamanan oleh peneliti — tidak ada data yang dikumpulkan"), buktikan subdomain menampilkan placeholder itu, lalu segera laporkan ke program/pemilik dan lepaskan/serahkan sesuai arahan.

**Standar lulus:** persetujuan Muse tercatat SEBELUM klaim; placeholder tidak berbahaya; bukti tangkapan layar + waktu klaim tercatat; pelepasan/penyerahan tercatat. Klaim tanpa persetujuan tercatat = PELANGGARAN — laporkan ke Muse segera.

### Langkah 5 — Nilai dampak + tulis draf

Tulis apa yang didapat penyerang bila mengambil alih subdomain itu (mis. hosting phishing atas nama domain tepercaya target, mencuri cookie bila cookie domain longgar, merusak reputasi). Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (layanan + apa yang bisa di-host di subdomain itu), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| `dig` / `nslookup` | Catat CNAME/A/NS tiap subdomain (keluaran persis) |
| curl / browser | Minta URL kandidat; catat status + isi + header untuk pencocokan fingerprint |
| Akun layanan pihak ketiga milik sendiri | HANYA untuk klaim percobaan bila Langkah 4 diizinkan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua subdomain + DNS + fingerprint + keputusan triase |

## Format output

Log setiap kandidat ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Subdomain: [nama subdomain]
Catatan DNS: [CNAME → ... | A → ... — keluaran dig persis]
Layanan tujuan: [mis. GitHub Pages / Heroku / ...]
Respons layanan: [status + isi/header persis — fingerprint cocok/tidak]
Klaim percobaan: [tidak dilakukan / dilakukan atas izin Muse — placeholder ... — dilepas/diserahkan ...]
Dampak: [apa yang didapat penyerang bila mengambil alih subdomain ini]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Fingerprint layanan berubah seiring waktu — pola di skill ini acuan, bukan kebenaran abadi; respons aktual yang menentukan.
- Sebagian program hanya menerima laporan takeover bila disertai bukti klaim — bila program itu mensyaratkan klaim SEMENTARA aturan program tidak mengizinkannya, serahkan ke Muse; jangan mengklaim diam-diam.
- CNAME ke layanan yang sudah tidak ada perusahaannya (layanan tutup) umumnya tidak bisa diklaim lagi — catat sebagai "tidak dapat diklaim" bila terkonfirmasi, bukan sebagai temuan.

### Available connectors

Tidak ada konektor khusus untuk skill ini; DNS diperiksa dengan `dig`/`nslookup` dan respons layanan dengan curl/browser.

### Websites

- Halaman aturan program resmi (sumber scope + apakah klaim percobaan diizinkan).
- Dokumentasi layanan pihak ketiga (cara klaim + fingerprint halaman tidak diklaim).

### Alternatives for better results

- Bila `dig` tidak tersedia, pakai layanan DNS lookup daring dari sumber tepercaya — catat sumbernya di log.
- Bila satu subdomain punya banyak CNAME berantai, telusuri sampai ujung rantai (layanan akhir yang melayani) sebelum menilai — CNAME perantara bukan vonis.
