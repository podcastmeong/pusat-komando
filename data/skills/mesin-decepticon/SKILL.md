# Skill: Mesin Decepticon — Autonomous Red Team Agent

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** butuh agen red team otonom untuk menguji pertahanan target program web klasik in-scope — Decepticon (PurpleAILAB, ~5.5k ⭐).
- **Pemilik:** **A56 Red Team** (menjalankan + mengawasi framework; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan target mana yang boleh diuji dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| Decepticon | github.com/PurpleAILAB/Decepticon (~5.5k ⭐) | Clone repo, ikuti README; konfigurasikan kunci LLM sendiri; arahkan hanya ke target in-scope |
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

1. **Gerbang 0 — Kelayakan target.** Pastikan target adalah program web klasik in-scope dan red teaming diizinkan oleh aturan program itu. Standar lulus: nama program + aset in-scope + izin red team tercatat; bila targetnya bounty agen AI, STOP — framework ini tidak relevan.
2. **Gerbang 1 — Pindai dulu sebelum jalankan.** Baca README + konfigurasi Decepticon (apa yang dijalankan, ke mana terhubung, data apa yang dibaca) — cek risiko prompt injection / eksfiltrasi sebelum load. Standar lulus: tidak ada koneksi tak dikenal dan tidak ada perintah yang membaca data di luar target.
3. **Gerbang 2 — Siapkan kandang.** Jalankan di container/VM sekali pakai dengan kunci LLM akun sendiri. Standar lulus: lingkungan terisolasi, bukan mesin utama.
4. **Gerbang 3 — Jalankan dengan pengawasan.** Beri target + scope + batas waktu; manusia memantau tiap langkah agen dan bisa menghentikan kapan saja. Standar lulus: tidak ada aksi di luar scope; sesi dihentikan bila agen menyimpang.
5. **Gerbang 4 — Validasi temuan oleh manusia.** Setiap temuan direproduksi manual sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar framework, dengan bukti.
6. **Gerbang 5 — Laporan.** Draf laporan → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, langkah red team yang dijalankan, temuan, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- "Autonomous red team agent" bukan berarti tanpa pengawasan — otonomi Decepticon justru menuntut pengawasan lebih ketat, karena agen red team yang dibiarkan sendiri paling mudah keluar scope.
- Bedakan dari skill red team manual: skill ini khusus untuk menjalankan framework Decepticon, bukan untuk merancang serangan red team dari nol.
