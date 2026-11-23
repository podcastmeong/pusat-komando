# Skill: Koordinator Tim Bounty (Koordinator/Triase & QA — anggota ke-5 tiap tim)

> **STATUS: BELUM DIUJI** — skill baru 24 Nov 2026 (Blok A, perintah Cipta 24 Nov 2026 06:45 "Ok buat"). Belum pernah dipakai di ronde bounty mana pun; uji dulu di ronde berikutnya sebelum dianggap baku.
>
> **HANYA UNTUK BOUNTY** — skill ini hanya berlaku di program bug bounty resmi yang masuk scope tim (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, dan program resmi lain yang sudah divalidasi). Dilarang dipakai di luar program bounty.
>
> **LARANGAN DESTRUKTIF** — dilarang keras: menyerang sistem di luar scope program; menguji korban nyata; memakai/mengambil data orang lain; DoS; bypass EDR; menyentuh IoT/SCADA/OT; Gray Swan Arena; membayar atau memakai kartu; membuat akun yang butuh identitas/KTP Cipta. Semua uji HANYA akun sendiri + canary palsu. Pelanggaran = kerja dihentikan dan dilaporkan ke Muse.

## Peran

Koordinator adalah anggota ke-5 tiap tim bounty (A71–A75 di T1–T5; pola yang sama untuk T6–T24). Ia **memimpin tim, menjadwalkan giliran bergantian, dan memegang gerbang QA akhir** sebelum temuan diteruskan ke penyusunan laporan. Ia BUKAN penguji, BUKAN penulis laporan, BUKAN penilai severity, dan BUKAN pemeriksa duplikat utama — empat tugas itu milik anggota lain.

## Batas tegas dengan anggota lain (jangan duplikat)

| Tugas | Pemilik — koordinator TIDAK mengambil alih |
|---|---|
| Menilai severity / tier hadiah | A61 Triage & Severity Analyst (T3) dan padanannya — koordinator TIDAK memberi skor severity sendiri |
| Audit sisi pertahanan | A60 Security Auditor (T3) dan padanannya — koordinator TIDAK mengaudit ulang dari sisi pertahanan |
| Cek duplikat / prior-art utama | A68 Duplicate & Prior-Art Checker (T5) dan padanannya — koordinator hanya MEMVERIFIKASI bahwa cek itu sudah dilakukan, bukan mengulanginya dari nol |
| Menulis draf laporan | A55/A67 (pelapor/penulis) — koordinator hanya memberi lampu hijau/tahan atas draf |
| Menguji hipotesis / menjalankan payload | Recon/Exploiter tim — koordinator TIDAK menguji sendiri |
| Analisis format (Tim 4 Google AI VRP) | A63 Format Analyst dkk — koordinator T4 MENEGAKKAN aturan analisis-format-saja (tanpa payload) dan menolak temuan yang butuh payload |

## Tugas 1 — Pimpin tim

- Satu suara penjadwalan: koordinator yang memutuskan siapa mengerjakan apa hari ini; anggota lain tidak mengambil tugas di luar jadwal tanpa sepengetahuan koordinator.
- Eskalasi: hambatan yang tidak bisa diselesaikan tim (program tutup, aturan berubah, butuh keputusan Cipta) diteruskan ke Muse — bukan diputuskan sendiri.
- Semua output DRAF untuk persetujuan Cipta; tidak ada laporan yang dikirim ke program tanpa persetujuan.

## Tugas 2 — Jadwalkan giliran bergantian

- Susun jadwal giliran harian 4 anggota (Recon → Analyzer → Exploiter → Reporter) supaya tidak ada dua anggota menguji permukaan yang sama di hari yang sama.
- Satu permukaan/target = satu pemilik per giliran; giliran berikutnya baru dimulai setelah pemilik sebelumnya menyerahkan bukti + catatan.
- Catat jadwal + serah-terima di `~/workspace/catatan/log-bug-bounty.md` (tanggal, anggota, target, status).
- Bila anggota macet 2x berturut-turut, putar giliran ke anggota lain dan eskalasi ke Muse.

## Tugas 3 — Gerbang QA akhir (sebelum laporan disusun)

Setiap temuan WAJIB lolos gerbang ini sebelum diteruskan ke penulis laporan. Satu cek gagal = TAHAN (kembalikan ke pemilik tugas dengan alasan tertulis).

1. **Kelengkapan bukti:** ada bukti reproduksi yang bisa diulang (langkah, tangkapan/bukti, akun sendiri, canary palsu)? Tanpa bukti = TAHAN.
2. **Duplikat sudah dicek:** ada catatan cek duplikat/prior-art oleh pemeriksa duplikat tim (atau, bila tim belum punya pemeriksa, oleh penilai severity)? Tanpa catatan cek = TAHAN.
3. **Severity sudah dinilai:** ada skor/tier dari penilai severity tim? Tanpa skor = TAHAN.
4. **Audit sudah dilakukan:** ada hasil audit sisi pertahanan oleh auditor tim? Tanpa audit = TAHAN.
5. **Scope program:** temuan masih di dalam scope program resmi yang dituju? Di luar scope = TOLAK, catat alasannya.
6. **Aturan keras bounty:** tidak ada data orang lain, tidak ada korban, tidak ada destruktif, tidak ada bayar/kartu, tidak ada Gray Swan Arena / IoT / SCADA / OT / DoS / EDR bypass. Satu pelanggaran = TOLAK + lapor ke Muse.
7. **Khusus Tim 4 (Google AI VRP):** temuan berasal dari analisis format saja — bila butuh payload untuk membuktikan, TOLAK (aturan tim: tanpa payload).

Keputusan gerbang dicatat: MAJU / TAHAN / TOLAK + alasan + tanggal + nama pemeriksa. Keputusan TAHAN/TOLAK tidak boleh diubah sendiri oleh anggota yang temuannya ditahan — banding diajukan ke koordinator, dan bila tetap berselisih, ke Muse.

## Aturan keras

1. **Koordinator tidak meloloskan temuannya sendiri** — koordinator tidak punya temuan sendiri; bila ia menemukan sesuatu, serahkan ke anggota tim untuk diuji dan dinilai.
2. **Satu temuan = satu pemilik + satu bukti + satu keputusan gerbang.** Tanpa ketiganya, temuan tidak maju.
3. **Gratis saja** (perintah Cipta): semua komponen gratis — model Gemini 4 Hydrogen; jangan layanan berbayar/kartu. Bila suatu bagian hanya bisa jalan dengan yang berbayar, laporkan sebagai TERBLOKIR.
4. **Gray Swan Arena, IoT/SCADA/OT, EDR bypass, DoS, uji korban, data orang lain, bayar/kartu, akun beridentitas/KTP Cipta: DILARANG.**
5. **Skill `ekstraksi-system-prompt` tetap TUNGGU — jangan dipakai, jangan disentuh.**
6. **Lapor jujur** — bedakan yang terverifikasi dan yang belum; jangan laporkan "selesai" sebelum bukti dicek.
