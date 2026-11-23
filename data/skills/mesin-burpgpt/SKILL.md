# Skill: Mesin BurpGPT — JANGAN PAKAI (Skill Penjaga)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini disusun dari ringkasan artikel "Top 43 AI Security Skills" (23 Nov 2026) dan belum pernah dijalankan di Pusat Komando. Skill ini adalah **skill penjaga**: tujuannya mencegah pemakaian, bukan mengajarkan pemakaian.

## Pemicu + pemilik

- **Dipakai saat:** ada yang mengusulkan memakai burpgpt, atau burpgpt muncul di daftar/rekomendasi mana pun — skill ini dipakai untuk MEMBATALKAN usulan itu dengan alasan yang tercatat.
- **Pemilik:** **A64 Web Application Tester** (memverifikasi status repo + menegakkan larangan; keputusan akhir tetap manusia).
- **Pemimpin:** **Muse** (memutuskan bila ada yang memohon pengecualian — default: tidak ada pengecualian).

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| burpgpt (YANG DILARANG) | github.com/aress31/burpgpt (~2.4k ⭐) | **JANGAN INSTALL. JANGAN JALANKAN.** Repo ini hanya dibuka untuk verifikasi status (lihat langkah 1–2) |
| Pengganti: mcp-burp-official | PortSwigger official mcp-server (~1.2k ⭐) | Mulai dari sini bila butuh integrasi Burp + LLM — server MCP resmi PortSwigger |
| Pengganti lain (bila perlu) | BurpMCP-Ultra / Cy-S3c (~220 ⭐, ~150 tools, Burp Pro); BurpMcp / swgee (~60 ⭐); burp-mcp-agents / six2dez (~230 ⭐, panduan wiring + template IDOR/SSRF/auth) | Pilih sesuai kebutuhan; masing-masing tetap harus dipindai sebelum dipakai |

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr.
2. **Hanya akun sendiri + canary palsu; tanpa data orang lain.**
3. **Tanpa uji korban** — victim-agent fraud tests DIBLOKIR, jangan dicoba.
4. **Tanpa DoS/DDoS.**
5. **Tanpa payload di permukaan publik.**
6. **Validasi human-in-the-loop** — AI bantu, manusia putuskan dan validasi.
7. **Tanpa laporan tanpa persetujuan Cipta.**
8. **Patuhi larangan otomasi program** — huntr "Humans only"; Gray Swan dilewati total, jangan buat skill untuknya.
9. **Framework otonom di kategori ini HANYA untuk target in-scope dan HANYA dengan human-in-the-loop — jangan biarkan framework jalan sendiri tanpa pengawasan; untuk bounty agen AI, framework klasik ini hanya relevan bila targetnya program web klasik.**
10. **Larangan khusus skill ini: JANGAN INSTALL DAN JANGAN JALANKAN burpgpt dalam keadaan apa pun.** Usulan memakai burpgpt WAJIB dijawab dengan skill ini + diarahkan ke pengganti di atas.

## Alasan: kenapa JANGAN PAKAI burpgpt

1. **MATI — push terakhir Juni 2024.** Repo tidak diperbarui sejak Juni 2024; tidak ada perbaikan bug, tidak ada penyesuaian terhadap perubahan API Burp maupun model LLM.
2. **README-nya sendiri mengakui Community edition ditinggalkan.** Proyek ini secara terbuka menyatakan edisi Community tidak lagi diteruskan — memakai alat yang ditinggalkan pembuatnya sendiri berarti memakai alat tanpa dukungan dan tanpa perbaikan keamanan.
3. **Masih muncul di banyak daftar.** Angka ~2.4k ⭐ dan kemunculannya di banyak daftar/rekomendasi membuat orang mengira alat ini masih hidup. Itulah alasan skill penjaga ini ada: bintang dan daftar bukan bukti alat masih terawat.
4. **Risiko keamanan:** alat mati yang terhubung ke Burp (yang menyimpan histori request/response) dan ke LLM adalah risiko supply-chain — tidak ada yang menambal celah bila ditemukan.

## Langkah + gerbang (langkah verifikasi status repo + keputusan pakai/jangan)

1. **Gerbang 1 — Verifikasi status repo.** Buka github.com/aress31/burpgpt dan cek: tanggal push/commit terakhir, isi README (apakah masih menyatakan Community edition ditinggalkan), dan issue/PR terbuka. Standar lulus: tanggal push terakhir + pernyataan README tercatat di log dengan tanggal verifikasi.
2. **Gerbang 2 — Bandingkan dengan pengganti.** Cek status mcp-burp-official (PortSwigger) — apakah masih aktif diperbarui. Standar lulus: status pengganti tercatat; pengganti harus lebih aktif daripada burpgpt.
3. **Gerbang 3 — Keputusan.** Bila burpgpt masih mati (push terakhir Juni 2024 atau tidak ada tanda hidup kembali) → keputusan: **JANGAN PAKAI**, arahkan ke mcp-burp-official. Bila suatu hari repo hidup kembali (push baru + README diperbarui + ada rilis) → JANGAN langsung pakai; laporkan ke Muse dan minta evaluasi ulang skill ini. Standar lulus: keputusan tertulis di log; tidak ada instalasi burpgpt dalam keadaan apa pun tanpa evaluasi ulang yang disetujui Muse.
4. **Gerbang 4 — Bila ada yang tetap mengusulkan burpgpt.** Tunjukkan skill ini + hasil verifikasi gerbang 1–3, lalu tawarkan pengganti. Standar lulus: usulan dibatalkan atau dialihkan ke pengganti; bila pemohon tetap memaksa, eskalasi ke Muse — jangan instal diam-diam.

## Format output

- Log verifikasi ke `~/workspace/catatan/log-bug-bounty.md` (tanggal verifikasi, push terakhir burpgpt, isi pernyataan README, status mcp-burp-official, keputusan: JANGAN PAKAI / EVALUASI ULANG).
- Bila usulan pemakaian dibatalkan: catat siapa yang mengusulkan, kapan, dan pengganti apa yang dipakai.
- Verdict: `JANGAN PAKAI (terverifikasi mati)` / `EVALUASI ULANG (tanda hidup kembali — butuh persetujuan Muse)`.

## Catatan

- Skill penjaga ini sengaja dibuat dengan struktur yang sama seperti skill lain supaya mudah ditemukan saat seseorang mencari "burp" di daftar skill — dan langsung menemukan larangan, bukan tutorial.
- Pola yang sama berlaku untuk alat mati lain di referensi (cyproxio/mcp-for-security diarsipkan Maret 2026; Nmap MCP server diarsipkan; reconftw_ai STALLED) — bila salah satunya diusulkan, buat skill penjaga yang sama sebelum ada yang menginstalnya.
