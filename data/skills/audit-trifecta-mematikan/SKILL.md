# Skill: Audit Trifecta Mematikan — Audit Tiga Kaki (Data Privat + Konten Tak Tepercaya + Saluran Keluar) per Panggilan Model

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi audit dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 1; Simon Willison, "The lethal trifecta", 16 Jun 2025; Meta "Agents Rule of Two", 31 Okt 2025), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah aplikasi/agen AI yang dalam satu sesi bisa membaca data privat, menerima konten tak tepercaya, DAN melakukan aksi/komunikasi keluar (kirim email, panggil API, ubah state).
- Ditemukan fitur agen yang menggabungkan retrieval dokumen + pemrosesan konten eksternal (email, halaman web, file) + tool aksi.
- Dipakai SEBELUM pengujian injeksi/eksfiltrasi apa pun pada agen: audit trifecta dulu, hipotesis kemudian, pengujian terakhir.
- Studi kasus rujukan: EchoLeak (CVE-2025-32711, zero-click) — trifecta lengkap yang dibuktikan lewat kanal keluar; pakai skill ini + `eksfiltrasi-markdown` untuk memetakan kasus sejenis.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan tiga kaki per panggilan model + menjalankan gerbang pengujian |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Keracunan/persistensi konten RAG (arah masuk, konten beracun bertahan lintas sesi) → skill `racun-rag-memori`.
- Jalur keluar data via konteks/RAG/integrasi (eksfiltrasi) → skill `eksfiltrasi-data-ai`.
- Penyalahgunaan tool/agen (tool misuse, agent abuse) → skill `penyalahgunaan-tool-agen`.
- XSS/SSRF via output AI yang dirender → skill `output-tidak-aman`.
- Kanal keluar lewat gambar/tautan Markdown yang dirender di klien → skill `eksfiltrasi-markdown`.
- Scope/batas kepercayaan secara umum (tanpa metode hitung tiga kaki) → skill `scope-and-safety-guardian`, `analisis-batas-kepercayaan`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji tiap kaki trifecta.
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

### Gerbang 1 — Petakan tiga kaki per panggilan model

Untuk SETIAP panggilan model/agen yang in-scope, jawab tiga pertanyaan dengan bukti (ya/tidak + sumber bukti). Tulis peta ke log. Standar lulus: ketiga kaki terjawab untuk tiap panggilan model yang dipetakan.

1. **Kaki A — Akses data privat:** apakah panggilan ini bisa membaca data sensitif milik pengguna (dokumen, email, kalender, kredensial, riwayat)? Catat sumber data + izin apa yang dipegang agen.
2. **Kaki B — Paparan konten tak tepercaya:** apakah panggilan ini menerima konten yang bisa ditulis pihak luar (email masuk, halaman web, dokumen bersama, komentar, tool output)? Catat tiap sumber konten + siapa yang bisa menulisnya.
3. **Kaki C — Saluran komunikasi keluar:** apakah panggilan ini bisa memicu aksi keluar (kirim email/pesan, panggil API/webhook, ubah state, render gambar/tautan yang dimuat browser)? Catat tiap saluran, termasuk yang non-obvious: request web, render gambar Markdown, tautan untuk diklik pengguna.

### Gerbang 2 — Terapkan aturan dua-dari-tiga (Rule of Two)

Nilai tiap panggilan model dengan kriteria yang bisa dihitung:

- **0–1 kaki hadir = aman** (catat, lanjut ke panggilan berikutnya).
- **2 kaki hadir = waspada** — catat kombinasi kakinya; agen hanya boleh memegang maksimal dua dari tiga dalam satu sesi. Bila kombinasi A+B atau A+C atau B+C hadir tanpa pemisah yang terbukti (approval, sanitasi, pemisah konteks), lanjut ke Gerbang 2b.
- **3 kaki hadir = TRIFECTA LENGKAP = kandidat temuan** — lanjut ke Gerbang 2b.

**Gerbang 2b — Uji pemisah (bila 2–3 kaki hadir):** periksa apakah ada pemisah yang benar-benar ditegakkan antara kaki-kaki itu: (a) konfirmasi manusia sebelum aksi keluar, (b) pemisahan konteks instruksi vs data, (c) filter egress (destinasi/format yang diblokir). Uji tiap pemisah dengan canary palsu milik sendiri: pemisah yang lolos saat diuji normal tapi gagal saat konten tak tepercaya memancing aksi = pemisah tidak ditegakkan. Catat hasil tiap pemisah.

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = trifecta lengkap (3 kaki) TERBUKTI dengan aksi keluar nyata memakai canary palsu (mis. canary terkirim ke server canary milik sendiri, atau aksi tool sensitif terpicu oleh konten tak tepercaya milik sendiri). **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat arsitektur/otorisasi, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (User A / User B, tenant/org/peran berbeda) | Wajib untuk menguji kaki A (data privat milik siapa yang bisa dibaca). Keduanya milik sendiri. |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan sebagai "data privat" dan sebagai pemicu di konten tak tepercaya. |
| Konten tak tepercaya milik sendiri | Email/dokumen/halaman milik sendiri yang berisi instruksi pemancing — satu-satunya konten tak tepercaya yang dipakai. |
| Server canary milik sendiri | Penampung callback untuk membuktikan kaki C (saluran keluar) tanpa melibatkan pihak lain. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta trifecta + hasil uji pemisah + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur agen AI]
Panggilan model: [nama alur/fitur yang diaudit]
Kaki A (data privat): [ya/tidak + sumber data + izin]
Kaki B (konten tak tepercaya): [ya/tidak + sumber konten + siapa bisa menulis]
Kaki C (saluran keluar): [ya/tidak + tiap saluran, termasuk non-obvious]
Skor trifecta: [0/1/2/3 kaki]
Pemisah diuji: [konfirmasi/pemisah konteks/filter egress + hasil uji]
Langkah reproduksi: [dua akun uji + konten pemancing + aksi keluar yang terpicu]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur Agen] - Trifecta lengkap (data privat + konten tak tepercaya + saluran keluar) memungkinkan [Dampak Spesifik]`. Isi laporan: Peta Trifecta (tiga kaki + bukti tiap kaki); Langkah Reproduksi (dua akun uji + konten pemancing milik sendiri + callback canary); Rekomendasi Perbaikan (terapkan rule-of-two: pisahkan sesi baca data privat dari sesi yang menerima konten tak tepercaya, atau wajibkan konfirmasi manusia sebelum aksi keluar).

## Batasan yang diketahui

- Metodologi ini dari riset (Simon Willison + Meta), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Trifecta lengkap tanpa aksi keluar yang terbukti (hanya potensi) = bukan temuan yang dibayar — bukti harus berupa aksi/canary yang benar-benar keluar.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik — gunakan skill ini sebagai metodologi audit, bukan daftar target.

## Available connectors

- Gmail (`/opt/hatch/connectors/gmail/CONNECTOR.md`) — membaca email uji sendiri bila kaki B memakai email sebagai konten tak tepercaya.
- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan sumber trifecta.

## Websites

- Simon Willison, "The lethal trifecta" — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Meta, "Agents Rule of Two" — rujukan aturan dua-dari-tiga (cek dokumentasi publik Meta).
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya satu kanal keluar spesifik lewat gambar/tautan Markdown, pakai `eksfiltrasi-markdown`.
- Bila fokusnya audit arsitektur RAG/LLM secara umum (bukan trifecta per panggilan model), pakai `audit-rag-llm`.
- Bila fokusnya penyalahgunaan tool/izin agen, pakai `penyalahgunaan-tool-agen`.
