# Skill: MCP Bolt — Kali Dockerized 100+ Alat, Penerus mcp-for-security

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026) dan ringkasannya di `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`. Belum pernah dijalankan di lab maupun di program bounty nyata. Langkah, perintah, dan jumlah tool di bawah ini WAJIB dicek ulang dari README repo sebelum dipakai pertama kali.

## Pemicu — kapan dipakai

Dipakai saat A57 Penetration Tester butuh lingkungan Kali lengkap yang sudah jadi (Dockerized Kali, 100+ tools, 33 MCP tools) untuk **program web klasik (mis. huntr)** — bukan untuk bounty agen AI. Bolt adalah pilihan utama bila butuh satu server MCP yang menulis ulang dan menggantikan koleksi lama mcp-for-security, dengan dukungan Docker penuh.

## Pemilik

- **Pemilik: A57 Penetration Tester** — yang menjalankan, memilih tool yang dipakai, dan memvalidasi hasil.
- **Pemimpin: Muse** — yang memutuskan temuan mana yang layak jadi laporan.

## ⚠️ PENJAGA — mcp-for-security sudah mati

> **cyproxio/mcp-for-security DIARSIPKAN Maret 2026 — JANGAN PAKAI; pakai bolt sebagai penggantinya.**

README repo lama itu sendiri menyatakan semua tool sudah dimigrasi ke Bolt. Jangan clone, install, atau jalankan `cyprox/mcp-for-security` dalam bentuk apa pun (repo, image Docker, maupun fork yang tidak terawat). Bila menemukan panduan lama yang masih mengarah ke mcp-for-security, ganti rujukannya ke Bolt.

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

- Apa yang dilakukan: baca aturan program target, catat domain/IP in-scope dan yang dilarang, catat apakah otomasi diizinkan.
- Standar lulus: target tertulis di catatan kerja; target DI LUAR scope = BERHENTI. Bila program melarang otomasi, skill ini TIDAK BOLEH dipakai untuk program itu.

### Gerbang 1 — Verifikasi repo sebelum install

- Apa yang dilakukan: buka https://github.com/cyberstrikeus/bolt, cek bintang, push terakhir, dan README; pastikan ini repo Bolt yang aktif (bukan arsip mcp-for-security).
- Standar lulus: repo masih aktif, README terbaca, tidak ada peringatan arsip. Bila repo mati/diarsipkan = BERHENTI dan laporkan ke Muse.

### Gerbang 2 — Instalasi Docker

- Apa yang dilakukan: ikuti README repo (Docker) untuk menarik dan menjalankan Bolt; jalankan hanya di container/VM yang bisa dibuang; jangan jalankan di mesin produksi atau mesin berisi data pribadi.
- Standar lulus: server Bolt merespons (`tools/list` mengembalikan 33 MCP tools); tidak ada error autentikasi/dependensi yang belum diselesaikan.

### Gerbang 3 — Pilih tool sesuai tugas (jangan borong)

- Apa yang dilakukan: dari 100+ tools yang tersedia, pilih hanya yang relevan dengan target (mis. nmap + ffuf untuk web, sqlmap untuk parameter yang dicurigai). Catat tool apa yang dipakai dan kenapa.
- Standar lulus: daftar tool yang dipakai tertulis sebelum eksekusi; tidak ada tool destruktif (hapus/timpa) yang dijalankan tanpa persetujuan manusia.

### Gerbang 4 — Eksekusi in-scope saja

- Apa yang dilakukan: jalankan tool yang dipilih terhadap target in-scope, satu per satu, dengan rate wajar.
- Standar lulus: semua trafik mengarah ke target in-scope; tidak ada trafik ke host lain; tidak ada tanda DoS. Output tiap tool disimpan mentah.

### Gerbang 5 — Validasi manual oleh manusia

- Apa yang dilakukan: A57 memeriksa tiap temuan secara manual dan mengulanginya sendiri. AI hanya merangkum; manusia yang memutuskan nyata vs false positive.
- Standar lulus: tiap temuan yang diteruskan punya bukti yang bisa diulang (perintah + output + tangkapan layar/transkrip). Temuan tanpa bukti = BUKAN temuan.

### Gerbang 6 — Laporan (hanya dengan persetujuan Cipta)

- Apa yang dilakukan: tulis draf laporan (lihat "Format output"), serahkan ke Muse → Cipta. Kirim HANYA setelah Cipta setuju.
- Standar lulus: laporan berisi scope, alat yang dipakai, bukti yang bisa diulang, dan dampak; tanpa klaim yang tidak dibuktikan di Gerbang 5.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| **Bolt** (Dockerized Kali, 100+ tools, 33 MCP tools) | https://github.com/cyberstrikeus/bolt (~60 bintang, baru) | Docker sesuai README; jalankan di container/VM sekali pakai |
| nmap, sqlmap, ffuf, nuclei, masscan | termasuk di Bolt | Scan/fuzzing target in-scope (Gerbang 4) |
| **JANGAN PAKAI: cyproxio/mcp-for-security** | https://github.com/cyproxio/mcp-for-security (DIARSIPKAN Maret 2026) | Dilarang — semua toolnya sudah pindah ke Bolt (lihat PENJAGA di atas) |
| SkillSpector (pemindai skill/MCP) | https://github.com/NVIDIA/SkillSpector | Pindai skill/MCP dari prompt injection sebelum install |

## Format output

Tulis log tiap sesi ke `~/workspace/catatan/log-bug-bounty.md` (tambahkan entri baru, jangan timpa log lama) dengan format:

```
Tanggal: <YYYY-MM-DD>
Program: <nama program bounty>
Target (in-scope): <domain/IP>
Alat: mcp-bolt — tool yang dipakai: <daftar>
Temuan: <ringkasan per temuan + bukti perintah/output>
Status: <RECON / SCAN / VALID / DRAF LAPORAN — menunggu persetujuan Cipta>
```

Draf laporan lengkap (scope, langkah, bukti, dampak) ditulis sebagai file terpisah di `~/workspace/catatan/` dan diserahkan ke Muse sebelum dikirim ke program. **Tidak ada laporan yang dikirim tanpa persetujuan Cipta.**

## Catatan yang belum terverifikasi

- Jumlah "100+ tools / 33 MCP tools" dan "~60 bintang" berasal dari artikel (per 23 Nov 2026); Bolt masih baru dan jumlahnya bisa berubah cepat — cek `tools/list` dan README saat instalasi pertama.
- Belum diuji: instalasi Docker Bolt, daftar tool persisnya, dan apakah Bolt jalan di VM Pusat Komando.
