# Skill: Kebersihan Worktree — Bersihkan Salinan Repo Lokal Sebelum Pemindaian Kode

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/referensi-skill-langka-high-critical-2026-11-24.md` Bagian 1 (Worktree Hygiene, khusus audit kode). Seluruh isi di bawah ini adalah ringkasan riset, bukan pengalaman teruji sampai ada satu repo yang dibersihkan dengan skill ini dan dipakai untuk audit yang dicatat di log.

## Pemicu (Trigger & Scope)

Dipakai SETIAP KALI repo lokal akan dipindai / diaudit kodenya — sebelum `kopilot-analisis-kode`, `analisis-statis-js`, `skill-trail-of-bits`, atau pemindaian kode lain apa pun dimulai. Satu repo = satu kali pembersihan sebelum pemindaian pertama. Bila repo sudah dibersihkan dan tidak ada perubahan pada salinannya, jangan bersihkan ulang — pakai manifest pembersihan yang sudah ada.

Skill ini adalah **persiapan worktree**: tugasnya menyingkirkan direktori dan berkas yang mendistorsi konteks — kode pengujian, benchmark, dokumentasi, dan file instruksi bawaan repo — supaya agen tidak melaporkan kerentanan palsu di kode pengujian dan tidak terdistorsi konteks pengembang. Skill ini BUKAN analisis kode (itu tugas skill pemindai) dan BUKAN penilaian temuan (itu tugas `gerbang-tujuh-pertanyaan-triase` + `skeptic-false-positive-eliminator`).

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A58 Vulnerability Researcher** | Menyalin repo, membersihkan salinan, menulis manifest, menyerahkan salinan bersih ke pemindai |
| Audit | **A60 Security Auditor** | Memeriksa manifest + salinan bersih sebelum pemindaian dimulai; A60 tidak meloloskan karyanya sendiri |
| Pemimpin | **Muse** | Memutuskan salinan bersih dipakai untuk pemindaian atau dibersihkan ulang |

## Sudah tercakup (jangan diduplikat)

- **Cara mengarahkan kopilot membaca kode** (pertanyaan sempit, peta, chunking, kutipan baris) ada di `kopilot-analisis-kode` — skill ini berjalan SEBELUM kopilot dibuka: kopilot hanya menerima salinan yang sudah bersih, bukan repo mentah.
- **Pembedahan file JS + source map** ada di `analisis-statis-js` — skill ini menyiapkan bahan mentahnya (salinan bersih), bukan mengulang pembedahannya.
- **Checklist review kode langkah-demi-langkah** ada di `skill-trail-of-bits` — skill ini bukan checklist itu; skill ini memastikan checklist itu dijalankan pada kode produksi, bukan pada kode pengujian.
- **Temuan di kode pengujian yang tetap lolos ke triase** ditolak di hilir oleh `daftar-tolak-selalu` Pola 1 (dead code / kode tak tereksekusi) — skill ini adalah pencegahan di hulu; daftar-tolak adalah jaring pengaman kedua.
- Alur sesudah skill ini: salinan bersih + manifest → `kopilot-analisis-kode` (hipotesis) → `rekonstruksi-iterasi-payload` (pengujian) → `verifikasi-poc-aman` (bukti) → `daftar-tolak-selalu` → `gerbang-tujuh-pertanyaan-triase` → `gerbang-sinyal-dampak` → `skeptic-false-positive-eliminator` → `triase-duplikat` → draf laporan → tinjau manusia → persetujuan Cipta → kirim.

## Aturan keras

1. **Hanya program bounty resmi in-scope:** Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr. Di luar itu = jangan pindai.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain; tanpa mengubah/menghapus data pengguna lain.
3. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR).** Tanpa DoS/DDoS. Tanpa payload di permukaan publik.
4. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
5. **Tanpa laporan tanpa persetujuan Cipta.**
6. **Patuhi larangan otomasi program:** huntr "Humans only"; **Gray Swan dilewati total** (jangan disentuh).
7. **Larang aksi destruktif (DROP, DELETE, hapus data).** Penghapusan di skill ini HANYA berlaku untuk berkas di dalam SALINAN LOKAL repo (lihat Gerbang 0) — tidak pernah menyentuh data server target.
8. **Penghapusan HANYA pada SALINAN LOKAL repo di workspace sendiri — bukan repo target, bukan upstream, bukan di tempat lain.** Jangan pernah menghapus berkas di repositori target, di remote/upstream, atau di checkout asli yang bukan salinan audit. Bila ragu apakah direktori itu salinan atau aslinya — BERHENTI, jangan hapus apa pun, tanya Muse.
9. **Jangan hapus AGENTS.md Pusat Komando / file kerja sendiri.** Yang boleh dihapus hanya `AGENTS.md` (dan file instruksi sejenis) MILIK REPO YANG DIAUDIT, di dalam salinannya. `~/AGENTS.md`, `~/workspace/catatan/`, data Pusat Komando, dan file kerja tim TIDAK PERNAH masuk daftar hapus — bila path penghapusan menyentuh salah satunya, BERHENTI.
10. **Kode yang dianalisis harus legal dibaca** — repo publik, kode milik sendiri, atau kode yang program bounty izinkan untuk diaudit. Jangan membaca kode hasil curian/bocoran.
11. **Satu gerbang gagal = BERHENTI, jangan pindai.** Salinan yang belum bersih = pemindaian belum boleh dimulai. Perbaiki gerbangnya, jangan memindai dari salinan kotor "sambil jalan".

## Langkah + gerbang

### Gerbang 0 — Salin dulu, jangan sentuh aslinya

1. Buat SALINAN repo ke direktori audit di workspace sendiri, mis. `~/workspace/tmp/audit-<program>-<repo>/salinan/` — salinan inilah yang dibersihkan dan dipindai. Repo asli / checkout asli / remote TIDAK PERNAH disentuh.
2. Periksa sebelum menyalin: salinan berasal dari sumber legal (repo publik, kode milik sendiri, atau kode yang program izinkan diaudit) dan programnya in-scope. Catat sumber + commit/versi yang disalin.
3. **Standar lulus:** path salinan tertulis; path itu berada di dalam workspace sendiri (`~/workspace/tmp/...`); sumber + versi tercatat. **Gagal = BERHENTI** — jangan lanjut ke Gerbang 1.

### Gerbang 1 — Hapus direktori dan berkas pengganggu (hanya di dalam salinan)

Hapus dari DALAM salinan (Gerbang 0) saja — dengan path eksplisit, satu per satu, dan catat tiap yang dihapus ke manifest (Gerbang 2):

**Direktori yang dihapus:**
- `test`, `tests`, `__tests__`, `spec`, `specs` — kode pengujian (sumber utama kerentanan palsu: celah di kode tes bukan celah produksi).
- `benchmark`, `benchmarks` — kode pengukuran kinerja, bukan kode produksi.
- `docs`, `doc` — dokumentasi (contoh kode di docs sering tidak lengkap / tidak aman dengan sengaja).
- `examples`, `example`, `fixtures`, `samples` — contoh dan data uji, bukan kode produksi.

**Berkas dan direktori instruksi bawaan repo yang dihapus:**
- `.github` — instruksi CI / alur kerja pengembang repo.
- `.cursor` — aturan dan konteks pengembang repo.
- `AGENTS.md`, `CLAUDE.md` — file instruksi bawaan repo untuk agen AI (konteks pengembang yang mendistorsi penilaian agen audit).
- `CONTRIBUTING.md` — panduan kontributor (bukan kode produksi).

**Yang TIDAK boleh dihapus:**
- Kode sumber produksi (`src/`, `lib/`, `app/`, paket inti, dan sejenisnya) — walau ada yang terlihat "mencurigakan", itu bahan audit.
- Berkas konfigurasi build / dependensi (`package.json`, `go.mod`, `requirements.txt`, `Cargo.toml`, dan sejenisnya) — dibutuhkan untuk memahami apa yang benar-benar dipakai produksi.
- `README.md` di akar repo — dibaca sebagai konteks (apa repo ini), bukan dihapus; README di subdirektori yang sudah terhapus ikut terhapus bersama direktorinya.
- AGENTS.md Pusat Komando, `~/workspace/catatan/`, dan semua file kerja tim sendiri — TIDAK PERNAH disentuh (aturan keras 9).

**Standar lulus:** semua direktori/berkas dari daftar di atas yang ADA di salinan sudah dihapus; tidak satu pun berkas produksi terhapus; tiap penghapusan tercatat di manifest. **Gagal = BERHENTI** — bila ada direktori dari daftar yang tidak bisa dihapus (mis. izin), catat dan lanjutkan HANYA bila A60 menyetujui pengecualian tertulis; bila tidak, berhenti.

### Gerbang 2 — Verifikasi salinan bersih + tulis manifest

1. Daftarkan isi salinan sesudah dibersihkan (daftar direktori tingkat atas + jumlah berkas sebelum/sesudah). Pastikan tidak ada lagi direktori `test` / `benchmark` / `docs` / `.github` / `.cursor` yang tersisa di salinan.
2. Periksa keutuhan kode produksi: titik masuk utama masih ada (mis. `src/` / `app/` / berkas utama masih lengkap); salinan masih bisa dibaca (bukan kosong / rusak karena salah hapus).
3. Tulis manifest pembersihan ke `~/workspace/catatan/log-bug-bounty.md` (lihat Format output): path salinan, sumber + versi, daftar yang dihapus, jumlah berkas sebelum/sesudah, dan nama pemeriksa (A60).
4. **Standar lulus:** manifest lengkap; tidak ada direktori pengganggu tersisa; kode produksi utuh. **Gagal = BERHENTI** — bersihkan ulang dari salinan baru (Gerbang 0), jangan menambal salinan yang sudah rusak.

### Gerbang 3 — Serahkan salinan bersih ke pemindai

1. Beri tahu pemindai (A58 + kopilot) path salinan bersih + manifestnya. Pemindai HANYA membaca salinan ini — jangan membuka repo asli / salinan kotor selama audit.
2. Aturan selama pemindaian: temuan yang lokasinya ternyata berada di direktori/berkas yang SEHARUSNYA sudah dihapus (mis. kutipan kode dari `tests/`) = temuan TIDAK VALID — buang, jangan diteruskan ke hipotesis. Bila pemindai menemukan celah di contoh/docs yang terlewat penghapusan, catat sebagai "lolos pembersihan" dan kembali ke Gerbang 1.
3. **Standar lulus:** pemindai mengonfirmasi ia bekerja dari salinan bersih (path tercatat di log hipotesis). Tanpa konfirmasi itu, hipotesis dari pemindaian itu belum boleh maju ke pengujian.

## Alat

| Alat | Cara pakai |
|---|---|
| `cp -r` / `git clone` ke direktori audit | Membuat salinan repo (Gerbang 0) — sumber legal saja |
| `rm -rf <path-eksplisit-di-dalam-salinan>` | Menghapus direktori/berkas pengganggu — SATU path eksplisit per perintah, tidak pernah dengan wildcard di luar salinan, tidak pernah di luar `~/workspace/tmp/...` |
| `find <salinan> -maxdepth 2 -type d` + `find <salinan> -type f \| wc -l` | Verifikasi Gerbang 2: direktori tersisa + jumlah berkas sebelum/sesudah |
| `~/workspace/catatan/log-bug-bounty.md` | Manifest pembersihan + log hipotesis yang merujuk path salinan bersih |

## Human-in-the-loop

- A60 memeriksa manifest + salinan bersih sebelum pemindaian dimulai. Bila A60 menemukan direktori pengganggu yang tersisa atau berkas produksi yang ikut terhapus, pemindaian ditunda sampai salinan dibuat ulang.
- Keputusan "pengecualian" (direktori dari daftar yang dipertahankan karena alasan tertentu) hanya sah bila tertulis di manifest + disetujui A60 — bukan keputusan sepihak A58.

## Format output

Tulis manifest ke `~/workspace/catatan/log-bug-bounty.md` dengan format ini:

```
- [tanggal] Worktree: <program> / <repo> @ <commit/versi> | Sumber: <URL repo publik / milik sendiri>
  - Salinan: <path salinan di ~/workspace/tmp/...>
  - Dihapus: <daftar direktori/berkas yang dihapus, satu per baris>
  - Berkas: <jumlah sebelum> → <jumlah sesudah>
  - Verifikasi A60: <lolos / ditolak + alasan>
  - Dipakai untuk: <kopilot-analisis-kode / analisis-statis-js / skill-trail-of-bits — path salinan dicatat di tiap hipotesis>
```

Tiap hipotesis dari pemindaian salinan ini wajib mencantumkan path salinan bersihnya (lihat format output `kopilot-analisis-kode`). Hipotesis tanpa path salinan = belum bisa dilacak kebersihannya = jangan maju ke pengujian.

## Batasan yang diketahui

- Pembersihan ini hanya menyingkirkan konteks yang JELAS-JELAS bukan produksi. Kode produksi yang berisi contoh di dalamnya (mis. contoh di dalam `src/`) tetap bisa menyesatkan — pemindai tetap wajib membedakan "ada di kode" vs "saya duga" dengan kutipan baris (`kopilot-analisis-kode` Gerbang 4).
- Salinan yang dibersihkan bisa menjadi basi bila repo upstream berubah — bila audit berlanjut melewati perubahan upstream yang relevan, buat salinan baru dari versi terbaru dan ulangi Gerbang 0–2, jangan menambal salinan lama.
- Skill ini tidak menggantikan pemahaman dasar kerentanan — tanpa fondasi (lihat `fondasi-kerentanan-web-api`), hipotesis dari salinan bersih pun tidak bisa dinilai benar/salah.
