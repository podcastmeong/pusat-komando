# Skill: Jalur Belajar Ethical Hacker — Kurikulum Maraton (Fondasi Berurutan, Bukan Sprint)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 6 + batch 7 (FAQ), 24 Nov 2026. Kurikulum ini belum pernah dijalani sampai tuntas oleh satu agent pun; label ini berlaku untuk semua bagian sampai ada satu agent yang menyelesaikan semua fase dan mencatatnya di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill kurikulum/metode — mengatur URUTAN BELAJAR agent bounty — BUKAN skill pengujian: skill ini tidak memberi langkah untuk menemukan atau mengeksploitasi kerentanan. Materi kursus/sertifikasi (mis. EC-Council, OWASP) disebut di sini HANYA sebagai rujukan jalur belajar, bukan sebagai isi skill — skill ini tidak mengajarkan materi sertifikasi dan tidak menjanjikan sertifikasi apa pun.

## Pemicu

Dipakai setiap kali agent baru bergabung ke tim bounty, setiap kali agent merasa mentok di satu teknik (tanda fondasi di bawahnya belum kuat), dan setiap kali tim memutuskan mempelajari teknologi baru. Dipakai juga saat menyusun rencana belajar mingguan tim. Bila agent sudah menguasai satu fase, skill ini cukup dipakai untuk memeriksa fase berikutnya — jangan mengulang fase yang sudah lulus.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Penjaga kurikulum | **Muse** | Menetapkan urutan fase, memutuskan agent lulus/tidak dari satu fase, menjaga agar tidak ada yang loncat fondasi |
| Pengerjaan | **A51–A70 (semua tim)** | Menempuh fase demi fase, mencatat kemajuan dan bukti kelulusan tiap fase di log |
| Audit | **A60 Security Auditor** | Memvalidasi bukti kelulusan fase (A60 tidak meluluskan dirinya sendiri) |
| Pemimpin | **Muse** | Memutuskan kapan tim siap naik ke program/target yang lebih berat |

## Sudah tercakup (jangan diduplikat)

- Jalur belajar TryHackMe (langkah platform spesifik) → skill `jalur-belajar-tryhackme`. Skill ini TIDAK mengulang langkah platform itu — skill ini mengatur URUTAN FASE UMUM; TryHackMe hanya salah satu lab di Fase 5.
- Kurikulum minggu pertama mobile → skill `kurikulum-minggu-pertama-mobile`. Skill itu khusus mobile; skill ini kurikulum umum ethical hacker.
- Lab spesifik (Hack The Box, PortSwigger, lab mobile) → skill `lab-hack-the-box`, `lab-portswigger-academy`, dan keluarga lab. Skill ini tidak mengulang isi lab — skill ini menempatkan lab pada urutan yang benar.
- Pemantauan CVE + kasus breach nyata → skill `pemantauan-cve-breach-nyata`. Skill ini menempatkannya sebagai Fase 7; mekanik pemantauannya tetap di skill itu.
- Pola pikir penyerang → skill `pola-pikir-penyerang-analitis`. Skill ini menempatkannya sebagai kemampuan yang diasah sepanjang fase, bukan fase tersendiri.
- Triad pemula (Networking, Linux CLI, keamanan web dasar) dan timeline 6–12 bulan berasal dari FAQ batch 7 — keduanya DILIPAT ke dalam skill ini (Fase 1–2–4 dan bagian Timeline), bukan skill terpisah.

## Prinsip maraton

1. **Berurutan, jangan loncat.** Fondasi harus dikuasai mendalam sebelum naik: networking → OS/Linux → programming → keamanan web → lab → metodologi → breach/CVE → bounty pemula. Loncat fondasi = rapuh di tengah jalan.
2. **Maraton, bukan sprint.** Fondasi (networking, Linux, dasar keamanan web) rata-rata butuh **6–12 bulan intensif** dari nol. Jadi profesional yang diakui butuh **beberapa tahun pengalaman nyata** (pentest + bug bounty). Tidak ada jalan pintas.
3. **Bukti kelulusan, bukan hafalan.** Satu fase lulus bila agent bisa MEMPRAKTIKKANNYA di lab, bukan bila agent bisa menghafal definisinya.
4. **Berhenti belajar = ketinggalan.** Teknik serangan baru muncul setiap hari; berhenti satu bulan saja sudah tertinggal jauh. Belajar tidak pernah selesai — Fase 7–8 berjalan selamanya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Latihan dan pengujian hanya di akun dan data milik sendiri, canary palsu, atau lab legal.
3. **Tanpa data orang lain.** Jangan menyentuh, menyimpan, atau memakai data pengguna lain selama belajar atau berlatih.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan atau akun yang bukan milik sendiri DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan, termasuk saat latihan.
6. **Tanpa payload di permukaan publik.** Materi belajar, catatan, dan draf jangan di-host atau dibagikan di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Latihan hanya di lab legal.** Jangan coba-coba di sistem orang lain. Lab yang sah: Hack The Box, TryHackMe, PortSwigger Academy, CTF, dan lab keluarga lab-* yang sudah ada.
8. **Validasi human-in-the-loop.** Kelulusan fase diputuskan Muse/A60, bukan oleh agent yang belajar itu sendiri.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data apa pun selama belajar atau berlatih — termasuk data lab milik sendiri di luar skenario lab itu. DILARANG memakai apa yang dipelajari untuk mengakses akun siapa pun atau memperoleh keuntungan di luar hadiah bounty resmi.

## Langkah + gerbang

### Fase 0 — Mindset (prasyarat semua fase)

1. Pahami: ethical hacker = kemampuan teknis tajam + mindset benar; pentest menuntut pemikiran analitis kreatif seperti penyerang; batas tegasnya adalah etika profesional dan izin (lihat skill `izin-tertulis-batas-legal`).
2. **Standar lulus:** agent bisa menjelaskan beda ethical hacker vs cyber criminal (izin + niat) tanpa membaca catatan.

### Fase 1 — Networking dulu (triad pemula #1)

1. Kuasai TCP/IP dan model OSI: beda data Layer 3 (IP) vs Layer 4 (TCP/UDP); cara kerja routing/switching, firewall, DNS, VPN, subnetting.
2. **Standar lulus:** agent bisa menjelaskan ke mana paket pergi dari komputer A ke server B dan di lapisan mana celah biasanya muncul; bisa memetakan subnet sederhana.

### Fase 2 — Linux + CLI (triad pemula #2)

1. Mahir command line Linux (Kali/Parrot sebagai kantor wajib); manajemen user + permission; file system dan proses; konfigurasi layanan (HTTP, SSH, FTP). Pahami juga dasar Windows + Active Directory.
2. **Standar lulus:** agent bisa menyelesaikan tugas audit dasar lewat CLI tanpa antarmuka grafis; bisa menjelaskan risiko permission yang terlalu longgar.

### Fase 3 — Programming dan scripting dasar

1. Pahami dasar scripting + logika pemrograman — tidak harus expert di semua bahasa. Python (automation, analisis malware, logika exploit) dan JavaScript (keamanan web) adalah bekal utama; tambah SQL dan Bash/PowerShell.
2. **Standar lulus:** agent bisa menulis skrip kecil untuk mengotomatisasi satu tugas repetitif dan menjelaskan logika exploit sederhana.

### Fase 4 — Dasar keamanan web (triad pemula #3)

1. Kuasai SQL Injection, XSS, CSRF, dan authentication bypass — cara kerja, bukan sekadar nama. Pahami OWASP Top 10 sebagai peta.
2. **Standar lulus:** agent bisa menjelaskan alur satu serangan web dasar dan di mana letak asumsi developer yang salah (lihat skill `pola-pikir-penyerang-analitis`).

### Fase 5 — Lab legal

1. Latihan di lab simulasi: Hack The Box, TryHackMe, PortSwigger Academy, CTF. Jangan coba di sistem orang lain.
2. **Standar lulus:** minimal satu lab/mesin selesai per minggu selama satu bulan, dengan catatan tertulis tentang apa yang dipelajari (bukan sekadar "selesai").

### Fase 6 — Kursus + metodologi

1. Ikuti kursus cybersecurity dasar yang fokus pada metodologi (berbasis standar EC-Council atau OWASP): kerangka berpikir profesional yang terstruktur + hukumnya. Metodologi pentest ujung-ke-ujung mengikuti skill `metodologi-pentest-ujung-ke-ujung`.
2. **Standar lulus:** agent bisa menjalankan satu pentest kecil mengikuti 5 tahap (recon → scanning → eksploitasi → eskalasi → reporting) di lab.

### Fase 7 — Baca breach nyata + CVE (berjalan selamanya)

1. Rutin membaca laporan kerentanan (CVE) dan case study data breach nyata; pahami bagaimana cyber criminal beroperasi. Mekaniknya mengikuti skill `pemantauan-cve-breach-nyata` dan `intelijen-ancaman-berkala`.
2. **Standar lulus:** agent bisa menyebutkan satu breach nyata dan celah yang dieksploitasi, serta apa yang seharusnya diperbaiki.

### Fase 8 — Bug bounty pemula (berjalan selamanya)

1. Ikut program bug bounty dengan target yang lebih ringan, legal dan etis — cara mendapat pengalaman nyata + potensi bayaran. Mulai dari program in-scope yang paling ringan; ikuti skill `buru-bug-bounty`.
2. **Standar lulus:** satu laporan triage-ready pertama (lolos atau tidak, yang dinilai adalah kualitas laporan dan kepatuhan scope).

## Timeline

| Tahap | Perkiraan |
|---|---|
| Fase 0–4 (fondasi) | 6–12 bulan intensif dari nol |
| Fase 5–6 (lab + metodologi) | 3–6 bulan setelah fondasi |
| Fase 7–8 (breach/CVE + bounty pemula) | Berjalan selamanya, bersamaan dengan fase lain |
| Profesional yang diakui | Beberapa tahun pengalaman nyata (pentest + bug bounty) |

## Alat

| Alat | Cara pakai |
|---|---|
| Lab legal (HTB, TryHackMe, PortSwigger, CTF) | Tempat latihan Fase 5–6 — satu-satunya tempat praktik sebelum bounty |
| Skill keluarga lab-* + `jalur-belajar-tryhackme` | Langkah platform spesifik per lab |
| Skill `pemantauan-cve-breach-nyata` + `intelijen-ancaman-berkala` | Mekanik Fase 7 |
| Skill `buru-bug-bounty` + `metodologi-pentest-ujung-ke-ujung` | Mekanik Fase 6 dan 8 |
| `~/workspace/catatan/log-bug-bounty.md` | Log kemajuan belajar + bukti kelulusan tiap fase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Agent: [A51–A70 / Muse]
Fase: [0–8 + nama fase]
Yang dipelajari: [satu baris — topik + sumber]
Bukti kelulusan: [apa yang dipraktikkan di lab — bukan hafalan]
Status: [LULUS — divalidasi Muse/A60 / BELUM — alasan]
Fase berikutnya: [nama fase]
```

## Batasan yang diketahui

- Timeline 6–12 bulan adalah rata-rata intensif, bukan janji. Agent yang belajar sambil mengerjakan tugas lain bisa lebih lambat — itu normal untuk maraton.
- Skill ini mengatur urutan belajar, bukan memberi nasihat karier. Permintaan global terhadap security professional memang naik (Cloud Security + AI), tetapi skill ini tidak menjanjikan pekerjaan atau penghasilan.
- Sertifikasi disebut hanya sebagai rujukan jalur belajar; skill ini tidak mengajarkan materi sertifikasi dan tidak menggantikan pelatihan formal.
- Bila agent mentok di satu fase lebih dari dua minggu, kembalikan ke fase di bawahnya — fondasinya yang belum kuat, bukan fasenya yang terlalu sulit.

### Available connectors

Tidak ada konektor khusus untuk skill ini; kemajuan belajar dicatat manual di log dan divalidasi Muse/A60.

### Websites

- Platform lab legal: Hack The Box, TryHackMe, PortSwigger Academy (sumber latihan Fase 5).
- Standar metodologi: OWASP dan EC-Council sebagai rujukan kerangka berpikir (hanya rujukan — bukan isi skill ini).

### Alternatives for better results

- Bila satu fase terasa terlalu besar, pecah jadi sub-fase kecil dengan standar lulus sendiri — maraton ditempuh selangkah demi selangkah.
- Bila agent sudah punya pengalaman di satu fase (mis. sudah mahir Linux), uji langsung lewat standar lulusnya — lulus berarti boleh loncat fase itu, tetapi keputusan loncat tetap di tangan Muse/A60.
- Belajar berkelompok (2–5 agent membahas satu breach nyata bersama) lebih efektif daripada belajar sendiri — pakai papan pesan antar-agent untuk diskusi.
