# Skill: Daftar Periksa Audit MCP — Checklist Server & Klien dari Spesifikasi Resmi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah daftar periksa audit dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 37; sumber: spesifikasi resmi MCP 2025-03-26 + MCP Security Checklist SlowMist di `Puliczek/awesome-mcp-security`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebelum atau selama audit keamanan MCP pada target in-scope: periksa tiap kewajiban server dan klien satu per satu dari spesifikasi resmi, bukan dari ingatan.
- Ditemukan server atau klien MCP pada target dan perlu dinilai kepatuhannya terhadap spesifikasi resmi MCP.
- Saat mengubah pelanggaran checklist menjadi temuan bounty yang terdokumentasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan checklist per kewajiban, mencatat patuh/tidak patuh |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Validasi temuan yang sudah ada (bukan checklist audit) → skill `gerbang-tujuh-pertanyaan-triase`.
- Membaca aturan program dan memetakan scope → skill `parsing-scope-program`.
- Taksonomi ancaman MCP dari literatur → skill `taksonomi-ancaman-mcp` (peta klasifikasi vektor, bukan checklist kewajiban).
- Studi kasus eksploitasi MCP nyata → skill `studi-kasus-eksploitasi-mcp-nyata`.
- Skill ini KHUSUS daftar periksa audit MCP berbasis spesifikasi resmi MCP 2025-03-26 dan checklist SlowMist — memeriksa tiap kewajiban server dan klien satu per satu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum audit dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji tiap kewajiban checklist.
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

### Gerbang 1 — Jalankan checklist server (spesifikasi resmi MCP 2025-03-26)

Periksa tiap kewajiban server di bawah satu per satu terhadap server MCP target in-scope. Tulis PATUH / TIDAK PATUH / TIDAK DAPAT DIUJI beserta bukti singkatnya. Standar lulus: semua butir terjawab, tidak ada yang dikosongkan.

**Kewajiban server (spesifikasi resmi MCP):**

| # | Kewajiban | Cara memeriksa |
|---|---|---|
| S1 | Server WAJIB validasi input | Kirim input tidak valid/aneh ke tool (canary sendiri); apakah ditolak atau diteruskan mentah |
| S2 | Server WAJIB kontrol akses | Coba panggil tool sensitif dengan akun uji berhak rendah; apakah ditolak |
| S3 | Server WAJIB rate limit | Kirim rangkaian request wajar-beruntun; apakah ada pembatasan (tanpa DoS — jangan membanjiri) |
| S4 | Server WAJIB sanitasi output | Periksa output tool: apakah instruksi terselip di output diteruskan mentah ke agen |

Tambahkan butir dari MCP Security Checklist (SlowMist) bila relevan dengan target — cek ulang checklist SlowMist dari sumbernya sebelum mengutip butirnya.

### Gerbang 2 — Jalankan checklist klien (spesifikasi resmi MCP 2025-03-26)

Periksa tiap kewajiban klien satu per satu terhadap klien MCP target in-scope. Standar lulus: semua butir terjawab dengan bukti.

**Kewajiban klien (spesifikasi resmi MCP):**

| # | Kewajiban | Cara memeriksa |
|---|---|---|
| K1 | Klien WAJIB konfirmasi operasi sensitif | Picu operasi sensitif lewat agen (akun uji sendiri); apakah ada konfirmasi manusia |
| K2 | Klien WAJIB anotasi tool tidak tepercaya | Periksa apakah tool dari server tak tepercaya ditandai/dibatasi |
| K3 | Klien WAJIB human-in-the-loop | Periksa apakah ada langkah yang butuh persetujuan manusia sebelum aksi berdampak |

### Gerbang 3 — Ubah pelanggaran menjadi temuan (bukti dampak, bukan sekadar centang)

Pelanggaran checklist HANYA maju bila dibuktikan dampaknya: data canary sendiri terbaca/keluar, tool sensitif terpicu tanpa otorisasi/konfirmasi, atau instruksi beracun dari output diikuti agen. Ulangi 3× bila melibatkan perilaku agen (probabilistik). Standar lulus: dampak teramati ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **Satu centang "TIDAK PATUH" tanpa bukti dampak BUKAN laporan** — yang maju adalah pelanggaran yang terbukti berdampak.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Spesifikasi resmi MCP 2025-03-26 (Security Considerations) | Sumber kewajiban S1–S4 dan K1–K3; cek ulang teks spesifikasinya sebelum mengutip. |
| MCP Security Checklist (SlowMist) | Butir tambahan; cek ulang dari sumbernya. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai saat menguji tiap butir. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log checklist server → checklist klien → pelanggaran → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + server/klien MCP]
Checklist server: [S1: PATUH/TIDAK PATUH/TIDAK DAPAT DIUJI + bukti] | [S2: ...] | [S3: ...] | [S4: ...]
Checklist klien: [K1: ...] | [K2: ...] | [K3: ...]
Pelanggaran diuji: [nomor butir + komponen target]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Dampak terbukti: [data/aksi yang lolos, read-only]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [diaudit / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Server/Klien MCP] - [Kewajiban spesifikasi yang dilanggar] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Checklist (butir yang dilanggar + teks kewajiban dari spesifikasi); Langkah Reproduksi (akun uji sendiri + log HTTP); Rekomendasi Perbaikan (penuhi kewajiban spesifikasinya: validasi input, kontrol akses, rate limit, sanitasi output, konfirmasi operasi sensitif, anotasi tool tak tepercaya, human-in-the-loop).

## Batasan yang diketahui

- Daftar periksa ini dari riset (spesifikasi 2025-03-26 + SlowMist), bukan pengalaman teruji — tiap butir butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Spesifikasi MCP bisa diperbarui: cek ulang versi spesifikasi terbaru sebelum memakai checklist ini untuk program baru.
- Beberapa kewajiban (mis. anotasi tool tak tepercaya di klien) tidak bisa diuji dari luar — catat sebagai "TIDAK DAPAT DIUJI", jangan diklaim patuh atau tidak patuh.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan jumlah centang TIDAK PATUH.

## Websites

- Spesifikasi MCP — https://modelcontextprotocol.io/specification/2025-03-26
- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh peta klasifikasi vektor (bukan checklist kewajiban), pakai `taksonomi-ancaman-mcp`.
- Bila butuh kasus nyata per pola, pakai `studi-kasus-eksploitasi-mcp-nyata`.
- Bila pelanggaran checklist adalah deskripsi tool beracun, dalami dengan `peracunan-deskripsi-tool-mcp`.
