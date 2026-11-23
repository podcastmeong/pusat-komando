# Skill: Perburuan Host Header — Reset Poisoning, Cache Poisoning & SSRF Routing via Host

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 45, sumber: Claude-BugHunter `hunt-host-header`, 16 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target membangun tautan dari Host header request (tautan reset kata sandi di email, tautan verifikasi, URL di respons) atau memakai Host/`X-Forwarded-Host` untuk routing ke upstream.
- Ada sinyal: mengubah Host mengubah isi respons (tautan/host di body), atau cache menyimpan respons yang berisi host kiriman.
- Dipakai pada akun uji sendiri; Host canary yang dipakai HANYA host milik sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Menguji Host header per endpoint + memetakan tiga dampaknya |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap dampak memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Cache poisoning secara umum (unkeyed input, deception) → skill `peracunan-cache`. Skill itu memakai `X-Forwarded-Host` SEBAGAI SALAH SATU contoh unkeyed input untuk cache poisoning. Skill ini fokus pada Host header sebagai AKAR dari TIGA dampak berbeda (reset poisoning, cache poisoning, SSRF routing/ACL bypass) — bukan sekadar satu contoh unkeyed input.
- Host Header Injection pada alur reset saja → skill `alur-reset-kata-sandi-ato` Teknik A (satu teknik di dalam alur reset). Skill ini adalah pendalaman Host header lintas endpoint + dua dampak lainnya.
- Penemuan virtual host (aplikasi tersembunyi di balik satu IP) → skill `penemuan-vhost` (itu soal menemukan vhost, bukan meracuni Host).
- SSRF umum / callback out-of-band → skill `ssrf-oast` (di sini SSRF spesifik lewat routing berbasis Host).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang diuji berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri dan host canary milik sendiri (mis. `canary-<id>.example.com` yang dikendalikan sendiri, atau domain uji milik sendiri). Jangan pernah memakai host/domain orang lain sebagai canary.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.** Host canary hanya dikirim ke endpoint in-scope milik target; jangan sebar tautan beracun.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Khusus reset poisoning: pembuktian cukup sampai tautan reset berisi host canary TERKIRIM ke email akun uji sendiri — JANGAN memakai tautan itu untuk mengubah kata sandi, dan JANGAN meminta reset untuk akun orang lain.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Petakan pemakaian Host per endpoint

1. **Petakan endpoint:** reset kata sandi, verifikasi email, pembuatan tautan/undangan, dan endpoint yang mengembalikan host di respons. Catat header yang memengaruhi respons: `Host`, `X-Forwarded-Host`, `X-Host`, `X-Forwarded-Server`.
2. **Baseline:** kirim request dengan Host ASLI → catat tautan/respons normal (akun uji sendiri).
3. **Standar lulus:** daftar endpoint + header yang memengaruhi respons tercatat. Tidak ada endpoint yang memakai Host dari request = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji tiga dampak (satu dampak = satu putaran)

Uji berurutan; tiap dampak memakai host canary milik sendiri.

#### Dampak A — Peracunan tautan reset-password hingga ATO
Minta reset kata sandi untuk AKUN UJI SENDIRI dengan `Host: canary-milik-sendiri`. Periksa email akun uji sendiri: apakah tautan reset memakai host canary? **Terbukti bila:** tautan reset di email berisi host canary milik sendiri. BERHENTI di sini — jangan klik tautan untuk mengubah kata sandi (pembuktian cukup sampai tautan terkirim). Lihat juga `alur-reset-kata-sandi-ato` Teknik A.

#### Dampak B — Peracunan cache web lewat Host / X-Forwarded-Host yang tidak dijadikan kunci cache
Kirim DUA request dengan kunci cache canary yang SAMA tapi nilai Host/`X-Forwarded-Host` BERBEDA (canary milik sendiri): (a) request "racun" berisi host canary → catat respons + status cache (MISS, lalu tersimpan); (b) request kedua dengan kunci sama TAPI tanpa host racun → bila respons yang keluar adalah respons beracun (host canary terlihat) DAN status cache HIT, peracunan TERBUKTI pada kunci canary itu. Detail metode → `peracunan-cache`.

#### Dampak C — SSRF berbasis routing dan bypass ACL karena Host memilih upstream
Uji apakah nilai Host memengaruhi upstream yang dipilih (mis. Host internal `localhost`/`169.254.169.254`/nama layanan internal mengubah respons) atau melewati ACL yang memeriksa Host. Kirim Host internal HANYA sebagai nilai uji dan amati respons — jangan mengeksploitasi layanan internal yang terjangkau. **Terbukti bila:** respons menunjukkan routing ke upstream berbeda / konten internal terbaca lewat Host yang dimanipulasi. Bila konten internal terbaca, catat bukti minimal (status + potongan non-sensitif) dan BERHENTI — jangan menjelajah layanan internal.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** (A) tautan reset berisi host canary di email akun uji sendiri; ATAU (B) respons beracun tersaji dari cache pada kunci canary; ATAU (C) routing/ACL berubah karena Host. **TOLAK** = Host diabaikan server, atau perubahan hanya di respons tanpa dampak (mis. host tercermin tapi tidak dipakai di tautan/cache/routing).
2. **Reproduksibilitas deterministik — standar lulus:** ulangi dampak yang sama minimal 2×. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi/reset dan data pribadi pada log HTTP/email sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib; semua reset/tautan memakai email akun uji sendiri. |
| Host canary milik sendiri | Satu-satunya host yang disisipkan ke Host header; catat identifier-nya. |
| Proxy HTTP (Burp/mitmproxy) | Mengubah Host/`X-Forwarded-Host`; simpan raw request/response + status cache. |
| Email akun uji sendiri | Memeriksa tautan reset yang terkirim (hanya email milik sendiri). |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta endpoint + hasil tiap dampak + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Header diuji: [Host / X-Forwarded-Host / X-Host]
Dampak diuji: [A reset poisoning / B cache poisoning / C SSRF routing-ACL]
Host canary: [canary-<id> milik sendiri]
Indikator teramati: [apa yang terjadi, persis — tautan reset / status cache HIT + isi beracun / respons routing]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - Host header [dampak] menyebabkan [dampak spesifik]`. Isi laporan: Ringkasan (header + dampak); Langkah Reproduksi (akun uji + host canary + log HTTP); Rekomendasi Perbaikan (jangan bangun tautan dari Host request — pakai host yang dikonfigurasi di server; jadikan Host kunci cache atau tolak Host tak dikenal; routing/ACL jangan percaya pada Host dari klien).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-host-header`, 16 laporan), bukan pengalaman teruji — tiap dampak butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Banyak aplikasi modern sudah memakai host allowlist — Host yang diabaikan adalah hasil "aman", bukan kegagalan.
- Dampak C (SSRF routing) paling sensitif: bila konten internal terbaca, catat bukti minimal dan berhenti — jangan menjelajah layanan internal.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan Host header.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila hanya cache poisoning yang dicurigai (bukan Host sebagai akar), pakai langsung `peracunan-cache`.
- Bila hanya alur reset yang dicurigai, pakai `alur-reset-kata-sandi-ato`.
