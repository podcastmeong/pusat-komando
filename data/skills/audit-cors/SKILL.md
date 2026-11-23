# Skill: Audit CORS — Pantulan Origin Sembarangan + Kredensial

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 38 (CORS Misconfiguration Auditing). Jangan klaim metode ini terbukti sampai ada satu endpoint yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat target web/API klasik in-scope mengembalikan header CORS (`Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`) dan ada dugaan origin sembarangan dipantulkan sehingga situs lain bisa membaca respons terotentikasi. Dipakai SETELAH `pemetaan-permukaan-serangan` menginventarisasi endpoint API — audit ini menguji header tiap endpoint sensitif, bukan menebak endpoint baru.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Mengirim permintaan uji Origin + mencatat header respons |
| Pengerjaan | **A54 Penguji Live** | Membuktikan pembacaan lintas-origin di browser milik sendiri |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Inventarisasi endpoint API** → `pemetaan-permukaan-serangan` langkah 5. Skill ini menguji header endpoint itu, bukan menginventarisasi ulang.
- **Pembuktian dampak umum + laporan triage-ready** → `triase-duplikat` + `laporan-abstrak`. Skill ini menambah cara membuktikan dampak KHUSUS CORS (baca lintas-origin).
- **Gerbang false-positive akhir sebelum laporan** → `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan.
5. **Tanpa payload di permukaan publik.** Halaman uji lintas-origin jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only: cukup MEMBACA respons milik akun sendiri lintas-origin; jangan mengubah/menghapus data, jangan mencuri sesi orang lain.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik CORS klasik.

## Yang dicari (definisi singkat)

- **Pantulan Origin sembarangan:** server mengembalikan `Access-Control-Allow-Origin: <Origin yang dikirim>` untuk origin apa pun (bukan daftar allowlist), sehingga situs penyerang diizinkan browser membaca respons.
- **Kombinasi berbahaya:** pantulan Origin + `Access-Control-Allow-Credentials: true` pada endpoint yang mengembalikan data sensitif milik pengguna yang sedang login — inilah yang berdampak (situs lain bisa membaca data korban yang sedang login).
- **Bukan temuan (umumnya):** `Access-Control-Allow-Origin: *` TANPA kredensial pada endpoint publik (browser memang mengizinkan itu, dan data publik bukan rahasia); pantulan Origin pada endpoint yang tidak mengembalikan data sensitif dan tidak mengubah state. Nilai dampak apa adanya — jangan membesar-besarkan.
- **Perlu dicek juga:** header `Vary: Origin` (bila tidak ada, ada risiko cache menyimpan respons CORS untuk origin lain — kaitkan ke `peracunan-cache` bila relevan) dan respons preflight `OPTIONS` (`Access-Control-Allow-Methods` / `Access-Control-Allow-Headers` yang terlalu longgar).

## Langkah + gerbang

### Langkah 1 — Pilih endpoint sensitif

Dari indeks `pemetaan-permukaan-serangan`, pilih endpoint yang mengembalikan data milik pengguna login (profil, saldo, token, daftar data pribadi) atau mengubah state. Endpoint publik tanpa data sensitif dicatat tapi BUKAN prioritas.

**Standar lulus:** daftar endpoint tertulis dengan alasan sensitifnya; endpoint tanpa data sensitif ditandai "bukan prioritas".

### Langkah 2 — Uji pantulan Origin

Untuk tiap endpoint, kirim permintaan dengan header `Origin` sembarangan milik sendiri (mis. origin canary `https://canary-milik-sendiri.example`) — tanpa kredensial dulu, lalu DENGAN kredensial sesi sendiri (cookie/token akun sendiri). Catat respons persis: `Access-Control-Allow-Origin` (apakah memantulkan origin yang dikirim, `*`, atau allowlist tetap), `Access-Control-Allow-Credentials`, dan `Vary`.

Uji juga varian: origin `null`, origin subdomain sendiri, dan preflight `OPTIONS` (bila endpoint menerima metode kustom/header kustom).

**Standar lulus:** tiap endpoint punya tabel hasil (Origin dikirim → ACAO diterima → ACAC → Vary), untuk tanpa-kredensial DAN dengan-kredensial. Endpoint yang tidak memantulkan origin = AMAN, tutup dengan buktinya.

### Langkah 3 — Buktikan pembacaan lintas-origin di browser sendiri

Header yang memantulkan saja BELUM cukup — buktikan browser benar-benar mengizinkan situs lain membaca respons: buat halaman uji milik sendiri di origin canary, yang melakukan `fetch` ke endpoint target DENGAN kredensial (`credentials: "include"`) memakai sesi login akun sendiri, lalu tampilkan isi respons yang berhasil dibaca. Jalankan halaman itu di browser milik sendiri.

**Standar lulus (gerbang utama): tanpa bukti pembacaan lintas-origin di browser = BELUM BERHASIL.** Yang dihitung: halaman origin lain berhasil membaca data milik akun sendiri. Bila browser memblokir (mis. ACAO `*` + kredensial = kombinasi yang browser tolak), itu BUKTI TIDAK BERDAMPAK — catat dan tutup.

### Langkah 4 — Nilai dampak + tulis draf

Tulis data apa yang bisa dibaca situs lain bila korbannya sungguhan (data persis yang terbaca di Langkah 3, bukan dugaan). Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (data yang terbaca + siapa yang bisa membacanya), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien HTTP | Kirim permintaan dengan header `Origin` kustom; catat header respons persis |
| Halaman uji milik sendiri (origin canary) | `fetch` lintas-origin dengan kredensial sesi sendiri; hanya di lingkungan terkendali milik sendiri |
| Browser milik sendiri (`uji-live-browser`) | Tempat halaman uji dijalankan dan pembacaan dibuktikan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua endpoint + header + bukti pembacaan + keputusan triase |

## Format output

Log setiap endpoint ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Endpoint: [METODE path — data sensitif yang dikembalikan]
Origin dikirim: [origin canary milik sendiri]
Header respons: [ACAO: ... | ACAC: ... | Vary: ...]
Bukti pembacaan lintas-origin: [halaman canary berhasil membaca ... / browser memblokir — atau "TIDAK ADA"]
Dampak: [data apa yang bisa dibaca situs lain bila korban sungguhan]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Pantulan Origin pada endpoint publik/tanpa-kredensial umumnya tidak berdampak — jangan dipaksakan jadi temuan.
- Kombinasi `ACAO: *` + `ACAC: true` tidak diizinkan browser (browser menolak membaca respons berkredensial) — bila itu yang ditemukan, dampaknya TIDAK terbukti lewat jalur ini.

### Available connectors

Tidak ada konektor khusus untuk skill ini; permintaan HTTP dikirim dengan curl/klien HTTP dan halaman uji dijalankan di browser milik sendiri.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi target (endpoint API yang diuji).

### Alternatives for better results

- Bila endpoint memakai token Bearer (bukan cookie), kredensial tidak otomatis terkirim lintas-origin — uji tetap dilakukan, tapi dampaknya dinilai dari token yang bisa dicuri lewat jalur lain, bukan dari CORS saja; catat batas ini jujur di draf.
- Bila preflight `OPTIONS` diblokir tapi permintaan sederhana (`GET`/`POST` form) lolos, dampak tetap mungkin lewat permintaan sederhana — uji keduanya dan catat masing-masing.
