# Skill: SSRF & OAST — Server Out-of-Band untuk SSRF Blind + Akses Metadata Cloud

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 30).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada parameter yang berisi URL/alamat dan server yang mengambilnya — ambil gambar dari URL, webhook, pratinjau tautan, impor dari URL, konversi dokumen dari URL, atau proxy gambar/PDF. Dipakai juga saat SSRF diduga BLIND (tidak ada isi respons yang kembali) sehingga bukti hanya bisa didapat lewat callback out-of-band. Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) — skill ini adalah panduan PENGUJIAN operasionalnya, termasuk penyiapan server OAST.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menyiapkan canary OAST, menguji parameter URL, mendokumentasikan bukti callback |
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan parameter URL + membaca pasal scope soal metadata internal |
| Audit | **A60 Security Auditor** | Memvalidasi bukti callback sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep SSRF + standar pembuktian dampak secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian blind + penyiapan OAST, bukan mengulang konsepnya).
- SSRF lewat JAWABAN AI yang dirender (payload lahir dari jawaban model, bukan dari parameter URL) → skill `output-tidak-aman` (vektor berbeda — jangan dicampur; skill ini khusus parameter URL/server-side fetch klasik).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Payload Collaborator lewat MCP Burp (alat) → skill `mcp-burp-repeater` + `mcp-burp-ultra` (skill ini soal METODOLOGI SSRF-nya; alat Burp hanya salah satu cara menyiapkan canary).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.** Server canary (OAST) milik sendiri; satu ID unik per uji.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target atau canary dengan permintaan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai SSRF untuk menyerang layanan internal (memanggil endpoint admin internal, mengubah data internal, memicu aksi di layanan lain). Pembuktian HARUS aman: cukup callback canary OAST milik sendiri.
11. **METADATA CLOUD — CEK PASAL SCOPE DULU.** Alamat metadata cloud (`169.254.169.254`, `metadata.google.internal`) HANYA boleh diuji bila pasal scope program secara eksplisit mengizinkan pengujian metadata internal. Bila scope tidak menyebutkannya, atau ragu — JANGAN akses metadata sungguhan; bukti callback canary milik sendiri SUDAH CUKUP untuk membuktikan SSRF. Mengakses kredensial cloud sungguhan tanpa izin eksplisit = pelanggaran.
12. **Jangan membaca isi layanan internal.** Bila respons SSRF mengembalikan isi layanan internal, JANGAN menyimpan/membaca isinya lebih jauh dari yang perlu untuk membuktikan jangkauan (cukup status + bukti server menghubungi alamat itu). Jangan mengekstrak data dari layanan internal.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + pasal metadata dulu

1. Baca pasal scope program: (a) apakah pengujian SSRF diizinkan pada target ini? (b) apakah pengujian metadata cloud/internal diizinkan secara eksplisit? (c) apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** ketiga jawaban tercatat di log sebelum satu payload pun dikirim. Metadata TIDAK diizinkan secara eksplisit = Gerbang 4 dan 5 tidak dijalankan; bukti berhenti di callback canary (Gerbang 3).

### Gerbang 1 — Petakan parameter URL

1. Cari permukaan SSRF: parameter berisi URL (`url=`, `image=`, `webhook=`, `callback=`, `file=`, `preview=`), fitur impor/unggah-dari-URL, pratinjau tautan, dan header yang diteruskan sebagai URL (mis. `Referer`, `Host` pada fitur tertentu).
2. Untuk tiap parameter catat: apakah server benar-benar mengambil URL itu (respons berisi isi URL / waktu respons bertambah / error fetch), atau hanya menyimpannya.
3. **Standar lulus:** daftar parameter URL tertulis dengan bukti awal "server mengambil URL ini". Parameter yang hanya disimpan tanpa di-fetch = bukan SSRF, jangan diuji lanjut.

### Gerbang 2 — Siapkan server OAST (canary) milik sendiri

1. Siapkan server canary: Interactsh (self-hosted atau layanan resmi) atau Burp Collaborator milik sendiri. Satu subdomain/ID unik per uji supaya satu hit tidak tertukar dengan uji lain.
2. Canary hanya mencatat: waktu, IP peminta, path/ID unik, dan (bila ada) header dasar. Canary TIDAK menyimpan data apa pun selain log akses itu.
3. **Standar lulus:** canary aktif + teruji menerima hit dari luar (uji dengan `curl` dari mesin sendiri ke URL canary, pastikan tercatat) SEBELUM dipakai untuk SSRF. Canary yang belum teruji = bukti nanti tidak bisa dipercaya.

### Gerbang 3 — Uji SSRF blind via callback canary

1. Kirim URL canary sebagai nilai parameter (satu parameter per uji, satu ID unik per uji): `url=https://<id-unik>.canary-milik-sendiri/uji-ssrf-1`.
2. Tunggu dan periksa log canary: apakah ada hit dari IP server target (bukan IP sendiri)? Catat waktu kirim vs waktu hit.
3. Variasikan bila tidak ada hit: skema (`http` vs `https`), URL tanpa path, parameter di body vs query string, dan (bila diizinkan program) pengalih internal — SATU variasi per putaran, sesuai `rekonstruksi-iterasi-payload`.
4. **Standar lulus (gerbang utama):** hit canary tercatat dengan ID unik yang cocok + IP peminta adalah server target. Tanpa hit = BELUM BERHASIL — catat kenapa gagal, variasikan, ulangi. Hit dari IP sendiri (mis. karena pratinjau di browser sendiri) = BUKAN bukti SSRF, jangan diklaim.

### Gerbang 4 — Uji jangkauan internal (HANYA bila Gerbang 0 mengizinkan metadata/internal)

1. Bila scope mengizinkan: uji alamat internal yang TIDAK menyimpan kredensial dulu, mis. `http://169.254.169.254/latest/meta-data/` HANYA untuk melihat apakah terjangkau — dan BERHENTI bila respons berisi kredensial/token (jangan dibaca/disimpan/dipakai).
2. Bila scope TIDAK mengizinkan: lewati gerbang ini sepenuhnya — bukti Gerbang 3 sudah cukup untuk laporan.
3. **Standar lulus:** ada bukti server mencapai alamat internal (status respons / hit canary lanjutan) TANPA satu pun kredensial/token yang dibaca, disimpan, atau dipakai. Kredensial terbaca = pelanggaran aturan 11, hentikan uji dan laporkan pelanggaran itu ke Muse.

### Gerbang 5 — Buktikan dampak, serahkan ke triase

1. Tulis dampak konkret: apa yang bisa dilakukan penyerang dengan SSRF ini (sesuai yang TERBUKTI — mis. "server menghubungi URL pilihan penyerang" + jangkauan internal bila Gerbang 4 lolos). Jangan klaim dampak yang tidak terbukti (mis. jangan klaim "bisa membaca kredensial cloud" bila hanya callback canary yang terbukti).
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti callback (log canary persis + payload persis + langkah reproduksi) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti callback = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Interactsh (self-hosted / layanan resmi) | Server OAST: hasilkan subdomain unik per uji, periksa log hit; hanya milik sendiri |
| Burp Collaborator (milik sendiri, via `mcp-burp-repeater`) | Alternatif canary OOB; satu payload sekali jalan, lalu cek interaksi yang kembali |
| Permintaan HTTP manual / Burp Repeater | Kirim SATU payload URL per uji; hanya bila program mengizinkan alat itu |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload URL (nilai → hit canary ya/tidak → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter URL]
Pasal scope metadata: [diizinkan eksplisit / tidak disebut / dilarang]
Server OAST: [Interactsh / Burp Collaborator — ID unik per uji]
Payload: [URL canary persis yang dikirim]
Bukti callback: [log canary: waktu, IP peminta, path/ID unik — atau "TIDAK ADA"]
Jangkauan internal: [hanya bila Gerbang 0 mengizinkan — alamat + status, tanpa kredensial]
Dampak: [apa yang didapat penyerang, sesuai bukti]
Yang TIDAK dilakukan: [tanpa serang layanan internal, tanpa baca kredensial cloud]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- SSRF blind yang tidak memicu callback bisa disebabkan WAF/egress-filter, bukan tidak adanya celah — hasil negatif pada satu parameter bukan berarti seluruh aplikasi aman.
- Hit canary dari IP yang bukan server target (mis. CDN/proxy pihak ketiga) harus diselidiki sebelum diklaim sebagai bukti — catat IP peminta persis.
- Skill ini tidak membahas SSRF pada protokol non-HTTP (gopher, dict, ftp) — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
