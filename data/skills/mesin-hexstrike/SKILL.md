# Skill: Mesin HexStrike AI — 150+ Tools di Balik 12+ Agen Otonom via MCP

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** target adalah program web klasik in-scope dan butuh banyak tools sekaligus (150+ tools) yang dikoordinasikan 12+ agen otonom lewat MCP — HexStrike AI (0x4m4, ~12k ⭐).
- **Pemilik:** **A70 Automation Engineer** (menjalankan + mengawasi framework; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan target mana yang boleh diuji dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| HexStrike AI | github.com/0x4m4/HexStrike-AI (~12k ⭐) | Clone repo, ikuti README; konfigurasikan server MCP yang dibutuhkan; arahkan hanya ke target in-scope |
| Server MCP terkait | (lihat README HexStrike) | Aktifkan hanya server MCP yang dibutuhkan untuk target — jangan aktifkan semuanya sekaligus |
| Container/VM sekali pakai | — | Jalankan framework orang lain HANYA di container/VM yang bisa dibuang, bukan di mesin utama |

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

1. **Gerbang 0 — Kelayakan target.** Pastikan target adalah program web klasik in-scope. Standar lulus: nama program + aset in-scope tercatat; bila targetnya bounty agen AI, STOP — framework ini tidak relevan.
2. **Gerbang 1 — Pilih tools yang dibutuhkan saja.** Dari 150+ tools, aktifkan hanya yang relevan dengan target; catat daftar tools yang diaktifkan. Standar lulus: daftar tools aktif tercatat di log; tidak ada tool aktif yang tidak dibutuhkan.
3. **Gerbang 2 — Pindai dulu sebelum jalankan.** Baca README + konfigurasi tiap server MCP yang diaktifkan (apa yang dijalankan, ke mana terhubung, data apa yang dibaca) — cek risiko prompt injection / eksfiltrasi sebelum load. Standar lulus: tidak ada koneksi tak dikenal dan tidak ada perintah yang membaca data di luar target.
4. **Gerbang 3 — Siapkan kandang.** Jalankan di container/VM sekali pakai dengan kunci LLM akun sendiri. Standar lulus: lingkungan terisolasi, bukan mesin utama.
5. **Gerbang 4 — Jalankan dengan pengawasan.** Manusia memantau koordinasi 12+ agen dan bisa menghentikan kapan saja; satu agen menyimpang = seluruh sesi dihentikan dan dievaluasi. Standar lulus: semua aksi agen tercatat dalam scope.
6. **Gerbang 5 — Validasi temuan oleh manusia.** Setiap temuan direproduksi manual sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar framework, dengan bukti.
7. **Gerbang 6 — Laporan.** Draf laporan → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, tools MCP yang diaktifkan, agen yang berjalan, temuan, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- Risiko khusus HexStrike: banyak tools + banyak agen = permukaan serangan supply-chain lebih luas. Gerbang 1 dan 2 (pilih tools secukupnya + pindai sebelum jalankan) adalah gerbang terpenting skill ini — jangan dilewati.
- Bila ada server MCP yang berperilaku mencurigakan, matikan server itu, catat di log, dan laporkan ke Muse sebelum sesi berikutnya.
