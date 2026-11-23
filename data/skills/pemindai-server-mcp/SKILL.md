# Skill: Pemindai Server MCP — Scan Keamanan Server MCP dengan Scanner Khusus

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pemindaian dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 29; sumber: `Puliczek/awesome-mcp-security` — Tools), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Ditemukan server MCP pada target in-scope dan perlu dinilai cepat: misconfig, tool beracun, permukaan SSRF.
- Sebelum pengujian manual mendalam: jalankan scanner khusus MCP dulu untuk memetakan permukaan.
- Saat hasil scanner perlu ditafsirkan: bedakan temuan benar dari false positive sebelum maju ke triase.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan scanner, menafsirkan hasil, memvalidasi temuan |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Suite 300+ alat pentest klasik dalam satu Docker (nmap, nuclei, sqlmap, Ghidra, BloodHound sebagai tool klasik) → skill `mcp-security-hub` — itu suite alat KLASIK untuk program web klasik, bukan scanner khusus MCP.
- Pemindaian skill/MCP sebelum install (gerbang statis) → skill `skill-skillspector` — itu pemindai skill pihak ketiga sebelum dipakai, bukan pemindai server MCP target.
- Recon OSINT lewat MCP (37 tools, 12 sumber publik) → skill `mcp-osint`.
- Skill ini KHUSUS scanner yang memang dibuat untuk server MCP (MCP Watch, mcp-scan, Secure MCP, MCP-Shield, mcpserverscanner.com, mcpscan.ai) — cara pakai dan interpretasi hasilnya berbeda dari scanner klasik.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh server MCP berada dalam in-scope program sebelum pemindaian dimulai.
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

### Gerbang 1 — Verifikasi scanner sebelum dipakai

Periksa tiap scanner dari README resminya sebelum menjalankan (cek ulang perintah di bawah dari README — jangan mengarang flag):

| Scanner | Sumber | Kegunaan |
|---|---|---|
| MCP Watch | awesome-mcp-security → Tools | Memantau/mengawasi server MCP |
| mcp-scan | `invariantlabs-ai/mcp-scan` | Memindai tool beracun dan misconfig server MCP |
| Secure MCP | `makalin/secure-mcp` | Pemeriksaan keamanan server MCP |
| MCP-Shield | awesome-mcp-security → Tools | Perisai/pemindai server MCP |
| mcpserverscanner.com | Layanan web | Pemindaian server MCP dari luar |
| mcpscan.ai | Layanan web | Pemindaian server MCP dari luar |

Standar lulus: repo/layanan masih aktif, README terbaca, tidak ada peringatan arsip; scanner dipahami cara kerjanya (apa yang dipindai, apa outputnya). Bila repo mati/diarsipkan = BERHENTI dan laporkan ke Muse.

### Gerbang 2 — Pindai server in-scope saja

Jalankan scanner HANYA terhadap server MCP yang tertulis in-scope di Gerbang 0 (baca aturan program dulu). Satu server, satu scanner, satu waktu. Jangan memindai server di luar scope, jangan memindai server milik pihak ketiga yang tidak tercantum. Standar lulus: ada laporan hasil scanner per server (misconfig, tool beracun, permukaan SSRF) dengan target yang jelas in-scope.

### Gerbang 3 — Tafsirkan dan validasi manual (lawan false positive)

Untuk tiap temuan scanner, lakukan TIGA langkah sebelum maju: (a) baca deskripsi tool/server yang ditandai — apakah benar beracun atau hanya pola yang mirip; (b) validasi manual dengan akun uji sendiri + canary palsu (bukti baca/callback canary, read-only); (c) ulangi 3× bila temuan melibatkan perilaku agen (probabilistik). Standar lulus: temuan terkonfirmasi manual ATAU dinyatakan false positive dengan alasannya. **Hasil scanner mentah BUKAN laporan** — yang maju hanya temuan yang lolos validasi manual ini.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| MCP Watch, mcp-scan, Secure MCP, MCP-Shield | Scanner lokal; ikuti README masing-masing, jangan mengarang flag. |
| mcpserverscanner.com, mcpscan.ai | Scanner layanan web; pakai hanya untuk server in-scope, jangan kirim data sensitif. |
| Akun uji sendiri + canary palsu | Validasi manual temuan scanner. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hasil scanner → tafsir → validasi → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + server MCP]
Scanner: [nama scanner + versi + perintah yang dijalankan]
Hasil mentah: [temuan scanner, apa adanya]
Tafsir: [benar / false positive + alasan]
Validasi manual: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipindai / divalidasi / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Server MCP] - [Jenis temuan scanner yang tervalidasi] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Scanner (alat + hasil mentah); Validasi Manual (akun uji sendiri + log HTTP + bukti read-only); Rekomendasi Perbaikan (perbaiki misconfig, hapus/karantina tool beracun, batasi permukaan SSRF).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap scanner butuh satu kali pemakaian nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Scanner MCP masih muda: false positive tinggi, dan scanner bisa ketinggalan dari pola racun terbaru — validasi manual (Gerbang 3) tidak boleh dilewati.
- Scanner layanan web (mcpserverscanner.com, mcpscan.ai) memindai dari luar — jangan kirim kredensial, token, atau data sensitif ke layanan tersebut.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan skor scanner.

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- mcp-scan (Invariant Labs) — https://github.com/invariantlabs-ai/mcp-scan
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh suite alat pentest klasik (bukan scanner MCP), pakai `mcp-security-hub`.
- Bila butuh memindai skill/MCP pihak ketiga SEBELUM install, pakai `skill-skillspector`.
- Bila temuan scanner adalah deskripsi tool beracun, dalami dengan `peracunan-deskripsi-tool-mcp`.
