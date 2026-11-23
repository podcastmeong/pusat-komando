# Skill: Kegagalan Berantai Agen — Efek Domino, Perambatan Racun Antar-Agen & Tidak Adanya Circuit Breaker

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 9; OWASP ASI08:2026 Cascading Failures), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah sistem multi-agen/rantai agen yang berjalan: satu agen yang keliru/terkompromi bisa meracuni agen hilir lewat output/memori bersama, atau loop perbaikan-diri yang berputar tanpa henti.
- Ditemukan rantai agen tanpa circuit breaker, tanpa batas percobaan ulang, atau tanpa pemisah antara agen hulu dan hilir.
- Dipakai saat menguji PERAMBATAN KEGAGALAN antar-agen dalam satu sistem yang berjalan — BUKAN rantai exploit oleh penguji (itu `eskalasi-dampak-otomatis`, `perangkaian-kerentanan`) dan BUKAN pesan antar-agen yang dipalsukan (itu `komunikasi-antar-agen-tidak-aman`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan rantai agen + menguji perambatan + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Eskalasi/merangkai temuan tunggal oleh penguji → skill `eskalasi-dampak-otomatis`, `perangkaian-kerentanan`.
- Pesan antar-agen yang dipalsukan/disusupi → skill `komunikasi-antar-agen-tidak-aman`.
- Racun memori/RAG antar-sesi → skill `racun-rag-memori`.
- Loop/edge-case logika aplikasi (overflow, timeout parsial, gagal rollback) → skill `kondisi-luar-biasa`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah); semua agen dalam rantai yang diuji adalah agen milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan. **Khusus skill ini:** loop perbaikan-diri diuji dengan BATAS — maksimal 3 putaran loop yang diamati, lalu berhenti dan catat; JANGAN membiarkan loop berputar tanpa henti sampai kuota/token habis.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan rantai agen + blast radius

Petakan rantai dan titik pemutusnya. Tulis peta ke log. Standar lulus: tiap titik terjawab atau dinyatakan "tidak ditemukan" dengan bukti.

1. **Rantai:** agen apa saja yang tersusun berantai (hulu → hilir)? Output agen mana yang menjadi input/memori agen berikutnya? Apakah ada memori bersama?
2. **Blast radius:** bila satu agen keliru, agen/aksi apa saja yang ikut terpengaruh? Seberapa jauh dampaknya bisa merambat (satu rantai, seluruh sistem)?
3. **Titik pemutus:** apakah ada circuit breaker (batas percobaan ulang, batas waktu, validasi output antar-agen, persetujuan manusia di tengah rantai)? Di mana letaknya — dan apakah benar-benar ditegakkan?
4. **Loop:** apakah ada loop perbaikan-diri (agen memperbaiki outputnya sendiri / agen saling memperbaiki)? Apakah ada batas putaran?

### Gerbang 2 — Uji tiga pola perambatan (satu pola per putaran)

Uji hanya dengan rantai agen milik sendiri + canary palsu. Satu pola per putaran; catat output tiap agen dalam rantai persis.

1. **Pola A — Satu agen keliru meracuni hilir:** buat agen hulu milik sendiri mengeluarkan output yang mengandung fakta/instruksi canary yang salah (mis. kode canary palsu sebagai "fakta" atau instruksi canary sebagai "langkah berikutnya"). Amati apakah agen hilir memakai output itu tanpa verifikasi dan meneruskannya (canary muncul di output hilir, lalu di hilir berikutnya). Indikator: canary merambat ≥2 tingkat tanpa ada yang memverifikasi/menghentikan = kandidat temuan.
2. **Pola B — Loop perbaikan-diri tanpa henti:** buat kondisi di mana agen hulu dan hilir saling "memperbaiki" output satu sama lain (atau satu agen memperbaiki dirinya sendiri) dengan umpan yang tidak pernah memuaskan. Amati maksimal 3 putaran: apakah ada yang menghentikan loop (circuit breaker, batas putaran, eskalasi ke manusia)? Indikator: tidak ada yang menghentikan dalam 3 putaran yang diamati + tidak ada batas yang terdokumentasi = kandidat temuan (catat jumlah putaran yang diamati, lalu HENTIKAN — jangan biarkan berputar terus, aturan keras 5).
3. **Pola C — Tidak ada titik pemutus saat kegagalan:** buat agen hulu gagal secara jelas (output kosong, error, atau output yang bertentangan dengan kebijakan yang dinyatakan). Amati apakah agen hilir tetap melanjutkan seolah tidak ada kegagalan, dan apakah kegagalan itu dilaporkan ke pengguna/manusia. Indikator: rantai melanjutkan tanpa peringatan + kegagalan tidak dilaporkan = kandidat temuan.
4. **Standar lulus tiap pola:** tercatat output tiap agen dalam rantai + berapa tingkat canary/kegagalan merambat + titik pemutus mana yang diuji (dan hasilnya).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = kegagalan/racun TERBUKTI merambat ke agen hilir dan memicu aksi nyata (aksi tool, pengiriman canary ke server milik sendiri, atau keputusan yang diambil dari output yang sudah teracuni) pada akun uji sendiri; ATAU loop tanpa pemutus TERBUKTI berjalan tanpa henti yang teramati. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi; TOLAK juga bila rambatan berhenti di tingkat pertama (ada pemutus yang bekerja).
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat rantai/circuit breaker, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Sertakan output tiap agen dalam rantai sebagai lampiran bukti.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Rantai agen uji milik sendiri | Satu-satunya rantai yang diuji; semua agen hulu/hilir milik sendiri. |
| Canary palsu (string non-sensitif) | Satu-satunya "racun" yang dirambatkan; satu canary unik per percobaan. |
| Server canary milik sendiri | Penampung callback untuk membuktikan aksi keluar di ujung rantai tanpa melibatkan pihak lain. |
| Log output tiap agen dalam rantai | Bukti inti: output hulu → hilir → hilir berikutnya, persis. Simpan lengkap. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta rantai + blast radius + pola uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + sistem/rantai agen]
Peta rantai: [agen hulu → hilir + memori bersama?] | [blast radius] | [titik pemutus: ...] | [loop: ada/tidak + batas putaran]
Pola diuji: [A/B/C + nama pola]
Output per agen (persis): [hulu: ...] → [hilir 1: ...] → [hilir 2: ...]
Rambatan: [canary/kegagalan merambat berapa tingkat + aksi akhir yang terpicu]
Titik pemutus diuji: [nama pemutus + hasil: bekerja/tidak ada/tidak bekerja]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Sistem/Rantai Agen] - Kegagalan [agen hulu] merambat tanpa circuit breaker ke [agen hilir/aksi akhir]`. Isi laporan: Peta Rantai (agen + blast radius + titik pemutus yang tidak ada/tidak bekerja); Langkah Reproduksi (output tiap agen persis + rambatan canary); Rekomendasi Perbaikan (validasi output antar-agen sebelum diteruskan, circuit breaker: batas percobaan ulang + batas waktu + eskalasi ke manusia, pemisah memori antar-agen agar racun tidak menyebar).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP ASI08:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Loop perbaikan-diri HANYA diamati maksimal 3 putaran lalu dihentikan (aturan keras 5) — jangan biarkan loop menghabiskan kuota/token.
- Bila yang diuji adalah pesan antar-agen yang dipalsukan (bukan perambatan kegagalan), pakai `komunikasi-antar-agen-tidak-aman`.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for Agentic Applications.

## Websites

- OWASP Top 10 for Agentic Applications 2026, ASI08 Cascading Failures — https://owasp.org/www-project-top-10-for-agentic-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya merangkai temuan tunggal menjadi rantai exploit, pakai `eskalasi-dampak-otomatis` / `perangkaian-kerentanan`.
- Bila fokusnya pesan antar-agen yang dipalsukan, pakai `komunikasi-antar-agen-tidak-aman`.
- Bila fokusnya racun memori bersama, pakai `racun-rag-memori`.
