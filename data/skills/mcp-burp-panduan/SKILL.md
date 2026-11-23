# Skill: MCP Burp Panduan — Wiring server PortSwigger ke Codex, Gemini CLI, Ollama, LM Studio + template prompt

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel Medium Abhishek Meena, "Top 43 AI Security Skills, MCP Servers & GitHub Repos Every Bug Hunter Needs" (14 Sep 2026), bagian "MCP servers — The Burp question" (`~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`). Belum pernah dipakai dalam perburuan nyata oleh tim; langkah wiring dan isi template di bawah ini belum terverifikasi langsung. Baca dan uji dulu di lab sendiri sebelum wiring untuk program bounty apa pun.

## Pemicu (kapan dipakai)

- **BACA INI SEBELUM WIRING SENDIRI.** A64 Web Application Tester hendak menghubungkan MCP server PortSwigger ke klien lain selain Claude Desktop — Codex, Gemini CLI, Ollama, atau LM Studio — dan belum tahu konfigurasi yang benar.
- Dipakai untuk menyiapkan wiring sekali, lalu memakai ulang template prompt IDOR/SSRF/auth-flow untuk pengujian web klasik.
- Dipakai HANYA untuk program web klasik in-scope (mis. huntr) — lihat Aturan Keras poin 9. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menyiapkan wiring MCP ke klien yang dipilih, memakai template prompt, memvalidasi temuan |
| Pemimpin | **Muse** | Memutuskan klien/target mana yang dipakai; menyetujui laporan sebelum dikirim |

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
11. **Wiring lokal dulu, target belakangan.** Jangan menghubungkan MCP server ke target bounty sebelum koneksi diuji di lab (Gerbang 1). Kredensial/config klien tidak boleh berisi rahasia apa pun — tanpa kunci/token/kata sandi di file konfigurasi.
12. **Template adalah titik mulai, bukan perintah otomatis.** Template prompt di skill ini harus dibaca, disesuaikan ke target in-scope, dan disetujui A64 per pemakaian — jangan dijalankan mentah-mentah sebagai rangkaian otomatis.

## Alat

| Alat | Repo GitHub | Cara pakai |
|---|---|---|
| burp-mcp-agents | six2dez / burp-mcp-agents (~230 bintang) | Panduan wiring MCP server PortSwigger ke Codex, Gemini CLI, Ollama, dan LM Studio + template prompt IDOR/SSRF/auth-flow yang bisa dipakai ulang. Ikuti README repo ini langkah demi langkah; jangan mengarang konfigurasi. |
| MCP server resmi PortSwigger (mcp-server) | PortSwigger — cari "mcp-server" di organisasi PortSwigger di GitHub (~1.2k bintang) | Server yang di-wiring: SSE server port 9876 + stdio proxy untuk Claude Desktop (lihat skill `mcp-burp-official`). |
| Klien MCP (pilih satu) | Codex / Gemini CLI / Ollama / LM Studio | Klien yang menerima konfigurasi MCP dari panduan burp-mcp-agents. Pilih SATU klien per sesi; jangan wiring ke banyak klien sekaligus. |
| SkillSpector (NVIDIA) | SkillSpector / NVIDIA (~17k bintang) | Pindai panduan/repo sebelum dipakai — cek prompt injection, eksfiltrasi data, dan supply-chain. Baca apa yang dilakukan MCP server dengan histori Burp sebelum konek. |

Catatan: isi konfigurasi persis per klien (nama file, format JSON, flag CLI) **BELUM DIUJI** — ambil dari README repo burp-mcp-agents saat wiring, jangan mengarang.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target (standar lulus: SEMUA terpenuhi)

1. Program target adalah program web klasik in-scope (mis. huntr) dan targetnya in-scope — buktikan dengan membaca halaman scope program, catat URL + tanggal cek.
2. Cek larangan otomasi program: bila program melarang otomasi (huntr "Humans only"), template prompt hanya dipakai sebagai panduan manual, BUKAN sebagai rangkaian otomatis. Bila ragu, tanya Muse dulu.
3. **Standar lulus:** scope tertulis di log; status larangan otomasi tercatat. Satu gagal = STOP, jangan lanjut.

### Gerbang 1 — Wiring di lab (standar lulus: koneksi terbukti, tanpa rahasia)

1. Pindai repo burp-mcp-agents dengan SkillSpector (atau baca README + kodenya) sebelum dipakai — catat hasilnya.
2. Jalankan Burp Suite + MCP server resmi PortSwigger (lihat skill `mcp-burp-official`).
3. Ikuti panduan burp-mcp-agents untuk SATU klien yang dipilih (Codex, Gemini CLI, Ollama, atau LM Studio); tulis konfigurasinya tanpa rahasia apa pun.
4. Uji koneksi di lab: dari klien itu, panggil satu tool MCP baca-saja (mis. proxy history) dan pastikan respons kembali.
5. **Standar lulus:** tool baca-saja berhasil dari klien yang dipilih; file konfigurasi tidak berisi kunci/token/kata sandi. Bila gagal, catat errornya, jangan lanjut ke target.

### Gerbang 2 — Pilih dan sesuaikan template (standar lulus: template disetujui A64)

1. Pilih SATU template dari panduan (IDOR, SSRF, atau auth-flow) yang cocok dengan target.
2. Sesuaikan template ke target in-scope: ganti placeholder dengan host/path/parameter nyata dari proxy history; hapus bagian yang tidak relevan; tambahkan batasan (akun sendiri + canary palsu saja).
3. A64 membaca template yang sudah disesuaikan dan menyetujuinya SEBELUM dipakai.
4. **Standar lulus:** template yang disesuaikan tertulis di log; persetujuan A64 tercatat; belum ada request uji yang dikirim.

### Gerbang 3 — Jalankan template, satu hipotesis sekali jalan (standar lulus: bukti nyata)

1. Jalankan template yang disetujui lewat klien MCP — satu hipotesis, satu request uji.
2. Simpan request/response lengkap sebagai bukti; bandingkan dengan perilaku normal (baseline).
3. Ulangi hanya untuk hipotesis berikutnya setelah yang sebelumnya dicatat hasilnya.
4. **Standar lulus:** tiap hipotesis punya bukti request/response yang bisa diulang; tidak ada payload di permukaan publik; tidak ada banjir request.

### Gerbang 4 — Validasi manusia + laporan (standar lulus: disetujui Cipta)

1. A64 memvalidasi sendiri tiap temuan (ulangi manual di Burp tanpa agen) — AI bantu, manusia putuskan.
2. Tulis draf laporan (lihat Format output); kirim ke Muse untuk audit.
3. **Standar lulus:** temuan terulang manual oleh manusia; draf laporan lengkap; laporan TIDAK dikirim ke program sebelum Cipta menyetujui.

## Template prompt (titik mulai — sesuaikan per target, jangan jalankan mentah)

> Semua template di bawah ini **BELUM DIUJI**. Isi placeholder `[...]` dengan nilai nyata dari target in-scope sebelum dipakai, dan minta persetujuan A64 dulu.

### Template A — IDOR

```
Target in-scope: [host + path endpoint, mis. /api/users/{id}]
Akun: hanya akun saya sendiri + canary palsu [nilai canary].
Baseline: ambil objek milik akun saya, catat respons normal (status, body).
Uji: minta objek yang sama dengan ID milik canary palsu, SATU request.
Bandingkan: apakah respons mengembalikan data canary? Bila ya, simpan request/response sebagai bukti dan STOP — jangan lanjut ke ID lain.
Bila tidak, catat gagal dan berhenti.
```

### Template B — SSRF

```
Target in-scope: [host + path endpoint yang menerima URL, mis. /api/fetch?url=]
Akun: hanya akun saya sendiri.
Uji: SATU request dengan URL ke Collaborator milik saya sendiri [URL Collaborator unik].
Buktikan: cek interaksi yang kembali di Collaborator — cocok dengan token unik payload?
Bila ya, simpan request/response + bukti Collaborator dan STOP.
Bila tidak, catat gagal dan berhenti. Jangan arahkan SSRF ke host internal/orang lain.
```

### Template C — Auth-flow

```
Target in-scope: [host + alur login/reset/otorisasi]
Akun: hanya akun saya sendiri + canary palsu [nilai canary].
Baseline: jalankan alur normal dengan akun saya, catat tiap langkah + respons.
Uji: ulangi alur dengan SATU penyimpangan (mis. lewati satu langkah, tukar token antar akun sendiri/canary) — SATU penyimpangan per uji.
Bandingkan: apakah alur menerima penyimpangan itu? Bila ya, simpan bukti dan STOP.
Bila tidak, catat gagal dan berhenti.
```

## Format output

- **Log kerja:** `~/workspace/catatan/log-bug-bounty.md` — satu entri per sesi: tanggal, program, target in-scope, klien MCP yang di-wiring, template yang dipakai (A/B/C) + penyesuaiannya, hasil per hipotesis, bukti (path file request/response).
- **Konfigurasi wiring:** simpan file konfigurasi klien (tanpa rahasia) di folder kerja sesi; sebutkan path-nya di log.
- **Bukti request/response:** simpan file mentah (`.http`/`.txt`) di folder kerja sesi, sebutkan path-nya di log.
- **Draf laporan:** dokumen draf (bukan pengiriman) — berisi ringkasan, langkah reproduksi (template + nilai yang dipakai), bukti, dampak, dan saran perbaikan; diserahkan ke Muse untuk audit, lalu ke Cipta untuk persetujuan sebelum dikirim ke program.
- **Verdict jujur di tiap entri:** tulis "TERVERIFIKASI MANUAL" bila sudah diulang manusia, atau "BELUM DIUJI / BELUM TERVERIFIKASI" bila belum.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Burp Suite, MCP server resmi PortSwigger, dan klien MCP (Codex / Gemini CLI / Ollama / LM Studio) dijalankan lokal.

## Websites

- Repo burp-mcp-agents — six2dez / burp-mcp-agents di GitHub (~230 bintang, panduan wiring + template prompt).
- Repo MCP server resmi PortSwigger — cari "mcp-server" di organisasi PortSwigger di GitHub (~1.2k bintang).
- Ringkasan sumber artikel: `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md` (bagian "MCP servers — The Burp question").
- Panduan umum bikin skill: `~/workspace/catatan/panduan-bikin-skill-2026-11-23.md`.

## Alternatives for better results

- Bila memakai Claude Desktop saja (tanpa wiring klien lain): pakai skill `mcp-burp-official` — tidak perlu skill ini.
- Bila butuh ~150 tools, fuzzing, dan kontrol scanner: lihat skill `mcp-burp-ultra` (BurpMCP-Ultra, butuh Burp Pro).
- Bila hanya butuh kirim-ulang request (Repeater untuk LLM): lihat skill `mcp-burp-repeater`.
- Bila targetnya bounty agen AI (bukan web klasik): JANGAN pakai skill ini — pakai skill kategori target aplikasi AI (garak, promptfoo, PyRIT, AgentDojo).
