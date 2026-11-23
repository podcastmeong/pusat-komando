# Skill: Triase + Cek Duplikat (untuk A61 Triage & Severity Analyst + A68 Duplicate & Prior-Art Checker)

> Perintah Cipta 23 Nov 2026 — hanya temuan yang berpeluang dibayar yang maju. Duplikat = hadiah dibagi atau hilang.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Skor setiap temuan berdasarkan tier hadiah program; putuskan maju/tidak |
| Pengerjaan | **A68 Duplicate & Prior-Art Checker** | Cek temuan terhadap laporan publik/CVE sebelum tenaga dihabiskan |
| Audit | **A60 Security Auditor** | Validasi temuan yang lolos triase sebelum draf laporan |

## Tier hadiah per program (terverifikasi 23 Nov 2026)

| Program | Tier |
|---|---|
| Muse (Meta) | $5rb (bypass kontrol) · $7,5rb (eskalasi hak) · $10rb (source code/rahasia fleet) · $25rb (info disclosure bernilai tinggi) · $130rb (agent pengguna tertentu; 0-click $130rb / 0,5-click $90rb / 1-click $50rb / 2 klik $25rb / >2 $10rb) · $250rb (fleetwide) · $300rb (kompromi produksi Meta) · minimum $500 |
| OpenAI Safety | P1 $5.500–$7.500 (pool $1jt/tahun) |
| Google AI VRP | S1 $20rb · S2 $15rb · A1 $5rb · A2 $5rb · maks $30rb/laporan (pengali kualitas 0,8–1,2 + novelty $1rb–$5rb) — dieksekusi Tim 4 via analisis format saja (tanpa payload; payload diblokir) |
| 0din | Low ≤$500 · Medium ≤$2.500 · High ≤$5.000 · Severe ≤$15.000 |
| ViKernel | $500/musim (Season 1–3) · $1.000 (Season 4) + $500 Special Award tiap musim |

## Aturan keras

1. **Skor dulu, kirim kemudian.** Setiap temuan diberi skor (dampak × tier program × bukti) SEBELUM masuk antrean laporan. Tanpa skor = tidak maju.
2. **Cek duplikat SEBELUM tenaga dihabiskan.** Periksa laporan publik, pengungkapan, CVE, writeup, HackerOne/Bugcrowd. Temuan yang kemungkinan duplikat ditandai dan TIDAK dikirim.
3. **Aturan duplikat 0din:** Medium+ yang diterima dalam 7 hari sejak pengiriman pertama BERBAGI hadiah. Low: ke-1 100%, ke-2 50%, ke-3 20%, sisanya kredit saja.
4. **Meta: duplikat = tidak dibayar.** Jangan kirim temuan yang sudah dikenal.
5. **Hanya yang lolos triase maju ke A60.** A60 mengaudit; A60 tidak pernah meloloskan temuannya sendiri.
6. **Catat semua keputusan** (maju/tidak + alasan) di `~/workspace/catatan/log-bug-bounty.md`.

## Alur kerja

Temuan masuk → A68 cek duplikat (publik/CVE/writeup) → A61 skor per tier program → lolos? → A60 audit → draf laporan (A67) → Cipta setuju → kirim. Tidak lolos → catat alasan, kembali ke riset/varian.
