# Skill: Giskard — Scanning Agen LLM (Injeksi + Halusinasi), Kuat di CI

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil Giskard sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu memindai agen LLM untuk injeksi prompt dan halusinasi — terutama sebagai pemeriksaan berulang (misalnya dipasang di CI pada agen/repo sendiri) atau sebagai pemetaan awal sebelum uji manual ke target program.
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
| Giskard | https://github.com/Giskard-AI/giskard (~5.8k bintang) | `pip install giskard` lalu `giskard scan` terhadap model/agen; kuat bila dipasang di CI. **BELUM DIUJI** — perintah scan, format laporan, dan cara mengarahkan ke agen target kita belum terverifikasi di lingkungan kita; cek dokumentasi repo sebelum menjalankan. |

- Giskard memindai agen — pakai pada agen sendiri / lingkungan uji sendiri sebagai pemetaan; hasil scan bukan temuan bounty sampai direproduksi manual pada target in-scope.
- Jangan pasang scan otomatis berulang ke endpoint program tanpa memastikan batas rate dan aturan otomasi program itu.

## Langkah + gerbang

1. **Tentukan agen/model yang dipindai + program kaitannya.** Standar lulus: program in-scope, kategori (injeksi/halusinasi) tidak masuk daftar out-of-scope di Aturan keras.
2. **Jalankan scan Giskard pada lingkungan uji sendiri.** Standar lulus: laporan scan tersimpan lengkap.
3. **Baca laporan: pisahkan temuan scan dari noise.** Standar lulus: tiap kandidat punya deskripsi jelas + langkah reproduksi.
4. **Reproduksi manual kandidat terbaik di akun sendiri pada target in-scope.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji transfer ke program lain (adaptasi minimal), catat per program.** Standar lulus: hasil per program tercatat di log.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Laporan scan Giskard + ringkasan saring: `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, agen yang dipindai, ringkasan temuan, kandidat yang lolos saring).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
