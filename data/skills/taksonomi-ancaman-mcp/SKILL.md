# Skill: Taksonomi Ancaman MCP — Peta Vektor Serangan Ekosistem MCP dari Literatur Sistematis

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah taksonomi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 28; sumber: `Puliczek/awesome-mcp-security` — Papers), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebelum memilih target dan teknik pengujian MCP: petakan dulu seluruh permukaan ancaman agar tidak hanya menguji satu vektor yang sudah dikenal.
- Ditemukan ekosistem MCP pada target in-scope (server, klien, transport, otorisasi) dan belum jelas dari mana mulai menguji.
- Saat menyusun rencana pengujian MCP untuk satu program: taksonomi ini menjadi daftar periksa cakupan.
- Dipakai SEBELUM pengujian MCP apa pun: peta dulu, hipotesis kemudian, pengujian terakhir.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Memetakan taksonomi ke target, memilih cabang yang diuji |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Membaca aturan program dan memetakan scope → skill `parsing-scope-program`.
- Inventaris aset dan endpoint target web/API secara umum → skill `pemetaan-permukaan-serangan`.
- Studi kasus eksploitasi MCP nyata (kasus per kasus) → skill `studi-kasus-eksploitasi-mcp-nyata`.
- Daftar periksa audit MCP berbasis spesifikasi resmi → skill `daftar-periksa-audit-mcp`.
- Skill ini adalah TAKSONOMI (peta klasifikasi vektor dari literatur), bukan checklist audit dan bukan korpus kasus.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji cabang taksonomi.
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

### Gerbang 1 — Bangun peta taksonomi untuk target

Petakan target ke lima cabang taksonomi di bawah (berbasis paper "Systematic Analysis of MCP Security", "Beyond the Protocol: Attack Vectors in the MCP Ecosystem", "MCP: Landscape, Security Threats, and Future Research", "MCP Safety Audit", "Enterprise-Grade Security for MCP" — cek ulang isi paper sebelum mengutip). Tulis peta ke log. Standar lulus: tiap cabang dinyatakan "ada di target" (dengan nama komponennya) atau "tidak ditemukan" dengan bukti.

1. **Server:** server MCP jahat/typosquat, deskripsi tool beracun, rug pull (tool berubah perilaku setelah dipercaya), resource poisoning, server tanpa validasi input.
2. **Klien:** klien yang mengeksekusi instruksi dari tool output tanpa verifikasi, klien tanpa konfirmasi operasi sensitif, klien tanpa anotasi tool tidak tepercaya.
3. **Transport:** sesi MCP tanpa autentikasi, token yang bocor lewat transport, server jarak jauh (remote MCP/SSE) tanpa kontrol akses.
4. **Otorisasi & identitas:** tool yang mewarisi kredensial pengguna tanpa batas, delegasi yang melebar, tidak ada pemisahan "siapa memanggil" vs "atas nama siapa".
5. **Rantai pasok & konfigurasi:** dependensi server MCP tanpa tanda tangan/hash, konfigurasi default yang permisif, tidak ada rate limit, output tanpa sanitasi.

### Gerbang 2 — Pilih cabang dan rumuskan hipotesis

Pilih SATU cabang per putaran pengujian. Rumuskan hipotesis dalam bentuk: "Bila [komponen target] tidak [kontrol yang seharusnya], maka [aksi/dampak] bisa terjadi lewat [jalur]". Standar lulus: hipotesis menyebut komponen target yang konkret dan kontrol yang diduga absen — bukan sekadar nama cabang taksonomi.

### Gerbang 3 — Uji hipotesis, bukti read-only

Uji hipotesis hanya dengan akun dan data uji sendiri, hanya di lingkungan in-scope. Pembuktian aman: baca yang seharusnya tidak terbaca (canary sendiri), callback canary milik sendiri, atau `document.domain` — JANGAN menjalankan aksi destruktif, JANGAN menyentuh data orang lain, JANGAN melibatkan korban. Ulangi 3× (perilaku agen probabilistik). Standar lulus: hipotesis terbukti ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Paper taksonomi MCP (lihat Gerbang 1) | Sumber klasifikasi; cek ulang isi paper sebelum mengutip. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai saat menguji cabang. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log peta taksonomi → hipotesis → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + ekosistem MCP]
Peta taksonomi: [server] | [klien] | [transport] | [otorisasi] | [rantai pasok]
Cabang diuji: [nama cabang + komponen target konkret]
Hipotesis: [bila ... tidak ..., maka ... lewat ...]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Komponen MCP] - [Cabang taksonomi] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Taksonomi (cabang + kenapa komponen target masuk cabang itu); Langkah Reproduksi (akun uji sendiri + log HTTP); Rekomendasi Perbaikan (kontrol per cabang: validasi input server, konfirmasi klien, autentikasi transport, scope kredensial, tanda tangan dependensi).

## Batasan yang diketahui

- Taksonomi ini dari riset literatur, bukan pengalaman teruji — tiap cabang butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Literatur MCP bergerak cepat: paper baru bisa menambah cabang — cek ulang `awesome-mcp-security` sebelum memakai peta ini untuk program baru.
- Taksonomi adalah peta, bukan bukti: menyebut nama cabang di laporan tanpa bukti reproduksi = DITOLAK di triase.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan klasifikasi taksonomi.

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh kasus nyata per pola (bukan klasifikasi), pakai `studi-kasus-eksploitasi-mcp-nyata`.
- Bila butuh daftar periksa kewajiban server/klien dari spesifikasi resmi, pakai `daftar-periksa-audit-mcp`.
- Bila target bukan MCP (aplikasi web klasik), pakai `pemetaan-permukaan-serangan` + `fondasi-kerentanan-web-api`.
