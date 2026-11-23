# Skill: Alat Vigil — Pemindai Deteksi Injeksi Prompt Berbasis Pola

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `deadbits/vigil-llm`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu memindai input-output LLM target in-scope dengan pemindai deteksi injeksi berbasis pola/aturan.
- Perlu membandingkan hasil deteksi rule-based (Vigil) dengan detektor self-hardening (Rebuff) atau toolkit umum (llm-guard).
- Perlu menguji aplikasi LLM dengan aturan deteksi yang bisa dikonfigurasi sendiri di lab.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang Vigil di lab + menjalankan pemindaian terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Toolkit deteksi injeksi umum multi-vektor → skill `alat-llm-guard`.
- Detektor injeksi self-hardening (belajar dari serangan baru) → skill `alat-rebuff` (kandidat 13 — pendekatan berbeda: adaptif, bukan rule-based).
- Perburuan injeksi prompt LLM secara umum (tanpa tool spesifik) → skill `perburuan-llm-ai`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji target.
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

### Gerbang 1 — Pasang Vigil di lab sendiri

Vigil adalah toolkit deteksi injeksi prompt berbasis pola/aturan (scanner) yang bisa dikonfigurasi: aturan deteksi ditulis sebagai pola yang dicocokkan terhadap input dan output LLM.

1. Clone repo: `git clone https://github.com/deadbits/vigil-llm.git` lalu ikuti `README.md` (instalasi Python, file konfigurasi `config.yaml`).
2. Perintah dasar: jalankan pemindai Vigil terhadap sebuah prompt/teks sesuai petunjuk repo (mis. mode scan CLI atau pustaka Python-nya); catat perintah persis yang dipakai.
3. Pelajari file aturan bawaan: aturan apa saja yang aktif, pola apa yang dicocokkan (mis. frasa "abaikan instruksi", pola penyisipan instruksi, pola kebocoran prompt).
4. Catat versi Vigil dan daftar aturan aktif di log — hasil pindai hanya bermakna bila konfigurasi tercatat.

### Gerbang 2 — Pelajari cara membaca hasil pemindaian

1. Vigil menandai input/output sebagai: bersih, mencurigakan (aturan tertentu cocok), atau terdeteksi injeksi (beserta aturan mana yang memicu).
2. Uji dengan tiga kelompok input di lab sendiri: (a) injeksi jelas, (b) teks jinak yang mengandung kata-kata pemicu aturan (dokumentasi, contoh, kutipan), (c) injeksi terselubung (parafrasa, pemecah kata, sisipan di tengah teks panjang).
3. Catat tingkat false positive tiap aturan: aturan yang terlalu sering memicu pada teks jinak harus dicatat sebagai "aturan berisik" dan tidak dipakai sebagai bukti tunggal.

### Gerbang 3 — Pindai target in-scope

1. Kumpulkan input-output dari endpoint target in-scope HANYA memakai akun uji sendiri; jalankan Vigil terhadap pasangan input-output itu di lab.
2. Untuk tiap temuan Vigil: uji ulang input yang sama langsung ke target (3×) dan catat apakah efek nyata terjadi (aksi, kebocoran data, perubahan perilaku) atau hanya skor pemindai.
3. Temuan valid HANYA bila skor pemindai didukung efek nyata yang dapat diulang — skor Vigil sendiri BUKAN bukti kerentanan.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Vigil menandai teks jinak (aturan cocok pada kata umum seperti "instruksi", "sistem") | False positive scanner — BUKAN temuan; catat aturan berisiknya |
| Vigil menandai injeksi, tapi model target menolak menjalankan instruksinya | Bukan temuan — deteksi ≠ eksekusi |
| Vigil menandai injeksi DAN model menjalankan instruksi dengan efek nyata, dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo Vigil (`deadbits/vigil-llm`) | Clone + ikuti README; mode scan CLI / pustaka Python; konfigurasi `config.yaml` |
| Akun uji sendiri | Wajib untuk Gerbang 3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi Vigil + aturan aktif + hasil tiap pindai + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI]
Versi Vigil lab: [commit/tag] | Aturan aktif: [daftar]
Input uji: [teks input]
Hasil Vigil: [bersih/mencurigakan/terdeteksi + aturan pemicu]
Respons target: [efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur AI target] - [Jenis injeksi] lolos deteksi menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool Vigil **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Pemindai berbasis pola rentan false positive pada teks jinak yang mengandung kata pemicu — jangan jadikan skor Vigil sebagai bukti tunggal.
- Vigil memindai input-output, bukan membuktikan eksekusi: efek nyata di target tetap harus dibuktikan terpisah.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi Vigil dan scope program.

## Websites

- Vigil — https://github.com/deadbits/vigil-llm
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila detektor target adaptif/self-hardening, pakai `alat-rebuff`.
- Bila perlu toolkit deteksi umum multi-vektor, pakai `alat-llm-guard`.
- Bila perlu fuzzing generatif massal, pakai `alat-llmfuzzer`.
