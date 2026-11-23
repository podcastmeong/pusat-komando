# Skill: Audit RAG & LLM — Metodologi Audit Keamanan Arsitektur RAG & Aplikasi LLM

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi audit dari riset (referensi: `~/workspace/catatan/referensi-skill-audit-rag-llm-2026-11-24.md`, SKILL.md lengkap, OWASP Top 10 for LLM Applications), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Ditemukan fitur chatbot AI, asisten virtual, atau pencarian semantik pada target.
- Ditemukan endpoint API terkait inferensi model, embedding, atau vector database.
- Cipta atau Muse meminta peninjauan keamanan pada integrasi LLM/RAG.
- Dipakai SEBELUM pengujian RAG/LLM apa pun: pemetaan arsitektur dulu, hipotesis kemudian, pengujian terakhir.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan arsitektur + menjalankan area pengujian A–E |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Keracunan/persistensi konten RAG (arah masuk, konten beracun bertahan lintas sesi) → skill `racun-rag-memori`.
- Jalur keluar data via konteks/RAG/integrasi (eksfiltrasi) → skill `eksfiltrasi-data-ai`.
- Penyalahgunaan tool/agen (tool misuse, agent abuse) → skill `penyalahgunaan-tool-agen`.
- XSS/SSRF via output AI yang dirender → skill `output-tidak-aman`.
- Ekstraksi system prompt → skill `ekstraksi-system-prompt` berstatus **TUNGGU — jangan dipakai** (out of scope Google AI VRP + 0din, N/A Muse Spark). Skill ini TIDAK menutup ekstraksi system prompt umum — lihat Gerbang 3.1 (ditolak bila tanpa rahasia/kredensial maupun celah otorisasi).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji isolasi dokumen atau riwayat percakapan.
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

### Gerbang 1 — Pemetaan arsitektur 4 komponen

Petakan target SEBELUM menguji apa pun. Tulis peta arsitektur ke log (format di bawah). Standar lulus: keempat komponen teridentifikasi atau dinyatakan "tidak ditemukan" dengan bukti.

1. **Antarmuka Input (Input Channels):** input langsung (kotak obrolan, parameter API); input tidak langsung (dokumen PDF, DOCX, Markdown, ringkasan halaman web, email, tiket dukungan, metadata profil).
2. **Lapisan Retrieval & Vector Store:** bagaimana sistem mengindeks dan mengambil konteks (metadata filter seperti `user_id`, `org_id`, `role`; apakah filter diterapkan per sesi atau tidak).
3. **Integrasi Fungsi & Tools (Plugins / Function Calling):** aksi yang dapat dipicu model (baca database, kirim email, panggil webhook internal, ubah pengaturan akun).
4. **Penanganan Output (Output Sinks):** bagaimana respons model dirender di klien (Markdown, HTML, tautan eksternal, render gambar otomatis).

### Gerbang 2 — Area pengujian A–E

Uji satu area per putaran, dengan dua akun uji sendiri (User A dan User B, tenant/org/peran berbeda). Standar lulus tiap area: indikator yang tercantum teramati ATAU dinyatakan tidak ada dengan bukti negatif.

**A. Isolasi Data & Kontrol Akses pada RAG (multi-tenant):** User A (Org X / Admin) mengunggah dokumen berisi canary string non-sensitif; User B (Org Y / Regular User) bertanya merujuk topik dokumen. Indikator: model mengembalikan/merujuk dokumen User A ke User B = kandidat temuan (kebocoran lintas-tenant). Bila model menolak/tidak merujuk = aman, catat.

**B. Penanganan Input Tidak Langsung (Indirect Context Influence):** apakah sistem memisahkan system instructions dari data eksternal RAG. Indikator: delimiters antara instruksi sistem dan konteks data tidak diterapkan dengan benar (instruksi di dalam dokumen terindeks memengaruhi perilaku agen). Catat: ini permukaan yang sama dengan indirect prompt injection — bukti harus berupa aksi/efek, bukan sekadar jawaban aneh (lihat Gerbang 3.1).

**C. Otoritas Berlebih pada Pemanggilan Fungsi (Excessive Agency):** apakah backend memvalidasi ulang izin sesi (session token / RBAC) sebelum mengeksekusi fungsi. Indikator: agen memicu fungsi sensitif (baca database, kirim email, ubah pengaturan) tanpa verifikasi hak akses di level API backend. Pembuktian: bandingkan respons fungsi memakai sesi User A (berhak) vs User B (tidak berhak) — bila User B berhasil memicu fungsi yang sama = kandidat temuan. Lihat juga `penyalahgunaan-tool-agen` dan `analisis-batas-kepercayaan`.

**D. Eksposur Informasi Sensitif & Konfigurasi:** periksa HTTP response endpoint AI untuk metadata internal (raw chunks + similarity score, path penyimpanan internal, stack trace). Verifikasi conversation ID yang dapat ditebak (IDOR pada riwayat obrolan): minta riwayat User A memakai sesi User B. Indikator: raw chunk milik tenant lain terbaca, atau riwayat User A terbuka untuk User B = kandidat temuan.

**E. Penanganan Output yang Tidak Aman:** apakah klien merender Markdown/HTML tanpa sanitasi; apakah aplikasi otomatis memuat sumber daya eksternal (tag gambar Markdown `![alt](url)`) yang bisa membocorkan parameter URL saat dirender di browser korban. Pembuktian: hanya di browser/sesi sendiri — cetak `document.domain` atau callback canary milik sendiri; jangan libatkan browser korban. Lihat juga `output-tidak-aman`.

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = kebocoran data lintas-akun nyata, eksekusi fungsi tidak sah (IDOR/Privilege Escalation via AI), eksekusi skrip di klien (XSS via output AI). **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat arsitektur/otorisasi, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (User A / User B, tenant/org/peran berbeda) | Wajib untuk area A, C, D. Keduanya milik sendiri. |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke dokumen/konteks uji. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta arsitektur + area pengujian + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI/RAG]
Peta arsitektur: [input channels] | [retrieval & vector store + filter] | [fungsi/tools] | [output sinks]
Area: [A/B/C/D/E + nama area]
Langkah reproduksi: [dua akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Komponen AI/RAG] - [Jenis Kerentanan] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Arsitektur (alur data bermasalah, misal kurangnya filter `tenant_id` pada query vector store); Langkah Reproduksi (dua akun uji terpisah + log HTTP); Rekomendasi Perbaikan (metadata filtering berbasis sesi di vector database, validasi RBAC pada setiap tool handler, sanitasi output HTML/Markdown).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP Top 10 for LLM Applications), bukan pengalaman teruji — tiap area butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik — gunakan skill ini sebagai metodologi audit, bukan daftar target.

## Available connectors

- Gmail (`/opt/hatch/connectors/gmail/CONNECTOR.md`) — membaca email uji sendiri bila area B memakai email sebagai input tidak langsung.
- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for LLM.

## Websites

- OWASP Top 10 for LLM Applications — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target bukan RAG/LLM (aplikasi web klasik), pakai `fondasi-kerentanan-web-api` + skill Fase 5/6 (injeksi, client-side).
- Bila fokusnya keracunan/persistensi konten RAG (bukan audit arsitektur), pakai `racun-rag-memori`.
- Bila fokusnya jalur keluar data via RAG, pakai `eksfiltrasi-data-ai`.
