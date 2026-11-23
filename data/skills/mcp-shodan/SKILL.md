# Skill: MCP Shodan — Recon Jaringan & CVE via API Shodan + CVEDB

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026) dan ringkasannya di `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`. Belum pernah dijalankan di lab maupun di program bounty nyata. Langkah, perintah, dan jumlah tool di bawah ini WAJIB dicek ulang dari README repo sebelum dipakai pertama kali.

## Pemicu — kapan dipakai

Dipakai saat A59 Threat Hunter butuh intel jaringan dan kerentanan dari data yang SUDAH dikumpulkan Shodan — tanpa memindai sendiri — untuk **program web klasik (mis. huntr)**: IP lookup (port, produk, CVE, TLS), pencarian perangkat, CVE dengan CVSS/EPSS/KEV, DNS, dan CPE. Bukan untuk bounty agen AI. Cocok sebagai langkah recon pasif sebelum memutuskan scan aktif.

## Pemilik

- **Pemilik: A59 Threat Hunter** — yang menjalankan query, menjaga kuota kredit Shodan, dan memvalidasi hasil.
- **Pemimpin: Muse** — yang memutuskan temuan mana yang layak jadi laporan.

## ⚠️ Alamat repo baru — jangan pakai alamat lama

> **Repo ini PINDAH dari `BurtTheCoder/mcp-shodan` ke `w0h1v/mcp-shodan` — pakai alamat baru.** Alamat lama (`github.com/BurtTheCoder/mcp-shodan`) sudah tidak berlaku sebagai sumber utama; panduan, instalasi, dan update WAJIB merujuk ke `https://github.com/w0h1v/mcp-shodan`. Bila menemukan panduan lama yang masih mengarah ke BurtTheCoder, anggap kedaluwarsa dan ganti ke alamat baru.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban** (victim-agent fraud tests DIBLOKIR — jangan dicoba).
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop** (AI bantu, manusia putuskan dan validasi).
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **PENTING untuk kategori ini: alat MCP suite/recon adalah alat KLASIK — HANYA untuk program web klasik (mis. huntr), BUKAN untuk bounty agen AI (Muse, OpenAI, 0din, Google AI VRP, ViKernel).**

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu (wajib, sebelum query apa pun)

- Apa yang dilakukan: baca aturan program target, catat IP/domain in-scope dan yang dilarang.
- Standar lulus: target tertulis; query terhadap IP/domain DI LUAR scope = DILARANG, jangan lanjut.

### Gerbang 1 — Verifikasi repo + siapkan API key sendiri

- Apa yang dilakukan: buka https://github.com/w0h1v/mcp-shodan (alamat BARU), cek push terakhir dan README; siapkan API key Shodan milik sendiri lewat variabel lingkungan (`SHODAN_API_KEY`); cek sisa kredit dengan `api_info`.
- Standar lulus: repo aktif dan README terbaca; API key terbaca dari environment (JANGAN tulis key di skill, log, atau chat); sisa kredit diketahui sebelum query berbayar. Tanpa key sendiri = BERHENTI.

### Gerbang 2 — Mulai dari yang gratis (CVEDB + count)

- Apa yang dilakukan: pakai dulu tool gratis — `cve_lookup`, `cpe_lookup`, `cves_by_product` (CVEDB, gratis, tidak makan kredit) dan `shodan_count` (hitung hasil tanpa mengambil data).
- Standar lulus: ada gambaran CVE/produk dan ukuran hasil pencarian SEBELUM memakai kredit berbayar. Langsung ke pencarian berbayar tanpa sizing = boros, ulangi gerbang ini.

### Gerbang 3 — Query berbayar seperlunya (IP lookup + search)

- Apa yang dilakukan: `ip_lookup` (port, produk, CVE, TLS, lokasi, cloud untuk satu IP in-scope), `shodan_search` (sintaks query Shodan, dengan paging dan facet), `domain_info` (subdomain + DNS record untuk domain in-scope), `dns_lookup` / `reverse_dns_lookup` (batch secukupnya).
- Standar lulus: setiap query menargetkan IP/domain in-scope; jumlah halaman dibatasi (tiap halaman tambah = 1 kredit); sisa kredit dicek lagi dengan `api_info` setelah sesi. Kredit habis di tengah jalan = BERHENTI, jangan pakai key orang lain.

### Gerbang 4 — Korelasikan CVE dengan bukti (CVSS/EPSS/KEV)

- Apa yang dilakukan: untuk tiap CVE yang muncul, tarik detailnya (`cve_lookup`): skor CVSS, EPSS, status KEV, CPE yang terdampak; cocokkan dengan versi produk yang terlihat di `ip_lookup`.
- Standar lulus: tiap klaim kerentanan punya pasangan (CVE + versi produk yang terdampak + skor). CVE tanpa versi produk yang cocok = BELUM TERBUKTI, jangan diteruskan sebagai temuan.

### Gerbang 5 — Validasi manual oleh manusia

- Apa yang dilakukan: A59 memeriksa tiap temuan secara manual. AI hanya merangkum; manusia yang memutuskan nyata vs false positive.
- Standar lulus: tiap temuan yang diteruskan punya bukti yang bisa diulang (query + output + tanggal). Temuan tanpa bukti = BUKAN temuan.

### Gerbang 6 — Laporan (hanya dengan persetujuan Cipta)

- Apa yang dilakukan: tulis draf laporan (lihat "Format output"), serahkan ke Muse → Cipta. Kirim HANYA setelah Cipta setuju.
- Standar lulus: laporan berisi scope, query yang dipakai, bukti yang bisa diulang, dan dampak; tanpa klaim yang tidak dibuktikan di Gerbang 4–5.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| **mcp-shodan** (7 tools di atas API Shodan + CVEDB) | https://github.com/w0h1v/mcp-shodan (~170 bintang) — alamat BARU, pindahan dari BurtTheCoder/mcp-shodan | `git clone https://github.com/w0h1v/mcp-shodan` lalu ikuti README; butuh `SHODAN_API_KEY` sendiri |
| ip_lookup, shodan_search, shodan_count, domain_info | termasuk di mcp-shodan | Recon jaringan + pencarian perangkat (Gerbang 3) |
| cve_lookup, cpe_lookup, cves_by_product | termasuk di mcp-shodan (CVEDB) | Intel CVE: CVSS, EPSS, KEV, CPE — gratis, tidak makan kredit (Gerbang 2, 4) |
| dns_lookup, reverse_dns_lookup, search_filters, api_info | termasuk di mcp-shodan | DNS batch + daftar filter + cek sisa kredit |
| SkillSpector (pemindai skill/MCP) | https://github.com/NVIDIA/SkillSpector | Pindai skill/MCP dari prompt injection sebelum install |

## Format output

Tulis log tiap sesi ke `~/workspace/catatan/log-bug-bounty.md` (tambahkan entri baru, jangan timpa log lama) dengan format:

```
Tanggal: <YYYY-MM-DD>
Program: <nama program bounty>
Target (in-scope): <IP/domain>
Alat: mcp-shodan — tool yang dipakai: <daftar>
Kredit Shodan: <sisa sebelum> → <sisa sesudah>
Temuan: <ringkasan per temuan + CVE/CVSS/EPSS/KEV + bukti query/output>
Status: <RECON / VALID / DRAF LAPORAN — menunggu persetujuan Cipta>
```

Draf laporan lengkap (scope, query, bukti, dampak) ditulis sebagai file terpisah di `~/workspace/catatan/` dan diserahkan ke Muse sebelum dikirim ke program. **Tidak ada laporan yang dikirim tanpa persetujuan Cipta.**

## Catatan yang belum terverifikasi

- Jumlah "7 tools" berasal dari artikel (per 23 Nov 2026); versi terbaru repo mencatat 11 read-only tools (tambahan `shodan_count`, `domain_info`, `search_filters`, `api_info`) — cek `tools/list` saat instalasi pertama dan pakai daftar terbaru.
- Belum diuji: instalasi, pemakaian API key, dan konsumsi kredit di akun Shodan tim.
- API key Shodan adalah milik tim — JANGAN pernah menulis nilainya di skill, log, atau chat.
