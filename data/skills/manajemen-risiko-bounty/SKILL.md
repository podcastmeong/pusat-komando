# Skill: Manajemen Risiko Bounty — Mengidentifikasi, Menganalisis, dan Memitigasi Risiko Perburuan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 11 (artikel Clarusway, Risk Management) + batch 12 (artikel Kamsib, Analisis & Mitigasi Risiko) + batch 14 (artikel Coursera, Risk management), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill MANAJEMEN RISIKO operasi perburuan: mengidentifikasi risiko yang mengancam perburuan (risiko scope, risiko akun diblokir, risiko false positive, risiko hukum, risiko program tutup), menganalisis likelihood + dampaknya, memitigasi dengan kontrol, dan menjaga kelangsungan perburuan (business continuity) bila satu program bermasalah. Skill ini BUKAN skill penilaian severity temuan (lihat `penilaian-cvss`) dan BUKAN nasihat hukum.

## Pemicu

Dipakai secara berkala (tiap awal putaran perburuan) dan setiap kali ada perubahan risiko: program mengubah scope/aturan, akun uji mendekati batas, teknik baru yang berisiko, atau program mendekati tanggal tutup. Dipakai SEBELUM putaran dimulai — daftar risiko putaran ini menjadi pagar pengaman eksekusi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Mengidentifikasi risiko putaran ini + mengusulkan mitigasi |
| Audit | **A60 Security Auditor** | Memvalidasi analisis risiko + mitigasi sebelum putaran jalan |
| Pemimpin | **Muse** | Memutuskan risiko mana yang diterima, dimitigasi, atau membuat putaran dihentikan |

## Sudah tercakup (jangan diduplikat)

- Penilaian severity temuan → skill `penilaian-cvss`. Skill ini menilai RISIKO OPERASI perburuan (bukan severity satu temuan).
- Penjaga scope + safety → skill `scope-and-safety-guardian`. Skill ini MEMAKAI gerbang itu sebagai salah satu kontrol mitigasi — bukan mengulanginya.
- Pemantauan program (scope/hadiah/deadline) → skill `recon-pantau-program`. Skill ini memakai data program itu untuk menilai risiko program tutup/berubah.
- Analisis risiko kuantitatif dalam dolar (FAIR) → skill `analisis-risiko-kuantitatif-fair`. Skill ini menilai risiko KUALITATIF operasi (likelihood × dampak dalam skala) — bukan nilai dolar.
- Posisi bounty dalam manajemen risiko penyelenggara → skill `membaca-scope-penyelenggara`. Skill ini menilai risiko dari sisi HUNTER, bukan penyelenggara.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Mitigasi risiko tidak pernah memakai data atau akun orang lain.
3. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
4. **Tanpa DoS/DDoS.** Jangan membanjiri target atas nama "uji risiko".
5. **Tanpa payload di permukaan publik.** Daftar risiko + mitigasi hanya di log internal.
6. **Risiko tanpa mitigasi = jangan jalan.** Bila suatu teknik punya risiko tinggi tanpa mitigasi yang jelas, teknik itu DITUNDA sampai mitigasi ada — jangan memaksakan eksekusi.
7. **Berhenti 1 hari sebelum program tutup.** Aturan ini mutlak (lihat `recon-pantau-program` untuk tanggal tutup tiap program).
8. **Validasi human-in-the-loop.** Daftar risiko + mitigasi harus diperiksa manusia (Muse/A60) sebelum putaran jalan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Risiko yang berujung temuan tetap lewat jalur draf → Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG mengambil risiko yang merusak target, data orang lain, atau reputasi tim atas nama "peluang". Manajemen risiko di sini HANYA untuk menjaga perburuan tetap aman, legal, dan berkelanjutan.

## Langkah + gerbang

### Gerbang 0 — Identifikasi risiko putaran ini

1. Daftarkan risiko putaran ini dalam 5 keluarga: (a) scope — program mengubah scope/aturan; (b) akun — akun uji diblokir/dibatasi; (c) teknik — teknik yang dipakai ternyata dilarang program; (d) bukti — false positive merusak kredibilitas; (e) program — program tutup/berubah hadiah.
2. **Standar lulus:** daftar risiko tertulis per keluarga. Keluarga tanpa risiko tercatat = tulis "tidak ada" dengan alasan, jangan kosong.

### Gerbang 1 — Analisis likelihood × dampak

1. Untuk tiap risiko, nilai likelihood (rendah/sedang/tinggi) + dampak (rendah/sedang/tinggi) + alasan singkat. Hitung tingkat risiko: tinggi = likelihood tinggi + dampak tinggi; sedang = salah satu tinggi; rendah = keduanya rendah/sedang.
2. **Standar lulus:** tiap risiko punya likelihood + dampak + tingkat + alasan. Risiko tanpa nilai = belum dianalisis.

### Gerbang 2 — Mitigasi + kontrol

1. Untuk tiap risiko tingkat SEDANG dan TINGGI, tentukan mitigasi: hindari (jangan pakai teknik itu), kurangi (batasi rate/jadwal), transfer (serahkan keputusan ke Muse), atau terima (dengan alasan tertulis + batas). Catat kontrol yang dipakai (mis. `scope-and-safety-guardian` untuk risiko scope, jeda rate-limit untuk risiko akun).
2. **Standar lulus:** tiap risiko sedang/tinggi punya mitigasi + kontrol. Risiko tinggi tanpa mitigasi = putaran DITUNDA.

### Gerbang 3 — Rencana kelangsungan (business continuity)

1. Tulis rencana bila satu program bermasalah di tengah putaran: program cadangan mana yang diambil alih, hipotesis mana yang dipindah, dan siapa yang memutuskan perpindahan (Muse). Pastikan tidak ada putaran yang bergantung pada SATU program saja.
2. **Standar lulus:** rencana kelangsungan tertulis (program cadangan + pemindahan hipotesis + penanggung jawab). Tanpa rencana = putaran rapuh, perbaiki dulu.

### Gerbang 4 — Serahkan daftar risiko ke putaran

1. Serahkan daftar risiko + mitigasi + rencana kelangsungan yang sudah divalidasi A60 ke koordinator putaran. Skill ini BERHENTI di sini — eksekusi mengikuti pagar yang sudah ditetapkan.
2. **Standar lulus:** daftar risiko tercatat di log + validasi A60. Skill ini tidak mencatat "temuan" — hanya "risiko + mitigasi diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| `recon-pantau-program` | Data program (scope, hadiah, deadline, perubahan aturan) sebagai masukan risiko |
| `scope-and-safety-guardian` | Kontrol mitigasi risiko scope (gerbang sebelum eksekusi) |
| `penilaian-cvss` | Referensi severity bila risiko menyentuh nilai temuan |
| `analisis-risiko-kuantitatif-fair` | Lanjutan kuantitatif bila risiko butuh nilai dolar |
| `~/workspace/catatan/log-bug-bounty.md` | Log risiko putaran: daftar, analisis, mitigasi, kelangsungan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal/putaran) dengan format:

```
Tanggal putaran: [YYYY-MM-DD]
Program aktif: [daftar]
Risiko: [risiko ... — keluarga ... — likelihood ... — dampak ... — tingkat ...]
Mitigasi: [risiko ... — strategi: hindari/kurangi/transfer/terima — kontrol: ...]
Kelangsungan: [bila program ... bermasalah → cadangan ... — hipotesis pindah: ... — penanggung jawab: Muse]
Validasi A60: [ya/tidak]
Yang TIDAK dilakukan: [tanpa eksekusi berisiko tanpa mitigasi]
Status: [risiko diserahkan / putaran ditunda: alasan]
```

## Batasan yang diketahui

- Analisis risiko kualitatif (rendah/sedang/tinggi) bersifat perkiraan — likelihood dan dampak dinilai dari pengalaman putaran lalu + data program, bukan dari statistik formal. Bila butuh angka, lanjutkan ke `analisis-risiko-kuantitatif-fair`.
- Risiko baru bisa muncul di tengah putaran (program mengubah aturan mendadak). Daftar risiko bukan dokumen sekali tulis — tinjau ulang bila ada perubahan, dan hentikan eksekusi yang terkena perubahan sampai risikonya dinilai ulang.
- Mitigasi mengurangi risiko, tidak menghilangkannya. Risiko yang "diterima" tetap dicatat dan dipantau — jangan lupakan risiko yang sudah diterima.
- Skill ini tidak membahas manajemen risiko organisasi secara umum (ERM) atau risiko bisnis di luar perburuan. Fokusnya: risiko OPERASI perburuan bounty tim ini.
