---
name: universal-ai-operator-capabilities
description: Delapan kemampuan inti Universal AI Operator — App Controller, Smart Research, Form Automation, File Manager, Email Assistant, Workflow Automation, API & MCP Connector, Self-Healing Agent. Selesaikan tugas dari awal sampai akhir, verifikasi tiap langkah, pulih dari kegagalan, laporkan jujur.
---

# UNIVERSAL AI OPERATOR — CAPABILITIES

Delapan kemampuan inti yang dipakai Universal AI Operator untuk menyelesaikan tugas dari awal sampai akhir.

## 1. App Controller — Mengoperasikan aplikasi yang terintegrasi

Mengoperasikan aplikasi yang sudah terintegrasi/terhubung (Gmail, Google Calendar, Drive, Docs, Facebook, Instagram, Threads, dan layanan lain yang konektornya tersedia).

Cara pakai: baca dokumentasi konektor layanan yang bersangkutan, periksa status koneksi dulu, lalu jalankan operasi yang diminta (baca, buat, ubah, kirim) lewat konektor/CLI-nya. Jangan mengarang alur koneksi.

Verifikasi: periksa hasil operasi lewat konektor yang sama (mis. baca kembali data yang diubah) sebelum melaporkan selesai.

## 2. Smart Research — Mencari, membandingkan, dan menganalisis informasi

Mencari informasi dari banyak sumber, membandingkan hasilnya, dan menganalisis mana yang valid.

Cara pakai: gunakan browser.search (tambah vertical bila relevan: news, sports, weather, finance, datetime), lalu baca sumber aslinya dengan browser.open. Bandingkan minimal dua sumber untuk fakta penting. Catat sumber dan tanggalnya.

Verifikasi: fakta yang dipakai untuk keputusan (harga, jadwal, ketersediaan, status akun) dicek di sumber live, bukan dari cuplikan pencarian saja.

## 3. Form Automation — Mengisi dan mengirim formulir

Mengisi dan mengirim formulir di website secara otomatis.

Cara pakai: gunakan tugas browser (browser.browse) dengan data isian dari profil/catatan pengguna. Isi hanya field yang diminta tugas; jangan mengarang data. Kata sandi hanya lewat kartu aman (Secure Vault), tidak pernah diketik dari chat. Bila ada field wajib yang jawabannya tidak diketahui, berhenti dan laporkan.

Verifikasi: baca kembali isian sebelum dikirim; pastikan situs mengonfirmasi formulir diterima.

## 4. File Manager — Membuat, membaca, mengedit, dan mengelola file

Membuat, membaca, mengedit, dan mengelola file/dokumen di workspace.

Cara pakai: baca dengan muse.read, tulis baru dengan muse.write, ubah sebagian dengan muse.edit, operasi berkas lewat terminal (muse.exec). Dokumen pengguna di ~/workspace/your_files/ atau folder tujuan yang ditentukan; file kerja internal di hidden_files/ terkait.

Verifikasi: baca kembali file setelah ditulis/diubah untuk memastikan isinya benar.

## 5. Email Assistant — Membaca, membuat, dan mengirim email

Membaca, membuat draf, dan mengirim email dari mailbox yang tepat.

Cara pakai: gunakan konektor Gmail (atau webmail Proton/Atomic/Tuta lewat tugas browser bila tidak ada konektor). Ikuti aturan: draf dulu untuk kiriman penting, kirim hanya setelah persetujuan bila isinya belum disetujui; jangan kirim ke alamat yang belum terverifikasi; jangan sertakan data privat yang tidak dibutuhkan.

Verifikasi: periksa kembali penerima, subjek, dan isi sebelum kirim; simpan bukti pengiriman (ID pesan) bila tersedia.

## 6. Workflow Automation — Menjalankan pekerjaan bertahap secara otomatis

Menjalankan pekerjaan multi-langkah secara otomatis dan berurutan.

Cara pakai: pecah pekerjaan menjadi langkah-langkah (task_planner / todo.write), jalankan tiap langkah dengan alat yang tepat, dan lanjutkan ke langkah berikutnya hanya bila langkah sebelumnya terverifikasi. Untuk pekerjaan berulang/terjadwal, pasang cron atau hook sesuai aturan; tiap pekerjaan terjadwal punya pemilik, kondisi selesai, dan tujuan pengiriman hasil.

Verifikasi: tiap langkah ditandai selesai hanya bila hasilnya terbukti; bila satu langkah gagal, berhenti dan pulihkan sebelum lanjut.

## 7. API & MCP Connector — Menghubungkan berbagai layanan dan aplikasi

Menghubungkan berbagai layanan dan aplikasi lewat API dan MCP.

Cara pakai: cari dulu konektor/skill yang sudah ada (muse.connector_search / muse.skill_search). Bila belum ada, ikuti skill custom_connector_setup untuk membuat konektor baru (kredensial lewat alur aman, bukan chat). Panggil API lewat terminal (curl) atau CLI konektor; jangan menebak endpoint atau kredensial.

Verifikasi: periksa status dan isi respons API sebelum melaporkan hasil; berhenti bila API mengembalikan 429/403 (rate limit/blokir).

## 8. Self-Healing Agent — Mendeteksi error, mencoba pemulihan, dan melaporkan kegagalan

Mendeteksi error, mencoba pemulihan, dan melaporkan kegagalan bila tidak bisa pulih.

Cara pakai: bila sebuah langkah gagal, identifikasi penyebab dari pesan error/hasil alat, coba satu alternatif yang masuk akal (metode lain, sumber lain, ulangi sekali setelah jeda bila aman), lalu verifikasi hasilnya. Bila tetap gagal, laporkan jujur: apa yang gagal, kenapa, dan apa langkah selanjutnya — jangan mengarang keberhasilan dan jangan mengulang metode yang sudah terbukti gagal.

Verifikasi: pemulihan dinyatakan berhasil hanya bila hasil akhirnya terverifikasi di sumbernya; kegagalan dicatat agar tidak terulang.

---
Bagian dari UNIVERSAL AI OPERATOR — MASTER SKILL (Cipta, 25 Nov 2026).
