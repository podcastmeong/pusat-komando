# Skill: Paket Prompt & Skill AI (untuk A40 Prompt & Skill)

> Tugas A40: kemas prompt dan skill AI untuk dijual di Swarms, Agensi.io, dan PromptBase. Harga patokan: skill $12, prompt $2,99–$12 (jangan diubah tanpa persetujuan Cipta).

## Aturan keras

1. **Jangan klaim contoh yang bukan asli** — contoh output harus dari materi asli yang benar-benar ada (video/naskah/puisi yang sudah dibuat). Bila template direkonstruksi dari hasil jadi, tulis jujur di panduan bahwa itu rekonstruksi, bukan prompt asli.
2. **Jangan sertakan kredensial/kunci/token** apa pun dalam paket.
3. **Jujur soal batas produk** — tulis batasan jujur di deskripsi (contoh: suara per klip bisa berubah karena tiap klip digambar ulang; contoh puisi yang gagal pitch harus diregenerasi).
4. **Draf dulu** — paket dibuat draf; terbitkan hanya setelah Cipta menyetujui harga + isi persisnya.

## Format per marketplace

- **Swarms:** skill = paket SKILL.md + modul. Publish via `POST /api/v1/publish/product` type `prompt`; isi SKILL.md di field `prompt`; wajib name, prompt, useCases ≥1, tags; `is_free:false, price_usd:12`. Butuh API key akun Cipta (masduki1189@gmail.com). TIDAK ada endpoint khusus skill. Contoh paket jadi: `~/workspace/skill-pusat-komando-swarms/` (baca `PUBLISH.md`).
- **Agensi.io:** skill = file ZIP (SKILL.md + modul, maks 50 MB, maks 10 tools); tulis kebutuhan kunci API di SKILL.md bila ada. Kreator 70%. Daftar via Google sign-in + creator mode (agensi.io/sell).
- **PromptBase:** HANYA prompt TEMPLATE dengan [variabel] + 4–9 contoh output + panduan kreator yang lolos review (15 mnt–36 jam). Harga satuan $2,99–$4,99; penjual baru maks $19,99. Komisi 20% marketplace / 0% link sendiri (0% setelah 5+ penjualan). Payout Stripe min $30, akun min 30 hari. Contoh draf jadi: `~/workspace/promptbase-14-16/draf-listing-promptbase.md` (9 listing).

## Cara kerja satu paket

1. Pilih produk (skill Pusat Komando / prompt video / prompt ilustrasi / prompt puisi / prompt cerpen).
2. Kumpulkan materi asli (naskah, prompt, contoh output, audio) — jangan karang contoh.
3. Tulis SKILL.md / template prompt + panduan + contoh output (4–9 untuk PromptBase).
4. Uji paket: file bisa dibuka, contoh benar-benar dihasilkan dari template, tidak ada klaim palsu.
5. Laporkan: isi paket, harga usulan, dan apa yang butuh Cipta — lalu terbitkan setelah disetujui.

## Daftar produk A40 (sesuai kebutuhan eksekusi)

| Produk | Marketplace | Harga | Pemilik bersama |
|---|---|---|---|
| Skill Pusat Komando (SKILL.md + 68 modul) | Swarms | $12 | A37 (listing), A38 (QA) |
| Skill Pusat Komando (ZIP ≤50 MB) | Agensi.io | $12 | A37, A38 |
| V1 Paket Prompt Video 60 Detik (Flow/Veo, 6 bagian) | PromptBase | $9,99 | A37, A38 |
| V2 Prompt Video Klip 10 Detik (Flow) | PromptBase | $4,99 | A37, A38 |
| V3 Paket Character-Lock Block | PromptBase | $3,99 | A37, A38 |
| V4 Generator Naskah + Prompt Video (Gemini→Flow) | PromptBase | $4,99 | A37, A38 |
| I1 Prompt Ilustrasi Kucing POD | PromptBase | $3,99 | A37, A38 |
| I2 Paket Prompt Ilustrasi Hewan & Anak | PromptBase | $4,99 | A37, A38 |
| T1 Generator Puisi Indonesia | PromptBase | $2,99 | A37, A38 |
| T2 Prompt Cerpen Kucing Lucu | PromptBase | $3,99 | A37, A38 |
| S1 Skill Pusat Komando | PromptBase | $12,00 | A37, A38 |

Total bila tiap produk terjual 1×: Swarms/Agensi.io $12 + PromptBase $50,96.

## Langkah publish per marketplace (lengkap)

**Swarms — skill $12:**
1. Pastikan API key sudah ada (dibuat Cipta dari swarms.world/platform/api-keys setelah masuk Google masduki1189@gmail.com). JANGAN minta/buat kunci sendiri.
2. Periksa paket di `~/workspace/skill-pusat-komando-swarms/`: SKILL.md + `publish-payload.json` + `publish.sh` (baca `PUBLISH.md` dulu).
3. Jalankan `publish.sh --live` dengan `SWARMS_API_KEY` dari environment. Tanpa kunci, JANGAN jalankan mode live (dry-run saja).
4. Bila berhasil, catat URL listing `https://swarms.world/prompt/<id>` + tanggal di `data/marketplace-20-eksekusi.md`. Bila gagal, laporkan pesan error persisnya — jangan ulangi berkali-kali.
5. Batas platform: 500 prompt berbayar/hari/pengguna; penjual 90% ($10,80/penjualan $12).

**Agensi.io — skill $12:**
1. Daftar/masuk via Google (ciptabintanglestari@gmail.com) + mode kreator di agensi.io/sell.
2. Kemas ZIP: SKILL.md + modul (≤50 MB, ≤10 tools); tulis kebutuhan kunci API (Gemini) di SKILL.md.
3. Upload + isi deskripsi + harga $12 (sekali beli). Kreator 70% ($8,40/penjualan).
4. Tunggu review (keamanan + AI + manusia). Bila ditolak, catat alasannya dan perbaiki — jangan ajukan ulang tanpa perbaikan.

**PromptBase — 9 prompt:**
1. Buat akun PromptBase (browser; bila butuh verifikasi, laporkan ke Muse — jangan lewati dengan data palsu).
2. Per listing: template prompt dengan [variabel] + 4–9 contoh output ASLI + panduan kreator + kategori + tag + harga (lihat `~/workspace/promptbase-14-16/draf-listing-promptbase.md`).
3. Submit satu-satu; review 15 mnt–36 jam. Bila ditolak, catat alasan + perbaiki.
4. Payout via Stripe (min $30, akun min 30 hari; penjualan pending 72 jam). RISIKO: Cipta tanpa kartu kredit — bila Stripe meminta kartu/bank/ID yang tidak bisa dipenuhi, LAPORKAN dan jangan lanjutkan; alternatif Zoneless belum diriset.

## Checklist paket sebelum diserahkan ke A38 (QA)

- [ ] Semua file bisa dibuka; ZIP lolos test; tidak ada file kosong/rusak.
- [ ] Setiap contoh output berasal dari materi asli (atau ditandai jelas sebagai rekonstruksi).
- [ ] Tidak ada klaim fitur yang tidak ada di produk.
- [ ] Tidak ada kredensial/kunci/token di paket mana pun.
- [ ] Harga sesuai patokan; nama + deskripsi sesuai draf yang disetujui Cipta.
- [ ] Panduan kreator menjelaskan cara pakai + batasan jujur produk.

## File kerja

- Paket skill Swarms: `~/workspace/skill-pusat-komando-swarms/` (PUBLISH.md, publish-payload.json, publish.sh, app.py, 68 modul).
- Draf PromptBase: `~/workspace/promptbase-14-16/draf-listing-promptbase.md` + `kekurangan-promptbase.md` (isi kekurangan: T2 butuh 4 contoh cerpen, T1 butuh puisi ke-3, I1/I2 butuh prompt asli + model gambar bila ada).
- Referensi syarat/komisi: `data/skills/eksekusi-marketplace/referensi-20-marketplace.md`.
