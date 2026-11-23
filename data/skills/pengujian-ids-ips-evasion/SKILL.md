# Skill: Pengujian IDS/IPS & Evasion — Firewall sebagai Pintu Gerbang, IDS/IPS sebagai CCTV yang Diuji dan Diakali Konfigurasinya

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 2, 24 Nov 2026 (Firewall & IDS/IPS: pengujian dan evasion konfigurasi keamanan jaringan). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk 9 program bounty resmi: Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, dan huntr. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Pengujian IDS/IPS dan firewall HANYA pada lab/jaringan SENDIRI — sensor, aturan, dan firewall milik sendiri yang dipasang di lab sendiri. Tanpa mengakali IDS/IPS milik orang lain, tanpa menguji evasion terhadap target program di luar scope, dan tanpa memakai evasion untuk menyembunyikan serangan terhadap sistem orang lain.

## Pemicu

Dipakai saat ada IDS/IPS atau firewall di lab sendiri yang perlu diuji ketajaman deteksinya: apakah aturan deteksi benar-benar menangkap lalu lintas uji yang sudah diketahui berbahaya, apakah ada celah evasion (lalu lintas berbahaya yang lolos tanpa alert), dan apakah aturan firewall benar-benar menegakkan kebijakan yang tertulis. Analoginya: firewall adalah pintu gerbang (menentukan siapa boleh masuk/keluar), IDS/IPS adalah CCTV (melihat dan merekam apa yang lewat, IPS sekaligus bisa memblokir). Ethical hacker menguji keduanya: apakah gerbangnya benar-benar terkunci, dan apakah CCTV-nya benar-benar melihat. Dipakai SETELAH sensor dan aturan lab sendiri terpasang dan baseline-nya diketahui — skill ini menguji KONFIGURASI deteksi, bukan memasang sensor dari nol.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis deteksi (aturan mana yang seharusnya menangkap lalu lintas apa) + membaca aturan sensor |
| Pengerjaan | **A62 Exploit Developer** | Menjalankan lalu lintas uji terhadap sensor sendiri, mendokumentasikan alert yang muncul/tidak muncul |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep kerentanan web/API dan WAF secara umum → skill `fondasi-kerentanan-web-api` (WAF hanya disinggung sebagai pengubah respons; skill ini menguji IDS/IPS dan firewall jaringan secara khusus).
- Pemetaan jaringan dan permukaan serangan → skill `pemetaan-jaringan-osi-tcpip` + `pemetaan-permukaan-serangan` (inventarisasi, bukan pengujian deteksi).
- Pengujian konfigurasi switching/routing internal → skill `routing-switching-pentesting-internal` (jalur paket, bukan deteksi/aturan IDS/IPS).
- Enumerasi aset cloud → skill `enumerasi-aset-cloud` (bukan sensor jaringan lab sendiri).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya lab/jaringan SENDIRI.** Sensor, aturan IDS/IPS, dan firewall yang diuji adalah milik sendiri di lab sendiri. Tanpa mengakali IDS/IPS milik orang lain atau target program di luar scope — evasion terhadap sensor orang lain = DILARANG.
3. **Hanya akun sendiri + canary palsu.** Lalu lintas uji hanya berasal dari host uji sendiri menuju target uji sendiri; tanpa data orang lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau host yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri sensor atau target dengan lalu lintas — tiap varian evasion dikirim dalam volume kecil dengan jeda, dan berhenti segera bila sensor/target menunjukkan beban abnormal.
6. **Tanpa payload di permukaan publik.** Aturan deteksi, log sensor, dan varian evasion yang berhasil jangan dipublikasikan.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai evasion untuk menyembunyikan serangan nyata terhadap sistem orang lain, DILARANG menonaktifkan atau melemahkan sensor/firewall milik orang lain, DILARANG menghapus atau mengubah log deteksi. Di lab sendiri pun, perubahan aturan hanya untuk keperluan tuning yang didokumentasikan — dan bila satu-satunya cara membuktikan adalah menyerang sistem di luar lab, BERHENTI dan serahkan ke Muse.

## Yang dicari (definisi singkat)

- **Aturan deteksi yang tidak menangkap:** lalu lintas uji yang polanya sudah diketahui (mis. pola serangan klasik yang aturannya diklaim ada) lewat tanpa alert sama sekali — sensor buta terhadap pola itu.
- **Evasion yang berhasil:** varian lalu lintas uji yang sama isinya tetapi bentuknya diubah (fragmentasi, pengkodean, segmentasi, pengaturan waktu) sehingga lolos dari aturan yang seharusnya menangkap bentuk aslinya.
- **Firewall yang longgar:** aturan firewall mengizinkan lalu lintas yang kebijakannya melarang — port yang seharusnya tertutup ternyata terbuka, atau egress yang seharusnya diblokir ternyata lolos (mis. host uji bisa keluar ke layanan yang dilarang kebijakan).
- **Alert yang tidak bisa ditindaklanjuti:** alert muncul tetapi tanpa konteks yang cukup (tanpa alamat sumber/tujuan, tanpa aturan yang memicunya) sehingga tidak bisa dipakai untuk respons — temuan kualitas tuning, bukan celah kritis.
- **Bukan temuan:** lalu lintas jinak yang tidak menghasilkan alert (itu sensor BEKERJA dengan benar); aturan yang sengaja dimatikan di lab untuk keperluan pengujian lain (buktikan dulu status aturannya sebelum mengklaim celah); dan evasion terhadap sensor yang memang tidak dirancang mendeteksi pola itu (mis. sensor berbasis signature tidak bisa diharapkan menangkap serangan zero-day yang belum ada signaturenya).

## Langkah + gerbang

### Gerbang 0 — Cek scope + kenali sensor dan aturannya dulu

1. Baca pasal scope program: apakah pengujian keamanan jaringan ini diizinkan, dan pada aset apa? Untuk pengujian evasion, yang diuji adalah sensor/firewall LAB SENDIRI — catat itu eksplisit di log beserta programnya.
2. Kumpulkan aturan yang berlaku: daftar aturan IDS/IPS yang aktif di sensor sendiri, kebijakan firewall tertulis (port/layanan mana yang diizinkan/dilarang, arah ingress/egress), dan mode sensor (IDS/deteksi saja atau IPS/mem blokir).
3. **Standar lulus:** scope + daftar aturan aktif + mode sensor tercatat di log sebelum satu paket uji pun dikirim. Tanpa daftar aturan = jangan mulai (tidak ada pembanding "seharusnya tertangkap").

### Gerbang 1 — Tetapkan baseline deteksi

1. Kirim lalu lintas JINAK dari host uji sendiri ke target uji sendiri (mis. permintaan normal ke layanan lab) dan catat: tidak ada alert — ini baseline negatif.
2. Kirim lalu lintas UJI yang polanya sudah diketahui dan aturannya diklaim ada (satu pola per uji, volume kecil) dan catat: alert muncul dengan nama aturan yang benar, atau tidak muncul.
3. **Standar lulus:** baseline jinak (tanpa alert) + minimal satu pola uji yang alertnya TERCATAT dengan nama aturan dan waktunya. Bila pola yang aturannya diklaim ada ternyata tidak menghasilkan alert = temuan potensial Gerbang 1, catat dan lanjutkan untuk memastikan bukan kesalahan konfigurasi pengiriman.

### Gerbang 2 — Uji tiap aturan satu per satu

1. Untuk tiap aturan deteksi yang relevan, kirim SATU varian lalu lintas uji yang seharusnya memicunya, lalu periksa log sensor: alert muncul atau tidak, nama aturannya benar atau salah, dan apakah IPS memblokir (bila modenya IPS).
2. Ulangi tiap uji 2x dengan jeda — alert yang hanya muncul sekali dari dua percobaan dicatat sebagai "tidak konsisten", bukan "terbukti".
3. **Standar lulus:** tiap aturan tercatat "menangkap / tidak menangkap / tidak konsisten" beserta bukti log sensor. Aturan yang tidak menangkap = temuan potensial; semua menangkap = deteksi BEKERJA, tutup dengan buktinya.

### Gerbang 3 — Uji evasion (bentuk diubah, isi sama)

1. Ambil SATU pola uji yang terbukti tertangkap di Gerbang 2, lalu ubah BENTUKNYA tanpa mengubah isinya — satu teknik per putaran: fragmentasi paket, pengkodean ulang, segmentasi aliran, perubahan urutan/penundaan antar-bagian, atau perubahan kapitalisasi/pemisah pada protokol teks. Kirim varian itu ke target uji sendiri dan periksa apakah alert tetap muncul.
2. Bila satu varian lolos tanpa alert, ULANGI 2x untuk memastikan bukan noise, lalu catat teknik mana yang meloloskan dan aturan mana yang seharusnya menangkap.
3. **Standar lulus:** tiap teknik tercatat "tetap tertangkap / lolos (terulang 2x)" beserta aturan yang dilewati. Varian yang lolos sekali tanpa pengulangan = belum terbukti. Catatan: yang diuji di sini adalah METODE evasion terhadap sensor sendiri — jangan menulis payload serangan siap pakai di log; cukup pola bentuknya (mis. "fragmentasi menjadi 2 bagian") dan hasil deteksinya.

### Gerbang 4 — Uji aturan firewall (gerbang + egress)

1. Uji ingress: dari host uji sendiri, coba jangkau port/layanan di target uji sendiri yang kebijakannya melarang — satu port per uji. Port yang berhasil dijangkau padahal dilarang = temuan potensial.
2. Uji egress: dari target uji sendiri, coba keluar ke layanan yang kebijakannya melarang (mis. layanan luar yang dilarang) dan catat apakah koneksi lolos atau diblokir.
3. **Standar lulus:** tiap port/layanan yang diuji tercatat "diizinkan/diblokir" + bunyi kebijakan yang dilanggar (atau dipatuhi). Tanpa kebijakan pembanding = belum terbukti, jangan klaim.

### Gerbang 5 — Nilai tuning: false positive dan kualitas alert

1. Periksa alert yang muncul selama pengujian: apakah ada alert palsu dari lalu lintas jinak (Gerbang 1)? Apakah tiap alert membawa konteks yang cukup (aturan, sumber, tujuan, waktu) untuk ditindaklanjuti?
2. Tulis rekomendasi tuning: aturan mana yang perlu diperketat, dilonggarkan, atau dilengkapi konteksnya — sebagai rekomendasi, bukan sebagai perubahan yang langsung diterapkan ke sensor orang lain.
3. **Standar lulus:** daftar false positive (bila ada) + penilaian kualitas alert tertulis. Temuan tuning tanpa dampak keamanan yang jelas dinilai apa adanya — jangan dibesar-besarkan menjadi temuan kritis.

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal: pola/aturan yang dilewati + teknik evasion yang berhasil (bentuknya, bukan payload siap pakai) + log sensor yang menunjukkan ketiadaan alert + kebijakan firewall yang dilanggar. BERHENTI di situ — jangan memakai evasion yang berhasil untuk menyerang sistem lain.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (lalu lintas uji + log sensor persis + hasil persis) + keputusan triase tercatat. Tanpa bukti log sensor = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Sensor IDS/IPS lab sendiri (mis. Suricata/Snort/Zeek di lab sendiri) | Sumber log alert; baca aturannya yang aktif dan mode (IDS/IPS) |
| Firewall lab sendiri | Baca kebijakan/aturan yang berlaku; uji ingress + egress dari host uji sendiri |
| tcpdump / Wireshark di lab sendiri | Rekam lalu lintas uji dan verifikasi bentuk paket yang dikirim |
| Host uji + target uji sendiri | Satu-satunya asal dan tujuan lalu lintas uji |
| `~/workspace/catatan/log-bug-bounty.md` | Log scope → aturan → baseline → hasil tiap gerbang → keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + sensor/firewall lab sendiri + versi aturan]
Kutipan scope: [teks aturan program — pengujian hanya pada lab sendiri]
Aturan aktif: [aturan IDS/IPS yang diuji + mode IDS/IPS + kebijakan firewall]
Baseline: [jinak: tanpa alert — pola uji yang tertangkap: nama aturan + waktu]
Gerbang aturan: [aturan — menangkap/tidak/tidak konsisten + bukti log]
Gerbang evasion: [teknik bentuk — tetap tertangkap/lolos 2x — aturan yang dilewati]
Gerbang firewall: [port/layanan — diizinkan/diblokir — kebijakan yang dilanggar/dipatuhi]
Tuning: [false positive — kualitas alert — rekomendasi]
Dampak: [pola apa yang lolos dari deteksi + apa yang bisa lewat tanpa terlihat]
Yang TIDAK dilakukan: [tanpa sensor orang lain, tanpa payload siap pakai di log, tanpa serang sistem lain]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Hasil evasion sangat bergantung pada versi aturan dan mode sensor — catat versi aturan dan mode (IDS vs IPS) agar temuan bisa direproduksi; aturan yang diperbarui besok bisa menutup celah yang ditemukan hari ini.
- Sensor berbasis signature tidak dirancang menangkap pola yang belum ada signaturenya — jangan klaim "sensor buta" untuk pola yang memang di luar cakupan signature.
- Pengujian ini mengukur konfigurasi deteksi di lab sendiri, bukan keamanan target program — temuan hanya maju ke triase bila program secara eksplisit menerima temuan konfigurasi jaringan/semacamnya, atau bila temuan itu berupa kelemahan aturan pada aset in-scope yang tertulis.
- Evasion yang berhasil di lab sendiri TIDAK BOLEH dipakai untuk menyembunyikan pengujian terhadap sistem lain — itu penyalahgunaan, bukan temuan (aturan keras 2 dan 10).
