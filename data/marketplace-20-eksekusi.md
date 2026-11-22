# Eksekusi 20 Marketplace — WAJIB, Tim Produksi

Perintah Cipta, 22 Nov 2026 08:50–08:57: eksekusi SEMUA 20 marketplace, satu-satu dari no. 1; kalau selesai lanjut next. Yang bisa dikerjakan dulu; berhenti hanya bila benar-benar mentok. **Diserahkan ke Tim Produksi (A11–A19), dipimpin A37 Marketplace — WAJIB.** Bekal skill tim: `data/skills/eksekusi-marketplace/SKILL.md` (+ `referensi-20-marketplace.md`) — dibaca sebelum mengerjakan marketplace mana pun. A38 QA memeriksa live sebelum lapor selesai; A40 Prompt & Skill mengemas produk prompt/skill. Aturan Cipta yang berlaku: "Aku g ngerti, biar cepet. Seperti yang kita bicarakan kemarin." — Muse + tim yang mengerjakan, Cipta hanya keputusan urgent.

## Produk per marketplace

| No | Marketplace | Produk | Harga | Status 22 Nov 2026 |
|----|-------------|--------|-------|---------------------|
| 1 | Swarms | Skill Pusat Komando (SKILL.md + modul) | $12 | Paket SIAP (1,6 MB, payload siap). Menunggu Cipta masuk Google masduki1189 → API key → publish |
| 2 | Agensi.io | Skill Pusat Komando | $12 | Harga diputuskan. Balasan ke Joeri menunggu "Setuju" teks persis Cipta; registrasi belum |
| 3 | MCP Market | Skill (bila bisa dijual) | — | BUKAN toko jualan (Hub pengelolaan skill & MCP) — tidak ada jalur jual terverifikasi |
| 4 | Neura Market | Workflow otomatisasi + prompt | — | Belum dieksekusi — riset syarat seller dulu |
| 5 | Apify Store | Tools AI (Actor) | — | Belum cocok — produk kita bukan Actor |
| 6 | Salesforce AgentExchange | Solusi enterprise | — | Belum cocok — butuh kemitraan enterprise |
| 7 | AWS Marketplace | Software/SaaS enterprise | — | Belum dieksekusi — riset syarat seller dulu |
| 8 | Microsoft Marketplace | Aplikasi bisnis | — | Belum dieksekusi — riset syarat seller dulu |
| 9 | Envato Market | Aplikasi Kasir Toko | $59 | Draf listing siap. Pendaftaran author DIJEDA sejak 6 Nov 2026 |
| 10 | CodeCanyon | Aplikasi Kasir Toko | $59 | Draf listing siap. Pendaftaran invitation-only (Code tidak diundang) |
| 11 | Codester | Aplikasi Faktur & Invoice | $29 | Paket listing SIAP (ZIP + dokumentasi EN + 6 screenshot + preview 800×400 + icon 200×200 + demo live). Menunggu Cipta setuju teks + harga + bahasa UI |
| 12 | Unity Asset Store | — | — | TIDAK COCOK apa adanya (butuh proyek Unity/C#). Hanya bila Cipta putuskan port game jadi template Unity |
| 13 | Gumroad | eBook, aplikasi, produk digital | — | LIVE (satukiki.gumroad.com; Payments BCA tersimpan) — isi produk |
| 14 | Creative Market | 8 ilustrasi POD, 3 cover eBook, 3 paket foto | $12–$29/item (usulan) | Draf 14 item + harga usulan siap (total $222 bila terjual 1×). Butuh: portofolio Behance (belum ada) + persetujuan harga + nama toko |
| 15 | Etsy | eBook cerita nabi (Inggris) + POD | — | Akun saja, belum ada toko. Kata kunci + 10 draf listing siap. Biaya setup $19 DILEWATI |
| 16 | PromptBase | 9 paket prompt + skill Pusat Komando | $2,99–$12 (usulan) | Draf 9 listing + harga usulan siap (total $50,96 bila terjual 1×). Butuh persetujuan harga + akun belum dibuat; risiko payout Stripe belum jelas |
| 17 | Payhip | eBook, game, aplikasi, demo website, video promo, POD, musik | — | LIVE (6/10 produk fase 1; 4 tertahan kartu persetujuan) |
| 18 | Whop | Software + membership | — | Belum dieksekusi — riset syarat seller dulu |
| 19 | Fiverr | Jasa: video promo, poster, aplikasi | $19/$39/$69 video | Profil 25%, Gig 1 DRAF. TERHALANG pertanyaan keamanan (hanya Cipta bisa jawab) |
| 20 | Udemy | Kursus (4 modul belajar AI) | — | Belum dieksekusi — riset syarat kursus dulu |

## Urutan kerja (satu-satu)

1 → 11 → 14/16 → 2 → 4, 5, 18, 20 (riset) → 9, 10 (pantau pembukaan) → 3, 6, 7, 8, 12, 15, 19 (butuh keputusan/berkas Cipta).

## Yang butuh Cipta (hanya ini — selebihnya tim yang kerjakan)

- Masuk Google masduki1189 (satu ketukan, di aplikasi Muse) — untuk API key Swarms (no. 1).
- Setuju teks + harga $29 + bahasa UI — Codester (no. 11).
- Setuju harga — Creative Market (no. 14) + PromptBase (no. 16).
- Setuju teks balasan $12 ke Joeri — Agensi.io (no. 2).
- Jawab pertanyaan keamanan Fiverr — no. 19.
- Putuskan: port game jadi template Unity? Buka toko Etsy? — no. 12, 15.

## File kerja

- Paket skill Swarms: `~/workspace/skill-pusat-komando-swarms/` (PUBLISH.md + publish-payload.json + publish.sh)
- Draf 9–12: `~/workspace/marketplace-9-12/` (envato/codecanyon/codester-draf-listing.md + codester-paket/)
- Draf 14: `~/workspace/creative-market-14-16/` — Draf 16: `~/workspace/promptbase-14-16/`
- Pelacak status: `~/workspace/marketplace-20-status.md`
