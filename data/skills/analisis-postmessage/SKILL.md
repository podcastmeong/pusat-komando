# Skill: Analisis PostMessage — Listener Tanpa Validasi event.origin

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 39 (PostMessage Vulnerability Analysis). Jangan klaim metode ini terbukti sampai ada satu listener yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat kode JS target in-scope memakai `window.addEventListener("message", ...)` (atau `onmessage`) dan ada dugaan handler itu tidak memvalidasi `event.origin` sebelum memakai `event.data`. Dipakai SETELAH `pemetaan-permukaan-serangan` langkah 4 mengumpulkan file JS — skill ini khusus menganalisis listener pesan antar-frame, bukan semua aliran data.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Menemukan listener + menelusur pemakaian `event.data` |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + halaman pengirim uji |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Pengumpulan file JS** → `pemetaan-permukaan-serangan` langkah 4. Skill ini menganalisis listener di file itu.
- **Aliran DOM source→sink secara umum** → `pelacakan-taint-xss-dom`. `event.data` adalah salah satu source di sana — skill ini menambah analisis KHUSUS origin (validasi, bypass, dan pembuktian lintas-origin).
- **Pembuktian eksekusi JS di browser** → `verifikasi-xss`. Bila handler bermuara ke sink eksekusi (innerHTML/eval), pembuktiannya memakai skill itu.
- **Pembuktian dampak umum + laporan triage-ready** → `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan.
5. **Tanpa payload di permukaan publik.** Halaman pengirim uji jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only: cukup tunjukkan handler menerima pesan dari origin lain milik sendiri dan memicu efek yang teramati di sesi sendiri — jangan mengubah/menghapus data, jangan mencuri sesi orang lain.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik postMessage klasik.

## Yang dicari (definisi singkat)

- **Listener tanpa validasi origin:** handler `message` memakai `event.data` tanpa memeriksa `event.origin` sama sekali — halaman mana pun (termasuk situs penyerang) bisa mengirim pesan ke target.
- **Validasi lemah (bypass):** origin diperiksa dengan cara yang bisa dilewati, mis. `origin.includes("target.com")` (lolos oleh `https://target.com.penyerang.example`), `endsWith` tanpa titik pemisah, regex longgar, atau hanya memeriksa `event.source` tanpa origin.
- **Validasi benar (aman):** perbandingan persis dengan allowlist origin (`event.origin === "https://app.target.com"` atau termasuk dalam daftar persis) SEBELUM `event.data` dipakai.
- **Yang menentukan dampak adalah APA yang dilakukan handler dengan `event.data`:** sekadar mencatat pesan = tidak berdampak; tetapi bila data dipakai ke sink (`innerHTML`, `eval`, `postMessage` balasan berisi data sensitif, perubahan state/autentikasi, pemuatan URL) = berdampak. Listener tanpa validasi TAPI datanya tidak dipakai untuk apa pun yang sensitif = bukan temuan.

## Langkah + gerbang

### Langkah 1 — Temukan semua listener

Cari di file JS target semua `addEventListener("message"`, `addEventListener('message'`, dan `onmessage`. Catat tiap listener dengan file + baris + potongan handler lengkap.

**Standar lulus:** daftar listener tertulis (atau pernyataan "tidak ada listener"); listener tanpa file:baris = belum dicatat.

### Langkah 2 — Periksa validasi origin

Untuk tiap listener, baca handler-nya dan kutip persis bagaimana `event.origin` diperiksa (atau tidak diperiksa):

- Tidak ada pemeriksaan origin → KANDIDAT.
- Pemeriksaan lemah (`includes`, `indexOf`, `endsWith` tanpa batas, regex longgar) → KANDIDAT (catat pola bypass-nya).
- Perbandingan persis dengan allowlist → AMAN, tutup dengan kutipan kodenya.

**Standar lulus:** tiap listener punya kutipan pemeriksaan origin-nya (atau pernyataan "tidak ada pemeriksaan"); penilaian "lemah" harus menyebut pola bypass konkret, bukan dugaan.

### Langkah 3 — Telusur pemakaian event.data

Telusuri apa yang dilakukan handler dengan `event.data`: ke sink apa (innerHTML/eval/URL/state), apakah data diteruskan ke `postMessage` lain, apakah memicu aksi sensitif (login, ganti pengaturan, tampilkan data). Bila handler hanya mencatat/mengabaikan data → TIDAK BERDAMPAK, tutup.

**Standar lulus (gerbang utama):** tiap kandidat berisi (a) listener + file:baris, (b) kutipan validasi origin, (c) rantai `event.data` → efek/sink. Kandidat tanpa efek yang jelas = dugaan, buang.

### Langkah 4 — Buktikan dengan halaman pengirim milik sendiri

Buat halaman pengirim milik sendiri di origin canary (bukan origin target) yang membuka target di iframe dan mengirim pesan `event.data` yang dirancang untuk memicu efek Langkah 3. Jalankan di browser milik sendiri dengan sesi login akun sendiri. Amati: apakah handler target menerima pesan dari origin canary dan memicu efek yang teramati (mis. konten berubah, `document.domain` tercetak via sink, state berubah di akun sendiri)?

**Standar lulus:** efek teramati dan terdokumentasi dari pengirim origin lain milik sendiri; bila handler menolak pesan (tidak ada efek) = GAGAL — catat kenapa, lalu variasikan `event.data` atau tutup.

### Langkah 5 — Nilai dampak + tulis draf

Tulis apa yang didapat penyerang bila korbannya sungguhan (situs penyerang mengirim pesan ke target yang sedang dibuka korban). Serahkan draf ke A60 untuk audit, lalu ke Muse/Cipta. Jangan kirim laporan apa pun tanpa persetujuan Cipta.

**Standar lulus:** dampak ditulis konkret (efek + data/aksi yang didapat), draf mengikuti format output di bawah, dan status triase diputuskan A60 — bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar file JS dari `pemetaan-permukaan-serangan` | Sumber listener yang dianalisis |
| Pencarian teks / AST parser JS | Cari listener + telusur `event.data` |
| Halaman pengirim milik sendiri (origin canary) | Mengirim `postMessage` ke target di iframe; hanya di lingkungan terkendali milik sendiri |
| Browser milik sendiri (`uji-live-browser`) | Tempat target + pengirim dijalankan dan efek diamati |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua listener + validasi + bukti + keputusan triase |

## Format output

Log setiap listener ke `~/workspace/catatan/log-bug-bounty.md` (hari itu juga), dengan format:

```
Tanggal: [YYYY-MM-DD]
Aplikasi: [nama + program bounty]
Listener: [addEventListener("message") — file:baris]
Validasi origin: [tidak ada / lemah: <pola + bypass> / persis allowlist — kutipan kode]
Pemakaian event.data: [rantai data → efek/sink]
Bukti lintas-origin: [halaman canary memicu efek ... — atau "TIDAK ADA"]
Dampak: [apa yang didapat penyerang bila korban sungguhan]
Keputusan triase: [BERHASIL / GAGAL — alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Listener tanpa validasi origin TAPI datanya tidak dipakai untuk efek sensitif bukan temuan — jangan dipaksakan.
- Bila target tidak bisa dibuka di iframe (header `X-Frame-Options` / CSP `frame-ancestors`), pembuktian lintas-origin lewat iframe tidak bisa jalan — catat batasnya dan serahkan ke Muse; jangan memaksa dengan cara yang melanggar aturan program.

### Available connectors

Tidak ada konektor khusus untuk skill ini; halaman pengirim dijalankan di browser milik sendiri.

### Websites

- Halaman aturan program resmi (sumber scope + aturan bukti yang diterima triase).
- Dokumentasi target (alur fitur yang memakai postMessage, mis. widget/embed).

### Alternatives for better results

- Bila handler memakai `event.source.postMessage` untuk membalas, periksa juga APA yang dibalas (bila balasan berisi data sensitif ke origin mana pun, dampaknya bisa lebih besar) — catat isi balasan di Langkah 3.
- Bila ada beberapa listener di file yang sama, uji satu per satu dengan pesan yang berbeda-beda — jangan mengirim satu pesan generik dan mengklaim semua listener rentan.
