# Skill: Penambangan Parameter — Temukan Parameter Tersembunyi (GET, POST/JSON, Header)

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 15. Belum pernah dipakai dalam perburuan nyata oleh tim; nama tool dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat sudah ada endpoint in-scope dari indeks aset (`pemetaan-permukaan-serangan`) dan endpoint itu diduga menerima parameter yang tidak terlihat di UI/dokumentasi — parameter tersembunyi di query string (GET), body (POST/JSON), atau HTTP header. Hasilnya adalah daftar parameter kandidat yang teruji ada/tidak, untuk diteruskan ke pengujian (`rekonstruksi-iterasi-payload`). Bukan untuk bounty agen AI — ini teknik web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menjalankan penambangan parameter, mencatat hasil per parameter |
| Audit | **A60 Security Auditor** | Memvalidasi parameter yang dinyatakan "ada" sebelum diteruskan ke pengujian |
| Pemimpin | **Muse** | Putuskan endpoint mana yang ditambang dan kapan daftar parameter dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Variasi nilai pada parameter yang SUDAH diketahui** ada di `rekonstruksi-iterasi-payload` Gerbang 4 — skill itu mengasumsikan parameternya sudah ada; skill ini MENEMUKAN parameternya. Jangan campur: temukan dulu (skill ini), baru variasikan nilainya (skill itu).
- **Fuzzing inline lewat Burp MCP** sudah ada sebagai tool di `mcp-burp-ultra` Gerbang 3 — itu eksekutornya; skill ini adalah WORKFLOW penambangannya (wordlist apa, permukaan apa, bagaimana membedakan "ada" vs "tidak ada").
- **Parameter yang terlihat dari JS/dokumentasi** sudah tercakup di `analisis-statis-js` dan `penemuan-api-swagger` — skill ini hanya untuk parameter yang TIDAK ditemukan di sana. Parameter yang sudah diketahui dari JS/dokumen jangan ditambang ulang.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Endpoint di luar scope = jangan ditambang.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Fuzzing hanya pada parameter/endpoint target in-scope, dengan rate limit maks **5 req/detik** (lihat `scope-and-safety-guardian`); jeda antar batch; hentikan bila server mengembalikan error massal.
4. **Tanpa payload di permukaan publik.** Parameter uji berisi nilai canary palsu yang tidak berbahaya; tidak ada payload eksploitasi di tahap penambangan (tahap ini hanya menanyakan "apakah parameter ini dikenali server?").
5. **Larang aksi destruktif (DROP, DELETE, hapus data).** Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Daftar parameter bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja; penambangan otomatis pada challenge huntr DILARANG); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Satu parameter kandidat, satu nilai uji yang tidak berbahaya.** Jangan mengirim nilai yang bisa mengubah/menghapus data (mis. `?admin=true`, `?role=admin` dengan nilai yang langsung mengubah peran) — bila parameternya sensitif, catat sebagai kandidat dan serahkan ke Muse sebelum menguji nilainya.
10. **Bila program melarang otomasi, penambangan otomatis DILARANG** — lakukan penambangan manual (satu parameter sekali jalan, ditinjau manusia) atau jangan jalankan; bila ragu, tanya Muse dulu.

## Langkah + gerbang

### Gerbang 0 — Pilih endpoint + permukaan

1. Pilih 1–3 endpoint dari indeks aset yang paling mungkin punya parameter tersembunyi (form dengan banyak field, endpoint pencarian/filter, endpoint admin).
2. Tentukan permukaan yang ditambang: query string (GET), body JSON/form (POST), dan/atau header HTTP — tulis ketiganya atau yang dipilih, dengan alasan.
3. **Standar lulus:** endpoint tertulis dengan metode + parameter yang SUDAH diketahui dari indeks; permukaan tertulis. Endpoint tanpa catatan otorisasi di indeks = jangan ditambang.

### Gerbang 1 — Siapkan wordlist + baseline

1. Siapkan wordlist parameter dari sumber yang sah: nama parameter yang umum (mis. `id`, `user_id`, `debug`, `admin`, `role`, `redirect`, `callback`, `sort`, `filter`, `page`, `limit`), plus nama yang ditemukan di JS/dokumentasi target (`analisis-statis-js`, `penemuan-api-swagger`).
2. Ambil BASELINE: kirim request normal tanpa parameter tambahan, simpan responsnya (status, panjang body, pola). Baseline inilah pembanding semua hasil.
3. **Standar lulus:** wordlist tercatat (sumber + jumlah entri); baseline tersimpan. Tanpa baseline, tidak ada hasil yang bisa dinilai — jangan mulai.

### Gerbang 2 — Tambang satu permukaan sekali jalan

1. Untuk tiap nama parameter dalam wordlist, kirim SATU request dengan parameter itu bernilai canary yang tidak berbahaya (mis. string acak `canary123`), pada SATU permukaan (GET dulu, lalu POST, lalu header — jangan campur permukaan dalam satu batch).
2. Bandingkan respons dengan baseline: status berubah, panjang body berubah signifikan, pesan error menyebut parameter itu, atau perilaku aplikasi berubah = kandidat "ada".
3. **Standar lulus:** tiap nama parameter punya verdict (ADA / TIDAK ADA / TIDAK JELAS) + bukti responsnya. Parameter tanpa perbandingan baseline = belum diuji.

### Gerbang 3 — Konfirmasi kandidat "ada"

1. Ulangi tiap kandidat ADA dengan nilai canary yang BERBEDA: bila respons berubah mengikuti nilai (mis. pesan error mengutip nilai itu, atau hasil filter berubah), parameter itu BENAR-BENAR diproses server.
2. Bila respons sama persis untuk dua nilai berbeda, turunkan verdict jadi TIDAK JELAS dan catat alasannya — jangan diteruskan sebagai parameter terbukti.
3. **Standar lulus:** tiap parameter yang diteruskan sudah lolos uji dua nilai berbeda; tidak ada parameter TIDAK JELAS yang diteruskan sebagai "ada".

### Gerbang 4 — Serahkan ke pengujian

1. Serahkan daftar parameter terkonfirmasi (nama + permukaan + bukti dua nilai) ke `rekonstruksi-iterasi-payload` untuk diuji nilainya, dan perbarui indeks aset (`pemetaan-permukaan-serangan`) dengan parameter baru itu.
2. **Standar lulus:** indeks diperbarui; daftar serah-terima berisi bukti per parameter; A60 mengaudit bahwa tidak ada parameter TIDAK JELAS yang lolos.

## Alat

| Alat | Cara pakai |
|---|---|
| Tool penambang parameter (Arjun atau x8 — pilih satu yang tersedia) | Menambang nama parameter dari wordlist pada GET/POST/header. Ambil cara pakai dari README repo resminya saat instalasi — jangan mengarang flag. Bila tidak ada tool, lakukan manual satu parameter sekali jalan (Gerbang 2). |
| Wordlist parameter | Dari sumber di Gerbang 1; simpan salinannya di folder kerja sesi. |
| Burp Suite (via `mcp-burp-official` / `mcp-burp-ultra`) | Pembanding manual: kirim ulang request dengan parameter kandidat dan baca responsnya. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi penambangan. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Penambangan parameter — <program/target/endpoint> — <tanggal>
- Alat: <Arjun/x8/manual + versi> | larangan otomasi program: <diizinkan/dilarang + sumber>
- Permukaan: <GET/POST/JSON/header>
- Wordlist: <n> entri (sumber: <...>)
- Baseline: <status + panjang body + hash ringkas>
- Hasil: <n> ADA, <n> TIDAK ADA, <n> TIDAK JELAS
- Per parameter ADA: <nama> | <permukaan> | <bukti nilai 1 → respons> | <bukti nilai 2 → respons>
- Diserahkan ke rekonstruksi-iterasi-payload: <n> parameter
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; penambangan dilakukan lewat HTTP langsung atau Burp lokal.

### Websites

- Repo Arjun / x8 di GitHub — cara pakai tool penambang parameter.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila program melarang otomasi: tambang manual — pilih 5–10 nama parameter paling mungkin dari JS/dokumentasi, uji satu per satu dengan Burp Repeater (`mcp-burp-repeater`), bukan wordlist massal.
- Bila semua respons identik dengan baseline (server mengabaikan parameter tak dikenal): catat sebagai "server mengabaikan parameter tak dikenal" dan hentikan penambangan di endpoint itu — jangan menaikkan volume.
- Bila parameter kandidat sensitif (`admin`, `role`, `is_admin`): JANGAN uji nilainya di skill ini — catat sebagai kandidat, serahkan ke Muse; pengujian nilainya lewat `rekonstruksi-iterasi-payload` dengan persetujuan manusia.
