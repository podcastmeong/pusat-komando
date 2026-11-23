# Skill: Pipeline Pengiriman 0din (untuk A119, A120 — T14 0din Repro & Submission)

> **STATUS: BELUM DIUJI.** Skill baru 24 Nov 2026 (Blok D, T14). Belum pernah dipakai dalam pengiriman nyata — pakai dengan pengawasan Koordinator T14 (A120) dan catat hasil pertama di `~/workspace/catatan/log-bug-bounty.md`.
>
> **HANYA UNTUK BOUNTY** — hanya dipakai untuk pengiriman ke program bug bounty resmi 0din. **LARANGAN DESTRUKTIF:** dilarang mengirim laporan palsu/bohong, dilarang mengirim tanpa persetujuan Cipta, dilarang memakai identitas/KTP orang lain. Payout butuh KTP + form IRS W-8 — itu urusan Cipta, bukan agent.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A119 Pelapor 0din** | Susun abstrak + laporan lengkap; isi portal pengiriman |
| Pengerjaan | **A118 Pendamping Repro** | Siapkan paket repro langkah-demi-langkah untuk Cipta |
| Audit | **A120 Koordinator T14** | Triase akhir + cek duplikat sebelum draf ke Cipta |

## Alur pengiriman 0din (terverifikasi 23 Nov 2026)

1. **Abstrak dulu (wajib):** abstrak + model terdampak → jawaban scope + kisaran hadiah ≤3 hari kerja.
2. **Detail lengkap/PoC** setelah abstrak diterima → validasi ≤2 minggu → bayar ≤30 hari setelah kesepakatan kontraktual.
3. **Dokumen payout:** wajib foto ID pemerintah + form IRS W-8 (non-AS, termasuk Indonesia) — disiapkan Cipta sendiri; agent TIDAK meminta, menyimpan, atau mengirim dokumen identitas Cipta.
4. **Tier hadiah 0din:** Low ≤$500 · Medium ≤$2.500 · High ≤$5.000 · Severe ≤$15.000.

## Aturan keras

1. **TIDAK PERNAH kirim tanpa persetujuan Cipta.** Draf boleh disiapkan; pengiriman (abstrak maupun laporan lengkap) hanya setelah Cipta setuju.
2. **Aturan duplikat 0din:** Medium+ yang diterima dalam 7 hari sejak pengiriman pertama BERBAGI hadiah. Low: ke-1 100%, ke-2 50%, ke-3 20%, sisanya kredit saja. Cek duplikat (publik/CVE/writeup) SEBELUM abstrak dikirim.
3. **Struktur abstrak:** judul 1 baris (dampaknya jelas) → model terdampak → ringkasan 2–3 kalimat → scope yang kena. Struktur laporan lengkap: judul → ringkasan → langkah repro bernomor (bisa diulang) → bukti (tangkapan layar/transkrip) → scope → dampak.
4. **Bahasa:** Inggris untuk portal 0din; simpan salinan Indonesia di log bila perlu.
5. **Lacak status:** setiap pengiriman dicatat (terkirim/menunggu/ditolak/dibayar + tanggal + tenggat jawaban) — Koordinator (A120) yang melacak.
6. **Repro didampingi, bukan dijalankan tim:** paket repro disiapkan agar Cipta bisa menjalankan sendiri di perangkat/akunnya; tim TIDAK menjalankan uji korban.

## Alur kerja

Temuan lolos triase (A120) → A118 siapkan paket repro → A119 tulis abstrak → draf abstrak ke Cipta → Cipta setuju → kirim abstrak → jawaban scope ≤3 hari kerja → A119 tulis laporan lengkap + bukti → draf ke Cipta → Cipta setuju → kirim detail → lacak validasi ≤2 minggu → lacak bayar ≤30 hari.
