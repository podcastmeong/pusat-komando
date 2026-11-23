# Skill: Pemindaian Port & Layanan — Port Non-Standar (Selain 80/443) + Layanan di Baliknya

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 8 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu pemindaian nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat daftar IP/host in-scope sudah ada (dari `penemuan-asn-ip` / `enumerasi-subdomain` + `probing-http-fingerprint`) dan perlu diketahui port apa saja yang terbuka — terutama port non-standar di luar 80/443 — serta layanan + versi di balik tiap port. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan pemindaian, deteksi layanan, korelasi CVE, penyerahan ke indeks |
| Pemimpin | **Muse** | Putuskan IP mana yang dipindai dan kapan hasil dinyatakan lengkap |

## Sudah tercakup (jangan diduplikat)

- **Payung recon** ada di `pemetaan-permukaan-serangan` (langkah 3 menyebut port scanning dalam satu baris) — skill ini adalah panduan langkah-demi-langkah teknik itu sendiri; hasilnya diserahkan ke indeks aset skill itu.
- **Info port pasif dari Shodan** ada di `mcp-shodan` (`ip_lookup`) — Gerbang 1 skill ini memakai data itu; pemindaian aktif di bawah adalah teknik terpisah.
- **Alat-alatnya** (nmap, naabu) dirujuk dari `mcp-security-hub` — jangan duplikat dokumentasi alatnya; JANGAN pakai server Nmap MCP yang berdiri sendiri (sudah diarsipkan + ada peringatan prompt injection — lihat `mcp-security-hub`).
- **Korelasi CVE dengan versi produk** ada di `mcp-shodan` (Gerbang 4) — skill ini hanya mencatat layanan + versi yang terlihat, tanpa menyimpulkan kerentanan.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** IP di luar scope = HENTIKAN, jangan dipindai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; timing lambat (nmap `-T2`/`-T3`, bukan `-T4`/`-T5`); tanpa SYN flood, tanpa UDP flood, tanpa pemindaian seluruh 65.535 port sekaligus tanpa jeda. Satu target, satu pemindaian, satu waktu.
4. **Tanpa payload di permukaan publik.** Pemindaian hanya SYN/connect + banner grab — tidak mengirim payload eksploitasi, tidak login ke layanan yang ditemukan, tidak mengubah/menghapus data.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Hasil pemindaian bukan laporan.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program).
10. **Port terbuka ≠ rentan.** Layanan + versi dicatat sebagai "terlihat"; kerentanan diputuskan di tahap pengujian dengan bukti terpisah (lihat `skeptic-false-positive-eliminator`).

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope + daftar IP (wajib, sebelum paket apa pun dikirim)

- Apa yang dilakukan: ambil daftar IP IN-SCOPE dari `penemuan-asn-ip` (Gerbang 4); baca aturan program — catat apakah pemindaian port diizinkan dan batas kecepatannya.
- Standar lulus: daftar IP tertulis + izin pemindaian tertulis; IP tanpa dasar in-scope = DILARANG dipindai; bila program melarang pemindaian aktif, BERHENTI di Gerbang 1 (pasif saja).

### Gerbang 1 — Port pasif dulu (Shodan)

- Apa yang dilakukan: `ip_lookup` (`mcp-shodan`) untuk tiap IP in-scope; catat port + produk + versi yang SUDAH diketahui publik.
- Standar lulus: tiap IP punya daftar port-pasif + sumber (Shodan + tanggal); port yang hanya dari sumber pasif dicatat "pasif — belum dikonfirmasi aktif".

### Gerbang 2 — Pemindaian top-port (aktif, in-scope saja)

- Apa yang dilakukan: pindai top-port umum dulu (mis. nmap top 1000 atau naabu dengan daftar top-port — cek README/flag alat sebelum pakai pertama kali), satu IP per sesi, timing `-T2`/`-T3`, rate ≤5 req/detik. Catat port terbuka + status (open/filtered).
- Standar lulus: tiap IP punya hasil top-port + perintah yang dipakai + waktu; tidak ada paket ke IP di luar daftar Gerbang 0; tidak ada tanda gangguan layanan (timeout massal, 429, keluhan).

### Gerbang 3 — Perluas ke port non-standar (bila Gerbang 2 memberi sinyal)

- Apa yang dilakukan: bila Gerbang 2 menemukan layanan menarik (mis. port admin, database, remote access) ATAU program mengizinkan, perluas ke rentang port yang lebih luas secara bertahap (bukan langsung full-range); prioritaskan port non-standar yang umum untuk layanan (8080, 8443, 8000, 8888, 9000, 3000, 5000, 5432, 3306, 6379, 27017, 22, 21, 25, 53 — sesuaikan dengan konteks target).
- Standar lulus: perluasan tercatat dengan alasan (sinyal Gerbang 2 / izin program); full-range scan hanya bila ada alasan tertulis dan izin program; tiap port baru tercatat sumbernya (top-port / perluasan).

### Gerbang 4 — Deteksi layanan + versi (banner grab)

- Apa yang dilakukan: untuk tiap port terbuka, deteksi layanan + versi (mis. nmap `-sV` pada port terbuka saja, atau banner grab manual). Catat banner persis seperti terlihat (potong bila terlalu panjang; sensor kredensial bila banner membocorkannya — tulis `[REDACTED]`).
- Standar lulus: tiap port terbuka punya layanan + versi (atau "tidak teridentifikasi"); banner tersimpan sebagai bukti; tidak ada upaya login ke layanan yang ditemukan.

### Gerbang 5 — Korelasi CVE (tanpa exploit) + validasi manual

- Apa yang dilakukan: untuk tiap pasangan layanan+versi, tarik CVE terkait (`cve_lookup` / `cves_by_product` di `mcp-shodan`); cocokkan versi yang terlihat dengan versi terdampak. A57 memeriksa tiap temuan secara manual — CVE tanpa versi yang cocok = BELUM TERBUKTI.
- Standar lulus: tiap klaim kerentanan punya pasangan (CVE + versi terdampak + skor CVSS/EPSS/KEV); tanpa pasangan = dicatat sebagai "layanan terlihat", bukan temuan.

### Gerbang 6 — Serahkan ke indeks (Muse)

- Apa yang dilakukan: tulis port + layanan + versi + CVE terkait ke `indeks-aset-<program>-<tanggal>.md` + log sesi.
- Standar lulus: tiap IP punya daftar port lengkap (pasif + aktif) dengan status konfirmasi; tidak ada port tanpa sumber yang lolos ke tahap uji.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Port scanning + deteksi layanan | nmap / naabu via `mcp-security-hub` (cek README sebelum pakai; JANGAN server Nmap MCP mandiri) |
| Info port + CVE pasif | `mcp-shodan` (`ip_lookup`, `cve_lookup`, `cves_by_product`) |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |
| Validasi temuan (anti false-positive) | `skeptic-false-positive-eliminator` |
| Payung indeks aset | `pemetaan-permukaan-serangan` |

## Format output

### Hasil pemindaian

Simpan di `~/workspace/catatan/port-<target>-<tanggal>.md`:

```
- IP: <alamat> | ASN: <nomor, bila diketahui>
- Port: <nomor/tcp> | status: <open/filtered> | sumber: <pasif-Shodan / top-port / perluasan>
- Layanan: <nama + versi / tidak teridentifikasi> | banner: <ringkasan>
- CVE terkait: <CVE + CVSS/EPSS/KEV / belum terbukti>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Pemindaian port & layanan — <program/target>
- IP dipindai: <n> | port terbuka: <n> (standar: <n>, non-standar: <n>)
- Layanan teridentifikasi: <n> | CVE terkait (terbukti versi): <n>
- Perintah: <perintah nmap/naabu yang dipakai> | rate: <req/detik> | timing: <T2/T3>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi nmap (https://nmap.org/book/man.html) — flag dan timing.
- Halaman aturan program resmi (sumber scope + izin pemindaian Gerbang 0).

### Alternatives for better results

- Bila nmap tidak tersedia, naabu (ProjectDiscovery) adalah pengganti yang lebih cepat untuk top-port — tetap dengan rate limit yang sama.
- Bila program melarang pemindaian aktif sepenuhnya, hasil Gerbang 1 (Shodan pasif) adalah hasil akhir skill ini — catat "aktif dilarang program" dan jangan memaksa.
