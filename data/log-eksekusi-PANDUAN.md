# Log Eksekusi — Kontrak Pencatatan Hasil Tugas

**File:** `data/log-eksekusi.jsonl` (satu baris JSON per pemeriksaan/eksekusi; log per TUGAS, bukan per agen).
**Ditulis oleh:** cron eksekusi (tiap tugas yang selesai/gagal) + cron `watchdog-tugas-harian` (tiap pemeriksaan).
**Dibaca oleh:** watchdog (untuk hitung retry + deteksi tugas yang konsisten kosong) dan laporan malam 20.00 (rekap 3 angka: Berjalan & Ada Output / Kosong-Gagal / Tidak Terjadwal-Nonaktif).

## Format satu baris

```json
{"ts":"2026-11-23T11:30:00+07:00","job_id":"penawaran-baru-0900","agent":"A25","task":"kirim 20 penawaran toko","status":"OK","jumlah_output":20,"bukti":"goals/daily-oyen-60-second-podcast-videos/hidden_files/log-penawaran-2026-11-23.csv (20 TERKIRIM)"}
```

## Status

- `OK` — bukti ada dan memenuhi target.
- `SEBAGIAN` — bukti ada tapi di bawah target (tulis jumlah_output yang sebenarnya).
- `KOSONG` — tugas jalan (atau tidak jalan) tapi tidak ada bukti output.
- `GAGAL` — tugas error / gagal setelah retry.
- `DIPICU_ULANG` — watchdog memicu ulang job (tulis `retry_ke`: 1 atau 2).
- `NONAKTIF` — job sengaja nonaktif (tulis alasannya, mis. perintah Cipta).

## Aturan

- Satu baris per tugas per pemeriksaan — jangan menimpa baris lama.
- `jumlah_output` = jumlah output NYATA yang terverifikasi (bukan rencana, bukan draf).
- `bukti` = path file / ID / tautan hasil — harus bisa dicek ulang.
- Retry maks 2× per tugas per hari; hitung dari baris `DIPICU_ULANG` hari ini di file ini.
- Jangan pernah menulis status `OK` tanpa bukti.
