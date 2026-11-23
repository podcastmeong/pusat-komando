# Skill: Hipotesis Thread-Grant Perplexity (P-1) — Automations

> BELUM DIUJI — dibangun 24 Nov 2026 dari perintah Cipta ("Ok buat", 24 Nov 06:45, Blok F / T20). Hipotesis P-1 BELUM teruji; skill ini hanya memandu perumusan + pengujian hipotesis, bukan bukti celah. HANYA UNTUK BOUNTY (program resmi saja — Perplexity VDP). LARANGAN DESTRUKTIF: dilarang merusak, menghapus, atau mengubah data apa pun; dilarang menguji akun orang lain; dilarang eksfiltrasi data.

## Hipotesis P-1 (satu kalimat)

Recurring runs (automations terjadwal) mewarisi thread-level grants — sebuah run berulang dapat melakukan aksi yang hanya diizinkan oleh grant di level thread, bukan oleh grant run itu sendiri.

## ATURAN FRAMING (wajib, tanpa kecuali)

- JANGAN PERNAH pakai kata "prompt injection", "hallucination", atau "model safety" — baik di hipotesis, catatan uji, maupun draf laporan.
- Framing resmi SATU-SATUNYA: **unauthorized action via reused thread-level grant**.
- Bila sebuah sumber/temuan memakai istilah terlarang di atas, terjemahkan ke framing resmi sebelum dicatat; jangan kutip istilah itu mentah-mentah ke laporan.

## Gerbang akses (keputusan bayar hanya Cipta)

- Pengujian live hipotesis P-1 butuh **Perplexity Pro $20/bln**. Status per 24 Nov 2026: **TERTUNDA — belum diputuskan Cipta**.
- JANGAN asumsikan akses berbayar ada. Sampai Cipta memutuskan: tim T20 hanya riset, perumusan hipotesis, dan penyiapan paket uji (langkah, akun canary sendiri, kriteria sukses/gagal).
- Bila Cipta menolak bayar: hipotesis dicatat sebagai "tertunda — butuh Pro" dan tim beralih ke riset pasif (dokumentasi publik Perplexity, scope VDP, changelog Automations).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Perplexity VDP). Di luar scope = JANGAN.
2. **Hanya akun sendiri + canary palsu milik sendiri.** Tidak ada akun orang lain, tidak ada data orang lain, tidak ada eksfiltrasi.
3. **Setujui target SEBELUM Exploiter berjalan** — Koordinator T20 (A150) menyetujui target + langkah uji; tanpa persetujuan itu, tidak ada eksekusi uji.
4. **Satu akun, satu thread uji, satu grant per uji** — jangan campur grant dari beberapa thread dalam satu uji (hasil jadi tidak bisa diatribusikan).
5. **Bukti minimal:** (a) grant yang ada di level thread, (b) grant yang dimiliki run berulang, (c) aksi yang terjadi padahal run tidak punya grant itu, (d) HTTP request/response + langkah reproduksi lengkap.
6. **Bila hasil negatif** (run TIDAK mewarisi grant): catat sebagai hipotesis gugur dengan bukti — bukan kegagalan; jangan ulangi uji yang sama tanpa variabel baru.
7. **Tidak ada DoS, tidak ada uji korban, tidak ada bypass EDR, tidak ada IoT/SCADA/OT.**

## Alur kerja T20 (5 peran)

| Peran | Agent | Tugas |
|---|---|---|
| Recon | A146 | Petakan permukaan Automations: endpoint, dokumentasi publik, scope VDP |
| Analyzer | A147 | Baca hasil recon + JS/endpoint; rumuskan varian hipotesis P-1 yang paling teruji |
| Exploiter | A148 | Rancang + uji paket uji P-1 (HANYA setelah target disetujui A150 + akses Pro diputuskan Cipta) |
| Reporter | A149 | Susun draf laporan framing resmi + bukti request/response + reproduksi |
| Koordinator/Triase & QA | A150 | Pimpin tim, jadwalkan giliran, cek duplikat + validitas sebelum laporan disusun |

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | T20 (A146–A150) | Hipotesis P-1 Perplexity Automations |
| Pemimpin | Muse | Putuskan hipotesis mana yang diuji + laporan mana yang dikirim |
