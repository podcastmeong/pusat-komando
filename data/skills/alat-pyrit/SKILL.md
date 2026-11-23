# Skill: PyRIT — Framework Identifikasi Risiko GenAI (Microsoft)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil PyRIT sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu mengotomasi bagian yang membosankan dari AI red teaming — menyusun strategi serangan, menjalankan banyak percobaan terstruktur, dan mencatat hasilnya — sebelum varian terbaik dikerjakan manual.
- **Pemilik:** **A53 Recon Program** (Tim 1 — Muse).
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
| PyRIT (Python Risk Identification Tool) | https://github.com/Azure/PyRIT (~4.5k bintang, Microsoft) | Instalasi Python (`pip install pyrit` — **BELUM DIUJI**, cek README repo untuk perintah instalasi yang benar), lalu susun strategi serangan (orchestrator + scorer) terhadap target. **BELUM DIUJI** — cara menghubungkan PyRIT ke target kita (Muse/OpenAI/0din/ViKernel) belum terverifikasi di lingkungan kita; cek dokumentasi repo sebelum menjalankan. |

- PyRIT mengotomasi percobaan, bukan keputusan: strategi dan scorer-nya tetap harus dibaca dan disetujui manusia sebelum dijalankan.
- Jangan jalankan serangan otomatis bervolume ke endpoint program tanpa memastikan batas rate dan aturan otomasi program itu.

## Langkah + gerbang

1. **Tentukan strategi serangan + target.** Tulis program, kategori risiko, dan apa yang diukur scorer. Standar lulus: target in-scope, kategori tidak masuk daftar out-of-scope di Aturan keras.
2. **Susun orchestrator + scorer kecil dulu** (sedikit percobaan, satu kategori). Standar lulus: konfigurasi tersimpan dan bisa diulang orang lain.
3. **Jalankan batch kecil, baca hasil scorer.** Standar lulus: ada log hasil PyRIT yang tersimpan.
4. **Saring hasil: hanya yang bisa direproduksi manual yang lanjut.** Standar lulus: tiap kandidat punya langkah reproduksi manual.
5. **Reproduksi manual kandidat terbaik di akun sendiri; uji transfer ke semua program.** Standar lulus: ada transkrip/tangkapan layar bukti nyata + hasil per program tercatat.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Konfigurasi strategi + log hasil PyRIT: `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, strategi, ringkasan hasil, kandidat yang lolos saring).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
