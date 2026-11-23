# Skill: Cisco Packet Tracer Lab — Simulasi jaringan gratis sebelum menguji serangan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 15. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: lab simulasi saja; bukan target nyata.

## Pemicu (kapan dipakai)

Dipakai untuk BELAJAR dan BERLATIH di lab simulasi: membangun dan mengonfigurasi jaringan virtual (router, switch, PC) di Cisco Packet Tracer sebelum menguji konsep serangan di lab — tanpa menyentuh target nyata mana pun. Skill latihan, bukan skill pengujian target.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Model OSI/TCP-IP → skill `pemetaan-jaringan-osi-tcpip` (No. 3).
- Konfigurasi firewall/router/switch → skill `konfigurasi-firewall-router-switch` (No. 20).
- Protokol DHCP/VPN → skill `protokol-dhcp-vpn` (No. 21).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (SEMUA — kesembilan program (latihan; platform latihan saja)). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Lab simulasi saja — bukan target nyata.** Apa pun yang dibangun di Packet Tracer tidak boleh diterapkan ke jaringan nyata tanpa scope program dan gerbang skill terkait.
12. **Hasil lab bukan bukti kerentanan target nyata.** Temuan di simulasi hanya membuktikan pemahaman konsep; jangan melaporkannya sebagai temuan bounty.

## Langkah + gerbang

### Gerbang 0 — Tetapkan tujuan latihan

1. Tulis tujuan latihan (mis. memahami routing antar-subnet, mengonfigurasi ACL, menguji DHCP) dan topologi yang akan dibangun.
2. **Standar lulus:** tujuan + topologi tertulis sebelum membangun.

### Gerbang 1 — Bangun topologi di Packet Tracer

1. Bangun jaringan virtual sesuai topologi: perangkat, pengkabelan, pengalamatan IP (lihat No. 4), dan konfigurasi dasar tiap perangkat.
2. **Standar lulus:** topologi berjalan (ping antar-host dalam simulasi berhasil atau kegagalan tercatat dengan penyebabnya).

### Gerbang 2 — Konfigurasi dan uji konsep

1. Terapkan konfigurasi yang dilatih (routing, ACL, DHCP, NAT) dan uji perilakunya di simulasi: apakah lalu lintas mengalir sesuai harapan? Apakah aturan blokir bekerja?
2. **Standar lulus:** hasil tiap uji tercatat (berhasil/gagal + perilaku yang teramati).

### Gerbang 3 — Catat pelajaran untuk pengujian nyata

1. Tulis pelajaran yang bisa dipakai di pengujian nyata (dan batasnya: apa yang TIDAK bisa disimpulkan dari simulasi). Simpan topologi + catatan sebagai bahan latihan.
2. **Standar lulus:** catatan pelajaran tertulis. Latihan tanpa catatan = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| Cisco Packet Tracer | Membangun dan mengonfigurasi jaringan simulasi |
| Catatan topologi + hasil uji | Bahan latihan yang disimpan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Tujuan latihan: [tujuan]
Topologi: [perangkat + pengalamatan]
Pelajaran: [yang bisa dipakai + batasnya]
Scope guard dipatuhi: [ya — Scope guard: lab simulasi saja; bukan target nyata.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Packet Tracer adalah simulasi — perilaku perangkat nyata bisa berbeda (terutama firmware dan fitur keamanan); jangan menganggap hasil simulasi sama dengan hasil di perangkat nyata.
- Skill ini tidak memberi izin mengonfigurasi perangkat nyata.
