# Skill: Konfigurasi Firewall Router Switch — Membaca postur keamanan jaringan dari konfigurasi perangkat

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 20. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: lab sendiri; tanpa menguji perangkat orang lain.

## Pemicu (kapan dipakai)

Dipakai untuk MEMAHAMI konfigurasi firewall, router, dan switch — aturan firewall, ACL, dan NAT — sebagai dasar membaca postur keamanan jaringan. Latihan dan analisis dilakukan pada perangkat/lab SENDIRI; bukan menguji perangkat orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Lab simulasi → skill `cisco-packet-tracer-lab` (No. 15).
- Model OSI/TCP-IP → skill `pemetaan-jaringan-osi-tcpip` (No. 3).
- Protokol DHCP/VPN → skill `protokol-dhcp-vpn` (No. 21).

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
11. **Lab/perangkat sendiri saja.** DILARANG membaca, menguji, atau mengubah konfigurasi firewall/router/switch milik orang lain atau milik program tanpa izin eksplisit di pasal scope.
12. **Jangan menerapkan konfigurasi lab ke perangkat nyata** tanpa scope program dan gerbang skill terkait.

## Langkah + gerbang

### Gerbang 0 — Tetapkan perangkat lab yang dipelajari

1. Tulis perangkat lab sendiri yang akan dipelajari (firewall/router/switch virtual atau fisik milik sendiri) dan tujuan pembelajarannya.
2. **Standar lulus:** perangkat + tujuan tertulis. Perangkat yang bukan milik sendiri = jangan dipakai.

### Gerbang 1 — Baca dan uraikan aturan

1. Pada perangkat lab sendiri, baca aturan firewall/ACL/NAT yang berlaku dan uraikan: lalu lintas apa yang diizinkan, apa yang diblokir, dan dalam urutan apa aturan dievaluasi (urutan menentukan hasil).
2. **Standar lulus:** uraian aturan tertulis dengan urutan evaluasinya. Aturan yang tidak dipahami = ditandai, bukan ditebak.

### Gerbang 2 — Uji perilaku aturan di lab

1. Uji di lab sendiri: kirim lalu lintas uji milik sendiri dan amati apakah aturan bekerja sesuai uraian (diizinkan/diblokir sesuai harapan). Catat penyimpangan antara uraian dan perilaku.
2. **Standar lulus:** hasil tiap uji tercatat. Penyimpangan dicatat sebagai pelajaran, bukan sebagai temuan bounty.

### Gerbang 3 — Terapkan pemahaman ke postur target

1. Gunakan pemahaman ini HANYA untuk menafsirkan perilaku target in-scope yang teramati dari luar (mis. port yang tertutup, respons yang diblokir) — tanpa menguji perangkat target secara langsung.
2. **Standar lulus:** tafsiran tertulis + batasnya (apa yang tidak bisa disimpulkan dari luar).

## Alat

| Alat | Cara pakai |
|---|---|
| Perangkat lab sendiri / Packet Tracer | Membaca dan menguji aturan firewall/ACL/NAT |
| Catatan aturan + hasil uji | Bahan pembelajaran yang disimpan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Perangkat lab: [perangkat milik sendiri]
Aturan diuraikan: [izin/blokir + urutan]
Tafsiran postur target: [perilaku luar + batasnya]
Scope guard dipatuhi: [ya — Scope guard: lab sendiri; tanpa menguji perangkat orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Aturan firewall dievaluasi berurutan — satu aturan 'allow' di atas bisa membatalkan 'deny' di bawahnya; selalu baca urutannya.
- NAT menyembunyikan topologi internal — jangan menyimpulkan struktur internal hanya dari alamat yang terlihat dari luar.
