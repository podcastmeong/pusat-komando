# Skill: Pemetaan Permukaan Serangan — Inventaris Aset & Endpoint Target Web/API In-Scope

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset Perspektif 1 (Reconnaissance & Attack Surface Mapping) dan komponen 2 arsitektur multi-agent (Recon & Context Engine), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu pemetaan nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih (mis. jalur audit kode OSV huntr) dan targetnya perlu dipetakan secara teknis SEBELUM pengujian apa pun. Bukan untuk bounty agen AI — di Muse, OpenAI, 0din, Google AI VRP, dan ViKernel yang dinilai adalah HASIL/outcome pada agennya, bukan scanning web klasik; jangan buang waktu memindai situs program AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Enumerasi subdomain + inventarisasi endpoint API |
| Pengerjaan | **A59 Threat Hunter** | Analisis file JavaScript + pemetaan arsitektur aplikasi |
| Pengerjaan | **A57 Penetration Tester** | Port scanning dalam scope + verifikasi endpoint dari indeks |
| Pemimpin | **Muse** | Putuskan target mana yang dipetakan dan kapan indeks dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Recon PROGRAM** (direktori, scope, hadiah, deadline, aturan AI) ada di `recon-pantau-program` — skill ini beda: recon TEKNIS target, bukan mencari program.
- **Penjaga scope & rate limit** ada di `scope-and-safety-guardian` — skill ini memakai batasnya, bukan menulis ulang.
- **Alat-alatnya** ada di skill MCP masing-masing (`mcp-shodan`, `mcp-osint`, `alat-dorkagent`, `mcp-security-hub`) — skill ini hanya merujuk namanya sebagai "tangan", jangan duplikat dokumentasi alatnya.
- **Validasi temuan** (clean session, PoC deterministik, skeptic gate) BUKAN bagian skill ini — itu gerbang tahap pengujian setelah indeks selesai.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Target di luar scope = HENTIKAN, jangan dipetakan.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban — victim-agent fraud tests DIBLOKIR.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** (lihat `scope-and-safety-guardian`); tanpa pemindaian massal tanpa jeda.
4. **Tanpa payload di permukaan publik.** Pemetaan ini hanya MENGAMATI dan MENCATAT — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Agen HANYA boleh menguji URL yang tercatat di indeks.** Dilarang mengarang nama endpoint, menebak path, atau menguji URL yang tidak ada di indeks.
6. **Satu endpoint/fitur per tugas.** Batasi konteks per agen agar tidak mencampur parameter antar-API.
7. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, tanpa payload.
8. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
9. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Indeks aset bukan laporan — jangan kirim apa pun ke program dari skill ini.

## Langkah + gerbang

### 1. Tetapkan scope teknis (A53)
Ambil daftar aset in-scope dari aturan program (domain, subdomain, IP, API) yang sudah divalidasi `recon-pantau-program`. Tulis daftar itu di kepala indeks. **Standar lulus:** tiap aset punya sumber aturan program + tautan resmi; aset tanpa sumber = belum dipetakan.

### 2. Enumerasi subdomain (A53)
Enumerasi subdomain target dalam scope (pakai `mcp-osint` / `alat-dorkagent` sebagai tangan). Catat tiap subdomain: nama, sumber penemuan, status hidup/mati, dan layanan yang terlihat. **Standar lulus:** tidak ada subdomain in-scope yang diketahui tapi tidak tercatat; subdomain out-of-scope dicatat sebagai out-of-scope, bukan diuji.

### 3. Port scanning dalam scope (A57)
Pindai port pada aset in-scope saja (pakai `mcp-shodan` / `mcp-security-hub`), maks 5 req/detik, tanpa stress test. Catat port terbuka + layanan + versi bila terlihat. **Standar lulus:** tidak ada pemindaian di luar scope; tidak ada jeda rate limit yang dilanggar; hasil tercatat per aset.

### 4. Analisis file JavaScript (A59)
Kumpulkan file JS yang dimuat aplikasi target; cari endpoint tersembunyi, parameter API tak terdokumentasi, hardcoded secrets/konfigurasi, dan URL internal. **Standar lulus:** tiap temuan dicatat dengan file sumber + baris/konteks; secret yang ditemukan DISENSOR di log (`[REDACTED]`) dan TIDAK dipakai untuk mengakses apa pun — hanya dicatat sebagai temuan pemetaan.

### 5. Inventarisasi endpoint API (A53)
Susun daftar endpoint dari dokumentasi/OpenAPI resmi + pengamatan sebagai pengguna asli (alur yang dilewati pengguna sungguhan). Tiap entri wajib berisi: metode, path, parameter, dan catatan otorisasi (token apa, peran apa, milik siapa). **Standar lulus: entri tanpa catatan otorisasi = belum dipetakan** — tidak boleh diuji sebelum otorisasinya ditulis.

### 6. Pemetaan arsitektur aplikasi (A59)
Gambarkan arsitektur dari hasil langkah 2–5: komponen (frontend, API, auth, layanan pihak ketiga), alur data, dan batas kepercayaan (mana yang dipercaya server tanpa verifikasi). **Standar lulus:** tiap komponen tertaut ke entri indeks; komponen tanpa sumber di indeks = asumsi, tulis sebagai asumsi, bukan fakta.

### 7. Bekukan indeks + serahkan (Muse)
Indeks aset terstruktur disimpan dan dinyatakan SIAP UJI hanya bila semua gerbang 1–6 lolos. Setelah itu pengujian memakai indeks ini — dan hanya indeks ini. **Standar lulus:** indeks lengkap (tiap entri punya metode, parameter, otorisasi); tidak ada entri "belum dipetakan" yang lolos ke tahap uji.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Info aset & intelijen OSINT | `mcp-shodan`, `mcp-osint` |
| Pencarian terpandu / dorking | `alat-dorkagent` |
| Pemindaian & perkakas keamanan | `mcp-security-hub` |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |

## Format output

### Indeks aset (file/DB terstruktur — satu sumber kebenaran)

Simpan di samping skill atau di `~/workspace/catatan/` dengan nama `indeks-aset-<program>-<tanggal>.md` (atau DB setara). Format per entri:

```
- Aset: <subdomain/IP/API base> | sumber: <aturan program/dokumen>
- Endpoint: <METODE path> | parameter: <daftar> | otorisasi: <token/peran pemilik>
- Layanan: <port/layanan/versi> | JS: <file sumber temuan>
- Status: TERPETAKAN / BELUM DIPETAKAN (tanpa otorisasi = BELUM DIPETAKAN)
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Pemetaan permukaan serangan — <program/target>
- Aset terpetakan: <n> subdomain, <n> endpoint, <n> layanan
- Belum dipetakan: <n> entri (alasan: tanpa otorisasi / dst.)
- Indeks: <path file indeks>
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi/OpenAPI resmi target (sumber inventarisasi endpoint langkah 5).
- Halaman aturan program resmi (sumber scope langkah 1).

### Alternatives for better results

- Bila target tidak punya dokumentasi/OpenAPI, andalkan pengamatan sebagai pengguna asli (langkah 5) — jangan mengarang endpoint dari tebakan.
- Bila pemetaan mentok (JS ter-obfuscate, endpoint tak terlihat), catat sebagai "belum dipetakan" dan serahkan ke Muse — jangan memaksa dengan pemindaian agresif.
