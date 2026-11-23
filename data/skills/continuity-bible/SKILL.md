# Skill: Continuity Bible — Penjaga Konsistensi Karakter (untuk A11 AI Video Producer + A44 Persiapan Video, diverifikasi A04 Quality Control)

> Perintah Cipta 23 Nov 2026 — Masalah: suara berubah antar klip, karakter dan warna melenceng, mulut kucing beku saat bicara. Riset dunia 23 Nov 2026 membuktikan: model video TIDAK ingat klip sebelumnya — konsistensi hanya dijaga dengan gambar referensi yang SAMA + blok teks verbatim di tiap generasi. Bible ini adalah satu-satunya sumber kebenaran untuk Oyen & Momo. File lengkap: `CONTINUITY-BIBLE.md` di folder skill ini (v1.0, 202 baris); gambar referensi di `ref/`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A11 AI Video Producer** | Generate klip dari prompt bible ini; WAJIB pakai referensi + blok verbatim; WAJIB lewati gerbang QC video sebelum lapor "siap" |
| Pengerjaan | **A44 Persiapan Video** | Merakit prompt tiap klip dari bible ini (identitas + set + gerakan rahang + format + dialog verbatim) + melampirkan gambar referensi |
| Pengawasan | **A04 Quality Control** | Menegakkan gerbang QC video (skill video-qc); satu gerbang gagal = GAGAL; memeriksa referensi yang dipakai adalah set yang benar |

## Aturan keras

1. **TIDAK ADA generasi tanpa referensi dari folder ini.** Model tidak ingat klip sebelumnya — semua yang harus tetap sama dibawa ulang tiap generasi sebagai gambar + blok teks verbatim.
2. **Blok VERBATIM ditempel apa adanya** — tidak boleh diubah kata-katanya antar generasi.
3. **Satu set referensi sama di semua klip.** Jangan buat referensi baru per episode. Ganti referensi hanya bila ada frame LOLOS yang jelas lebih baik, dan catat di Changelog bible.
4. **Jangan deskripsikan wajah dengan kata-kata bila foto referensi sudah dilampirkan** — kata yang bertentangan dengan foto = drift karakter.
5. **Video digenerate BISU, voiceover ditempel belakangan.** JANGAN pakai suara native model untuk dialog karakter berulang — suara pasti berubah antar klip (temuan riset #1). Oyen = MAI_01 (tinggi, speed 110, pitch >200 Hz); Momo = MAI_03 (rendah, speed 100, pitch <200 Hz). Suara terkunci — jangan ganti.
6. **Frames-to-Video + frame awal statis DILARANG untuk klip bicara** — membekukan mulut secara struktural (akar cacat A1). Klip bicara = Text-to-Video + referensi gambar terkunci.
7. **Maks 2x percobaan per klip** — bila masih gagal, ganti pendekatan (Kling Elements → Dreamina OmniHuman / Kling Avatar sebagai penyelamat lip-sync), jangan bakar kredit.
8. **Jangan pakai klip CACAT sebagai referensi.** Daftar tolak ada di bible Bagian 2 (edukasi klip 3 — Cipta menemukan detik 28 mulut diam; detektif klip 2 t=5; detektif klip 3 — kostum; semua klip Momo promo).
9. **Pembuat TIDAK BOLEH meloloskan karyanya sendiri** — pemeriksa kedua wajib (aturan QC 23 Nov 12:21).

## Gambar referensi (folder `ref/` — semua 720×1280, dari klip LOLOS sweep QC 23 Nov)

| File | Sumber klip | Detik | Isi |
|---|---|---|---|
| `ref-oyen-1.png` | promo-pod klip3-oyen-cta (LOLOS) | t=2 | Oyen mulut terbuka LEBAR, dua-shot studio, stand kaos di tengah meja |
| `ref-oyen-2.png` | promo-jasa klip3-oyen-dm (LOLOS) | t=5 | Oyen mulut terbuka lebar, close-up studio, papan kayu "KikiWorks" |
| `ref-oyen-3.png` | edukasi-ep1-klip-01 (LOLOS) | t=2 | Oyen solo di depan laptop, kalung hitam + lonceng (varian edukasi) |
| `ref-momo-1.png` | edukasi-ep1-klip-02 (LOLOS) | t=6 | Momo mulut terbuka JELAS (gigi terlihat), Oyen diam mulut tertutup |
| `ref-momo-2.png` | edukasi-ep1-klip-04-FIXED (LOLOS) | t=2 | Momo mulut terbuka, dua-shot meja + laptop game ikan |
| `ref-momo-3.png` | edukasi-ep1-klip-04-FIXED (LOLOS) | t=5 | Momo mulut terbuka (ujung gigi terlihat), profil bicara |

**Kalung Oyen — inkonsistensi tercatat:** Oyen memakai kalung hitam + lonceng HANYA di set Meja Edukasi; TIDAK memakai kalung di set Studio Podcast. Kanon: **tanpa kalung = tampilan baku studio** (pakai ref-oyen-1/2); kalung = varian edukasi saja (ref-oyen-3). Momo tidak pernah memakai kalung.
**Yang tidak boleh berubah:** warna bulu (Oyen oren, Momo abu-abu solid), warna mata (Oyen amber, Momo hijau), posisi (Oyen SELALU kiri, Momo SELALU kanan), spesies (kucing realistis — bukan kartun, bukan boneka).
**Catatan validasi Momo:** tidak ada klip LOLOS yang mulut Momonya terbuka LEBAR seperti Oyen — ref-momo-1 adalah bukaan paling jelas yang ada. Bila regenerasi Momo menghasilkan bukaan lebih lebar + lolos QC, ganti ref-momo-1 dengan frame baru itu dan catat di Changelog.

## Identitas karakter — VERBATIM (tempel di setiap prompt)

### OYEN — VERBATIM
> Oyen is a realistic orange tabby cat with bright orange fur and darker orange stripes, cream-white chest and muzzle, large round amber eyes, a pink nose, long white whiskers, upright pointed ears, and an expressive cheerful face. He sits on the left.

### MOMO — VERBATIM
> Momo is a realistic solid slate-grey cat with dense grey fur, a round face, large round green eyes, a small pink-grey nose, white whiskers, upright ears, and a calm sceptical expression. She sits on the right.

## Set sheet (tiga set — pilih sesuai video)

### SET A — Studio Podcast Rumahan (promo-pod, promo-jasa, episode podcast)
> A cozy home podcast studio, warm lighting, wooden desk. Oyen sits on the left and Momo on the right, each behind a black studio microphone on a boom arm. A wooden "KikiWorks" nameplate stands in the center of the desk. Behind them: a bookshelf with books, green plants, and warm string lights. An audio mixer sits on the right side of the desk, a mug and cables on the left.

### SET B — Tepi Kolam Koi (promo-kolam)
> An outdoor koi pond garden in soft daylight, mossy rocks, lily pads, orange koi fish swimming in the pond. Oyen sits on the left and Momo on the right on a flat rock at the pond's edge, one black podcast microphone on a stand between them.

### SET C — Meja Edukasi / Meja Kerja (Edukasi Ep 1, Detektif)
> A wooden work desk in a warm home office, a laptop showing a colorful fish game on screen, a bookshelf with books and green plants behind, warm lamps, a mug and a notebook on the desk. Oyen sits on the left and Momo on the right behind the desk.

## Blok prompt verbatim (tempel di setiap generasi klip bicara)

### Blok gerakan rahang — VERBATIM (wajib)
> The speaking cat's mouth MUST move visibly while speaking — its jaw opens and closes clearly in sync with every word, wide open when talking, never still while dialogue plays. Only the speaking cat's mouth moves; the other cat stays still with mouth closed. Natural small head movement, smooth shot.

### Blok format — VERBATIM
> Realistic video, portrait 9:16, 10 seconds, 360p. Two realistic cats sitting side by side, Oyen on the left, Momo on the right. Camera static, no zoom, no pan.

### Cara merakit prompt klip bicara
1. Blok identitas karakter yang bicara (di atas) + sebutkan kucing satunya "sitting still beside her/him with mouth closed".
2. Blok set (A/B/C sesuai video).
3. Blok gerakan rahang + blok format.
4. Dialog verbatim, format: `Dialogue (English, low voice): "..."` untuk Momo, `Dialogue (English, high voice): "..."` untuk Oyen. Dialog Indonesia: `Dialogue (Indonesian, low/high voice): "..."`.
5. Lampirkan gambar referensi: ref karakter yang bicara + 1 ref dua-shot set yang sama (maks 3 gambar untuk Veo Ingredients; 2–4 gambar per elemen untuk Kling Elements).

### Contoh jadi — Promo-Jasa klip 2 (Momo)
> Realistic grey cat Momo speaking directly to camera in a cozy home podcast studio, sitting at a wooden desk behind a black studio microphone, orange cat Oyen sitting still beside her on the left with mouth closed, wooden "KikiWorks" nameplate on the desk, bookshelf with plants and warm string lights behind. Momo's mouth MUST move visibly while speaking — her jaw opens and closes clearly in sync with every word, wide open when talking, never still while dialogue plays. Only Momo's mouth moves; Oyen stays still with mouth closed. Natural small head movement, smooth shot. Dialogue (English, low voice): "Fifteen seconds, seventy-five thousand rupiah. Thirty seconds, one-fifty. Sixty seconds, two-fifty."

## Aturan suara (dikunci di luar model)

- Mux voiceover ke video (saat perakitan, bukan saat generate): `ffmpeg -i video-bisu.mp4 -i voiceover.wav -c:v copy -map 0:v -map 1:a -shortest hasil.mp4`
- Cek pitch tiap klip dengan `qc-pitch.py`: Oyen >200 Hz, Momo <200 Hz. Drift >30 Hz = perbaiki dengan pitch-shift (terbukti di Edukasi klip 4: 247,0 → 162,5 Hz) — JANGAN generate ulang video hanya karena suara salah.
- Dialog 17–25 kata per klip 10 detik, selesai sebelum detik 10. Judul kuning tebal outline hitam di detik pertama (2 baris, strip gelap di belakang).

## Naskah resmi — VERBATIM (dari promo-produk-20-30detik.md, 18 Nov 2026)

### Promo 1 — eBook Kolam
- Klip 1 — Oyen: "Momo! I wrote a book! About me guarding a fish pond! It's hilarious!"
- Klip 2 — Momo: "You chased the fish for sixty pages, Oyen. That's not guarding, that's a buffet."
- Klip 3 — Oyen: "Read it yourself! Link in bio! Only twenty-nine thousand rupiah, fish not included!"

### Promo 2 — POD kaos Zazzle
- Klip 1 — Oyen: "Momo, look! I'm on a T-shirt now! Orange, handsome, and very famous!"
- Klip 2 — Momo: "Famous? You photobombed a T-shirt. The grey cat is the real model here."
- Klip 3 — Oyen: "Get yours! Cute cat shirts, link in bio! Wear Oyen everywhere you go!"

### Promo 3 — Jasa Video Promo KikiWorks
- Klip 1 — Oyen: "Attention pet shops! Want a video like this for your store? We make it!"
- Klip 2 — Momo: "Fifteen seconds, seventy-five thousand rupiah. Thirty seconds, one-fifty. Sixty seconds, two-fifty."
- Klip 3 — Oyen: "DM us now! Your products, our cats, your sales go up! Meow!"

Catatan: harga di naskah ini adalah harga 18 Nov 2026 (Rp). Harga toko saat ini sudah USD (jasa video promo $19/$39/$69). Untuk voiceover yang SUDAH direkam, pakai naskah di atas apa adanya; untuk naskah BARU, konfirmasi harga terbaru dulu ke toko — jangan mengarang harga.

## Pendaftaran referensi — Kling Elements + Veo Ingredients

Pendaftaran lewat dashboard di perangkat/browser yang sudah login — JANGAN coba login sendiri dari subagent. Panduan lengkap di bible Bagian 9; ringkasnya:

### Kling AI — Element Library (kling.ai)
1. Login (akun Lawak Lucu, lawaklucu182@gmail.com) → menu **Element Library**.
2. **Create Element → Character** `Oyen` → upload `ref-oyen-1/2/3.png` → simpan.
3. **Create Element → Character** `Momo` → upload `ref-momo-1/2/3.png` → simpan.
4. (Opsional) **Create Element → Scene** `Studio Podcast` / `Kolam Koi`.
5. Saat generate: centang elemen `Oyen` + `Momo` (+ scene). Maks 3 elemen terikat per generasi.
- Kling 3.0 Omni bisa mengikat suara ke elemen karakter (cadangan saja — voiceover TTS tetap utama).
- Batasan gratis: 66 kredit/hari (habis 17 Des 2026); free = watermark + tanpa hak komersial — jangan tayangkan video jasa hasil free tier sebelum Cipta memutuskan soal watermark.

### Google Flow / Veo 3.1 — Ingredients to Video (flow.google.com)
1. Login akun Google (rotasi Flow) → model **Veo 3.1** → **Text-to-Video** → **Ingredients to Video**.
2. Upload maks 3 gambar: `ref-oyen-1.png` + `ref-momo-1.png` + 1 gambar set. Beri label ("Oyen the orange cat", "Momo the grey cat").
3. Tempel prompt dari skill ini — sebut nama karakter sesuai label, JANGAN deskripsikan ulang wajahnya.
4. Generate 10 detik, 360p, 9:16. Ulangi dengan SET YANG SAMA untuk tiap klip berikutnya.
- Flow MENOLAK video upload sebagai referensi lanjutan — hanya gambar yang bisa jadi ingredient. Kamera statis (gerakan ekstrem merusak konsistensi).

### Cadangan (bila Kling/Veo gagal 2x)
- **Dreamina OmniHuman 1.5** (dreamina.capcut.com): foto + audio → lip-sync, mendukung hewan + multi-karakter, kredit harian gratis. Upload 1 frame terbaik klip CACAT + voiceover .wav yang sama → generate → QC gerbang mulut. Periksa watermark + ketentuan komersial free tier sebelum tayang.
- **Runway Gen-4 References** (runwayml.com): maks 3 referensi, tag @, gambar ≥1024px (ref kita 720×1280 memenuhi).
- **Act-Two / Soul ID untuk kucing BELUM TERVERIFIKASI — jangan andalkan.**

## Alur kerja generasi (cara Flow yang sudah terbukti di tangan Cipta)

Cipta BERHASIL membuat video 60 detik dan 300 detik dengan Flow — alur ini dibangun DI ATAS caranya, bukan menggantinya.

1. Siapkan prompt dari skill ini (identitas + set + rahang + format + dialog verbatim) + lampirkan ref.
2. Generate klip 10 detik di Flow (Text-to-Video, 360p, 9:16) — akun rotasi, cek saldo live dulu; bila kredit habis, berhenti dan lapor (jangan pakai berbayar tanpa izin).
3. QC per klip SEBELUM dirakit — 5 gerbang skill video-qc: (1) mulut yang bicara bergerak (frame t=2,5,8); (2) suara konsisten per karakter (pitch); (3) hanya satu mulut bergerak; (4) dialog selesai sebelum detik 10; (5) judul di detik pertama. Satu gerbang gagal = CACAT. Verdict TERTULIS di `~/workspace/catatan/keputusan.md` SEBELUM publish.
4. Klip Momo dicek PERTAMA di setiap video baru (klip Momo paling sering gagal — penyebab pasti belum diketahui).
5. Mux voiceover .wav ke klip yang lolos.
6. Rakit 60 detik (6 klip) / 300 detik (30 klip) seperti yang sudah berhasil Cipta lakukan — via Scenebuilder Flow atau concat ffmpeg, lalu QC final rakitan + verdict tertulis.

## Bukti + lapor

- Setiap klip: file klip + prompt yang dipakai (tempel verbatim) + ref yang dilampirkan + hasil QC + satu baris `data/log-eksekusi.jsonl`.
- Verdict QC ditulis ke `~/workspace/catatan/keputusan.md` setiap kali (format di skill video-qc), BUKAN hanya di log harian.
- Bila referensi diganti: catat di Changelog `CONTINUITY-BIBLE.md` (tanggal, file lama → baru, alasan) DAN perbarui salinan di folder skill ini — kedua salinan harus sama.
