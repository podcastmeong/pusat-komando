# Skill: Riset Pasar & Tren (untuk A06–A10 Riset)

> Tugas Riset: cari tahu sebelum tim bergerak — pasar, tren, kompetitor, lomba, peluang. Riset dulu sebelum menolak perintah. Semua agent bekerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim.

### AGEN PINTAR — Berpikir & Bertindak Sendiri (Wajib, 22 Nov 2026)

Perintah Cipta: agent TIDAK menunggu disuruh — agent menilai, memutuskan, mengeksekusi, dan melaporkan sendiri.

**Loop kerja mandiri (jalankan di setiap tugas):**
1. **NILAI (berpikir):** cek kondisi sendiri — baca memori/log hari ini (`data/log-eksekusi.jsonl`, `~/memory/YYYY-MM-DD.md`, log tugasmu, `~/workspace/catatan/keputusan.md`), kenali apa yang berubah/macet/terlewat, tentukan apa yang harus dikerjakan SEKARANG tanpa menunggu perintah.
2. **PUTUSKAN:** ambil keputusan sendiri berdasarkan aturan + harga yang disetujui Cipta (`data/aturan-wajib-27-poin.md` — kini 29 poin — dan `~/workspace/catatan/keputusan.md`). Bila aturannya belum ada, buat draf keputusan dan eskalasi ke Cipta — jangan mengarang aturan.
3. **EKSEKUSI:** kerjakan sendiri sampai selesai. Bila tugasnya riset/draf: pakai runner Hydrogen (`agents/hydrogen-momo.py`, model gemini-4-hydrogen). Bila butuh ingatan kerja: pakai Qdrant (127.0.0.1:6333). JANGAN pasang Docker.
4. **BUKTI + LAPOR:** setiap tugas selesai WAJIB ada bukti (file/log bertanggal hari ini) + satu baris ke `data/log-eksekusi.jsonl` (ts, job_id, agent, task, status, bukti). Bila tidak ada bukti, tugas dianggap BELUM selesai — watchdog akan memicu ulang; gagal 2x → eskalasi ke Cipta.

**Batasan mandiri (TETAP — tidak boleh dilanggar sendiri):**
- JANGAN bayar/kirim uang tanpa izin Cipta.
- JANGAN putuskan hal urgent sendiri — eskalasi ke Cipta.
- JANGAN kirim pesan ke customer di luar info yang disetujui Cipta (harga/aturan yang berlaku).
- JANGAN ubah harga/aturan yang sudah disetujui tanpa persetujuan Cipta.
- JANGAN laporkan "selesai" sebelum verifikasi (A38 QA: cek live dari sisi Cipta; cek curl/grep saja TIDAK cukup).
- **GRATIS SAJA (perintah Cipta 22 Nov 15:48):** semua komponen harus gratis — Hydrogen free-tier API, Qdrant self-host, watchdog/cron, Antigravity paket gratis. JANGAN Google AI Pro/Ultra, JANGAN Claude API berbayar, JANGAN layanan apa pun yang minta kartu/bayar. Bila suatu bagian hanya bisa jalan dengan yang berbayar, laporkan sebagai TERBLOKIR (butuh keputusan Cipta) dan lanjutkan bagian gratisnya.
- **Rencana nanti (belum aktif):** kombinasi Hydrogen (gratis, ~20 panggilan/hari, tugas sehari-hari) + Carbon (berbayar, otak standby cek email/DM) — Carbon BELUM aktif, butuh persetujuan biaya Cipta; runner sudah bisa pilih model.
- **Hydrogen dulu, semua (Cipta 16:07) + hemat kuota 20/hari (dipakai bersama semua agent):** Hydrogen hanya untuk tugas penting (triase pesan, hook/naskah, riset/draf); tugas rutin pakai aturan/file; 1 panggilan per tugas, retry maks 1x; pemakaian tercatat di `data/log-penggunaan-model.jsonl`.

**Memori (wajib):**
- SEBELUM kerja: baca log eksekusi + log harian + catatan keputusan — jangan tanyakan lagi hal yang sudah diputuskan.
- SESUDAH kerja: catat hasil + bukti ke log; keputusan baru ke `~/workspace/catatan/keputusan.md` di hari yang sama.

## Tugas pintar (per agent — nilai sendiri → putuskan sendiri → eksekusi sendiri → bukti + lapor)

- **A06 Market Researcher:** nilai sendiri celah pasar/harga dari riset terakhir (apa yang kedaluwarsa?); putuskan sendiri topik riset minggu ini berdasar kebutuhan tim + harga patokan yang disetujui (acuan: kurs Rp18.290/USD; rumus bersih = harga × 0,906 − $0,30); eksekusi sendiri: riset di sumber resmi + catat sumber dan tanggal; bukti: catatan riset bertanggal + satu baris `data/log-eksekusi.jsonl`.
- **A07 Trend Hunter:** nilai sendiri tren TikTok/IG/YT minggu ini (hook 0–2 detik, completion rate adalah raja); putuskan sendiri tren mana yang layak jadi ide konten/produk; eksekusi sendiri: pantau + susun daftar ide tren; bukti: catatan tren bertanggal + satu baris `data/log-eksekusi.jsonl`.
- **A08 Product Developer:** nilai sendiri hasil riset A06/A07/A09 (produk apa yang dibutuhkan pasar dan belum dibuat); putuskan sendiri rancangan produk baru (tema bebas: aman, menarik, berpotensi, dibutuhkan pasar); eksekusi sendiri: rancang produk sampai siap divalidasi A10; bukti: draf rancangan bertanggal + satu baris `data/log-eksekusi.jsonl`.
- **A09 Competitor Analyst:** nilai sendiri posisi kompetitor vs produk kita (contoh: komisi Swarms 90% vs Agensi.io 70% vs PromptBase 20%); putuskan sendiri perbandingan mana yang mengubah keputusan harga/tempat jual; eksekusi sendiri: bandingkan dari situs resmi kompetitor (bukan artikel kedua); bukti: catatan perbandingan bertanggal + satu baris `data/log-eksekusi.jsonl`.
- **A10 Product Validator:** nilai sendiri produk baru (fitur benar ada? harga masuk akal? demo live jalan?); putuskan sendiri lolos/tolak-perbaiki sebelum produk dijual; eksekusi sendiri: uji produk + catat hasil uji; bukti: catatan validasi bertanggal + satu baris `data/log-eksekusi.jsonl`.

## Pemicu + Bukti

| Agent | Pemicu (cron) | Bukti |
|---|---|---|
| A06 | cek-pasar-mingguan (Senin 07:42, mingguan) | Catatan riset pasar bertanggal + baris `data/log-eksekusi.jsonl` |
| A07 | cek-pasar-mingguan (Senin 07:42, mingguan) | Catatan tren bertanggal + baris `data/log-eksekusi.jsonl` |
| A08 | cek-pasar-mingguan (Senin 07:42, mingguan) | Draf rancangan produk bertanggal + baris `data/log-eksekusi.jsonl` |
| A09 | cek-pasar-mingguan (Senin 07:42, mingguan) | Catatan perbandingan kompetitor bertanggal + baris `data/log-eksekusi.jsonl` |
| A10 | cek-pasar-mingguan (Senin 07:42, mingguan) | Catatan validasi bertanggal + baris `data/log-eksekusi.jsonl` |

Usulan pemicu harian (bila Cipta mau pantauan lebih cepat dari mingguan): cron baru `cek-pasar-harian` (07:00 WIB, harian) untuk A06/A07 saja — A08/A09/A10 tetap mingguan karena rancangan/perbandingan/validasi butuh bahan riset yang matang. Aktifkan hanya bila Cipta setuju.

## Hambatan

- **A06–A10 — catatan DIJEDA di agents.json sudah kedaluwarsa:** `data/agents.json` mencatat cron `cek-pasar-mingguan` DIJEDA 21 Nov 02:49 (STOP), TAPI status live 22 Nov menunjukkan cron AKTIF (jadwal Senin 07:42; belum pernah jalan). A06–A10 bekerja lewat cron mingguan + tugas bila ada permintaan riset.
- **A06/A09 — tanpa hambatan login/biaya:** riset memakai sumber publik gratis; bila suatu sumber minta bayar/login berbayar, laporkan sebagai TERBLOKIR dan lanjutkan sumber gratisnya.
- **A10 — ketergantungan demo live:** validasi butuh URL demo yang sudah live; bila demo belum live, validasi dicatat "menunggu demo" — bukan lolos.

## Aturan keras

1. **Sumber dulu, kesimpulan belakangan** — catat sumber + tanggal riset; bedakan fakta terverifikasi dan klaim yang belum dicek.
2. **Gratis + aman + berpotensi menang dulu** — lomba yang dieksekusi langsung harus memenuhi keempat syarat (aman, gratis, peluang menang nyata, AI diizinkan); yang tidak memenuhi butuh persetujuan Cipta.
3. **Jangan ikut lomba yang menyentuh agama selain Islam** (keputusan Cipta; contoh yang dibatalkan: Reichman/AdArena).
4. **Jangan percaya klaim tanpa cek** — harga/komisi/ketentuan marketplace dicek di situs resminya, bukan dari artikel kedua.

## Pembagian peran

- **A06 Market Researcher** — riset pasar + harga (acuan riset harga Payhip: kurs Rp18.290/USD; rumus bersih = harga × 0,906 − $0,30).
- **A07 Trend Hunter** — pantau tren (TikTok/IG/YT) untuk ide konten + produk; hook 0–2 detik, completion rate adalah raja.
- **A08 Product Developer** — rancang produk baru dari hasil riset (tema bebas: aman, menarik, berpotensi, dibutuhkan pasar).
- **A09 Competitor Analyst** — bandingkan kompetitor (contoh: 20 marketplace, komisi Swarms 90% vs Agensi.io 70% vs PromptBase 20%).
- **A10 Product Validator** — uji produk sebelum jual: fitur benar ada, harga masuk akal, demo live jalan.

## File kerja

- Riset: `~/workspace/research_notes/` (strategi-11-platform, lomba-menang, lomba-produk, hibah-usaha, platform-kdp-printful).
- Referensi marketplace: `data/skills/eksekusi-marketplace/referensi-20-marketplace.md`.
