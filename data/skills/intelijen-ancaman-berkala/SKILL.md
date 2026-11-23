# Skill: Intelijen Ancaman Berkala — Tren Ancaman Global dan Umpan Balik ke Prioritas Perburuan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 5, 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill riset threat intelligence berkala — membaca tren ancaman global, mempelajari cara cyber criminal beroperasi dan TTP (taktik, teknik, prosedur) baru, lalu memberi umpan balik ke prioritas perburuan: teknik yang sedang tren menentukan skill pengujian apa yang dipakai berikutnya. Skill ini BUKAN skill pengujian dan BUKAN skill penargetan individu: tidak ada langkah menyerang siapa pun di sini.

## Pemicu

Dipakai secara berkala (mis. tiap awal pekan perburuan, atau tiap kali ada laporan tren ancaman besar) dan setiap kali ada perubahan pola yang relevan: teknik baru yang ramai dipakai penyerang, kampanye besar yang diberitakan, atau perubahan prioritas di program bounty yang sedang diikuti. Dipakai SEBELUM menyusun prioritas perburuan putaran berikutnya — hasil skill ini menjadi masukan "teknik apa yang sedang tren → skill apa yang dipakai". Dipakai bersamaan dengan `pemantauan-cve-breach-nyata` (yang memberi CVE spesifik) — skill ini memberi KONTEKS tren di sekeliling CVE itu.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Membaca sumber intelijen publik berkala; merangkum tren + TTP baru |
| Pengerjaan | **A58 Vulnerability Researcher** | Menerjemahkan tren/TTP menjadi prioritas skill pengujian yang dipakai |
| Audit | **A60 Security Auditor** | Memvalidasi rangkuman tren + rekomendasi prioritas sebelum dipakai (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan prioritas perburuan putaran berikutnya berdasarkan umpan balik skill ini |

## Sudah tercakup (jangan diduplikat)

- CVE spesifik + kasus breach nyata yang dipetakan ke target → skill `pemantauan-cve-breach-nyata`. Skill ini membahas TREN dan TTP secara umum — bukan CVE per CVE.
- Pemantauan PROGRAM bounty (scope/hadiah/deadline program) → skill `recon-pantau-program`. Skill ini memantau ANCAMAN, bukan program.
- Pengujian teknik yang sedang tren → skill pengujian yang sesuai (dipilih berdasarkan rekomendasi skill ini, dieksekusi di sana — bukan di sini).
- Penanganan data temuan → skill `etika-kerahasiaan-data-bounty` + `kebersihan-bukti`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Intelijen yang dikumpulkan tidak pernah dipakai terhadap akun orang lain.
3. **Tanpa data orang lain.** Tanpa mengumpulkan, menyimpan, atau memakai data pribadi siapa pun dari sumber intelijen.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan atas nama "mengikuti tren".
6. **Tanpa payload di permukaan publik.** Rangkuman tren dan rekomendasi prioritas jangan dibagikan di tempat umum — hanya di log internal.
7. **Validasi human-in-the-loop.** Setiap rangkuman tren dan rekomendasi prioritas harus diperiksa manusia (Muse/A60) sebelum dipakai — jangan pakai hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan yang lahir dari prioritas skill ini ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai intelijen ancaman untuk menyerang, merusak, atau mengakses target di luar scope bounty. DILARANG menarget individu (peneliti, karyawan, pengguna) berdasarkan intelijen. DILARANG memakai data pribadi dari sumber intelijen dalam bentuk apa pun. Intelijen di sini HANYA dipakai untuk memilih teknik perburuan yang diizinkan program.

## Langkah + gerbang

### Gerbang 0 — Cek scope + sumber intelijen publik dulu

1. Pastikan program yang diikuti masih aktif (lihat `recon-pantau-program`). Daftar sumber intelijen publik yang dipakai putaran ini: laporan tren ancaman vendor keamanan yang kredibel, laporan insiden publik, dan advisory publik. Catat sumbernya — sumber yang tidak kredibel (tanpa penulis, tanpa tanggal, tanpa bukti) dicoret.
2. **Standar lulus:** daftar sumber tercatat + sumber yang dicoret beserta alasannya. Tanpa daftar sumber = jangan mulai.

### Gerbang 1 — Kumpulkan tren + TTP baru

1. Baca sumber putaran ini dan catat: (a) teknik/TTP apa yang sedang naik (mis. teknik prompt injection baru, pola bypass autentikasi, penyalahgunaan agen AI); (b) siapa yang diserang (sektor/komponen — BUKAN individu); (c) komponen atau pola apa yang dieksploitasi; (d) apakah ada kaitannya dengan target in-scope.
2. Bedakan FAKTA (apa yang dilaporkan terjadi) dari OPINI (apa yang diprediksi penulis laporan). Hanya fakta yang masuk rangkuman; opini dicatat terpisah sebagai "prediksi, belum terverifikasi".
3. **Standar lulus:** tiap tren tercatat dengan sumber + fakta vs opini dipisah. Tren tanpa sumber = rumor, jangan dipakai.

### Gerbang 2 — Petakan tren ke skill pengujian

1. Untuk tiap tren yang relevan dengan target in-scope, tentukan skill pengujian apa yang dipakai untuk memburunya (mis. tren bypass autentikasi → skill otorisasi; tren prompt injection pada agen → skill injeksi prompt; tren penyalahgunaan API → skill pengujian API). Bila belum ada skill yang cocok, catat sebagai "butuh skill baru — ajukan ke Muse", jangan memaksakan tren ke skill yang tidak cocok.
2. **Standar lulus:** tiap tren relevan punya skill pengujian yang dituju (atau status "butuh skill baru"). Tren tanpa pemetaan = belum bisa dieksekusi.

### Gerbang 3 — Susun prioritas putaran berikutnya

1. Urutkan tren berdasarkan: relevansi dengan target in-scope, apakah tekniknya diizinkan program (periksa larangan otomasi dan larangan teknik — mis. Google AI VRP memblokir payload injeksi; huntr "Humans only"), dan seberapa baru tren itu (tren yang sudah lama dan sudah ditambal massal bernilai lebih rendah).
2. Tulis rekomendasi prioritas: urutan teknik + skill yang dipakai + alasan. Serahkan ke A60 untuk validasi.
3. **Standar lulus:** daftar prioritas tertulis + divalidasi A60. Prioritas tanpa validasi A60 = belum boleh dipakai.

### Gerbang 4 — Umpan balik: catat hasil putaran lalu

1. Sebelum putaran baru dimulai, tinjau putaran sebelumnya: teknik dari tren mana yang terbukti menghasilkan temuan, mana yang gagal, dan mana yang ternyata sudah ditambal. Hasil ini mengubah bobot tren di putaran berikutnya (tren yang terbukti → naik; tren yang berulang kali gagal → turun).
2. **Standar lulus:** tiap rekomendasi putaran lalu punya hasil tercatat (terbukti / gagal / ditambal). Tanpa tinjauan balik = putaran baru mengulang tebakan lama.

### Gerbang 5 — Serahkan prioritas ke perburuan

1. Serahkan daftar prioritas yang sudah divalidasi ke A58/A59 untuk dieksekusi lewat skill pengujian masing-masing. Skill ini BERHENTI di sini — tidak ada pengujian di dalam skill ini.
2. **Standar lulus:** prioritas tercatat di log + penerima (skill pengujian yang dituju) tercatat. Skill ini tidak mencatat "temuan" — hanya "prioritas yang diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Laporan tren ancaman publik (vendor keamanan kredibel) | Sumber utama tren + TTP — periksa penulis, tanggal, dan bukti sebelum dipakai |
| Laporan insiden publik | Pelajari pola serangan yang benar-benar terjadi — HANYA laporan publik, tanpa data pribadi |
| Advisory publik + `pemantauan-cve-breach-nyata` | Konteks CVE di sekeliling tren; CVE spesifik tetap ditangani skill CVE |
| Indeks scope program (`recon-pantau-program`) | Memastikan tren yang diprioritaskan relevan dengan program yang masih aktif |
| `~/workspace/catatan/log-bug-bounty.md` | Log putaran intelijen: tren, pemetaan ke skill, prioritas, hasil umpan balik |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal/putaran) dengan format:

```
Tanggal putaran: [YYYY-MM-DD]
Sumber dibaca: [laporan tren ... / laporan insiden ... — sumber dicoret: ... + alasan]
Tren + TTP: [teknik apa yang naik — sektor/komponen yang diserang — kaitan dengan target in-scope]
Fakta vs opini: [fakta: ... | prediksi belum terverifikasi: ...]
Pemetaan ke skill: [tren ... → skill ... | tren ... → butuh skill baru]
Prioritas putaran: [urutan #1, #2, ... + alasan + validasi A60: ya/tidak]
Umpan balik putaran lalu: [rekomendasi ... → terbukti / gagal / ditambal]
Yang TIDAK dilakukan: [tanpa menarget individu, tanpa data pribadi, tanpa pengujian di skill ini]
Status: [putaran selesai / prioritas diserahkan]
```

## Batasan yang diketahui

- Laporan tren ancaman sering ditulis untuk menjual produk vendor — baca dengan skeptis: cari bukti (data insiden, contoh nyata) di balik klaim "tren naik". Klaim tanpa bukti = opini, bukan fakta.
- Tren global belum tentu relevan dengan target in-scope: teknik yang ramai di satu sektor bisa tidak berlaku di program yang diikuti. Relevansi dengan scope selalu diperiksa dulu (Gerbang 2–3).
- TTP penyerang berubah cepat; prioritas putaran ini bisa basi dalam hitungan minggu. Itulah gunanya putaran berkala + umpan balik (Gerbang 4) — jangan memakai prioritas lama tanpa meninjaunya.
- Skill ini tidak membahas penargetan individu atau pengumpulan data pribadi. Bila suatu sumber intelijen memuat data pribadi, jangan salin atau simpan — catat hanya pola tekniknya.

### Available connectors

Tidak ada konektor khusus untuk skill ini; sumber intelijen dibaca manual dari laporan publik.

### Websites

- Laporan tren ancaman publik dari vendor keamanan yang kredibel.
- Laporan insiden publik + halaman aturan program resmi (sumber scope + larangan teknik).

### Alternatives for better results

- Bila dua sumber independen melaporkan tren yang sama, naikkan bobot tren itu — konfirmasi silang lebih kuat daripada satu laporan.
- Bila suatu tren menunjuk ke CVE spesifik, teruskan CVE itu ke skill `pemantauan-cve-breach-nyata` agar dipetakan ke target secara rinci.
- Bila prioritas putaran lalu berulang kali gagal karena target sudah menambal, turunkan bobotnya dan cari tren yang lebih baru — jangan mengulang teknik yang sudah mati.
