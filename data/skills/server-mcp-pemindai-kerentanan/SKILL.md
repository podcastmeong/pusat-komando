# Skill: Server MCP Pemindai Kerentanan — Menjalankan Nuclei, Semgrep, dan Pemeriksa Lain lewat MCP

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pemindaian lewat MCP dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 36; sumber: `Puliczek/awesome-mcp-security` — MCP Security Servers), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Perlu memindai kerentanan/kode target in-scope DALAM alur kerja agen: Nuclei dan Semgrep dijalankan sebagai server MCP agar agen bisa memindai, menafsirkan, dan merangkai hasilnya otomatis.
- Ditemukan server MCP scanner pada target atau di lingkungan kerja tim: Nuclei MCP Integration, Semgrep MCP Server, VirusTotal MCP Server, DNStwist MCP Server, urlDNA MCP.
- Saat butuh cek file/URL/domain (VirusTotal, urlDNA, DNStwist) sebagai bagian dari rantai pengujian agen.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan scanner lewat MCP, menafsirkan hasil, memvalidasi temuan |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- OSINT umum lewat MCP (VirusTotal sebagai 1 dari 12 sumber publik, tanpa pemindaian kerentanan) → skill `mcp-osint` — itu recon data publik; skill ini soal MENGEKSEKUSI scanner (Nuclei/Semgrep) lewat antarmuka MCP.
- Suite 300+ alat pentest klasik dalam satu Docker → skill `mcp-security-hub` — Nuclei/Semgrep di sana adalah tool klasik di dalam suite untuk program web klasik, bukan server MCP scanner yang dirangkai agen.
- Pemindaian server MCP dengan scanner khusus MCP → skill `pemindai-server-mcp` — itu memindai SERVER MCP-nya; skill ini memakai scanner KEAMANAN sebagai server MCP untuk memindai target.
- Skill ini KHUSUS pemakaian scanner keamanan sebagai server MCP (Nuclei, Semgrep, VirusTotal, DNStwist, urlDNA) dalam alur kerja agen bounty — fungsi dan interpretasi hasilnya lain dari ketiga skill di atas.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh target pemindaian berada dalam in-scope program sebelum scanner dijalankan.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat memvalidasi temuan scanner.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pemindaian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Pilih server MCP scanner dan verifikasi dari README

Pilih server sesuai kebutuhan (cek README masing-masing sebelum memakai — jangan mengarang flag):

| Server MCP | Kegunaan |
|---|---|
| Nuclei MCP Integration | Memindai kerentanan target dengan template Nuclei |
| Semgrep MCP Server | Memindai kode (milik sendiri/in-scope) dengan aturan Semgrep |
| VirusTotal MCP Server | Cek file/URL/domain terhadap reputasi VirusTotal |
| DNStwist MCP Server | Cek domain typosquat/serupa terhadap domain target |
| urlDNA MCP | Cek URL/domain (reputasi, konten, perilaku) |

Standar lulus: server yang dipilih merespons `tools/list`; template/aturan yang dipakai tercatat (nama template Nuclei / aturan Semgrep); API key yang dipakai adalah milik tim sendiri dan TIDAK PERNAH ditulis di skill, log, atau chat. Bila repo server mati/diarsipkan = BERHENTI dan laporkan ke Muse.

### Gerbang 2 — Pindai target in-scope saja, satu target satu waktu

Jalankan scanner HANYA terhadap target yang tertulis in-scope. Satu target, satu scanner, satu waktu. Untuk Nuclei: pakai template yang relevan dengan permukaan target (jangan jalankan semua template sekaligus tanpa alasan). Untuk Semgrep: pindai hanya kode milik sendiri/in-scope. Untuk VirusTotal/DNStwist/urlDNA: cek hanya file/URL/domain yang terkait target in-scope. Standar lulus: ada laporan hasil scanner per target dengan target yang jelas in-scope; tidak ada trafik ke host lain; tidak ada tanda DoS (rate wajar, jeda antar request).

### Gerbang 3 — Tafsirkan dan validasi manual (lawan false positive)

Untuk tiap temuan scanner, lakukan TIGA langkah sebelum maju: (a) baca temuan mentahnya — apakah benar kerentanan atau hanya pola yang mirip; (b) validasi manual dengan akun uji sendiri + canary palsu (bukti baca/callback canary, read-only); (c) ulangi 3× bila temuan melibatkan perilaku agen (probabilistik). Standar lulus: temuan terkonfirmasi manual ATAU dinyatakan false positive dengan alasannya. **Hasil scanner mentah BUKAN laporan** — yang maju hanya temuan yang lolos validasi manual ini.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Nuclei MCP Integration, Semgrep MCP Server | Scanner utama lewat MCP; ikuti README masing-masing. |
| VirusTotal MCP Server, DNStwist MCP Server, urlDNA MCP | Pemeriksa file/URL/domain; pakai key sendiri, jangan kirim data sensitif. |
| Akun uji sendiri + canary palsu | Validasi manual temuan scanner. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log scanner → tafsir → validasi → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + host/kode in-scope]
Server MCP scanner: [nama server + versi + template/aturan yang dipakai]
Hasil mentah: [temuan scanner, apa adanya]
Tafsir: [benar / false positive + alasan]
Validasi manual: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipindai / divalidasi / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Target] - [Jenis kerentanan tervalidasi] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Scanner (server MCP + template/aturan + hasil mentah); Validasi Manual (akun uji sendiri + log HTTP + bukti read-only); Rekomendasi Perbaikan (perbaiki kerentanan yang ditemukan, sesuai jenisnya).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap server MCP scanner butuh satu kali pemakaian nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Scanner menghasilkan false positive — Gerbang 3 (validasi manual) tidak boleh dilewati dengan alasan apa pun.
- Template Nuclei dan aturan Semgrep terus bertambah/berubah — catat versi template/aturan yang dipakai agar hasil bisa direproduksi.
- API key (VirusTotal dan sejenisnya) adalah milik tim — JANGAN pernah menulis nilainya di skill, log, atau chat.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan jumlah temuan mentah scanner.

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang dipindai adalah server MCP-nya (bukan target lewat scanner), pakai `pemindai-server-mcp`.
- Bila butuh recon OSINT pasif (bukan pemindaian aktif), pakai `mcp-osint`.
- Bila butuh suite alat klasik sekaligus (bukan scanner lewat MCP), pakai `mcp-security-hub`.
