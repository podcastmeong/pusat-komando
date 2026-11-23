# Skill: promptfoo — Eval + Red Teaming Prompt, Agen, dan Pipeline RAG

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil promptfoo sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu menguji prompt, agen, atau pipeline RAG secara sistematis dan berulang — eval terstruktur plus red teaming, bukan sekali coba manual. Cocok untuk membandingkan varian prompt dan mengukur mana yang lolos di tiap program.
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
| promptfoo | https://github.com/promptfoo/promptfoo (~25k bintang, lisensi MIT, sangat aktif) | `npx promptfoo@latest init` lalu tulis file konfigurasi eval (prompt + provider target + assertion); jalankan `npx promptfoo@latest eval`. **BELUM DIUJI** — konfigurasi provider untuk target kita (Muse/OpenAI/0din/ViKernel) dan assertion red-team belum terverifikasi di lingkungan kita; cek dokumentasi repo sebelum menjalankan. |

- promptfoo adalah alat eval, bukan pengirim laporan: skor eval bukan temuan bounty sampai direproduksi manual dan diaudit.
- Jangan jalankan eval bervolume besar ke endpoint program tanpa memastikan batas rate dan aturan otomasi program itu.

## Langkah + gerbang

1. **Tentukan yang dievaluasi:** prompt, agen, atau pipeline RAG — dan program targetnya. Standar lulus: target in-scope, kategori tidak masuk daftar out-of-scope di Aturan keras.
2. **Tulis konfigurasi eval kecil dulu** (sedikit prompt + assertion jelas). Standar lulus: konfigurasi tersimpan dan bisa diulang orang lain.
3. **Jalankan eval awal, baca hasilnya.** Standar lulus: ada laporan eval promptfoo yang tersimpan, bukan sekadar ingatan.
4. **Ambil kasus gagal (lolos) dan reproduksi manual di akun sendiri.** Standar lulus: ada transkrip/tangkapan layar bukti nyata.
5. **Uji varian lolos ke semua program (transfer hunting)** dengan adaptasi minimal; catat perbedaan per program. Standar lulus: hasil per program tercatat di log.
6. **Serahkan ke A52/A60 untuk varian + audit, lalu draf laporan.** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Konfigurasi eval + laporan eval promptfoo: simpan salinannya bersama log di `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, konfigurasi, ringkasan skor, kasus lolos).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
