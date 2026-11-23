# Skill: MITRE ATT&CK — Memetakan Taktik dan Teknik ke Temuan Bounty

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 8 (artikel Edoxi "12 Hacking Skills", No. 12) + batch 14 (artikel Coursera, Threat knowledge), 24 Nov 2026. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill PEMETAAN — memetakan tiap temuan/hypothesis ke taktik + teknik MITRE ATT&CK (dan, bila relevan, MITRE ATLAS untuk serangan terhadap agen AI) agar: (a) cakupan perburuan terlihat (taktik mana yang sudah diuji, mana yang belum); (b) laporan memakai bahasa standar yang dipahami triager; (c) celah cakupan ditemukan sebelum putaran berakhir. Skill ini BUKAN skill pengujian: tidak ada langkah menyerang di sini — pemetaan dilakukan ATAS temuan/hipotesis yang sudah ada.

## Pemicu

Dipakai setiap kali ada temuan kandidat yang perlu diklasifikasikan, dan secara berkala (tiap awal putaran) untuk memeriksa cakupan: taktik ATT&CK mana yang belum pernah diuji pada target in-scope. Dipakai SETELAH temuan tervalidasi (`skeptic-false-positive-eliminator`) dan SEBELUM triase (`triase-duplikat`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A61 Triage & Severity Analyst** | Memetakan temuan ke taktik + teknik ATT&CK; menyusun peta cakupan per putaran |
| Audit | **A60 Security Auditor** | Memvalidasi pemetaan (taktik/teknik yang dipilih harus cocok dengan bukti) |
| Pemimpin | **Muse** | Memutuskan taktik mana yang jadi prioritas putaran berikutnya |

## Sudah tercakup (jangan diduplikat)

- Pemetaan temuan ke framework (ATT&CK + NIST CSF + D3FEND + ATLAS) sebagai BAGIAN dari skill lain → skill `skill-cybersecurity-anthropic` (Gerbang 1). Skill ini adalah pemetaan ATT&CK yang MENDALAM dan BERKELANJUTAN (peta cakupan per putaran + prioritas taktik) — bukan sekadar satu gerbang klasifikasi.
- Klasifikasi severity temuan → skill `penilaian-cvss`. Skill ini memetakan TAKTIK/TEKNIK, bukan skor.
- Tren ancaman + TTP → skill `intelijen-ancaman-berkala`. Skill ini memakai TTP dari skill itu sebagai masukan pemetaan — bukan mengulang riset tren.
- Prioritas perburuan → skill `buru-bug-bounty` (induk). Skill ini memberi MASUKAN cakupan (taktik yang belum diuji) ke prioritas itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pemetaan tidak mengubah apa pun pada target — ini pekerjaan klasifikasi di atas kertas.
3. **Tanpa data orang lain.** Tanpa memakai data korban atau data pihak ketiga dalam pemetaan.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Pemetaan tidak mengirim request ke target.
6. **Tanpa payload di permukaan publik.** Peta cakupan + pemetaan temuan hanya di log internal dan jalur resmi program.
7. **Pemetaan harus cocok dengan bukti.** Jangan memaksakan teknik ATT&CK yang tidak didukung bukti temuan. Bila tidak ada teknik yang cocok, tulis "tidak terpetakan" — jangan mengarang.
8. **Validasi human-in-the-loop.** Setiap pemetaan harus diperiksa manusia (Muse/A60) sebelum masuk laporan.
9. **Tanpa laporan tanpa persetujuan Cipta.** Pemetaan ini bahan draf; Muse yang meneruskan ke Cipta.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG memakai pemetaan ATT&CK untuk merencanakan serangan di luar scope bounty. Pemetaan di sini HANYA untuk klasifikasi temuan dan perencanaan cakupan yang sah.

## Langkah + gerbang

### Gerbang 0 — Kenali taktik yang relevan dengan target

1. Dari 14 taktik ATT&CK Enterprise (Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact), tentukan mana yang RELEVAN dengan target in-scope dan programnya. Untuk target agen AI, tambahkan taktik MITRE ATLAS yang relevan.
2. **Standar lulus:** daftar taktik relevan tertulis + alasan. Taktik di luar scope program = dicoret dengan alasan.

### Gerbang 1 — Petakan tiap temuan ke teknik

1. Untuk tiap temuan kandidat, tentukan: taktik apa (mis. Credential Access) + teknik apa (mis. T1110 Brute Force — bila relevan dan terbukti) + sub-teknik bila ada. Cantumkan ID teknik + nama + bukti yang mendukung.
2. **Standar lulus:** tiap temuan punya taktik + teknik + ID + bukti — atau status "tidak terpetakan" dengan alasan. Pemetaan tanpa bukti = belum lulus.

### Gerbang 2 — Susun peta cakupan putaran

1. Buat matriks sederhana: taktik (baris) × status (sudah diuji / belum diuji / tidak relevan). Tandai taktik yang belum diuji tapi relevan — itu kandidat prioritas putaran berikutnya.
2. **Standar lulus:** matriks cakupan tertulis + daftar taktik belum diuji yang relevan. Tanpa matriks = cakupan tidak terlihat.

### Gerbang 3 — Prioritaskan taktik yang belum diuji

1. Urutkan taktik belum diuji berdasarkan: relevansi dengan target, apakah tekniknya diizinkan program, dan apakah ada skill pengujian yang cocok. Serahkan prioritas ke Muse untuk putaran berikutnya.
2. **Standar lulus:** daftar prioritas taktik tertulis + skill pengujian yang dituju per taktik. Prioritas tanpa skill tujuan = belum bisa dieksekusi.

### Gerbang 4 — Serahkan pemetaan ke triase

1. Serahkan pemetaan temuan (taktik + teknik + ID) ke `triase-duplikat` sebagai bagian dari paket triase. Skill ini BERHENTI di sini.
2. **Standar lulus:** pemetaan tercatat di log + masuk paket triase. Skill ini tidak mencatat "temuan" — hanya "pemetaan diserahkan".

## Alat

| Alat | Cara pakai |
|---|---|
| Matriks MITRE ATT&CK (Enterprise + ATLAS bila relevan) | Referensi taktik + teknik + ID — pakai versi terbaru yang diketahui |
| `intelijen-ancaman-berkala` | TTP tren sebagai masukan pemetaan |
| `penilaian-cvss` + `triase-duplikat` | Penerima pemetaan dalam paket triase |
| `~/workspace/catatan/log-bug-bounty.md` | Log pemetaan: temuan → taktik/teknik, matriks cakupan, prioritas |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal/putaran) dengan format:

```
Tanggal putaran: [YYYY-MM-DD]
Target + program: [nama — program]
Taktik relevan: [daftar + alasan — dicoret: ... + alasan]
Pemetaan temuan: [temuan ... — taktik ... — teknik ... (ID ...) — bukti: ...]
Matriks cakupan: [taktik ... — status: sudah/belum/tidak relevan]
Prioritas taktik belum diuji: [urutan #1, #2, ... — skill pengujian: ...]
Diserahkan ke triase: [ya/tidak]
Yang TIDAK dilakukan: [tanpa pengujian di skill ini, tanpa serangan di luar scope]
Status: [pemetaan selesai / prioritas diserahkan]
```

## Batasan yang diketahui

- ATT&CK disusun untuk serangan terhadap infrastruktur enterprise klasik — tidak semua tekniknya berlaku untuk target agen AI. Untuk target agen AI, utamakan MITRE ATLAS + teknik yang memang relevan; jangan memaksakan teknik enterprise ke temuan AI.
- Versi ATT&CK diperbarui berkala (teknik baru ditambah, lama diubah). Catat versi yang dipakai tiap putaran; pemetaan putaran lama bisa basi bila versinya berubah.
- Pemetaan yang salah (teknik tidak cocok dengan bukti) merusak kredibilitas laporan — bila ragu antara dua teknik, pilih yang buktinya paling kuat dan catat keraguannya, jangan menebak.
- Skill ini tidak membahas D3FEND (kontrol pertahanan) secara mendalam — lihat `kontrol-framework-keamanan` untuk kerangka kontrol. Bila laporan butuh pemetaan D3FEND, serahkan ke skill itu.
