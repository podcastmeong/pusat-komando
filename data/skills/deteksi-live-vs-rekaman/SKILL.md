# Skill: Deteksi Live-vs-Rekaman — Bedakan Uji Langsung dari Rekaman Sebelum Klaim Apa Pun

> **BELUM DIUJI — dibangun dari kebutuhan Tim T19 ViKernel S4 (24 Nov 2026), bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bounty resmi (ViKernel, Muse, OpenAI Safety, 0din, Google AI VRP, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar program resmi = tidak boleh dipakai.

## Larangan destruktif

DILARANG: merusak sistem, menyerang korban, memakai data orang lain, memalsukan bukti, mengklaim hasil rekaman sebagai bukti live, memakai canary yang meniru data nyata orang lain, dan segala bentuk DoS / EDR bypass / IoT-SCADA-OT. Uji HANYA akun sendiri + canary PALSU milik sendiri. Tidak ada eksfiltrasi data nyata — canary hanya token/nilai palsu yang unik dan hanya milik sendiri.

## Aturan keras — hasil rekaman BUKAN bukti

1. **Hasil rekaman dilabeli `REKAMAN — BUKAN BUKTI`.** Rekaman (tangkapan layar/video/log lama) hanya dipakai sebagai petunjuk arah uji, TIDAK PERNAH sebagai bukti temuan.
2. **ALLOW (temuan dinyatakan lolos) HANYA bila direproduksi ≥2x di sesi live berbeda.** Satu sesi live saja tidak cukup; dua sesi live terpisah dengan bukti masing-masing adalah syarat minimum.
3. **Deteksi live-vs-recorded WAJIB dilakukan SEBELUM uji apa pun** — sebelum Exploiter menjalankan payload, Analyzer/Koordinator memastikan target benar-benar live.
4. **Canary HANYA palsu.** Canary adalah token/tautan/file/nilai palsu unik milik sendiri; canary yang menyentuh data nyata orang lain = pelanggaran, temuan dibatalkan.

## Sinyal D1–D12 (checklist — semua WAJIB diperiksa, catat hasil tiap sinyal)

| Sinyal | Yang diperiksa | Live bila… |
|---|---|---|
| D1 | Cap waktu server | Timestamp respons sesuai jam sesi saat ini, bukan jam lama |
| D2 | Nonce/token sesi unik | Setiap sesi memakai nonce/token baru yang tidak bisa dipakai ulang |
| D3 | Interaksi dua arah real-time | Target merespons input baru yang dikirim DALAM sesi, bukan jawaban beku |
| D4 | Respons terhadap input tak terduga | Target bereaksi terhadap nilai acak/nonce yang baru dibuat di sesi itu |
| D5 | Perubahan state bertahan | Perubahan yang dibuat di sesi 1 masih terlihat di sesi 2 |
| D6 | Jejak audit/log | Ada entri log/audit dengan timestamp sesi yang bisa diverifikasi |
| D7 | Canary disentuh di sesi live | Canary palsu milik sendiri tersentuh DALAM sesi live, tercatat waktunya |
| D8 | Konsistensi urutan kejadian | Urutan request → respons → efek samping runtut dan tidak melompat |
| D9 | Sinyal jaringan/latensi | Latensi dan perilaku jaringan konsisten dengan sesi interaktif, bukan pemutaran file |
| D10 | Reproduksi di sesi kedua berbeda | Hasil yang sama muncul lagi di sesi live lain (syarat ALLOW, lihat aturan 2) |
| D11 | Bukti tak bisa dibuat dari rekaman statis | Bukti memuat nilai sesi-spesifik (nonce/canary baru) yang tidak ada di rekaman lama |
| D12 | Konfirmasi Koordinator/Triase | Koordinator memeriksa D1–D11 dan menandatangani verdict live sebelum laporan disusun |

**Verdict:** LIVE bila D1–D4 + D7 + D11 terpenuhi dan D10 menyusul di sesi kedua; REKAMAN bila salah satu dari D1–D4/D11 gagal — labeli `REKAMAN — BUKAN BUKTI` dan JANGAN lanjut ke laporan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A141 Pengintai Live Detection (T19)** | Periksa D1–D12 pada target sebelum uji; pasang canary palsu |
| Pengerjaan | **A142 Pemeta & Penyaring S4 (T19)** | Nilai hasil D1–D12, kelompokkan mana yang live vs rekaman |
| Pengerjaan | **A143 Penguji Kernel Breach (T19)** | Hanya uji target berverdict LIVE; ulangi di sesi kedua untuk D10 |
| Audit | **A145 Koordinator T19** | Konfirmasi D12; batalkan temuan bila verdict REKAMAN; A145 tidak meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan target mana yang layak diuji setelah verdict live |

## Sudah tercakup (jangan diduplikat)

- Pembuktian dampak dengan canary → skill `canary-pembuktian-dampak` (MEMAKAI canary dari skill itu; skill ini hanya menilai live-vs-rekaman).
- Uji di browser live → skill `uji-live-browser`.
- Triase duplikat + validitas → skill `triase-duplikat`.
- Audit trifecta (data privat + konten tak tepercaya + saluran keluar) → skill `audit-trifecta-mematikan`.
