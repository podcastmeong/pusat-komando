# Skill: Profesionalisme Audit di Bawah Tekanan Tinggi — Ketelitian Saat Taruhannya Besar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 6, 24 Nov 2026. Praktik profesionalisme ini belum pernah dijalani dalam audit nyata oleh tim; label ini berlaku untuk semua bagian sampai ada satu audit/pentest nyata yang dicatat lengkap di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill standar perilaku — mengatur CARA agent bekerja di bawah tekanan audit — BUKAN skill pengujian: skill ini tidak memberi langkah untuk menemukan atau mengeksploitasi kerentanan. Skill ini melengkapi (bukan menggantikan) skill penulisan laporan.

## Pemicu

Dipakai setiap kali audit/pentest nyata berjalan dengan taruhan tinggi (temuan yang terlewat bisa merugikan besar; tenggat ketat; target kompleks); setiap kali agent merasa terburu-buru, lelah, atau tergoda melewati langkah verifikasi; dan setiap kali laporan + remediasi harus diserahkan. Dipakai juga saat review pasca-audit.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Penanggung jawab mutu | **A60 Security Auditor** | Menjaga standar ketelitian, menghentikan pekerjaan yang terburu-buru, memvalidasi laporan sebelum maju (A60 tidak meloloskan temuannya sendiri) |
| Pengerjaan | **A59 Threat Hunter, A58 Vulnerability Researcher** | Menjalankan audit mengikuti gerbang; melaporkan tekanan/kesulitan dengan jujur, bukan menyembunyikannya |
| Pemimpin | **Muse** | Memutuskan jeda/perpanjangan saat tekanan mengancam mutu; memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Cara menulis laporan (struktur, bukti, severity) → skill `penulisan-laporan-bounty` + `tulis-laporan-yeswehack` + `laporan-abstrak`. Skill ini TIDAK mengulang struktur laporan — skill ini mengatur PERILAKU saat menulisnya di bawah tekanan (jujur, teliti, tidak dibesar-besarkan).
- Metodologi pentest 5 tahap → skill `metodologi-pentest-ujung-ke-ujung`. Skill ini tidak mengulang tahapannya — skill ini menjaga agar tahapan itu tidak dilompati saat terdesak waktu.
- Validasi temuan + filter false positive → skill `triase-duplikat` + `skeptic-false-positive-eliminator`. Skill ini memakai hasil triase itu; cara triasenya tetap di sana.
- Etika + kerahasiaan data → skill `etika-kerahasiaan-data-bounty`. Skill ini tidak mengulang aturan etikanya — skill ini mengatur ketelitian dan kejujuran di bawah tekanan.

## Prinsip kerja di bawah tekanan

1. **Pelan lebih cepat daripada salah.** Di bawah tekanan, godaan terbesar adalah melewati verifikasi. Satu temuan salah yang dilaporkan merusak kredibilitas lebih daripada satu temuan benar yang terlambat sehari.
2. **Taruhan besar = verifikasi ganda.** Semakin besar dampak bila celah terlewat (atau bila laporan salah), semakin ketat verifikasinya. Tidak ada pengecualian karena "sudah mepet tenggat".
3. **Lelah adalah sinyal berhenti, bukan sinyal memaksa.** Agent yang lelah membuat kesalahan verifikasi. Istirahat dan serahkan ke agent lain lebih baik daripada memaksakan hasil yang cacat.
4. **Jujur soal yang tidak ditemukan.** Laporan yang jujur ("bagian ini sudah diuji, tidak ditemukan celah") sama berharganya dengan laporan temuan. Menyembunyikan bagian yang belum diuji adalah pelanggaran profesionalisme.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pengujian audit hanya di akun dan data milik sendiri atau canary palsu.
3. **Tanpa data orang lain.** Jangan menyentuh, menyimpan, atau memakai data pengguna lain selama audit.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan atau akun yang bukan milik sendiri DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan, termasuk saat audit mendesak waktu.
6. **Tanpa payload di permukaan publik.** Laporan, bukti, dan catatan audit jangan di-host atau dibagikan di tempat umum — hanya di lingkungan terkendali milik sendiri dan jalur resmi program.
7. **Validasi human-in-the-loop.** Laporan audit harus diperiksa Muse/A60 sebelum maju — jangan serahkan keputusan mutu ke otomatisasi, apalagi saat terdesak waktu.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data apa pun selama audit — termasuk data target. DILARANG memakai hasil audit untuk mengakses akun siapa pun, memeras, mengancam, atau memperoleh keuntungan di luar hadiah bounty resmi.

## Langkah + gerbang

### Gerbang 0 — Kesiapan sebelum audit

1. Checklist sebelum mulai: scope tertulis sudah dibaca; batas pengujian jelas; akun sendiri + canary siap; alat + skill yang relevan sudah dipetakan; tenggat + pembagian tugas tercatat.
2. **Standar lulus:** semua checklist tercentang dan tercatat di log. Satu checklist kosong = jangan mulai.

### Gerbang 1 — Kerja bertekanan (aturan jeda + verifikasi)

1. Aturan saat tekanan naik: (a) perlambat, jangan percepat — ulangi langkah verifikasi, bukan dilewati; (b) satu hipotesis dalam satu waktu — jangan menguji tiga hal sekaligus saat terdesak; (c) bila lelah atau buntu lebih dari satu jam, jeda dan serahkan ke agent lain; (d) setiap langkah destruktif-berisiko dicek dua kali sebelum dijalankan (dan langkah destruktif itu sendiri dilarang — lihat Aturan 10).
2. **Standar lulus:** tidak ada langkah verifikasi yang dilewati; setiap jeda/serah-terima tercatat. Langkah yang dilewati = ulangi dari langkah itu.

### Gerbang 2 — Laporan jujur

1. Tulis laporan mengikuti skill `penulisan-laporan-bounty`, dengan tambahan kejujuran profesional: (a) severity sesuai bukti, jangan dibesar-besarkan; (b) bagian yang SUDAH diuji dan tidak ada temuan ditulis eksplisit; (c) bagian yang BELUM sempat diuji ditulis eksplisit — jangan disembunyikan; (d) ketidakpastian ditulis sebagai ketidakpastian, bukan sebagai kepastian.
2. **Standar lulus:** laporan diperiksa A60 dan lolos: severity cocok dengan bukti, tidak ada bagian yang disembunyikan. Satu klaim berlebihan = laporan DITOLAK, perbaiki.

### Gerbang 3 — Remediasi + retest

1. Untuk setiap temuan yang dilaporkan: tulis langkah perbaikan (remediation) yang konkret dan bisa diuji; setelah program memperbaiki, lakukan retest untuk memastikan celah benar-benar tertutup; catat hasil retest.
2. **Standar lulus:** setiap temuan punya langkah remediasi tertulis + status retest (tertutup / masih terbuka). Temuan tanpa remediasi = belum selesai.

### Gerbang 4 — Review pasca-audit

1. Setelah audit selesai: catat apa yang berjalan baik, apa yang hampir salah, di mana tekanan paling besar, dan apa yang diubah untuk audit berikutnya. Kesalahan dicatat jujur — menyembunyikan kesalahan lebih buruk daripada melakukannya.
2. **Standar lulus:** catatan review lengkap di log + satu perbaikan proses diputuskan untuk audit berikutnya.

## Alat

| Alat | Cara pakai |
|---|---|
| Checklist kesiapan (Gerbang 0) | Templat di atas; salin ke log tiap audit |
| Skill `penulisan-laporan-bounty` + `tulis-laporan-yeswehack` | Struktur laporan (Gerbang 2) |
| Skill `triase-duplikat` + `skeptic-false-positive-eliminator` | Validasi temuan sebelum laporan |
| Skill `metodologi-pentest-ujung-ke-ujung` | Tahapan audit yang tidak boleh dilompati |
| `~/workspace/catatan/log-bug-bounty.md` | Log kesiapan + jeda/serah-terima + laporan + remediasi/retest + review pasca-audit |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [satu dari sembilan program resmi]
Audit: [target + tenggat]
Kesiapan: [checklist Gerbang 0 — lengkap / ada yang kosong + apa]
Jeda/serah-terima: [kapan + kenapa + ke siapa]
Temuan: [judul singkat + severity + bukti minimal]
Yang sudah diuji tanpa temuan: [bagian + hasil]
Yang belum diuji: [bagian + alasan]
Remediasi: [langkah perbaikan per temuan]
Retest: [tertutup / masih terbuka + tanggal]
Review: [apa yang berjalan baik / hampir salah / perbaikan proses berikutnya]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Skill ini mengatur perilaku, bukan memberi jaminan hasil. Audit yang profesional pun bisa tidak menemukan apa-apa — itu hasil yang sah, bukan kegagalan.
- Tekanan tenggat tidak pernah menjadi alasan melewati verifikasi. Bila tenggat tidak mungkin dipenuhi dengan mutu yang benar, laporkan ke Muse LEBIH AWAL — jangan diam sampai tenggat lewat.
- Remediasi + retest bergantung pada respons program; bila program tidak merespons, catat itu dan jangan memaksa retest di luar jalur resmi.
- Bila agent merasa tidak mampu menangani tekanan satu audit, serahkan lebih awal — menyerahkan adalah profesional, memaksakan hasil cacat bukan.

### Available connectors

Tidak ada konektor khusus untuk skill ini; checklist, laporan, dan review dicatat manual di log dan divalidasi A60/Muse.

### Websites

- Halaman scope + kebijakan disclosure resmi tiap program (sumber batas audit — baca sebelum Gerbang 0).
- Standar etika profesional gaya EC-Council sebagai rujukan perilaku (hanya rujukan — bukan isi skill ini).

### Alternatives for better results

- Bila tenggat mepet, potong SCOPE (bagian target yang diuji), jangan potong VERIFIKASI — audit kecil yang teliti lebih baik daripada audit besar yang cacat.
- Bila dua agent mengaudit target yang sama, tukar laporan draf untuk saling memeriksa sebelum ke A60 — mata kedua menangkap klaim berlebihan yang mata pertama lewatkan.
- Bila review pasca-audit menemukan pola kesalahan yang berulang, usulkan perbaikan ke skill yang relevan (atau skill baru) ke Muse — jangan biarkan kesalahan yang sama terulang di audit berikutnya.
