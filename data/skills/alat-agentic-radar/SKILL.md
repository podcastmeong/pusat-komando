# Skill: Alat Agentic Radar — Pemindai Keamanan Alur Kerja Agen

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `splx-ai/agentic-radar`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope memakai alur kerja agen (agentic workflow): agen yang memanggil tool, memakai memori, dan memanggil agen lain.
- Perlu memindai rantai tool/memori/pemanggilan antar-agen secara otomatis untuk menemukan titik rawan.
- Perlu menandai titik injeksi lewat output tool dan eskalasi antar-langkah agen sebelum pengujian manual.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang Agentic Radar di lab + menjalankan pemindaian terhadap alur kerja agen in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penyalahgunaan tool oleh agen secara konseptual/manual → skill `penyalahgunaan-tool-agen`.
- Perburuan injeksi prompt LLM secara umum → skill `perburuan-llm-ai`.
- Audit arsitektur RAG/LLM (pemetaan 4 komponen) → skill `audit-rag-llm` (pemetaan manual; skill ini adalah pemindai otomatis khusus alur kerja agen).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur agen berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat memindai/menguji alur kerja target.
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

### Gerbang 1 — Pasang Agentic Radar di lab sendiri

Agentic Radar adalah pemindai keamanan alur kerja agen lewat CLI: ia memetakan rantai tool, memori, dan pemanggilan antar-agen, lalu menandai titik rawan seperti injeksi lewat output tool dan eskalasi antar-langkah agen.

1. Clone repo: `git clone https://github.com/splx-ai/agentic-radar.git` lalu ikuti `README.md` (instalasi CLI, konfigurasi pemindaian).
2. Jalankan pemindaian contoh di lab sendiri (terhadap alur kerja agen uji sendiri) untuk memastikan tool berjalan; catat versi dan perintah persis di log.
3. Pelajari format laporan pemindai: kategori titik rawan apa saja yang ditandai dan tingkat keparahannya.

### Gerbang 2 — Petakan alur kerja agen target in-scope

1. Petakan alur kerja agen target dari dokumentasi publik / perilaku yang teramati (rantai tool apa saja, memori apa yang dipakai, agen apa yang saling memanggil) — HANYA dari permukaan in-scope.
2. Jalankan Agentic Radar terhadap definisi/jejak alur kerja tersebut di lab; catat titik rawan yang ditandai pemindai beserta alasannya.
3. Pilih titik rawan yang paling berdampak (injeksi lewat output tool → aksi sensitif; eskalasi antar-langkah → hak akses melebar) untuk diuji manual.

### Gerbang 3 — Uji titik rawan dengan efek nyata

1. Uji SATU titik rawan per putaran ke target in-scope dengan akun uji sendiri dan canary palsu.
2. Temuan valid HANYA bila titik rawan menghasilkan efek nyata: agen menjalankan instruksi dari output tool tak tepercaya, atau eskalasi hak akses antar-langkah terbukti (aksi yang seharusnya tidak diizinkan berhasil).
3. Ulangi 3× per titik rawan; gagal direproduksi 3× = TOLAK.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Pemindai menandai titik rawan, tapi pengujian manual menunjukkan output tool disanitasi / izin divalidasi ulang | False positive pemindai — BUKAN temuan |
| Agen menjalankan instruksi dari output tool tapi aksinya jinak/tidak berdampak | Bukan temuan — butuh efek keamanan nyata |
| Agen menjalankan instruksi dari output tool tak tepercaya dengan efek nyata (aksi sensitif/kebocoran), dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo Agentic Radar (`splx-ai/agentic-radar`) | Clone + ikuti README; CLI pemindai alur kerja agen |
| Akun uji sendiri | Wajib untuk Gerbang 3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input/output tool uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi Agentic Radar + peta alur kerja + titik rawan + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alur kerja agen]
Versi Agentic Radar lab: [commit/tag]
Peta alur kerja: [rantai tool] | [memori] | [pemanggilan antar-agen]
Titik rawan ditandai: [titik + alasan pemindai]
Titik diuji: [titik + langkah reproduksi]
Efek teramati: [apa yang terjadi, persis]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Alur kerja agen target] - [Jenis titik rawan] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool Agentic Radar **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Pemindai menandai titik rawan berdasarkan pola statis — hasil pindai BUKAN bukti kerentanan; efek nyata harus dibuktikan manual (Gerbang 3).
- Pemetaan alur kerja target bergantung pada apa yang teramati dari luar; bagian alur yang tidak terlihat tidak bisa dipindai.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi Agentic Radar dan scope program.

## Websites

- Agentic Radar — https://github.com/splx-ai/agentic-radar
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila alur kerja agen perlu dipetakan manual dulu (tanpa pemindai), pakai `audit-rag-llm` Gerbang 1.
- Bila fokusnya penyalahgunaan tool secara konseptual, pakai `penyalahgunaan-tool-agen`.
- Bila fokusnya keracunan memori antar-agen, pakai `racun-rag-memori`.
