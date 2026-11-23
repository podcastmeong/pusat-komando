# Skill: Komunikasi Antar-Agen Tidak Aman — Pesan Antar-Agen Tanpa Autentikasi, Spoofing & Instruksi Selundupan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 8; OWASP ASI07:2026 Insecure Inter-Agent Communication), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah sistem multi-agen: beberapa agen saling berkirim pesan, memanggil satu sama lain, atau berbagi memori/konteks (orkestrator + sub-agen, agen yang mendelegasikan ke agen lain, rantai agen).
- Ditemukan fitur di mana satu agen bisa memicu agen lain, atau pesan antar-agen bisa memengaruhi perilaku agen penerima.
- Dipakai saat menguji KEPERCAYAAN ANTAR-AGEN sebagai permukaan serangan — BUKAN protokol transport (itu `analisis-websocket-grpc`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan graf komunikasi agen + menguji spoofing/selundupan + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Protokol transport real-time (WebSocket/gRPC) → skill `analisis-websocket-grpc`.
- Penyalahgunaan tool/izin agen → skill `penyalahgunaan-tool-agen`.
- Racun memori/RAG antar-sesi → skill `racun-rag-memori`.
- Perambatan kegagalan antar-agen dalam satu sistem yang berjalan → skill `kegagalan-berantai-agen` (fokusnya efek domino kegagalan, bukan pesan antar-agen yang dipalsukan).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah); semua agen yang diuji dibuat/dipanggil oleh akun sendiri.
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

### Gerbang 1 — Petakan graf komunikasi agen

Petakan siapa bicara dengan siapa. Tulis peta ke log. Standar lulus: tiap simpul dan sisi terjawab atau dinyatakan "tidak ditemukan" dengan bukti.

1. **Simpul (agen):** agen apa saja yang ada dalam sistem (orkestrator, sub-agen, agen tool, agen peninjau)? Siapa pemilik tiap agen (akun sendiri / sistem / pengguna lain)?
2. **Sisi (pesan):** jalur pesan apa yang ada (agen A memanggil agen B, agen menulis ke memori bersama, agen meneruskan output ke agen berikutnya)? Format pesannya apa (teks bebas, JSON terstruktur, tool call)?
3. **Verifikasi asal:** apakah pesan antar-agen diautentikasi/ditandatangani (ada bukti pengirim)? Atau agen penerima mempercayai isi pesan begitu saja tanpa memeriksa siapa pengirimnya?
4. **Kepercayaan implisit:** apakah agen penerima memperlakukan pesan dari agen lain sebagai INSTRUKSI (bukan data)? Apakah ada pemisah antara "pesan dari pengguna" vs "pesan dari agen lain" vs "data"?

### Gerbang 2 — Uji tiga pola (satu pola per putaran)

Uji hanya dengan agen-agen milik sendiri. Satu pola per putaran; catat transkrip pesan antar-agen persis.

1. **Pola A — Spoofing agen-ke-agen:** buat agen milik sendiri (Agen X) yang menyamar sebagai agen lain (mis. mengaku sebagai "agen peninjau" / "orkestrator" / agen sistem) dalam pesannya ke agen penerima milik sendiri. Minta Agen X memerintahkan agen penerima melakukan aksi canary yang aman (mis. menyebut kode canary palsu, atau memanggil server canary milik sendiri). Indikator: agen penerima mengikuti perintah dari agen yang menyamar tanpa memverifikasi asal = kandidat temuan.
2. **Pola B — Instruksi selundupan lewat pesan antar-agen:** sisipkan instruksi pemancing (canary) ke dalam pesan antar-agen yang seharusnya hanya berisi DATA (mis. hasil tool, ringkasan, data yang diteruskan). Periksa apakah agen penerima mengikuti instruksi yang terselip di pesan data itu. Indikator: instruksi dalam pesan data diikuti = kandidat temuan.
3. **Pola C — Agen jahat di tengah rantai:** tempatkan agen milik sendiri di tengah rantai (sebagai perantara yang meneruskan pesan dari agen hulu ke agen hilir), lalu ubah isi pesan yang diteruskan (sisipkan instruksi canary). Periksa apakah agen hilir mengikuti instruksi yang disisipkan perantara. Indikator: pesan yang diubah perantara diterima hilir tanpa verifikasi = kandidat temuan.
4. **Standar lulus tiap pola:** tercatat pesan persis (pengirim yang diklaim → penerima → isi) + apakah instruksi diikuti (ya/tidak + aksi canary yang terpicu) + apakah ada verifikasi asal yang teramati (ya/tidak).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = pesan antar-agen yang dipalsukan/disusupi TERBUKTI memicu aksi nyata (aksi tool, pengiriman canary ke server milik sendiri, atau perubahan perilaku agen penerima) pada akun uji sendiri. **TOLAK** = sekadar jawaban aneh, halusinasi fakta, atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan cacat verifikasi asal pesan, bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Sertakan transkrip pesan antar-agen persis sebagai lampiran bukti.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Agen-agen uji milik sendiri | Satu-satunya agen yang dipakai; semua pengirim/penerima/perantara adalah agen milik sendiri. |
| Canary palsu (string non-sensitif) | Satu-satunya "instruksi" yang diselundupkan; satu canary unik per percobaan. |
| Server canary milik sendiri | Penampung callback untuk membuktikan aksi keluar tanpa melibatkan pihak lain. |
| Transkrip pesan antar-agen | Bukti inti: pengirim yang diklaim → penerima → isi persis. Simpan lengkap. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log graf komunikasi agen + pola uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + sistem multi-agen]
Graf komunikasi: [simpul agen] | [sisi pesan + format] | [verifikasi asal: ya/tidak] | [pesan agen = instruksi atau data?]
Pola diuji: [A/B/C + nama pola]
Pesan antar-agen (persis): [pengirim yang diklaim] → [penerima] : [isi]
Langkah reproduksi: [agen pengirim + pesan + aksi agen penerima]
Indikator teramati: [instruksi diikuti? ya/tidak + aksi canary yang terpicu]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Sistem Multi-Agen] - Pesan antar-agen tanpa verifikasi asal memungkinkan [Spoofing/Selundupan] memicu [Aksi Spesifik]`. Isi laporan: Graf Komunikasi (simpul + sisi + ada/tidaknya verifikasi asal); Langkah Reproduksi (transkrip pesan persis + aksi yang terpicu); Rekomendasi Perbaikan (tandatangani/autentikasi pesan antar-agen, verifikasi asal sebelum mengikuti instruksi dari agen lain, perlakukan pesan antar-agen sebagai data tak tepercaya kecuali dari pengirim terverifikasi).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP ASI07:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Bila sistem target tidak punya komunikasi antar-agen yang bisa diamati/diuji (agen tunggal), skill ini tidak berlaku — jangan dipaksakan.
- Bila yang diuji adalah perambatan kegagalan (bukan pesan yang dipalsukan), pakai `kegagalan-berantai-agen`.
- Untuk Google, pengujian payload injeksi diblokir — skill ini di Tim 4 hanya berupa analisis format.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan OWASP Top 10 for Agentic Applications.

## Websites

- OWASP Top 10 for Agentic Applications 2026, ASI07 Insecure Inter-Agent Communication — https://owasp.org/www-project-top-10-for-agentic-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila fokusnya protokol transport (WebSocket/gRPC), pakai `analisis-websocket-grpc`.
- Bila fokusnya perambatan kegagalan antar-agen, pakai `kegagalan-berantai-agen`.
- Bila fokusnya racun memori bersama antar-agen, pakai `racun-rag-memori`.
