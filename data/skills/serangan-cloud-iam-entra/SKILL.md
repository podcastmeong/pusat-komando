# Skill: Serangan Cloud IAM & Entra — Confused Deputy AWS STS, Penyalahgunaan AssumeRole, dan Rantai Federasi Identitas Enterprise

> Dibangun dari riset keenam "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`, Kategori 3 — Rantai Pasok & Infrastruktur Enterprise).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata per kategori yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat program bounty enterprise in-scope secara eksplisit mencantumkan aset cloud / identitas (akun AWS, tenant Microsoft Entra ID, organisasi Okta, atau aplikasi federasi milik target) dan ada hipotesis: peran IAM bisa diasumsikan lintas akun tanpa pengaman confused deputy, trust policy AssumeRole terlalu longgar, atau rantai federasi identitas (SAML/OIDC) bisa dimanipulasi untuk mendapat token atas identitas lain. Dipakai sesudah fondasi (`fondasi-kerentanan-web-api`) dikuasai — skill ini hanya menambah kategori cloud IAM & federasi, bukan menggantikannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menjalankan recon + pembuktian AssumeRole/federasi pada akun/tenant uji milik sendiri |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar lulus kategori itu |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Enumerasi bucket cloud terbuka (S3/GCS/Azure Blob, read-only) → `enumerasi-aset-cloud`. Skill ini beda: IAM + federasi identitas, bukan keterbukaan bucket.
- Discovery tenant M365 secara pasif (domain → tenant) → `mcp-osint` (M365 tenant discovery). Skill ini beda: rantai serangan federasi Entra/Okta, bukan sekadar menemukan tenant.
- Pemetaan permukaan serangan (inventaris aset/endpoint) → `pemetaan-permukaan-serangan`. Skill ini memakai indeksnya sebagai masukan, bukan mengulanginya.
- Validasi temuan + laporan triage-ready → `triase-duplikat` + `laporan-abstrak`.
- Variasi payload secara sistematis → `rekonstruksi-iterasi-payload`.

## Trigger & Scope

**Trigger (skill aktif bila SEMUA terpenuhi):**
1. Program bounty enterprise resmi dan aset cloud/identitasnya tercantum eksplisit di scope program (akun AWS / tenant Entra ID / organisasi Okta / aplikasi federasi target).
2. Ada sinyal awal: trust policy / konfigurasi federasi terlihat dari dokumentasi publik, error message, atau metadata aplikasi (mis. endpoint `/.well-known/openid-configuration`, metadata SAML publik); atau aplikasi target memakai login federasi / peran lintas akun.
3. Agen sudah punya akun AWS + tenant uji milik sendiri (dua akun/tenant terpisah milik sendiri) untuk pembuktian.

**Scope (yang BOLEH diuji):** hanya akun, tenant, dan aplikasi federasi yang TERCANTUM di scope program. **Yang TIDAK BOLEH:** infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali — tidak boleh menguji tenant Entra / organisasi Okta / akun AWS milik pihak ketiga di luar scope.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Target di luar scope = BERHENTI.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit program; satu percobaan AssumeRole per putaran, jangan membanjiri endpoint STS/IdP.
4. **Tanpa payload di permukaan publik.** Token canary hanya di akun/tenant uji milik sendiri.
5. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
6. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
8. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only.
9. **Teknik ini untuk program enterprise klasik, BUKAN untuk bounty agen AI** (Muse, OpenAI, 0din, Google AI VRP, ViKernel — di sana yang dinilai hasil/outcome agen, bukan IAM cloud).
10. **BATASAN KHUSUS KATEGORI 3 — WAJIB:** kategori ini HANYA untuk program enterprise yang secara eksplisit in-scope (program bounty enterprise dengan aset infrastruktur tercantum). Infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali; dilarang memindai/menguji cloud milik pihak ketiga di luar scope.
11. **AssumeRole/federasi hanya pada akun/tenant uji milik sendiri.** Replikasi trust policy target di akun AWS / tenant Entra uji milik sendiri (dua akun/tenant milik sendiri: penyerang + korban simulasi). JANGAN pernah memanggil `AssumeRole` / menukar token federasi terhadap akun/tenant target yang sebenarnya, dan JANGAN memakai kredensial/token milik siapa pun selain milik sendiri.
12. **JANGAN menyentuh data orang lain.** Bila pembuktian tanpa sengaja menampilkan data milik orang lain (daftar pengguna, grup, peran), BERHENTI — jangan simpan, jangan baca isinya, laporkan segera ke Muse.
13. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "kelihatan rentan" tanpa pembuktian dampak = tidak maju ke triase.
14. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.

## Methodology & Payloads

### 1. Cross-Account Confused Deputy pada AWS STS

- **Definisi:** peran IAM di akun korban mempercayai identitas dari akun lain (mis. `Principal: { "AWS": "*" }` atau akun penyerang) tanpa syarat pengaman (`ExternalId` / `aws:PrincipalTag` / `aws:SourceAccount`), sehingga siapa pun yang bisa mengasumsikan peran itu mendapat akses ke sumber daya akun korban — serangan "confused deputy": layanan/peran yang bingung siapa yang memerintahkannya.
- **Cara mengenali:** baca trust policy peran yang terekspos dari dokumentasi/konfigurasi publik target (atau dari error `AccessDenied` yang menyebut ARN peran): cari `Principal` yang luas (akun lain, `*`, layanan AWS) TANPA `Condition` (`sts:ExternalId`, `aws:PrincipalArn`, `aws:SourceAccount`). Tanda lain: aplikasi target meminta pengguna memasukkan `ExternalId` sendiri, atau tidak meminta sama sekali.
- **Pola pengujian (AMAN — dua akun AWS uji milik sendiri):**
  1. Di akun uji A (simulasi korban), buat peran dengan trust policy yang MENIRU pola target (principal luas tanpa `ExternalId`).
  2. Di akun uji B (simulasi penyerang, milik sendiri juga), panggil `sts:AssumeRole` ke peran akun A dengan kredensial akun B — TANPA `ExternalId`.
  3. Bukti = respons `AssumeRole` berhasil + kredensial sementara yang diterbitkan + satu panggilan read-only (`sts:GetCallerIdentity`) yang menunjukkan identitas peran A.
  4. Kontrol negatif: ulangi dengan trust policy yang SUDAH memakai `ExternalId` — `AssumeRole` tanpa `ExternalId` yang benar HARUS gagal.
- **Standar lulus:** ada bukti `AssumeRole` berhasil tanpa `ExternalId` pada peran replika + bukti kontrol negatif (dengan `ExternalId` yang benar, percobaan tanpa `ExternalId` gagal) + trust policy asli target yang menunjukkan pola yang sama (dokumen publik / konfigurasi terekspos). Sekadar "trust policy tidak punya Condition" tanpa pembuktian AssumeRole di replika = belum terbukti. **DILARANG keras:** memanggil `AssumeRole` ke peran milik target yang sebenarnya.

### 2. Penyalahgunaan AssumeRole (trust policy longgar)

- **Definisi:** trust policy peran mengizinkan principal yang tidak semestinya — mis. semua pengguna federasi, semua akun dalam satu organisasi tanpa batasan, atau layanan AWS apa pun — sehingga peran dengan izin tinggi bisa diasumsikan pihak yang tidak berhak.
- **Cara mengenali:** periksa siapa saja yang tercantum di `Principal` + `Condition` trust policy: `*`, federasi tanpa batasan `aud`/`sub`, atau `aws:PrincipalOrgID` tanpa batasan peran tambahan. Bandingkan izin peran (`Action` yang diizinkan) dengan siapa yang boleh mengasumsikannya — peran berizin tulis/administratif + principal luas = kandidat kuat.
- **Pola pengujian (AMAN — akun uji milik sendiri):**
  1. Replikasi trust policy + kebijakan izin peran target di akun uji milik sendiri.
  2. Dari principal uji yang TIDAK semestinya berhak (akun kedua milik sendiri / identitas federasi uji), panggil `AssumeRole` lalu satu panggilan read-only yang membuktikan izin peran itu (mis. `sts:GetCallerIdentity` + `iam:SimulatePrincipalPolicy` bila tersedia di akun uji).
  3. Bukti = kredensial sementara terbit + hasil simulasi kebijakan yang menunjukkan izin yang didapat.
- **Standar lulus:** ada bukti principal yang tidak semestinya berhasil mengasumsikan peran replika + bukti izin yang didapat (hasil simulasi / `GetCallerIdentity`) + trust policy asli target yang menunjukkan pola yang sama. Sekadar "principal terlihat luas" tanpa pembuktian asumsi peran di replika = belum terbukti.

### 3. Rantai Serangan Federasi Identitas Enterprise (Okta, Microsoft Entra ID)

- **Definisi:** celah pada rantai login federasi (SAML/OIDC) — mis. aplikasi tidak memvalidasi `audience`/`issuer` token, menerima token dari IdP lain, tidak memeriksa tanda tangan, atau alur "federasi" mempercayai klaim (grup/peran) dari token tanpa verifikasi — sehingga token dari tenant/organisasi lain (atau token yang dimanipulasi klaimnya) diterima sebagai identitas di aplikasi target.
- **Cara mengenali:** amati alur login federasi aplikasi target sebagai pengguna asli: endpoint `/.well-known/openid-configuration` dan metadata SAML publik (issuer, audience, endpoint token); periksa apakah aplikasi membedakan token dari IdP yang berbeda, dan apakah klaim grup/peran dari token langsung dipakai untuk otorisasi.
- **Pola pengujian (AMAN — dua tenant/organisasi uji milik sendiri):**
  1. Siapkan dua tenant/organisasi uji milik sendiri (IdP A = "benar", IdP B = "lain") + aplikasi uji milik sendiri yang meniru validasi aplikasi target.
  2. Minta token dari IdP B (milik sendiri) lalu ajukan ke aplikasi uji: catat apakah diterima atau ditolak.
  3. Varian kedua: token dari IdP A dengan klaim grup/peran yang diubah (di tenant uji milik sendiri, ubah keanggotaan grup pengguna uji) — catat apakah aplikasi uji memakai klaim itu tanpa verifikasi ulang.
  4. Bukti = respons aplikasi uji (sesi terbentuk / ditolak) + token yang dipakai (header/klaim, TANPA nilai rahasia — sensor signature bila perlu) + langkah reproduksi persis.
- **Standar lulus:** ada bukti token dari IdP B (milik sendiri) diterima aplikasi uji yang meniru validasi target, ATAU klaim grup yang diubah langsung memberi peran yang tidak semestinya — dengan kedua tenant milik sendiri + konfigurasi validasi aplikasi target yang terdokumentasi (publik). Sekadar "aplikasi memakai login federasi" atau "metadata SAML terbuka" tanpa token yang diterima = belum terbukti. **DILARANG keras:** memakai token/identitas dari tenant/organisasi target yang sebenarnya, atau memanipulasi klaim pengguna sungguhan.

## Validation Gate (verifikasi deterministik — baseline vs exploit)

Sebelum menyimpulkan adanya kerentanan, WAJIB lolos gerbang ini per kategori:

1. **Baseline:** catat perilaku normal DULU — `AssumeRole` dengan principal yang benar + `ExternalId` yang benar berhasil; `AssumeRole` tanpa `ExternalId` pada peran yang SUDAH diamankan gagal; token dari IdP yang benar diterima, token dari IdP lain ditolak. Simpan output baseline (respons STS / respons aplikasi uji) dengan tanggal.
2. **Exploit (canary, lingkungan uji):** jalankan pola di atas — `AssumeRole` tanpa `ExternalId` berhasil pada peran replika / token IdP lain diterima aplikasi uji. Simpan output exploit dengan tanggal.
3. **Perbandingan:** baseline vs exploit harus BERBEDA pada tepat satu variabel (ada/tidaknya `ExternalId` / asal IdP token / principal yang mengasumsikan). Bila baseline sudah "berhasil" tanpa canary, temuan itu artefak konfigurasi uji — ulangi dari lingkungan bersih.
4. **Pengulangan:** ulangi exploit dari state bersih minimal 1 kali; hasil yang sama = deterministik, boleh maju. Sekali berhasil tanpa pengulangan = belum terbukti.
5. **Human-in-the-loop:** A58 + A60 memeriksa baseline vs exploit sebelum draf laporan. Temuan yang gagal di gerbang mana pun = DITOLAK dengan alasan, dicatat di log.

## Langkah + gerbang

### Gerbang 0 — Cek scope enterprise dulu (standar lulus: program + aset cloud/identitas tercantum tertulis di log sebelum recon dimulai)

1. Tulis di `~/workspace/catatan/log-bug-bounty.md`: program, aset in-scope (akun AWS / tenant Entra / organisasi Okta / aplikasi federasi), dan batas yang berlaku.
2. Bila aset TIDAK tercantum eksplisit di scope → BERHENTI. Jangan recon.

### Gerbang 1 — Recon pasif konfigurasi federasi + trust policy (standar lulus: daftar trust policy / endpoint federasi yang relevan, masing-masing dengan sumber publiknya)

1. Kumpulkan metadata federasi publik (`/.well-known/openid-configuration`, metadata SAML) + trust policy / dokumentasi konfigurasi yang terekspos dari target (hanya yang publik / in-scope).
2. Catat tiap pola berisiko (principal luas, tanpa `ExternalId`, tanpa validasi `audience`) dengan sumber (dokumen + baris/bagian).

### Gerbang 2 — Nilai hipotesis (standar lulus: tiap hipotesis punya label kategori + rencana pembuktian di akun/tenant uji)

1. Tiap hipotesis dinilai: kategorinya apa (salah satu dari 3 di atas)? Cara pembuktian di akun/tenant uji-nya apa (sesuai standar lulus kategori itu)?
2. Hipotesis tanpa label kategori dan tanpa rencana bukti = ditolak, jangan diuji.

### Gerbang 3 — Buktikan di lingkungan uji (standar lulus: lolos Validation Gate di atas)

1. Jalankan pola Methodology & Payloads HANYA di akun/tenant uji milik sendiri; bukti memakai standar lulus tiap kategori.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun AWS uji milik sendiri (A = simulasi korban, B = simulasi penyerang) | Wajib untuk pembuktian confused deputy + AssumeRole. |
| Dua tenant/organisasi uji milik sendiri (Entra ID / Okta) | Wajib untuk pembuktian rantai federasi. |
| AWS CLI (`aws sts assume-role`, `aws sts get-caller-identity`, `aws iam simulate-principal-policy`) | Panggilan read-only di akun uji milik sendiri; JANGAN arahkan ke akun target. |
| Aplikasi uji milik sendiri (meniru validasi aplikasi target) | Wajib untuk pembuktian penerimaan token lintas IdP. |
| `curl` ke endpoint metadata federasi publik | Cek `/.well-known/openid-configuration` + metadata SAML (read-only). |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + baseline vs exploit + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program enterprise + aset in-scope: akun AWS / tenant Entra / organisasi Okta]
Kategori: [Confused Deputy STS / Penyalahgunaan AssumeRole / Rantai Federasi Entra-Okta]
Baseline: [perilaku normal + bukti respons STS/aplikasi uji + tanggal]
Exploit (lingkungan uji milik sendiri): [langkah + bukti respons + tanggal]
Perbandingan: [variabel yang berubah: ExternalId / asal IdP / principal]
Pengulangan: [berhasil diulang dari state bersih: ya/tidak]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui (BELUM DIUJI)

- Pola di atas diringkas dari riset, bukan dari satu kasus nyata yang lolos triase — tiap kategori punya varian (mis. `Condition` dengan `aws:PrincipalTag` yang sudah benar, IdP yang memvalidasi `audience` dengan ketat, kebijakan organisasi AWS `SCP` yang membatasi) yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Kredensial sementara dan token uji adalah milik sendiri — JANGAN pernah menulis nilainya di skill, log, atau chat; sensor sebelum dicatat.

### Available connectors

Tidak ada konektor khusus untuk skill ini; AWS CLI dan IdP uji dipakai lewat akun milik sendiri.

### Websites

- Dokumentasi AWS IAM resmi (trust policy, `ExternalId`, confused deputy, `AssumeRole`).
- Dokumentasi Microsoft Entra ID + Okta resmi (federasi SAML/OIDC, validasi token, klaim grup).
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila trust policy target tidak terekspos publik, andalkan audit konfigurasi lewat dokumentasi program + `enumerasi-aset-cloud` (bucket sebagai petunjuk organisasi) — jangan menebak ARN peran lalu memanggil `AssumeRole` ke akun target.
- Bila aplikasi target tidak memakai federasi (login lokal saja), skill ini tidak berlaku — catat sebagai "tidak ada sinyal federasi" dan serahkan ke Muse.
