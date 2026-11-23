# Skill: OWASP Top 10 LLM — Kerangka Pemetaan & Taksonomi Temuan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah kerangka pemetaan dari riset (referensi: `corca-ai/awesome-llm-security`, OWASP Top 10 for LLM Applications 2026), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebuah temuan sudah terbukti (atau diduga) dan perlu dipetakan ke kategori standar industri sebelum ditulis ke laporan.
- Perlu memeriksa cakupan pengujian: kategori OWASP mana yang sudah diuji pada target, mana yang belum.
- Perlu menerjemahkan temuan ke bahasa yang dipahami tim keamanan vendor (kategori OWASP + CVSS).
- Dipakai SETELAH pengujian, sebagai kerangka triase — BUKAN sebagai pengganti pengujian tiap kategori.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memetakan temuan ke kategori OWASP + memeriksa cakupan pengujian |
| Audit | **A60 Security Auditor** | Memeriksa apakah pemetaan tiap temuan sudah benar |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Skill ini adalah KERANGKA PEMETAAN/TAKSONOMI, bukan pengulangan isi tiap kategori OWASP.** Isi tiap kategori sudah tercakup di skill lain — tabel di bawah hanya memetakan kategori ke skill yang mengajarkan cara mengujinya. Jangan menulis ulang teknik tiap kategori di sini; pakai skill yang dirujuk.
- Penilaian keparahan temuan → skill `penilaian-cvss`.
- Validasi temuan yang sudah ada → skill `gerbang-tujuh-pertanyaan-triase`.

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

### Gerbang 1 — Tabel pemetaan OWASP Top 10 for LLM Applications 2026

Gunakan tabel ini untuk memetakan SETIAP temuan ke satu kategori utama (dan satu kategori sekunder bila relevan). Bila temuan tidak masuk satu pun kategori, catat sebagai "di luar OWASP Top 10 LLM" — jangan dipaksakan masuk.

| Kode | Kategori OWASP 2026 | Ringkasan satu baris | Skill yang mengajarkan cara mengujinya |
|---|---|---|---|
| LLM01 | Prompt Injection | Instruksi jahat menyusup lewat input langsung/tidak langsung | `perburuan-llm-ai`, `alat-pyrit`, `alat-garak`, `alat-promptfoo`, `alat-agentdojo` |
| LLM02 | Sensitive Information Disclosure | Data sensitif bocor lewat jawaban model | `eksfiltrasi-data-ai`, `audit-rag-llm` (area D) |
| LLM03 | Excessive Agency | Agen/tool diberi wewenang berlebih | `penyalahgunaan-tool-agen`, `analisis-batas-kepercayaan`, `scope-and-safety-guardian` |
| LLM04 | Supply Chain | Model/dataset/plugin/dependensi AI tidak tepercaya | `recon-rantai-pasok-cicd`, skill rantai pasok AI (bila ada) |
| LLM05 | Data and Model Poisoning | Data latih/RAG/model diracuni | `racun-rag-memori`, `perburuan-rag-vektor`, `racun-data-model-pelatihan` (kandidat 67), `serangan-backdoor-llm` |
| LLM06 | Unbounded Consumption | Konsumsi token/biaya tak terbatas (DoW/DoS) | `pengujian-konsumsi-tak-terbatas` (kandidat G3 — periksa statusnya; posisi tim: DoS tidak dibayar, verifikasi scope program dulu) |
| LLM07 | Misinformation | Output model disajikan sebagai fakta tanpa verifikasi | `pengujian-misinformasi-overreliance` (kandidat 4, kelompok lain) |
| LLM08 | Hidden Context Exposure | Konteks tersembunyi bocor (bukan hanya system prompt) | `paparan-konteks-tersembunyi` (kandidat 5, kelompok lain); `ekstraksi-system-prompt` (TUNGGU — jangan dipakai) |
| LLM09 | Vector and Embedding Weaknesses | Kelemahan lapisan vektor/embedding | `kelemahan-vektor-embedding` (kandidat 6, kelompok lain); `perburuan-rag-vektor`, `audit-rag-llm` |
| LLM10 | Improper Output Handling | Output AI tidak aman saat dirender/dieksekusi | `output-tidak-aman` |

**Catatan versi:** daftar di atas adalah OWASP Top 10 for LLM Applications 2026 (rilis 4 Agu 2026, Black Hat USA). LLM08 Hidden Context Exposure adalah kategori baru 2026 yang menggantikan System Prompt Leakage. Bila OWASP merilis versi lebih baru, perbarui tabel ini dan catat tanggal pembaruan di log.

### Gerbang 2 — Petakan temuan ke kategori

1. Ambil satu temuan yang sudah terbukti (lolos gerbang validasi skill pengujinya).
2. Tentukan kategori utama dari tabel Gerbang 1 berdasarkan DAMPAK temuan, bukan berdasarkan teknik yang dipakai (mis. injeksi yang menyebabkan kebocoran data → LLM02 sebagai utama, LLM01 sebagai sekunder).
3. Tulis pemetaan ke log dengan alasan satu kalimat: kenapa kategori ini, bukan kategori lain.
4. Bila dua kategori sama-sama cocok, pilih yang dampaknya paling besar sebagai utama dan catat yang lain sebagai sekunder.

### Gerbang 3 — Periksa cakupan pengujian per target

1. Untuk satu target in-scope, tandai kategori mana yang sudah diuji (dengan skill yang dirujuk) dan mana yang belum.
2. Kategori yang belum diuji = daftar kerja berikutnya — bukan temuan. Jangan menulis "temuan" untuk kategori yang belum diuji.
3. Serahkan daftar cakupan ke Muse untuk prioritas pengujian berikutnya.

### Gerbang 4 — Bedakan pemetaan benar dari pemetaan salah

| Gejala | Penilaian |
|---|---|
| Temuan dipetakan ke kategori hanya karena tekniknya mirip, padahal dampaknya beda | Pemetaan salah — petakan ulang berdasarkan DAMPAK |
| Satu temuan dipetakan ke 3+ kategori sekaligus | Terlalu longgar — pilih maksimal 1 utama + 1 sekunder |
| Temuan tidak masuk kategori mana pun tapi dipaksakan masuk | Pemetaan salah — catat "di luar OWASP Top 10 LLM" |
| Pemetaan konsisten dengan dampak + didukung bukti dari skill penguji | Pemetaan benar — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |

## Alat

| Alat | Cara pakai |
|---|---|
| Tabel pemetaan Gerbang 1 | Acuan pemetaan tiap temuan; perbarui bila OWASP merilis versi baru |
| Skill-skill yang dirujuk di tabel | Untuk pengujian tiap kategori — skill ini TIDAK menggantikan pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log pemetaan tiap temuan + cakupan pengujian per target |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI]
Temuan: [ringkasan temuan + skill penguji]
Kategori utama: [LLMxx + nama]
Kategori sekunder: [LLMxx + nama / tidak ada]
Alasan pemetaan: [satu kalimat berdasarkan dampak]
Cakupan target: [kategori sudah diuji: ... | belum diuji: ...]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Komponen AI] - [Jenis Kerentanan] (OWASP LLMxx) menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Skill ini adalah kerangka pemetaan, BUKAN pengganti pengujian: temuan tetap harus dibuktikan lewat skill penguji yang dirujuk di tabel.
- Tabel pemetaan ini dari riset OWASP 2026, bukan pengalaman teruji — tiap pemetaan butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Beberapa kategori merujuk skill kandidat kelompok lain (4, 5, 6, 67, G3) yang mungkin belum dibangun saat skill ini dipakai — bila skill rujukan belum ada, catat itu di log dan pakai skill terdekat yang tersedia.
- Kategori LLM06 (Unbounded Consumption): posisi tim saat ini adalah DoS tidak dibayar — verifikasi dulu program in-scope mana yang benar-benar membayarnya sebelum menguji kategori ini.
- OWASP memperbarui daftarnya berkala — periksa versi terbaru sebelum memakai tabel ini untuk laporan formal.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset OWASP Top 10 for LLM Applications terbaru dan scope program.

## Websites

- OWASP Top 10 for LLM Applications — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila perlu menilai keparahan temuan setelah dipetakan, pakai `penilaian-cvss`.
- Bila perlu memvalidasi temuan sebelum dipetakan, pakai `gerbang-tujuh-pertanyaan-triase`.
- Bila perlu menguji kategori tertentu, pakai skill yang dirujuk di tabel Gerbang 1.
