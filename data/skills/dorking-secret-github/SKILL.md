# Skill: Dorking & Secret Scanning GitHub/GitLab — Repo Publik Organisasi/Karyawan: API Key, Kredensial, Hardcoded Secrets

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 11 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu pemindaian nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih dan perlu diketahui apakah organisasi target (atau karyawannya, sebatas repo publik yang terkait organisasi) membocorkan secret di repo publik GitHub/GitLab — API key, kredensial, token, hardcoded secrets. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Menjalankan dorking + secret scanning, triase pola, redaksi, penyerahan ke indeks |
| Pemimpin | **Muse** | Putuskan secret mana yang dinyatakan temuan kandidat dan kapan diserahkan ke Cipta |

## Sudah tercakup (jangan diduplikat)

- **Dorking otomatis sebagai alat yang dipantau** ada di `alat-dorkagent` (status PANTAU — Google dorking LLM, bukan panduan teknik dorking GitHub/GitLab + secret scanning) — skill ini adalah panduan tekniknya.
- **Secret scanning sebagai alat** disebut di `mcp-security-hub` (gitleaks) dan `mcp-osint` (tanpa detail) — skill ini adalah panduan langkah-demi-langkah pemakaiannya pada repo in-scope.
- **Payung recon** ada di `pemetaan-permukaan-serangan` (langkah 4 menyebut hardcoded secrets di file JS dalam satu baris) — secret yang ditemukan di repo diserahkan ke indeks aset skill itu.
- **Redaksi secret di log** mengikuti aturan yang sama dengan `pemetaan-permukaan-serangan` langkah 4: secret DISENSOR (`[REDACTED]`).

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Hanya repo publik milik organisasi target / proyek in-scope yang dinyatakan program. Repo karyawan yang tidak terkait program = JANGAN dipindai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; patuhi rate limit API GitHub/GitLab (60 req/jam tanpa token, 5.000 req/jam dengan token sendiri); jangan membanjiri code search.
4. **Tanpa payload di permukaan publik.** Dorking + scanning hanya MEMBACA repo publik — tidak mengirim payload, tidak mengubah/menghapus data, tidak membuka issue/PR.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **DILARANG memakai secret yang ditemukan untuk mengakses apa pun.** Secret yang ketemu (API key, token, kredensial, private key) TIDAK BOLEH dipakai untuk login, memanggil API, atau mengakses layanan — sekalipun untuk "memverifikasi masih aktif". Validasi keaktifan hanya dari metadata publik (tanggal commit, apakah file masih ada di HEAD, apakah secret sudah di-revoke menurut riwayat repo) atau oleh pemilik program. Satu-satunya pengecualian: secret itu milik akun TIM SENDIRI / canary palsu.
7. **DILARANG menyimpan / menyebarkan nilai secret.** Nilai secret TIDAK PERNAH ditulis utuh di skill, log, chat, atau laporan draf — tulis pola + lokasi + `[REDACTED]`. Hasil dork yang menyingkap data orang lain TIDAK BOLEH disimpan, disebar, atau dipakai — laporkan ke Muse dan hapus salinan lokalnya.
8. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar secret bukan laporan.
9. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
11. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program). Clone repo publik in-scope untuk dipindai lokal adalah read-only dan diizinkan; clone repo di luar scope DILARANG.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope repo (wajib, sebelum pencarian apa pun)

- Apa yang dilakukan: baca aturan program; catat organisasi GitHub/GitLab target + repo yang dinyatakan in-scope; catat apakah program mengizinkan pengujian repo (bila tidak dinyatakan, dorking repo publik organisasi target tetap dibatasi ke repo publiknya saja).
- Standar lulus: organisasi + daftar repo in-scope tertulis; repo di luar daftar = DILARANG dipindai.

### Gerbang 1 — Dorking code search GitHub/GitLab

- Apa yang dilakukan: cari di code search publik dengan query sempit per pola, dibatasi ke organisasi target (mis. GitHub: `org:<org> "api_key"`, `org:<org> filename:.env`, `org:<org> "aws_secret_access_key"`, `org:<org> "password ="`, `org:<org> extension:pem`; GitLab: pencarian kode setara di grup target). Satu pola per sesi; catat query + jumlah hasil. Patuhi rate limit API.
- Standar lulus: tiap query tercatat (teks query + tanggal + jumlah hasil); query tanpa pembatas organisasi = DILARANG (sapu jagat); hasil di luar organisasi target dibuang, tidak dicatat.

### Gerbang 2 — Secret scanning otomatis pada repo in-scope (clone read-only)

- Apa yang dilakukan: clone repo publik in-scope (read-only, tanpa kredensial) ke VM yang bisa dibuang, lalu pindai lokal dengan gitleaks dan/atau trufflehog (cek README alat sebelum pakai pertama kali) — termasuk riwayat commit (`--history` / pemindaian git log), karena secret sering sudah dihapus dari HEAD tapi masih ada di histori.
- Standar lulus: tiap repo punya hasil pindaian (jumlah temuan + pola); clone dilakukan tanpa kredensial; repo di luar Gerbang 0 tidak di-clone.

### Gerbang 3 — Triase pola (bedakan secret nyata vs contoh/dummy)

- Apa yang dilakukan: untuk tiap temuan, periksa konteks: apakah nilai cocok dengan format secret asli (mis. `AKIA[0-9A-Z]{16}` untuk AWS, `ghp_`/`github_pat_` untuk GitHub, `xox[baprs]-` untuk Slack) vs placeholder/contoh (`xxx`, `your-key-here`, `test`, `example`); periksa apakah file itu contoh/dokumentasi/test fixture. Kelompokkan: (a) pola secret asli, (b) dummy/contoh — buang, (c) meragukan — tandai "belum diputuskan".
- Standar lulus: tiap temuan punya putusan (a/b/c) + alasan (format + konteks file); nilai secret TIDAK ditulis utuh di mana pun — hanya pola + lokasi + `[REDACTED]`.

### Gerbang 4 — Verifikasi tanpa memakai secret (metadata saja)

- Apa yang dilakukan: untuk tiap temuan kelompok (a), verifikasi dari metadata publik saja: apakah file masih ada di HEAD atau sudah dihapus (kapan), apakah commit-nya lama/baru, apakah ada commit lanjutan yang me-revoke/mengganti secret itu. JANGAN memanggil API/layanan dengan secret itu (Aturan keras 6).
- Standar lulus: tiap temuan (a) punya status "masih ada di HEAD" / "hanya di histori (commit <hash tanggal>)" / "sudah diganti di commit <hash>"; tidak ada bukti yang diperoleh dengan memakai secret.

### Gerbang 5 — Redaksi + serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis temuan kandidat (pola, repo, file, baris, status HEAD/histori — nilai `[REDACTED]`) ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Hapus clone lokal setelah pemindaian selesai. Temuan diserahkan ke Muse → Cipta; pengiriman ke program HANYA setelah Cipta setuju.
- Standar lulus: tidak ada nilai secret utuh di indeks, log, atau file mana pun; clone lokal sudah dihapus; tiap temuan punya lokasi + status verifikasi metadata.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Code search GitHub/GitLab | UI/API code search GitHub & GitLab (token sendiri bila perlu — JANGAN tulis token di skill/log) |
| Secret scanning lokal (repo + histori) | gitleaks, trufflehog (via `mcp-security-hub` bila tersedia — cek README sebelum pakai) |
| Dorking otomatis (pantau dulu) | `alat-dorkagent` (status PANTAU — pakai hanya bila sudah naik jadi andalan) |
| Validasi temuan (anti false-positive) | `skeptic-false-positive-eliminator` |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |

## Format output

### Daftar secret kandidat (TEREDAKSI)

Simpan di `~/workspace/catatan/secret-<target>-<tanggal>.md`:

```
- Repo: <org/repo> | file: <path> | baris: <n> | commit: <hash + tanggal>
- Pola: <mis. AWS access key / GitHub PAT / Slack token> | nilai: [REDACTED]
- Konteks: <file contoh/dokumentasi/kode produksi> | putusan: <secret asli / dummy / belum diputuskan>
- Status: <masih di HEAD / hanya di histori / sudah diganti>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Dorking & secret scanning GitHub/GitLab — <program/target>
- Query dorking: <n> | repo dipindai: <n> | temuan pola: <n>
- Secret asli (kandidat): <n> | dummy dibuang: <n> | belum diputuskan: <n>
- Nilai secret ditulis: TIDAK ADA (semua [REDACTED]) | clone lokal: <dihapus/ya>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi gitleaks (https://github.com/gitleaks/gitleaks) dan trufflehog (https://github.com/trufflesecurity/trufflehog).
- GitHub Code Search dan GitLab Code Search (pencarian dibatasi organisasi target).
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila gitleaks/trufflehog tidak tersedia, pemindaian pola manual dengan `grep -rE` atas pola regex secret pada clone lokal tetap sah untuk repo kecil — catat "pola manual" di log.
- Bila code search GitHub membatasi hasil, lengkapi dengan pemindaian histori lokal (Gerbang 2) — histori sering menyimpan secret yang sudah tidak muncul di pencarian.
