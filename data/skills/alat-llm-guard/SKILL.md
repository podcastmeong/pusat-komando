# Skill: llm-guard — Scanning Input/Output Interaksi LLM (ProtectAI)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil llm-guard sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu memahami lapisan pertahanan yang harus dicoba ditembus — llm-guard memindai input dan output interaksi LLM (injeksi, secrets, toksisitas). Pelajari apa yang ditangkapnya, lalu rancang varian yang lolos dari lapisannya.
- **Pemilik:** **A60 Security Auditor** (Tim 1 — Muse).
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
| llm-guard | https://github.com/protectai/llm-guard (~3.2k bintang, ProtectAI) | `pip install llm-guard` lalu jalankan scanner input/output (mis. `llm-guard scan` — **BELUM DIUJI**, cek dokumentasi repo untuk perintah yang benar) terhadap interaksi LLM di lingkungan uji sendiri. **BELUM DIUJI** — daftar scanner (injeksi, secrets, toksisitas), format output, dan cara memasangnya sebagai lapisan uji belum terverifikasi di lingkungan kita. |

- llm-guard adalah lapisan yang harus dicoba ditembus: pahami dulu apa yang ditangkap tiap scanner-nya sebelum merancang varian.
- Jangan kirim data asli (secrets/prompt asli program) ke scanner di lingkungan yang tidak kita kendalikan; pakai canary palsu.

## Langkah + gerbang

1. **Tentukan scanner yang dipelajari** (injeksi / secrets / toksisitas) dan kaitannya dengan program target. Standar lulus: scanner + program tercatat.
2. **Jalankan llm-guard pada interaksi uji sendiri.** Standar lulus: hasil scan tersimpan (apa yang ditangkap, apa yang lolos).
3. **Analisis celah: varian apa yang lolos dari tiap scanner dan kenapa.** Standar lulus: ada catatan mekanisme celah per scanner.
4. **Rancang varian dari celah itu; reproduksi manual di akun sendiri pada target in-scope.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji transfer ke program lain, catat per program.** Standar lulus: hasil per program tercatat di log.
6. **Audit (A60) + draf laporan (A67).** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Hasil scan + analisis celah per scanner: `~/workspace/catatan/log-bug-bounty.md` (tanggal, scanner, apa yang ditangkap/lolos, mekanisme celah, hasil adaptasi per program).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
