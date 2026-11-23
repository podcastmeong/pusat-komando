# Skill: Analisis Active Directory Lewat MCP — Pemetaan Jalur Serangan AD/Azure AD dengan BloodHound & RoadRecon

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi analisis AD lewat MCP dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 3, kandidat 35; sumber: `Puliczek/awesome-mcp-security` — MCP Security Servers → BloodHound-MCP-AI, RoadRecon MCP), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program in-scope secara eksplisit mencantumkan aset Active Directory / Azure AD (Entra ID) sebagai target, dan perlu dipetakan jalur serangannya lewat MCP.
- Ditemukan server MCP BloodHound-MCP-AI atau RoadRecon MCP yang bisa dipakai untuk membaca graf hubungan AD/Azure AD.
- Saat butuh menemukan jalur eskalasi (user → grup → admin → domain) dari data graf, bukan dari tebakan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A56** | Menjalankan analisis graf AD/Azure AD lewat MCP, menemukan jalur eskalasi |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi Gerbang 3 |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- OSINT umum lewat MCP (37 tools, 12 sumber publik) → skill `mcp-osint` — itu recon data publik, bukan pemetaan graf AD.
- Enumerasi bucket/aset cloud → skill `enumerasi-aset-cloud`.
- Rantai federasi identitas cloud (AWS STS/AssumeRole, Entra) → skill `serangan-cloud-iam-entra` — itu soal rantai federasi/assume-role, bukan pemetaan graf AD lewat MCP.
- BloodHound sebagai satu baris tool di dalam suite klasik → skill `mcp-security-hub` (hanya disebut sebagai tool yang termasuk di hub, tanpa metodologi analisis graf).
- Skill ini KHUSUS analisis AD/Azure AD lewat server MCP (BloodHound-MCP-AI, RoadRecon MCP): membaca graf hubungan dan menemukan jalur eskalasi — HANYA pada lingkungan in-scope yang diizinkan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan aset AD/Azure AD yang dianalisis TERTULIS in-scope di program — bila tidak tertulis, BERHENTI.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya akun uji milik sendiri; jangan sentuh akun, grup, atau data pengguna lain.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain). JANGAN mengubah keanggotaan grup, JANGAN mereset kredensial, JANGAN mengubah kebijakan AD.
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.
12. **JANGAN sentuh AD/Azure AD di luar scope.** Analisis ini HANYA pada lingkungan in-scope yang diizinkan secara tertulis. AD produksi perusahaan lain, tenant Entra yang tidak tercantum, dan domain yang tidak disebut di program = DILARANG.

## Langkah + gerbang

### Gerbang 1 — Konfirmasi scope tertulis, lalu kumpulkan data graf

Konfirmasi DULU dari halaman program: aset AD/Azure AD apa yang in-scope (nama domain/tenant, apa yang boleh diuji). Tulis kutipan scope-nya ke log. Bila tidak ada penyebutan AD/Azure AD = BERHENTI, skill ini tidak boleh dipakai. Setelah itu kumpulkan data graf dengan server MCP (cek README masing-masing sebelum memakai — jangan mengarang flag):

| Server MCP | Kegunaan |
|---|---|
| BloodHound-MCP-AI | Memetakan jalur serangan di domain AD lewat graf BloodHound |
| RoadRecon MCP | Memetakan Azure AD (Entra ID) — pengguna, grup, aplikasi, peran |

Standar lulus: scope tertulis tercatat; data graf terkumpul dari lingkungan in-scope saja; tidak ada data dari domain/tenant di luar scope.

### Gerbang 2 — Baca graf, temukan jalur eskalasi

Baca graf hubungan dan cari jalur eskalasi dari akun uji sendiri: user → grup berhak → admin → kontrol domain; peran Azure AD yang melebar; aplikasi/service principal dengan izin berlebih; hubungan tidak langsung (nested group, delegasi). Standar lulus: tiap jalur yang ditemukan tercatat lengkap (simpul awal → simpul antara → simpul target + jenis hubungan) — jalur yang hanya "kelihatannya mungkin" tanpa simpul konkret = BELUM TERBUKTI.

### Gerbang 3 — Buktikan jalur dengan akun uji sendiri, read-only

Buktikan SATU jalur per putaran, hanya dengan akun uji milik sendiri, hanya read-only: tunjukkan bahwa akun uji benar bisa mencapai simpul berikutnya (mis. membaca atribut/keanggotaan yang seharusnya tidak terbaca, atau memanggil fungsi yang seharusnya ditolak) — tanpa mengubah apa pun di AD. Ulangi 3× bila melibatkan perilaku agen. Standar lulus: jalur terbukti ATAU dinyatakan tidak ada dengan bukti negatif; gagal direproduksi 3× = TOLAK. **Jalur di graf saja BUKAN laporan** — yang maju hanya jalur yang terbukti bisa dilalui dengan dampak nyata.

Hanya temuan yang lolos Gerbang 3 yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| BloodHound-MCP-AI | Pemetaan jalur serangan AD lewat graf; ikuti README-nya. |
| RoadRecon MCP | Pemetaan Azure AD (Entra ID); ikuti README-nya. |
| Akun uji sendiri + canary palsu | Satu-satunya akun yang dipakai untuk membuktikan jalur. |
| Log HTTP mentah | Simpan request/response sebagai bukti; berikan hanya reference ID ke LLM saat menyusun laporan. |
| `~/workspace/catatan/log-bug-bounty.md` | Log scope tertulis → graf → jalur → keputusan gerbang. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + domain/tenant AD atau Azure AD in-scope]
Kutipan scope: [teks aturan program yang mengizinkan AD/Azure AD]
Server MCP: [BloodHound-MCP-AI / RoadRecon MCP + versi]
Jalur ditemukan: [simpul awal] → [simpul antara + hubungan] → [simpul target]
Pembuktian: [akun uji + langkah + log HTTP]
Indikator teramati: [apa yang terjadi, persis]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Domain/Tenant AD] - [Jalur eskalasi] menyebabkan [Dampak Spesifik]`. Isi laporan: Ringkasan Graf (jalur + hubungan antar simpul); Langkah Reproduksi (akun uji sendiri + log HTTP + bukti read-only); Rekomendasi Perbaikan (rapikan keanggotaan grup bersarang, batasi delegasi, tinjau peran Azure AD berlebih, hapus jalur yang tidak dibutuhkan).

## Batasan yang diketahui

- Metodologi ini dari riset, bukan pengalaman teruji — tiap server MCP AD butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- Skill ini HANYA dipakai bila program secara eksplisit mencantumkan aset AD/Azure AD — untuk kebanyakan program bounty agen AI, skill ini TIDAK relevan dan tidak boleh dipakai.
- Data graf AD bisa berisi nama pengguna dan struktur organisasi asli — sensor semua nama orang/grup di laporan (tulis peran/jenis simpulnya, bukan nama aslinya) dan jangan simpan data graf mentah di luar log tim.
- Jalur di graf belum tentu bisa dilalui: validasi hidup (Gerbang 3) tidak boleh dilewati.
- Untuk bounty agen AI (Muse, OpenAI, Google, 0din), yang dinilai adalah HASIL/outcome (aksi nyata/data keluar), bukan panjangnya jalur di graf.

## Websites

- awesome-mcp-security — https://github.com/Puliczek/awesome-mcp-security
- Dokumentasi scope program bounty yang sedang diuji (per program, baca pasal scope sebelum menguji).

## Alternatives for better results

- Bila yang diuji adalah rantai federasi/assume-role cloud (bukan graf AD), pakai `serangan-cloud-iam-entra`.
- Bila target adalah aset cloud (bucket, bukan AD), pakai `enumerasi-aset-cloud`.
- Bila program tidak menyebut AD sama sekali, skill ini TIDAK dipakai — kembali ke `pemetaan-permukaan-serangan`.
