# Skill: Pemantauan Perubahan Target — Memantau perubahan target in-scope sebagai pemicu perburuan ulang

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 19. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya target in-scope; tanpa pemindaian agresif.

## Pemicu (kapan dipakai)

Dipakai secara berkala selama program bounty berjalan: memantau apakah target in-scope berubah (endpoint baru, halaman baru, perubahan teknologi, fitur baru) — perubahan adalah pemicu untuk mengulang perburuan, karena permukaan baru berarti peluang temuan baru.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pemetaan permukaan agen AI → skill `spionase-permukaan-agen-ai` (No. 1) — peta yang diperbarui saat ada perubahan.
- Pemetaan teknologi/stack → skill `pemetaan-teknologi-stack` (No. 11).
- Pemantauan sertifikat baru → skill `pemantauan-sertifikat-baru` (No. 24).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Muse). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Hanya target in-scope, dengan cara pasif/ringan.** Pemantauan dilakukan lewat sumber publik dan request normal; jangan memakai pemindaian agresif atau fuzzing berulang sebagai 'pemantauan'.
12. **Perubahan di luar scope bukan target.** Bila target berubah di luar area in-scope, catat saja — jangan mengujinya.

## Langkah + gerbang

### Gerbang 0 — Tetapkan baseline

1. Tulis baseline target in-scope: daftar endpoint/halaman/teknologi saat ini (dari peta No. 1 dan No. 11) + tanggal baseline.
2. **Standar lulus:** baseline tertulis + tanggalnya. Tanpa baseline = perubahan tidak bisa dikenali.

### Gerbang 1 — Periksa perubahan berkala

1. Pada jadwal yang ditetapkan (mis. mingguan), periksa target in-scope dengan cara ringan: halaman kunci masih sama? Ada endpoint/halaman baru? Teknologi berubah? Catat tiap perbedaan dari baseline.
2. **Standar lulus:** hasil tiap pemeriksaan tercatat (berubah/tidak + apa yang berubah). Pemeriksaan tanpa catatan = tidak terjadi.

### Gerbang 2 — Klasifikasikan perubahan

1. Kelompokkan perubahan: permukaan baru (endpoint/fitur baru), perubahan teknologi, perubahan perilaku, atau hanya perubahan konten. Tandai mana yang in-scope.
2. **Standar lulus:** klasifikasi tertulis per perubahan. Perubahan di luar scope = ditandai "di luar scope".

### Gerbang 3 — Picu perburuan ulang

1. Untuk perubahan in-scope yang menambah permukaan, perbarui peta (No. 1/No. 11) dan serahkan ke A58 sebagai pemicu perburuan ulang dengan hipotesis baru.
2. **Standar lulus:** peta diperbarui + pemicu perburuan tercatat. Perubahan tanpa tindak lanjut = pemantauan yang sia-sia.

## Alat

| Alat | Cara pakai |
|---|---|
| Baseline peta (No. 1/No. 11) | Pembanding perubahan |
| Request normal / sumber publik | Pemeriksaan ringan berkala |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Baseline: [tanggal + isi ringkas]
Perubahan terdeteksi: [apa + tanggal + klasifikasi]
Pemicu perburuan: [ya/tidak + hipotesis baru]
Scope guard dipatuhi: [ya — Scope guard: hanya target in-scope; tanpa pemindaian agresif.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Perubahan kecil (teks, gambar) biasanya bukan permukaan baru — fokus pada endpoint, fitur, dan teknologi.
- Jangan memantau dengan frekuensi yang membanjiri server; jadwal berkala yang wajar sudah cukup.
