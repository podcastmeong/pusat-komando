# Skill: Latihan MCP Rentan — Lab Sendiri dengan Damn Vulnerable MCP Server

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi latihan dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 32; sumber: `Puliczek/awesome-mcp-security` — Tools → Damn Vulnerable MCP Server `harishsg993010`), bukan pengalaman teruji sampai ada teknik dari lab ini yang lolos triase di program nyata dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Sebelum menguji server MCP in-scope: latih dulu teknik eksploitasi MCP di lab sendiri agar teknik yang dibawa ke target sudah terbukti bekerja.
- Ada teknik MCP baru yang ingin dicoba tapi belum pernah dijalankan — jalankan DULU di lab, baru ke target.
- Saat butuh memahami cara kerja serangan MCP (tool beracun, kebocoran file, RCE lewat tool) tanpa risiko menyentuh target nyata.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan lab, mengeksploitasi kerentanan lab, mencatat teknik yang terbukti |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan teknik mana yang boleh dipindahkan ke program in-scope |

## Sudah tercakup (jangan diduplikat)

- Pengujian live di browser pada target nyata → skill `uji-live-browser`.
- Verifikasi PoC yang aman pada target nyata → skill `verifikasi-poc-aman`.
- Latihan agen AI melawan agen live (akademi Wraith) → kandidat 58 (latihan-primitif-akademi-wraith, kelompok lain) — yang itu latihan agen vs agen, yang ini lab MCP rentan.
- Skill ini KHUSUS lab latihan MCP (setara DVWA untuk MCP): Damn Vulnerable MCP Server di lingkungan sendiri; teknik yang terbukti di lab BARU dipindahkan ke program in-scope.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan seluruh fitur/server MCP berada dalam in-scope program sebelum pengujian dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri — di lab maupun di target.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.
12. **Lab HANYA di lingkungan sendiri.** Damn Vulnerable MCP Server dijalankan HANYA di VM/container lab milik tim yang bisa dibuang — tidak di mesin produksi, tidak di jaringan yang bisa dijangkau publik, tidak dengan data asli.

## Langkah + gerbang

### Gerbang 1 — Bangun lab sendiri

Jalankan Damn Vulnerable MCP Server (`harishsg993010/damn-vulnerable-mcp-server`, lihat README resminya untuk perintah instalasi — jangan mengarang flag) di container/VM lab milik tim yang bisa dibuang, tanpa akses dari internet, tanpa data asli, tanpa kredensial asli. Standar lulus: server lab merespons `tools/list`, terisolasi dari jaringan produksi, dan tidak ada data sensitif di dalamnya. Bila lab tidak bisa diisolasi = BERHENTI, jangan lanjut.

### Gerbang 2 — Eksploitasi kerentanan lab, satu per putaran

Eksploitasi kerentanan yang sengaja dibuat di lab, SATU per satu: baca deskripsi kerentanannya, rumuskan hipotesis, jalankan terhadap lab sendiri. Catat tiap teknik: apa pemicunya, apa yang berhasil, apa outputnya, dan kondisi apa yang membuatnya berhasil. Standar lulus: tiap teknik tercatat lengkap dengan langkah reproduksi di lab — teknik yang hanya "katanya berhasil" tanpa langkah tercatat = BELUM TERBUKTI, jangan dipindahkan.

### Gerbang 3 — Pindahkan teknik yang terbukti ke program in-scope

HANYA teknik yang terbukti di Gerbang 2 yang boleh dibawa ke target in-scope — dan hanya setelah cek scope program (Gerbang 0 program target) menyatakan permukaan itu in-scope. Di target, pakai hanya akun uji sendiri + canary palsu, bukti read-only, ulangi 3× (perilaku agen probabilistik). Standar lulus: teknik terkonfirmasi di target ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **Hasil lab BUKAN laporan** — yang maju hanya temuan di target nyata yang lolos validasi ini.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Damn Vulnerable MCP Server (`harishsg993010`) | Lab rentan; jalankan hanya di container/VM lab sendiri yang terisolasi. |
| Container/VM lab yang bisa dibuang | Satu-satunya tempat lab berjalan; hapus setelah sesi bila tidak perlu. |
| Akun uji sendiri + canary palsu | Satu-satunya data yang dipakai di target nyata. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log teknik lab → pemindahan ke target → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Lab: [Damn Vulnerable MCP Server + versi + tanggal sesi]
Teknik lab: [nama teknik + kerentanan lab yang dieksploitasi]
Langkah reproduksi di lab: [langkah + output]
Target: [program + server MCP in-scope]
Pemindahan: [langkah yang sama di target + akun uji + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dilatih / dipindahkan / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Server MCP] - [Teknik dari lab] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Teknik (asal lab + cara kerja); Langkah Reproduksi di target (akun uji sendiri + log HTTP); Rekomendasi Perbaikan (perbaiki kerentanan yang sama seperti di lab: validasi input, batasi tool, konfirmasi manusia).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — lab ini belum pernah dijalankan tim; instalasi pertama WAJIB dicatat hasilnya sebelum dijadikan rutinitas.
- Kerentanan di lab sengaja dibuat dan bisa jadi TIDAK ADA di target nyata — teknik lab adalah hipotesis, bukan bukti.
- Lab yang terekspos ke internet menjadi risiko keamanan tim sendiri — Gerbang 1 (isolasi) tidak boleh dilewati dengan alasan apa pun.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome di target nyata, bukan keberhasilan di lab.

## Websites

- Damn Vulnerable MCP Server — https://github.com/harishsg993010/damn-vulnerable-mcp-server
- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila butuh verifikasi PoC di target nyata (bukan lab), pakai `verifikasi-poc-aman`.
- Bila butuh pengujian live di browser target, pakai `uji-live-browser`.
- Bila teknik dari lab adalah deskripsi tool beracun, dalami dengan `peracunan-deskripsi-tool-mcp`.
