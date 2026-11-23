# Skill: AI-Infra-Guard — Red Teaming Full-Stack AI (Tencent)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil AI-Infra-Guard sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu menguji lebih dari sekadar model — seluruh tumpukan AI: agent scan, skills scan, MCP scan, AI infra scan, dan jailbreak evaluation. Cocok untuk temuan supply-chain AI, bukan cuma kelemahan model.
- **Pemilik:** **A63 Format Analyst** (Tim 4 — Google AI VRP, analisis format).
- **Program sasaran:** 5 program AI kita — Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel. Bukan untuk program web klasik.

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
10. System prompt extraction OUT OF SCOPE di Google AI VRP dan 0din (dan N/A untuk Muse Spark) — jangan kejar di program itu.
11. Direct prompt injection / jailbreak / halusinasi / bocor system prompt OUT OF SCOPE di Google AI VRP — hanya indirect injection yang in-scope di sana.
12. Tim 4 Google = analisis format saja, tanpa payload live.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| AI-Infra-Guard | https://github.com/Tencent/AI-Infra-Guard (~6.3k bintang, Tencent) | Klon repo dan jalankan modul scan yang dibutuhkan (agent scan, skills scan, MCP scan, AI infra scan, jailbreak evaluation). **BELUM DIUJI** — perintah tiap modul, format output, dan cara mengarahkan ke target kita belum terverifikasi di lingkungan kita; cek README repo sebelum menjalankan. |

- AI-Infra-Guard mencakup supply chain AI: periksa juga skill/MCP dari sumber anonim sebelum dipakai (aturan supply-chain kita — cek dulu, jangan asal install).
- Scan infra hanya terhadap aset sendiri / dalam scope program; jangan memindai infrastruktur di luar scope.

## Langkah + gerbang

1. **Tentukan modul + target.** Tulis program dan modul yang dipakai (agent/skills/MCP/infra/jailbreak eval). Standar lulus: target in-scope, modul tidak menyentuh kategori out-of-scope di Aturan keras.
2. **Jalankan satu modul dulu (mulai dari yang paling sempit).** Standar lulus: log modul tersimpan lengkap.
3. **Saring hasil per modul; pisahkan temuan dari noise.** Standar lulus: tiap kandidat punya deskripsi + langkah reproduksi.
4. **Reproduksi manual kandidat terbaik di akun sendiri.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji transfer ke program lain, catat per program.** Standar lulus: hasil per program tercatat di log.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Log per modul + ringkasan saring: `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, modul, ringkasan hasil, kandidat yang lolos saring).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
