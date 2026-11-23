# Skill: Perburuan SAML / SSO — Serangan Protokol SAML (Assertion, Audience/Issuer, Validasi Signature)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 48, sumber: Claude-BugHunter `hunt-saml`, 6 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai login federasi SAML (Service Provider yang menerima assertion dari Identity Provider).
- Ada sinyal: endpoint SAML terlihat (`/saml/acs`, `/saml/sso`, `/saml/metadata`), metadata SAML publik, atau alur login melewati IdP.
- Dipakai pada akun uji sendiri + IdP yang dikendalikan sendiri; jangan pernah memakai IdP/tenant target yang sebenarnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Membaca alur SAML target + menguji titik validasi satu per satu |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- OAuth/SSO secara umum (salah konfigurasi `redirect_uri`, `state`, token OIDC) → skill `perburuan-kerentanan-spesifik` Gerbang 1.3. Skill ini spesifik pada PROTOKOL SAML (XML assertion), bukan OAuth/OIDC.
- Rantai federasi identitas cloud (SAML/OIDC, trust policy AssumeRole, Entra/federasi) → skill `serangan-cloud-iam-entra`. Skill itu membahas federasi sebagai rantai IAM cloud; skill ini membahas serangan protokol SAML pada aplikasi web (assertion, audience/issuer, signature) — sudut dan buktinya berbeda.
- Pola bypass autentikasi umum (termasuk SAML XML Signature Wrapping sebagai salah satu pola) → skill `perburuan-bypass-autentikasi`. **Batas dengan skill itu:** skill itu memakai wrapping sebagai SATU pola di antara banyak pola bypass; skill ini adalah pendalaman penuh protokol SAML. Bila temuan terbukti murni SAML, pendalaman dilakukan di sini.
- Manipulasi JWT (alg none, key confusion, JWK/JKU) → skill `manipulasi-jwt` (itu token JWT, bukan assertion SAML XML).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh alur SAML berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri dan IdP yang dikendalikan sendiri. Jangan pernah memakai assertion/token dari IdP/tenant orang lain atau memanipulasi identitas pengguna sungguhan.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Pembuktian cukup sampai sesi akun uji sendiri terbentuk lewat assertion yang dimanipulasi; jangan ubah kredensial, peran, atau data akun apa pun.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Baca alur SAML target + catat baseline

1. **Baca alur:** ambil metadata SAML publik target (issuer, audience/SP EntityID, endpoint ACS, sertifikat publik) — hanya yang publik/in-scope. Lakukan login SAML normal akun uji sendiri dan simpan alur: AuthnRequest → IdP → SAMLResponse (assertion) → ACS → sesi.
2. **Petakan titik validasi:** apakah SP memvalidasi signature assertion? Apakah memeriksa `Audience`/`Issuer`? Apakah memeriksa `NotBefore`/`NotOnOrAfter` dan `InResponseTo`? Apakah ada dua parser XML yang bisa berbeda pendapat?
3. **Baseline:** login SAML normal akun uji sendiri → sesi penuh terbentuk; assertion kedaluwarsa/dari IdP lain → ditolak (bila bisa diuji dengan IdP sendiri). Simpan raw request/response (assertion disensor).
4. **Standar lulus:** metadata + alur + titik validasi tercatat. Target tidak memakai SAML = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji pola serangan SAML satu per satu (satu pola = satu putaran)

Uji berurutan; tiap pola memakai IdP milik sendiri + akun uji sendiri, dari state bersih (logout penuh + sesi baru).

#### Pola A — Manipulasi assertion (ubah isi tanpa merusak signature)
Ubah isi assertion yang ditandatangani (mis. `NameID`/username menjadi akun uji B, atau ubah atribut peran/grup) lalu kirim ke ACS. **Terbukti bila:** SP menerima assertion yang isinya berubah dan memberi sesi Akun B — artinya signature tidak benar-benar mengikat isi.

#### Pola B — Kebingungan audience / issuer
Kirim assertion yang ditujukan untuk SP lain (Audience berbeda, milik sendiri) atau dengan Issuer IdP lain (milik sendiri) ke ACS target. **Terbukti bila:** SP menerima assertion yang Audience/Issuer-nya bukan untuk dirinya.

#### Pola C — Cacat validasi signature
Uji varian: hapus elemen signature; ganti algoritma signature; tandatangani dengan kunci sendiri (bukan kunci IdP yang dipercaya); pindahkan signature ke elemen lain. **Terbukti bila:** salah satu varian diterima SP dan memberi sesi penuh.

#### Pola D — SAML XML Signature Wrapping
Sisipkan assertion kedua (tidak ditandatangani, berisi identitas Akun B) di dalam dokumen SAML yang sama, di luar elemen yang ditandatangani, sehingga validator memeriksa signature elemen pertama sementara aplikasi memakai assertion kedua. **Terbukti bila:** sesi Akun B terbentuk dari assertion yang tidak ditandatangani. (Pola ini juga tercantum di `perburuan-bypass-autentikasi` Pola A — pendalaman di sini.)

#### Pola E — Pemakaian ulang assertion (replay)
Ambil SAMLResponse valid dari login sebelumnya (akun uji sendiri) lalu kirim ulang ke ACS setelah sesi berakhir. **Terbukti bila:** assertion lama diterima lagi dan memberi sesi baru — artinya tidak ada pemeriksaan `InResponseTo`/sekali pakai/kedaluwarsa yang efektif.

#### Pola F — Perbedaan parser (parser differential)
Kirim assertion dengan konstruksi XML yang ditafsirkan berbeda oleh validator vs aplikasi (komentar, namespace ganda, entitas, duplikasi elemen `NameID`). **Terbukti bila:** satu komponen menerima identitas yang komponen lain tolak, dan sesi terbentuk dari identitas itu.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** sesi akun uji lain terbentuk lewat assertion yang dimanipulasi, ATAU assertion yang seharusnya ditolak (audience/issuer salah, tanpa signature, replay) DITERIMA dan memberi sesi. **TOLAK** = SP menolak semua varian, atau manipulasi hanya tampak di klien tanpa sesi server.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pola yang sama minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor assertion, signature, dan token sesi pada log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri (Akun A / Akun B) + IdP milik sendiri | Wajib untuk semua pola. Semua milik sendiri. |
| Metadata SAML publik target | Issuer, Audience, endpoint ACS, sertifikat publik (hanya yang publik/in-scope). |
| Proxy HTTP (Burp/mitmproxy) + tool SAML (mis. SAML Raider / skrip XML sendiri) | Mengubah assertion; simpan raw request/response. |
| `~/workspace/catatan/log-bug-bounty.md` | Log alur SAML + titik validasi + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + SP SAML]
Metadata: [Issuer: ... | Audience: ... | ACS: ...]
Titik validasi: [signature: ya/tidak] | [audience/issuer: ya/tidak] | [NotBefore/NotOnOrAfter: ya/tidak] | [InResponseTo: ya/tidak]
Pola diuji: [A/B/C/D/E/F + nama pola + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[SP SAML] - [Pola Serangan SAML] menyebabkan [sesi akun lain / bypass autentikasi federasi]`. Isi laporan: Ringkasan (pola + titik validasi yang gagal); Langkah Reproduksi (akun uji + IdP sendiri + log HTTP, assertion disensor); Rekomendasi Perbaikan (validasi signature atas SELURUH assertion dengan kunci IdP yang dipercaya; periksa Audience + Issuer + NotBefore/NotOnOrAfter + InResponseTo di setiap login; satu parser XML kanonis; tolak assertion tanpa signature; assertion sekali pakai).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-saml`, 6 laporan), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Pengujian SAML butuh IdP yang dikendalikan sendiri — tanpa itu, hanya Pola A/C yang bisa diuji sebagian lewat manipulasi respons login normal; jangan memakai IdP/tenant target yang sebenarnya.
- Pola D (wrapping) dan F (parser differential) sangat bergantung pada library XML target — catat library yang teridentifikasi agar tidak mengulang pola yang sama di stack yang sama.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan serangan SAML.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya federasi cloud/IAM (AssumeRole, trust policy, Entra), pakai `serangan-cloud-iam-entra`.
- Bila fokusnya pola bypass autentikasi umum (bukan SAML murni), pakai `perburuan-bypass-autentikasi`.
- Bila fokusnya rantai ATO menyeluruh, pakai `perburuan-pengambilalihan-akun`.
