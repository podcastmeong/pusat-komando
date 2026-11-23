# Skill: Peracunan Cache — Cache Poisoning & Cache Deception

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 42 (Cache Poisoning & Cache Deception). Jangan klaim metode ini terbukti sampai ada satu respons cache yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat target web klasik in-scope berada di balik cache/CDN (header `Age`, `X-Cache`, `CF-Cache-Status`, `X-Cache-Status` terlihat) dan ada dugaan respons cache dipengaruhi input yang TIDAK dijadikan kunci cache (unkeyed input), sehingga penyerang bisa meracuni cache atau menipu cache menyimpan respons privat. Dipakai SETELAH `pemetaan-permukaan-serangan` menginventarisasi endpoint — skill ini menguji perilaku cache tiap endpoint, bukan menginventarisasi ulang.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menguji header unkeyed + perilaku cache tiap endpoint |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menilai dampak |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Inventarisasi endpoint + otorisasi** → `pemetaan-permukaan-serangan` langkah 5. Skill ini menguji perilaku cache endpoint itu.
- **Variasi header/payload secara sistematis** → `rekonstruksi-iterasi-payload`. Skill ini memakai variasinya untuk header unkeyed, bukan menulis ulang metodenya.
- **Pembuktian dampak umum + laporan triage-ready** → `triase-duplikat` + `laporan-abstrak`.
- **Gerbang false-positive akhir sebelum laporan** → `skeptic-false-positive-eliminator`.
- **Risiko `Vary: Origin` hilang pada respons CORS** → `audit-cors`. Bila temuan CORS itu mengarah ke cache, catat kaitannya di sini.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target atau CDN dengan permintaan; batasi jumlah permintaan uji dan patuhi rate limit program.
5. **Tanpa payload di permukaan publik.** Jangan meng-host halaman pemicu di tempat umum.
6. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only.
10. **JANGAN meracuni cache yang melayani pengguna lain.** Ini aturan khusus skill ini: semua uji memakai kunci cache UNIK milik sendiri (path/query canary yang tidak pernah dipakai pengguna sungguhan — mis. `/canary-<id-unik>/...`), sehingga entri cache yang terpengaruh HANYA bisa diambil oleh permintaan dengan kunci canary yang sama. JANGAN PERNAH mengirim header/sisipan berbahaya pada URL yang dipakai pengguna sungguhan. Bila entri cache bersama tidak sengaja terpengaruh, LAPORKAN SEGERA ke Muse + program dan minta purge — jangan diam.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik cache klasik.

## Yang dicari (definisi singkat)

- **Cache poisoning (peracunan cache):** penyerang mengirim permintaan dengan input yang TIDAK dijadikan kunci cache (unkeyed input — mis. header `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Host`, parameter query yang diabaikan cache) sehingga respons yang dihasilkan (mis. berisi host penyerang di tautan/skrip) disimpan cache dan disajikan ke pengguna lain yang meminta URL yang sama.
- **Cache deception (penipuan cache):** penyerang menipu cache agar menyimpan respons PRIVAT (mis. halaman akun yang sedang login) di bawah URL yang kelihatan publik/statik (mis. menambahkan `/akun.css` atau `/profil.js` di belakang path privat), sehingga pengguna anonim bisa mengambil data privat itu dari cache.
- **Yang menentukan adalah kunci cache:** bila cache mengunci SEMUA input yang memengaruhi respons (termasuk header dan cookie yang relevan), tidak ada celah. Uji selalu menjawab: input apa yang memengaruhi respons TAPI tidak memengaruhi kunci cache?

## Langkah + gerbang

### Langkah 1 — Petakan cache + kunci cache

Untuk tiap endpoint, catat header cache: `Cache-Control`, `Age`, `X-Cache` / `CF-Cache-Status` / `X-Cache-Status` (HIT/MISS), `Vary`, dan `X-Cache-Key` bila ada. Kirim permintaan yang sama dua kali: respons kedua harus HIT (membuktikan cache aktif untuk URL itu). Bila tidak ada HIT = cache tidak menyimpan endpoint itu, tutup.

**Standar lulus:** tiap endpoint punya catatan header cache + bukti HIT/MISS; endpoint tanpa HIT dicatat "tidak di-cache", bukan diuji lanjut.

### Langkah 2 — Cari unkeyed input

Uji input yang mungkin memengaruhi respons tapi tidak dijadikan kunci: header `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Host`, `X-Original-URL`, `X-Rewrite-URL`, parameter query tak dikenal, dan (untuk deception) akhiran path statik. Kirim DUA permintaan dengan kunci cache canary yang SAMA tapi nilai unkeyed BERBEDA — bila respons berbeda (mis. host canary muncul di isi respons) padahal kunci sama, input itu unkeyed dan memengaruhi respons.

**Standar lulus:** tiap input yang diuji tercatat (nilai dikirim → pengaruh ke respons → memengaruhi kunci atau tidak). Input yang tidak memengaruhi respons = bukan vektor, tutup.

### Langkah 3 — Buktikan peracunan pada kunci canary sendiri

Dengan kunci cache canary UNIK milik sendiri (aturan keras 10): (a) kirim permintaan "racun" (unkeyed input berisi penanda canary, mis. host canary) → catat respons + status cache (MISS, lalu tersimpan); (b) kirim permintaan KEDUA dengan kunci canary yang sama TAPI tanpa input racun → bila respons yang keluar adalah respons beracun (penanda canary terlihat) DAN status cache HIT, peracunan TERBUKTI pada kunci canary itu.

**Standar lulus (gerbang utama poisoning): tanpa respons beracun + HIT pada kunci canary = BELUM BERHASIL.** Respons beracun yang hanya muncul di permintaan pertama (MISS) bukan bukti — bukti adalah permintaan kedua yang bersih tetap menerima respons beracun dari cache.

### Langkah 4 — Buktikan deception dengan data canary sendiri

Dengan akun sendiri yang datanya HANYA canary palsu: (a) login sebagai akun sendiri, minta URL privat dengan akhiran statik (mis. `/akun/canary-<id>.css`); (b) catat apakah respons privat itu di-cache (header HIT pada permintaan anonim berikutnya); (c) minta URL yang sama TANPA autentikasi (sesi anonim) → bila data canary milik akun sendiri terbaca dari cache, deception TERBUKTI. Jangan pernah memakai data asli/pribadi untuk uji ini — hanya canary palsu.

**Standar lulus (gerbang utama deception): tanpa data canary terbaca anonim dari cache = BELUM BERHASIL.** Respons privat yang tidak di-cache, atau yang di-cache tapi tetap butuh autentikasi untuk diambil, = GAGAL — catat kenapa dan tutup.

### Langkah 5 — Nilai dampak + tulis draf

Tulis dampak konkret: untuk poisoning — apa yang disajikan cache beracun ke pengguna lain (tautan/skrip berbahaya berisi host penyerang); untuk deception — data privat apa yang bisa diambil anonim dari cache. Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (isi respons beracun / data yang bocor), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Kirim permintaan dengan header unkeyed kustom; baca header cache + isi respons persis |
| Akun uji sendiri (data canary palsu) | Wajib untuk deception: akun yang datanya "bocor" adalah akun sendiri |
| Sesi anonim (tanpa login) | Mengambil URL canary tanpa autentikasi untuk membuktikan deception |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua endpoint + header cache + bukti HIT + keputusan triase |

## Format output

Log setiap endpoint ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Endpoint: [METODE path]
Header cache: [Cache-Control: ... | X-Cache/CF-Cache-Status: ... | Vary: ...]
Unkeyed input diuji: [mis. X-Forwarded-Host: canary-<id> — memengaruhi respons: ya/tidak]
Bukti poisoning: [permintaan ke-2 bersih menerima respons beracun + HIT pada kunci canary — atau "TIDAK ADA"]
Bukti deception: [data canary akun sendiri terbaca anonim dari cache — atau "TIDAK ADA"]
Kunci canary dipakai: [path/query canary unik — BUKAN url pengguna sungguhan]
Dampak: [apa yang didapat penyerang bila korban sungguhan]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Tidak semua CDN meng-cache respons yang sama — perilaku cache bisa berbeda per wilayah/edge; satu HIT di satu edge bukan jaminan semua edge sama. Catat edge/region bila terlihat di header.
- Bila `Vary` mencakup header yang diuji (mis. `Vary: X-Forwarded-Host`), header itu SUDAH dijadikan kunci — bukan unkeyed; tutup dengan buktinya.
- Bila uji tidak sengaja memengaruhi entri cache bersama, laporkan segera ke Muse + program dan minta purge (aturan keras 10) — jangan menunggu draf laporan selesai.

### Available connectors

Tidak ada konektor khusus untuk skill ini; permintaan HTTP dikirim dengan curl/klien HTTP.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi CDN target bila diketahui (perilaku kunci cache).

### Alternatives for better results

- Bila header `X-Forwarded-Host` tidak berpengaruh, uji header unkeyed lain satu per satu (`X-Host`, `X-Forwarded-Scheme`, query tak dikenal) — jangan mengirim semuanya sekaligus, karena tidak ketahuan mana yang berpengaruh.
- Bila cache hanya aktif untuk metode GET, fokus ke GET; POST yang tidak di-cache tidak perlu diuji untuk poisoning (catat alasannya).
