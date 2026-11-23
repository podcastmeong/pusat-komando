# Skill: Analisis Lalu Lintas Wireshark — Membaca paket jaringan untuk menemukan informasi bocor

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 2. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: lab sendiri / lalu lintas sendiri; tanpa menyadap jaringan orang lain.

## Pemicu (kapan dipakai)

Dipakai saat perlu memeriksa lalu lintas jaringan MILIK SENDIRI (lab, perangkat sendiri, sesi akun sendiri) untuk menemukan informasi yang bocor: kredensial, token, atau data plaintext yang terkirim tanpa enkripsi. Dipakai juga untuk memahami alur komunikasi aplikasi target in-scope dari sisi klien sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemetaan jaringan dan model OSI → skill `pemetaan-jaringan-osi-tcpip` (No. 3) dan `analisis-websocket-grpc`.
- Pengujian TLS/spoofing email → skill `perburuan-tls-dns-email-spoofing` (skill ini hanya MEMBACA lalu lintas sendiri, bukan menyerang TLS orang lain).
- Validasi temuan + laporan → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Hanya lalu lintas yang dihasilkan perangkat/sesi milik sendiri.** DILARANG menangkap lalu lintas jaringan orang lain, jaringan bersama yang bukan milik sendiri, atau sesi pengguna lain — itu penyadapan.
12. **Kredensial/token yang terlihat di lalu lintas sendiri TIDAK BOLEH dipakai ulang di luar PoC** dan tidak boleh dicatat utuh di log — catat jenis dan lokasinya saja, lalu putar (rotate) kredensial itu.

## Langkah + gerbang

### Gerbang 0 — Cek scope + legalitas penangkapan

1. Pastikan penangkapan hanya pada antarmuka/perangkat milik sendiri atau lab sendiri, dan program mengizinkan analisis lalu lintas klien sendiri. Bila program melarang, berhenti.
2. **Standar lulus:** sumber lalu lintas (perangkat/lab sendiri) tercatat. Tanpa itu = jangan menangkap paket.

### Gerbang 1 — Tangkap lalu lintas sesi sendiri

1. Jalankan Wireshark/tcpdump pada perangkat sendiri saat memakai aplikasi target in-scope dengan akun sendiri. Simpan tangkapan (pcap) di lingkungan terkendali milik sendiri.
2. **Standar lulus:** file tangkapan tersimpan + sesi yang ditangkap tercatat (aplikasi, akun sendiri, waktu). Tangkapan tanpa konteks sesi = tidak bisa dipakai sebagai bukti.

### Gerbang 2 — Saring dan baca paket

1. Saring berdasarkan protokol dan host target in-scope (mis. filter tampilan Wireshark per protokol/host). Periksa: apakah ada kredensial, token, atau data sensitif yang terkirim plaintext (HTTP tanpa TLS, header Authorization, cookie sesi, parameter sensitif di URL)?
2. **Standar lulus:** tiap temuan dicatat dengan protokol + arah + jenis data yang bocor (bukan nilai utuhnya). Tidak ada plaintext sensitif = catat "bersih pada sesi ini" dan tutup.

### Gerbang 3 — Bedakan bocor nyata vs noise

1. Konfirmasi: apakah data itu benar-benar dikirim aplikasi target (bukan layanan latar perangkat sendiri)? Ulangi penangkapan sekali lagi pada sesi baru; bila bocor terulang, lanjut.
2. **Standar lulus:** kebocoran teramati pada 2 sesi berbeda. Satu tangkapan saja = belum terbukti.

### Gerbang 4 — Nilai dampak + tulis draf

1. Tulis data apa yang bocor, siapa yang bisa melihatnya (jaringan yang sama? perantara?), dan langkah reproduksi. Serahkan ke A60 untuk audit, lalu ke Muse/Cipta.
2. **Standar lulus:** dampak ditulis konkret (jenis data + siapa yang bisa mengintip), draf mengikuti format output, dan status triase diputuskan A60.

## Alat

| Alat | Cara pakai |
|---|---|
| Wireshark | Membaca dan menyaring paket (filter tampilan per protokol/host) — hanya pada lalu lintas sendiri |
| tcpdump | Penangkapan baris perintah di lab/perangkat sendiri |
| Akun tes sendiri + perangkat sendiri | Satu-satunya sumber lalu lintas yang ditangkap |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Lalu lintas diperiksa: [perangkat/lab sendiri + sesi akun sendiri]
Kebocoran ditemukan: [jenis data + protokol + arah — tanpa nilai utuh]
Terulang: [ya/tidak — 2 sesi]
Scope guard dipatuhi: [ya — Scope guard: lab sendiri / lalu lintas sendiri; tanpa menyadap jaringan orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Lalu lintas terenkripsi (TLS) tidak bisa dibaca isinya tanpa kunci — skill ini hanya membuktikan kebocoran plaintext; jangan mencoba mendekripsi lalu lintas orang lain.
- Banyak aplikasi memakai pinning atau enkripsi tambahan; ketiadaan temuan pada satu sesi bukan bukti aplikasi aman secara umum.
