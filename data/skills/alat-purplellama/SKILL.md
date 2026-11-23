# Skill: PurpleLlama — Benchmark Defensif Meta (CyberSecEval, LlamaGuard, Klasifikasi Injeksi)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil PurpleLlama sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu memahami pertahanan yang harus ditembus — sisi riset defensif. Jalankan benchmark CyberSecEval, LlamaGuard, dan klasifikasi injeksi untuk mempelajari apa yang dideteksi pertahanan, lalu rancang serangan yang lolos dari deteksi itu.
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
| PurpleLlama | https://github.com/meta-llama/PurpleLlama (~4.4k bintang, Meta) | Klon repo; komponennya: CyberSecEval (benchmark keamanan), LlamaGuard (klasifikasi keamanan input/output), dan klasifikasi injeksi. **BELUM DIUJI** — perintah tiap komponen dan cara menjalankan benchmark/klasifikasi belum terverifikasi di lingkungan kita; cek README repo sebelum menjalankan. |

- PurpleLlama adalah alat defensif/riset: pakai untuk memahami apa yang dideteksi, bukan untuk menyerang langsung.
- Hasil klasifikasi LlamaGuard bukan bukti temuan — bukti tetap reproduksi manual pada target in-scope.

## Langkah + gerbang

1. **Tentukan pertanyaan defensifnya:** apa yang dideteksi LlamaGuard/klasifikasi injeksi, dan di mana celahnya. Standar lulus: pertanyaan tercatat, kaitannya dengan program target jelas.
2. **Jalankan benchmark/klasifikasi yang relevan di lab.** Standar lulus: hasil tersimpan (apa yang terdeteksi, apa yang lolos).
3. **Analisis celah: pola apa yang lolos dari deteksi dan kenapa.** Standar lulus: ada catatan mekanisme celah, bukan hanya daftar skor.
4. **Rancang serangan dari celah itu; reproduksi manual di akun sendiri pada target in-scope.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji transfer ke program lain, catat per program.** Standar lulus: hasil per program tercatat di log.
6. **Audit (A60) + draf laporan (A67).** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Hasil benchmark/klasifikasi + analisis celah: `~/workspace/catatan/log-bug-bounty.md` (tanggal, komponen yang dipakai, apa yang terdeteksi/lolos, mekanisme celah, hasil adaptasi per program).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
