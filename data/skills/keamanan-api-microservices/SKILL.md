# Skill: Keamanan API Microservices — Celah Antar-Layanan, Service Mesh & Trust Antar-Service

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 4, 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk lima program bounty resmi berikut — di luar itu tidak boleh dipakai:

1. **huntr** (HUNTR)
2. **Perplexity VDP** (PPLX)
3. **Mistral VDP** (MISTRAL)
4. **Anthropic** (ANTH)
5. **Muse** (MUSE)

Empat program lainnya (OpenAI Safety, 0din, Google AI VRP, ViKernel) BUKAN scope skill ini: Google AI VRP menilai hasil pada agen AI-nya (bukan celah web/API klasik) dan 0din/OpenAI Safety/ViKernel tidak memakai sudut microservices ini — jangan pakai skill ini untuk keempatnya.

## Pemicu

Dipakai saat target in-scope diketahui (atau diduga kuat) berarsitektur microservices — banyak layanan kecil di balik satu gateway, endpoint API yang memanggil layanan lain, atau dokumentasi yang menyebut service, mesh, gateway, atau komunikasi antar-layanan. Dipakai SETELAH inventaris API tersedia (`penemuan-api-swagger` untuk spesifikasi resmi, `perburuan-shadow-api-spa` untuk endpoint dari bundle JS) — skill ini menguji KEPERCAYAAN ANTAR-LAYANAN di balik API itu, bukan menginventarisasi endpointnya lagi.

Sudut yang dicari skill ini — dan hanya skill ini: apa yang terjadi DI ANTARA layanan, bukan di depan pengguna. Layanan A memanggil layanan B: apakah B memeriksa siapa yang memanggilnya, atau B percaya begitu saja karena "yang memanggil pasti layanan internal"? API internal yang seharusnya hanya bisa dijangkau sesama layanan: apakah masih bisa dijangkau dari luar lewat gateway? Kebijakan service mesh: apakah benar-benar membatasi siapa boleh memanggil siapa, atau hanya hiasan yang tidak ditegakkan?

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan arsitektur layanan + merumuskan hipotesis trust antar-service |
| Pengerjaan | **A62 Exploit Developer** | Menguji hipotesis antar-service secara aman dan read-only; menolak uji yang butuh aksi destruktif |
| Audit | **A60 Security Auditor** | Mengaudit bukti + keputusan triase (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan hipotesis mana yang maju ke pengujian dan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Penemuan dokumentasi API publik (OpenAPI/Swagger)** → skill `penemuan-api-swagger` (skill ini memakai daftar endpoint itu sebagai peta, bukan menemukannya ulang; dokumentasi yang terekspos BUKAN temuan skill ini).
- **Perburuan shadow API / endpoint dari bundle JS (termasuk path `/admin/...`, `/internal/...`, `/ops/...`)** → skill `perburuan-shadow-api-spa` (skill itu menginventarisasi + menguji liveness endpoint; skill ini menguji apakah endpoint internal itu bisa dipanggil TANPA identitas layanan yang sah dan apakah layanan di belakangnya memeriksa pemanggil — sudut trust antar-service yang tidak dibahas skill itu).
- **Pengujian otorisasi antar-AKUN pengguna (BOLA/IDOR, perbandingan respons lintas akun uji)** → skill `access-control-differential-analyst` (skill itu membandingkan User_A vs User_B; skill ini membandingkan LAYANAN pemanggil vs layanan lain — subjeknya berbeda: identitas service, bukan identitas pengguna).
- **Perburuan kerentanan spesifik (race condition, OAuth/SSO, dsb.)** → skill `perburuan-kerentanan-spesifik` (skill ini tidak mengulang kelas kerentanan itu; bila celah antar-service ternyata berwujud race condition atau cacat OAuth, pengujian lanjutannya lewat skill itu).
- **Fondasi kerentanan web/API secara umum** → skill `fondasi-kerentanan-web-api` (skill ini menambah sudut microservices di atas fondasi itu).
- **Pembuktian dampak umum + laporan triage-ready** → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.
- **Pola pikir penyerang (asumsi + jalur tersembunyi)** → skill `pola-pikir-penyerang-analitis` (dipakai untuk merumuskan hipotesis di skill ini; asumsi "internal = tepercaya" adalah salah satu asumsi yang diburu di sana).

## Aturan keras

1. **Hanya program bounty resmi in-scope** — lima program pada `Aturan utama` di atas (HUNTR, PPLX, MISTRAL, ANTH, MUSE). Di luar itu jangan diuji.
2. **Hanya akun uji SENDIRI.** Semua pengujian memakai akun tes milik sendiri dan data canary palsu — tanpa kecuali.
3. **Tanpa membaca data pengguna lain.** Pembuktian berhenti pada data milik akun sendiri; bila respons mengandung data pengguna lain, BERHENTI, jangan disimpan/dibaca lebih jauh, dan catat kejadiannya di log.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri gateway atau layanan dengan permintaan — volume uji kecil, berjeda, satu dimensi per putaran.
6. **Tanpa payload di permukaan publik.** Rencana uji dan bukti hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibuat, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai aksi yang menghapus/mengubah data (DROP, DELETE, UPDATE, hapus akun, transfer dana nyata) dan DILARANG mengubah konfigurasi layanan/mesh/gateway target. Pembuktian HARUS aman dan read-only: bukti baca atas data milik sendiri sudah cukup.

## Yang dicari (definisi singkat)

- **Autentikasi antar-service yang lemah / tidak ada:** layanan tujuan (service B) menerima panggilan tanpa memeriksa identitas pemanggil — tidak ada token identitas service, atau token apa pun diterima, atau token kedaluwarsa/tidak terikat layanan tertentu tetap diterima. Ciri khas: panggilan langsung ke layanan internal berhasil tanpa kredensial service yang sah, padahal dokumentasi/arsitektur menyatakan layanan itu "hanya untuk internal".
- **API internal yang terekspos lewat gateway:** endpoint yang ditujukan untuk komunikasi antar-layanan (mis. endpoint admin/ops/internal, endpoint antar-service) ternyata bisa dijangkau dari luar melalui API gateway — gateway meneruskan permintaan tanpa memeriksa apakah pemanggil berhak, atau rute internal tidak diblokir di gateway. Bukan temuan bila endpoint itu memang ditujukan untuk publik.
- **Misconfig service mesh:** kebijakan mesh (aturan siapa boleh memanggil siapa, enkripsi antar-service, identitas workload) tidak ditegakkan: lalu lintas antar-service berjalan tanpa identitas terverifikasi, kebijakan akses antar-service mengizinkan semua pemanggil, atau satu layanan yang berhasil dikompromikan secara teori bisa memanggil layanan lain tanpa batas. Yang dinilai adalah KEBIJAKAN YANG TIDAK DITEGAKKAN, bukan sekadar keberadaan mesh.
- **Broken Access Control antar-service:** layanan A (dengan hak terbatas) bisa meminta layanan B melakukan aksi di luar wewenang A — mis. layanan notifikasi memanggil layanan pembayaran untuk membaca data transaksi, atau layanan publik memanggil layanan internal untuk membaca data yang bukan bagiannya. Pembuktian: permintaan dari konteks layanan berhak-rendah mengembalikan data/aksi milik konteks lain — selalu dengan akun uji sendiri.
- **Bukan temuan (umumnya):** endpoint internal yang memang tidak bisa dijangkau dari luar (gateway memblokir, mesh menolak) — itu AMAN, tutup dengan buktinya; layanan yang meminta identitas service dan menolak token yang salah — itu AMAN; dan perbedaan perilaku antar-layanan yang tidak mengubah data/akses apa pun.

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah target microservices ini in-scope, apakah pengujian API diizinkan, apakah otomasi dilarang (huntr "Humans only" = uji manual saja).
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu permintaan uji pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan arsitektur layanan (dari sumber yang sah)

1. Kumpulkan peta layanan dari sumber yang sudah ada: spesifikasi OpenAPI (`penemuan-api-swagger`), endpoint dari bundle JS (`perburuan-shadow-api-spa`), dokumentasi publik target, dan header respons yang menyebut gateway/service (nama gateway, ID layanan, jejak routing).
2. Untuk tiap layanan catat: nama/peran, endpoint yang diekspos, apakah endpoint itu publik atau internal (dari dokumentasi/penamaan), dan layanan apa yang diduga memanggilnya.
3. **Standar lulus:** peta layanan tertulis (minimal: gateway + 2 layanan + hubungan pemanggil-dipanggil). Tanpa peta = jangan menebak arsitektur; itu tebakan buta.

### Gerbang 2 — Uji autentikasi antar-service

1. Pilih satu layanan tujuan yang diduga internal. Kirim permintaan ke endpointnya TANPA identitas service apa pun (tanpa token service, tanpa header identitas layanan) — memakai akun uji sendiri bila endpoint itu juga mengenal autentikasi pengguna.
2. Ulangi dengan identitas service yang TIDAK SAH: token milik layanan lain (bila bisa diperoleh secara sah dari akun sendiri), token yang sudah kedaluwarsa, atau token dengan cakupan layanan yang berbeda.
3. Bandingkan respons: apakah layanan membedakan pemanggil sah vs tidak sah (menolak yang tidak sah), atau semua varian diterima sama?
4. **Standar lulus:** hasil tiap varian tercatat (tanpa identitas / identitas salah / identitas layanan lain → diterima/ditolak). Bila identitas service diperiksa dengan benar = AMAN untuk layanan ini, tutup dengan buktinya dan lanjut ke layanan berikut.

### Gerbang 3 — Uji eksposur API internal lewat gateway

1. Dari peta Gerbang 1, pilih endpoint internal (admin/ops/antar-service). Coba jangkau dari luar melalui gateway publik — dengan akun uji sendiri, permintaan baca saja.
2. Variasikan cara gateway meneruskan permintaan: path persis, path dengan awalan versi berbeda, dan pemakaian header yang biasa dipakai gateway untuk routing internal — SATU variasi per putaran, catat respons tiap variasi.
3. **Standar lulus:** tiap variasi punya respons tercatat (diteruskan/diblokir + status). Bila gateway memblokir semua variasi = AMAN, tutup dengan buktinya. Bila satu variasi diteruskan dan mengembalikan data milik akun sendiri = lanjut ke Gerbang 6 (bukti + triase); bila mengembalikan data orang lain = BERHENTI (aturan keras 3) dan laporkan kejadiannya ke Muse.

### Gerbang 4 — Uji kebijakan mesh / segmentasi antar-service

1. Tentukan kebijakan yang diklaim target: dari dokumentasi publik atau perilaku yang teramati, layanan mana yang BOLEH memanggil layanan mana, dan apakah lalu lintas antar-service wajib memakai identitas terverifikasi.
2. Uji dari konteks berhak-rendah yang sah dimiliki (akun uji sendiri / layanan publik yang bisa dijangkau): coba panggil layanan yang menurut kebijakan seharusnya TIDAK bisa dipanggil dari konteks itu — permintaan baca saja, volume kecil.
3. **Standar lulus:** hasil uji vs kebijakan tertulis berdampingan (kebijakan melarang X, uji menunjukkan X bisa/tidak bisa). Kebijakan yang ditegakkan = AMAN; kebijakan yang tidak ditegakkan + akses terbukti = temuan, lanjut ke Gerbang 6.

### Gerbang 5 — Uji Broken Access Control antar-service

1. Pilih pasangan layanan: layanan pemanggil berhak-rendah (mis. layanan publik/notifikasi) dan layanan tujuan yang menyimpan data/aksi sensitif.
2. Kirim permintaan atas nama konteks berhak-rendah untuk membaca data atau memicu aksi yang hanya boleh dilakukan konteks berhak-tinggi — SELALU atas data milik akun uji sendiri (mis. minta layanan B menampilkan data transaksi milik akun sendiri lewat jalur layanan A yang tidak berhak).
3. Bandingkan dengan permintaan yang sama lewat jalur yang sah (konteks berhak-tinggi milik sendiri): bila jalur berhak-rendah mengembalikan hasil yang sama dengan jalur sah, kontrol akses antar-service GAGAL.
4. **Standar lulus:** perbandingan jalur berhak-rendah vs jalur sah tercatat dengan respons persis. Tanpa perbandingan = belum terbukti (bisa jadi layanan itu memang terbuka untuk semua konteks internal).

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal yang dikumpulkan: respons read-only atas data milik akun sendiri yang membuktikan (a) identitas service tidak diperiksa, (b) API internal bisa dijangkau dari luar, (c) kebijakan mesh tidak ditegakkan, atau (d) kontrol akses antar-service gagal — dengan langkah reproduksi persis (endpoint + variasi identitas + respons).
2. Tulis dampak konkret: layanan/aksi apa yang bisa dijangkau pihak yang tidak berhak, dan data/aksi milik siapa yang terdampak (hanya akun sendiri yang dibuktikan; dampak terhadap pengguna lain ditulis sebagai RISIKO yang wajar, bukan sebagai hal yang sudah dibuktikan dengan data mereka).
3. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
4. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah + perbandingan (varian diterima vs ditolak, atau jalur rendah vs jalur sah) + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Klien HTTP / curl | Kirim SATU permintaan per uji dengan variasi identitas service; hanya bila program mengizinkan alat itu |
| Spesifikasi OpenAPI + endpoint dari bundle JS | Peta arsitektur layanan — dari `penemuan-api-swagger` + `perburuan-shadow-api-spa` |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua variasi identitas, respons gateway/mesh, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + target + layanan tujuan]
Peta layanan: [gateway — layanan pemanggil → layanan tujuan]
Kelas celah: [autentikasi antar-service lemah / API internal terekspos / misconfig mesh / BAC antar-service]
Uji identitas service: [tanpa identitas: diterima/ditolak — identitas salah: diterima/ditolak — identitas layanan lain: diterima/ditolak]
Uji gateway: [endpoint internal — variasi — diteruskan/diblokir]
Uji mesh/segmentasi: [kebijakan yang diklaim — hasil uji]
Uji BAC antar-service: [jalur berhak-rendah vs jalur sah — respons]
Bukti read-only: [respons atas data milik akun sendiri]
Yang TIDAK dilakukan: [tanpa baca data orang lain, tanpa ubah konfigurasi, tanpa aksi destruktif]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Arsitektur microservices dari luar hanya bisa dipetakan sebagian — peta Gerbang 1 adalah dugaan terbaik dari sumber publik; layanan yang tidak terlihat dari luar tidak bisa diuji dan dicatat sebagai "tidak terpetakan", bukan "aman".
- Gateway dan mesh bisa berperilaku berbeda per rute — hasil pada satu endpoint tidak boleh digeneralisasi ke semua endpoint; tiap endpoint diuji sendiri.
- Identitas service yang sah (token antar-layanan asli) umumnya tidak bisa diperoleh penguji luar — karena itu Gerbang 2 menguji dari sisi NEGATIF (tanpa identitas / identitas salah): bila layanan menolak semua varian negatif, itu bukti kontrolnya bekerja; bila menerima, itu temuan.
- Skill ini tidak membahas keamanan container/orchestrator (Kubernetes RBAC, secret management) — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
