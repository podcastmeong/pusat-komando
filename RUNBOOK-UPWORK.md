# RUNBOOK UPWORK — Operasional Harian Tim Upwork
Dibuat 20 Nov 2026 · Berlaku bersama SOP Kerja Sama Agent AI v1.3 · Strategi lengkap: `~/workspace/your_files/strategi-upwork/strategi-upwork.docx` · Riset: `~/workspace/your_files/oyen-podcast/riset-upwork-2026-11-20.md`

## Aturan keras (baca dulu)
- Semua output Agen 14 adalah **DRAF** sampai Cipta menyetujui isi persisnya.
- **Tidak ada pengiriman proposal/lamaran, pembayaran, atau submit dokumen tanpa persetujuan eksplisit Cipta.** Agen 14 tidak punya fungsi kirim — sengaja.
- Dilarang mengarang portofolio, klien, penghasilan, rating, atau janji views/viral/penjualan naik. Bila data kurang, tulis "belum cukup data".
- Fokus gratis dulu: dilarang langganan berbayar (Freelancer Plus, Connects berbayar) sampai ada pemasukan dan Cipta setuju.
- Kode verifikasi TIDAK PERNAH disimpan di file/log/memori.

## File & alat
| Apa | Lokasi |
|---|---|
| Agen 14 (kode) | `pusat-komando/agents/a14_upwork.py` |
| Log lamaran | `pusat-komando/data/lamaran_upwork.json` |
| Profil freelancer (draf) | `pusat-komando/profil-upwork.md` |
| Template proposal (draf) | `pusat-komando/template-proposal-upwork.md` |
| Tab dasbor | Pusat Komando → tab "14 · Upwork" (lokal; deploy Faable tertunda) |
| Strategi | `~/workspace/your_files/strategi-upwork/strategi-upwork.docx` |
| Riset | `~/workspace/your_files/oyen-podcast/riset-upwork-2026-11-20.md` |

## Status lamaran di lamaran_upwork.json
`riset` → `draf` → `disetujui` → `dikirim` → `dibalas` → `wawancara` → `menang` / `tolak` / `tidak_merespons`.
Jangan lamar job yang sama dua kali — Agen 14 cek duplikat judul+klien/tautan sebelum mencatat.

## Alur harian
### PAGI — 05:00 (rencana harian, sebelum laporan pagi)
1. Agen 14 cari job baru di 5 kategori prioritas (video AI/ads, short-form editing, website statis, web app satu file, game HTML5).
2. Saring tiap job (cek_job_layak): pembayaran klien terverifikasi; fixed ≥ $50; hourly ≥ $10/jam; baru diposting (<2 jam); proposal masih <10–15; tolak "unpaid test"/"free trial"/janji viral/crypto.
3. Target: **5 job diteliti/hari**. Catat ke `lamaran_upwork.json` (status `riset`).
4. Untuk 2–3 job terbaik: tulis draf proposal (panjang + singkat, dari `template-proposal-upwork.md`, personalisasi per job: sebut detail job, 1–2 sampel relevan, 2–3 pertanyaan). Status → `draf`.
5. Cek Connects: biaya per job + sisa jatah gratis (10/bln). Lewati job >6 Connects selama pakai jatah gratis.
6. Masukkan ke rencana pagi 05:00: job diteliti, draf siap, Connects tersisa, undangan masuk (bila ada).

### SIANG — persetujuan & pengiriman
1. Muse tampilkan draf proposal ke Cipta (isi persis + job + biaya Connects + tarif).
2. **Hanya yang disetujui Cipta yang dikirim.** Setelah kirim: status → `dikirim`, catat tanggal + Connects terpakai.
3. Undangan klien (0 Connects): balas <1 jam bila ada — draf balasan tetap perlu persetujuan Cipta bila berisi penawaran/harga.
4. Bila klien membalas: status → `dibalas`; bila lanjut interview: `wawancara`. Draf jawaban interview disiapkan Agen 14, disetujui Cipta.

### MALAM — 20:00 (laporan malam)
Masukkan ke laporan malam (seperti agen lain):
- Proposal terkirim hari ini (judul + klien + Connects).
- Balasan / wawancara / kontrak baru.
- Connects tersisa bulan ini; job diteliti vs target 5/hari.
- Kendala (mis. verifikasi, Connects habis, tidak ada job cocok).

## Checklist sebelum kirim proposal (wajib)
- [ ] Cipta sudah menyetujui isi persis proposal ini (bukan template umum).
- [ ] Job lolos saringan (pembayaran terverifikasi, budget layak, proposal masih sedikit).
- [ ] Proposal 100–150 kata, hook personal (detail job), 1–2 sampel relevan + tautan hidup, 2–3 pertanyaan, tanpa janji palsu.
- [ ] Tarif jelas ($10/jam atau fixed per scope) dan konsisten dengan tangga tarif.
- [ ] Biaya Connects dicek + sisa jatah cukup; tidak ada boost.
- [ ] Bukan job duplikat (cek `lamaran_upwork.json`).
- [ ] Setelah kirim: status diubah ke `dikirim` + Connects dicatat.

## Setelah kontrak menang
1. Status → `menang`. Kerja HANYA di dalam kontrak Upwork.
2. Fixed-price: tunggu label **Funded** sebelum mulai. Hourly: catat waktu di **Upwork Desktop App**.
3. Serahkan hasil lewat Upwork; minta review dengan sopan setelah selesai.
4. Bila klien minta kerja di luar Upwork / bayar di luar: TOLAK dan laporkan ke Muse (melanggar aturan Upwork).
5. Bila selesai + review masuk: hitung bersih (kotor − service fee 0–15% − withdrawal) dan catat di laporan mingguan; evaluasi tangga tarif.

## Rutinitas mingguan (Senin)
- Agen 10: perbarui riset (tarif, kategori ramai, kompetitor, aturan Upwork terbaru) → masuk `riset-upwork-*.md` bila ada perubahan.
- Agen 14: laporan mingguan (lihat template di bawah).
- Evaluasi fase target (Bab 5 strategi). Bila meleset 2 minggu: evaluasi kategori/harga/proposal — jangan banting harga.

## Template laporan mingguan (isi + kirim ke laporan malam Senin)
```
MINGGU KE-__ (tanggal __ s.d. __) — UPWORK
- Job diteliti: __ / target 35 (5/hari)
- Proposal dikirim: __ (Connects terpakai: __ / sisa bulan ini: __)
- Balasan: __ | Wawancara: __ | Kontrak menang: __ | Ditolak: __ | Tidak merespons: __
- Penghasilan minggu ini: $___ (kotor) → $___ (bersih setelah fee + withdrawal)
- Total kumulatif: $___ kotor / $___ bersih | Review: __ | Tarif saat ini: $___/jam
- Kendala: ...
- Rencana minggu depan: ...
```

## Yang diputuskan Cipta (terbuka, 20 Nov 2026)
- [ ] Opsi billing method untuk beli Connects (kartu debit BCA Mastercard/Visa? tetap gratis? pakai saldo penghasilan nanti?) — tanpa kartu kredit, pembelian Connects tertahan.
- [ ] Metode payout utama: PayPal (masduki1189@gmail.com) atau Direct to Local Bank BCA ($0,99) — nama harus "Masduki" di semua tempat.
- [ ] KTP untuk verifikasi identitas (diajukan saat Upwork meminta, maks 7 hari).
- [ ] Naik tarif ($15 → $20–25 → $30) — hanya setelah review masuk, per tangga tarif.
- [ ] Freelancer Plus ($19,99/bln) — hanya bila penghasilan sudah menutupinya.
- [ ] Setelah Upwork jalan: Fiverr, Freelancer.com, Sribulancer, Projects.co.id, Fastwork.

## Siap dipakai besok (21 Nov, saat akun jadi)
1. Profil freelancer draf (`profil-upwork.md`) — salin ke Upwork setelah Cipta periksa.
2. Template proposal (`template-proposal-upwork.md`) — panjang + singkat + follow-up.
3. Log lamaran kosong siap isi (`lamaran_upwork.json`).
4. Runbook ini + strategi + riset.
5. Urutan besok: Cipta klik Cloudflare → Muse isi akun (judul, $10/jam, foto, overview, skill, portofolio 5 tautan) → ajukan verifikasi identitas (KTP bila diminta) → isi info pajak (W-8BEN) → tambah metode penarikan (PayPal/BCA — Cipta putuskan) → Agen 14 mulai cari 5 job pertama.
