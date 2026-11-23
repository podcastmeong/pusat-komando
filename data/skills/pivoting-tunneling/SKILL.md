# Skill: Pivoting & Tunneling — Pivoting & tunneling: memakai satu host yang sudah ditembus sebagai batu loncatan menyerang jaringan internal di belakang firewall.

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Sumber: `~/workspace/catatan/riset-skill-spionase-hacking-sabotase-100-2026-11-24.md`, kandidat HACKING No. 54 (laporan riset skill spionase-hacking-sabotase 100, 24 Nov 2026). Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Aturan utama — HANYA UNTUK BOUNTY

Skill ini HANYA dipakai dalam 9 program bounty resmi — **Muse (Meta), OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr**. Di luar program resmi = tidak boleh dipakai. Program yang dilayani skill ini: **HUNTR, PPLX, MISTRAL**.

Catatan program: Google AI VRP mengecualikan direct prompt injection, jailbreak, halusinasi, dan system-prompt-leak — bila kandidat menyentuh itu, arahkan ke MUSE/OAI-S/0DIN/VK/ANTH, bukan G-VRP. Perplexity VDP: jangan pakai kata "prompt injection"/"hallucination"/"model safety" dalam laporan — bingkai sebagai aksi tanpa izin via grant yang dipakai ulang.

## Pemicu (kapan dipakai)

Dipakai saat ada hipotesis pivoting & tunneling: memakai satu host yang sudah ditembus sebagai batu loncatan menyerang jaringan internal di belakang firewall. Dipakai sesudah permukaan target dipetakan dan hipotesis dirumuskan — skill ini adalah panduan PENGUJIAN operasionalnya, bukan konsepnya. Scope guard laporan: Hanya lab/jaringan sendiri atau aset in-scope eksplisit.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji kerentanan ini, mendokumentasikan bukti read-only |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- `metasploit-framework` (No. 40) — modul dan sesi yang dipakai sebagai titik pivot
- `eksploitasi-eternalblue-smb-lab` (No. 53) — pola menembus satu host lab
- `pemindaian-port-layanan` — pemindaian dari titik pivot
- `triase-duplikat` + `laporan-abstrak` — validasi dan pelaporan
- Pembuktian dampak umum + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, Perplexity VDP, Mistral VDP, Anthropic, huntr). Di luar itu jangan diuji.
2. **Hanya akun sendiri + canary palsu.** Tanpa data orang lain, tanpa menyentuh sesi/browser/perangkat pengguna lain.
3. **Tanpa data orang lain.** Jangan membaca, menyalin, atau memakai data milik pengguna lain — walau terlihat.
4. **Tanpa uji korban.** Victim-agent fraud tests DIBLOKIR — jangan pernah menguji terhadap korban sungguhan atau akun yang bukan milik sendiri.
5. **Tanpa DoS/DDoS.** Jangan membanjiri server target dengan permintaan; pakai jeda antar-permintaan dan hentikan bila target melambat.
6. **Tanpa payload di permukaan publik.** Halaman/file PoC jangan di-host di tempat umum — hanya di lingkungan terkendali milik sendiri.
7. **Validasi human-in-the-loop.** Setiap klaim harus diperiksa manusia (Muse/A60) sebelum ditulis sebagai temuan — jangan kirim hasil mentah otomatisasi.
8. **Tanpa laporan tanpa persetujuan Cipta.** Temuan ditulis sebagai DRAF dulu; Muse yang meneruskan ke Cipta.
9. **Patuhi larangan otomasi program.** huntr: "Humans only" — otomasi berujung banned. Gray Swan dilewati total — jangan dibangun, jangan didaftar, jangan dieksekusi.
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG menghapus/mengubah data, merusak layanan, menyebar paket/file berbahaya, atau memakai kredensial yang terbaca di luar PoC. Pembuktian HARUS aman, minimal, dan reversibel.
11. **Scope guard kandidat ini (WAJIB):** Hanya lab/jaringan sendiri atau aset in-scope eksplisit.
12. **Catatan khusus kandidat:** Scope guard laporan WAJIB: hanya lab/jaringan sendiri atau aset in-scope eksplisit. Pivoting ke jaringan internal orang lain tanpa pencantuman eksplisit adalah penyerangan, bukan bounty.

## Langkah + gerbang

### Gerbang 0 — Cek scope eksplisit dulu

- Pivoting HANYA di lab/jaringan sendiri, atau pada aset in-scope yang secara eksplisit mencantumkan jaringan internal. Tanpa pencantuman eksplisit = hanya lab.
- Catat pasal scope di log sebelum pivot apa pun.

**Standar lulus:** Pasal scope eksplisit tercatat, atau batas lab-saja dicatat. Tanpa itu = jangan mulai.

### Gerbang 1 — Petakan topologi lab / jaringan in-scope

- Gambar topologi: segmen mana yang terlihat langsung, segmen mana yang hanya terlihat dari titik pivot, dan firewall apa yang memisahkannya.
- Catat host dan layanan tiap segmen.

**Standar lulus:** Topologi tercatat.

### Gerbang 2 — Tetapkan titik pivot di host lab sendiri

- Tentukan satu host lab sendiri sebagai titik pivot; verifikasi akses ke host itu sah (lab sendiri / aset in-scope).
- Catat host pivot + cara aksesnya.

**Standar lulus:** Titik pivot tercatat + dasar aksesnya.

### Gerbang 3 — Teruskan lalu lintas lewat pivot, pindai segmen dalam

- Atur tunneling/port-forward lewat titik pivot; pindai layanan di segmen dalam dari titik pivot — hanya layanan lab sendiri / aset in-scope eksplisit.
- Jangan menyentuh host di luar lab/scope; hentikan bila lalu lintas menunjukkan host yang tidak dikenal.

**Standar lulus:** Hasil pemindaian segmen dalam tercatat; tidak ada host di luar scope yang disentuh.

### Gerbang 4 — Buktikan jangkauan + serahkan ke triase

- Buktikan jangkauan ke layanan dalam (mis. banner layanan canary di segmen dalam terbaca lewat pivot) lalu serahkan ke A60 audit → triase-duplikat → draf laporan → Cipta setuju → kirim. Bila latihan, simpan sebagai catatan lab.

**Standar lulus:** Bukti jangkauan + keputusan (laporan atau catatan lab) tercatat.

## Alat

| Alat | Cara pakai |
|---|---|
| Jaringan lab milik sendiri (dua segmen atau lebih) | Satu-satunya jaringan tempat pivoting dilatih/diuji. |
| Host lab yang sudah ditembus (milik sendiri) | Titik pivot; hanya host lab sendiri. |
| Alat tunneling (port forward, proxychains, modul pivot Metasploit) | Meneruskan lalu lintas lewat titik pivot di lab. |
| `~/workspace/catatan/log-bug-bounty.md` | Log topologi lab, titik pivot, dan hasil. |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Tanggal: [YYYY-MM-DD]
Skill: [pivoting-tunneling — No. 54]
Target: [program + target in-scope]
Hipotesis: [apa yang diuji + dasarnya]
Langkah: [gerbang yang dijalankan + hasil tiap gerbang]
Bukti: [bukti minimal pada akun/lab sendiri — tanpa data orang lain]
Yang TIDAK dilakukan: [tanpa data orang lain, tanpa DoS, tanpa aksi destruktif, tanpa uji korban]
Keputusan triase: [maju / ditolak + alasan, diputuskan A60]
Status: [DRAF — menunggu persetujuan Cipta / dikirim / ditolak]
```

## Batasan yang diketahui

- Jaringan internal yang terlihat dari titik pivot sering berisi host yang tidak tercantum di scope — host yang tidak dikenal jangan disentuh, catat keberadaannya saja dan tanyakan ke Muse.
- Skill ini tidak menulis payload exploit siap pakai atau kode eksploitasi lengkap — hanya METODE, pola, dan langkah pengujian. Pola probe kecil untuk identifikasi boleh bila metodenya memang butuh itu.
- Tanpa bukti reproduksi langkah-demi-langkah pada akun/lab sendiri, temuan belum terbukti — jangan maju ke laporan.
