# Panduan Playwright — Tes Browser (Tahap 5, BINTANG COMMAND CENTER 4.0)

Terverifikasi 21 Nov 2026: Playwright Python **1.65.2**, Chromium **1255** + headless shell, terpasang di VM ini. Dipakai untuk tes halaman toko/demo sebelum dilaporkan selesai.

## Cara tes cepat (cek console error halaman lokal)

```bash
PK_NO_LOG=1 python3 /tmp/pw_test.py "file:///home/hatch/workspace/tmp/podcastmeong.github.io/toko.html"
```

Skrip `/tmp/pw_test.py` membuka halaman, menunggu 4 detik, lalu mencetak judul + jumlah `console.error` + `pageerror`. Kriteria lulus: **0 JS page error**. (Bila skrip terhapus, buat ulang dari pola di bawah.)

Pola minimal (sync API):

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page()
    pg.on("pageerror", lambda e: print("JS ERROR:", e))
    pg.on("console", lambda m: print("console.", m.type, m.text) if m.type == "error" else None)
    pg.goto("file:///home/hatch/workspace/tmp/podcastmeong.github.io/toko.html", timeout=30000)
    pg.wait_for_timeout(4000)
    b.close()
```

Untuk melihat URL sumber daya yang gagal dimuat, tambahkan:

```python
pg.on("requestfailed", lambda r: print("GAGAL:", r.url, "::", r.failure))
```

## Batasan yang sudah diketahui (bukan bug halaman)

- Chromium headless di sandbox VM **tidak bisa menjangkau CDN Google** (fonts.googleapis.com, googletagmanager.com) dan layanan penghitung eksternal (abacus) — gagal dengan `net::ERR_TUNNEL_CONNECTION_FAILED`. Itu kegagalan jaringan sandbox, bukan kesalahan halaman.
- Tes 21 Nov 2026 pada `toko.html` lokal: **0 JS page error**, 4 request eksternal gagal (Google Fonts, gtag GA4, 2× abacus). Halaman dinyatakan lulus bila 0 JS error.
- Selalu tes pada **file lokal byte-identik** (clone repo), bukan URL live — agar yang diuji sama persis dengan yang akan diterbitkan.

## Catatan

- Playwright di sini adalah **alat tes**, bukan alat aksi browser untuk agen — JANGAN daftarkan sebagai alat di Tool Registry (kemampuan aksi browser di luar cakupan Tahap 5 ini).
- Jangan jalankan tes Playwright bersamaan dengan `npm install` berat (memori VM ketat) — bisa OOM.
