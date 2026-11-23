# Skill: Pemetaan Rute Traceroute — Traceroute dan pemetaan rute jaringan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga SPIONASE No. 22. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Di luar target in-scope program = tidak boleh dipakai. Scope guard: hanya target in-scope; tanpa memetakan jaringan pihak ketiga.

## Pemicu (kapan dipakai)

Dipakai saat perlu memahami topologi dan hop antara penguji dan target in-scope: menjalankan traceroute ke target in-scope dan memetakan rute yang dilalui paket. Hanya ke target in-scope — bukan memetakan jaringan pihak ketiga.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan langkah pemetaan/recon sesuai gerbang di bawah, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis dari peta permukaan + menentukan temuan mana yang layak diuji lanjut |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Model OSI/TCP-IP → skill `pemetaan-jaringan-osi-tcpip` (No. 3).
- Alamat IP/subnetting → skill `alamat-ip-subnetting-cidr` (No. 4).
- Penemuan perangkat jaringan → skill `penemuan-perangkat-jaringan` (No. 6).

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
11. **Hanya target in-scope.** Jalankan traceroute hanya ke host yang tercantum di pasal scope program; jangan memakai traceroute untuk memetakan jaringan pihak ketiga atau infrastruktur di luar scope.
12. **Traceroute adalah pengukuran, bukan pemindaian agresif** — jalankan dengan frekuensi wajar dan hentikan bila target tidak merespons; jangan mengulang-ulang secara agresif.

## Langkah + gerbang

### Gerbang 0 — Cek scope + target

1. Tetapkan host target in-scope dan baca pasal scope. Catat hostnya.
2. **Standar lulus:** host tertulis. Host di luar scope = jangan di-traceroute.

### Gerbang 1 — Jalankan traceroute

1. Jalankan traceroute (ICMP/UDP/TCP sesuai yang diizinkan) dari perangkat sendiri ke target in-scope. Simpan output mentah dengan tanggal dan waktu.
2. **Standar lulus:** output tersimpan + tanggalnya. Output tanpa tanggal = tidak bisa dibandingkan nanti.

### Gerbang 2 — Petakan hop dan topologi

1. Uraikan tiap hop: alamat IP, nama host bila diumumkan, dan waktu respons. Tandai hop yang tidak merespons (bintang) — itu biasa (firewall memblokir ICMP), bukan bukti ketiadaan.
2. **Standar lulus:** daftar hop tertulis dengan status tiap hop. Hop tanpa respons dicatat "tidak merespons", bukan diisi tebakan.

### Gerbang 3 — Tafsirkan dan serahkan

1. Tafsirkan: berapa hop ke target, apakah rute melewati jaringan yang dikenal (CDN, penyedia cloud), dan apakah ada hop yang aneh. Serahkan peta rute ke A58 bila relevan dengan pengujian lanjut.
2. **Standar lulus:** tafsiran tertulis + peta rute diserahkan. Rute yang tidak ditafsirkan = belum selesai.

## Alat

| Alat | Cara pakai |
|---|---|
| traceroute / tracert / mtr | Memetakan hop ke target in-scope |
| Catatan hop + waktu | Peta rute yang disimpan |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [nama program bounty]
Target: [aset in-scope]
Target: [host in-scope]
Hop: [daftar IP + waktu + status]
Tafsiran: [jumlah hop + jaringan yang dilalui]
Scope guard dipatuhi: [ya — Scope guard: hanya target in-scope; tanpa memetakan jaringan pihak ketiga.]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hop yang tidak merespons sangat umum — jangan menyimpulkan topologi dari hop yang hilang.
- Rute bisa berubah antar-waktu (load balancing, perubahan routing); catat tanggal tiap pengukuran dan jangan membandingkan pengukuran dari tanggal berbeda tanpa menyebutkannya.
