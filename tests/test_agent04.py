# ======================================================================
# Unit test Agent 4 — Penjualan Harian (a04_penjualan_harian).
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$HOME \
#     ~/workspace/audio-tools/python-packages/bin/python \
#     -m unittest tests.test_agent04 -v
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

import a04_penjualan_harian as A04  # noqa: E402


def _tmp_file(nama):
    tmp = Path(tempfile.mkdtemp())
    return tmp / nama


def _toko_contoh():
    return {
        "nama": "Toko Contoh Jaya",
        "jenis": "pet shop",
        "alamat": "Jl. Contoh No.1",
        "kecamatan": "Pasar Minggu",
        "kontak_hp": "0812-0000-1111",
        "kontak_sumber": "Google Maps",
        "medsos": "IG @contohjaya",
        "verifikasi": "wa_terkonfirmasi",
        "observasi": "jual pakan dan pasir kucing",
        "produk_tawaran": "video",
    }


class Basis(unittest.TestCase):
    def setUp(self):
        self.data_file = _tmp_file("penjualan_toko.json")
        self.leads_file = _tmp_file("leads.json")
        self.leads_file.write_text(json.dumps({"leads": []}, ensure_ascii=False),
                                   encoding="utf-8")

    def _tambah(self, **kw):
        d = _toko_contoh()
        d.update(kw)
        toko, info = A04.tambah_toko(data_file=str(self.data_file), **d)
        self.assertIsNotNone(toko, info)
        return toko


# ---------------------------------------------------------------------------
# Draf penawaran (memakai generator Agent 2 bila ada, fallback bila tidak)
# ---------------------------------------------------------------------------
class TestDraf(Basis):
    def test_draf_video_ada_harga_tautan_tanpa_janji(self):
        draf = A04.draf_personal("Toko Contoh Jaya",
                                 "jual pakan dan pasir kucing", "video")
        self.assertIn("Rp75.000", draf)
        self.assertIn(A04.CONTOH_VIDEO, draf)
        self.assertIn(A04.WEBSITE, draf)
        self.assertIn("Toko Contoh Jaya", draf)
        self.assertEqual(A04.cek_draf(draf), [])

    def test_draf_observasi_tidak_masuk_slot_produk(self):
        # Regresi 21 Nov 2026: observasi pernah dikirim ke slot produk
        # template wa_outreach -> "contoh konsep dulu untuk di Kebagusan ...".
        draf = A04.draf_personal(
            "Balini Petshop",
            "di Kebagusan Raya jual makanan untuk banyak hewan", "video")
        self.assertIn("Saya lihat toko Kakak di Kebagusan Raya", draf)
        self.assertIn("contoh konsep dulu untuk video", draf)
        self.assertNotIn("contoh konsep dulu untuk di Kebagusan", draf)
        self.assertEqual(A04.cek_draf(draf), [])

    def test_draf_aplikasi_harga_benar(self):
        draf = A04.draf_personal("Toko Contoh Jaya", "", "aplikasi")
        self.assertIn("Rp499.000", draf)
        self.assertIn("Rp400.000", draf)
        self.assertEqual(A04.cek_draf(draf), [])

    def test_draf_website_dan_poster(self):
        self.assertIn("Rp1.500.000",
                      A04.draf_personal("Toko X", "", "website"))
        self.assertIn("Rp35.000",
                      A04.draf_personal("Toko X", "", "poster"))
        self.assertIn("Rp9.900.000",
                      A04.draf_personal("Toko X", "", "website"))

    def test_cek_draf_tolak_kata_terlarang(self):
        masalah = A04.cek_draf("Video ini pasti viral dan views naik! Rp75.000 "
                               + A04.CONTOH_VIDEO + " " + A04.WEBSITE)
        self.assertTrue(any("viral" in m for m in masalah))

    def test_cek_draf_tolak_tanpa_harga(self):
        masalah = A04.cek_draf("Halo Kak, ini penawaran. " + A04.CONTOH_VIDEO
                               + " " + A04.WEBSITE)
        self.assertTrue(any("harga" in m for m in masalah))

    def test_draf_followup_sopan(self):
        draf = A04.draf_followup("Toko Contoh Jaya")
        self.assertIn("follow-up", draf.lower())
        self.assertIn("Rp75.000", draf)
        self.assertEqual(A04.cek_draf(draf), [])

    def test_a02_tidak_menjatuhkan_draf(self):
        # _a02() boleh mengembalikan modul atau None — keduanya harus aman.
        a02 = A04._a02()
        draf = A04.draf_personal("Toko X", "", "video")
        self.assertIn("Rp75.000", draf)
        if a02 is not None:
            self.assertTrue(hasattr(a02, "template_generator"))


# ---------------------------------------------------------------------------
# Data: tambah / duplikat / status / draf
# ---------------------------------------------------------------------------
class TestData(Basis):
    def test_tambah_dan_muat_ulang(self):
        toko = self._tambah()
        self.assertEqual(toko["id"], "toko-01")
        self.assertEqual(toko["status"], "draf")
        self.assertEqual(len(A04.load_toko(str(self.data_file))), 1)

    def test_duplikat_nama_ditolak(self):
        self._tambah()
        toko, info = A04.tambah_toko(nama="Toko Contoh Jaya",
                                     kontak_hp="0812-9999-8888",
                                     data_file=str(self.data_file))
        self.assertIsNone(toko)
        self.assertIn("Sudah ada", info)

    def test_duplikat_nomor_ditolak(self):
        self._tambah()
        toko, info = A04.tambah_toko(nama="Toko Lain",
                                     kontak_hp="0812-0000-1111",
                                     data_file=str(self.data_file))
        self.assertIsNone(toko)
        self.assertIn("Sudah ada", info)

    def test_nama_kosong_ditolak(self):
        toko, info = A04.tambah_toko(nama="   ", data_file=str(self.data_file))
        self.assertIsNone(toko)

    def test_verifikasi_tidak_dikenal_ditolak(self):
        toko, info = A04.tambah_toko(nama="Toko X", verifikasi="aneh",
                                     data_file=str(self.data_file))
        self.assertIsNone(toko)

    def test_ubah_status_valid_dan_tidak_valid(self):
        toko = self._tambah()
        ubah, _ = A04.ubah_status(toko["id"], "disetujui",
                                  data_file=str(self.data_file))
        self.assertEqual(ubah["status"], "disetujui")
        ubah2, info2 = A04.ubah_status(toko["id"], "aneh",
                                       data_file=str(self.data_file))
        self.assertIsNone(ubah2)
        self.assertIn("tidak dikenal", info2)

    def test_simpan_draf(self):
        toko = self._tambah()
        draf, _ = A04.buat_draf_untuk_toko(toko["id"], "video",
                                          data_file=str(self.data_file))
        self.assertIsNotNone(draf)
        self.assertIn("Rp75.000", draf)
        tersimpan = A04.load_toko(str(self.data_file))[0]
        self.assertEqual(tersimpan["draf"], draf)

    def test_buat_draf_toko_tidak_ada(self):
        draf, info = A04.buat_draf_untuk_toko("toko-99", "video",
                                             data_file=str(self.data_file))
        self.assertIsNone(draf)
        self.assertIn("tidak ditemukan", info)


# ---------------------------------------------------------------------------
# Alur data dengan Agent 2
# ---------------------------------------------------------------------------
class TestAlurAgent2(Basis):
    def test_kirim_terverifikasi_jadi_lead(self):
        toko = self._tambah()
        lead, info = A04.kirim_ke_agent2(toko["id"], str(self.data_file),
                                         str(self.leads_file))
        self.assertIsNotNone(lead, info)
        self.assertEqual(lead["status"], "baru")
        self.assertEqual(lead["nama"], "Toko Contoh Jaya")
        leads = json.loads(self.leads_file.read_text(encoding="utf-8"))["leads"]
        self.assertEqual(len(leads), 1)

    def test_kirim_belum_terverifikasi_ditolak(self):
        toko = self._tambah(verifikasi="perlu_dicek")
        lead, info = A04.kirim_ke_agent2(toko["id"], str(self.data_file),
                                         str(self.leads_file))
        self.assertIsNone(lead)
        self.assertIn("belum terverifikasi", info)

    def test_kirim_ganda_ditolak(self):
        toko = self._tambah()
        A04.kirim_ke_agent2(toko["id"], str(self.data_file), str(self.leads_file))
        lead2, info2 = A04.kirim_ke_agent2(toko["id"], str(self.data_file),
                                           str(self.leads_file))
        self.assertIsNone(lead2)
        self.assertIn("Sudah jadi lead", info2)

    def test_ambil_lead_baru_saja(self):
        leads = [
            {"id": "lead-01", "nama": "Toko Baru A", "kontak": "0812-2222-3333",
             "alamat": "Jl. A", "jenis": "pet shop", "status": "baru",
             "terverifikasi": True, "catatan": ""},
            {"id": "lead-02", "nama": "Toko Lama B", "kontak": "0812-4444-5555",
             "alamat": "Jl. B", "jenis": "pet shop", "status": "dihubungi",
             "terverifikasi": False, "catatan": ""},
        ]
        self.leads_file.write_text(json.dumps({"leads": leads}, ensure_ascii=False),
                                   encoding="utf-8")
        diambil, info = A04.ambil_lead_agent2(str(self.data_file),
                                              str(self.leads_file))
        self.assertEqual(len(diambil), 1)
        self.assertEqual(diambil[0]["nama"], "Toko Baru A")
        self.assertEqual(diambil[0]["verifikasi"], "wa_terkonfirmasi")
        self.assertEqual(diambil[0]["status"], "draf")

    def test_ambil_lead_lewati_duplikat(self):
        self._tambah(nama="Toko Sama", kontak_hp="0812-0000-1111")
        leads = [{"id": "lead-01", "nama": "Toko Sama",
                  "kontak": "0812-0000-1111", "alamat": "", "jenis": "pet shop",
                  "status": "baru", "terverifikasi": True, "catatan": ""}]
        self.leads_file.write_text(json.dumps({"leads": leads}, ensure_ascii=False),
                                   encoding="utf-8")
        diambil, _ = A04.ambil_lead_agent2(str(self.data_file),
                                           str(self.leads_file))
        self.assertEqual(len(diambil), 0)


# ---------------------------------------------------------------------------
# Ringkasan & rencana harian
# ---------------------------------------------------------------------------
class TestRencana(Basis):
    def test_rencana_kosong_kurang_15(self):
        r = A04.rencana_harian(str(self.data_file))
        self.assertEqual(r["target_harian"], 15)
        self.assertEqual(r["kurang"], 15)
        self.assertEqual(r["toko_hari_ini"], 0)

    def test_rencana_target_tercapai(self):
        for i in range(15):
            self._tambah(nama="Toko %02d" % i, kontak_hp="0812-0000-%04d" % i)
        r = A04.rencana_harian(str(self.data_file))
        self.assertEqual(r["kurang"], 0)
        self.assertEqual(r["toko_hari_ini"], 15)

    def test_ringkasan_menghitung_status(self):
        t1 = self._tambah(nama="Toko A", kontak_hp="0812-0000-0001")
        self._tambah(nama="Toko B", kontak_hp="0812-0000-0002")
        A04.ubah_status(t1["id"], "disetujui", data_file=str(self.data_file))
        s = A04.ringkasan(str(self.data_file))
        self.assertEqual(s["total"], 2)
        self.assertEqual(s["per_status"]["disetujui"], 1)
        self.assertEqual(s["per_status"]["draf"], 1)

    def test_mode_tanpa_key_template(self):
        import os
        os.environ.pop("GEMINI_API_KEY", None)
        self.assertEqual(A04.mode_ai(), "template")


# ---------------------------------------------------------------------------
# UI Gradio (dilewati bila gradio tidak tersedia di mesin tes)
# ---------------------------------------------------------------------------
class TestUI(unittest.TestCase):
    def test_build_ui_blocks(self):
        try:
            import gradio as gr  # noqa: F401
        except Exception as e:  # noqa: BLE001
            self.skipTest("gradio tidak tersedia: {}".format(e))
        demo = A04.build_ui()
        self.assertIsNotNone(demo)
        self.assertTrue(hasattr(demo, "render"))


if __name__ == "__main__":
    unittest.main()
