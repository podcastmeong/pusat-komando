# Skill: Latihan Primitif Akademi Wraith — Kurikulum Latihan Agen AI Sebelum Submit

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah kurikulum latihan dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 68; Wraith Academy, https://www.wraith.sh/ dan https://www.wraith.sh/academy), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebelum submit bounty AI pertama / sebelum menguji kelas serangan baru — latihan dulu, submit kemudian (prinsip Wraith: "train the attack classes first, then submit").
- Agen (atau anggota tim) belum pernah mengeksekusi suatu kelas serangan terhadap agen live.
- Dipakai sebagai jalur latihan terstruktur, BUKAN sebagai teknik serang atau pelaporan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menjalankan modul + challenge + mencatat flag dan pelajaran |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Skill induk perburuan (perintah kerja, bukan kurikulum latihan) → skill `buru-bug-bounty`.
- Lab MCP rentan (setara DVWA untuk MCP) → kandidat 32 (`latihan-mcp-rentan`, kelompok lain). Yang itu lab MCP; yang ini kurikulum latihan agen AI (modul + CTF melawan agen live + sertifikasi).
- Skill ini adalah SATU-SATUNYA kandidat bertipe pelatihan (bukan teknik serang atau pelaporan) di antara 170+ skill — tidak ada skill latihan/drill lain. Memenuhi slogan Cipta: gratis, AI boleh ikut (Wraith Academy gratis).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Latihan dilakukan di platform latihan Wraith Academy (gratis) — BUKAN pada target bounty live; teknik yang dipelajari baru dipakai ke target live bila targetnya in-scope.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri saat latihan maupun saat tekniknya diterapkan.
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

### Gerbang 1 — Jalur modul (11 modul, ±45–60 menit/modul)

Urutan modul Wraith Academy — pelajari modulnya DULU, challenge-nya kemudian:

| # | Modul | Skill teknik yang dipetakan |
|---|---|---|
| 1 | How LLMs Work | Dasar — wajib pertama |
| 2 | Prompt Injection | `perburuan-llm-ai` |
| 3 | Indirect Prompt Injection | `injeksi-prompt-tidak-langsung-agen` |
| 4 | System Prompt Extraction | `ekstraksi-system-prompt` — status TUNGGU, jangan dipakai di target live |
| 5 | Tool Abuse | `penyalahgunaan-tool-agen` |
| 6 | Data Exfiltration | `eksfiltrasi-data-ai` |
| 7 | Jailbreaks & Guardrail Bypass | `perburuan-llm-ai`, `jailbreak-universal-lintas-topik` (kriteria) |
| 8 | Insecure Output Handling | `output-tidak-aman` |
| 9 | Vector & Embedding Weaknesses | `perburuan-rag-vektor`, `audit-rag-llm` |
| 10 | Unbounded Consumption | `pengujian-konsumsi-tak-terbatas` — peringatan DoS berlaku |
| 11 | Memory Poisoning | `racun-rag-memori` |
| 12 | Data & Model Poisoning | `racun-data-model-pelatihan` — riset/audit, bukan hadiah |

Standar lulus per modul: ringkasan 3–5 baris (apa primitifnya, apa oracle pengujiannya, apa yang TIDAK boleh dilakukan) ditulis ke log sebelum lanjut ke challenge-nya.

### Gerbang 2 — Challenge CTF melawan agen live (23 challenge)

Kerjakan challenge Wraith melawan agen live di platform latihan: ekstrak flag, lalu tulis PELAJARAN (kenapa serangan berhasil — primitif mana, lapis pertahanan mana yang gagal, apa yang berubah bila lapis itu diperbaiki). Satu challenge = satu entri log: flag (boleh dicatat sebagai "diperoleh/tidak"), teknik yang berhasil, dan pelajaran. Standar lulus: minimal 5 flag untuk membuka ujian WCAP (lihat Gerbang 3); tiap flag disertai pelajaran tertulis — flag tanpa pelajaran = latihan belum selesai.

### Gerbang 3 — Ujian sertifikasi WCAP

Syarat: 5 flag (kohort pendiri, gratis). Ujian: 24 jam, 10 skenario, dinilai otomatis, masuk registry publik bila lulus. Peringkat Wraith: Initiate → Operator → Specter → Wraith. Standar lulus: ujian diambil HANYA bila Gerbang 1–2 selesai; hasil (lulus/gagal + skenario yang gagal + pelajarannya) dicatat ke log. Gagal ujian = kembali ke Gerbang 1–2 pada modul skenario yang gagal, bukan mengulang ujian membabi buta.

## Alat

| Alat | Cara pakai |
|---|---|
| Wraith Academy (https://www.wraith.sh/academy, gratis) | Platform latihan: 11 modul + 23 challenge + ujian WCAP |
| Basis data 58 insiden nyata (Wraith) | Bahan belajar pola serangan nyata per modul |
| `~/workspace/catatan/log-bug-bounty.md` | Log modul + flag + pelajaran + hasil WCAP |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Modul: [nomor + nama] — ringkasan: [3–5 baris: primitif + oracle + larangan]
Challenge: [nama] — flag: [diperoleh/tidak] — teknik berhasil: [..] — pelajaran: [kenapa berhasil]
Flag total: [n/23] — peringkat: [Initiate/Operator/Specter/Wraith]
WCAP: [belum syarat / siap / lulus / gagal — skenario gagal: ..]
Status: [latihan-berjalan / siap-submit-kelas-X / WCAP-lulus]
```

## Batasan yang diketahui

- Kurikulum ini dari riset (Wraith Academy), bukan pengalaman teruji — label BELUM DIUJI berlaku sampai tim menyelesaikan modul + challenge dan mencatat hasilnya di log.
- Latihan di platform Wraith BUKAN pengujian bounty — teknik yang dipelajari tetap tunduk pada Aturan keras (khususnya in-scope + tanpa uji korban) saat diterapkan ke target live.
- Modul 4 (System Prompt Extraction) tetap berstatus TUNGGU untuk target live — pelajari teorinya, jangan pakai di target bounty.
- Peringkat dan syarat WCAP mengikuti ketentuan Wraith saat itu — cek halaman akademi bila berubah.
