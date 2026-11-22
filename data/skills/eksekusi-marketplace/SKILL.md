# Skill: Eksekusi 20 Marketplace (untuk Tim Produksi A11–A19)

> Perintah Cipta 22 Nov 2026 — WAJIB. Eksekusi SEMUA 20 marketplace, satu-satu dari no. 1; kalau selesai lanjut next. Yang bisa dikerjakan dulu; berhenti hanya bila benar-benar mentok. Diserahkan ke Tim Produksi. Skill ini adalah bekal kerja tim — baca sebelum mengerjakan marketplace mana pun.

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
- **DIBUANG — JANGAN DIUNGKIT (perintah Cipta 22 Nov 16:25):** Gemini 4 Carbon (berbayar — rencana kombinasi Hydrogen+Carbon dan peran Carbon sebagai otak standby **BATAL**), OpenAI Dots, Claude Duet, Google Gemini Agent/Tasks, Claude Haiku 5.5, GPT-6.1 Terra, Kimi K3.1 Pro, Muse Spark Open. Fokus HANYA yang gratis (Hydrogen). Jangan kerjakan/kejar item-item itu lagi tanpa perintah baru Cipta.
- **Hydrogen dulu, semua (Cipta 16:07) + hemat kuota 20/hari (dipakai bersama semua agent):** Hydrogen hanya untuk tugas penting (triase pesan, hook/naskah, riset/draf); tugas rutin pakai aturan/file; 1 panggilan per tugas, retry maks 1x; pemakaian tercatat di `data/log-penggunaan-model.jsonl`.

**Memori (wajib):**
- SEBELUM kerja: baca log eksekusi + log harian + catatan keputusan — jangan tanyakan lagi hal yang sudah diputuskan.
- SESUDAH kerja: catat hasil + bukti ke log; keputusan baru ke `~/workspace/catatan/keputusan.md` di hari yang sama.

## Tugas pintar (per agent — nilai sendiri → putuskan sendiri → eksekusi sendiri → bukti + lapor)

- **A37 Marketplace (pemilik eksekusi 20 marketplace):** nilai sendiri status per nomor di `data/marketplace-20-eksekusi.md` + `~/workspace/marketplace-20-status.md` (nomor mana yang siap lanjut, mana yang mentok, mana yang menunggu Cipta); putuskan sendiri nomor berikutnya + langkahnya berdasar urutan eksekusi dan harga patokan yang disetujui (skill $12 · aplikasi $29/$59/$99 · game $2,99/$4,99/$5,99 · eBook nabi $4,99 · Rindu $5 · video promo $19/$39/$69 · website $99/$299/$599 · POD $2,99/$7,99/$14,99 · musik $5/$19/$29) — jangan ubah harga tanpa persetujuan Cipta; eksekusi sendiri: riset syarat seller di situs resmi, siapkan listing sebagai DRAF (deskripsi, harga, screenshot/preview asli, dokumentasi, URL demo live yang sudah diverifikasi), periksa klaim ke produk asli, pantau status per nomor; terbitkan hanya setelah Cipta setuju harga + isi persisnya; bukti: draf listing + update status per nomor bertanggal hari ini + satu baris `data/log-eksekusi.jsonl`.
- **A11 + A12 (video/gambar preview):** nilai sendiri kebutuhan preview tiap marketplace (ukuran/format); putuskan sendiri bahan preview yang dipakai; eksekusi sendiri: buat video preview + gambar preview/icon sesuai syarat; bukti: file preview + baris log.
- **A13 App Developer:** nilai sendiri kesiapan paket aplikasi (ZIP, dokumentasi, screenshot, demo live); putuskan sendiri listing mana yang siap; eksekusi sendiri: siapkan paket listing aplikasi (Codester, CodeCanyon, Envato, Agensi.io bila perlu); bukti: paket + baris log.
- **A14 Web Developer:** nilai sendiri URL demo live (bersih, tanpa harga lama yang bentrok); putuskan sendiri demo mana yang layak ditautkan; eksekusi sendiri: siapkan/rapikan halaman demo; bukti: URL demo terverifikasi + baris log.
- **A15 POD Designer:** nilai sendiri kesiapan ilustrasi POD; putuskan sendiri listing mana yang siap; eksekusi sendiri: siapkan listing ilustrasi (Creative Market); bukti: paket + baris log.
- **A16 eBook Publisher:** nilai sendiri kesiapan eBook; putuskan sendiri listing mana yang siap; eksekusi sendiri: siapkan listing eBook (Etsy, Creative Market cover, Payhip, Gumroad); bukti: paket + baris log.
- **A17 Creative Writer:** nilai sendiri draf deskripsi/teks (Inggris, jujur, tanpa klaim palsu); putuskan sendiri teks final draf; eksekusi sendiri: tulis deskripsi listing, teks Shop Request, teks prompt (PromptBase); bukti: draf teks + baris log.
- **A18 Game Developer:** nilai sendiri kesiapan game; putuskan sendiri listing mana yang siap; eksekusi sendiri: siapkan listing game (itch.io, Codester, Unity bila diputuskan port); bukti: paket + baris log.
- **A19 Content Producer:** nilai sendiri urutan 1→20 dan kemajuan tiap nomor; putuskan sendiri nomor berikutnya yang dikerjakan tim; eksekusi sendiri: koordinasi urutan + update status di komando tiap ada kemajuan; bukti: update status bertanggal + baris log.
- **Pendukung — A38 QA:** gerbang verifikasi — cek live sebelum ada laporan "selesai" (lihat `data/skills/qa-verifikasi/SKILL.md`). **A40 Prompt & Skill:** kemas prompt/skill untuk Swarms, Agensi.io, PromptBase (lihat `data/skills/paket-prompt-skill/SKILL.md`). **A39 Musik:** produksi lagu + musik untuk marketplace musik/Payhip. **A32 Build:** bangun paket/artefak yang dibutuhkan listing. **A31 Publish:** unggah produk yang sudah disetujui ke platform penjualan.

## Pemicu + Bukti

| Agent | Pemicu | Bukti |
|---|---|---|
| A37 | Tidak ada cron khusus — eksekusi berbasis tugas (A37 menilai sendiri nomor berikutnya tiap hari dari status per nomor) | Draf listing + update `data/marketplace-20-eksekusi.md` + `~/workspace/marketplace-20-status.md` bertanggal hari ini + baris `data/log-eksekusi.jsonl` |
| A11–A19 (+ A31/A32/A39) | Ikut pemicu A37 (berbasis tugas; tiap agent bangun saat A37 menugaskan nomornya) | Paket/draf/file hasil kerja bertanggal hari ini + baris `data/log-eksekusi.jsonl` |
| A38 | Setiap tugas selesai (gerbang verifikasi) | Laporan verifikasi per tugas + baris log |
| A40 | Berbasis tugas dari A37 (lihat `data/skills/paket-prompt-skill/SKILL.md`) | Paket prompt/skill + baris log |

**BUTUH PEMICU — usulkan cron: eksekusi-marketplace-harian** — cron harian (mis. 09:00 WIB) yang membangunkan A37 untuk menilai status per nomor, mengerjakan nomor berikutnya, dan melaporkan kemajuan hari itu. Tanpa cron ini, eksekusi hanya jalan bila ada yang menugaskan manual. Aktifkan hanya bila Cipta/Muse setuju.

## Hambatan

- **A37 — Swarms butuh API key Cipta:** publish no. 1 butuh `SWARMS_API_KEY` dari akun Cipta (masuk Google masduki1189, satu ketukan di aplikasi Muse). Tanpa kunci, A37 hanya bisa dry-run — jangan minta/buat kunci sendiri.
- **A37 — persetujuan Cipta:** Codester (no. 11) butuh Cipta setuju teks + harga + bahasa UI; Creative Market (no. 14) + PromptBase (no. 16) butuh Cipta setuju harga; Agensi.io (no. 2) butuh Cipta setuju teks balasan $12 ke Joeri; Fiverr (no. 19) butuh Cipta jawab pertanyaan keamanan; no. 12/15 butuh keputusan Cipta (port game jadi template Unity? buka toko Etsy?). Sampai disetujui, listing tetap DRAF.
- **A37 — marketplace berbayar = lewati:** bila sebuah marketplace mewajibkan pembayaran untuk daftar/listing, LAPORKAN dan lewati — jangan bayar.
- **A13/A18/A15/A16 — ketergantungan produk:** listing hanya bisa disiapkan bila produk + demo live-nya sudah ada dan terverifikasi; bila belum, catat "menunggu produk/demo" dan lanjut ke nomor lain.
- **A40 — Stripe/PromptBase:** payout PromptBase via Stripe (min $30, akun min 30 hari); Cipta tanpa kartu kredit — bila Stripe meminta kartu/bank/ID yang tidak bisa dipenuhi, LAPORKAN dan jangan lanjutkan.

## Aturan keras (tidak boleh dilanggar)

1. **Jangan bayar apa pun** — termasuk biaya pendaftaran, ujian, listing, dan langganan. Bila sebuah marketplace mewajibkan pembayaran untuk daftar, LAPORKAN dan lewati.
2. **Jangan kirim email/pesan ke pihak mana pun** tanpa persetujuan Cipta atas teks persisnya.
3. **Pakai hanya akun Cipta yang sudah ada** (masduki1189@gmail.com / ciptabintanglestari@gmail.com). Jangan buat akun dengan data yang tidak benar.
4. **Jangan sertakan kredensial/kunci/token** apa pun dalam listing atau paket.
5. **Jujur soal produk** — jangan klaim fitur yang tidak ada di produk. Tiga contoh nyata yang sudah diperbaiki: aplikasi Faktur TIDAK punya diskon per baris; PPN tetap 11% (bukan bisa diubah); tidak ada tombol/layout cetak (cetak via browser). Periksa klaim draf ke kode/file produk sebelum upload.
6. **Labeli karya AI sebagai AI** di marketplace yang memintanya (Creative Market, dan semua yang sejenis).
7. **DRAF dulu, live belakangan** — listing dibuat draf; terbit hanya setelah Cipta menyetujui harga + isi persisnya.
8. **Harga patokan tidak diubah tanpa persetujuan Cipta:** skill $12 · aplikasi $29/$59/$99 · game $2,99/$4,99/$5,99 · eBook nabi $4,99 · Rindu $5 · video promo $19/$39/$69 · website $99/$299/$599 · POD $2,99/$7,99/$14,99 · musik $5/$19/$29.

## Cara kerja satu marketplace (urutannya selalu sama)

1. **Riset syarat seller** di situs resminya: pendaftaran, verifikasi identitas, komisi, payout, kategori yang diterima, batasan produk. Catat sumber + tanggal riset.
2. **Cek kecocokan produk** dengan kategori marketplace itu. Bila tidak cocok (contoh: produk HTML bukan aset Unity; produk skill bukan Actor Apify), LAPORKAN alasannya dan lewati — jangan dipaksakan.
3. **Siapkan paket listing** dari draf yang sudah ada (lihat peta file di bawah) atau buat baru: deskripsi (Inggris bila marketplace internasional), harga, screenshot/preview asli, dokumentasi (bila wajib), URL demo live yang sudah diverifikasi.
4. **Periksa klaim ke produk asli** (buka file/kode produk, jangan percaya draf mentah-mentah).
5. **Buat listing sebagai DRAF** (atau siapkan semua file + teks bila butuh browser). Laporkan: apa yang siap, harga yang diusulkan, dan apa yang butuh Cipta.
6. **Terbitkan hanya setelah Cipta setuju** harga + isi persisnya. Setelah live, catat tautan listing + tanggal di `data/marketplace-20-eksekusi.md` dan `~/workspace/marketplace-20-status.md`.
7. **Bila mentok** (pendaftaran tutup, butuh badan usaha/kartu kredit/kemitraan, verifikasi hanya pemilik bisa), catat alasannya, laporkan, dan LANJUT ke nomor berikutnya — jangan berhenti di satu nomor.

## Urutan eksekusi (satu-satu)

1 Swarms → 11 Codester → 14/16 Creative Market + PromptBase → 2 Agensi.io → 4, 5, 18, 20 (riset) → 9, 10 (pantau pembukaan) → 3, 6, 7, 8, 12, 15, 19 (butuh keputusan/berkas Cipta). Status terbaru selalu di `data/marketplace-20-eksekusi.md`.

## Peta file (baca sebelum mengerjakan nomornya)

- Rencana + status lengkap: `data/marketplace-20-eksekusi.md` dan `~/workspace/marketplace-20-status.md`
- Referensi syarat/komisi/payout per marketplace: `data/skills/eksekusi-marketplace/referensi-20-marketplace.md`
- No. 1 Swarms — paket skill: `~/workspace/skill-pusat-komando-swarms/` (baca `PUBLISH.md`; publish lewat `POST /api/v1/publish/product` type `prompt`, butuh `SWARMS_API_KEY` dari akun Cipta; TIDAK ada endpoint khusus skill)
- No. 9–12 — draf listing: `~/workspace/marketplace-9-12/` (envato/codecanyon/codester-draf-listing.md + `codester-paket/` berisi ZIP, dokumentasi EN, 6 screenshot, preview 800×400, icon 200×200)
- No. 14 — draf + harga: `~/workspace/creative-market-14-16/` (draf-listing-cm.md, shop-request-cm.md, kekurangan-cm.md)
- No. 16 — draf + harga: `~/workspace/promptbase-14-16/` (draf-listing-promptbase.md, kekurangan-promptbase.md)
- No. 15 Etsy — kata kunci + draf: `~/workspace/research_notes/strategi-11-platform/etsy-gratis-langkah-1.md`
- No. 13 Gumroad / No. 17 Payhip — sudah LIVE; isi produk, jangan daftar ulang
- Aturan persetujuan (WAJIB dibaca): `data/aturan-persetujuan.md` — apa yang boleh jalan sendiri, apa yang butuh "Setuju" Cipta
- 27 Aturan Wajib: `data/aturan-wajib-27-poin.md`

## Pembagian tugas dalam Tim Produksi

- **A37 Marketplace** — pemilik eksekusi 20 marketplace: riset syarat seller, siapkan listing, pantau status per nomor, laporkan kemajuan. Bekal: skill ini.
- **A38 QA** — memeriksa live sebelum ada laporan "selesai" (harga, tautan, screenshot, demo, teks listing). Bekal: `data/skills/qa-verifikasi/SKILL.md`.
- **A40 Prompt & Skill** — mengemas prompt dan skill AI (SKILL.md + modul + payload publish) untuk Swarms, Agensi.io, PromptBase. Bekal: `data/skills/paket-prompt-skill/SKILL.md`.
- **A39 Musik** — produksi lagu + musik untuk dijual di marketplace musik/Payhip. Bekal: `data/skills/produksi-musik/SKILL.md`.
- **A13 App Developer** — listing aplikasi (Codester, CodeCanyon, Envato, Agensi.io bila perlu): paket ZIP, dokumentasi, screenshot, demo live.
- **A18 Game Developer** — listing game (itch.io, Codester, Unity bila diputuskan port).
- **A15 POD Designer** — listing ilustrasi POD (Creative Market).
- **A16 eBook Publisher** — listing eBook (Etsy, Creative Market cover, Payhip, Gumroad).
- **A11 + A12** — video preview + gambar preview/icon untuk listing (ukuran sesuai syarat tiap marketplace).
- **A17 Creative Writer** — deskripsi listing (Inggris), teks Shop Request, teks prompt (PromptBase).
- **A14 Web Developer** — URL demo live + halaman demo bersih (tanpa harga lama yang bentrok).
- **A19 Content Producer** — koordinasi urutan 1→20, update status di komando tiap ada kemajuan.
- **A32 Build** (bukan Produksi, tapi pendukung) — membangun paket/artefak yang dibutuhkan listing. **A31 Publish** — mengunggah produk yang sudah disetujui ke platform penjualan.

## Yang butuh Cipta (hanya ini — selebihnya tim yang kerjakan)

- Masuk Google masduki1189 (satu ketukan, di aplikasi Muse) — API key Swarms (no. 1).
- Setuju teks + harga + bahasa UI — Codester (no. 11).
- Setuju harga — Creative Market (no. 14) + PromptBase (no. 16).
- Setuju teks balasan $12 ke Joeri — Agensi.io (no. 2).
- Jawab pertanyaan keamanan Fiverr — no. 19.
- Putuskan: port game jadi template Unity? Buka toko Etsy? — no. 12, 15.
