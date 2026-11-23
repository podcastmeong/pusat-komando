# Skill: MCP Metasploit — JANGAN PAKAI (Skill Penjaga: Repo Stale, Terakhir Push Februari 2026)

> **SKILL PENJAGA — JANGAN PAKAI.** Skill ini BUKAN panduan memakai MetasploitMCP. Skill ini ada untuk MENCEGAH pemakaian MetasploitMCP yang sudah stale. Isinya hanya: alasan larangan + langkah verifikasi status repo + keputusan pakai/jangan + penggantinya.
>
> **BELUM DIUJI — dibangun dari riset artikel, bukan pengalaman teruji.** Alasan di bawah disusun dari artikel "Top 43 AI Security Skills" (Abhishek Meena, 14 Sep 2026) dan ringkasannya di `~/workspace/catatan/referensi-43-ai-security-skills-2026-11-23.md`. Status "push terakhir Februari 2026" adalah temuan artikel per 23 Nov 2026 dan WAJIB dicek ulang sebelum keputusan apa pun.

## Pemicu — kapan dipakai

Dipakai SETIAP KALI ada yang mengusulkan, menemukan panduan lama, atau tergoda memakai MetasploitMCP (GH05TCREW) untuk mengendalikan Metasploit via MCP — sebelum instalasi apa pun dilakukan. Skill ini juga dipakai saat audit berkala daftar tool tim menemukan rujukan ke MetasploitMCP.

## Pemilik

- **Pemilik: A57 Penetration Tester** — yang menjalankan verifikasi status repo dan menegakkan keputusan.
- **Pemimpin: Muse** — yang memutuskan bila hasil verifikasi meragukan.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban** (victim-agent fraud tests DIBLOKIR — jangan dicoba).
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop** (AI bantu, manusia putuskan dan validasi).
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program** (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).
10. **PENTING untuk kategori ini: alat MCP suite/recon adalah alat KLASIK — HANYA untuk program web klasik (mis. huntr), BUKAN untuk bounty agen AI (Muse, OpenAI, 0din, Google AI VRP, ViKernel).**

## Kenapa JANGAN PAKAI — alasan larangan

1. **STALE — push terakhir Februari 2026.** Per artikel (per 23 Nov 2026), repo ini terakhir diperbarui Februari 2026 — sekitar 9 bulan tanpa perawatan saat skill ini ditulis. Repo keamanan yang tidak dirawat berarti: bug tidak diperbaiki, dependensi menua, dan tidak ada yang menanggapi isu keamanan baru.
2. **Risiko tinggi bila mati.** MetasploitMCP memberi LLM akses langsung ke Metasploit via `msfrpcd` (module search, menjalankan exploit, post modules, sessions, Meterpreter, handlers). Server MCP yang tidak terawat + akses exploit = kombinasi paling berbahaya: satu bug atau satu injeksi prompt bisa berakibat fatal.
3. **Ada pengganti yang hidup dan terawat.** Kebutuhan yang sama (pentest klasik lewat MCP) sudah dipenuhi `mcp-pentest` dan `mcp-security-hub` — keduanya aktif dan punya kontrol scope/engagement. Tidak ada alasan memakai repo stale.
4. **Aturan tim: cek dulu sebelum pakai.** Sesuai peringatan artikel: baca apa yang dilakukan MCP server sebelum konek, jalankan agen orang lain di container/VM yang bisa dibuang, dan pindai dengan SkillSpector. Repo stale gagal di gerbang pertama ini.

## Langkah — verifikasi status repo + keputusan pakai/jangan

### Gerbang 1 — Cek status repo (wajib, tanpa install apa pun)

- Apa yang dilakukan: buka https://github.com/GH05TCREW/MetasploitMCP; catat tanggal push/commit terakhir, status arsip, dan isu/PR terbuka; bandingkan dengan tanggal hari ini.
- Standar lulus gerbang ini: lanjut ke Gerbang 2 HANYA bila ada push dalam 3 bulan terakhir DAN repo tidak diarsipkan. Bila push terakhir masih Februari 2026 (atau lebih dari 3 bulan lalu) atau repo diarsipkan → **KEPUTUSAN: JANGAN PAKAI**, lompat ke Gerbang 4.

### Gerbang 2 — Cek pengganti sudah memenuhi kebutuhan (hanya bila Gerbang 1 lulus)

- Apa yang dilakukan: tulis kebutuhan persis yang membuat MetasploitMCP diusulkan (mis. "butuh menjalankan exploit X"); cek apakah `mcp-pentest` atau `mcp-security-hub` sudah memenuhi kebutuhan itu.
- Standar lulus: bila pengganti memenuhi kebutuhan → **KEPUTUSAN: JANGAN PAKAI MetasploitMCP**, pakai pengganti. Lanjut ke Gerbang 3 HANYA bila pengganti TERBUKTI tidak memenuhi kebutuhan DAN repo MetasploitMCP lulus Gerbang 1.

### Gerbang 3 — Uji coba terbatas (hanya bila Gerbang 1 DAN 2 lulus — hampir tidak pernah terjadi)

- Apa yang dilakukan: pindai repo dengan SkillSpector; baca README lengkap (termasuk peringatan keamanannya); jalankan HANYA di VM/container sekali pakai yang terisolasi, HANYA terhadap lab milik sendiri, dengan `msfrpcd` di `127.0.0.1` saja; jangan sambungkan ke program bounty apa pun sebelum uji lab lolos.
- Standar lulus: uji lab berhasil tanpa error dependensi DAN tidak ada temuan SkillSpector yang kritis DAN Muse menyetujui pemakaian. Satu saja gagal → **KEPUTUSAN: JANGAN PAKAI**, lompat ke Gerbang 4.

### Gerbang 4 — Catat keputusan + arahkan ke pengganti

- Apa yang dilakukan: tulis hasil verifikasi ke log (lihat "Format output"); bila keputusan JANGAN PAKAI, beri tahu pengusul dan arahkan ke pengganti di bawah; hapus rujukan ke MetasploitMCP dari rencana kerja yang sedang berjalan.
- Standar lulus: keputusan tertulis (PAKAI / JANGAN PAKAI + alasan + tanggal cek); tidak ada instalasi MetasploitMCP yang berjalan tanpa keputusan PAKAI tertulis.

## Alat

| Alat | Repo | Status |
|---|---|---|
| **MetasploitMCP — JANGAN PAKAI** (kendali Metasploit via msfrpcd: module search, running exploits, post modules, sessions, Meterpreter, handlers) | https://github.com/GH05TCREW/MetasploitMCP (~730 bintang) | **STALE — push terakhir Februari 2026. Verifikasi masih hidup sebelum dipakai; bila mati, jangan dipakai.** |
| **Pengganti 1: pentest-mcp** (18 tools + engagement recording + report tools, auth di transport) | https://github.com/DMontgomery40/pentest-mcp | Pakai ini — lihat skill `mcp-pentest` |
| **Pengganti 2: mcp-security-hub** (38 server, 300+ tools) | https://github.com/FuzzingLabs/mcp-security-hub | Pakai ini — lihat skill `mcp-security-hub` |
| SkillSpector (pemindai skill/MCP) | https://github.com/NVIDIA/SkillSpector | Pindai repo sebelum install apa pun |

## Format output

Tulis hasil verifikasi ke `~/workspace/catatan/log-bug-bounty.md` (tambahkan entri baru, jangan timpa log lama) dengan format:

```
Tanggal: <YYYY-MM-DD>
Verifikasi: MetasploitMCP (GH05TCREW)
Push terakhir repo: <tanggal + sumber pengecekan>
Status repo: <AKTIF / STALE / DIARSIPKAN>
Keputusan: <JANGAN PAKAI — <alasan> / PAKAI BERSYARAT — <syarat, bila Gerbang 1–3 lulus>>
Pengganti yang dipakai: <mcp-pentest / mcp-security-hub>
```

Bila keputusan JANGAN PAKAI, laporkan juga ke Muse supaya rujukan ke MetasploitMCP dihapus dari rencana kerja tim.

## Catatan yang belum terverifikasi

- Status "push terakhir Februari 2026" berasal dari artikel per 23 Nov 2026 — repo bisa saja hidup lagi setelah itu. Gerbang 1 ada justru untuk mengecek fakta terbaru; JANGAN jadikan tanggal Februari 2026 sebagai fakta abadi tanpa cek ulang.
- Skill ini belum pernah dipakai untuk verifikasi nyata; belum ada catatan verifikasi MetasploitMCP di log.
