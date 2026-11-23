# Skill: Spoofing Header Proxy Konektor — Tool Output Palsu lewat Proxy/Konektor

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Definisi

Spoofing header proxy konektor: header, metadata, atau identitas asal yang melewati proxy/konektor (MCP, connector, atau perantara tool) dipalsukan atau dimanipulasi, sehingga tool output yang diterima agen Muse tampak berasal dari sumber tepercaya / berotoritas, padahal isinya dikendalikan penguji — lalu agen mempercayai dan menindaklanjuti output itu. Skill ini HANYA menguji rantai itu pada akun dan konektor sendiri dengan canary palsu.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam program bounty resmi, di sini: **Muse (Meta)**. Di luar program resmi = tidak boleh dipakai. Hanya akun sendiri, konektor sendiri + canary palsu. Tanpa data orang lain, tanpa uji korban, tanpa eksfiltrasi.

## Pemicu (kapan dipakai)

Dipakai saat menguji apakah header/proxy metadata dari konektor bisa dipalsukan; saat menguji apakah tool output yang lewat proxy dipercaya agen tanpa verifikasi asal; saat menguji varian tool-output spoofing yang memanfaatkan jalur konektor/proxy, bukan isi dokumen langsung.

## Sudah tercakup (jangan diduplikat)

- Tool output tidak aman / spoofing output secara umum → skill `output-tidak-aman`.
- Injeksi tak terlihat multimodal → skill `injeksi-tak-terlihat-multimodal`.
- Peracunan deskripsi tool MCP → skill `peracunan-deskripsi-tool-mcp`.
- Taksonomi ancaman MCP → skill `taksonomi-ancaman-mcp`.
- Studi kasus eksploitasi MCP nyata → skill `studi-kasus-eksploitasi-mcp-nyata`.
- Gateway MCP aman / pembungkus pengaman MCP → skill `gateway-mcp-aman`, `pembungkus-pengaman-mcp`.
- Pemindai server MCP → skill `pemindai-server-mcp`, `server-mcp-pemindai-kerentanan`.
- Injeksi header CRLF/log → skill `injeksi-header-crlf-log`.
- Pembuktian dampak dengan canary → skill `canary-pembuktian-dampak`.

## Tahap rantai (petakan sebelum menguji)

| Tahap | Yang diuji | Bukti yang dicari |
|---|---|---|
| 1. Jalur | Tool output melewati proxy/konektor tertentu ke agen | Jalur + header/metadata tercatat |
| 2. Palsu | Header/metadata/identitas asal dipalsukan dari sisi penguji (server/konektor sendiri) | Output diterima dengan identitas palsu |
| 3. Percaya | Agen memperlakukan output sebagai tepercaya (mengutip, memakai sebagai fakta) | Agen mengutip isi canary sebagai fakta |
| 4. Tindak | Agen menindaklanjuti output (job/aksi) berdasarkan kepercayaan itu | Canary tersentuh = aksi terjadi |

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta untuk skill ini).
2. **Hanya akun/konektor/server sendiri + canary palsu.** Server/proxy uji milik sendiri; isi palsu HANYA canary unik milik sendiri.
3. **Tanpa data orang lain.** Jangan memakai kredensial, token, atau identitas orang lain sebagai header palsu.
4. **Tanpa uji korban — victim-agent fraud tests DIBLOKIR.** Jalur yang diuji hanya jalur akun sendiri.
5. **Gerbang persetujuan manusia SEBELUM tahap tindak.** Exploiter TIDAK menguji tahap 4 sebelum Koordinator/Triase & QA dan Muse menyetujui target + canary-nya; persetujuan dicatat.
6. **Tanpa DoS/DDoS.** Satu varian header per hipotesis, volume kecil.
7. **Tanpa payload di permukaan publik.** Server/proxy uji tidak dipublikasikan sebagai layanan umum.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG header palsu yang berujung hapus data, kirim dana, kirim ke pihak ketiga, atau menyamar sebagai pihak nyata (pemerintah, bank, perusahaan). Identitas palsu HARUS jelas-jelas canary (nilai unik yang tidak meniru identitas nyata). Setelah uji selesai, server/proxy uji DIMATIKAN dan canary DIBERSIHKAN; catat pembersihan.
10. **Satu hipotesis = satu header = satu catatan.** Tiap varian (header mana, nilai apa, jalur konektor mana) dicatat terpisah dengan hasil lolos/gagal.

## Langkah + gerbang

### Gerbang 0 — Tulis hipotesis + canary (Recon + Analyzer)

1. Tulis hipotesis satu kalimat: "Header X yang dipalsukan lewat konektor Y membuat agen mempercayai output Z."
2. Pilih canary unik yang HANYA bisa muncul bila agen mempercayai output itu.
3. Catat scope program Muse yang berlaku; bila ragu soal scope, TANYA dulu — jangan uji.

### Gerbang 1 — Petakan jalur + pasang server uji sendiri (Recon)

4. Petakan jalur tool output: konektor/proxy mana, header/metadata apa yang diteruskan.
5. Pasang server/proxy uji MILIK SENDIRI yang mengembalikan output berisi canary dengan header palsu. Catat konfigurasi persis.

### Gerbang 2 — Amati percaya (Analyzer)

6. Amati apakah agen mengutip/memakai isi canary sebagai fakta — TANPA memancing aksi.
7. Bila tidak dipercaya: catat GAGAL untuk varian itu. Bila dipercaya: lanjut ke Gerbang 3.

### Gerbang 3 — Persetujuan tindak (Koordinator/Triase & QA + Muse)

8. Koordinator memeriksa: target in-scope? canary inert + bukan penyamaran identitas nyata? duplikat dengan temuan lama? Bila satu saja TIDAK, uji BERHENTI.
9. Muse menyetujui target + canary secara tertulis di log tim.

### Gerbang 4 — Uji tindak + bukti (Exploiter + Reporter)

10. Uji apakah kepercayaan itu berujung aksi; pantau canary. Tangkap bukti: request/response, header persis, langkah reproduksi.
11. Reporter menyusun draf sesuai standar platform (HackerOne/Bugcrowd): ringkasan, langkah reproduksi, dampak, bukti canary. Draf dulu — kirim hanya setelah persetujuan Cipta.
12. Matikan server uji + bersihkan canary; catat pembersihan.
