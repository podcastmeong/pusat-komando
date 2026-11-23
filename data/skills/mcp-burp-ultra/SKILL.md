# Skill: MCP Burp Ultra — BurpMCP-Ultra dengan ~150 tools untuk pengujian web klasik mendalam

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel Medium Abhishek Meena, "Top 43 AI Security Skills, MCP Servers & GitHub Repos Every Bug Hunter Needs" (14 Sep 2026), bagian "MCP servers — The Burp question" (`~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`). Belum pernah dipakai dalam perburuan nyata oleh tim; jumlah tool, nama kategori, dan perilaku server di bawah ini belum terverifikasi langsung. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu (kapan dipakai)

- A64 Web Application Tester sudah melewati titik mulai (`mcp-burp-official`) dan butuh kemampuan lebih dalam: proxy history, inline fuzzing, kontrol scanner/crawl, Collaborator OOB, guided probes (SQLi/SSTI/IDOR), serangan JWT, dan panen endpoint dari JavaScript.
- Dipakai HANYA untuk program web klasik in-scope (mis. huntr) — lihat Aturan Keras poin 9. Bukan untuk bounty agen AI.
- Dipakai HANYA bila Burp Pro tersedia (syarat server ini).

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menjalankan Burp Pro + BurpMCP-Ultra, mengarahkan agen memakai tool MCP, memvalidasi temuan |
| Pemimpin | **Muse** | Memutuskan program/target mana yang dikerjakan; menyetujui laporan sebelum dikirim |

## Aturan keras

1. Hanya program bounty resmi in-scope (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. Hanya akun sendiri + canary palsu.
3. Tanpa data orang lain.
4. Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).
5. Tanpa DoS/DDoS.
6. Tanpa payload di permukaan publik.
7. Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).
8. Tanpa laporan tanpa persetujuan Cipta.
9. Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **PENTING untuk kategori ini: alat Burp/MCP recon adalah alat KLASIK — HANYA untuk program web klasik (mis. huntr), BUKAN untuk bounty agen AI (Muse, OpenAI, 0din, Google AI VRP, ViKernel).** Jangan memakai skill ini untuk menyerang permukaan agen AI; untuk itu pakai skill kategori target aplikasi AI (garak, promptfoo, PyRIT, AgentDojo).
11. **Khusus skill ini: butuh Burp Pro.** Tanpa lisensi Burp Pro, jangan paksakan — kembali ke `mcp-burp-official` (server resmi PortSwigger).
12. **Fuzzing terkendali saja.** Inline fuzzing dan scanner/crawl hanya pada endpoint in-scope, dengan laju rendah dan jumlah request kecil. Fuzzing massal/otomatis tanpa pengawasan = pelanggaran Aturan Keras poin 5 dan 9.

## Alat

| Alat | Repo GitHub | Cara pakai |
|---|---|---|
| BurpMCP-Ultra | Cy-S3c / BurpMCP-Ultra (~220 bintang) | MCP server untuk Burp Pro dengan ~150 tools dalam 37 kategori. Hubungkan klien MCP ke server ini setelah Burp Pro berjalan; agen memanggil tool per kategori (lihat langkah). |
| Burp Suite Professional | portswigger.net/burp | Wajib — BurpMCP-Ultra butuh Burp Pro. |
| Burp Collaborator | bawaan Burp Pro | Untuk pengujian out-of-band (OOB): pakai Collaborator milik sendiri; jangan pakai Collaborator/interaksi pihak ketiga yang menyimpan data orang lain. |
| SkillSpector (NVIDIA) | SkillSpector / NVIDIA (~17k bintang) | Pindai skill/MCP sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. Baca apa yang dilakukan MCP server dengan histori Burp sebelum konek. |

Catatan: daftar 37 kategori dan nama tool persis **BELUM DIUJI** — ambil dari README repo BurpMCP-Ultra saat instalasi, jangan mengarang nama tool.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target (standar lulus: SEMUA terpenuhi)

1. Program target adalah program web klasik in-scope (mis. huntr) dan targetnya in-scope — buktikan dengan membaca halaman scope program, catat URL + tanggal cek.
2. Cek larangan otomasi program: bila program melarang otomasi (huntr "Humans only"), tool scanner/crawl/fuzzing otomatis DILARANG dipakai — hanya tool baca (proxy history, panen endpoint) yang boleh. Bila ragu, tanya Muse dulu.
3. Pastikan Burp Pro aktif dan lisensinya sah.
4. **Standar lulus:** scope tertulis di log; status larangan otomasi tercatat; Burp Pro jalan. Satu gagal = STOP, jangan lanjut.

### Gerbang 1 — Siapkan server + pindai keamanan (standar lulus: koneksi + pindaian bersih)

1. Jalankan Burp Pro; pastikan proxy aktif.
2. Pindai repo BurpMCP-Ultra dengan SkillSpector (atau baca README + kodenya) sebelum install — catat hasilnya.
3. Jalankan BurpMCP-Ultra sesuai README; dari klien MCP, panggil satu tool baca-saja (mis. proxy history) dan pastikan respons kembali.
4. **Standar lulus:** tool baca-saja berhasil; tidak ada temuan supply-chain yang belum dijelaskan. Bila gagal, catat errornya, jangan lanjut.

### Gerbang 2 — Panen permukaan (standar lulus: peta tercatat, belum ada serangan)

1. Jelajahi target lewat browser yang diproxy Burp.
2. Pakai tool MCP: baca proxy history, lalu panen endpoint dari file JavaScript (JS endpoint harvesting) untuk menemukan API/path tersembunyi.
3. Susun peta permukaan: host, path, parameter, header auth — tanpa mengirim payload.
4. **Standar lulus:** peta permukaan tercatat di log; belum ada request uji berbahaya yang dikirim.

### Gerbang 3 — Guided probes, satu hipotesis sekali jalan (standar lulus: bukti nyata per probe)

1. Pilih SATU endpoint + SATU hipotesis (SQLi, SSTI, IDOR, JWT, atau SSRF — pakai guided probe server ini, bukan fuzzing buta).
2. A64 meninjau dan menyetujui hipotesis + payloadnya SEBELUM dikirim. Payload hanya ke target in-scope, dengan akun sendiri + canary palsu.
3. Untuk dugaan OOB (mis. SSRF/blind SQLi): pakai Burp Collaborator milik sendiri, satu payload sekali jalan, lalu cek interaksi yang kembali.
4. Simpan request/response lengkap sebagai bukti.
5. **Standar lulus:** tiap probe punya hipotesis tertulis + bukti request/response yang bisa diulang; tidak ada payload di permukaan publik; tidak ada banjir request.

### Gerbang 4 — Scanner/crawl hanya bila diizinkan (standar lulus: izin tercatat + hasil ditriase manusia)

1. Bila — dan hanya bila — program mengizinkan scanner/crawl otomatis: jalankan crawl/scan terbatas pada path in-scope, laju rendah.
2. Triase SEMUA temuan scanner secara manual: sebagian besar temuan scanner adalah false positive.
3. **Standar lulus:** izin program tercatat di log; tiap temuan yang diteruskan sudah divalidasi manual oleh A64. Bila program melarang otomasi, gerbang ini DILEWATI (tulis "dilewati — program melarang otomasi" di log).

### Gerbang 5 — Validasi manusia + laporan (standar lulus: disetujui Cipta)

1. A64 memvalidasi sendiri tiap temuan (ulangi manual di Burp tanpa agen) — AI bantu, manusia putuskan.
2. Tulis draf laporan (lihat Format output); kirim ke Muse untuk audit.
3. **Standar lulus:** temuan terulang manual oleh manusia; draf laporan lengkap; laporan TIDAK dikirim ke program sebelum Cipta menyetujui.

## Format output

- **Log kerja:** `~/workspace/catatan/log-bug-bounty.md` — satu entri per sesi: tanggal, program, target in-scope, status larangan otomasi, tool/kategori MCP yang dipakai, endpoint yang diuji, hasil (lolos/gagal), bukti (path file request/response).
- **Peta permukaan:** daftar host/path/parameter hasil Gerbang 2, disimpan bersama log sesi (atau file terpisah yang path-nya disebut di log).
- **Bukti request/response:** simpan file mentah (`.http`/`.txt`) di folder kerja sesi, sebutkan path-nya di log.
- **Draf laporan:** dokumen draf (bukan pengiriman) — berisi ringkasan, langkah reproduksi, bukti, dampak, dan saran perbaikan; diserahkan ke Muse untuk audit, lalu ke Cipta untuk persetujuan sebelum dikirim ke program.
- **Verdict jujur di tiap entri:** tulis "TERVERIFIKASI MANUAL" bila sudah diulang manusia, atau "BELUM DIUJI / BELUM TERVERIFIKASI" bila belum.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Burp Suite Professional dan BurpMCP-Ultra dijalankan lokal; klien MCP adalah Claude Desktop atau agen yang mendukung MCP.

## Websites

- Repo BurpMCP-Ultra — Cy-S3c / BurpMCP-Ultra di GitHub (~220 bintang, ~150 tools, 37 kategori).
- Ringkasan sumber artikel: `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md` (bagian "MCP servers — The Burp question").
- Panduan umum bikin skill: `~/workspace/catatan/panduan-bikin-skill-2026-11-23.md`.

## Alternatives for better results

- Bila belum punya Burp Pro: pakai skill `mcp-burp-official` (server resmi PortSwigger) dulu.
- Bila hanya butuh kirim-ulang request (Repeater untuk LLM): lihat skill `mcp-burp-repeater`.
- Bila belum tahu cara wiring server ke Codex/Gemini CLI/Ollama/LM Studio: baca skill `mcp-burp-panduan` DULU sebelum wiring sendiri.
- Bila targetnya bounty agen AI (bukan web klasik): JANGAN pakai skill ini — pakai skill kategori target aplikasi AI (garak, promptfoo, PyRIT, AgentDojo).
