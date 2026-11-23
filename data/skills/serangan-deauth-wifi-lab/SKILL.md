# Skill: Serangan Deauth Wi-Fi Lab — Uji Ketahanan Jaringan Nirkabel Sendiri

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 112. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: memutuskan klien dari jaringan Wi-Fi LAB SENDIRI untuk membuktikan apakah jaringan itu rentan terhadap serangan deauthentication — dan apakah pertahanan (802.11w / Protected Management Frames) menahannya. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Hanya jaringan Wi-Fi sendiri/lab; tanpa memutuskan klien orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **huntr, Perplexity VDP, Mistral VDP**. Skill ini adalah skill LAB: hasil lab dipakai untuk memahami pola serangan dan menulis laporan hanya bila program mencantumkan aset jaringan nirkabel yang relevan — temuan lab sendiri bukan temuan pada target program kecuali direproduksi pada aset in-scope sesuai pasal scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu menguji ketahanan jaringan Wi-Fi sendiri: apakah klien lab bisa diputus paksa dengan frame deauthentication, apakah klien tersambung kembali otomatis, apakah Protected Management Frames (802.11w) memblokir serangan, dan apakah pemutusan bisa dipakai sebagai langkah awal penangkapan handshake (handshake yang ditangkap HANYA dari jaringan sendiri — lihat `pengujian-wifi-handshake-cracking-lab`). Dipakai di lab Wi-Fi milik sendiri (AP/router milik sendiri + klien milik sendiri, di lokasi yang tidak mengganggu jaringan tetangga). Dipakai SEBELUM mengklaim kerentanan Wi-Fi pada target program — lab membuktikan pola serangannya, target in-scope membuktikan relevansinya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Membangun lab Wi-Fi, mengirim frame deauth ke klien sendiri, merekam hasilnya |
| Pengerjaan | **A54 Penguji Live** | Memantau klien lab (putus/tersambung kembali) dan memverifikasi pemulihan |
| Audit | **A60 Security Auditor** | Memvalidasi bukti lab sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Menangkap handshake Wi-Fi dan menguji kekuatan kata sandi jaringan sendiri → skill `pengujian-wifi-handshake-cracking-lab` (skill ini tentang PEMUTUSAN klien, bukan cracking handshake).
- MITM/ARP spoofing di lab → skill `mitm-arp-spoofing-lab`.
- Uji ketahanan DoS pada layanan sendiri → skill `ketahanan-dos-lab-sendiri` (deauth adalah DoS nirkabel — hanya di lab sendiri, aturan yang sama berlaku).
- Penemuan perangkat dalam satu jaringan → skill `penemuan-perangkat-jaringan`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** AP/router, klien, dan kata sandi Wi-Fi dalam uji ini milik sendiri; kata sandi Wi-Fi lab adalah kata sandi canary.
3. **Tanpa data orang lain.** Tanpa menangkap handshake atau lalu lintas milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR; tanpa memutuskan klien orang lain.** Klien yang diputus adalah perangkat MILIK SENDIRI.
5. **Tanpa DoS/DDoS pada target program.** Frame deauth hanya dikirim di jaringan lab sendiri, ke MAC klien sendiri, dalam durasi singkat yang direncanakan.
6. **Tanpa payload di permukaan publik.** Alat dan konfigurasi lab tidak di-host/dibagikan di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengirim frame deauth ke jaringan yang bukan milik sendiri (Wi-Fi tetangga, kantor, kampus, kafe, atau jaringan program). DILARANG memutuskan klien orang lain — walau hanya "sebentar" atau "untuk menguji". DILARANG memakai deauth untuk menangkap handshake jaringan orang lain. DILARANG membanjiri kanal Wi-Fi bersama dengan frame deauth berdurasi panjang. Setelah uji selesai, hentikan pengiriman frame, pastikan klien lab tersambung kembali normal, dan catat pemulihannya.

## Langkah + gerbang

### Gerbang 0 — Cek scope + bangun lab Wi-Fi terisolasi

1. Baca pasal scope program yang dituju; catat relevansi aset nirkabel. Bangun lab: AP/router milik sendiri dengan SSID lab khusus + minimal satu klien milik sendiri. Pilih kanal dan lokasi yang meminimalkan gangguan ke jaringan lain. Catat BSSID AP lab + MAC klien lab.
2. **Standar lulus:** lab terisolasi (SSID/BSSID/MAC milik sendiri tercatat) dan pasal scope tercatat. Lab belum terisolasi = jangan mulai.

### Gerbang 1 — Baseline: koneksi normal + status 802.11w

1. Sambungkan klien lab ke AP lab. Catat: apakah AP/klien mengaktifkan Protected Management Frames (802.11w), jenis enkripsi (WPA2/WPA3), dan stabilitas koneksi normal. Rekam lalu lintas nirkabel milik sendiri bila perlu.
2. **Standar lulus:** baseline tercatat (802.11w aktif/tidak + enkripsi + koneksi stabil). Tanpa baseline, dampak deauth tidak terukur.

### Gerbang 2 — Kirim frame deauth ke klien sendiri

1. Dari mesin lab (antarmuka nirkabel dalam mode monitor, milik sendiri), kirim frame deauthentication yang ditujukan HANYA ke MAC klien lab, dengan BSSID AP lab sebagai sumber — durasi singkat dan jumlah terbatas sesuai rencana. Amati apakah klien terputus.
2. **Standar lulus:** tercatat apakah klien terputus (ya/tidak) beserta waktu putus. Klien tidak terputus = pertahanan bekerja — catat dan tutup sebagai hasil negatif yang valid.

### Gerbang 3 — Amati pemulihan klien

1. Hentikan pengiriman frame. Amati apakah klien tersambung kembali otomatis, berapa lama, dan apakah perlu intervensi manual. Verifikasi konektivitas normal (klien bisa mengakses layanan lab).
2. **Standar lulus:** waktu pemulihan tercatat + konektivitas normal terverifikasi. Tanpa pemulihan terverifikasi = uji belum selesai.

### Gerbang 4 — Nilai relevansi ke target program

1. Nilai: apakah pola yang terbukti di lab relevan dengan aset in-scope program (mis. jaringan nirkabel target tanpa 802.11w)? Bila ya, rancang reproduksi pada aset in-scope sesuai pasal scope; bila tidak, lab tetap dicatat sebagai pembelajaran. Catat juga apakah AP lab dengan 802.11w aktif berhasil menahan serangan — itu pertahanan yang bekerja.
2. **Standar lulus:** penilaian relevansi tertulis + status 802.11w tercatat sebagai faktor penentu.

### Gerbang 5 — Tulis draf (bila relevan dengan target in-scope)

1. Tulis dampak konkret pada aset in-scope (bukan sekadar "klien bisa diputus di lab"). Serahkan ke A60 audit → Muse → Cipta setuju → kirim.
2. **Standar lulus:** draf mengikuti format output + keputusan triase diputuskan A60, bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab Wi-Fi milik sendiri (AP/router + klien, SSID lab) | Satu-satunya jaringan tempat deauth dikirim |
| Antarmuka nirkabel mode monitor + alat deauth (mis. Aircrack-ng aireplay-ng) | HANYA ke MAC klien lab sendiri, durasi singkat |
| Monitor koneksi klien lab | Mencatat putus / tersambung kembali / waktu pemulihan |
| Kata sandi Wi-Fi canary lab | Satu-satunya kredensial dalam uji ini |
| `~/workspace/catatan/log-bug-bounty.md` | Log lab, baseline, hasil tiap gerbang, bukti, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [huntr / Perplexity VDP / Mistral VDP]
Lab: [SSID/BSSID AP milik sendiri + MAC klien milik sendiri]
Baseline: [802.11w: aktif/tidak | enkripsi: WPA2/WPA3 | koneksi stabil]
Deauth: [frame dikirim ke MAC klien lab — klien terputus: ya/tidak]
Pemulihan: [tersambung kembali otomatis: ya/tidak — waktu ... — konektivitas normal: ya]
Klien lain terganggu: [tidak ada — hanya klien lab sendiri]
Relevansi target in-scope: [aset + pola yang sama — atau "hanya pembelajaran lab"]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program — lab hanya membuktikan pola; relevansi ke aset in-scope harus dibuktikan terpisah.
- AP/klien dengan 802.11w (Protected Management Frames) yang ditegakkan akan menolak frame deauth palsu — hasil "tidak terputus" adalah temuan negatif yang valid.
- Deauth yang berhasil di lab tidak otomatis berarti dampak bisnis pada target — nilai dampak apa adanya, jangan membesar-besarkan.
- Skill ini tidak membahas penangkapan/cracking handshake (lihat `pengujian-wifi-handshake-cracking-lab`) — handshake yang tertangkap selama uji ini HANYA dari jaringan sendiri.
