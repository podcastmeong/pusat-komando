# Skill: Alat LLMFuzzer — Fuzzing Generatif Otomatis terhadap LLM

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah cara pakai tool dari riset (referensi: `corca-ai/awesome-llm-security`, repo `mnns/LLMFuzzer`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu menguji model/aplikasi LLM target in-scope secara massal dan sistematis, bukan satu prompt manual per satu.
- Perlu membangkitkan input adversarial baru (bukan memakai daftar payload tetap) untuk menemukan jailbreak atau kebocoran yang belum diketahui.
- Perlu mengelompokkan respons gagal dari ratusan putaran fuzzing menjadi pola temuan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54** | Memasang LLMFuzzer di lab + menjalankan putaran fuzzing terhadap target in-scope |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Eval/red-teaming prompt dengan kasus uji tetap → skill `alat-promptfoo`.
- Pemindai LLM dengan probe tetap → skill `alat-garak`.
- Fuzzing prompt pada aplikasi GenAI yang sudah jadi (level aplikasi/produk) → skill `alat-prompt-fuzzer` (kandidat 16 — sudut aplikasi, sedangkan skill ini menyasar model dan membangkitkan input baru secara generatif).
- Mutasi payload dari respons WAF → skill `mutasi-payload-dinamis`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur AI berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri (test accounts terpisah) saat fuzzing target.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan. **Khusus fuzzing: batasi jumlah putaran dan jeda antar request (lihat Gerbang 3); fuzzing massal tanpa batas = pelanggaran aturan ini.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji. **Bila program melarang pengujian otomatis pada endpoint inferensi, fuzzing TIDAK BOLEH dijalankan ke target itu — pakai LLMFuzzer hanya di lab sendiri.**

## Langkah + gerbang

### Gerbang 1 — Pasang LLMFuzzer di lab sendiri

LLMFuzzer adalah fuzzer generatif: ia membangkitkan input adversarial baru sendiri (dari seed prompt + mutasi) lalu menjalankannya terhadap model, berbeda dari pemindai yang memakai daftar probe tetap.

1. Clone repo: `git clone https://github.com/mnns/LLMFuzzer.git` lalu ikuti `README.md` (dependensi Python, konfigurasi target/model).
2. Siapkan seed prompt awal: 5–10 prompt jailbreak/injeksi yang sudah dikenal (dari riset publik) sebagai benih mutasi.
3. Jalankan satu putaran kecil di lab sendiri (model lokal atau endpoint uji sendiri) untuk memastikan fuzzer berjalan; catat versi dan konfigurasi di log.

### Gerbang 2 — Jalankan putaran fuzzing dan kelompokkan hasil

1. Tentukan anggaran putaran SEBELUM mulai (mis. maks 50–100 input per sesi, jeda antar request, berhenti bila rate limit menyala) — tulis anggaran di log.
2. Jalankan fuzzer; setiap input yang dibangkitkan + respons model dicatat.
3. Kelompokkan respons yang menunjukkan kegagalan keamanan: jailbreak berhasil, kebocoran (canary/system prompt), perilaku tak diinginkan. Kelompokkan per pola, bukan per input tunggal.
4. Buang kelompok yang hanya berisi jawaban aneh/halusinasi tanpa efek keamanan (lihat Gerbang 4).

### Gerbang 3 — Uji ulang pola yang lolos ke target in-scope

1. Ambil SATU pola per kelompok yang lolos di lab; uji pola itu ke endpoint target in-scope dengan akun uji sendiri, maksimal 3× per pola.
2. Patuhi anggaran putaran dan jeda (skill `pacing-request-aman`); hentikan fuzzing bila target memberi rate limit atau error — jangan memaksa.
3. Temuan valid HANYA bila pola yang sama menghasilkan efek nyata di target dan dapat diulang 3×.

### Gerbang 4 — Bedakan temuan benar dari false positive

| Gejala | Penilaian |
|---|---|
| Fuzzer menandai respons sebagai "gagal" padahal hanya jawaban aneh/halusinasi tanpa efek | False positive — BUKAN temuan |
| Pola lolos di lab (model lokal) tapi tidak di target | Bukan temuan target — catat sebagai perbedaan model, bukan kerentanan |
| Pola yang sama menghasilkan efek nyata di target (aksi/kebocoran), dapat diulang 3× | Kandidat temuan — lanjut ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → persetujuan Cipta |
| Hasil berubah-ubah antar putaran tanpa perubahan input | Perilaku probabilistik — ulangi 3×; gagal direproduksi 3× = TOLAK |

## Alat

| Alat | Cara pakai |
|---|---|
| Repo LLMFuzzer (`mnns/LLMFuzzer`) | Clone + ikuti README; seed prompt + konfigurasi putaran |
| Akun uji sendiri | Wajib untuk Gerbang 3; milik sendiri |
| Canary palsu (string non-sensitif) | Satu-satunya data yang disisipkan ke input uji |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan |
| `~/workspace/catatan/log-bug-bounty.md` | Log versi LLMFuzzer + anggaran putaran + kelompok hasil + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur AI/model]
Versi LLMFuzzer lab: [commit/tag] | Anggaran: [jumlah input + jeda]
Seed: [jumlah + sumber seed]
Kelompok hasil: [pola] | [jumlah input lolos di lab] | [efek di target]
Pola diuji ke target: [pola + input contoh]
Respons target: [efek yang teramati]
Reproduksi: [x/3 putaran berhasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Model/fitur target] - [Jenis kegagalan] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Repo/tool LLMFuzzer **belum terverifikasi** berfungsi di lingkungan ini — perintah di atas berasal dari dokumentasi repo, bukan dari instalasi yang sudah dicoba. Bila instalasi gagal, catat kegagalannya di log dan jangan klaim tool berfungsi.
- Fuzzing generatif menghasilkan banyak noise: sebagian besar input yang "lolos" di lab adalah false positive atau artefak model lokal — triase kelompok (Gerbang 2) wajib sebelum menyentuh target.
- Fuzzing massal berisiko melanggar aturan rate limit / pengujian otomatis program — anggaran putaran dan jeda wajib ditulis SEBELUM mulai; bila program melarang otomasi, jangan fuzzing ke target.
- Perilaku LLM probabilistik: satu kali percobaan tidak cukup — ulangi minimal 3×.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi LLMFuzzer dan scope program.

## Websites

- LLMFuzzer — https://github.com/mnns/LLMFuzzer
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila target adalah aplikasi GenAI yang sudah jadi (bukan model mentah), pakai `alat-prompt-fuzzer`.
- Bila cukup memakai kasus uji tetap (bukan membangkitkan input baru), pakai `alat-promptfoo` atau `alat-garak`.
- Bila perlu menjaga ritme request agar tidak terblokir, pakai `pacing-request-aman`.
