# Skill: Serangan vCenter & VPN Enterprise — Fingerprinting dan Eksploitasi Kerentanan Spesifik Perangkat Jaringan Korporat

> Dibangun dari riset keenam "Skill Langka AI Agent untuk Bug Bounty" (24 Nov 2026, `~/workspace/catatan/referensi-skill-langka-bug-bounty-2026-11-24.md`, Kategori 3 — Rantai Pasok & Infrastruktur Enterprise).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata per kategori yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat program bounty enterprise in-scope secara eksplisit mencantumkan perangkat jaringan korporat (VMware vCenter, Citrix NetScaler/ADC, Ivanti/Pulse Secure, Fortinet FortiGate, Palo Alto GlobalProtect, atau perangkat sejenis milik target) dan ada hipotesis: perangkat itu bisa dikenali versinya dari luar (fingerprinting) lalu cocok dengan kerentanan spesifik yang diketahui (CVE) dan bisa dibuktikan dampaknya secara aman. Dipakai sesudah fondasi (`fondasi-kerentanan-web-api`) dikuasai — skill ini hanya menambah kategori perangkat jaringan enterprise, bukan menggantikannya. Perangkat ini sering terlewat dari pemindaian aplikasi web biasa karena bukan aplikasi web umum — justru itu celahnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan fingerprinting + pembuktian CVE pada perangkat uji / lab milik sendiri |
| Pengerjaan | **A59 Threat Hunter** | Korelasi versi perangkat dengan CVE (CVSS/EPSS/KEV) |
| Audit | **A60 Security Auditor** | Memeriksa apakah pembuktian dampak tiap temuan memenuhi standar lulus kategori itu |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Recon jaringan umum + intel CVE via Shodan/CVEDB (IP lookup, pencarian perangkat, CVSS/EPSS/KEV) → `mcp-shodan`. Skill ini beda: fingerprinting + pembuktian kerentanan SPESIFIK per produk (vCenter, Citrix, Ivanti/Pulse, Fortinet, GlobalProtect) — bukan query Shodan umum.
- Pemetaan permukaan serangan (inventaris aset/endpoint, port scanning dalam scope) → `pemetaan-permukaan-serangan`. Skill ini memakai indeksnya sebagai masukan, bukan mengulanginya.
- Scan aktif ringan (nmap, nuclei, ffuf) → `mcp-security-hub`. Skill ini beda: template/cek yang ditargetkan ke SATU produk enterprise + standar pembuktian dampaknya — bukan scan generik.
- Validasi temuan + laporan triage-ready → `triase-duplikat` + `laporan-abstrak`.
- Penilaian severity → `penilaian-cvss`.

## Trigger & Scope

**Trigger (skill aktif bila SEMUA terpenuhi):**
1. Program bounty enterprise resmi dan perangkat jaringannya tercantum eksplisit di scope program (nama produk + IP/domain perangkat target).
2. Ada sinyal awal: port/layanan khas perangkat terlihat di indeks `pemetaan-permukaan-serangan` (mis. 443 dengan banner/sertifikat khas, path khas seperti `/ui/`, `/dana-na/`, `/remote/login`, portal VPN), atau CVE baru untuk produk itu baru diumumkan.
3. Agen sudah punya lab/perangkat uji milik sendiri (VM/appliance versi yang sama, atau replika layanan) untuk pembuktian — atau setidaknya satu perangkat uji untuk membandingkan baseline.

**Scope (yang BOLEH diuji):** hanya perangkat (IP/domain + produk) yang TERCANTUM di scope program. **Yang TIDAK BOLEH:** infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali — dilarang memindai/menguji perangkat VPN/vCenter/cloud milik pihak ketiga di luar scope.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Target di luar scope = BERHENTI.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik**; satu perangkat, satu cek, satu waktu — jangan membanjiri perangkat (perangkat VPN/vCenter mudah kewalahan; banjir = DoS).
4. **Tanpa payload di permukaan publik.** Payload pembuktian hanya di lab/perangkat uji milik sendiri.
5. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
6. **Tanpa laporan tanpa persetujuan Cipta.**
7. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
8. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only.
9. **Teknik ini untuk program enterprise klasik, BUKAN untuk bounty agen AI** (Muse, OpenAI, 0din, Google AI VRP, ViKernel — di sana yang dinilai hasil/outcome agen, bukan perangkat jaringan).
10. **BATASAN KHUSUS KATEGORI 3 — WAJIB:** kategori ini HANYA untuk program enterprise yang secara eksplisit in-scope (program bounty enterprise dengan aset infrastruktur tercantum). Infrastruktur perusahaan yang tidak tercantum di scope program TIDAK BOLEH diuji sama sekali; dilarang memindai/menguji perangkat VPN/vCenter/cloud milik pihak ketiga di luar scope.
11. **Pembuktian eksploitasi HANYA di lab milik sendiri.** Replikasi layanan perangkat target (versi yang sama) di VM/lab milik sendiri, buktikan CVE di sana, lalu laporkan pola + bukti replikasi — JANGAN menjalankan payload eksploitasi terhadap perangkat target yang sebenarnya. Terhadap perangkat target: HANYA fingerprinting pasif (banner, header, sertifikat, halaman login) + SATU request pembuktian baca-saja bila program mengizinkan dan risikonya sudah dinilai A60 (mis. request yang hanya membuktikan versi/path rentan merespons, tanpa mengubah state).
12. **JANGAN memakai kredensial bocor / mencoba login dengan kredensial apa pun selain akun uji milik sendiri.** Bila fingerprinting menemukan portal login, JANGAN brute-force — catat saja keberadaan + versinya.
13. **Tidak ada laporan tanpa bukti dampak.** Temuan yang hanya "versi cocok dengan CVE" tanpa pembuktian dampak = belum terbukti, tidak maju ke triase.
14. **Jangan membesar-besarkan severity.** Nilai dampak apa adanya (pakai `penilaian-cvss`); triase yang menentukan tier hadiah.

## Methodology & Payloads

### 1. Fingerprinting Perangkat Enterprise (kenali produk + versi dari luar)

- **Definisi:** mengenali produk dan versi perangkat dari respons yang memang terekspos publik — banner HTTP, header `Server`, sertifikat TLS (issuer/subject), halaman login khas, path khas, dan favicon/JS khas — tanpa login dan tanpa payload.
- **Cara mengenali (per produk — pola umum, cek dokumentasi produk sebelum menyimpulkan):**
  - **VMware vCenter:** halaman `/ui/` + header/sertifikat khas vCenter; endpoint API `/api/` merespons tanpa kredensial dengan info versi.
  - **Citrix NetScaler/ADC:** path `/vpn/` + header `NSC_*` / cookie `NSC_*`; halaman login khas NetScaler Gateway.
  - **Ivanti/Pulse Secure:** path `/dana-na/` + cookie `DSID`; halaman login Pulse Connect Secure khas.
  - **Fortinet FortiGate:** halaman `/remote/login` + header/cookie khas FortiOS; sertifikat self-signed Fortinet.
  - **Palo Alto GlobalProtect:** portal `/global-protect/` + header khas; halaman login GlobalProtect.
- **Pola pengujian (pasif, read-only):**
  1. Satu request `GET` ke halaman utama/path khas + baca header + sertifikat TLS (pakai `curl -k -s -D - -o /dev/null https://<target>/` dan `openssl s_client`, atau `mcp-shodan` `ip_lookup` untuk data yang sudah terkumpul).
  2. Catat: produk yang diduga + versi bila terlihat + sumber tiap petunjuk (header/banner/path/sertifikat).
  3. Bila versi TIDAK terlihat: catat sebagai "produk teridentifikasi, versi tidak terungkap" — jangan memaksa dengan fuzzing agresif.
- **Standar lulus:** ada bukti header/banner/sertifikat/path yang menunjukkan produk (+ versi bila ada) + tanggal pengecekan. Sekadar "port 443 terbuka" tanpa petunjuk produk = belum teridentifikasi.

### 2. Korelasi Versi → CVE Spesifik (A59)

- **Definisi:** mencocokkan versi perangkat yang teridentifikasi dengan CVE yang diketahui untuk produk itu (mis. RCE/auth-bypass pada vCenter, Ivanti, Fortinet, Citrix, GlobalProtect) beserta skor CVSS, EPSS, dan status KEV (diketahui dieksploitasi di alam liar).
- **Cara mengenali:** pakai `mcp-shodan` (`cve_lookup`, `cves_by_product` — gratis, CVEDB) + basis data CVE resmi: cari CVE untuk produk + versi yang teridentifikasi; prioritaskan yang berstatus KEV dan berdampak RCE/auth-bypass/SSRF.
- **Pola pengujian:**
  1. Untuk tiap CVE kandidat, catat: CVE ID + versi yang terdampak + CVSS + EPSS + status KEV + kondisi yang dibutuhkan (mis. endpoint tertentu harus ada, autentikasi tidak diperlukan).
  2. Cek kondisi itu dari luar secara pasif (apakah endpoint/path yang disebut di CVE memang ada di perangkat target — satu request `GET` status saja).
  3. Bila kondisi terpenuhi, lanjut ke kategori 3 (pembuktian di lab). Bila tidak terpenuhi, coret dengan alasan.
- **Standar lulus:** tiap klaim CVE punya pasangan (CVE + versi perangkat yang terdampak + skor + kondisi yang terpenuhi). CVE tanpa versi perangkat yang cocok = BELUM TERBUKTI, jangan diteruskan.

### 3. Pembuktian Kerentanan Spesifik di Lab (A57 — HANYA lab milik sendiri)

- **Definisi:** membuktikan CVE yang berkorelasi itu benar-benar berdampak — di REPLIKA perangkat (VM/appliance versi sama di lab milik sendiri), bukan di perangkat target.
- **Pola pengujian (AMAN — lab milik sendiri):**
  1. Bangun replika: instal/konfigurasi perangkat versi yang sama di lab milik sendiri (VM/appliance uji, tanpa data siapa pun).
  2. Baseline dulu: perilaku normal replika (endpoint merespons normal, login uji bekerja, tidak ada akses tanpa kredensial).
  3. Jalankan pola pembuktian CVE di replika — pola umum per jenis dampak:
     - **Auth bypass:** akses endpoint yang seharusnya butuh login TANPA kredensial di replika; bukti = respons berisi data/fungsi yang seharusnya terproteksi.
     - **SSRF / path traversal:** minta replika mengambil/menampilkan resource internal CANARY milik sendiri (file/URL canary di lab sendiri); bukti = isi canary muncul di respons / hit canary tercatat.
     - **RCE (pembuktian aman):** perintah baca-saja di replika (mis. `id` / `echo CANARY-<acak>`) — bukti = output perintah muncul; JANGAN perintah yang mengubah/menghapus data, JANGAN reverse shell, JANGAN eksfiltrasi.
  4. Ulangi dari state bersih minimal 1 kali.
- **Standar lulus:** ada bukti baseline vs exploit di replika (respons sebelum/sesudah + pengulangan dari state bersih) + CVE yang berkorelasi + bukti perangkat target punya versi + kondisi yang sama (dari kategori 1–2). Sekadar "CVE cocok dengan versi" tanpa pembuktian di replika = belum terbukti. **DILARANG keras:** menjalankan pola di atas terhadap perangkat target yang sebenarnya.

## Validation Gate (verifikasi deterministik — baseline vs exploit)

Sebelum menyimpulkan adanya kerentanan, WAJIB lolos gerbang ini per temuan:

1. **Baseline:** catat perilaku normal DULU — di replika lab: endpoint terproteksi menolak akses tanpa kredensial (401/403/redirect login); di perangkat target: hanya fingerprinting pasif (produk + versi + status path). Simpan output baseline dengan tanggal.
2. **Exploit (lab milik sendiri):** jalankan pola kategori 3 di replika — akses tanpa kredensial berhasil / canary SSRF muncul / output perintah baca-saja muncul. Simpan output exploit dengan tanggal.
3. **Perbandingan:** baseline vs exploit harus BERBEDA pada tepat satu variabel (ada/tidaknya kredensial / URL canary / payload pembuktian). Bila baseline sudah "terbuka" tanpa payload, temuan itu artefak konfigurasi lab — ulangi dari replika bersih.
4. **Pengulangan:** ulangi exploit dari replika bersih minimal 1 kali; hasil yang sama = deterministik, boleh maju. Sekali berhasil tanpa pengulangan = belum terbukti.
5. **Human-in-the-loop:** A57 + A60 memeriksa baseline vs exploit sebelum draf laporan. Temuan yang gagal di gerbang mana pun = DITOLAK dengan alasan, dicatat di log.

## Langkah + gerbang

### Gerbang 0 — Cek scope enterprise dulu (standar lulus: program + perangkat tercantum tertulis di log sebelum fingerprinting dimulai)

1. Tulis di `~/workspace/catatan/log-bug-bounty.md`: program, perangkat in-scope (produk + IP/domain), dan batas yang berlaku.
2. Bila perangkat TIDAK tercantum eksplisit di scope → BERHENTI. Jangan fingerprinting.

### Gerbang 1 — Fingerprinting pasif (standar lulus: produk teridentifikasi + versi bila terlihat, masing-masing dengan bukti header/banner/sertifikat)

1. Jalankan pola kategori 1 (satu request per path khas, maks 5 req/detik) pada perangkat in-scope saja.
2. Serahkan hasil ke indeks `pemetaan-permukaan-serangan`.

### Gerbang 2 — Korelasi CVE (standar lulus: tiap CVE kandidat punya pasangan CVE + versi + skor + kondisi)

1. A59 menjalankan pola kategori 2 (`mcp-shodan` CVEDB + basis data CVE resmi).
2. CVE tanpa versi yang cocok = dicoret dengan alasan; yang lolos lanjut ke Gerbang 3.

### Gerbang 3 — Buktikan di lab (standar lulus: lolos Validation Gate di atas)

1. A57 menjalankan pola kategori 3 HANYA di lab milik sendiri.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** keputusan triase tercatat di log dengan alasan.

## Alat

| Alat | Cara pakai |
|---|---|
| `curl` / `openssl s_client` | Fingerprinting pasif: header, banner, sertifikat TLS (Gerbang 1). |
| `mcp-shodan` (`ip_lookup`, `cve_lookup`, `cves_by_product`) | Intel CVE + data perangkat yang sudah terkumpul (Gerbang 2). |
| `mcp-security-hub` (nuclei — template produk spesifik) | HANYA template yang ditargetkan ke produk in-scope, di lab dulu; JANGAN scan generik ke perangkat target. |
| Lab/VM milik sendiri (replika perangkat versi sama) | Wajib untuk pembuktian CVE (Gerbang 3). |
| `penilaian-cvss` | Nilai severity temuan yang terbukti. |
| `~/workspace/catatan/log-bug-bounty.md` | Log hipotesis + baseline vs exploit + keputusan triase. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program enterprise + perangkat in-scope: produk + IP/domain]
Produk/versi: [produk + versi + bukti fingerprinting + tanggal]
CVE: [CVE ID + CVSS + EPSS + KEV + versi terdampak + kondisi terpenuhi]
Baseline (lab): [perilaku normal replika + bukti + tanggal]
Exploit (lab milik sendiri): [langkah + bukti + tanggal]
Perbandingan: [variabel yang berubah]
Pengulangan: [berhasil diulang dari replika bersih: ya/tidak]
Keputusan triase: [maju / ditolak + alasan]
Status: [dipelajari / diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui (BELUM DIUJI)

- Pola di atas diringkas dari riset, bukan dari satu kasus nyata yang lolos triase — tiap produk punya varian fingerprinting (banner yang disamarkan, versi yang disembunyikan, path yang diubah admin) yang tidak tercantum di sini. Bila menemui varian baru, catat di log dan ajukan sebagai tambahan skill.
- Replika lab mungkin tidak identik 100% dengan perangkat target (konfigurasi admin berbeda) — catat perbedaan konfigurasi yang diketahui sebagai asumsi, bukan fakta.
- Template nuclei generik bisa memberi false positive pada perangkat enterprise — JANGAN jadikan hasil scan sebagai temuan tanpa Gerbang 3.

### Available connectors

Tidak ada konektor khusus untuk skill ini; fingerprinting memakai `curl`/`openssl` dan intel CVE lewat `mcp-shodan`.

### Websites

- Basis data CVE resmi (NVD) + vendor advisory tiap produk (VMware, Citrix, Ivanti, Fortinet, Palo Alto) — sumber CVE + versi terdampak + perbaikan.
- Dokumentasi produk resmi (path/endpoint khas tiap produk).
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila versi perangkat tidak terungkap dari fingerprinting pasif, andalkan korelasi CVE berdasarkan produk saja dengan label "versi tidak terkonfirmasi" — jangan memaksa dengan fuzzing agresif atau login percobaan.
- Bila lab replika tidak bisa dibangun (appliance berbayar), buktikan dampak lewat dokumentasi vendor + kondisi yang terpenuhi di target, lalu serahkan ke Muse — jangan mengklaim terbukti tanpa Gerbang 3.
