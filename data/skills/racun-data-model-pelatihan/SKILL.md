# Skill: Racun Data Model Pelatihan — Audit Keracunan Pre-Deployment (Riset/Audit, Bukan Perburuan Hadiah)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi audit dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 67; Wraith Academy Modul 11, "Data and Model Poisoning", https://www.wraith.sh/academy), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

> **PERINGATAN — BELUM DITEMUKAN PROGRAM IN-SCOPE AKTIF YANG MEMBAYAR KATEGORI INI.** Sampai riset ini ditulis, tidak ditemukan satu pun program bounty in-scope aktif yang membayar keracunan data/model tahap pelatihan. Nilai skill ini adalah **riset/audit**, bukan perburuan hadiah. **JANGAN klaim kategori ini berbayar** — jangan tulis angka hadiah, jangan kirim laporan bounty untuk kategori ini sebelum `recon-pantau-program` memverifikasi ada program in-scope yang benar-benar membayarnya. Bila program seperti itu ditemukan, catat sumber primernya di log dan baru ubah status skill ini.

## Pemicu (kapan dipakai)

- Ada akses audit (bukan eksploitasi) ke artefak model, dataset, atau pipeline fine-tuning milik sendiri / lab sendiri.
- Perlu menilai apakah sebuah model/dataset bisa diracuni SEBELUM deployment — satu-satunya serangan yang mendarat sebelum model dipakai.
- Dipakai sebagai audit provenance/integritas, BUKAN sebagai pengujian live terhadap model produksi orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menjalankan audit provenance/integritas artefak + dataset |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Keracunan RAG & memori jangka panjang pada lapisan retrieval saat runtime → skill `racun-rag-memori`. Itu racun SETELAH deployment (isi retrieval); skill ini racun SEBELUM deployment (data pelatihan + bobot model) — lapisan berbeda.
- Backdoor pada model yang sudah ada (pemicu tersembunyi, virtual prompt injection) → kandidat 21 (`serangan-backdoor-llm`, kelompok lain). Yang itu soal backdoor pada model yang sudah jadi; yang ini soal keracunan TAHAP PELATIHAN yang menanam backdoor itu.
- Keracunan tool/skill/MCP (deskripsi tool beracun, rug pull) → kandidat G2 (skill lain, bila sudah dibangun).
- Skill ini HANYA membahas keracunan tahap pelatihan + apa yang bisa diaudit tanpa akses training.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Audit ini dilakukan pada artefak/dataset MILIK SENDIRI atau lab sendiri — bukan pada aset produksi program tanpa izin eksplisit.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain). **Khusus skill ini: JANGAN meracuni dataset/model apa pun milik orang lain — keracunan hanya didemonstrasikan pada salinan lab milik sendiri.**
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan tiga jalur keracunan pelatihan

| # | Jalur | Cara kerja (dari riset) |
|---|---|---|
| J1 | Fine-tuning poisoning (backdoor lewat fine-tuning) | Sejumlah kecil contoh latih beracun disisipkan ke data fine-tuning; model belajar perilaku pemicu → aksi tersembunyi |
| J2 | Poisoning data skala web | Data latih yang diambil dari web (crawl) diracuni di sumbernya sebelum dikumpulkan |
| J3 | Artefak model yang dirusak | File model/adapter/tokenizer yang didistribusikan (mis. lewat hub model) sudah dimodifikasi sebelum diunduh pemakai |

Standar lulus: jalur yang diaudit teridentifikasi + artefak/dataset yang diaudit tercatat (nama, sumber, hash bila ada).

### Gerbang 2 — Audit tanpa akses training (provenance + integritas)

Yang BISA diaudit tanpa akses ke proses training: (a) provenance data — dari mana tiap sumber data berasal, apakah sumbernya tepercaya dan apakah ada sumber yang bisa ditulis publik tanpa moderasi; (b) integritas artefak — hash/tanda tangan file model/adapter/dataset, apakah berubah sejak diterbitkan, apakah ada versi yang tidak bertanda tangan; (c) anomali perilaku pada salinan lab sendiri — uji model lab dengan pemicu yang dicurigai dan bandingkan dengan perilaku baseline (model yang sama dari sumber tepercaya). Kenapa pengujian pasca-training tidak bisa menghilangkannya: backdoor yang tertanam di bobot bertahan melewati evaluasi perilaku normal — ia hanya aktif saat pemicunya muncul. Standar lulus: minimal dua dari tiga pemeriksaan (a/b/c) dilakukan dan hasilnya tercatat; bila hanya satu, nyatakan keterbatasannya di log.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** Valid = artefak/dataset terbukti dirusak (hash tidak cocok / sumber tidak tepercaya yang terbukti menyisipkan contoh beracun) ATAU backdoor terpicu secara deterministik pada salinan lab sendiri dengan pemicu yang terdokumentasi. **TOLAK** = sekadar "sumber data bisa ditulis publik" tanpa bukti penyisipan, atau perilaku aneh satu kali tanpa pemicu yang jelas.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pemicu pada salinan lab minimal **3 kali**. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Temuan yang lolos diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta. **INGAT peringatan di atas: jangan kirim sebagai laporan bounty sebelum ada program in-scope terverifikasi yang membayar kategori ini** — jalurnya adalah laporan audit/riset, bukan laporan hadiah.

## Alat

| Alat | Cara pakai |
|---|---|
| Salinan lab artefak/dataset milik sendiri | Satu-satunya objek yang diuji/diracuni untuk demonstrasi |
| Hash + tanda tangan artefak (sha256, dsb.) | Verifikasi integritas vs nilai yang diterbitkan sumber |
| Catatan provenance sumber data | Daftar sumber data + siapa bisa menulis ke sana |
| `~/workspace/catatan/log-bug-bounty.md` | Log jalur + hasil audit + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Artefak/dataset: [nama + sumber + hash]
Jalur: [J1/J2/J3 + penjelasan]
Provenance: [sumber data + siapa bisa menulis]
Integritas: [hash cocok / tidak cocok / tidak bertanda tangan]
Perilaku lab: [pemicu diuji + hasil 3× ulangan]
Program pembayar: [TIDAK ADA yang terverifikasi — riset/audit saja]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [diaudit / terbukti / dilaporkan-sebagai-riset / ditolak]
```

## Batasan yang diketahui

- Metodologi ini dari riset (Wraith Academy Modul 11), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Belum ada program in-scope aktif yang membayar kategori ini** — prioritas rendah sebagai perburuan; nilai utamanya riset/audit dan pemahaman ancaman.
- Tanpa akses training, audit hanya bisa membuktikan provenance/integritas dan perilaku pemicu — bukan isi data latih yang sebenarnya.
- Jangan pernah meracuni dataset/model milik orang lain, walau "untuk pembuktian" — demonstrasi hanya pada salinan lab sendiri.
