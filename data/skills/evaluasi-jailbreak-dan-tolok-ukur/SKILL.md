# Skill: Evaluasi Jailbreak & Tolok Ukur — JailbreakBench, AgentHarm, Open-Prompt-Injection

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi evaluasi dari riset (referensi: `corca-ai/awesome-llm-security`, repo `controllability/jailbreak-evaluation`, benchmark JailbreakBench, AgentHarm, dataset Open-Prompt-Injection), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu mengukur jailbreak secara terukur dan bisa diulang — bukan sekadar "satu prompt berhasil sekali".
- Perlu menjalankan benchmark JailbreakBench atau AgentHarm terhadap target in-scope (agen yang melakukan tindakan berbahaya).
- Perlu memakai dataset Open-Prompt-Injection untuk menguji serangan dan pertahanan injeksi prompt.
- Perlu membandingkan tingkat keberhasilan serangan (attack success rate) antar teknik atau antar putaran.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Menjalankan paket evaluasi + benchmark terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Satu benchmark serangan/pertahanan agen (AgentDojo) → skill `alat-agentdojo`.
- Validasi temuan yang sudah ada → skill `gerbang-tujuh-pertanyaan-triase`.
- Perburuan jailbreak/injeksi secara umum (tanpa benchmark) → skill `perburuan-llm-ai`.
- Teknik jailbreak lanjutan (cipher, multibahasa, many-shot) → skill `jailbreak-lanjutan-cipher-multibahasa-many-shot` (kandidat 26 — tekniknya; skill ini adalah cara MENGUKURNYA dengan benchmark).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menjalankan benchmark terhadap target.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan. **Khusus benchmark: batasi jumlah kasus uji per sesi dan beri jeda; menjalankan seluruh benchmark sekaligus tanpa batas = pelanggaran aturan ini.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji. **Bila program melarang pengujian otomatis, benchmark TIDAK BOLEH dijalankan ke target itu — pakai paket evaluasi hanya di lab sendiri.**

## Langkah + gerbang

### Gerbang 1 — Pasang paket evaluasi + benchmark di lab sendiri

1. Clone repo paket evaluasi: `git clone https://github.com/controllability/jailbreak-evaluation.git` lalu ikuti `README.md`.
2. Siapkan benchmark/dataset: JailbreakBench (kumpulan prompt jailbreak standar + penilai), AgentHarm (skenario agen melakukan tindakan berbahaya), Open-Prompt-Injection (dataset serangan dan pertahanan injeksi prompt).
3. Jalankan satu subset kecil di lab sendiri (model/aplikasi uji sendiri) untuk memastikan paket berjalan; catat versi paket, versi benchmark/dataset, dan metrik yang dipakai (mis. attack success rate / ASR) di log.

### Gerbang 2 — Jalankan benchmark terhadap target in-scope

1. Tentukan subset kasus uji SEBELUM mulai (mis. 10–20 kasus per kategori, bukan seluruh benchmark) dan jeda antar request — tulis di log.
2. Jalankan kasus uji ke endpoint target in-scope dengan akun uji sendiri; catat tiap kasus: berhasil/gagal + respons persis.
3. Hitung ASR per kategori (jailbreak, injeksi prompt, tindakan berbahaya agen) — angka ini adalah ukuran, bukan bukti temuan.

### Gerbang 3 — Verifikasi kasus yang berhasil dengan efek nyata

1. Ambil tiap kasus benchmark yang "berhasil" menurut penilai otomatis; uji ulang manual 3× ke target.
2. Temuan valid HANYA bila kasus menghasilkan efek nyata (aksi tidak sah, kebocoran canary/data, tindakan berbahaya agen yang benar-benar dieksekusi) — skor penilai otomatis BUKAN bukti.
3. Buang kasus yang hanya "berhasil" menurut penilai tapi tidak berdampak (mis. model menjawab dengan teks berbahaya tanpa aksi, atau penilai salah menilai).

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Penilai otomatis menandai berhasil, tapi verifikasi manual menunjukkan tidak ada efek nyata | False positive penilai — BUKAN temuan |
| Kasus berhasil tapi hanya jawaban teks berbahaya tanpa aksi/kebocoran | Bukan temuan bounty (cek scope program: sebagian program menganggap ini out of scope) |
| Kasus berhasil DAN menghasilkan efek nyata (aksi/kebocoran/tindakan berbahaya), dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Paket jailbreak-evaluation (`controllability/jailbreak-evaluation`) | Clone + ikuti README; jalankan evaluasi + hitung ASR |
| Benchmark JailbreakBench | Kumpulan prompt jailbreak standar + penilai |
| Benchmark AgentHarm | Skenario agen melakukan tindakan berbahaya |
| Dataset Open-Prompt-Injection | Dataset serangan + pertahanan injeksi prompt |
| Akun uji sendiri | Wajib untuk Gerbang 2–3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi paket/benchmark + subset kasus + ASR per kategori + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI/model]
Paket evaluasi: [versi] | Benchmark: [JailbreakBench/AgentHarm/Open-Prompt-Injection + versi]
Subset kasus: [jumlah per kategori + jeda]
ASR: [kategori: x/y berhasil]
Kasus terverifikasi manual: [kasus + efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur AI target] - [Jenis jailbreak/injeksi] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool jailbreak-evaluation dan benchmark/dataset di atas **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Penilai otomatis benchmark bisa salah menilai (false positive/negative) — verifikasi manual (Gerbang 3) wajib.
- ASR adalah ukuran, bukan bukti: satu kasus dengan ASR tinggi tetap harus dibuktikan efek nyatanya.
- Menjalankan seluruh benchmark sekaligus berisiko melanggar rate limit / aturan otomasi program — subset dan jeda wajib ditulis SEBELUM mulai.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi paket evaluasi/benchmark dan scope program.

## Websites

- jailbreak-evaluation — https://github.com/controllability/jailbreak-evaluation
- JailbreakBench — https://github.com/JailbreakBench/jailbreakbench
- AgentHarm — https://github.com/centerforaisafety/AgentHarm
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila hanya perlu satu benchmark serangan/pertahanan agen, pakai `alat-agentdojo`.
- Bila perlu membangkitkan input adversarial baru (bukan kasus benchmark tetap), pakai `alat-llmfuzzer`.
- Bila perlu teknik jailbreak lanjutan untuk diuji, pakai `jailbreak-lanjutan-cipher-multibahasa-many-shot`.
