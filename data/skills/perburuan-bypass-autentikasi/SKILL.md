# Skill: Perburuan Bypass Autentikasi — Pola Bypass dari Laporan Nyata (SAML Wrapping, Parser, SSO)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 39, sumber: Claude-BugHunter `hunt-auth-bypass`, 12 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai autentikasi dengan asumsi yang bisa diuji: login federasi (SAML/OIDC), SSO, penegakan domain, atau verifikasi token di sisi server.
- Ada sinyal: endpoint login menerima assertion/token, ada perbedaan perilaku antar parser, atau alur SSO memakai XMLRPC/endpoint lama.
- Dipakai pada akun uji sendiri, setelah alur login normal dipetakan. Jangan dipakai untuk membobol akun orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan asumsi autentikasi + menguji pola bypass satu per satu |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Ketidaksesuaian autentikasi ANTAR kanal (web vs API mobile vs endpoint lama) → skill `diskrepansi-autentikasi-lintas-kanal`. Skill ini BUKAN perbandingan kanal: ini pola bypass mekanisme autentikasi itu sendiri.
- Salah konfigurasi OAuth/SSO secara umum → skill `perburuan-kerentanan-spesifik` Gerbang 1.3 (kategori OAuth/SSO, bukan teknik bypass SAML/XMLRPC di sini).
- Serangan protokol SAML secara mendalam (manipulasi assertion, kebingungan audience/issuer, cacat validasi signature) → skill `perburuan-saml-sso`. **Batas dengan skill itu:** skill ini memakai SAML XML Signature Wrapping dan perbedaan parser SEBAGAI SALAH SATU pola bypass di antara banyak pola; `perburuan-saml-sso` adalah pendalaman penuh protokol SAML. Bila temuan terbukti murni SAML, serahkan pendalaman ke `perburuan-saml-sso`.
- Bypass 2FA/MFA → skill `analisis-bypass-2fa`.
- Manipulasi JWT (alg none, key confusion, JWK/JKU) → skill `manipulasi-jwt`.
- Rantai ATO secara keseluruhan → skill `perburuan-pengambilalihan-akun`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh alur autentikasi berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri dan IdP yang dikendalikan sendiri (bila memakai SAML/SSO uji). Jangan pernah memakai assertion/token dari IdP/tenant orang lain atau memanipulasi identitas pengguna sungguhan.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Khusus bypass autentikasi: pembuktian cukup sampai sesi akun uji sendiri terbentuk lewat jalur bypass; jangan ubah kredensial, peran, atau data akun apa pun.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Petakan asumsi autentikasi target

Petakan alur login SEBELUM menguji apa pun. Tulis peta ke log. Standar lulus: tiap asumsi tercatat dengan buktinya (endpoint, parameter, respons).

1. **Mekanisme autentikasi:** kata sandi saja / SSO SAML / OIDC / XMLRPC / campuran? Catat endpoint login, callback, dan token yang diterbitkan.
2. **Asumsi yang rapuh (hipotesis):** apakah server memvalidasi signature assertion? Apakah ada dua parser yang bisa berbeda pendapat (mis. parser XML vs validator)? Apakah penegakan domain dilakukan di klien atau server? Apakah assertion dari IdP lain diterima?
3. **Baseline:** login normal akun uji sendiri → sesi penuh terbentuk; login dengan kredensial salah → ditolak. Simpan raw request/response keduanya (token disensor).

### Gerbang 2 — Uji pola bypass satu per satu (satu pola = satu putaran)

Uji berurutan pada akun uji sendiri; tiap pola dicoba dari state bersih (logout penuh + sesi baru).

#### Pola A — SAML XML Signature Wrapping
Sisipkan assertion kedua (yang tidak ditandatangani / berisi identitas akun uji B) di dalam dokumen SAML yang sama, di luar elemen yang ditandatangani, sehingga validator memeriksa signature elemen pertama sementara aplikasi memakai assertion kedua. **Terbukti bila:** sesi Akun B terbentuk dari assertion yang tidak ditandatangani. Pendalaman penuh → `perburuan-saml-sso`.

#### Pola B — Perbedaan parser (parser differential)
Kirim assertion/token yang ditafsirkan berbeda oleh dua komponen (mis. parser XML yang longgar vs validator yang ketat, atau perbedaan penanganan namespace/komentar). **Terbukti bila:** satu komponen menerima identitas yang komponen lain tolak, dan sesi terbentuk dari identitas itu.

#### Pola C — Penghapusan signature
Hapus elemen signature dari assertion/token lalu kirim ulang. **Terbukti bila:** server tetap menerima assertion tanpa signature dan memberi sesi penuh.

#### Pola D — Bypass penegakan domain
Bila login dibatasi domain tertentu (mis. hanya `@perusahaan.com`), uji apakah penegakan dilakukan di klien saja (ubah parameter domain di request), atau apakah domain bisa dipalsukan lewat alamat email dengan subdomain/karakter khusus. **Terbukti bila:** akun uji dengan domain yang seharusnya ditolak berhasil login.

#### Pola E — Pemakaian ulang assertion lintas IdP
Ambil assertion valid dari IdP milik sendiri (IdP A) lalu kirim ke aplikasi yang seharusnya hanya percaya IdP B. **Terbukti bila:** assertion dari IdP yang tidak dipercaya diterima dan memberi sesi. DILARANG memakai assertion dari IdP/tenant target yang sebenarnya.

#### Pola F — Bypass SSO via XMLRPC / endpoint lama
Uji endpoint autentikasi lama (mis. XMLRPC, endpoint API versi lama) yang mungkin melewati pemeriksaan SSO/2FA yang diterapkan di alur baru. **Terbukti bila:** login lewat endpoint lama memberi sesi penuh tanpa melewati pemeriksaan yang diwajibkan alur baru. Lihat juga `diskrepansi-autentikasi-lintas-kanal` untuk perbandingan kanal.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** sesi akun uji lain terbentuk lewat jalur bypass, ATAU pemeriksaan autentikasi yang diwajibkan berhasil dilewati. **TOLAK** = sekadar pesan error berbeda, atau bypass yang hanya bekerja di klien tanpa sesi server.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, assertion, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (Akun A / Akun B) + IdP milik sendiri | Wajib untuk Pola A, B, E. Semua milik sendiri. |
| Proxy HTTP (Burp/mitmproxy) | Mengubah assertion/token di tengah alur login; simpan raw request/response. |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke assertion/token uji. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta asumsi + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + mekanisme autentikasi]
Peta asumsi: [mekanisme] | [validasi signature: ya/tidak] | [penegakan domain: server/klien] | [IdP dipercaya: ...]
Pola diuji: [A/B/C/D/E/F + nama pola + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Mekanisme Autentikasi] - [Pola Bypass] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Asumsi Rapuh (asumsi apa yang dilanggar); Langkah Reproduksi (akun uji + IdP sendiri + log HTTP); Rekomendasi Perbaikan (validasi signature di seluruh elemen assertion, satu parser kanonis, penegakan domain di server, whitelist IdP yang dipercaya, nonaktifkan endpoint autentikasi lama).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-auth-bypass`, 12 laporan terungkap), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Pola SAML di sini adalah pintu masuk; pendalaman protokol SAML ada di `perburuan-saml-sso` — jangan menduplikat isinya ke sini.
- Perbedaan parser sangat bergantung pada stack target; pola yang gagal di satu target bisa berhasil di target lain — catat stack yang diuji agar tidak mengulang pola yang sama di stack yang sama.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan bypass autentikasi.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya perbandingan kanal yang sama (web vs API mobile vs endpoint lama), pakai `diskrepansi-autentikasi-lintas-kanal`.
- Bila fokusnya SAML penuh (assertion, audience/issuer, signature), pakai `perburuan-saml-sso`.
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
