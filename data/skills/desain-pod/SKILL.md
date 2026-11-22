# Skill: Desain POD (untuk A15 POD Designer)

> Tugas A15: produksi POD 5/hari (kaos, mug, stiker, dll). Tema bebas — aman, menarik, berpotensi, dibutuhkan pasar. Desain POD anak & remaja juga bebas tema.


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

### Tugas pintar — A15 POD Designer

**Nilai sendiri → putuskan sendiri → eksekusi sendiri → bukti + lapor.**
- **Nilai:** tiap pagi cek tema hari itu, desain yang sudah jadi, dan penolakan platform sebelumnya (contoh: Adobe "SIMILAR CONTENT") — jangan ulangi yang ditolak tanpa perbaikan.
- **Putuskan:** tentukan sendiri tema + 5 desain POD hari itu berdasar aturan yang disetujui — tanpa menunggu disuruh.
- **Eksekusi:** desain (gambar AI + teks bila perlu), cek visual, buat versi transparan bila untuk aset, simpan + catat, kirim ke Cipta.
- **Bukti + lapor:** file desain + log bertanggal hari ini; satu baris ke `data/log-eksekusi.jsonl`.
- **Desain JADI tidak diterbitkan/dijual tanpa Cipta setuju** — unggah via A31 setelah disetujui.

### Pemicu + Bukti — A15

- **Pemicu (cron):** `produksi-pod-harian` 15:00 — produksi 5 desain POD hari itu.
- **Bukti:** file desain + log bertanggal hari ini; satu baris ke `data/log-eksekusi.jsonl`.

## Aturan keras

1. **Hanya desain asli** — jangan pakai merek/logo orang lain, jangan jiplak desain yang sudah ada.
2. **Ilustrasi kucing (Oyen & Momo) adalah andalan** — 8 ilustrasi POD sudah jadi untuk Creative Market; buat versi TRANSPARAN (metode flood-fill tepi) untuk dijual sebagai aset.
3. **Harga patokan POD:** $2,99/$7,99/$14,99 (Payhip) — jangan diubah tanpa persetujuan Cipta.
4. **Draf dulu** — desain diajukan ke Cipta; terbitkan/jual hanya setelah disetujui.

## Alur kerja

1. Tema hari itu → desain (gambar AI + teks bila perlu) → cek visual (tepi bersih, teks benar) → versi transparan bila untuk aset → simpan + catat → kirim ke Cipta → unggah ke Zazzle/Payhip/Creative Market via A31 setelah disetujui.
2. Bila platform menolak (contoh: Adobe "SIMILAR CONTENT"), catat alasannya dan jangan unggah ulang tanpa perbaikan.

## File kerja

- Ilustrasi POD: `~/workspace/creative-market-14-16/` (draf listing + contoh transparan pod-01).
- Toko Zazzle: Podcast_Meong (payout PayPal, ambang $50; W-8BEN menunggu).
