# Skill: Alamat IP Subnetting CIDR — Menghitung rentang IP dan memetakan ruang lingkup target

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 4. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: pengetahuan dasar; tanpa pemindaian di luar scope.

## Pemicu (kapan dipakai)

Dipakai saat membaca pasal scope program yang ditulis dalam CIDR (mis. 203.0.113.0/24) atau saat perlu menghitung alamat jaringan, broadcast, dan jumlah host dari sebuah rentang — untuk memastikan uji hanya menyentuh alamat yang in-scope. Dipakai SEBELUM pemindaian apa pun.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penemuan perangkat dalam satu jaringan → skill `penemuan-perangkat-jaringan` (No. 6).
- Pemindaian port/layanan → skill `pemindaian-port-layanan`.
- Pemetaan rute → skill `pemetaan-rute-traceroute` (No. 22).

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
11. **Menghitung rentang BUKAN izin memindai rentang itu.** Rentang yang dihitung hanya boleh dipindai bila pasal scope program secara eksplisit mencantumkannya; rentang di luar scope tetap dilarang walau sudah dihitung.
12. **Bedakan IP publik vs privat** — alamat privat (10/8, 172.16/12, 192.168/16) di lab sendiri bukan target program; jangan mengujinya sebagai target program.

## Langkah + gerbang

### Gerbang 0 — Kuasai notasi CIDR

1. Bisa mengubah CIDR ke netmask dan sebaliknya (mis. /24 = 255.255.255.0), serta menghitung alamat jaringan, alamat broadcast, rentang host, dan jumlah host.
2. **Standar lulus:** perhitungan untuk satu CIDR contoh dikerjakan dengan benar dan bisa diulang tanpa kalkulator daring.

### Gerbang 1 — Terapkan pada pasal scope

1. Ambil pasal scope program dan tulis tiap rentang CIDR yang tercantum beserta alamat jaringan, broadcast, dan jumlah host-nya. Tandai rentang yang in-scope vs di luar scope.
2. **Standar lulus:** tabel rentang scope tertulis. Scope yang tidak ditulis dalam CIDR (mis. hanya nama domain) = catat sebagai "bukan rentang IP — jangan dipindai sebagai rentang".

### Gerbang 2 — Bedakan publik, privat, dan NAT

1. Untuk tiap alamat yang ditemui, klasifikasikan: publik, privat, loopback, link-local, atau CGNAT; dan catat bagaimana NAT memengaruhi apa yang terlihat dari luar (alamat privat di balik NAT tidak bisa dijangkau langsung dari internet).
2. **Standar lulus:** klasifikasi tiap alamat tercatat. Alamat yang tidak bisa diklasifikasikan = jangan diasumsikan in-scope.

### Gerbang 3 — Tetapkan batas uji

1. Tulis daftar alamat IP yang BOLEH diuji (hanya yang tercantum di scope) dan serahkan ke skill pemindaian terkait. Batas ini mengikat semua uji berikutnya.
2. **Standar lulus:** daftar alamat yang boleh diuji tertulis dan disetujui Muse/A60 sebelum pemindaian dimulai.

## Alat

| Alat | Cara pakai |
|---|---|
| Kalkulator subnet (offline/lokal) | Menghitung jaringan, broadcast, dan jumlah host dari CIDR |
| Pasal scope program | Sumber kebenaran rentang yang in-scope |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Rentang scope: [CIDR + jaringan + broadcast + jumlah host]
Alamat yang boleh diuji: [daftar — hanya dari scope]
Scope guard dipatuhi: [ya — Scope guard: pengetahuan dasar; tanpa pemindaian di luar scope.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- IPv6 memakai notasi dan aturan yang berbeda (prefix /64 dst.) — jangan menerapkan aturan IPv4 mentah-mentah ke IPv6; hitung terpisah bila scope menyebut IPv6.
- NAT bisa menyembunyikan banyak host di balik satu IP publik — satu IP publik bukan berarti satu host.
