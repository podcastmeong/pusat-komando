# Skill: Penemuan ASN & IP Range — Pemetaan Infrastruktur via BGP/ASN + Reverse WHOIS

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 6 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu pemetaan nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat sebuah program bounty web/API klasik in-scope sudah dipilih dan infrastruktur target perlu dipetakan di tingkat jaringan — ASN dan rentang IP mana yang dimiliki/digunakan organisasi target — SEBELUM pemindaian port atau pengujian apa pun. Masukan: satu atau beberapa IP/domain in-scope yang sudah diketahui (dari `enumerasi-subdomain` atau `probing-http-fingerprint`). Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A53 Recon Program** | Menjalankan lookup ASN/BGP/WHOIS, memangkas range ke scope, menyerahkan ke indeks |
| Pemimpin | **Muse** | Putuskan ASN/range mana yang dinyatakan in-scope dan kapan peta dinyatakan lengkap |

## Sudah tercakup (jangan diduplikat)

- **WHOIS/RDAP + BGPView sebagai alat** ada di `mcp-osint` (Gerbang 2: `whois_ip`, GeoIP, BGPView) — skill ini adalah panduan teknik pemetaan ASN→range→aset, bukan dokumentasi alatnya.
- **Payung recon** ada di `pemetaan-permukaan-serangan` — hasilnya (ASN + range + IP) diserahkan ke indeks aset skill itu.
- **Pemindaian port pada IP hasil pemetaan** ada di `pemindaian-port-layanan` — skill ini berhenti di peta IP; pemindaian adalah langkah terpisah.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** ASN/range di luar scope = HENTIKAN, jangan dipetakan lebih jauh.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; query WHOIS/BGP secukupnya, jangan membanjiri.
4. **Tanpa payload di permukaan publik.** Pemetaan ini hanya MENGAMATI dan MENCATAT.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Peta ASN bukan laporan.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program).
10. **Range ASN ≠ in-scope otomatis.** ASN besar (mis. cloud provider) berisi ribuan pelanggan lain — HANYA IP/range yang dinyatakan in-scope oleh aturan program yang boleh dipindai/diuji. Menemukan range tidak memberi izin menguji seluruh range.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope + IP awal (wajib, sebelum query apa pun)

- Apa yang dilakukan: baca aturan program; catat IP/domain in-scope yang sudah diketahui dan apakah program menyatakan IP range/ASN sebagai in-scope (tertulis) atau hanya domain tertentu.
- Standar lulus: IP awal tertulis + status scope ASN tertulis ("ASN dinyatakan in-scope" / "hanya domain X"). Bila program hanya mengizinkan domain, pemetaan ASN dipakai HANYA untuk memahami kepemilikan — bukan untuk memperluas target pemindaian.

### Gerbang 1 — WHOIS/RDAP per IP awal

- Apa yang dilakukan: `whois_ip` (`mcp-osint`) atau `whois` RDAP untuk tiap IP awal; catat organisasi pemilik, ASN, negara, dan abuse contact.
- Standar lulus: tiap IP awal punya ASN + organisasi pemilik + sumber query + tanggal.

### Gerbang 2 — ASN → prefix/route via BGP

- Apa yang dilakukan: BGPView (`mcp-osint`) atau bgp.he.net untuk ASN dari Gerbang 1; tarik daftar prefix IPv4/IPv6 yang diumumkan ASN itu (prefix, ukuran, deskripsi).
- Standar lulus: tiap ASN punya daftar prefix + jumlah alamat; prefix yang diumumkan tapi milik pelanggan lain (bila terlihat dari deskripsi/WHOIS) ditandai "bukan milik target".

### Gerbang 3 — Reverse WHOIS: organisasi → ASN & domain lain

- Apa yang dilakukan: cari berdasarkan nama organisasi pemilik (reverse WHOIS / pencarian RDAP): ASN lain yang didaftarkan atas nama yang sama, dan domain lain yang terdaftar atas organisasi itu — silangkan dengan hasil `enumerasi-subdomain`.
- Standar lulus: tiap ASN/domain tambahan punya sumber + status ("milik target terkonfirmasi" / "nama sama, belum terkonfirmasi"); yang belum terkonfirmasi TIDAK masuk daftar target uji.

### Gerbang 4 — Pangkas range ke scope program

- Apa yang dilakukan: bandingkan prefix hasil Gerbang 2–3 dengan aturan program; buat dua daftar tegas: (a) IP/range IN-SCOPE yang boleh dipindai, (b) IP/range DIKETAHUI TAPI OUT-OF-SCOPE (dicatat, tidak diuji). Bila program memakai wildcard domain, IP yang teresolusi dari domain in-scope masuk daftar (a); sisa prefix ASN masuk daftar (b).
- Standar lulus: tidak ada IP yang masuk daftar (a) tanpa dasar aturan program tertulis; daftar (b) ada dan lengkap; ambiguitas dicatat sebagai "belum diputuskan — tanya Muse", bukan diasumsikan in-scope.

### Gerbang 5 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis peta ASN + kedua daftar IP ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Daftar (a) menjadi masukan `pemindaian-port-layanan`.
- Standar lulus: tiap IP/range punya ASN, organisasi, prefix sumber, dan status IN-SCOPE / OUT-OF-SCOPE; tidak ada IP tanpa status yang lolos ke tahap pemindaian.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| WHOIS/RDAP, BGPView, GeoIP | `mcp-osint` (`whois_ip`, `whois_domain`, BGPView, GeoIP) |
| Intel IP tambahan (bila perlu) | `mcp-shodan` (`ip_lookup`) |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |
| Payung indeks aset | `pemetaan-permukaan-serangan` |

## Format output

### Peta ASN & IP range

Simpan di `~/workspace/catatan/asn-<target>-<tanggal>.md`:

```
- ASN: <AS12345> | organisasi: <nama> | sumber: <BGPView/RDAP>
- Prefix: <CIDR> | alamat: <jumlah> | milik target: <ya/tidak/belum terkonfirmasi>
- IP IN-SCOPE (boleh dipindai): <daftar + dasar aturan program>
- IP OUT-OF-SCOPE (dicatat, jangan diuji): <daftar>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Penemuan ASN & IP range — <program/target>
- ASN ditemukan: <n> | prefix: <n> | IP in-scope: <n> | IP out-of-scope: <n>
- Reverse WHOIS: <n> ASN/domain tambahan (<n> terkonfirmasi)
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- BGPView (https://bgpview.io) dan bgp.he.net — data ASN/prefix.
- Halaman aturan program resmi (sumber scope Gerbang 0 dan dasar daftar in-scope Gerbang 4).

### Alternatives for better results

- Bila BGPView tidak merespons, pakai `whois -h whois.radb.net` / Team Cymru IP-to-ASN sebagai sumber kedua — catat sumber pengganti di log.
- Bila organisasi target memakai cloud (AWS/GCP/Azure), ASN yang muncul adalah ASN cloud provider — jangan klaim seluruh prefix cloud sebagai milik target; batasi ke IP yang teresolusi dari domain in-scope.
