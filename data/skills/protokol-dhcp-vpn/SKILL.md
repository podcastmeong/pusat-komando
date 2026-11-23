# Skill: Protokol DHCP VPN — Cara kerja DHCP dan VPN sebagai dasar pengujian permukaan jaringan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 21. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: lab sendiri; tanpa menyadap tunnel orang lain.

## Pemicu (kapan dipakai)

Dipakai sebagai dasar memahami permukaan jaringan: cara kerja DHCP (pemberian alamat otomatis) dan VPN (tunnel, enkripsi, misconfig umum) — agar pengujian permukaan jaringan berikutnya tepat sasaran. Dipelajari dan diuji di lab sendiri.

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
- Lab simulasi → skill `cisco-packet-tracer-lab` (No. 15).

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
11. **Lab sendiri saja.** Uji DHCP/VPN hanya pada server/jaringan lab milik sendiri; jangan menguji server DHCP/VPN orang lain atau milik program tanpa izin eksplisit.
12. **DILARANG menyadap tunnel VPN orang lain** — lalu lintas di dalam tunnel orang lain bukan milik penguji dan tidak boleh dibaca.

## Langkah + gerbang

### Gerbang 0 — Kuasai cara kerja DHCP

1. Uraikan alur DHCP (Discover–Offer–Request–Acknowledge), masa sewa (lease), dan apa yang diberikan server selain alamat IP (gateway, DNS, dan sebagainya).
2. **Standar lulus:** alur DORA tertulis dengan benar. Tanpa itu = jangan lanjut ke pengujian.

### Gerbang 1 — Kuasai cara kerja VPN

1. Uraikan cara kerja VPN: tunnel, enkripsi, autentikasi ujung tunnel, dan misconfig umum (mis. split tunneling yang membocorkan lalu lintas, kebocoran DNS, kill switch yang tidak ada).
2. **Standar lulus:** uraian tunnel + daftar misconfig umum tertulis. Misconfig tanpa penjelasan dampaknya = belum selesai.

### Gerbang 2 — Uji di lab sendiri

1. Bangun server DHCP dan tunnel VPN di lab sendiri; amati alurnya dengan lalu lintas sendiri (lihat No. 2) dan uji perilaku misconfig yang dipelajari — hanya di lab sendiri.
2. **Standar lulus:** hasil tiap uji lab tercatat. Uji yang gagal = dicatat penyebabnya.

### Gerbang 3 — Terapkan pemahaman ke target in-scope

1. Gunakan pemahaman ini untuk menafsirkan perilaku target in-scope yang teramati dari luar (mis. apakah layanan VPN target mengumumkan misconfig yang dikenal) — pengujian aktif pada target hanya bila program mengizinkan dan lewat gerbang skill terkait.
2. **Standar lulus:** tafsiran tertulis + rencana uji (bila ada) diserahkan ke A58.

## Alat

| Alat | Cara pakai |
|---|---|
| Server DHCP + VPN lab sendiri | Membangun dan menguji alur di lab |
| Wireshark (lalu lintas sendiri) | Mengamati alur DORA dan tunnel di lab |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Alur DHCP: [DORA + lease]
Misconfig VPN umum: [daftar + dampak]
Hasil uji lab: [per uji]
Scope guard dipatuhi: [ya — Scope guard: lab sendiri; tanpa menyadap tunnel orang lain.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- DHCP tanpa autentikasi berarti siapa pun di jaringan yang sama bisa menjadi server DHCP palsu — di lab sendiri hal ini dipelajari, di jaringan orang lain hal ini adalah serangan dan dilarang.
- VPN tidak otomatis aman — enkripsi yang lemah atau kebocoran DNS membatalkan perlindungan tunnel.
