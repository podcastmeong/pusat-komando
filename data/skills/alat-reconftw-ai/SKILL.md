# Skill: Alat ReconFTW-AI — JANGAN PAKAI (Skill Penjaga)

> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Skill ini ditulis dari ringkasan artikel "Top 43 AI Security Skills" (14 Sep 2026, diringkas 23 Nov 2026). Skill ini adalah SKILL PENJAGA: tujuannya mencegah pemakaian alat yang sudah STALLED, bukan mengajarkan cara memakainya.

## Kapan dipakai (pemicu)

- Saat ada yang mengusulkan memakai reconftw_ai, atau saat muncul rencana recon yang mengandalkan LLM lokal di atas reconftw.
- Saat tim menilai alat recon baru dan perlu memeriksa apakah reconftw_ai masih hidup.
- Saat ada keraguan: "apakah reconftw_ai masih bisa dipakai?"

## Pemilik

**A70 Automation Engineer** — memverifikasi status repo secara berkala dan menegakkan keputusan JANGAN PAKAI. A70 TIDAK boleh membalikkan keputusan ini sendiri; perubahan status hanya oleh Muse atas bukti repo aktif kembali.

## Tentang alat ini — kenapa JANGAN PAKAI

- **Nama:** reconftw_ai
- **Pembuat:** six2dez
- **Bintang GitHub:** ~100 (per Sep 2026)
- **Ide:** benar — LLM lokal di atas reconftw untuk interpretasi hasil per kategori.
- **Status: STALLED — JANGAN PAKAI.** Push terakhir sudah lebih dari setahun lalu (per Sep 2026). Awasi saja, jangan bangun rencana di atasnya.
- **Keputusan:** JANGAN PAKAI reconftw_ai. Jangan install, jangan jadikan andalan, jangan bangun alur kerja di atasnya. Alat yang tidak dirawat bisa berisi dependensi kedaluwarsa, bug yang tidak diperbaiki, dan perilaku yang tidak lagi cocok dengan target saat ini.

## Pengganti yang dipakai

| Kebutuhan | Pengganti | Catatan |
|---|---|---|
| Recon klasik (subdomain, port, direktori, dsb.) | reconftw klasik (six2dez/reconftw) | Repo utama yang aktif dan terawat — pakai ini, bukan varian _ai-nya |
| Interpretasi hasil recon dengan LLM | mcp-osint | MCP server OSINT untuk memberi agen "tangan" menginterpretasi hasil; pakai sesuai dokumentasi konektornya |
| Gabungan keduanya | reconftw klasik + mcp-osint | Alur: reconftw klasik mengumpulkan hasil → mcp-osint / agen membantu menafsirkan per kategori, dengan validasi manusia |

## Aturan keras

1. Hanya program bounty resmi in-scope (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. Hanya akun sendiri + canary palsu.
3. Tanpa data orang lain.
4. Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).
5. Tanpa DoS/DDoS.
6. Tanpa payload di permukaan publik.
7. Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).
8. Tanpa laporan tanpa persetujuan Cipta.
9. Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **JANGAN install, JANGAN jalankan, JANGAN jadikan andalan reconftw_ai** — sampai ada keputusan tertulis Muse yang membalikkan status ini berdasarkan bukti repo aktif kembali.
11. Bila ada agent lain yang mengusulkan reconftw_ai, tunjukkan skill ini dan arahkan ke pengganti di atas.

## Langkah verifikasi status repo + keputusan pakai/jangan

### Gerbang 1 — Cek status repo (tiap pemantauan)

- **Lakukan:** buka repo GitHub reconftw_ai (six2dez/reconftw_ai), catat tanggal push terakhir, rilis terakhir, dan isu terbuka.
- **Standar lulus (untuk tetap diawasi):** repo tercatat, tanggal push terakhir dicatat di log. **Standar untuk MEMAKAI: tidak ada** — status saat ini tetap JANGAN PAKAI apa pun hasil gerbang ini, kecuali gerbang 4 terpenuhi.

### Gerbang 2 — Bandingkan dengan pengganti

- **Lakukan:** periksa apakah reconftw klasik masih aktif dan apakah mcp-osint masih tersedia. Catat versi keduanya.
- **Standar lulus:** pengganti (reconftw klasik + mcp-osint) tersedia dan aktif. Bila pengganti juga bermasalah: laporkan ke Muse, jangan kembali ke reconftw_ai sebagai jalan pintas.

### Gerbang 3 — Keputusan pakai/jangan (tiap pemantauan)

- **Lakukan:** berdasarkan gerbang 1, putuskan: (a) repo masih STALLED (>1 tahun tanpa push) → keputusan tetap JANGAN PAKAI; (b) repo aktif kembali (push/komit baru yang substansial) → laporkan ke Muse untuk penilaian ulang, TETAP JANGAN PAKAI sampai ada keputusan tertulis.
- **Standar lulus:** keputusan tercatat di log beserta tanggal push terakhir yang ditemukan. Tidak ada pemakaian tanpa keputusan tertulis Muse.

### Gerbang 4 — Pembalikan status (hanya bila repo hidup kembali)

- **Lakukan:** bila repo menunjukkan aktivitas substansial berkelanjutan (beberapa push/rilis dalam 3 bulan, isu dijawab), A70 melaporkan bukti itu ke Muse. Muse yang memutuskan apakah status berubah dari JANGAN PAKAI menjadi PANTAU — dan bila berubah, skill ini ditulis ulang sebagai skill pantau biasa dengan gerbang uji.
- **Standar lulus:** ada keputusan tertulis Muse. Tanpa itu, status tetap JANGAN PAKAI.

## Status pemantauan — apa yang dipantau

| Yang dipantau | Sinyal yang dicatat |
|---|---|
| Tanggal push terakhir reconftw_ai | Apakah sudah ada aktivitas baru setelah >1 tahun diam |
| Rilis / komit baru | Apakah perubahannya substansial atau hanya kosmetik |
| Status pengganti (reconftw klasik + mcp-osint) | Apakah pengganti tetap aktif dan bisa dipakai |

**Skill ini berubah status hanya bila:** gerbang 4 terpenuhi (repo aktif kembali secara substansial) DAN Muse memutuskan tertulis. Sampai saat itu, reconftw_ai tetap JANGAN PAKAI.

## Alat

| Alat | Repo | Cara pakai |
|---|---|---|
| reconftw_ai | GitHub: six2dez/reconftw_ai | JANGAN PAKAI — hanya dipantau status repo-nya (baca halaman repo, jangan install). |
| reconftw klasik (pengganti) | GitHub: six2dez/reconftw | Pakai ini untuk recon klasik, mengikuti dokumentasi resmi repo. |
| mcp-osint (pengganti) | Lihat dokumentasi konektor MCP OSINT | Pakai ini untuk interpretasi hasil recon, mengikuti dokumentasi konektornya. |

## Format output

- **Log pemantauan** ke `~/workspace/catatan/log-bug-bounty.md` — satu baris per pengecekan: tanggal, tanggal push terakhir reconftw_ai, keputusan (TETAP JANGAN PAKAI / LAPORKAN KE MUSE UNTUK PENILAIAN ULANG), dan status pengganti.
- **Bila ada yang mengusulkan memakai reconftw_ai:** jawab dengan merujuk skill ini + arahkan ke pengganti (reconftw klasik + mcp-osint), dan catat usulan itu di log.
- **Laporan temuan bounty** mengikuti alur biasa: draf oleh A70 → Muse putuskan → Cipta setuju → baru dikirim. Tanpa persetujuan Cipta, tidak ada laporan yang dikirim.
