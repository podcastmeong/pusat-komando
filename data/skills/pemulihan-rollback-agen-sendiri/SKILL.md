# Skill: Pemulihan & Rollback Agen Sendiri — Uji Apakah Aksi Tak Diinginkan Bisa Dibatalkan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 116. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: menguji pada akun SENDIRI apakah aksi agen yang tidak diinginkan bisa dipulihkan/dibatalkan (rollback) — dan apakah jejak (audit log) aksi itu lengkap. Bila aksi tak diinginkan TIDAK bisa dibatalkan atau jejaknya hilang, itulah dampak yang dibuktikan. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Akun/sistem sendiri; tanpa merusak data nyata.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Anthropic**. Catatan program: Google AI VRP secara eksplisit mengecualikan prompt injection langsung, jailbreak, halusinasi, dan system-prompt-leak — untuk G-VRP, bingkai temuan sebagai dampak aksi tanpa izin yang tidak bisa dipulihkan. Perplexity VDP: jangan memakai kata "prompt injection" / "hallucination" / "model safety" dalam laporan.

## Pemicu (kapan dipakai)

Dipakai SETELAH sebuah aksi agen yang tidak diinginkan terbukti pada akun sendiri (oleh `sabotase-pembuktian-dampak`, `pemicu-terjadwal-agen-sendiri`, atau `perilaku-fail-open-agen`): apakah aksi itu bisa dibatalkan, apakah ada tombol/fitur undo, apakah data yang diubah bisa dikembalikan ke nilai semula, dan apakah jejak aksi itu tercatat lengkap di log/riwayat sehingga pemilik bisa mengetahui apa yang terjadi. Dipakai juga saat merancang PoC: pemulihan adalah bagian dari pembuktian dampak — aksi yang tidak bisa dipulihkan bernilai lebih tinggi daripada aksi yang mudah dibatalkan, dan itu harus diukur, bukan diasumsikan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56 Red Team** | Merancang skenario aksi tak diinginkan + rencana pemulihan pada akun sendiri |
| Pengerjaan | **A54 Penguji Live** | Menjalankan aksi canary, mencoba rollback, memeriksa jejak/log |
| Audit | **A60 Security Auditor** | Memvalidasi bukti pemulihan/kegagalan sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pembuktian dampak ujung-ke-ujung → skill `sabotase-pembuktian-dampak` (skill ini menguji FASE SETELAH aksi: pemulihan).
- Merancang dan memasang canary → skill `canary-pembuktian-dampak`.
- Pemicu terjadwal → skill `pemicu-terjadwal-agen-sendiri`; fail-open → skill `perilaku-fail-open-agen` (pemicu aksi yang dipulihkan).
- Ketahanan backup sendiri → skill `ketahanan-backup-sendiri` (pemulihan dari backup sistem, bukan rollback aksi agen).
- Kondisi luar biasa / gagal rollback → skill `kondisi-luar-biasa`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Anthropic untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Aksi yang diuji dan dipulihkan hanya pada akun/sistem milik sendiri; data yang diubah adalah data canary.
3. **Tanpa data orang lain.** Tanpa mengubah, menghapus, atau memulihkan data milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Jangan pernah menguji aksi tak diinginkan terhadap korban atau akun orang lain.
5. **Tanpa DoS/DDoS pada target program.** Uji pemulihan dilakukan satu aksi per uji, volume kecil.
6. **Tanpa payload di permukaan publik.** Skenario dan data uji hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim pemulihan/kegagalan diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menguji pemulihan dengan aksi destruktif yang tidak bisa dipulihkan (hapus permanen data nyata, kirim ke orang lain, transfer dana). Aksi yang diuji HARUS reversibel dan pada milik sendiri — dan SEBELUM aksi dijalankan, backup/snapshot state milik sendiri WAJIB sudah dibuat agar pemulihan selalu mungkin dari sisi penguji. Bila satu-satunya aksi yang tersedia bersifat permanen, JANGAN jalankan aksi itu — buktikan lewat aksi reversibel yang setara, atau serahkan ke Muse. Setelah uji selesai, state milik sendiri WAJIB kembali ke nilai semula (lewat rollback produk atau lewat backup penguji) dan pengembaliannya dicatat.

## Langkah + gerbang

### Gerbang 0 — Cek scope + pilih aksi canary yang reversibel

1. Baca pasal scope program. Pilih SATU aksi agen yang tidak diinginkan untuk diuji pemulihannya — aksi reversibel pada milik sendiri (mis. ubah nilai preferensi menjadi nilai canary, buat item canary, ubah pengaturan milik sendiri). Buat BACKUP/snapshot state milik sendiri sebelum aksi.
2. **Standar lulus:** aksi terpilih reversibel + backup/snapshot terverifikasi + pasal scope tercatat. Tanpa backup = jangan mulai.

### Gerbang 1 — Jalankan aksi canary + catat baseline dan jejak

1. Jalankan aksi canary (sendiri, atau biarkan agen menjalankannya lewat skenario dari skill pemicu). Catat: nilai sebelum dan sesudah, waktu aksi, dan APAKAH aksi itu tercatat di log/riwayat/audit trail produk (isi jejak persis).
2. **Standar lulus:** perubahan tercatat + jejak tercatat (ada/tidak + isinya). Tanpa catatan jejak, kelengkapan audit tidak terukur.

### Gerbang 2 — Coba rollback lewat fitur produk

1. Cari dan coba mekanisme pemulihan yang disediakan produk: tombol undo, riwayat versi, fitur pulihkan, atau pengembalian manual lewat antarmuka. Catat: apakah ada, apakah berhasil, berapa lama, dan apakah state kembali persis ke nilai semula.
2. **Standar lulus:** hasil tiap mekanisme tercatat (ada/tidak + berhasil/gagal + waktu). Bila tidak ada mekanisme sama sekali, itu hasil yang valid — catat "tidak ada".

### Gerbang 3 — Coba rollback lewat backup penguji (bila produk gagal)

1. Bila rollback produk gagal atau tidak ada, pulihkan state dari backup/snapshot Gerbang 0. Catat apakah pemulihan dari backup berhasil penuh atau sebagian (ada nilai yang tidak kembali?).
2. **Standar lulus:** state akhir tercatat (kembali persis / kembali sebagian / tidak kembali) + cara pemulihannya. State tidak kembali ke semula = uji belum selesai sampai dicatat dan ditangani.

### Gerbang 4 — Nilai kelengkapan jejak + dampak

1. Nilai dua hal: (a) KETIDAKBALIKAN — apakah ada bagian aksi yang tidak bisa dibatalkan lewat cara apa pun? (b) JEJAK — apakah log/riwayat mencatat aksi itu lengkap (apa, kapan, oleh siapa/apa)? Tulis dampak: apa yang hilang/rusak permanen, dan apa yang tidak bisa diketahui pemilik karena jejak tidak lengkap.
2. **Standar lulus:** penilaian ketidakbalikan + kelengkapan jejak tertulis apa adanya. Jangan membesar-besarkan: aksi yang mudah dibatalkan = dampak rendah, catat begitu.

### Gerbang 5 — Tulis draf

1. Tulis dampak konkret: aksi + hasil rollback + kelengkapan jejak + langkah reproduksi. Serahkan ke A60 audit → Muse → Cipta setuju → kirim.
2. **Standar lulus:** draf mengikuti format output + keputusan triase diputuskan A60, bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun/sistem sendiri | Satu-satunya tempat aksi dan pemulihan diuji |
| Canary (nilai/file/item palsu unik) | Target aksi — lihat `canary-pembuktian-dampak` |
| Backup/snapshot state milik sendiri | Jaring pengaman sebelum aksi; dipakai bila rollback produk gagal |
| Log/riwayat/audit trail produk | Diperiksa kelengkapan jejak aksi |
| `~/workspace/catatan/log-bug-bounty.md` | Log aksi, rollback, jejak, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [Muse / OpenAI Safety / 0din / Google AI VRP / ViKernel / Anthropic]
Aksi canary: [aksi persis pada akun sendiri — reversibel]
Backup sebelum aksi: [ya — terverifikasi]
Jejak aksi: [tercatat lengkap / sebagian / tidak ada — isi jejak]
Rollback produk: [ada — berhasil/gagal, waktu ... / tidak ada]
Rollback lewat backup: [berhasil penuh / sebagian / tidak perlu]
State akhir: [kembali persis ke semula / sebagian / tidak kembali — detail]
Bagian tak bisa dibatalkan: [tidak ada / ... — detail]
Dampak: [apa yang hilang permanen + apa yang tak terlacak]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Aksi yang mudah dibatalkan lewat undo = dampak rendah — nilai apa adanya, jangan membesar-besarkan.
- Jejak yang lengkap di satu tampilan (mis. riwayat) belum tentu lengkap di semua tempat — periksa log, riwayat, dan notifikasi bila tersedia.
- Pemulihan dari backup penguji BUKAN pengganti rollback produk: bila produk tidak punya rollback, itu tetap kelemahan walau penguji bisa memulihkan sendiri.
- Skill ini tidak membahas ketahanan backup sistem (lihat `ketahanan-backup-sendiri`) atau pembuktian dampak awal (lihat `sabotase-pembuktian-dampak`).
