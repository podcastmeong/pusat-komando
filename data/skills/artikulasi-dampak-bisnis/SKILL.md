# Skill: Artikulasi Dampak Bisnis — Terjemahkan Celah Teknis jadi Risiko Bisnis Nyata

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md` butir 49. Isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu pernyataan dampak yang dicatat di log dan lolos triase. Label ini berlaku untuk semua bagian sampai ada kasus nyata yang dicatat.

## Pemicu

Dipakai setiap kali ada temuan berstatus **VERIFIED** dari `skeptic-false-positive-eliminator` yang dampak teknisnya sudah terbukti, tapi belum bisa dijelaskan dalam bahasa bisnis — sebelum skor CVSS dihitung (`penilaian-cvss`, yang butuh dampak terbukti untuk metrik C/I/A) dan sebelum draf laporan (`laporan-poc-otomatis`). Satu temuan = satu pernyataan dampak bisnis + satu kalimat dampak utama. Tanpa pernyataan ini, laporan hanya berisi jargon teknis yang triager sulit menilai.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Menulis pernyataan dampak bisnis dari bukti; memberi label TERBUKTI vs ESTIMASI pada tiap angka |
| Dukungan | **A55 Analis Rantai & Pelapor** | Menyediakan konteks rantai serangan (langkah demi langkah) bila dampak muncul dari gabungan celah |
| Audit | **A60 Security Auditor** | Memeriksa tiap angka dan klaim terhadap bukti; menolak angka yang tidak bisa ditelusur |
| Pemimpin | **Muse** | Memutuskan pernyataan dampak maju ke laporan atau dikembalikan |

## Sudah tercakup (jangan diduplikat)

- **Gerbang 3 `skeptic-false-positive-eliminator`** ("Verifikasi dampak bisnis") hanya MENANYAKAN dampak dalam 2–3 kalimat sebagai filter lolos/tolak — skill ini **bukan** gerbang itu. Skill ini adalah **cara menulis dampak yang terukur** setelah temuan lolos gerbang tersebut: siapa, apa, berapa banyak, seberapa sensitif, dan apa akibat bisnisnya.
- **Pembuktian dampak per jenis kerentanan** (IDOR butuh dua akun, SSRF butuh hit canary, dst.) ada di `fondasi-kerentanan-web-api` — skill ini memakai bukti itu, bukan mengulang cara membuktikannya.
- **Skor CVSS** ada di `penilaian-cvss` — skill ini menyediakan bahan dampaknya (apa yang bocor/diubah, seberapa luas), bukan angkanya.
- **Struktur laporan** ada di `laporan-poc-otomatis` — pernyataan dampak dari skill ini DISISIPKAN ke bagian Dampak laporan itu.
- Alur sesudah skill ini: pernyataan dampak → `penilaian-cvss` (metrik C/I/A) → `triase-duplikat` (cek duplikat + tier hadiah) → draf laporan (`laporan-poc-otomatis`) → tinjau manusia → persetujuan Cipta → kirim.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan dinilai, jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.**
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya; triase yang menentukan tier hadiah. Angka yang dibesarkan = kredibilitas hilang + risiko ditolak triase.
8. **Pisahkan TERBUKTI dan ESTIMASI — selalu.** Angka yang diukur langsung dari pengujian sendiri (akun canary) = TERBUKTI. Angka populasi, kerugian uang, atau jumlah korban di dunia nyata = ESTIMASI, dan WAJIB berlabel ESTIMASI + sumber perkiraannya. Jangan pernah menulis angka estimasi seolah-olah terukur.
9. **Jangan pernah menulis angka korban/data dari data orang lain.** Jumlah record yang bocor hanya boleh dihitung dari akun/data MILIK SENDIRI yang diuji. Bila endpoint mengembalikan daftar (mis. total count di respons API), angka itu TERBUKTI hanya sebagai "angka yang dikembalikan server", bukan sebagai "data yang sudah dicuri".
10. **Sensor PII pada semua bukti** (screenshot/log) sebelum pernyataan dampak disusun — nama, email, nomor identitas, dan data pribadi lain diganti `[REDACTED]`. Pernyataan dampak menyebut JENIS data (mis. "data KTP"), bukan ISI data orang lain.
11. **Pembuat temuan tidak boleh meloloskan pernyataan dampaknya sendiri** — A60 yang mengaudit.

## Langkah + gerbang

### Gerbang 1 — Jawab 5 pertanyaan dampak dari bukti

Tulis jawaban singkat untuk tiap pertanyaan, masing-masing dengan reference ID bukti:

1. **SIAPA penyerangnya?** Profil penyerang paling lemah yang bisa melakukannya: tanpa login / akun gratis / akun pengguna biasa / butuh korban klik. (Ini juga bahan metrik PR/UI di `penilaian-cvss`.)
2. **APA yang bisa dicuri / diubah / diakses tanpa sah?** Sebutkan JENIS data atau aksi persisnya: mis. "data profil + nomor KTP", "ubah harga barang di keranjang", "baca pesan pengguna lain", "hapus akun orang lain".
3. **BERAPA BANYAK?** Hitung dari bukti sendiri: berapa record/akun yang TERBUKTI bisa diakses dalam pengujian (akun canary sendiri). Bila respons server menyebut total populasi, tulis sebagai "server mengembalikan total X record (TERBUKTI sebagai angka respons; jumlah yang benar-benar bisa diambil tidak diuji)".
4. **SEBERAPA SENSITIF?** Klasifikasikan jenis datanya (lihat tabel Gerbang 2).
5. **APA KERUGIAN bagi pemilik program?** Pilih dari Gerbang 3 — keuangan, operasional, reputasi, hukum/regulasi — dan tulis SATU akibat paling nyata per kategori yang relevan, bukan semuanya.

**Standar lulus:** kelima pertanyaan terjawab, tiap jawaban punya reference ID bukti. Pertanyaan tanpa bukti = gerbang gagal, kembali ke pengujian.

### Gerbang 2 — Klasifikasikan sensitivitas data (bukan dari perasaan)

| Kelas | Contoh | Bobot dalam pernyataan dampak |
|---|---|---|
| **Kritis** | Kata sandi, token sesi, KTP/NIK, data keuangan (rekening, kartu), data kesehatan, kunci API/secret | Sebut di kalimat pertama pernyataan dampak. Ini yang membuat dampak serius |
| **Tinggi** | Email + nama lengkap, alamat rumah, nomor telepon, riwayat transaksi, pesan pribadi | Sebut eksplisit; jelaskan apa yang bisa dilakukan penyerang dengannya (mis. phishing, penipuan, pemerasan) |
| **Sedang** | Nama pengguna, foto profil, preferensi, metadata aktivitas | Sebut secukupnya; jangan dibesar-besarkan |
| **Rendah / publik** | Data yang memang ditampilkan publik (nama tampilan, postingan publik) | Bila hanya ini yang bocor, dampaknya RENDAH — tulis apa adanya; jangan klaim kebocoran serius |

- **Standar lulus:** tiap jenis data yang disebut di pernyataan dampak punya kelasnya. Data tanpa kelas = belum selesai.

### Gerbang 3 — Petakan akibat bisnis (pilih yang relevan, buktikan satu per satu)

| Akibat | Contoh pernyataan (sesuaikan dengan bukti) |
|---|---|
| **Keuangan langsung** | "Penyerang bisa mengubah harga / mengambil saldo / menebus voucher berulang — tiap transaksi bernilai RpX (TERBUKTI dari pengujian sendiri sebesar RpX)". Jangan kalikan ke populasi tanpa label ESTIMASI |
| **Kebocoran data massal** | "Endpoint mengembalikan data pengguna lain tanpa pemeriksaan kepemilikan; server mengembalikan total X record (angka respons). Bila dieksploitasi massal, seluruh populasi pengguna terdampak (ESTIMASI, berdasarkan angka respons server)" |
| **Pengambilalihan akun (ATO)** | "Penyerang bisa masuk ke akun korban tanpa kata sandi → kendali penuh atas akun, termasuk ubah kata sandi dan kunci pemilik asli keluar" |
| **Reputasi / kepercayaan** | "Bila dipublikasikan, pengguna kehilangan kepercayaan karena data [jenis data] mereka bisa dibaca orang lain" — tulis sebagai risiko, bukan sebagai fakta yang sudah terjadi |
| **Hukum / regulasi** | "Kebocoran data pribadi (KTP/NIK) berpotensi melanggar kewajiban perlindungan data pribadi (mis. UU PDP di Indonesia) — tulis sebagai potensi, bukan vonis hukum" |
| **Operasional** | "Penyerang bisa menghapus/mengubah data sehingga layanan tidak bisa dipakai / butuh pemulihan manual" |

- **Standar lulus:** minimal SATU akibat bisnis tertulis dengan bukti pendukungnya; akibat yang ditulis tanpa bukti = hapus. Akibat yang hanya "mungkin" ditulis dengan kata "berpotensi" + label ESTIMASI.

### Gerbang 4 — Tulis pernyataan dampak: 1 kalimat utama + 1 paragraf

**Kalimat utama (satu kalimat, format baku):**

> "[Jenis celah] ini memungkinkan [profil penyerang] untuk [aksi tanpa sah] terhadap [apa + berapa banyak + kelas sensitivitas], yang mengakibatkan [akibat bisnis paling nyata]."

Contoh format (CONTOH FORMAT SAJA, bukan temuan nyata):

> "IDOR ini memungkinkan penyerang dengan akun gratis untuk mengunduh 500.000 data KTP pelanggan (angka populasi dari respons server — ESTIMASI), yang mengakibatkan kebocoran data pribadi massal dan risiko penipuan identitas."

**Paragraf pendukung (3–5 kalimat):** uraikan 5 jawaban Gerbang 1 + kelas data Gerbang 2 + akibat Gerbang 3, dengan label TERBUKTI/ESTIMASI pada tiap angka. Akhiri dengan batas yang DIUJI: "Pengujian hanya memakai akun sendiri; tidak ada data pengguna lain yang diakses/diubah."

**Standar lulus:** kalimat utama bisa dibaca triager dalam 10 detik dan menjawab siapa–apa–berapa–akibat; paragraf pendukung bisa ditelusur ke bukti; A60 menyetujui tiap angka.

## Alat

| Alat | Cara pakai |
|---|---|
| Bukti sesi bersih | Pasangan Request/Response + reference ID dari `skeptic-false-positive-eliminator` — dasar tiap jawaban Gerbang 1 |
| `artikulasi-dampak-bisnis` (skill ini) | Template kalimat utama + tabel kelas data + tabel akibat bisnis di atas |
| Sensor PII | Ganti nama, email, NIK, nomor telepon, token, dan data pribadi lain dengan `[REDACTED]` sebelum bukti dipakai |
| `~/workspace/catatan/log-bug-bounty.md` | Catat pernyataan dampak + label TERBUKTI/ESTIMASI + verdict A60 |

## Human-in-the-loop

- A60 mengaudit tiap angka dan klaim sebelum pernyataan dampak dipakai di draf laporan. Angka tanpa bukti = hapus, bukan "diperbaiki" dengan perkiraan.
- Pernyataan dampak adalah **usulan untuk triager**, bukan keputusan hadiah. Tier hadiah tetap diputuskan triager/program (`triase-duplikat`).

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per temuan) dengan format:

```
- [tanggal] Temuan: <nama singkat> | Program: <nama> | Reference ID bukti: <FP-...>
  - Kalimat dampak: <satu kalimat format baku>
  - Siapa: <profil penyerang> — <bukti>
  - Apa: <jenis data/aksi + kelas sensitivitas> — <bukti>
  - Berapa: <angka TERBUKTI dari pengujian sendiri> | <angka ESTIMASI + sumber perkiraan>
  - Akibat bisnis: <keuangan / kebocoran / ATO / reputasi / hukum / operasional — pilih yang relevan + bukti>
  - Batas pengujian: hanya akun sendiri; tidak ada data pengguna lain yang diakses/diubah
  - Audit A60: SETUJU / TOLAK — <alasan>
```

## Batasan yang diketahui

- Pernyataan dampak BUKAN bukti hukum atau audit keuangan — ini bahasa triase agar triager menilai cepat. Jangan menulis klaim hukum yang pasti ("melanggar pasal X") — tulis "berpotensi melanggar kewajiban perlindungan data pribadi".
- Untuk bounty agen AI (Muse, OpenAI, Google AI VRP, 0din), dampaknya adalah HASIL/outcome (aksi nyata yang dilakukan agen / data yang keluar) — rumuskan dengan pertanyaan yang sama (siapa–apa–berapa–akibat), tapi jangan paksakan kelas data web klasik bila outcome-nya berupa aksi (mis. agen mengirim email tanpa persetujuan).
- Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI kecuali dinyatakan berlaku di skill itu.
