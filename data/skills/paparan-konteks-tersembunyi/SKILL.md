# Skill: Paparan Konteks Tersembunyi — Kebocoran RAG, Memori, State, dan Tool Response (OWASP LLM08:2026)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 5; OWASP LLM08:2026 Hidden Context Exposure — kategori baru 2026 yang menggantikan System Prompt Leakage), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah aplikasi AI yang dalam konteksnya memegang hal yang tak boleh keluar: dokumen yang di-retrieve, isi memori, info pengguna lain, state aplikasi, respons tool — lalu menjawab pertanyaan pengguna.
- Ditemukan fitur AI yang menampilkan potongan konteks mentah (raw chunks, kutipan dokumen, isi memori, respons tool) dalam jawaban, log, atau reasoning trace.
- Dipakai saat menguji kebocoran konteks tersembunyi SELAIN system prompt — RAG, memori, state, tool response.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan isi konteks tersembunyi + menguji tiap jalur keluar + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Ekstraksi system prompt umum → skill `ekstraksi-system-prompt` berstatus **TUNGGU — jangan dipakai** (out of scope Google AI VRP + 0din, N/A Muse Spark). **Skill ini TIDAK menutup ekstraksi system prompt umum dan TIDAK memperluas skill itu** — status TUNGGU tetap berlaku dan hanya Cipta yang bisa mengubahnya. Skill ini menutup konteks tersembunyi LAIN: dokumen RAG, memori, state aplikasi, dan respons tool.
- Keracunan/persistensi konten RAG (arah masuk) → skill `racun-rag-memori`.
- Jalur keluar data via konteks/RAG/integrasi (eksfiltrasi umum) → skill `eksfiltrasi-data-ai`.
- Audit arsitektur RAG/LLM secara umum → skill `audit-rag-llm` (khususnya area D: eksposur informasi sensitif & konfigurasi).
- Kebocoran embedding di lapisan vektor → skill `perburuan-rag-vektor`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji tiap jalur keluar konteks.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.
12. **Batas skill ini — JANGAN sentuh ekstraksi system prompt umum:** bila jalur keluar yang diuji mengarah ke system prompt (bukan RAG/memori/state/tool response), STOP dan catat batasannya — itu wilayah `ekstraksi-system-prompt` (status TUNGGU). Skill ini hanya menguji konteks tersembunyi selain system prompt.

## Langkah + gerbang

### Gerbang 1 — Petakan "apa saja yang ada di konteks tapi tak boleh keluar"

Petakan isi konteks tersembunyi target SEBELUM menguji. Tulis peta ke log. Standar lulus: tiap sumber konteks terjawab (ada/tidak + siapa pemiliknya + siapa yang berhak membacanya).

1. **Dokumen yang di-retrieve (RAG):** dokumen apa yang bisa masuk konteks (milik siapa, tenant/org apa)? Apakah ada dokumen yang hanya boleh dibaca pemiliknya?
2. **Isi memori:** memori persisten/sesi apa yang dipegang agen (riwayat percakapan, preferensi, ringkasan)? Milik siapa?
3. **State aplikasi:** state apa yang ada di konteks (pengaturan akun, status langganan, data sesi)?
4. **Respons tool:** respons tool apa yang masuk konteks (hasil baca database, isi email, data API internal)? Apakah respons itu mengandung data yang tak boleh keluar?
5. Untuk tiap sumber catat: jalur keluar yang mungkin — jawaban, log, reasoning trace, ekspor, atau tool output berikutnya.

### Gerbang 2 — Uji tiap jalur keluar (satu sumber × satu jalur per putaran)

Tanam canary palsu unik di tiap sumber konteks milik sendiri, lalu uji apakah canary itu keluar lewat tiap jalur. Satu kombinasi sumber × jalur per putaran.

1. **Jalur jawaban:** ajukan pertanyaan normal yang merujuk topik canary (tanpa menyebut canary). Periksa apakah canary muncul verbatim/di parafrasa dalam jawaban.
2. **Jalur kutipan/sumber:** minta agen mengutip sumber jawabannya. Periksa apakah kutipan itu menampilkan isi dokumen/memori mentah yang seharusnya tidak keluar.
3. **Jalur reasoning trace/log:** bila target menampilkan reasoning/trace/log (atau log itu bisa diakses), periksa apakah canary muncul di sana.
4. **Jalur tool berikutnya:** minta agen memakai tool yang meneruskan konteks (mis. meneruskan pesan, mengekspor ringkasan, membuat dokumen dari percakapan). Periksa apakah canary ikut tersalin ke output tool itu.
5. **Jalur lintas akun (dua akun uji sendiri):** dari akun B (yang tidak berhak atas canary akun A), ajukan pertanyaan merujuk topik canary. Canary akun A muncul di jawaban akun B = kebocoran lintas-akun.
6. **Standar lulus tiap kombinasi:** tercatat pertanyaan persis + respons persis + canary muncul? (ya/tidak + verbatim/parafrasa) + jalur keluarnya.

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = canary dari konteks tersembunyi TERBUKTI keluar lewat salah satu jalur (jawaban, kutipan, trace/log, tool output, atau ke akun lain yang tidak berhak) pada akun uji sendiri. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi (lihat aturan keras 12 — itu wilayah TUNGGU, bukan temuan skill ini).
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat pemisahan konteks, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Canary palsu boleh ditulis di log (tidak ada artinya).

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (User A / User B, tenant/org/peran berbeda) | Wajib untuk jalur lintas akun (Gerbang 2.5). Keduanya milik sendiri. |
| Canary palsu (string non-sensitif) | Satu canary unik per sumber konteks per percobaan — satu-satunya "data sensitif" dalam pengujian. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta konteks tersembunyi + kombinasi sumber × jalur + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI]
Peta konteks tersembunyi: [RAG: ...] | [memori: ...] | [state: ...] | [tool response: ...]
Kombinasi diuji: [sumber konteks + jalur keluar]
Canary: [kode canary + sumber tempat tanam + siapa yang berhak baca]
Langkah reproduksi: [pertanyaan persis + respons persis]
Indikator teramati: [canary muncul? ya/tidak + verbatim/parafrasa + jalur]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur AI] - [Sumber Konteks: RAG/memori/state/tool response] bocor lewat [Jalur Keluar] ke [Pihak yang Tidak Berhak]`. Isi laporan: Peta Konteks (sumber konteks + pemilik + siapa berhak baca); Langkah Reproduksi (dua akun uji + pertanyaan + respons persis dengan canary); Rekomendasi Perbaikan (filter konteks per sesi/tenant sebelum masuk prompt, jangan tampilkan raw chunk/respons tool mentah di jawaban/kutipan/trace, sensor data sensitif di log dan reasoning trace).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP LLM08:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Skill ini SENGAJA tidak menutup ekstraksi system prompt umum — itu tetap TUNGGU (aturan keras 12). Jangan pakai skill ini sebagai jalan memutar untuk ekstraksi system prompt.
- Bila yang bocor adalah data antar-tenant di level jawaban RAG, hasil uji ini bisa dirujuk silang ke `racun-rag-memori` (arah masuk/persistensi) — jangan klaim ulang dampak yang sama di dua skill.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Gmail (`/opt/hatch/connectors/gmail/CONNECTOR.md`) — membaca email uji sendiri bila sumber konteks memakai email.
- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for LLM.

## Websites

- OWASP Top 10 for LLM Applications 2026, LLM08 Hidden Context Exposure — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang diuji adalah kebocoran di lapisan vektor/embedding (bukan jalur keluar jawaban), pakai `perburuan-rag-vektor`.
- Bila fokusnya audit arsitektur RAG/LLM secara umum, pakai `audit-rag-llm`.
- Bila fokusnya jalur keluar data secara umum (email/ekspor/API), pakai `eksfiltrasi-data-ai`.
