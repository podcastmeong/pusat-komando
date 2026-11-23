# Skill: Isolasi Runtime MCP — Menilai Apakah Deployment MCP Target Terisolasi

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi penilaian isolasi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 33; sumber: `Puliczek/awesome-mcp-security` — Tools → ToolHive `StacklokLabs/toolhive`), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Target in-scope menjalankan server MCP dan perlu dinilai: apakah server itu berjalan terisolasi (container/sandbox) atau tanpa pembatas sehingga server jahat/tereksploitasi bisa mengakses file, kredensial, dan jaringan host.
- Ditemukan server MCP yang membaca file host, menjalankan perintah, atau mengakses jaringan tanpa batas yang jelas.
- Saat triase butuh menilai blast radius: bila satu server MCP terkompromi, apa saja yang bisa dijangkaunya.
- Dipakai sebagai lensa PENILAI isolasi deployment target — bukan panduan memasang ToolHive untuk target.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menilai isolasi deployment MCP target, menguji batas yang bisa dijangkau |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Suite alat pentest klasik lewat MCP → skill `mcp-security-hub`.
- Wrapper/pemantau/pemblokir MCP di sisi server → skill `pembungkus-pengaman-mcp` (kontrol perilaku, bukan isolasi runtime).
- Gateway/proxy MCP sebagai lapisan kontrol → skill `gateway-mcp-aman`.
- Skill ini KHUSUS isolasi runtime/container sebagai kontrol tersendiri (ToolHive: menjalankan server MCP dalam container/sandbox) dan cara menilai apakah deployment target sudah terisolasi atau masih berjalan tanpa pembatas.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri saat menguji batas isolasi.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain). JANGAN menghapus atau mengubah file host, JANGAN menjalankan perintah yang mengubah state.
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Petakan deployment MCP target

Petakan bagaimana server MCP target dijalankan: apakah ada tanda isolasi (container/sandbox, ToolHive, batasan filesystem/jaringan) atau justru berjalan langsung di host tanpa pembatas. Pahami model isolasi ToolHive dari README-nya (`StacklokLabs/toolhive` — cek ulang sebelum mengutip): server MCP berjalan dalam container agar server jahat atau tereksploitasi tidak bisa mengakses file, kredensial, dan jaringan host. Standar lulus: model deployment tercatat (terisolasi / tidak terisolasi / tidak dapat ditentukan dari luar) dengan bukti yang mendasarinya.

### Gerbang 2 — Uji batas yang bisa dijangkau, read-only saja

Uji SATU batas per putaran, hanya dengan akun uji sendiri, hanya read-only: (a) filesystem — apakah tool MCP bisa membaca file di luar direktori kerjanya (baca file canary sendiri yang diletakkan di luar direktori kerja, JANGAN file sistem/kredensial asli); (b) jaringan — apakah tool MCP bisa menjangkau alamat internal/metadata (callback canary milik sendiri saja); (c) kredensial — apakah variabel lingkungan/kredensial host terbaca lewat tool (hanya nilai canary palsu yang sengaja disiapkan, JANGAN kredensial asli). Standar lulus: tiap batas dinyatakan "tertahan" (dengan bukti penolakan) atau "tembus" (dengan bukti baca canary).

### Gerbang 3 — Buktikan tembusnya isolasi dengan dampak nyata

Tembusnya batas HANYA maju bila dibuktikan dampaknya: file canary di luar direktori kerja terbaca, callback canary dari jaringan internal diterima, atau nilai canary dari lingkungan host terbaca. Ulangi 3× (perilaku agen probabilistik). Standar lulus: dampak teramati ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **"Tidak memakai container" saja bukan temuan** — yang dilaporkan adalah batas isolasi yang terbukti tembus dengan dampak nyata.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Dokumentasi ToolHive (`StacklokLabs/toolhive`) | Pahami model isolasi yang benar sebelum menilai target. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai: file canary, callback canary, nilai canary di lingkungan. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log model deployment → batas diuji → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + server MCP]
Model deployment: [terisolasi / tidak terisolasi / tidak dapat ditentukan + bukti]
Batas diuji: [filesystem / jaringan / kredensial]
Langkah reproduksi: [akun uji + langkah + log HTTP]
Indikator teramati: [tertahan / tembus + bukti, persis]
Dampak terbukti: [canary yang terbaca/keluar, read-only]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Server MCP] - [Isolasi runtime tembus di batas X] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Deployment (model isolasi target + yang seharusnya); Langkah Reproduksi (akun uji sendiri + log HTTP + bukti canary); Rekomendasi Perbaikan (jalankan server MCP dalam container/sandbox seperti ToolHive, batasi filesystem dan jaringan per server, jangan wariskan kredensial host ke server MCP).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap batas isolasi butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Isolasi deployment sering tidak terlihat dari luar: bila tidak dapat ditentukan, catat begitu — jangan mengklaim "tidak terisolasi" tanpa bukti.
- Pengujian batas filesystem/jaringan WAJIB read-only dan hanya dengan canary sendiri — membaca file atau kredensial asli host adalah pelanggaran aturan keras 3 dan 10.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan sekadar "deployment tidak memakai container".

## Websites

- ToolHive — https://github.com/StacklokLabs/toolhive
- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang diuji adalah wrapper/pemantau MCP (bukan isolasi runtime), pakai `pembungkus-pengaman-mcp`.
- Bila yang diuji adalah gateway/proxy MCP, pakai `gateway-mcp-aman`.
- Bila server MCP yang tembus isolasinya adalah server RE (Ghidra/IDA), dalami dengan `rekayasa-balik-lewat-mcp`.
