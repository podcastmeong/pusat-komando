# Skill: Studi Kasus Eksploitasi MCP Nyata — Pola Serangan dari Writeup yang Sudah Terjadi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah korpus studi kasus dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 27; sumber: `Puliczek/awesome-mcp-security` — Articles/Blog Posts), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebelum menguji server/klien MCP in-scope: pelajari dulu pola serangan yang sudah terbukti di dunia nyata agar pengujian tidak mengulang dari nol.
- Ditemukan server MCP, integrasi MCP, atau agen yang memanggil tool MCP pada target in-scope.
- Saat triase butuh pembanding: apakah pola yang diamati di target sama dengan pola eksploitasi MCP yang sudah dilaporkan publik.
- Dipakai SEBELUM memilih teknik: petakan kasus → pola → hipotesis → baru uji.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Mempelajari kasus, memetakan pola ke target, menjalankan pengujian pola |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Menulis dan merangkai temuan menjadi laporan → skill `laporan-poc-otomatis`, `laporan-abstrak`, `perangkaian-kerentanan`.
- Pemindaian server MCP dengan scanner khusus → skill `pemindai-server-mcp`.
- Deskripsi tool/skill sebagai vektor racun (tool poisoning, rug pull) → skill `peracunan-deskripsi-tool-mcp`.
- Skill ini BUKAN kumpulan teknik baru — ini korpus kasus nyata sebagai bahan belajar pola; teknik pengujiannya dirujuk ke skill yang sesuai.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji pola dari studi kasus.
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

### Gerbang 1 — Kumpulkan kasus dan ekstrak polanya

Baca writeup publik di `Puliczek/awesome-mcp-security` (Articles/Blog Posts) dan ekstrak tiap kasus ke tabel pola: vektor masuk, pemicu, aksi agen yang disalahgunakan, dampak. Standar lulus: minimal 5 kasus terpetakan dengan pola yang berbeda.

Kasus acuan (cek ulang detailnya dari writeup asli sebelum dipakai):

| Kasus | Pola | Dampak |
|---|---|---|
| GitHub MCP Server dieksploitasi | Server MCP tepercaya memanggil tool atas data tak tepercaya | Akses repo privat |
| WhatsApp MCP | Tool pesan mengekspos riwayat ke agen | Ekstraksi riwayat pesan |
| Slack MCP (Anthropic) | Data Slack bocor lewat tool MCP | Kebocoran data |
| Neon remote MCP | Server MCP jarak jauh dieksploitasi | Akses data tak sah |
| mcp-remote RCE (437.000+ unduhan) | Paket/komponen MCP jarak jauh berisi RCE | Eksekusi kode jarak jauh |
| Cursor dibajak lewat Jira MCP | Tool Jira menyisipkan instruksi ke agen Cursor | Pembajakan agen |
| Base-MCP | Tool MCP mengalihkan transaksi | Pengalihan transaksi |
| Asana MCP | Paparan data lewat tool MCP | Data exposure |
| Cato "Living Off AI" | Agen dipakai sebagai living-off-the-land | Penyalahgunaan agen |
| Pencurian `.env` lewat MCP malware | Server MCP jahat membaca file sensitif host | Pencurian kredensial |

### Gerbang 2 — Petakan pola ke target in-scope

Untuk tiap pola, jawab: (a) apakah target punya permukaan yang sama (server MCP, tool yang membaca file, tool yang mengirim data keluar, integrasi pihak ketiga)? (b) tool MCP mana di target yang memegang data privat + saluran keluar sekaligus (lihat `audit-trifecta-mematikan` bila sudah dibangun; bila belum, catat manual)? Standar lulus: tiap pola yang dipetakan punya nama tool/endpoint target yang konkret, atau dinyatakan "tidak ada permukaan ini" dengan bukti.

### Gerbang 3 — Uji satu pola per putaran, bukti read-only

Uji pola yang terpetakan SATU per satu, hanya dengan akun dan data uji sendiri, hanya di lingkungan in-scope. Pembuktian aman: baca yang seharusnya tidak terbaca (canary sendiri), callback canary milik sendiri, atau `document.domain` — JANGAN menjalankan aksi destruktif, JANGAN menyentuh data orang lain, JANGAN melibatkan korban. Ulangi 3× (perilaku agen probabilistik). Standar lulus: pola teramati ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Korpus writeup `Puliczek/awesome-mcp-security` | Sumber kasus; baca writeup asli, jangan hanya judulnya. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai saat menguji pola. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log tabel pola → pemetaan target → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur/server MCP]
Kasus acuan: [nama kasus + URL writeup]
Pola: [vektor masuk] → [aksi agen disalahgunakan] → [dampak]
Pemetaan target: [tool/endpoint target yang punya permukaan sama]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Server/Fitur MCP] - [Pola serangan] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Pola (kasus acuan + cara pola itu bekerja di target); Langkah Reproduksi (akun uji sendiri + log HTTP); Rekomendasi Perbaikan (validasi asal tool, batasan tool per sesi, konfirmasi manusia untuk aksi sensitif).

## Batasan yang diketahui

- Korpus ini dari riset writeup publik, bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Detail tiap kasus bisa berubah atau writeup bisa ditarik — cek ulang URL writeup asli sebelum mengutipnya di laporan.
- Pola yang sama belum tentu berdampak sama di target lain: yang dinilai adalah HASIL/outcome di target in-scope, bukan kemiripan nama kasus.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah aksi nyata/data keluar, bukan sekadar "pola ini pernah terjadi di tempat lain".

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh taksonomi ancaman MCP secara sistematis (bukan kasus per kasus), pakai `taksonomi-ancaman-mcp`.
- Bila fokusnya deskripsi tool sebagai racun, pakai `peracunan-deskripsi-tool-mcp`.
- Bila target bukan MCP (aplikasi web klasik), pakai `fondasi-kerentanan-web-api` + skill Fase 5/6.
