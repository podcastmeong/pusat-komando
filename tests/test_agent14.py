# ======================================================================
# Unit test Agent 14 — Upwork (a14_upwork).
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$HOME \
#     ~/workspace/audio-tools/python-packages/bin/python \
#     -m unittest tests.test_agent14 -v
# (env bersih diperlukan karena gradio gagal impor bila variabel proxy
# VM ini terbaca.)
# Semua test memakai data_dir sementara — tidak menyentuh data asli.
# ======================================================================
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT))

import a14_upwork as A14  # noqa: E402


def _tmp_file(nama):
    tmp = Path(tempfile.mkdtemp())
    return tmp / nama


def _job_contoh():
    return {
        "judul": "Create a 30s AI product video ad",
        "klien": "Acme Corp",
        "kategori": "video-ai",
        "jenis": "fixed",
        "anggaran_usd": 100,
        "tautan": "https://www.upwork.com/jobs/~0123456789abcdef",
        "catatan": "video vertikal 9:16 untuk produk skincare",
    }


class Basis(unittest.TestCase):
    def setUp(self):
        self.data_file = _tmp_file("lamaran_upwork.json")

    def _tambah(self, **kw):
        d = _job_contoh()
        d.update(kw)
        job, info = A14.tambah_job(data_file=str(self.data_file), **d)
        self.assertIsNotNone(job, info)
        return job


# ---------------------------------------------------------------------------
# Status akun (mode persiapan — akun belum ada)
# ---------------------------------------------------------------------------
class TestStatusAkun(unittest.TestCase):
    def test_akun_belum_ada(self):
        s = A14.status_akun()
        self.assertFalse(s["akun_ada"])
        self.assertEqual(s["status"], "belum_ada")
        self.assertIn("Cloudflare", s["keterangan"])
        self.assertEqual(s["rencana"]["tarif_per_jam_usd"], 10)
        self.assertEqual(s["rencana"]["email"], "masduki1189@gmail.com")


# ---------------------------------------------------------------------------
# Teks profil freelancer
# ---------------------------------------------------------------------------
class TestProfil(unittest.TestCase):
    def test_profil_ada_judul_tarif_portofolio(self):
        teks = A14.teks_profil()
        self.assertIn("AI Video Creator & Web Developer", teks)
        self.assertIn("$10/hour", teks)
        self.assertIn(A14.WEBSITE, teks)
        self.assertIn("Aq98mScKCLA", teks)
        self.assertIn("Masduki", teks)
        self.assertIn("Jakarta", teks)

    def test_profil_tanpa_klaim_palsu(self):
        teks = A14.teks_profil().lower()
        for kata in ("viral", "guaranteed", "100+ clients", "top rated"):
            self.assertNotIn(kata, teks)

    def test_profil_singkat(self):
        teks = A14.teks_profil_singkat()
        self.assertIn("AI Video Creator", teks)
        self.assertIn(A14.WEBSITE, teks)


# ---------------------------------------------------------------------------
# Template proposal
# ---------------------------------------------------------------------------
class TestProposal(unittest.TestCase):
    def test_proposal_panjang_ada_tautan_tarif_nama(self):
        p = A14.template_proposal("Create a 30s AI product video ad",
                                  "Acme Corp", "fixed", 100)
        self.assertIn("Masduki", p)
        self.assertIn("Acme Corp", p)
        self.assertIn(A14.WEBSITE, p)
        self.assertIn("Aq98mScKCLA", p)
        self.assertIn("per scope", p)
        self.assertEqual(A14.cek_proposal(p), [])

    def test_proposal_hourly_tarif_per_jam(self):
        p = A14.template_proposal("Edit short-form videos", "", "hourly", 10)
        self.assertIn("$10/hour", p)
        self.assertEqual(A14.cek_proposal(p), [])

    def test_proposal_singkat(self):
        p = A14.template_proposal_singkat("Landing page for a cafe")
        self.assertIn("Masduki", p)
        self.assertIn("$10/hour", p)
        self.assertIn(A14.WEBSITE, p)
        self.assertEqual(A14.cek_proposal(p), [])

    def test_cek_proposal_tolak_kata_terlarang(self):
        masalah = A14.cek_proposal(
            "I guarantee viral views! Masduki. $10/hour. " + A14.WEBSITE)
        self.assertTrue(any("viral" in m or "guaranteed" in m for m in masalah))

    def test_cek_proposal_tolak_tanpa_portofolio(self):
        masalah = A14.cek_proposal("Hi, I'm Masduki. $10/hour. Let's work.")
        self.assertTrue(any("portofolio" in m for m in masalah))

    def test_cek_proposal_tolak_tanpa_tarif(self):
        masalah = A14.cek_proposal("Hi, I'm Masduki. Portfolio: " + A14.WEBSITE)
        self.assertTrue(any("Tarif" in m for m in masalah))

    def test_followup_sopan(self):
        f = A14.template_followup("Create a 30s AI product video ad", "Acme")
        self.assertIn("Acme", f)
        self.assertIn("following up", f.lower())
        self.assertNotIn("viral", f.lower())


# ---------------------------------------------------------------------------
# Riset job — kelayakan
# ---------------------------------------------------------------------------
class TestCekJob(unittest.TestCase):
    def test_job_layak(self):
        layak, _ = A14.cek_job_layak("AI product video", "30s vertical ad",
                                     True, 100, "fixed")
        self.assertTrue(layak)

    def test_tolak_unpaid_test(self):
        layak, alasan = A14.cek_job_layak("Video editor (unpaid test)",
                                          "free trial first", True, 200, "fixed")
        self.assertFalse(layak)
        self.assertIn("unpaid test", alasan)

    def test_tolak_pembayaran_belum_terverifikasi(self):
        layak, alasan = A14.cek_job_layak("Landing page", "", False, 500, "fixed")
        self.assertFalse(layak)
        self.assertIn("terverifikasi", alasan)

    def test_tolak_anggaran_di_bawah_minimum(self):
        layak, alasan = A14.cek_job_layak("Video ad", "", True, 20, "fixed")
        self.assertFalse(layak)
        self.assertIn("minimum", alasan)

    def test_tolak_tarif_jam_di_bawah_minimum(self):
        layak, alasan = A14.cek_job_layak("Video editing", "", True, 5, "hourly")
        self.assertFalse(layak)
        self.assertIn("minimum", alasan)

    def test_kategori_ada_lima(self):
        kats = A14.daftar_kategori()
        self.assertEqual(len(kats), 5)
        self.assertEqual({k["id"] for k in kats},
                         {"video-ai", "video-pendek", "web-statis", "web-app",
                          "game-html5"})


# ---------------------------------------------------------------------------
# Data: tambah / duplikat / status / proposal
# ---------------------------------------------------------------------------
class TestData(Basis):
    def test_tambah_dan_muat_ulang(self):
        job = self._tambah()
        self.assertEqual(job["id"], "lam-01")
        self.assertEqual(job["status"], "riset")
        self.assertEqual(len(A14.load_lamaran(str(self.data_file))), 1)

    def test_duplikat_judul_klien_ditolak(self):
        self._tambah()
        job, info = A14.tambah_job(judul="Create a 30s AI product video ad",
                                   klien="Acme Corp",
                                   data_file=str(self.data_file))
        self.assertIsNone(job)
        self.assertIn("Sudah ada", info)

    def test_duplikat_tautan_ditolak(self):
        self._tambah()
        job, info = A14.tambah_job(judul="Judul lain", klien="Klien lain",
                                   tautan="https://www.upwork.com/jobs/~0123456789abcdef",
                                   data_file=str(self.data_file))
        self.assertIsNone(job)
        self.assertIn("Sudah ada", info)

    def test_judul_kosong_ditolak(self):
        job, info = A14.tambah_job(judul="   ", data_file=str(self.data_file))
        self.assertIsNone(job)

    def test_kategori_tidak_dikenal_ditolak(self):
        job, info = A14.tambah_job(judul="Job X", kategori="aneh",
                                   data_file=str(self.data_file))
        self.assertIsNone(job)

    def test_ubah_status_valid_dan_tidak_valid(self):
        job = self._tambah()
        ubah, _ = A14.ubah_status(job["id"], "disetujui",
                                  data_file=str(self.data_file))
        self.assertEqual(ubah["status"], "disetujui")
        ubah2, info2 = A14.ubah_status(job["id"], "aneh",
                                       data_file=str(self.data_file))
        self.assertIsNone(ubah2)
        self.assertIn("tidak dikenal", info2)

    def test_buat_proposal_tersimpan(self):
        job = self._tambah()
        proposal, _ = A14.buat_proposal_untuk_job(job["id"], "panjang",
                                                  data_file=str(self.data_file))
        self.assertIsNotNone(proposal)
        self.assertIn("Masduki", proposal)
        tersimpan = A14.load_lamaran(str(self.data_file))[0]
        self.assertEqual(tersimpan["proposal"], proposal)
        self.assertEqual(tersimpan["status"], "draf")

    def test_buat_proposal_job_tidak_ada(self):
        proposal, info = A14.buat_proposal_untuk_job(
            "lam-99", "panjang", data_file=str(self.data_file))
        self.assertIsNone(proposal)
        self.assertIn("tidak ditemukan", info)


# ---------------------------------------------------------------------------
# Ringkasan & rencana harian
# ---------------------------------------------------------------------------
class TestRencana(Basis):
    def test_rencana_kosong_kurang_5_dan_mode_persiapan(self):
        r = A14.rencana_harian(str(self.data_file))
        self.assertEqual(r["target_harian"], 5)
        self.assertEqual(r["kurang"], 5)
        self.assertEqual(r["job_hari_ini"], 0)
        self.assertTrue(any("MODE PERSIAPAN" in a["judul"] for a in r["aksi"]))

    def test_rencana_target_tercapai(self):
        for i in range(5):
            self._tambah(judul="Job %02d" % i, klien="Klien %02d" % i,
                         tautan="https://www.upwork.com/jobs/~%d" % i)
        r = A14.rencana_harian(str(self.data_file))
        self.assertEqual(r["kurang"], 0)
        self.assertEqual(r["job_hari_ini"], 5)

    def test_ringkasan_menghitung_status(self):
        j1 = self._tambah(judul="Job A", klien="Klien A",
                          tautan="https://www.upwork.com/jobs/~a")
        self._tambah(judul="Job B", klien="Klien B",
                     tautan="https://www.upwork.com/jobs/~b")
        A14.ubah_status(j1["id"], "disetujui", data_file=str(self.data_file))
        s = A14.ringkasan(str(self.data_file))
        self.assertEqual(s["total"], 2)
        self.assertEqual(s["per_status"]["disetujui"], 1)
        self.assertEqual(s["per_status"]["riset"], 1)
        self.assertFalse(s["akun_ada"])

    def test_mode_tanpa_key_template(self):
        import os
        os.environ.pop("GEMINI_API_KEY", None)
        self.assertEqual(A14.mode_ai(), "template")


# ---------------------------------------------------------------------------
# UI Gradio (dilewati bila gradio tidak tersedia di mesin tes)
# ---------------------------------------------------------------------------
class TestUI(unittest.TestCase):
    def test_build_ui_blocks(self):
        try:
            import gradio as gr  # noqa: F401
        except Exception as e:  # noqa: BLE001
            self.skipTest("gradio tidak tersedia: {}".format(e))
        demo = A14.build_ui()
        self.assertIsNotNone(demo)
        self.assertTrue(hasattr(demo, "render"))


if __name__ == "__main__":
    unittest.main()
