# Skill: Trail of Bits Skills — Audit Kode & Aturan Deteksi ala Auditor Profesional

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026), bukan pengalaman teruji. Semua langkah di bawah ini belum pernah dijalankan tim; uji dulu di satu kasus kecil sebelum dipakai untuk laporan bounty.

## Pemicu (kapan dipakai)

- Ada kode sumber (C/C++, Rust, smart contract, workflow GitHub Actions) yang diduga mengandung kerentanan dan perlu diaudit secara sistematis sebelum dilaporkan.
- Ada pola kerentanan baru yang perlu dijadikan aturan deteksi (Semgrep/YARA) agar bisa dipakai ulang di audit berikutnya.
- A58 butuh metode audit yang rapi (bukan sekadar "baca kode lalu tebak") untuk temuan di program bounty.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Jalankan skill audit, tulis temuan + bukti |
| Pemeriksa | **A60 Security Auditor** | Audit ulang temuan A58 sebelum draf laporan |
| Pemimpin | **Muse** | Putuskan temuan mana yang naik ke draf laporan |

## Sumber

- Repo: **trailofbits/skills** — https://github.com/trailofbits/skills (~7–8k bintang, lisensi CC-BY-SA-4.0).
- Koleksi skill/plugin Claude Code dari Trail of Bits; instal: `/plugin marketplace add trailofbits/skills` di Claude Code, atau `npx skills add trailofbits/skills`.
- Skill yang relevan untuk kita: `c-review` (review keamanan C/C++ lengkap, output SARIF), `rust-review` (review Rust: batas safe/unsafe, memory safety, konkurensi, panic-DoS, FFI, async), `semgrep-rule-creator` (buat aturan Semgrep baru), `semgrep-rule-variant-creator` (porting aturan Semgrep ke bahasa lain, validasi berbasis tes), `yara-authoring` (buat aturan YARA), `constant-time-analysis` (deteksi timing side-channel di kode kripto), `supply-chain-risk-auditor` (audit risiko dependensi), `static-analysis` (CodeQL + Semgrep + parsing SARIF), `differential-review` (review perubahan kode dengan konteks git), `agentic-actions-auditor` (audit workflow GitHub Actions untuk kerentanan integrasi agen AI).

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — temuan AI bukan temuan sampai manusia memverifikasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu (standar lulus: program + target tertulis di log sebelum audit dimulai)

1. Tulis di `~/workspace/catatan/log-bug-bounty.md`: program, target in-scope, dan batas yang berlaku.
2. Bila target di luar scope → BERHENTI. Jangan audit.

### Gerbang 1 — Pilih skill audit yang tepat (standar lulus: 1 skill dipilih + alasannya dicatat)

1. Kode C/C++ → `c-review`; Rust → `rust-review`; pola baru → `semgrep-rule-creator`; dependensi → `supply-chain-risk-auditor`; kode kripto → `constant-time-analysis`.
2. Jangan load semua skill sekaligus — pilih yang sesuai target.

### Gerbang 2 — Jalankan audit dengan bukti (standar lulus: tiap temuan punya file + baris + bukti reproduksi)

1. Jalankan skill audit pada kode target (kode sendiri / kode program in-scope yang terbuka untuk audit).
2. Catat tiap kandidat temuan: file, baris, alasan, dan bukti (output tool / potongan kode).
3. Temuan tanpa bukti = BUKAN temuan. Jangan diteruskan.

### Gerbang 3 — Saring false positive (standar lulus: tiap temuan dicek manual oleh A58, yang tidak terbukti dicoret dengan alasan)

1. Uji tiap kandidat: apakah benar-benar bisa dieksploitasi / melanggar aturan program?
2. Buat aturan Semgrep/YARA dari pola yang terbukti, bila pola itu bisa muncul lagi — uji aturan itu pada kode bersih (harus TIDAK berbunyi) dan kode rentan (harus berbunyi).

### Gerbang 4 — Serahkan ke auditor (standar lulus: A60 memeriksa ulang dan menandai SETUJU / TOLAK per temuan)

1. A58 serahkan daftar temuan + bukti ke A60.
2. Hanya temuan yang disetujui A60 yang masuk draf laporan (lihat skill `laporan-abstrak` / `triase-duplikat` untuk langkah berikutnya).

## Alat

| Alat | Repo / cara pakai |
|---|---|
| trailofbits/skills (c-review, rust-review, semgrep, YARA, constant-time, supply-chain) | https://github.com/trailofbits/skills — `/plugin marketplace add trailofbits/skills` |
| Semgrep | `pip install semgrep` lalu `semgrep --config <aturan> <target>` |
| CodeQL | Unduh dari GitHub codeql; dipakai lewat skill `static-analysis` |
| YARA | `yara <aturan.yar> <target>` — aturan dibuat lewat skill `yara-authoring` |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per temuan: tanggal | program | target | skill dipakai | temuan | bukti | status (kandidat / terverifikasi A58 / disetujui A60).
- Draf laporan: ikut format skill `laporan-abstrak`; jangan kirim sebelum Cipta setuju.
- Aturan Semgrep/YARA yang terbukti jalan disimpan di repo Pusat Komando (folder skill ini, bila ada `references/` di masa depan — saat ini hanya SKILL.md).

## Batasan yang diketahui (BELUM DIUJI)

- Repo ini marketplace plugin Claude Code; cara pakainya di lingkungan tim kita (bukan Claude Code) belum diuji.
- Jumlah skill di repo berubah-ubah (30+ plugin, ~97 file skill menurut sumber berbeda) — daftar di atas bisa kedaluwarsa; cek README repo sebelum memakai.
- Lisensi CC-BY-SA-4.0: bila kita menurunkan/membagikan skill turunan, wajib mencantumkan Trail of Bits dan memakai lisensi yang sama.
