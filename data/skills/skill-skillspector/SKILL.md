# Skill: SkillSpector — Pindai Skill/MCP Sebelum Install (Gerbang Wajib)

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026) + dokumentasi SkillSpector, bukan pengalaman teruji. Tool ini belum pernah dijalankan tim; jalankan pertama kali di satu skill kecil dan catat hasilnya sebelum dijadikan gerbang wajib.

## Pemicu (kapan dipakai)

- SEBELUM menginstal/memakai skill, plugin, atau MCP server dari pihak ketiga (termasuk semua skill di artikel 43 AI Security Skills: Trail of Bits, mukul975, Claude-Red, Raptor, BountyForge).
- SEBELUM me-load skill baru ke Pusat Komando atau ke Claude Code tim.
- Setiap kali ada skill/MCP baru yang diusulkan siapa pun — tanpa kecuali.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A60 Security Auditor** | Jalankan pemindaian, putuskan verdict per skill |
| Pendukung | **Agent pemilik skill yang diusulkan** | Sediakan sumber skill (URL/folder) untuk dipindai |
| Pemimpin | **Muse** | Putuskan bila verdict CAUTION: install atau tolak |

## Sumber

- Repo: **NVIDIA/skillspector** — https://github.com/NVIDIA/skillspector (lisensi Apache-2.0; ~17k bintang menurut artikel, ~24–27k menurut sumber November 2026).
- Deskripsi repo: "Security scanner for AI agent skills" — mendeteksi kerentanan, pola berbahaya, prompt injection, eksfiltrasi data, dan risiko supply-chain di skill Claude Code, Codex, dan MCP SEBELUM diinstal.
- Cara kerja: 71 pola kerentanan dalam 17 kategori (prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt leakage, memory poisoning, tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code via AST, taint tracking, YARA, MCP least privilege, MCP tool poisoning). Tahap 1 statis (regex, AST Python, taint tracking, YARA, cek OSV.dev); tahap 2 opsional LLM (menilai maksud: bandingkan klaim skill vs isi kodenya).
- Skor: 0–20 SAFE, 21–50 CAUTION, >50 DO NOT INSTALL. Temuan CRITICAL +50, HIGH +25, MEDIUM +10, LOW +5; pengali 1,3 bila skill berisi script executable.
- Instal: `uv tool install git+https://github.com/NVIDIA/skillspector.git`.
- Perintah dasar:
  - `skillspector scan ./my-skill/ --no-llm` — pindai folder skill, statis saja (tanpa LLM).
  - `skillspector scan https://github.com/user/my-skill` — pindai langsung dari URL GitHub.
  - `skillspector scan ./my-skill/ --format sarif --output report.sarif` — laporan SARIF.
  - `skillspector scan ./my-skill/ --format json` — laporan JSON.
  - `skillspector mcp` — jalankan sebagai MCP server.
- Batasan tool (menurut README): analisis statis saja, tidak mengeksekusi skill; "defense-in-depth, bukan sandbox" — hasil bersih BUKAN izin memberi skill akses luas. Pindai OSV mengirim nama+versi dependensi ke OSV.dev meski `--no-llm`; mode LLM mengirim isi file ke provider yang dikonfigurasi — JANGAN pakai mode LLM untuk skill yang berisi data sensitif.
- Konteks tim: skill adalah instruksi yang dijalankan agen dengan akses shell/file/jaringan kita. Dataset riset NVIDIA: dari 31.132 skill yang dianalisis, 26,1% mengandung kerentanan dan 5,2% menunjukkan kemungkinan niat jahat. Itu sebabnya gerbang ini wajib.

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — verdict scanner bukan verdict sampai A60 membaca laporannya.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**
11. **TIDAK ADA skill/MCP pihak ketiga yang diinstal tanpa pemindaian ini.** Verdict DO NOT INSTALL = dilarang install, tanpa kecuali. Verdict CAUTION = hanya Muse yang boleh memutuskan, dengan alasan tertulis.
12. **Jangan jalankan skill orang lain di mesin utama tanpa wadah sekali pakai.** Bila skill harus dicoba, jalankan di container/VM yang bisa dibuang.
13. **Mode LLM SkillSpector TIDAK dipakai untuk skill yang berisi data sensitif** (mode LLM mengirim isi file ke provider).

## Langkah + gerbang

### Gerbang 0 — Terima usulan skill (standar lulus: sumber skill tercatat: URL/folder + siapa yang mengusulkan + untuk program apa)

1. Catat di `~/workspace/catatan/log-bug-bounty.md`: tanggal, nama skill, sumber (URL/folder), pengusul, tujuan pemakaian.
2. Tanpa sumber yang jelas → TOLAK (tidak bisa dipindai = tidak bisa dipakai).

### Gerbang 1 — Baca manual dulu (standar lulus: SKILL.md + script yang menyertainya dibaca penuh oleh A60; ringkasan 3 baris tertulis: apa yang diklaim dilakukan skill ini)

1. Baca SKILL.md dan semua script yang dikirim bersama skill.
2. Periksa manual: adakah perintah yang mengirim data ke luar (curl ke host asing, upload, exfiltrasi)? Adakah instruksi tersembunyi (teks putih, komentar aneh, base64)?
3. Bila ada yang mencurigakan → langsung DO NOT INSTALL, catat alasannya, berhenti.

### Gerbang 2 — Pindai dengan SkillSpector (standar lulus: perintah scan selesai + skor + verdict tercatat)

1. Jalankan: `skillspector scan <sumber> --no-llm --format json` (tahap statis dulu; mode LLM hanya bila A60 memutuskan perlu).
2. Catat skor + verdict (SAFE / CAUTION / DO NOT INSTALL) + daftar temuan per kategori.
3. Verdict DO NOT INSTALL → TOLAK, catat di log, berhenti. Verdict CAUTION → lanjut ke Gerbang 3. Verdict SAFE → lanjut ke Gerbang 4.

### Gerbang 3 — Keputusan Muse untuk CAUTION (standar lulus: keputusan tertulis Muse: INSTALL dengan batasan / TOLAK, beserta alasannya)

1. A60 serahkan laporan pindai + ringkasan bacaan manual ke Muse.
2. Bila diizinkan: tulis batasan pemakaian (mis. hanya di container sekali pakai, hanya skill X, tanpa akses jaringan).

### Gerbang 4 — Install terbatas + catat (standar lulus: skill terinstal di lokasi yang benar + entri log lengkap + skill didaftarkan di agents.json bila skill Pusat Komando)

1. Install sesuai batasan Gerbang 3 (atau tanpa batasan bila SAFE).
2. Catat hasil di log; bila skill Pusat Komando, daftarkan di `data/agents.json` pada array `skills` agent pemiliknya (lihat panduan bikin skill).
3. Uji skill pada satu kasus kecil yang aman sebelum dipakai untuk kerja bounty.

## Alat

| Alat | Repo / cara pakai |
|---|---|
| SkillSpector | https://github.com/NVIDIA/skillspector — `uv tool install git+https://github.com/NVIDIA/skillspector.git`, lalu `skillspector scan <target> --no-llm` |
| OSV.dev | Dipakai otomatis oleh SkillSpector untuk cek CVE dependensi |
| Container/VM sekali pakai | Tempat menjalankan skill yang verdict-nya CAUTION |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per pemindaian: tanggal | nama skill | sumber | skor | verdict (SAFE/CAUTION/DO NOT INSTALL) | temuan utama | keputusan (install/tolak + batasan) | pemeriksa (A60).
- Laporan pindai (JSON/SARIF) disimpan di folder kerja skill yang dipindai, namanya dicatat di log.
- Skill yang DITOLAK dicatat juga (nama + sumber + alasan) supaya tidak diusulkan ulang sia-sia.

## Batasan yang diketahui (BELUM DIUJI)

- Tool belum pernah dijalankan tim; perintah di atas diambil dari dokumentasi, belum terverifikasi di lingkungan kita (butuh `uv` + Python).
- Jumlah pola (71 vs 68 menurut sumber berbeda) dan skor bisa berubah mengikuti versi tool.
- Analisis statis saja: skill yang berbahaya tapi lolos pola statis tetap bisa lolos — Gerbang 1 (baca manual) tidak boleh dilewati dengan alasan "scanner bilang aman".
