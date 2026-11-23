# Skill: Perburuan TLS / DNS / Email Spoofing — Salah Konfigurasi Permukaan Jaringan

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 50, Claude-BugHunter `hunt-tls-network`, 6 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target punya domain, subdomain, atau layanan email yang tercantum in-scope.
- Ditemukan sertifikat kedaluwarsa/tidak valid, tidak ada HSTS, atau cipher lemah saat recon.
- Ditemukan domain tanpa SPF/DKIM/DMARC, transfer zona DNS terbuka, atau CNAME menggantung.
- Dipakai SEBELUM mengklaim "spoofing mungkin": pemeriksaan pasif dulu, pembuktian dampak kemudian.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan pemeriksaan TLS/DNS/email + membuktikan dampak spoofing |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Takeover subdomain (CNAME menggantung → klaim layanan) → skill `deteksi-takeover-subdomain`. Skill ini hanya memakai CNAME menggantung sebagai satu sinyal di antara banyak pemeriksaan DNS, bukan mengulang metodologinya.
- Recon DNS pasif (lookup A/MX/TXT, `dns_email_security` SPF+DMARC+DKIM, CT log) → skill `mcp-osint`. Skill ini memakai hasil recon itu sebagai input, lalu menguji dampaknya.
- Penilaian "missing SPF/DMARC/DKIM tanpa dampak = noise" → skill `gerbang-tujuh-pertanyaan-triase` (Pertanyaan 4) dan `skeptic-false-positive-eliminator` (Gerbang 2). **Aturan turunan: temuan email-auth TANPA skenario eksploitasi nyata = TOLAK.** Skill ini mengajarkan cara membuktikan dampaknya, bukan sekadar melaporkan ketidakhadirannya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh domain/layanan yang diperiksa tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji spoofing email atau downgrade TLS.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (pemeriksaan pasif, spoofing ke mailbox sendiri, callback canary milik sendiri).
11. **Jangan kirim email spoof ke alamat orang lain.** Uji spoofing HANYA ke mailbox uji milik sendiri (atau mailbox canary program bila program menyediakannya). Email spoof yang sampai ke inbox korban = pelanggaran.

## Langkah + gerbang

### Gerbang 1 — Pemeriksaan pasif (tanpa menyentuh target secara aktif)

Kumpulkan dari luar, tanpa request berbahaya. Standar lulus: tiap item tercatat "ada / tidak ada" dengan bukti perintah + output.

1. **TLS:** versi TLS yang didukung (TLS 1.0/1.1 masih aktif?), cipher suite lemah (RC4, 3DES, EXPORT), sertifikat (kedaluwarsa, CN/SAN tidak cocok, self-signed, rantai tidak lengkap), HSTS (header `Strict-Transport-Security` ada? `includeSubDomains`? `preload`?), mTLS (apakah endpoint internal menuntut sertifikat klien — dan apakah bisa dilewati tanpa sertifikat?).
2. **DNS:** transfer zona AXFR (`dig AXFR @ns`), wildcard, CNAME menggantung (→ `deteksi-takeover-subdomain` bila mengarah ke layanan yang bisa diklaim), DNSSEC tidak ada.
3. **Email auth:** SPF (`v=spf1` — `-all` vs `~all` vs tidak ada), DKIM (selector ada? kunci lemah?), DMARC (`p=reject` vs `p=none` vs tidak ada).

### Gerbang 2 — Pembuktian dampak (hanya yang lolos Gerbang 1)

Satu sinyal tanpa dampak = noise. Buktikan SATU rantai dampak per temuan, dengan akun/mailbox sendiri saja:

- **Downgrade TLS:** tunjukkan koneksi bisa dipaksa ke TLS 1.0/cipher lemah dari klien uji sendiri (bukti: handshake log). Dampak yang diklaim: intersepsi kredensial/sesi di jaringan — hanya bila ada endpoint login/sensitif di jalur yang sama.
- **Email spoofing:** kirim email spoof dari domain target ke MAILBOX UJI SENDIRI, tunjukkan email itu lolos SPF/DKIM/DMARC (atau tidak ada kebijakan yang menolaknya) dan tampil sebagai pengirim sah di klien email. Rantai lanjut yang menaikkan severity: spoof → tautan reset-password palsu → ATO (buktikan hanya sampai inbox sendiri; JANGAN kirim ke korban).
- **AXFR / DNS:** tunjukkan data internal yang bocor lewat AXFR (nama host internal, alamat IP) dan apa yang bisa dirantai darinya (mis. host admin yang terekspos → `pemetaan-permukaan-serangan`).
- **mTLS bypass:** tunjukkan endpoint yang seharusnya butuh sertifikat klien bisa diakses tanpa sertifikat dari IP uji sendiri.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = spoof/downgrade yang terbukti sampai ke mailbox/klien sendiri + rantai dampak konkret. **TOLAK** = sekadar "tidak ada SPF/DMARC/HSTS" tanpa pembuktian (lihat `gerbang-tujuh-pertanyaan-triase` Pertanyaan 4).
2. **Reproduksibilitas:** ulangi pemeriksaan minimal 2× (konfigurasi DNS/TLS bisa berubah); simpan output mentah perintah.
3. **Higienitas bukti:** sensor alamat email pribadi dan data internal target yang tidak relevan sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `openssl s_client`, `testssl.sh`, `sslyze` | Pemeriksaan TLS/cipher/sertifikat/HSTS |
| `dig` (AXFR, TXT, CNAME), `dnsrecon` | Pemeriksaan DNS dan transfer zona |
| `mcp-osint` (`dns_email_security`, `dns_spf_chain`) | Recon SPF/DKIM/DMARC pasif |
| Mailbox uji sendiri | Satu-satunya penerima email spoof uji |
| `~/workspace/catatan/log-bug-bounty.md` | Log pemeriksaan + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + domain]
Pemeriksaan: [TLS | DNS | Email-auth + hasil pasif]
Pembuktian dampak: [apa yang dibuktikan ke akun/mailbox sendiri + bukti]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Domain] - [Kelas: TLS Downgrade / Email Spoofing / DNS AXFR] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-tls-network`, 6 laporan), bukan pengalaman teruji — tiap kelas butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Banyak program secara eksplisit mengecualikan "missing SPF/DMARC/DKIM" dan "missing security headers" — baca pasal out-of-scope program SEBELUM menguji; bila dikecualikan, jangan buang waktu.
- Pemeriksaan TLS/DNS bersifat pasif dan aman, tetapi pembuktian spoofing email tetap butuh kehati-hatian: satu email nyasar ke orang lain sudah cukup merusak reputasi akun hunter.
