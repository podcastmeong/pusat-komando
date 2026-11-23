# Skill: Penemuan Virtual Host (VHost) — Aplikasi Internal/Staging Tersembunyi di Balik Satu IP

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: butir 9 Fase 2 "50 Skill Esensial AI Agent Pemburu Bug Bounty" (`~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), 23 Nov 2026. Jangan klaim metode ini terbukti sebelum satu penemuan nyata lolos gerbang di bawah dan diperiksa pihak kedua.

## Pemicu

Dipakai saat satu IP in-scope diketahui melayani beberapa aplikasi lewat header `Host` (server virtual-hosting) dan perlu diketahui vhost apa saja yang tersembunyi di balik IP itu — terutama aplikasi internal/staging yang tidak muncul di enumerasi subdomain publik. Masukan: IP in-scope + daftar subdomain yang sudah diketahui. Bukan untuk bounty agen AI.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A57 Penetration Tester** | Menjalankan brute-force Host header, membedakan respons, verifikasi, penyerahan ke indeks |
| Pemimpin | **Muse** | Putuskan vhost mana yang dinyatakan in-scope dan boleh diuji lebih jauh |

## Sudah tercakup (jangan diduplikat)

- **Enumerasi subdomain** (sumber kandidat vhost) ada di `enumerasi-subdomain` — skill ini memakai daftarnya + wordlist, bukan membuatnya.
- **Data historis** (sumber kandidat vhost lama) ada di `penambangan-data-historis` — silangkan hasilnya ke sini.
- **Payung recon** ada di `pemetaan-permukaan-serangan` — vhost yang ditemukan diserahkan ke indeks aset skill itu.
- **Probing HTTP** (status/teknologi host yang sudah diketahui) ada di `probing-http-fingerprint` — skill ini mencari host yang BELUM diketahui; setelah ketemu, probing-nya memakai skill itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope.** IP di luar scope = HENTIKAN, jangan diprobing.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Patuhi rate limit maks **5 req/detik** kecuali program mengizinkan lebih; wordlist kecil dulu; ikuti 429 dengan backoff.
4. **Tanpa payload di permukaan publik.** Brute-force Host header hanya request GET/HEAD biasa — tidak mengirim payload eksploitasi, tidak login, tidak mengubah/menghapus data.
5. **Tanpa aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, `document.domain`) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar vhost bukan laporan.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Recon pasif diutamakan; pemindaian aktif hanya pada target in-scope dengan rate limit** (maks 5 req/detik kecuali diizinkan program).
10. **Vhost internal/staging yang ketemu BELUM tentu in-scope.** Aplikasi internal/staging di balik IP in-scope sering kali DI LUAR scope program — JANGAN diuji lebih jauh sebelum Muse memastikan status scope-nya dari aturan program. Menemukan ≠ boleh menguji.

## Langkah + gerbang

### Gerbang 0 — Tetapkan scope + IP target + baseline (wajib, sebelum brute-force)

- Apa yang dilakukan: baca aturan program; pilih SATU IP in-scope yang akan diuji; ambil baseline: respons server bila diminta tanpa Host yang dikenal (request ke IP langsung + Host header acak yang pasti tidak ada) — catat status, panjang, title baseline.
- Standar lulus: IP tertulis + baseline tercatat (status + panjang + title); tanpa baseline, hasil brute-force tidak bisa dibedakan — jangan lanjut.

### Gerbang 1 — Kumpulkan kandidat vhost

- Apa yang dilakukan: gabungkan (a) subdomain yang sudah diketahui dari `enumerasi-subdomain`, (b) nama lama dari `penambangan-data-historis`, (c) wordlist vhost umum (dev, staging, stg, test, qa, internal, admin, api, beta, demo, uat, preprod + nama produk/perusahaan). Dedup; catat sumber tiap kandidat.
- Standar lulus: daftar kandidat tertulis + sumber tiap entri; wordlist yang dipakai tercatat (nama + jumlah entri).

### Gerbang 2 — Brute-force Host header (aktif, in-scope saja)

- Apa yang dilakukan: kirim request ke IP target dengan header `Host: <kandidat>` yang bervariasi (mis. `ffuf -u http://<IP>/ -H "Host: FUZZ.<domain>" -w <wordlist> -fs <ukuran-baseline> -rate 5` — cek README/flag alat sebelum pakai pertama kali). Filter otomatis terhadap ukuran/status baseline agar hanya respons yang BERBEDA yang dicatat.
- Standar lulus: wordlist + filter tercatat; rate ≤5 req/detik; tidak ada request ke IP lain; kandidat yang responsnya sama persis dengan baseline dicatat "sama dengan baseline — bukan vhost", bukan sebagai temuan.

### Gerbang 3 — Bedakan respons kandidat

- Apa yang dilakukan: untuk tiap kandidat yang lolos filter, bandingkan dengan baseline: status, panjang, title, header khas (`Server`, `Location`, cookie). Kelompokkan: (a) respons UNIK — kemungkinan vhost nyata; (b) respons sama dengan baseline — buang; (c) respons redirect ke host lain — catat tujuan.
- Standar lulus: tiap kandidat punya putusan (a/b/c) + bukti perbandingan; tidak ada kandidat "lolos filter" yang dibiarkan tanpa putusan.

### Gerbang 4 — Verifikasi manual tiap vhost unik

- Apa yang dilakukan: A57 membuka sendiri tiap vhost kelompok (a) dengan Host header yang sama (mis. `curl -H "Host: <vhost>" http://<IP>/ -i`), bandingkan dengan baseline dan dengan vhost default; pastikan responsnya stabil dan bisa diulang, bukan kesalahan satu kali (error acak, halaman parkir).
- Standar lulus: tiap vhost terverifikasi punya bukti request+respons yang bisa diulang + tanggal; vhost yang tidak bisa diulang dicatat "tidak terkonfirmasi", bukan sebagai fakta.

### Gerbang 5 — Tentukan status scope + serahkan ke indeks (Muse)

- Apa yang dilakukan: untuk tiap vhost terverifikasi, Muse memastikan dari aturan program apakah vhost itu in-scope (mis. `*.target` in-scope → vhost `staging.target` in-scope; IP-only scope → vhost internal kemungkinan out-of-scope). Tulis vhost + status scope-nya ke `indeks-aset-<program>-<tanggal>.md` + log sesi. Vhost in-scope diteruskan ke `probing-http-fingerprint`.
- Standar lulus: tiap vhost punya status IN-SCOPE / OUT-OF-SCOPE / BELUM DIPUTUSKAN; tidak ada vhost "belum diputuskan" yang lolos ke tahap pengujian.

## Alat

| Keperluan | "Tangan" (rujuk skill-nya, jangan duplikat) |
|---|---|
| Brute-force Host header + filter respons | ffuf (via `mcp-security-hub` bila tersedia — cek README sebelum pakai) |
| Verifikasi manual request Host header | `curl -H "Host: <vhost>" http://<IP>/ -i` |
| Sumber kandidat vhost | `enumerasi-subdomain`, `penambangan-data-historis` |
| Probing lanjutan vhost in-scope | `probing-http-fingerprint` |
| Penjaga scope & rate limit | `scope-and-safety-guardian` |

## Format output

### Daftar vhost

Simpan di `~/workspace/catatan/vhost-<target>-<tanggal>.md`:

```
- IP: <alamat> | baseline: <status + panjang + title>
- VHost: <nama> | sumber kandidat: <subdomain/historis/wordlist>
- Respons: <status + panjang + title> | beda dari baseline: <ya, bukti / tidak>
- Status scope: IN-SCOPE / OUT-OF-SCOPE / BELUM DIPUTUSKAN
- Wordlist: <nama + jumlah entri> | rate: <req/detik>
```

### Log

Tulis ringkasan ke `~/workspace/catatan/log-bug-bounty.md` hari itu juga:

```
[TANGGAL] Penemuan VHost — <program/target IP>
- Kandidat diuji: <n> | respons unik: <n> | terverifikasi: <n>
- In-scope: <n> | out-of-scope: <n> | belum diputuskan: <n>
- Indeks: <path file indeks>
- Status: SELESAI / BELUM (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; alat-alat di atas dipakai lewat skill MCP masing-masing.

### Websites

- Dokumentasi ffuf (https://github.com/ffuf/ffuf) — flag dan filter.
- Halaman aturan program resmi (sumber scope Gerbang 0 dan penentu status vhost Gerbang 5).

### Alternatives for better results

- Bila ffuf tidak tersedia, brute-force manual dengan `curl` dalam loop kecil (wordlist ≤100) tetap sah — catat "brute-force manual" di log.
- Bila server memakai SNI/TLS per vhost, ulangi pengujian lewat HTTPS dengan SNI yang sesuai; catat bila TLS menghalangi (SNI mismatch) sebagai keterbatasan, bukan sebagai kegagalan.
