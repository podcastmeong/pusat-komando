# Skill: MCP Security Hub — Suite 300+ Alat Pentest Klasik dalam Satu Docker

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026) dan ringkasannya di `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`. Belum pernah dijalankan di lab maupun di program bounty nyata. Langkah, perintah, dan jumlah tool di bawah ini WAJIB dicek ulang dari README repo sebelum dipakai pertama kali.

## Pemicu — kapan dipakai

Dipakai saat A57 Penetration Tester butuh BANYAK alat pentest klasik sekaligus (recon, scan web, analisis biner, OSINT) dalam satu sesi kerja untuk **program web klasik (mis. huntr)** — bukan untuk bounty agen AI. Satu `docker pull` memberi 38 server MCP dengan 300+ tools, jadi tidak perlu memasang nmap, nuclei, sqlmap, ffuf, subfinder, katana, searchsploit, hashcat, Ghidra, BloodHound, dan gitleaks satu per satu.

## Pemilik

- **Pemilik: A57 Penetration Tester** — yang menjalankan, memilih server yang diaktifkan, dan memvalidasi hasil.
- **Pemimpin: Muse** — yang memutuskan temuan mana yang layak jadi laporan.

## ⚠️ PENJAGA — Nmap MCP

> **Nmap MCP server DIARSIPKAN dan README-nya sendiri memperingatkan risiko prompt injection — JANGAN PAKAI Nmap MCP; pakai nmap lewat mcp-security-hub atau mcp-pentest.**

Jangan pernah memasang server MCP nmap yang berdiri sendiri. Kalau butuh nmap, jalankan server nmap yang sudah termasuk di dalam mcp-security-hub ini.

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

### Gerbang 0 — Cek scope dulu (wajib, sebelum alat apa pun jalan)

- Apa yang dilakukan: baca aturan program target (halaman program huntr / kebijakan bounty), catat domain/IP yang in-scope dan yang dilarang, catat apakah otomasi diizinkan.
- Standar lulus: target tertulis di catatan kerja; target DI LUAR scope = BERHENTI, jangan lanjut ke Gerbang 1. Bila program melarang otomasi, skill ini TIDAK BOLEH dipakai untuk program itu.

### Gerbang 1 — Verifikasi repo sebelum install

- Apa yang dilakukan: buka https://github.com/FuzzingLabs/mcp-security-hub, cek bintang, push terakhir, dan README; baca apa yang dilakukan tiap server yang akan diaktifkan; jalankan hanya di container/VM yang bisa dibuang.
- Standar lulus: repo masih aktif (ada push dalam beberapa bulan terakhir), README terbaca, tidak ada peringatan arsip. Bila repo mati/diarsipkan = BERHENTI dan laporkan ke Muse.

### Gerbang 2 — Instalasi (satu docker pull)

- Apa yang dilakukan: ikuti README repo (Docker Compose) untuk menarik dan menjalankan server; **aktifkan HANYA server yang dibutuhkan** untuk tugas ini (menjalankan ke-38 server sekaligus menghabiskan banyak resource).
- Standar lulus: server yang dipilih merespons (mis. `tools/list` mengembalikan daftar tool); server yang tidak dibutuhkan tetap MATI.

### Gerbang 3 — Recon pasif dulu

- Apa yang dilakukan: mulai dari alat pasif/tanpa sentuhan berat — subfinder, katana (crawl), Shodan, gitleaks (pada repo sendiri/in-scope), searchsploit (pencarian lokal, tanpa kirim exploit).
- Standar lulus: ada daftar aset/subdomain/permukaan yang terpetakan, semuanya masih di dalam scope Gerbang 0. Tanpa peta ini, jangan lanjut ke scan aktif.

### Gerbang 4 — Scan aktif ringan (in-scope saja)

- Apa yang dilakukan: nmap (port scan, tanpa flood), nuclei (template scan), ffuf (fuzzing direktori dengan wordlist kecil), nikto bila perlu. Satu target, satu alat, satu waktu.
- Standar lulus: setiap pemindaian menargetkan HANYA host in-scope; tidak ada trafik ke host lain; tidak ada tanda DoS (rate wajar, jeda antar request). Temuan dicatat apa adanya — belum disimpulkan.

### Gerbang 5 — Validasi manual oleh manusia

- Apa yang dilakukan: A57 memeriksa tiap temuan scan secara manual (buka sendiri, ulangi sendiri). AI hanya merangkum; manusia yang memutuskan "ini temuan nyata" atau "ini false positive".
- Standar lulus: tiap temuan yang diteruskan punya bukti yang bisa diulang (perintah + output + tangkapan layar/transkrip). Temuan tanpa bukti = BUKAN temuan, jangan diteruskan.

### Gerbang 6 — Laporan (hanya dengan persetujuan Cipta)

- Apa yang dilakukan: tulis draf laporan (lihat "Format output"), serahkan ke Muse → Cipta. Kirim HANYA setelah Cipta setuju.
- Standar lulus: laporan berisi scope, alat yang dipakai, bukti yang bisa diulang, dan dampak; tanpa klaim yang tidak dibuktikan di Gerbang 5.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| **mcp-security-hub** (38 server MCP, 300+ tools) | https://github.com/FuzzingLabs/mcp-security-hub (~800 bintang) | Docker Compose sesuai README; aktifkan hanya server yang dibutuhkan |
| nmap, masscan | termasuk di hub | Port scanning in-scope saja (lihat Gerbang 4); JANGAN pakai server Nmap MCP yang berdiri sendiri (lihat PENJAGA di atas) |
| nuclei, sqlmap, ffuf, nikto | termasuk di hub | Scan kerentanan web pada target in-scope |
| subfinder, katana | termasuk di hub | Enumerasi subdomain + crawl (Gerbang 3) |
| Shodan | termasuk di hub | Recon internet-facing (butuh API key sendiri — JANGAN tulis key di skill/log) |
| searchsploit, hashcat | termasuk di hub | Pencarian exploit lokal + cracking hash milik sendiri |
| Ghidra, radare2, Binwalk, YARA | termasuk di hub | Analisis biner (file milik sendiri / sampel in-scope) |
| BloodHound, gitleaks | termasuk di hub | Pemetaan Active Directory + pemindaian secret di repo in-scope |
| SkillSpector (pemindai skill/MCP) | https://github.com/NVIDIA/SkillSpector | Pindai skill/MCP dari prompt injection sebelum install (lihat referensi artikel) |

## Format output

Tulis log tiap sesi ke `~/workspace/catatan/log-bug-bounty.md` (tambahkan entri baru, jangan timpa log lama) dengan format:

```
Tanggal: <YYYY-MM-DD>
Program: <nama program bounty>
Target (in-scope): <domain/IP>
Alat: mcp-security-hub — server yang diaktifkan: <daftar>
Temuan: <ringkasan per temuan + bukti perintah/output>
Status: <RECON / SCAN / VALID / DRAF LAPORAN — menunggu persetujuan Cipta>
```

Draf laporan lengkap (scope, langkah, bukti, dampak) ditulis sebagai file terpisah di `~/workspace/catatan/` dan diserahkan ke Muse sebelum dikirim ke program. **Tidak ada laporan yang dikirim tanpa persetujuan Cipta.**

## Catatan yang belum terverifikasi

- Jumlah "38 server / 300+ tools" dan daftar tool di atas berasal dari artikel + README ringkasan (per 23 Nov 2026); jumlah persisnya bisa berubah seiring versi repo — cek `tools/list` saat instalasi pertama.
- Belum diuji: instalasi Docker, konsumsi resource, dan apakah semua server jalan di VM Pusat Komando.
