# Skill: Injeksi Tak Terlihat Multimodal — Instruksi Tersembunyi yang Tak Terlihat Manusia di Gambar, Screenshot, dan Audio

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 2; Simon Willison, "Unseeable prompt injections in screenshots", 21 Okt 2025, kasus Brave/Perplexity Comet; pola injeksi via gambar/audio di arsip Simon Willison), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah agen vision/browser yang membaca screenshot, gambar, atau audio (agen penjelajah web, asisten multimodal, agen yang memproses lampiran gambar/suara).
- Ditemukan fitur agen yang menindaklanjuti isi gambar/screenshot/audio tanpa membedakan instruksi vs data.
- Dipakai saat menguji permukaan injeksi lintas-modalitas — BUKAN injeksi teks biasa (itu `perburuan-llm-ai`).
- Cross-reference: skill kelompok lain `serangan-white-box-multimodal` (kandidat 20) membahas suffix adversarial white-box + jailbreak gambar/suara — skill ini fokus pada **instruksi tak terlihat manusia** (teks nyaris tak kasatmata, teks di screenshot yang ditempel), bukan suffix adversarial. Bila temuan memakai suffix white-box, lanjutkan ke skill itu; bila memakai instruksi tersembunyi yang tak terlihat mata manusia, tetap di skill ini.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menyiapkan media uji + menjalankan matriks modalitas + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Injeksi prompt teks (langsung/tidak langsung via dokumen/email) → skill `perburuan-llm-ai`.
- Pengujian live di browser (navigasi, interaksi halaman) → skill `uji-live-browser`.
- Suffix adversarial white-box + jailbreak gambar/suara → skill `serangan-white-box-multimodal` (kelompok lain, kandidat 20) — cross-reference, jangan digabung.
- XSS/SSRF via output AI yang dirender → skill `output-tidak-aman`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah); semua media uji dibuat sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.** Media uji hanya dipakai di akun/sesi milik sendiri, tidak diunggah ke halaman, repo, atau forum publik.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan matriks modalitas target

Petakan modalitas apa saja yang dibaca agen target dan bagaimana tiap modalitas diperlakukan. Tulis peta ke log. Standar lulus: tiap modalitas terjawab (dibaca/tidak + diperlakukan sebagai instruksi atau data?).

| Modalitas | Pertanyaan pemetaan |
|---|---|
| Gambar/lampiran | Apakah agen membaca isi gambar (OCR/vision)? Apakah teks dalam gambar diperlakukan sama seperti prompt pengguna? |
| Screenshot | Apakah agen membaca screenshot halaman (mis. agen browser)? Apakah teks di screenshot bisa memerintah agen? |
| Audio/suara | Apakah agen mentranskripsi audio lalu mengikuti instruksi di dalamnya? |
| Video | Apakah agen membaca frame/teks dalam video? |

### Gerbang 2 — Uji instruksi tak terlihat manusia (satu modalitas per putaran)

Buat media uji milik sendiri dengan instruksi yang **tak terlihat mata manusia** tapi bisa dibaca model. Uji satu varian per putaran; catat respons persis + aksi yang terjadi.

1. **Teks nyaris tak kasatmata di gambar:** teks kontras sangat rendah, ukuran sangat kecil, atau tersembunyi di area yang tidak diperhatikan (mis. footer gambar, piksel tepi). Instruksi pemancing: minta agen melakukan aksi canary yang aman dan teramati (mis. membuka halaman canary milik sendiri, atau menyebut kode canary palsu).
2. **Teks di screenshot yang ditempel:** screenshot halaman milik sendiri yang berisi instruksi tersembunyi (mis. di kolom komentar, di teks kecil halaman). Minta agen meringkas/menindaklanjuti screenshot itu; periksa apakah instruksi di screenshot diikuti.
3. **Instruksi di audio:** audio milik sendiri berisi instruksi yang disamarkan (kecepatan/volume rendah, terselip di tengah audio panjang). Minta agen mentranskripsi/meringkas; periksa apakah instruksi diikuti.
4. **Standar lulus tiap varian:** tercatat (a) media uji + cara penyembunyian, (b) apakah instruksi diikuti (aksi canary terpicu? ya/tidak), (c) apakah manusia biasa yang melihat media yang sama bisa menemukan instruksi itu (uji kontrol: tunjukkan media ke manusia — bila manusia langsung melihatnya, itu BUKAN "tak terlihat", catat sebagai injeksi biasa dan lanjutkan ke `perburuan-llm-ai`).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = instruksi tak terlihat manusia TERBUKTI memicu aksi nyata (aksi tool, navigasi, pengiriman data canary ke server milik sendiri) pada akun uji sendiri. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi; TOLAK juga bila instruksi sebenarnya terlihat jelas oleh manusia (bukan "tak terlihat").
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat arsitektur/otorisasi, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Sertakan media uji ASLI (file gambar/audio) sebagai lampiran bukti.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Media uji buatan sendiri (gambar, screenshot, audio) | Satu-satunya media yang dipakai; instruksi tersembunyi hanya di media milik sendiri. |
| Canary palsu (string non-sensitif) | Satu-satunya data yang dipakai sebagai "data sensitif" yang dipancing keluar/dipakai aksi. |
| Server canary milik sendiri | Penampung callback untuk membuktikan aksi keluar tanpa melibatkan pihak lain. |
| Akun uji sendiri | Agen diuji hanya di akun/sesi milik sendiri. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log matriks modalitas + varian uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur agen multimodal]
Matriks modalitas: [gambar: ya/tidak] | [screenshot: ya/tidak] | [audio: ya/tidak] | [video: ya/tidak]
Varian uji: [modalitas + cara penyembunyian + instruksi pemancing]
Kontrol manusia: [manusia bisa melihat instruksi? ya/tidak]
Langkah reproduksi: [media uji + permintaan ke agen + aksi yang terpicu]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur Agen Multimodal] - Instruksi tak terlihat di [gambar/screenshot/audio] memicu [Aksi Spesifik]`. Isi laporan: Matriks Modalitas (modalitas yang rentan + cara penyembunyian); Langkah Reproduksi (media uji terlampir + permintaan + aksi terpicu); Rekomendasi Perbaikan (perlakukan semua konten media sebagai data tak tepercaya, bukan instruksi; minta konfirmasi manusia sebelum aksi yang dipicu konten media; tandai sumber tiap instruksi).

## Batasan yang diketahui

- Metodologi ini dari riset (arsip Simon Willison), bukan pengalaman teruji — tiap varian butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Bila instruksi sebenarnya terlihat jelas oleh manusia, temuan ini bukan "tak terlihat" — pindahkan ke `perburuan-llm-ai` (injeksi tidak langsung biasa).
- Bila temuan memakai suffix adversarial white-box (bukan instruksi tersembunyi yang bisa dibaca manusia/model), pindahkan ke `serangan-white-box-multimodal` (kelompok lain, kandidat 20).
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan arsip Simon Willison.

## Websites

- Simon Willison, "Unseeable prompt injections in screenshots" — https://simonwillison.net/2025/Oct/21/unseeable-prompt-injections-in-screenshots/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila injeksinya lewat teks (dokumen/email/halaman) bukan media, pakai `perburuan-llm-ai`.
- Bila memakai suffix adversarial white-box, pakai `serangan-white-box-multimodal` (kelompok lain, kandidat 20).
- Bila pengujian live di browser secara umum, pakai `uji-live-browser`.
