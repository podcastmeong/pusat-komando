# Skill: Pelacakan Taint XSS DOM — Lacak Aliran Data Source ke Sink Berbahaya di Kode JS

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 6 butir 36 (DOM-Based XSS Taint Tracking). Jangan klaim metode ini terbukti sampai ada satu aliran source→sink yang lolos gerbang di bawah dan dicatat di log.

## Pemicu

Dipakai saat target web/API klasik in-scope memuat JavaScript yang membaca data kendali-pengguna (URL, `window.name`, pesan antar-frame, penyimpanan lokal) dan ada dugaan data itu sampai ke sink berbahaya tanpa sanitasi. Dipakai SETELAH `pemetaan-permukaan-serangan` langkah 4 mengumpulkan file JS target, dan SEBELUM pengujian dinamis (`verifikasi-xss`). Skill ini menemukan HIPOTESIS aliran taint secara statis — pembuktian eksekusi memakai `verifikasi-xss`.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A59 Threat Hunter** | Mengumpulkan file JS + melacak aliran source→sink |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + langkah uji dari aliran yang ditemukan |
| Audit | **A60 Security Auditor** | Memvalidasi aliran (source, sink, sanitasi) sebelum jadi target uji; tidak pernah meloloskan temuannya sendiri |
| Pemimpin | **Muse** | Memutuskan hipotesis mana yang dilanjutkan ke `verifikasi-xss` |

## Sudah tercakup (jangan diduplikat)

- **Workflow umum mengarahkan kopilot membaca kode** (pertanyaan sempit, chunking, kutipan baris) → `kopilot-analisis-kode`. Skill ini khusus **taint DOM XSS**: daftar source/sink + cara menelusur alirannya.
- **Pengumpulan file JS + inventaris endpoint** → `pemetaan-permukaan-serangan` langkah 4–5. Skill ini memakai daftar file itu, bukan mengumpulkannya ulang.
- **Definisi + standar bukti XSS secara umum** → `fondasi-kerentanan-web-api` (bagian XSS). Skill ini menambah cara menemukan varian DOM yang TIDAK lewat pantulan server.
- **Pembuktian eksekusi dinamis di headless browser** → `verifikasi-xss`. Skill ini berhenti di hipotesis aliran.
- **Source `postMessage` secara mendalam** (validasi `event.origin`, isi `event.data`) → `analisis-postmessage`. Bila aliran bermula dari `message`, serahkan analisis origin-nya ke skill itu.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser pengguna lain.
3. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
4. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan.
5. **Tanpa payload di permukaan publik.** Payload dan halaman pemicu jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
6. **Validasi human-in-the-loop.** Setiap aliran yang diklaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai hipotesis — jangan kirim hasil mentah otomatisasi.
7. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
8. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
9. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only: bukti eksekusi cukup mencetak `document.domain` / alert canary di browser/sesi sendiri, jangan mencuri sesi orang lain.
10. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu. Program AI menilai hasil/outcome pada agennya, bukan trik XSS klasik.
11. **Self-XSS umumnya TIDAK dibayar.** Aliran yang hanya menyerang diri sendiri (payload yang sama dimasukkan dan dieksekusi oleh akun yang sama, tanpa korban kedua) bukan temuan yang layak lapor — bukti yang dihitung adalah eksekusi saat dilihat akun/sesi kedua milik sendiri (lihat `verifikasi-xss`).

## Daftar source & sink (acuan kerja)

### Source — tempat data kendali-penyerang masuk

| Source | Catatan |
|---|---|
| `location.hash` | Sering TIDAK dikirim ke server — DOM XSS murni; periksa pemakaian setelah `#` |
| `location.search` / `location.pathname` | Via `URLSearchParams` atau parsing manual |
| `document.referrer` | Bisa dikendalikan penyerang lewat halaman perantara |
| `window.name` | Bertahan lintas navigasi; sering dilupakan |
| `document.cookie` | Bila cookie ditulis dari input pengguna |
| `localStorage` / `sessionStorage` | Data tersimpan yang pernah ditulis dari input |
| `event.data` (postMessage) | Lihat `analisis-postmessage` |
| Respons API / JSON yang dirender | Data server yang ternyata berisi input pengguna lama |

### Sink — tempat data menjadi kode

| Sink | Catatan |
|---|---|
| `innerHTML`, `outerHTML`, `insertAdjacentHTML` | Sink paling umum; periksa apakah data sampai tanpa encoding |
| `document.write` / `document.writeln` | Sink klasik, masih ada di kode lama |
| `eval()`, `new Function()`, `setTimeout`/`setInterval` (string) | Eksekusi string sebagai kode |
| `jQuery.html()`, `.append()` dengan string | Pembungkus `innerHTML` |
| `dangerouslySetInnerHTML` (React), `v-html` (Vue) | Sink framework — periksa data yang masuk |
| `location.href = "javascript:..."`, `location.assign` | Sink URL eksekusi |
| `element.src` / `href` dengan skema `javascript:` | Sink atribut |

## Langkah + gerbang

### Langkah 1 — Inventarisasi file JS target

Ambil daftar file JS dari indeks `pemetaan-permukaan-serangan` (langkah 4). Bila belum ada, kumpulkan file JS yang dimuat halaman in-scope (termasuk bundle dan source map `.js.map` bila tersedia). Catat tiap file: URL, ukuran, dan apakah diminifikasi/dapat dibaca.

**Standar lulus:** daftar file tertulis; file yang tidak bisa dibaca (ter-obfuscate berat) dicatat sebagai "belum dianalisis", bukan diasumsikan aman.

### Langkah 2 — Cari source dan sink

Cari di tiap file (grep/pencarian teks, atau AST bila tersedia) semua kemunculan source dan sink dari daftar di atas. Catat tiap kemunculan dengan file + baris + potongan kode.

**Standar lulus:** tiap file punya daftar source dan sink yang ditemukan (atau pernyataan "tidak ada source/sink dari daftar ini"); kemunculan tanpa file:baris = belum dicatat.

### Langkah 3 — Telusur aliran (taint tracking)

Untuk tiap pasangan source→sink yang berada di file/alur yang sama, telusuri jalannya data: variabel apa yang membawa data source, fungsi apa yang dilewati, apakah ada transformasi (encoding, `encodeURIComponent`, `textContent`, DOMPurify, sanitizer kustom) sebelum sink.

- Bila data sampai ke sink **tanpa sanitasi yang memadai** → hipotesis DOM XSS.
- Bila ada sanitasi (mis. DOMPurify, `textContent`, encoding konteks yang benar) → aliran AMAN; catat sanitasi-nya dan tutup.
- Bila tidak bisa dipastikan dari kode statis saja (alur lewat banyak fungsi/framework, data dari API) → tandai "butuh uji dinamis", jangan ditebak.

**Standar lulus (gerbang utama):** tiap hipotesis berisi (a) source + file:baris, (b) sink + file:baris, (c) rantai variabel/fungsi di antaranya, (d) penilaian sanitasi (ada/tidak + kenapa tidak cukup). Hipotesis tanpa rantai = dugaan, buang.

### Langkah 4 — Rumuskan hipotesis teruji

Tulis hipotesis dalam format: "Saya menduga [data dari source X di file Y:baris] sampai ke [sink Z di file W:baris] tanpa sanitasi karena [alasan], diuji dengan [payload canary + langkah konkret di `verifikasi-xss`]." Serahkan ke A60 untuk validasi.

**Standar lulus:** hipotesis punya lokasi kode, rantai aliran, dan langkah uji konkret. Hipotesis yang hanya berbunyi "mungkin rentan" = GAGAL, tulis ulang.

### Langkah 5 — Serahkan ke verifikasi dinamis

Hipotesis yang lolos A60 diteruskan ke `verifikasi-xss` untuk pembuktian eksekusi di headless browser. Skill ini TIDAK memutuskan keberhasilan — hanya `verifikasi-xss` + `skeptic-false-positive-eliminator` yang boleh menyatakan temuan terbukti.

**Standar lulus:** setiap hipotesis tercatat statusnya (lolos A60 / ditolak + alasan / diteruskan ke verifikasi).

## Alat

| Alat | Cara pakai |
|---|---|
| Daftar file JS dari `pemetaan-permukaan-serangan` | Sumber file yang dianalisis |
| Pencarian teks / AST parser JS | Cari source & sink; telusur variabel antar-fungsi |
| Kopilot AI (`kopilot-analisis-kode`) | Membantu membaca potongan kode rumit — jawaban wajib dikutip barisnya, jangan diterima mentah |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua aliran + hipotesis + validasi A60 |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + halaman/file JS]
Source: [mis. location.hash — file:baris]
Sink: [mis. innerHTML — file:baris]
Rantai aliran: [variabel/fungsi: source → ... → sink]
Sanitasi: [tidak ada / DOMPurify / textContent — kenapa (tidak) cukup]
Hipotesis: [satu kalimat + langkah uji yang diusulkan]
Validasi A60: [lolos / ditolak + alasan]
Status: [hipotesis / diteruskan ke verifikasi-xss / ditolak]
```

Hipotesis TIDAK dikirim sebagai laporan. Yang dikirim hanya temuan yang sudah terbukti lewat pengujian + audit A60 + persetujuan Cipta (lihat `laporan-abstrak`).

## Batasan yang diketahui

- Analisis statis mudah salah di dua arah: melewatkan aliran yang lewat framework/API (false negative) dan menuduh aliran yang sebenarnya disanitasi di tempat lain (false positive) — karena itu Langkah 3 mewajibkan penilaian sanitasi dan Langkah 5 mewajibkan verifikasi dinamis.
- Kode diminifikasi/obfuscate berat membuat penelusuran manual tidak andal; catat sebagai "belum dianalisis" dan serahkan ke Muse, jangan memaksa.

### Available connectors

Tidak ada konektor khusus untuk skill ini; file JS dibaca dari target in-scope lewat `pemetaan-permukaan-serangan`.

### Websites

- Dokumentasi/OpenAPI resmi target (sumber inventarisasi endpoint).
- Halaman aturan program resmi (sumber scope).

### Alternatives for better results

- Bila file JS terlalu besar untuk dibaca manual, dahulukan file yang memuat source dari daftar (cari `location.hash` / `window.name` dulu) — jangan membaca bundle dari baris pertama.
- Bila source map (`.js.map`) tersedia, pakai itu untuk memetakan bundle ke kode sumber aslinya sebelum menelusur aliran.
