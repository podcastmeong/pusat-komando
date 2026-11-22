# Otomasi Agen — Hasil Tukar Pikiran 5 AI (22 Nov 2026)

**Tanggal:** 22 Nov 2026 | **Status:** solusi disepakati 3 AI, eksekusi prioritas 1 jalan | **Sumber:** ChatGPT (chat "Otomasi Agen AI SatuKiki"), DeepSeek (chat "Otomasi agen"), Gemini (22 Nov 13.50 WIB); Claude GAGAL (akun belum terverifikasi — hanya Cipta yang bisa verifikasi di Portal Verifikasi Anthropic); Copilot TERTUNDA (menunggu kode Microsoft dari Cipta — referensi kode tidak bisa dipakai browser untuk live.com, digitnya harus dari Cipta).

DOKUMEN RAHASIA PERUSAHAAN — tidak dipublikasikan.

## Masalah (disepakati ketiga AI + audit Muse)

Agent diam saat Muse sibuk BUKAN karena kurang pintar atau kurang instruksi. Penyebabnya: **tidak ada mesin eksekusi + pengawas.** File instruksi (SKILL.md, agents.json) adalah teks — pasif. Cron hanya "mengetuk pintu" (memanggil), tapi tidak memastikan pekerjaan selesai dengan bukti. Buktinya dari audit 22 Nov 13:48: 30+ cron aktif, tapi **TIDAK ADA cron untuk jendela penawaran 09.00–11.00** (hanya follow-up 19.30) — itu sebabnya hari ini 0 penawaran terkirim di jendela pagi. Beberapa cron hanya membuat draf/laporan, bukan mengeksekusi.

## Solusi (konsensus 3 AI)

1. **Cron = kontrak eksekusi, bukan pengingat.** Setiap cron harus punya Definition of Done (syarat selesai yang terukur + bukti). Contoh A25: "kirim 20 penawaran, tiap penawaran tercatat di log dengan status terkirim; selesai = 20 baris TERKIRIM terverifikasi." Pecah 20 penawaran jadi batch kecil (4×5 tiap ~25 menit) supaya satu batch gagal tidak menggagalkan semuanya; jeda ≥3 menit antar DM; ID unik per pengiriman (jangan kirim ganda saat retry).
2. **Watchdog terpisah dari agen yang diawasi.** Skrip/proses deterministik tiap 15–30 menit yang memeriksa LOG (bukan status "running"): jadwal wajib yang tidak jalan, hasil kosong (EMPTY), error. Retry maks 2–3× dengan jeda; bila tetap gagal → tandai NEEDS_HUMAN_ATTENTION + eskalasi ke Cipta. Jangan retry pengiriman pesan tanpa memeriksa status kirim sebelumnya.
3. **Log terstruktur per tugas.** Setiap eksekusi menulis satu baris (JSON/CSV): job_id, agent_id, scheduled_at, started_at, finished_at, status (SUCCESS/EMPTY/ERROR), jumlah output nyata, bukti/tautan. Log per TUGAS, bukan per agen — supaya ketahuan job mana yang konsisten tidak jalan. Rekap harian (17.00/20.00): 3 angka — Berjalan & Ada Output / Kosong-Gagal / Tidak Terjadwal-Nonaktif.
4. **Antrean kerja (task queue) + database tugas.** Riset → simpan prospek ke database → buat tugas untuk A25 → A25 ambil tugas → eksekusi → simpan hasil → watchdog verifikasi. Jangan andalkan komunikasi antar file instruksi.

## Batas jujur (disepakati ketiga AI)

- File instruksi TIDAK BISA "bangun sendiri" — model bahasa stateless antar pemanggilan; tanpa pemicu eksternal (cron/watchdog/event), agen tidak pernah dieksekusi. Otomatisasi sejati terjadi di lapisan orkestrasi, BUKAN di dalam file agen. Jangan tambah kompleksitas di file instruksi untuk "menyuruh diri sendiri".
- LLM tidak menjamin eksekusi 100% deterministik — bisa melewatkan langkah atau mengarang status "selesai". Validasi hasil harus dipegang kode/workflow, bukan instruksi.
- 40 agen paralel ≠ kapasitas 40 orang — biaya token/API, rate limit, konflik data (dua agen hubungi prospek yang sama), kebisingan koordinasi. Kelompokkan peran jadi unit kerja yang jelas.
- Otomatisasi penuh tetap punya batas: keputusan berisiko (refund, komplain keras, nego harga khusus) tetap eskalasi ke manusia; pengiriman massal WA berisiko dibatasi/diblokir bila tidak terukur.
- Prinsip baru (ChatGPT): tidak ada tugas tanpa jadwal/pemicu; tidak ada jadwal tanpa fungsi eksekusi; tidak ada eksekusi tanpa pencatatan; tidak ada status selesai tanpa bukti; tidak ada kegagalan yang boleh diam-diam; tidak ada retry yang menyebabkan tindakan ganda.

## Prioritas (konsensus 3 AI)

1. **Hari 1–2 — mesin eksekusi penjualan:** cron jendela 09.00–11.00 dengan DoD 20 penawaran terkirim + log. ✅ DIEKSEKUSI 22 Nov 13:52 — cron `penawaran-baru-0900` dibuat (harian 09.00, kontrak eksekusi + log CSV harian + batch 4×5 + template DM baru + kanal yang dibatasi dicatat); jalan pertama Senin 23 Nov 09.00 WIB.
2. **Hari 3–5 — watchdog + log terpusat:** aktifkan watchdog minimal + ubah tugas "draf/laporan" jadi output nyata + log standar. ⏳ BERIKUTNYA.
3. **Hari 6–7 — perluasan ke 40 agen:** audit 30+ cron, klasifikasikan (eksekusi/laporan/pengingat/nonaktif), dashboard status 40 agen. ⏳ BERIKUTNYA.

## KOREKSI PENTING — cek chat customer WA TETAP NONAKTIF (alasan: perintah Cipta)

Ketiga AI menyarankan "aktifkan kembali jadwal cek chat WA". **JANGAN — jadwal itu nonaktif karena perintah Cipta sendiri 19 Nov 15:58: "Nanti kamu tolong Bantu jawab bila ada customer nanya. Saat ini belum. Nanti."** Jadwal `cek-chat-customer-wa` tetap nonaktif sampai Cipta bilang jalan. Bila nanti diaktifkan, harga di isi tugasnya masih IDR lama (video promo Rp75.000/150.000/250.000; eBook Rp29.000) — harus diperbarui dulu ke aturan harga lokal/global.
