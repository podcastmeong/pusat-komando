# Skill: Ketahanan DoS Lab Sendiri — Uji Layanan Sendiri Bertahan dan Pulih dari Beban

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 111. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: menguji apakah layanan SENDIRI di lab bertahan dan pulih saat dibebani — sebagai uji ketahanan, bukan serangan. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain.

## Peringatan tegas — DoS tidak dibayar, jangan uji DoS pada target program

**DoS tidak dibayar di program bounty.** Posisi tim: jangan uji DoS pada target program sebelum membaca pasal scope — dan umumnya pasal scope MELARANG pengujian DoS/DDoS. Skill ini HANYA untuk layanan SENDIRI di lab. Uji ketahanan di lab dipakai untuk memahami perilaku layanan sendiri (batas beban, pemulihan, rate-limit) dan untuk menulis laporan hanya bila program secara eksplisit meminta/mengizinkan pengujian ketahanan pada aset tertentu — yang hampir tidak pernah terjadi. Bila pasal scope melarang DoS, JANGAN uji pada target, apa pun alasannya.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **Lab sendiri** — skill ini adalah skill lab murni; tidak ada program yang dilayani langsung dengan pengujian DoS pada targetnya. Hasil lab dipakai sebagai pembelajaran dan rujukan ketahanan, bukan sebagai temuan pada target program.

## Pemicu (kapan dipakai)

Dipakai saat perlu mengetahui batas ketahanan layanan SENDIRI di lab: berapa beban yang membuat layanan melambat/tidak responsif, apakah layanan pulih sendiri setelah beban berhenti, apakah rate-limit / pembatas beban bekerja, dan apakah data tetap utuh setelah beban. Dipakai pada layanan lab milik sendiri (server web, API, atau layanan lain yang dijalankan di mesin sendiri, jaringan terisolasi). Dipakai SEBELUM mengklaim apa pun soal ketahanan — klaim tanpa angka beban dan tanpa bukti pemulihan adalah dugaan, bukan temuan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Merancang skenario beban di lab, menjalankan uji, mengukur pemulihan |
| Pengerjaan | **A54 Penguji Live** | Memantau layanan lab selama uji dan memverifikasi pemulihan + integritas data |
| Audit | **A60 Security Auditor** | Memvalidasi angka dan bukti sebelum dicatat sebagai hasil (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan apakah hasil lab relevan untuk dilaporkan/dipelajari |

## Sudah tercakup (jangan diduplikat)

- Fuzzing direktori/file dengan jeda antar-request (tanpa DoS) → skill `fuzzing-direktori-file`.
- MITM/ARP spoofing di lab → skill `mitm-arp-spoofing-lab`; poisoning SMB/LLMNR → skill `smb-llmnr-poisoning-lab`; deauth Wi-Fi → skill `serangan-deauth-wifi-lab`.
- Uji ketahanan backup sendiri → skill `ketahanan-backup-sendiri`; pemulihan/rollback agen sendiri → skill `pemulihan-rollback-agen-sendiri`.
- Teknik web klasik yang dilarang membanjiri server → aturan keras di `injeksi-sql-kontekstual` (time-based: satu permintaan per uji, jeda antar-uji).

## Aturan keras

1. **Hanya program bounty resmi in-scope — dan untuk skill ini: HANYA lab sendiri.** Tidak ada pengujian DoS pada target program apa pun sebelum membaca pasal scope; bila pasal melarang, jangan uji.
2. **Hanya akun sendiri + canary palsu.** Layanan yang dibebani adalah layanan MILIK SENDIRI di lab; data di dalamnya adalah data canary/palsu.
3. **Tanpa data orang lain.** Tanpa membebani layanan yang dipakai orang lain, tanpa memakai data pengguna lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Tidak ada "korban" dalam uji ini — hanya layanan lab sendiri.
5. **Tanpa DoS/DDoS pada target program.** Ini aturan inti skill ini: beban HANYA pada layanan lab sendiri, di jaringan terisolasi, dengan volume yang disengaja kecil dan terkendali. DILARANG membanjiri target program, layanan publik, atau layanan pihak ketiga.
6. **Tanpa payload di permukaan publik.** Skenario dan alat beban lab tidak di-host/dibagikan di tempat umum.
7. **Validasi human-in-the-loop.** Setiap angka dan klaim diperiksa manusia (Muse/A60) sebelum dicatat sebagai hasil.
8. **Tanpa laporan tanpa persetujuan Cipta.** Hasil ditulis sebagai DRAF/catatan lab dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi beban hanya di lab sendiri; otomasi terhadap target program mengikuti pasal scope.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menguji DoS pada target program, layanan publik, atau layanan orang lain. DILARANG memakai volume beban yang bisa merembet keluar lab (mis. membanjiri jaringan bersama). DILARANG merusak data lab secara permanen — data lab HARUS bisa dipulihkan dari backup sebelum uji. Bila layanan lab tidak pulih setelah beban berhenti, hentikan uji, pulihkan dari backup, dan catat kegagalan pemulihan sebagai hasil.

## Langkah + gerbang

### Gerbang 0 — Cek scope + siapkan lab dan backup

1. Baca pasal scope program yang relevan dan catat larangan DoS-nya. Siapkan layanan lab milik sendiri di jaringan terisolasi. Buat BACKUP lengkap layanan + data canary SEBELUM uji apa pun. Tentukan batas beban maksimum yang diizinkan di lab (mis. jumlah permintaan/detik) dan batas waktu uji.
2. **Standar lulus:** pasal scope tercatat + backup terverifikasi bisa dipulihkan + batas beban tertulis. Tanpa backup = jangan mulai.

### Gerbang 1 — Baseline: kinerja normal tanpa beban

1. Ukur kinerja normal layanan lab: waktu respons, throughput, penggunaan CPU/memori, dan integritas data canary. Catat angka baseline.
2. **Standar lulus:** angka baseline tercatat. Tanpa baseline, dampak beban tidak terukur.

### Gerbang 2 — Beban bertahap, ukur titik melambat

1. Beri beban bertahap dari kecil ke batas yang ditentukan (naikkan perlahan, jeda antar-tahap). Di tiap tahap catat waktu respons, error rate, dan penggunaan sumber daya. BERHENTI menaikkan beban begitu layanan tidak responsif atau error rate melonjak — jangan terus membanjiri layanan yang sudah jatuh.
2. **Standar lulus:** titik beban saat layanan melambat/tidak responsif tercatat dengan angka (beban X → respons Y / error Z%). Tanpa angka = belum terbukti.

### Gerbang 3 — Hentikan beban, ukur pemulihan

1. Hentikan semua beban. Ukur berapa lama layanan kembali normal (waktu respons kembali ke baseline), dan periksa integritas data canary (apakah ada data rusak/hilang). Bila layanan tidak pulih sendiri, pulihkan dari backup Gerbang 0 dan catat itu sebagai kegagalan pemulihan.
2. **Standar lulus:** waktu pemulihan tercatat + integritas data terverifikasi (utuh/rusak — apa adanya). Tanpa pemeriksaan integritas = uji belum selesai.

### Gerbang 4 — Uji pertahanan: rate-limit / pembatas beban

1. Ulangi beban kecil sambil mengamati apakah rate-limit atau pembatas beban layanan bekerja (apakah permintaan berlebih ditolak dengan respons yang wajar, bukan crash). Catat ambang dan perilakunya.
2. **Standar lulus:** perilaku rate-limit tercatat (ambang + respons penolakan) atau ketiadaannya tercatat. Ketiadaan rate-limit di lab sendiri adalah catatan ketahanan, bukan temuan pada target.

### Gerbang 5 — Tulis hasil lab

1. Tulis hasil lengkap: baseline, titik beban, waktu pemulihan, integritas data, perilaku rate-limit. Serahkan ke A60 untuk validasi angka. Hasil lab disimpan sebagai pembelajaran; hanya maju ke draf laporan program bila program secara eksplisit mengizinkan pengujian ketahanan pada aset tertentu.
2. **Standar lulus:** hasil mengikuti format output + angka divalidasi A60. Tanpa validasi angka = jangan jadikan rujukan.

## Alat

| Alat | Cara pakai |
|---|---|
| Layanan lab milik sendiri (server web/API di mesin sendiri) | Satu-satunya target beban |
| Alat pembangkit beban (mis. ApacheBench / wrk / skrip sendiri) | HANYA ke layanan lab sendiri, volume bertahap dan dibatasi |
| Monitor sumber daya + pengukur waktu respons | Mencatat baseline, titik melambat, dan waktu pemulihan |
| Backup layanan lab + data canary | Dipulihkan bila layanan tidak pulih sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log baseline, beban, pemulihan, dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [Lab sendiri — bukan pengujian pada target program]
Layanan lab: [nama + alamat lab milik sendiri]
Backup sebelum uji: [ya — terverifikasi bisa dipulihkan]
Baseline: [waktu respons ... | throughput ... | CPU/memori ...]
Titik melambat: [beban ... → respons ... / error ...%]
Waktu pemulihan: [... — setelah beban dihentikan]
Integritas data canary: [utuh / rusak — detail]
Rate-limit: [ada — ambang ... / tidak ada]
Target program diuji DoS: [TIDAK — dilarang pasal scope / tidak ada]
Keputusan: [pembelajaran lab / maju ke draf — diputuskan A60 + Muse]
Status: [DRAF — menunggu persetujuan Cipta / dicatat sebagai pembelajaran]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program dan umumnya TIDAK DIBAYAR — DoS tidak dibayar di program bounty.
- Angka beban lab tidak bisa dipindahkan mentah-mentah ke layanan nyata (perangkat keras, konfigurasi, dan lalu lintas nyata berbeda).
- Uji ini tidak mengukur ketahanan terhadap DDoS terdistribusi — hanya beban dari satu sumber di lab.
- Bila layanan lab memakai layanan pihak ketiga (mis. database cloud), beban TIDAK BOLEH diteruskan ke layanan itu — batasi uji pada komponen milik sendiri.
