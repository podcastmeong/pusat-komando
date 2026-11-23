# Skill: Audit Smart Contract & Web3 — 10 Kelas Bug DeFi + PoC Foundry

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 55, Agentic-Bug-Hunter `web3-audit` + Claude-BugHunter `web3-audit`, 10 kelas bug DeFi), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program bounty (Immunefi, Code4rena, Sherlock, Cantina, atau program proyek DeFi) in-scope secara eksplisit mencakup smart contract / protokol DeFi.
- Ditemukan repositori kontrak target (GitHub in-scope) atau alamat kontrak yang sudah di-deploy dengan TVL yang relevan.
- Dipakai SEBELUM menyentuh kode: sinyal kill dulu, audit kemudian, PoC terakhir.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan audit kontrak + PoC Foundry lokal |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Metode audit kode secara umum + aturan deteksi** → skill `skill-trail-of-bits`. Skill ini TIDAK mengulang metode audit umum — hanya 10 kelas bug DeFi, sinyal kill, dan template PoC Foundry yang spesifik.
- **Audit paralel smart contract + web/API** (orkestrasi audit) → skill `skill-bountyforge`. Skill ini TIDAK mengulang orkestrasinya — hanya isi audit DeFi-nya. Foundry di `skill-bountyforge` hanya disebut sebagai tool (`forge test`, `cast call`); template PoC-nya ada di skill ini.
- **Rug pull / token meme** (honeypot, hidden mint, otoritas token) → skill `audit-meme-coin-token`. Skill ini soal bug LOGIKA DeFi pada kontrak yang sah, bukan soal token penipu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Immunefi, Code4rena, Sherlock, Cantina, program proyek DeFi yang terdaftar). Pastikan alamat kontrak / repositori yang diaudit tercantum in-scope sebelum analisis dimulai.
2. **Hanya akun sendiri + canary palsu.** Pengujian HANYA di fork lokal (Foundry `anvil` / fork mainnet lokal) dengan akun uji sendiri. **DILARANG bertransaksi di mainnet/testnet live dengan dana nyata atau dana orang lain.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang membanjiri jaringan atau menghabiskan gas secara berlebihan. PoC HANYA di fork lokal.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only terhadap jaringan live. **DILARANG:** mengeksekusi exploit di mainnet, menguras dana (sekalipun "untuk pembuktian"), atau mengubah state kontrak live. Semua PoC berjalan di fork lokal `anvil`.
11. **Jangan memakai dana nyata.** Bila PoC butuh token, pakai token palsu di fork lokal atau faucet testnet yang disediakan program — jangan pernah memakai dana Cipta atau dana orang lain.

## Langkah + gerbang

### Gerbang 0 — Sinyal kill pra-penyelaman (STOP sebelum audit bila ada yang kena)

Periksa SEBELUM membaca kode. Bila satu sinyal kill kena, JANGAN audit — catat alasannya dan pindah target.

| Sinyal kill | Ambang / tanda |
|---|---|
| TVL terlalu kecil | TVL di bawah ambang program (biasanya < $100rb–$1jt, cek aturan program) — dampak terlalu kecil untuk dibayar |
| Kontrak tidak terverifikasi | Source code tidak terverifikasi di Etherscan / tidak ada repo in-scope — tidak bisa diaudit |
| Sudah diaudit berkali-kali + tidak ada perubahan | Laporan audit terakhir sudah mencakup area yang sama dan kode tidak berubah sejak itu — kemungkinan duplikat tinggi |
| Program sudah tutup / contest selesai | Cek deadline program sebelum mulai (lihat `recon-pantau-program`) |
| Bukan DeFi sungguhan | Kontrak hanya token ERC20 polos tanpa logika DeFi — pakai `audit-meme-coin-token` bila ada indikasi rug pull, atau lewati |

### Gerbang 1 — Pemetaan kontrak & 10 kelas bug DeFi

Petakan kontrak target (fungsi, peran, aliran dana), lalu periksa tiap kelas di bawah. Standar lulus: tiap kelas dinyatakan "ada indikasi / tidak ada" dengan lokasi kode (file:baris).

| # | Kelas bug DeFi | Yang dicari |
|---|---|---|
| 1 | Accounting desync | Saldo internal (mapping) tidak sinkron dengan saldo aktual token (mis. setelah transfer langsung / fee-on-transfer / rebasing token) |
| 2 | Access control | Fungsi sensitif (mint, pause, set oracle, upgrade) tanpa `onlyOwner` / role check, atau role yang bisa diambil alih |
| 3 | Incomplete code path | Cabang yang tidak menangani kasus tepi (mis. `if` tanpa `else` saat harga 0, daftar kosong, atau token pertama) |
| 4 | Off-by-one | Pembulatan / batas yang salah satu (mis. `>` vs `>=`, pembagian sebelum perkalian, dust yang tertinggal) |
| 5 | Oracle manipulation | Harga dari satu sumber (spot price, TWAP pendek, atau oracle yang bisa dimanipulasi flash loan) tanpa validasi/staleness check |
| 6 | ERC4626 share inflation | Deposit pertama / share calculation yang memungkinkan inflasi share (donasi langsung ke vault sebelum deposit pertama) |
| 7 | Reentrancy | Panggilan eksternal sebelum update state (checks-effects-interactions dilanggar), termasuk cross-function dan read-only reentrancy |
| 8 | Flash loan | Fungsi yang mengasumsikan saldo/harga tidak berubah dalam satu transaksi — bisa dimanipulasi pinjaman kilat |
| 9 | Signature replay | EIP-712 / permit tanpa nonce, deadline, atau domain separator yang benar — signature bisa dipakai ulang lintas chain/kontrak |
| 10 | Proxy / upgrade | Proxy yang bisa di-upgrade oleh pihak yang salah, storage collision, atau fungsi init yang bisa dipanggil ulang |

### Gerbang 2 — PoC Foundry (fork lokal saja)

Untuk tiap indikasi dari Gerbang 1, tulis PoC dengan template di bawah dan jalankan di fork lokal (`anvil` / `forge test --fork-url`). Standar lulus: PoC menunjukkan kerugian/keuntungan yang terukur (jumlah token/ETH) ATAU dinyatakan tidak terbukti dengan alasan.

```solidity
// Template PoC Foundry — jalankan HANYA di fork lokal (anvil), JANGAN di mainnet
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "forge-std/Test.sol";

contract PoC_<NamaKelas> is Test {
    address target = <ALAMAT_KONTRAK_IN_SCOPE>; // dari scope program
    address attacker = address(0xA77A...);      // akun uji sendiri (fork lokal)
    address victim = address(0xBEEF...);        // akun uji sendiri (fork lokal)

    function setUp() public {
        vm.createSelectFork(vm.envString("FORK_URL")); // fork lokal, bukan mainnet live
        vm.label(attacker, "Attacker (akun uji sendiri)");
        vm.label(victim, "Victim (akun uji sendiri)");
    }

    function test_<namaSerangan>() public {
        uint256 saldoAwal = <ukur saldo / share / harga sebelum>;
        vm.startPrank(attacker);
        // ... langkah exploit (hanya di fork lokal) ...
        vm.stopPrank();
        uint256 saldoAkhir = <ukur sesudah>;
        assertGt(saldoAkhir, saldoAwal, "Exploit tidak menghasilkan keuntungan terukur");
        emit log_named_uint("Keuntungan (wei/token)", saldoAkhir - saldoAwal);
    }
}
```

Aturan PoC: (a) semua alamat adalah akun uji sendiri di fork lokal; (b) keuntungan HARUS terukur angkanya — klaim tanpa angka = TOLAK; (c) JANGAN pernah jalankan PoC di mainnet/testnet live.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = PoC fork lokal menunjukkan kerugian/keuntungan terukur + kelas bug teridentifikasi di kode. **TOLAK** = sekadar "pola mencurigakan" tanpa PoC, atau PoC yang hanya bekerja dengan asumsi yang tidak realistis (mis. attacker sudah jadi owner).
2. **Reproduksibilitas:** PoC bisa dijalankan ulang dengan `forge test` dan menghasilkan hasil yang sama; sertakan perintah + hash commit repo yang diaudit.
3. **Higienitas bukti:** sensor kunci privat, alamat dompet pribadi, dan data pengguna sebelum dilampirkan (`[REDACTED]`). JANGAN lampirkan private key fork lokal.

Hanya temuan yang lolos ketiga gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Foundry (`forge test`, `cast call`, `anvil`) | PoC + fork lokal; uji lokal, bukan jaringan live |
| `skill-trail-of-bits` | Metode audit kode + aturan deteksi (referensi, bukan diulang) |
| `skill-bountyforge` | Orkestrasi audit paralel (referensi, bukan diulang) |
| Etherscan / repo in-scope | Verifikasi source code + alamat kontrak |
| `~/workspace/catatan/log-bug-bounty.md` | Log kelas bug yang diperiksa + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + alamat kontrak / repo + commit hash]
Sinyal kill: [lolos / kena + alasan]
Kelas bug: [nomor + nama + lokasi file:baris]
PoC: [perintah forge test + keuntungan terukur]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Protokol] - [Kelas Bug DeFi] menyebabkan [Dampak Spesifik + Jumlah Terukur]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Agentic-Bug-Hunter + Claude-BugHunter `web3-audit`, 10 kelas bug DeFi), bukan pengalaman teruji — tiap kelas butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- PoC fork lokal membuktikan bug secara logis, tetapi triase program sering meminta PoC di testnet yang disediakan program — ikuti instruksi program bila ada testnet resmi, tetap tanpa dana nyata.
- Kelas 5 (oracle) dan 8 (flash loan) sering membutuhkan kondisi pasar tertentu — bila PoC hanya bekerja dengan asumsi harga/TVL yang tidak realistis, nyatakan asumsi itu dengan jujur di laporan.
- Jangan mengklaim "dana bisa dicuri $X" dari PoC fork lokal tanpa menghitung batas nyata (likuiditas pool, slippage, gas) — angka yang menggelembung merusak kredibilitas (lihat `skeptic-false-positive-eliminator`).
