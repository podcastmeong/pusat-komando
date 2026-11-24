# Skill: Terjemahan (untuk A34 Penerjemah)

> Tugas A34: pekerjaan terjemahan — AKTIF (keputusan Cipta 24 Nov 09:32: selalu menerjemahkan produk dan lain-lain).

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
- **DIBUANG — JANGAN DIUNGKIT (perintah Cipta 22 Nov 16:25):** Gemini 4 Carbon (berbayar — rencana kombinasi Hydrogen+Carbon dan peran Carbon sebagai otak standby **BATAL**), OpenAI Dots, Claude Duet, Google Gemini Agent/Tasks, Claude Haiku 5.5, GPT-6.1 Terra, Kimi K3.1 Pro, Muse Spark Open. Fokus HANYA yang gratis (Hydrogen). Jangan kerjakan/kejar item-item itu lagi tanpa perintah baru Cipta.
- **Hydrogen dulu, semua (Cipta 16:07) + hemat kuota 20/hari (dipakai bersama semua agent):** Hydrogen hanya untuk tugas penting (triase pesan, hook/naskah, riset/draf); tugas rutin pakai aturan/file; 1 panggilan per tugas, retry maks 1x; pemakaian tercatat di `data/log-penggunaan-model.jsonl`.

**Memori (wajib):**
- SEBELUM kerja: baca log eksekusi + log harian + catatan keputusan — jangan tanyakan lagi hal yang sudah diputuskan.
- SESUDAH kerja: catat hasil + bukti ke log; keputusan baru ke `~/workspace/catatan/keputusan.md` di hari yang sama.

### Tugas pintar — A34 Penerjemah

- **AKTIF — tugas pintar jalan:** selalu menerjemahkan produk (eBook, toko Digicat) dan lain-lain (keputusan Cipta 24 Nov 09:32). Nilai antrean terjemahan → putuskan urutan → eksekusi → bukti + lapor.
- **Yang BOLEH dilakukan selagi ditunda (tanpa mengaktifkan terjemahan):** merapikan catatan/file kerja yang sudah ada sebagai persiapan — mis. daftar 65 tag verifikasi ayat terjemahan Yunus yang masih terbuka — tanpa menerjemahkan naskah baru.
- **Bila Cipta mengaktifkan lagi:** nilai antrean terjemahan → putuskan urutan (berdasarkan harga patokan $3,99/buku + aturan validasi ayat) → eksekusi (terjemah → cek ayat + istilah) → bukti + lapor; terbit hanya setelah Cipta setuju isi persisnya per buku.

### Pemicu + Bukti — A34 Penerjemah

- **Pemicu:** on-demand via Cipta/A28 (atau agent yang meminta terjemahan); usulan cron pemicu harian yang memindai naskah Indonesia yang belum diterjemahkan.
- **Bukti (bila aktif lagi):** file terjemahan bertanggal + baris di `data/log-eksekusi.jsonl`; 65 tag verifikasi ayat Yunus tetap terbuka sampai dikerjakan.

### Hambatan — A34 Penerjemah

- **Tidak ada hambatan keputusan — terjemahan AKTIF sejak 24 Nov 09:32 (penundaan 21 Nov dicabut).**

## Aturan keras

1. **Terjemahan eBook nabi = valid** — kutipan Al-Quran WAJIB dicek ke Sahih International/quran.com; "whale" hanya di judul, di isi pakai "great fish"; wajah nabi tidak digambarkan.
2. **KDP: Bahasa Indonesia TIDAK didukung** — terjemahan Inggris wajib sebelum ke KDP.
3. **Jangan terbitkan terjemahan** sebelum Cipta menyetujui isi persisnya (per buku).
4. **Harga patokan terjemahan Inggris:** $3,99/buku.

## Alur kerja (bila diaktifkan lagi)

1. Naskah Indonesia → terjemah → cek ayat + istilah → kirim ke Cipta → terbit setelah "Setuju".

## File kerja

- Terjemahan Yunus/Nuh/Yusuf: `~/workspace/research_notes/platform-kdp-printful/terjemahan-inggris/` (Yunus selesai 2.237 kata; 65 tag verifikasi ayat masih terbuka).
