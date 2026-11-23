# Skill: Analisis Format Injeksi Berhasil (untuk A126–A130 — T16 Google Format & Scope Analysis)

> **STATUS: BELUM DIUJI.** Skill baru 24 Nov 2026 (Blok D, T16). Belum pernah dipakai dalam analisis nyata — pakai dengan pengawasan Koordinator T16 (A130) dan catat hasil pertama di `~/workspace/catatan/log-bug-bounty.md`.
>
> **HANYA UNTUK BOUNTY** — hanya dipakai dalam program bug bounty resmi (di sini: Google AI VRP) dan hanya terhadap publikasi/writeup publik + data milik sendiri. **ANALISIS FORMAT SAJA, TANPA PAYLOAD.** Skill ini TIDAK merancang payload, TIDAK menguji payload, dan TIDAK menyentuh sistem live. **LARANGAN DESTRUKTIF:** dilarang membuat/menguji muatan injeksi, dilarang uji korban, dilarang memakai data orang lain.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A126 Pengintai Format Injeksi** | Kumpulkan writeup/publikasi publik kasus injeksi tidak langsung |
| Pengerjaan | **A127 Pemeta Format Injeksi** | Petakan pola format: posisi muatan, pembungkus, pemicu |
| Pengerjaan | **A128 Penguji Format Injeksi** | Uji hipotesis FORMAT pada data publik/dokumen sendiri (bukan payload) |
| Audit | **A130 Koordinator T16** | Verifikasi scope + pastikan tidak ada payload yang dibuat/dijalankan |

## Kasus acuan (publik, formatnya saja yang dianalisis)

| Kasus | Yang dianalisis dari formatnya |
|---|---|
| EchoLeak | Di mana instruksi tersembunyi diletakkan dalam data yang dibaca agen; bagaimana agen menyampaikannya kembali |
| ShadowLeak | Pola penyembunyian dalam konten yang tampak wajar; kondisi pemicu |
| SafeBreach | Struktur kasus yang lolos filter; pembungkus yang dipakai |
| Miggo | Format pemicu lewat integrasi/alat; urutan langkah yang membuat agen menindaklanjuti |

Fokus analisis: (1) posisi instruksi dalam dokumen/data; (2) pembungkus/format yang membuatnya tampak sebagai data, bukan perintah; (3) pemicu yang membuat agen menindaklanjuti; (4) apa yang membedakan kasus berhasil vs gagal; (5) apakah pola itu masuk scope Google AI VRP (H7/H8/H10/H11 — BELUM terverifikasi, jadi verifikasi scope adalah bagian dari tugas).

## Aturan keras

1. **TANPA PAYLOAD — tanpa kecuali.** Tidak ada muatan injeksi yang ditulis, disusun, atau diuji. Yang diuji hanya hipotesis tentang FORMAT (mis. "kasus berhasil menaruh instruksi di bagian X dokumen") terhadap data publik/dokumen sendiri.
2. **Sumber hanya publik + milik sendiri.** Writeup publik, pengungkapan resmi, dokumentasi program. Tidak ada data orang lain, tidak ada uji korban.
3. **Verifikasi scope dulu.** Sebelum kesimpulan apa pun diteruskan ke tim lain, Koordinator (A130) memverifikasi apakah pola itu masuk scope program Google AI VRP; scope H7/H8/H10/H11 BELUM terverifikasi — jangan klaim sudah masuk scope.
4. **Hasil berupa tabel pola, bukan paket serang.** Keluaran skill ini: tabel perbandingan format (berhasil vs gagal), hipotesis format, dan penilaian scope. Bukan langkah repro, bukan payload.
5. **TIDAK PERNAH kirim laporan tanpa persetujuan Cipta.** Draf analisis boleh disiapkan; pengiriman hanya setelah Cipta setuju.

## Alur kerja

Recon kumpulkan kasus publik (A126) → Analyzer petakan pola format (A127) → Penguji Format uji hipotesis format pada data publik/sendiri (A128) → Koordinator verifikasi scope + pastikan tanpa payload (A130) → Reporter susun draf analisis (A129) → draf ke Cipta.
