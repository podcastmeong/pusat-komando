# Rencana Penerapan 3.0 — 7 Langkah Berikutnya (Disesuaikan dengan Kita)

**Sumber:** Share ChatGPT #17, bagian 13 — "Langkah berikutnya" (7 langkah).
**Diterapkan:** 21 Nov 2026. Target akhir spec: "Anda cukup memberikan perintah kepada CEO Agent melalui satu dashboard. CEO membagi pekerjaan, mengawasi seluruh divisi, meminta persetujuan ketika diperlukan, dan melaporkan hasil bisnis kepada Anda."

## Status per langkah

| # | Langkah spec | Status kita | Keterangan |
|---|---|---|---|
| 1 | Instalasi dashboard dan database | **SUDAH** | Pusat Komando live di Faable (24 tab, termasuk "0 · Command Center"); database = JSON di `data/` |
| 2 | Hubungkan Google Sheets dan Apps Script | **DISESUAIKAN — tidak dipakai** | Data tetap JSON: gratis, tanpa server, sudah jalan. Sheets/SQL hanya bila suatu hari butuh multi-user |
| 3 | Instalasi n8n dan impor workflow | **SEBAGIAN** | n8n 2.48.5 lokal sudah ada; `workflows.json` (3 alur) sudah ditulis — **impor + uji end-to-end BELUM dilakukan** |
| 4 | Hubungkan Gemini API | **SUDAH** | Gemini free tier via env `GEMINI_API_KEY`; tanpa key jalan mode template |
| 5 | Aktifkan CEO Agent dan 8 direktorat | **SUDAH** | Muse = CEO; 14 agen = 8 direktorat; tab Command Center live |
| 6 | Uji Approval Center | **SUDAH (uji dasar)** | Approval Center = antrean handoff status "diperiksa" di tab 0; uji = cek antrean terbuka terlihat. Uji kirim-ke-Cipta penuh menunggu ada item antrean nyata |
| 7 | Hubungkan akun IG/TikTok/YT/Threads/email/website/toko | **SEBAGIAN** | Lihat `data/agents.json` per agent. Belum: WA Web rusak; IG/Threads Messages belum terhubung; TikTok @meongcast butuh login Cipta |

## Yang masih terbuka (jujur)

1. **Impor `workflows.json` ke n8n belum diuji.** File valid JSON dan struktur node/koneksi konsisten (dicek `TESTING.md`), tetapi belum pernah diimpor ke n8n sungguhan. Jangan klaim workflow jalan sebelum uji impor.
2. **Tidak ada layanan 24 jam.** Agen pasif; shift malam spec (00.00–06.00) tidak berjalan. Yang berjalan: cron + perintah Muse.
3. **Akun Upwork belum ada** (tertahan Cloudflare, butuh Cipta klik). Fiverr dkk. antre.
4. **14 cron dijeda** (STOP 21 Nov 02:49) — aktifkan lagi hanya bila Cipta bilang jalan.
5. **Angka spec tidak konsisten:** "71 Agent Roles" padahal 8 + 62 = 70; "32 agent spesialis" padahal daftarnya 62; "8 kanal media" padahal rinciannya 7 akun media. Pemetaan memakai daftar 62 dan 9 aset.
6. **Paket ZIP starter kit yang diklaim ChatGPT tidak ada file-nya di sini.** Yang ada: `data/agents.json` + `workflows.json` + `TESTING.md` + dokumen ini + `pemetaan-agen-3.0.md`.

## Urutan kerja berikutnya (bila Cipta bilang jalan lagi)

1. Uji impor `workflows.json` ke n8n lokal; catat hasilnya di `TESTING.md`.
2. Aktifkan kembali 14 cron yang dijeda.
3. Selesaikan langkah 7: tautkan ulang WA Web (Cipta pindai QR), sambungkan IG/Threads Messages (Cipta ketuk tautan connect), login TikTok @meongcast (Cipta sendiri).
4. Buat akun Upwork (Cipta klik Cloudflare) → Agent 14 mulai cari 5 job.
