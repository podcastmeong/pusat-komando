# Skill: Claude-Red — Metodologi Ofensif untuk Permukaan Serang Klasik (BACA DULU SEBELUM LOAD)

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026), bukan pengalaman teruji. Repo ini berisi metodologi serangan nyata; skill ini mengatur CARA MEMBACA dan MEMBATASINYA, bukan cara menyerang bebas.

> ⚠️ PERINGATAN — BACA DULU SEBELUM LOAD: repo Claude-Red berisi ~60–78 skill ofensif (SQLi, shellcode, EDR evasion, exploit dev). README-nya TIDAK menjelaskan bagaimana skill-skill itu diuji, dan pemindaian sampel pihak ketiga menemukan kegagalan pada sebagian skill. JANGAN load skill apa pun dari repo ini tanpa membaca isi SKILL.md-nya dulu dan tanpa memindainya (skill `skill-skillspector`). JANGAN jalankan satu pun prosedurnya di luar program in-scope.

## Pemicu (kapan dipakai)

- A62 menemukan dugaan kerentanan di permukaan serang KLASIK (web/API) dari program bounty yang in-scope dan butuh metodologi pengujian yang sistematis (bukan sekadar coba-coba).
- Ada temuan di program web klasik (mis. huntr) yang perlu diuji dengan metode standar (SQLi, JWT, business logic) sebelum dilaporkan.
- TIDAK dipakai untuk bounty agen AI (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel) — permukaan serang di sana adalah agen/model, bukan aplikasi web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Baca skill yang relevan, uji HANYA di program web klasik in-scope |
| Pemeriksa | **A60 Security Auditor** | Periksa prosedur yang akan dipakai + hasil uji sebelum draf laporan |
| Pemimpin | **Muse** | Putuskan prosedur mana yang boleh dipakai; bunuh yang di luar scope |

## Sumber

- Repo: **SnailSploit/Claude-Red** — https://github.com/SnailSploit/Claude-Red (lisensi MIT; ~4k bintang menurut artikel, ~11k menurut sumber lain — angka berubah; badge repo: 78 skill, 23 kategori, roadmap ~130).
- Kategori terbesar: Web Application (16 skill), Wireless (14), Infrastructure and Red Team (7).
- Contoh skill: `offensive-sqli`, `offensive-jwt`, `offensive-active-directory`, `offensive-edr-evasion`, `offensive-container-escape`, `offensive-shellcode`, `offensive-api-security`, `offensive-business-logic`, `offensive-reporting`.
- Instal per kategori (sparse checkout, JANGAN clone semua): `git clone --filter=blob:none --sparse https://github.com/SnailSploit/Claude-Red` lalu `git sparse-checkout set Skills/web Skills/active-directory`.
- Repo ini TIDAK berasal dari vendor keamanan yang dikenal — tidak ada perusahaan yang bisa diverifikasi di balik akun SnailSploit. Itu sebabnya aturan "baca dulu" bersifat mutlak.

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — prosedur AI bukan prosedur sampai manusia membaca dan menyetujuinya.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**
11. **BACA DULU SEBELUM LOAD.** Setiap file SKILL.md dari repo ini WAJIB dibaca penuh + dipindai SkillSpector SEBELUM dipakai. Skill yang belum dibaca = skill yang dilarang dipakai.
12. **Skill ofensif HANYA untuk program web klasik in-scope.** Skill wireless (evil twin, deauth), EDR evasion, shellcode, dan Active Directory TIDAK dipakai — tidak ada program kita yang mencakup itu.
13. **Tidak ada exploit otomatis.** Prosedur di repo ini adalah metodologi; eksekusi dilakukan manual, satu langkah per satu langkah, dengan persetujuan Muse per langkah yang berisiko.

## Langkah + gerbang

### Gerbang 0 — Cek scope: apakah ini program web klasik? (standar lulus: program + permukaan serang tertulis; bila programnya bounty agen AI → BERHENTI, skill ini tidak berlaku)

1. Tulis program + target di `~/workspace/catatan/log-bug-bounty.md`.
2. Bila targetnya agen/model AI → pakai skill bounty agen AI (`transfer-hunting`, `recon-pantau-program`), BUKAN skill ini.

### Gerbang 1 — Baca + pindai skill yang akan dipakai (standar lulus: SKILL.md dibaca penuh, hasil SkillSpector tercatat, tidak ada temuan CRITICAL)

1. Pilih SATU skill yang sesuai permukaan serang (mis. `offensive-sqli` untuk dugaan SQLi).
2. Baca seluruh isi SKILL.md-nya; catat langkah apa saja yang akan dijalankan dan mana yang TIDAK akan dijalankan (karena di luar scope).
3. Pindai dengan SkillSpector (skill `skill-skillspector`). Skor DO NOT INSTALL = skill dilarang dipakai.

### Gerbang 2 — Uji manual, satu langkah (standar lulus: tiap langkah dicatat + ada bukti respons target; tidak ada langkah yang dijalankan otomatis berurutan)

1. Jalankan prosedur manual, satu langkah, di akun sendiri, di target in-scope.
2. Simpan bukti tiap langkah (respons, tangkapan layar, log).
3. Bila langkah meminta sesuatu yang dilarang aturan keras (DoS, payload publik, data orang lain) → LEWATI langkah itu dan catat alasannya.

### Gerbang 3 — Verifikasi A60 (standar lulus: A60 memeriksa bukti + prosedur; temuan tanpa bukti = BUKAN temuan)

1. Serahkan bukti ke A60; hanya temuan terverifikasi yang masuk draf laporan.

### Gerbang 4 — Draf laporan (standar lulus: draf ikut format `laporan-abstrak`; metodologi yang dipakai disebutkan jujur)

1. Tulis draf laporan; sebutkan skill Claude-Red mana yang dipakai sebagai metodologi.
2. Jangan kirim sebelum Cipta setuju.

## Alat

| Alat | Repo / cara pakai |
|---|---|
| Claude-Red (metodologi ofensif) | https://github.com/SnailSploit/Claude-Red — sparse checkout per kategori, BACA DULU |
| SkillSpector (pindai sebelum load) | Lihat skill `skill-skillspector` |
| Burp Suite (hanya program web klasik) | Manual, di target in-scope saja |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per uji: tanggal | program | skill Claude-Red dipakai | langkah dijalankan | hasil | status (kandidat / terverifikasi A60).
- Draf laporan: ikut format skill `laporan-abstrak`; jangan kirim sebelum Cipta setuju.
- Skill yang dibaca tapi DITOLAK (alasan: di luar scope / skor pindai buruk) dicatat juga di log, supaya tidak dibaca ulang sia-sia.

## Batasan yang diketahui (BELUM DIUJI)

- Repo belum pernah di-clone/diuji tim; jumlah skill (60 vs 78 menurut sumber berbeda) dan isinya bisa berubah.
- README repo tidak menjelaskan pengujian skill-skillnya; sebagian skill gagal pemindaian sampel pihak ketiga — jangan percaya isinya mentah-mentah.
- Repo ini metodologi, BUKAN otorisasi: lisensi MIT tidak memberi izin menyerang sistem apa pun. Otorisasi hanya dari aturan program bounty yang in-scope.
