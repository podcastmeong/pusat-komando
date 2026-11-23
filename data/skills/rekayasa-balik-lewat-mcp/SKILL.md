# Skill: Rekayasa Balik Lewat MCP — Bedah Biner/APK dengan Server MCP RE

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi RE lewat MCP dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 34; sumber: `Puliczek/awesome-mcp-security` — MCP Security Servers), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope menyediakan aplikasi (APK/biner) dan perlu dibedah lewat alur agen: Ghidra, IDA Pro, Binary Ninja, atau Jadx yang diekspos sebagai tool MCP.
- Ditemukan server MCP RE pada target atau di lingkungan kerja tim: GhidraMCP, IDA-Pro-MCP, binaryninja-mcp, Jadx MCP Plugin, TriageMCP.
- Saat butuh triase statis cepat file PE/APK lewat percakapan agen, bukan bedah manual satu per satu.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan RE lewat MCP, mengekstrak endpoint/secret/logika dari hasil bedah |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Dekompilasi aplikasi mobile MANUAL (apktool/jadx, manifest, resource, kode DEX/Swift/Obj-C) → skill `dekompilasi-aplikasi-mobile` — itu workflow manual APK/IPA; skill ini adalah alur RE yang DIJALANKAN AGEN lewat server MCP (GhidraMCP, IDA-Pro-MCP, binaryninja-mcp, Jadx MCP Plugin, TriageMCP).
- Analisis file JS aplikasi web → skill `analisis-statis-js`.
- Daftar tool analisis biner sebagai bagian suite klasik → skill `mcp-security-hub` (Ghidra dkk. hanya disebut sebagai tool di dalam suite, bukan alur RE lewat MCP).
- Inventaris endpoint hasil bedah → skill `pemetaan-permukaan-serangan` (skill ini menyerahkan hasilnya ke sana, bukan menggantikannya).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh aplikasi/biner yang dibedah berasal dari program in-scope dan salinannya diperoleh secara sah.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri; jangan bedah aplikasi yang berisi data orang lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain). Jangan menjalankan kode hasil uraian; hanya dibaca.
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Peroleh salinan sah dan pilih server MCP RE

Peroleh salinan aplikasi/biner HANYA dari sumber sah: toko resmi (Google Play/App Store) atau dari program itu sendiri. Jangan unduh dari situs pihak ketiga. Pilih server MCP RE sesuai jenis file (cek README masing-masing sebelum memakai — jangan mengarang flag):

| Server MCP | Cocok untuk |
|---|---|
| GhidraMCP | Biner native (PE/ELF) — dekompilasi dan analisis fungsi |
| IDA-Pro-MCP | Biner native — analisis mendalam IDA Pro |
| binaryninja-mcp | Biner native — analisis Binary Ninja |
| Jadx MCP Plugin | APK Android — DEX menjadi kode terbaca |
| TriageMCP | Triase statis file PE |

Standar lulus: salinan sah diperoleh (sumber + versi tercatat); server MCP RE yang dipilih merespons `tools/list`. Bila tidak ada salinan sah = BERHENTI, jangan bedah salinan dari sumber lain.

### Gerbang 2 — Bedah lewat agen, kumpulkan artefak

Minta agen membedah lewat tool MCP RE: daftar fungsi/string, endpoint/URL, secret/kunci yang ter-hardcode, deep link, dan logika bisnis yang relevan. Jangan menjalankan kode hasil uraian — hanya dibaca. Standar lulus: ada daftar artefak (endpoint, secret [REDACTED], deep link, logika) dengan lokasi file:barisnya; artefak yang hanya muncul di kode dicatat sebagai "HANYA DI KODE", bukan sebagai temuan hidup.

### Gerbang 3 — Validasi artefak di target hidup (bukan hanya di kode)

Untuk tiap artefak yang berpotensi jadi temuan (endpoint, secret, logika), validasi di target hidup dengan akun uji sendiri: endpoint benar merespons, secret benar valid (pakai canary/uji read-only milik sendiri — JANGAN pakai secret asli orang lain untuk masuk), logika benar bisa dipicu. Ulangi 3× bila melibatkan perilaku agen. Standar lulus: artefak terkonfirmasi hidup ATAU dinyatakan hanya-di-kode dengan buktinya. **Yang ada di kode saja BUKAN laporan** — yang maju hanya artefak yang terbukti hidup dan berdampak.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| GhidraMCP, IDA-Pro-MCP, binaryninja-mcp, Jadx MCP Plugin, TriageMCP | Server MCP RE; ikuti README masing-masing, jangan mengarang flag. |
| Toko resmi (Google Play / App Store) | Satu-satunya sumber salinan aplikasi (selain dari program itu sendiri). |
| Akun uji sendiri + canary palsu | Validasi artefak di target hidup. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log salinan → artefak → validasi → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi/biner + versi]
Sumber salinan: [toko resmi/program] | versi: [...]
Server MCP RE: [nama server + versi]
Artefak: <n> endpoint, <n> secret [REDACTED], <n> deep link, <n> logika bisnis
Per artefak: <file:lokasi> | <jenis> | <nilai> | <status: TERKONFIRMASI-HIDUP / HANYA-DI-KODE>
Validasi: [akun uji + langkah + log HTTP]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dibedah / divalidasi / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Aplikasi/Biner] - [Jenis artefak yang tervalidasi] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Bedah (server MCP RE + artefak yang ditemukan); Validasi Hidup (akun uji sendiri + log HTTP + bukti read-only); Rekomendasi Perbaikan (hapus secret dari biner, kunci endpoint yang terekspos, tambah otorisasi server-side untuk logika yang ditemukan di klien).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap server MCP RE butuh satu kali pemakaian nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Hasil bedah agen bisa salah (nama fungsi/string yang salah tafsir) — Gerbang 3 (validasi hidup) tidak boleh dilewati.
- Bila aplikasi memakai obfuscation berat: prioritaskan string URL dan konfigurasi yang tidak ter-obfuscate; catat bagian yang tidak terbaca sebagai "belum terpetakan".
- Bila aplikasi ternyata hanya membungkus website (WebView): pakai `crawling-browser-headless` + `analisis-statis-js` untuk bagian webnya, bukan RE biner.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome di target hidup, bukan jumlah artefak yang ditemukan di kode.

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Halaman aturan program resmi (sumber scope Gerbang 0).

## Alternatives for better results

- Bila bedah dilakukan manual (tanpa MCP), pakai `dekompilasi-aplikasi-mobile`.
- Bila hasil bedah adalah inventaris endpoint untuk diuji lanjut, serahkan ke `pemetaan-permukaan-serangan`.
- Bila artefak yang ditemukan adalah secret di repo publik, pakai `dorking-secret-github`.
