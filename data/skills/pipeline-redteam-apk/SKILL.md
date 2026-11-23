# Skill: Pipeline Redteam APK — Akuisisi, Dekompilasi, Frida & Intent Injection

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 62, Claude-BugHunter `apk-redteam-pipeline`, 1 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program bounty in-scope secara EKSPLISIT mencakup aplikasi mobile Android (nama paket / APK tercantum di scope).
- Ditemukan APK target yang perlu diaudit ujung-ke-ujung: dari akuisisi sampai runtime.
- **Tanpa pencantuman aplikasi mobile secara eksplisit di scope, skill ini TIDAK dipakai** — bedah APK di luar scope bukan bounty.
- Dipakai SETELAH `dekompilasi-aplikasi-mobile` (bedah statis) dipahami — skill ini menambahkan akuisisi otomatis, runtime Frida, komponen terekspos, dan intent injection.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan pipeline akuisisi → statis → runtime |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- **Dekompilasi APK statis** (ekstraksi endpoint/secret dari APK) → skill `dekompilasi-aplikasi-mobile`. Skill ini TIDAK mengulang bedah statisnya — hanya memakai hasilnya sebagai input tahap 2, lalu menambah akuisisi otomatis, analisis runtime Frida, komponen terekspos, dan intent injection.
- **Pembalikan signing klien** (rekonstruksi signing agar replay bisa berjalan) → skill `pembalikan-klien-signing`. Skill ini TIDAK mengulang rekonstruksi signing — bila API di balik APK butuh signing, pakai skill itu.
- **Analisis statis JS** → skill `analisis-statis-js` (untuk WebView/JS di dalam APK, bila relevan).

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN aplikasi mobile tercantum eksplisit.** Bila program hanya mencantumkan website, JANGAN mengunduh/membedah APK-nya.
2. **Hanya akun sendiri + canary palsu.** Semua pengujian runtime memakai akun uji sendiri di perangkat/emulator uji sendiri.
3. **Tanpa data orang lain.**
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang membanjiri API backend dari APK.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG:** mengubah data pengguna lain lewat intent/component yang terekspos, menghapus data, atau mengeksekusi transaksi nyata dari perangkat uji.
11. **Jangan mengunggah APK hasil modifikasi ke Play Store atau membagikannya.** APK yang di-instrumentasi HANYA dipakai di perangkat/emulator uji sendiri.
12. **Jangan melewati pembayaran/lisensi.** Instrumentasi runtime HANYA untuk menguji keamanan API/komponen — BUKAN untuk membuka fitur berbayar atau mengakali lisensi.

## Langkah + gerbang

### Gerbang 1 — Akuisisi APK otomatis

Dapatkan APK target yang SAMA dengan versi yang tercantum di scope. Standar lulus: APK didapat + hash dicatat + versi cocok dengan scope.

| Sumber | Cara | Catatan |
|---|---|---|
| Play Store | Unduh via perangkat uji sendiri (akun uji sendiri) atau tool akuisisi yang sah | Sumber utama; versi terbaru |
| apkpure | Fallback bila Play Store tidak bisa diakses dari perangkat uji | Verifikasi hash + nama paket cocok |
| apkmirror | Fallback kedua | Verifikasi hash + nama paket + signature cocok dengan Play Store |

Verifikasi: nama paket (`package`) cocok dengan scope; versi (`versionName`/`versionCode`) cocok; bila hash berbeda antar sumber, pakai yang dari Play Store dan catat perbedaannya.

### Gerbang 2 — Dekompilasi + pencarian statis (pakai `dekompilasi-aplikasi-mobile`)

1. Dekompilasi dengan `jadx` (atau `apktool` + `dex2jar`).
2. Cari: secret/kunci API, URL endpoint, token JWT, konfigurasi Firebase, string hardcoded — dengan `grep` / `jadx` search.
3. Catat temuan statis (endpoint + secret yang teramati) — JANGAN memakai secret itu di luar sesi uji, dan sensor sebelum dicatat.

### Gerbang 3 — Ekstraksi pinned-cert & enumerasi komponen terekspos

1. **Pinned cert:** ekstrak sertifikat yang di-pin (dari `network_security_config.xml`, `res/raw/`, atau kode pinning) — catat apakah pinning ada dan di mana. Pinning BUKAN temuan dengan sendirinya; catat sebagai prasyarat untuk instrumentasi runtime (Gerbang 4).
2. **Komponen terekspos:** enumerasi dari `AndroidManifest.xml` — Activity, Service, Broadcast Receiver, Content Provider dengan `android:exported="true"` (atau intent-filter tanpa `exported=false` di API <31). Catat tiap komponen + permission yang melindunginya (bila ada).

### Gerbang 4 — Instrumentasi runtime Frida (perangkat/emulator uji sendiri)

Template instrumentasi Frida — jalankan HANYA di perangkat/emulator uji sendiri dengan APK target + akun uji sendiri:

```javascript
// Template Frida — instrumentasi runtime APK uji sendiri
// Jalankan: frida -U -f <nama-paket> -l script.js --no-pause
Java.perform(function () {
    // 1. Bypass SSL pinning (HANYA di perangkat uji sendiri, untuk mencegat traffic sendiri)
    //    — catat bahwa pinning berhasil dilewati di perangkat uji, bukan di perangkat korban.
    // 2. Hook fungsi kriptografi / penyimpanan: catat kunci/parameter yang dipakai
    //    saat AKUN UJI SENDIRI login — jangan catat data pengguna lain.
    // 3. Hook pemanggilan API: catat endpoint + parameter yang dikirim dari sesi sendiri.
    console.log("[*] Frida terpasang pada sesi uji sendiri");
});
```

Aturan Frida: (a) hanya perangkat/emulator uji sendiri; (b) hanya akun uji sendiri; (c) jangan menyimpan kunci/token yang tertangkap ke file yang dibagikan — sensor di log; (d) bila pinning tidak bisa dilewati tanpa modifikasi APK yang berisiko, catat sebagai batas dan lanjutkan dengan analisis statis saja.

### Gerbang 5 — Probe injeksi intent (komponen terekspos)

Untuk tiap komponen terekspos dari Gerbang 3, uji dengan intent yang berisi canary milik sendiri:

```bash
# Contoh probe intent — HANYA komponen in-scope, HANYA canary sendiri
adb shell am start -n <paket>/<aktivitas-tereekspos> \
  --es "canary" "intent-probe-own-test-123"
adb shell am broadcast -a <aksi-receiver-tereekspos> \
  --es "canary" "intent-probe-own-test-123"
```

Indikator: komponen merespons intent eksternal tanpa otorisasi (mis. Activity sensitif terbuka, Service menjalankan aksi, Provider mengembalikan data) = kandidat. **STOP bila komponen itu mengakses/mengubah data pengguna lain** — cukup buktikan keterbukaannya, jangan eksploitasi isinya.

### Gerbang 6 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = secret/endpoint bocor dari statis + terbukti dipakai / komponen terekspos merespons intent eksternal / runtime menunjukkan data sensitif tanpa proteksi — dengan bukti pada sesi sendiri. **TOLAK** = sekadar "APK bisa didekompilasi" atau "komponen exported=true" tanpa pembuktian respons.
2. **Reproduksibilitas:** ulangi probe minimal 2×; simpan perintah + output (dengan sensor).
3. **Higienitas bukti:** sensor token, secret, kunci, dan data pribadi sebelum dilampirkan (`[REDACTED]`). JANGAN lampirkan APK hasil instrumentasi.

Hanya temuan yang lolos keenam gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| Play Store / apkpure / apkmirror | Akuisisi APK (verifikasi nama paket + hash) |
| `jadx` / `apktool` | Dekompilasi + pencarian statis (lihat `dekompilasi-aplikasi-mobile`) |
| Frida (`frida-server` di emulator/perangkat uji) | Instrumentasi runtime — perangkat uji sendiri saja |
| `adb` | Probe intent + enumerasi komponen |
| `pembalikan-klien-signing` | Bila API di balik APK butuh rekonstruksi signing |
| `~/workspace/catatan/log-bug-bounty.md` | Log tiap tahap pipeline + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + nama paket + versi APK + hash]
Akuisisi: [sumber + hash + versi cocok scope ya/tidak]
Statis: [secret/endpoint yang ditemukan — disensor]
Komponen terekspos: [daftar komponen exported=true + hasil probe intent]
Runtime Frida: [apa yang teramati pada sesi sendiri]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Nama Paket] - [Kelas: Komponen Terekspos / Secret Bocor / Intent Injection] menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `apk-redteam-pipeline`, 1 laporan terungkap), bukan pengalaman teruji — tiap tahap butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Skill ini HANYA dipakai bila program in-scope secara eksplisit mencakup aplikasi mobile.** Program web biasa = JANGAN dipakai.
- Frida di perangkat non-root / Android baru sering butuh patching APK — bila patching tidak memungkinkan di perangkat uji, catat sebagai batas dan lanjutkan dengan analisis statis + probe intent saja.
- Secret yang ditemukan di APK sering sudah tidak berlaku / sudah dirotasi — verifikasi apakah secret itu masih berfungsi pada API in-scope (dengan akun uji sendiri) sebelum mengklaim dampak; secret mati = TOLAK.
- Pipeline ini paling bernilai bila digabung dengan `pembalikan-klien-signing` (API di balik APK) dan `dekompilasi-aplikasi-mobile` (statis) — jangan laporkan "APK bisa didekompilasi" sebagai temuan; laporkan APA yang ditemukan di dalamnya dan apa dampaknya.
