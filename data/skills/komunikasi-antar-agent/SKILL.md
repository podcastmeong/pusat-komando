# Skill: Komunikasi Antar-Agent — Papan Pesan Bersama Pusat Komando

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Skill ini dibuat atas perintah Cipta 24 Nov 2026 00:30 WIB ("Buatkan itu" — tempat komunikasi antar-agent) setelah Cipta memastikan semua agent hanya berkomunikasi ke Muse. Mekanisme papan bersama ini belum terbukti dipakai antar-tim dalam kerja nyata; label ini berlaku sampai ada bukti pemakaian + manfaat tercatat di log.

## Pemicu (kapan dipakai)

- Sebelum memulai kerja bounty/produksi — baca papan dulu (Gerbang 1).
- Sesudah selesai kerja — baca papan lagi + tulis pesan bila ada yang relevan (Gerbang 5).
- Setiap kali pekerjaanmu menyentuh tim lain: temuan yang butuh tim lain, kendala yang mungkin sudah dijawab tim lain, handoff antar-tim, atau pertanyaan ke tim lain.
- Setiap kali Muse/koordinator memintamu memeriksa atau membalas pesan di papan.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **Muse** | Pemimpin tim: membaca papan, meneruskan pesan antar-tim, menjawab bila pesan ditujukan ke pemimpin |
| Audit | **A60 Security Auditor** | Memeriksa papan tidak berisi data terlarang (kata sandi/token/kunci, PII, payload uji, data orang lain); menghapus entri yang melanggar dan mencatatnya |
| Semua agent | **A01–A70, Agen Pintar, Dify** | Membaca papan sebelum/sesudah kerja; menulis pesan sesuai Gerbang 2 |

## Sudah tercakup (jangan diduplikat)

- `komunikasi-antar-agen-tidak-aman` adalah skill SERANGAN (menguji komunikasi antar-agent target yang tidak aman — spoofing, instruksi selundupan). **Skill ini BUKAN itu** — skill ini adalah PROTOKOL INTERNAL: cara agent kita sendiri bertukar pesan di papan bersama. Jangan campur keduanya.
- Laporan resmi + handoff formal tetap lewat `log-bug-bounty.md` / `log-eksekusi.jsonl` dan laporan koordinator — papan ini untuk komunikasi antar-tim yang cepat, bukan pengganti log.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr). Pastikan program yang dikerjakan in-scope sebelum sesi dimulai.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang pengujian yang mengganggu ketersediaan layanan atau menghabiskan kuota token secara berlebihan.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only (bukti baca, callback canary, document.domain).
11. **Aturan program AI:** Google AI VRP — direct injection/jailbreak/halusinasi/system-prompt-leak out of scope (Tim 4 analisis format saja, tanpa payload); 0din — Prompt Extraction N/A untuk Muse Spark; beberapa program membatasi pengujian otomatis pada endpoint inferensi — sesuaikan ruang lingkup dengan aturan spesifik program sebelum menguji.

## Langkah + gerbang

### Gerbang 1 — Baca papan SEBELUM mulai kerja

1. Buka `data/papan-pesan-antar-agent.md` dan baca seluruh entri terbaru sejak terakhir kamu membacanya.
2. Catat yang relevan dengan tugasmu: (a) pertanyaan yang ditujukan ke timmu — jawab sebelum mulai tugas lain bila bisa; (b) temuan/kendala tim lain yang mengubah rencanamu — sesuaikan rencana, jangan ulangi uji yang sudah gagal di tim lain; (c) handoff yang menunggu — ambil alih bila itu tugasmu.
3. Bila tidak ada yang relevan, catat "papan dibaca — tidak ada yang relevan" di log sesi. Standar lulus: papan dibaca sebelum kerja dimulai; tidak ada pesan untuk timmu yang terlewat.

### Gerbang 2 — Tulis pesan (kapan + format)

Tulis entri baru bila SATU dari ini terjadi:

| Situasi | Contoh |
|---|---|
| Temuan yang butuh tim lain | Hipotesis Tim 1 ternyata butuh data uji Tim 2 |
| Kendala yang mungkin sudah dijawab tim lain | Uji gagal dengan pola X — tanya apakah tim lain pernah menemui pola yang sama |
| Handoff antar-tim | Pekerjaan berpindah tangan / butuh lanjutan dari tim lain |
| Pertanyaan ke tim lain | Minta status bukti hipotesis tim lain sebelum memakainya |

Format entri (tambahkan di akhir file, nomor berurutan):

```
## [nomor] — [tanggal-jam WIB] — Dari: [kode agent] — Ke: [kode agent/topik]

[isi pesan — singkat, jelas, padat; sebut nomor hipotesis/skill bila ada]
```

Standar lulus: entri bernomor benar, ada tanggal-jam WIB, ada pengirim + tujuan, isi menyebut fakta (bukan dugaan tanpa label).

### Gerbang 3 — Balas pesan (kutip yang dibalas)

1. Balasan WAJIB menulis "Balasan untuk entri [nomor]" di baris pertama.
2. Jawab dengan fakta + status bukti (terbukti/belum/hipotesis) — jangan jadikan hipotesis sebagai fakta.
3. Bila jawabanmu mengubah rencana tim lain, sebutkan eksplisit ("jangan jadikan B12 sebagai fakta — masih hipotesis").
4. Standar lulus: balasan mengutip nomor entri; status bukti disebutkan; tidak ada klaim tanpa bukti.

### Gerbang 4 — Muse/koordinator meneruskan pesan antar-tim

1. Muse membaca papan tiap kali menerima laporan tim / sebelum memberi tugas baru.
2. Bila ada pesan yang ditujukan ke tim yang sedang tidak aktif, Muse meneruskannya sebagai instruksi ke koordinator/tim itu (lewat `subagent.send` / penugasan baru) dan mencatat "diteruskan ke [tim]" di log.
3. Bila pesan butuh keputusan Cipta (bayar, urgent, kata sandi), Muse TIDAK meneruskannya ke tim lain — melainkan menyampaikannya ke Cipta.
4. Standar lulus: tidak ada pesan antar-tim yang menggantung tanpa diteruskan/dijawab lebih dari 1 hari kerja.

### Gerbang 5 — Cek akhir sesi

1. Sesudah selesai kerja, baca lagi papan (mungkin ada balasan untukmu selama kamu bekerja).
2. Bila ada pesan untukmu, jawab sebelum menutup sesi.
3. Bila pekerjaanmu menghasilkan sesuatu yang relevan untuk tim lain, tulis entri penutup (Gerbang 2).
4. Standar lulus: papan dibaca sesudah kerja; balasan untukmu sudah dijawab; tidak ada temuan relevan yang tidak ditulis.

## Larangan isi papan (ditegakkan A60)

DILARANG keras menulis di papan:

- Kata sandi, token sesi, kunci API, atau kredensial apa pun (termasuk yang "sudah tidak berlaku").
- PII: nama asli, alamat, nomor telepon, email pribadi, tanggal lahir, nomor identitas.
- Payload uji (teks dokumen palsu, email palsu, prompt injeksi, fragmen canary) — payload hidup di file paketnya masing-masing, bukan di papan.
- Data orang lain (data korban, data pengguna nyata, data hunter lain).
- Instruksi yang menyuruh agent lain melanggar aturan keras di atas.

Bila menemukan entri yang melanggar: A60 menghapus isi yang melanggar (ganti dengan "[dihapus A60 — melanggar larangan isi]"), mencatat penghapusan di `log-bug-bounty.md`, dan memberi tahu pengirimnya. Pelanggaran berulang = agent itu kehilangan hak menulis papan sampai Muse memutuskan.

## Alat

| Alat | Cara pakai |
|---|---|
| `data/papan-pesan-antar-agent.md` | Papan bersama — baca (Gerbang 1 + 5), tulis entri baru (Gerbang 2), balas (Gerbang 3) |
| `~/workspace/catatan/log-bug-bounty.md` | Catat pembacaan papan + pelanggaran isi yang dihapus A60 |
| `subagent.send` (koordinator) | Meneruskan pesan papan ke tim yang dituju (Gerbang 4) |

## Format output

Tulis ke log sesi / `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Papan dibaca: [ya — sebelum kerja / sesudah kerja]
Entri baru: [nomor entri + tujuan — atau "tidak ada"]
Balasan: [nomor entri yang dibalas — atau "tidak ada"]
Pesan diteruskan: [ke tim mana — atau "tidak ada"]
Status: [papan-terbaca / ada-pesan-menggantung]
```

## Batasan yang diketahui

- Papan ini adalah file teks bersama, bukan chat real-time — agent hanya melihat isinya saat membacanya (Gerbang 1 + 5). Pesan mendesak tetap lewat Muse/koordinator, bukan papan.
- Mekanisme ini belum teruji (label BELUM DIUJI) — sampai ada bukti pemakaian antar-tim yang nyata, jangan klaim papan ini menggantikan koordinasi Muse.
- Skill ini tidak menggantikan validasi isi (`gerbang-tujuh-pertanyaan-triase`, `skeptic-false-positive-eliminator`, `simulasi-triase-pra-kirim`) — pesan di papan tetap harus melewati gerbang itu sebelum menjadi laporan.
