# Skill: Fingerprinting LLM — Identifikasi Model dari Luar

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi identifikasi dari riset (referensi: `corca-ai/awesome-llm-security`, paper "Instructional Fingerprinting", TRAP honeypot, "LLMmap: Fingerprinting for Large Language Models"), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu mengetahui model dan versinya di balik endpoint AI target in-scope sebelum memilih teknik pengujian (rekonesans).
- Target menyembunyikan identitas modelnya dan perlu ditebak lewat respons/perilaku.
- Perlu memakai honeypot prompt adversarial (TRAP) untuk identifikasi black-box.
- Dipakai SEBELUM pengujian mendalam: fingerprint dulu, baru pilih teknik yang sesuai dengan model itu.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Menjalankan fingerprinting terhadap model in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Fingerprinting infrastruktur web/server (HTTP, header, banner) → skill `probing-http-fingerprint`.
- Pemetaan permukaan serangan secara umum → skill `pemetaan-permukaan-serangan`.
- Ekstraksi system prompt → skill `ekstraksi-system-prompt` (status TUNGGU — jangan dipakai). **Fingerprinting BUKAN ekstraksi system prompt: yang ditebak adalah identitas model/versi, bukan isi instruksi sistem.**

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan model/fitur AI berada dalam in-scope program sebelum fingerprinting dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat fingerprinting.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan. **Fingerprinting dilakukan dengan sedikit prompt (puluhan, bukan ribuan); jangan membanjiri endpoint.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Fingerprinting perilaku (LLMmap)

LLMmap adalah metode identifikasi model dari luar: menebak model dan versinya lewat respons dan perilaku — gaya jawaban, pengetahuan cutoff, pola penolakan, cara menangani pertanyaan jebakan, dan sidik perilaku lainnya.

1. Siapkan daftar prompt probe perilaku (dari riset LLMmap / publik): pertanyaan pengetahuan cutoff, permintaan format khas, pertanyaan jebakan yang tiap model jawab berbeda.
2. Kirim probe ke endpoint target in-scope dengan akun uji sendiri; catat respons persis.
3. Bandingkan pola respons dengan sidik perilaku model yang dikenal (dari riset publik / lab sendiri): model apa yang paling cocok? Catat tingkat keyakinan (cocok kuat / cocok lemah / tidak dapat ditentukan).
4. Fingerprinting perilaku TIDAK PERNAH memberi kepastian 100% — catat selalu sebagai dugaan berkeyakinan, bukan fakta.

### Gerbang 2 — Honeypot prompt adversarial (TRAP)

TRAP memakai honeypot prompt adversarial untuk identifikasi black-box: prompt yang dirancang agar tiap model merespons dengan pola khasnya.

1. Pilih prompt honeypot dari riset TRAP (publik) yang relevan dengan target.
2. Kirim ke target in-scope dengan akun uji sendiri; catat pola respons khas yang muncul.
3. Cocokkan pola dengan sidik TRAP yang dikenal; bila cocok dengan satu model secara konsisten di beberapa honeypot, keyakinan naik.

### Gerbang 3 — Fingerprinting instruksional

Instructional fingerprinting: memakai instruksi khusus yang membuat model menunjukkan sidiknya (mis. meminta model mendeskripsikan dirinya dengan cara yang memicu pola khas, atau instruksi yang hanya model tertentu yang patuhi dengan cara tertentu).

1. Uji instruksi fingerprinting terhadap target in-scope; catat apakah pola khas muncul.
2. **BATAS:** jangan memakai teknik ini untuk mengekstrak system prompt atau instruksi sistem — bila respons mulai membocorkan instruksi sistem, HENTIKAN dan catat sebagai temuan potensial terpisah (bukan fingerprinting), lalu konsultasikan scope program sebelum lanjut.

### Gerbang 4 — Pakai hasil fingerprinting

1. Tulis kesimpulan fingerprinting ke log: model yang diduga + versi (bila dapat ditebak) + tingkat keyakinan + bukti pola.
2. Pilih teknik pengujian berikutnya berdasarkan model yang diduga (mis. suffix GCG yang diketahui bekerja pada keluarga model itu → `serangan-white-box-multimodal`; teknik jailbreak yang diketahui → `jailbreak-lanjutan-cipher-multibahasa-many-shot`).
3. **Fingerprinting sendiri BUKAN temuan bounty** — ia hanya rekonesans. Temuan bounty lahir dari pengujian lanjutan yang membuktikan kerentanan, bukan dari "model berhasil diidentifikasi".

### Gerbang 5 — Bedakan identifikasi benar dari tebakan salah

| Gejala | Penilaian |
|---|---|
| Satu probe cocok dengan satu model, probe lain cocok dengan model lain | Tidak dapat ditentukan — catat sebagai ambigu, jangan pakai sebagai dasar teknik |
| Beberapa probe + honeypot konsisten menunjuk satu model/keluarga | Dugaan berkeyakinan — boleh dipakai untuk memilih teknik pengujian |
| Respons membocorkan instruksi sistem / system prompt | HENTIKAN fingerprinting; nilai sebagai temuan potensial terpisah sesuai scope program |
| Model mengaku sebagai model X saat ditanya langsung | Jangan percaya begitu saja — klaim identitas diri mudah dipalsukan/diatur; butuh bukti perilaku |

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar prompt probe perilaku (LLMmap) | Prompt cutoff, format khas, pertanyaan jebakan — dari riset publik |
| Prompt honeypot adversarial (TRAP) | Prompt yang memicu pola khas per model — dari riset publik |
| Akun uji sendiri | Wajib untuk Gerbang 1–3; milik sendiri |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log probe + respons + dugaan model + keyakinan + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI/model]
Probe dipakai: [LLMmap x prompt | TRAP x prompt | instruksional x prompt]
Pola respons: [pola khas yang teramati]
Dugaan model: [model/keluarga + versi bila ada]
Keyakinan: [kuat/lemah/tidak dapat ditentukan]
Teknik lanjutan dipilih: [skill + alasan]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju — dari pengujian lanjutan, bukan dari fingerprinting): `[Model/fitur target] - [Jenis kerentanan] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset paper, bukan pengalaman teruji — tiap metode butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Fingerprinting perilaku tidak pernah memberi kepastian 100% — selalu catat sebagai dugaan berkeyakinan.
- Klaim identitas diri model ("saya adalah model X") mudah dipalsukan/diatur — jangan jadikan bukti tunggal.
- Fingerprinting sendiri BUKAN temuan bounty — ia rekonesans; temuan lahir dari pengujian lanjutan.
- Batas dengan ekstraksi system prompt: bila fingerprinting mulai membocorkan instruksi sistem, HENTIKAN dan nilai terpisah sesuai scope (skill `ekstraksi-system-prompt` berstatus TUNGGU — jangan dipakai).
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3× per probe penting.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset paper LLMmap/TRAP/instructional fingerprinting dan scope program.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target adalah infrastruktur web (bukan model), pakai `probing-http-fingerprint`.
- Bila permukaan serangan perlu dipetakan secara umum, pakai `pemetaan-permukaan-serangan`.
- Setelah model teridentifikasi, pilih teknik lanjutan: `serangan-white-box-multimodal`, `jailbreak-lanjutan-cipher-multibahasa-many-shot`, atau `perburuan-llm-ai`.
