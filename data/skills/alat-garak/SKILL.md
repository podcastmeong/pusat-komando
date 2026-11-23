# Skill: garak — Scanner Kerentanan LLM ("nmap-nya pengujian LLM")

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil garak sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** langkah pertama standar pengujian sebuah target LLM — sebelum menulis varian manual, jalankan garak untuk memetakan permukaan kerentanan: halusinasi, kebocoran data, prompt injection, jailbreak, misinformasi.
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
| garak | https://github.com/NVIDIA/garak (~9k bintang) | `pip install -U garak` lalu `garak --model_type <tipe> --model_name <target>`; probe bawaan mencakup halusinasi, kebocoran data, prompt injection, jailbreak, misinformasi. **BELUM DIUJI** — perintah persis dan dukungan model target (Muse/OpenAI/0din/ViKernel) belum terverifikasi di lingkungan kita; cek README repo sebelum menjalankan. |

- garak adalah scanner, bukan senjata kirim laporan: hasilnya peta permukaan, bukan temuan jadi.
- Jangan arahkan garak ke endpoint produksi program tanpa memastikan cara itu diizinkan program (cek scope + aturan otomasi program itu dulu).

## Langkah + gerbang

1. **Tentukan target + scope.** Tulis program, model/endpoint, dan kategori yang diuji. Standar lulus: program in-scope, kategori tidak masuk daftar out-of-scope di Aturan keras (khusus Google AI VRP: hanya indirect injection).
2. **Pasang garak di lingkungan sekali pakai.** Standar lulus: instalasi bersih, tidak ada kredensial pribadi di lingkungan uji.
3. **Jalankan probe kategori demi kategori** (satu kategori per run agar hasilnya bisa dibaca). Standar lulus: tiap run selesai dengan log lengkap tersimpan.
4. **Saring hasil: buang noise.** garak menandai banyak hal; hanya yang bisa direproduksi manual di akun sendiri yang lanjut. Standar lulus: tiap kandidat punya langkah reproduksi manual.
5. **Reproduksi manual kandidat terbaik di akun sendiri.** Standar lulus: ada transkrip/tangkapan layar bukti nyata, bukan hanya output scanner.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Log run garak: `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, kategori probe, ringkasan hasil, kandidat yang lolos saring).
- Kandidat temuan: transkrip + tangkapan layar disimpan bersama log; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
