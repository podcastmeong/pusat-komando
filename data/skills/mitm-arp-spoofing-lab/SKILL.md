# Skill: MITM & ARP Spoofing Lab — Uji Ketahanan Jaringan Sendiri di Lab

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 109. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: memposisikan diri di tengah komunikasi di jaringan LAB SENDIRI untuk membuktikan apakah lalu lintas bisa dicegat/diubah — dan apakah pertahanan (enkripsi, HSTS, certificate pinning) menahannya. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Lab/jaringan SENDIRI saja; tanpa mencegat, mengubah, atau membaca komunikasi milik orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **huntr, Perplexity VDP, Mistral VDP**. Skill ini adalah skill LAB: hasil lab dipakai untuk memahami pola serangan dan menulis laporan hanya bila program mencantumkan aset jaringan/aplikasi yang relevan — temuan lab sendiri bukan temuan pada target program kecuali direproduksi pada aset in-scope sesuai pasal scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu menguji ketahanan jaringan/aplikasi terhadap posisi man-in-the-middle: apakah klien di lab sendiri menerima sertifikat palsu, apakah lalu lintas plaintext (HTTP, DNS, kredensial tanpa TLS) bocor saat ARP diracuni, apakah aplikasi menolak koneksi yang dicegat. Dipakai di lab yang dibangun sendiri (dua mesin/VM + router/AP milik sendiri, jaringan terisolasi dari jaringan orang lain). Dipakai SEBELUM mengklaim kerentanan MITM pada target program — lab membuktikan pola serangannya, target in-scope membuktikan relevansinya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Membangun lab, meracuni ARP di jaringan sendiri, merekam lalu lintas sendiri |
| Pengerjaan | **A54 Penguji Live** | Menjalankan klien korban (mesin sendiri) dan memeriksa apa yang bocor/berubah |
| Audit | **A60 Security Auditor** | Memvalidasi bukti lab sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Membaca paket jaringan (Wireshark/tcpdump) → skill `analisis-lalu-lintas-wireshark` (skill ini MEMAKAI analisis paket di lab MITM, bukan mengulang teorinya).
- Penemuan perangkat dalam satu jaringan → skill `penemuan-perangkat-jaringan`.
- Pemetaan jaringan OSI/TCP/IP, DHCP/VPN, traceroute → skill `pemetaan-jaringan-osi-tcpip`, `protokol-dhcp-vpn`, `pemetaan-rute-traceroute`.
- Simulasi jaringan → skill `cisco-packet-tracer-lab`.
- Uji ketahanan DoS pada layanan sendiri → skill `ketahanan-dos-lab-sendiri`.
- Keracunan SMB/LLMNR di lab → skill `smb-llmnr-poisoning-lab`; deauth Wi-Fi di lab → skill `serangan-deauth-wifi-lab`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Semua mesin, klien, dan data dalam uji ini milik sendiri; kredensial yang dipakai adalah kredensial palsu/canary lab.
3. **Tanpa data orang lain.** Tanpa membaca, menyimpan, atau memakai lalu lintas/komunikasi milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR; tanpa mencegat komunikasi orang lain.** Korban dalam lab adalah mesin MILIK SENDIRI yang sengaja diposisikan sebagai klien.
5. **Tanpa DoS/DDoS pada target program.** Peracunan ARP hanya di lab sendiri; jangan membanjiri jaringan apa pun.
6. **Tanpa payload di permukaan publik.** Alat dan skrip lab tidak di-host/dibagikan di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG meracuni ARP di jaringan yang bukan milik sendiri (jaringan kantor, kampus, kafe, tetangga, atau jaringan program). DILARANG mencegat, mengubah, atau mencuri lalu lintas orang lain. DILARANG memakai hasil lab untuk menyerang layanan nyata. Setelah uji selesai, pulihkan tabel ARP semua mesin lab ke kondisi semula dan matikan alat peracun.

## Langkah + gerbang

### Gerbang 0 — Cek scope + bangun lab terisolasi

1. Baca pasal scope program yang dituju; catat apakah pengujian jaringan/MITM relevan dengan aset in-scope. Bangun lab terisolasi: router/AP milik sendiri, minimal dua mesin (penyerang + klien) milik sendiri, jaringan yang TIDAK terhubung ke jaringan orang lain. Catat alamat IP/MAC semua mesin lab.
2. **Standar lulus:** lab terisolasi terbukti (daftar mesin + jaringan milik sendiri) dan pasal scope tercatat. Lab belum terisolasi = jangan mulai.

### Gerbang 1 — Baseline: lalu lintas normal tanpa racun

1. Dari klien lab, akses layanan canary milik sendiri (HTTP dan HTTPS) tanpa peracunan. Rekam dengan Wireshark/tcpdump: apa yang terlihat plaintext, apakah sertifikat divalidasi, apakah HSTS aktif.
2. **Standar lulus:** baseline tercatat (apa yang bocor tanpa MITM vs apa yang terlindungi). Tanpa baseline, dampak MITM tidak terukur.

### Gerbang 2 — Racuni ARP di lab sendiri

1. Dari mesin penyerang lab, kirim ARP reply palsu yang mengaitkan IP gateway dengan MAC mesin penyerang — HANYA untuk IP gateway dan klien lab milik sendiri. Verifikasi tabel ARP klien berubah ke MAC penyerang.
2. **Standar lulus:** tabel ARP klien lab menunjuk MAC penyerang (terbukti dengan `arp -a` / tangkapan paket). Bila tabel tidak berubah = racun gagal, catat kenapa dan tutup.

### Gerbang 3 — Amati apa yang bisa dicegat/diubah

1. Dengan posisi MITM aktif, ulangi akses klien ke layanan canary: (a) HTTP plaintext — apakah kredensial canary terlihat? (b) HTTPS — apakah klien menolak sertifikat palsu, atau menerima? (c) DNS — apakah respons bisa diubah? Rekam semuanya; pakai HANYA kredensial canary palsu.
2. **Standar lulus:** tiap varian tercatat (terlihat/ditolak/diterima) dengan bukti tangkapan paket. Klaim tanpa tangkapan = belum terbukti.

### Gerbang 4 — Pulihkan + nilai relevansi ke target program

1. Hentikan peracunan, pulihkan tabel ARP semua mesin lab, verifikasi konektivitas normal kembali. Nilai: apakah pola yang terbukti di lab relevan dengan aset in-scope program (mis. aplikasi target tanpa HSTS, layanan tanpa TLS)? Bila ya, rancang reproduksi pada aset in-scope sesuai pasal scope; bila tidak, lab tetap dicatat sebagai pembelajaran.
2. **Standar lulus:** ARP pulih + konektivitas normal terverifikasi + penilaian relevansi tertulis. Tanpa pemulihan = uji belum selesai.

### Gerbang 5 — Tulis draf (bila relevan dengan target in-scope)

1. Tulis dampak konkret pada aset in-scope (bukan sekadar "MITM mungkin di lab"). Serahkan ke A60 audit → Muse → Cipta setuju → kirim.
2. **Standar lulus:** draf mengikuti format output + keputusan triase diputuskan A60, bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab terisolasi (router/AP + 2 mesin/VM milik sendiri) | Satu-satunya jaringan tempat peracunan ARP dilakukan |
| Alat peracun ARP (mis. arpspoof / Ettercap) | HANYA di lab sendiri, HANYA terhadap IP lab sendiri |
| Wireshark / tcpdump | Merekam lalu lintas MILIK SENDIRI untuk bukti |
| Kredensial canary palsu | Satu-satunya kredensial yang boleh terlihat dalam tangkapan |
| `~/workspace/catatan/log-bug-bounty.md` | Log lab, baseline, hasil tiap gerbang, bukti, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [huntr / Perplexity VDP / Mistral VDP]
Lab: [jaringan milik sendiri — router/AP + mesin penyerang + mesin klien, IP/MAC]
Baseline: [lalu lintas normal — apa yang plaintext / terlindungi]
Racun ARP: [IP gateway + klien lab — tabel ARP berubah: ya/tidak]
Yang dicegat: [HTTP plaintext: ... | HTTPS sertifikat palsu: ditolak/diterima | DNS: ...]
Kredensial dipakai: [canary palsu saja — tanpa kredensial nyata/orang lain]
ARP dipulihkan: [ya — konektivitas normal terverifikasi]
Relevansi target in-scope: [aset + pola yang sama — atau "hanya pembelajaran lab"]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program — lab hanya membuktikan pola; relevansi ke aset in-scope harus dibuktikan terpisah.
- HTTPS dengan validasi sertifikat yang benar dan HSTS akan menolak MITM — hasil "ditolak" adalah temuan negatif yang valid, catat apa adanya.
- Sebagian jaringan modern memakai Dynamic ARP Inspection / port security yang memblokir racun ARP — bila racun gagal karena itu, catat sebagai pertahanan yang bekerja.
- Skill ini tidak membahas pencurian hash (lihat `smb-llmnr-poisoning-lab`) atau pemutusan klien Wi-Fi (lihat `serangan-deauth-wifi-lab`).
