# Skill: AgentDojo — Benchmark Prompt Injection terhadap Agen (ETH Zurich, NeurIPS)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil AgentDojo sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu lab dinamis untuk menguji serangan dan pertahanan prompt injection pada sistem agen — benchmark NeurIPS untuk melihat pola injeksi mana yang berhasil melawan agen, sebelum pola itu diadaptasi ke target program kita.
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
| AgentDojo | https://github.com/ethz-spylab/agentdojo (~820 bintang, ETH Zurich) | Klon repo dan jalankan benchmark prompt injection terhadap agen di lab; pakai sebagai tempat belajar pola serangan/pertahanan. **BELUM DIUJI** — cara menjalankan benchmark, daftar tugas injeksi, dan cara mengadaptasi pola ke target kita belum terverifikasi di lingkungan kita; cek README repo sebelum menjalankan. |

- AgentDojo adalah lab/benchmark, bukan target: pola yang berhasil di lab belum tentu berhasil di program nyata — adaptasi dan reproduksi manual tetap wajib.
- Jangan salin mentah serangan lab ke permukaan publik; uji hanya di akun sendiri dalam scope.

## Langkah + gerbang

1. **Pilih tugas benchmark yang relevan** (jenis injeksi + jenis agen). Standar lulus: tugas tercatat, kaitannya dengan program target jelas.
2. **Jalankan benchmark di lab.** Standar lulus: hasil benchmark tersimpan (pola mana berhasil, mana gagal, dan kenapa).
3. **Pilih pola yang berhasil di lab dan pahami mekanismenya** (bukan sekadar salin teks). Standar lulus: ada catatan mekanisme pola, bukan hanya prompt mentah.
4. **Adaptasi pola ke target program in-scope; reproduksi manual di akun sendiri.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji transfer ke program lain, catat per program.** Standar lulus: hasil per program tercatat di log.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Hasil benchmark + catatan mekanisme pola: `~/workspace/catatan/log-bug-bounty.md` (tanggal, tugas benchmark, pola berhasil/gagal, adaptasi ke program, hasil per program).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
