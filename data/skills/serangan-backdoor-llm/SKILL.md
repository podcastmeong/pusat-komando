# Skill: Serangan Backdoor LLM — Pemicu Tersembunyi pada Model yang Sudah Ada

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi serangan dari riset (referensi: `corca-ai/awesome-llm-security`, paper BITE, "Prompt as Triggers", "Backdooring Instruction-Tuned LLMs with Virtual Prompt Injection", PoisonGPT), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope memakai model hasil instruction-tuning / model pihak ketiga (mis. dari hub model) yang perilakunya tampak normal.
- Perlu menguji apakah model memiliki pemicu tersembunyi (trigger) yang mengubah perilakunya saat pemicu itu muncul.
- Perlu memeriksa model yang disebar (mis. lewat Hugging Face) apakah beracun — tampak normal tapi terpicu oleh pemicu tertentu.
- Perlu membedakan backdoor pada model yang sudah ada dari keracunan tahap pelatihan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Menguji pemicu backdoor terhadap model in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Keracunan data retrieval/RAG (meracuni konten yang diambil model) → skill `racun-rag-memori`, `perburuan-rag-vektor`.
- Keracunan tahap pelatihan model (data latih diracuni sebelum model dilatih) → skill `racun-data-model-pelatihan` (kandidat 67, kelompok lain — **cross-reference**: skill ini soal backdoor pada model yang SUDAH ADA — bobot/prompt instruksi yang sudah jadi; skill 67 soal keracunan TAHAP PELATIHAN. Jangan duplikat isinya; bila temuanmu ternyata berasal dari data latih, laporkan lewat skill 67).
- Ekstraksi system prompt → skill `ekstraksi-system-prompt` (status TUNGGU — jangan dipakai).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan model/fitur AI berada dalam in-scope program sebelum pengujian dimulai. **Jangan mengunduh dan menjalankan model beracun yang dicurigai di luar lab terisolasi; jangan menyebarkan model yang dicurigai beracun.**
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji model target.
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

### Gerbang 1 — Petakan model target dan asal-usulnya

1. Identifikasi model yang dipakai target in-scope: nama, versi, asal (buatan sendiri / pihak ketiga / hub model), dan apakah hasil instruction-tuning.
2. Periksa rantai pasok model: apakah model diunduh dari sumber yang bisa dimodifikasi pihak ketiga (hub publik tanpa verifikasi hash/tanda tangan)? Catat bila ya — ini konteks risiko, bukan bukti.
3. Bila model buatan sendiri dengan rantai pasok tertutup, peluang backdoor kecil — catat dan lanjut hanya bila ada indikasi perilaku aneh.

### Gerbang 2 — Uji pemicu (trigger) yang dicurigai

Backdoor LLM bekerja lewat pemicu tersembunyi: model tampak normal pada input biasa, tapi berperilaku berbeda (mengikuti instruksi tersembunyi, membocorkan data, melewati guardrail) saat pemicu muncul. Bentuk pemicu: kata/frasa tertentu (BITE, "Prompt as Triggers"), virtual prompt injection pada model hasil instruction-tuning, atau model beracun yang disebar (PoisonGPT).

1. Susun daftar pemicu kandidat dari riset publik (frasa pemicu yang diketahui dari paper, pola virtual prompt injection) — JANGAN membuat pemicu yang menargetkan pengguna nyata.
2. Uji tiap pemicu ke model target in-scope dengan akun uji sendiri: bandingkan perilaku model pada input biasa vs input yang sama + pemicu.
3. Indikator backdoor: perubahan perilaku yang tajam dan konsisten HANYA saat pemicu hadir (mis. model yang biasanya menolak tiba-tiba patuh; model membocorkan canary hanya saat pemicu hadir).

### Gerbang 3 — Verifikasi bahwa perilaku itu backdoor, bukan kebetulan

1. Uji pemicu yang sama 3× dan uji input kontrol (tanpa pemicu) 3× — perilaku harus berbeda secara konsisten.
2. Uji variasi pemicu (parafrasa, posisi berbeda): backdoor sejati terikat pada pemicu spesifik; bila SEMUA variasi menghasilkan perilaku sama, itu lebih mungkin kelemahan guardrail umum — laporkan lewat `perburuan-llm-ai`, bukan sebagai backdoor.
3. Bila memungkinkan (model open-weight in-scope): periksa apakah perilaku terpicu itu konsisten dengan virtual prompt injection — instruksi tersembunyi yang tertanam saat instruction-tuning.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Model berperilaku aneh pada SEMUA input, dengan atau tanpa pemicu | Bukan backdoor — kelemahan umum / halusinasi |
| Perilaku berubah hanya sekali, tidak dapat diulang | Perilaku probabilistik — TOLAK bila gagal direproduksi 3× |
| Perilaku berubah tajam dan konsisten HANYA saat pemicu hadir, dapat diulang 3×, dengan efek nyata (aksi/kebocoran) | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Temuan ternyata berasal dari data latih yang diracuni (bukan backdoor pada model jadi) | Laporkan lewat `racun-data-model-pelatihan` (kandidat 67), bukan skill ini |

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar pemicu kandidat dari riset publik | Frasa/pola pemicu dari paper BITE, "Prompt as Triggers", virtual prompt injection |
| Akun uji sendiri | Wajib untuk Gerbang 2–3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log asal model + pemicu diuji + perbandingan kontrol + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + model/fitur AI]
Asal model: [buatan sendiri/pihak ketiga/hub + versi]
Pemicu diuji: [pemicu + sumber riset]
Perilaku tanpa pemicu: [respons kontrol]
Perilaku dengan pemicu: [respons terpicu + efek]
Reproduksi: [x/3 putaran berhasil + kontrol x/3]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Model target] - Backdoor terpicu [pemicu] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset paper, bukan pengalaman teruji — tiap pola pemicu butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Membuktikan backdoor (bukan sekadar kelemahan guardrail) itu sulit dari luar: butuh konsistensi pemicu + kontrol yang bersih (Gerbang 3).
- Jangan mengunduh/menjalankan model yang dicurigai beracun di luar lab terisolasi; jangan menyebarkan model yang dicurigai beracun.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3× (plus kontrol 3×).
- Batas dengan skill `racun-data-model-pelatihan` (kandidat 67): skill ini HANYA untuk backdoor pada model yang sudah ada; keracunan tahap pelatihan dilaporkan lewat skill 67.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset paper backdoor LLM dan scope program.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila perilaku aneh terjadi pada semua input (bukan terikat pemicu), pakai `perburuan-llm-ai`.
- Bila keracunan ada di data retrieval/RAG, pakai `racun-rag-memori` atau `perburuan-rag-vektor`.
- Bila temuan berasal dari tahap pelatihan, pakai `racun-data-model-pelatihan`.
- Bila perlu memeriksa rantai pasok artefak AI (model/adapter/dataset tanpa tanda tangan), pakai skill rantai pasok AI yang relevan.
