# Skill: Gateway MCP Aman — Menguji Perantara MCP sebagai Lapisan Kontrol

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi pengujian gateway dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 31; sumber: `Puliczek/awesome-mcp-security` — Tools), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope menaruh perantara (gateway/proxy) antara LLM dan server MCP — dan perlu diuji apakah gateway itu benar-benar menegakkan autentikasi, otorisasi, dan pembatasan.
- Ditemukan pola gateway: Lasso MCP Gateway, MCPAuth, workers-mcp (Cloudflare), Pomerium sebagai proxy zero-trust + MCP.
- Saat triase butuh menilai: apakah celah ada DI gateway (kontrol dilewati) atau DI BELAKANG gateway (server langsung terekspos).
- Dipakai SEBELUM pengujian server MCP mendalam: petakan dulu apakah ada gateway dan apa yang ditegakkannya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Memetakan gateway target, menguji tiap kontrol gateway |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Suite alat pentest klasik lewat MCP (bukan arsitektur gateway) → skill `mcp-security-hub`.
- Rantai federasi identitas cloud (AWS STS/AssumeRole, Entra) → skill `serangan-cloud-iam-entra` — itu soal identitas cloud, bukan pola perantara MCP.
- Wrapper/pemantau/pemblokir MCP di sisi server → skill `pembungkus-pengaman-mcp`.
- Isolasi runtime/container server MCP → skill `isolasi-runtime-mcp`.
- Skill ini KHUSUS pola gateway/proxy MCP sebagai lapisan kontrol dan cara menguji apakah gateway benar-benar menegakkan kontrolnya.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh gateway/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji kontrol gateway.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan arsitektur gateway target

Identifikasi apakah target memakai gateway dan produk apa (dari dokumentasi publik, header/respons, atau perilaku). Kenali pola tiap produk dari README-nya (cek ulang sebelum mengutip):

| Produk/pola | Sumber | Peran sebagai kontrol |
|---|---|---|
| MCP Gateway (Lasso Security) | `lasso-security/mcp-gateway` | Perantara dengan autentikasi + otorisasi + pembatasan |
| MCPAuth | awesome-mcp-security → Tools | Auth enterprise untuk MCP |
| workers-mcp (Cloudflare) | awesome-mcp-security → Tools | Gateway MCP di atas Cloudflare Workers |
| Pomerium | awesome-mcp-security → Tools | Proxy zero-trust + MCP |

Standar lulus: arsitektur tercatat — klien → gateway (produk + kontrol yang diklaim) → server MCP (nama server + tool) — atau dinyatakan "tidak ada gateway yang teridentifikasi" dengan bukti. Catat juga: apakah server MCP bisa dijangkau LANGSUNG tanpa lewat gateway (bypass arsitektur)?

### Gerbang 2 — Uji tiap kontrol gateway, satu per putaran

Uji SATU kontrol per putaran, hanya dengan akun uji sendiri: (a) autentikasi — apakah request tanpa token/kredensial tetap diteruskan ke server; (b) otorisasi — apakah akun uji berhak rendah bisa memanggil tool sensitif lewat gateway; (c) pembatasan — apakah gateway membatasi tool/rate/scope yang dijanjikan, atau semua tool diteruskan apa adanya; (d) bypass langsung — apakah server MCP di belakang gateway bisa diakses langsung (melewati gateway). Standar lulus: tiap kontrol dinyatakan "ditegakkan" (dengan bukti penolakan) atau "gagal ditegakkan" (dengan bukti lolosnya).

### Gerbang 3 — Buktikan kegagalan dengan dampak nyata

Kegagalan kontrol HANYA maju bila dibuktikan dampaknya: data canary sendiri terbaca/keluar, tool sensitif terpicu tanpa otorisasi, atau server MCP dijangkau langsung tanpa autentikasi gateway. Ulangi 3× (perilaku agen probabilistik). Standar lulus: dampak teramati ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **"Gateway tidak ada" saja bukan temuan** — yang dilaporkan adalah kontrol gateway yang diklaim ada tapi gagal, atau server yang terekspos langsung di belakang gateway.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumentasi produk gateway (README masing-masing) | Pahami kontrol yang diklaim sebelum menguji. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai saat menguji kontrol; pakai dua akun (berhak rendah vs berhak tinggi) untuk uji otorisasi. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log arsitektur gateway → kontrol diuji → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + gateway/server MCP]
Arsitektur: [klien] → [gateway + produk + kontrol diklaim] → [server MCP + tool]
Kontrol diuji: [autentikasi / otorisasi / pembatasan / bypass langsung]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [ditolak / lolos + bukti, persis]
Dampak terbukti: [data/aksi yang lolos, read-only]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Gateway MCP] - [Kontrol yang gagal] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Arsitektur (alur klien → gateway → server + kontrol yang diklaim); Langkah Reproduksi (akun uji sendiri + log HTTP + bukti lolosnya kontrol); Rekomendasi Perbaikan (tegakkan auth/otorisasi di gateway, tutup akses langsung ke server di belakang gateway, batasi tool per peran).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap produk gateway butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Gateway bisa berjalan di infrastruktur yang tidak terlihat dari luar (mis. di dalam VPC target) — bila kontrolnya tidak bisa diamati dari luar, catat sebagai "tidak dapat diuji dari luar", jangan diklaim gagal.
- Akses langsung ke server di belakang gateway hanya diuji bila server itu sendiri in-scope; bila servernya out-of-scope, BERHENTI di gateway.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan sekadar "gateway X tidak dipakai".

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang diuji adalah wrapper/pemantau di sisi server (bukan perantara), pakai `pembungkus-pengaman-mcp`.
- Bila yang diuji adalah identitas/federasi cloud di belakang gateway, pakai `serangan-cloud-iam-entra`.
- Bila target bukan MCP (API web klasik), pakai `analisis-batas-kepercayaan` + `pengujian-bfla`.
