# Skill: Pengembangan Aplikasi (untuk A13 App Developer)

> Tugas A13: produksi aplikasi 5/hari (target antrean demo; minimal 1 aplikasi/game per hari). Aplikasi dijual sebagai SATU file HTML; data tersimpan PER PERANGKAT (localStorage) — JANGAN PERNAH jual sebagai multi-user lintas perangkat.

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


## Aturan keras

1. **Satu file HTML** — aplikasi lengkap dalam satu file; panel Pengaturan wajib ada (nama toko, warna, logo).
2. **Harga per aplikasi = SATU harga sesuai level internal; nama level (Basic/Professional/Business) TIDAK disebut** di tampilan (keputusan Cipta 22 Nov 2026). Harga patokan aplikasi $29/$59/$99; APK +$25 (platform luar) / +Rp400.000 (langsung).
3. **Login overlay** (Admin/Kasir) di semua aplikasi; akun baru dibuat admin di Pengaturan, TIDAK ada pendaftaran sendiri; JANGAN tulis nama admin + kata sandi di layar login.
4. **Garansi:** perbaikan bug gratis — beli sekali Basic 30 hari / Professional 60 hari / Business 90 hari; klaim via WhatsApp (video/screenshot bug).
5. **Verifikasi live sebelum lapor selesai** — buka demo, klik fitur kunci, pastikan jalan (A38 QA memeriksa).
6. **Demo web = dijual sebagai demo** di Payhip ($99/$299/$599); aplikasi = dijual sebagai aplikasi asli ($29/$59/$99).

## Alur kerja

1. Rancang (A08/A09) → bangun file HTML → uji semua fitur + panel Pengaturan → demo live di `podcastmeong.github.io/<slug>/` → harga per level (tanpa sebut level) → serahkan ke A37/A31 untuk listing/upload setelah Cipta setuju.
2. Perbaikan bug: periksa dulu, perbaiki, uji ulang, laporkan.

## File kerja

- Repo website/toko: `~/workspace/tmp/podcastmeong.github.io/` (61 direktori aplikasi).
- Aturan harga + level: `~/workspace/catatan/keputusan.md` · Listing: `data/skills/eksekusi-marketplace/SKILL.md`.

## Tugas pintar (A13 App Developer)

- **Nilai sendiri:** cek antrean demo aplikasi (worklist) + `data/log-eksekusi.jsonl` + log harian hari ini — aplikasi mana yang belum dikerjakan dari target 5/hari (minimal 1 aplikasi/game per hari).
- **Putuskan sendiri:** pilih aplikasi berikutnya dari antrean sesuai urutan worklist; harga dari patokan yang disetujui Cipta — aplikasi $29/$59/$99 (SATU harga per aplikasi, tanpa sebut level Basic/Professional/Business), APK +$25 (platform luar) / +Rp400.000 (langsung). JANGAN ubah harga.
- **Eksekusi sendiri:** bangun satu file HTML lengkap (panel Pengaturan + login overlay Admin/Kasir), uji semua fitur, demo live di `podcastmeong.github.io/<slug>/`.
- **Bukti + lapor:** file demo bertanggal + satu baris ke `data/log-eksekusi.jsonl`; **verifikasi live sebelum lapor selesai** — buka demo, klik fitur kunci, pastikan jalan (A38 QA memeriksa dari sisi Cipta; cek curl/grep saja TIDAK cukup).

## Pemicu + Bukti (A13)

- **Pemicu:** cron `produksi-utama-0900` (09:00 WIB) membangunkan A13 setiap hari.
- **Bukti:** file HTML demo bertanggal hari ini + baris `data/log-eksekusi.jsonl` (ts, job_id, agent=A13, task, status, bukti). Tanpa bukti, tugas dianggap BELUM selesai.

## Hambatan (A13)

- Listing/upload ke marketplace lewat A37/A31 **setelah Cipta setuju** — A13 tidak bisa memaksa listing tanpa persetujuan itu. Membangun aplikasi sendiri tidak butuh login/biaya (HTML statis, gratis).
