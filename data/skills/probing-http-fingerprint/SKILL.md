# Skill: Probing HTTP & Fingerprinting — Server Aktif, Status HTTP, Teknologi Backend, Framework, CDN

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 7 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu probing nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat daftar subdomain/IP in-scope sudah ada (dari `enumerasi-subdomain` / `penemuan-asn-ip`) dan perlu diketahui mana yang benar-benar hidup, status HTTP-nya, serta teknologi di baliknya (server, framework, bahasa, CDN/WAF) — SEBELUM pengujian kerentanan apa pun. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan probing + fingerprinting, klasifikasi, penyerahan ke indeks |
| Pengerjaan | **A59 Threat Hunter** | Mengorelasikan teknologi yang terdeteksi dengan CVE yang diketahui (tanpa exploit) |
| Pemimpin | **Muse** | Putuskan host mana yang diprioritaskan untuk pengujian |

## Sudah tercakup (jangan diduplikat)

- **Payung recon** ada di `pemetaan-permukaan-serangan` — hasil probing (status + teknologi per host) diserahkan ke indeks aset skill itu.
- **Enumerasi subdomain** (sumber daftar host) ada di `enumerasi-subdomain`; **pemetaan ASN/IP** ada di `penemuan-asn-ip` — skill ini memakai daftarnya, bukan membuatnya.
- **Alat-alatnya** (httpx, Wappalyzer, whatweb) dirujuk dari `mcp-security-hub` / `mcp-pentest` bila tersedia — skill ini adalah panduan teknik probing, bukan dokumentasi alat.
- **Korelasi CVE dengan versi produk** ada di `mcp-shodan` (Gerbang 4) — skill ini hanya mencatat teknologi + versi yang terlihat, tanpa menyimpulkan kerentanan.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** Host di luar scope = HENTIKAN, jangan diprobing.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; batasi konkurensi (mis. ≤10 thread) dan ikuti `Retry-After` / 429 dengan backoff — 429 adalah perintah berhenti sementara, bukan undangan mencoba lagi lebih keras.
4. **Tanpa payload di permukaan publik.** Probing hanya request GET/HEAD biasa ke path `/` (dan redirect-nya) — tidak mengirim payload eksploitasi, tidak mengubah/menghapus data, tidak login, tidak submit form.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Hasil probing bukan laporan.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program).
10. **Fingerprinting = pengamatan header/respons, bukan eksploitasi.** Versi teknologi yang terdeteksi dicatat sebagai "terlihat", bukan sebagai "rentan" — kerentanan diputuskan di tahap pengujian dengan bukti terpisah.

## Langkah + gerbang

### Gerbang 0 — Siapkan daftar + scope (wajib, sebelum request apa pun)

- Apa yang dilakukan: ambil daftar host dari `enumerasi-subdomain` / `penemuan-asn-ip`; baca aturan program; pastikan tiap host in-scope.
- Standar lulus: daftar host tertulis + jumlahnya; host out-of-scope sudah dibuang dari daftar probing.

### Gerbang 1 — Probing hidup/mati + status HTTP (logika httpx)

- Apa yang dilakukan: probe tiap host (mis. `httpx -l <daftar> -status-code -title -content-length -follow-redirects -tls-probe -rate-limit 5` — cek README/flag alat sebelum pakai pertama kali). Catat: status akhir, rantai redirect, title, content-length, sertifikat TLS (penerbit, kedaluwarsa).
- Standar lulus: tiap host punya status akhir + title + content-length (atau "tidak merespons" + jenis error: timeout/DNS/connection-refused); tidak ada host yang diprobing dua kali tanpa alasan.

### Gerbang 2 — Fingerprinting teknologi (logika Wappalyzer/whatweb)

- Apa yang dilakukan: identifikasi teknologi dari header respons (`Server`, `X-Powered-By`, `X-AspNet-Version`), cookie (`PHPSESSID`, `JSESSIONID`, dsb.), pola HTML/JS (generator meta, path aset khas framework), dan hash favicon. Catat: web server + versi (bila terlihat), framework/CMS, bahasa, dan teknologi frontend — masing-masing dengan bukti (header/nilai yang terlihat).
- Standar lulus: tiap host hidup punya ≥1 teknologi tercatat DENGAN bukti; teknologi tanpa bukti dicatat "dugaan", bukan fakta; header yang tidak memberi info dicatat "tidak terungkap".

### Gerbang 3 — Deteksi CDN / WAF / proxy

- Apa yang dilakukan: kenali CDN/WAF dari header khas (`CF-Ray`/`Server: cloudflare`, `X-Cache`, `X-Amz-Cf-Id`, `Server: AkamaiGHost`), CNAME host, dan ASN IP hasil resolusi (silangkan dengan `penemuan-asn-ip`). Catat CDN/WAF yang terdeteksi + bukti.
- Standar lulus: tiap host hidup punya status CDN/WAF ("terdeteksi: <nama + bukti>" / "tidak terdeteksi"); host di balik CDN dicatat IP CDN-nya, bukan diklaim sebagai IP origin.

### Gerbang 4 — Klasifikasi + prioritas

- Apa yang dilakukan: klasifikasikan tiap host: HIDUP (200/3xx dengan konten), REDIRECT (rantai ke host lain — catat tujuan), PARKIR/DEFAULT (halaman default server/parkir domain), ERROR (4xx/5xx), MATI (tidak merespons). Prioritaskan untuk pengujian: host HIDUP dengan teknologi teridentifikasi > host ERROR > PARKIR (terendah).
- Standar lulus: tiap host punya satu klasifikasi + prioritas; host REDIRECT dicatat tujuan akhirnya (bila tujuan out-of-scope, host itu ditandai "jangan diuji lewat redirect").

### Gerbang 5 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis hasil probing ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Hanya host klasifikasi HIDUP/ERROR yang diteruskan sebagai kandidat pengujian.
- Standar lulus: tiap entri indeks punya status, teknologi + bukti, CDN/WAF, dan klasifikasi; tidak ada host MATI/PARKIR yang lolos sebagai kandidat uji.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Probing HTTP massal (status, title, TLS) | httpx (via `mcp-security-hub` / `mcp-pentest` bila tersedia — cek README sebelum pakai) |
| Fingerprinting teknologi | Wappalyzer (ekstensi/CLI), whatweb — logika: header + pola HTML + favicon hash |
| Korelasi CDN/WAF ↔ ASN/IP | `penemuan-asn-ip`, `mcp-osint` (BGPView) |
| Korelasi teknologi ↔ CVE (tanpa exploit) | `mcp-shodan` (`cve_lookup`, `cves_by_product`) |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |

## Format output

### Hasil probing

Simpan di `~/workspace/catatan/probing-<target>-<tanggal>.md`:

```
- Host: <nama> | status: <kode akhir> | title: <judul> | panjang: <bytes>
- Redirect: <rantai, bila ada> | TLS: <penerbit, kedaluwarsa>
- Teknologi: <server/framework/bahasa + bukti header/nilai>
- CDN/WAF: <nama + bukti / tidak terdeteksi>
- Klasifikasi: HIDUP / REDIRECT / PARKIR / ERROR / MATI | prioritas: <1-3>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Probing HTTP & fingerprinting — <program/target>
- Host diprobing: <n> | hidup: <n> | redirect: <n> | parkir: <n> | error: <n> | mati: <n>
- Teknologi teridentifikasi: <ringkasan per teknologi>
- CDN/WAF terdeteksi: <daftar>
- Rate: <req/detik> | 429 diterima: <ya/tidak, tindakan>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi httpx (https://github.com/projectdiscovery/httpx) — flag dan pemakaian.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila httpx tidak tersedia, probing manual dengan `curl -I -L` per host tetap sah untuk daftar kecil (<20 host) — catat "probing manual" di log.
- Bila teknologi tidak teridentifikasi dari header, jangan memaksa dengan request tambahan ke path tebak-tebakan — catat "tidak terungkap" dan serahkan ke analisis JS (`pemetaan-permukaan-serangan` langkah 4).
