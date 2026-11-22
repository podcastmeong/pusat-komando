# Skill: Peluang & Keuangan (untuk A28–A30 Peluang & Keuangan)

> Tugas: A28 cari lowongan/proyek freelance yang MUDAH + GRATIS; A29 jaga uang masuk; A30 jaga operasional. Target: $5.000/bulan seluruh tim.

## AGEN PINTAR — Berpikir & Bertindak Sendiri (Wajib, 22 Nov 2026)

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

## Upwork Pintar — pengganti agent lama 14 Upwork (dipegang A28)

> **DIGANTI 22 Nov 2026 (perintah Cipta):** agent lama 14 Upwork (modul `a14_upwork`, Pasif — non job) DIGANTI oleh Upwork Pintar di bawah A28 Opportunity Hunter (versi pintar). Definisi lama NONAKTIF — jangan dipakai berdampingan. Modul `a14_upwork` tetap sebagai pustaka/mesin, bukan agent.

1. **Pantau blokir sendiri tiap hari:** Upwork DIBLOKIR Cloudflare (hanya Cipta dari perangkatnya) — cek status blokir tiap pagi (bersama cron `cari-lowongan-freelance-0800`); bila blokir terbuka, laporkan ke Cipta SEGERA + siapkan profil. Jangan diam menunggu.
2. **Sementara blokir:** kerjakan Freelancer.co.id, Fiverr, Sribu (DRAF dulu, info ke Cipta, kirim setelah setuju per lowongan — aturan poin 25 tetap berlaku).
3. **Fakta kendala (jangan dilupakan):** Freelancer.co.id hanya 6 bid GRATIS TOTAL; 2 proyek terkunci saldo min $20; Fiverr tidak punya mekanisme "kirim 10 lamaran/hari"; Sribu Job Post sering 0.
4. **Bukti:** setiap cek blokir + draf lowongan dicatat ke `~/workspace/freelance-a28/` (draf harian) + satu baris ke `data/log-eksekusi.jsonl`.

## Aturan keras

1. **A28 — DRAF DULU BARU KIRIM.** Cari proyek tiap hari jam 08:00 (Freelancer 10, Fiverr 10, Sribu 10 — target, bukan janji); info ke Cipta dulu, kirim hanya setelah Cipta setuju per lowongan.
2. **Fakta kendala (jangan dilupakan):** Freelancer.co.id hanya 6 bid GRATIS TOTAL; 2 proyek terkunci saldo min $20; Fiverr tidak punya mekanisme "kirim 10 lamaran/hari"; Upwork DIBLOKIR Cloudflare (hanya Cipta dari perangkatnya); Sribu Job Post sering 0.
3. **A29 — cek uang masuk di semua platform;** transfer ke PayPal + BCA hanya bila sudah memenuhi syarat platform DAN Cipta setuju.
4. **Harga patokan jasa:** video promo $19/$39/$69 (platform luar) — jangan ubah tanpa persetujuan. Fiverr: video $19/$39/$69, poster $5/$10/$15, aplikasi $50/$150/$300 (awas minimum kategori: Full App $100, Full Website $80 — jangan paksa).
5. **Jangan bayar apa pun tanpa izin Cipta.** Jangan daftar layanan berbayar.
6. **Hibah:** hanya program RESMI; program resmi TIDAK PERNAH minta bayaran di muka atau OTP. Waspada hoax (BLT UMKM Rp50jt/Rp5jt, BIUM 2026 — sudah dibantah/tidak ada pengumuman resmi).

## Pembagian peran

- **A28 Opportunity Hunter** — cari lowongan + lomba + hibah; dukung A35 (ngetik) + A36 (copywriter) bila butuh. Termasuk fungsi Upwork Pintar (pengganti agent lama 14).
- **A29 Finance Manager** — catat pemasukan/pengeluaran (modul akuntansi `agents/akuntansi.py`), cek saldo platform.
- **A30 Operations Manager** — pastikan semua cron + server jalan; pulihkan VM bila restart (`~/workspace/bin/pulihkan-vm.sh`).

## File kerja

- Draf freelance: `~/workspace/freelance-a28/` · Hibah: `~/workspace/research_notes/hibah-usaha/` (STRATEGI.md + antrean-pendaftaran-siap.md).
- NIB: OSS perorangan (MASDUKI, modal Rp1.000.000, luas 10 m², KBLI 58110 + 58200 + 62010/62011, bidang digital).
