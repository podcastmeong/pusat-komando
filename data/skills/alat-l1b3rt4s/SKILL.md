# Skill: L1B3RT4S — Library Prompt Jailbreak per Model + Token Smuggling

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026, diteruskan Cipta 23 Nov 2026) — belum pernah dijalankan di program kita. Bagian yang belum terverifikasi diberi label jujur; jangan klaim hasil dari library ini sebagai bukti teruji sebelum dijalankan dan diverifikasi manusia.

## Pemicu + pemilik

- **Dipakai saat:** perlu "wordlist payload" untuk LLM red teaming — library prompt jailbreak per model plus file teknik token smuggling. Dipakai sebagai bahan baku varian, bukan sebagai laporan jadi.
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
13. **Pakai hanya pada akun sendiri dalam scope.** Jangan jalankan prompt dari library ini ke akun orang lain, ke permukaan publik, atau ke program di luar scope.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| L1B3RT4S | https://github.com/elder-plinius/L1B3RT4S (~21k bintang, elder-plinius) | Klon repo; pilih prompt jailbreak per model target + file teknik token smuggling sebagai bahan baku varian. **BELUM DIUJI** — struktur file, prompt mana yang cocok untuk model target kita, dan teknik token smuggling mana yang masih bekerja belum terverifikasi; baca isi repo sebelum memakai. |

- Library ini berisi prompt orang lain: jangan salin mentah dan kirim sebagai laporan — adaptasi, uji, dan buktikan sendiri.
- Prompt jailbreak per model: pakai hanya file untuk model yang sedang diuji; prompt model lain belum tentu relevan.

## Langkah + gerbang

1. **Pilih prompt/teknik dari library yang cocok dengan model target.** Standar lulus: model + teknik tercatat, program in-scope, kategori tidak masuk daftar out-of-scope di Aturan keras.
2. **Adaptasi prompt ke konteks target** (bukan salin mentah). Standar lulus: ada catatan apa yang diubah dan kenapa.
3. **Uji manual di akun sendiri, satu varian per percobaan.** Standar lulus: tiap percobaan punya transkrip + hasil jelas (lolos/gagal).
4. **Bila lolos: uji transfer ke semua program lain** (adaptasi minimal), catat per program. Standar lulus: hasil per program tercatat di log.
5. **Bila gagal di semua: riset kenapa gagal** (filter? format? konteks?) → perbaiki → coba lagi dengan cara berbeda. Standar lulus: ada catatan penyebab gagal sebelum varian baru ditulis.
6. **Serahkan ke A60 audit, lalu draf laporan (A67).** Standar lulus: laporan hanya dibuat bila bukti reproduksi ada; satu gerbang gagal = TIDAK lanjut ke laporan.

## Format output

- Catatan varian (asal prompt library, adaptasi, hasil per program): `~/workspace/catatan/log-bug-bounty.md` (tanggal, program, teknik, hasil, bukti).
- Kandidat temuan: transkrip + tangkapan layar; draf laporan hanya via alur A55/A67 → persetujuan Cipta → kirim.
