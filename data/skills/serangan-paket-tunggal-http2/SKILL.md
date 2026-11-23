# Skill: Serangan Paket Tunggal HTTP/2 — Permintaan Paralel dalam Satu Paket TCP untuk Race Condition

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: Bagian 5 "Business Logic & Race Condition Synthesizer" di `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` (HTTP/2 Single-Packet Attack, jawaban AI lain diteruskan Cipta 24 Nov 2026 00:05 WIB). Teknik single-packet (pengiriman paralel dalam satu paket TCP, termasuk varian last-byte sync) memang belum dirinci di skill mana pun — `perburuan-kerentanan-spesifik` hanya memakai konkurensi minimal 2 request biasa. Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai satu race condition terbukti lewat teknik ini dan lolos triase.

## Pemicu (kapan dipakai)

Dipakai saat hipotesis race condition sudah ada (dari `perburuan-kerentanan-spesifik` + permata dari `analisis-mahkota-permata`) pada endpoint kritis — penukaran kupon, transfer dana, voting, pembuatan slot reservasi — dan pengiriman 2 request biasa BELUM berhasil membuktikan race, sehingga diduga jendela balapannya hanya sepersekian milidetik dan butuh ketepatan waktu yang tidak bisa dicapai request berurutan. Dipakai sesudah Gerbang 1 `perburuan-kerentanan-spesifik` (definisi + cara mengenali race condition) dikuasai. Bukan langkah pertama: jangan memakai teknik ini sebelum hipotesis race + permata target tertulis.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menentukan endpoint kritis + hipotesis race yang butuh single-packet |
| Pengerjaan | **A62 Exploit Developer** | Menyusun + menjalankan skrip single-packet (satu paket TCP, jumlah request minimal) |
| Audit | **A60 Security Auditor** | Memeriksa jumlah request, bukti reproduksi, dan pemulihan state sebelum maju ke triase |
| Pemimpin | **Muse** | Menyetujui pemakaian teknik ini per endpoint; memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Definisi race condition + cara mengenali (cek-lalu-tulis) + standar bukti (reproduksi deterministik, 2x dari state bersih)** ada di `perburuan-kerentanan-spesifik` Gerbang 1.2 — skill ini TIDAK mengulang definisi itu; ia hanya menambah TEKNIK PENGIRIMAN presisi waktu yang belum ada di sana.
- **Penentuan aset paling berharga yang diburu** ada di `analisis-mahkota-permata` — endpoint kritis di sini harus berasal dari tabel permata itu.
- **Pacing/rate limit agar tidak terblokir sendiri** ada di `pacing-request-aman` — skill ini memakai batasnya, bukan menulis ulang.
- **Variasi payload sistematis** ada di `rekonstruksi-iterasi-payload` — satu dimensi per putaran tetap berlaku di sini.
- **Validasi temuan + laporan triage-ready** ada di `triase-duplikat` + `laporan-abstrak`.

## Signal

Sinyal bahwa endpoint layak diuji dengan single-packet (bukan request biasa):

| # | Signal | Keterangan |
|---|---|---|
| 1 | **Endpoint kritis dari tabel permata** | Penukaran kupon, transfer dana, voting, pembuatan slot reservasi — operasi yang membaca lalu menulis resource yang sama |
| 2 | **Pola cek-lalu-tulis** | Ada jeda antara "cek" (saldo/kupon/stok/slot masih ada) dan "tulis" (kurangi/tandai terpakai) — dari pengamatan alur sebagai pengguna asli |
| 3 | **Request biasa gagal membuktikan** | 2 request bersamaan biasa sudah dicoba (sesuai `perburuan-kerentanan-spesifik`) dan belum menghasilkan double-use — jendela diduga < 1 ms |
| 4 | **Server mendukung HTTP/2** | Teramati dari respons/negosiasi koneksi (ALPN `h2`) — tanpa HTTP/2, teknik single-packet tidak bisa dipakai apa adanya |
| 5 | **Tidak ada kunci atomik yang terlihat** | Tidak ada token sekali pakai / idempotency key yang ditegakkan server pada endpoint itu |

Endpoint yang tidak cocok dengan signal 1 + 2 = JANGAN diuji dengan teknik ini; endpoint tanpa signal 4 = catat sebagai "tidak bisa single-packet" dan kembali ke request biasa.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus data)** — pembuktian aman dan read-only.
11. **Google AI VRP: payload injeksi DIBLOKIR — Tim 4 analisis format saja, jangan menguji payload injeksi.**
12. **HANYA pada endpoint kritis akun uji sendiri** (kupon/transfer/voting/reservasi milik sendiri) — jangan pernah menyentuh resource pengguna lain.
13. **Jumlah request dibatasi secukupnya untuk membuktikan race, bukan banjir.** Mulai dari 2 request dalam satu paket; tambah SATU per putaran hanya bila 2 belum cukup; MAKSIMAL 5 request per paket tanpa persetujuan Muse. Lebih dari itu = banjir, bukan pembuktian.
14. **Berhenti bila server menunjukkan tanda beban** — respons 429, latensi melonjak tajam, atau error 5xx: hentikan pengujian SEGERA, tunggu, catat, dan jangan ulangi di hari yang sama tanpa persetujuan Muse.
15. **Jangan pernah menguras/mengubah saldo atau slot pengguna lain.** Bila race berhasil mengubah state (mis. kupon terpakai dua kali, saldo terpotong ganda, slot ganda terbuat): SEGERA kembalikan state ke semula bila bisa (batalkan pesanan kedua / kembalikan kupon lewat alur normal akun sendiri), catat perubahan state sebelum/sesudah, dan JANGAN ulangi eksploitasi untuk "memastikan" — reproduksi ulang hanya dari state bersih dengan persetujuan Muse.
16. **Satu endpoint per tugas, satu paket per putaran.** Jangan menguji dua endpoint kritis dalam satu skrip yang sama — hasilnya tidak bisa diatribusikan.

## Probe Steps

### Langkah 1 — Pilih endpoint + tulis hipotesis race

Dari tabel mahkota permata (`analisis-mahkota-permata`), pilih SATU endpoint kritis (kupon/transfer/voting/reservasi). Tulis hipotesis satu kalimat: "Saya menduga endpoint X membaca [saldo/kupon/stok/slot] lalu menulisnya dalam dua langkah terpisah, sehingga N request yang tiba bersamaan bisa memakai resource yang sama N kali." Catat juga bukti bahwa request biasa sudah dicoba dan gagal (signal 3) — bila belum dicoba, coba request biasa dulu di `perburuan-kerentanan-spesifik`, jangan langsung single-packet.

**Standar lulus:** hipotesis tertulis + nomor permata + catatan percobaan request biasa yang gagal.

### Langkah 2 — Verifikasi dukungan HTTP/2 + siapkan skrip

1. Verifikasi server mendukung HTTP/2 (ALPN `h2` pada koneksi TLS target, atau header/respons yang menunjukkan HTTP/2). Bila tidak mendukung = STOP, catat "tidak bisa single-packet", kembali ke request biasa.
2. Susun skrip kecil (Python + pustaka HTTP/2 yang tersedia, mis. `httpx`/`h2` — ambil cara pakai dari dokumentasi resminya, jangan mengarang flag) yang:
   - membuka SATU koneksi HTTP/2 ke target;
   - menyiapkan N request identik (N=2 dulu) ke endpoint kritis, memakai sesi + kredensial akun uji sendiri;
   - mengirim semua frame request dalam SATU paket TCP (single-packet: semua request dilepas bersamaan, tanpa jeda antar-request) — prinsipnya sama dengan teknik last-byte sync: server menerima seluruh request pada saat yang sama, sehingga jendela cek-lalu-tulis tidak sempat menutup di antara request;
   - mencatat timestamp kirim + tiap respons (status, body, waktu) per request.
3. Uji skrip DULU pada endpoint BACA yang aman (mis. GET profil sendiri) untuk memastikan skrip mengirim N request paralel dengan benar — jangan langsung menembak endpoint kritis dengan skrip yang belum teruji.

**Standar lulus:** HTTP/2 terverifikasi + skrip lolos uji kering di endpoint baca (N respons diterima, tanpa error) + N=2 sebagai titik awal.

### Langkah 3 — Tembak endpoint kritis, sekali per putaran

1. Siapkan state bersih akun sendiri (saldo/kupon/slot dalam keadaan awal yang tercatat — foto state sebelum: saldo, status kupon, jumlah slot).
2. Jalankan skrip SATU KALI dengan N=2. Simpan semua respons + state sesudah.
3. Bandingkan: apakah resource yang sama terpakai 2 kali (mis. 2 pesanan berhasil dari 1 saldo, kupon memberi diskon 2 kali, 2 slot terbuat dari 1 jatah)?
   - Ya → lanjut Langkah 4 (pemulihan + reproduksi).
   - Tidak → tambah N SATU per putaran (maks 5) dan ulangi dari state bersih. Bila N=5 tetap gagal = hipotesis GAGAL untuk teknik ini; catat dan berhenti, jangan naikkan N lagi.
4. Patuhi `pacing-request-aman` antar-putaran (jeda, jangan beruntun tanpa jeda).

**Standar lulus per putaran:** state sebelum/sesudah tercatat + semua respons tersimpan + keputusan lanjut/berhenti tertulis. Putaran tanpa catatan state = tidak sah.

### Langkah 4 — Pulihkan state + reproduksi deterministik

1. Bila race berhasil: SEGERA kembalikan state (aturan keras 15) — batalkan hasil kedua lewat alur normal akun sendiri, catat bukti pemulihan (state kembali seperti sebelum).
2. Reproduksi dari state bersih MINIMAL 1 kali pengulangan penuh sesudah pembuktian pertama (total 2 kali berhasil, sesuai standar `perburuan-kerentanan-spesifik`). Sekali berhasil tanpa pengulangan = belum terbukti.
3. Serahkan ke A60 audit → `triase-duplikat` (skor + cek duplikat) → draf laporan (A67) → Cipta setuju → kirim.

**Standar lulus:** 2 kali berhasil dari state bersih + bukti pemulihan state + audit A60.

## Execution Gate

| Gerbang | Syarat lulus | Bila gagal |
|---|---|---|
| G1 — Hipotesis + permata | Hipotesis race tertulis + nomor permata + bukti request biasa sudah dicoba dan gagal | Kembali ke `perburuan-kerentanan-spesifik`; jangan pakai single-packet |
| G2 — HTTP/2 + uji kering | HTTP/2 terverifikasi + skrip lolos uji kering di endpoint baca | STOP — catat "tidak bisa single-packet" |
| G3 — Batas jumlah | N mulai 2, naik 1 per putaran, maks 5 tanpa persetujuan Muse | Hentikan; N > 5 tanpa persetujuan = pelanggaran |
| G4 — Tanda beban | Tidak ada 429 / latensi melonjak / 5xx selama pengujian | HENTIKAN segera; jangan ulangi hari itu tanpa persetujuan Muse |
| G5 — Reproduksi + pemulihan | 2x berhasil dari state bersih + state dipulihkan + audit A60 | Belum terbukti — jangan maju ke triase |

## Alat

| Alat | Cara pakai |
|---|---|
| Akun tes sendiri + canary palsu | Satu-satunya akun dan data yang dipakai; state bersih disiapkan sebelum tiap putaran |
| Skrip single-packet kecil (Python + pustaka HTTP/2, mis. `httpx`/`h2`) | Satu koneksi HTTP/2, N request identik dalam satu paket TCP; ambil cara pakai dari dokumentasi resmi pustaka, jangan mengarang flag |
| Endpoint baca yang aman (GET profil sendiri) | Uji kering skrip sebelum menembak endpoint kritis |
| `pacing-request-aman` | Jeda antar-putaran + batas rate |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + N per putaran + respons + state sebelum/sesudah + pemulihan + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint kritis]
Permata: #[n] dari tabel mahkota permata — [nama aset]
Hipotesis race: [satu kalimat]
HTTP/2: [terverifikasi h2 / TIDAK — kembali ke request biasa]
Percobaan request biasa: [gagal membuktikan — tanggal/catatan]
Putaran single-packet:
  - Putaran 1 (N=2): [hasil — resource terpakai 1x/2x] — [reference ID respons + state]
  - Putaran 2 (N=3): [hasil] — [reference ID]
State sebelum: [saldo/kupon/slot awal] | State sesudah: [saldo/kupon/slot akhir]
Pemulihan state: [dipulihkan — bukti / tidak perlu — race gagal]
Reproduksi: [1x / 2x berhasil dari state bersih / belum]
Tanda beban: [tidak ada / 429/lambat/5xx — pengujian dihentikan]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Available connectors

Tidak ada konektor khusus untuk skill ini. Pengujian memakai akun sendiri di program target, skrip HTTP/2 lokal, dan pencatatan di file log di atas.

## Websites

- Referensi riset Bagian 5: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md`
- Definisi + standar bukti race condition: `~/workspace/tmp/pusat-komando-push/data/skills/perburuan-kerentanan-spesifik/SKILL.md`
- Tabel permata: `~/workspace/tmp/pusat-komando-push/data/skills/analisis-mahkota-permata/SKILL.md`
- Pacing/rate limit: `~/workspace/tmp/pusat-komando-push/data/skills/pacing-request-aman/SKILL.md`

## Alternatives for better results

- Bila server tidak mendukung HTTP/2: kembali ke request biasa di `perburuan-kerentanan-spesifik` (konkurensi minimal 2) — jangan memaksakan single-packet lewat HTTP/1.1.
- Bila single-packet gagal di N=5: hipotesis race untuk endpoint itu GAGAL dengan teknik ini — catat, lalu pertimbangkan apakah celahnya business logic biasa (bukan race) lewat `perburuan-kerentanan-spesifik` Gerbang 1.1.
- Bila endpoint ternyata memakai idempotency key yang ditegakkan server: itu BUKAN race condition — catat sebagai kontrol yang bekerja dan berhenti menguji endpoint itu.

## Batasan yang diketahui

- Teknik ini hanya mempersempit jendela waktu pengiriman; bila server sudah memakai penguncian atomik, tidak ada teknik pengiriman yang bisa membuktikan race — hasil negatif adalah hasil yang sah, bukan kegagalan teknik.
- Skrip HTTP/2 di sini ditulis dari riset, bukan dari satu kasus nyata yang lolos triase — pustaka dan flag wajib diambil dari dokumentasi resmi pustaka yang dipakai, bukan dari ingatan.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome pada agennya — teknik web klasik ini untuk program web/API klasik (huntr dsb.), bukan untuk bounty agen AI.
