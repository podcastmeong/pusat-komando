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

## 7. Pusat Komando v2.0 — Mesin Eksekusi (21 Nov 2026)

- [x] `data/agents.json` valid JSON; versi 2.0; key `agent_lama` (14 entri,
      status "Pasif — non job"); key `platform` per agent Bintang (21
      platform terhubung + 6 belum terhubung tercakup).
- [x] `python -c "import app; app.build_app()"` jalan tanpa error
      (venv-pk, env bersih) — 21 Nov ~05:00: **5 tab** ("0 · Command Center",
      "B · 30 Agent", "C · Dashboard Agent", "🏠 Papan Handoff",
      "🔄 Koordinasi"); API `jalankan_mesin_eksekusi` ada; tombol
      "Jalankan Mesin Eksekusi" ada di tab Dashboard; header menampilkan
      v2.0.
- [x] `tests/` lolos — 21 Nov ~05:00: **220/220** (`unittest discover`,
      venv-pk, env bersih). Termasuk `tests/test_mesin_eksekusi.py` (baru:
      impor, antrean berstatus, eksekusi A12 + A25 mode tugas, audit log,
      persetujuan, status 14 lama = pasif non-job, larangan kirim/bayar,
      CLI tanpa sentuh data nyata) dan pembaruan `test_dashboard.py` +
      `test_koordinasi.py` ke model v2.0.
- [x] Proof run mesin di data asli (tanpa PK_NO_LOG): A12 "ilustrasi eBook
      — Nabi Yunus dan Ikan Paus" (run ME-20261121045453-A12-001, mode
      tugas, prompt gambar nyata) + A25 "Draf penawaran: Balini Petshop"
      (run ME-20261121045454-A25-001, mode tugas, via
      a04_penjualan_harian.draf_personal). Keduanya tercatat di
      `data/mesin_eksekusi_log.json` + `data/activity_log.json` dengan
      status "menunggu persetujuan".
- [x] Dashboard data nyata setelah proof run: total_agent 30, aktif 3
      (A01, A12, A25), aktif sebagian 4, belum jalan 23, mesin_pasif 14,
      terkendala 0, handoff menunggu 11, draf penawaran toko 12.
- [ ] Live di Faable (https://pusat-komando-972u7.faable.link/): HTTP 200 —
      dicek setelah push commit v2.0 (catat hasilnya di sini).

## Catatan

- STOP semua agent 21 Nov 02:49 **DICABUT 21 Nov 04:30** (15 cron aktif
  lagi). Pengujian di atas tidak mengaktifkan cron apa pun; mesin eksekusi
  jalan hanya saat dipicu (tombol/CLI), bukan layanan 24 jam.
- Bila ada cek yang gagal, catat tanggal + apa yang gagal di bawah ini sebelum melapor selesai.
