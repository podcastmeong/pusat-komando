# TESTING — Checklist Pengujian AI Business Autonomous Agent 3.0

**Diterapkan:** 21 Nov 2026 (adaptasi dari "Checklist pengujian" di starter kit Share ChatGPT #17).
**Aturan:** jangan klaim selesai sebelum cek di bawah lolos. Bila satu cek gagal, tulis apa yang gagal — jangan tutupi.

## 1. Konfigurasi agent

- [x] `data/agents.json` valid JSON (python `json.load`).
- [x] 8 direktorat, 62 agent spesialis (8+9+7+6+7+11+7+7).
- [x] Setiap agent punya `code`, `task`, `mapped_to`, `status`, `authority` (hijau/kuning/merah).
- [x] Keputusan spec tercatat: Hybrid, Rp0, Penjualan, persetujuan hanya tindakan penting/berisiko.

## 2. Dashboard (Pusat Komando)

- [x] `python -c "import app; app.build_app()"` jalan tanpa error (venv `~/workspace/tmp/venv-pk/bin/python`, env bersih tanpa proxy) — 21 Nov 03:36.
- [x] Jumlah tab = **24** (23 lama + "0 · Command Center") — 21 Nov 03:36, tab tingkat atas dihitung langsung.
- [x] `tests/` lolos — 21 Nov 03:36: **161/161** (`unittest discover`, venv-pk, env bersih). Catatan: angka "55/55" di laporan lama adalah subset lama; suite kini 161 test.
- [x] Live di Faable (https://pusat-komando-972u7.faable.link/): HTTP 200, 1.339.116 byte, 21 Nov 03:37 (commit 71930a1). Tab "0 · Command Center" terverifikasi lewat build_app() + 62 baris agent + 11 baris antrean Approval Center (cek lokal, karena Gradio dirender di sisi klien).

## 3. Workflow n8n (`workflows.json`)

- [x] Valid JSON; 3 workflow; setiap node punya `id`, `name`, `type`, `typeVersion`, `position`, `parameters`.
- [x] Setiap `connections` merujuk node yang ada (dicek otomatis).
- [ ] **Impor ke n8n BELUM diuji** — uji impor + jalankan satu workflow end-to-end, catat hasilnya di sini.
- [ ] Workflow TIDAK boleh mengunggah/mengirim/membayar otomatis: ujung setiap alur adalah "Menunggu persetujuan Cipta".

## 4. Approval Center

- [ ] Tab 0 menampilkan antrean handoff terbuka (draf/diperiksa) — sama isinya dengan tab Papan Handoff.
- [ ] Ubah status handoff di tab Papan Handoff → segarkan tab 0 → status berubah.

## 5. Halaman demo (Share ChatGPT #16)

- [x] https://podcastmeong.github.io/agen-bisnis-otonom-3/ — HTTP 200, 37.873 byte, byte-identik dengan file lokal (commit c35a182).
- [x] JS lolos `node --check`; 0× kata "ChatGPT" di halaman.
- [x] Kartu Kamar Aplikasi muncul 1×; total kartu kamar 73 (chip "Semua (71)" sengaja TIDAK diubah — menunggu keputusan Cipta).
- [x] Perilaku klik di browser (tab direktorat + filter kewenangan) — **lolos 21 Nov 03:37** (Playwright headless, file lokal byte-identik): klik B → panel B terlihat, panel A tersembunyi; filter Merah → 7 dari 13 baris terlihat; filter Semua → 13 baris kembali; 0 console error.

## 6. Halaman demo (Share ChatGPT #17)

- [ ] Dibangun setelah #16 selesai (antre — satu repo, satu push sekali jalan).
- [ ] Verifikasi sama seperti #16 (HTTP 200, byte-identik, node --check, 0× "ChatGPT", kartu kamar).

## Catatan

- Semua cron dijeda 21 Nov 02:49 (STOP Cipta). Pengujian di atas tidak mengaktifkan cron apa pun.
- Bila ada cek yang gagal, catat tanggal + apa yang gagal di bawah ini sebelum melapor selesai.
