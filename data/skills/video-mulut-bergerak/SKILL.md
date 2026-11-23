# Skill: Video Mulut Bergerak (untuk A11 AI Video Producer + A44 Persiapan Video, diverifikasi A04 Quality Control)

> Perintah Cipta 23 Nov 2026 — Masalah: klip Edukasi 5+6 gagal 2x regenerasi, Detektif suara tertukar, film Artefact tenggat 1 Des belum ada klip. Frames-to-Video + frame awal statis hasilnya gambar nyaris diam + voiceover — mulut kucing TIDAK bergerak. Skill ini berisi pola yang DILARANG dan pola yang harus dicoba, supaya kredit tidak habis untuk pola yang sudah terbukti gagal.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A11 AI Video Producer** | Produksi klip; WAJIB pakai pola di bawah; WAJIB lewati gerbang QC video sebelum lapor "siap" |
| Pengerjaan | **A44 Persiapan Video** | Menyiapkan prompt Flow per klip dari naskah yang disetujui — prompt HARUS memuat perintah gerakan mulut (lihat bawah) |
| Pengawasan | **A04 Quality Control** | Menegakkan gerbang QC video (skill video-qc); satu gerbang gagal = GAGAL, video TIDAK BOLEH dilaporkan siap |

## Aturan keras

1. **DILARANG mengulang pola gagal:** Frames-to-Video + frame awal statis untuk klip kucing BICARA. Pola ini terbukti 2x gagal di Edukasi klip 5+6 (23 Nov) — hasilnya gambar diam. Maksimal 2x generate ulang per klip dengan pola yang sama; bila gagal, GANTI pendekatan, jangan bakar kredit.
2. **Kredit:** Flow akun Lawak Lucu tinggal 10 kredit (23 Nov). Cek saldo tiap akun SEBELUM produksi; bila habis ganti akun; bila semua habis, kabari Cipta (aturan 07:56) — jangan pakai layanan berbayar sebagai jalan pintas.
3. **Suara terkunci:** Momo = MAI_03 (rendah <200 Hz, speed 100), Oyen = MAI_01 (tinggi >200 Hz, speed 110), Bahasa Indonesia. Dialog 17–25 kata per klip 10 detik.
4. **Satu gerbang QC gagal = video GAGAL** — TIDAK BOLEH dilaporkan "siap" / "menunggu persetujuan" (skill video-qc, `~/workspace/custom-skills/video-qc/SKILL.md`).

## Pola yang harus dicoba (urut — coba 1 dulu, bila gagal lanjut 2, dst.)

1. **Text-to-Video TANPA frame awal** — tanpa frame statis sebagai referensi; gerakan dibuat model dari nol. Prompt WAJIB memuat gerakan mulut, contoh: "the orange cat speaks directly to camera, jaw moves clearly while speaking, mouth opens and closes in sync with speech, expressive, natural head movement".
2. **Prompt gerakan rahang eksplisit** (bila tetap pakai Frames-to-Video): tambahkan kalimat gerakan mulut di awal prompt, dan minta gerakan kepala kecil + kedipan — jangan hanya "cat talking".
3. **Kling** untuk klip spesial (alat cadangan utama Cipta).
4. **Manus** cadangan darurat. Video generator Muse DITOLAK permanen (403 region) — jangan dicoba lagi.

## Perbaikan lokal (bila suara salah, bukan gambar)

- Bila pitch karakter tertukar (Oyen <200 Hz atau Momo >200 Hz): perbaiki dengan pitch-shift ffmpeg rubberband — TERBUKTI berhasil di Edukasi klip 4 (247,0 → 162,5 Hz, QC lolos). Jangan generate ulang video hanya karena pitch.

## Gerbang QC video (ringkas — lengkap di skill video-qc)

1. Mulut kucing yang bicara HARUS bergerak — cek frame t=2, t=5, t=8 tiap klip (alat `qc-frame-sheet.py`).
2. Suara konsisten per karakter (Oyen >200 Hz, Momo <200 Hz; alat `qc-pitch.py`).
3. Hanya satu mulut bergerak dalam satu klip.
4. Dialog selesai sebelum detik 10.
5. Judul kuning tebal outline hitam di detik pertama; format 360x640 9:16.

## Bukti + lapor

- Setiap klip: file klip + hasil QC (frame sheet + angka pitch) + satu baris `data/log-eksekusi.jsonl`.
- Verdict QC ditulis ke `~/workspace/catatan/keputusan.md` setiap kali (format di skill video-qc), BUKAN hanya di log harian.
