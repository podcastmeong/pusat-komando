# Skill: Recon Rantai Pasok & CI/CD — Dependency Confusion, Kebocoran Artifact Paket Internal, dan Workflow Injection

> Dibangun dari riset keenam "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`, Kategori 3 — Rantai Pasok & Infrastruktur Enterprise).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata per kategori yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat program bounty enterprise in-scope secara eksplisit mencantumkan aset rantai pasok / CI/CD (repositori, organisasi, registry paket internal, atau pipeline CI/CD milik target) dan ada hipotesis: nama paket internal bisa diklaim di registry publik (dependency confusion), artifact paket internal bocor ke publik, atau workflow CI/CD bisa disuntik lewat input yang dikendalikan penyerang (GitHub Actions workflow injection / poisoned pipeline execution). Dipakai sesudah fondasi (`fondasi-kerentanan-web-api`) dikuasai — skill ini hanya menambah kategori rantai pasok & CI/CD, bukan menggantikannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menjalankan recon + pembuktian canary pada repo/registry uji milik sendiri |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar lulus kategori itu |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Audit risiko dependensi STATIS (baca daftar dependensi, nilai risikonya) → `skill-trail-of-bits` (sub-skill upstream `supply-chain-risk-auditor`). Skill ini beda: pembuktian AKTIF dependency confusion dengan paket canary milik sendiri + kebocoran artifact + injeksi workflow — bukan audit statis.
- Audit workflow GitHub Actions STATIS untuk integrasi agen AI → `skill-trail-of-bits` (sub-skill upstream `agentic-actions-auditor`). Skill ini beda: pembuktian workflow injection / poisoned pipeline execution pada pipeline in-scope.
- Pemindaian secret di repo → `dorking-secret-github`. Skill ini memakai hasilnya sebagai petunjuk nama paket internal, bukan mengulanginya.
- Validasi temuan + laporan triage-ready → `triase-duplikat` + `laporan-abstrak`.
- Variasi payload secara sistematis → `rekonstruksi-iterasi-payload`.

## Trigger & Scope

**Trigger (skill aktif bila SEMUA terpenuhi):**
1. Program bounty enterprise resmi dan targetnya tercantum eksplisit di scope program (nama organisasi / repositori / registry / pipeline).
2. Ada sinyal awal: nama paket internal terlihat di file manifes publik (`package.json`, `requirements.txt`, `pom.xml`, `go.mod`), di log build yang bocor, atau di dokumentasi; atau workflow CI/CD memproses input dari luar (issue, PR, komentar, nama branch).
3. Agen sudah punya repositori/organisasi uji + registry uji milik sendiri untuk pembuktian canary.

**Scope (yang BOLEH diuji):** hanya repositori, organisasi, registry, dan pipeline yang TERCANTUM di scope program. **Yang TIDAK BOLEH:** infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali — tidak boleh memindai, menebak nama paket internal perusahaan lain, atau menguji pipeline organisasi lain.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Target di luar scope = BERHENTI.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit program; satu build uji per putaran, jangan membanjiri runner CI.
4. **Tanpa payload di permukaan publik.** Payload canary hanya di repo/registry uji milik sendiri — jangan menaruh payload di repo, issue, PR, atau komentar publik milik target.
5. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
6. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
8. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only.
9. **Teknik ini untuk program enterprise klasik, BUKAN untuk bounty agen AI** (Muse, OpenAI, 0din, Google AI VRP, ViKernel — di sana yang dinilai hasil/outcome agen, bukan rantai pasok).
10. **BATASAN KHUSUS KATEGORI 3 — WAJIB:** kategori ini HANYA untuk program enterprise yang secara eksplisit in-scope (program bounty enterprise dengan aset infrastruktur tercantum). Infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali.
11. **Dependency confusion hanya dibuktikan dengan paket canary milik sendiri.** JANGAN menimpa/mengunggah paket ke registry publik dengan nama paket internal milik target, dan JANGAN mengunggah paket apa pun yang meniru nama paket internal target ke registry publik. Pembuktian = paket canary bernama unik milik sendiri yang diunggah ke registry UJI milik sendiri (atau registry publik hanya bila namanya jelas-jelas canary milik sendiri dan tidak menabrak nama paket siapa pun), lalu tunjukkan resolver target lebih memilih sumber yang salah — tanpa pernah menyentuh nama paket internal target di registry publik.
12. **Workflow injection hanya pada repositori/organisasi uji milik sendiri.** Jangan menyuntik workflow di repo target; replikasi workflow target (salin file `.yml` yang publik) ke repo uji milik sendiri, buktikan injeksi di sana, lalu laporkan pola + bukti replikasi — bukan eksekusi di repo target.
13. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "kelihatan rentan" tanpa pembuktian dampak = tidak maju ke triase.
14. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah.

## Methodology & Payloads

### 1. Dependency Confusion (kebingungan dependensi)

- **Definisi:** manajer paket (npm, pip, Maven) mengambil paket dari registry publik padahal paket bernama sama ada di registry internal — karena registry publik diprioritaskan atau versinya lebih tinggi — sehingga kode dari registry publik (milik penyerang) dijalankan saat build/install.
- **Cara mengenali:** nama paket internal muncul di manifes publik (`package.json` → `dependencies`, `requirements.txt`, `pom.xml` → `<artifactId>`), di lockfile (`package-lock.json`, `Pipfile.lock`), atau di log build; lalu cek apakah nama yang sama ADA di registry publik (npmjs, PyPI, Maven Central) dan versi publiknya lebih tinggi, atau tidak ada sama sekali di publik (ruang kosong untuk diklaim).
- **Pola pengujian (AMAN — canary milik sendiri):**
  1. Buat paket canary bernama unik milik sendiri (mis. `<nama-tim>-canary-<acak>`) — JANGAN memakai nama paket internal target.
  2. Unggah canary ke registry UJI milik sendiri / registry publik hanya dengan nama canary itu.
  3. Di lingkungan uji milik sendiri, tiru konfigurasi resolver target (urutan registry + aturan versi dari dokumentasi/konfigurasi publik) dan tunjukkan resolver mengambil canary dari sumber yang tidak semestinya.
  4. Bukti = log resolver/install di lingkungan uji yang menunjukkan sumber paket yang terpilih + versi yang terpilih.
- **Standar lulus:** ada bukti resolver di lingkungan uji memilih sumber yang salah (canary milik sendiri terambil dari registry yang tidak semestinya) + nama paket internal target terbukti tercantum di manifes publik + nama itu tidak ada / versinya lebih rendah di registry yang benar. Sekadar "nama paket internal terlihat di package.json" tanpa bukti resolver = belum terbukti. **DILARANG keras:** mengklaim nama paket internal target di registry publik — itu menyerang rantai pasok target secara nyata, bukan pembuktian.

### 2. Kebocoran Artifact Paket Internal (npm, PyPI, Maven)

- **Definisi:** paket/artifact yang seharusnya hanya ada di registry internal ternyata bisa diakses publik — lewat registry yang salah konfigurasi, URL artifact yang bisa ditebak, atau cache/proxy publik yang menyimpan salinannya.
- **Cara mengenali:** URL registry internal muncul di konfigurasi publik (`.npmrc`, `pip.conf`, `settings.xml`, file CI), atau nama paket internal + versi bisa ditebak dari manifes; cek apakah artifact bisa diambil tanpa kredensial dari alamat publik.
- **Pola pengujian (read-only):**
  1. Minta metadata paket (bukan isi paket) dari alamat publik dengan request anonim: `GET` ke endpoint metadata registry (`/-/v1/search`, `/simple/<nama>/`, `.../maven-metadata.xml`) — status + daftar versi saja.
  2. Bila metadata terbuka, catat: nama paket + versi yang terekspos + URL-nya. JANGAN mengunduh isi artifact bila isinya kode/data milik target — itu data orang lain (lihat Aturan keras 2).
  3. Bila yang terekspos hanya metadata/daftar versi (bukan isi file), itu sudah cukup sebagai bukti keterbukaan; bila isi file terbuka dan berisi data orang lain: BERHENTI, jangan unduh, jangan baca isinya, laporkan segera ke Muse.
- **Standar lulus:** ada bukti status HTTP + metadata/daftar versi yang bisa diakses anonim untuk paket internal target + bukti paket itu memang internal (tercantum di manifes/konfigurasi internal target). Sekadar "URL registry merespons" tanpa bukti paket internal yang terekspos = belum terbukti.

### 3. GitHub Actions Workflow Injection & Poisoned Pipeline Execution (PPE)

- **Definisi:** workflow CI/CD mengeksekusi input yang dikendalikan penyerang (judul issue, isi komentar, nama branch, isi PR) tanpa sanitasi — mis. ekspresi `${{ github.event.issue.title }}` dipakai langsung di `run:` — sehingga penyerang bisa menyuntik perintah shell yang jalan di runner dengan token `GITHUB_TOKEN` dan akses repo.
- **Cara mengenali:** baca file workflow publik (`.github/workflows/*.yml` di repo target): cari `run:` yang menginterpolasi konteks event (`github.event.*`, `github.head_ref`, `github.ref`) langsung di shell, atau `pull_request_target` yang menjalankan kode dari PR, atau job yang memakai `GITHUB_TOKEN` berizin tulis.
- **Pola pengujian (AMAN — repo uji milik sendiri):**
  1. Salin file workflow target (yang publik) ke repositori UJI milik sendiri, tanpa mengubah logika yang diuji.
  2. Di repo uji, picu workflow dengan input canary milik sendiri (judul issue / nama branch berisi penanda canary, mis. `CANARY-<acak>` + perintah baca-saja seperti `echo` penanda ke log) — JANGAN perintah yang mengubah/menghapus data, JANGAN eksfiltrasi secret.
  3. Bukti = log run di repo uji yang menunjukkan penanda canary tereksekusi sebagai perintah, + potongan workflow asli yang menunjukkan interpolasi tidak aman.
- **Standar lulus:** ada bukti log run repo uji (perintah canary baca-saja tereksekusi) + file workflow asli target yang menunjukkan pola interpolasi yang sama + langkah reproduksi persis. Sekadar "workflow memakai `${{ github.event... }}` di `run:`" tanpa eksekusi canary di repo uji = belum terbukti. **DILARANG keras:** memicu injeksi di repo target (issue/PR/komentar berisi payload di repo target) — itu payload di permukaan publik.

## Validation Gate (verifikasi deterministik — baseline vs exploit)

Sebelum menyimpulkan adanya kerentanan, WAJIB lolos gerbang ini per kategori:

1. **Baseline:** catat perilaku normal DULU — resolver mengambil paket dari registry yang benar; metadata paket internal menolak akses anonim (401/403/404); workflow mengeksekusi input biasa tanpa menjalankan perintah tambahan. Simpan output baseline (log/status) dengan tanggal.
2. **Exploit (canary, lingkungan uji):** jalankan pola di atas — canary terambil dari sumber salah / metadata terbuka / penanda canary tereksekusi di log run repo uji. Simpan output exploit dengan tanggal.
3. **Perbandingan:** baseline vs exploit harus BERBEDA pada tepat satu variabel (sumber paket / akses anonim / input canary). Bila baseline sudah "terbuka"/"tereksekusi" tanpa canary, temuan itu artefak konfigurasi uji — ulangi dari lingkungan bersih.
4. **Pengulangan:** ulangi exploit dari state bersih minimal 1 kali; hasil yang sama = deterministik, boleh maju. Sekali berhasil tanpa pengulangan = belum terbukti.
5. **Human-in-the-loop:** A58 + A60 memeriksa baseline vs exploit sebelum draf laporan. Temuan yang gagal di gerbang mana pun = DITOLAK dengan alasan, dicatat di log.

## Langkah + gerbang

### Gerbang 0 — Cek scope enterprise dulu (standar lulus: program + aset rantai pasok/CI-CD tercantum tertulis di log sebelum recon dimulai)

1. Tulis di `~/workspace/catatan/log-bug-bounty.md`: program, aset in-scope (organisasi/repo/registry/pipeline), dan batas yang berlaku.
2. Bila aset TIDAK tercantum eksplisit di scope → BERHENTI. Jangan recon.

### Gerbang 1 — Recon pasif nama paket + workflow (standar lulus: daftar nama paket internal + file workflow yang relevan, masing-masing dengan sumber publiknya)

1. Kumpulkan manifes/lockfile/konfigurasi publik + file `.github/workflows/*.yml` dari repo target (hanya yang publik / in-scope).
2. Catat tiap nama paket internal + tiap pola interpolasi workflow dengan sumber (file + baris).

### Gerbang 2 — Nilai hipotesis (standar lulus: tiap hipotesis punya label kategori + rencana pembuktian canary)

1. Tiap hipotesis dinilai: kategorinya apa (salah satu dari 3 di atas)? Cara pembuktian canary-nya apa (sesuai standar lulus kategori itu)?
2. Hipotesis tanpa label kategori dan tanpa rencana bukti canary = ditolak, jangan diuji.

### Gerbang 3 — Buktikan di lingkungan uji (standar lulus: lolos Validation Gate di atas)

1. Jalankan pola Methodology & Payloads HANYA di repo/registry uji milik sendiri; bukti memakai standar lulus tiap kategori.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| Repositori + organisasi uji milik sendiri | Wajib untuk pembuktian workflow injection (salinan workflow + run canary). |
| Registry uji milik sendiri (npm/pip/Maven lokal atau privat) | Wajib untuk pembuktian dependency confusion dengan canary milik sendiri. |
| Paket canary milik sendiri (nama unik + penanda acak) | Satu-satunya paket yang diunggah; JANGAN memakai nama paket internal target. |
| `npm view` / `pip index` / `curl` ke endpoint metadata registry | Cek keberadaan + versi paket (metadata saja, read-only). |
| GitHub CLI / antarmuka web repo uji | Picu workflow uji + baca log run canary. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + baseline vs exploit + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program enterprise + aset in-scope: organisasi/repo/registry/pipeline]
Kategori: [Dependency Confusion / Kebocoran Artifact / Workflow Injection-PPE]
Baseline: [perilaku normal + bukti status/log + tanggal]
Exploit (canary, lingkungan uji): [langkah + bukti log/status + tanggal]
Perbandingan: [variabel yang berubah: sumber paket / akses anonim / input canary]
Pengulangan: [berhasil diulang dari state bersih: ya/tidak]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui (BELUM DIUJI)

- Pola di atas diringkas dari riset, bukan dari satu kasus nyata yang lolos triase — tiap kategori punya varian (mis. resolver yang memakai lockfile ketat, registry dengan autentikasi token, workflow yang memakai `env:` dengan benar) yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Perilaku resolver paket berubah antar versi manajer paket — cek dokumentasi versi yang dipakai target sebelum menyimpulkan.

### Available connectors

Tidak ada konektor khusus untuk skill ini; registry/repositori uji dipakai lewat akun milik sendiri.

### Websites

- Dokumentasi registry resmi target (npm, PyPI, Maven Central) — sumber aturan resolver + endpoint metadata.
- Dokumentasi GitHub Actions resmi (keamanan workflow, `pull_request_target`, izin `GITHUB_TOKEN`).
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila repo target tidak punya workflow publik, andalkan audit statis `skill-trail-of-bits` (`agentic-actions-auditor`) — jangan mengarang workflow dari tebakan.
- Bila nama paket internal tidak terlihat di manifes publik, catat sebagai "belum ada sinyal" dan serahkan ke Muse — jangan menebak nama paket internal lalu mengklaimnya di registry publik.
