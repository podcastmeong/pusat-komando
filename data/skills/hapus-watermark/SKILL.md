# Skill: Hapus Watermark + Kebijakan (untuk A11 AI Video Producer, diawasi A04 Quality Control)

> Perintah Cipta 23 Nov 2026 — Masalah: klip gratis Kling ber-watermark ("KlingAI 4.0" kanan bawah); Manus watermark muncul mulai klip ke-3/4. Alat lokal `hapus-watermark.py` (di folder skill ini) membersihkan watermark video hasil generate sendiri — teruji 23 Nov 2026. TAPI: hapus watermark TIDAK memberi hak komersial. Kebijakan di bawah adalah bagian dari skill ini — melanggarnya = CACAT.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A11 AI Video Producer** | Menjalankan alat ini pada video yang memenuhi kebijakan; mencatat metode + tujuan pakai setiap kali |
| Pengawasan | **A04 Quality Control** | Menegakkan kebijakan di bawah; menolak video yang dibersihkan watermarknya untuk lomba/jualan bila sumbernya tier gratis |

## Aturan keras — KEBIJAKAN WATERMARK (keputusan Cipta 23 Nov 12:36 + 12:38)

1. **Hanya untuk video hasil generate KITA SENDIRI** (Flow/Kling/Dreamina/Manus/dll. yang kita generate). Jangan pernah hapus watermark milik kreator lain.
2. **BOLEH: konten umum + promosi di akun** (sosmed). Contoh: klip Kling free yang watermarknya dihapus untuk konten akun biasa.
3. **LOMBA dan MENAWARKAN PRODUK (jualan): video HARUS bersih dari sumbernya.** Artinya pakai sumber yang memang tanpa watermark + haknya jelas — Flow (tidak ber-watermark) atau paket berbayar (Kling Standard $8,80/bln untuk hak komersial). JANGAN mengandalkan alat ini untuk lomba/jualan.
4. **Hapus watermark TIDAK memberi hak komersial.** Output tier gratis (mis. Kling free: watermark + tanpa hak komersial) TETAP tidak boleh dipakai jualan — yang dihapus hanya tampilan watermarknya, bukan larangan komersialnya.
5. **Manus: watermark biasanya muncul klip ke-3/4** (info Cipta 23 Nov 12:39) — klip pertama biasanya bersih. Rencanakan produksi dengan ini: jangan kaget bila klip awal bersih lalu watermark muncul di tengah seri.
6. **Kling free: watermark + tanpa hak komersial.** Bila video jasa dipakai jualan, jalannya adalah paket berbayar — bukan alat ini.

## Alat

`hapus-watermark.py` (di folder skill ini; salinan kanonik di `~/workspace/goals/daily-oyen-60-second-podcast-videos/hidden_files/hapus-watermark.py`). Butuh: ffmpeg (+ cv2+numpy bila metode inpaint).

```
hapus-watermark.py <video.mp4> [--preset kling] [--metode delogo|inpaint|crop]
                   [--box x,y,w,h] [--out hasil.mp4]
```

Keluar: `<nama>-nowm.mp4` di folder yang sama (audio ikut tersalin, durasi tidak berubah).

### Metode

| Metode | Cara | Kapan dipakai |
|---|---|---|
| `delogo` (default) | Filter ffmpeg delogo — blur/interpolasi kotak watermark | Cepat, tanpa unduhan; cukup untuk watermark statis kecil |
| `inpaint` | Inpainting OpenCV Telea per frame | Lebih halus dari delogo; lebih lambat |
| `crop` | Potong strip bawah berisi watermark | Bila watermark di tepi bawah dan kehilangan sedikit frame tidak masalah |

### Preset

| Preset | Posisi (kanvas 720×1280) | Keterangan |
|---|---|---|
| `kling` | x=540, y=1205, w=175, h=65 (kanan bawah) | Logo "KlingAI" — koordinat diskalakan otomatis bila resolusi beda |
| `custom` | `--box x,y,w,h` | Tentukan sendiri kotaknya |

**Tidak didukung penuh:** watermark BERGERAK (mis. TikTok) — delogo hanya menutup satu posisi tetap.

## Uji yang sudah dilakukan (23 Nov 2026)

- File: `kolam-ikan/kling-part1-10detik.mp4` (Kling, 720×1280, watermark "KlingAI 4.0" kanan bawah) → `kling-part1-10detik-nowm.mp4` (10,04 dtk, metode delogo preset kling).
- Verifikasi: frame t=5 dicek visual — watermark HILANG, gambar lain utuh, durasi sama.
- Aturan: sebelum memakai hasil untuk apa pun, cek 1 frame (awal + tengah + akhir) bahwa watermark hilang dan gambar tidak rusak.

## Cara pakai (langkah)

1. Pastikan video memenuhi kebijakan (aturan 1–4 di atas) — bila untuk lomba/jualan, BERHENTI, pakai sumber bersih (aturan 3).
2. Tentukan preset (`kling`) atau `--box` custom (cek frame dulu untuk posisi watermark).
3. Jalankan: `python3 data/skills/hapus-watermark/hapus-watermark.py <video.mp4> --preset kling --metode delogo`
4. Cek hasil: ekstrak frame awal/tengah/akhir (`ffmpeg -vf select=...`), pastikan watermark hilang + gambar utuh.
5. Catat di `data/log-eksekusi.jsonl`: file sumber, metode, tujuan pakai (konten umum/promosi — bukan lomba/jualan).

## Bukti + lapor

- Setiap video yang dibersihkan: satu baris `data/log-eksekusi.jsonl` (ts, agent A11, file sumber, metode, tujuan pakai).
- Bila A04 menemukan video lomba/jualan yang watermarknya dihapus dari sumber gratis: verdict CACAT, video ditarik, tulis ke `~/workspace/catatan/keputusan.md` di hari yang sama.
