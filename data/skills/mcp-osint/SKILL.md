# Skill: MCP OSINT — 37 Alat OSINT dari 12 Sumber

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026) dan ringkasannya di `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`. Belum pernah dijalankan di lab maupun di program bounty nyata. Langkah, perintah, dan jumlah tool di bawah ini WAJIB dicek ulang dari README repo sebelum dipakai pertama kali.

## Pemicu — kapan dipakai

Dipakai saat A59 Threat Hunter butuh memetakan permukaan serangan sebuah domain/IP dari data PUBLIK untuk **program web klasik (mis. huntr)** — bukan untuk bounty agen AI. Satu server memberi 37 tools dari 12 sumber (DNS, RDAP/WHOIS, crt.sh, GeoIP, BGPView, Wayback, M365 tenant discovery, Shodan, VirusTotal, Censys, SecurityTrails, dan lain-lain); 21 tools jalan tanpa API key, jadi recon awal bisa mulai tanpa kredensial apa pun.

## Pemilik

- **Pemilik: A59 Threat Hunter** — yang menjalankan query, menjaga API key, dan memvalidasi hasil.
- **Pemimpin: Muse** — yang memutuskan temuan mana yang layak jadi laporan.

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
11. **OSINT = data publik saja.** Jangan memakai tool ini untuk mengumpulkan data pribadi orang lain, kredensial bocor milik orang lain, atau informasi non-publik. Yang dicari hanya permukaan serangan target in-scope (domain, subdomain, IP, sertifikat, DNS, histori).

## Langkah + gerbang

### Gerbang 0 — Cek scope dulu (wajib, sebelum query apa pun)

- Apa yang dilakukan: baca aturan program target, catat domain/IP in-scope dan yang dilarang.
- Standar lulus: target tertulis; query terhadap domain/IP DI LUAR scope = DILARANG, jangan lanjut.

### Gerbang 1 — Verifikasi repo + instalasi tanpa key

- Apa yang dilakukan: buka https://github.com/badchars/osint-mcp-server, cek push terakhir dan README; install via `npx osint-mcp-server` (tanpa install) atau clone repo; JANGAN masukkan API key dulu.
- Standar lulus: server jalan dan 21 tools tanpa API key merespons. Bila repo mati/diarsipkan = BERHENTI dan laporkan ke Muse.

### Gerbang 2 — Recon pasif tanpa key (21 tools)

- Apa yang dilakukan: `dns_lookup` (A/AAAA/MX/TXT/NS/SOA/CNAME/SRV), `dns_reverse`, `dns_email_security` (SPF + DMARC + DKIM), `dns_spf_chain`, `dns_wildcard_check`, `whois_domain` / `whois_ip` (RDAP), `crtsh_search` (subdomain dari Certificate Transparency), plus GeoIP, BGPView, dan Wayback.
- Standar lulus: ada peta awal — daftar subdomain, record DNS, status email security, dan histori — semuanya untuk target in-scope. Tanpa peta ini, jangan lanjut ke tool ber-key.

### Gerbang 3 — Tambah key HANYA bila perlu (dan hanya key sendiri)

- Apa yang dilakukan: bila Gerbang 2 kurang, tambahkan key sendiri satu per satu sesuai kebutuhan: `SHODAN_API_KEY` (4 tools Shodan), `VT_API_KEY` (4 tools VirusTotal), `CENSYS_API_ID` + `CENSYS_API_SECRET` (3 tools Censys), `ST_API_KEY` (3 tools SecurityTrails). Key lewat variabel lingkungan saja.
- Standar lulus: tiap key yang dipakai adalah milik tim sendiri; nilai key TIDAK PERNAH ditulis di skill, log, atau chat; tool ber-key yang tidak dibutuhkan tetap MATI.

### Gerbang 4 — Korelasi lintas sumber

- Apa yang dilakukan: silangkan hasil antar sumber — mis. subdomain dari crt.sh vs DNS vs VirusTotal; IP dari BGPView vs Shodan; M365 tenant discovery hanya untuk domain in-scope.
- Standar lulus: tiap aset yang dicatat muncul dengan sumbernya (tool + tanggal query); aset yang hanya muncul di satu sumber tanpa konfirmasi dicatat sebagai "belum terkonfirmasi", bukan sebagai fakta.

### Gerbang 5 — Validasi manual oleh manusia

- Apa yang dilakukan: A59 memeriksa tiap temuan secara manual. AI hanya merangkum; manusia yang memutuskan nyata vs false positive.
- Standar lulus: tiap temuan yang diteruskan punya bukti yang bisa diulang (query + output + tanggal). Temuan tanpa bukti = BUKAN temuan.

### Gerbang 6 — Laporan (hanya dengan persetujuan Cipta)

- Apa yang dilakukan: tulis draf laporan (lihat "Format output"), serahkan ke Muse → Cipta. Kirim HANYA setelah Cipta setuju.
- Standar lulus: laporan berisi scope, sumber yang dipakai, bukti yang bisa diulang, dan dampak; tanpa klaim yang tidak dibuktikan di Gerbang 4–5.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| **osint-mcp-server** (37 tools, 12 sumber) | https://github.com/badchars/osint-mcp-server (~50 bintang) | `npx osint-mcp-server` (tanpa install) atau clone repo; 21 tools jalan tanpa API key |
| dns_lookup, dns_reverse, dns_email_security, dns_spf_chain, dns_srv_discover, dns_wildcard_check | termasuk di osint-mcp-server | Recon DNS + email security — tanpa key (Gerbang 2) |
| whois_domain, whois_ip | termasuk di osint-mcp-server | RDAP/WHOIS domain + IP — tanpa key (Gerbang 2) |
| crtsh_search | termasuk di osint-mcp-server | Subdomain dari Certificate Transparency — tanpa key (Gerbang 2) |
| GeoIP, BGPView, Wayback, M365 tenant discovery | termasuk di osint-mcp-server | Lokasi, routing, histori, tenant — tanpa key (Gerbang 2) |
| shodan_host, shodan_search, shodan_dns_resolve, shodan_exploits | termasuk di osint-mcp-server | Butuh `SHODAN_API_KEY` sendiri (Gerbang 3) |
| vt_domain, vt_ip, vt_subdomains, vt_url | termasuk di osint-mcp-server | Butuh `VT_API_KEY` sendiri (Gerbang 3) |
| Censys (3 tools), SecurityTrails (3 tools) | termasuk di osint-mcp-server | Butuh `CENSYS_API_ID` + `CENSYS_API_SECRET` / `ST_API_KEY` sendiri (Gerbang 3) |
| SkillSpector (pemindai skill/MCP) | https://github.com/NVIDIA/SkillSpector | Pindai skill/MCP dari prompt injection sebelum install |

## Format output

Tulis log tiap sesi ke `~/workspace/catatan/log-bug-bounty.md` (tambahkan entri baru, jangan timpa log lama) dengan format:

```
Tanggal: <YYYY-MM-DD>
Program: <nama program bounty>
Target (in-scope): <domain/IP>
Alat: mcp-osint — tool yang dipakai: <daftar + sumber tiap hasil>
Temuan: <ringkasan per temuan + bukti query/output + status konfirmasi>
Status: <RECON / VALID / DRAF LAPORAN — menunggu persetujuan Cipta>
```

Draf laporan lengkap (scope, sumber, bukti, dampak) ditulis sebagai file terpisah di `~/workspace/catatan/` dan diserahkan ke Muse sebelum dikirim ke program. **Tidak ada laporan yang dikirim tanpa persetujuan Cipta.**

## Catatan yang belum terverifikasi

- Jumlah "37 tools / 12 sumber / 21 tanpa API key" berasal dari artikel + README (per 23 Nov 2026); daftar tool persisnya bisa berubah — cek `tools/list` saat instalasi pertama.
- Belum diuji: instalasi via npx, tool tanpa key, maupun tool ber-key di VM Pusat Komando.
- API key (Shodan, VirusTotal, Censys, SecurityTrails) adalah milik tim — JANGAN pernah menulis nilainya di skill, log, atau chat.
