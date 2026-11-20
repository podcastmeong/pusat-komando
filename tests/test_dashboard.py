# ======================================================================
# Unit test Dashboard Pergerakan Agent (agents/dashboard.py).
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH="$PATH" HOME="$HOME" ~/workspace/tmp/venv-pk/bin/python \
#     -m unittest discover -s tests -v
# Tes tulis hanya memakai folder sementara; tes baca memakai data nyata
# (read-only) untuk memastikan angka dashboard sesuai file yang ada.
# ======================================================================
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT))

import dashboard  # noqa: E402


def _tulis(folder, nama, data):
    with open(Path(folder) / nama, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class TestLogActivity(unittest.TestCase):
    def setUp(self):
        self._pk_no_log = os.environ.pop("PK_NO_LOG", None)
        self.tmp = tempfile.mkdtemp(prefix="pk-dash-")

    def tearDown(self):
        if self._pk_no_log is not None:
            os.environ["PK_NO_LOG"] = self._pk_no_log
        else:
            os.environ.pop("PK_NO_LOG", None)

    def test_log_ditulis_dan_dibaca_terbaru_dulu(self):
        self.assertTrue(dashboard.log_activity("A01", "uji aksi 1", "hasil 1",
                                               base=self.tmp))
        self.assertTrue(dashboard.log_activity("A02", "uji aksi 2", "hasil 2",
                                               base=self.tmp))
        log = dashboard.baca_log(base=self.tmp)
        self.assertEqual(len(log), 2)
        self.assertEqual(log[0]["kode_agent"], "A02")
        self.assertEqual(log[0]["aksi"], "uji aksi 2")
        self.assertEqual(log[1]["kode_agent"], "A01")
        self.assertIn("waktu", log[0])

    def test_log_dibatasi_500(self):
        for i in range(505):
            dashboard.log_activity("A01", "aksi %d" % i, "hasil", base=self.tmp)
        with open(Path(self.tmp) / "activity_log.json", encoding="utf-8") as f:
            tersimpan = json.load(f)
        self.assertEqual(len(tersimpan), 500)
        self.assertEqual(tersimpan[0]["aksi"], "aksi 5")
        self.assertEqual(tersimpan[-1]["aksi"], "aksi 504")

    def test_pk_no_log_menekan_penulisan(self):
        os.environ["PK_NO_LOG"] = "1"
        self.assertFalse(dashboard.log_activity("A01", "x", "y", base=self.tmp))
        self.assertFalse((Path(self.tmp) / "activity_log.json").exists())

    def test_log_gagal_diam_tanpa_exception(self):
        # base menunjuk ke sebuah FILE (bukan folder) — mkdir gagal.
        berkas = Path(self.tmp) / "bukan-folder"
        berkas.write_text("x", encoding="utf-8")
        self.assertFalse(dashboard.log_activity("A01", "x", "y", base=berkas))
        self.assertEqual(dashboard.baca_log(base=berkas), [])

    def test_baca_log_kosong_bila_tidak_ada_file(self):
        self.assertEqual(dashboard.baca_log(base=self.tmp), [])

    def test_wiring_log_di_modul_b(self):
        # Pemeriksaan statis (tanpa efek samping): modul b memanggil
        # log_activity di _draf_dasar.
        for nama in ("b01_ceo_director.py", "b15_pod_designer.py",
                     "b30_operations_manager.py"):
            sumber = (AGENTS / nama).read_text(encoding="utf-8")
            self.assertIn("from dashboard import log_activity", sumber, nama)
            self.assertIn('log_activity(KODE, "buat draf: " + jenis, judul)',
                          sumber, nama)


class TestTabelFixture(unittest.TestCase):
    def setUp(self):
        self._pk_no_log = os.environ.pop("PK_NO_LOG", None)
        self.tmp = tempfile.mkdtemp(prefix="pk-dash-")
        _tulis(self.tmp, "agents.json", {"agent_30": {"agents": [
            {"code": "A01", "name": "CEO Director", "division": "Direksi",
             "boss": "Pemilik", "job_desc": "j", "mapped_to": "Muse",
             "status": "Aktif"},
            {"code": "A02", "name": "COO Manager", "division": "Direksi",
             "boss": "A01", "job_desc": "j", "mapped_to": "Muse",
             "status": "Aktif sebagian"}]}})
        _tulis(self.tmp, "handoff.json", [
            {"id": "HO-001", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 1", "ringkasan": "Tugas uji", "status": "draf"}])

    def tearDown(self):
        if self._pk_no_log is not None:
            os.environ["PK_NO_LOG"] = self._pk_no_log
        else:
            os.environ.pop("PK_NO_LOG", None)

    def test_tabel_16_baris_dan_handoff_agent1(self):
        rows = dashboard.tabel_semua_agent(base=self.tmp)
        self.assertEqual(len(rows), 2 + 14)
        a01 = next(r for r in rows if r["kode"] == "A01")
        self.assertEqual(a01["aktivitas_terakhir"], "belum ada aktivitas")
        agent1 = next(r for r in rows if r["kode"] == "1")
        self.assertIn("HO-001", agent1["aktivitas_terakhir"])
        self.assertIn("Tugas uji", agent1["output_terakhir"])

    def test_ringkasan_matematika_fixture(self):
        # A01 Aktif tanpa aktivitas -> belum jalan; A02 Aktif sebagian;
        # Agent 1 (handoff) + Agent 7 (baseline keuangan tercatat) -> aktif;
        # Agent 14 -> mode persiapan; sisanya belum jalan.
        r = dashboard.ringkasan_dashboard(base=self.tmp)
        self.assertEqual(r["total_agent"], 16)
        self.assertEqual(r["aktif"], 2)
        self.assertEqual(r["aktif_sebagian"], 1)
        self.assertEqual(r["belum_jalan"], 12)
        self.assertEqual(r["mode_persiapan"], 1)
        self.assertEqual(r["handoff_menunggu"], 1)

    def test_tugas_menunggu_jujur_tanpa_tanggal(self):
        t = dashboard.tugas_menunggu(base=self.tmp)
        self.assertEqual(len(t["handoff"]), 1)
        self.assertIn("tidak mencatat tanggal", t["catatan"])
        self.assertEqual(dashboard.persetujuan_menunggu(base=self.tmp),
                         t["handoff"])


class TestDataNyata(unittest.TestCase):
    """Baca data nyata (read-only): angka dashboard harus cocok dengan file."""

    def test_tabel_44_baris(self):
        rows = dashboard.tabel_semua_agent()
        self.assertEqual(len(rows), 44)
        kode = {r["kode"] for r in rows}
        self.assertEqual(kode, {"A%02d" % i for i in range(1, 31)}
                         | {str(i) for i in range(1, 15)})

    def test_nilai_aktivitas_agent_lama(self):
        rows = {r["kode"]: r for r in dashboard.tabel_semua_agent()}
        self.assertIn("2 penawaran terkirim, 12 draf",
                      rows["4"]["aktivitas_terakhir"])
        self.assertIn("28 lomba tercatat", rows["6"]["aktivitas_terakhir"])
        self.assertIn("3 dikirim", rows["6"]["aktivitas_terakhir"])
        self.assertIn("baseline Rp0", rows["7"]["aktivitas_terakhir"])
        self.assertIn("56/61 demo selesai", rows["9"]["aktivitas_terakhir"])
        self.assertEqual(rows["10"]["aktivitas_terakhir"],
                         "belum ada aktivitas")
        self.assertIn("2026-11-18 23:56", rows["13"]["aktivitas_terakhir"])
        self.assertIn("mode persiapan", rows["14"]["status"])
        self.assertIn("Belum ada lamaran", rows["14"]["aktivitas_terakhir"])
        self.assertIn("15 lead tercatat", rows["2"]["aktivitas_terakhir"])

    def test_ringkasan_data_nyata(self):
        r = dashboard.ringkasan_dashboard()
        self.assertEqual(r["total_agent"], 44)
        self.assertEqual(r["handoff_menunggu"], 11)
        self.assertEqual(r["penawaran_toko_draf"], 12)
        self.assertEqual(r["aktif_sebagian"], 4)
        self.assertEqual(r["mode_persiapan"], 1)
        self.assertGreaterEqual(r["entri_log"], 3)
        self.assertEqual(r["aktif"] + r["aktif_sebagian"] + r["belum_jalan"]
                         + r["mode_persiapan"], 44)

    def test_feed_memuat_entri_seed(self):
        log = dashboard.baca_log(limit=50)
        self.assertGreaterEqual(len(log), 3)
        aksi = [e["aksi"] for e in log]
        self.assertIn("30 modul dibuat", aksi)
        self.assertIn("agents.json digabung", aksi)


if __name__ == "__main__":
    unittest.main()
