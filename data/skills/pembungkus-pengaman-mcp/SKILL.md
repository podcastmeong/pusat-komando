# Skill: Pembungkus Pengaman MCP — Menilai Lapisan Pertahanan MCP Target

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi penilaian pertahanan dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 30; sumber: `Puliczek/awesome-mcp-security` — Tools dan Papers), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope memakai (atau mengklaim memakai) lapisan pertahanan MCP dan perlu dinilai apakah pertahanan itu benar-benar menegakkan kontrolnya.
- Ditemukan wrapper/pemantau/pemblokir MCP pada target: context-protector, MCP Guardian, MCP Defender, Defenter, MCP-Dandan.
- Saat triase butuh menilai: apakah celah yang ditemukan adalah kegagalan pertahanan, atau pertahanan memang tidak ada.
- Dipakai sebagai lensa PENILAI (defense evaluator), bukan sebagai panduan memasang pertahanan untuk target.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Memetakan pertahanan target, menguji apakah kontrolnya ditegakkan |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Penjaga scope dan batas kepercayaan DALAM kerja agen tim (bukan produk pertahanan MCP) → skill `scope-and-safety-guardian`, `analisis-batas-kepercayaan`.
- Isolasi runtime/container server MCP → skill `isolasi-runtime-mcp` (kontrol tersendiri, bukan wrapper/pemantau).
- Gateway/proxy MCP sebagai lapisan kontrol → skill `gateway-mcp-aman`.
- Skill ini KHUSUS produk pertahanan MCP konkret (wrapper, pemantau semantik, pemblokir lalu lintas) dan cara menilai apakah pertahanannya bekerja.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji pertahanan target.
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

### Gerbang 1 — Identifikasi lapisan pertahanan target

Petakan pertahanan MCP apa yang dipakai target (dari dokumentasi publik, header/respons, atau perilaku yang teramati). Kenali produknya dari README masing-masing (cek ulang sebelum mengutip):

| Produk | Sumber | Cara kerja yang diklaim |
|---|---|---|
| mcp-context-protector | `trailofbits/mcp-context-protector` | Wrapper keamanan server MCP |
| MCP Guardian | `eqtylab/mcp-guardian` (paper: MCP Guardian) | Penjaga/pemantau server MCP |
| MCP Defender | awesome-mcp-security → Tools | Pemblokir lalu lintas MCP berbahaya |
| Defenter | awesome-mcp-security → Tools | Pemantau semantik komunikasi agen–MCP |
| MCP-Dandan | awesome-mcp-security → Tools | Lapisan pengaman MCP |

Standar lulus: tiap lapisan pertahanan yang diklaim target tercatat dengan nama produknya (atau dinyatakan "tidak ada lapisan pertahanan yang teridentifikasi" dengan bukti). Jangan berasumsi produknya dari nama saja — verifikasi dari perilaku/respons.

### Gerbang 2 — Uji apakah kontrolnya ditegakkan

Untuk tiap lapisan, uji SATU kontrol per putaran dengan akun uji sendiri: (a) wrapper — apakah input berbahaya ke tool tetap diteruskan tanpa filter; (b) pemantau semantik — apakah komunikasi agen–MCP yang menyimpang tetap lolos; (c) pemblokir — apakah lalu lintas MCP berbahaya tetap sampai ke server. Gunakan hanya canary palsu dan aksi read-only. Standar lulus: tiap kontrol dinyatakan "ditegakkan" (dengan bukti pemblokiran) atau "gagal ditegakkan" (dengan bukti lolosnya).

### Gerbang 3 — Buktikan kegagalan dengan dampak nyata

Kegagalan kontrol HANYA maju bila dibuktikan dampaknya: data canary sendiri terbaca/keluar, tool sensitif terpicu tanpa otorisasi, atau instruksi beracun dari tool output diikuti agen. Ulangi 3× (perilaku agen probabilistik). Standar lulus: dampak teramati ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **"Pertahanan tidak ada" saja bukan temuan** — yang dilaporkan adalah kontrol yang diklaim ada tapi gagal, atau ketiadaan kontrol yang berujung dampak nyata.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumentasi produk pertahanan (README masing-masing) | Pahami kontrol yang diklaim sebelum menguji. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai saat menguji kontrol. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log lapisan pertahanan → kontrol diuji → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + fitur/server MCP]
Lapisan pertahanan: [nama produk + kontrol yang diklaim]
Kontrol diuji: [kontrol + cara uji]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [diblokir / lolos + bukti, persis]
Dampak terbukti: [data/aksi yang lolos, read-only]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Produk/Lapisan MCP] - [Kontrol yang gagal] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Pertahanan (produk + kontrol yang diklaim); Langkah Reproduksi (akun uji sendiri + log HTTP + bukti lolosnya kontrol); Rekomendasi Perbaikan (tegakkan kontrol di lapisan yang gagal, tambah konfirmasi manusia untuk aksi sensitif, catat dan alert saat kontrol dilewati).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap produk pertahanan butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Nama produk saja tidak membuktikan kontrolnya bekerja: verifikasi selalu dari perilaku yang teramati, bukan dari klaim dokumentasi.
- Beberapa pertahanan berjalan di sisi klien (bukan server) sehingga tidak bisa diuji dari luar — catat sebagai "tidak dapat diuji dari luar" bila begitu, jangan diklaim gagal.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan sekadar "pertahanan X tidak dipakai".

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- mcp-context-protector (Trail of Bits) — https://github.com/trailofbits/mcp-context-protector
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang diuji adalah gateway/proxy MCP (bukan wrapper/pemantau), pakai `gateway-mcp-aman`.
- Bila yang diuji adalah isolasi runtime/container, pakai `isolasi-runtime-mcp`.
- Bila pertahanan yang gagal adalah deskripsi tool beracun yang lolos, dalami dengan `peracunan-deskripsi-tool-mcp`.
