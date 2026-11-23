# Skill: Jebakan per Kelas Kerentanan — Ambang Bukti Minimum + Pola Auto-Close + Jebakan Overclaim

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah katalog referensi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 5 kandidat 70; YesWeHack Claude Kit, skill `gotchas`, https://www.yeswehack.com/learn-bug-bounty/triager-grade-reports-claude-code), bukan pengalaman teruji sampai ada laporan yang lolos triase berkat katalog ini dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Draf laporan sudah ada dan kelas kerentanannya diketahui — cek katalog ini SEBELUM kirim (referensi cek cepat, bukan alur kerja).
- Ragu apakah bukti PoC sudah cukup untuk kelas itu, atau apakah klaim dampaknya berlebihan.
- Dipakai bersama `simulasi-triase-pra-kirim` (langkah "gotchas per kelas") dan sebelum menulis seksi PoC/Impact di `tulis-laporan-yeswehack`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Mencocokkan draf dengan baris katalog kelasnya + menandai yang gagal ambang |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Katalog CARA membuktikan aman per jenis → skill `verifikasi-poc-aman` (itu cara membuktikan; skill ini ambang bukti minimum + pola auto-close + jebakan overclaim per kelas).
- Filter penolakan 4 gerbang (default TOLAK) → skill `skeptic-false-positive-eliminator` (itu alur penolakan; skill ini referensi per kelas).
- Skor keparahan → skill `penilaian-cvss`; artikulasi dampak → skill `artikulasi-dampak-bisnis`.
- Skill ini HANYA katalog referensi cek cepat per kelas — bukan alur kerja, bukan cara membuktikan, bukan filter penolakan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan kelas + aset yang dilaporkan in-scope.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya bukti dari akun uji milik sendiri.
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

### Gerbang 1 — Cocokkan kelas temuan dengan baris katalog

Cari kelas temuan di tabel. Tiap baris berisi tiga hal: (a) bukti minimum yang WAJIB ditunjukkan PoC; (b) pola false positive yang langsung ditutup (auto-close); (c) jebakan klaim dampak berlebihan (overclaim). Bila kelas tidak ada di tabel → catat sebagai "kelas di luar katalog" dan pakai `verifikasi-poc-aman` + `skeptic-false-positive-eliminator` sebagai pengganti.

| Kelas | (a) Bukti minimum PoC | (b) Pola auto-close (langsung ditutup) | (c) Jebakan overclaim |
|---|---|---|---|
| XSS | Skrip dieksekusi di konteks korban (bukti eksekusi, mis. `document.domain` dari sesi uji sendiri) — bukan sekadar payload terpantul di respons | Payload terpantul tapi tidak dieksekusi; self-XSS (hanya menyerang diri sendiri) | Klaim "akun takeover" tanpa rantai ke aksi sensitif |
| SQLi | Data/kondisi dari database terbukti (error berbasis data, blind boolean/time yang konsisten) — bukan sekadar error sintaks | Error sintaks generik tanpa ekstraksi/kondisi; WAF block | Klaim "dump seluruh DB" dari satu error |
| SSRF | Server benar-benar melakukan request ke target internal DAN body respons metadata terbaca — resolve DNS saja = baru lookup, bukan request | Hanya resolve DNS / hanya koneksi tanpa respons; URL yang diizinkan (allowlist) | Klaim "RCE internal" dari SSRF tanpa bukti lanjutan |
| IDOR | Objek milik akun uji A terbaca/diubah dari sesi akun uji B (dua akun sendiri) | ID tak tertebak (UUID) tanpa cara memperoleh ID korban — nilai sebagai AC:H, bukan kritis; objek milik sendiri saja | Klaim dampak massal tanpa cara memperoleh ID korban |
| CSRF | Aksi state-changing tereksekusi lintas-situs tanpa token valid (bukti request berhasil dari origin lain) | GET tanpa efek samping; token valid tapi diklaim "bypass" tanpa bukti; SameSite=Lax menahan | Klaim "akun takeover" dari CSRF ganti profil non-sensitif |
| RCE | Perintah dieksekusi di server (bukti output perintah / callback canary server sendiri) | Output perintah dari sisi klien saja; error tanpa eksekusi | Klaim "kompromi penuh" dari satu perintah `id` tanpa eskalasi |
| SSTI | Ekspresi template dievaluasi server (mis. `7*7` → `49` di respons server) | Refleksi tanpa evaluasi; error template tanpa evaluasi | Klaim RCE dari SSTI tanpa rantai ke eksekusi |
| XXE | Entitas eksternal diproses server (file internal terbaca / callback canary) | Parser menolak DTD; error tanpa pembacaan | Klaim "baca semua file" dari satu file terbaca |
| Race condition | Invarian yang TERSIMPAN rusak (saldo/jumlah ganda tercatat di server) — bukan sekadar banyak respons 200 | Banyak respons 200 tanpa perubahan state yang tersimpan; duplikat yang ditolak server | Klaim "saldo ganda" tanpa bukti state tersimpan |
| CORS | Origin penyerang membaca respons DENGAN credentials (bukti baca lintas-origin + kredensial) | `Access-Control-Allow-Origin: *` TANPA credentials = bukan temuan | Klaim "baca data korban" dari `*` tanpa credentials |
| Open redirect | Redirect ke domain penyerang terbukti DAN dirantai (mis. pencurian token OAuth → ATO) | Redirect ke domain sendiri/subdomain tepercaya; redirect tanpa rantai dampak | Klaim "phishing" tanpa rantai ke token/akun |
| Info disclosure | Data sensitif nyata terbaca (bukan kunci publik) | Kunci publik seperti Firebase/Stripe `pk_` = bukan temuan; versi server saja | Klaim "kebocoran massal" dari satu record uji sendiri |
| Path traversal / LFI | File di luar webroot terbaca (bukti isi file uji sendiri / canary) | Error path tanpa isi file; file yang memang publik | Klaim "baca /etc/passwd" tanpa isi file terbaca |
| Client-side template injection | Ekspresi dievaluasi di klien dalam konteks aplikasi (bukti evaluasi, bukan refleksi) | Refleksi tanpa evaluasi; sandbox template menahan | Klaim XSS dari CSTI tanpa bukti eksekusi |

Standar lulus: baris kelas ditemukan; (a) terpenuhi dengan bukti; (b) tidak cocok dengan pola auto-close; (c) klaim dampak sudah diturunkan ke yang terbukti.

### Gerbang 2 — Turunkan klaim dampak ke yang terbukti

Bila (c) terlanggar (klaim melebihi bukti): turunkan severity/klaim ke tingkat yang dibuktikan (mis. IDOR UUID → AC:H; SSRF DNS-only → bukan temuan / info saja). Tulis penurunan itu ke log — triager menghargai klaim jujur lebih dari klaim besar yang runtuh. Standar lulus: tidak ada klaim di draf yang melebihi bukti PoC.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** bukti minimum (a) terpenuhi. Tidak terpenuhi = TOLAK, lengkapi bukti dulu.
2. **Reproduksibilitas deterministik — standar lulus:** PoC diulang minimal **3 kali** (LLM) atau 1× deterministik (web klasik). Gagal direproduksi = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya draf yang lolos ketiga gerbang di atas yang diteruskan ke `simulasi-triase-pra-kirim` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Tabel katalog di atas (14 kelas) | Referensi cek cepat sebelum kirim |
| `verifikasi-poc-aman` | Cara membuktikan aman per jenis (bila kelas di luar katalog) |
| `skeptic-false-positive-eliminator` | Filter penolakan bila katalog memberi sinyal meragukan |
| `~/workspace/catatan/log-bug-bounty.md` | Log hasil cek katalog + penurunan klaim |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Kelas: [nama kelas]
Bukti minimum: [terpenuhi/tidak — bukti: ..]
Pola auto-close: [cocok/tidak — pola: ..]
Klaim dampak awal: [..] → diturunkan menjadi: [..]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dicek / siap-kirim / ditolak]
```

## Batasan yang diketahui

- Katalog ini dari riset (YesWeHack Claude Kit, 14 kelas), bukan pengalaman teruji — butuh laporan yang lolos triase berkat katalog ini sebelum label BELUM DIUJI dicabut.
- Kelas AI/LLM (prompt injection, jailbreak, RAG) TIDAK ada di katalog 14 kelas ini — untuk kelas AI pakai `audit-rag-llm`, `injeksi-prompt-tidak-langsung-agen`, dan `jailbreak-universal-lintas-topik`.
- Pola auto-close bersifat umum — program tertentu bisa punya kebijakan berbeda; `parsing-scope-program` tetap dibaca untuk program tujuan.
