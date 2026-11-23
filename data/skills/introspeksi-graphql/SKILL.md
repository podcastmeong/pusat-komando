# Skill: Introspeksi GraphQL — Uji Introspection & Rekonstruksi Skema

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`), butir 17. Belum pernah dipakai dalam perburuan nyata oleh tim; query dan perilaku di bawah ini diambil dari riset, bukan pengalaman teruji. Uji dulu di lab sendiri sebelum dipakai di program bounty apa pun.

## Pemicu

Dipakai saat target punya endpoint GraphQL (biasanya `/graphql`, kadang `/api/graphql` atau `/v1/graphql`) dan skemanya perlu diketahui — untuk memetakan query/mutation/field yang tersedia sebelum pengujian. Dipakai pada tahap recon teknis; hasilnya masuk ke indeks aset (`pemetaan-permukaan-serangan`). Bukan untuk bounty agen AI — ini teknik web klasik.

## Pemilik

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A64 Web Application Tester** | Menguji introspection, merekam pesan error, merekonstruksi skema |
| Audit | **A60 Security Auditor** | Memvalidasi skema hasil rekonstruksi sebelum masuk indeks |
| Pemimpin | **Muse** | Putuskan endpoint GraphQL mana yang dipetakan dan kapan skema dinyatakan siap uji |

## Sudah tercakup (jangan diduplikat)

- **Penemuan endpoint `/graphql` itu sendiri** adalah bagian `penemuan-api-swagger` Gerbang 1 (path umum) — bila endpoint ditemukan di sana, skill ini yang melanjutkan pemetaan skemanya. Jangan mengulang pemeriksaan path di sini.
- **Inventaris endpoint REST** ada di `penemuan-api-swagger` — skill ini HANYA untuk GraphQL, bukan REST. Jangan campur keduanya dalam satu inventaris.
- **Pengujian celah pada field GraphQL** (IDOR antar field, otorisasi per field) BUKAN bagian skill ini — itu pengujian, lewat `rekonstruksi-iterasi-payload` + `access-control-differential-analyst`, setelah skema dipetakan.
- **Validasi temuan + laporan** ada di `triase-duplikat` + `laporan-abstrak`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr jalur audit kode OSV saja). Endpoint GraphQL di luar scope = jangan disentuh.
2. **Hanya akun sendiri + canary palsu.** Query hanya dengan akun tes sendiri; tanpa data orang lain; tanpa uji korban.
3. **Tanpa DoS/DDoS.** Introspection dan rekonstruksi memakai SEDIKIT query kecil; rate limit ≤5 req/detik; JANGAN mengirim query introspection raksasa berulang-ulang atau query rekursif dalam yang membebani server.
4. **Tanpa payload di permukaan publik.** Skill ini hanya MEMBACA skema — tidak mengirim mutation yang mengubah/menghapus data, tidak ada payload eksploitasi.
5. **Larang aksi destruktif (DROP, DELETE, hapus data) — dan larang MUTATION apa pun di skill ini.** Hanya query baca (introspection + field suggestion); mutation HANYA di tahap pengujian (`rekonstruksi-iterasi-payload`) dengan persetujuan manusia. Pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain) sesuai prinsip zero false-positive.
6. **Validasi human-in-the-loop; tanpa laporan tanpa persetujuan Cipta.** Skema hasil rekonstruksi bukan laporan — jangan kirim apa pun ke program dari skill ini.
7. **Patuhi larangan otomasi program** — huntr "Humans only" (jalur audit kode OSV saja); Gray Swan dilewati total.
8. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** kecuali dinyatakan berlaku di skill itu.
9. **Jangan meminta data asli lewat introspection.** Query introspection hanya meminta NAMA tipe/field, bukan isi data pengguna; bila respons mengembalikan data pengguna lain, HENTIKAN, sensor, dan laporkan ke Muse — jangan dibaca lanjut.
10. **Bila program melarang otomasi, rekonstruksi otomatis DILARANG** — lakukan manual (satu query saran field sekali jalan, ditinjau manusia) atau jangan jalankan; bila ragu, tanya Muse dulu.

## Langkah + gerbang

### Gerbang 0 — Kelayakan target

1. Pastikan program adalah program web/API klasik in-scope dan endpoint GraphQL-nya in-scope — baca halaman scope program, catat URL + tanggal cek.
2. Pastikan endpoint GraphQL sudah diketahui (dari `penemuan-api-swagger` atau dari JS/crawl) — skill ini tidak menebak-nebak URL endpoint.
3. **Standar lulus:** scope tertulis; endpoint GraphQL tertulis dengan sumber penemuannya. Endpoint tanpa sumber = jangan diuji.

### Gerbang 1 — Uji introspection (query standar)

1. Kirim SATU query introspection standar yang kecil (meminta daftar tipe + field tingkat atas saja, bukan seluruh skema bertingkat sekaligus): contoh pola `query { __schema { types { name kind } } }` — sesuaikan dengan dokumentasi GraphQL, jangan mengarang sintaks.
2. Catat respons: introspection AKTIF (skema dikembalikan) atau NONAKTIF (error/ditolak).
3. **Standar lulus:** status introspection tercatat (AKTIF/NONAKTIF + respons persis); bila AKTIF, lanjut ke Gerbang 2; bila NONAKTIF, lanjut ke Gerbang 3 (rekonstruksi dari error). Satu query saja di gerbang ini — jangan mengulang dengan variasi sebelum mencatat hasilnya.

### Gerbang 2 — Simpan skema bila introspection aktif

1. Unduh skema lengkap (tetap dalam batch kecil, bukan satu query raksasa) dan simpan ke folder kerja lokal (satu file per target + tanggal).
2. Susun inventaris dari skema: daftar query, mutation, dan field tiap tipe — beserta argumennya. Tandai mutation sensitif (hapus, ubah peran, baca massal) — tandai saja, JANGAN diuji di skill ini.
3. **Standar lulus:** skema tersimpan lokal; inventaris punya query/mutation/field + argumen; mutation sensitif ditandai. Skema yang tidak disimpan = belum selesai.

### Gerbang 3 — Rekonstruksi dari pesan error bila introspection nonaktif

1. Kirim query kecil dengan field yang SALAH secara sengaja (mis. field yang tidak ada) dan rekam pesan errornya: banyak server GraphQL membalas dengan saran field ("Did you mean ...?") atau daftar field yang valid.
2. Ulangi SATU field sekali jalan, dengan jeda, memakai saran dari error sebelumnya untuk menebak field berikutnya — rekonstruksi bertahap, bukan brute-force ribuan nama field.
3. Hentikan bila server berhenti memberi saran, mengembalikan error generik, atau mulai me-rate-limit — catat titik berhentinya.
4. **Standar lulus:** tiap field hasil rekonstruksi punya bukti pesan error yang menyebutkannya; field tanpa bukti error = dugaan, tulis sebagai dugaan, bukan fakta. Bila tidak ada saran sama sekali, tulis "skema tidak dapat direkonstruksi dari error" dan berhenti.

### Gerbang 4 — Serahkan ke indeks + audit

1. Serahkan inventaris skema (Gerbang 2 atau 3) ke A53 untuk dimasukkan ke indeks aset (`pemetaan-permukaan-serangan`), dengan catatan otorisasi tiap query/mutation (token/peran apa — bila belum diketahui, tulis "otorisasi belum diketahui" dan entri = BELUM DIPETAKAN).
2. A60 mengaudit: tiap field bisa dilacak ke respons introspection/error; tidak ada dugaan sebagai fakta; tidak ada mutation yang diuji di skill ini.
3. **Standar lulus:** audit A60 lolos; indeks diperbarui; entri tanpa otorisasi = BELUM DIPETAKAN dan tidak boleh diuji.

## Alat

| Alat | Cara pakai |
|---|---|
| Query GraphQL manual (curl / klien HTTP) | Kirim query introspection + query saran field satu per satu; simpan request/response. |
| Tool introspection GraphQL (mis. graphql-voyager / graphiql — pilih yang tersedia, jalankan lokal) | Menampilkan skema hasil Gerbang 2; JANGAN arahkan tool online pihak ketiga ke target (data target tidak boleh dikirim ke layanan luar). |
| `penemuan-api-swagger` Gerbang 1 | Sumber penemuan endpoint `/graphql`. |
| `scope-and-safety-guardian` | Penjaga scope + rate limit (≤5 req/detik). |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap sesi introspection. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Introspeksi GraphQL — <program/target/endpoint> — <tanggal>
- Endpoint: <URL> (sumber penemuan: <...>)
- Introspection: <AKTIF/NONAKTIF> (bukti: <respons ringkas>)
- Skema: <tersimpan di <path> / direkonstruksi dari error / tidak dapat direkonstruksi>
- Inventaris: <n> query, <n> mutation (<n> sensitif, ditandai saja), <n> field
- Per field hasil rekonstruksi: <nama field> | <bukti: pesan error yang menyebutkannya>
- Diserahkan ke indeks: <n> entri (otorisasi diketahui/belum)
- Audit A60: [lolos/ditolak + alasan]
- Status: SIAP UJI / BELUM SIAP (alasan)
```

### Available connectors

Tidak ada konektor khusus untuk skill ini; query dikirim lewat HTTP biasa.

### Websites

- Spesifikasi GraphQL (spec.graphql.org) — sintaks query introspection.
- Halaman aturan program resmi (sumber scope Gerbang 0).

### Alternatives for better results

- Bila introspection aktif: JANGAN rekonstruksi dari error — pakai skema lengkapnya (Gerbang 2), lebih cepat dan lebih akurat.
- Bila introspection nonaktif DAN error tidak memberi saran: berhenti — skema tidak bisa dipetakan dari luar; andalkan `analisis-statis-js` (string query GraphQL di file JS aplikasi) sebagai sumber alternatif.
- Bila endpoint GraphQL butuh autentikasi: pakai token akun tes sendiri saja; bila token itu tidak cukup untuk introspection, catat "introspection butuh peran lebih tinggi" dan serahkan ke Muse — jangan memakai token akun lain.
