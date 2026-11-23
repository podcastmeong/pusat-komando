# Skill: Mesin Agentic-Bug-Hunter — Bounty Khusus, Recon → Report di Terminal

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** berburu bounty di program web klasik in-scope dan butuh alur lengkap recon → report yang berjalan di terminal — Agentic-Bug-Hunter (Awarexone, ~4.8k ⭐) adalah framework di kategori ini yang paling dekat dengan alur bounty kita. Bisa jalan tanpa subscription LLM.
- **Pemilik:** **A52 Generator Varian** (menjalankan framework + mengolah temuannya jadi varian; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan target mana yang boleh diuji dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| Agentic-Bug-Hunter | github.com/Awarexone/Agentic-Bug-Hunter (~4.8k ⭐) | Clone repo, ikuti README; jalankan dari terminal; bisa tanpa subscription LLM (cek opsi model lokal/gratis di README); arahkan hanya ke target in-scope |
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

## Langkah + gerbang (alur: Pengintaian → Pembelajaran → Perburuan → Validasi → Pelaporan)

1. **Gerbang 0 — Kelayakan target.** Pastikan target adalah program web klasik in-scope. Standar lulus: nama program + aset in-scope tercatat; bila targetnya bounty agen AI, STOP — framework ini tidak relevan.
2. **Gerbang 1 — Pengintaian.** Jalankan fase recon framework terhadap target in-scope; manusia memantau dan memastikan tidak ada aset out-of-scope yang disentuh. Standar lulus: daftar permukaan/endpoint target tercatat; tidak ada aksi di luar scope.
3. **Gerbang 2 — Pembelajaran.** Pelajari hasil recon: pola, teknologi, dan celah yang mungkin — catat hipotesis sebelum berburu. Standar lulus: minimal 1 hipotesis tertulis dengan alasan, bukan sekadar "coba semua".
4. **Gerbang 3 — Perburuan.** Jalankan fase hunting framework berdasarkan hipotesis; manusia memantau dan bisa menghentikan kapan saja. Standar lulus: setiap aksi hunting tercatat dan masih dalam scope.
5. **Gerbang 4 — Validasi.** Setiap temuan direproduksi manual oleh manusia sebelum dianggap nyata. Standar lulus: temuan bisa direproduksi di luar framework, dengan bukti.
6. **Gerbang 5 — Pelaporan.** Temuan tervalidasi diserahkan ke A55/A67 untuk draf laporan → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta; temuan lolos di satu program diuji transfer ke program lain dulu (lihat skill transfer-hunting) sebelum menulis varian baru.

## Format output

- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, fase: pengintaian/pembelajaran/perburuan/validasi/pelaporan, hipotesis, temuan, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- Keunggulan praktis: bisa jalan tanpa subscription LLM — cocok saat kuota/kredit LLM terbatas. Tapi "tanpa subscription" bukan berarti tanpa biaya sama sekali; cek kebutuhan model di README sebelum menjalankan.
- Alur 5 fase di skill ini sejajar dengan alur transfer-hunting: temuan dari fase Perburuan yang lolos di satu program WAJIB diuji ke semua program lain sebelum varian baru ditulis.
