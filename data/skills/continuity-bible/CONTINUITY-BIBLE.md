# CONTINUITY BIBLE — Podcast Meong (Oyen & Momo)

**Versi:** 1.0 — 23 November 2026
**Perintah:** Cipta — "Eksekusi yang gratis" (langkah gratis #1 dari riset konsistensi-video-ai-2026-11-23)
**Tujuan:** satu sumber kebenaran agar Oyen & Momo, suara, set, dan bentuknya TETAP SAMA di setiap klip lanjutan. Model video tidak ingat klip sebelumnya — semua yang harus tetap sama dibawa ulang di tiap generasi sebagai gambar + blok teks verbatim dari file ini.
**Aturan pakai:** TIDAK ADA generasi tanpa referensi dari folder ini. Blok bertanda VERBATIM ditempel apa adanya, tidak boleh diubah kata-katanya antar generasi.

---

## 0. FAKTA PEMILIK (jangan dibantah riset)

- **Cipta BERHASIL membuat video 60 detik dan 300 detik dengan Flow.** Alur kerja di bible ini dibangun DI ATAS cara Flow yang sudah terbukti di tangannya (generate klip 10 detik → rangkai di Scenebuilder / concat ffmpeg), bukan menggantinya.
- Riset menyebut Seedance satu-satunya multi-shot ≤30 detik di dalam satu generasi — itu fakta alat, bukan bantahan atas keberhasilan Cipta di Flow. Flow tetap alat utama; Seedance/Dreamina hanya cadangan/penyelamat lip-sync.

---

## 1. IDENTITAS KARAKTER — VERBATIM (jangan diubah kata-katanya)

Tempel blok ini di SETIAP prompt generasi. Bila foto referensi sudah dilampirkan, JANGAN menambah deskripsi wajah lain (kata yang bertentangan dengan foto = drift).

### OYEN — VERBATIM
> Oyen is a realistic orange tabby cat with bright orange fur and darker orange stripes, cream-white chest and muzzle, large round amber eyes, a pink nose, long white whiskers, upright pointed ears, and an expressive cheerful face. He sits on the left.

### MOMO — VERBATIM
> Momo is a realistic solid slate-grey cat with dense grey fur, a round face, large round green eyes, a small pink-grey nose, white whiskers, upright ears, and a calm sceptical expression. She sits on the right.

### Catatan identitas (hasil verifikasi visual 23 Nov 2026)
- **Posisi tetap:** Oyen SELALU kiri, Momo SELALU kanan — di semua set.
- **Kalung Oyen — INKONSISTENSI TERCATAT:** Oyen memakai kalung hitam + lonceng bulat HANYA di set Meja Edukasi (edukasi-ep1-klip-01 s.d. 04), dan TIDAK memakai kalung di set Studio Podcast (promo-pod, promo-jasa). Kanon: **tanpa kalung = tampilan baku studio**; kalung hitam + lonceng = varian khusus set Meja Edukasi saja. Saat generate untuk set studio, pakai ref-oyen-1 / ref-oyen-2 (tanpa kalung). Saat generate untuk set edukasi, pakai ref-oyen-3 (berkalung).
- **Momo tidak pernah memakai kalung** di semua klip LOLOS.
- **Yang tidak boleh berubah:** warna bulu (Oyen oren, Momo abu-abu solid), warna mata (Oyen amber, Momo hijau), posisi kiri-kanan, spesies (kucing realistis — bukan kartun, bukan boneka).

---

## 2. GAMBAR REFERENSI (satu set, dipakai di semua klip)

Folder: `~/workspace/goals/daily-oyen-60-second-podcast-videos/hidden_files/continuity-bible/`
Semua PNG 720×1280 (portrait 9:16). Sumber asli klip Flow 360p — di-upscale 2x lanczos ke 720×1280 untuk upload referensi (tidak menambah detail, hanya menyamakan format akhir).
Setiap gambar diambil dari klip berverdict **LOLOS** di sweep QC 23 Nov 2026 (`~/workspace/catatan/qc-video-platform-2026-11-23.md`) — mulut karakter yang bicara TERBUKA JELAS di detik yang dicatat.

| File | Sumber klip (verdict) | Detik | Isi |
|---|---|---|---|
| `ref-oyen-1.png` | promo-pod/klip3-oyen-cta.mp4 (LOLOS — Oyen terbuka lebar t=2,5) | t=2 | Oyen mulut terbuka LEBAR, dua-shot studio, stand kaos Oyen di tengah meja |
| `ref-oyen-2.png` | promo-jasa/klip3-oyen-dm.mp4 (LOLOS — Oyen terbuka lebar t=5) | t=5 | Oyen mulut terbuka lebar, close-up studio, papan kayu "KikiWorks" |
| `ref-oyen-3.png` | produksi-2026-11-22/edukasi-ep1-klip-01.mp4 (LOLOS — Oyen terbuka jelas t=2) | t=2 | Oyen solo di depan laptop, mulut terbuka, kalung hitam + lonceng (varian edukasi) |
| `ref-momo-1.png` | produksi-2026-11-22/edukasi-ep1-klip-02.mp4 (LOLOS — Momo terbuka tipis t=2,5) | t=6 | Momo mulut terbuka JELAS (gigi terlihat), Oyen diam mulut tertutup, dua-shot meja |
| `ref-momo-2.png` | produksi-2026-11-22/edukasi-ep1-klip-04-FIXED.mp4 (LOLOS — Momo terbuka t=2,5) | t=2 | Momo mulut terbuka, dua-shot meja + laptop game ikan |
| `ref-momo-3.png` | produksi-2026-11-22/edukasi-ep1-klip-04-FIXED.mp4 (LOLOS) | t=5 | Momo mulut terbuka (ujung gigi terlihat), profil bicara, laptop game ikan |

**Catatan validasi Momo:** tidak ada satu pun klip LOLOS yang mulut Momonya terbuka LEBAR seperti Oyen — semua "terbuka tipis". ref-momo-1 (t=6) adalah bukaan mulut Momo paling jelas yang ada. Bila regenerasi Momo menghasilkan bukaan lebih lebar + lolos QC, ganti ref-momo-1 dengan frame baru itu dan catat di Changelog.
**Yang DITOLAK sebagai referensi (dicatat supaya tidak dipakai lagi):**
- edukasi-ep1-klip-03.mp4 — verdict awal LOLOS (tipis), tapi Cipta menemukan detik 28 mulut diam (23 Nov 12:24, terkonfirmasi frame t=27,28,29) → CACAT, jangan dipakai.
- detektif-klip-02.mp4 t=5 — verdict LOLOS (tipis), tapi frame t=5 mulut Momo tertutup → tidak memenuhi syarat "mulut terbuka jelas".
- detektif-klip-03.mp4 t=5 — Oyen mulut terbuka, tapi memakai topi detektif + kaca pembesar (kostum merusak identitas baku) → ditolak.
- Semua klip Momo promo (promo-pod klip2, promo-jasa klip2, promo-kolam klipB) — CACAT, mulut Momo tidak pernah terbuka.

---

## 3. SET SHEET (tiga set yang dipakai serial ini)

### SET A — Studio Podcast Rumahan (promo-pod, promo-jasa, episode podcast)
> A cozy home podcast studio, warm lighting, wooden desk. Oyen sits on the left and Momo on the right, each behind a black studio microphone on a boom arm. A wooden "KikiWorks" nameplate stands in the center of the desk. Behind them: a bookshelf with books, green plants, and warm string lights. An audio mixer sits on the right side of the desk, a mug and cables on the left.

Properti tetap: meja kayu, 2 mikrofon hitam (boom arm), papan kayu "KikiWorks", rak buku, tanaman, lampu string hangat, mixer kanan, mug kiri.

### SET B — Tepi Kolam Koi (promo-kolam)
> An outdoor koi pond garden in soft daylight, mossy rocks, lily pads, orange koi fish swimming in the pond. Oyen sits on the left and Momo on the right on a flat rock at the pond's edge, one black podcast microphone on a stand between them.

Properti tetap: kolam koi, batu berlumut, teratai, ikan koi oren, 1 mikrofon hitam di antara mereka, cahaya siang lembut.

### SET C — Meja Edukasi / Meja Kerja (Edukasi Ep 1, Detektif)
> A wooden work desk in a warm home office, a laptop showing a colorful fish game on screen, a bookshelf with books and green plants behind, warm lamps, a mug and a notebook on the desk. Oyen sits on the left and Momo on the right behind the desk.

Properti tetap: meja kayu, laptop (layar game ikan warna-warni), rak buku, tanaman, lampu hangat, mug, buku catatan. Oyen memakai kalung hitam + lonceng di set ini.

---

## 4. BLOK PROMPT VERBATIM (tempel di setiap generasi)

### 4a. Blok gerakan rahang — VERBATIM (wajib di setiap klip bicara)
> The speaking cat's mouth MUST move visibly while speaking — its jaw opens and closes clearly in sync with every word, wide open when talking, never still while dialogue plays. Only the speaking cat's mouth moves; the other cat stays still with mouth closed. Natural small head movement, smooth shot.

### 4b. Blok format — VERBATIM
> Realistic video, portrait 9:16, 10 seconds, 360p. Two realistic cats sitting side by side, Oyen on the left, Momo on the right. Camera static, no zoom, no pan.

### 4c. Cara merakit prompt klip bicara
1. Blok identitas karakter yang bicara (Bagian 1) + sebutkan kucing satunya "sitting still beside her/him with mouth closed".
2. Blok set (Bagian 3 — pilih A/B/C sesuai video).
3. Blok gerakan rahang (4a) + blok format (4b).
4. Dialog verbatim dari Bagian 6, format: `Dialogue (English, low voice): "..."` untuk Momo, `Dialogue (English, high voice): "..."` untuk Oyen. (Untuk dialog Indonesia: `Dialogue (Indonesian, low/high voice): "..."`.)
5. Lampirkan gambar referensi: ref karakter yang bicara + 1 ref dua-shot set yang sama (maks 3 gambar untuk Veo Ingredients; 2–4 gambar per elemen untuk Kling Elements).

### Contoh jadi — Promo-Jasa klip 2 (Momo, sudah dipakai di spec regenerasi)
> Realistic grey cat Momo speaking directly to camera in a cozy home podcast studio, sitting at a wooden desk behind a black studio microphone, orange cat Oyen sitting still beside her on the left with mouth closed, wooden "KikiWorks" nameplate on the desk, bookshelf with plants and warm string lights behind. Momo's mouth MUST move visibly while speaking — her jaw opens and closes clearly in sync with every word, wide open when talking, never still while dialogue plays. Only Momo's mouth moves; Oyen stays still with mouth closed. Natural small head movement, smooth shot. Dialogue (English, low voice): "Fifteen seconds, seventy-five thousand rupiah. Thirty seconds, one-fifty. Sixty seconds, two-fifty."

---

## 5. ATURAN SUARA (dikunci di luar model)

- **JANGAN pakai suara native model video untuk dialog karakter berulang.** Model (Veo/Kling/Seedance) mensintesis suara dari nol tiap klip — suara pasti berubah antar klip (temuan riset #1). Video di-generate BISU (atau audio native dibuang), dialog ditempel sebagai voiceover.
- **Oyen = MAI_01, tinggi, speed 110, pitch >200 Hz.** Momo = MAI_03, rendah, speed 100, pitch <200 Hz. (Suara terkunci — jangan ganti.)
- **Mux voiceover ke video** (saat perakitan, bukan saat generate):
  `ffmpeg -i video-bisu.mp4 -i voiceover.wav -c:v copy -map 0:v -map 1:a -shortest hasil.mp4`
- **Cek pitch tiap klip** dengan `qc-pitch.py` (di `hidden_files/`): Oyen >200 Hz, Momo <200 Hz. Drift >30 Hz = perbaiki dengan pitch-shift (terbukti di Edukasi klip 4: 247,0 → 162,5 Hz) — JANGAN generate ulang video hanya karena suara salah.
- **Dialog 17–25 kata per klip 10 detik**, selesai sebelum detik 10. Judul kuning tebal outline hitam di detik pertama (2 baris, strip gelap di belakang).

---

## 6. NASKAH RESMI — VERBATIM (dari promo-produk-20-30detik.md, 18 Nov 2026)

### Promo 1 — eBook Kolam
- Klip 1 — Oyen: "Momo! I wrote a book! About me guarding a fish pond! It's hilarious!"
- Klip 2 — Momo: "You chased the fish for sixty pages, Oyen. That's not guarding, that's a buffet."
- Klip 3 — Oyen: "Read it yourself! Link in bio! Only twenty-nine thousand rupiah, fish not included!"
- CTA layar: "Si Oyen Penjaga Kolam Ikan — Rp29.000 — link in bio"

### Promo 2 — POD kaos Zazzle
- Klip 1 — Oyen: "Momo, look! I'm on a T-shirt now! Orange, handsome, and very famous!"
- Klip 2 — Momo: "Famous? You photobombed a T-shirt. The grey cat is the real model here."
- Klip 3 — Oyen: "Get yours! Cute cat shirts, link in bio! Wear Oyen everywhere you go!"
- CTA layar: "Podcast Meong merch — Zazzle — link in bio"

### Promo 3 — Jasa Video Promo KikiWorks
- Klip 1 — Oyen: "Attention pet shops! Want a video like this for your store? We make it!"
- Klip 2 — Momo: "Fifteen seconds, seventy-five thousand rupiah. Thirty seconds, one-fifty. Sixty seconds, two-fifty."
- Klip 3 — Oyen: "DM us now! Your products, our cats, your sales go up! Meow!"
- CTA layar: "KikiWorks — Promo videos for pet shops — DM to order"

Catatan: harga di naskah ini adalah harga 18 Nov 2026 (Rp). Harga toko saat ini sudah USD (jasa video promo $19/$39/$69). Bila dialog menyebut harga, pakai naskah di atas apa adanya untuk voiceover yang SUDAH direkam; untuk naskah BARU, konfirmasi harga terbaru dulu ke toko (jangan mengarang harga).

---

## 7. LARANGAN (keras — pelanggaran = CACAT otomatis)

1. **Frames-to-Video + frame awal statis DILARANG untuk klip bicara** — membekukan mulut secara struktural (akar cacat A1). Klip bicara = Text-to-Video + referensi gambar terkunci.
2. **Jangan deskripsikan wajah dengan kata-kata bila foto referensi sudah dilampirkan** — kata yang bertentangan dengan foto = drift karakter.
3. **Jangan buat referensi baru per episode** — satu set ini dipakai di semua klip. Ganti referensi hanya bila ada frame LOLOS yang jelas lebih baik, dan catat di Changelog.
4. **Jangan generate ulang video hanya karena suara salah** — perbaiki suara dengan pitch-shift / speech-to-speech.
5. **Maks 2x percobaan per klip** — bila masih gagal, ganti pendekatan (Kling Elements → Dreamina OmniHuman / Kling Avatar sebagai penyelamat lip-sync), jangan bakar kredit.
6. **Jangan pakai klip CACAT sebagai referensi** — daftar tolak ada di Bagian 2.
7. **Jangan mengubah posisi kiri-kanan, warna bulu, atau warna mata** antar klip.

---

## 8. ALUR KERJA GENERASI (cara Flow yang sudah terbukti di tangan Cipta)

1. **Siapkan prompt** dari Bagian 4 (identitas + set + rahang + format + dialog verbatim) + lampirkan ref dari Bagian 2.
2. **Generate klip 10 detik di Flow** (Text-to-Video, 360p, portrait 9:16) — akun rotasi, cek saldo live dulu; bila kredit habis, berhenti dan lapor (jangan pakai berbayar tanpa izin).
3. **QC per klip SEBELUM dirakit** — 5 gerbang skill video-qc: (1) mulut yang bicara bergerak (frame t=2,5,8); (2) suara konsisten per karakter (pitch); (3) hanya satu mulut bergerak; (4) dialog selesai sebelum detik 10; (5) judul di detik pertama. Satu gerbang gagal = CACAT. Verdict TERTULIS di `~/workspace/catatan/keputusan.md` SEBELUM publish.
4. **Klip Momo dicek PERTAMA** di setiap video baru (klip Momo paling sering gagal — akar A8, penyebab pasti belum diketahui).
5. **Mux voiceover .wav** (Bagian 5) ke klip yang lolos.
6. **Rakit 60 detik** (6 klip) / 300 detik (30 klip) seperti yang sudah berhasil Cipta lakukan di Flow — via Scenebuilder Flow atau concat ffmpeg, lalu QC final rakitan + verdict tertulis.
7. **Pembuat TIDAK BOLEH meloloskan karyanya sendiri** — pemeriksa kedua wajib (aturan QC 23 Nov 12:21).

---

## 9. PENDAFTARAN REFERENSI — Kling Elements + Veo Ingredients (panduan dashboard)

Pendaftaran dilakukan lewat dashboard di perangkat/browser yang sudah login — JANGAN coba login sendiri dari subagent. Langkah-langkah di bawah untuk Cipta / agen browser.

### 9a. Kling AI — Element Library (kling.ai)
- **Syarat elemen:** 2–4 gambar per elemen (atau dibuat dari video). Elemen bisa karakter, hewan, properti, kostum, atau scene.
- **Langkah:**
  1. Buka kling.ai → login (akun Lawak Lucu, Google lawaklucu182@gmail.com) → menu **Element Library** / **Elements**.
  2. **Create Element → Character**: beri nama `Oyen` → upload `ref-oyen-1.png`, `ref-oyen-2.png`, `ref-oyen-3.png` (3 gambar, depan + dua-shot) → simpan.
  3. **Create Element → Character**: beri nama `Momo` → upload `ref-momo-1.png`, `ref-momo-2.png`, `ref-momo-3.png` → simpan.
  4. (Opsional) **Create Element → Scene**: beri nama `Studio Podcast` → upload 1 frame set A (pakai ref-oyen-2, latar studio lengkap) → simpan. Ulangi untuk `Kolam Koi` (frame klipA promo-kolam) bila perlu.
  5. Saat generate video: pilih mode **Elements / Text-to-Video dengan elemen** → centang elemen `Oyen` + `Momo` (+ scene bila ada) → tempel prompt dari Bagian 4. Maks 3 elemen terikat per generasi (start-frame); maks 7 karakter referensi per video.
- **Kling 3.0 Omni — voice binding:** elemen karakter bisa diikat ke satu suara ("the character always maintains the same face and voice across different works", panduan resmi Kling). Bila tersedia di akun, ikat elemen Momo ke suara rendah + Oyen ke suara tinggi sebagai cadangan — TAPI voiceover TTS tetap cara utama (Bagian 5).
- **Batasan gratis:** 66 kredit/hari (akun Lawak Lucu, habis 17 Des 2026); free = watermark + tanpa hak komersial. **Jangan tayangkan video jasa hasil free tier sebelum Cipta memutuskan soal watermark/hak komersial.**

### 9b. Google Flow / Veo 3.1 — Ingredients to Video (flow.google.com)
- **Syarat:** maks 3 gambar referensi (karakter, objek, style) per generasi. Konsistensi identitas antar scene (update Jan 2026): "Keep your characters looking the same even as the setting changes."
- **Langkah:**
  1. Buka flow.google.com → login akun Google (rotasi Flow) → buat proyek baru / buka proyek berjalan.
  2. Pilih model **Veo 3.1** → mode **Text-to-Video** → cari **Ingredients to Video** (tombol tambah gambar referensi / "Ingredients").
  3. Upload 3 gambar: `ref-oyen-1.png` (Oyen), `ref-momo-1.png` (Momo), + 1 gambar set (pakai ref-oyen-2 untuk studio / frame kolam untuk set B). Beri label tiap ingredient bila diminta (mis. "Oyen the orange cat", "Momo the grey cat").
  4. Tempel prompt dari Bagian 4 — sebut nama karakter sesuai label ingredient, JANGAN deskripsikan ulang wajahnya.
  5. Generate 10 detik, 360p, 9:16. Ulangi dengan SET YANG SAMA untuk tiap klip berikutnya.
- **Batasan:** konsistensi menurun di sekuens sangat panjang; gerakan kamera ekstrem bisa merusaknya — kamera dibuat statis (blok 4b). Biaya: Fast ±20 kredit / Quality 100 kredit per klip (cek saldo live dulu).
- **Catatan:** Flow MENOLAK video upload sebagai referensi lanjutan — hanya gambar yang bisa jadi ingredient.

### 9c. Cadangan (bila Kling/Veo gagal 2x)
- **Dreamina OmniHuman 1.5** (dreamina.capcut.com): foto + audio → lip-sync, mendukung hewan + multi-karakter, kredit harian gratis. Cara: upload 1 frame terbaik klip CACAT + voiceover .wav yang sama → generate → QC gerbang mulut. Periksa watermark + ketentuan komersial free tier sebelum tayang.
- **Runway Gen-4 References** (runwayml.com): maks 3 referensi, panggil dengan tag @, gambar ≥1024px (ref kita 720×1280 memenuhi). **Act-Two / Soul ID untuk kucing belum terverifikasi — jangan andalkan.**

---

## 10. VALIDASI BIBLE INI

- [x] Semua 6 gambar referensi berasal dari klip berverdict LOLOS di sweep QC 23 Nov 2026 (sumber klip + detik tercatat di Bagian 2).
- [x] Setiap gambar diperiksa visual langsung 23 Nov 2026 — mulut karakter yang bicara terbuka jelas; kucing satunya mulut tertutup.
- [x] Dialog Bagian 6 disalin verbatim dari `promo-produk-20-30detik.md` (18 Nov 2026) — dicek kata per kata.
- [x] Deskripsi set A/B dicocokkan dengan spec regenerasi `REGENERASI-promo-jasa-klip2-kolam-klipB.md` (23 Nov 12:30); set C dicocokkan dengan frame edukasi.
- [x] Aturan suara (MAI_01/MAI_03, pitch, mux) dicocokkan dengan MEMORY + skill video-qc.
- [x] Panduan Elements/Ingredients dicocokkan dengan laporan riset `~/workspace/research_notes/konsistensi-video-ai-2026-11-23/report.md` Bagian 2 + 4.
- [ ] **Belum terverifikasi (uji lapangan):** apakah Elements/Ingredients bekerja sama baik pada kucing seperti pada manusia; apakah Dreamina/Kling Avatar cukup baik untuk video jualan. Uji pertama: regenerasi promo-jasa klip2 + promo-kolam klipB dengan bible ini.

---

## Changelog
- **v1.0 — 23 Nov 2026:** Bible dibuat (perintah Cipta "Eksekusi yang gratis"). 6 ref dari klip LOLOS; 3 set; blok verbatim; panduan Kling Elements + Veo Ingredients; larangan Frames-to-Video. Siap dipakai untuk regenerasi promo-jasa/kolam + edukasi klip 3/5/6.
