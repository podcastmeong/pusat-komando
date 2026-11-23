# Skill: Pantau Kuota + Kredit (untuk A29 Finance Manager)

> Perintah Cipta 23 Nov 2026 — Masalah: saldo kredit selalu ketahuan SETELAH habis. Flow tinggal 10, Canva habis sampai 1 Des, Dify Momo kuota 0, Higgsfield 0 — tidak pernah ada peringatan sebelumnya, produksi berhenti mendadak. Skill ini memastikan setiap saldo dipantau harian dan diperingatkan SEBELUM habis.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A29 Finance Manager** | Mencatat pendapatan, biaya, saldo dan laporan; WAJIB menjalankan cek kuota harian ini |
| Pengguna kuota | **A11** (Flow), **A31** (Canva/CapCut), **A16/A32** (Dify), semua agent | Melaporkan pemakaian tiap kali memakai kredit; bila saldo 0, berhenti dan kabari A29 + Cipta |

## Aturan keras

1. **Bila kredit/saldo habis di platform mana pun, KABARI Cipta** (aturan 07:56) — jangan diam, jangan pakai layanan berbayar sebagai jalan pintas tanpa keputusan Cipta.
2. **Cek harian SEBELUM jam kerja (05:00, ikut rencana pagi).** Peringatan datang sebelum produksi, bukan sesudah produksi macet.
3. **Rotasi akun:** bila kredit satu akun habis, langsung lanjut ke akun berikutnya (aturan Cipta 16 Nov) — jangan berhenti. Catat sisa kredit tiap akun saat dipakai.
4. **GRATIS SAJA** — bila suatu bagian hanya bisa jalan dengan yang berbayar, laporkan sebagai TERBLOKIR (butuh keputusan Cipta), jangan beli sendiri.

## Daftar yang dipantau (saldo 23 Nov 2026 — perbarui tiap cek)

| Platform | Saldo 23 Nov | Ambang peringatan | Catatan |
|---|---|---|---|
| Flow (akun Lawak Lucu) | 10 kredit | <20 | 50 → 10 (40 habis untuk 4 regenerasi Edukasi gagal). 7–10 kredit per klip 10 dtk. Total 13 akun ≈ 650 kredit/hari bila penuh |
| Flow (akun lain, 12 akun) | cek harian | <20 per akun | Catat sisa tiap akun saat dipakai |
| Canva AI credits | 0 (habis) | — | Reset 1 Des 2026 07:00 WIB. 5 template tertunda sampai reset |
| Dify (Central Brain) | 200/200 | <50 | Momo (udify.app/chat/CoDt7ugLumQaHElZ) kuota 0 — tunggu atau pasang API key sendiri (menunggu Cipta) |
| Higgsfield | 0 | — | Tidak ada jalur edit film berbayar gratis; proyek privat tidak dapat reward-review |
| Kling / Manus | cek harian | — | Cadangan video (Kling spesial, Manus darurat) |
| Freelancer.co.id | 2 bid gratis tersisa (dari 6 TOTAL) | <3 | Bukan per hari — 6 bid gratis TOTAL; 2 proyek terkunci saldo min $20 |
| Gumroad | batas 10 produk / 24 jam bergulir | — | Slot berikut 23 Nov 13:11 WIB |

## Cara cek + catat

1. **Pagi (05:00):** cek tiap platform di atas, tulis ke `data/log-kuota.json` (tanggal, platform, saldo, ambang, status: AMAN / WASPADA / HABIS) + satu baris `data/log-eksekusi.jsonl`.
2. **WASPADA (di bawah ambang):** laporkan di rencana pagi + siapkan rotasi (akun cadangan / alat cadangan).
3. **HABIS:** kabari Cipta hari itu juga (bukan besok) + catat di `~/workspace/catatan/keputusan.md` bila memengaruhi produksi hari itu.
4. **Pemakaian:** setiap agent yang memakai kredit mencatat pemakaiannya di log yang sama (berapa kredit, untuk apa, sisa berapa) — supaya saldo besok bisa dihitung tanpa menebak.

## Format log (`data/log-kuota.json`)

```json
{"tanggal": "2026-11-23", "platform": "Flow-LawakLucu", "saldo": 10, "satuan": "kredit", "status": "WASPADA", "catatan": "4 regenerasi Edukasi gagal menghabiskan 40"}
```
