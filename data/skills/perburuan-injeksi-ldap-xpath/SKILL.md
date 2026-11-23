# Skill: Perburuan Injeksi LDAP & XPath — Bypass Autentikasi, Ekfiltrasi Blind & Enumerasi AD/XML

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 46, sumber: Claude-BugHunter `hunt-ldap`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target memakai direktori LDAP/Active Directory untuk autentikasi atau penyimpanan berbasis XML yang memakai query XPath.
- Ada sinyal: error message menyebut LDAP (`LDAPException`, `Invalid DN syntax`, filter error) atau XPath (`XPathException`, `Invalid expression`); atau login memakai format DN/username yang diteruskan ke filter.
- Dipakai pada akun uji sendiri; injeksi hanya memakai karakter sintaks, bukan data orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan filter LDAP/XPath + menguji pola injeksi satu per satu |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Tidak ada skill LDAP/XPath di daftar yang ada — kandidat murni baru. Satu-satunya sebutan LDAP ada di `perburuan-shadow-api-spa` (insidental, bukan metodologi injeksi).
- Injeksi SQL (sintaks mirip tapi dialek berbeda) → skill `injeksi-sql-kontekstual`. Skill ini mengajarkan cara MEMBEDAKAN injeksi LDAP dari SQL — jangan memakai payload SQL di sini.
- Injeksi NoSQL (operator JSON MongoDB/CouchDB) → skill `injeksi-nosql`.
- Analisis Active Directory lewat MCP (BloodHound/RoadRecon) → skill `analisis-active-directory-lewat-mcp` bila ada (bila belum ada, catatan ini merujuk pada kandidat Bagian 3) — skill ini soal injeksi filter LDAP, bukan pemetaan graf AD.
- Enumerasi aset/pengguna secara umum → skill `enumerasi-subdomain` dan `penemuan-api-swagger` (bukan enumerasi via filter LDAP).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint LDAP/XPath berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri. Jangan pernah mengekstrak atribut, enumerasi pengguna/grup, atau menguji autentikasi akun orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan. Filter wildcard luas (`*`) yang membebani direktori DILARANG; ekfiltrasi blind dibatasi maksimal 20 percobaan per atribut.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Injeksi LDAP/XPath hanya untuk MEMBACA (bypass autentikasi akun uji sendiri / ekfiltrasi karakter atribut akun uji sendiri) — JANGAN mengubah, menambah, atau menghapus entri direktori/XML.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Bedakan LDAP/XPath dari SQL + petakan filter

1. **Bedakan sintaks:** LDAP memakai filter `(atribut=nilai)` dengan karakter khusus `* ( ) \ NUL` dan operator `& | !`; XPath memakai ekspresi `//elemen[@atribut='nilai']` dengan karakter khusus `' " [ ]`. Uji pemisah: kirim `*` ke field login — bila respons berubah secara khas LDAP (bukan error SQL), hipotesis LDAP menguat; kirim `'` ke field pencarian XML — bila error XPath muncul, hipotesis XPath menguat.
2. **Petakan filter:** catat field mana yang diteruskan ke filter LDAP (username, pencarian pengguna) atau query XPath (pencarian, filter dokumen XML), plus respons sukses vs gagal vs error.
3. **Standar lulus:** jenis injeksi (LDAP/XPath) + field yang rentan tercatat. Tidak ada sinyal LDAP/XPath = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji pola injeksi satu per satu (satu pola = satu putaran)

Uji berurutan pada akun uji sendiri; tiap pola dicoba dari state bersih.

#### Pola A — Bypass autentikasi lewat filter LDAP
Kirim username dengan filter LDAP yang selalu benar, mis. `*)(uid=*))(|(uid=*` atau variasi yang menutup filter awal dan membuka kondisi OR — HANYA terhadap akun uji sendiri. **Terbukti bila:** login berhasil tanpa kata sandi yang benar untuk akun uji sendiri, atau respons menunjukkan filter berhasil dimanipulasi. Jangan pakai pola ini terhadap akun orang lain.

#### Pola B — Ekfiltrasi atribut karakter demi karakter secara blind (LDAP)
Dengan filter LDAP boolean-based, tebak atribut akun uji sendiri satu karakter demi satu karakter (mis. `(uid=akun-uji*)(mail=a*)` → respons berbeda bila huruf pertama benar). Batas: maksimal 20 percobaan per atribut; cukup buktikan SATU karakter pertama + satu karakter tengah untuk menunjukkan ekfiltrasi blind dimungkinkan — jangan ekstrak atribut utuh. **Terbukti bila:** perbedaan respons konsisten mengikuti tebakan karakter yang benar.

#### Pola C — Enumerasi user/grup AD (LDAP)
Uji apakah filter pencarian LDAP mengembalikan daftar pengguna/grup tanpa otorisasi memadai — HANYA dengan filter yang menargetkan akun uji sendiri dan grup yang anggotanya akun uji sendiri. **Terbukti bila:** pencarian mengembalikan entri di luar yang seharusnya terlihat oleh akun uji. Jangan enumerasi seluruh direktori.

#### Pola D — Bypass pada penyimpanan berbasis XML via XPath
Kirim input XPath yang selalu benar ke field pencarian/filter, mis. `' or '1'='1` atau `'] | //* | //*['` — HANYA terhadap data uji sendiri. **Terbukti bila:** query mengembalikan data di luar yang diminta (mis. seluruh dokumen XML / node yang seharusnya tidak terlihat oleh akun uji sendiri).

#### Pola E — Ekfiltrasi blind via XPath
Dengan XPath boolean-based, tebak isi node akun uji sendiri karakter demi karakter (mis. `//user[username='akun-uji' and substring(password,1,1)='a']`). Batas: maksimal 20 percobaan per node; cukup buktikan SATU karakter untuk menunjukkan ekfiltrasi dimungkinkan. **Terbukti bila:** perbedaan respons konsisten mengikuti tebakan yang benar.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** bypass autentikasi akun uji sendiri TERBUKTI, ATAU ekfiltrasi blind terbukti lewat perbedaan respons yang konsisten, ATAU enumerasi/entri di luar hak terbaca. **TOLAK** = hanya error sintaks tanpa perubahan perilaku, atau perbedaan respons tidak konsisten saat diulang.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pola yang sama minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor kredensial, DN, dan data pribadi pada log HTTP sebelum dilampirkan (`[REDACTED]`); untuk ekfiltrasi blind, lampirkan maksimal 2 karakter yang terbukti (bukan atribut utuh). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib untuk semua pola. Milik sendiri. |
| Proxy HTTP (Burp/mitmproxy) | Mengirim payload filter LDAP/XPath; simpan raw request/response. |
| Daftar karakter uji (a-z, 0-9) | Untuk ekfiltrasi blind; maksimal 20 percobaan per atribut/node. |
| `~/workspace/catatan/log-bug-bounty.md` | Log jenis injeksi + field + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Jenis injeksi: [LDAP / XPath]
Field rentan: [username / pencarian / filter dokumen]
Pola diuji: [A/B/C/D/E + nama pola + payload + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Ekfiltrasi blind: [karakter terbukti: maks 2 | percobaan: ≤20]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Endpoint] - Injeksi [LDAP/XPath] menyebabkan [bypass autentikasi / ekfiltrasi / enumerasi]`. Isi laporan: Ringkasan (jenis + field + pola); Langkah Reproduksi (akun uji + payload + log HTTP); Rekomendasi Perbaikan (parameterisasi filter LDAP — escape `* ( ) \ NUL` atau pakai API berparameter; parameterisasi query XPath — jangan gabungkan input ke string query; least-privilege pada akun bind LDAP; jangan kembalikan error filter mentah ke klien).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-ldap`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Ekfiltrasi blind dibatasi 20 percobaan per atribut — cukup untuk membuktikan kemungkinan, bukan untuk mengekstrak data utuh.
- Sintaks LDAP dan SQL tampak mirip tapi berbeda — payload SQL yang ditempel ke filter LDAP hanya menghasilkan error dan membuang waktu; selalu bedakan dulu di Gerbang 1.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan injeksi LDAP/XPath.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target memakai SQL (bukan LDAP/XPath), pakai `injeksi-sql-kontekstual`.
- Bila target memakai NoSQL, pakai `injeksi-nosql`.
