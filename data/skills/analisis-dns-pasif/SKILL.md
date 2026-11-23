# Skill: Analisis DNS Pasif — DNS pasif: riwayat record dan jejak subdomain tanpa menyentuh server target

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 13. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pasif; tanpa zone transfer paksa di luar scope.

## Pemicu (kapan dipakai)

Dipakai saat memetakan permukaan DNS target in-scope dari data historis dan publik: riwayat record, MX/TXT/SPF, dan jejak subdomain — tanpa mengirim query yang menyentuh server target secara agresif dan tanpa mencoba zone transfer.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Enumerasi subdomain → skill `enumerasi-subdomain`.
- Takeover subdomain → skill `deteksi-takeover-subdomain`.
- Spoofing TLS/DNS/email → skill `perburuan-tls-dns-email-spoofing`.

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
11. **Pasif saja.** Gunakan data DNS historis/publik dan resolver publik; jangan mencoba zone transfer (AXFR) atau query yang memaksa server target di luar scope.
12. **Data historis bisa kedaluwarsa** — record yang tercatat di arsip belum tentu masih aktif; verifikasi keaktifannya hanya lewat cara yang diizinkan program (mis. resolusi normal) sebelum mengklaim temuan.

## Langkah + gerbang

### Gerbang 0 — Cek scope + domain target

1. Tetapkan domain target in-scope dan baca pasal scope. Catat domainnya.
2. **Standar lulus:** domain tertulis. Tanpa itu = jangan mulai.

### Gerbang 1 — Kumpulkan riwayat record DNS

1. Dari data DNS historis/publik, kumpulkan record domain target: A/AAAA, MX, TXT (termasuk SPF/DKIM/DMARC bila ada), NS, dan CNAME. Catat tanggal riwayat bila tersedia.
2. **Standar lulus:** tabel record tertulis dengan sumber + tanggal. Record tanpa sumber = jangan dipakai.

### Gerbang 2 — Jejak subdomain dari data historis

1. Dari data historis (termasuk CT log yang sudah dipetakan skill lain), daftar subdomain yang pernah tercatat untuk domain target. Kelompokkan: masih aktif (menurut data terbaru), tidak aktif, dan tidak diketahui.
2. **Standar lulus:** daftar subdomain tertulis dengan statusnya. Subdomain tanpa status = ditandai "tidak diketahui".

### Gerbang 3 — Nilai temuan DNS

1. Nilai: apakah ada record yang aneh (mis. MX yang mengarah ke layanan yang tidak dikenal, TXT yang membocorkan layanan internal, subdomain yang mengarah ke layanan yang sudah tidak diklaim)? Serahkan kandidat ke A58.
2. **Standar lulus:** daftar kandidat tertulis + alasan. Tidak ada yang aneh = catat "bersih pada data ini" dan tutup.

## Alat

| Alat | Cara pakai |
|---|---|
| Data DNS historis/publik | Riwayat record dan jejak subdomain |
| Resolver publik (query normal) | Verifikasi record saat ini bila diizinkan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Domain: [domain in-scope]
Record: [A/MX/TXT/NS/CNAME + sumber]
Subdomain dari data historis: [daftar + status]
Scope guard dipatuhi: [ya — Scope guard: pasif; tanpa zone transfer paksa di luar scope.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Zone transfer (AXFR) pada server yang tidak mengizinkannya adalah upaya paksa — dilarang di luar scope.
- Record DNS berubah cepat; selalu catat tanggal data yang dipakai.
