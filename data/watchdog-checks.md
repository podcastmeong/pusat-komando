# Daftar Periksa Watchdog — Tugas Harian yang Wajib Ada Buktinya

**Dipakai oleh:** cron `watchdog-tugas-harian` (tiap 1 jam, hanya bertindak 08.00–21.00 WIB).
**Aturan:** bukti = file/baris log bertanggal HARI INI. Bila bukti kosong dan tenggat sudah lewat → picu ulang jobnya SEKALI (maks 2×/tugas/hari, dihitung dari `data/log-eksekusi.jsonl`). Bila sudah 2× tetap kosong → status GAGAL + eskalasi ke Cipta. **JANGAN picu ulang pengiriman pesan (penawaran/DM) tanpa memeriksa log pengiriman dulu** — bila log menunjukkan sudah terkirim, JANGAN kirim ulang (cegah ganda).

| Job (cron id) | Agen | Bukti yang diharapkan (hari ini) | Tenggat |
|---|---|---|---|
| rencana-pagi-0500 | A03 | Rencana pagi terkirim ke chat Cipta (laporan 05.00) | 06.00 |
| persiapan-video-0630 | A11 | Naskah/persiapan video hari ini di folder video harian | 07.00 |
| produksi-utama-0900 | A18/A13/A14 | File aplikasi/website/game baru atau update repo hari ini | 12.00 |
| penawaran-baru-0900 | A25 | `log-penawaran-YYYY-MM-DD.csv` — pukul 10.00 ≥10 baris TERKIRIM; pukul 11.30 ≥20 baris TERKIRIM | 11.30 |
| gerakan-operasional-1000 | A04/A05/A08/A29/A30 | Laporan gerakan operasional 10.00 terkirim | 11.00 |
| distribusi-1300 | A31 | Bukti distribusi/publish hari ini | 14.00 |
| produksi-ebook-harian | A16 | File eBook baru hari ini | 15.00 |
| produksi-pod-harian | A15 | Desain POD baru hari ini | 16.00 |
| produksi-tulisan-harian | A17 | Puisi/cerpen/cerbung baru hari ini | 17.00 |
| paket-konten-harian | A19 | Paket konten 17.00 selesai | 18.00 |
| follow-up-penjualan-harian | A25 | Follow-up 19.30 jalan + laporan (balasan toko) | 21.00 |
| laporan-malam-2000 | A01 | Laporan malam 20.00 (PPT + ringkasan) terkirim | 21.00 |
| produksi-video-2100 | A11 | Video hari ini selesai (cek mulut per klip) | 22.00 |
| cek-dm-toko | A26 | Cek DM 2×/hari jalan (balasan penawaran) | 21.00 |
| cek-email-customer-cepat | A27 | Cek tiap 30 menit jalan (draf balasan bila ada email customer) | 21.00 |
| upload-foto-harian | A12 | Foto batch hari ini ter-upload (ledger diperbarui) | 21.00 |
| cari-lowongan-freelance-0800 | A28 | Draf lowongan hari ini (draf saja, info ke Cipta) | 09.00 |

**Catatan:** `cek-chat-customer-wa` SENGAJA nonaktif (perintah Cipta 19 Nov "Saat ini belum. Nanti") — JANGAN dimasukkan ke daftar periksa sampai Cipta bilang jalan. `cek-email-a27-0530/1930` dan `cek-hibah-harian` hanya info — buktinya laporan ke chat bila ada temuan.
