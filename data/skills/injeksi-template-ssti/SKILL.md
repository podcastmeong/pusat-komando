# Skill: Injeksi Template SSTI — Kenali Template Engine, Uji RCE Aman

> Dibangun dari riset "50 Skill Esensial AI Agent Pemburu Bug Bounty" (23 Nov 2026, `~/workspace/catatan/referensi-50-skill-esensial-bounty-2026-11-23.md`, Fase 5 butir 31).
> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh langkah di bawah ini belum pernah dijalankan sampai temuan terbayar; label ini berlaku untuk semua bagian sampai ada satu kasus nyata yang lolos triase dan dicatat di log.

## Pemicu (kapan dipakai)

Dipakai saat input pengguna diduga dirender sebagai template server-side — nama/profil/pesan yang tampil kembali dengan sintaks template yang ikut dievaluasi, atau halaman yang merespons ekspresi template (`{{7*7}}` menjadi `49`). Dipakai sesudah fondasi dikuasai (`fondasi-kerentanan-web-api`) dan hipotesis dirumuskan (`kopilot-analisis-kode`) — skill ini adalah panduan PENGUJIAN operasionalnya.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62 Exploit Developer** | Menguji deteksi engine + pembuktian RCE aman, mendokumentasikan bukti |
| Pengerjaan | **A58 Vulnerability Researcher** | Merumuskan hipotesis + menentukan engine dari petunjuk |
| Audit | **A60 Security Auditor** | Memvalidasi bukti sebelum jadi draf laporan (A60 tidak meloloskan temuannya sendiri) |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Konsep injeksi secara umum → skill `fondasi-kerentanan-web-api` (skill ini menambah LANGKAH deteksi engine + uji RCE aman, bukan mengulang konsepnya).
- Variasi payload secara sistematis (satu dimensi per putaran, log nilai → respons) → skill `rekonstruksi-iterasi-payload`.
- Rumusan hipotesis dari kode → skill `kopilot-analisis-kode`.
- Eksekusi perintah OS secara umum → skill `injeksi-perintah-rce` (skill ini khusus jalur TEMPLATE; bila SSTI terbukti sampai RCE, pembuktian perintahnya mengikuti aturan allowlist skill itu).
- Validasi temuan + laporan triage-ready → skill `triase-duplikat` + `laporan-abstrak`; filter false positive akhir → skill `skeptic-false-positive-eliminator`.

## Aturan keras

1. **Hanya program bounty resmi in-scope** (Muse/Meta, OpenAI Safety, 0din, Google AI VRP, ViKernel, huntr).
2. **Hanya akun sendiri + canary palsu.**
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS/DDoS.**
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **LARANGAN DESTRUKTIF — MUTLAK.** DILARANG membaca file sensitif server (`/etc/passwd`, `.env`, konfigurasi, kredensial), DILARANG menulis file ke server, DILARANG menghapus/mengubah data apa pun. Pembuktian HARUS aman.
11. **Bukti RCE aman yang diizinkan:** eksekusi yang hanya mengembalikan canary (mis. `echo CANARY-UNIK`), `id`, atau callback DNS/HTTP ke canary OAST milik sendiri. DILARANG `cat` file, `curl` ke layanan internal, reverse shell, atau perintah apa pun yang membaca/menulis data.
12. **DILARANG dump konfigurasi/rahasia.** Ekspresi seperti `{{ config }}`, `{{ config.items() }}`, atau `{{ self }}` yang menampilkan konfigurasi/kredensial aplikasi DILARANG dipakai — walau itu "hanya pembuktian". Bukti cukup dengan evaluasi aritmetika + echo canary.
13. **Teknik web klasik ini untuk program web/API klasik (huntr dsb.), BUKAN untuk bounty agen AI** — kecuali scope program itu menyatakan pengujian web klasik berlaku. Jangan pakai skill ini untuk Google AI VRP (payload injeksi DIBLOKIR; Tim 4 analisis format saja).

## Langkah + gerbang

### Gerbang 0 — Cek scope + larangan otomasi dulu

1. Baca pasal scope program: apakah pengujian injeksi template diizinkan pada target ini? Apakah otomasi dilarang (huntr "Humans only" = uji manual saja)?
2. **Standar lulus:** pasal scope + aturan otomasi tercatat di log sebelum satu payload pun dikirim. Tanpa itu = jangan mulai.

### Gerbang 1 — Deteksi: apakah input dievaluasi sebagai template?

1. Kirim ekspresi aritmetika sederhana yang hasilnya beda bila dievaluasi vs ditampilkan mentah: `{{7*7}}` (hasil `49` bila dievaluasi), `${7*7}`, `#{7*7}`, `<%= 7*7 %>`, `*{7*7}`.
2. Uji juga dengan string: `{{7*'7'}}` — Jinja2/Twig menghasilkan `49` (string dikali) atau `7777777`; perbedaan ini membantu membedakan engine.
3. **Standar lulus:** respons menampilkan HASIL evaluasi (bukan teks payload mentah) pada minimal satu sintaks. Payload tampil mentah = tidak ada SSTI di permukaan itu, catat dan pindah permukaan.

### Gerbang 2 — Kenali template engine

1. Bedakan engine dari perilaku sintaks (uji satu sintaks per putaran):

   | Engine | Bahasa/stack | Uji deteksi | Hasil bila engine itu |
   |---|---|---|---|
   | Jinja2 | Python (Flask) | `{{7*7}}` | `49` |
   | Twig | PHP (Symfony) | `{{7*'7'}}` | `49` |
   | Freemarker | Java | `${7*7}` | `49` |
   | Thymeleaf | Java (Spring) | `[[${7*7}]]` | `49` |
   | ERB | Ruby | `<%= 7*7 %>` | `49` |
   | Velocity | Java | `#set($x=7*7)$x` | `49` |
   | Smarty | PHP | `{7*7}` | `49` |
   | Handlebars | JS | `{{#with "x"}}{{this}}{{/with}}` | perilaku khas (bukan RCE langsung) |

2. Bila `{{7*7}}` menghasilkan `49` tapi `{{7*'7'}}` menghasilkan `7777777` → Jinja2. Bila keduanya `49` → Twig. Catat petunjuk stack (header `X-Powered-By`, teknologi dari recon) sebagai pendukung, bukan bukti.
3. **Standar lulus:** engine teridentifikasi dengan SATU perilaku pembeda yang tercatat. Engine belum jelas = lanjut Gerbang 3 dengan payload generik yang aman, jangan menebak RCE spesifik engine.

### Gerbang 3 — Konfirmasi eksekusi aman (tanpa baca/tulis file)

1. Konfirmasi dengan ekspresi yang mengembalikan canary tanpa efek samping, mis. Jinja2: `{{ 'CANARY-UNIK' }}` atau `{{ cycler('CANARY','x').current }}`; Twig: `{{ 'CANARY-UNIK' }}`; Freemarker: `${"CANARY-UNIK"}`.
2. Bila tersedia jalur OAST: konfirmasi blind SSTI via callback DNS/HTTP ke canary milik sendiri (lihat `ssrf-oast` untuk penyiapan canary).
3. **Standar lulus:** canary kembali persis di respons (atau hit canary tercatat) dan TIDAK ADA file yang dibaca/ditulis. Bukti ini saja sudah cukup untuk mengklaim "template injection terbukti".

### Gerbang 4 — Uji RCE aman (HANYA bila Gerbang 3 lolos, dan hanya echo canary)

1. Bila engine mengizinkan akses objek (mis. Jinja2), uji RCE dengan perintah yang HANYA meng-echo canary, mis. Jinja2: `{{ namespace.__init__.__globals__.os.popen('echo CANARY-UNIK').read() }}` — dan TIDAK ADA perintah lain.
2. Perintah yang diizinkan di gerbang ini: `echo CANARY-UNIK` dan `id` saja. DILARANG: `cat`, `ls`, `curl`, `wget`, `nc`, pengalihan output (`>`), penulisan file, dan segala bentuk shell interaktif/reverse shell.
3. **Standar lulus:** respons berisi canary hasil eksekusi perintah (atau hit canary OAST dari eksekusi), tanpa satu pun file dibaca/ditulis. Bila RCE tidak tercapai tapi Gerbang 3 lolos, temuan tetap dilaporkan sebagai SSTI (tanpa klaim RCE) — jangan memaksakan RCE.

### Gerbang 5 — Buktikan dampak, serahkan ke triase

1. Tulis dampak sesuai yang TERBUKTI: SSTI saja (eksekusi template) atau SSTI→RCE (echo canary). Jangan klaim "bisa membaca file server" bila hanya echo canary yang terbukti.
2. Serahkan ke A61/A68 (`triase-duplikat`): skor + cek duplikat → A60 audit → draf laporan (A67) → Cipta setuju → kirim.
3. **Standar lulus:** ada bukti reproduksi langkah-demi-langkah (payload persis + respons persis) + dampak tertulis sesuai bukti + keputusan triase tercatat. Tanpa bukti = belum berhasil, jangan maju ke laporan.

## Alat

| Alat | Cara pakai |
|---|---|
| Permintaan HTTP manual / Burp Repeater (lihat `mcp-burp-repeater`) | Kirim SATU payload template per uji, amati respons; hanya bila program mengizinkan alat itu |
| Server canary OAST milik sendiri (lihat `ssrf-oast`) | Konfirmasi SSTI blind via callback DNS/HTTP |
| Skrip pengujian buatan sendiri (Python/bash) | HANYA bila program mengizinkan otomasi (bukan huntr); satu sintaks per putaran — lihat `rekonstruksi-iterasi-payload` |
| Akun tes sendiri + data canary palsu | Satu-satunya akun dan data yang dipakai dalam pengujian |
| `~/workspace/catatan/log-bug-bounty.md` | Log semua payload template (nilai → respons → verdict) dan keputusan |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + endpoint + parameter]
Template engine: [Jinja2 / Twig / Freemarker / Thymeleaf / ERB / Velocity / belum teridentifikasi — bukti]
Payload deteksi: [payload persis + respons]
Payload bukti: [payload canary/RCE-aman persis + respons]
Dampak terbukti: [SSTI saja / SSTI→RCE echo canary]
Yang TIDAK dilakukan: [tanpa baca file sensitif, tanpa tulis file, tanpa dump config, tanpa reverse shell]
Keputusan triase: [maju / ditolak + alasan]
Status: [diuji / terbukti / dilaporkan / ditolak]
```

## Batasan yang diketahui

- Banyak engine memakai sandbox (mis. Jinja2 SandboxedEnvironment) yang memblokir akses objek — hasil negatif pada satu payload RCE bukan berarti SSTI-nya tidak ada; laporkan SSTI-nya bila Gerbang 3 lolos.
- Sintaks template kadang juga dievaluasi di sisi klien (mis. AngularJS `{{}}` di browser) — itu BUKAN SSTI server-side; bedakan dari mana hasil evaluasi berasal sebelum mengklaim.
- Skill ini tidak membahas SSTI pada engine yang jarang (Pebble, Mustache, EJS) — bila menemukannya, catat di log dan ajukan sebagai tambahan skill.
