# Skill: Perburuan Pengambilalihan Akun — Taksonomi 9 Jalur ATO & Rantai Gabungannya

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 38, sumber: Claude-BugHunter `hunt-ato`, 7 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai akun pengguna dengan alur login, reset kata sandi, verifikasi email, atau login federasi.
- Satu jalur ATO sudah diuji dan gagal — jangan berhenti; petakan 9 jalur lain sebelum menutup hipotesis.
- Dipakai SETELAH `alur-reset-kata-sandi-ato` dan `analisis-bypass-2fa` sudah dipakai atau dinyatakan tidak berlaku, karena skill ini adalah payung taksonomi di atas keduanya.
- Hanya pada akun uji sendiri; ATO terhadap akun orang lain DILARANG keras.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan 9 jalur + menguji masing-masing + merangkai rantai ATO |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap jalur memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Cacat reset kata sandi / token reset (Host header injection, token dapat diprediksi, kebocoran via Referer, token tidak terikat akun) → skill `alur-reset-kata-sandi-ato`. Skill ini memakai skill itu sebagai JALUR 1 dari 9, bukan mengulanginya.
- Bypass 2FA/MFA (manipulasi respons, kebocoran OTP, rate-limit OTP) → skill `analisis-bypass-2fa` (jalur 2FA di sini hanya satu jalur dari 9).
- Bypass autentikasi umum (SAML wrapping, perbedaan parser, bypass penegakan domain) → skill `perburuan-bypass-autentikasi`.
- Manajemen sesi (fixation, invalidasi tidak tuntas, session ID dapat diprediksi) → skill `perburuan-manajemen-sesi`.
- Open redirect sebagai rantai menuju pencurian token OAuth → skill `perburuan-open-redirect`.
- Host header sebagai vektor reset poisoning → skill `perburuan-host-header`.
- SAML/SSO → skill `perburuan-saml-sso`.
- Perangkaian temuan umum → skill `perangkaian-kerentanan`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh alur akun berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri (minimal dua akun: Akun A dan Akun B). Jangan pernah menguji ATO terhadap akun orang lain, akun karyawan target, atau akun produksi sungguhan.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Khusus ATO: **BERHENTI sebelum mengubah kata sandi, email, atau pengaturan keamanan akun uji** — pembuktian cukup sampai sesi akun uji lain terbentuk atau token reset valid terbukti, lalu serahkan ke A60. Jangan pernah menyelesaikan pengambilalihan sampai ke perubahan kredensial.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Petakan 9 jalur ATO pada target

Petakan alur akun target SEBELUM menguji apa pun. Tulis peta ke log. Standar lulus: tiap jalur dinyatakan "ada/tidak ada" dengan bukti (endpoint, parameter, respons).

| # | Jalur | Sinyal awal |
|---|---|---|
| 1 | Reset kata sandi (token reset) | Endpoint forgot-password, token di URL/email |
| 2 | Bypass 2FA/MFA | Langkah verifikasi kedua setelah kata sandi |
| 3 | Session fixation / hijacking | Session ID tidak diregenerasi saat login |
| 4 | OAuth/SSO token theft | Parameter `redirect_uri`, `code`, `state` |
| 5 | Host header poisoning (reset link) | Tautan reset memakai Host dari request |
| 6 | Email change tanpa verifikasi ulang | Ganti email tanpa konfirmasi ke email lama |
| 7 | Password reset via enumerasi / pertanyaan keamanan lemah | Pertanyaan keamanan dapat ditebak / dijawab dari data publik |
| 8 | Credential stuffing / brute-force login | Tidak ada rate limit / lockout pada login |
| 9 | Subdomain takeover / cookie scope luas | Cookie `Domain=.target` + subdomain rentan |

### Gerbang 2 — Uji satu jalur per putaran

Uji berurutan; tiap jalur dicoba dari state bersih (logout penuh + sesi baru). Satu jalur = satu putaran. Standar lulus tiap jalur: indikator teramati ATAU dinyatakan tidak ada dengan bukti negatif.

1. **Jalur reset (1):** pakai `alur-reset-kata-sandi-ato` — uji token Akun A dari sesi Akun B; berhenti sebelum ubah kata sandi.
2. **Jalur 2FA (2):** pakai `analisis-bypass-2fa` — manipulasi respons, kebocoran OTP, rate-limit OTP (maksimal belasan percobaan).
3. **Jalur sesi (3):** pakai `perburuan-manajemen-sesi` — fixation, invalidasi, entropi session ID.
4. **Jalur OAuth (4):** uji `redirect_uri` terbuka + `state` tidak divalidasi; rantai dengan `perburuan-open-redirect`. Pembuktian hanya dengan akun uji sendiri + IdP sendiri.
5. **Jalur Host header (5):** pakai `perburuan-host-header` — tautan reset berisi host canary milik sendiri.
6. **Jalur ganti email (6):** dari Akun A, ganti email ke alamat canary milik sendiri tanpa verifikasi ke email lama; bila berhasil tanpa konfirmasi = kandidat temuan. Jangan ganti email ke alamat orang lain.
7. **Jalur pertanyaan keamanan (7):** uji apakah jawaban dapat ditebak dari data publik milik sendiri (bukan data orang lain); bila pertanyaan keamanan bisa dilewati dengan jawaban kosong/umum = kandidat temuan.
8. **Jalur stuffing/brute-force (8):** pakai `perburuan-brute-force-rate-limit` — uji ADA/TIDAKNYA rate limit dengan volume minimal (lihat pagar ketat di skill itu); jangan membanjiri.
9. **Jalur cookie/subdomain (9):** periksa scope cookie (`Domain`, `Path`, `Secure`, `HttpOnly`) + status subdomain (pakai `deteksi-takeover-subdomain`); cookie `.target` + subdomain rentan = rantai kandidat.

### Gerbang 3 — Rangkai rantai ATO + serahkan ke triase

1. **Rantai gabungan — standar lulus:** minimal DUA jalur lemah yang bila digabung menghasilkan sesi penuh Akun B dari Akun A (mis. open redirect + token OAuth bocor; Host header + token reset tidak terikat akun). Satu jalur lemah saja yang tidak menghasilkan sesi = belum cukup, catat sebagai temuan parsial.
2. **Pembuktian akhir:** sesi Akun B terbentuk dari tangan Akun A, dibuktikan dengan endpoint profil Akun B yang mengembalikan data Akun B dalam sesi itu — lalu SEGERA logout dan kembalikan state (jangan ubah kata sandi/email Akun B).
3. **Reproduksibilitas:** ulangi rantai minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
4. Hanya temuan yang lolos gerbang ini yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (Akun A / Akun B) | Wajib untuk semua jalur. Keduanya milik sendiri. |
| Canary palsu (string/host/email non-sensitif milik sendiri) | Satu-satunya data yang disisipkan ke tautan reset, Host header, dan alur ganti email. |
| Log HTTP mentah | Simpan request/response sebagai bukti; sensor token/kode sebelum dilampirkan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta 9 jalur + hasil tiap jalur + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alur akun]
Peta 9 jalur: [1 reset: ada/tidak] | [2 2FA: ada/tidak] | [3 sesi: ada/tidak] | [4 OAuth: ada/tidak] | [5 Host: ada/tidak] | [6 ganti-email: ada/tidak] | [7 pertanyaan: ada/tidak] | [8 stuffing: ada/tidak] | [9 cookie/subdomain: ada/tidak]
Jalur diuji: [nomor + nama jalur + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Rantai: [jalur X + jalur Y → sesi Akun B terbentuk: ya/tidak]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Jalur ATO] - [Rantai Jalur] menyebabkan pengambilalihan akun [Akun Uji]`. Isi laporan: Ringkasan Taksonomi (jalur mana yang lemah); Langkah Reproduksi (dua akun uji + log HTTP); Rekomendasi Perbaikan (per jalur: token reset terikat akun + kedaluwarsa singkat, regenerasi sesi saat login, validasi `redirect_uri` + `state`, verifikasi ulang ke email lama saat ganti email, rate limit + lockout login).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-ato`, 7 laporan terungkap), bukan pengalaman teruji — tiap jalur butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Taksonomi 9 jalur adalah kerangka kerja; tidak semua target punya kesembilan jalur — jalur yang tidak ada dicatat "tidak ada" dan ditutup, bukan dipaksakan.
- ATO adalah kelas berdampak tertinggi sekaligus paling sensitif: pembuktian WAJIB berhenti sebelum perubahan kredensial, dan setiap langkah dicatat agar audit A60 bisa memverifikasi tidak ada akun orang lain yang tersentuh.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan ATO.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila hanya satu jalur reset yang dicurigai, pakai langsung `alur-reset-kata-sandi-ato` tanpa payung taksonomi ini.
- Bila target bukan web klasik (aplikasi LLM/RAG), pakai `audit-rag-llm` + skill Fase 5/6.
