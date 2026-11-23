# Skill: Enumerasi Subdomain — Pasif (Certificate Transparency, Shodan, Censys) + Aktif (DNS Brute-Force)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 5 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu enumerasi nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih dan domain targetnya perlu diinventarisasi subdomainnya SEBELUM probing atau pengujian apa pun — sebagai langkah pertama `pemetaan-permukaan-serangan`. Bukan untuk bounty agen AI (Muse, OpenAI, 0din, Google AI VRP, ViKernel) — di sana yang dinilai hasil/outcome pada agennya, bukan scanning web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan enumerasi pasif + aktif, dedup, dan penyerahan ke indeks |
| Pemimpin | **Muse** | Putuskan domain mana yang dienumerasi dan kapan daftar dinyatakan lengkap |

## Sudah tercakup (jangan diduplikat)

- **Recon PROGRAM** (direktori, scope, hadiah, deadline) ada di `recon-pantau-program` — skill ini beda: enumerasi TEKNIS subdomain target.
- **Payung recon** ada di `pemetaan-permukaan-serangan` (langkah 2 menyebut enumerasi subdomain dalam satu baris) — skill ini adalah panduan langkah-demi-langkah teknik itu sendiri; hasilnya diserahkan ke indeks aset skill payung tersebut.
- **Alat-alatnya** ada di skill MCP masing-masing (`mcp-osint`, `mcp-shodan`, `mcp-security-hub`) — skill ini hanya merujuk namanya sebagai "tangan", jangan duplikat dokumentasi alatnya.
- **Probing hasil enumerasi** (status HTTP, teknologi) ada di `probing-http-fingerprint` — skill ini berhenti di daftar subdomain yang teresolusi.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Domain di luar scope = HENTIKAN, jangan dienumerasi.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; tanpa pemindaian massal tanpa jeda.
4. **Tanpa payload di permukaan publik.** Enumerasi hanya MENGAMATI dan MENCATAT — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar subdomain bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program).
10. **Subdomain out-of-scope yang ikut ketemu dicatat sebagai out-of-scope, bukan diuji.** Menemukan bukan berarti boleh menguji.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope (wajib, sebelum query apa pun)

- Apa yang dilakukan: baca aturan program, catat domain in-scope (domain apex + wildcard `*.target` bila dinyatakan in-scope) dan yang dilarang.
- Standar lulus: domain tertulis; enumerasi terhadap domain DI LUAR scope = DILARANG, jangan lanjut.

### Gerbang 1 — Enumerasi pasif via Certificate Transparency

- Apa yang dilakukan: tarik subdomain dari log CT — `crtsh_search` (`mcp-osint`), crt.sh web/API, dan Censys (`mcp-osint` Gerbang 3, key sendiri bila perlu). Catat tiap subdomain + sumber penemuan + tanggal.
- Standar lulus: ada daftar awal dari ≥1 sumber CT; tiap entri punya sumber. CT hanya mencatat subdomain yang pernah punya sertifikat — ketiadaan di CT bukan bukti tidak ada.

### Gerbang 2 — Enumerasi pasif via agregator (Shodan, VirusTotal, SecurityTrails)

- Apa yang dilakukan: `domain_info` / `shodan_search` (`mcp-shodan`), `vt_subdomains` dan Censys/SecurityTrails (`mcp-osint` Gerbang 3). Gabungkan dengan hasil Gerbang 1, dedup berdasarkan nama subdomain.
- Standar lulus: daftar gabungan terdokumentasi per sumber; duplikat dihapus; subdomain yang hanya muncul di satu sumber dicatat "belum terkonfirmasi", bukan sebagai fakta.

### Gerbang 3 — Enumerasi aktif: DNS brute-force (hanya in-scope, rate limit)

- Apa yang dilakukan: brute-force label subdomain dengan wordlist (mis. `subfinder -d <domain> -all` untuk pasif+aktif, atau `dnsx -d <domain> -w <wordlist>` / `amass enum -brute -d <domain>` — cek README alat sebelum pakai pertama kali). Pakai wordlist kecil dulu, besarkan hanya bila perlu. Jeda antar query, maks 5 req/detik.
- Standar lulus: wordlist yang dipakai tercatat (nama + ukuran); tidak ada query ke domain di luar scope; tidak ada tanda rate-limit/ban dari resolver; hasil brute-force dicatat terpisah dari hasil pasif (beri label sumber "brute-force").

### Gerbang 4 — Resolusi + deteksi wildcard + dedup akhir

- Apa yang dilakukan: resolusi semua kandidat (mis. `dnsx -l <daftar> -a -resp`); uji wildcard dengan menanyakan label acak yang hampir pasti tidak ada (`<random>.target`) — bila ikut teresolusi, domain memakai wildcard dan hasil brute-force harus difilter terhadap IP wildcard itu.
- Standar lulus: tiap subdomain punya status resolusi (IP / tidak teresolusi); hasil wildcard teridentifikasi dan dibuang dari daftar "subdomain nyata"; daftar akhir bebas duplikat.

### Gerbang 5 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis daftar akhir ke `indeks-aset-<program>-<tanggal>.md` (format `pemetaan-permukaan-serangan`) + log sesi. Subdomain yang hidup diserahkan ke `probing-http-fingerprint` untuk probing; yang mati dicatat "mati" dan tidak diprobing.
- Standar lulus: tiap entri punya nama, sumber penemuan, status resolusi, dan status hidup/mati (atau "belum diprobing"); tidak ada subdomain in-scope yang diketahui tapi tidak tercatat.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| CT log, DNS, RDAP/WHOIS, agregator pasif | `mcp-osint` (`crtsh_search`, `dns_lookup`, Censys, SecurityTrails, VirusTotal) |
| Intel Shodan (domain_info, DNS) | `mcp-shodan` |
| Brute-force DNS, resolusi, agregasi | `mcp-security-hub` (subfinder, dnsx, amass — cek README repo sebelum pakai) |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |
| Payung indeks aset | `pemetaan-permukaan-serangan` |

## Format output

### Daftar subdomain

Simpan di `~/workspace/catatan/subdomain-<target>-<tanggal>.md`:

```
- Subdomain: <nama> | sumber: <CT/Shodan/VT/brute-force> | resolusi: <IP / tidak teresolusi>
- Status: HIDUP / MATI / BELUM DIPROBING | wildcard: <ya/tidak>
- Wordlist brute-force: <nama + jumlah entri> | rate: <req/detik>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Enumerasi subdomain — <program/target>
- Pasif: <n> subdomain (CT: <n>, agregator: <n>)
- Aktif (brute-force): <n> tambahan | wordlist: <nama>
- Teresolusi: <n> | wildcard: <ya/tidak, IP wildcard>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- crt.sh (https://crt.sh) — log Certificate Transparency.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila CT + agregator sudah memberi daftar yang cukup dan program melarang pemindaian aktif, lewati Gerbang 3 — catat "brute-force dilewati (program melarang aktif)" dan lanjut ke Gerbang 4.
- Bila wordlist besar memicu rate-limit resolver, kecilkan wordlist dan naikkan jeda — jangan menaikkan kecepatan melewati batas program.
