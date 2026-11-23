# Skill: Audit Meme Coin & Token — Deteksi Rug Pull

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 56, Agentic-Bug-Hunter `meme-coin-audit` + Claude-BugHunter `meme-coin-audit`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program bounty in-scope secara EKSPLISIT mencakup token / meme coin / program audit token (mis. program audit token di Immunefi, Code4rena, atau program proyek token).
- Ditemukan token dengan otoritas mencurigakan, likuiditas yang bisa ditarik, atau pola honeypot saat memeriksa kontrak token.
- **Tanpa pencantuman token secara eksplisit di scope, skill ini TIDAK dipakai** — audit token di luar program bukan bounty, melainkan riset pasar.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan pemeriksaan otoritas token + likuiditas |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Audit smart contract DeFi umum (10 kelas bug logika) → skill `audit-smart-contract-web3`. Skill ini soal pola RUG PULL pada token, bukan bug logika DeFi pada protokol yang sah.
- Metode audit kode umum → skill `skill-trail-of-bits` dan `skill-bountyforge` (keduanya membahas smart contract umum, bukan rug pull token).

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN token tercantum eksplisit.** Bila program tidak mencantumkan token itu, JANGAN audit — temuan di luar scope tidak dibayar dan bisa dianggap pengujian tanpa izin.
2. **Hanya akun sendiri + canary palsu.** Pengujian HANYA di fork lokal / testnet program dengan akun uji sendiri. **DILARANG membeli/menjual token target dengan dana nyata.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang membanjiri jaringan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only terhadap jaringan live. **DILARANG:** mengeksekusi rug pull, menarik likuiditas, membekukan akun orang lain, atau mengubah otoritas token live. Semua pembuktian di fork lokal.
11. **Jangan memakai dana nyata dan jangan memperdagangkan token yang diaudit.** Audit ini untuk laporan bounty, bukan sinyal trading — jangan membeli token sebelum/sesudah audit, dan jangan membagikan hasil audit sebagai "sinyal beli/jual" ke publik.

## Langkah + gerbang

### Gerbang 1 — Pemeriksaan otoritas token (baca kode + state, tanpa transaksi)

Periksa kontrak token (EVM dan/atau Solana SPL) dari source terverifikasi / repo in-scope. Standar lulus: tiap otoritas tercatat "ada + pemegangnya" atau "sudah dicabut/dikunci" dengan bukti.

**EVM (ERC20 / token meme):**

| Pola rug pull | Yang diperiksa |
|---|---|
| Honeypot | Fungsi transfer yang hanya mengizinkan beli tapi menolak jual (mis. `require` yang gagal saat jual, atau daftar hitam penjual); uji dengan simulasi fork lokal, BUKAN transaksi live |
| Hidden mint | Fungsi `mint` yang masih bisa dipanggil owner / tanpa batas suplai (cap) |
| Manipulasi fee | Fungsi `setFee` / `setTax` tanpa batas — owner bisa menaikkan fee jual ke 99–100% |
| Bypass LP lock | Klaim "LP terkunci" tapi lock bisa dibatalkan, kedaluwarsa sebentar lagi, atau lock dipegang owner sendiri (bukan locker pihak ketiga) |
| Blacklist / pause sepihak | Owner bisa memasukkan alamat ke blacklist atau pause transfer kapan saja |

**Solana (SPL Token / Token-2022):**

| Pola rug pull | Yang diperiksa |
|---|---|
| Mint authority masih aktif | `mintAuthority` belum dicabut — pemilik bisa mencetak token tanpa batas |
| Freeze authority masih aktif | `freezeAuthority` belum dicabut — pemilik bisa membekukan akun pemegang token |
| Mutabilitas metadata | Metadata (nama, simbol, URI) masih bisa diubah — token bisa "berganti identitas" |
| Risiko ekstensi Token-2022 | Ekstensi berbahaya: transfer fee yang bisa diubah, confidential transfer, atau permanent delegate yang memberi kuasa penuh atas akun token |
| Serangan bonding curve & LP | Kurva bonding yang bisa dimanipulasi (harga awal, slope), atau LP yang belum dikunci/dibakar |

### Gerbang 2 — Pemeriksaan likuiditas

1. Di mana LP token berada (DEX mana, pair apa)? Berapa besar likuiditasnya, dan siapa yang memegang token LP?
2. Apakah token LP terkunci (locker pihak ketiga, durasi berapa lama) atau dibakar (burn address)? Bila dipegang owner = bisa ditarik kapan saja.
3. Apakah ada timelock / multisig pada fungsi owner? Satu kunci owner tanpa timelock = risiko rug pull lebih tinggi.

### Gerbang 3 — Pembuktian di fork lokal (tanpa transaksi live)

Untuk tiap indikasi dari Gerbang 1–2, buktikan di fork lokal (Foundry `anvil` untuk EVM; simulasi lokal untuk Solana):

- Honeypot: simulasikan beli lalu jual dengan akun uji sendiri di fork lokal — jual gagal = terbukti.
- Hidden mint / fee: panggil fungsi sebagai owner (di fork lokal, dengan kunci uji) dan tunjukkan efeknya (suplai bertambah / fee berubah).
- Freeze/mint authority Solana: tunjukkan otoritas masih aktif di state akun (bukti baca), tanpa mengeksekusinya di jaringan live.

### Gerbang 4 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = pola rug pull terbukti di fork lokal + otoritas/likuiditas terkonfirmasi dari state. **TOLAK** = sekadar "owner masih punya otoritas" tanpa menunjukkan bagaimana otoritas itu bisa merugikan pemegang (banyak token sah yang masih punya otoritas untuk upgrade yang sah — bedakan "otoritas ada" dari "otoritas bisa disalahgunakan untuk merugikan").
2. **Reproduksibilitas:** ulangi pemeriksaan state minimal 2× (state on-chain bisa berubah); simpan alamat kontrak + slot/field yang diperiksa.
3. **Higienitas bukti:** sensor alamat dompet pribadi dan data pengguna sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos keempat gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Etherscan / Solscan / repo in-scope | Verifikasi source code + baca state otoritas token |
| Foundry (`anvil`, `cast call`) | Simulasi fork lokal EVM (beli/jual, mint, fee) |
| Solana CLI / explorer | Baca `mintAuthority`, `freezeAuthority`, metadata, ekstensi Token-2022 |
| `audit-smart-contract-web3` | Bila temuan ternyata bug logika DeFi, bukan rug pull — pindah ke skill itu |
| `~/workspace/catatan/log-bug-bounty.md` | Log otoritas yang diperiksa + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alamat token + chain]
Otoritas: [mint / freeze / fee / blacklist + pemegang + status]
Likuiditas: [DEX + pair + status lock/burn LP]
Pembuktian fork lokal: [simulasi + hasil]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Token] - [Pola Rug Pull] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter + Claude-BugHunter `meme-coin-audit`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Skill ini HANYA dipakai bila program in-scope secara eksplisit mencakup token tersebut.** Audit token acak di luar program bukan bounty.
- "Owner masih punya otoritas" saja BUKAN temuan — banyak proyek sah yang mempertahankannya untuk upgrade darurat. Temuan harus menunjukkan JALUR penyalahgunaan yang konkret (mis. fee bisa dinaikkan ke 100% tanpa timelock, LP bisa ditarik karena tidak terkunci).
- Harga dan likuiditas berubah cepat — bukti state harus bertanggal dan bisa diverifikasi ulang oleh triager (sertakan slot/block height saat pemeriksaan).
- Jangan pernah memperdagangkan token yang diaudit atau membagikan hasil audit sebagai sinyal trading (Aturan keras 11).
