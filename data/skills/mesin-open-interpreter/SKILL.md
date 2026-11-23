# Skill: Mesin Open Interpreter — Agen Eksekusi Kode General ("Duct Tape" Pipeline Agen)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** butuh agen eksekusi kode general untuk menyambung langkah-langkah pipeline agen — Open Interpreter (~68k ⭐), "duct tape" untuk pipeline agen. Ini BUKAN alat khusus keamanan: pakai hanya sebagai perekat antar-langkah, bukan sebagai mesin perburuan.
- **Pemilik:** **A70 Automation Engineer** (menjalankan + mengawasi; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan pipeline mana yang memakai Open Interpreter dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| Open Interpreter | github.com/OpenInterpreter/open-interpreter (~68k ⭐) | Clone repo, ikuti README; jalankan di terminal; beri instruksi langkah demi langkah; arahkan hanya ke target in-scope |
| Container/VM sekali pakai | — | Jalankan agen eksekusi kode orang lain HANYA di container/VM yang bisa dibuang, bukan di mesin utama |

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
10. **Batas peran (khusus skill ini):** Open Interpreter hanya perekat pipeline — ia mengeksekusi kode yang diperintahkan. Jangan suruh ia merancang serangan sendiri; rancangan serangan tetap dari manusia/A70, Open Interpreter hanya menjalankannya langkah demi langkah.

## Langkah + gerbang

1. **Gerbang 0 — Kelayakan tugas.** Pastikan tugasnya adalah menyambung langkah pipeline untuk target program web klasik in-scope — bukan perburuan otonom. Standar lulus: daftar langkah pipeline tertulis sebelum dijalankan; bila tugasnya bounty agen AI, STOP — pakai alat uji permukaan agen AI (garak/promptfoo/PyRIT/AgentDojo).
2. **Gerbang 1 — Tulis langkah dulu, baru jalankan.** Setiap langkah yang akan dieksekusi ditulis dan dibaca manusia SEBELUM diberikan ke Open Interpreter. Standar lulus: tidak ada langkah yang dijalankan tanpa dibaca manusia dulu.
3. **Gerbang 2 — Siapkan kandang.** Jalankan di container/VM sekali pakai dengan kunci LLM akun sendiri. Standar lulus: lingkungan terisolasi, bukan mesin utama.
4. **Gerbang 3 — Jalankan langkah demi langkah dengan pengawasan.** Satu langkah selesai → manusia memeriksa hasilnya → baru lanjut ke langkah berikut. Jangan biarkan Open Interpreter merantai langkah sendiri tanpa jeda pemeriksaan. Standar lulus: tiap hasil langkah diperiksa manusia; tidak ada langkah yang melompat sendiri.
5. **Gerbang 4 — Validasi temuan oleh manusia.** Setiap temuan direproduksi manual sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar Open Interpreter, dengan bukti.
6. **Gerbang 5 — Laporan.** Draf laporan → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Daftar langkah pipeline disimpan di log sebelum eksekusi (langkah, perintah, hasil yang diharapkan).
- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, langkah yang dijalankan, hasil per langkah, temuan, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- Open Interpreter adalah repo terbesar di kategori ini (~68k ⭐) justru karena ia general — bukan karena ia alat keamanan terbaik. Jangan tertipu angka bintang: untuk perburuan, framework khusus (PentAGI, Agentic-Bug-Hunter) lebih tepat; Open Interpreter hanya perekat.
- Risiko khusus: agen eksekusi kode bisa menjalankan perintah apa pun yang ia hasilkan. Gerbang 1 dan 3 (baca langkah dulu + periksa tiap hasil) adalah pengaman utamanya — jangan dilewati.
