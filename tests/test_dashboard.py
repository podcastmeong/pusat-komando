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
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
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
        # 14 mesin lama: status pasif non-job, aktivitas tetap dihitung.
        self.assertEqual(agent1["status"], dashboard.STATUS_PASIF)
        self.assertIn("HO-001", agent1["aktivitas_terakhir"])
        self.assertIn("Tugas uji", agent1["output_terakhir"])

    def test_ringkasan_matematika_fixture(self):
        # Hitungan utama hanya 30 Bintang (di fixture cuma 2): A01 Aktif
        # tanpa aktivitas -> belum jalan; A02 Aktif sebagian. 14 mesin lama
        # dihitung terpisah sebagai mesin_pasif, bukan sebagai agent.
        r = dashboard.ringkasan_dashboard(base=self.tmp)
        self.assertEqual(r["total_agent"], 2)
        self.assertEqual(r["aktif"], 0)
        self.assertEqual(r["aktif_sebagian"], 1)
        self.assertEqual(r["belum_jalan"], 1)
        self.assertEqual(r["mesin_pasif"], 14)
        self.assertEqual(r["terkendala"], 0)
        self.assertEqual(r["handoff_menunggu"], 1)
        self.assertNotIn("mode_persiapan", r)

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
        # 21 Nov 2026: draf 12 -> 9 (Balini menunggu persetujuan,
        # Zoom + Efxi dilewati — lihat data/penjualan_toko.json).
        self.assertIn("2 penawaran terkirim, 9 draf",
                      rows["4"]["aktivitas_terakhir"])
        self.assertIn("28 lomba tercatat", rows["6"]["aktivitas_terakhir"])
        self.assertIn("3 dikirim", rows["6"]["aktivitas_terakhir"])
        self.assertIn("baseline Rp0", rows["7"]["aktivitas_terakhir"])
        self.assertIn("56/61 demo selesai", rows["9"]["aktivitas_terakhir"])
        self.assertEqual(rows["10"]["aktivitas_terakhir"],
                         "belum ada aktivitas")
        self.assertIn("2026-11-18 23:56", rows["13"]["aktivitas_terakhir"])
        # 14 mesin lama: status pasif non-job (bukan "mode persiapan").
        self.assertEqual(rows["14"]["status"], dashboard.STATUS_PASIF)
        self.assertIn("Belum ada lamaran", rows["14"]["aktivitas_terakhir"])
        self.assertIn("15 lead tercatat", rows["2"]["aktivitas_terakhir"])

    def test_ringkasan_data_nyata(self):
        r = dashboard.ringkasan_dashboard()
        self.assertEqual(r["total_agent"], 30)
        # KOREKSI 22 Nov 2026 (perintah Cipta): agent lama no 1–6 aktif,
        # diganti nama jadi A31–A36 — mesin pasif tinggal 8 (no 7–14).
        self.assertEqual(r["mesin_pasif"], 8)
        rows = {x["kode"]: x for x in dashboard.tabel_semua_agent()}
        self.assertEqual(rows["1"]["status"],
                         "Aktif — diganti nama jadi A31 Publish")
        self.assertEqual(rows["6"]["status"],
                         "Aktif — diganti nama jadi A36 Copywriter")
        self.assertEqual(rows["7"]["status"], dashboard.STATUS_PASIF)
        # 21 Nov 2026: 11 penugasan harian 19 Nov diarsipkan (digantikan
        # jadwal mesin v2.0) -> handoff menunggu 0; draf toko 12 -> 9.
        self.assertEqual(r["handoff_menunggu"], 0)
        self.assertEqual(r["penawaran_toko_draf"], 9)
        self.assertEqual(r["aktif_sebagian"], 4)
        self.assertEqual(r["terkendala"], 0)
        self.assertGreaterEqual(r["entri_log"], 6)
        self.assertEqual(r["aktif"] + r["aktif_sebagian"] + r["belum_jalan"],
                         30)
        self.assertGreaterEqual(r["aktif"], 1)

    def test_feed_memuat_entri_seed(self):
        log = dashboard.baca_log(limit=50)
        self.assertGreaterEqual(len(log), 3)
        aksi = [e["aksi"] for e in log]
        self.assertIn("30 modul dibuat", aksi)
        self.assertIn("agents.json digabung", aksi)


class TestFungsiBaruDashboard(unittest.TestCase):
    """Antrean kerja, pekerjaan terkendala, target 30 hari, platform."""

    def setUp(self):
        self._pk_no_log = os.environ.pop("PK_NO_LOG", None)
        self.tmp = tempfile.mkdtemp(prefix="pk-dash-")
        _tulis(self.tmp, "agents.json", {"agent_30": {"agents": [
            {"code": "A01", "name": "CEO Director", "division": "Direksi",
             "boss": "Pemilik", "job_desc": "j", "mapped_to": "Muse",
             "status": "Aktif"}]}})
        _tulis(self.tmp, "handoff.json", [
            {"id": "HO-001", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 1", "ringkasan": "Tugas uji", "status": "draf"},
            {"id": "HO-002", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 3",
             "ringkasan": "Posting video baru ke TikTok @meongcast hari ini",
             "status": "draf"},
        ])
        _tulis(self.tmp, "penjualan_toko.json", {"toko": [
            {"id": "toko-01", "nama": "Toko Uji", "status": "draf",
             "catatan": "IG toko aktif. | HASIL: belum dikirim"}]})
        _tulis(self.tmp, "produksi_game.json", [{"nama": "P1"}])
        _tulis(self.tmp, "lomba.json", [{"nama": "L1", "status": "dikirim"}])
        _tulis(self.tmp, "keuangan_data.json",
               {"baseline_tanggal": "2026-11-18", "entries": []})

    def tearDown(self):
        if self._pk_no_log is not None:
            os.environ["PK_NO_LOG"] = self._pk_no_log
        else:
            os.environ.pop("PK_NO_LOG", None)

    def test_antrean_kerja_fixture(self):
        antrean = dashboard.antrean_kerja(base=self.tmp)
        self.assertEqual(len(antrean), 3)
        by_id = {a["id"]: a for a in antrean}
        self.assertEqual(by_id["HO-HO-001"]["agent"], "A26")
        self.assertEqual(by_id["HO-HO-001"]["status"], "menunggu")
        self.assertEqual(by_id["HO-HO-001"]["prioritas"], "normal")
        self.assertEqual(by_id["HO-HO-001"]["tenggat"], "—")
        self.assertEqual(by_id["TK-toko-01"]["agent"], "A25")

    def test_tugas_terkendala_terpisah(self):
        terkendala = dashboard.tugas_terkendala(base=self.tmp)
        self.assertEqual(len(terkendala), 1)
        self.assertEqual(terkendala[0]["id"], "HO-HO-002")
        self.assertIn("TikTok @meongcast", terkendala[0]["penyebab"])
        self.assertIn("login", terkendala[0]["dibutuhkan_dari_cipta"])

    def test_target_30_hari_fixture(self):
        t = dashboard.target_30_hari(base=self.tmp)
        target = {x["nama"]: x for x in t["target"]}
        self.assertEqual(len(t["target"]), 5)
        self.assertEqual(target["Produk digital selesai"]["target"], 15)
        self.assertEqual(target["Produk digital selesai"]["realisasi"], 1)
        self.assertEqual(target["Lomba diikuti"]["realisasi"], 1)
        self.assertEqual(target["Pemasukan pertama"]["realisasi"], "Rp0")
        self.assertEqual(target["Konten terbit"]["realisasi"],
                         "belum cukup data")
        self.assertIn("bukan janji", t["catatan_jujur"])

    def test_platform_per_agent_data_nyata(self):
        data = {p["kode"]: p for p in dashboard.platform_per_agent()}
        a20 = data["A20"]
        self.assertIn("Instagram posting @meongcast", a20["terhubung"])
        self.assertIn("Instagram Messages @meongcast", a20["terhubung"])
        self.assertIn("Instagram @podcast_meong (login ditolak)",
                      a20["belum_terhubung"])
        a27 = data["A27"]
        self.assertIn("Gmail (tidak terhubung — kerja via browser, draf saja)",
                      a27["belum_terhubung"])
        # Semua 21 platform terhubung + 6 belum terhubung tercakup oleh
        # pemetaan (per agent memakai label dengan keterangan peran, jadi
        # dicek per nama platform, bukan jumlah string yang sama persis).
        terhubung_21 = ["Instagram posting @meongcast",
                        "Instagram Messages @meongcast",
                        "Threads posting @ciptabintanglestari",
                        "Threads Messages @ciptabintanglestari",
                        'Facebook "Masduki Kiki"', "TikTok @podcast_kucing",
                        "YouTube Podcast meong", "KaryaKarsa", "Lynk.id",
                        "Zazzle", "KBM", "Saweria", "Trakteer", "PayPal",
                        "BCA", "Adobe Stock", "Dreamstime", "Impact.com",
                        "GitHub Pages", "Faable", "DeployVera"]
        belum_6 = ["Gmail", "TikTok @meongcast", "Instagram @podcast_meong",
                   "YouTube @meongcast", "Mayar", "Upwork"]
        semua_terhubung = [p for a in data.values() for p in a["terhubung"]]
        semua_belum = [p for a in data.values() for p in a["belum_terhubung"]]
        for nama in terhubung_21:
            self.assertTrue(any(nama in p for p in semua_terhubung), nama)
        for nama in belum_6:
            self.assertTrue(any(nama in p for p in semua_belum), nama)
            self.assertFalse(any(nama in p for p in semua_terhubung), nama)


class TestTargetHarian(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="pk-dash-target-")
        shutil.copy(ROOT / "data" / "agents.json",
                    Path(self.tmp) / "agents.json")
        hari_ini = dashboard._waktu_sekarang()[:10]
        kemarin = (datetime.now(dashboard.WIB)
                   - timedelta(days=1)).strftime("%Y-%m-%d")
        _tulis(self.tmp, "mesin_eksekusi_log.json", [
            {"id": "ME-T1", "kode_agent": "A12", "status": "selesai",
             "waktu_selesai": hari_ini + " 04:54"},
            {"id": "ME-T2", "kode_agent": "A25",
             "status": "menunggu persetujuan",
             "waktu_selesai": hari_ini + " 05:19"},
            {"id": "ME-T3", "kode_agent": "A25", "status": "selesai",
             "waktu_selesai": kemarin + " 20:00"},
        ])

    def test_tiga_puluh_baris_target_per_agent(self):
        rows = dashboard.target_harian_dashboard(base=self.tmp)
        self.assertEqual(len(rows), 30)
        for r in rows:
            self.assertTrue(r["target_harian"]
                            and r["target_harian"] != "—", r["kode"])
            self.assertTrue(r["tugas_harian"]
                            and r["tugas_harian"] != "—", r["kode"])
        a12 = next(r for r in rows if r["kode"] == "A12")
        self.assertEqual(a12["target_harian"], "3–5 visual siap QC")
        self.assertTrue(a12["jalan"])
        self.assertEqual(a12["jalan_hari_ini"], 1)
        self.assertEqual(a12["draf_menunggu"], 0)
        a25 = next(r for r in rows if r["kode"] == "A25")
        # Run kemarin tidak dihitung sebagai jalan hari ini.
        self.assertEqual(a25["jalan_hari_ini"], 1)
        self.assertEqual(a25["draf_menunggu"], 1)
        a01 = next(r for r in rows if r["kode"] == "A01")
        self.assertFalse(a01["jalan"])
        self.assertEqual(a01["jalan_hari_ini"], 0)


if __name__ == "__main__":
    unittest.main()
