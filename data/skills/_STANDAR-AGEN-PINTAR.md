# STANDAR AGEN PINTAR — Pusat Komando (Wajib, 22 Nov 2026)

Perintah Cipta 22 Nov 2026 15:36: (1) semua agent.ai diganti dengan versi pintar; (2) upgrade skill MAKSIMAL — agent harus bisa BERPIKIR dan BERTINDAK SENDIRI; (3) agent pasif juga ikut diganti — jangan ada yang dilewati (A01–A40 semua aktif/pintar).

**Definisi "versi pintar" (4 pilar):**
1. **OTAK** — instruksi jelas + model terbaru untuk riset/draf (runner Hydrogen `agents/hydrogen-momo.py`, model gemini-4-hydrogen). JUJUR: agent jalan sebagai subagent/cron di atas Muse — model per-agent TIDAK bisa diganti ke penyedia lain; yang di-upgrade adalah instruksi, memori, dan loop verifikasi. Jangan klaim sebaliknya.
2. **MEMORI** — Qdrant (127.0.0.1:6333, tanpa Docker) + `data/log-eksekusi.jsonl` + log harian `~/memory/YYYY-MM-DD.md`. Agent ingat apa yang sudah dikerjakan dan tidak mengulang kesalahan yang sama.
3. **KONTRAK EKSEKUSI** — setiap tugas punya Definition of Done + bukti (file/log bertanggal hari ini). Watchdog (`watchdog-tugas-harian`, tiap jam) memeriksa bukti; gagal 2x → eskalasi ke Cipta.
4. **DIAWASI** — watchdog + A38 QA (cek live dari sisi Cipta sebelum lapor "selesai").

**Docker DILARANG dipasang di VM ini** (bisa bentrok dengan runtime). Qdrant sudah terpasang tanpa Docker.

## GRATIS SAJA (perintah Cipta 22 Nov 2026 15:48 — WAJIB)

Semua komponen versi pintar HARUS gratis. Yang BOLEH: Hydrogen lewat API free tier (API key kita sudah terbukti jalan), Qdrant self-host gratis, watchdog/cron gratis, Antigravity paket gratis Individual (termasuk Gemini 3.8 Flash, Claude Sonnet/Opus 4.6 thinking, GPT-OSS-120b), Gemini Gem gratis, ChatGPT Project gratis, Dify free.
Yang JANGAN: Google AI Pro/Ultra, Claude API berbayar, layanan apa pun yang minta kartu atau bayar. JANGAN beli/langganan apa pun.
Bila suatu bagian upgrade ternyata HANYA bisa jalan dengan yang berbayar, laporkan bagian itu sebagai TERBLOKIR (butuh keputusan Cipta) dan lanjutkan bagian gratisnya.

## DIBUANG (perintah Cipta 22 Nov 16:25 — BATAL, JANGAN DIUNGKIT)

8 item AI ini DIBUANG — jangan dikerjakan/dikejar lagi tanpa perintah baru Cipta: **Gemini 4 Carbon, OpenAI Dots, Claude Duet, Google Gemini Agent/Tasks, Claude Haiku 5.5, GPT-6.1 Terra, Kimi K3.1 Pro, Muse Spark Open.** Akibatnya: **rencana kombinasi Hydrogen + Carbon BATAL** dan **peran Carbon sebagai otak standby (cek email/DM) BATAL** — Carbon dibuang karena berbayar. Fokus HANYA yang gratis: Hydrogen untuk SEMUA agent (~20 panggilan/hari, hemat kuota), Cloudflare staging, SaaS, Godot, dan ganti 44 agent. Runner tetap menolak Carbon (guard: butuh `data/persetujuan-carbon.md` + env `SATUKIKI_CARBON_APPROVED=1` — file persetujuan itu TIDAK akan dibuat). Dokumen rencana kombinasi (`data/rencana-kombinasi-hydrogen-carbon.md`) dinyatakan BATAL dan disimpan sebagai arsip saja.

## HYDROGEN DULU, SEMUA (perintah Cipta 22 Nov 2026 16:07 — WAJIB)

Hydrogen (gratis, free tier ~20 panggilan/hari) dipakai untuk SEMUA agent — bukan cuma pilot A27. Hanya Hydrogen — Carbon DIBUANG 22 Nov 16:25, tidak ada kombinasi nanti.

**Disiplin kuota 20/hari (dipakai BERSAMA semua agent — hemat!):**
1. Prioritas panggilan Hydrogen: (1) triase pesan masuk A27 (penting/urgent), (2) hook/naskah video Oyen/A11/A17, (3) riset/draf penting lainnya.
2. Tugas rutin/lookup pakai aturan + file, BUKAN Hydrogen (baca `data/`, `~/workspace/catatan/keputusan.md`, log — jangan panggil model untuk hal yang sudah tertulis).
3. Satu panggilan per tugas; bila gagal, coba lagi MAKSIMAL 1x; bila tetap gagal, kerjakan langsung dan catat kegagalannya.
4. Pemakaian tercatat otomatis di `data/log-penggunaan-model.jsonl` (runner mencatat tiap panggilan); runner memberi peringatan bila hari ini sudah ≥15 panggilan. Watchdog memeriksa hitungan ini — bila kuota habis di tengah hari, tugas Hydrogen ditunda ke besok (jangan pakai model berbayar sebagai jalan pintas).

---

## Bagian yang ditempel ke SETIAP SKILL.md (verbatim, sesuaikan nama agent)

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
