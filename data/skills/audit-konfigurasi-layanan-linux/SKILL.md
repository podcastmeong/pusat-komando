# Skill: Audit Konfigurasi Layanan Linux — HTTP, SSH, FTP: Konfigurasi Salah adalah Celah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 2, 24 Nov 2026 (Audit konfigurasi layanan Linux — HTTP, SSH, FTP). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk 9 program bounty resmi: Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, dan huntr. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Audit konfigurasi HANYA pada sistem/lab SENDIRI atau aset in-scope eksplisit — tanpa membaca atau mengubah konfigurasi layanan orang lain, dan tanpa mengubah satu baris pun konfigurasi pada sistem yang bukan milik sendiri.

## Pemicu

Dipakai saat aset Linux in-scope menjalankan layanan HTTP, SSH, atau FTP dan ada dugaan konfigurasinya salah: layanan terekspos dengan pengaturan default yang tidak aman, autentikasi yang lemah, banner yang membocorkan versi, atau izin file konfigurasi yang terlalu longgar. Prinsipnya sederhana: konfigurasi salah = celah. Layanan yang kodenya aman pun bisa bobol bila file konfigurasinya mengizinkan login root, menonaktifkan autentikasi kunci, membiarkan direktori bisa dijelajahi, atau membocorkan versi persisnya. Dipakai SETELAH layanan dan port-nya diinventarisasi — skill ini mengaudit ISI konfigurasi layanan, bukan menemukan layanan dari luar.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis konfigurasi (pengaturan mana yang diduga salah) + membaca file konfigurasi |
| Pengerjaan | **A62 Exploit Developer** | Menguji dampak konfigurasi dari luar (banner, autentikasi, akses direktori) dengan akun uji sendiri |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Manajemen pengguna, izin file, sistem file, dan proses Linux secara umum → skill fondasi No. 36/38 (bukan skill ini — skill ini mengaudit file konfigurasi LAYANAN HTTP/SSH/FTP, bukan akun, izin umum, atau proses).
- Konsep kerentanan web/API secara umum → skill `fondasi-kerentanan-web-api` (konsep celah aplikasi, bukan audit baris-per-baris file konfigurasi layanan).
- Pemetaan jaringan dan permukaan serangan → skill `pemetaan-jaringan-osi-tcpip` + `pemetaan-permukaan-serangan` (inventarisasi layanan, bukan audit konfigurasinya).
- Audit konfigurasi keamanan Windows/endpoint → skill `audit-konfigurasi-keamanan-windows` (platform berbeda — jangan dicampur).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya sistem/lab SENDIRI atau aset in-scope eksplisit.** Tanpa membaca atau mengubah konfigurasi layanan orang lain — konfigurasi SSH/HTTP/FTP sistem lain = DILARANG disentuh.
3. **Hanya akun sendiri + canary palsu.** Pengujian autentikasi hanya dengan akun uji milik sendiri; tanpa data orang lain, tanpa mencoba kredensial orang lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan dengan permintaan — uji autentikasi dibatasi hitungan kecil dengan jeda, dan berhenti segera bila layanan menunjukkan beban abnormal.
6. **Tanpa payload di permukaan publik.** Isi file konfigurasi, banner versi, dan temuan jangan dipublikasikan.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengubah file konfigurasi layanan apa pun (tanpa mengubah `sshd_config`, tanpa mengubah konfigurasi web/FTP, tanpa mengubah izin file), DILARANG me-restart layanan orang lain, DILARANG mengunci akun dengan percobaan login berulang. Audit ini READ-ONLY: baca konfigurasi yang boleh dibaca + uji perilaku dari luar dengan akun sendiri. Bila satu-satunya cara membuktikan adalah mengubah konfigurasi — BERHENTI dan serahkan ke Muse.

## Yang dicari (definisi singkat)

- **SSH yang longgar:** login root diizinkan, autentikasi kata sandi tanpa batas percobaan, protokol/algoritma usang yang masih aktif, autentikasi kunci tidak diwajibkan padahal kebijakan mewajibkannya, atau port forwarding yang tidak perlu.
- **HTTP yang membocorkan:** banner/server header menampilkan nama dan versi persis, direktori bisa dijelajahi (directory listing aktif), file sensitif bisa diakses lewat web (file konfigurasi, cadangan, `.git`), header keamanan tidak ada, atau TLS usang/sertifikat tidak valid.
- **FTP yang terbuka:** login anonim diizinkan, direktori bisa ditulis anonim, autentikasi polos tanpa enkripsi padahal data sensitif lewat, atau banner membocorkan versi.
- **Izin file konfigurasi yang salah:** file konfigurasi layanan atau kunci privat bisa dibaca/ditulis oleh pengguna yang tidak seharusnya (mis. kunci host SSH bisa dibaca semua pengguna).
- **Bukan temuan:** pengaturan yang memang disengaja dan terdokumentasi (mis. login anonim FTP pada server unduhan publik yang memang dirancang begitu — buktikan dulu kebijakannya); banner versi pada layanan yang memang sengaja menampilkan versi dan tidak ada celah yang diketahui pada versi itu; dan pengaturan default yang sudah diperketat oleh hardening standar.

## Langkah + gerbang

### Gerbang 0 — Cek scope + inventarisasi layanan dulu

1. Baca pasal scope program: apakah aset Linux ini tertulis in-scope? Tulis kutipan scope-nya ke log. Bila tidak tertulis = BERHENTI.
2. Inventarisasi layanan pada sistem sendiri: layanan apa yang berjalan (HTTP/SSH/FTP), port mana yang mendengarkan, dan versi paketnya. Catat dari dalam sistem sendiri, bukan dari pemindaian luar.
3. **Standar lulus:** kutipan scope + daftar layanan (nama + port + versi paket) tercatat di log sebelum satu file konfigurasi pun dibaca. Tanpa itu = jangan mulai.

### Gerbang 1 — Baca file konfigurasi (read-only)

1. Baca file konfigurasi tiap layanan yang boleh dibaca (konfigurasi daemon SSH, konfigurasi server web, konfigurasi daemon FTP) beserta file include-nya — catat tiap pengaturan yang menyimpang dari praktik aman: login root, autentikasi kata sandi, protokol usang, listing direktori, akses anonim, dan pengaturan TLS.
2. Periksa izin file konfigurasi dan kunci (siapa yang bisa membaca/menulis) serta kepemilikan filenya.
3. **Standar lulus:** tiap pengaturan yang dicurigai tercatat persis (nama pengaturan + nilainya + file sumbernya). Pengaturan yang "kelihatan salah" tanpa nilai persis dan sumber file = belum terbukti, jangan klaim.

### Gerbang 2 — Uji banner dan pengungkapan versi dari luar

1. Dari host uji sendiri, sambungkan ke tiap layanan dan catat banner/header yang dikembalikan: apakah nama dan versi persis dibocorkan, dan apakah versi itu memiliki celah yang diketahui dan terdokumentasi publik?
2. Bandingkan banner dengan file konfigurasi (Gerbang 1): apakah pengaturan penyembunyian banner benar-benar bekerja, atau banner tetap bocor walau sudah dimatikan di konfigurasi?
3. **Standar lulus:** banner persis tercatat + hasil perbandingan dengan konfigurasi. Banner yang hanya menampilkan nama layanan tanpa versi = BUKAN temuan; versi yang dibocorkan tapi tidak punya celah yang diketahui = temuan rendah, nilai apa adanya.

### Gerbang 3 — Uji autentikasi dengan akun sendiri

1. Uji metode autentikasi yang dikonfigurasi: coba login dengan akun uji sendiri memakai metode yang seharusnya ditolak (mis. kata sandi bila kebijakan mewajibkan kunci, atau login root bila seharusnya dilarang) — hitungan kecil, dengan jeda, dan hanya akun sendiri.
2. Periksa perlindungan terhadap tebakan berulang: apakah ada batas percobaan atau penundaan setelah gagal berulang, dan apakah akun uji terkunci setelah sejumlah kecil percobaan yang gagal.
3. **Standar lulus:** tiap metode tercatat "diterima/ditolak" + ada/tidaknya perlindungan tebakan berulang. Login yang berhasil padahal kebijakan melarang = temuan potensial; semua ditolak = autentikasi BEKERJA, catat sebagai bukti negatif.

### Gerbang 4 — Uji akses file dan direktori (HTTP/FTP)

1. Untuk HTTP: dari host uji sendiri, coba akses jalur yang seharusnya tidak bisa diakses — daftar direktori, file cadangan, file konfigurasi, dan direktori tersembunyi — satu jalur per uji, hanya pada layanan sendiri.
2. Untuk FTP: periksa apakah login anonim diizinkan dan apakah direktori anonim bisa ditulis (uji tulis HANYA dengan file canary bernama jelas milik sendiri, lalu hapus kembali dan catat penghapusannya).
3. **Standar lulus:** tiap jalur tercatat "bisa/tidak bisa diakses" + isi yang terlihat (atau tidak). Akses yang berhasil ke file sensitif = temuan potensial; semua ditolak = AMAN, tutup dengan buktinya.

### Gerbang 5 — Uji TLS dan header keamanan (HTTP)

1. Periksa konfigurasi TLS: versi protokol yang diizinkan, cipher yang diizinkan, dan status sertifikat (valid, kedaluwarsa, nama tidak cocok).
2. Periksa header keamanan pada respons layanan sendiri: apakah header yang diwajibkan kebijakan ada atau tidak.
3. **Standar lulus:** versi TLS/cipher + status sertifikat + daftar header tercatat. TLS usang yang masih diterima = temuan potensial; semua sudah modern = AMAN.

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal: pengaturan yang salah (nama + nilai + file sumber) + perilaku yang teramati dari luar (banner/autentikasi/akses) + kebijakan yang dilanggar. BERHENTI di situ — jangan mengeksploitasi konfigurasi yang salah untuk masuk lebih dalam, jangan membaca data pengguna lain.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (pengaturan + uji persis + hasil persis) + keputusan triase tercatat. Tanpa pasangan "pengaturan + perilaku teramati" = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Akses baca ke sistem/lab sendiri | Baca file konfigurasi layanan + izin file + versi paket; read-only, tanpa mengubah apa pun |
| curl / klien HTTP dari host uji sendiri | Baca banner/header, uji akses jalur, periksa header keamanan dan TLS |
| Klien SSH/FTP dari host uji sendiri | Uji banner + metode autentikasi dengan akun uji sendiri (hitungan kecil, berjeda) |
| Pemeriksa TLS (mis. openssl s_client) | Periksa versi TLS, cipher, dan status sertifikat layanan sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log scope → layanan → pengaturan → hasil tiap gerbang → keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + sistem Linux in-scope + layanan yang diaudit]
Kutipan scope: [teks aturan program yang mengizinkan aset ini]
Layanan: [HTTP — port + versi | SSH — port + versi | FTP — port + versi]
Gerbang konfigurasi: [pengaturan — nilai — file sumber]
Gerbang banner: [banner persis — versi bocor/tidak — celah diketahui/tidak]
Gerbang autentikasi: [metode — diterima/ditolak — perlindungan tebakan: ada/tidak]
Gerbang akses file: [jalur — bisa/tidak diakses — file canary dihapus: ya/tidak]
Gerbang TLS/header: [versi TLS — cipher — sertifikat — header yang hilang]
Dampak: [pengaturan salah apa + perilaku apa yang dimungkinkan + kebijakan yang dilanggar]
Yang TIDAK dilakukan: [tanpa ubah konfigurasi, tanpa kredensial orang lain, tanpa baca data orang lain]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Audit konfigurasi hanya sekuat akses bacanya — bila file konfigurasi tidak bisa dibaca akun uji, yang tersisa hanya pengujian perilaku dari luar; nyatakan batas itu di log, jangan mengklaim isi konfigurasi yang tidak dibaca.
- Pengaturan default berbeda antar distribusi dan versi paket — catat distribusi dan versi paket agar temuan bisa direproduksi; "default" di satu distribusi belum tentu "default" di distribusi lain.
- Banner versi saja bukan bukti eksploitasi — versi yang bocor baru menjadi temuan bila ada celah yang diketahui pada versi itu, atau bila kebijakan secara eksplisit melarang pengungkapan versi.
- Pengujian autentikasi yang berulang bisa mengunci akun — batasi percobaan, beri jeda, dan hanya pakai akun uji sendiri (aturan keras 5 dan 10).
