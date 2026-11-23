# Skill: Penyalahgunaan Identitas Agen — Agen sebagai Identitas Tersendiri, Warisan Kredensial & Delegasi yang Melebar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 7; OWASP ASI03:2026 Identity & Privilege Abuse), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah platform agen AI di mana agen punya identitasnya sendiri: agen dibuat oleh satu pengguna lalu bisa dipanggil pengguna lain, agen memegang kredensial/koneksi layanan, atau agen bertindak "atas nama" seseorang.
- Ditemukan fitur berbagi agen, agen terjadwal, atau agen yang menyimpan kredensial/koneksi (Connector/MCP) yang bisa dipakai pemanggil lain.
- Dipakai saat menguji identitas NON-MANUSIA (agen) dan penyalahgunaan delegasi — BUKAN sesi login manusia (itu `manajemen-sesi-multi-peran`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan identitas agen + menguji warisan kredensial/delegasi + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Sesi admin/member/guest MANUSIA (regenerasi ID sesi, invalidasi, entropi) → skill `manajemen-sesi-multi-peran`.
- Titik kepercayaan server secara umum → skill `analisis-batas-kepercayaan`.
- Penyalahgunaan tool/izin agen (tool misuse, agent abuse) → skill `penyalahgunaan-tool-agen`.
- Manipulasi JWT (alg none, secret lemah, key confusion) → skill `manipulasi-jwt`.
- Diskrepansi autentikasi lintas kanal → skill `diskrepansi-autentikasi-lintas-kanal`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah); semua agen/koneksi yang diuji dibuat oleh akun sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan identitas agen target

Petakan siapa "agen" itu di mata sistem. Tulis peta ke log. Standar lulus: tiap titik terjawab atau dinyatakan "tidak ditemukan" dengan bukti.

1. **Identitas agen:** apakah agen punya identitas sendiri (ID agen, peran, kredensial) yang terpisah dari pengguna pemanggil? Atau agen selalu bertindak persis sebagai pemanggil?
2. **Warisan kredensial:** kredensial/koneksi apa yang dipegang agen (koneksi layanan pembuat, token yang di-cache, API key di tool)? Siapa yang bisa memakainya — hanya pembuat, atau siapa pun yang memanggil agen?
3. **Delegasi:** bagaimana delegasi bekerja — apakah ada batas (scope, masa berlaku, persetujuan ulang)? Apakah delegasi bisa melebar (agen memanggil agen lain yang mewarisi kredensial yang sama)?
4. **Pemisah "siapa memanggil" vs "atas nama siapa":** apakah sistem mencatat dan menegakkan perbedaan antara pemanggil dan pemilik kredensial? Apakah audit log membedakan keduanya?

### Gerbang 2 — Uji empat pola penyalahgunaan (satu pola per putaran)

Siapkan dua akun uji sendiri (User A = pembuat/pemilik kredensial, User B = pemanggil lain) + satu layanan dummy milik sendiri dengan kunci API PALSU (canary). Uji satu pola per putaran.

1. **Pola A — Warisan kredensial pembuat:** User A membuat agen yang terhubung ke layanan dummy (kunci canary). User B memanggil agen itu dan meminta agen memakai koneksi tersebut (mis. membaca data layanan dummy). Indikator: agen berhasil memakai kredensial User A untuk User B = kandidat temuan.
2. **Pola B — Kredensial yang di-cache:** User A memakai agen dengan koneksi sensitif, lalu sesi/kredensial itu tetap tersimpan. User B (atau sesi baru User A dengan peran lebih rendah) memanggil agen yang sama dan meminta aksi yang memakai kredensial yang di-cache. Indikator: aksi berhasil tanpa otentikasi ulang = kandidat temuan.
3. **Pola C — Delegasi yang melebar:** User A memberi agen izin sempit (mis. baca saja). Minta agen melakukan aksi di luar izin itu lewat rantai (agen memanggil tool lain, agen memanggil agen lain, atau agen meminta persetujuan atas nama User A). Indikator: aksi di luar scope berhasil = kandidat temuan.
4. **Pola D — Eskalasi lewat peran agen:** bandingkan apa yang bisa dilakukan User B langsung vs lewat agen (mis. User B tidak berhak membaca data X, tapi agen yang dipanggil User B bisa). Indikator: agen memberi User B akses yang tidak dimiliki User B sendiri = kandidat temuan.
5. **Standar lulus tiap pola:** tercatat langkah persis + respons/aksi + apakah kredensial/izin pemilik dipakai pemanggil lain (ya/tidak + bukti callback canary / isi data yang terbaca).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = kredensial/izin milik User A TERBUKTI dipakai oleh User B lewat agen (data canary terbaca, aksi sensitif terpicu atas nama pemilik) pada akun uji sendiri. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat identitas/delegasi, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Kunci canary palsu boleh ditulis (tidak ada artinya).

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (User A pembuat/pemilik, User B pemanggil) | Wajib untuk semua pola. Keduanya milik sendiri. |
| Layanan dummy milik sendiri + kunci API PALSU (canary) | Satu-satunya kredensial yang dipakai; canary berbentuk kredensial asli tapi tidak terhubung ke layanan sungguhan. |
| Server canary milik sendiri | Penampung callback untuk membuktikan kredensial dipakai tanpa melibatkan pihak lain. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta identitas agen + pola uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + platform agen AI]
Peta identitas agen: [identitas agen: ya/tidak] | [kredensial yang dipegang] | [aturan delegasi] | [pemisah pemanggil vs pemilik]
Pola diuji: [A/B/C/D + nama pola]
Langkah reproduksi: [User A buat agen + koneksi canary] → [User B panggil agen + minta aksi] → [hasil]
Indikator teramati: [kredensial/izin pemilik dipakai pemanggil lain? ya/tidak + bukti]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Platform Agen] - Agen mewariskan kredensial [Pemilik] ke pemanggil lain, memungkinkan [Aksi Spesifik] tanpa otorisasi`. Isi laporan: Peta Identitas (identitas agen + kredensial + aturan delegasi); Langkah Reproduksi (dua akun uji + layanan dummy canary + langkah pemanggil); Rekomendasi Perbaikan (kredensial agen berumur pendek dan ter-scope per pemanggil, pisahkan identitas agen dari identitas pembuat, minta persetujuan ulang saat pemanggil berbeda dari pemilik kredensial, catat pemanggil vs pemilik di audit log).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP ASI03:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Bila platform tidak punya konsep agen yang bisa dipanggil pengguna lain (agen selalu milik pemanggil), pola A/B/D tidak berlaku — jangan dipaksakan; yang berlaku hanya pola C (delegasi melebar dalam satu akun).
- Bila yang diuji adalah sesi login manusia (bukan identitas agen), pakai `manajemen-sesi-multi-peran`.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for Agentic Applications.

## Websites

- OWASP Top 10 for Agentic Applications 2026, ASI03 Identity & Privilege Abuse — https://owasp.org/www-project-top-10-for-agentic-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya penyalahgunaan tool/izin (bukan identitas/delegasi), pakai `penyalahgunaan-tool-agen`.
- Bila fokusnya sesi manusia, pakai `manajemen-sesi-multi-peran`.
- Bila fokusnya perbedaan autentikasi antar kanal, pakai `diskrepansi-autentikasi-lintas-kanal`.
