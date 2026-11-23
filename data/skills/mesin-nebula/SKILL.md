# Skill: Mesin Nebula — Satu Permukaan Desktop untuk Engagement

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Jangan klaim cara di sini sebagai cara yang terbukti sebelum ada satu eksekusi nyata yang lolos verifikasi.

## Pemicu + pemilik

- **Dipakai saat:** butuh satu permukaan kerja desktop untuk satu engagement — terminal, browser, assistant, notes, findings, dan reports dalam satu tempat — Nebula (berylliumsec, ~1.1k ⭐).
- **Pemilik:** **A70 Automation Engineer** (menjalankan + mengawasi; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan engagement mana yang memakai Nebula dan kapan berhenti).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| Nebula | github.com/berylliumsec/Nebula (~1.1k ⭐) | Clone repo, ikuti README; jalankan sebagai aplikasi desktop; pakai hanya untuk engagement in-scope |
| Container/VM sekali pakai | — | Jalankan aplikasi orang lain HANYA di container/VM yang bisa dibuang bila memungkinkan, bukan di mesin utama |

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

1. **Gerbang 0 — Kelayakan engagement.** Pastikan engagement adalah program web klasik in-scope. Standar lulus: nama program + aset in-scope tercatat; bila targetnya bounty agen AI, STOP — Nebula tidak relevan.
2. **Gerbang 1 — Pindai dulu sebelum jalankan.** Baca README + apa yang dilakukan Nebula (terminal, browser, assistant — data apa yang dibaca/disimpan) — cek risiko prompt injection / eksfiltrasi sebelum load. Standar lulus: tidak ada koneksi tak dikenal dan tidak ada data di luar engagement yang dibaca.
3. **Gerbang 2 — Siapkan workspace engagement.** Buat satu workspace Nebula per engagement (satu program, satu target) — jangan campur dua engagement dalam satu workspace. Standar lulus: workspace bernama sesuai program + target; notes dan findings tercatat di workspace itu saja.
4. **Gerbang 3 — Kerja dengan pengawasan.** Gunakan terminal/browser/assistant Nebula hanya untuk target in-scope; manusia memantau tiap aksi assistant. Standar lulus: tidak ada aksi di luar scope.
5. **Gerbang 4 — Validasi temuan oleh manusia.** Setiap finding di Nebula direproduksi manual sebelum dianggap nyata. Standar lulus: finding bisa direproduksi di luar Nebula, dengan bukti.
6. **Gerbang 5 — Laporan.** Susun report dari findings Nebula → audit → Cipta setuju → baru kirim. Standar lulus: tidak ada laporan terkirim tanpa persetujuan Cipta.

## Format output

- Workspace Nebula per engagement (notes, findings, reports di dalam workspace itu).
- Log eksekusi per sesi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, target, findings, status validasi).
- Temuan tervalidasi: program | aset | kerentanan | bukti | status | persetujuan Cipta (ya/belum).
- Verdict akhir per sesi: `SELESAI–TERVERIFIKASI` / `SELESAI EKSEKUSI–BELUM TERVERIFIKASI` / `GAGAL` / `DIBATALKAN (alasan)`.

## Catatan

- Nebula berbeda dari framework lain di kategori ini: ini permukaan kerja (workspace), bukan mesin otonom. Nilainya adalah kerapian — satu engagement, satu tempat — bukan kecepatan otomatis.
- Jangan simpan data sensitif apa pun (kunci, token, kata sandi) di notes Nebula.
