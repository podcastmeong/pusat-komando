# Skill: Vektor Manipulasi Dokumen (untuk A112, A113 — T13 0din Content Manipulation, V6)

> **STATUS: BELUM DIUJI.** Skill baru 24 Nov 2026 (Blok D, T13). Belum pernah dipakai dalam pengujian nyata — pakai dengan pengawasan Koordinator T13 (A115) dan catat hasil pertama di `~/workspace/catatan/log-bug-bounty.md`.
>
> **HANYA UNTUK BOUNTY** — hanya dipakai dalam program bug bounty resmi (di sini: 0din) dan hanya terhadap target yang masuk scope program. **LARANGAN DESTRUKTIF:** dilarang menghapus/merusak dokumen orang lain, dilarang uji korban, dilarang memakai data orang lain, dilarang eksfiltrasi. Uji HANYA akun sendiri + dokumen/canary palsu milik sendiri.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A112 Pemeta Vektor Konten** | Petakan permukaan vektor dokumen: kolom komentar, revisi bersama, lampiran, metadata |
| Pengerjaan | **A113 Perancang Paket Manipulasi** | Rancang paket uji + langkah repro terdokumentasi (TIDAK menjalankan repro korban) |
| Audit | **A115 Koordinator T13** | Periksa scope + validitas sebelum paket diteruskan ke Reporter |

## Ruang lingkup (V6 — vektor dokumen)

Dokumen bersama/berbagi (mis. dokumen kolaboratif, komentar, saran revisi, lampiran, deskripsi/metadata file) sebagai pembawa konten yang kemudian dibaca/diringkas/ditindaklanjuti agen AI korban. Pertanyaan pemetaan: (1) di mana teks dokumen masuk ke konteks agen; (2) siapa yang bisa menulis ke dokumen itu (pemilik, editor, pemberi komentar, publik); (3) apakah agen membedakan instruksi pemilik vs instruksi dari isi dokumen; (4) jejak apa yang tertinggal (riwayat revisi, penulis komentar).

## Aturan keras

1. **Repro HANYA dijalankan Cipta sendiri di perangkat/akunnya sendiri.** Tim ini hanya menyiapkan paket + dokumentasi. TIDAK PERNAH menjalankan uji korban — tidak ada pengiriman dokumen berisi muatan ke orang lain, tidak ada undangan/berbagi ke korban.
2. **Hanya akun sendiri + canary palsu.** Semua uji memakai akun dan dokumen milik Cipta sendiri; canary (penanda palsu) dipakai untuk membuktikan aliran data tanpa data asli orang lain.
3. **Tanpa eksfiltrasi.** Bukti yang dikumpulkan hanya menunjukkan bahwa konten dokumen bisa memengaruhi agen — bukan isi data orang lain.
4. **Setujui target SEBELUM Exploiter berjalan.** Koordinator (A115) menyetujui target + scope tertulis dulu; tanpa persetujuan itu, A113 tidak merancang paket.
5. **Paket berisi:** deskripsi vektor, permukaan yang kena, langkah repro bernomor (untuk Cipta), bukti yang diharapkan, dampak, dan batasan scope program 0din.
6. **TIDAK PERNAH kirim laporan tanpa persetujuan Cipta.** Draf boleh disiapkan; pengiriman hanya setelah Cipta setuju.

## Alur kerja

Recon petakan permukaan (A111) → Analyzer petakan vektor dokumen (A112) → Koordinator setujui target (A115) → Exploiter rancang paket + langkah repro (A113) → Reporter susun draf (A114) → draf ke Cipta → Cipta jalankan repro sendiri bila setuju → kirim bila Cipta setuju.
