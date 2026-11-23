# Skill: Injeksi Perintah & RCE — Eksekusi Perintah OS via Input / Deserialization Tidak Aman

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 33).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis bahwa input pengguna diteruskan ke perintah OS (parameter yang dipakai sebagai nama file/host/perintah, fitur ping/traceroute/konversi, webhook yang menjalankan skrip) atau ke deserializer yang tidak aman (objek Java/Python/PHP/.NET yang diterima dari pengguna). Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji injeksi perintah + deserialization, mendokumentasikan bukti echo canary |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan permukaan perintah/deserializer |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH pengujian perintah OS + deserialization, bukan mengulang konsepnya).
- Penyiapan server canary OAST + bukti callback → skill `ssrf-oast` (skill ini memakai canary itu untuk blind RCE; jangan ulangi cara menyiapkan canary di sini).
- Variasi payload secara sistematis → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- RCE via template engine (SSTI) → skill `injeksi-template-ssti` (jalur template; bila SSTI terbukti sampai RCE, perintahnya mengikuti allowlist skill ini).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.** Server canary (OAST) milik sendiri; satu ID unik per uji.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri server dengan `sleep` berulang atau perintah berat.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG reverse shell, DILARANG mengunduh/menjalankan file dari luar, DILARANG menulis file ke server, DILARANG menghapus/mengubah data atau konfigurasi, DILARANG membaca file sensitif server (`/etc/passwd`, `.env`, kredensial), DILARANG `cat`/`ls` direktori sensitif, DILARANG `curl`/`wget` ke layanan internal, DILARANG perintah yang mengubah sistem (`rm`, `shutdown`, `chmod`, `chown`, `kill`, pengalihan output `>`).
11. **ALLOWLIST PERINTAH PEMBUKTIAN — hanya ini yang boleh dieksekusi di server target:** `echo CANARY-UNIK` (mengembalikan canary), `id` (menampilkan uid/gid proses), `sleep N` (N kecil, maks. 5 detik, untuk blind time-based), dan callback DNS/HTTP ke canary OAST milik sendiri (mis. `nslookup <id-unik>.canary-milik-sendiri` / `ping -c 1 <id-unik>.canary-milik-sendiri`). Perintah di luar allowlist ini = pelanggaran, hentikan uji.
12. **Deserialization: deteksi saja, tanpa rantai exploit penuh.** Bila deserializer tidak aman terdeteksi, bukti cukup dengan callback canary dari gadget yang hanya memanggil canary (tanpa baca/tulis file, tanpa perintah di luar allowlist). DILARANG membangun rantai gadget yang mengeksekusi perintah di luar allowlist atau yang merusak state server.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian injeksi perintah/RCE diizinkan pada target ini? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan permukaan perintah

1. Cari permukaan: parameter yang dipakai sebagai host/nama file/perintah (fitur ping, traceroute, nslookup, konversi file, ekspor), serta endpoint yang menerima objek serial (Java `ObjectInputStream`, Python `pickle`, PHP `unserialize`, .NET `BinaryFormatter`, JSON yang diubah jadi objek).
2. Untuk tiap permukaan catat: input apa yang dikendalikan penyerang, dan respons normalnya seperti apa (baseline).
3. **Standar lulus:** daftar permukaan tertulis dengan baseline respons tiap permukaan. Permukaan tanpa baseline = belum dipetakan, jangan diuji.

### Gerbang 2 — Deteksi injeksi perintah (tanpa eksekusi berbahaya)

1. Uji pemisah perintah SATU per satu, selalu dengan perintah allowlist (`echo CANARY-UNIK`), mis. pada parameter host: `127.0.0.1; echo CANARY-UNIK`, `127.0.0.1 | echo CANARY-UNIK`, `127.0.0.1 && echo CANARY-UNIK`, `127.0.0.1$(echo CANARY-UNIK)`, `` 127.0.0.1`echo CANARY-UNIK` ``.
2. Uji juga tanpa pemisah bila input langsung jadi argumen perintah (mis. `$(echo CANARY-UNIK)` atau backtick di dalam nilai).
3. **Standar lulus:** canary kembali persis di respons pada minimal satu pemisah, atau respons berubah konsisten mengikuti pemisah. Tidak ada perubahan = permukaan itu tidak rentan terhadap pemisah itu, catat dan lanjut.

### Gerbang 3 — Blind command injection (bila output perintah tidak kembali)

1. Bila output tidak kembali, buktikan eksekusi via waktu: `; sleep 5` (atau `| sleep 5`) dan bandingkan waktu respons dengan baseline — konfirmasi dengan `sleep 2` vs `sleep 8` agar terbukti respons mengikuti nilai tunda.
2. Atau via callback OAST: `; nslookup <id-unik>.canary-milik-sendiri` / `; ping -c 1 <id-unik>.canary-milik-sendiri`, lalu periksa log canary (lihat `ssrf-oast`).
3. **Standar lulus:** waktu respons mengikuti nilai sleep pada 2 nilai berbeda, ATAU hit canary tercatat dengan ID unik yang cocok. Satu bukti saja tanpa konfirmasi = belum terbukti.

### Gerbang 4 — Deteksi deserialization tidak aman

1. Kenali format serial dari permintaan: objek Java (byte `AC ED 00 05`), Python pickle (`c__builtin__` / opcode `c`), PHP (`O:8:"NamaClass"`), .NET (byte `00 01 00 00 00 FF FF FF FF`), atau JSON yang diubah jadi objek di server.
2. Uji dengan objek yang HANYA memicu callback canary (gadget yang memanggil URL canary milik sendiri), tanpa rantai yang membaca/menulis file atau mengeksekusi perintah di luar allowlist. Bila tidak ada gadget canary yang aman, bukti cukup berupa: server menerima + memproses objek serial dari pengguna (error/pesan khas deserializer) — catat sebagai "deserializer terekspos, RCE belum dibuktikan".
3. **Standar lulus:** callback canary dari deserialization tercatat, ATAU bukti server memproses objek serial tercatat dengan respons persis. Klaim "RCE via deserialization" HANYA bila callback/echo canary terbukti — jangan klaim dari sekadar "objek diterima".

### Gerbang 5 — Buktikan dampak, serahkan ke triase

1. Tulis dampak sesuai yang TERBUKTI: injeksi perintah terbukti (echo canary / sleep / callback) atau deserializer terekspos. Jangan klaim "server bisa diambil alih penuh" bila hanya echo canary yang terbukti — tulis "eksekusi perintah terbukti pada allowlist; eskalasi lebih jauh tidak diuji, sesuai aturan aman".
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (payload persis + respons/waktu/log canary persis) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU payload perintah per uji, amati respons; hanya bila program mengizinkan alat itu |
| Server canary OAST milik sendiri (lihat `ssrf-oast`) | Bukti callback untuk blind RCE; satu ID unik per uji |
| Stopwatch / pengukuran waktu respons | Untuk blind time-based: catat waktu respons tiap uji + baseline |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload perintah (nilai → respons/waktu → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter]
Permukaan: [injeksi perintah / deserialization — format serial bila ada]
Pemisah/format terbukti: [; / | / && / $() / backtick / format serial]
Payload: [payload persis — hanya perintah allowlist]
Bukti: [canary kembali di respons / waktu respons X dtk vs baseline Y dtk / hit canary OAST]
Dampak terbukti: [eksekusi perintah allowlist / deserializer terekspos]
Yang TIDAK dilakukan: [tanpa reverse shell, tanpa tulis/baca file, tanpa perintah di luar allowlist]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Filter input (blokir `;`, spasi, kata kunci) sering bisa dilewati encoding — tapi setiap variasi tetap mengikuti allowlist perintah dan satu dimensi per putaran (lihat `rekonstruksi-iterasi-payload`).
- Deserialization tanpa gadget yang aman untuk canary tidak selalu bisa dibuktikan sampai RCE — laporkan sebagai "deserializer terekspos" dengan bukti yang ada, jangan memaksakan rantai exploit.
- Skill ini tidak membahas RCE via unggah file yang dieksekusi server — itu mengikuti skill `bypass-unggah-file` (bypass filter) + skill ini (pembuktian perintah, bila file yang diunggah mengeksekusi).
