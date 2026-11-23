# Skill: Mesin HackingBuddyGPT — Bangun Agen Pengujian Keamanan LLM Sendiri

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** butuh agen pengujian keamanan LLM yang dirakit sendiri, kecil dan transparan — hackingBuddyGPT (ipa-lab, ~1.2k ⭐), dengan klaim "50 baris kode atau kurang" per agen, plus konektor SSH/shell/psexec.
- **Pemilik:** **A70 Automation Engineer** (merakit + menjalankan agen; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan agen mana yang dirakit dan target apa yang boleh diuji).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| hackingBuddyGPT | github.com/ipa-lab/hackingBuddyGPT (~1.2k ⭐) | Clone repo, ikuti README; rakit agen sendiri mengikuti contoh minimal di repo; arahkan hanya ke target in-scope |
| Konektor SSH / shell / psexec | (termasuk di repo hackingBuddyGPT) | Pakai hanya ke mesin sendiri / mesin lab sendiri — JANGAN ke mesin target atau mesin orang lain |
| Container/VM sekali pakai | — | Jalankan kode orang lain HANYA di container/VM yang bisa dibuang, bukan di mesin utama |

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr.
2. **Hanya akun sendiri + canary palsu; tanpa data orang lain.**
3. **Tanpa uji korban** — victim-agent fraud tests DIBLOKIR, jangan dicoba.
4. **Tanpa DoS/DDoS.**
5. **Tanpa payload di permukaan publik.**
6. **Validasi human-in-the-loop** — AI bantu, manusia putuskan dan validasi.
7. **Tanpa laporan tanpa persetujuan Cipta.**
8. **Patuhi larangan otomasi program** — huntr "Humans only"; Gray Swan dilewati total, jangan buat skill untuknya.
9. **Framework otonom di kategori ini HANYA untuk target in-scope dan HANYA dengan human-in-the-loop — jangan biarkan framework jalan sendiri tanpa pengawasan; untuk bounty agen AI, framework klasik ini hanya relevan bila targetnya program web klasik.**

## Langkah + gerbang

1. **Gerbang 0 — Kelayakan target.** Pastikan target adalah program web klasik in-scope. Standar lulus: nama program + aset in-scope tercatat; bila targetnya bounty agen AI, STOP — framework klasik ini tidak relevan (untuk uji permukaan agen AI pakai garak/promptfoo/PyRIT/AgentDojo).
2. **Gerbang 1 — Rakit agen minimal.** Tulis agen mengikuti contoh repo (target "50 baris kode atau kurang") — satu agen, satu tugas, kode yang bisa dibaca manusia sampai habis. Standar lulus: seluruh kode agen bisa dibaca dan dipahami A70 tanpa bantuan; tidak ada kode yang tidak dimengerti.
3. **Gerbang 2 — Pindai dulu sebelum jalankan.** Baca kode repo + kode agen sendiri (apa yang dijalankan, ke mana terhubung, data apa yang dibaca) — cek risiko prompt injection / eksfiltrasi. Standar lulus: tidak ada koneksi tak dikenal dan tidak ada perintah yang membaca data di luar target.
4. **Gerbang 3 — Uji di lab sendiri dulu.** Jalankan agen terhadap mesin lab sendiri (via konektor SSH/shell/psexec ke mesin sendiri) sebelum menyentuh target nyata. Standar lulus: agen berperilaku sesuai rancangan di lab; tidak ada aksi di luar yang diperintahkan.
5. **Gerbang 4 — Jalankan ke target dengan pengawasan.** Beri target in-scope; manusia memantau tiap aksi agen dan bisa menghentikan kapan saja. Standar lulus: tidak ada aksi di luar scope.
6. **Gerbang 5 — Validasi temuan oleh manusia.** Setiap temuan direproduksi manual sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar agen, dengan bukti.
7. **Gerbang 6 — Laporan.** Draf laporan → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Kode agen disimpan di repo kerja tim (satu file per agen, dengan komentar: tugas agen, target, tanggal dibuat).
- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, agen yang dipakai, temuan, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- Nilai utama hackingBuddyGPT: transparansi. Agen yang dirakit sendiri dan kodenya pendek bisa diaudit manusia sampai habis — kebalikan dari framework besar yang perilakunya sulit ditebak.
- Konektor SSH/shell/psexec HANYA ke mesin sendiri. Memakai konektor ini ke mesin target atau mesin orang lain = pelanggaran aturan keras nomor 2 dan 3.
- Jangan simpan kredensial apa pun (kunci SSH, kata sandi) di dalam kode agen atau di skill ini.
