# Skill: Pengujian API SOAP/WSDL — Enumerasi operasi dari WSDL, otorisasi per operasi, dan injeksi pada pesan XML

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber riset: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, keluarga HACKING kandidat No. 73. Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bug bounty resmi: **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL, ANTH**. Skill ini untuk program web/API klasik; bukan untuk bounty agen AI kecuali scope program menyatakan berlaku.
Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila pengujian menyentuh area itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan. ViKernel: jalankan deteksi live-vs-recorded sebelum uji.

## Pemicu (kapan dipakai)

Dipakai saat target in-scope mengekspos API SOAP dengan dokumen WSDL — ada dugaan operasi sensitif bisa dipanggil tanpa otorisasi yang benar, atau pesan XML rentan injeksi.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + merancang langkah pengujian dan bukti |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Dokumentasi API/otorisasi endpoint → skill `dokumentasi-api-otorisasi-endpoint` (REST/OpenAPI; skill ini khusus SOAP/WSDL).
- Injeksi XXE → skill `injeksi-xxe` (XML; skill ini menguji operasi SOAP, bukan hanya parser XML).
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** — HUNTR, PPLX, MISTRAL, ANTH. Di luar program resmi atau di luar scope = jangan diuji.
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR, jangan dicoba.**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program — huntr "Humans only", Gray Swan dilewati total; jangan buat skill untuknya.**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data, sistem, atau layanan. Pembuktian HARUS aman, read-only, dan reversibel sebisa mungkin; bila satu-satunya pembuktian bersifat destruktif, serahkan ke Muse sebelum menguji.
11. **Scope guard kandidat:** Akun uji sendiri; tanpa menyentuh data pengguna lain.

## Langkah + gerbang

### Gerbang 0 — Cek scope + aturan program dulu

1. Baca pasal scope: apakah API SOAP ini in-scope? Catat aturan otomasi program.
2. **Standar lulus:** scope tercatat di log sebelum satu permintaan pun dikirim.

### Gerbang 1 — Enumerasi operasi dari WSDL

1. Unduh dan baca WSDL: daftar operasi, parameter, dan tipe datanya. Susun matriks otorisasi per operasi (operasi mana yang seharusnya butuh autentikasi/peran tertentu).
2. **Standar lulus:** daftar operasi + matriks otorisasi tertulis. Tanpa matriks = jangan menguji acak.

### Gerbang 2 — Uji otorisasi per operasi

1. Panggil tiap operasi sensitif dengan akun uji sendiri TANPA token, lalu dengan akun uji berperang rendah; bandingkan dengan perilaku yang seharusnya.
2. Catat operasi mana yang merespons data/aksi tanpa otorisasi yang benar — hanya data milik akun sendiri yang dipakai.
3. **Standar lulus:** hasil per operasi tercatat (ditolak/diterima + peran yang dipakai). Operasi yang ditolak dengan benar = AMAN.

### Gerbang 3 — Uji injeksi pada pesan XML

1. Pada operasi yang menerima input, uji karakter XML dan pola injeksi (bukan XXE destruktif) dengan nilai canary milik sendiri; amati error atau perubahan perilaku.
2. **Standar lulus:** hasil uji injeksi tercatat; tanpa membaca data pengguna lain.

### Gerbang 4 — Serahkan ke triase

1. Serahkan bukti (operasi yang lolos otorisasi / injeksi yang terbukti) ke A60 audit → draf laporan → Cipta setuju → kirim.
2. **Standar lulus:** ada bukti reproduksi + keputusan triase tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| curl / klien SOAP (SoapUI atau skrip) | Panggil operasi SOAP dengan variasi otorisasi |
| Pembaca WSDL | Enumerasi operasi dan parameter |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua langkah + hasil + keputusan triase |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pengujian-api-soap-wsdl] — No. 73
Program: [HUNTR, PPLX, MISTRAL, ANTH]
Target: [program + aset/endpoint/aplikasi yang diuji]
Hipotesis: [Operasi SOAP in-scope bisa dipanggil tanpa otorisasi yang benar, atau pesan XML-nya rentan injeksi.]
Langkah: [gerbang yang dilalui + hasil tiap gerbang]
Bukti: [bukti read-only / hasil lab / tangkapan yang relevan]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Hanya akun uji sendiri; jangan memanggil operasi yang mengubah/menghapus data pengguna lain.
- Jangan memakai XXE untuk membaca file server atau SSRF internal; uji injeksi sebatas perilaku respons.
- Operasi yang mengubah state hanya diuji dengan data milik sendiri dan nilai canary yang reversibel.
