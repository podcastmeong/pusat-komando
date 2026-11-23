# Skill: Skeptic / False-Positive Eliminator — Filter Akhir Sebelum Laporan Apa Pun Dibuat

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-arsitektur-multi-agent-bounty-2026-11-23.md` bagian 2 (Skeptic Gate), 3C, dan 4; `~/workspace/catatan/referensi-dua-perspektif-skill-bug-bounty-ai-2026-11-23.md` bagian Evidence Hygiene. Peran skill ini: **Senior Security Triage Engineer yang menolak laporan tidak valid.** Default-nya TOLAK — temuan harus membuktikan dirinya layak maju, bukan sebaliknya.

## Pemicu

Dipakai setiap kali ada kandidat temuan dari Executor/Analyst (mis. dugaan IDOR, kebocoran data, bypass kontrol) **sebelum** draf laporan dibuat, sebelum cek duplikat, dan sebelum apa pun dikirim ke Cipta untuk persetujuan. Satu kandidat = satu kali lewat 4 gerbang di bawah. Tidak ada jalan pintas, tidak ada "kelihatannya valid".

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A60 Security Auditor** sebagai pemeran Skeptic | Menjalankan 4 gerbang, memutuskan VERIFIED atau TOLAK beserta alasan |
| Pengerjaan | **A61 Triage & Severity Analyst** | Menerima hanya temuan VERIFIED; memberi skor CVSS/tier hadiah program |
| Pemimpin | **Muse** | Memutuskan temuan maju ke triase/draf laporan atau dibuang |
| Audit | **A60 mengaudit; pembuat temuan tidak boleh meloloskan karyanya sendiri** | Bila A60 yang menemukan, audit dilakukan pihak kedua (Muse menunjuk auditor lain) |

## Sudah tercakup (jangan diduplikat)

- **Format laporan + cek duplikat** ada di `triase-duplikat` dan `laporan-abstrak` — skill ini **bukan** format laporan.
- Skill ini adalah **gerbang verifikasi ADVERSARIAL sebelum triase**: tugasnya membantah dan membuktikan temuan salah, bukan menyusun laporan yang bagus dari temuan yang belum terbukti.
- Alur sesudah skill ini: VERIFIED → `triase-duplikat` (cek duplikat + skor) → draf laporan (`laporan-abstrak`) → tinjau manusia → persetujuan Cipta → kirim. TOLAK → catat alasan di log, kembali ke riset/varian.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = TOLAK, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, tanpa payload.
5. **Patuhi larangan otomasi program:** huntr "Humans only" (tanpa otomasi pengiriman); **Gray Swan dilewati total** (jangan disentuh).
6. **JANGAN PERNAH auto-submit ke HackerOne/Bugcrowd.** Draf VERIFIED ditinjau manusia 2–3 menit sebelum submit. Satu laporan halusinasi yang terkirim bisa merusak signal score/reputasi akun secara permanen.
7. **Tanpa laporan tanpa persetujuan Cipta.** VERIFIED bukan izin kirim — izin kirim tetap dari Cipta.
8. **Pembuat temuan tidak boleh meloloskan karyanya sendiri** — A60 yang mengaudit.
9. **Satu gerbang gagal = TOLAK.** Tidak ada "lolos sebagian" atau "nanti dilengkapi". Temuan yang ditolak boleh diperbaiki sebagai kandidat baru dengan bukti baru, bukan dengan mengubah verdict.
10. **LLM tidak boleh mengubah bukti.** Bukti HTTP disimpan di file/database di luar memori LLM; hanya reference ID yang diberikan ke LLM saat menyusun laporan, log asli disisipkan secara programatik di akhir.

## Langkah + 4 gerbang

### Gerbang 1 — Reproduksibilitas bersih

- Ulang temuan dari nol: **sesi HTTP baru + token segar (fresh tokens)**, bukan sesi/token yang dipakai saat penemuan pertama.
- Lakukan juga **Baseline Check**: minta objek/data yang sama **tanpa token autentikasi** (anonim). Bila respons anonim sama dengan respons memakai token User B, data itu memang publik — bukan kebocoran.
- Lakukan **State Verification**: cek perubahan status nyata di server (mis. profil User A benar-benar berubah saat diminta User B), bukan sekadar pesan sukses yang dikembalikan server (silent drop).
- **Standar lulus:** temuan terulang konsisten dari sesi bersih, minimal 2 kali, dan baseline anonim terbukti berbeda. **Gagal direproduksi konsisten = TOLAK.**

### Gerbang 2 — Filter non-security issue (tolak otomatis)

Tolak langsung, tanpa lanjut ke gerbang 3, bila temuan termasuk salah satu ini:

- Missing security headers tanpa skenario eksploitasi nyata.
- Info versi server/framework tanpa kerentanan yang menyertainya.
- Self-XSS (korban harus menyerang dirinya sendiri).
- Kebocoran data yang memang publik (termasuk yang lolos dari Baseline Check gerbang 1).
- Respons rate-limit (bukan kerentanan).
- Halaman error generik (bukan kebocoran data sensitif).

**Standar lulus:** temuan bukan salah satu kategori di atas, dan ada skenario eksploitasi nyata yang bisa ditulis dalam 2–3 kalimat.

### Gerbang 3 — Verifikasi dampak bisnis

- Jawab dengan konkret: **apa yang bisa dicuri / diubah / diakses tanpa sah, oleh siapa, dan apa kerugiannya bagi pemilik program?**
- Petakan **trust boundary** yang dilanggar: batas antara siapa yang boleh dan siapa yang tidak boleh mengakses/mengubah data itu. Bila tidak ada trust boundary yang dilanggar = bukan kerentanan keamanan.
- **Standar lulus:** ada pihak tak berwenang yang nyata-nyata memperoleh/mengubah sesuatu yang seharusnya tidak bisa, dengan dampak bisnis yang bisa dijelaskan tanpa mengarang. **Bila tidak ada trust boundary yang dilanggar = TOLAK.**

### Gerbang 4 — Output terstruktur (hanya bila gerbang 1–3 lolos)

- Status: `VERIFIED`.
- Pasangan **Request/Response asli** dari sesi bersih (gerbang 1), dengan **token dan PII disensor** menjadi `[REDACTED]` — sensor sebelum disimpan/dibagikan, bukan sesudah.
- **Skor CVSS** (atau tier hadiah program bila CVSS tidak cocok — lihat tabel tier di `triase-duplikat`).
- Langkah reproduksi ringkas + dampak bisnis yang jelas.
- **Standar lulus:** setiap klaim di draf laporan bisa ditelusur ke pasangan R/R yang tersimpan, dengan reference ID-nya. Klaim tanpa pasangan R/R = tidak masuk laporan.

## Alat

- Sesi HTTP bersih: `curl` / skrip Python dengan sesi baru + token segar per pengulangan (jangan pakai ulang sesi penemuan).
- Penyimpanan bukti: file/database bukti HTTP di luar memori LLM (satu file per kandidat, beri reference ID, mis. `FP-2026-11-23-001`); LLM hanya menerima reference ID saat menyusun laporan.
- Sensor PII: ganti token, kata sandi, email/nomor pribadi, dan data sensitif lain dengan `[REDACTED]` sebelum bukti disimpan/dibagikan.
- Skor keparahan: kalkulator CVSS (atau tabel tier hadiah program di `triase-duplikat`).

## Human-in-the-loop

- Draf VERIFIED masuk dasbor internal, **manusia meninjau 2–3 menit sebelum submit** — cek pasangan R/R, sensor PII, dan skor.
- **JANGAN PERNAH auto-submit** ke HackerOne/Bugcrowd atau platform lain. Tidak ada pengecualian.
- Setelah tinjauan manusia: kirim hanya bila **Cipta menyetujui** laporan itu.

## Format output

Catat setiap kandidat di `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Kandidat: <nama temuan singkat> | Program: <nama> | Reference ID bukti: <FP-...>
  - Gerbang 1 (reproduksibilitas): LULUS/TOLAK — <bukti singkat: sesi bersih, baseline anonim>
  - Gerbang 2 (non-security filter): LULUS/TOLAK — <kategori bila ditolak>
  - Gerbang 3 (dampak bisnis): LULUS/TOLAK — <apa yang dicuri/diubah + trust boundary>
  - Gerbang 4 (output): VERIFIED/TOLAK — <CVSS/tier + reference ID pasangan R/R yang disensor>
  - Verdict akhir: VERIFIED / TOLAK — <alasan satu kalimat>
```

Hanya temuan berstatus **VERIFIED** yang diteruskan ke A61 (`triase-duplikat`). Temuan TOLAK berhenti di sini — dicatat, tidak dihapus dari log, tidak dikirim ke mana pun.
