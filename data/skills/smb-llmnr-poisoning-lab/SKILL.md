# Skill: SMB & LLMNR Poisoning Lab — Uji Keracunan Protokol Windows di Jaringan Sendiri

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 110. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: memanfaatkan kelemahan protokol berbagi file Windows (SMB, LLMNR/NBT-NS) di jaringan LAB SENDIRI untuk membuktikan apakah hash kata sandi bisa tertangkap — memakai akun dan hash CANARY milik sendiri. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Lab/jaringan sendiri SAJA; tanpa mencuri hash milik orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **huntr, Perplexity VDP, Mistral VDP**. Skill ini adalah skill LAB: hasil lab dipakai untuk memahami pola keracunan protokol dan menulis laporan hanya bila program mencantumkan aset Windows/jaringan yang relevan — temuan lab sendiri bukan temuan pada target program kecuali direproduksi pada aset in-scope sesuai pasal scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu menguji ketahanan jaringan Windows terhadap keracunan nama (LLMNR/NBT-NS poisoning): apakah klien lab sendiri mengirim hash autentikasi ke responder palsu saat meminta nama yang tidak ada, dan apakah hash canary itu tertangkap. Dipakai di lab Windows milik sendiri (minimal satu klien Windows + satu mesin responder, jaringan terisolasi). Dipakai SEBELUM mengklaim kerentanan relay/poisoning pada target program — lab membuktikan pola serangannya, target in-scope membuktikan relevansinya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Membangun lab Windows, menjalankan responder di jaringan sendiri, merekam hash canary |
| Pengerjaan | **A54 Penguji Live** | Memicu permintaan nama dari klien lab sendiri dan memeriksa hash yang tertangkap |
| Audit | **A60 Security Auditor** | Memvalidasi bukti lab sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- SMB relay (memakai ulang kredensial tertangkap ke sistem lain) → skill `smb-relay-ntlm-lab` (skill ini tentang PENANGKAPAN hash lewat poisoning, bukan relay-nya).
- Pass-the-Hash → skill `pass-the-hash-lab`.
- Eksploitasi layanan SMB usang (EternalBlue) → skill `eksploitasi-eternalblue-smb-lab`.
- MITM/ARP spoofing di lab → skill `mitm-arp-spoofing-lab`.
- Cracking kata sandi (Hydra/Hashcat) → skill `cracking-kata-sandi-hydra-hashcat` — hash canary yang tertangkap HANYA boleh diuji crack di lab sendiri.
- Serangan ADCS / pivoting → skill `serangan-adcs-esc-lab`, `pivoting-tunneling`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Semua mesin, akun Windows, dan hash dalam uji ini milik sendiri; kata sandi akun lab adalah kata sandi canary yang dibuat khusus untuk lab.
3. **Tanpa data orang lain.** Tanpa menangkap, menyimpan, atau memakai hash/kredensial milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR; tanpa hash milik orang lain.** Klien yang "tertipu" adalah mesin MILIK SENDIRI.
5. **Tanpa DoS/DDoS pada target program.** Responder hanya berjalan di lab sendiri.
6. **Tanpa payload di permukaan publik.** Alat dan konfigurasi lab tidak di-host/dibagikan di tempat umum.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menjalankan responder/poisoner di jaringan yang bukan milik sendiri. DILARANG menangkap hash orang lain. DILARANG memakai hash yang tertangkap untuk mengautentikasi ke sistem nyata apa pun (relay ke sistem nyata DILARANG — relay hanya dibahas di `smb-relay-ntlm-lab` dan tetap lab saja). DILARANG memecahkan (crack) hash selain hash canary milik sendiri. Setelah uji selesai, matikan responder, hapus hash canary dari log alat, dan kembalikan konfigurasi klien lab ke semula.

## Langkah + gerbang

### Gerbang 0 — Cek scope + bangun lab Windows terisolasi

1. Baca pasal scope program yang dituju; catat relevansi aset Windows/jaringan. Bangun lab terisolasi: minimal satu klien Windows + satu mesin responder, semua milik sendiri, jaringan TIDAK terhubung ke jaringan orang lain. Buat akun lab dengan kata sandi canary (unik, tidak dipakai di mana pun).
2. **Standar lulus:** lab terisolasi terbukti + akun canary tercatat. Lab belum terisolasi = jangan mulai.

### Gerbang 1 — Baseline: tanpa responder, apa yang terjadi

1. Dari klien lab, minta nama host yang tidak ada (mis. UNC path ke nama palsu) tanpa responder berjalan. Catat: apakah klien mengirim permintaan LLMNR/NBT-NS, dan apakah ada respons? Rekam lalu lintas dengan Wireshark/tcpdump.
2. **Standar lulus:** baseline tercatat (permintaan nama terlihat, tanpa respons). Tanpa baseline, dampak poisoning tidak terukur.

### Gerbang 2 — Jalankan responder di lab sendiri

1. Jalankan alat responder (mis. Responder) di mesin lab, HANYA mendengarkan di antarmuka jaringan lab. Dari klien lab, ulangi permintaan nama yang tidak ada. Amati apakah klien mengirim hash autentikasi ke responder.
2. **Standar lulus:** tercatat apakah hash canary tertangkap (ya/tidak) beserta jenis hashnya. Hash tidak tertangkap = hasil negatif yang valid — catat kenapa (mis. LLMNR sudah dimatikan) dan tutup.

### Gerbang 3 — Verifikasi hash itu milik sendiri dan hanya canary

1. Periksa hash yang tertangkap: pastikan berasal dari akun canary lab (cocokkan nama pengguna), dan pastikan TIDAK ada hash lain yang ikut tertangkap. Bila ada hash yang bukan canary, HENTIKAN uji, hapus data itu, dan laporkan ke Muse — itu pelanggaran batas lab.
2. **Standar lulus:** hanya hash canary yang tercatat; tidak ada hash lain. Pelanggaran batas = hentikan uji.

### Gerbang 4 — Matikan responder + nilai relevansi ke target program

1. Matikan responder, hapus hash canary dari penyimpanan alat, kembalikan konfigurasi klien lab. Nilai: apakah pola yang terbukti di lab relevan dengan aset in-scope program (mis. jaringan korporat target tanpa mitigasi LLMNR)? Bila ya, rancang reproduksi pada aset in-scope sesuai pasal scope; bila tidak, lab tetap dicatat sebagai pembelajaran.
2. **Standar lulus:** responder mati + hash canary dihapus + penilaian relevansi tertulis.

### Gerbang 5 — Tulis draf (bila relevan dengan target in-scope)

1. Tulis dampak konkret pada aset in-scope (bukan sekadar "hash tertangkap di lab"). Serahkan ke A60 audit → Muse → Cipta setuju → kirim.
2. **Standar lulus:** draf mengikuti format output + keputusan triase diputuskan A60, bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab Windows terisolasi (klien + responder, milik sendiri) | Satu-satunya jaringan tempat poisoning dilakukan |
| Alat responder (mis. Responder) | HANYA di lab sendiri, HANYA mendengarkan antarmuka lab |
| Wireshark / tcpdump | Merekam lalu lintas MILIK SENDIRI untuk bukti |
| Akun + kata sandi canary lab | Satu-satunya kredensial dalam uji ini; hash-nya satu-satunya hash yang boleh dicatat |
| `~/workspace/catatan/log-bug-bounty.md` | Log lab, baseline, hasil tiap gerbang, bukti, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [huntr / Perplexity VDP / Mistral VDP]
Lab: [jaringan milik sendiri — klien Windows + mesin responder]
Baseline: [permintaan nama tanpa responder — terlihat/tidak]
Hash tertangkap: [ya/tidak — jenis hash — akun canary saja]
Hash lain ikut tertangkap: [tidak ada — bila ada, uji dihentikan + dilaporkan]
Responder dimatikan + hash dihapus: [ya]
Relevansi target in-scope: [aset + pola yang sama — atau "hanya pembelajaran lab"]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program — lab hanya membuktikan pola; relevansi ke aset in-scope harus dibuktikan terpisah.
- LLMNR/NBT-NS yang sudah dimatikan (via Group Policy) atau SMB signing yang ditegakkan akan menggagalkan penangkapan — hasil "tidak tertangkap" adalah temuan negatif yang valid.
- Hash yang tertangkap TIDAK BOLEH di-crack kecuali hash canary milik sendiri, dan TIDAK BOLEH dipakai relay ke sistem nyata.
- Skill ini tidak membahas relay hash ke sistem lain (lihat `smb-relay-ntlm-lab`) atau MITM umum (lihat `mitm-arp-spoofing-lab`).
