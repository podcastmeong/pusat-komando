# Skill: Pengujian Misinformasi & Overreliance — Output Model yang Disajikan sebagai Fakta Tanpa Verifikasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 1 butir 4; OWASP LLM07:2026 Misinformation, naik dari #9 di 2025 ke #7), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target adalah aplikasi yang menyajikan output model sebagai fakta/teks otoritatif tanpa verifikasi: ringkasan dokumen, jawaban atas pertanyaan faktual, kutipan/sumber, rekomendasi yang masuk ke keputusan bisnis/pengguna.
- Ditemukan fitur AI yang menampilkan jawaban tanpa penandaan ketidakpastian, tanpa sumber yang bisa dicek, atau tanpa peringatan bahwa output bisa salah.
- Dipakai saat menguji misinformasi/halusinasi sebagai KELAS KERENTANAN yang bisa dilaporkan — BUKAN sekadar mencatat "model berhalusinasi".

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merancang kasus uji faktual + menjalankan pengujian + mendokumentasikan bukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Probe halusinasi/misinformasi sebagai KATEGORI SCANNER (bukan metodologi pelaporan) → skill `alat-garak` (probe bawaan mencakup halusinasi/misinformasi — hasil scanner adalah peta permukaan, bukan temuan jadi).
- Validasi temuan yang sudah ada → skill `gerbang-tujuh-pertanyaan-triase`.
- Penilaian keparahan → skill `penilaian-cvss`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah).
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.
12. **Gerbang khusus skill ini — halusinasi murni BUKAN temuan:** sesuai `buru-bug-bounty` ("JANGAN buang waktu pada yang TIDAK dibayar: ... halusinasi"), jawaban salah yang berdiri sendiri TANPA dampak keputusan/aksi = DITOLAK. Skill ini hanya maju bila misinformasi masuk ke keputusan/aksi nyata (lihat Gerbang 3.1).

## Langkah + gerbang

### Gerbang 1 — Petakan jalur fakta-ke-keputusan

Petakan bagaimana output model dipakai target. Tulis peta ke log. Standar lulus: tiap titik terjawab atau dinyatakan "tidak ditemukan" dengan bukti.

1. **Sumber klaim:** pertanyaan/klaim faktual apa yang bisa diajukan ke model (tanggal, angka, nama, aturan, kutipan)?
2. **Penyajian:** apakah jawaban disajikan sebagai fakta (tanpa penanda ketidakpastian, tanpa sumber, tanpa peringatan)? Apakah ada kutipan/sumber — dan apakah sumber itu bisa dicek (nyata vs palsu)?
3. **Jalur ke keputusan/aksi:** apakah jawaban itu masuk ke keputusan bisnis, rekomendasi tindakan, dokumen yang diteruskan, atau aksi otomatis? Tanpa jalur ini, misinformasi = keterbatasan model, bukan kerentanan (lihat aturan keras 12).

### Gerbang 2 — Uji kasus faktual (satu kasus per putaran)

Rancang kasus uji yang jawabannya bisa dicek benar/salah secara objektif. Uji satu kasus per putaran; catat jawaban persis + sumber yang diklaim.

1. **Kasus uji A — Fakta yang bisa dicek:** ajukan pertanyaan dengan jawaban benar yang sudah diketahui dan terverifikasi dari sumber independen (mis. tanggal/angka/aturan yang pasti). Catat apakah jawaban salah, dan apakah disajikan dengan percaya diri tanpa penanda ketidakpastian.
2. **Kasus uji B — Kutipan/sumber palsu:** minta model mengutip sumber untuk jawabannya. Periksa tiap sumber yang diklaim: apakah sumber itu nyata (ada, isinya sesuai) atau palsu (tidak ada / isinya berbeda)? Kutipan palsu yang tampak meyakinkan = indikator kuat.
3. **Kasus uji C — Overreliance pengguna:** uji apakah antarmuka mendorong pengguna percaya begitu saja — mis. tidak ada peringatan, tidak ada tautan verifikasi, jawaban ditampilkan dengan format otoritatif (dokumen resmi, ringkasan eksekutif). Catat elemen UI yang menghilangkan keraguan pengguna.
4. **Standar lulus tiap kasus:** tercatat pertanyaan persis + jawaban persis + verifikasi independen (jawaban benar menurut sumber apa) + apakah jawaban masuk ke keputusan/aksi (ya/tidak + jalurnya).

### Gerbang 3 — Gerbang validasi laporan (Triage & Impact Gate)

1. **Dampak keamanan nyata — standar lulus:** Valid = misinformasi TERBUKTI masuk ke keputusan/aksi nyata yang merugikan (mis. rekomendasi salah yang dieksekusi, dokumen dengan kutipan palsu yang diteruskan sebagai resmi, keputusan bisnis yang diambil dari jawaban salah) pada akun uji sendiri. **TOLAK** = jawaban salah yang berdiri sendiri tanpa jalur ke keputusan/aksi (halusinasi murni — lihat aturan keras 12); TOLAK juga sekadar jawaban aneh atau ekstraksi system prompt umum tanpa rahasia/kredensial maupun celah otorisasi.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pengujian minimal **3 kali** (perilaku LLM probabilistik) — pastikan misinformasi sistematis (jawaban salah yang sama/serupa berulang), bukan variasi acak bahasa. Gagal direproduksi 3× = TOLAK.
3. **Higienitas bukti — standar lulus:** sensor token sesi, kunci API, dan data pribadi pada screenshot maupun log HTTP sebelum dilampirkan (`[REDACTED]`). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan. Sertakan verifikasi independen (sumber benar yang membuktikan jawaban model salah).

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Kasus uji faktual (jawaban benar terverifikasi) | Satu-satunya dasar penilaian benar/salah; jawaban benar harus dari sumber independen, bukan dari model yang sama. |
| Akun uji sendiri | Pengujian hanya di akun/sesi milik sendiri. |
| Log HTTP mentah + screenshot jawaban | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta jalur fakta-ke-keputusan + kasus uji + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI yang menyajikan fakta]
Jalur fakta-ke-keputusan: [sumber klaim] | [penyajian: ada/tidak penanda ketidakpastian + sumber] | [jalur ke keputusan/aksi]
Kasus uji: [A/B/C + pertanyaan persis]
Jawaban model (persis): [kutipan jawaban + sumber yang diklaim]
Verifikasi independen: [jawaban benar + sumber independen]
Jalur dampak: [keputusan/aksi apa yang memakai jawaban ini]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Fitur AI] - Misinformasi [jenis: fakta salah/kutipan palsu] masuk ke [Keputusan/Aksi Spesifik] tanpa verifikasi`. Isi laporan: Peta Jalur (klaim → penyajian → keputusan/aksi); Langkah Reproduksi (kasus uji + jawaban persis + verifikasi independen); Rekomendasi Perbaikan (tandai ketidakpastian, tampilkan sumber yang bisa dicek, beri peringatan sebelum jawaban dipakai untuk keputusan, verifikasi fakta kritis ke sumber independen).

## Batasan yang diketahui

- Metodologi ini dari riset (OWASP LLM07:2026), bukan pengalaman teruji — butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — Gerbang 3.2 (minimal 3×) wajib.
- Mayoritas program bounty TIDAK membayar halusinasi murni — skill ini hanya berguna bila ada jalur nyata ke keputusan/aksi; bila tidak ada jalur itu, JANGAN buang waktu (aturan keras 12).
- Untuk Google AI VRP, halusinasi out of scope — skill ini di Tim 4 hanya berupa analisis format.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi klasik — gunakan skill ini sebagai metodologi pengujian, bukan daftar target.

## Available connectors

- Browser (`browser.search`, `browser.open`) — verifikasi independen jawaban benar dari sumber publik tepercaya + riset dokumentasi program.

## Websites

- OWASP Top 10 for LLM Applications 2026, LLM07 Misinformation — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh peta permukaan halusinasi/misinformasi secara cepat sebelum pengujian manual, jalankan `alat-garak` dulu (probe bawaan) — hasilnya peta, bukan temuan jadi.
- Bila misinformasi berasal dari dokumen beracun di RAG (bukan dari model sendiri), pakai `racun-rag-memori`.
- Bila temuan sudah ada dan butuh validasi, pakai `gerbang-tujuh-pertanyaan-triase`.
