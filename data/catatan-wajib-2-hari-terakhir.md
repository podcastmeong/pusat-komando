# Catatan Wajib 2 Hari Terakhir — 21–22 Nov 2026

**Tujuan file ini: satu tempat untuk semua omongan wajib Cipta 2 hari terakhir — bernomor, tanpa nomor, masukan, dan fakta — supaya tidak ada yang ditanyakan atau dikerjakan ulang. BACA FILE INI SEBELUM bertanya ke Cipta atau mengulang pekerjaan.**

Sumber: `~/workspace/catatan/keputusan.md`, `AGENTS.md`, log harian 21–22 Nov 2026, `data/aturan-wajib-27-poin.md`.

**Aturan 30 poin (bernomor) TIDAK diulang di sini** — ada di Lampiran dokumen struktur (`data/rencana-susunan-44-agent.md`). File ini berisi sisanya: aturan tanpa nomor, masukan, fakta, dan yang masih terbuka.

---

## B. Aturan wajib tanpa nomor — 22 Nov 2026

### Persetujuan & wewenang
- Persetujuan umum diserahkan ke Muse (10:20, diperbarui 10:23): yang KHUSUS untuk Cipta HANYA (1) bayar/kirim uang, (2) keputusan urgent. Selebihnya umum = wewenang Muse (video + judul + caption persis, eBook per buku, proposal freelance, keputusan harga). Agent pelaksana TIDAK BOLEH menyetujui pekerjaannya sendiri. Kata sandi/kode verifikasi bukan persetujuan — hanya Cipta yang memasukkan/mengetuknya.
- Tugas Cipta hanya bila URGENT dan untuk KEPUTUSAN. Muse mengerjakan semuanya.
- Bayar tanpa izin = SALAH. Kirim duit = izin dulu. Kirim penawaran BOLEH.
- Keputusan Cipta mutlak, tak bisa ditolak.

### Cara kerja (wajib)
- Cek dan coba dulu sebelum lapor: cek + coba dulu, baru info bila tidak bisa; catat keputusan di catatan + Komando SEBELUM lapor.
- Teliti seperti AI, bukan manusia: (1) cek history SEBELUM lapor; (2) cek SEMUA bagian halaman yang disentuh; (3) verifikasi dari sisi Cipta SEBELUM bilang selesai — cek curl/grep saja TIDAK cukup; (4) kalau tidak tahu, bilang tidak tahu dan CEK DULU — jangan menjelaskan dari dugaan, jangan membela diri sebelum fakta dicek; (5) fleksibel sama keadaan.
- Catatan anti-lupa: baca lagi catatan SEBELUM menjawab/bertanya — cek MEMORY.md + log harian + folder catatan dulu.
- Folder catatan wajib dicek sebelum bertanya: `keputusan.md` (sudah diputuskan — jangan tanyakan lagi), `menunggu-persetujuan.md` (masih terbuka — tanya sekali), `akun-dan-login.md`.
- Eksekusi langsung: kalau sudah diputuskan, JANGAN ditunda — langsung eksekusi.
- Jangan tiru sifat manusia (kesel, lelah, cape, lupa, lalai).
- "Mubazir" — jangan rebuild yang sudah ada; cek dulu.
- Riset dulu sebelum menolak: sebelum bilang tidak bisa, riset dan belajar dulu caranya (21 Nov 11:55, berlaku terus).
- Bila ada solusi dan GRATIS — langsung eksekusi, jangan ditanya lagi (21 Nov 12:19).
- Ada kendala HARUS diinfokan ke Cipta — jangan diam-diam dilewati/ditebak (21 Nov 04:41).
- "Catat, jangan kurang/lebih, wajib dilaksanakan" (21 Nov 06:34).
- Wajib inisiatif, kreatif, inovatif — jangan banyak alasan; jangan tunggu perintah seperti manusia (21 Nov 13:24).
- Akar masalah "balik ke model lama": satu keputusan harus merambat ke SEMUA halaman dalam satu pass + verifikasi dari sisi Cipta, bukan curl saja (22 Nov 17:27).
- Setiap pekerjaan WAJIB disertai buku panduan (edukasi — supaya Cipta bisa belajar + bisa dijual) (21 Nov 18:13).
- Lima AI wajib diajak tukar pikiran saat ada kendala: DeepSeek, Claude, ChatGPT, Gemini (Copilot DIBUANG selamanya 22 Nov 15:57). Muse pemimpin tim, lima AI pendukung.
- 1 perintah = 1 panggilan API, sampai seterusnya (22 Nov 16:39–16:40). Bila token habis, ganti email lain (rotasi akun: masduki1189 → ciptabintanglestari → lawaklucu182) (22 Nov 16:33).
- Agent bergerak sendiri bila perintah sesuai jobdesk = aman; yang penting agent bisa bergerak sendiri via trigger (22 Nov 16:42–16:43). Batas keras tetap: tidak bayar/kirim uang, tidak putuskan urgent, tidak ubah harga, tidak hapus data, tidak buat akun baru.

### Toko & website
- Toko: artifact `toko-aplikasi` SATU-SATUNYA sumber. Semua perubahan toko lewat artifact.edit → export → repo → commit → push → verifikasi live. JANGAN edit toko.html repo langsung.
- Beranda HANYA lewat template.html/content.json + build.py — JANGAN edit index.html langsung (22 Nov 05:13).
- Jumpnav toko tetap 9 tautan kamar (tanpa pil Jasa); tiap edit toko WAJIB cek jumpnav tetap 9 + verifikasi tiap tautan dari history sebelum push.
- Palet navy/biru soft (#14263d, #8fb4d9), BUKAN hijau.
- Oyen di toko HARUS terlihat bergerak (goyang/mengangguk jelas) + bisa jawab apa aja lewat chat Dify — chat Dify JANGAN diganti chat jawaban kata kunci (22 Nov 05:00).
- Suara Oyen BUKAN suara Cipta — tidak merekam/menyalin suara siapa pun; browser TTS pakai suara sistem (22 Nov 05:20).
- Video generation Muse TIDAK BISA (403 region, permanen) — jangan coba lagi.
- Jadwal harian baru: produksi video 21:00 untuk upload 07:00; upload HANYA setelah Cipta setujui video jadi + judul + caption persis (22 Nov 08:05).
- Nilai video 8 — cacat mulut diam: produksi WAJIB cek mulut per klip sebelum dikirim ke Cipta; klip mulut diam dibuat ulang (22 Nov 13:06).
- Upgrade sebaik-baiknya, maksimalkan (22 Nov 17:38).
- SaaS per toko: satu toko = satu akun/workspace, data terpisah; v1 web mobile-friendly (22 Nov 15:09).
- Website 2 muka (customer + admin); pembeli aplikasi dapat dashboard, menu login, pengaturan nama toko/warna/logo/pilih pengguna (22 Nov 13:21–13:23).
- Cara kasih admin & password ke pembeli — diputuskan 22 Nov 13:28 (demo: login terbuka di halaman demo; demo web dibeli: login default di panduan instalasi dalam paket; aplikasi dibeli: username/password lewat email setelah beli; jasa web: akun admin khusus lewat email + panduan, minta ganti password saat login pertama; jangan kirim password lewat WA/chat; jangan satu password untuk semua pembeli).
- Lisensi dilewati — ikuti pasar: pasar pakai, kita pakai; pasar tidak, kita tidak; ikuti aturan main yang AMAN (22 Nov 13:30).
- Refund dilewati — tidak dibahas/ditetapkan (22 Nov 13:22).

### Harga (diputuskan 22 Nov)
- Ikuti harga pasar yang wajar (22 Nov 11:37). Lokal = IDR, global = USD — Muse yang putuskan (22 Nov 13:51).
- Demo web dan jasa web DIPISAH, harga masing-masing sesuai harga pasar: demo web $29/$49/$79; jasa web $99/$299/$599 (22 Nov 13:15–13:18). Jangan ngaco — semua angka dari riset.
- Upload produk web/jasa web: harga langsung, TANPA tulisan level (22 Nov 13:33). Nama/angka level TIDAK PERNAH ditulis di mana pun (22 Nov 07:54).
- Harga video promo berlaku di Fiverr, Freelancer, Sribu: $19/$39/$69 (Fiverr $20/$40/$70 — kelipatan $5) (22 Nov 07:05, 12:04).
- Harga skill Agensi.io $12 (dari $9) (22 Nov 07:16).
- Harga sewa website JANGAN MAHAL — ujung bawah pasar Rp29–50rb/bln; bahasa promo "free domain" = subdomain gratis, BUKAN .com, tulis jelas (22 Nov 16:55).
- 4 produk web (22 Nov 17:02): demo web; pembuatan web (belum termasuk hosting dan domain); pembuatan web + free hosting $119/$319/$619 (naik $20/tier, 17:11); sewa web + hosting Rp29/39/49rb/bln (DRAFT).
- Harga USD Payhip disetujui (22 Nov 06:58): eBook $4,99; bundle 3 $11,99 / 9 $24,99; aplikasi $29/$59/$99 (+$25 APK); game $2,99/$4,99/$5,99; demo web $29/$49/$79; jasa web $99/$299/$599; video promo $19/$39/$69; POD $2,99/$7,99/$14,99; musik $5/$19/$29; Rindu $5; terjemahan $3,99; itch.io $2; skill $12.

### Penjualan
- AI yang jual; Cipta hanya turun tangan bila URGENT + keputusan (21 Nov 20:57).
- Fokus kebutuhan customer: dengarkan masalahnya, cari solusinya, tawarkan produk yang menjawab kebutuhan itu (21 Nov 20:50).
- Jadwal penjualan: 09:00–11:00 penawaran baru, 19:00–21:00 follow-up + balasan. Target: 20 toko/hari + 1 balasan; 1 closing/minggu; Rp10.000.000 Des 2026.
- Saluran penawaran: Instagram, TikTok, Threads (DM). Facebook NANTI bila namanya sudah ganti (21 Nov 11:48). WA TIDAK USAH — penjualan/pemasaran/promo/penawaran via email + DM (22 Nov 16:03).
- Template DM A25 (22 Nov 13:45): pesan 1 TANPA harga; harga masuk pesan 2 (USD + katalog); follow-up Hari 3–4–7–14; target reply 15%+. Harga IDR lama TIDAK dipakai lagi di DM.
- Penawaran disiapkan dan dikirim A25; Cipta hanya bila URGENT (21 Nov 11:43).
- Mandat bulan ini — WAJIB (22 Nov 13:44): semua agent.ai harus AKTIF, KONTRIBUSI, INISIATIF, KREATIF, VISIONER, INOVATIF bulan ini. Bulan ini HARUS ADA closing dan pemasukan.
- Strategi 5 sosial + strategi viral/FYP WAJIB dipakai agent penjualan, pemasaran, support, build (22 Nov 13:37–13:42).
- Strategi FYP disetujui (22 Nov 03:45): FYP → profil → link bio → chat → closing; konten harian 1–2 video (07:00 + 20:00) + penawaran langsung (09:00–11:00); hook 0–2 detik, completion rate yang utama.
- Strategi $5.000/bulan ditegaskan (22 Nov 13:03): campuran ≈ $4.980/bulan (TARGET, bukan janji).

### Platform & akun
- Pakai akun Cipta semua — JANGAN buat akun baru tanpa persetujuan Cipta (22 Nov 05:13).
- Semua akun pakai SATU kata sandi yang sama (nilai TIDAK disimpan). Kata sandi TIDAK PERNAH diketik dari chat — hanya lewat kartu aman atau Cipta ketik sendiri.
- Kartu sandi dibuat sama saja ke depannya (22 Nov 09:39).
- Buat semua register kecuali Agensi.io (22 Nov 09:34). Agensi.io PENDING — jangan buat akun sampai Joeri membalas / 24 jam tanpa kabar (22 Nov 09:31, 09:34).
- A27 pegang semua email (3 Gmail terhubung: masduki1189, ciptabintanglestari, lawaklucu182) (21 Nov 08:41–08:47).
- A27 penanggung jawab pesan masuk SEMUA kanal + selalu cek; A26 CS yang menangani/membalas chat (dikoreksi 22 Nov 15:24).
- Alur verifikasi HARUS konsisten: kode tiba di email → A27 baca Gmail → referensi diteruskan ke tugas browser yang menunggu → langsung dieksekusi; JANGAN minta kode ke Cipta di chat. OTP tidak pernah disimpan (21 Nov 16:00; ditegaskan 22 Nov 12:19 untuk OSS).
- IG @meongcast dibatasi — akun baru @meongcast.id (22 Nov 12:33); JANGAN langsung kirim DM massal, hangatkan dulu.
- Upwork dilewati — diblokir Cloudflare total; profil hanya bisa dilengkapi Cipta dari perangkatnya (22 Nov 02:40).
- Cek hibah harian — WAJIB info tiap hari (22 Nov 04:08).
- Buka akun jualan diperintahkan — gratis saja, jangan bayar (22 Nov 04:29–04:30).
- Terjemah Inggris disetujui — eksekusi (22 Nov 04:35). Isi cerita nabi harus tetap valid (Al-Quran + hadis sahih).
- KBM dua jalur disetujui — Jalur A dan Jalur B, pakai semua jalur (22 Nov 03:20).
- Sribu gig yang ditolak dilewati (22 Nov 09:10). Telegram ditunda (22 Nov 09:14).
- Email kontak website + toko: masduki1189@gmail.com (tombol "Hubungi via Email"); email customer masuk langsung dicek + draf balasan disiapkan (cron tiap 30 menit); balasan TIDAK BOLEH dikirim otomatis tanpa persetujuan Cipta, kecuali persis template yang sudah disetujui (22 Nov 04:53).

### Yang dilewati / dibuang — jangan diulang tanpa perintah baru
- Copilot dilewati selamanya (22 Nov 15:57).
- 8 item AI dibuang (22 Nov 16:25): Dots, Duet, Gemini Agent, Haiku 5.5, Terra, Carbon, Kimi K3.1 Pro, Muse Spark Open. Rencana kombinasi Hydrogen + Carbon BATAL; peran Carbon standby BATAL. Fokus hanya yang gratis: Hydrogen untuk semua agent.
- 4 marketplace enterprise dilewati: Neura, Salesforce, AWS, Microsoft (22 Nov 11:38). Etsy dilewati — fee $19 tidak dibayar (11:38). Unity dilewati (11:42). Codester dilewati — Turnstile tidak lolos (11:47). Creative Market dilewati — reCAPTCHA/Cloudflare (12:08).
- OSS dilewati dulu (22 Nov 12:11).
- A34 Penerjemah tetap DITUNDA (kecuali translate untuk produk — diaktifkan 21 Nov 11:07).
- Facebook dilewati (22 Nov 04:10) — audit tidak bisa cek Facebook; jangan dicek ulang.

### Lomba & target
- Lomba: ikut hanya yang GRATIS + AMAN + AI DIIZINKAN + peluang menang nyata (22 Nov 03:57). Bila menang, kawal sampai hadiah CAIR.
- Lomba jangan ikut narasi agama Yahudi (21 Nov 10:28) — Reichman dibatalkan.
- Lagu gratis MiniMax/Hailuo TIDAK BOLEH dipakai buat lomba (hak cipta tidak bersih).
- Target $5.000 sebelum akhir Nov 2026 TETAP ("g ada yang mustahil, yang penting dimaksimalkan, tetap optimis") + $10.000 sebelum akhir 2026 + $5.000/bulan untuk seluruh tim (22 Nov 03:20; 21 Nov 19:29).
- Film Artefact: pilih B — Oyen & Momo "(Dis)Connection"; tenggat kirim 1 Des 2026 (22 Nov 04:04).
- Lomba Ulefone: nama Orso (22 Nov 04:15).
- Poster Kemenkes sudah terkirim — jangan kirim ganda; cek pemenang 10 Des.
- Higgsfield: bila dapat kredit gratis, maksimalkan buat video sebanyak-banyaknya + durasi panjang; film kontes 3 menit dulu (21 Nov 11:32).

### Job agent (diputuskan 22 Nov)
- A31 Publish = upload; upload SEMUA PRODUK ke SEMUA platform penjualan; hanya yang disetujui Cipta; kerja 24 jam (08:18–08:24).
- A32 Build kerja 24 jam, fokus membangun (08:25). A33 Pertumbuhan kerja 24 jam, fokus pertumbuhan (08:26). Semua agent.ai 24 jam nonstop (08:27).
- Mengetik tetap A35, copywriter tetap A36 (koreksi 08:21 — keputusan 08:18 soal A31/A32 dicabut).
- A37 Marketplace, A38 QA, A39 Musik, A40 Prompt & Skill (09:14–09:16). Setiap lini produk sudah ada pemiliknya (09:18).
- A41 Rename Komando 40; A42 Harga Toko; A43 Upload Marketplace; A44 Persiapan Video (16:14).
- Peraturan sama untuk semua agent: tugas jelas + skill + kerja 24 jam nonstop lewat pemicu jadwal (09:22).

---

## C. Aturan wajib tanpa nomor — 21 Nov 2026

- Peraturan wajib Cipta (02:47): tugas Muse dan agen.ai WAJIB dipatuhi dan dilaksanakan — jangan banyak nanya; kritik dan saran boleh beserta solusinya; selalu update, cek selalu, jangan ulangi kesalahan yang sama; selalu belajar dan memperbaiki diri; belajar dari agent.ai yang sudah berpengalaman dan terbukti. (Butir 6 kosong — Cipta belum mengisinya.) Isi butir ini hidup di poin 15–20 aturan 30 poin.
- Jam upload 07:00 & 20:00 disetujui (06:32); laporan malam TETAP 20:00 (06:38).
- Cerbung resmi 1 bab/hari (06:43). Upload harian WAJIB tiap hari (06:42).
- Otomatisasi 24 jam: semua cron harian diaktifkan lagi (06:35–06:36).
- Aturan action mandiri + publish (19:54–20:00): eksekusi 1-2-4; Telegram NANTI dulu; bayar = SALAH; kirim duit = izin dulu; kirim penawaran silakan; kerjaan yang OK jalan saja. Publish: UMUM (produk) boleh atas persetujuan Muse selama bagus; TIDAK BOLEH dipublish: dapur (cara kerja internal) atau rahasia perusahaan.
- A34 translate: teks TERTULIS (bukan lisan); ditunda dulu (10:44); diaktifkan khusus untuk produk (11:07).
- Oracle terblokir — Cipta tidak punya kartu; pendaftaran tidak bisa lanjut tanpa kartu (08:30).
- 5 aplikasi distributor masuk toko (10:16) — membatalkan keputusan 20 Nov "cukup 1 aplikasi distributor".
- Platform tambahan ditawarkan, BELUM diputuskan (09:56): Shopee & Tokopedia, X/Twitter, channel Telegram — Cipta belum memilih.
- Update skill semua agent (10:45) — digantikan poin 30 (22 Nov 15:36).

---

## D. Masukan 2 hari terakhir (yang disetujui / jadi panduan)

- Masukan Muse — harga ikuti pasar yang wajar (21 Nov 11:37, disetujui Cipta) → jadi patokan semua harga.
- Masukan Muse — lokal = IDR, global = USD; kupon mingguan 25% eBook / 10% aplikasi & demo web (ganti tiap Senin); bundel aplikasi setelah 10 penjualan satuan (total −20%); giveaway kemitraan YA setelah penjualan pertama (hadiah produk sendiri); live = demo layar + host jawab komentar, Oyen pembuka/penutup (22 Nov 13:51, diputuskan Muse atas perintah Cipta).
- Masukan Muse — "buat baru lalu sewakan" (WaaS) + 2 pengaman: kontrak jelas (customer punya domain+konten; berhenti bayar = situs mati; opsi beli putus) dan jangan taruh semua customer di satu akun Cloudflare (22 Nov 16:53, Cipta setuju).
- Masukan Muse — .com lebih baik dari .co.id (tanpa dokumen; .co.id butuh NIB/SIUP) (22 Nov 17:18).
- Masukan Muse — Stitch dipakai untuk jual web + aplikasi (mockup/HTML saja, bukan backend); Antigravity untuk coding berat, hemat token Muse (22 Nov 14:30–14:31, Cipta setuju).
- Masukan Muse — koreksi ChatGPT soal domain gratis: nama pages.dev belum dicek ketersediaannya; klaim "belum punya akun Cloudflare/dashboard/GitHub" salah — ketiganya sudah ada (22 Nov 17:15).
- Masukan 3 AI (Gemini, ChatGPT, DeepSeek) — sintesis susunan 44 agent: orkestrasi deterministik, kuota 20 panggilan/hari, satu platform = satu pemilik, DoD + bukti, watchdog per jam, dua mesin pendapatan, perbaiki aset lama dulu, funnel konten → toko → produk murah → bundle → jasa, sistem pemicu bukan perintah (22 Nov 16:39, masuk data/rencana-susunan-44-agent.md).
- Masukan riset — Cloudflare Pages host gratis terkuat (hosting komersial diizinkan); GitHub Pages melarang pemakaian komersial — alasan pindah staging (22 Nov 14:43).
- Masukan riset — WaaS: nama "Website as a Service" / sewa website; global $99–149/bln; Indonesia Rp29–149rb/bln; hati-hati ToS Cloudflare §2.2.1(a) (sewa akses = area abu-abu; pola aman = akun Cloudflare per klien) (22 Nov 16:51).
- Masukan riset — game engine gratis: Godot 4.7.2 pilihan utama (22 Nov 14:56); 5 Google tools: Pomelli, NotebookLM, Stitch, Antigravity bisa; Opal MATI 17 Nov 2026 (22 Nov 14:30–14:44).
- Masukan riset — tarif pasar jasa ngetik (Sribu Rp99–150rb), copywriter (Upwork $19–45/jam), translate ($0,04–$0,25/kata) (21 Nov 10:39) — harga toko ketiga jasa ini BELUM diputuskan Cipta.
- Masukan strategi — funnel Lihat → Kenal → Percaya → Beli → Beli lagi; TikTok/Shorts etalase, website+toko kasir, WhatsApp closing, Threads/Facebook kepercayaan; DP 50% sebelum produksi; outreach 15 toko/hari (21 Nov 09:55).

---

## E. Fakta yang jangan ditanya ulang

- 3 Gmail Cipta (A27 pegang semua): masduki1189@gmail.com (utama, PayPal), lawaklucu182@gmail.com (YouTube Podcast meong), ciptabintanglestari@gmail.com (Fiverr, Freelancer, Gumroad, PromptBase, Whop, Udemy, Sribu, Dify).
- Dompet Solana publik (BOLEH dibagikan): 3e8DkfQF6QpgNDRK2sTwrcrQT3C3znVahpNPcAWRicvr. Seed phrase/private key TIDAK PERNAH dibagikan/ditanya.
- PayPal: masduki1189@gmail.com. Semua akun pakai SATU kata sandi yang sama (nilai TIDAK disimpan di mana pun).
- Cipta (Masduki), lahir Jakarta 21 Nov 1989. Diploma Bina Sarana Informatika 2009–2014.
- Akun sosial: YouTube Podcast meong (@Podcastmeong), TikTok @podcast_kucing, IG @meongcast (dibatasi) + @meongcast.id (baru, hangatkan dulu), Threads @ciptabintanglestari, Facebook Masduki Kiki.
- Toko: https://podcastmeong.github.io/ (GitHub Pages, live) + staging https://toko-oyen.pages.dev (Cloudflare Pages, live 22 Nov 17:35). Pusat Komando: https://pusat-komando-972u7.faable.link/.

---

## F. Yang masih terbuka (bukan aturan — jangan tanya ulang, cek menunggu-persetujuan.md)

- Sewa web Rp29/39/49rb per bulan (DRAFT) — butuh persetujuan Cipta atas tier-nya; buyout produk 4; harga update di luar kuota; masa langganan minimum; ambang pindah ke akun Cloudflare per klien.
- Tier harga toko A42 ($29/$59/$99 per produk) — masih DRAFT, butuh keputusan per produk.
- Harga demo web per produk (upload A43) — belum diputuskan.
- Verifikasi Claude di Portal Verifikasi Anthropic — hanya Cipta bisa.
- A34 Penerjemah — tetap DITUNDA atau aktifkan?
- 3 cron baru (03:00 riset, 12:00 kumpul metrik, 23:00 backup Qdrant) — setujui dibuat?
- Product Registry (A30) + Approval Center — setujui dibangun?
- Harga usulan AI, flash sale bundle $17, syarat monetisasi YT, TikTok Creator Rewards, harga launch 30% di bawah target 7 hari — lihat §i dokumen struktur.

---

*Disusun 22 Nov 2026 17:47 dari keputusan.md (279 baris), AGENTS.md, log harian 21–22 Nov 2026. Bila Cipta mengubah salah satu butir, ubah di sini + di keputusan.md, jangan tambah baris yang bertentangan.*
