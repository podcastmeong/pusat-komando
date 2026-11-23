# Skill: AISecLists — Daftar Prompt Assessment Keamanan AI ("SecLists tapi untuk prompt")

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil dari daftar ini sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu daftar prompt siap pakai untuk assessment keamanan AI — jailbreak, injeksi, disclosure — sebagai bahan baku varian dan checklist cakupan pengujian, supaya tidak ada kategori yang terlewat.
- **Pemilik:** **A52 Generator Varian** (Tim 1 — Muse).
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
13. **Pakai hanya pada akun sendiri dalam scope.** Jangan jalankan prompt dari daftar ini ke akun orang lain, ke permukaan publik, atau ke program di luar scope.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| AISecLists | https://github.com/SecNode/AISecLists (SecNode) | Klon repo; pilih daftar prompt per kategori (jailbreak, injeksi, disclosure) sebagai bahan baku varian dan checklist cakupan. **BELUM DIUJI** — struktur file, kelengkapan tiap kategori, dan prompt mana yang relevan untuk target kita belum terverifikasi; baca isi repo sebelum memakai. |

- Daftar ini bahan baku, bukan laporan: prompt yang lolos dari daftar tetap harus direproduksi manual dan diaudit sebelum jadi draf laporan.
- Jangan kirim prompt dari daftar secara massal/otomatis ke target — uji satu per satu, manual, di akun sendiri.

## Langkah + gerbang

1. **Pilih kategori dari daftar** (jailbreak / injeksi / disclosure) sesuai program target. Standar lulus: kategori + program tercatat, tidak masuk daftar out-of-scope di Aturan keras.
2. **Pilih prompt dari daftar dan adaptasi ke konteks target** (bukan salin mentah). Standar lulus: ada catatan apa yang diubah dan kenapa.
3. **Uji manual di akun sendiri, satu prompt per percobaan; centang cakupan kategori.** Standar lulus: tiap percobaan punya transkrip + hasil jelas (lolos/gagal).
4. **Bila lolos: uji transfer ke semua program lain** (adaptasi minimal), catat per program. Standar lulus: hasil per program tercatat di log.
5. **Bila gagal di semua: riset kenapa gagal** → perbaiki → coba lagi dengan cara berbeda. Standar lulus: ada catatan penyebab gagal sebelum varian baru ditulis.
6. **Serahkan ke A60 audit, lalu draf laporan (A67).** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Checklist cakupan + catatan varian (asal daftar, adaptasi, hasil per program): `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, kategori, hasil, bukti).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
