# Skill: Perburuan GraphQL Fintech — Kerentanan Logika Uang (Mutasi, IDOR Ledger, Presisi Desimal, Idempotency)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 44, sumber: Claude-BugHunter `hunt-fintech-graphql`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target fintech (dompet, pembayaran, investasi, kartu) memakai GraphQL dan punya mutasi terkait uang: transfer, redemption, withdrawal, top-up kartu, atau perubahan saldo/portofolio.
- Ada sinyal: endpoint `/graphql` aktif, mutasi uang tidak memakai idempotency-key, atau query ledger/saldo menerima ID objek yang bisa diubah.
- Dipakai SETELAH skema GraphQL dipetakan dengan `introspeksi-graphql`.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A55** | Memetakan mutasi uang + menguji logika uang satu per satu |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap pola memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Introspeksi GraphQL / rekonstruksi skema secara umum → skill `introspeksi-graphql`. Skill ini memakai skema hasil skill itu, lalu menguji LOGIKA UANG di atasnya — bukan mengulang introspection.
- IDOR umum (akses objek milik pengguna lain) → skill `access-control-differential-analyst`. Di sini IDOR spesifik pada query ledger/saldo/portofolio fintech.
- Race condition umum → skill `perburuan-kerentanan-spesifik` Gerbang 1.2 dan `serangan-paket-tunggal-http2`. Di sini race spesifik pada bypass idempotency-key mutasi uang.
- Pelompakan alur / state machine → skill `pelompakan-alur-state-machine` (alur umum; di sini alur mutasi uang fintech).

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh endpoint GraphQL fintech berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri (minimal dua akun: Akun A dan Akun B, keduanya milik sendiri).
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only.
11. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali dinyatakan berlaku di skill itu.

### PAGAR KHUSUS — pengujian mutasi uang (bagian dari Aturan keras, WAJIB dibaca sebelum Gerbang 2)

- **Pengujian mutasi uang HANYA dengan akun uji sendiri, tanpa merugikan pihak lain, tanpa menyentuh dana nyata.** Semua mutasi (transfer, redemption, withdrawal, top-up) dilakukan ANTAR AKUN UJI MILIK SENDIRI, dengan jumlah MINIMAL yang diizinkan sistem (atau jumlah uji yang disediakan program/sandbox bila ada).
- **Gunakan mode sandbox / akun uji program bila tersedia.** Bila program menyediakan lingkungan sandbox atau dana uji, pakai itu — jangan uji mutasi uang di produksi bila sandbox tersedia.
- **Jangan pernah menarik dana ke rekening/bank sungguhan, jangan pernah mengirim dana ke pengguna sungguhan, dan jangan pernah mengubah saldo akun orang lain.** Bila mutasi terbukti berhasil ganda (idempotency bypass), BERHENTI segera setelah bukti pertama tercatat — jangan mengulang untuk "memperbesar" jumlah, dan laporkan kelebihan saldo yang tercipta di akun uji sendiri ke A60/Muse agar bisa dikembalikan/dilaporkan ke program.
- **Catat saldo sebelum dan sesudah tiap mutasi uji** (akun uji sendiri) agar dampak terukur dan dapat dipertanggungjawabkan.

## Langkah + gerbang

### Gerbang 1 — Petakan skema + mutasi uang

1. **Petakan skema:** pakai `introspeksi-graphql` — simpan daftar query (`ledger`, `balance`, `portfolio`, `transactions`) dan mutasi (`transfer`, `redeem`, `withdraw`, `topUp`, dan sejenisnya) beserta argumennya.
2. **Petakan alur uang normal:** lakukan satu mutasi sah antar akun uji sendiri (jumlah minimal) dan catat: saldo sebelum/sesudah, idempotency-key yang dipakai, respons sukses/gagal.
3. **Standar lulus:** daftar mutasi uang + alur normal + baseline saldo tercatat. Target tidak punya mutasi uang di GraphQL = STOP, skill ini tidak berlaku.

### Gerbang 2 — Uji pola logika uang satu per satu (satu pola = satu putaran, jumlah minimal)

Uji berurutan; tiap pola dicoba dari state bersih (saldo tercatat sebelum/sesudah).

#### Pola A — Mutasi pemindahan uang antar akun uji
Uji apakah mutasi `transfer`/`withdraw` bisa diarahkan ke akun yang bukan milik pengirim (hanya ke Akun B milik sendiri) atau dengan jumlah yang tidak semestinya (negatif, nol, melebihi saldo). **Terbukti bila:** mutasi dengan jumlah negatif/nol/melebihi saldo DITERIMA dan saldo berubah tidak semestinya — pada akun uji sendiri.

#### Pola B — IDOR pada query ledger / saldo / portofolio
Minta `ledger`/`balance`/`portfolio` milik Akun B memakai sesi Akun A (ubah ID objek di query). **Terbukti bila:** data keuangan Akun B (milik sendiri) terbaca dari sesi Akun A.

#### Pola C — Penyalahgunaan presisi desimal dan pembulatan
Uji mutasi dengan jumlah berpresisi aneh (mis. `0.001`, banyak desimal, pembulatan ke bawah/atas) dan lihat apakah saldo berubah lebih dari yang seharusnya. **Terbukti bila:** selisih pembulatan menguntungkan pengirim secara berulang dan terukur pada akun uji sendiri.

#### Pola D — Bypass idempotency-key (eksekusi ganda)
Kirim mutasi yang SAMA (jumlah minimal, antar akun uji sendiri) dua kali dengan idempotency-key yang sama, lalu dengan key berbeda, lalu tanpa key. **Terbukti bila:** mutasi yang sama dieksekusi DUA KALI (saldo berubah dua kali) padahal key-nya sama — atau tanpa key tetap dieksekusi berulang. BERHENTI setelah bukti pertama; jangan mengulang untuk memperbesar jumlah.

#### Pola E — Redemption / top-up ganda
Uji apakah voucher/kode redemption atau top-up kartu bisa dipakai berulang (kirim ulang request redemption yang sama). **Terbukti bila:** redemption yang sama memberi saldo dua kali pada akun uji sendiri. BERHENTI setelah bukti pertama.

### Gerbang 3 — Gerbang validasi laporan

1. **Dampak keamanan nyata — standar lulus:** saldo/data keuangan berubah tidak semestinya ATAU data keuangan akun uji lain terbaca — terukur dari saldo sebelum/sesudah. **TOLAK** = mutasi ditolak server, atau perubahan saldo sesuai dengan yang seharusnya.
2. **Reproduksibilitas deterministik — standar lulus:** ulangi pola yang sama minimal 2× (jumlah minimal, antar akun uji sendiri). Gagal direproduksi = TOLAK. Pengecualian: Pola D/E yang terbukti eksekusi ganda cukup dibuktikan 1× + bukti saldo, lalu BERHENTI (jangan ulangi untuk memperbesar).
3. **Higienitas bukti — standar lulus:** sensor token sesi, nomor akun, dan data pribadi pada log HTTP sebelum dilampirkan (`[REDACTED]`); lampirkan saldo sebelum/sesudah (akun uji sendiri). Bukti tanpa sensor = TIDAK BOLEH maju ke laporan.

Hanya temuan yang lolos ketiga gerbang di atas yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dua akun uji sendiri (Akun A / Akun B) | Wajib untuk semua pola. Keduanya milik sendiri. |
| Skema GraphQL (dari `introspeksi-graphql`) | Daftar query + mutasi uang + argumennya. |
| Proxy HTTP (Burp/mitmproxy) | Mengirim query/mutasi GraphQL; simpan raw request/response. |
| Catatan saldo (sebelum/sesudah) | Saldo akun uji sendiri tiap mutasi; bukti dampak terukur. |
| `~/workspace/catatan/log-bug-bounty.md` | Log skema + mutasi + saldo + hasil tiap pola + keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program fintech + endpoint GraphQL]
Mutasi uang: [transfer / redeem / withdraw / topUp / ...]
Saldo sebelum: [Akun A: ... | Akun B: ...] | Saldo sesudah: [Akun A: ... | Akun B: ...]
Pola diuji: [A/B/C/D/E + nama pola + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Mutasi GraphQL] - [Pola Logika Uang] menyebabkan [dampak saldo/data keuangan]`. Isi laporan: Ringkasan (mutasi + pola); Langkah Reproduksi (akun uji + jumlah minimal + log HTTP + saldo sebelum/sesudah); Rekomendasi Perbaikan (validasi jumlah di server — tolak negatif/nol/melebihi saldo; otorisasi per objek pada query ledger; presisi desimal tetap — pakai integer minor unit; idempotency-key wajib + disimpan + dicek sebelum eksekusi; redemption sekali pakai).

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-fintech-graphql`), bukan pengalaman teruji — tiap pola butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Bila program menyediakan sandbox/dana uji, WAJIB pakai itu — jangan uji mutasi uang di produksi bila sandbox tersedia.
- Kelebihan saldo yang tercipta di akun uji sendiri selama pengujian HARUS dilaporkan ke A60/Muse dan ke program — jangan dibiarkan, jangan dipakai.

## Available connectors

- Browser (`browser.search`, `browser.open`) — riset dokumentasi publik program dan pola laporan GraphQL fintech.

## Websites

- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila skema GraphQL belum dipetakan, pakai dulu `introspeksi-graphql`.
- Bila fokusnya race condition umum (bukan idempotency mutasi uang), pakai `perburuan-kerentanan-spesifik` atau `serangan-paket-tunggal-http2`.
