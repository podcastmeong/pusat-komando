# Skill: MCP Burp Repeater — "Repeater for LLMs" (simpan dan kirim ulang request lewat agen)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel Medium Abhishek Meena, "Top 43 AI Security Skills, MCP Servers & GitHub Repos Every Bug Hunter Needs" (14 Sep 2026), bagian "MCP servers — The Burp question" (`~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`). Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku server di bawah ini belum terverifikasi langsung. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu (kapan dipakai)

- A64 Web Application Tester perlu memberi agen kemampuan Repeater: menyimpan sebuah request, mengubahnya sedikit (mis. regex-modified resends), lalu mengirim ulangnya — tanpa salin-tempel manual antara Burp dan agen.
- Dipakai untuk pengujian out-of-band (OOB): menghasilkan payload Collaborator lewat agen untuk menguji SSRF/blind injection.
- Dipakai HANYA untuk program web klasik in-scope (mis. huntr) — lihat Aturan Keras poin 9. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menjalankan Burp + BurpMcp, mengarahkan agen menyimpan/mengubah/mengirim ulang request, memvalidasi temuan |
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
11. **Satu perubahan, satu kirim ulang.** Regex-modified resend hanya mengubah SATU hal dalam satu kirim ulang (satu parameter, satu header, satu nilai) supaya penyebab hasil jelas. Mengubah banyak hal sekaligus = hasil tidak bisa diatribusikan.
12. **Jangan jadikan Repeater sebagai fuzzer.** Kirim ulang dilakukan satu per satu dengan persetujuan A64 per request. Pengiriman massal/otomatis dilarang — itu fuzzing tanpa pengawasan dan melanggar Aturan Keras poin 5 dan 9.

## Alat

| Alat | Repo GitHub | Cara pakai |
|---|---|---|
| BurpMcp | swgee / BurpMcp (~60 bintang) | MCP server "Repeater for LLMs": simpan request, kirim ulang lewat agen, regex-modified resends, dan Collaborator payload generation untuk OOB testing. Hubungkan klien MCP ke server ini setelah Burp berjalan. |
| Burp Suite (Community atau Professional) | portswigger.net/burp | Burp harus sudah berjalan dan proxy aktif sebelum MCP server dihubungkan. |
| Burp Collaborator | bawaan Burp (Pro) / layanan Collaborator | Untuk pengujian OOB: pakai Collaborator milik sendiri; jangan pakai layanan pihak ketiga yang menyimpan data orang lain. |
| SkillSpector (NVIDIA) | SkillSpector / NVIDIA (~17k bintang) | Pindai skill/MCP sebelum install — cek prompt injection, eksfiltrasi data, dan supply-chain. Baca apa yang dilakukan MCP server dengan histori Burp sebelum konek. |

Catatan: nama tool dan perintah peluncuran persis **BELUM DIUJI** — ambil dari README repo BurpMcp saat instalasi, jangan mengarang nama tool atau flag.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target (standar lulus: SEMUA terpenuhi)

1. Program target adalah program web klasik in-scope (mis. huntr) dan targetnya in-scope — buktikan dengan membaca halaman scope program, catat URL + tanggal cek.
2. Cek larangan otomasi program: bila program melarang otomasi (huntr "Humans only"), kirim ulang hanya dilakukan atas perintah manual A64 per request, bukan rangkaian otomatis. Bila ragu, tanya Muse dulu.
3. **Standar lulus:** scope tertulis di log; status larangan otomasi tercatat. Satu gagal = STOP, jangan lanjut.

### Gerbang 1 — Siapkan server (standar lulus: simpan + kirim ulang terbukti di lab)

1. Jalankan Burp Suite; pastikan proxy aktif.
2. Pindai repo BurpMcp dengan SkillSpector (atau baca README + kodenya) sebelum install — catat hasilnya.
3. Jalankan BurpMcp sesuai README; hubungkan klien MCP.
4. Uji di lab (bukan target bounty): simpan satu request, kirim ulang tanpa perubahan, pastikan respons kembali sama.
5. **Standar lulus:** simpan + kirim ulang tanpa perubahan berhasil dan respons cocok dengan aslinya. Bila gagal, catat errornya, jangan lanjut ke target.

### Gerbang 2 — Tangkap dan simpan request dasar (standar lulus: baseline tercatat)

1. Jelajahi target lewat browser yang diproxy Burp; pilih SATU request yang menarik (mis. ganti profil, panggil API, alur auth).
2. Simpan request itu lewat agen (BurpMcp) sebagai baseline; catat respons aslinya.
3. **Standar lulus:** request baseline + respons aslinya tersimpan dan bisa diulang; belum ada modifikasi yang dikirim.

### Gerbang 3 — Kirim ulang bermodifikasi, satu perubahan sekali jalan (standar lulus: bukti per perubahan)

1. Agen mengusulkan SATU modifikasi (mis. ubah nilai parameter via regex, tukar ID pengguna dengan canary palsu untuk uji IDOR, sisipkan payload Collaborator untuk uji OOB).
2. A64 meninjau dan menyetujui modifikasi itu SEBELUM dikirim. Modifikasi hanya ke target in-scope, dengan akun sendiri + canary palsu.
3. Kirim ulang, simpan request/response, bandingkan dengan baseline: apa yang berubah?
4. Ulangi untuk modifikasi berikutnya — satu per satu, jangan menumpuk.
5. **Standar lulus:** tiap kirim ulang punya satu perubahan yang tercatat + respons yang dibandingkan dengan baseline; tidak ada payload di permukaan publik; tidak ada banjir request.

### Gerbang 4 — Uji OOB dengan Collaborator (standar lulus: interaksi terbukti milik sendiri)

1. Bila hipotesis butuh bukti OOB (mis. SSRF/blind injection): minta agen menghasilkan SATU payload Collaborator lewat BurpMcp, kirim sekali, lalu cek interaksi yang kembali di Collaborator milik sendiri.
2. **Standar lulus:** interaksi Collaborator yang kembali cocok dengan payload yang dikirim (ID/token unik per payload); tidak ada data orang lain yang tersentuh.

### Gerbang 5 — Validasi manusia + laporan (standar lulus: disetujui Cipta)

1. A64 memvalidasi sendiri tiap temuan (ulangi manual di Burp Repeater tanpa agen) — AI bantu, manusia putuskan.
2. Tulis draf laporan (lihat Format output); kirim ke Muse untuk audit.
3. **Standar lulus:** temuan terulang manual oleh manusia; draf laporan lengkap; laporan TIDAK dikirim ke program sebelum Cipta menyetujui.

## Format output

- **Log kerja:** `~/workspace/catatan/log-bug-bounty.md` — satu entri per sesi: tanggal, program, target in-scope, status larangan otomasi, request baseline (path), tiap modifikasi + hasil perbandingannya dengan baseline, bukti (path file request/response).
- **Bukti request/response:** simpan file mentah (`.http`/`.txt`) di folder kerja sesi — baseline dan tiap kirim ulang — sebutkan path-nya di log.
- **Draf laporan:** dokumen draf (bukan pengiriman) — berisi ringkasan, langkah reproduksi (request baseline + modifikasi persis), bukti, dampak, dan saran perbaikan; diserahkan ke Muse untuk audit, lalu ke Cipta untuk persetujuan sebelum dikirim ke program.
- **Verdict jujur di tiap entri:** tulis "TERVERIFIKASI MANUAL" bila sudah diulang manusia, atau "BELUM DIUJI / BELUM TERVERIFIKASI" bila belum.

## Available connectors

Tidak ada konektor khusus untuk skill ini. Burp Suite dan BurpMcp dijalankan lokal; klien MCP adalah Claude Desktop atau agen yang mendukung MCP.

## Websites

- Repo BurpMcp — swgee / BurpMcp di GitHub (~60 bintang, "Repeater for LLMs").
- Ringkasan sumber artikel: `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md` (bagian "MCP servers — The Burp question").
- Panduan umum bikin skill: `~/workspace/catatan/panduan-bikin-skill-2026-11-23.md`.

## Alternatives for better results

- Bila butuh titik mulai yang paling aman: pakai skill `mcp-burp-official` (server resmi PortSwigger) dulu.
- Bila butuh ~150 tools, fuzzing, dan kontrol scanner: lihat skill `mcp-burp-ultra` (BurpMCP-Ultra, butuh Burp Pro).
- Bila belum tahu cara wiring server ke Codex/Gemini CLI/Ollama/LM Studio: baca skill `mcp-burp-panduan` DULU sebelum wiring sendiri.
- Bila targetnya bounty agen AI (bukan web klasik): JANGAN pakai skill ini — pakai skill kategori target aplikasi AI (garak, promptfoo, PyRIT, AgentDojo).
