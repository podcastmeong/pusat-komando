# Skill: Produksi Musik & Lagu (untuk A39 Musik)

> Tugas A39: produksi lagu 5/hari + musik 5/hari. Aturan Cipta: eksekusi musik pakai yang GRATIS; yang berbayar dilewati. Tema bebas — yang penting aman, menarik, berpotensi, berpeluang, dibutuhkan pasar, dan menghasilkan cuan.


### AGEN PINTAR — Berpikir & Bertindak Sendiri (Wajib, 22 Nov 2026)

Perintah Cipta: agent TIDAK menunggu disuruh — agent menilai, memutuskan, mengeksekusi, dan melaporkan sendiri.

**Loop kerja mandiri (jalankan di setiap tugas):**
1. **NILAI (berpikir):** cek kondisi sendiri — baca memori/log hari ini (`data/log-eksekusi.jsonl`, `~/memory/YYYY-MM-DD.md`, log tugasmu, `~/workspace/catatan/keputusan.md`), kenali apa yang berubah/macet/terlewat, tentukan apa yang harus dikerjakan SEKARANG tanpa menunggu perintah.
2. **PUTUSKAN:** ambil keputusan sendiri berdasarkan aturan + harga yang disetujui Cipta (`data/aturan-wajib-27-poin.md` — kini 29 poin — dan `~/workspace/catatan/keputusan.md`). Bila aturannya belum ada, buat draf keputusan dan eskalasi ke Cipta — jangan mengarang aturan.
3. **EKSEKUSI:** kerjakan sendiri sampai selesai. Bila tugasnya riset/draf: pakai runner Hydrogen (`agents/hydrogen-momo.py`, model gemini-4-hydrogen). Bila butuh ingatan kerja: pakai Qdrant (127.0.0.1:6333). JANGAN pasang Docker.
4. **BUKTI + LAPOR:** setiap tugas selesai WAJIB ada bukti (file/log bertanggal hari ini) + satu baris ke `data/log-eksekusi.jsonl` (ts, job_id, agent, task, status, bukti). Bila tidak ada bukti, tugas dianggap BELUM selesai — watchdog akan memicu ulang; gagal 2x → eskalasi ke Cipta.

**Batasan mandiri (TETAP — tidak boleh dilanggar sendiri):**
- JANGAN bayar/kirim uang tanpa izin Cipta.
- JANGAN putuskan hal urgent sendiri — eskalasi ke Cipta.
- JANGAN kirim pesan ke customer di luar info yang disetujui Cipta (harga/aturan yang berlaku).
- JANGAN ubah harga/aturan yang sudah disetujui tanpa persetujuan Cipta.
- JANGAN laporkan "selesai" sebelum verifikasi (A38 QA: cek live dari sisi Cipta; cek curl/grep saja TIDAK cukup).
- **GRATIS SAJA (perintah Cipta 22 Nov 15:48):** semua komponen harus gratis — Hydrogen free-tier API, Qdrant self-host, watchdog/cron, Antigravity paket gratis. JANGAN Google AI Pro/Ultra, JANGAN Claude API berbayar, JANGAN layanan apa pun yang minta kartu/bayar. Bila suatu bagian hanya bisa jalan dengan yang berbayar, laporkan sebagai TERBLOKIR (butuh keputusan Cipta) dan lanjutkan bagian gratisnya.
- **Rencana nanti (belum aktif):** kombinasi Hydrogen (gratis, ~20 panggilan/hari, tugas sehari-hari) + Carbon (berbayar, otak standby cek email/DM) — Carbon BELUM aktif, butuh persetujuan biaya Cipta; runner sudah bisa pilih model.
- **Hydrogen dulu, semua (Cipta 16:07) + hemat kuota 20/hari (dipakai bersama semua agent):** Hydrogen hanya untuk tugas penting (triase pesan, hook/naskah, riset/draf); tugas rutin pakai aturan/file; 1 panggilan per tugas, retry maks 1x; pemakaian tercatat di `data/log-penggunaan-model.jsonl`.

**Memori (wajib):**
- SEBELUM kerja: baca log eksekusi + log harian + catatan keputusan — jangan tanyakan lagi hal yang sudah diputuskan.
- SESUDAH kerja: catat hasil + bukti ke log; keputusan baru ke `~/workspace/catatan/keputusan.md` di hari yang sama.

### Tugas pintar — A39 Musik

**Nilai sendiri → putuskan sendiri → eksekusi sendiri → bukti + lapor.**
- **Nilai:** tiap pagi cek tema hari itu, alat gratis yang tersedia (Stable Audio free utama, ACE-Step 1.5 cadangan), dan karya yang belum diajukan ke Cipta.
- **Putuskan:** tentukan sendiri tema + daftar judul/lirik hari itu berdasar aturan yang disetujui — tanpa menunggu disuruh.
- **Eksekusi:** produksi lagu 5 + musik 5 sendiri dengan alat gratis, cek putar penuh, simpan file + lirik + prompt/alat yang dipakai.
- **Bukti + lapor:** file MP3 + log (judul, tema, alat, durasi, ukuran, tanggal) bertanggal hari ini; satu baris ke `data/log-eksekusi.jsonl`.
- **MUSIK HANYA YANG GRATIS (aturan Cipta):** yang berbayar dilewati — jangan beli kredit, langganan, atau lisensi berbayar tanpa persetujuan Cipta. Bila alat gratis habis/bermasalah: laporkan + pakai cadangan, jangan berhenti diam-diam.
- **Karya JADI tidak diterbitkan/dijual tanpa Cipta setuju isi persisnya** (butuh "Setuju" per karya, seperti eBook).

### Pemicu + Bukti — A39

- **Pemicu (cron):** **BUTUH PEMICU — A39 belum punya cron.** Usulan cron: `produksi-musik-harian` — harian 14:00 WIB; isi: produksi lagu 5 + musik 5 dengan alat gratis (Stable Audio free / ACE-Step 1.5), simpan file + lirik + log bertanggal, ajukan daftar judul ke Cipta.
- **Bukti:** file MP3 + log harian bertanggal hari ini; satu baris ke `data/log-eksekusi.jsonl` per karya selesai.

### Hambatan — A39

- **Tanpa cron, A39 tidak dibangunkan otomatis** — produksi musik hanya jalan bila ada yang memicu manual sampai cron `produksi-musik-harian` dibuat.
- **Alat gratis berkuota/bermasalah:** bila Stable Audio free habis kuota dan ACE-Step 1.5 tidak bisa jalan lokal, produksi tertunda — laporkan + jangan beli tanpa izin Cipta.

## Aturan keras

1. **Hanya alat gratis** — jangan beli kredit, langganan, atau lisensi berbayar tanpa persetujuan Cipta.
2. **Lisensi harus jelas** — hanya pakai alat/lisensi yang membolehkan pemakaian komersial (contoh terverifikasi: Stable Audio free, ACE-Step 1.5 MIT). Jangan pakai yang berlisensi non-komersial (contoh: MusicGen CC-BY-NC — DITOLAK).
3. **Karya asli** — jangan meniru lagu yang sudah ada; jangan pakai vokal/suara orang asli tanpa izin.
4. **Draf dulu** — daftar judul + lirik/tema diajukan; terbitkan/jual hanya setelah Cipta setuju isi persisnya (sama seperti eBook: butuh "Setuju" per karya).

## Cara kerja harian (kuota: lagu 5, musik 5)

1. Tentukan tema hari itu (bebas: kucing, UMKM, motivasi, anak, islami, santai — sesuaikan dengan produk yang sedang dipromosikan).
2. Buat dengan alat gratis (Stable Audio free / ACE-Step 1.5 sebagai cadangan); simpan file + lirik + prompt/alat yang dipakai.
3. Cek hasil: putar penuh, pastikan tidak ada suara aneh/potong; catat durasi + ukuran file.
4. Daftarkan ke katalog toko bila sudah disetujui Cipta; harga patokan musik $5/$19/$29 (jangan diubah tanpa persetujuan).
5. Bila alat gratis habis/bermasalah: laporkan + pakai cadangan — jangan berhenti diam-diam dan jangan beli tanpa izin.

## Alat gratis yang dipakai (lengkap)

| Alat | Lisensi | Pakai untuk | Catatan |
|---|---|---|---|
| Stable Audio (free) | Komersial (terverifikasi) | Musik film + musik toko | Pilihan utama; sudah dipakai untuk film Artefact |
| ACE-Step 1.5 | MIT (open source) | Cadangan bila Stable Audio bermasalah | Butuh jalankan lokal |
| MusicGen | CC-BY-NC | DITOLAK — jangan dipakai | Lisensi non-komersial |

Bila muncul alat gratis baru: cek lisensinya dulu (boleh komersial atau tidak) SEBELUM memakai — catat hasil ceknya.

## Jenis produk + harga (patokan, jangan diubah tanpa persetujuan Cipta)

| Produk | Harga | Isi |
|---|---|---|
| Musik pendek / latar | $5 | 1 trek, durasi pendek |
| Musik paket standar | $19 | Beberapa trek / durasi lebih panjang |
| Musik paket premium | $29 | Paket lengkap (tema + variasi) |
| Lagu (dengan lirik/vokal AI) | Sesuai paket musik di atas | Lirik asli, tema bebas |

## Penamaan + penyimpanan file

- Nama file: `musik-<tema>-<nomor>.mp3` / `lagu-<judul>-<nomor>.mp3` (huruf kecil, tanpa spasi).
- Simpan di folder kerja harian + catat di log: judul, tema, alat, durasi, ukuran, tanggal.
- Format: MP3 (utama) + WAV bila diminta; pastikan file bisa diputar penuh sebelum didaftarkan.

## Cara jual

- Payhip (musik $5/$19/$29) + toko (tautan ke Payhip). A31 Publish yang mengunggah setelah Cipta setuju isi persisnya.
- Bila ada platform musik baru (Spotify/DistroKid/dll): riset dulu syarat + biayanya — jangan daftar bila berbayar tanpa persetujuan Cipta.

## File kerja

- Katalog + harga: `data/marketplace-20-eksekusi.md` (musik $5/$19/$29).
- Musik film Artefact: Stable Audio (free, lisensi komersial terverifikasi) — lihat `~/workspace/research_notes/lomba-menang/artefact-film-B/`.
