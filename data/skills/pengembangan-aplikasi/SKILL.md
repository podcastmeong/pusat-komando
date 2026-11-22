# Skill: Pengembangan Aplikasi (untuk A13 App Developer)

> Tugas A13: produksi aplikasi 5/hari (target antrean demo; minimal 1 aplikasi/game per hari). Aplikasi dijual sebagai SATU file HTML; data tersimpan PER PERANGKAT (localStorage) — JANGAN PERNAH jual sebagai multi-user lintas perangkat.

## Aturan keras

1. **Satu file HTML** — aplikasi lengkap dalam satu file; panel Pengaturan wajib ada (nama toko, warna, logo).
2. **Harga per aplikasi = SATU harga sesuai level internal; nama level (Basic/Professional/Business) TIDAK disebut** di tampilan (keputusan Cipta 22 Nov 2026). Harga patokan aplikasi $29/$59/$99; APK +$25 (platform luar) / +Rp400.000 (langsung).
3. **Login overlay** (Admin/Kasir) di semua aplikasi; akun baru dibuat admin di Pengaturan, TIDAK ada pendaftaran sendiri; JANGAN tulis nama admin + kata sandi di layar login.
4. **Garansi:** perbaikan bug gratis — beli sekali Basic 30 hari / Professional 60 hari / Business 90 hari; klaim via WhatsApp (video/screenshot bug).
5. **Verifikasi live sebelum lapor selesai** — buka demo, klik fitur kunci, pastikan jalan (A38 QA memeriksa).
6. **Demo web = dijual sebagai demo** di Payhip ($99/$299/$599); aplikasi = dijual sebagai aplikasi asli ($29/$59/$99).

## Alur kerja

1. Rancang (A08/A09) → bangun file HTML → uji semua fitur + panel Pengaturan → demo live di `podcastmeong.github.io/<slug>/` → harga per level (tanpa sebut level) → serahkan ke A37/A31 untuk listing/upload setelah Cipta setuju.
2. Perbaikan bug: periksa dulu, perbaiki, uji ulang, laporkan.

## File kerja

- Repo website/toko: `~/workspace/tmp/podcastmeong.github.io/` (61 direktori aplikasi).
- Aturan harga + level: `~/workspace/catatan/keputusan.md` · Listing: `data/skills/eksekusi-marketplace/SKILL.md`.
