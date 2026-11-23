# Skill: Perburuan Framework ASP.NET — ViewState, MachineKey & Endpoint Diagnostik

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 53, Claude-BugHunter `hunt-aspnet`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target teridentifikasi memakai ASP.NET / ASP.NET Core (header `X-AspNet-Version`, `X-Powered-By: ASP.NET`, cookie `.ASPXAUTH`, `__VIEWSTATE` di form).
- Ditemukan endpoint diagnostik (`trace.axd`, `elmah.axd`) atau error page yang membocorkan stack trace .NET.
- Dipakai SETELAH framework teridentifikasi via fingerprint (`probing-http-fingerprint`) — jangan menebak framework.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprint + pengujian pola khas ASP.NET |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Kelas kerentanan umum (SQLi, XSS, deserialisasi generik) → skill `fondasi-kerentanan-web-api`, `injeksi-sql-kontekstual`, `perburuan-deserialisasi` (bila ada). Skill ini HANYA pola khas ASP.NET.
- Deserialisasi generik per bahasa → lihat skill deserialisasi; skill ini hanya ViewState + machineKey.
- Lihat juga skill framework lain bila target memakai banyak stack: `perburuan-framework-laravel`, `perburuan-framework-nextjs`, `perburuan-framework-nodejs`, `perburuan-framework-springboot`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG:** menjalankan gadget deserialisasi yang mengeksekusi perintah (RCE) di server target — buktikan ViewState yang tidak tervalidasi dengan payload canary yang hanya menulis string penanda ke respons/log milik sendiri, atau cukup tunjukkan `enableViewStateMac=false` + machineKey yang bisa diprediksi dari sumber publik.

## Langkah + gerbang

### Gerbang 1 — Fingerprint ASP.NET

Standar lulus: framework terkonfirmasi atau dinyatakan "bukan ASP.NET" dengan bukti.

1. Header/cookie: `X-AspNet-Version`, `X-AspNetMvc-Version`, `.ASPXAUTH`, `ASP.NET_SessionId`, `__VIEWSTATE` / `__EVENTVALIDATION` di HTML.
2. Error page khas: "Server Error in '/' Application", stack trace `System.Web.*`.
3. Endpoint diagnostik: `GET /trace.axd`, `GET /elmah.axd` — 200 tanpa auth = kandidat langsung.

### Gerbang 2 — Pola khas (uji satu per satu, read-only)

| Pola | Cara uji aman | Indikator |
|---|---|---|
| Deserialisasi ViewState | Periksa `__VIEWSTATE` di form: apakah `enableViewStateMac=false` terdeteksi (ViewState bisa diubah tanpa MAC dan server menerimanya)? Uji dengan mengubah satu byte ViewState milik SESI SENDIRI dan lihat apakah server menolak/menerima. | Server menerima ViewState yang dimodifikasi = kandidat |
| Recovery machineKey | Cari machineKey di sumber publik: file `web.config` yang bocor (lihat `dorking-secret-github`, `penemuan-api-swagger`), error page, atau nilai default/lemah yang diketahui. JANGAN menebak dari data internal target. | machineKey ditemukan di sumber publik + ViewState bisa ditandatangani = kandidat kritis |
| Bypass MAC dual-parser | Uji perbedaan parser: ViewState yang valid menurut satu parser tapi tidak menurut parser lain (mis. perbedaan penanganan encoding). Hanya pada sesi sendiri. | Inkonsistensi penerimaan = kandidat |
| trace.axd / elmah.axd | `GET /trace.axd`, `GET /elmah.axd` tanpa auth. | 200 + isi log/error request pengguna lain = kandidat (STOP: jangan baca isi log pengguna lain — cukup buktikan halaman terbuka + judul/struktur, lalu sensor) |

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = ViewState termodifikasi diterima / endpoint diagnostik terbuka + dampak konkret. **TOLAK** = sekadar "header ASP.NET terlihat" atau "versi terdeteksi".
2. **Reproduksibilitas:** ulangi minimal 2×; simpan request/response mentah.
3. **Higienitas bukti:** sensor token sesi, machineKey LENGKAP (tampilkan hanya 4 karakter pertama + panjang), dan data pengguna lain sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `probing-http-fingerprint` | Fingerprint framework dari header/cookie/error page |
| Burp Suite Repeater | Modifikasi `__VIEWSTATE` sesi sendiri, amati penerimaan server |
| `dorking-secret-github` | Cari `web.config` / machineKey yang bocor di sumber publik |
| `~/workspace/catatan/log-bug-bounty.md` | Log pola yang diuji + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Framework: [ASP.NET / ASP.NET Core + bukti fingerprint]
Pola diuji: [ViewState / machineKey / dual-parser / trace.axd + hasil]
Pembuktian: [apa yang dibuktikan pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - [Pola ASP.NET] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-aspnet`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- ViewState modern (ASP.NET Core, .NET 4.5+ dengan MAC default) umumnya sudah aman — pola ini hanya relevan pada aplikasi lama atau konfigurasi yang sengaja melemahkan MAC.
- machineKey yang bocor di repo publik sering sudah dirotasi — verifikasi bahwa kunci itu masih berlaku pada target in-scope sebelum mengklaim dampak; kunci yang sudah tidak berlaku = TOLAK.
- JANGAN menjalankan gadget RCE (ysoserial .NET) terhadap server target — pembuktian berhenti di penerimaan ViewState termodifikasi / keterbukaan endpoint diagnostik.
