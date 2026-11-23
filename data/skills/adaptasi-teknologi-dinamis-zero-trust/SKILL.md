# Skill: Adaptasi Teknologi Dinamis & Zero Trust — Menyesuaikan Senjata Saat Medan Berubah

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: materi suplemen Cipta batch 6, 24 Nov 2026. Metode adaptasi ini belum pernah dijalankan sampai menghasilkan temuan; label ini berlaku untuk semua bagian sampai ada satu adaptasi teknologi yang tercatat dan lolos triase di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai untuk sembilan program bounty resmi in-scope: **Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar kesembilan program itu, skill ini tidak boleh dipakai. Skill ini adalah skill metode — mengatur CARA tim beradaptasi saat teknologi target berubah — BUKAN skill pengujian: skill ini tidak memberi langkah untuk menemukan atau mengeksploitasi kerentanan tertentu. Zero Trust Architecture dibahas di sini sebagai LENSA analisis (di mana kepercayaan diasumsikan tanpa verifikasi), bukan sebagai produk atau sertifikasi.

## Pemicu

Dipakai setiap kali muncul teknologi, platform, atau pola arsitektur baru di program target (mis. pergeseran fokus dari web ke cloud lalu ke AI); setiap kali threat intelligence menunjukkan tren ancaman baru; dan setiap kali satu keluarga serangan berhenti membuahkan hasil (tanda medan sudah berubah). Dipakai juga saat tim memutuskan apakah skill lama masih relevan atau perlu diperbarui.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pemantau tren | **A59 Threat Hunter** | Membaca threat intelligence + CVE terbaru, melaporkan pergeseran teknologi yang relevan ke tim |
| Pengerjaan | **A58 Vulnerability Researcher** | Memetakan permukaan baru dari teknologi yang berubah; mencari asumsi kepercayaan di dalamnya |
| Audit | **A60 Security Auditor** | Memvalidasi peta permukaan + asumsi kepercayaan sebelum diuji (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan adaptasi mana yang dijalankan dan skill mana yang diperbarui |

## Sudah tercakup (jangan diduplikat)

- Pemantauan CVE + kasus breach nyata → skill `pemantauan-cve-breach-nyata`. Skill ini TIDAK mengulang mekanik pemantauan — skill ini memakai HASIL pemantauan itu sebagai pemicu adaptasi.
- Threat intelligence berkala → skill `intelijen-ancaman-berkala`. Skill ini memakai tren yang dilaporkan skill itu; cara membaca threat intelligence tetap di sana.
- Analisis batas kepercayaan → skill `analisis-batas-kepercayaan`. Skill ini memakai lensa yang sama pada teknologi BARU; mekanik pemetaan batas kepercayaan tetap di skill itu.
- Kurikulum belajar teknologi baru → skill `jalur-belajar-ethical-hacker-maraton`. Skill ini tidak mengatur urutan belajar — skill ini mengatur adaptasi TAKTIS saat medan berubah di tengah perburuan.

## Prinsip adaptasi

1. **Medan berubah, misi tetap.** Hari ini keamanan aplikasi web jadi fokus, besok mungkin cloud security atau AI security. Yang berubah adalah permukaan; yang tetap adalah pertanyaan: di mana asumsi yang salah?
2. **Zero Trust sebagai lensa.** Prinsip Zero Trust: jangan pernah percaya, selalu verifikasi; hak akses seminimal mungkin; anggap pelanggaran sudah terjadi; verifikasi berkelanjutan. Setiap tempat sistem MEMPERCAYAI sesuatu tanpa verifikasi adalah kandidat celah — cari di sana dulu.
3. **Fleksibel, jangan kaku.** Jangan memegang teknik lama bila teknologi target sudah berubah. Satu teknik yang berhenti membuahkan hasil selama berminggu-minggu adalah sinyal untuk beradaptasi, bukan untuk mengulanginya lebih keras.
4. **Adaptasi dicatat, bukan dihafal.** Setiap adaptasi yang berhasil (atau gagal) ditulis ke log beserta alasannya, supaya tim berikutnya tidak mengulang dari nol.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan dipakai.
2. **Hanya akun sendiri + canary palsu.** Pengujian adaptasi hanya di akun dan data milik sendiri atau canary palsu.
3. **Tanpa data orang lain.** Jangan menyentuh, menyimpan, atau memakai data pengguna lain selama memetakan teknologi baru.
4. **Tanpa uji korban — DIBLOKIR.** Victim-agent fraud tests dan pengujian apa pun terhadap korban sungguhan atau akun yang bukan milik sendiri DIBLOKIR — jangan dicoba.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan, termasuk saat memetakan permukaan baru.
6. **Tanpa payload di permukaan publik.** Peta permukaan, catatan adaptasi, dan draf jangan di-host atau dibagikan di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Peta permukaan + asumsi kepercayaan baru harus diperiksa Muse/A60 sebelum diuji — jangan serahkan keputusan scope ke otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus, mengubah, atau merusak data apa pun selama adaptasi — termasuk konfigurasi target. DILARANG memakai hasil pemetaan untuk mengakses akun siapa pun atau memperoleh keuntungan di luar hadiah bounty resmi.

## Langkah + gerbang

### Gerbang 0 — Deteksi perubahan

1. Dari `pemantauan-cve-breach-nyata` + `intelijen-ancaman-berkala`: catat teknologi/pola baru apa yang muncul (mis. arsitektur baru, layanan baru, tren ancaman baru) dan program mana yang terdampak.
2. **Standar lulus:** perubahan tercatat (teknologi + program + sumber) sebelum adaptasi apa pun dimulai. Tanpa catatan = jangan lanjut.

### Gerbang 1 — Petakan permukaan baru

1. Petakan permukaan teknologi baru itu: komponen apa saja, data apa yang mengalir, siapa yang berkomunikasi dengan siapa, dan di mana batas kepercayaannya. Gunakan skill `analisis-batas-kepercayaan` untuk mekaniknya.
2. **Standar lulus:** peta permukaan tertulis + diserahkan ke A60. Peta yang hanya ada di kepala = belum ada.

### Gerbang 2 — Cari asumsi kepercayaan (lensa Zero Trust)

1. Untuk setiap komponen di peta, tanyakan dengan lensa Zero Trust: apa yang DIPERCAYA komponen ini tanpa verifikasi? (identitas pemanggil, asal data, keutuhan token, hak akses, status sesi). Daftar asumsi itu dari yang paling berisiko.
2. **Standar lulus:** minimal 3 asumsi kepercayaan tercatat dengan alasan risikonya. Nol asumsi = peta belum cukup dalam, ulangi Gerbang 1.

### Gerbang 3 — Uji asumsi dalam scope

1. Uji satu asumsi dalam satu waktu, HANYA di target in-scope, HANYA dengan akun sendiri + canary palsu. Ikuti skill pengujian yang relevan (mis. keluarga SPIONASE/HACKING) untuk mekanik ujinya — skill ini tidak memberi mekanik uji.
2. **Standar lulus:** hasil uji tercatat (asumsi terbukti salah / terbukti benar + bukti minimal). Asumsi yang gagal dibuktikan = coret dan lanjut ke asumsi berikutnya, jangan dipaksa.

### Gerbang 4 — Catat adaptasi + perbarui skill

1. Tulis ke log: teknologi apa yang berubah, asumsi apa yang diuji, hasilnya, dan skill mana yang perlu diperbarui (atau skill baru apa yang dibutuhkan). Bila satu asumsi terbukti salah dan berdampak, serahkan ke triase lewat jalur biasa.
2. **Standar lulus:** catatan adaptasi lengkap di log + keputusan perbarui/tidak suatu skill tercatat. Adaptasi tanpa catatan = tidak terjadi.

## Alat

| Alat | Cara pakai |
|---|---|
| Skill `pemantauan-cve-breach-nyata` + `intelijen-ancaman-berkala` | Sumber deteksi perubahan (Gerbang 0) |
| Skill `analisis-batas-kepercayaan` | Mekanik pemetaan batas kepercayaan (Gerbang 1) |
| Lensa Zero Trust (jangan percaya, selalu verifikasi; hak minimal; anggap sudah bocor; verifikasi berkelanjutan) | Kerangka pertanyaan Gerbang 2 |
| Skill keluarga SPIONASE/HACKING yang relevan | Mekanik pengujian asumsi (Gerbang 3) |
| `~/workspace/catatan/log-bug-bounty.md` | Log perubahan teknologi + asumsi + hasil uji + keputusan adaptasi |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Perubahan: [teknologi/pola baru + program terdampak + sumber]
Peta permukaan: [ringkasan komponen + batas kepercayaan]
Asumsi kepercayaan: [daftar asumsi + risiko masing-masing]
Hasil uji: [asumsi → terbukti salah / terbukti benar + bukti minimal]
Adaptasi: [skill diperbarui / skill baru diusulkan / tidak ada perubahan]
Status: [DRAF / maju ke triase / ditolak + alasan]
```

## Batasan yang diketahui

- Zero Trust di sini adalah lensa analisis, bukan sertifikasi atau produk. Skill ini tidak mengajarkan implementasi Zero Trust dan tidak menggantikan pelatihan arsitektur formal.
- Tidak semua pergeseran teknologi relevan untuk semua program — periksa scope program dulu sebelum beradaptasi; adaptasi di luar scope adalah buang waktu.
- Asumsi kepercayaan yang terbukti benar BUKAN kegagalan — itu hasil yang valid dan menghemat waktu tim. Catat dan lanjut.
- Bila satu teknologi baru belum punya skill pengujian yang relevan, usulkan skill baru ke Muse — jangan memaksakan skill lama ke permukaan yang tidak cocok.

### Available connectors

Tidak ada konektor khusus untuk skill ini; peta permukaan dan catatan adaptasi dicatat manual di log dan divalidasi A60/Muse.

### Websites

- Laporan CVE dan threat intelligence terbaru (sumber deteksi perubahan — lihat skill `pemantauan-cve-breach-nyata` dan `intelijen-ancaman-berkala`).
- Dokumentasi arsitektur resmi teknologi target (sumber peta permukaan — baca dokumentasi publik program, bukan hasil bocoran).

### Alternatives for better results

- Bila peta permukaan terlalu besar, potong per komponen dan uji satu komponen dulu — adaptasi kecil yang selesai lebih baik daripada peta besar yang tidak pernah diuji.
- Bila dua agent memetakan teknologi yang sama, bandingkan peta mereka — perbedaan peta sering menunjukkan asumsi yang terlewat.
- Bila tren baru ternyata hanya ganti nama dari teknologi lama, catat itu dan pakai skill lama — jangan membangun adaptasi untuk sesuatu yang sebenarnya tidak berubah.
