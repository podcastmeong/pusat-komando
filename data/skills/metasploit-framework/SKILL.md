# Skill: Metasploit Framework — Metasploit Framework: memakai modul exploit/auxiliary/payload yang sudah diketahui untuk menguji kerentanan layanan.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 40 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis metasploit Framework: memakai modul exploit/auxiliary/payload yang sudah diketahui untuk menguji kerentanan layanan. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya target in-scope/lab; bukan wrapper MCP (skill mcp-metasploit berstatus JANGAN PAKAI).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `mcp-metasploit` — JANGAN PAKAI (repo stale, terakhir push Februari 2026); skill ini adalah penggantinya — pakai framework langsung, bukan wrapper MCP
- `eksploitasi-eternalblue-smb-lab` (No. 53) — pola eksploitasi layanan jaringan dengan Metasploit di lab
- `pemindaian-port-layanan` — pemindaian layanan sebelum memilih modul
- `triase-duplikat` + `laporan-abstrak` — validasi dan pelaporan
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser/perangkat pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyalin, atau memakai data milik pengguna lain — walau terlihat.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pakai jeda antar-permintaan dan hentikan bila target melambat.
6. **Tanpa payload di permukaan publik.** Halaman/file PoC jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus/mengubah data, merusak layanan, menyebar paket/file berbahaya, atau memakai kredensial yang terbaca di luar PoC. Pembuktian HARUS aman, minimal, dan reversibel.
11. **Scope guard kandidat ini (WAJIB):** Hanya target in-scope/lab; bukan wrapper MCP (skill mcp-metasploit berstatus JANGAN PAKAI).
12. **Catatan khusus kandidat:** PERNYATAAN TEGAS: skill `mcp-metasploit` berstatus JANGAN PAKAI (repo stale) — JANGAN dipakai. Skill ini memakai Metasploit Framework LANGSUNG (msfconsole, modul exploit/auxiliary/payload) sebagai penggantinya.

## Langkah + gerbang

### Gerbang 0 — TEGAS: framework langsung, bukan wrapper MCP

- Skill `mcp-metasploit` berstatus JANGAN PAKAI (repo stale) dan JANGAN dipakai dalam bentuk apa pun. Semua pekerjaan Metasploit memakai framework langsung (msfconsole) seperti skill ini.
- Baca pasal scope program: modul hanya terhadap target in-scope atau lab sendiri. Catat di log.

**Standar lulus:** Penegasan 'bukan MCP' tercatat; pasal scope tercatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Pilih modul dari kerentanan yang sudah diketahui

- Pilih modul HANYA untuk kerentanan yang sudah teridentifikasi (versi layanan + CVE/kerentanan yang cocok) — jangan menjalankan modul secara membabi buta.
- Baca deskripsi modul: target yang didukung, opsi wajib, dan dampaknya; catat pilihan modul + alasannya.

**Standar lulus:** Modul terpilih punya dasar (versi layanan + kerentanan yang cocok) yang tercatat.

### Gerbang 2 — Uji modul auxiliary dulu (non-eksploitasi)

- Jalankan modul auxiliary (pemindaian/identifikasi, tanpa eksploitasi) terhadap target in-scope/lab untuk mengonfirmasi layanan dan versinya.
- Bila auxiliary menunjukkan layanan tidak cocok, BERHENTI — jangan memaksa modul exploit.

**Standar lulus:** Hasil auxiliary tercatat; kecocokan layanan terkonfirmasi atau pengujian dihentikan.

### Gerbang 3 — Jalankan modul exploit di lab / target in-scope

- Jalankan modul exploit dengan opsi yang benar di lab sendiri (atau target in-scope eksplisit); pakai payload yang paling tidak invasif (mis. pembuktian sesi/pembacaan canary), bukan payload destruktif.
- Hentikan segera bila modul menunjukkan perilaku di luar yang didokumentasikan.

**Standar lulus:** Hasil modul tercatat; payload destruktif tidak dipakai.

### Gerbang 4 — Buktikan dampak minimal + serahkan ke triase

- Buktikan dampak seminimal mungkin (sesi terbukti / file canary terbaca di lab) lalu serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim.

**Standar lulus:** Bukti minimal + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Metasploit Framework langsung (msfconsole, msfvenom hanya untuk lab) | Modul exploit/auxiliary/payload yang sudah diketahui; dijalankan dari CLI, bukan lewat MCP. |
| Mesin lab / VM terisolasi milik sendiri | Tempat utama pengujian modul; target program hanya bila in-scope eksplisit. |
| Basis data modul + dokumentasi modul | Baca deskripsi modul (target, opsi wajib, dampak) sebelum menjalankan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log modul yang dipakai, opsi, target, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [metasploit-framework — No. 40]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Menjalankan modul exploit tanpa mengetahui kerentanan yang dituju adalah pemindaian membabi buta yang bisa merusak layanan dan berujung banned. Modul yang gagal karena target tidak cocok bukan kegagalan — itu informasi yang dicatat dan ditutup.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
