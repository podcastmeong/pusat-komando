# Rencana Susunan 44 Agent — Desain Final (Sintesis 3 AI, 22 Nov 2026)

**Sumber:** brainstorm Gemini, ChatGPT, DeepSeek (22 Nov 2026, file `~/workspace/research_notes/brainstorm-44-agent-{gemini,chatgpt,deepseek}-2026-11-22.md`).
**Claude: TIDAK ADA jawabannya** — akun "Cipta Bintang Lestari" belum terverifikasi, pesan gagal terkirim. Tidak diada-adakan; bila Cipta verifikasi nanti, brainstorm Claude bisa ditambahkan sebagai lampiran.
**Status:** desain final untuk dieksekusi. Nomor agent TIDAK diubah — semua ide dipetakan ke roster yang sudah ada (`data/agents.json`).

## Aturan keras yang mengikat desain ini

- **Roster tetap:** A01–A44 sesuai `data/agents.json` + 2 standalone (Oyen Pintar, Momo Pintar). Pemetaan A01–A44 yang dikarang ketiga AI saling bertentangan dan bertentangan dengan roster → **dibuang semua**.
- **Harga tetap** (disetujui Cipta 22 Nov 06:58, 13:15–13:18, 13:51): eBook $4,99; bundle 3 $11,99 / 9 $24,99; aplikasi $29/$59/$99 (+$25 APK); game $2,99/$4,99/$5,99, bundle 3 $9,99; demo web $29/$49/$79; jasa web $99/$299/$599; video promo $19/$39/$69 (Fiverr $20/$40/$70); POD $2,99/$7,99/$14,99; musik $5/$19/$29; Rindu $5; terjemahan $3,99; itch.io $2; skill $12. Lokal (DM langsung): video Rp75.000/150.000/250.000; aplikasi Rp499.000+; eBook Rp29.000; Rindu Rp19.000.
- **Penawaran:** A25 (AI) yang MENGIRIM penawaran; Cipta hanya bila URGENT (aturan 21 Nov 11:43, 20:50, 20:57). Usulan ChatGPT "DM butuh persetujuan" **tidak dipakai**.
- **Persetujuan:** umum diserahkan ke Muse (22 Nov 10:20–10:23); KHUSUS Cipta hanya (1) bayar/kirim uang, (2) keputusan urgent. Agent pelaksana TIDAK BOLEH menyetujui pekerjaannya sendiri.
- **Gratis saja.** Hydrogen 20 panggilan/hari per proyek API. Bila kuota habis → **rotasi akun** (perintah Cipta 22 Nov 16:33: "Klo token mereka habis ganti email lain buat masuk") — lihat §6.5. Jangan pernah bayar.
- **Jangan sentuh:** artifact toko, harga toko, `toko.html` repo, cron yang sudah jalan.

---

## (a) Kesepakatan 3 AI — 12 poin yang sama di ketiganya

1. **Orkestrasi deterministik.** Mayoritas kerja pakai aturan/template/skrip (cron, Python, template, Qdrant). LLM hanya untuk keputusan bernilai tinggi, sintesis kreatif/strategis, dan verifikasi kompleks. Jangan biarkan 44 agent memanggil API bebas.
2. **Kuota 20 panggilan/hari adalah batas keras bersama.** Batching: 1 panggilan memproses 5–10 item sekaligus, bukan 1 item = 1 panggilan. Satu Budget Manager + cache/Qdrant supaya pertanyaan sama tidak diulang.
3. **Satu platform = satu pemilik.** Tidak ada dua agent yang memegang kanal yang sama — mencegah tabrakan dan "tidak ada yang jaga".
4. **DoD + bukti, bukan laporan.** Tugas selesai hanya bila ada output nyata + bukti (file/URL/log bertanggal). Verifier independen — agent tidak boleh memeriksa hasil kerjanya sendiri.
5. **Watchdog per jam + eskalasi bertingkat.** Gagal 2× → eskalasi. Heartbeat diawasi; tugas lewat tenggat masuk antrean eskalasi.
6. **Dua mesin pendapatan bersamaan.** Mesin A penjualan langsung (jasa + bundle, cepat) dan Mesin B audience organik (views/follow/subs/like/jam tayang, jangka panjang). Jangan tunggu monetisasi platform untuk mulai jualan — audience diarahkan ke toko/jasa sejak hari pertama.
7. **Product Lifecycle dulu, produk baru kemudian.** Perbaiki 61 aplikasi + 15 demo website + listing yang sudah ada sebelum membuat produk baru (ChatGPT: 60% waktu ke aset lama). Ide baru harus lolos gate riset → validasi → produksi → QA → rilis.
8. **Funnel yang sama.** Konten gratis (hook masalah/cerita) → follow/subscribe/trust (bukti nyata: demo, cuplikan isi, log kerja) → toko/marketplace (produk murah $5–$19) → bundle/upsell ($39–$99) → jasa ($99–$599).
9. **Sistem pemicu, bukan perintah.** Kerja jalan lewat trigger (waktu, event, kondisi, tenggat, kegagalan, target) + antrean tugas — agent mengambil tugas sendiri, bukan menunggu Muse menyuruh.
10. **Yang tetap butuh manusia:** bayar/kirim uang, akun/login/KYC/verifikasi, ubah harga, refund/sengketa, klaim sensitif ("terbaik", "dijamin"), konten keagamaan sensitif, hapus produk/database.
11. **Oyen & Momo independen.** Keduanya standalone, memori terpisah, tidak mengambil alih tanggung jawab agent mana pun, tidak mengubah kontrak tugas/data inti agent lain. Oyen = strategi + kreatif; Momo = auditor + memori.
12. **$5.000 dalam 8 hari sangat agresif, bukan janji.** Ketiganya sepakat: dari posisi Rp0 + audiens kecil, target itu hanya mungkin lewat penjualan jasa bernilai tinggi + bundle — bukan lewat views/followers atau iklan.

---

## (b) Perbedaan + yang dipakai / dibuang

| Topik | Gemini | ChatGPT | DeepSeek | Keputusan |
|---|---|---|---|---|
| Pemetaan A01–A44 | 7 divisi karangan | 8 divisi karangan (bahkan 2 pemetaan berbeda dalam 1 jawaban) | 3 lapis karangan | **Dibuang semua.** Pakai roster `agents.json` (§c). |
| Harga jasa web | $150–$500/proyek | Paket IDR Rp1,5jt–Rp5jt | $50 landing page | **Ditunda — butuh keputusan Cipta.** Harga disetujui ($99/$299/$599) tetap. |
| Harga video promo | $50–$150/paket | Rp75.000 (paket) | $25 (Fiverr) | **Ditunda — butuh keputusan Cipta.** Harga disetujui ($19/$39/$69; Fiverr $20/$40/$70) tetap. |
| Bundle flash sale | Bundle $49–$149 | Bundle Rp99rb–299rb | Bundle $17 (eBook+prompt+game) | **Ditunda — butuh keputusan Cipta.** Bundle eBook 3 $11,99 / 9 $24,99 sudah disetujui dan tetap. |
| DM penjualan | — | "DM butuh persetujuan" | Draft → manusia kirim | **Ditolak.** Aturan Cipta berlaku: A25 (AI) mengirim; Cipta hanya bila URGENT. |
| Syarat monetisasi YT | — | 500 subs/3.000 jam atau 3 jt Shorts; 1.000 subs/4.000 jam atau 10 jt Shorts | 8.000 jam mulai 1 Feb 2027 | **Keduanya KLAIM AI, belum terverifikasi, dan bertentangan.** Dipakai sebagai target kerja sementara: kejar 1.000 subs + 4.000 jam (jalur lama). Verifikasi resmi sebelum diklaim ke Cipta. |
| TikTok Creator Rewards | — | Indonesia TIDAK termasuk (klaim) | Dianggap bisa (klip 60–180 dtk) | **Klaim bertentangan, belum terverifikasi.** Jangan andalkan untuk pendapatan. Fokus TikTok = audiens + jualan lewat tautan. |
| Alokasi 20 panggilan/hari | Oyen 2, produksi+konten 8–10, QA/katalog/penawaran 4, Momo+eskalasi 2–3, buffer 1–2 | Per divisi: direksi 2, riset 4, produksi+QA 5, marketing 3, penjualan 3, analisis 2, cadangan 1 | Hanya A01/A02/A04 pakai LLM (~9) | **Dipakai: model ChatGPT per divisi (§6.4) + batas keras DeepSeek (LLM hanya untuk keputusan) + batching Gemini.** |
| Volume konten harian | 1–2 Shorts/kanal, 2–3 Reels/akun, 3–4 TikTok, 3–5 Threads | 8–12 konten pendek/hari total | 1 post+2 story/IG, 1 video/TikTok, 1 Shorts/YT | **Aturan wajib Cipta (poin 2) menang:** video min 5, foto 50, eBook 20, dst. Angka AI jadi target operasional per kanal (§e). |
| Jadwal kerja | Tidur 85–90% waktu, bangun via trigger | Jadwal 24 jam (tiap jam ada tugas) | Cron 4 titik (jam, 06:00, 12:00, 23:00) | **Dipakai: tidur default (Gemini) + slot pemicu ChatGPT sebagai cron, bukan jam kerja LLM (§6.6).** |
| Peran Oyen Pintar | Chief of Staff + Revenue Strategist | Creative Lab | Dashboard approval harian | **Gabungan (§d).** |
| Peran Momo Pintar | Chief Memory, Quality & Watchdog Auditor | Independent Auditor | Alert WA eskalasi kritis | **Gabungan (§d).** Alert ke Muse/Cipta lewat laporan (WA customer tetap tidak dipakai untuk penawaran). |
| Prioritas produk | QA katalog + toko dulu | 60% aset lama; skor bobot 1–5 | 5 gate (riset→validasi→produksi→QA→rilis) | **Dipakai semua:** skor ChatGPT + 5 gate DeepSeek + audit toko Gemini (§5). |

---

## (c) Susunan final — 7 divisi di atas roster yang ada

| Divisi | Agent | Tugas inti (dari roster) | Output / bukti harian | Pemicu utama | Anggaran API/hari |
|---|---|---|---|---|---|
| **D1 Komando** | A01 CEO, A02 COO, A03 Command Controller, A04 QC, A05 Business Analyst, A30 Operations | A01 arah+prioritas+eskalasi; A02 kapasitas/jadwal; A03 bagi tugas+lacak status; A04 periksa akurasi/kualitas/kepatuhan; A05 hitung KPI/risiko/profit; A30 SOP/dokumen/jadwal | Brief harian (maks 3 prioritas), dashboard status, 1 ringkasan harian A05 | 05:00 rencana pagi; 06:00 brief direksi; 16:00 rekap; 22:00 laporan | 3 |
| **D2 Riset & Peluang** | A06 Market Researcher, A07 Trend Hunter, A08 Product Developer, A09 Competitor Analyst, A10 Product Validator, A28 Opportunity Hunter | A06 masalah+segmen pelanggan; A07 tren+keyword; A08 konsep dari kebutuhan tervalidasi; A09 pesaing/harga/celah; A10 skor validasi ide (1–5 × 5 kriteria, ≥20 kerjakan); A28 lomba/freelance/hibah/kemitraan (+ Upwork Pintar) | 5 ide → 1 ide prioritas; 5 tren; 3 pesaing; 1 brief tervalidasi; maks 5 draf proposal | 03:00 riset tren; 07:00 riset prospek; Senin 07:42 cek pasar mingguan | 4 |
| **D3 Produksi Kreatif** | A11 Video Producer, A12 Image Designer, A15 POD Designer, A17 Creative Writer, A19 Content Producer, A35 Ngetik, A39 Musik, A44 Persiapan Video | A11 naskah+storyboard+video AI; A12 visual/ilustrasi; A15 desain POD; A17 puisi/cerpen/cerbung; A19 1 ide → 7 format draf; A35 ketik draf/naskah/dokumen; A39 lagu 5 + musik 5/hari (gratis); A44 prompt Flow per klip dari naskah disetujui + cek kata dialog + cek mulut | 1 aset utama + variasi; 5 video/hari; 50 foto/hari; 5 puisi+5 cerpen/hari; 1 bab cerbung; 12 prompt klip/malam produksi | 06:30 persiapan video; 09:00 produksi utama; 11:00 produksi video/materi; 13:00 produksi eBook/game; 21:00 produksi video | 5 |
| **D4 Produksi Produk Digital** | A13 App Developer, A14 Web Developer, A16 eBook Publisher, A18 Game Developer, A32 Build, A40 Prompt & Skill | A13 aplikasi (backlog); A14 website/landing/katalog; A16 eBook (nulis+edit+terbit); A18 game; A32 build aplikasi/website/produk 24 jam; A40 kemas prompt+skill (Swarms/Agensi.io/PromptBase) | 1 tugas kecil/hari per agent; rilis kecil 1/minggu; paket ZIP + manifest + checksum | 09:00 produksi utama; 12:00 produksi aplikasi/website; brief tervalidasi dari D2 | 2 |
| **D5 Pemasaran & Platform** | A20 Instagram (2 akun), A21 TikTok (2 akun), A22 YouTube (2 kanal), A23 Threads (1 akun), A24 SEO & Growth, A33 Pertumbuhan | A20 caption+visual+jadwal+inbox IG; A21 video+hook+caption+analitik TikTok; A22 Shorts/video+judul+deskripsi YT; A23 utas+percakapan Threads; A24 keyword+optimasi+distribusi; A33 riset konten + naikkan follower/subs/view/like + strategi monetisasi | 3–5 konten terbit/hari lintas kanal (setelah izin); 1 ide → 7 format draf; 1 optimasi + 3 keyword/hari | 07:00 + 20:00 upload (aturan wajib poin 1); 05:00 kalender konten; 16:00 analisis sosmed; 18:00 distribusi | 3 |
| **D6 Penjualan & Marketplace** | A25 Sales, A26 CS, A27 Email/Messages, A31 Publish, A36 Copywriter, A37 Marketplace, A38 QA, A42 Harga Toko, A43 Upload Marketplace | A25 pipeline+penawaran+closing (**A25 yang MENGIRIM penawaran**); A26 jawab pertanyaan/komentar/keluhan; A27 pemilik pesan masuk SEMUA kanal + email + kode verifikasi; A31 upload SEMUA produk ke semua platform (hanya yang disetujui); A36 teks pemasaran/penjualan; A37 eksekusi 20 marketplace; A38 QA verifikasi live sebelum lapor selesai; A42 satu harga per aplikasi toko; A43 upload 61 aplikasi + 15 demo web ke Gumroad/Payhip | 20 penawaran/hari + 1 balasan (target); 1 closing/minggu; Rp10.000.000 Des 2026; inbox terpantau, respons draf <1 jam; 1 batch upload/hari bila disetujui | 09:00–11:00 penawaran baru; 19:00–21:00 follow-up; cek pesan masuk tiap 2 jam (08:00–20:00); cek email tiap 30 mnt | 2 |
| **D7 Keuangan & Sistem** | A29 Finance, A34 Penerjemah (**DITUNDA**), A41 Rename Komando | A29 catat pemasukan/biaya/saldo + rekonsiliasi harian + pantau KYC Mayar; A34 terjemahan — DITUNDA perintah Cipta (tetap di divisi, nonaktif); A41 jaga konsistensi nama+jumlah agent (30→40) di paket skill, app.py, listing live | 1 rekonsiliasi harian; 0 penyebutan jumlah lama di luar pengecualian; laporan keuangan masuk laporan malam 20:00 | 15:00 peluang+keuangan; 16:00 rekap; 00:00 audit backup; 23:00 backup Qdrant | 0 |

**Total anggaran API: 3+4+5+2+3+2+0 = 19 + cadangan 1 = 20 panggilan/hari** (akun utama). Rotasi akun bila habis (§6.5).

**Catatan pemetaan:** A34 tetap DITUNDA (keputusan Cipta) — tidak diberi tugas aktif sampai Cipta mengaktifkan. A41 tugasnya selesai bila 0 penyebutan lama — setelah itu jadi penjaga (cek grep berkala). A42 tugasnya selesai bila semua aplikasi toko 1 harga — setelah itu jadi penjaga harga.

---

## (d) Peran Oyen Pintar & Momo Pintar (disepakati 3 AI)

| | Oyen Pintar | Momo Pintar |
|---|---|---|
| **Peran** | Chief of Staff + Creative Lab + Revenue Strategist | Independent Auditor + Chief Memory, Quality & Watchdog |
| **Tugas** | Daily Priority & API Budget Brief (JSON/MD di repo + Qdrant); putuskan kampanye/penawaran utama harian; ide komedi, hook, dialog, evaluasi daya tarik konten; bantu A11, A17, A20–A23 | DoD Verification Ledger; Qdrant Hygiene Report; Watchdog Incident Log; kritik klaim pemasaran ("terbaik", "dijamin"); uji logika produk; alert eskalasi kritis ke Muse/Cipta |
| **Memori** | Terpisah; boleh bertukar hasil dengan Momo | Terpisah; tidak mengubah kontrak tugas/data inti agent lain |
| **Batas** | Tidak mengubah kontrak tugas agent lain; tidak mengambil alih tanggung jawab agent mana pun | Tidak menghapus data tanpa persetujuan manusia; tidak memanggil LLM hanya untuk menampilkan data (tampilan dari A01/A03) |
| **Anggaran API** | 2/hari (sudah termasuk dalam jatah D1: morning strategy + evening review) | 2–3/hari (sudah termasuk dalam jatah D1/D6: audit + eskalasi) |

---

## (e) Mesin pendapatan 2 jalur + target harian 23–30 Nov 2026

**Posisi awal (jujur):** pemasukan Rp0 di semua platform (cek 22 Nov 03:51). YouTube 79 subs, TikTok 78 followers, IG 2 followers. $5.000 dalam 8 hari = $625/hari — ketiga AI sepakat ini sangat agresif dan bukan janji.

### Jalur A — Penjualan langsung (prioritas 23–30 Nov)
Produk yang dijual (harga disetujui): jasa web $99/$299/$599; video promo $19/$39/$69 (Fiverr $20/$40/$70); demo web $29/$49/$79; aplikasi $29/$59/$99; eBook $4,99; bundle 3 $11,99 / 9 $24,99; game $2,99/$4,99/$5,99; skill $12.
- **Aktivitas harian:** 20 penawaran personal/hari (A25, template DM: pesan 1 tanpa harga, pesan 2 harga USD + katalog); 10 follow-up jatuh tempo; 3 halaman produk diperbaiki (D4+D6); 1 flash bundle/offer aktif.
- **Target aktivitas 23–30 Nov:** 160 penawaran terkirim; reply 15% ≈ 24 balasan; prospek berkualitas 20/hari (riset A28/D2 → verifikasi A25).
- **Target omzet (skenario kerja, bukan janji):** 23–24 Nov $0–$99 (fondasi + 40 penawaran pertama); 25–27 Nov $200–$400 (target 1 closing jasa web $99 + 5 video promo $19–$39); 28–30 Nov $300–$600 (follow-up H+3/H+7 + bundle). **Kumulatif realistis minggu ini: $500–$1.000.** $5.000 tercapai hanya bila 2–3 proyek jasa web $299/$599 closing ATAU ~50 closing produk kecil — di luar jangkauan organik 8 hari; pipeline yang dibangun minggu ini adalah jalan ke $10.000 Desember.
- **Aturan:** fokus kebutuhan customer (dengarkan masalahnya, cari solusinya, baru tawarkan produk yang menjawabnya). Jangan kirim pesan massal yang sama ke semua toko. Satu pelanggan bisa dibeli bertingkat: website → aplikasi kasir → video promo.

### Jalur B — Audience organik (fondasi $5.000/bulan + monetisasi)
- **Konten harian (aturan wajib poin 2):** video min 5, foto 50, eBook 20, lagu 5, musik 5, puisi 5, cerpen 5, POD 5, game 5, website 5, aplikasi 5, prompt 20×6, skill 5, toko live 5, cerbung 1 bab. Publikasi 07:00 + 20:00.
- **Per kanal (target operasional 30 hari, bukan janji):** IG 2 akun — 500 follower/akun, 3% engagement; TikTok 2 akun — 1.000 follower/akun; YT — 300 subs, 500 jam tayang (target 90 hari: 1.000 subs, 4.000 jam — **klaim syarat monetisasi belum terverifikasi**, lihat §b); Threads — 200 follower; email list — 100 subscriber.
- **Rumus konten (DeepSeek, dipakai):** 1 long-form (5–10 mnt)/minggu per kanal YT → dipotong jadi 5–7 klip 60–180 dtk → distribusi ke TikTok/Shorts/Reels. Shorts = discovery, long-form = jam tayang. **Satu ide, banyak format** (ChatGPT): 1 ide → TikTok 30 dtk + Shorts + Reels + Threads + video panjang 3–5 mnt.
- **Eksperimen mingguan (A33):** uji hook A/B (pertanyaan vs kejadian absurd vs punchline vs bersambung) dengan sampel dan hasil jelas — bukan sekadar laporan follower.
- **Funnel:** views → klik toko 20–40/hari → prospek 200 → penawaran 100 → pembelian 10 (angka funnel ChatGPT adalah asumsi awal yang harus diuji, bukan konversi yang dijamin).

---

## (f) Sistem otomatis-mandiri

### 6.1 Enam jenis trigger (ChatGPT, dipakai semua)
| # | Jenis | Contoh | Pemilik |
|---|---|---|---|
| 1 | Time-based (cron) | 05:00 rencana pagi; 06:30 persiapan video; 09:00 produksi utama; 21:00 produksi video; watchdog tiap jam | A03/A01 |
| 2 | Event-based | Produk baru selesai dibuat → QA otomatis aktif; penjualan baru → email terima kasih + upsell (template); order Fiverr masuk → A25/A31 ambil tugas | A04/A38; A27/A16→A26 |
| 3 | Condition-based | Produk tidak terjual 14 hari → review harga/bundle; antrean siap terbit ≥5 → jadwalkan publish | A05/A42; A31 |
| 4 | Deadline-based | Penawaran H+3/H+7 jatuh tempo → follow-up otomatis masuk antrean A25 | A25 |
| 5 | Failure-based | Demo website error / tautan mati → A38 + A14 perbaiki; API timeout → retry exponential backoff, gagal 2× → eskalasi | A38/A43→A14 |
| 6 | Goal-based | Omzet harian masih Rp0 → A01 perintahkan A25 prioritaskan pipeline; A28 siapkan prospek; A36 buat penawaran personal | A01/A05/A29 |

### 6.2 Kontrak eksekusi (DoD) — template wajib
Tugas SELESAI hanya bila 4 syarat terpenuhi (Gemini): (1) input/brief valid; (2) output nyata ada dan tidak kosong; (3) bukti terlampir (timestamp, path/URL/ID, hasil verifikasi); (4) lolos audit Momo Pintar (tanpa error kritis, tanpa duplikat, terindeks Qdrant bila bernilai memori).
```json
{
  "task_id": "MKT-2026-11-23-001",
  "agent": "A25",
  "task_name": "Kirim 20 penawaran personal toko",
  "priority": "high",
  "trigger": "daily_0900",
  "deadline": "2026-11-23T11:00:00+07:00",
  "input": {"market": "UMKM Indonesia", "target_count": 20},
  "definition_of_done": ["20 penawaran terkirim", "Nama toko + kebutuhan tercatat", "Sumber prospek tercatat", "Tidak ada duplikasi"],
  "evidence_required": ["log-penawaran-2026-11-23.csv", "completion_report"],
  "handoff": {"next_agent": "A26", "condition": "ada balasan"},
  "retry_limit": 2,
  "approval_required": false,
  "status": "PENDING"
}
```
Perhatikan: tugas riset prospek TIDAK otomatis memberi izin mengirim pesan — pengiriman adalah tugas A25 dengan kontraknya sendiri.

### 6.3 Status seragam — pakai 9 status SOP Komando (sudah diputuskan, jangan buat baru)
`BACKLOG` (belum dijadwalkan) · `READY` (brief+PIC+tenggat lengkap) · `DOING` (sedang dikerjakan) · `QC` (menunggu pemeriksaan) · `APPROVAL` (menunggu keputusan Cipta) · `APPROVED` (disetujui) · `PUBLISHED / SENT` (sudah terbit/terkirim — simpan URL, waktu, bukti) · `BLOCKED` (terhambat — catat alasan + siapa yang harus bertindak) · `DONE` (selesai — lampirkan hasil + metrik). `ESCALATED` dicatat di `data/log-eksekusi.jsonl` bila tugas naik tingkat. Jangan anggap DONE hanya karena model memberi jawaban — verifier (A04/A38) memeriksa bukti dulu.

### 6.4 Anggaran 20 panggilan Hydrogen/hari (akun utama)
| Divisi | Jatah | Dipakai untuk |
|---|---|---|
| D1 Komando (+ Oyen/Momo) | 3 + 2 = 5 | Prioritas harian, analisis A05, audit Momo, brief Oyen |
| D2 Riset & Peluang | 4 | Batch riset tren/pesaing/prospek, validasi ide |
| D3 Produksi Kreatif | 5 | Batch naskah/hook/dialog, prompt video |
| D4 Produksi Produk | 2 | Batch draf eBook/deskripsi produk |
| D5 Pemasaran & Platform | 3 | Batch hook/caption, eksperimen A33 |
| D6 Penjualan & Marketplace | 2 | Triase pesan A27, batch penawaran personal A25/A36 |
| D7 Keuangan & Sistem | 0 | Rule-based dari file (tanpa LLM) |
| Cadangan | 1 | Gagal/retry |
| **Total** | **20** | |

Aturan hemat (ketiganya sepakat): 1 panggilan per tugas, retry maks 1×; tugas rutin/lookup pakai aturan+file, bukan LLM; simpan hasil riset di Qdrant agar tidak mengulang pertanyaan sama; jangan panggil AI untuk menghitung penjualan atau mengubah status; pemakaian tercatat di `data/log-penggunaan-model.jsonl`; peringatan di ≥15 panggilan. **Satuan hitung (perintah Cipta 22 Nov 16:39–16:40): 1 perintah = 1 panggilan, sampai seterusnya — mis. 1 kali perintah standby cek keluar-masuk surat = 1 panggilan, berapa pun banyaknya surat masuk maupun keluar yang dicek dalam perintah itu.**

### 6.5 Rotasi akun bila kuota habis (perintah Cipta 22 Nov 16:33)
Bila akun utama mencapai 20 panggilan atau menerima 429, runner beralih ke proyek API akun berikutnya: **masduki1189 → ciptabintanglestari → lawaklucu182** (masing-masing 20 panggilan/hari, total maks 60/hari). Setiap peralihan dicatat di `data/log-penggunaan-model.jsonl` (akun, jam, alasan). Bila ketiga akun habis → tugas Hydrogen ditunda besok; jangan pakai model berbayar sebagai jalan pintas. Implementasi di runner (`agents/hydrogen-momo.py`) adalah tindak lanjut minggu pertama (§h).

### 6.6 Jadwal 24 jam — slot pemicu (bukan jam kerja LLM)
Agent "tidur" (mode siaga skrip, 0 panggilan LLM) kecuali ada trigger. Slot yang sudah jalan (cron): 03:30 backup · 05:00 rencana pagi · 05:30/19:30 cek email A27 · 06:30 persiapan video · 07:00 + 20:00 upload · 08:00 freelance (draf) · 09:00 produksi utama + penawaran baru · 10:00 gerakan operasional · 12:00 metrik (baru, A05/A33) · 13:00 distribusi · 14:00 eBook · 15:00 POD · 16:00 tulisan · 17:00 paket konten · 19:30 follow-up penjualan · 20:00 laporan malam · 21:00 produksi video · 23:00 backup Qdrant (baru, A41→A30) · watchdog tiap jam (08:00–21:00).
Slot baru yang diusulkan (butuh persetujuan cron — lihat §i): 03:00 riset tren (D2), 12:00 kumpul metrik (D1/D5), 23:00 backup Qdrant (D7).

### 6.7 Watchdog per jam + eskalasi bertingkat
**Yang diperiksa tiap jam (A38 + Momo Pintar, tanpa LLM kecuali anomali):** heartbeat semua agent ada? Ada pekerjaan macet? Ada tugas lewat tenggat? Antrean menumpuk? Ada kegagalan API? Ada tugas duplikat? Ada hasil tanpa bukti? Ada pemakaian API tidak wajar?
**Aturan:** heartbeat tidak ada 2 jam → WARNING; 6 jam → STALE (A03 routing ulang); output gagal DoD 2× → BLOCKED → eskalasi; penjualan 0 selama 48 jam (Jalur A) → alert ke Muse/Cipta; API melebihi kuota → hentikan pemanggilan AI; output tanpa bukti → ditolak; tugas duplikat → hentikan duplikatnya.
**Tingkat eskalasi:** L1 agent (retry 1–2×, otomatis) → L2 koordinator divisi (ubah prioritas, alihkan tugas) → L3 A02/A03 (konflik antar divisi, sumber daya) → L4 A01/Muse (keputusan bisnis, prioritas strategis) → L5 Cipta (risiko, uang, publikasi sensitif, otorisasi manusia).

### 6.8 Product Registry (pemilik: A30, pemeriksa: A04)
Satu database wajib untuk 61 aplikasi + 15 demo web + eBook + game + jasa (format JSON di `data/`, mengikuti pola Komando — bukan Sheets/SQL baru). Kolom: product_id, product_name, category, version, status (ide/produksi/QA/live/maintenance), owner_agent, qa_agent, price, marketplace, product_url, demo_url, last_updated, sales_count, defect_count, next_action. Dengan registry ini A31 tahu produk mana yang belum dipublikasikan, A37 tahu marketplace mana yang belum terisi, A29 tahu produk mana yang menghasilkan uang.

### 6.9 Alur produksi end-to-end (5 gate, DeepSeek + ChatGPT)
1. **Riset** (D2, Senin): scan tren + 5 kompetitor → 3 ide berskor (demand/kompetisi/effort 1–5; lolos bila demand ≥3 dan kompetisi ≤3; skor prioritas ChatGPT: permintaan 30%, potensi pendapatan 25%, kemudahan produksi 15%, persaingan 10%, kesesuaian aset 20%; total ≥20 kerjakan).
2. **Validasi** (A10): ada ≥3 produk serupa yang terjual? Bisa dibuat ≤3 hari? Bisa dijual $7–$27 (produk kecil) atau sesuai harga jasa? Bila tidak, tolak.
3. **Produksi** (D3/D4, Selasa–Kamis): 1 produk baru per siklus; DoD per lini (eBook: PDF + cover 1200×1800 + listing copy 150 kata + harga terpasang).
4. **Quality Gate** (A04/A38, Jumat): link/file, typo fatal, cover pecah, harga konsisten di semua platform. Gagal → kembali ke produksi (maks 2 putaran → eskalasi).
5. **Rilis** (A31/A37/A43): upload ke Gumroad/Payhip/toko, harga launch 30% di bawah target selama 7 hari (hanya bila disetujui — harga disetujui tetap patokan), affiliate 20% bila tersedia.
**Jadwal mingguan:** Senin riset → Selasa–Kamis produksi → Jumat QA+rilis → Sabtu update listing lama (harga, bundle) → Minggu evaluasi (produk mana yang dapat views/penjualan? catat di Qdrant).

---

## (g) Yang tetap butuh Cipta

1. Bayar/kirim uang (apa pun, berapa pun).
2. Keputusan urgent.
3. Login, kata sandi, kode verifikasi, KYC, verifikasi identitas (termasuk verifikasi Claude di Portal Verifikasi Anthropic — hanya Cipta bisa).
4. Ubah harga (termasuk semua usulan harga AI di §i).
5. Refund / sengketa pelanggan.
6. Klaim sensitif ("terbaik", "dijamin") dan konten keagamaan sensitif — review akhir.
7. Hapus produk / hapus database.
8. Buat akun baru (marketplace, rekening pembayaran).
9. Persetujuan video jadi + judul + caption persisnya sebelum upload; eBook per buku sebelum terbit. (Persetujuan umum lainnya di Muse; agent pelaksana tidak boleh menyetujui pekerjaannya sendiri.)
10. Keputusan atas daftar di §i.

---

## (h) Rencana eksekusi minggu pertama 23–29 Nov 2026

### Besok, Senin 23 Nov 2026
| Jam | Aksi | Agent |
|---|---|---|
| 07:00–09:00 | Audit + aktivasi: audit 44 agent (status/heartbeat), periksa file instruksi, periksa cron+trigger, periksa watchdog, periksa API+anggaran, aktifkan antrean prioritas | A01, A02, A03, A38, A30 |
| 07:00 | Riset tren + kata kunci (slot baru) | D2 (A06/A07) |
| 08:00 | Draf freelance (Freelancer/Fiverr/Sribu — draf dulu, kirim setelah setuju) | A28 |
| 09:00–11:00 | Fokus pelanggan: D2 kumpulkan 30 prospek → A25 verifikasi 20 terbaik → A36 buat 20 penawaran personal → A25 kirim 20 penawaran; A11 siapkan 3 contoh video promo | D2, A25, A36, A11 |
| 12:00 | Kumpul metrik harian (views/likes/follows/klik toko/penjualan) | A05, A33 |
| 12:00–18:00 | Perkuat aset penjualan: A38 uji aplikasi/website/eBook; D4 perbaiki 3 halaman produk; A37 periksa katalog marketplace; A33 uji 3 hook; D5 distribusikan konten | A38, D4, A37, A33, D5 |
| 19:00–21:00 | Follow-up jatuh tempo + balas toko; evaluasi performa penjualan | A25, A26, A27 |
| 21:00 | Produksi video (naskah disetujui saja) | A44, A11 |
| 22:00–23:00 | Laporan harian + prioritas besok + simpan ke Qdrant + backup Qdrant | A01, A05, A30 |

### 24–25 Nov (Selasa–Rabu) — Produksi + penjualan
- Produksi 1 produk baru per siklus (gate 1–3); A43 lanjutkan manifest upload (ZIP + screenshot + verifikasi demo live HTTP 200); 20 penawaran/hari + follow-up H+3; A42 lanjutkan spesifikasi harga toko (tier per produk masih DRAF — butuh keputusan Cipta, §i).

### 26–27 Nov (Kamis–Jumat) — QA + rilis + dorongan
- Jumat: Quality Gate + rilis produk minggu ini; evaluasi funnel (di mana kebocoran: jangkauan → klik → prospek → penawaran → beli); Oyen Pintar fokuskan push ke 20% penawaran/kanal dengan konversi nyata.

### 28–29 Nov (Sabtu–Minggu) — Evaluasi + persiapan Desember
- Sabtu: update listing lama (harga, bundle); Minggu: evaluasi mingguan — produk/kanal mana yang menghasilkan views/penjualan; catat di Qdrant; tetapkan target minggu ke-2 (Desember, jalan ke $10.000); audit 14 hari pertama dimulai (SOP: target versi 2 berdasarkan data).

### Tindak lanjut teknis minggu pertama (bukan keputusan Cipta)
- Implementasi rotasi akun di runner Hydrogen (§6.5) + catat peralihan di `data/log-penggunaan-model.jsonl`.
- Buat file pemicu: `queue/tasks.json`, folder `heartbeat/` (44 file), folder `events/` (DeepSeek) — di `data/`.
- Product Registry awal (A30): isi 61 aplikasi + 15 demo web + 10 eBook dari manifest A43 + katalog yang ada.
- 3 cron baru yang diusulkan (03:00 riset, 12:00 metrik, 23:00 backup Qdrant) — dibuat setelah Cipta setuju (§i no. 7).

---

## (i) Daftar keputusan yang masih butuh Cipta

1. **Harga usulan AI** — DeepSeek: video promo $25, jasa web $50. Gemini: jasa web $150–$500, video $50–$150. ChatGPT: paket IDR Rp499.000 / Rp1.500.000 / Rp75.000 / Rp99.000–299.000. Pakai salah satunya, atau tetap harga disetujui ($19/$39/$69 video; $99/$299/$599 jasa web)?
2. **Flash sale bundle $17** (DeepSeek: eBook + 1 prompt kit + 1 template game, normal $27) — buat dan listing di Gumroad+Payhip, atau tidak? (Bundle eBook 3 $11,99 / 9 $24,99 sudah disetujui.)
3. **Syarat monetisasi YouTube** — klaim bertentangan (ChatGPT: 1.000 subs/4.000 jam atau 10 jt Shorts; DeepSeek: 8.000 jam mulai 1 Feb 2027). Verifikasi resmi dulu, atau pakai jalur lama (1.000/4.000) sebagai target kerja?
4. **TikTok Creator Rewards di Indonesia** — klaim bertentangan (ChatGPT: Indonesia tidak termasuk; DeepSeek: bisa). Andalkan atau tidak?
5. **Rotasi akun API** — sudah diperintahkan Cipta 16:33 ("ganti email lain"); konfirmasi teknis: pakai 3 API key (masduki1189, ciptabintanglestari, lawaklucu182) di runner?
6. **A34 Penerjemah** — tetap DITUNDA atau aktifkan sekarang?
7. **3 cron baru** — 03:00 riset tren, 12:00 kumpul metrik, 23:00 backup Qdrant. Setujui dibuat?
8. **Product Registry** — setujui A30 sebagai pemilik + format kolom §6.8?
9. **Approval Center** — setujui dibangun (catatan siapa menyetujui apa, kapan)?
10. **Verifikasi Claude** — akun "Cipta Bintang Lestari" di Portal Verifikasi Anthropic (hanya Cipta bisa). Kapan dilakukan? (Tanpa ini, brainstorm Claude tidak ada.)
11. **Tier harga toko A42** — spesifikasi siap, tier per produk ($29/$59/$99) masih DRAF. Keputusan per produk tetap menunggu Cipta (terpisah dari dokumen ini; dicatat di `data/a42-spesifikasi-harga-toko.md`).
12. **Harga launch 30% di bawah target 7 hari** (DeepSeek, Gate 5) — setujui sebagai aturan rilis, atau harga langsung harga disetujui?

---

*Dokumen ini adalah desain final sintesis brainstorm 3 AI (Gemini, ChatGPT, DeepSeek), 22 Nov 2026. Claude tidak berpartisipasi (akun belum terverifikasi). Semua angka target adalah target kerja, bukan janji penjualan. Harga yang disetujui Cipta tidak berubah oleh dokumen ini.*
