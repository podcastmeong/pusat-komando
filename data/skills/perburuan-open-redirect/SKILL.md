# Skill: Perburuan Open Redirect — Penilaian dari Keberadaan ke Rantai Pencurian Token OAuth hingga ATO

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 47, sumber: Claude-BugHunter `hunt-open-redirect`, 28 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target punya parameter redirect (`next`, `returnUrl`, `redirect`, `url`, `continue`, `target`) pada login, logout, atau alur OAuth.
- Ada sinyal: mengubah parameter redirect mengubah tujuan pengalihan, atau validasi redirect tampak longgar (allowlist tidak ketat, pemeriksaan substring).
- Dipakai pada akun uji sendiri; redirect hanya ke host canary milik sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan parameter redirect + menguji varian + merangkai dampaknya |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap varian memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- OAuth/SSO secara umum (salah konfigurasi `redirect_uri`, `state`, token) → skill `perburuan-kerentanan-spesifik` Gerbang 1.3. Skill itu membahas OAuth/SSO sebagai kategori, BUKAN open redirect sebagai kelas tersendiri. Skill ini adalah pendalaman open redirect: semua jenisnya + cara merantainya menjadi pencurian token OAuth hingga ATO.
- Open redirect sebagai bahan rantai (disebut sekilas) → skill `perangkaian-kerentanan`, `eskalasi-dampak-otomatis`, `verifikasi-poc-aman`. Ketiganya menyebut open redirect sebagai komponen rantai, bukan metodologi pengujiannya.
- Rantai ATO menyeluruh → skill `perburuan-pengambilalihan-akun` (open redirect di sini adalah jalur 4 di taksonomi itu).
- SSRF (redirect ke internal) → skill `ssrf-oast` (bila redirect mengarah ke layanan internal, itu SSRF — serahkan ke skill itu).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint redirect berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri dan host canary milik sendiri sebagai tujuan redirect. Jangan pernah mengarahkan redirect ke domain orang lain atau memakai redirect untuk menjebak pengguna sungguhan.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.** Tautan redirect uji hanya dipakai di sesi sendiri; jangan disebar.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Pembuktian rantai OAuth cukup sampai token/kode akun uji sendiri TERKIRIM ke host canary milik sendiri — jangan pakai token itu untuk mengambil alih sesi, dan jangan pernah memakai token orang lain.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Petakan parameter redirect + baseline validasi

1. **Petakan parameter:** `next`, `returnUrl`, `redirect`, `url`, `continue`, `target`, `redirect_uri` (OAuth) — di endpoint login, logout, dan callback OAuth. Catat respons normal (redirect ke host sendiri).
2. **Baseline:** redirect ke path internal / host sendiri → DITERIMA (normal). Simpan raw request/response.
3. **Standar lulus:** daftar parameter redirect + perilaku normal tercatat. Tidak ada parameter redirect = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji varian open redirect + rangkai dampaknya (satu varian = satu putaran)

Uji berurutan; tiap varian mengarah HANYA ke host canary milik sendiri.

#### Varian A — Redirect terbuka polos
Isi parameter dengan `https://canary-milik-sendiri/`. **Terbukti bila:** server mengarahkan (302/JS redirect/meta refresh) ke host canary.

#### Varian B — Bypass validasi allowlist
Uji bypass umum bila Varian A ditolak: `https://target.canary-milik-sendiri/` (subdomain canary), `https://canary-milik-sendiri%2etarget/` (encoding), `//canary-milik-sendiri/` (protocol-relative), `https://target%2f@canary-milik-sendiri/` (userinfo trick), dan backslash `https:\\canary-milik-sendiri\`. **Terbukti bila:** salah satu varian mengarahkan ke host canary.

#### Varian C — Redirect berbasis path / open redirect DOM
Uji redirect yang dilakukan JavaScript di klien (parameter dibaca JS lalu `window.location` diubah) dan redirect lewat path (`/redirect/canary...`). **Terbukti bila:** halaman mengarahkan browser sendiri ke host canary.

#### Varian D — Rantai pencurian token OAuth hingga ATO
Bila alur OAuth memakai `redirect_uri` yang bisa diarahkan ke host canary: jalankan alur OAuth akun uji sendiri dengan `redirect_uri=https://canary-milik-sendiri/callback` dan amati apakah `code`/`token` terkirim ke host canary. **Terbukti bila:** kode/token OAuth akun uji sendiri tiba di server canary milik sendiri. BERHENTI di sini — jangan tukar kode itu menjadi sesi, dan jangan pernah memakai kode/token orang lain. Lihat juga `perburuan-kerentanan-spesifik` Gerbang 1.3 untuk konteks OAuth.

#### Varian E — Rantai phishing (dampak tidak langsung)
Bila redirect terbuka terbukti (Varian A/B/C) tapi tidak ada token yang bocor, nilai apakah redirect bisa dipakai untuk phishing yang meyakinkan (domain target di URL awal → redirect ke canary). **Terbukti bila:** URL awal memakai domain target tepercaya lalu mengarah ke host canary tanpa peringatan. Catat sebagai dampak phishing — nilainya lebih rendah daripada Varian D.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** redirect ke host canary TERBUKTI (Varian A/B/C), ATAU token/kode OAuth akun uji sendiri tiba di canary (Varian D). **TOLAK** = redirect ditolak/divalidasi dengan benar, atau redirect hanya ke path internal. Perhatian: open redirect polos tanpa rantai sering dinilai rendah/ditolak program — utamakan Varian D (rantai token) atau Varian E (phishing meyakinkan) sebagai dampaknya; bila hanya Varian A tanpa rantai apa pun, konsultasikan ke Muse sebelum maju.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi varian yang sama minimal 2×. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token/kode OAuth dan token sesi pada log HTTP sebelum dilampirkan (`[REDACTED]`); log server canary dilampirkan hanya sebagai bukti kedatangan (timestamp + path, tanpa isi token). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib untuk semua varian, terutama Varian D. Milik sendiri. |
| Host canary milik sendiri (+ server log) | Satu-satunya tujuan redirect; catat kedatangan redirect/token. |
| Proxy HTTP (Burp/mitmproxy) | Mengubah parameter redirect; simpan raw request/response. |
| `~/workspace/catatan/log-bug-bounty.md` | Log parameter redirect + hasil tiap varian + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Parameter redirect: [next / returnUrl / redirect_uri / ...]
Varian diuji: [A/B/C/D/E + nama varian + nilai uji + log HTTP]
Tujuan redirect: [host canary milik sendiri]
Token tiba di canary: [ya/tidak — bila ya, jenis: code/token]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - Open redirect pada [parameter] menyebabkan [pencurian token OAuth / phishing / ATO]`. Isi laporan: Ringkasan (parameter + varian yang lolos); Langkah Reproduksi (akun uji + host canary + log HTTP); Rekomendasi Perbaikan (allowlist ketat redirect_uri + validasi host persis — bukan substring; tolak protocol-relative dan userinfo trick; jangan kirim token/kode ke redirect_uri yang tidak terdaftar).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-open-redirect`, 28 laporan), bukan pengalaman teruji — tiap varian butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Open redirect polos tanpa rantai sering dinilai rendah/ditolak — nilai skill ini ada pada RANTAI (Varian D/E), bukan pada keberadaan redirectnya saja.
- Validasi redirect tiap target berbeda (allowlist, regex, pemeriksaan substring) — catat pola validasi yang diuji agar tidak mengulang varian yang sama di target dengan validasi yang sama.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan open redirect.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya salah konfigurasi OAuth/SSO secara umum (bukan redirect), pakai `perburuan-kerentanan-spesifik`.
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
