# ======================================================================
# Unit test Mesin Eksekusi 30 Agent Bintang (agents/mesin_eksekusi.py).
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH="$PATH" HOME="$HOME" ~/workspace/tmp/venv-pk/bin/python \
#     -m unittest discover -s tests -v
# Semua test tanpa panggilan jaringan (mode template; tanpa GEMINI_API_KEY)
# dan tanpa menyentuh data nyata (folder sementara + PK_NO_LOG + PK_DATA_DIR).
# ======================================================================
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("PK_NO_LOG", "1")  # tes tidak menulis activity_log nyata

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT))

import mesin_eksekusi as MESIN  # noqa: E402


def _tulis(folder, nama, data):
    with open(Path(folder) / nama, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _salin_agents_json(folder):
    shutil.copy(ROOT / "data" / "agents.json", Path(folder) / "agents.json")


class _BaseFixture(unittest.TestCase):
    def setUp(self):
        self._pk_no_log = os.environ.get("PK_NO_LOG")
        os.environ["PK_NO_LOG"] = "1"
        self.tmp = tempfile.mkdtemp(prefix="pk-mesin-")
        _salin_agents_json(self.tmp)
        _tulis(self.tmp, "handoff.json", [
            {"id": "HO-001", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 1", "ringkasan": "Tugas uji asisten",
             "status": "draf"},
            {"id": "HO-002", "jenis": "sales-lead", "dari_agent": "Muse",
             "ke_agent": "Agent 2",
             "ringkasan": "Penawaran ke Toko Uji",
             "isi": {"nama_toko": "Toko Uji"}, "status": "draf"},
            {"id": "HO-003", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 3",
             "ringkasan": "Posting video baru ke TikTok @meongcast hari ini",
             "status": "draf"},
            {"id": "HO-004", "jenis": "penugasan", "dari_agent": "Muse",
             "ke_agent": "Agent 13",
             "ringkasan": "Cek inbox dan balas email pelanggan",
             "status": "diperiksa"},
        ])
        _tulis(self.tmp, "penjualan_toko.json", {"toko": [
            {"id": "toko-01", "nama": "Toko Uji", "status": "draf",
             "catatan": "IG toko aktif, ramai. | HASIL: belum dikirim"},
            {"id": "toko-02", "nama": "Toko Kirim", "status": "terkirim"},
        ]})
        _tulis(self.tmp, "produksi_game.json", [{"nama": "P%d" % i} for i in range(3)])
        _tulis(self.tmp, "lomba.json", [
            {"nama": "L1", "status": "dikirim"},
            {"nama": "L2", "status": "baru"},
        ])
        _tulis(self.tmp, "keuangan_data.json",
               {"baseline_tanggal": "2026-11-18", "entries": []})

    def tearDown(self):
        if self._pk_no_log is not None:
            os.environ["PK_NO_LOG"] = self._pk_no_log
        else:
            os.environ.pop("PK_NO_LOG", None)


class TestDaftarDanJadwal(_BaseFixture):
    def test_daftar_30_agent(self):
        agents = MESIN.daftar_agent_bintang(self.tmp)
        self.assertEqual(len(agents), 30)
        self.assertEqual({a["code"] for a in agents},
                         {"A%02d" % i for i in range(1, 31)})
        # Job description tidak diubah: A12 tetap seperti di agents.json.
        a12 = next(a for a in agents if a["code"] == "A12")
        self.assertEqual(
            a12["job_desc"], "Membuat visual, foto, ilustrasi dan aset desain AI")
        self.assertEqual(a12["platform"]["terhubung"],
                         ["Adobe Stock (foto AI)", "Dreamstime (foto AI)"])

    def test_info_agent_tidak_dikenal(self):
        self.assertIsNone(MESIN.info_agent("A99", self.tmp))
        modul, err = MESIN.muat_modul_bintang("A99", self.tmp)
        self.assertIsNone(modul)
        self.assertIn("tidak ada", err)

    def test_jadwal_lima_slot_gemini(self):
        jadwal = MESIN.jadwal_harian_mesin(self.tmp)
        self.assertIn("06:00", jadwal["bingkai"])
        slot = jadwal["slot"]
        self.assertEqual(len(slot), 5)
        self.assertEqual(slot[0]["jam"], "06.00")
        self.assertEqual(slot[0]["agent"], ["A06", "A07", "A09", "A10", "A28"])
        self.assertEqual(slot[1]["agent"],
                         ["A%02d" % i for i in range(11, 20)])
        self.assertEqual(slot[2]["agent"],
                         ["A%02d" % i for i in range(20, 25)])
        self.assertEqual(slot[3]["agent"], ["A25", "A26", "A27"])
        self.assertEqual(slot[4]["agent"], ["A05", "A29"])

    def test_slot_untuk_jam(self):
        self.assertEqual(MESIN.slot_untuk_jam(6)["kegiatan"], "Riset & Lomba")
        self.assertEqual(MESIN.slot_untuk_jam(8)["kegiatan"], "Produksi")
        self.assertEqual(MESIN.slot_untuk_jam(15)["kegiatan"], "Distribusi")
        self.assertEqual(MESIN.slot_untuk_jam(21)["kegiatan"],
                         "Audit Keuangan & Operasional")
        self.assertEqual(MESIN.slot_untuk_jam(13)["kegiatan"], "CS & Closing")

    def test_target_30_hari_dari_data_fixture(self):
        t = MESIN.target_30_hari(self.tmp)
        target = {x["nama"]: x for x in t["target"]}
        self.assertEqual(target["Produk digital selesai"]["target"], 15)
        self.assertEqual(target["Produk digital selesai"]["realisasi"], 3)
        self.assertEqual(target["Konten terbit"]["realisasi"], "belum cukup data")
        self.assertEqual(target["Followers baru"]["realisasi"], "belum cukup data")
        self.assertEqual(target["Lomba diikuti"]["realisasi"], 1)
        self.assertEqual(target["Pemasukan pertama"]["realisasi"], "Rp0")
        self.assertIn("bukan janji", t["catatan_jujur"])


class TestAntreanDanKendala(_BaseFixture):
    def test_antrean_rute_dan_status(self):
        antrean = MESIN.antrean_kerja(self.tmp)
        by_id = {a["id"]: a for a in antrean}
        # Handoff penugasan ke Agent 1 -> A26 (mesin Asisten dipakai A26).
        self.assertEqual(by_id["HO-HO-001"]["agent"], "A26")
        self.assertEqual(by_id["HO-HO-001"]["status"], "menunggu")
        # Sales-lead -> A25; diperiksa -> menunggu persetujuan.
        self.assertEqual(by_id["HO-HO-002"]["agent"], "A25")
        self.assertEqual(by_id["HO-HO-004"]["status"], "menunggu persetujuan")
        # Draf toko -> A25 dengan tugas nyata (nama toko + observasi).
        tk = by_id["TK-toko-01"]
        self.assertEqual(tk["agent"], "A25")
        self.assertEqual(tk["tugas"]["nama_toko"], "Toko Uji")
        self.assertIn("IG toko aktif", tk["tugas"]["observasi"])
        # Toko terkirim tidak masuk antrean.
        self.assertNotIn("TK-toko-02", by_id)

    def test_kendala_tiktok_meongcast_terdeteksi(self):
        antrean = MESIN.antrean_kerja(self.tmp)
        item = next(a for a in antrean if a["id"] == "HO-HO-003")
        self.assertEqual(item["status"], "terkendala")
        self.assertIn("TikTok @meongcast", item["penyebab"])
        self.assertIn("login", item["dibutuhkan_dari_cipta"])
        self.assertEqual(len(MESIN.tugas_terkendala(self.tmp)), 1)

    def test_alamat_email_bukan_kendala_gmail(self):
        # "masduki1189@gmail.com" di teks tugas BUKAN butuh platform Gmail.
        item = {"ringkasan": "Riset Genspark login jadi, masduki1189@gmail.com",
                "tugas": {}}
        self.assertIsNone(MESIN.tentukan_kendala(item))
        # Tapi "kirim email lewat Gmail" (aksi + platform) terkendala.
        item2 = {"ringkasan": "Kirim email penawaran lewat Gmail ke toko",
                 "tugas": {}}
        kendala = MESIN.tentukan_kendala(item2)
        self.assertIsNotNone(kendala)
        self.assertIn("Gmail", kendala[0])

    def test_kendala_data_toko_tanpa_nama(self):
        item = {"sumber": "penawaran-toko", "ringkasan": "x",
                "tugas": {"nama_toko": ""}}
        kendala = MESIN.tentukan_kendala(item)
        self.assertIsNotNone(kendala)
        self.assertIn("nama toko", kendala[0])


class TestEksekusiNyata(_BaseFixture):
    def test_a12_tugas_nyata_bukan_contoh(self):
        r = MESIN.jalankan_agent(
            "A12", tugas={"jenis": "ilustrasi eBook",
                          "tema": "Nabi Yunus dan Ikan Paus"}, base=self.tmp)
        self.assertTrue(r["ok"])
        self.assertEqual(r["mode"], "tugas")
        self.assertEqual(r["status"], "menunggu persetujuan")
        self.assertIn("Nabi Yunus dan Ikan Paus",
                      r["draf"]["prompt_gambar_draf"])
        self.assertEqual(r["draf"]["status"], "draf")
        self.assertTrue(r["draf"]["butuh_persetujuan"])

    def test_a25_tugas_nyata_delegasi_mesin_lama(self):
        r = MESIN.jalankan_agent(
            "A25", tugas={"nama_toko": "Toko Uji", "produk": "video",
                          "observasi": "IG toko aktif, ramai"}, base=self.tmp)
        self.assertTrue(r["ok"])
        self.assertEqual(r["mode"], "tugas")
        self.assertIn("Toko Uji", r["draf"]["teks"])
        # Delegasi ke mesin lama a04 bila tersedia, dicatat jujur di draf.
        self.assertIn("sumber", r["draf"])

    def test_tanpa_tugas_jadi_contoh_dan_dicatat(self):
        r = MESIN.jalankan_agent("A12", tugas=None, base=self.tmp)
        self.assertTrue(r["ok"])
        self.assertEqual(r["mode"], "contoh")
        self.assertIn("contoh", r["alasan"])

    def test_agent_tidak_dikenal_gagal_sopan(self):
        r = MESIN.jalankan_agent("A99", base=self.tmp)
        self.assertFalse(r["ok"])
        self.assertIn("tidak ada", r["alasan"])

    def test_jalankan_antrean_proses_menunggu_lewati_terkendala(self):
        hasil = MESIN.jalankan_antrean(self.tmp, maks=10)
        # Fixture: 3 menunggu (HO-001, HO-002, TK-toko-01) dijalankan;
        # HO-003 terkendala + HO-004 sudah menunggu persetujuan dilewati
        # (tidak dobel, tidak dihitung sebagai kendala baru).
        self.assertEqual(hasil["dijalankan"], 3)
        self.assertEqual(hasil["berhasil"], 3)
        self.assertEqual(hasil["terkendala"], 0)
        self.assertEqual(hasil["dilewati"], 2)
        log = MESIN.audit_log(self.tmp)
        self.assertEqual(len(log), 3)
        # Jalan kedua: semua sudah diproses -> tidak ada yang dobel.
        hasil2 = MESIN.jalankan_antrean(self.tmp, maks=10)
        self.assertEqual(hasil2["dijalankan"], 0)
        self.assertEqual(len(MESIN.audit_log(self.tmp)), 3)

    def test_jalankan_slot_produksi(self):
        hasil = MESIN.jalankan_slot(8, self.tmp)
        self.assertEqual(hasil["kegiatan"], "Produksi")
        self.assertEqual(hasil["dijalankan"], 9)
        self.assertEqual(hasil["berhasil"], 9)
        self.assertTrue(all(r["mode"] == "contoh" for r in hasil["rincian"]))

    def test_kpi_dan_audit_dan_persetujuan(self):
        MESIN.jalankan_agent(
            "A12", tugas={"jenis": "ilustrasi", "tema": "Uji"}, base=self.tmp)
        kpi = {k["kode"]: k for k in MESIN.kpi_agent(self.tmp)}
        self.assertEqual(len(kpi), 30)
        self.assertEqual(kpi["A12"]["eksekusi"], 1)
        self.assertEqual(kpi["A12"]["draf_menunggu"], 1)
        self.assertEqual(kpi["A12"]["target"],
                         ["5–10 aset visual/hari (target rancangan)"])
        self.assertEqual(kpi["A13"]["eksekusi"], 0)
        self.assertEqual(kpi["A13"]["terakhir"], "—")
        run_id = MESIN.audit_log(self.tmp)[0]["id"]
        self.assertTrue(MESIN.catat_persetujuan(run_id, "disetujui",
                                                base=self.tmp))
        self.assertEqual(MESIN.audit_log(self.tmp)[0]["keputusan"], "disetujui")
        self.assertEqual(MESIN.audit_log(self.tmp)[0]["status"], "selesai")
        self.assertFalse(MESIN.catat_persetujuan("ME-TIDAK-ADA", "disetujui",
                                                 base=self.tmp))
        self.assertFalse(MESIN.catat_persetujuan(run_id, "ragu-ragu",
                                                 base=self.tmp))

    def test_platform_per_agent(self):
        data = {p["kode"]: p for p in MESIN.platform_per_agent(self.tmp)}
        self.assertIn("Instagram posting @meongcast",
                      data["A20"]["terhubung"])
        self.assertIn("Instagram @podcast_meong (login ditolak)",
                      data["A20"]["belum_terhubung"])
        self.assertIn("Gmail (tidak terhubung — kerja via browser, draf saja)",
                      data["A27"]["belum_terhubung"])
        self.assertIn("Upwork (belum ada akun)",
                      data["A28"]["belum_terhubung"])


class TestLaranganKeras(unittest.TestCase):
    def test_tidak_ada_fungsi_kirim_bayar(self):
        sumber = (AGENTS / "mesin_eksekusi.py").read_text(encoding="utf-8")
        for pola in ("def kirim", "def bayar", "def upload", "def publish",
                     "def submit", "def transfer", "smtplib", "requests.",
                     "urllib.request", "httpx", "whatsapp", "telegram"):
            self.assertNotIn(pola, sumber, pola)

    def test_cli_antrean_tanpa_sentuh_data_nyata(self):
        tmp = tempfile.mkdtemp(prefix="pk-mesin-cli-")
        _salin_agents_json(tmp)
        _tulis(tmp, "handoff.json", [])
        _tulis(tmp, "penjualan_toko.json", {"toko": []})
        log_nyata = ROOT / "data" / "mesin_eksekusi_log.json"
        sebelum = (log_nyata.exists(),
                   log_nyata.stat().st_mtime_ns if log_nyata.exists() else None)
        os.environ["PK_DATA_DIR"] = tmp
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = MESIN.main(["--antrean"])
            self.assertEqual(kode, 0)
            self.assertEqual(json.loads(buf.getvalue()), [])
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = MESIN.main(["A12", '{"jenis": "ilustrasi", "tema": "Uji CLI"}'])
            self.assertEqual(kode, 0)
            hasil = json.loads(buf.getvalue())
            self.assertTrue(hasil["ok"])
            self.assertEqual(hasil["mode"], "tugas")
            self.assertTrue((Path(tmp) / "mesin_eksekusi_log.json").exists())
            # Log mesin data nyata tidak berubah selama tes CLI.
            sesudah = (log_nyata.exists(),
                       log_nyata.stat().st_mtime_ns if log_nyata.exists() else None)
            self.assertEqual(sesudah, sebelum)
        finally:
            os.environ.pop("PK_DATA_DIR", None)


if __name__ == "__main__":
    unittest.main()
