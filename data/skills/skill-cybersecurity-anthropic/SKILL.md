# Skill: Cybersecurity Anthropic Skills (mukul975) — Peta Temuan ke Framework Industri

> BELUM DIUJI — dibangun dari riset artikel "Top 43 AI Security Skills" (23 Nov 2026), bukan pengalaman teruji. Repo belum pernah di-clone tim; pemetaan framework di bawah ini diambil dari dokumentasi repo, belum dipraktikkan.

## Pemicu (kapan dipakai)

- Ada temuan (atau dugaan temuan) yang perlu dipetakan ke taktik/teknik standar industri supaya laporan bounty terlihat profesional dan mudah dinilai triaser.
- A60 butuh klasifikasi temuan: taktik MITRE ATT&CK apa, fungsi NIST CSF apa, dan kontrol D3FEND apa yang relevan.
- Ada insiden/jejak serangan (mis. pola prompt injection berulang) yang perlu dianalisis polanya dengan ATT&CK Navigator.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A60 Security Auditor** | Petakan temuan ke framework, tulis klasifikasi di draf laporan |
| Pendukung | **A58 Vulnerability Researcher** | Sediakan temuan + bukti untuk dipetakan |
| Pemimpin | **Muse** | Putuskan klasifikasi mana yang dipakai di laporan akhir |

## Sumber

- Repo: **mukul975/Anthropic-Cybersecurity-Skills** — https://github.com/mukul975/Anthropic-Cybersecurity-Skills (~33k bintang, lisensi Apache-2.0). Proyek komunitas, BUKAN afiliasi Anthropic PBC.
- Isi: 817 skill terstruktur (agentskills.io) di 34 domain keamanan.
- Pemetaan per skill ke 6 framework: MITRE ATT&CK (805 skill), NIST CSF 2.0 (804), MITRE D3FEND (139), NIST AI RMF (97), MITRE ATLAS (93), MITRE Fight Fraud Framework F3 (94).
- Instal: `npx skills add mukul975/Anthropic-Cybersecurity-Skills` atau `git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git`.
- Skill yang paling relevan untuk kita: yang memetakan serangan terhadap agen AI (MITRE ATLAS + NIST AI RMF), analisis APT dengan MITRE ATT&CK Navigator (`analyzing-apt-group-with-mitre-navigator`), dan deteksi pola serangan (ATT&CK TA0043 Reconnaissance, TA0005 Defense Evasion, TA0011 Command and Control — taktik yang dipakai serangan prompt injection tidak langsung).

## ATURAN KERAS

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu = JANGAN.
2. **Hanya akun sendiri + canary palsu.** Tidak ada akun orang lain, tidak ada data orang lain.
3. **Tanpa data orang lain.** Jangan pakai, jangan simpan, jangan sebar data milik orang lain.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.** Jangan membanjiri layanan apa pun.
6. **Tanpa payload di permukaan publik.** Jangan menaruh payload di tempat yang bisa dilihat/dipakai orang lain.
7. **Validasi human-in-the-loop.** AI bantu, manusia putuskan dan validasi — klasifikasi AI bukan klasifikasi sampai manusia memverifikasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Draf laporan boleh dibuat; kirim hanya setelah Cipta setuju.
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **Alat klasik (nmap, sqlmap, Burp, MCP recon) HANYA untuk program web klasik, bukan bounty agen AI.**
11. **Repo ini berisi skill ofensif/dual-use.** Pakai HANYA skill yang relevan dengan program in-scope; JANGAN load skill C2/phishing/exploitation yang tidak berhubungan dengan temuan kita. Baca dulu sebelum load (lihat skill `skill-skillspector` — pindai dulu sebelum install).

## Langkah + gerbang

### Gerbang 0 — Cek scope + pilih skill (standar lulus: program in-scope tertulis; nama skill yang dipakai tercatat)

1. Tulis program + target di `~/workspace/catatan/log-bug-bounty.md`.
2. Pilih SATU skill dari repo yang sesuai kebutuhan (mis. pemetaan ATT&CK untuk temuan injeksi). Jangan load seluruh 817 skill.

### Gerbang 1 — Petakan temuan (standar lulus: tiap temuan punya minimal 1 taktik ATT&CK + 1 fungsi NIST CSF yang benar)

1. Untuk tiap temuan terverifikasi: cari taktik/teknik ATT&CK yang cocok (mis. injeksi tak langsung → TA0001 Initial Access / TA0005 Defense Evasion — verifikasi nomor tekniknya di situs MITRE, jangan hafalan).
2. Tambah pemetaan NIST CSF 2.0 (Govern/Identify/Protect/Detect/Respond/Recover) dan, bila temuan menyangkut agen AI, MITRE ATLAS + NIST AI RMF.
3. Bila tidak ada pemetaan yang cocok → tulis "tidak ada pemetaan yang pas", jangan memaksakan.

### Gerbang 2 — Buat lapisan Navigator (bila relevan) (standar lulus: file layer JSON valid + bisa dibuka di ATT&CK Navigator)

1. Bila temuan membentuk pola/rantai (beberapa teknik sekaligus), buat layer ATT&CK Navigator (JSON) dari teknik-teknik itu.
2. Gunakan layer itu untuk analisis celah deteksi: teknik mana yang belum tertutup kontrol — tulis di draf laporan sebagai konteks, bukan sebagai temuan tambahan.

### Gerbang 3 — Verifikasi manusia (standar lulus: A60 memeriksa tiap pemetaan; yang salah diperbaiki, yang tidak yakin dihapus)

1. A60 cek ulang setiap ID teknik (ATT&CK v19: Defense Evasion TA0005 dipecah jadi Stealth + Impair Defenses — pakai versi terbaru).
2. Pemetaan yang salah = laporan terlihat tidak profesional; lebih baik sedikit tapi benar daripada banyak tapi salah.

### Gerbang 4 — Masukkan ke draf laporan (standar lulus: klasifikasi tercantum di draf, dengan sumber framework + versinya)

1. Tulis klasifikasi di draf laporan (format skill `laporan-abstrak`).
2. Sertakan versi framework yang dipakai (mis. ATT&CK v19.1, NIST CSF 2.0).

## Alat

| Alat | Repo / cara pakai |
|---|---|
| Anthropic-Cybersecurity-Skills (817 skill) | https://github.com/mukul975/Anthropic-Cybersecurity-Skills — `npx skills add mukul975/Anthropic-Cybersecurity-Skills` |
| MITRE ATT&CK Navigator | https://mitre-attack.github.io/attack-navigator/ — buka layer JSON hasil Gerbang 2 |
| mitreattack-python / attackcti / stix2 | `pip install mitreattack-python attackcti stix2` — query data ATT&CK secara programatik |
| SkillSpector (pindai dulu) | Lihat skill `skill-skillspector` — pindai skill dari repo ini SEBELUM load |

## Format output

- Log kerja: `~/workspace/catatan/log-bug-bounty.md` — baris per temuan: tanggal | program | temuan | ATT&CK (taktik + teknik) | NIST CSF | ATLAS/AI RMF (bila ada) | status verifikasi A60.
- Klasifikasi masuk ke draf laporan (skill `laporan-abstrak`); jangan kirim sebelum Cipta setuju.
- File layer Navigator (JSON) disimpan di folder kerja temuan yang bersangkutan, namanya dicatat di log.

## Batasan yang diketahui (BELUM DIUJI)

- Repo belum pernah di-clone/diuji tim; jumlah skill (817) dan pemetaan framework bisa berubah.
- Pemetaan framework repo ini dibuat untuk keamanan siber umum, bukan khusus bounty agen AI — sebagian besar dari 817 skill TIDAK relevan untuk program kita; pilih manual.
- Repo berisi teknik ofensif/dual-use — risiko salah pakai nyata; gerbang "baca dulu sebelum load" wajib.
