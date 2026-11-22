**⛔ STATUS: BATAL — DIBUANG perintah Cipta 22 Nov 2026 16:25 ("Yang lain buang"). Jangan dilaksanakan, jangan diungkit tanpa perintah baru Cipta. Isi di bawah ini ARSIP saja. Alasan: Carbon berbayar; fokus hanya yang gratis (Hydrogen).**

---

# Rencana Kombinasi Hydrogen + Carbon — ⛔ BATAL

**Status: RENCANA SAJA (22 Nov 2026). Carbon BELUM aktif. Keputusan saat ini: yang FREE saja (15:48) + Hydrogen dulu untuk SEMUA agent (16:07).**

## Hydrogen dulu, semua (perintah Cipta 16:07 — WAJIB)

Hydrogen (gratis, free tier ~20 panggilan/hari) dipakai DULU untuk SEMUA agent — bukan cuma pilot A27. Carbon menyusul nanti (kombinasi, setelah Cipta setuju biayanya). Runner `agents/hydrogen-momo.py` adalah otak bersama semua agent (default `--model hydrogen`).

**Disiplin kuota 20/hari (dipakai BERSAMA semua agent — hemat!):** prioritas (1) triase pesan masuk A27, (2) hook/naskah video Oyen/A11/A17, (3) riset/draf penting; tugas rutin pakai aturan/file, bukan Hydrogen; 1 panggilan per tugas, retry maks 1x; pemakaian tercatat di `data/log-penggunaan-model.jsonl`; runner memberi peringatan bila hari ini sudah ≥15 panggilan; bila kuota habis di tengah hari, tugas Hydrogen ditunda ke besok — jangan pakai model berbayar sebagai jalan pintas.

## Peran masing-masing (perintah Cipta 16:05–16:06)

| Model | Peran | Biaya | Status |
|---|---|---|---|
| **Hydrogen** (gemini-4-hydrogen) | Tugas sehari-hari: riset, draf naskah, draf balasan, ringkasan | GRATIS (free tier API, ~20 panggilan/hari) | AKTIF — runner `agents/hydrogen-momo.py` |
| **Carbon** (gemini-4-carbon) | OTAK STANDBY: menilai pesan masuk (email + DM) secara berkala — mana yang penting/urgent — lalu bertindak atau meneruskan | BERBAYAR: $2/$10 per 1 jt token s.d. 30 Nov 2026, lalu $4/$20; kuota gratis 0 | BELUM AKTIF — terkunci, butuh persetujuan biaya Cipta |

## Catatan jujur soal standby

Standby itu sendiri adalah kerja SISTEM (cron + watchdog yang membangunkan agent): cron `cek-pesan-masuk-sosial`, `cek-chat-customer-wa`, `cek-email-customer-cepat` yang berjalan berkala. Carbon hanya otaknya — yang menilai isi pesan. Karena Carbon berbayar per token, standby terus-menerus dengan Carbon berarti biaya token jalan terus (setiap pengecekan = panggilan model). Perkiraan biaya standby harian HARUS dihitung dulu sebelum diaktifkan (jumlah cek/hari × token/cek × tarif) — jangan aktifkan tanpa angka ini.

## Cara mengaktifkan nanti (bila Cipta menyetujui biayanya)

1. Cipta menyetujui biaya Carbon (dicatat di `~/workspace/catatan/keputusan.md` + file `data/persetujuan-carbon.md` dibuat).
2. Set env `SATUKIKI_CARBON_APPROVED=1` pada pemanggil.
3. Yang diganti HANYA model di pemanggil cron standby: `--model hydrogen` → `--model carbon` (cron `cek-pesan-masuk-sosial`, `cek-chat-customer-wa`, `cek-email-customer-cepat`). Tidak ada perubahan kode lain — runner sudah bisa pilih model.
4. Pantau pemakaian lewat `data/log-penggunaan-model.jsonl` + tagihan Gemini API; bila biaya melewati batas yang disetujui, kembalikan ke Hydrogen.

## Kunci pengaman (jangan diakali)

Runner `agents/hydrogen-momo.py` menolak Carbon (exit 3) bila file `data/persetujuan-carbon.md` TIDAK ADA atau env `SATUKIKI_CARBON_APPROVED` bukan `1`. Kunci ini ada supaya tidak ada biaya yang jalan tanpa persetujuan Cipta. Aturan Cipta yang berlaku: bayar = SALAH tanpa izin.

## Kendala Hydrogen gratis (dicatat 22 Nov 2026)

Hydrogen free tier TIDAK STABIL saat beban tinggi: 22 Nov tercatat 4x gagal (2x HTTP 503 overload + 1x read timeout + 1x 503 lagi pada smoke test runner baru) berbanding 2x berhasil (draf Ep 2 + hook Oyen). Bila Hydrogen gagal: coba lagi sekali; bila tetap gagal, kerjakan tugas secara langsung (koordinator/Muse) dan catat kegagalannya. JANGAN pakai model berbayar sebagai jalan pintas. Model cadangan GRATIS masih dicari (bukan berbayar).
