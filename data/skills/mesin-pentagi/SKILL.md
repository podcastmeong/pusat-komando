# Skill: Mesin PentAGI — Agen Otonom Pentest End-to-End

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** target adalah program web klasik in-scope (bukan bounty agen AI) dan butuh pentest end-to-end yang dijalankan satu agen otonom — dari recon sampai exploit — dengan pengawasan manusia.
- **Pemilik:** **A70 Automation Engineer** (menjalankan + mengawasi framework; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan target mana yang boleh diuji dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| PentAGI | github.com/vxcontrol/pentagi (~24k ⭐) | Clone repo, ikuti README untuk instalasi (Docker direkomendasikan — jalankan di container/VM yang bisa dibuang); konfigurasikan kunci LLM sendiri; arahkan hanya ke target in-scope |
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

1. **Gerbang 0 — Kelayakan target.** Pastikan target adalah program web klasik in-scope dan scope-nya tertulis jelas. Standar lulus: nama program + daftar aset in-scope tercatat di log; bila targetnya bounty agen AI (bukan web klasik), STOP — framework ini tidak relevan.
2. **Gerbang 1 — Siapkan kandang.** Jalankan PentAGI di container/VM sekali pakai; kunci LLM memakai akun sendiri. Standar lulus: framework berjalan di lingkungan terisolasi, bukan mesin utama.
3. **Gerbang 2 — Pindai dulu sebelum jalankan.** Baca README + konfigurasi PentAGI (apa yang dijalankan, ke mana ia terhubung, data apa yang dibaca) — cek risiko prompt injection / eksfiltrasi sebelum load (prinsip SkillSpector). Standar lulus: tidak ada koneksi tak dikenal dan tidak ada perintah yang membaca data di luar target.
4. **Gerbang 3 — Jalankan dengan pengawasan.** Beri target + batas scope; manusia memantau tiap fase (recon → eksploitasi) dan bisa menghentikan kapan saja. Standar lulus: tidak ada aksi di luar scope; framework dihentikan bila menyentuh aset out-of-scope.
5. **Gerbang 4 — Validasi temuan oleh manusia.** Setiap temuan framework direproduksi manual oleh A70 sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar framework, dengan bukti (tangkapan layar/log).
6. **Gerbang 5 — Laporan.** Draf laporan ditulis A70 → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, fase yang dijalankan, temuan, status validasi).
- Temuan tervalidasi dicatat dengan format: program | aset | kerentanan | bukti | status (tervalidasi/belum) | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- PentAGI adalah framework paling lengkap di kategori ini (~24k ⭐) — tapi "paling lengkap" bukan berarti paling cocok untuk bounty agen AI. Untuk program agen AI, alat uji permukaan (garak, promptfoo, PyRIT, AgentDojo) lebih relevan.
- Bila PentAGI berhenti diperbarui atau perilakunya berubah, catat di log dan evaluasi ulang sebelum dipakai lagi.
