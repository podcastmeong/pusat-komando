# Skill: Rantai Pasok AI & AIBOM — Verifikasi Model, Adapter, Dataset & Tokenizer (OWASP LLM04 + ASI04:2026)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 12; OWASP LLM04:2026 Supply Chain + ASI04 Agentic Supply Chain; contoh OWASP: kompromi Amazon Q, 950.000+ instalasi; paket PyPI yang menyamar), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah aplikasi/platform AI yang memakai model, adapter, dataset, atau tokenizer dari pihak ketiga (model dari hub publik, paket Python, plugin/skill pihak ketiga, template chat).
- Ditemukan komponen AI tanpa tanda tangan/hash, file model yang di-deserialisasi secara tak aman, atau perubahan diam-diam pada chat template/tokenizer.
- Dipakai saat menguji rantai pasok KHUSUS AI (artefak model/dataset/tokenizer + AIBOM) — BUKAN rantai pasok CI/CD perangkat lunak umum (itu `recon-rantai-pasok-cicd`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menyusun AIBOM + menguji verifikasi artefak + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Rantai pasok CI/CD perangkat lunak umum (pipeline, dependensi, artefak build) → skill `recon-rantai-pasok-cicd`.
- Deserialisasi tak aman secara umum (gadget chain Java/PHP/Python/.NET) → skill `perburuan-deserialisasi` (bila sudah dibangun kelompok lain) / `fondasi-kerentanan-web-api`.
- Dorking & secret scanning repo publik → skill `dorking-secret-github`.
- Enumerasi aset cloud (bucket terbuka) → skill `enumerasi-aset-cloud`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh komponen AI yang diuji berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah); semua artefak uji dibuat sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.** Artefak uji hanya dipakai di lingkungan sendiri, tidak diunggah ke hub/repo/forum publik.
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Susun AI Bill of Materials (AIBOM)

Telusuri asal tiap komponen AI target. Tulis AIBOM ke log. Standar lulus: tiap komponen terjawab (asal + versi + tanda tangan/hash + cara verifikasi) atau dinyatakan "tidak ditemukan" dengan bukti.

| Komponen | Yang dicatat |
|---|---|
| Model dasar | Nama, sumber (hub/repo), versi/commit, hash, tanda tangan (ada/tidak) |
| Adapter/LoRA | Nama, sumber, versi, hash, tanda tangan (ada/tidak) |
| Dataset pelatihan/fine-tuning | Nama, sumber, versi, lisensi, apakah bisa diverifikasi isinya |
| Tokenizer + chat template | Sumber, versi, hash — apakah template bisa diubah diam-diam? |
| Dependensi eksekusi | Paket/framework yang memuat model (versi, sumber) |
| Skill/plugin pihak ketiga | Nama, sumber, versi, izin yang diminta |

### Gerbang 2 — Uji empat pola (satu pola per putaran)

Uji hanya pada komponen/lingkungan milik sendiri (lab sendiri) + target in-scope yang mengekspos komponennya. Satu pola per putaran.

1. **Pola A — Artefak tanpa tanda tangan/hash:** periksa apakah target memverifikasi tanda tangan/hash model/adapter/dataset sebelum memakainya. Bila target mengizinkan artefak tanpa verifikasi (mis. memuat model dari URL/hub tanpa cek hash), catat sebagai kandidat: buktikan dengan artefak uji milik sendiri yang hash-nya diubah — bila tetap dimuat tanpa peringatan = kandidat temuan.
2. **Pola B — Deserialisasi file model tak aman:** periksa format file model yang dimuat target (pickle, safetensors, format lain). Bila target memuat format yang mengeksekusi kode saat deserialisasi (mis. pickle) dari sumber yang tidak tepercaya, buktikan di lab sendiri dengan file model uji milik sendiri yang berisi callback canary (bukan perintah berbahaya) — callback terpanggil saat dimuat = kandidat temuan.
3. **Pola C — Perubahan diam-diam pada chat template/tokenizer:** periksa apakah chat template/tokenizer bisa diubah tanpa deteksi (mis. template dari sumber pihak ketiga yang bisa diperbarui diam-diam). Buktikan di lab sendiri: ubah satu baris template uji milik sendiri (mis. sisipkan instruksi canary) — bila perubahan itu memengaruhi perilaku model tanpa peringatan/verifikasi = kandidat temuan.
4. **Pola D — Model/artefak pihak ketiga yang tidak dievaluasi:** periksa apakah target memakai model/artefak pihak ketiga tanpa evaluasi keamanan (tanpa pengujian perilaku, tanpa daftar izin). Buktikan dengan model/artefak uji milik sendiri yang berperilaku menyimpang secara teramati (mis. selalu menyertakan kode canary dalam jawaban) — bila target memakainya tanpa deteksi = kandidat temuan.
5. **Standar lulus tiap pola:** tercatat komponen + cara verifikasi yang diuji + artefak uji milik sendiri + hasil (dimuat/ditolak, callback terpanggil/tidak, perubahan terdeteksi/tidak).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = artefak yang tidak terverifikasi TERBUKTI dimuat/dipakai target (hash diubah tetap dimuat, callback canary terpanggil saat deserialisasi, perubahan template memengaruhi perilaku tanpa deteksi) pada lingkungan/target in-scope milik sendiri. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi; TOLAK juga bila target memverifikasi artefak dengan benar (hash/tanda tangan ditolak saat diubah).
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** — pastikan cacat verifikasi rantai pasok, bukan kesalahan satu kali. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Sertakan AIBOM sebagai lampiran bukti.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Lab sendiri (lingkungan uji lokal) | Satu-satunya tempat artefak uji dibuat dan dimuat; file model/template uji milik sendiri. |
| Artefak uji milik sendiri | Model/adapter/template uji dengan hash diubah / callback canary — bukan artefak publik. |
| Server canary milik sendiri | Penampung callback deserialisasi tanpa melibatkan pihak lain. |
| Hash/tanda tangan artefak | Pembanding: hash yang diklaim vs hash artefak yang dimuat. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log AIBOM + pola uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aplikasi/platform AI]
AIBOM: [model: ...] | [adapter: ...] | [dataset: ...] | [tokenizer/template: ...] | [dependensi: ...] | [skill/plugin: ...]
Pola diuji: [A/B/C/D + nama pola]
Komponen diuji: [nama + sumber + versi + hash/tanda tangan: ada/tidak]
Artefak uji: [yang diubah: hash/template/format + callback canary]
Langkah reproduksi: [artefak uji + cara target memuatnya + hasil]
Indikator teramati: [dimuat tanpa verifikasi? callback terpanggil? perubahan terdeteksi?]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Aplikasi/Platform AI] - [Model/Adapter/Template] tanpa verifikasi [tanda tangan/hash] memungkinkan [Dampak Spesifik]`. Isi laporan: AIBOM (asal tiap komponen + status verifikasi); Langkah Reproduksi (artefak uji milik sendiri + cara target memuatnya); Rekomendasi Perbaikan (verifikasi tanda tangan/hash semua artefak AI di CI sebelum dipakai, pakai format model yang aman (safetensors, bukan pickle) untuk sumber tak tepercaya, kunci versi + hash chat template/tokenizer, evaluasi perilaku model pihak ketiga sebelum dipakai).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP LLM04 + ASI04:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Artefak uji HANYA dibuat dan dimuat di lab sendiri (aturan keras 6) — JANGAN mengunggah artefak beracun ke hub/repo publik.
- Callback canary dalam file model uji HANYA untuk membuktikan eksekusi saat deserialisasi — bukan perintah berbahaya, bukan akses data.
- Bila target tidak mengekspos komponen AI pihak ketiganya (semua tertutup), Gerbang 2 tidak bisa dijalankan — catat sebagai tidak dapat diuji, jangan dipaksakan.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for LLM/Agentic.

## Websites

- OWASP Top 10 for LLM Applications 2026, LLM04 Supply Chain — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Top 10 for Agentic Applications 2026, ASI04 Agentic Supply Chain — https://owasp.org/www-project-top-10-for-agentic-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya rantai pasok CI/CD perangkat lunak umum, pakai `recon-rantai-pasok-cicd`.
- Bila fokusnya deserialisasi umum (bukan file model), pakai `fondasi-kerentanan-web-api`.
- Bila fokusnya secret di repo publik, pakai `dorking-secret-github`.
