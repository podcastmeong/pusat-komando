# Ringkasan Perubahan — Restruktur Toko (PR #2, merge 22 Nov 2026)

Branch: `toko-level-basic-pro-bisnis` → main. Merge commit: `dbfb15c`.
Commit 1: `837e10d` — kontak email saja, tingkat Basic/Professional/Bisnis, game+web per tingkat, eBook per kategori.
Commit 2: `f6656ab` — kategori per kelompok + tautan Beli di + demo gratis.
PR: https://github.com/podcastmeong/podcastmeong.github.io/pull/2 (MERGED 22 Nov 2026 11:53:56 UTC)
Preview: https://toko-level-basic-pro-bisnis.toko-oyen.pages.dev/
Live: https://podcastmeong.github.io/

## Yang diubah

### Toko (artifact `toko-aplikasi` → toko.html, 370.728 byte)
- Kontak jadi EMAIL SAJA: wa.me 0, WA_NUMBER 0, waLink 0; mailto 12, mailLink 11; formulir pemesanan + tanya via email.
- Aplikasi 3 tingkat: Basic $29 / Professional $59 / Bisnis $99; APK +$25 ($54/$84/$124).
- Web 4 produk × 3 tingkat: Demo web $29/$49/$79; Pembuatan web $99/$299/$599; +Free Hosting $119/$319/$619; Sewa Rp29.000/Rp39.000/Rp49.000 per bulan (DRAF).
- Game: $2.99/$4.99/$5.99; APK +Rp400.000.
- Kategori per kelompok (judul + penjelasan): aplikasi per 12 sektor; game per genre (Arkade, Puzzle, Kuis & Edukasi, Simulasi, Lain-lain); POD per tema (Natal, Flora, Fauna, Teknologi, Animasi, Lain-lain); Jasa per jenis layanan (Video, Website, Sistem, Desain); eBook per kategori (Agama, Cerita Anak, Cerpen & Puisi).
- Beli di: label tombol menyebut platform — Beli di Payhip (eBook, EBOOK_PAYHIP + Rindu wgT2k), Beli di Fiverr (4 jasa video, gig https://www.fiverr.com/ciptabintangles/create-a-15-second-ai-promo-video-for-your-business), Beli di Zazzle (POD).
- Demo: tombol Coba Demo sudah ada (128/129 aplikasi); Lihat Demo → ../demo-website/ di 4 kartu web.
- Penjelasan singkat (desc) tampil di semua kartu (aplikasi 129/129, game 10/10, jasa, eBook).
- Tetap: jumpnav 9 kamar, badge 174, palet navy #14263d/#8fb4d9, GSC 1, GA4 2.

### Kamar produk (repo, 8 file)
- aplikasi/index.html: 132 kartu per sektor (12 sektor) + per tingkat; Coba Demo 128; wa.me 0.
- game/index.html: 10 kartu per genre; wa.me 0.
- demo-website/index.html: 15 template per jenis usaha + 4 produk web × 3 tingkat; Lihat Demo 16; Lihat Template Demo ×3 + anchor #template-demo; wa.me 0.
- ebook/index.html: 12 kartu per kategori (Agama 10, Cerita Anak 1, Cerpen & Puisi 1) + 39 judul rencana; Beli di Payhip ×6 (Nuh, Yunus, Yusuf, Musa, Ibrahim, Rindu); wa.me 0.
- pod/index.html: 14 kaos per tema; Beli di Zazzle ×14; wa.me 0.
- foto-stok/index.html: 12 foto per tema; wa.me 0.
- episode.html: 7 episode per genre (Podcast 3, Promo 3, Drama Horor 1); wa.me 0.
- studio.html: Beli di Fiverr ×3 (video 15/30/60 detik); wa.me 0.

## Verifikasi (preview + live, angka sama)
- 11 halaman HTTP 200; toko.html 370.728 byte (preview = live).
- wa.me 0 (literal) di toko + semua kamar; "Business" 0; 5 inline script lolos node --check.
- Harga per tingkat utuh (lihat toko.html); badge 174; GSC 1; GA4 2.
- eBook Payhip ×6, studio Fiverr ×3, pod Zazzle ×14, demo-web Template Demo ×3, aplikasi Coba Demo ×128.

## Sisa / terbuka (bukan gagal — di luar keputusan atau diblokir fakta)
- Koreksi tingkat per produk (DRAF): menunggu koreksi Cipta per produk.
- Gumroad: toko satukiki.gumroad.com MASIH KOSONG (catatan artifact v77) — klaim lama "10/10 eBook live" tidak benar; tidak ada tautan Gumroad per produk di mana pun. Hanya tautan toko di hero/footer.
- PromptBase (S1 in review, V1 submitting) dan Whop (menunggu Cipta) belum live — tidak ada tautan.
- Skill Pusat Komando BUKAN produk toko — tidak ada tautan Swarms di toko/kamar.
- Musik: tidak ada produk musik di toko/kamar mana pun — tidak ada yang dikelompokkan/ditautkan; jangan mengarang produk.
- eBook Abu Bakar, Umar, Syafi'i, Salahuddin: belum di Payhip (upload ditolak 3×) — tanpa tautan Payhip, tombol "Segera Hadir".
- Ayub: tidak ada tautan KaryaKarsa di kamar eBook (hanya Kolam + Rindu) — URL-nya tidak tercatat di kamar; toko menampilkannya sebagai Terbit.
- Harga lama Rp di luar keputusan ini TIDAK diubah: video promo Rp75/150/250rb, custom-system +Rp100/250/500rb, poster/foto Rp35/50/150rb, langganan Rp49/99/199rb per bulan, Kos Rp999.000, eBook Rp29.000/Rp19.000, cerbung KBM Rp1.500, Digital Menu QR premium Rp999.000/Rp1.499.000/Rp2.499.000.
- Sisa sebutan WhatsApp di toko (11) dan kamar (1 di aplikasi, fitur Faktur) adalah fitur produk / kanal distribusi, bukan tautan kontak — dibiarkan sesuai instruksi.
- Catatan: harga Fiverr ($20/$40/$70) vs harga langsung Rp75/150/250rb untuk video promo adalah dua kanal berbeda — harga tidak disamakan; keputusan harga kanal bila perlu menyusul.
- Tautan "Beli di Gumroad" di hero/footer toko mengarah ke toko Gumroad yang masih kosong — dibiarkan apa adanya sesuai keputusan sebelumnya (jangan klaim produk sudah bisa dibeli di sana).
