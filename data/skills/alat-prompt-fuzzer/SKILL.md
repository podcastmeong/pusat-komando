# Skill: Alat Prompt Fuzzer — Hardening Aplikasi GenAI dengan Prompt Fuzzing

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `prompt-security/ps-fuzz`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope adalah aplikasi GenAI yang sudah jadi (chatbot produk, asisten terintegrasi, fitur AI dalam aplikasi) — bukan model mentah.
- Perlu menguji aplikasi LLM terintegrasi dengan variasi prompt berbahaya dan mengukur mana yang lolos pertahanannya.
- Perlu menyusun rekomendasi perbaikan pertahanan aplikasi berdasarkan hasil fuzzing.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang ps-fuzz di lab + menjalankan fuzzing terhadap aplikasi GenAI in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Fuzzing generatif terhadap model (membangkitkan input baru sendiri) → skill `alat-llmfuzzer` (kandidat 15 — menyasar model; skill ini menyasar aplikasi GenAI yang sudah jadi, level aplikasi/produk).
- Audit arsitektur RAG/LLM secara umum → skill `audit-rag-llm` (khusus RAG; skill ini untuk aplikasi GenAI apa pun).
- Eval/red-teaming prompt dengan kasus uji tetap → skill `alat-promptfoo`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat fuzzing aplikasi target.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan. **Khusus fuzzing: batasi jumlah variasi dan jeda antar request; fuzzing tanpa batas = pelanggaran aturan ini.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji. **Bila program melarang pengujian otomatis, fuzzing TIDAK BOLEH dijalankan ke target itu — pakai ps-fuzz hanya di lab sendiri.**

## Langkah + gerbang

### Gerbang 1 — Pasang ps-fuzz di lab sendiri

ps-fuzz (Prompt Fuzzer) adalah tool hardening aplikasi GenAI: ia menguji aplikasi LLM terintegrasi dengan variasi prompt berbahaya, mengukur mana yang lolos, dan membantu menyusun rekomendasi perbaikan pertahanan aplikasinya.

1. Clone repo: `git clone https://github.com/prompt-security/ps-fuzz.git` lalu ikuti `README.md` (dependensi, konfigurasi target aplikasi).
2. Siapkan profil aplikasi target: endpoint, cara autentikasi akun uji sendiri, dan daftar variasi prompt berbahaya awal (injeksi, jailbreak, kebocoran, penyalahgunaan tool).
3. Jalankan satu putaran kecil terhadap aplikasi uji sendiri untuk memastikan tool berjalan; catat versi dan konfigurasi di log.

### Gerbang 2 — Fuzzing aplikasi target in-scope dan ukur tingkat lolos

1. Tentukan anggaran SEBELUM mulai (jumlah variasi, jeda antar request, berhenti bila rate limit menyala) — tulis di log.
2. Jalankan ps-fuzz terhadap aplikasi target in-scope dengan akun uji sendiri.
3. Untuk tiap variasi, catat: lolos (aplikasi menjalankan instruksi berbahaya / membocorkan data) atau tertahan (ditolak/dinetralkan).
4. Hitung tingkat lolos per kategori variasi (mis. injeksi X%, jailbreak Y%) — angka ini adalah ukuran pertahanan aplikasi, bukan bukti temuan.

### Gerbang 3 — Verifikasi variasi yang lolos dengan efek nyata

1. Ambil tiap variasi yang lolos; uji ulang manual 3× ke target dengan akun uji sendiri.
2. Temuan valid HANYA bila variasi menghasilkan efek nyata (aksi tidak sah, kebocoran canary/data, eksekusi fungsi tanpa izin) — bukan sekadar "aplikasi tidak menolak prompt".
3. Susun rekomendasi perbaikan pertahanan aplikasi untuk tiap pola yang lolos (sebagai bagian isi laporan, bukan pengganti bukti).

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Aplikasi tidak menolak prompt berbahaya tapi juga tidak menjalankan instruksinya | Bukan temuan — penolakan bukan satu-satunya pertahanan |
| Variasi lolos tapi hanya menghasilkan jawaban aneh/halusinasi tanpa efek | False positive — BUKAN temuan |
| Variasi lolos DAN menghasilkan efek nyata (aksi/kebocoran), dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo ps-fuzz (`prompt-security/ps-fuzz`) | Clone + ikuti README; konfigurasi target aplikasi + daftar variasi |
| Akun uji sendiri | Wajib untuk Gerbang 2–3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi ps-fuzz + anggaran + tingkat lolos per kategori + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi GenAI]
Versi ps-fuzz lab: [commit/tag] | Anggaran: [jumlah variasi + jeda]
Tingkat lolos: [kategori: x/y variasi lolos]
Variasi lolos: [contoh variasi + efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Rekomendasi pertahanan: [perbaikan yang disarankan]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Aplikasi GenAI target] - [Jenis variasi] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool ps-fuzz **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Tingkat lolos (bypass rate) adalah ukuran pertahanan, bukan bukti kerentanan: tiap variasi yang lolos tetap harus dibuktikan efek nyatanya (Gerbang 3).
- Fuzzing berisiko melanggar aturan rate limit / pengujian otomatis program — anggaran dan jeda wajib ditulis SEBELUM mulai; bila program melarang otomasi, jangan fuzzing ke target.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi ps-fuzz dan scope program.

## Websites

- Prompt Fuzzer (ps-fuzz) — https://github.com/prompt-security/ps-fuzz
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target adalah model mentah (bukan aplikasi jadi), pakai `alat-llmfuzzer`.
- Bila target memakai RAG, pakai `audit-rag-llm` untuk pemetaan arsitektur dulu.
- Bila cukup memakai kasus uji tetap, pakai `alat-promptfoo` atau `alat-garak`.
