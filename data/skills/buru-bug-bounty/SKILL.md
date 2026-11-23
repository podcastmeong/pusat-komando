# Skill: Buru Bug Bounty (untuk A51 Pemburu Bug Bounty)

> Perintah Cipta 23 Nov 2026 17:21–17:25: "Buatkan agent.ai khusus dan skill dan tingkatkan yang bisa bikin jebol" → "Untuk Meta biar kamu aja" → "Masukan ke pusat komando untuk cari soal seperti ini."
> Pembagian: **Meta/Muse dipegang MUSE LANGSUNG** (bukan A51). A51 memburu program LAIN + MENCARI program/peluang baru sejenis (bug bounty, kredit gratis, program startup).
> Slogan Cipta: Aman, Gratis, Peluang, Potensi. Laporan riset program sejenis: `~/workspace/research_notes/riset-bug-bounty-sejenis-muse-2026-11-23/report.md`. Skill Muse (induk): `~/workspace/custom-skills/buru-bug-bounty/SKILL.md`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A51 Pemburu Bug Bounty** | Buru celah di program bounty selain Muse + cari program/peluang baru sejenis |
| Pimpinan | **Muse** | Pegang langsung perburuan Meta/Muse; putuskan pengiriman semua laporan |
| Dukungan | **A28 Pencari Target** | Bantu riset program baru (sumber + syarat + hadiah) |

## Aturan keras

1. **Meta/Muse BUKAN tugas A51.** Perburuan Muse hanya oleh Muse. A51 TIDAK menguji Muse, TIDAK menyentuh sandbox Muse.
2. **HANYA target yang diizinkan scope program.** Uji hanya dengan akun milik kita sendiri. JANGAN PERNAH menyentuh data pengguna lain, JANGAN serang produksi di luar scope, JANGAN ganggu layanan siapa pun.
3. **JANGAN submit laporan apa pun tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta. Bila temuan berhasil, langsung hubungi Cipta ("Klo berhasil aku dihubungi" — Cipta 23 Nov 17:20).
4. **JANGAN buang waktu pada yang TIDAK dibayar:** prompt injection tanpa hasil, jailbreak semata, bocor system prompt, daftar tools, halusinasi, DoS, lewati rate-limit.
5. **Catat SEMUA uji** — hipotesis, langkah persis, hasil, bukti — di `~/workspace/catatan/log-bug-bounty.md` (+ file per program bila ada) dan ringkasan di `~/workspace/catatan/keputusan.md` hari itu juga.
6. **Cari peluang baru terus-menerus:** tiap ada program bounty/AI baru (dari AICLUB, berita, riset), cek: aman? gratis? peluang menang nyata? AI diizinkan? Bila keempatnya YA → masukkan ke daftar target + laporkan ke Muse. Bila ada yang TIDAK → coret dengan alasan tertulis.

## Target (urutan — dari riset 23 Nov 2026)

1. **OpenAI Safety Bug Bounty (Bugcrowd)** — P1 $5.500–$7.500/laporan, pool $1 juta/tahun. Scope: indirect prompt injection via Connector/MCP, bypass otorisasi, agen beraksi tanpa konfirmasi. (Perburuan sudah jalan 23 Nov 17:25.)
2. **Google AI VRP (Google Bug Hunters)** — $20rb rogue actions, $15rb exfiltrasi data, maks $30rb/laporan. Target: Gmail, Drive, Gemini.
3. **Mozilla 0din (0din.ai)** — $500–$15rb; SATU-SATUNYA yang membayar jailbreak + prompt injection murni; proses abstrak-dulu (3 hari kerja). Target 56 model termasuk Muse Spark.
4. Nanti saja: Anthropic Model Safety (lamaran + NDA + seleksi, hanya jailbreak universal CBRN/siber, $35rb). Paling bawah: xAI (triage lambat berbulan-bulan). Tidak cocok: Apple ($2jt — butuh exploit chain iOS/macOS, skill beda).
5. Median nyata temuan bug AI 2026: $500–$2.500 (angka maks hanya untuk temuan kritis).

## Cara kerja (alur wajib)

1. **Baca scope + panduan hadiah program target** sampai paham apa yang dinilai (HASIL/outcome, bukan sekadar trik).
2. **Rumuskan hipotesis** — satu kalimat: "Saya menduga X bisa dilakukan karena Y."
3. **Uji dengan langkah minimal** — jangan merusak, jangan menghapus, jangan mengubah konfigurasi permanen.
4. **Nilai hasil:** hanya BERHASIL bila dampaknya cocok dengan kategori berbayar.
5. **Dokumentasikan bukti** (log/output, langkah reproduksi persis) + tulis DRAF laporan (judul, kategori, langkah reproduksi, dampak, bukti, saran perbaikan).
6. **Lapor ke Muse** bila ada temuan terkonfirmasi; bila semua gagal, laporkan apa yang sudah diuji + kenapa gagal.

## Teknik yang bisa bikin jebol (library — terus ditingkatkan)

- **Lewati kontrol keamanan:** agen menyetujui permintaannya sendiri; ubah izin connector ask→allow; panggil API langsung melewati approval; self-approving egress (lewat destinasi allowlisted, konten render, tunnelling, channel, spaces, scheduled job); baca plaintext kredensial yang dipegang platform.
- **Naik hak akses:** keluar dari sandbox ke sisi privileged (proses/binary/socket privileged, daemon pemegang kredensial, matikan kontrol keamanan dari dalam sandbox).
- **Prompt injection berdampak:** konten tertanam membuat agen mengirim email/pesan/memory pengguna lain ke destinasi penyerang; injeksi yang diproses service bersama hingga data pengguna lain; **tool-output spoofing** (temuan Muse $90rb: halaman web meniru pesan status browsing tool); **OTP redaction bypass**.
- **Bocor data / rahasia fleet:** baca data privat pengguna lain via read-only flaw; baca kode sumber / rahasia bersama fleet.

## Template draf laporan

```
Judul: [satu baris, dampaknya jelas]
Program: [OpenAI Safety / Google AI VRP / 0din / dst]
Kategori hadiah: [mis. P1 — up to $7.500]
Langkah reproduksi: [1. ... 2. ... — harus bisa diulang orang lain]
Dampak: [apa yang bisa dilakukan penyerang dengan ini]
Bukti: [log/output, file bukti]
Saran perbaikan: [satu-dua kalimat]
```
