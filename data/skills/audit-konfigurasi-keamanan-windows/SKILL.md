# Skill: Audit Konfigurasi Keamanan Windows — GPO, Defender, LSA, Credential Guard, SMB Signing, dan RDP

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 2, 24 Nov 2026 (Audit konfigurasi keamanan Windows/endpoint). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk 9 program bounty resmi: Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, dan huntr. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Audit konfigurasi HANYA pada sistem/lab SENDIRI atau infrastruktur in-scope eksplisit — tanpa membaca atau mengubah konfigurasi endpoint orang lain, dan tanpa mengubah satu pengaturan pun pada sistem yang bukan milik sendiri.

## Pemicu

Dipakai saat aset Windows/endpoint in-scope perlu diaudit konfigurasinya: apakah Group Policy (GPO) benar-benar menegakkan yang diklaim, apakah Windows Defender berjalan dengan pengecualian yang wajar, apakah audit policy mencatat peristiwa yang penting, apakah LSA protection dan Credential Guard aktif, apakah SMB signing diwajibkan, dan apakah RDP dikunci dengan benar. Skill ini adalah AUDIT KONFIGURASI ENDPOINT — membaca dan menguji pengaturan keamanan sistem, bukan memetakan domain dan bukan mengeksploitasi eskalasi hak akses.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis konfigurasi (pengaturan mana yang diduga salah) + membaca kebijakan dan pengaturan |
| Pengerjaan | **A62 Exploit Developer** | Menguji dampak konfigurasi dari luar/dari akun uji sendiri, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemetaan jalur serangan Active Directory / Azure AD lewat graf (BloodHound/RoadRecon MCP) → skill `analisis-active-directory-lewat-mcp` (itu MEMETAKAN graf hubungan domain — siapa bisa menjadi admin lewat jalur apa. Skill ini TIDAK memetakan AD: ini mengaudit PENGATURAN keamanan satu endpoint Windows — GPO yang diterapkan, Defender, LSA, Credential Guard, SMB signing, RDP. Sudutnya berbeda: konfigurasi endpoint vs graf domain).
- Teknik eskalasi hak akses lokal Windows (mengeksploitasi kelemahan untuk naik hak akses) → TIDAK ADA skill bernama `eskalasi-hak-akses-windows` di kedua toko (dicek 24 Nov 2026 — tidak ditemukan). Skill ini BUKAN eskalasi: tidak ada langkah menaikkan hak akses, hanya membaca dan menguji pengaturan keamanan. Bila suatu hari skill eskalasi Windows dibangun, skill ini tetap berbeda — audit konfigurasi vs eksploitasi eskalasi.
- Serangan poisoning nama di jaringan lokal (LLMNR/NBT-NS) → skill `smb-llmnr-poisoning-lab` (teknik poisoning jaringan, bukan audit apakah SMB signing diwajibkan pada endpoint).
- Audit konfigurasi layanan Linux (HTTP/SSH/FTP) → skill `audit-konfigurasi-layanan-linux` (platform berbeda — jangan dicampur).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya sistem/lab SENDIRI atau infrastruktur in-scope eksplisit.** Tanpa membaca atau mengubah konfigurasi endpoint orang lain — GPO, Defender, dan pengaturan keamanan sistem lain = DILARANG disentuh.
3. **Hanya akun sendiri + canary palsu.** Pengujian hanya dengan akun uji milik sendiri; tanpa data orang lain, tanpa menyentuh sesi pengguna lain.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau host yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri endpoint atau layanan dengan permintaan — uji konektivitas dibatasi hitungan kecil dengan jeda.
6. **Tanpa payload di permukaan publik.** Isi kebijakan, daftar pengecualian Defender, dan temuan jangan dipublikasikan.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengubah pengaturan keamanan apa pun (tanpa mengubah GPO, tanpa menambah/menghapus pengecualian Defender, tanpa mematikan perlindungan, tanpa mengubah audit policy, tanpa mengubah pengaturan RDP/SMB), DILARANG menonaktifkan Defender atau perlindungan kredensial, DILARANG menghapus log. Audit ini READ-ONLY: baca pengaturan yang boleh dibaca + uji perilaku dari akun uji sendiri. Bila satu-satunya cara membuktikan adalah mengubah pengaturan — BERHENTI dan serahkan ke Muse.

## Yang dicari (definisi singkat)

- **GPO yang tidak ditegakkan:** kebijakan yang diklaim aktif ternyata tidak diterapkan pada endpoint (mis. hasil kebijakan menunjukkan pengaturan tidak berlaku, atau kebijakan ditimpa oleh pengaturan lokal yang lebih longgar).
- **Defender yang dilubangi:** daftar pengecualian (exclusions) yang terlalu luas — seluruh drive, folder sistem, atau jenis file yang seharusnya dipindai justru dikecualikan — atau perlindungan real-time yang ternyata mati.
- **Audit policy yang buta:** peristiwa penting tidak dicatat (logon gagal, perubahan kebijakan, akses objek sensitif) sehingga insiden tidak bisa ditelusuri.
- **LSA protection / Credential Guard mati:** perlindungan kredensial tidak aktif padahal kebijakan mewajibkannya, sehingga kredensial lebih mudah dibaca dari memori.
- **SMB signing tidak diwajibkan:** endpoint menerima koneksi SMB tanpa signing, sehingga lalu lintas SMB bisa dipalsukan/relay.
- **RDP yang longgar:** RDP aktif tanpa Network Level Authentication (NLA), tanpa batas percobaan login, atau bisa dijangkau dari segmen yang seharusnya tidak boleh.
- **Bukan temuan:** pengaturan yang memang disengaja dan terdokumentasi (mis. pengecualian Defender untuk folder aplikasi yang memang didokumentasikan dan beralasan — buktikan dulu kebijakannya); perlindungan yang mati karena endpoint memang bukan target kebijakan itu (mis. Credential Guard pada perangkat keras yang tidak mendukung — buktikan dulu batas perangkatnya, jangan klaim sebagai kelalaian konfigurasi).

## Langkah + gerbang

### Gerbang 0 — Cek scope + kenali kebijakan yang berlaku dulu

1. Baca pasal scope program: apakah aset Windows/endpoint ini tertulis in-scope? Tulis kutipan scope-nya ke log. Bila tidak tertulis = BERHENTI.
2. Kumpulkan kebijakan yang berlaku: GPO apa yang seharusnya diterapkan pada endpoint ini, standar hardening apa yang dipakai (mis. baseline keamanan yang dinyatakan program), dan peran endpoint (workstation, server, jump host).
3. **Standar lulus:** kutipan scope + daftar kebijakan/standar yang berlaku tercatat di log sebelum satu pengaturan pun dibaca. Tanpa pembanding kebijakan = jangan mulai (tidak ada ukuran "salah").

### Gerbang 1 — Baca kebijakan hasil (GPO) dan pengaturan lokal

1. Baca hasil kebijakan yang diterapkan pada endpoint sendiri (kebijakan hasil/GPO yang berlaku + pengaturan lokal) dan bandingkan dengan kebijakan yang seharusnya (Gerbang 0): pengaturan mana yang tidak diterapkan, ditimpa, atau berbeda nilainya.
2. Catat tiap penyimpangan persis (nama pengaturan + nilai yang berlaku + nilai yang seharusnya + sumbernya: GPO atau lokal).
3. **Standar lulus:** tiap penyimpangan tercatat persis. Penyimpangan yang "kelihatan ada" tanpa nilai dan sumber = belum terbukti, jangan klaim.

### Gerbang 2 — Audit Windows Defender dan pengecualiannya

1. Baca status Defender pada endpoint sendiri: apakah perlindungan real-time aktif, kapan terakhir diperbarui, dan apakah ada pengecualian (path, proses, ekstensi) beserta alasannya.
2. Nilai tiap pengecualian terhadap kebijakan: pengecualian yang terlalu luas (seluruh drive, folder sistem, semua file executable) dicatat sebagai temuan potensial; pengecualian yang sempit dan beralasan dicatat sebagai wajar.
3. **Standar lulus:** status Defender + daftar pengecualian persis tercatat beserta penilaiannya. Perlindungan yang mati = temuan potensial; semua aktif dan pengecualian wajar = AMAN, tutup dengan buktinya.

### Gerbang 3 — Audit audit policy dan pencatatan

1. Baca kebijakan audit yang berlaku pada endpoint sendiri: peristiwa apa saja yang dicatat (logon berhasil/gagal, perubahan kebijakan, akses objek, pembuatan proses) dan berapa lama log disimpan.
2. Uji pencatatan dengan akun uji sendiri: lakukan SATU peristiwa yang seharusnya tercatat (mis. satu logon gagal akun sendiri) lalu periksa apakah peristiwa itu benar-benar muncul di log dengan detail yang cukup.
3. **Standar lulus:** daftar peristiwa yang dicatat + hasil uji pencatatan tercatat. Peristiwa penting yang tidak tercatat = temuan potensial; semua tercatat = AMAN.

### Gerbang 4 — Audit LSA protection dan Credential Guard

1. Baca status perlindungan kredensial pada endpoint sendiri: apakah LSA protection aktif dan apakah Credential Guard berjalan (bila perangkat mendukungnya).
2. Bila perlindungan mati, periksa dulu alasannya: apakah perangkat memang tidak mendukung (batas perangkat keras/firmware) atau karena pengaturan yang dimatikan — hanya yang kedua yang merupakan temuan konfigurasi.
3. **Standar lulus:** status tiap perlindungan + alasan bila mati tercatat. Perlindungan yang dimatikan oleh pengaturan = temuan potensial; mati karena batas perangkat = BUKAN temuan, catat alasannya.

### Gerbang 5 — Uji SMB signing dan RDP dari akun uji sendiri

1. SMB signing: periksa pengaturan signing pada endpoint sendiri (apakah signing diwajibkan untuk klien dan server), lalu dari host uji sendiri coba sambungan SMB dan amati apakah sambungan tanpa signing diterima atau ditolak.
2. RDP: periksa apakah RDP aktif, apakah NLA diwajibkan, dan apakah ada batas percobaan login; dari host uji sendiri coba sambungan RDP ke endpoint sendiri dan catat responsnya (NLA diminta atau tidak).
3. **Standar lulus:** tiap pengaturan tercatat + hasil uji sambungan tercatat. Sambungan tanpa signing/NLA yang diterima = temuan potensial; semua ditolak = AMAN. Uji login RDP hanya dengan akun uji sendiri, hitungan kecil, dan jangan pernah mencoba kredensial orang lain.

### Gerbang 6 — Buktikan dampak read-only, serahkan ke triase

1. Bukti maksimal: pengaturan yang salah (nama + nilai + sumber GPO/lokal) + perilaku yang teramati (Defender/pencatatan/SMB/RDP) + kebijakan yang dilanggar. BERHENTI di situ — jangan menonaktifkan perlindungan untuk "membuktikan lebih jauh", jangan membaca kredensial, jangan menyentuh data pengguna lain.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (pengaturan + uji persis + hasil persis) + keputusan triase tercatat. Tanpa pasangan "pengaturan + perilaku teramati" = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Akses baca ke endpoint Windows sendiri | Baca hasil kebijakan (GPO), status Defender, audit policy, LSA/Credential Guard, SMB signing, dan pengaturan RDP; read-only |
| Perintah baca bawaan (mis. gpresult, Get-MpPreference, auditpol, Get-SmbServerConfiguration) | Hanya perintah BACA — tanpa perintah ubah; catat keluarannya persis |
| Klien SMB/RDP dari host uji sendiri | Uji apakah sambungan tanpa signing/NLA diterima atau ditolak; hanya akun uji sendiri |
| Penampil log peristiwa (Event Viewer / log audit) | Verifikasi peristiwa uji benar-benar tercatat |
| `~/workspace/catatan/log-bug-bounty.md` | Log scope → kebijakan → pengaturan → hasil tiap gerbang → keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint Windows in-scope + peran endpoint]
Kutipan scope: [teks aturan program yang mengizinkan aset ini]
Kebijakan yang berlaku: [GPO/standar yang seharusnya diterapkan]
Gerbang GPO: [pengaturan — nilai berlaku — nilai seharusnya — sumber GPO/lokal]
Gerbang Defender: [real-time: aktif/mati — pengecualian: daftar persis — penilaian]
Gerbang audit policy: [peristiwa yang dicatat — uji pencatatan: tercatat/tidak]
Gerbang LSA/Credential Guard: [status — alasan bila mati: pengaturan/batas perangkat]
Gerbang SMB/RDP: [signing: diwajibkan/tidak — uji sambungan: diterima/ditolak — NLA: ya/tidak]
Dampak: [pengaturan salah apa + perilaku apa yang dimungkinkan + kebijakan yang dilanggar]
Yang TIDAK dilakukan: [tanpa ubah pengaturan, tanpa matikan perlindungan, tanpa baca kredensial, tanpa hapus log]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Audit konfigurasi hanya sekuat akses bacanya — bila pengaturan tidak bisa dibaca akun uji, yang tersisa hanya pengujian perilaku dari luar; nyatakan batas itu di log, jangan mengklaim isi pengaturan yang tidak dibaca.
- Hasil kebijakan (GPO) bergantung pada urutan penerapan dan penimpaan lokal — catat sumber tiap nilai (GPO vs lokal) agar temuan bisa direproduksi; nilai yang "salah" di lokal belum tentu salah bila GPO yang benar menimpanya.
- Beberapa perlindungan (mis. Credential Guard) membutuhkan dukungan perangkat keras/firmware — ketiadaan perlindungan pada perangkat yang tidak mendukung BUKAN temuan konfigurasi; buktikan dulu batas perangkatnya.
- Pengaturan yang sama bisa wajar di satu peran endpoint dan berbahaya di peran lain (mis. RDP pada jump host vs workstation biasa) — nilai temuan menurut peran endpoint dan kebijakan yang berlaku, bukan menurut daftar generik.
