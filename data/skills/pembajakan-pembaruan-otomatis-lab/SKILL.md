# Skill: Pembajakan Pembaruan Otomatis Lab — Uji Kanal Update Sistem Sendiri di Lab

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, Keluarga SABOTASE No. 117. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi wajib — apa itu "sabotase" di bounty

**"Sabotase" di bounty BUKAN merusak sistem orang lain — melainkan membuktikan dampak pada akun/sistem SENDIRI dengan canary.** Untuk skill ini: menguji kanal pembaruan otomatis pada sistem SENDIRI di lab — apakah pembaruan bisa dibajak/diganti (mis. paket update yang tidak ditandatangani, kanal HTTP tanpa TLS, validasi tanda tangan yang longgar) — memakai paket canary milik sendiri. Pembeda sah vs dilarang: **sah = dampak dibuktikan pada milik sendiri dengan canary; dilarang = dampak menimpa orang lain atau layanan.** Tanpa korban nyata, tanpa merusak layanan, tanpa data orang lain. **Sistem sendiri/lab SAJA; tanpa membajak pembaruan orang lain.**

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini (kolom Program laporan): **huntr, Perplexity VDP, Mistral VDP, Anthropic**. Skill ini adalah skill LAB — terinspirasi temuan tim $1rb soal auto-update Mac: pola yang diuji di lab dipakai untuk memahami kelas kerentanan update, dan laporan hanya ditulis bila program mencantumkan aplikasi desktop/sistem dengan kanal pembaruan yang relevan — temuan lab sendiri bukan temuan pada target program kecuali direproduksi pada aset in-scope sesuai pasal scope.

## Pemicu (kapan dipakai)

Dipakai saat perlu menguji ketahanan kanal pembaruan otomatis: apakah sistem lab sendiri memverifikasi tanda tangan paket update, apakah kanal memakai TLS, apakah paket yang diganti (dengan paket canary bertanda "CANARY") diterima dan dijalankan, dan apakah ada pemeriksaan integritas (hash/checksum) sebelum instalasi. Dipakai pada sistem/aplikasi lab milik sendiri (VM atau mesin khusus lab, snapshot/backup sudah dibuat). Dipakai SEBELUM mengklaim kerentanan auto-update pada target program — lab membuktikan pola serangannya, target in-scope membuktikan relevansinya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Membangun lab update, menyiapkan server update canary, menguji validasi paket |
| Pengerjaan | **A54 Penguji Live** | Menjalankan pembaruan di sistem lab dan memeriksa paket canary diterima/ditolak |
| Audit | **A60 Security Auditor** | Memvalidasi bukti lab sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Pengujian aplikasi macOS termasuk mekanisme auto-update → skill `pengujian-aplikasi-macos` (skill ini menguji kanal update SECARA UMUM di lab, bukan spesifik macOS).
- Pengujian aplikasi desktop Electron (Node integration, preload) → skill `pengujian-electron-desktop`.
- DLL hijacking/sideloading → skill `dll-hijacking-windows`.
- Dependency confusion / typosquatting paket → skill `dependency-confusion`, `typosquatting-paket` (rantai pasok registry, bukan kanal update aplikasi).
- Pembajakan WebSocket / webhook → skill `pembajakan-websocket-cswsh`, `pengujian-webhook-signature`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (huntr, Perplexity VDP, Mistral VDP, Anthropic untuk skill ini).
2. **Hanya akun sendiri + canary palsu.** Sistem, server update, dan paket dalam uji ini milik sendiri; paket pengganti adalah paket CANARY yang jelas-jelas bertanda palsu dan tidak berbahaya.
3. **Tanpa data orang lain.** Tanpa menyentuh kanal update, sistem, atau paket milik orang lain.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Tidak ada korban dalam uji ini — hanya sistem lab sendiri.
5. **Tanpa DoS/DDoS pada target program.** Server update canary hanya melayani sistem lab sendiri.
6. **Tanpa payload di permukaan publik.** Paket canary dan server update lab tidak di-host/dibagikan di tempat umum — dan JANGAN PERNAH mengunggah paket canary ke registry/update-server publik.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total.** Otomasi hanya di program yang mengizinkan.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG membajak kanal pembaruan sistem orang lain atau layanan nyata. DILARANG menyebar paket pengganti ke siapa pun — paket canary HANYA untuk sistem lab sendiri dan HARUS jelas-jelas tidak berbahaya (tidak menjalankan kode berbahaya; cukup menulis penanda "CANARY" ke file log milik sendiri). DILARANG menguji pada sistem produksi atau sistem yang dipakai orang lain. SEBELUM uji, buat snapshot/backup sistem lab agar sistem bisa dipulihkan; SETELAH uji, pulihkan snapshot dan matikan server update canary.

## Langkah + gerbang

### Gerbang 0 — Cek scope + bangun lab update + snapshot

1. Baca pasal scope program yang dituju; catat relevansi aplikasi desktop/sistem. Bangun lab: sistem target (VM/mesin lab milik sendiri) + server update canary milik sendiri di jaringan terisolasi. Buat SNAPSHOT/backup sistem lab sebelum uji apa pun. Siapkan paket canary: paket bertanda jelas "CANARY", tidak berbahaya, yang bila dijalankan hanya menulis penanda ke file log milik sendiri.
2. **Standar lulus:** lab terisolasi + snapshot terverifikasi + paket canary inert tercatat. Tanpa snapshot = jangan mulai.

### Gerbang 1 — Baseline: pembaruan resmi berjalan normal

1. Jalankan pembaruan resmi (dari kanal asli, tanpa gangguan) di sistem lab. Catat: apakah paket diverifikasi (tanda tangan/hash), apakah kanal memakai TLS, dan apakah pembaruan terpasang normal.
2. **Standar lulus:** baseline tercatat (verifikasi ada/tidak + TLS ada/tidak). Tanpa baseline, kelemahan kanal tidak terukur.

### Gerbang 2 — Arahkan sistem lab ke server update canary

1. Arahkan kanal update sistem LAB SENDIRI ke server update canary (mis. lewat konfigurasi lab / hosts lab / proksi lab — hanya untuk sistem lab). Sajikan paket canary sebagai "pembaruan" dari server itu. Amati: apakah sistem meminta/memeriksa tanda tangan, hash, atau sertifikat sebelum menerima paket?
2. **Standar lulus:** tercatat pemeriksaan apa yang dilakukan sistem sebelum menerima paket (tanda tangan/hash/TLS/none). Bila sistem menolak paket canary = pertahanan bekerja, catat dan tutup sebagai hasil negatif yang valid.

### Gerbang 3 — Periksa apakah paket canary diterima/dijalankan

1. Bila sistem menerima paket canary, periksa apakah paket itu dijalankan/diinstal dan apakah penanda "CANARY" tertulis ke file log milik sendiri. Itu bukti kanal bisa dibajak — dengan paket yang tidak berbahaya. JANGAN lanjut ke paket lain; satu bukti canary sudah cukup.
2. **Standar lulus:** tercatat apakah penanda CANARY muncul (ya/tidak) beserta langkah yang membuatnya muncul. Penanda tidak muncul = belum terbukti, catat kenapa gagal.

### Gerbang 4 — Pulihkan snapshot + nilai relevansi ke target program

1. Pulihkan snapshot sistem lab, matikan server update canary, verifikasi sistem lab kembali normal. Nilai: apakah pola yang terbukti di lab relevan dengan aset in-scope program (aplikasi desktop target dengan kanal update serupa)? Bila ya, rancang reproduksi pada aset in-scope sesuai pasal scope; bila tidak, lab tetap dicatat sebagai pembelajaran.
2. **Standar lulus:** snapshot pulih + server canary mati + penilaian relevansi tertulis.

### Gerbang 5 — Tulis draf (bila relevan dengan target in-scope)

1. Tulis dampak konkret pada aset in-scope (bukan sekadar "paket canary diterima di lab"). Serahkan ke A60 audit → Muse → Cipta setuju → kirim.
2. **Standar lulus:** draf mengikuti format output + keputusan triase diputuskan A60, bukan oleh pembuat uji.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab terisolasi (sistem target + server update canary, milik sendiri) | Satu-satunya tempat pembajakan update diuji |
| Paket canary inert bertanda "CANARY" | Satu-satunya paket pengganti — hanya menulis penanda ke log milik sendiri |
| Snapshot/backup sistem lab | Dipulihkan setelah uji |
| Proksi/konfigurasi lab | Mengarahkan kanal update sistem lab ke server canary — hanya untuk sistem lab |
| `~/workspace/catatan/log-bug-bounty.md` | Log lab, baseline, hasil tiap gerbang, bukti, dan keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Program: [huntr / Perplexity VDP / Mistral VDP / Anthropic]
Lab: [sistem lab milik sendiri + server update canary milik sendiri]
Snapshot sebelum uji: [ya — terverifikasi]
Baseline: [pembaruan resmi — verifikasi tanda tangan/hash: ... | TLS: ...]
Pemeriksaan sebelum terima paket: [tanda tangan/hash/TLS/tidak ada]
Paket canary diterima/dijalankan: [ya — penanda CANARY muncul di log / tidak]
Snapshot dipulihkan + server canary dimatikan: [ya]
Relevansi target in-scope: [aset + pola yang sama — atau "hanya pembelajaran lab"]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hasil lab BUKAN temuan pada target program — lab hanya membuktikan pola; relevansi ke aset in-scope harus dibuktikan terpisah.
- Kanal update dengan penandatanganan paket + TLS + pinning yang benar akan menolak paket canary — hasil "ditolak" adalah temuan negatif yang valid.
- Paket canary HARUS inert dan bertanda jelas — jangan pernah memakai paket yang menjalankan kode berbahaya, walau di lab sendiri.
- Skill ini tidak membahas rantai pasok registry paket (lihat `dependency-confusion`, `typosquatting-paket`) atau DLL sideloading (lihat `dll-hijacking-windows`).
