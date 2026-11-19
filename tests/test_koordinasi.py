# ======================================================================
# Unit test Pusat Komando — bus koordinasi + tim Agent 9 (9A/9B/9C).
#
# File test asli (/tmp/test_koordinasi.py, 43 test) hilang karena /tmp
# bersifat ephemeral; suite ini dibuat ulang dari deskripsi cakupan di
# LAPORAN-KOORDINASI.md §3 (kirim/dedupe, transisi status, eskalasi R10,
# R1–R8 termasuk idempotensi + kasus "BELUM CUKUP DATA", Siklus Harian
# end-to-end + idempotensi siklus kedua, ringkasan/inbox/outbox),
# ditambah test baru untuk aturan rute R11–R13 dan modul tim 9A/9B/9C,
# lalu aturan rute R14–R16, klaim/kunci anti double-build, dan modul
# tim 9D Bangun-2, 9E Bangun-3, 9F Verifikasi & Katalog (19 Nov 2026).
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$HOME \
#     ~/workspace/audio-tools/python-packages/bin/python \
#     -m unittest tests.test_koordinasi -v
# (env bersih diperlukan karena gradio gagal impor bila variabel proxy
# VM ini terbaca — lihat LAPORAN-KOORDINASI.md §3.)
# Semua test memakai data_dir sementara — tidak menyentuh data asli.
# ======================================================================
import json
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT))

import koordinasi as K  # noqa: E402


def _tmp_data():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "data").mkdir()
    (tmp / "output").mkdir()
    return tmp, tmp / "data"


def _tulis(folder, nama, isi):
    (Path(folder) / nama).write_text(
        json.dumps(isi, ensure_ascii=False, indent=2), encoding="utf-8")


def _besok(n=3):
    return (date.today() + timedelta(days=n)).isoformat()


class Basis(unittest.TestCase):
    def setUp(self):
        self.tmp, self.data = _tmp_data()

    def _pesan(self):
        return K._muat(str(self.data))["pesan"]


# ---------------------------------------------------------------------------
# Warisan: kirim pesan + dedupe
# ---------------------------------------------------------------------------
class TestKirimPesan(Basis):
    def test_kirim_valid(self):
        p, info = K.kirim_pesan(10, 5, "product-brief", "normal",
                                "Brief layak", {"ide": "X"}, data_dir=str(self.data))
        self.assertIsNotNone(p)
        self.assertEqual(p["id"], "KB-001")
        self.assertEqual(p["status"], "baru")
        self.assertIn("terkirim", info)

    def test_ringkasan_kosong_ditolak(self):
        p, info = K.kirim_pesan(10, 5, "product-brief", "normal", "   ",
                                data_dir=str(self.data))
        self.assertIsNone(p)
        self.assertIn("wajib", info)

    def test_jenis_tidak_dikenal_ditolak(self):
        p, info = K.kirim_pesan(10, 5, "jenis-aneh", "normal", "X",
                                data_dir=str(self.data))
        self.assertIsNone(p)

    def test_prioritas_tidak_dikenal_ditolak(self):
        p, info = K.kirim_pesan(10, 5, "product-brief", "super", "X",
                                data_dir=str(self.data))
        self.assertIsNone(p)

    def test_dedupe_kunci_sama(self):
        K.kirim_pesan(10, 5, "product-brief", "normal", "A",
                      data_dir=str(self.data), kunci="k1")
        p2, info2 = K.kirim_pesan(10, 5, "product-brief", "normal", "A lagi",
                                  data_dir=str(self.data), kunci="k1")
        self.assertIsNone(p2)
        self.assertIn("duplikat", info2)
        self.assertEqual(len(self._pesan()), 1)

    def test_dedupe_setelah_ditolak_boleh_lagi(self):
        p, _ = K.kirim_pesan(10, 5, "product-brief", "normal", "A",
                             data_dir=str(self.data), kunci="k1")
        K.ubah_status_pesan(p["id"], "ditolak", data_dir=str(self.data))
        p2, _ = K.kirim_pesan(10, 5, "product-brief", "normal", "A lagi",
                              data_dir=str(self.data), kunci="k1")
        self.assertIsNotNone(p2)


# ---------------------------------------------------------------------------
# Warisan: transisi status
# ---------------------------------------------------------------------------
class TestTransisiStatus(Basis):
    def _buat(self):
        p, _ = K.kirim_pesan(10, 5, "product-brief", "normal", "A",
                             data_dir=str(self.data))
        return p["id"]

    def test_baru_ke_dibaca(self):
        pid = self._buat()
        self.assertIn("dibaca", K.ubah_status_pesan(pid, "dibaca", data_dir=str(self.data)))

    def test_dibaca_ke_dikerjakan(self):
        pid = self._buat()
        K.ubah_status_pesan(pid, "dibaca", data_dir=str(self.data))
        self.assertIn("dikerjakan", K.ubah_status_pesan(pid, "dikerjakan", data_dir=str(self.data)))

    def test_dikerjakan_ke_selesai(self):
        pid = self._buat()
        K.ubah_status_pesan(pid, "dibaca", data_dir=str(self.data))
        K.ubah_status_pesan(pid, "dikerjakan", data_dir=str(self.data))
        self.assertIn("selesai", K.ubah_status_pesan(pid, "selesai", data_dir=str(self.data)))

    def test_transisi_ilegal_baru_ke_selesai_ditolak(self):
        pid = self._buat()
        info = K.ubah_status_pesan(pid, "selesai", data_dir=str(self.data))
        self.assertIn("tidak diizinkan", info)
        self.assertEqual(self._pesan()[0]["status"], "baru")

    def test_status_terminal_selesai_terkunci(self):
        pid = self._buat()
        for s in ("dibaca", "dikerjakan", "selesai"):
            K.ubah_status_pesan(pid, s, data_dir=str(self.data))
        info = K.ubah_status_pesan(pid, "dibaca", data_dir=str(self.data))
        self.assertIn("terminal", info)

    def test_status_terminal_ditolak_terkunci(self):
        pid = self._buat()
        K.ubah_status_pesan(pid, "ditolak", data_dir=str(self.data))
        info = K.ubah_status_pesan(pid, "dibaca", data_dir=str(self.data))
        self.assertIn("terminal", info)

    def test_id_tidak_dikenal(self):
        info = K.ubah_status_pesan("KB-999", "dibaca", data_dir=str(self.data))
        self.assertIn("tidak ditemukan", info)


# ---------------------------------------------------------------------------
# Warisan: eskalasi R10
# ---------------------------------------------------------------------------
class TestEskalasiR10(Basis):
    def test_pesan_mendesak_dieskalasi_ke_muse(self):
        K.kirim_pesan(5, 2, "pengingat", "mendesak", "Uang masuk besar!",
                      data_dir=str(self.data))
        pesan = self._pesan()
        self.assertEqual(len(pesan), 2)
        self.assertEqual(pesan[1]["ke_agent"], "Muse")
        self.assertEqual(pesan[1]["jenis"], "eskalasi")

    def test_pesan_normal_tidak_dieskalasi(self):
        K.kirim_pesan(5, 2, "pengingat", "normal", "Biasa saja",
                      data_dir=str(self.data))
        self.assertEqual(len(self._pesan()), 1)


# ---------------------------------------------------------------------------
# Warisan: aturan rute R1–R8
# ---------------------------------------------------------------------------
class TestR1(Basis):
    def test_brief_layak_membuat_pesan(self):
        _tulis(self.data, "riset.json", [{"niche": "N", "ide": "I", "skor": 10,
                                          "verdict": "Layak dicoba"}])
        baru, lap = K._cek_r1({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["ke_agent"], 5)

    def test_brief_tidak_layak_tidak_membuat_pesan(self):
        _tulis(self.data, "riset.json", [{"niche": "N", "ide": "I", "skor": 3,
                                          "verdict": "Tidak disarankan"}])
        baru, _ = K._cek_r1({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_idempotent(self):
        _tulis(self.data, "riset.json", [{"niche": "N", "ide": "I", "skor": 10,
                                          "verdict": "Layak dicoba"}])
        K._cek_r1({}, str(self.data))
        baru2, _ = K._cek_r1({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_handoff_sudah_ada_melewati(self):
        _tulis(self.data, "riset.json", [{"niche": "N", "ide": "I", "skor": 10,
                                          "verdict": "Layak dicoba"}])
        _tulis(self.data, "handoff.json", [{"jenis": "product-brief",
                                            "ringkasan": "N — I (10/12, Layak dicoba)"}])
        baru, _ = K._cek_r1({}, str(self.data))
        self.assertEqual(len(baru), 0)


class TestR2(Basis):
    def test_draf_baru_membuat_dua_pesan(self):
        (self.tmp / "output" / "draf.md").write_text("draf", encoding="utf-8")
        baru, _ = K._cek_r2({}, str(self.data))
        self.assertEqual(len(baru), 2)
        self.assertEqual({b["ke_agent"] for b in baru}, {2, 8})

    def test_idempotent(self):
        (self.tmp / "output" / "draf.md").write_text("draf", encoding="utf-8")
        K._cek_r2({}, str(self.data))
        baru2, _ = K._cek_r2({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_handoff_sudah_ada_melewati(self):
        (self.tmp / "output" / "draf.md").write_text("draf", encoding="utf-8")
        _tulis(self.data, "handoff.json", [{"jenis": "draft-approval",
                                            "isi": {"file": "output/draf.md"}}])
        baru, _ = K._cek_r2({}, str(self.data))
        self.assertEqual(len(baru), 0)


class TestR3(Basis):
    def _lomba(self, hari, ai="diizinkan", status="baru"):
        return [{"nama": "L", "tenggat": _besok(hari), "kebijakan_ai": ai,
                 "status": status}]

    def test_tenggat_dekat_membuat_pesan(self):
        _tulis(self.data, "lomba.json", self._lomba(3))
        baru, _ = K._cek_r3({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["prioritas"], "tinggi")

    def test_tenggat_jauh_tidak_membuat_pesan(self):
        _tulis(self.data, "lomba.json", self._lomba(10))
        baru, _ = K._cek_r3({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_ai_tidak_diizinkan_tidak_membuat_pesan(self):
        _tulis(self.data, "lomba.json", self._lomba(3, ai="dilarang"))
        baru, _ = K._cek_r3({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_idempotent(self):
        _tulis(self.data, "lomba.json", self._lomba(3))
        K._cek_r3({}, str(self.data))
        baru2, _ = K._cek_r3({}, str(self.data))
        self.assertEqual(len(baru2), 0)


class TestR4(Basis):
    def test_payout_dekat_membuat_pesan(self):
        _tulis(self.data, "keuangan_data.json",
               {"pengingat_payout": [{"platform": "Zazzle", "tanggal": _besok(3)}]})
        baru, _ = K._cek_r4({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["ke_agent"], "Muse")

    def test_tanpa_data_belum_cukup_data(self):
        _tulis(self.data, "keuangan_data.json", {})
        baru, lap = K._cek_r4({}, str(self.data))
        self.assertEqual(len(baru), 0)
        self.assertIn("BELUM CUKUP DATA", lap)

    def test_pemasukan_menunggu_membuat_pesan(self):
        _tulis(self.data, "keuangan_data.json",
               {"entries": [{"platform": "Zazzle", "produk": "Kaos",
                             "jumlah": 100000, "status": "menunggu"}]})
        baru, _ = K._cek_r4({}, str(self.data))
        self.assertEqual(len(baru), 1)

    def test_idempotent(self):
        _tulis(self.data, "keuangan_data.json",
               {"pengingat_payout": [{"platform": "Zazzle", "tanggal": _besok(3)}]})
        K._cek_r4({}, str(self.data))
        baru2, _ = K._cek_r4({}, str(self.data))
        self.assertEqual(len(baru2), 0)


class TestR5(Basis):
    def test_email_tinggi_diarahkan_per_kategori(self):
        _tulis(self.data, "log-pemeriksaan-email.json",
               [{"prioritas": "Tinggi", "kategori": "Lomba", "perihal": "Pemenang"}])
        baru, _ = K._cek_r5({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["ke_agent"], 6)

    def test_email_biasa_tidak_membuat_pesan(self):
        _tulis(self.data, "log-pemeriksaan-email.json",
               [{"prioritas": "Rendah", "kategori": "Lomba", "perihal": "Info"}])
        baru, _ = K._cek_r5({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_idempotent(self):
        _tulis(self.data, "log-pemeriksaan-email.json",
               [{"prioritas": "Tinggi", "kategori": "Keuangan", "perihal": "Payout"}])
        K._cek_r5({}, str(self.data))
        baru2, _ = K._cek_r5({}, str(self.data))
        self.assertEqual(len(baru2), 0)


class TestR6(Basis):
    def test_perlu_perbaikan_membuat_pesan(self):
        _tulis(self.data, "log-penjagaan-oyen.json",
               [{"verdict": "PERLU PERBAIKAN", "ringkasan": "Suara lari"}])
        baru, _ = K._cek_r6({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["ke_agent"], 5)

    def test_tanpa_verdict_tidak_membuat_pesan(self):
        _tulis(self.data, "log-penjagaan-oyen.json",
               [{"verdict": "LULUS", "ringkasan": "Bagus"}])
        baru, _ = K._cek_r6({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_idempotent(self):
        _tulis(self.data, "log-penjagaan-oyen.json",
               [{"verdict": "PERLU PERBAIKAN", "ringkasan": "Suara lari"}])
        K._cek_r6({}, str(self.data))
        baru2, _ = K._cek_r6({}, str(self.data))
        self.assertEqual(len(baru2), 0)


class TestR7(Basis):
    def test_proyek_selesai_membuat_dua_pesan(self):
        _tulis(self.data, "game_data.json",
               [{"nama": "G", "jenis": "game", "status": "selesai"}])
        baru, _ = K._cek_r7({}, str(self.data))
        self.assertEqual(len(baru), 2)
        self.assertEqual({b["ke_agent"] for b in baru}, {2, 7})

    def test_tanpa_data_belum_cukup_data(self):
        baru, lap = K._cek_r7({}, str(self.data))
        self.assertEqual(len(baru), 0)
        self.assertIn("BELUM CUKUP DATA", lap)

    def test_idempotent(self):
        _tulis(self.data, "game_data.json",
               [{"nama": "G", "jenis": "game", "status": "diterbitkan"}])
        K._cek_r7({}, str(self.data))
        baru2, _ = K._cek_r7({}, str(self.data))
        self.assertEqual(len(baru2), 0)


class TestR8(Basis):
    def test_terjemahan_selesai_membuat_pesan(self):
        _tulis(self.data, "terjemah_progress.json", {"Buku X": "selesai"})
        baru, _ = K._cek_r8({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["ke_agent"], 2)

    def test_tanpa_data_belum_cukup_data(self):
        baru, lap = K._cek_r8({}, str(self.data))
        self.assertEqual(len(baru), 0)
        self.assertIn("BELUM CUKUP DATA", lap)

    def test_idempotent(self):
        _tulis(self.data, "terjemah_progress.json", {"Buku X": "selesai"})
        K._cek_r8({}, str(self.data))
        baru2, _ = K._cek_r8({}, str(self.data))
        self.assertEqual(len(baru2), 0)


# ---------------------------------------------------------------------------
# Warisan: Siklus Harian + ringkasan
# ---------------------------------------------------------------------------
class TestSiklus(Basis):
    def _seed(self):
        _tulis(self.data, "riset.json", [{"niche": "N", "ide": "I", "skor": 10,
                                          "verdict": "Layak dicoba"}])
        (self.tmp / "output" / "draf.md").write_text("draf", encoding="utf-8")
        _tulis(self.data, "lomba.json", [{"nama": "L", "tenggat": _besok(3),
                                          "kebijakan_ai": "diizinkan", "status": "baru"}])
        _tulis(self.data, "keuangan_data.json", {})
        _tulis(self.data, "game_data.json",
               [{"nama": "G", "jenis": "game", "status": "selesai"}])
        _tulis(self.data, "terjemah_progress.json", {"Buku X": "selesai"})

    def test_siklus_end_to_end_dan_ringkasan_r9(self):
        self._seed()
        lap = K.jalankan_siklus_harian(data_dir=str(self.data))
        pesan = self._pesan()
        self.assertGreater(len(pesan), 0)
        self.assertTrue(any(p["sumber"] == "aturan-rute-R9" for p in pesan))
        self.assertIn("Total pesan baru:", lap)

    def test_siklus_kedua_idempotent(self):
        self._seed()
        K.jalankan_siklus_harian(data_dir=str(self.data))
        lap2 = K.jalankan_siklus_harian(data_dir=str(self.data))
        self.assertIn("Total pesan baru: 0", lap2)


class TestRingkasan(Basis):
    def test_ringkasan_status_menghitung(self):
        K.kirim_pesan(10, 5, "product-brief", "normal", "A", data_dir=str(self.data))
        K.kirim_pesan(10, 5, "product-brief", "normal", "B", data_dir=str(self.data))
        K.kirim_pesan(5, 2, "draft-approval", "normal", "C", data_dir=str(self.data))
        ring = K.ringkasan_status(data_dir=str(self.data))
        self.assertEqual(ring["5"]["total"], 2)
        self.assertEqual(ring["2"]["total"], 1)

    def test_inbox_menyaring_penerima(self):
        K.kirim_pesan(10, 5, "product-brief", "normal", "A", data_dir=str(self.data))
        K.kirim_pesan(5, 2, "draft-approval", "normal", "C", data_dir=str(self.data))
        self.assertEqual(len(K.inbox(5, data_dir=str(self.data))), 1)
        self.assertEqual(len(K.inbox(2, data_dir=str(self.data))), 1)

    def test_outbox_menyaring_pengirim(self):
        K.kirim_pesan(10, 5, "product-brief", "normal", "A", data_dir=str(self.data))
        K.kirim_pesan(10, 5, "product-brief", "normal", "B", data_dir=str(self.data))
        self.assertEqual(len(K.outbox(10, data_dir=str(self.data))), 2)
        self.assertEqual(len(K.outbox(5, data_dir=str(self.data))), 0)


# ---------------------------------------------------------------------------
# Baru: aturan rute R11–R13 (tim 9A/9B/9C)
# ---------------------------------------------------------------------------
class TestR11R12R13(Basis):
    def _pipa(self, entries):
        _tulis(self.data, "produksi_game.json", entries)

    def test_r11_spesifikasi_selesai_ke_9b(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai"}])
        baru, _ = K._cek_r11({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["dari_agent"], "9A")
        self.assertEqual(baru[0]["ke_agent"], "9B")

    def test_r11_tanpa_spesifikasi_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "antrean"}])
        baru, _ = K._cek_r11({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r11_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai"}])
        K._cek_r11({}, str(self.data))
        baru2, _ = K._cek_r11({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_r12_uji_lolos_ke_9c(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos"}])
        baru, _ = K._cek_r12({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["dari_agent"], "9B")
        self.assertEqual(baru[0]["ke_agent"], "9C")

    def test_r12_tanpa_uji_lolos_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai"}])
        baru, _ = K._cek_r12({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r12_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos"}])
        K._cek_r12({}, str(self.data))
        baru2, _ = K._cek_r12({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_r13_siap_jual_ke_penjualan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "siap-jual"}])
        baru, _ = K._cek_r13({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["dari_agent"], "9C")
        self.assertEqual(baru[0]["ke_agent"], 2)

    def test_r13_tanpa_siap_jual_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos"}])
        baru, _ = K._cek_r13({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r13_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "siap-jual"}])
        K._cek_r13({}, str(self.data))
        baru2, _ = K._cek_r13({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_aturan_r11_r16_terdaftar_dan_aktif(self):
        ids = {a["id"]: a for a in K.ATURAN_RUTE}
        for rid in ("R11", "R12", "R13", "R14", "R15", "R16"):
            self.assertIn(rid, ids)
            self.assertTrue(ids[rid]["aktif"])
        self.assertEqual(len(K.ATURAN_RUTE), 16)


# ---------------------------------------------------------------------------
# Baru: modul tim 9A/9B/9C (memakai data_dir sementara)
# ---------------------------------------------------------------------------
class BasisTim(unittest.TestCase):
    def setUp(self):
        import a09_pipa as pipa
        self.pipa = pipa
        self.tmp = Path(tempfile.mkdtemp())
        self._lama = pipa.DATA_FILE
        pipa.DATA_FILE = self.tmp / "produksi_game.json"

    def tearDown(self):
        self.pipa.DATA_FILE = self._lama


class TestTim9A(BasisTim):
    def test_seed_17_proyek(self):
        data = self.pipa.muat_data()
        self.assertEqual(len(data), 17)
        ringkas = self.pipa.ringkasan_status(data)
        self.assertEqual(ringkas["di-toko"], 4)
        self.assertEqual(ringkas["siap-jual"], 1)
        self.assertEqual(ringkas["antrean"], 12)

    def test_buat_spesifikasi_antrean_ke_selesai(self):
        import a09a_rancang as r
        msg, draf, _ = r.buat_spesifikasi(
            "Arsip Dokumen", "Perusahaan kecil",
            "Simpan dokumen\nCari + filter", "20 dokumen contoh",
            "Semua tombol berfungsi\nRapi di HP",
            "1. Buka tab Arsip.\n2. Cari dokumen dengan kotak pencarian.")
        self.assertIn("spesifikasi-selesai", msg)
        self.assertIn("Arsip Dokumen", draf)
        self.assertIn("Buku Panduan", draf)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "spesifikasi-selesai")
        self.assertEqual(len(proyek["spesifikasi"]["fitur"]), 2)
        self.assertIn("Buka tab Arsip", proyek["spesifikasi"]["panduan"])

    def test_buat_spesifikasi_tanpa_panduan_ditolak(self):
        import a09a_rancang as r
        msg, _, _ = r.buat_spesifikasi(
            "Arsip Dokumen", "Perusahaan kecil",
            "Simpan dokumen", "20 dokumen contoh",
            "Semua tombol berfungsi", "")
        self.assertIn("panduan", msg.lower())
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "antrean")

    def test_buat_spesifikasi_proyek_tidak_ada_ditolak(self):
        import a09a_rancang as r
        msg, _, _ = r.buat_spesifikasi("Tidak Ada", "X", "F", "D", "K", "P")
        self.assertIn("tidak ditemukan", msg)

    def test_buat_spesifikasi_status_lewat_ditolak(self):
        import a09a_rancang as r
        msg, _, _ = r.buat_spesifikasi("Kasir Toko", "X", "F", "D", "K", "P")
        self.assertIn("sudah lewat tahap rancang", msg)

    def test_tambah_proyek_duplikat_ditolak(self):
        import a09a_rancang as r
        msg, _ = r.tambah_proyek("Arsip Dokumen", "aplikasi", "")
        self.assertIn("sudah ada", msg)


class TestTim9B(BasisTim):
    def _ke_spesifikasi(self):
        import a09a_rancang as r
        r.buat_spesifikasi("Arsip Dokumen", "Perusahaan kecil",
                           "Simpan dokumen", "20 dokumen",
                           "Semua tombol berfungsi",
                           "1. Buka tab Arsip.")

    def test_uji_gagal_tetap_dan_mencatat_perbaikan(self):
        import a09b_bangun as b
        self._ke_spesifikasi()
        msg, hasil, _ = b.uji_proyek("Arsip Dokumen", True, True, True, False,
                                     True, "Tabel meluber di HP")
        self.assertIn("BELUM LOLOS", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "spesifikasi-selesai")
        self.assertFalse(proyek["hasil_uji"]["lolos"])
        self.assertIn("Tabel meluber", proyek["hasil_uji"]["catatan_perbaikan"])

    def test_uji_gagal_bila_panduan_tidak_lengkap(self):
        import a09b_bangun as b
        self._ke_spesifikasi()
        msg, hasil, _ = b.uji_proyek("Arsip Dokumen", True, True, True, True,
                                     False, "")
        self.assertIn("BELUM LOLOS", msg)
        self.assertIn("panduan", hasil.lower())
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "spesifikasi-selesai")
        self.assertFalse(proyek["hasil_uji"]["lolos"])

    def test_uji_lolos_ke_diuji_lolos(self):
        import a09b_bangun as b
        self._ke_spesifikasi()
        msg, hasil, _ = b.uji_proyek("Arsip Dokumen", True, True, True, True,
                                     True, "")
        self.assertIn("LOLOS UJI", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "diuji-lolos")
        self.assertTrue(proyek["hasil_uji"]["lolos"])

    def test_uji_proyek_antrean_ditolak(self):
        import a09b_bangun as b
        msg, _, _ = b.uji_proyek("Arsip Dokumen", True, True, True, True,
                                 True, "")
        self.assertIn("belum bisa diuji", msg)


class TestTim9C(BasisTim):
    def _ke_diuji(self):
        import a09a_rancang as r, a09b_bangun as b
        r.buat_spesifikasi("Arsip Dokumen", "Perusahaan kecil",
                           "Simpan dokumen", "20 dokumen",
                           "Semua tombol berfungsi",
                           "1. Buka tab Arsip.")
        b.uji_proyek("Arsip Dokumen", True, True, True, True, True, "")

    def test_buat_listing_ke_siap_jual(self):
        import a09c_jualan as j
        self._ke_diuji()
        msg, draf, _ = j.buat_listing("Arsip Dokumen", "Arsip dokumen perusahaan kecil.",
                                      "Simpan + cari dokumen", "", "")
        self.assertIn("siap-jual", msg)
        self.assertIn("bisa negosiasi", draf)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "siap-jual")

    def test_buat_listing_proyek_antrean_ditolak(self):
        import a09c_jualan as j
        msg, _, _ = j.buat_listing("Arsip Dokumen", "D", "F", "", "")
        self.assertIn("belum bisa dibuatkan listing", msg)

    def test_draf_penawaran_memakai_listing(self):
        import a09c_jualan as j
        self._ke_diuji()
        j.buat_listing("Arsip Dokumen", "Arsip dokumen perusahaan kecil.",
                       "Simpan + cari dokumen", "bisa negosiasi", "")
        draf = j.draf_penawaran("Arsip Dokumen", "toko kelontong")
        self.assertIn("DRAF", draf)
        self.assertIn("toko kelontong", draf)
        self.assertIn("bisa negosiasi", draf)

    def test_tandai_di_toko(self):
        import a09c_jualan as j
        self._ke_diuji()
        j.buat_listing("Arsip Dokumen", "D", "F", "", "")
        msg, _ = j.tandai_di_toko("Arsip Dokumen")
        self.assertIn("di-toko", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "di-toko")


# ---------------------------------------------------------------------------
# Baru: pendaftaran di Pusat Komando + template handoff
# ---------------------------------------------------------------------------
class TestPendaftaranWadah(unittest.TestCase):
    def test_modul_tim_bisa_diimpor(self):
        import a09a_rancang, a09b_bangun, a09c_jualan, a09_pipa
        import a09d_bangun2, a09e_bangun3, a09f_verifikasi_katalog
        for m in (a09a_rancang, a09b_bangun, a09c_jualan,
                  a09d_bangun2, a09e_bangun3, a09f_verifikasi_katalog):
            self.assertTrue(callable(m.bangun_ui))
        self.assertEqual(len(a09_pipa.STATUS_ALUR), 5)
        self.assertEqual(a09_pipa.TIM_BANGUN, ["9B", "9D", "9E"])
        self.assertEqual(len(a09_pipa.CHECKLIST_UJI), 5)
        self.assertEqual(len(a09f_verifikasi_katalog.CHECKLIST), 7)

    def test_nama_agent_memuat_tim_9a_sampai_9f(self):
        import app
        for kunci in ("9A", "9B", "9C", "9D", "9E", "9F"):
            self.assertIn(kunci, app.NAMA_AGENT)
        self.assertIn("9A", app._URUTAN_AGENT)
        self.assertEqual(app._URUTAN_AGENT.index("9A"),
                         app._URUTAN_AGENT.index(9) + 1)
        self.assertEqual(app._URUTAN_AGENT.index("9D"),
                         app._URUTAN_AGENT.index("9C") + 1)
        self.assertEqual(app._URUTAN_AGENT.index("9F"),
                         app._URUTAN_AGENT.index(10) - 1)
        self.assertIn("game-pipeline", app.JENIS_HANDOFF)

    def test_modul_tim_termuat_di_app(self):
        import app
        self.assertIsNotNone(app.A09A)
        self.assertIsNotNone(app.A09B)
        self.assertIsNotNone(app.A09C)
        self.assertIsNotNone(app.A09D)
        self.assertIsNotNone(app.A09E)
        self.assertIsNotNone(app.A09F)
        self.assertIsNone(app.E09A)
        self.assertIsNone(app.E09B)
        self.assertIsNone(app.E09C)
        self.assertIsNone(app.E09D)
        self.assertIsNone(app.E09E)
        self.assertIsNone(app.E09F)

    def test_build_app_memuat_enam_tab_tim(self):
        import json as _json
        import app
        demo = app.build_app()
        teks = _json.dumps(demo.config, ensure_ascii=False, default=str)
        for label in ("9A · Rancang", "9B · Bangun", "9C · Jualan",
                      "9D · Bangun-2", "9E · Bangun-3",
                      "9F · Verifikasi & Katalog"):
            self.assertIn(label, teks)

    def test_template_game_pipeline_valid(self):
        path = ROOT / "data" / "handoff-templates" / "game-pipeline.json"
        tpl = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(tpl["jenis"], "game-pipeline")
        self.assertEqual(tpl["status"], "draf")
        for kunci in ("nama_proyek", "tahap", "spesifikasi", "hasil_uji", "listing"):
            self.assertIn(kunci, tpl["isi"])


# ---------------------------------------------------------------------------
# Baru: aturan rute R14–R16 (tim 9D/9E/9F)
# ---------------------------------------------------------------------------
class TestR14R15R16(Basis):
    def _pipa(self, entries):
        _tulis(self.data, "produksi_game.json", entries)

    def test_r14_spesifikasi_bebas_ke_9d_9e(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai", "klaim": None}])
        baru, _ = K._cek_r14({}, str(self.data))
        self.assertEqual(len(baru), 2)
        self.assertEqual({b["ke_agent"] for b in baru}, {"9D", "9E"})
        self.assertTrue(all(b["dari_agent"] == "9B" for b in baru))

    def test_r14_sudah_diklaim_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai",
                     "klaim": {"oleh": "9D", "tanggal": "2026-11-19"}}])
        baru, _ = K._cek_r14({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r14_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "spesifikasi-selesai", "klaim": None}])
        K._cek_r14({}, str(self.data))
        baru2, _ = K._cek_r14({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_r15_uji_9d_ke_9f(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "hasil_uji": {"diuji_oleh": "9D", "lolos": True},
                     "verifikasi_9f": None}])
        baru, _ = K._cek_r15({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["dari_agent"], "9D")
        self.assertEqual(baru[0]["ke_agent"], "9F")

    def test_r15_uji_9b_tidak_ke_9f(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "hasil_uji": {"diuji_oleh": "9B", "lolos": True},
                     "verifikasi_9f": None}])
        baru, _ = K._cek_r15({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r15_sudah_diverifikasi_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "hasil_uji": {"diuji_oleh": "9E", "lolos": True},
                     "verifikasi_9f": {"tanggal": "2026-11-19", "lolos": True}}])
        baru, _ = K._cek_r15({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r15_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "hasil_uji": {"diuji_oleh": "9D", "lolos": True},
                     "verifikasi_9f": None}])
        K._cek_r15({}, str(self.data))
        baru2, _ = K._cek_r15({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_r16_verifikasi_lolos_ke_9c(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "verifikasi_9f": {"tanggal": "2026-11-19", "lolos": True}}])
        baru, _ = K._cek_r16({}, str(self.data))
        self.assertEqual(len(baru), 1)
        self.assertEqual(baru[0]["dari_agent"], "9F")
        self.assertEqual(baru[0]["ke_agent"], "9C")

    def test_r16_verifikasi_gagal_tidak_membuat_pesan(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "verifikasi_9f": {"tanggal": "2026-11-19", "lolos": False}}])
        baru, _ = K._cek_r16({}, str(self.data))
        self.assertEqual(len(baru), 0)

    def test_r16_idempotent(self):
        self._pipa([{"nama": "Arsip Dokumen", "jenis": "aplikasi",
                     "status": "diuji-lolos",
                     "verifikasi_9f": {"tanggal": "2026-11-19", "lolos": True}}])
        K._cek_r16({}, str(self.data))
        baru2, _ = K._cek_r16({}, str(self.data))
        self.assertEqual(len(baru2), 0)

    def test_aturan_r14_r16_terdaftar_dan_aktif(self):
        ids = {a["id"]: a for a in K.ATURAN_RUTE}
        for rid in ("R14", "R15", "R16"):
            self.assertIn(rid, ids)
            self.assertTrue(ids[rid]["aktif"])
        self.assertEqual(len(K.ATURAN_RUTE), 16)


# ---------------------------------------------------------------------------
# Baru: klaim/kunci anti double-build (9B/9D/9E)
# ---------------------------------------------------------------------------
class TestKlaim(BasisTim):
    def _ke_spesifikasi(self, nama="Arsip Dokumen"):
        import a09a_rancang as r
        r.buat_spesifikasi(nama, "Perusahaan kecil",
                           "Simpan dokumen", "20 dokumen",
                           "Semua tombol berfungsi",
                           "1. Buka tab Arsip.")

    def test_klaim_9d_lalu_9e_ditolak(self):
        import a09_pipa as pipa
        self._ke_spesifikasi()
        msg, _ = pipa.klaim("Arsip Dokumen", "9D")
        self.assertIn("diklaim tim 9D", msg)
        msg2, _ = pipa.klaim("Arsip Dokumen", "9E")
        self.assertIn("sedang dikerjakan tim 9D", msg2)
        self.assertEqual(len(pipa.daftar_klaim()), 1)

    def test_klaim_dua_proyek_beda_tim_boleh(self):
        import a09_pipa as pipa
        self._ke_spesifikasi("Arsip Dokumen")
        self._ke_spesifikasi("Aset Perusahaan")
        pipa.klaim("Arsip Dokumen", "9D")
        msg, _ = pipa.klaim("Aset Perusahaan", "9E")
        self.assertIn("diklaim tim 9E", msg)
        self.assertEqual(len(pipa.daftar_klaim()), 2)

    def test_lepas_klaim_hanya_pemilik(self):
        import a09_pipa as pipa
        self._ke_spesifikasi()
        pipa.klaim("Arsip Dokumen", "9D")
        msg, _ = pipa.lepas("Arsip Dokumen", "9E")
        self.assertIn("hanya tim itu", msg)
        self.assertEqual(len(pipa.daftar_klaim()), 1)
        msg2, _ = pipa.lepas("Arsip Dokumen", "9D")
        self.assertIn("dilepas", msg2)
        self.assertEqual(len(pipa.daftar_klaim()), 0)

    def test_uji_tim_lain_ditolak_saat_diklaim(self):
        import a09d_bangun2 as d, a09e_bangun3 as e
        self._ke_spesifikasi()
        d.klaim_proyek("Arsip Dokumen")
        msg, _, _ = e.uji_proyek("Arsip Dokumen", True, True, True, True,
                                 True, "")
        self.assertIn("sedang dikerjakan tim 9D", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "spesifikasi-selesai")

    def test_uji_otomatis_mengklaim_bila_bebas_dan_melepas_setelahnya(self):
        import a09e_bangun3 as e
        self._ke_spesifikasi()
        msg, _, _ = e.uji_proyek("Arsip Dokumen", True, True, True, True,
                                 True, "")
        self.assertIn("LOLOS UJI", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["hasil_uji"]["diuji_oleh"], "9E")
        self.assertEqual(len(self.pipa.daftar_klaim()), 0)

    def test_klaim_status_bukan_spesifikasi_ditolak(self):
        import a09_pipa as pipa
        msg, _ = pipa.klaim("Kasir Toko", "9D")
        self.assertIn("belum bisa diklaim", msg)

    def test_klaim_tim_bukan_bangun_ditolak(self):
        import a09_pipa as pipa
        self._ke_spesifikasi()
        msg, _ = pipa.klaim("Arsip Dokumen", "9A")
        self.assertIn("bukan tim bangun", msg)

    def test_daftar_siap_bangun_hanya_yang_bebas(self):
        import a09_pipa as pipa
        self._ke_spesifikasi("Arsip Dokumen")
        self._ke_spesifikasi("Aset Perusahaan")
        pipa.klaim("Arsip Dokumen", "9D")
        self.assertEqual(pipa.daftar_siap_bangun(), ["Aset Perusahaan"])


# ---------------------------------------------------------------------------
# Baru: modul tim 9D/9E (builder paralel)
# ---------------------------------------------------------------------------
class TestTim9D9E(BasisTim):
    def _ke_spesifikasi(self):
        import a09a_rancang as r
        r.buat_spesifikasi("Arsip Dokumen", "Perusahaan kecil",
                           "Simpan dokumen", "20 dokumen",
                           "Semua tombol berfungsi",
                           "1. Buka tab Arsip.")

    def test_9d_uji_lolos_mencatat_diuji_oleh(self):
        import a09d_bangun2 as d
        self._ke_spesifikasi()
        msg, hasil, _ = d.uji_proyek("Arsip Dokumen", True, True, True, True,
                                     True, "")
        self.assertIn("LOLOS UJI", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["hasil_uji"]["diuji_oleh"], "9D")
        self.assertEqual(proyek["status"], "diuji-lolos")

    def test_9e_uji_gagal_bila_panduan_tidak_lengkap(self):
        import a09e_bangun3 as e
        self._ke_spesifikasi()
        msg, hasil, _ = e.uji_proyek("Arsip Dokumen", True, True, True, True,
                                     False, "")
        self.assertIn("BELUM LOLOS", msg)
        self.assertIn("panduan", hasil.lower())
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertEqual(proyek["status"], "spesifikasi-selesai")
        self.assertFalse(proyek["hasil_uji"]["lolos"])

    def test_9d_dan_9e_pakai_checklist_yang_sama_dengan_9b(self):
        import a09b_bangun as b, a09d_bangun2 as d, a09e_bangun3 as e
        self.assertEqual(d.CHECKLIST, b.CHECKLIST)
        self.assertEqual(e.CHECKLIST, b.CHECKLIST)
        self.assertEqual(len(d.CHECKLIST), 5)


# ---------------------------------------------------------------------------
# Baru: modul tim 9F (verifikasi QC + katalog + batch unggah)
# ---------------------------------------------------------------------------
MINI_KATALOG = """# Katalog Lengkap Produk

- **Status hanya ada 4 macam:** `Sudah jadi` (1 aplikasi), `Sedang dibangun` (tidak ada), `Di antrean Agent 9` (1 aplikasi, dengan nomor urut antrean), dan `Kandidat` (belum dibangun, belum masuk antrean).

## Ringkasan Jumlah Produk per Kategori

| Kategori | Jumlah | Sudah jadi | Sedang dibangun | Di antrean | Kandidat |
|---|---:|---:|---:|---:|---:|
| 10. Jasa & Bisnis | 2 | 0 | 0 | 1 | 1 |
| **Subtotal aplikasi** | **2** | **0** | **0** | **1** | **1** |

**Antrean Agent 9 (1 aplikasi, urutan resmi):** 1 Arsip Dokumen

### Kategori 10 — Jasa & Bisnis (2)

#### 10.1 Arsip Dokumen

- **Target pengguna:** Perusahaan kecil.
- **Fitur utama:** Simpan dokumen.
- **Harga:** Beli Sekali — Pemula Rp499.000 / Profesional Rp999.000 / Bisnis Rp1.999.000.
- **Status:** Di antrean Agent 9 — menunggu giliran di antrean Agent 9.

#### 10.2 Aset Perusahaan

- **Target pengguna:** Perusahaan kecil.
- **Fitur utama:** Catat aset.
- **Harga:** Beli Sekali — Pemula Rp499.000 / Profesional Rp999.000 / Bisnis Rp1.999.000.
- **Status:** Kandidat — belum dibangun, belum masuk antrean.
"""

MINI_KAT_JASA = """# Katalog — Jasa & Bisnis

#### 10.1 Arsip Dokumen

- **Target pengguna:** Perusahaan kecil.
- **Fitur utama:** Simpan dokumen.
- **Harga:** Beli Sekali — Pemula Rp499.000 / Profesional Rp999.000 / Bisnis Rp1.999.000.
- **Status:** Di antrean Agent 9 — menunggu giliran di antrean Agent 9.

#### 10.2 Aset Perusahaan

- **Target pengguna:** Perusahaan kecil.
- **Fitur utama:** Catat aset.
- **Harga:** Beli Sekali — Pemula Rp499.000 / Profesional Rp999.000 / Bisnis Rp1.999.000.
- **Status:** Kandidat — belum dibangun, belum masuk antrean.
"""


class BasisTim9F(BasisTim):
    def setUp(self):
        super().setUp()
        import a09f_verifikasi_katalog as f
        self.f = f
        self.tmpk = Path(tempfile.mkdtemp())
        self._kat_lama = (f.KATALOG_GABUNGAN, f.KATALOG_DIR,
                          f.LOG_KATALOG, f.BATCH_FILE)
        f.KATALOG_GABUNGAN = self.tmpk / "katalog-lengkap-aplikasi.md"
        f.KATALOG_DIR = self.tmpk / "katalog-per-kategori"
        f.KATALOG_DIR.mkdir()
        f.LOG_KATALOG = self.tmpk / "log_katalog.json"
        f.BATCH_FILE = self.tmpk / "batch_unggah.json"
        (self.tmpk / "katalog-lengkap-aplikasi.md").write_text(
            MINI_KATALOG, encoding="utf-8")
        (f.KATALOG_DIR / "jasa-bisnis.md").write_text(
            MINI_KAT_JASA, encoding="utf-8")

    def tearDown(self):
        f = self.f
        f.KATALOG_GABUNGAN, f.KATALOG_DIR, f.LOG_KATALOG, f.BATCH_FILE = \
            self._kat_lama
        super().tearDown()


class TestTim9F(BasisTim9F):
    def _ke_diuji(self, tim="9D", nama="Arsip Dokumen"):
        import a09a_rancang as r
        r.buat_spesifikasi(nama, "Perusahaan kecil",
                           "Simpan dokumen", "20 dokumen",
                           "Semua tombol berfungsi",
                           "1. Buka tab Arsip.")
        import importlib
        mod = {"9D": "a09d_bangun2", "9E": "a09e_bangun3",
               "9B": "a09b_bangun"}[tim]
        b = importlib.import_module(mod)
        b.uji_proyek(nama, True, True, True, True, True, "")

    def _ke_di_toko(self, nama="Arsip Dokumen"):
        import a09c_jualan as j
        self._ke_diuji("9D", nama)
        self.f.verifikasi_proyek(nama, True, True, True, True, True,
                                 True, True, "")
        j.buat_listing(nama, "Arsip dokumen perusahaan kecil.",
                       "Simpan + cari dokumen", "",
                       "https://podcastmeong.github.io/arsip-dokumen/")
        j.tandai_di_toko(nama)

    def test_verifikasi_lolos_mencatat_9f(self):
        self._ke_diuji("9D")
        msg, hasil, _ = self.f.verifikasi_proyek(
            "Arsip Dokumen", True, True, True, True, True, True, True, "")
        self.assertIn("LOLOS VERIFIKASI 9F", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertTrue(proyek["terverifikasi_9f"])
        self.assertEqual(proyek["verifikasi_9f"]["diverifikasi_oleh"], "9F")
        self.assertEqual(proyek["status"], "diuji-lolos")

    def test_verifikasi_gagal_demo_tetap_diuji_lolos(self):
        self._ke_diuji("9E")
        msg, hasil, _ = self.f.verifikasi_proyek(
            "Arsip Dokumen", True, True, True, True, True, False, True,
            "Demo tidak terbuka")
        self.assertIn("BELUM LOLOS VERIFIKASI 9F", msg)
        proyek = self.pipa.cari(self.pipa.muat_data(), "Arsip Dokumen")
        self.assertFalse(proyek["terverifikasi_9f"])
        self.assertEqual(proyek["status"], "diuji-lolos")

    def test_verifikasi_proyek_antrean_ditolak(self):
        msg, _, _ = self.f.verifikasi_proyek(
            "Arsip Dokumen", True, True, True, True, True, True, True, "")
        self.assertIn("belum bisa diverifikasi 9F", msg)

    def test_perbarui_katalog_status_tabel_dan_antrean(self):
        self._ke_di_toko()
        msg, _ = self.f.perbarui_katalog(
            "Arsip Dokumen", "di-toko",
            "https://podcastmeong.github.io/arsip-dokumen/")
        self.assertIn("Sudah jadi", msg)
        gab = (self.tmpk / "katalog-lengkap-aplikasi.md").read_text(
            encoding="utf-8")
        self.assertIn("- **Status:** Sudah jadi —", gab)
        self.assertIn("Demo: https://podcastmeong.github.io/arsip-dokumen/",
                      gab)
        self.assertIn("| 10. Jasa & Bisnis | 2 | 1 | 0 | 0 | 1 |", gab)
        self.assertIn("| **Subtotal aplikasi** | **2** | **1** | **0** | **0** | **1** |",
                      gab)
        self.assertIn("`Sudah jadi` (5 aplikasi)", gab)
        self.assertIn("**Antrean Agent 9 (11 aplikasi, urutan resmi):** 1 Aset Perusahaan,",
                      gab)
        self.assertNotIn("1 Arsip Dokumen,", gab.split("urutan resmi):**")[1].split("\n")[0])
        per = (self.f.KATALOG_DIR / "jasa-bisnis.md").read_text(encoding="utf-8")
        self.assertIn("- **Status:** Sudah jadi —", per)

    def test_perbarui_katalog_proyek_tidak_ada(self):
        msg, _ = self.f.perbarui_katalog("Tidak Ada", "di-toko")
        self.assertIn("tidak ditemukan", msg)

    def test_perbarui_katalog_status_tidak_dikenal(self):
        msg, _ = self.f.perbarui_katalog("Arsip Dokumen", "aneh")
        self.assertIn("tidak dikenal", msg)

    def test_buat_batch_dari_siap_jual(self):
        import a09c_jualan as j
        self._ke_diuji("9D", "Arsip Dokumen")
        j.buat_listing("Arsip Dokumen", "D", "F", "",
                       "https://podcastmeong.github.io/arsip-dokumen/")
        self._ke_diuji("9E", "Aset Perusahaan")
        j.buat_listing("Aset Perusahaan", "D", "F", "",
                       "https://podcastmeong.github.io/aset-perusahaan/")
        msg, _ = self.f.buat_batch(10)
        self.assertIn("UB-001", msg)
        self.assertIn("Arsip Dokumen", msg)
        self.assertIn("Aset Perusahaan", msg)
        msg2, _ = self.f.buat_batch(10)
        self.assertIn("Tidak ada demo selesai", msg2)

    def test_tandai_diunggah(self):
        import a09c_jualan as j
        self._ke_diuji("9D", "Arsip Dokumen")
        j.buat_listing("Arsip Dokumen", "D", "F", "",
                       "https://podcastmeong.github.io/arsip-dokumen/")
        self.f.buat_batch(10)
        msg, _ = self.f.tandai_diunggah("UB-001")
        self.assertIn("sudah diunggah", msg)
        msg2, _ = self.f.tandai_diunggah("UB-001")
        self.assertIn("sudah berstatus", msg2)
        msg3, _ = self.f.tandai_diunggah("UB-999")
        self.assertIn("tidak ditemukan", msg3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
