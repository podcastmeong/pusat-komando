# Skill: Pola Pikir Penyerang Analitis — Problem Solving & Analytical Thinking sebagai Metode Investigatif

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 4, 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi berikut — di luar itu tidak boleh dipakai:

1. **Muse** (Muse / Meta)
2. **OpenAI Safety** (OpenAI)
3. **0din**
4. **Google AI VRP**
5. **ViKernel**
6. **Perplexity VDP**
7. **Mistral VDP**
8. **Anthropic**
9. **huntr**

Skill ini adalah skill METODE berpikir — bukan skill pengujian. Ia menghasilkan pertanyaan, hipotesis, dan rencana uji; pengujian nyatanya selalu dijalankan lewat skill pengujian yang sudah ada dan selalu tunduk pada scope + aturan masing-masing program. Bila satu program melarang jenis pengujian tertentu, larangan itu menang atas rencana yang dihasilkan skill ini.

## Pemicu

Dipakai di AWAL setiap perburuan, sebelum satu pun permintaan uji dikirim — saat target sudah dipilih dan scope sudah dibaca, tapi belum ada hipotesis yang jelas. Dipakai juga di tengah jalan saat pengujian buntu: semua teknik standar sudah dicoba dan tidak ada temuan, atau hasil uji tidak konsisten dengan yang diharapkan. Dipakai setiap kali ada dugaan bahwa celah bersembunyi bukan di kode yang terlihat, melainkan di ASUMSI yang salah atau JALUR yang terlewat.

Skill ini TIDAK dipakai untuk menggantikan skill pengujian — ia mengorkestrasi pertanyaan pemicu + pemburuan asumsi + enumerasi jalur tersembunyi, lalu menyerahkan hipotesis terbaik ke skill pengujian yang tepat. Tanpa skill ini, pengujian mudah jadi tebakan acak; tanpa skill pengujian, skill ini hanya jadi daftar pertanyaan tanpa bukti.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan pertanyaan pemicu + memburu asumsi + menyusun hipotesis yang bisa diuji |
| Pengerjaan | **A62 Exploit Developer** | Menilai apakah hipotesis bisa dibuktikan secara aman dan read-only; menolak hipotesis yang butuh aksi destruktif |
| Audit | **A60 Security Auditor** | Mengaudit hipotesis + rencana uji sebelum dijalankan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan hipotesis mana yang maju ke pengujian dan kapan perburuan dinyatakan buntu |

## Sudah tercakup (jangan diduplikat)

- **Fondasi kerentanan web/API secara umum** → skill `fondasi-kerentanan-web-api` (skill ini menambah CARA BERPIKIR di atas fondasi itu, bukan mengulang konsepnya).
- **Rumusan hipotesis dari kode** → skill `kopilot-analisis-kode` (skill ini merumuskan hipotesis dari ASUMSI dan JALUR, bukan dari membaca kode baris per baris).
- **Inventarisasi permukaan serangan / endpoint** → skill `pemetaan-permukaan-serangan` (skill ini memakai inventaris itu sebagai bahan pertanyaan, bukan membuatnya ulang).
- **Penemuan API dari dokumentasi dan dari bundle JS** → skill `penemuan-api-swagger` + `perburuan-shadow-api-spa` (skill ini menanyakan jalur mana yang TERLEWAT dari kedua inventaris itu).
- **Pengujian otorisasi antar-akun (BOLA/IDOR)** → skill `access-control-differential-analyst` (skill ini menanyakan asumsi otorisasi apa yang mungkin salah, pengujiannya lewat skill itu).
- **Pengujian kerentanan spesifik (injeksi, CSRF, race condition, dsb.)** → skill pengujian masing-masing (skill ini TIDAK berisi langkah pengujian per kerentanan — ia hanya menunjuk skill mana yang dipakai).
- **Validasi temuan + laporan triage-ready** → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — sembilan program pada `Aturan utama` di atas. Di luar itu jangan dipakai, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Semua hipotesis diuji dengan akun tes milik sendiri dan data canary palsu — tanpa kecuali.
3. **Tanpa data orang lain.** Hipotesis yang pembuktiannya butuh membaca, mengubah, atau memakai data milik pengguna lain DITOLAK di Gerbang 4 — jangan diteruskan ke pengujian.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian terhadap korban sungguhan dilarang total — jangan pernah merumuskan hipotesis yang butuh korban.
5. **Tanpa DoS/DDoS.** Hipotesis yang butuh membanjiri server dengan permintaan DITOLAK — volume uji selalu kecil dan berjeda.
6. **Tanpa payload di permukaan publik.** Rencana uji, halaman PoC, dan bukti hanya di lingkungan terkendali milik sendiri — jangan di-host di tempat umum.
7. **Validasi human-in-the-loop.** AI merumuskan hipotesis, manusia (Muse/A60) yang memutuskan hipotesis mana yang diuji — jangan kirim hasil mentah otomatisasi ke mana pun.
8. **Tanpa laporan tanpa persetujuan Cipta.** Hipotesis dan draf temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibuat, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG merumuskan atau menguji hipotesis yang menghapus, mengubah, atau merusak data (DROP, DELETE, UPDATE, hapus akun, transfer dana nyata). Pembuktian HARUS aman dan read-only sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, hipotesis DITOLAK dan diserahkan ke Muse untuk keputusan.

## Langkah + gerbang

### Gerbang 0 — Cek scope + baca aturan program dulu

1. Baca pasal scope program: target apa yang in-scope, jenis pengujian apa yang diizinkan, dan apa yang dilarang (otomasi, jenis payload, batasan bukti).
2. Catat batasan itu sebagai "pagar" hipotesis: hipotesis apa pun yang melanggar pagar langsung ditolak, tidak peduli seberapa menariknya.
3. **Standar lulus:** pasal scope + larangan program tercatat di log sebelum satu pertanyaan pemicu pun dirumuskan. Tanpa itu = jangan mulai.

### Gerbang 1 — Ajukan tiga pertanyaan pemicu (dan turunannya)

Untuk tiap fitur/endpoint target, ajukan tiga pertanyaan inti — lalu kembangkan masing-masing menjadi pertanyaan turunan yang spesifik:

1. **"Bagaimana sistem ini bisa ditembus?"** — Turunan: alur mana yang paling kompleks (kompleksitas = tempat celah bersembunyi)? Langkah mana yang bisa dilewati, diulang, atau dibalik urutannya? Apa yang terjadi bila satu langkah gagal di tengah jalan?
2. **"Apa asumsi developer yang salah?"** — Turunan: asumsi apa yang dibuat kode ini tentang input, tentang pengguna, tentang layanan lain, tentang waktu/urutan? (Daftar asumsi umum ada di Gerbang 2.)
3. **"Apa jalur akses tersembunyi?"** — Turunan: endpoint, parameter, header, atau peran apa yang tidak terlihat di UI tapi masih aktif? (Enumerasi ada di Gerbang 3.)

Tambahkan tiga pertanyaan pelengkap bila tiga inti belum menghasilkan hipotesis: "Siapa yang dipercaya tanpa verifikasi?" (pengguna, layanan lain, header, token lama); "Apa yang bisa dipalsukan?" (identitas, peran, waktu, asal permintaan); "Di mana state bisa dimanipulasi?" (urutan langkah, nilai yang disimpan client, penghitung/kuota).

**Standar lulus:** tiap fitur target punya minimal 3 pertanyaan tertulis + minimal 1 hipotesis awal yang bisa diuji. Pertanyaan tanpa hipotesis = belum selesai, lanjut ke Gerbang 2.

### Gerbang 2 — Pemburuan asumsi (asumsi keliru = tempat celah lahir)

1. Susun daftar asumsi yang dibuat sistem tentang target, dari pola umum berikut — lalu tandai mana yang berlaku pada target ini:
   - Semua input pengguna aman / sudah divalidasi di client, jadi server tidak perlu memeriksa ulang.
   - Pengguna yang sudah login adalah pengguna yang jujur dan hanya memakai UI resmi.
   - Header, cookie, dan parameter tersembunyi tidak bisa diubah pengguna.
   - Layanan internal / jaringan internal selalu tepercaya, jadi tidak perlu autentikasi antar-layanan.
   - Token/ID yang panjang atau acak tidak bisa ditebak — jadi tidak perlu memeriksa kepemilikan.
   - Urutan langkah alur selalu diikuti (langkah 2 tidak mungkin terjadi sebelum langkah 1).
   - Satu permintaan = satu aksi (tidak ada pengulangan, tidak ada permintaan bersamaan).
   - Data lama / endpoint lama / akun lama sudah tidak aktif, jadi aman diabaikan.
   - Batasan (kuota, harga, peran) yang ditegakkan di UI juga ditegakkan di server.
   - Error / pesan gagal tidak membocorkan apa pun yang berguna.
2. Untuk tiap asumsi yang berlaku, tulis CARA MENGUJINYA dengan aman (akun sendiri, read-only, volume kecil) — dan skill pengujian mana yang dipakai untuk mengujinya.
3. **Standar lulus:** daftar asumsi tertulis dengan tanda berlaku/tidak + cara uji + skill pengujian per asumsi. Asumsi tanpa cara uji = "dugaan mentah", bukan hipotesis — jangan diteruskan.

### Gerbang 3 — Enumerasi jalur tersembunyi

1. Dari inventaris `pemetaan-permukaan-serangan`, `penemuan-api-swagger`, dan `perburuan-shadow-api-spa`, daftar jalur yang TIDAK terlihat di UI: endpoint lama/beta, parameter yang hanya muncul di bundle JS, peran admin/ops, alur debug, dan integrasi pihak ketiga.
2. Untuk tiap jalur, tanyakan: siapa yang boleh memakainya, apa yang terjadi bila akun tes sendiri memakainya, dan asumsi apa yang melindunginya (mis. "tidak ada yang tahu path ini" = asumsi keamanan lewat kerahasiaan — itu asumsi yang lemah).
3. **Standar lulus:** daftar jalur tersembunyi tertulis dengan asumsi pelindung tiap jalur + prioritas (jalur yang dilindungi asumsi lemah didahulukan). Jalur tanpa asumsi pelindung yang jelas = "belum dipahami", bukan "aman".

### Gerbang 4 — Prioritaskan hipotesis, tolak yang melanggar aturan

1. Gabungkan hasil Gerbang 1–3 menjadi daftar hipotesis, masing-masing dengan: asumsi yang diuji, cara uji yang aman, skill pengujian yang dipakai, dan dampak bila terbukti.
2. Terapkan filter keras: TOLAK hipotesis yang butuh data orang lain, korban, aksi destruktif, volume besar, atau pengujian di luar scope — tulis alasan penolakannya di log.
3. Urutkan sisanya: dampak terbesar + cara uji paling aman didahulukan. Kreativitas dan logika lebih berharga daripada kecepatan tools — hipotesis yang cerdas dengan satu permintaan uji yang tepat mengalahkan seribu permintaan acak.
4. **Standar lulus:** daftar hipotesis terprioritasi tertulis + hipotesis yang ditolak tercatat dengan alasannya + hipotesis #1 diserahkan ke skill pengujiannya. Tanpa daftar ini = jangan mulai menguji.

### Gerbang 5 — Serahkan ke skill pengujian, evaluasi hasil, ulangi bila buntu

1. Jalankan hipotesis #1 lewat skill pengujian yang ditunjuk (bukan lewat skill ini) — ikuti gerbang skill itu sampai verdict (terbukti / gagal / belum jelas).
2. Bila TERBUKTI: serahkan ke A61/A68 (`triase-duplikat`) → A60 audit → draf laporan (A67) → Cipta setuju → kirim. Bila GAGAL: catat KENAPA gagal (asumsi ternyata benar? jalur ternyata mati? bukti kurang?) — alasan gagal itu sendiri adalah informasi: ia menutup satu asumsi dan membuka pertanyaan baru.
3. Bila semua hipotesis gagal dan perburuan buntu: kembali ke Gerbang 1 dengan pertanyaan baru yang lahir dari kegagalan tadi (mis. "asumsi X ternyata benar — asumsi apa lagi yang belum diuji?"). Maksimal 2 putaran ulang per target per hari — setelah itu serahkan ke Muse untuk keputusan lanjut atau berhenti.
4. **Standar lulus:** tiap hipotesis punya verdict + alasan tertulis di log; hasil buntu pun tercatat sebagai hasil ("tidak ada hipotesis terbukti pada putaran ini"), bukan sebagai kekosongan.

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar pertanyaan pemicu (Gerbang 1) | Kerangka berpikir tiap fitur — dipakai sebelum tools apa pun dibuka |
| Daftar asumsi umum (Gerbang 2) | Checklist pemburuan asumsi — centang mana yang berlaku pada target |
| Inventaris permukaan serangan + API + shadow | Bahan enumerasi jalur tersembunyi — dari `pemetaan-permukaan-serangan`, `penemuan-api-swagger`, `perburuan-shadow-api-spa` |
| Skill pengujian yang sudah ada | Pelaksana pengujian tiap hipotesis — skill ini hanya menunjuk, tidak menguji sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua pertanyaan, asumsi, jalur, hipotesis, verdict, dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + target + fitur]
Pagar scope: [apa yang diizinkan/dilarang program ini]
Pertanyaan pemicu: [3 pertanyaan inti + turunan per fitur]
Asumsi yang diburu: [asumsi — berlaku/tidak — cara uji — skill pengujian]
Jalur tersembunyi: [jalur — asumsi pelindung — prioritas]
Hipotesis terprioritasi: [#1 ... #n — asumsi — cara uji aman — dampak bila terbukti]
Hipotesis ditolak: [hipotesis — alasan penolakan]
Verdict per hipotesis: [terbukti / gagal — alasan]
Keputusan triase: [maju / ditolak + alasan]
Status: [hipotesis / diuji / terbukti / dilaporkan / ditolak / buntu]
```

## Batasan yang diketahui

- Skill ini hanya sebagus pertanyaan yang diajukan — pertanyaan yang dangkal menghasilkan hipotesis yang dangkal. Bila hipotesis terus gagal, masalahnya biasanya di pertanyaan, bukan di target.
- Asumsi developer tidak selalu bisa dibaca dari luar; sebagian asumsi hanya terlihat setelah pengujian gagal berulang — karena itu Gerbang 5 memerintahkan putaran ulang dari kegagalan, bukan berhenti di kegagalan pertama.
- Skill ini tidak menggantikan keahlian teknis per kerentanan — hipotesis yang bagus tetap butuh skill pengujian yang benar untuk dibuktikan; hipotesis tanpa skill pengujian yang cocok dicatat sebagai "butuh skill baru", bukan dipaksakan dengan skill yang salah.
- Kreativitas tidak boleh menjadi alasan melanggar scope: hipotesis yang paling kreatif sekalipun DITOLAK bila pembuktiannya butuh korban, data orang lain, atau aksi destruktif.
