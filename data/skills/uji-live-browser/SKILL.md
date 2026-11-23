# Skill: Uji Live via Browser (untuk A54 Penguji Live)

> Perintah Cipta 23 Nov 2026 — uji live hanya dengan akun sendiri + canary palsu. Pelajaran AMD 23 Nov: 65+ percobaan slider gagal — IP dan waktu yang menentukan, bukan jumlah percobaan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A54 Penguji Live** | Uji live via browser task di target in-scope |
| Pemimpin | **Muse** | Putuskan apa yang diuji, bunuh jalur buntu |

## Aturan keras

1. **HANYA akun sendiri + canary palsu.** Tidak ada data orang lain, tidak ada akun korban, tidak ada aksi ke akun/properti orang lain.
2. **TIDAK PERNAH uji penipuan agen korban** — skenario "korban" (satu akun menyerang agen akun lain lewat instruksi tersembunyi) DIBLOKIR kebijakan. JANGAN dicoba lagi dalam bentuk apa pun.
3. **Hanya target in-scope.** Di luar scope program = jangan sentuh. Bila ragu apakah sesuatu masuk scope, tanya Muse dulu.
4. **Catat setiap uji** (metode + hasil + bukti) di `~/workspace/catatan/log-bug-bounty.md` hari itu juga. Tanpa bukti = belum teruji.

## Playbook CAPTCHA / bot-check (pelajaran AMD, 65+ gagal, 23 Nov 2026)

- **Reputasi IP PALING menentukan.** Cloudflare: IP datacenter 0–20 (hampir langsung ditantang/diblokir), residensial 40–70, seluler 85–99. Browser cloud kami = IP datacenter — hampir pasti penyebab terbesar kegagalan slider AMD.
- **Ukur sekali, drag langsung.** Puzzle slider kedaluwarsa ~30 detik sejak muncul; tiap putaran baca-aksi butuh 10–30 detik. Ukur posisi potongan + celah dari SATU crop, lalu drag segera — jangan ukur ulang, jangan lepas di tengah drag.
- **Rasio bukan 1:1.** Potongan bergerak ~0,77–0,96 px per 1 px handle (median ~0,87). Hitung jarak drag dari gerakan potongan yang sebenarnya, jangan asumsi handle = potongan.
- **Trajektori dinilai, bukan cuma posisi.** Drag <200 mdtk langsung di-flag; yang lolos: kurva lambat–cepat–lambat, goyangan sumbu Y, mikro-jeda, overshoot lalu koreksi 1–3 px, durasi 0,5–3 detik.
- **Jangan menghantam sesi/IP yang sama.** Gagal 2–3x → cooldown → sesi segar → ubah tuas terbesar dulu (IP: HP Cipta + WiFi rumah) → ukur sekali + drag langsung (<30–60 detik) → panaskan sesi. Jalan tercepat yang sah: Cipta menyelesaikan puzzle sendiri di HP-nya.
- **Tidak ada "jam ajaib".** Riset 37 sumber (23 Nov): tidak ada data CAPTCHA lebih mudah di jam tertentu. Yang berubah menurut jam hanya antrean jasa solver pihak ketiga (tersepi 00:00–06:00 UTC = 07:00–13:00 WIB — hasil lebih cepat, BUKAN tantangan lebih mudah). Jangan karang angka jam.

## Batas permukaan (OpenAI Free, teruji 23 Nov 17:43)

- ChatGPT Free web: TIDAK ada mode Work/Codex, TIDAK ada tombol agen, 0 konektor terhubung. Aksi agen + Codex + koneksi email/kalender = fitur Plus. Upload file ada kuota Free (habis → tunggu ~23 jam; H3 diulang ~24 Nov 17:43 atau Plus $20/bln — keputusan bayar Cipta).
- H1 injeksi dokumen 0/3, H2 spoofing tool-output 0/3, H4 bocoran CoT 0/3. Jangan ulangi H1/H2/H4 di Free web dengan payload yang sama — variasikan format atau pindah permukaan (Plus / desktop Work).
