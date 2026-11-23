# Skill: Pemantauan Sertifikat Baru — Memantau sertifikat TLS baru untuk domain target

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 24. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: data CT publik; tanpa menyentuh server target.

## Pemicu (kapan dipakai)

Dipakai sebagai peringatan dini: memantau sertifikat TLS baru yang diterbitkan untuk domain target in-scope lewat Certificate Transparency (CT) log publik — sertifikat baru sering menandakan subdomain atau aset baru sebelum diumumkan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis DNS pasif → skill `analisis-dns-pasif` (No. 13).
- Enumerasi subdomain → skill `enumerasi-subdomain`.
- Pemantauan perubahan target → skill `pemantauan-perubahan-target` (No. 19).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Data CT publik saja; tanpa menyentuh server target.** Pemantauan dilakukan lewat CT log publik — jangan memindai atau menguji server dari sertifikat baru sampai program mengonfirmasi aset itu in-scope.
12. **Sertifikat baru BUKAN otomatis aset in-scope.** Banyak sertifikat diterbitkan untuk pengujian internal atau otomatisasi; verifikasi status scope-nya dulu sebelum menguji.

## Langkah + gerbang

### Gerbang 0 — Tetapkan baseline + sumber CT

1. Tulis domain target in-scope dan sumber CT log publik yang akan dipantau, beserta baseline sertifikat yang sudah dikenal.
2. **Standar lulus:** domain + sumber + baseline tertulis. Tanpa baseline = sertifikat baru tidak bisa dikenali.

### Gerbang 1 — Pantau sertifikat baru berkala

1. Pada jadwal yang ditetapkan, periksa CT log publik untuk domain target: adakah sertifikat baru (nama domain/subdomain baru, tanggal terbit)? Catat tiap sertifikat baru dengan tanggalnya.
2. **Standar lulus:** hasil tiap pemeriksaan tercatat (ada/tidak ada sertifikat baru + detailnya). Pemeriksaan tanpa catatan = tidak terjadi.

### Gerbang 2 — Klasifikasikan sertifikat baru

1. Kelompokkan sertifikat baru: subdomain baru, perpanjangan sertifikat lama, sertifikat wildcard, atau sertifikat untuk layanan yang sudah dikenal. Tandai mana yang menandakan aset baru.
2. **Standar lulus:** klasifikasi tertulis per sertifikat. Sertifikat tanpa klasifikasi = ditandai "belum diklasifikasi".

### Gerbang 3 — Verifikasi scope lalu picu perburuan

1. Untuk sertifikat yang menandakan aset baru, verifikasi dulu apakah aset itu in-scope menurut program. Bila ya, perbarui peta (No. 1/No. 19) dan serahkan ke A58 sebagai pemicu perburuan ulang.
2. **Standar lulus:** status scope tiap aset baru tercatat + pemicu perburuan (bila in-scope) diserahkan. Aset di luar scope = dicatat saja.

## Alat

| Alat | Cara pakai |
|---|---|
| CT log publik (mis. crt.sh) | Memantau sertifikat baru untuk domain target |
| Baseline peta (No. 1/No. 19) | Pembanding aset baru |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Domain dipantau: [domain in-scope]
Sertifikat baru: [subdomain + tanggal terbit + klasifikasi]
Aset baru in-scope: [ya/tidak + tindak lanjut]
Scope guard dipatuhi: [ya — Scope guard: data CT publik; tanpa menyentuh server target.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- CT log bisa terlambat beberapa jam — sertifikat yang baru diterbitkan belum tentu langsung muncul; jangan menyimpulkan 'tidak ada sertifikat baru' dari satu pemeriksaan.
- Sertifikat wildcard mencakup banyak subdomain — jangan menganggap tiap nama di balik wildcard sebagai aset baru yang terkonfirmasi.
