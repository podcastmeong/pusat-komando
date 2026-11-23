# Skill: Penemuan Perangkat Jaringan — Menemukan perangkat aktif dalam satu jaringan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 6. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya jaringan sendiri/lab; tanpa memindai jaringan orang lain.

## Pemicu (kapan dipakai)

Dipakai sebagai langkah awal pemetaan permukaan jaringan: menemukan perangkat (host) aktif dalam satu jaringan sebelum memindai port atau layanan. HANYA pada jaringan sendiri atau lab sendiri — bukan jaringan orang lain dan bukan jaringan program (kecuali program secara eksplisit mengizinkan host discovery pada asetnya).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Perhitungan rentang jaringan → skill `alamat-ip-subnetting-cidr` (No. 4).
- Pemindaian port setelah host ditemukan → skill `pemindaian-port-layanan`.
- Pemetaan rute → skill `pemetaan-rute-traceroute` (No. 22).

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
11. **HANYA jaringan sendiri/lab sendiri.** DILARANG melakukan host discovery pada jaringan orang lain, jaringan kantor/organisasi yang bukan milik sendiri, atau jaringan program yang tidak mencantumkan izin ini.
12. **Gunakan metode paling ringan dulu** (mis. ping/ARP pada lab sendiri) dan berhenti bila perangkat sudah terpetakan — jangan mengulang-ulang pemindaian.

## Langkah + gerbang

### Gerbang 0 — Cek scope + jaringan yang boleh dipindai

1. Tetapkan jaringan yang dipindai: HANYA jaringan lab sendiri atau jaringan milik sendiri. Tulis rentang CIDR-nya (lihat No. 4). Bila jaringan itu bukan milik sendiri = BERHENTI.
2. **Standar lulus:** jaringan + pemiliknya tercatat ("milik sendiri/lab"). Tanpa itu = jangan mulai.

### Gerbang 1 — Temukan host aktif

1. Jalankan host discovery ringan pada jaringan sendiri (mis. ping sweep atau ARP scan pada lab). Catat tiap host aktif: alamat IP, alamat MAC (bila terlihat), dan nama host bila diumumkan perangkat itu sendiri.
2. **Standar lulus:** daftar host aktif tertulis. Host yang tidak merespons = dicatat "tidak merespons", bukan diasumsikan mati — bisa jadi firewall yang memblokir ping.

### Gerbang 2 — Klasifikasikan perangkat

1. Kelompokkan host yang ditemukan menurut peran yang terlihat: router/gateway, server, workstation, perangkat IoT lab, dan sebagainya — hanya dari informasi yang diumumkan perangkat itu sendiri.
2. **Standar lulus:** klasifikasi tertulis per host. Klasifikasi yang tidak berdasar bukti = ditandai "dugaan".

### Gerbang 3 — Serahkan peta host

1. Serahkan daftar host ke A58 untuk diputuskan mana yang relevan dengan tujuan (latihan lab atau pemetaan permukaan program bila diizinkan). Jangan lanjut memindai port host yang tidak relevan.
2. **Standar lulus:** peta host tertulis + keputusan host mana yang dilanjutkan. Peta tanpa keputusan = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| ping / ARP scan (lab sendiri) | Host discovery ringan pada jaringan sendiri |
| Nmap mode host discovery (`-sn`, lab sendiri) | Daftar host aktif tanpa pemindaian port |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Jaringan dipindai: [CIDR — milik sendiri/lab]
Host aktif: [IP + MAC + nama bila ada]
Klasifikasi: [peran per host]
Scope guard dipatuhi: [ya — Scope guard: hanya jaringan sendiri/lab; tanpa memindai jaringan orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Host yang tidak merespons ping belum tentu mati — banyak host memblokir ICMP; jangan menyimpulkan ketiadaan dari satu metode.
- Skill ini untuk jaringan sendiri/lab; pemetaan host pada aset program hanya bila program secara eksplisit mengizinkannya.
