# Skill: Analisis Batas Kepercayaan — Memetakan Titik yang Dipercaya Server Tanpa Verifikasi, Lalu Mengujinya

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: Perspektif 2 (Trust Boundary & Authorization Analysis) di `~/workspace/catatan/referensi-dua-perspektif-skill-bug-bounty-ai-2026-11-23.md` + strategi 2 "Audit batas kepercayaan (pola $300rb)" dan studi kasus $300rb proxy-header di `~/workspace/tmp/pusat-komando-push/data/skills/buru-bug-bounty/SKILL.md`. Metode di sini adalah rekonstruksi dari riset publik — langkah penemuan aslinya tidak dipublikasikan.

## Pemicu

Dipakai ketika menguji sistem AI agent (Muse, OpenAI, Google, 0din, ViKernel) dan pertanyaannya bukan "bisakah model ditipu berkata sesuatu", melainkan "apakah SERVER di belakang model mempercayai permintaan agent begitu saja tanpa memeriksa hak akses". Dipakai juga tiap ada perubahan/migrasi arsitektur target (lapisan proxy baru, konektor baru, tool baru) — batas kepercayaan paling sering jebol tepat setelah perubahan.

## Wawasan kunci

Model AI pada dasarnya mudah dimanipulasi — jailbreak, prompt injection, dan model yang berkata kasar saja TIDAK diterima sebagai bug keamanan dan TIDAK dibayar. Celah yang valid dan berbayar tinggi terjadi ketika **server di belakang model mempercayai permintaan agent begitu saja tanpa verifikasi hak akses (server-side authorization)**. Yang dinilai triase adalah HASIL di sisi server (aksi yang terjadi, data yang keluar), bukan trik terhadap modelnya.

Studi kasus pola ini: **$300rb — proxy-header auth (pra-peluncuran).** Migrasi menambah lapisan proxy kedua; sistem mempercayai header dari lingkungan yang bisa dipengaruhi penyerang, sehingga otorisasi dilewati. Pelajaran: audit batas kepercayaan, uji ulang tiap ada perubahan/migrasi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55 Analis Rantai & Pelapor** | Inventarisasi titik kepercayaan + rangkai temuan jadi rantai |
| Pengerjaan | **A58 Vulnerability Researcher** | Uji tiap titik dengan canary palsu + dokumentasikan bukti server-side |
| Pengerjaan | **A59 Threat Hunter** | Cari titik kepercayaan baru di perubahan/migrasi target |
| Audit | **A60 Security Auditor** | Audit temuan sebelum draf laporan; A60 tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Putuskan pengiriman semua laporan |

## Sudah tercakup (jangan diduplikat)

- Audit batas kepercayaan sebagai **satu baris strategi + studi kasus $300rb** sudah ada di `buru-bug-bounty` — skill ini adalah **METODOLOGI LENGKAP** (inventarisasi → uji → bukti), bukan baris strategi.
- Pembuktian diferensial (baseline 3 kondisi) → `access-control-differential-analyst`.
- Validasi + laporan → `triase-duplikat` + `laporan-abstrak`.
- Tool/function-calling abuse → `penyalahgunaan-tool-agen`. Injeksi tak langsung → `buru-bug-bounty`. RAG/memory poisoning → `racun-rag-memori`.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar scope = jangan sentuh.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa data asli pengguna mana pun. Nilai canary harus jelas palsu dan milik sendiri (mis. token/string acak yang kita buat, bukan kredensial hidup).
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Jangan pernah menanam perintah di akun/data orang lain atau menguji agent milik orang lain.
4. **Tanpa DoS/DDoS**, tanpa uji yang mengganggu layanan siapa pun, tanpa aksi destruktif (hapus/ubah konfigurasi permanen).
5. **Tanpa payload di permukaan publik.** Canary dan konten uji hanya di akun/ruang milik sendiri, tidak di-host di halaman/dokumen publik.
6. **Validasi human-in-the-loop.** Temuan tidak maju ke draf laporan sebelum A60 mengaudit dan Muse memutuskan.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu.
8. **Patuhi larangan otomasi program:** huntr "Humans only" (otomasi = banned); Gray Swan dilewati total (perintah Cipta 23 Nov 2026 18:35).
9. **Google AI VRP: payload injeksi DIBLOKIR, Tim 4 analisis format saja.** Jangan siapkan, parafrasa, atau cari jalan lain untuk payload injeksi Google.
10. **Bila program akan tutup, BERHENTI 1 hari sebelumnya** (ViKernel Season 1–3 tutup 16 Jan 2027 → STOP 15 Jan 2027; Season 4 tutup 15 Feb 2027 → STOP 14 Feb 2027).

## Langkah + gerbang

### Langkah 1 — Inventarisasi titik kepercayaan

Petakan secara sistematis setiap titik di mana server menerima sesuatu sebagai benar tanpa memeriksa ulang. Untuk tiap titik catat dalam tabel: (a) titiknya, (b) siapa yang bisa memengaruhinya, (c) apa yang dipercaya server tanpa verifikasi.

Titik yang wajib diperiksa:

| # | Titik kepercayaan | Siapa bisa memengaruhi | Yang dipercaya tanpa verifikasi |
|---|---|---|---|
| 1 | Header HTTP (mis. `X-Forwarded-For`, header auth/proxy) | Klien / proxy perantara | Identitas atau asal permintaan |
| 2 | Lapisan proxy (terutama setelah migrasi) | Konfigurasi infra / penyerang di jalur | Header yang diteruskan proxy |
| 3 | Variabel lingkungan | Proses / konfigurasi deployment | Nilai config/rahasia dari env |
| 4 | File lokal (mis. `AGENTS.md`, file konfigurasi) | Siapa pun yang bisa menulis file itu | Instruksi/aturan dari file |
| 5 | Metadata konektor | Pemilik konektor / data konektor | Identitas, scope, atau izin konektor |
| 6 | Skema tool | Definisi tool / server MCP | Argumen tool sesuai skema = sah |
| 7 | Deskripsi server MCP | Penyedia server MCP | Klaim kemampuan/identitas server |
| 8 | Pemicu scheduled job | Penjadwal / pemicu job | Job berjalan atas nama pemilik yang sah |
| 9 | Konten yang diteruskan antar-aplikasi | Aplikasi sumber / konten yang diteruskan | Konten terusan = perintah pemilik |

**Standar lulus:** peta berisi minimal 9 baris di atas (atau alasan tertulis bila satu titik tidak ada di target) + tiap baris lengkap kolom (a)–(c). Tanpa peta = jangan lanjut ke uji.

### Langkah 2 — Uji tiap titik dengan canary palsu

Untuk tiap titik, palsukan input yang dipercaya itu dengan nilai canary milik sendiri, lalu amati apakah backend bertindak tanpa memeriksa otorisasi server-side.

- Satu titik = satu hipotesis satu kalimat: "Saya menduga server mempercayai X tanpa memeriksa Y, sehingga Z bisa terjadi."
- Uji dengan langkah minimal; jangan merusak, jangan menghapus, jangan mengubah konfigurasi permanen.
- Hentikan uji di satu jalur begitu BERHASIL — lanjut ke dokumentasi, jangan dieksploitasi lebih jauh.

**Standar lulus:** tiap titik yang diuji punya hipotesis tertulis + nilai canary yang dipakai + hasil observasi (backend bertindak / menolak / tidak merespons). Titik yang tidak diuji dicatat alasannya.

### Langkah 3 — Buktikan dengan metode diferensial

Hubungkan ke `access-control-differential-analyst`: uji baseline 3 kondisi untuk membedakan "server memang tidak memeriksa" dari "model sekadar menurut".

1. Kondisi A — permintaan sah (akun sendiri, hak akses benar): aksi terjadi (kontrol positif).
2. Kondisi B — permintaan palsu (canary / identitas dipalsukan): aksi terjadi atau tidak?
3. Kondisi C — permintaan sah tapi hak akses dicabut/ditolak: aksi harus TIDAK terjadi (kontrol negatif).

**Standar lulus (gerbang utama):** temuan hanya VALID bila B terjadi (aksi server-side atas input palsu) DAN C tidak terjadi (pemeriksaan otorisasi memang ada dan bekerja pada jalur sah). Bila B tidak terjadi = belum berhasil. Bila C juga terjadi = otorisasi memang tidak ada di jalur itu sama sekali — catat sebagai temuan kelas berbeda, jangan klaim sebagai bypass.

### Langkah 4 — Kumpulkan standar bukti

Tanpa bukti ini, temuan = belum berhasil:

- **Aksi server-side yang terjadi atas input palsu** (log/output/tangkapan yang menunjukkan aksi nyata: data terkirim, state berubah, akses diberikan) — bukan sekadar model menjawab "baik, saya kirim".
- **Pemeriksaan otorisasi yang hilang/terlewati** — tunjukkan titik persisnya: permintaan mana yang lolos tanpa cek, dan apa yang seharusnya dicek menurut dokumentasi/scope program.
- **Langkah reproduksi persis** (bisa diulang orang lain dari sesi bersih).

**Tanpa aksi server = belum berhasil.** Model yang menurut saja, jawaban kasar, bocor system prompt, atau daftar tool — semuanya BUKAN temuan.

### Langkah 5 — Triase, audit, draf

Temuan yang lolos Langkah 3–4 → `triase-duplikat` (cek duplikat + skor per tier program) → A60 audit → draf laporan (`laporan-abstrak`) → Muse teruskan ke Cipta → Cipta setuju → kirim. Tidak lolos → catat alasan di log, kembali ke Langkah 1 (titik lain) atau riset ulang kenapa gagal.

**Standar lulus:** tidak ada temuan yang maju tanpa skor triase + audit A60 + persetujuan Cipta.

## Alat

- **Canary palsu:** token/string acak buatan sendiri (mis. `CANARY-<acak>-<tanggal>`) — dipakai sebagai nilai yang dipalsukan di header, env, file, metadata, atau argumen tool. Jangan pernah pakai kredensial/data asli.
- **Akun uji sendiri:** dua akun milik kita bila perlu membedakan peran (satu sebagai pemilik sah, satu sebagai pemalsu) — keduanya milik kita, tanpa data orang lain.
- **Pencatat:** `~/workspace/catatan/log-bug-bounty.md` (log semua uji) + `~/workspace/catatan/keputusan.md` (ringkasan hari itu juga).

## Format output

Log tiap sesi uji ke `~/workspace/catatan/log-bug-bounty.md`:

```
Tanggal: [YYYY-MM-DD HH:MM WIB]
Program/target: [nama program + target]
Peta titik kepercayaan: [tabel Langkah 1 — titik | siapa bisa memengaruhi | yang dipercaya]
Titik yang diuji: [nomor titik + hipotesis satu kalimat + nilai canary]
Bukti aksi server: [log/output aksi server-side atas input palsu — atau "TIDAK ADA"]
Pemeriksaan otorisasi yang hilang: [cek apa yang terlewati + di titik mana]
Dampak: [apa yang bisa dilakukan penyerang dengan ini]
Keputusan triase: [maju / tidak — alasan + skor bila maju]
Status: [BELUM BERHASIL / VALID — menunggu audit A60 / DRAF laporan / dikirim (dengan persetujuan Cipta)]
```

## Available connectors

Tidak ada konektor khusus untuk skill ini. Pengujian memakai akun sendiri di program target dan pencatatan di file log di atas.

## Websites

- Referensi dua perspektif: `~/workspace/catatan/referensi-dua-perspektif-skill-bug-bounty-ai-2026-11-23.md`
- Strategi + studi kasus $300rb: `~/workspace/tmp/pusat-komando-push/data/skills/buru-bug-bounty/SKILL.md`
- Pembuktian diferensial: `~/workspace/tmp/pusat-komando-push/data/skills/access-control-differential-analyst/SKILL.md`
- Validasi + laporan: `~/workspace/tmp/pusat-komando-push/data/skills/triase-duplikat/SKILL.md`, `~/workspace/tmp/pusat-komando-push/data/skills/laporan-abstrak/SKILL.md`

## Alternatives for better results

- Bila titik kepercayaan ternyata ada di skema tool/argumen: lanjutkan dengan `penyalahgunaan-tool-agen`.
- Bila titiknya ada di konten terusan antar-aplikasi (email/dokumen): lanjutkan dengan pola injeksi tak langsung di `buru-bug-bounty`.
- Bila titiknya ada di memori/RAG antar-tenant: lanjutkan dengan `racun-rag-memori`.
