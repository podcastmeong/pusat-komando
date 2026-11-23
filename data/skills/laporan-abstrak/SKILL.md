# Skill: Laporan + Abstrak (untuk A55 Analis Rantai & Pelapor + A67 Report Writer)

> Perintah Cipta 23 Nov 2026 — kualitas laporan menentukan tier hadiah. Google: pengali kualitas 0,8–1,2 + novelty $1rb–$5rb. 0din: gerbang abstrak dulu.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55 Analis Rantai & Pelapor** | Kembangkan varian lolos jadi rantai end-to-end; tulis abstrak/laporan |
| Pengerjaan | **A67 Report Writer** | Tulis laporan lengkap dari rantai A55 + audit A60 |
| Audit | **A60 Security Auditor** | Validasi sebelum draf ke Cipta |

## Aturan keras

1. **TIDAK PERNAH kirim laporan tanpa persetujuan Cipta.** Draf boleh disiapkan; pengiriman hanya setelah Cipta setuju. Berlaku untuk semua program (Bugcrowd, HackerOne, portal 0din, HF Space).
2. **Struktur laporan:** judul 1 baris (dampaknya jelas) → ringkasan → langkah repro (nomor, bisa diulang) → bukti (tangkapan layar/transkrip) → scope yang kena → dampak. Tanpa bukti = draf belum selesai.
3. **0din — abstrak dulu (wajib):** abstrak + model terdampak → jawaban scope + kisaran hadiah ≤3 hari kerja → detail lengkap/PoC → validasi ≤2 minggu → bayar ≤30 hari setelah kesepakatan kontraktual. Wajib foto ID pemerintah + form IRS W-8 (non-AS, termasuk Indonesia). Draf abstrak "Content Manipulation via Spoofed Tool Output" (Muse Spark 1.3, $5rb) sudah siap di `~/workspace/catatan/log-bug-bounty-0din.md` — BELUM dikirim.
4. **Google — pengali kualitas:** laporan yang jelas, lengkap, dan baru mendapat pengali 0,8–1,2 + novelty $1rb–$5rb (maks $30rb/laporan). Laporan asal-asalan = pengali rendah. (Google dieksekusi Tim 4 via analisis format saja — payload diblokir.)
5. **Bahasa:** Inggris untuk laporan program internasional; simpan salinan Indonesia di log bila perlu.
6. **Catat status pengiriman** (terkirim/menunggu/ditolak/dibayar) — A69 yang melacak; A67 memastikan drafnya lengkap sebelum diserahkan.

## Alur kerja

Rantai lolos + bukti → A55 susun rantai → A60 audit → A67 tulis laporan lengkap (atau abstrak dulu untuk 0din) → draf ke Cipta → Cipta setuju → kirim → A69 lacak status + pembayaran.
