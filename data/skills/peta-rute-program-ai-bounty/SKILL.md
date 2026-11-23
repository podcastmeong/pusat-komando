# Skill: Peta Rute Program AI Bounty — Kirim Temuan ke Program yang Membayarnya

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi routing dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 63; Wraith, "AI Bug Bounty Programs 2026", https://www.wraith.sh/learn/ai-bug-bounty-programs), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebuah temuan AI/LLM sudah lolos `gerbang-tujuh-pertanyaan-triase` dan `skeptic-false-positive-eliminator`, dan harus diputuskan program tujuannya.
- Sebelum menulis laporan apa pun: routing diputuskan DULU, baru format laporan dipilih (format per program berbeda).
- Ada keraguan apakah kelas temuan dibayar oleh program yang sedang diincar.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menentukan rute program per temuan + memverifikasi tier dari sumber primer |
| Audit | **A60 Security Auditor** | Memeriksa apakah rute dan klaim tier punya bukti sumber primer |
| Pemimpin | **Muse** | Memutuskan rute final sebelum draf laporan dibuat |

## Sudah tercakup (jangan diduplikat)

- Parse aturan SATU program (scope, eksklusi, cara kirim) → skill `parsing-scope-program`.
- Pantau perubahan scope/hadiah/deadline program dari waktu ke waktu → skill `recon-pantau-program`.
- Skor temuan per tier hadiah + aturan duplikat (termasuk aturan duplikat 0din) → skill `triase-duplikat`.
- Format laporan per platform → skill `laporan-poc-otomatis`, `tulis-laporan-yeswehack`.
- Skill ini HANYA menjawab: "temuan kelas X sebaiknya dikirim ke program mana" — fungsi routing lintas-program beserta jebakan eksklusinya. Bukan parse scope, bukan pantau deadline, bukan skor duplikat.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan kelas temuan berada dalam in-scope program TUJUAN sebelum routing diputuskan.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji kelas temuan di program tujuan.
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

### Gerbang 1 — Klasifikasikan temuan ke kelas (bukan ke program dulu)

Tentukan kelas temuan dari bukti, BUKAN dari program yang sedang disukai. Kelas utama: indirect prompt injection (via Connector/MCP, dokumen, email, web, tool output), jailbreak/guardrail bypass, tool abuse / rogue actions, eksfiltrasi data sensitif via AI, memory/context poisoning, RAG isolation (lintas-tenant), model/artefak poisoning, unbounded consumption, jailbreak universal. Tulis kelas + bukti outcome-nya (aksi nyata/data keluar) ke log. Standar lulus: kelas teridentifikasi dan outcome-nya terbukti, bukan sekadar "jawaban aneh".

### Gerbang 2 — Terapkan matriks rute + jebakan eksklusi

| Kelas temuan | Rute utama | Jebakan eksklusi |
|---|---|---|
| Indirect prompt injection berdampak (agen beraksi tanpa konfirmasi, kirim data ke destinasi penyerang) | OpenAI Safety; 0din; Google AI VRP (sebagai mekanisme di balik S1 Rogue Actions / S2 Sensitive Data Exfiltration) | Direct injection ke Google AI VRP = $0 (yang dibayar INDIRECT-nya); jangan kirim direct PI ke Google |
| Jailbreak / guardrail bypass sekali-pakai | 0din; OpenAI Safety | Google AI VRP = $0 (jailbreak EKSPLISIT out of scope); jailbreak semata tanpa outcome = tidak dibayar di mana pun |
| Jailbreak universal (lintas topik/model, sesi bersih) | Anthropic Model Safety; OpenAI Bio Bounty (khusus bio) | Lihat `jailbreak-universal-lintas-topik` — kriteria universalitas wajib dibuktikan dulu |
| Tool abuse / rogue actions / bypass otorisasi agen | OpenAI Safety; Google AI VRP S1; 0din | — |
| Eksfiltrasi data sensitif via AI | Google AI VRP S2; OpenAI Safety; 0din | Halusinasi / jawaban aneh tanpa data keluar = bukan temuan |
| Memory/context poisoning, RAG isolation lintas-tenant | 0din; OpenAI Safety | — |
| System prompt extraction | TIDAK ADA rute aktif untuk Muse Spark | 0din: Prompt Extraction N/A untuk Muse Spark; skill `ekstraksi-system-prompt` status TUNGGU — jangan dipakai |
| Unbounded consumption / DoS | TIDAK ADA rute terverifikasi | Lihat `pengujian-konsumsi-tak-terbatas` — DoS tidak dibayar menurut posisi tim saat ini |
| Data/model poisoning (tahap pelatihan) | TIDAK ADA rute terverifikasi | Lihat `racun-data-model-pelatihan` — nilai riset/audit, bukan hadiah |

Bila kelas tidak punya rute (baris "TIDAK ADA rute") → STOP. Jangan memaksakan pengiriman ke program yang tidak membayar kelas itu; catat sebagai riset, bukan laporan. Standar lulus: satu rute utama + satu rute cadangan tercatat, keduanya lolos cek eksklusi.

### Gerbang 3 — Verifikasi tier hadiah dari sumber primer SEBELUM menulis laporan

**PERINGATAN ANGKA — diskrepansi terverifikasi:** file riset mencatat angka Wraith (artikel 8 Jun 2026) bertentangan dengan catatan tim 23 Nov 2026: OpenAI Safety maks $100rb (Wraith) vs P1 $5.500–$7.500 (catatan tim di `triase-duplikat`); Anthropic maks $15rb/temuan (Wraith) vs $35rb (catatan tim di `buru-bug-bounty`). **JANGAN pakai angka hadiah dari Wraith tanpa verifikasi.** Angka HANYA boleh ditulis bila terverifikasi dari sumber primer program (halaman program / platform bounty-nya sendiri). Bila belum terverifikasi, tulis "belum terverifikasi dari sumber primer" dan arahkan ke `recon-pantau-program` untuk cek terbaru.

Tier yang tercatat di `triase-duplikat` (terverifikasi tim 23 Nov 2026 — tetap cek ulang ke sumber primer sebelum dipakai di laporan): Muse (Meta) $500 minimum s.d. $300rb; OpenAI Safety P1 $5.500–$7.500, pool $1jt/tahun; Google AI VRP S1 $20rb, S2 $15rb, A1/A2 $5rb, maks $30rb/laporan; 0din Low ≤$500, Medium ≤$2.500, High ≤$5.000, Severe ≤$15.000; ViKernel $500–$1.000/musim. Standar lulus: tier tertulis beserta sumber primernya (URL + tanggal cek) atau ditandai belum terverifikasi.

### Gerbang 4 — Urutan titik mulai

Urutan default bila beberapa rute valid: **0din dulu → kompetisi yang in-scope → Anthropic / OpenAI Safety**. Alasan: 0din punya scope LLM paling luas dan alur abstrak-dulu (risiko duplikat lebih kecil bila abstrak diterima); Anthropic dan OpenAI Safety/Bio bersifat lamaran/privat dan triase-nya lambat. Bila temuan bersifat time-sensitive (duplikat berisiko tinggi), dahulukan program dengan triase tercepat menurut `recon-pantau-program`. Standar lulus: urutan tertulis + alasan; bila rute cadangan dipilih, alasannya dicatat.

## Alat

| Alat | Cara pakai |
|---|---|
| `parsing-scope-program` | Parse scope program tujuan sebelum routing final |
| `recon-pantau-program` | Cek terbaru tier hadiah, deadline, dan status program tujuan |
| `triase-duplikat` | Skor temuan per tier + cek duplikat sebelum kirim |
| `~/workspace/catatan/log-bug-bounty.md` | Log rute yang diputuskan + sumber primer tier + alasan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Temuan: [kelas + outcome terbukti]
Rute utama: [program] — alasan: [kenapa kelas ini dibayar di sana]
Rute cadangan: [program] — alasan: [..]
Jebakan eksklusi dicek: [mis. direct PI ke Google = $0 — lolos/tidak relevan]
Tier hadiah: [angka + sumber primer + tanggal cek, atau "belum terverifikasi dari sumber primer"]
Urutan kirim: [0din dulu / dst. + alasan]
Status: [dirute / ditunda — tidak ada rute terverifikasi / dilaporkan]
```

## Batasan yang diketahui

- Matriks ini dari riset Wraith (artikel 8 Jun 2026) + catatan tim 23 Nov 2026 — angka hadiah berubah; SELALU cek sumber primer sebelum laporan.
- Program lamaran-only/privat (OpenAI Bio Bounty, xAI) triase-nya lambat (berbulan-bulan) — jangan jadikan rute utama untuk temuan yang rawan duplikat.
- Gray Swan Arena DILEWATI total atas perintah Cipta (18:35) — bukan rute, walau pool-nya besar.
- HackAPrompt tidak ada edisi 2026 — bukan rute.
