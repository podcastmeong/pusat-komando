# Skill: Alat Plexiglass — Toolbox Keamanan LLM Terpadu

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `kortex-labs/plexiglass`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu menguji dan mengamankan LLM dalam satu paket tool — dari pengujian serangan sampai pengamanan deployment — tanpa merangkai banyak tool terpisah.
- Perlu membandingkan hasil satu toolbox terpadu dengan toolbox lain (PurpleLlama, llm-guard).
- Target in-scope memakai Plexiglass sebagai lapisan keamanan LLM-nya dan perlu dinilai kekuatannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang Plexiglass di lab + menjalankan pengujian terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Toolbox keamanan LLM lain dengan cakupan dan perintah berbeda → skill `alat-purplellama`, `alat-llm-guard`.
- Pemindai LLM dengan probe tetap → skill `alat-garak`.
- Eval/red-teaming prompt → skill `alat-promptfoo`.

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

### Gerbang 1 — Pasang Plexiglass di lab sendiri

Plexiglass adalah toolbox keamanan LLM terpadu: satu paket untuk menguji serangan terhadap LLM dan mengamankan deployment-nya.

1. Clone repo: `git clone https://github.com/kortex-labs/plexiglass.git` lalu ikuti `README.md` (instalasi, modul yang tersedia, perintah tiap modul).
2. Inventarisasi modulnya: modul pengujian serangan apa saja yang tersedia, modul pengamanan deployment apa saja, dan perintah dasar tiap modul.
3. Jalankan satu modul pengujian terhadap model/aplikasi uji sendiri untuk memastikan tool berjalan; catat versi dan modul yang dipakai di log.

### Gerbang 2 — Pilih modul yang sesuai dengan target

1. Petakan target in-scope: model mentah, aplikasi RAG, atau alur kerja agen — lalu pilih modul Plexiglass yang sesuai (pengujian serangan vs pengamanan deployment).
2. Bila target memakai Plexiglass sebagai pertahanannya: pelajari modul pengamanannya untuk memahami apa yang diklaim dilindungi, lalu uji klaim itu satu per satu.
3. Bila target tidak memakai Plexiglass: pakai modul pengujiannya sebagai pemindai umum, dan bandingkan hasilnya dengan toolbox lain (`alat-purplellama`, `alat-llm-guard`) bila hasilnya meragukan.

### Gerbang 3 — Uji hasil modul dengan efek nyata

1. Untuk tiap temuan yang ditandai modul Plexiglass: uji ulang manual ke target in-scope dengan akun uji sendiri, 3× per temuan.
2. Temuan valid HANYA bila menghasilkan efek nyata (aksi tidak sah, kebocoran canary/data, bypass pertahanan yang diklaim) — skor/laporan modul sendiri BUKAN bukti.
3. Catat modul mana yang menandai temuan dan apakah temuan itu terkonfirmasi manual atau tidak — ini menilai keandalan modul itu sendiri.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Modul menandai serangan, tapi pengujian manual menunjukkan pertahanan target menahan / model menolak | False positive modul — BUKAN temuan |
| Modul menandai "kerentanan" yang hanya berupa jawaban aneh/halusinasi tanpa efek | False positive — BUKAN temuan |
| Modul menandai DAN pengujian manual membuktikan efek nyata, dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo Plexiglass (`kortex-labs/plexiglass`) | Clone + ikuti README; modul pengujian + modul pengamanan deployment |
| Akun uji sendiri | Wajib untuk Gerbang 3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi Plexiglass + modul dipakai + hasil per modul + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI]
Versi Plexiglass lab: [commit/tag] | Modul dipakai: [daftar modul]
Temuan modul: [modul + temuan yang ditandai]
Verifikasi manual: [langkah + efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur AI target] - [Jenis kerentanan] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool Plexiglass **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Toolbox terpadu berarti cakupan luas tapi tiap modul bisa lebih dangkal daripada tool khusus — bila satu modul memberi hasil meragukan, verifikasi dengan tool khusus (`alat-garak`, `alat-promptfoo`, `alat-llm-guard`).
- Hasil modul BUKAN bukti: efek nyata harus dibuktikan manual (Gerbang 3).
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi Plexiglass dan scope program.

## Websites

- Plexiglass — https://github.com/kortex-labs/plexiglass
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila perlu toolbox lain sebagai pembanding, pakai `alat-purplellama` atau `alat-llm-guard`.
- Bila perlu pemindai probe tetap, pakai `alat-garak`.
- Bila perlu eval/red-teaming kasus uji tetap, pakai `alat-promptfoo`.
