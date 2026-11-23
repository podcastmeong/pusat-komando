# Skill: MCP Burp Official — AI-assisted Burp lewat server MCP resmi PortSwigger

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel Medium Abhishek Meena, "Top 43 AI Security Skills, MCP Servers & GitHub Repos Every Bug Hunter Needs" (14 Sep 2026), bagian "MCP servers — The Burp question" (`~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`). Belum pernah dipakai dalam perburuan nyata oleh tim; langkah instalasi, nama tool, dan perilaku server di bawah ini belum terverifikasi langsung. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu (kapan dipakai)

- A64 Web Application Tester perlu memberi agen AI "tangan" ke Burp Suite — membaca proxy history, memeriksa request/response, dan menguji ulang request — lewat MCP, bukan lewat salin-tempel manual.
- Dipakai sebagai **titik mulai utama** untuk "AI-assisted Burp": sebelum mencoba server MCP Burp pihak ketiga (mcp-burp-ultra, mcp-burp-repeater), mulai dari server resmi ini dulu.
- Dipakai HANYA untuk program web klasik in-scope (mis. huntr) — lihat Aturan Keras poin 9.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menjalankan Burp + MCP server, mengarahkan agen memakai tool MCP, memvalidasi temuan |
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

## Alat

| Alat | Repo GitHub | Cara pakai |
|---|---|---|
| MCP server resmi PortSwigger (mcp-server) | PortSwigger — cari "mcp-server" di organisasi PortSwigger di GitHub (~1.2k bintang) | Jalankan sebagai SSE server di port 9876, atau lewat stdio proxy untuk Claude Desktop. Hubungkan klien MCP (Claude Desktop / agen) ke server ini; agen lalu memanggil tool MCP untuk berinteraksi dengan Burp yang sedang berjalan. |
| Burp Suite (Community atau Professional) | portswigger.net/burp | Burp harus sudah berjalan dan proxy aktif sebelum MCP server dihubungkan. |
| SkillSpector (NVIDIA) | SkillSpector / NVIDIA (~17k bintang) | Pindai skill/MCP sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. Baca apa yang dilakukan MCP server dengan histori Burp sebelum konek. |

Catatan: detail perintah instalasi/peluncuran persis (nama paket, flag CLI) **BELUM DIUJI** — ambil dari README repo resmi saat instalasi, jangan mengarang flag.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target (standar lulus: SEMUA terpenuhi)

1. Program target adalah program web klasik in-scope (mis. huntr) dan targetnya in-scope — buktikan dengan membaca halaman scope program, catat URL + tanggal cek.
2. Cek larangan otomasi program: bila program melarang otomasi (huntr "Humans only"), MCP hanya dipakai sebagai pembaca/penolong manual, BUKAN sebagai eksekutor otomatis. Bila ragu, tanya Muse dulu.
3. **Standar lulus:** scope tertulis di log; tidak ada langkah yang menyentuh target di luar scope; tidak ada langkah otomatis yang melanggar aturan program. Satu gagal = STOP, jangan lanjut.

### Gerbang 1 — Siapkan lab (standar lulus: koneksi MCP terbukti)

1. Jalankan Burp Suite; pastikan proxy mendengarkan dan browser diarahkan lewat proxy Burp.
2. Jalankan MCP server resmi PortSwigger (SSE port 9876, atau stdio proxy untuk Claude Desktop) sesuai README repo.
3. Dari klien MCP, panggil satu tool baca-saja (mis. daftar proxy history / status) dan pastikan respons kembali.
4. **Standar lulus:** tool baca-saja berhasil mengembalikan data dari Burp yang sedang berjalan; tidak ada error koneksi. Bila gagal, catat errornya, jangan lanjut ke pengujian target.

### Gerbang 2 — Recon lewat MCP (standar lulus: jejak tercatat)

1. Jelajahi target lewat browser yang diproxy Burp; minta agen merangkum proxy history lewat MCP: host, path, parameter, dan metode autentikasi yang terlihat.
2. Tandai endpoint menarik (form login, API, parameter yang diteruskan ke backend) — tanpa mengirim payload apa pun dulu.
3. **Standar lulus:** daftar endpoint + parameter tercatat di log; belum ada request berbahaya yang dikirim.

### Gerbang 3 — Uji manual berbantuan AI (standar lulus: bukti nyata)

1. Untuk tiap endpoint menarik, agen mengusulkan SATU hipotesis kerentanan + SATU request uji (bukan fuzzing massal).
2. A64 meninjau hipotesis itu, menyetujui, lalu request dikirim lewat Burp (manual atau lewat MCP) — dengan akun sendiri + canary palsu saja.
3. Simpan request/response lengkap sebagai bukti.
4. **Standar lulus:** tiap temuan punya bukti request/response yang bisa diulang; tidak ada payload di permukaan publik; tidak ada DoS.

### Gerbang 4 — Validasi manusia + laporan (standar lulus: disetujui Cipta)

1. A64 memvalidasi sendiri tiap temuan (ulangi manual di Burp tanpa agen) — AI bantu, manusia putuskan.
2. Tulis draf laporan (lihat Format output); kirim ke Muse untuk audit.
3. **Standar lulus:** temuan terulang manual oleh manusia; draf laporan lengkap; laporan TIDAK dikirim ke program sebelum Cipta menyetujui.

## Format output

- **Log kerja:** `~/workspace/catatan/log-bug-bounty.md` — satu entri per sesi: tanggal, program, target in-scope, alat yang dipakai, endpoint yang diuji, hasil (lolos/gagal), bukti (path file request/response).
- **Bukti request/response:** simpan file mentah (`.http`/`.txt`) di folder kerja sesi, sebutkan path-nya di log.
- **Draf laporan:** dokumen draf (bukan pengiriman) — berisi ringkasan, langkah reproduksi, bukti, dampak, dan saran perbaikan; diserahkan ke Muse untuk audit, lalu ke Cipta untuk persetujuan sebelum dikirim ke program.
- **Verdict jujur di tiap entri:** tulis "TERVERIFIKASI MANUAL" bila sudah diulang manusia, atau "BELUM DIUJI / BELUM TERVERIFIKASI" bila belum.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Burp Suite dan MCP server resmi PortSwigger dijalankan lokal; klien MCP adalah Claude Desktop atau agen yang mendukung MCP.

## Websites

- Repo MCP server resmi PortSwigger — cari "mcp-server" di organisasi PortSwigger di GitHub (~1.2k bintang).
- Ringkasan sumber artikel: `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md` (bagian "MCP servers — The Burp question").
- Panduan umum bikin skill: `~/workspace/catatan/panduan-bikin-skill-2026-11-23.md`.

## Alternatives for better results

- Bila butuh tool lebih banyak (±150 tools, fuzzing, scanner control): lihat skill `mcp-burp-ultra` (BurpMCP-Ultra, butuh Burp Pro).
- Bila hanya butuh kirim-ulang request (Repeater untuk LLM): lihat skill `mcp-burp-repeater`.
- Bila belum tahu cara wiring server ke Codex/Gemini CLI/Ollama/LM Studio: baca skill `mcp-burp-panduan` DULU sebelum wiring sendiri.
- Bila targetnya bounty agen AI (bukan web klasik): JANGAN pakai skill ini — pakai skill kategori target aplikasi AI (garak, promptfoo, PyRIT, AgentDojo).
