# Skill: Pemetaan Jaringan OSI TCP/IP — Model OSI & TCP/IP sebagai dasar membaca lalu lintas

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 3. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pengetahuan dasar; tanpa target di luar program.

## Pemicu (kapan dipakai)

Dipakai sebagai fondasi sebelum pekerjaan jaringan apa pun: saat perlu memahami di lapisan mana sebuah perilaku terjadi (fisik, data link, jaringan, transport, sesi, presentasi, aplikasi — atau model TCP/IP 4 lapis), dan saat membaca lalu lintas atau merancang uji jaringan. Dipakai di awal, bukan saat sudah menguji.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Analisis paket konkret → skill `analisis-lalu-lintas-wireshark` (No. 2).
- Pemindaian port/layanan → skill `pemindaian-port-layanan`.
- Pengujian jaringan aktif → skill dalam keluarga ini (No. 4, 5, 6, 14, 20, 21, 22).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (SEMUA — kesembilan program (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr)). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh data pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyimpan, atau memakai data milik orang lain — termasuk data yang "ikut terkirim" dalam respons.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.** Jeda antar-request, volume kecil, jangan membanjiri server target.
6. **Tanpa payload di permukaan publik.** Jangan meng-host halaman/probe di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi/skrip hanya di program yang mengizinkannya; baca pasal scope dulu sebelum memakai alat otomatis apa pun.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, konfigurasi, atau layanan apa pun. Pembuktian HARUS aman dan non-destruktif; bila satu-satunya cara membuktikan bersifat destruktif, BERHENTI dan serahkan ke Muse.
11. **Skill ini adalah pengetahuan dasar, bukan izin menguji.** Memahami OSI/TCP-IP tidak memberi izin memindai atau menguji jaringan apa pun — setiap uji tetap butuh scope program + gerbang skill terkait.

## Langkah + gerbang

### Gerbang 0 — Kuasai modelnya

1. Hafal dan bisa menjelaskan 7 lapis OSI (Fisik, Data Link, Jaringan, Transport, Sesi, Presentasi, Aplikasi) dan 4 lapis TCP/IP (Akses Jaringan, Internet, Transport, Aplikasi) beserta pemetaan antar-keduanya.
2. **Standar lulus:** bisa memetakan satu protokol ke lapisnya tanpa menebak (mis. IP = lapis Jaringan/Internet, TCP/UDP = Transport, HTTP/DNS = Aplikasi).

### Gerbang 1 — Petakan enkapsulasi

1. Untuk satu alur komunikasi (mis. permintaan HTTP dari klien sendiri ke target in-scope), uraikan bagaimana data dibungkus lapis demi lapis: segmen TCP → paket IP → frame Ethernet → bit fisik, dan sebaliknya saat diterima.
2. **Standar lulus:** uraian enkapsulasi tertulis untuk satu alur nyata milik sendiri. Tanpa uraian = fondasi belum siap.

### Gerbang 2 — Terapkan pada pembacaan lalu lintas

1. Ambil satu tangkapan lalu lintas sendiri (lihat No. 2) dan identifikasi tiap lapis pada satu paket: alamat MAC, alamat IP, port TCP/UDP, dan muatan aplikasi.
2. **Standar lulus:** identifikasi tiap lapis tercatat untuk minimal satu paket. Bila tidak bisa membaca satu paket sampai lapis aplikasi = ulangi Gerbang 1.

### Gerbang 3 — Gunakan untuk merancang uji

1. Saat merancang uji jaringan berikutnya, tulis dulu di lapis mana uji itu bekerja dan lapis mana yang TIDAK disentuh — ini mencegah uji melebar ke luar scope.
2. **Standar lulus:** setiap rencana uji mencantumkan lapis yang diuji. Rencana tanpa lapis = belum siap dieksekusi.

## Alat

| Alat | Cara pakai |
|---|---|
| Diagram model OSI/TCP-IP + catatan enkapsulasi | Rujukan saat membaca paket dan merancang uji |
| Wireshark (lalu lintas sendiri) | Latihan membaca lapis pada paket nyata milik sendiri |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Model diterapkan: [OSI/TCP-IP]
Alur yang diuraikan: [klien sendiri → target in-scope]
Lapis yang akan diuji berikutnya: [lapis + alasan]
Scope guard dipatuhi: [ya — Scope guard: pengetahuan dasar; tanpa target di luar program.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Model OSI adalah model konseptual — implementasi nyata (terutama TCP/IP) tidak selalu memisahkan lapis Sesi/Presentasi secara tegas; jangan memaksakan pemetaan yang tidak ada.
- Skill ini tidak membahas serangan per lapis; serangan dibahas skill masing-masing dengan scope guard-nya.
