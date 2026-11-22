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
