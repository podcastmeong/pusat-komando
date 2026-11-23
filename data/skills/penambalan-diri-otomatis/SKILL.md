# Skill: Penambalan Diri Otomatis — Tutup Titik yang Sudah Dilaporkan, Gali Permukaan Baru yang Lebih Dalam

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` Bagian 4 (Automated Self-Patching / Hunting Berkelanjutan). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu kasus nyata di mana patch lokal membuat agen berhenti mengulang titik yang sama dan menemukan permukaan baru, dicatat di log.

## Pemicu (kapan dipakai)

Dipakai SETIAP KALI sebuah kerentanan sudah berstatus VERIFIED (lolos `skeptic-false-positive-eliminator`), sudah lolos triase (`triase-duplikat`), draf laporannya sudah disusun (`laporan-poc-otomatis`), **dan laporannya sudah DISETUJUI Cipta dan DIKIRIM** ke program. Satu temuan terkirim = satu kali lewat skill ini, sebelum hunting dilanjutkan ke target/fitur yang sama. Dipakai hanya untuk target berskala besar, codebase terbuka, atau program VDP berkelanjutan — tempat satu titik lemah yang sama bisa menyedot waktu berhari-hari bila tidak ditutup secara sengaja. Untuk target kecil / satu fitur / program sekali jalan, skill ini TIDAK dipakai — langsung pindah target saja.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Membuat patch lokal sementara (Mode A) atau menutup titik di daftar hunting lokal (Mode B); mencatat patch di log |
| Pengerjaan | **A53 Recon Program** | Memetakan ulang attack surface sesudah patch dan memilih permukaan baru yang lebih dalam |
| Audit | **A60 Security Auditor** | Memeriksa patch hanya menyentuh salinan lokal, bukti asli tetap utuh, dan salinan murni tersimpan sebelum patch |
| Pemimpin | **Muse** | Memutuskan patch boleh diterapkan; meninjau log patch pada laporan malam |

## Sudah tercakup (jangan diduplikat)

- **Mencegah pengulangan pengujian yang gagal** ada di `koreksi-diri-manajemen-memori` — skill itu mencatat pengujian GAGAL agar tidak diulang. Skill ini kebalikannya: menutup titik yang BERHASIL dan sudah dilaporkan, supaya agen tidak terpaku mengulang titik yang sudah dibayar.
- **Verifikasi temuan + skor + draf laporan** ada di `skeptic-false-positive-eliminator`, `triase-duplikat`, `laporan-poc-otomatis` — skill ini baru jalan SESUDAH ketiganya selesai DAN laporan terkirim. Bukan pengganti verifikasi atau laporan.
- **Saran perbaikan untuk vendor** ada di `laporan-poc-otomatis` Gerbang 3 — saran itu ditulis UNTUK triager/vendor di dalam laporan. Patch di skill ini adalah perbaikan SEMENTARA pada SALINAN LOKAL milik agen sendiri, bukan saran untuk vendor dan bukan perbaikan pada target.
- **Mencari rantai lanjutan dari temuan rendah** ada di `eskalasi-dampak-otomatis` — skill itu memperdalam SATU temuan sebelum dilaporkan. Skill ini bekerja SESUDAH laporan terkirim dan memaksa pindah ke permukaan BARU, bukan memperdalam titik yang sama.
- **Pemetaan attack surface** ada di `pemetaan-permukaan-serangan` — skill ini MEMAKAI pemetaan itu ulang sesudah patch (Gerbang 4), bukan menggantinya.
- Alur sesudah skill ini: patch lokal tercatat → permukaan baru dipetakan (`pemetaan-permukaan-serangan`) → hunting lanjut di permukaan baru → temuan baru masuk kembali ke alur `skeptic-false-positive-eliminator` → `triase-duplikat` → `laporan-poc-otomatis` → persetujuan Cipta → kirim → skill ini lagi.

## Aturan keras

1. **Patch HANYA pada SALINAN LOKAL di workspace sendiri** (lingkungan kerja lokal agen). JANGAN PERNAH mengubah kode, konfigurasi, atau data pada target, repositori target, server, atau upstream.
2. **Penghapusan fungsi rentan hanya pada salinan lokal** untuk keperluan pengujian lanjutan — bukan pada target, bukan sebagai perbaikan resmi, dan bukan sebagai klaim bahwa celah sudah diperbaiki.
3. **Patch lokal TIDAK BOLEH dipakai sebagai bukti temuan.** Bukti tetap dari pengujian asli SEBELUM patch (pasangan Request/Response + reference ID dari `skeptic-false-positive-eliminator`). Pengujian yang dilakukan sesudah patch tidak boleh dikutip sebagai bukti temuan yang sudah dilaporkan.
4. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan diuji, jangan dipatch.
5. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
6. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
7. **Larang aksi destruktif pada target (DROP, DELETE, hapus data).** Pembuktian aman dan read-only — larangan ini berlaku juga sesudah patch; patch lokal bukan alasan untuk menguji lebih kasar.
8. **Patch lokal TIDAK BOLEH dikirim ke upstream** — jangan commit, push, atau buat pull request berisi patch ini, kecuali Cipta menyetujui secara eksplisit sebagai pekerjaan terpisah. Patch ini alat kerja internal, bukan kontribusi kode.
9. **Validasi human-in-the-loop.** Patch diterapkan hanya sesudah laporan terkirim (bukan sebelum), dan log patch ditinjau Muse pada laporan malam. Bila Muse menemukan patch menyentuh sesuatu di luar salinan lokal, patch dibatalkan (rollback) dan dicatat sebagai pelanggaran.
10. **Tanpa laporan tanpa persetujuan Cipta.** Patch tidak menggantikan persetujuan; temuan baru dari permukaan baru tetap butuh persetujuan Cipta sebelum dikirim.
11. **Patuhi larangan otomasi program:** huntr "Humans only" (tanpa otomasi pengiriman); **Gray Swan dilewati total** (jangan disentuh).
12. **Google AI VRP: payload injeksi DIBLOKIR** — Tim 4 analisis format saja, tanpa payload; patch lokal tidak mengubah aturan itu.
13. **Simpan salinan murni sebelum patch.** Patch tidak boleh menghancurkan kemampuan memverifikasi ulang temuan asli — salinan kode/data sebelum patch harus tersimpan terpisah (lihat Gerbang 1).
14. **Jangan menyimpan rahasia di log patch** — token, kata sandi, API key, dan data sensitif TIDAK PERNAH ditulis di log (sama seperti `koreksi-diri-manajemen-memori`).

## Signal — kapan patch dibuat, kapan tidak

| Signal | Keputusan |
|---|---|
| Laporan temuan sudah DIKIRIM (disetujui Cipta) + target masih luas / VDP berkelanjutan / codebase terbuka tersedia lokal | **PATCH** — lanjut ke Probe Steps |
| Laporan baru draf / belum disetujui / belum dikirim | **JANGAN PATCH** — bukti belum beku; patch bisa merusak reproduksi bila triager minta bukti tambahan |
| Target kecil, satu fitur, program sekali jalan | **JANGAN PATCH** — langsung pindah target; biaya patch lebih besar dari manfaatnya |
| Tidak ada salinan lokal kode (target remote tertutup) | **Mode B** — tutup titik di daftar hunting lokal, bukan patch kode (lihat Gerbang 2) |
| Temuan DITOLAK triase / duplikat / false positive | **JANGAN PATCH** — titik itu bukan temuan valid; catat saja di `koreksi-diri-manajemen-memori` |
| Patch akan menyentuh data/kode di luar workspace sendiri | **DILARANG** — batalkan, laporkan ke Muse |

## Probe Steps — urutan kerja

### Gerbang 1 — Bekukan bukti + simpan salinan murni (SEBELUM patch apa pun)

1. Pastikan status laporan = TERKIRIM (ada tanggal kirim + reference ID laporan di `~/workspace/catatan/log-bug-bounty.md`). Bila belum terkirim → BERHENTI, kembali ke `laporan-poc-otomatis`.
2. Bekukan bukti asli: pasangan Request/Response sesi bersih + reference ID bukti (mis. `FP-...`) sudah tersimpan di luar memori LLM dan TIDAK akan diubah lagi. Tulis di log: "Bukti beku: <reference ID>".
3. Simpan salinan murni (pristine snapshot) dari salinan lokal yang akan dipatch — salinan lengkap fungsi/file yang rentan SEBELUM diubah, di folder terpisah yang jelas namanya (mis. `worktree/<target>/pristine-<temuan-singkat>/`), atau `git stash` / commit lokal terpisah di repo LOKAL SENDIRI (bukan repo target). Salinan murni ini untuk verifikasi ulang bila triager minta bukti tambahan.
4. **Standar lulus:** ada (a) bukti beku dengan reference ID, (b) salinan murni yang bisa dikembalikan. Satu dari keduanya hilang = JANGAN PATCH.

### Gerbang 2 — Terapkan patch lokal (pilih SATU mode)

**Mode A — ada salinan lokal codebase (open source / huntr / VDP dengan kode tersedia):**

1. Di SALINAN LOKAL SAJA, terapkan patch sementara yang paling sederhana yang menutup titik itu, pilih salah satu:
   - Perbaiki validasi yang hilang (mis. tambah cek kepemilikan objek di fungsi yang IDOR; tambah allowlist di fungsi yang SSRF); atau
   - Hapus/nonaktifkan fungsi rentan di salinan lokal (stub yang mengembalikan 403) bila perbaikannya tidak sepele — catat bahwa ini stub sementara, bukan perbaikan benar.
2. Patch ditulis sebagai diff kecil + komentar `// PATCH LOKAL SEMENTARA — <temuan-singkat> — <tanggal> — BUKAN PERBAIKAN RESMI` di tiap tempat yang diubah, supaya tidak tertukar dengan kode asli.
3. Uji bahwa patch bekerja DI LOKAL SAJA: jalankan ulang payload/permintaan yang dulu berhasil — sekarang harus GAGAL (ditolak 403/404 atau fungsi tidak ada). Catat hasil uji lokal ini — ini bukti patch menutup titik, BUKAN bukti temuan.
4. **Standar lulus:** payload lama gagal di salinan lokal yang dipatch + diff tercatat + salinan murni utuh. Bila payload lama masih berhasil → patch tidak menutup titik; perbaiki patch atau pilih stub, jangan lanjut dengan patch setengah jalan.

**Mode B — target remote tertutup (tidak ada kode lokal untuk dipatch):**

1. Tidak ada kode yang diubah. Sebagai gantinya, tutup titik itu di daftar hunting lokal: tambahkan endpoint/fitur itu ke daftar pengecualian (exclusion list) di `~/workspace/catatan/memori-pengujian-bounty.md` dengan status `TERTUTUP — sudah dilaporkan <tanggal> — jangan uji ulang kecuali triager minta bukti tambahan`.
2. Tandai juga di catatan pemetaan permukaan (`pemetaan-permukaan-serangan`) bahwa titik itu sudah tertutup, supaya recon berikutnya tidak memasukkannya lagi sebagai permukaan terbuka.
3. **Standar lulus:** entri pengecualian tertulis dengan tanggal + reference ID laporan. Tanpa entri tertulis = titik dianggap masih terbuka.

### Gerbang 3 — Catat patch di log (apa + kenapa)

1. Tulis entri patch di `~/workspace/catatan/log-bug-bounty.md` (format di bawah): temuan apa, mode apa (A/B), file/fungsi apa yang diubah ATAU entri pengecualian apa yang dibuat, KENAPA patch itu dipilih (bukan perbaikan lain), diff/ringkasan perubahan, dan hasil uji lokal.
2. Catat juga di `koreksi-diri-manajemen-memori` (memori pengujian): titik ini `TERTUTUP`, supaya Gerbang 1 skill itu mencegah pengujian ulang oleh sub-agen lain.
3. **Standar lulus:** tiap patch punya entri log lengkap dengan KENAPA + hasil uji lokal. Patch tanpa entri log = patch liar — rollback dan catat sebagai pelanggaran prosedur.

### Gerbang 4 — Petakan ulang permukaan + pilih permukaan baru yang lebih dalam

1. Jalankan ulang `pemetaan-permukaan-serangan` pada target yang sama DENGAN titik yang sudah dipatch/ditutup dikeluarkan dari daftar permukaan terbuka.
2. Pilih permukaan baru dengan prioritas: (a) fitur yang berbagi kode/komponen dengan titik yang baru ditutup (celah sejenis sering berulang di sebelahnya); (b) endpoint/fitur yang belum pernah diuji; (c) permukaan yang lebih dalam (butuh 2+ langkah, alur multi-langkah, interaksi antar-fitur).
3. Tulis rencana hunting berikutnya: permukaan baru + hipotesis awal + sub-agen yang mengerjakannya. Serahkan ke alur normal (`skeptic-false-positive-eliminator` untuk temuan baru, dst.).
4. **Standar lulus:** ada rencana hunting tertulis untuk permukaan baru + titik lama tidak ada lagi di daftar permukaan terbuka. Bila tidak ada permukaan baru yang tersisa → target dinyatakan HABIS untuk ronde ini; pindah target/program, catat di log.

## Execution Gate (verifikasi deterministik sebelum hunting dilanjutkan)

Sebelum hunting di permukaan baru dimulai, A60 memeriksa SEKALI:

- [ ] Laporan temuan lama benar TERKIRIM (tanggal + reference ID ada di log) — bukan baru draf.
- [ ] Bukti asli beku dan TIDAK BERUBAH sesudah patch (bandingkan reference ID + isi file bukti sebelum/sesudah patch — harus identik).
- [ ] Salinan murni tersimpan dan bisa dikembalikan (uji rollback: kembalikan salinan murni ke salinan kerja sementara, pastikan payload lama berhasil lagi di salinan murni itu — ini membuktikan salinan murni memang keadaan rentan yang asli).
- [ ] Patch hanya menyentuh salinan lokal (diff hanya berisi file di workspace sendiri; tidak ada perubahan pada repo target, server, atau upstream).
- [ ] Entri log patch lengkap (apa + kenapa + hasil uji lokal).
- [ ] Titik lama tidak ada di daftar permukaan terbuka yang baru.

**Satu kotak gagal = hunting BARU belum boleh dimulai.** Perbaiki kotak yang gagal dulu (rollback patch bila perlu), baru lanjut. Pelanggaran aturan 1, 2, atau 8 (patch menyentuh target/upstream) = hentikan semua pekerjaan pada target itu dan laporkan ke Muse hari itu juga.

## Rollback — cara membatalkan patch

1. Hapus perubahan patch dari salinan kerja (kembalikan dari salinan murni di Gerbang 1) — salinan kerja kembali ke keadaan rentan yang asli.
2. Hapus entri `TERTUTUP` di memori pengujian bila rollback karena patch ternyata salah (tulis alasan rollback di log).
3. Rollback WAJIB dilakukan bila: triager meminta bukti tambahan/reproduksi ulang; patch ternyata menutup permukaan yang salah; Muse memerintahkan; atau patch terbukti menyentuh sesuatu di luar salinan lokal.
4. **Standar lulus rollback:** payload lama berhasil lagi di salinan yang sudah di-rollback + entri rollback tercatat di log.

## Alat

| Alat | Cara pakai |
|---|---|
| Salinan lokal codebase (worktree di workspace sendiri) | Satu-satunya kode yang boleh dipatch (Mode A); beri nama folder yang jelas + label patch lokal |
| `git diff` / `git stash` (repo LOKAL SENDIRI saja) | Mencatat diff patch + menyimpan salinan murni; JANGAN pernah push ke repo target/upstream |
| `~/workspace/catatan/log-bug-bounty.md` | Log patch (Gerbang 3) + rencana permukaan baru (Gerbang 4) + entri rollback |
| `~/workspace/catatan/memori-pengujian-bounty.md` | Status `TERTUTUP` per titik (Mode B + Gerbang 3); dibaca Gerbang 1 `koreksi-diri-manajemen-memori` |
| Bukti HTTP di luar memori LLM (reference ID `FP-...`) | Bukti beku temuan asli — tidak diubah sesudah patch |
| `pemetaan-permukaan-serangan` | Dipakai ulang di Gerbang 4 untuk memetakan permukaan baru |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Patch lokal: <nama temuan singkat> | Program: <nama> | Laporan terkirim: <tanggal> | Reference ID bukti beku: <FP-...>
  - Mode: [A — patch kode lokal / B — tutup di daftar hunting lokal]
  - Yang diubah: [file/fungsi + diff ringkas / entri pengecualian]
  - Kenapa patch ini: [alasan memilih perbaikan/stub/pengecualian ini]
  - Uji lokal: [payload lama di salinan dipatch → GAGAL (status ...) / di salinan murni → BERHASIL]
  - Salinan murni: [path folder / git stash — bisa rollback: ya/tidak]
  - Permukaan baru: [fitur/endpoint yang dipilih + hipotesis awal + sub-agen]
  - Status: [patch aktif / di-rollback + alasan]
```

## Batasan yang diketahui

- Patch lokal menutup titik di LINGKUNGAN KERJA AGEN, bukan di target — target tetap rentan sampai vendor memperbaiki; jangan pernah mengklaim celah "sudah diperbaiki" ke siapa pun.
- Mode B (tutup di daftar) hanya sekuat disiplin tim membaca daftar itu — satu sub-agen yang tidak membaca memori pengujian akan menguji ulang titik yang sama; Muse memeriksa kelengkapan memori tiap laporan malam.
- Patch yang terlalu kasar (stub fungsi besar) bisa menyembunyikan permukaan di sekitarnya — bila permukaan baru ternyata bergantung pada fungsi yang di-stub, rollback stub itu dan ganti dengan patch validasi yang lebih sempit.
- Skill ini hanya untuk hunting berkelanjutan; jangan dipakai untuk menutup temuan yang belum dilaporkan dengan alasan "sudah dipatch lokal" — temuan yang belum dilaporkan tetap harus dilaporkan dulu.
