# Skill: Alat Rebuff — Detektor Injeksi Prompt Self-Hardening

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `protectai/rebuff`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope memakai detektor injeksi prompt Rebuff (atau detektor sejenis) di depan aplikasi LLM-nya.
- Perlu menguji apakah detektor injeksi target bisa dilewati serangan yang lolos dari deteksi.
- Perlu memakai Rebuff di lab sendiri untuk mempelajari pola deteksi injeksi sebelum menguji target.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang Rebuff di lab + menjalankan uji deteksi terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Toolkit deteksi injeksi umum multi-vektor → skill `alat-llm-guard`.
- Perburuan injeksi prompt LLM secara umum (tanpa tool spesifik) → skill `perburuan-llm-ai`.
- Deteksi injeksi prompt rule-based/scanner → skill `alat-vigil` (kandidat 14, pendekatan berbeda: scanner berbasis pola, bukan self-hardening).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat menguji detektor target.
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

### Gerbang 1 — Pasang Rebuff di lab sendiri

Rebuff adalah detektor injeksi prompt yang "self-hardening": ia belajar dari serangan baru yang lolos dan memperbarui pertahanannya sendiri. Komponennya: detektor heuristik, detektor berbasis model, dan vector database berisi serangan yang diketahui.

1. Clone repo: `git clone https://github.com/protectai/rebuff.git` lalu ikuti `README.md` (server + PostgreSQL + pgvector, atau jalankan via Docker Compose yang disediakan repo).
2. Perintah dasar (Python SDK): `from rebuff import Rebuff`, `rb = Rebuff()`, lalu `rb.detect_injection("...")` dan `rb.detect_leakage("...")`.
3. Catat versi Rebuff yang terpasang dan konfigurasi threshold di log — hasil uji hanya bermakna bila versi tercatat.

### Gerbang 2 — Pelajari cara membaca hasil deteksi

1. `detect_injection` mengembalikan skor injeksi 0–1 beserta alasan detektor mana yang memicu (heuristik / model / kemiripan vektor dengan serangan lama).
2. Skor di atas threshold (default repo) = diblokir; di bawah = lolos.
3. Uji dengan tiga kelompok input di lab sendiri: (a) injeksi jelas ("Abaikan instruksi sebelumnya..."), (b) teks jinak yang mirip instruksi (dokumentasi, contoh kode, URL), (c) injeksi terselubung (parafrasa, sisipan di tengah teks panjang).
4. Catat mana yang benar terdeteksi, mana yang lolos, dan mana yang false positive — ini baseline perilaku detektor.

### Gerbang 3 — Uji detektor target in-scope

1. Kirim input uji HANYA ke endpoint target yang in-scope, memakai akun uji sendiri, dengan canary palsu bila perlu membuktikan eksekusi.
2. Variasikan satu dimensi per putaran: parafrasa, posisi sisipan, pemecah kata, konteks panjang. Satu variasi = satu catatan hasil.
3. Temuan valid HANYA bila: input yang Rebuff (di lab) tandai sebagai injeksi berhasil melewati detektor target DAN menghasilkan aksi/efek nyata (bukan sekadar jawaban aneh) — lihat Gerbang 4.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Detektor target memblokir teks jinak (dokumen, kode, instruksi sah) | False positive detektor — BUKAN temuan bounty (kecuali program membayar DoS fungsional; verifikasi scope dulu) |
| Input injeksi lolos detektor tapi model menolak menjalankan instruksinya | Bukan temuan — detektor bukan satu-satunya lapisan |
| Input injeksi lolos detektor DAN model menjalankan instruksi (aksi/efek nyata, dapat diulang 3×) | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo Rebuff (`protectai/rebuff`) | Clone + Docker Compose; Python SDK `Rebuff().detect_injection()` / `.detect_leakage()` |
| Akun uji sendiri | Wajib untuk Gerbang 3; keduanya milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi Rebuff + hasil tiap variasi input + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI + apakah Rebuff dipakai target (bila diketahui)]
Versi Rebuff lab: [commit/tag]
Input uji: [teks input / variasi]
Skor lab Rebuff: [skor + detektor pemicu]
Respons target: [diblokir / lolos + efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Detektor injeksi target] - [Jenis bypass] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool Rebuff **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Rebuff adalah detektor, bukan bukti kerentanan: lolos dari Rebuff di lab tidak sama dengan lolos dari detektor target — target mungkin memakai detektor lain atau lapisan tambahan.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.
- Self-hardening berarti perilaku detektor berubah seiring serangan baru yang dipelajari — baseline lab bisa basi; catat tanggal tiap baseline.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi Rebuff dan scope program.

## Websites

- Rebuff — https://github.com/protectai/rebuff
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target tidak memakai detektor khusus (atau tidak diketahui), pakai `perburuan-llm-ai` untuk perburuan injeksi umum.
- Bila detektor target berbasis pola/aturan, pakai `alat-vigil`.
- Bila perlu fuzzing generatif massal, pakai `alat-llmfuzzer`.
