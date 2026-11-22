"""BINTANG COMMAND CENTER — Agent A08 Product Developer.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Mengubah kebutuhan tervalidasi menjadi konsep dan produk
Divisi: Riset · Atasan: A03
Dipetakan ke (sistem kita): A5 Produksi + A9
Pemetaan Gemini #1: Divisi 1 — R&D — 1A — Market Researcher (pengembangan konsep)
Status nyata: Aktif

KEJUJURAN WAJIB — BACA DULU:
- Agent ini PASIF: dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri.
  A01 CEO = Muse sebagai koordinator (bukan agent yang berjalan sendiri).
- Semua output adalah DRAF untuk persetujuan Cipta. Modul ini TIDAK PUNYA
  fungsi kirim / bayar / publikasi / submit apa pun, sengaja.
- Dilarang mengarang portofolio, klien, penghasilan, rating, angka, atau
  janji views / viral / penjualan. Bila data kurang, tulis
  "belum cukup data".
- Target/KPI Gemini di bawah adalah TARGET RANCANGAN (Share Gemini #1),
  bukan hasil nyata dan bukan janji.
- Pusat komando BUKAN Agent.ai (dialihkan ke builderpack.com, cek live
  21 Nov 2026) dan database BUKAN Google Sheets (kita tetap JSON).
  Tidak ada framework otonom (CrewAI/AutoGen ditolak) dan tidak ada
  otomasi 24 jam.
- Gemini free tier HANYA dari env var GEMINI_API_KEY — tidak pernah
  ditulis di file. Tanpa key, semua fitur tetap jalan mode template.
"""
import json
import os
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
MODEL = "gemini-2.0-flash"

KODE = "A08"
NAMA = "Product Developer"
DIVISI = "Riset"
ATASAN = "A03"
JOB_DESC = "Mengubah kebutuhan tervalidasi menjadi konsep dan produk"
DIPETAKAN_KE = "A5 Produksi + A9"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 1 — R&D"
GEMINI_PERAN = "1A — Market Researcher (pengembangan konsep)"
GEMINI_KPI = ['5 ide produk valid/hari (target rancangan)']
GEMINI_TOOLS = ['Google Trends', 'Perplexity.ai', 'Gemini Deep Research']


KATA_TERLARANG = ["viral", "views naik", "penjualan naik", "pasti laku",
                  "dijamin", "guaranteed", "testimoni", "100% viral",
                  "penghasilan pasti"]


def gemini_client():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception:
        return None


def gemini_ask(prompt: str):
    """Kembalikan teks jawaban Gemini, atau None bila key tidak ada / gagal."""
    client = gemini_client()
    if client is None:
        return None
    try:
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        text = (getattr(resp, "text", "") or "").strip()
        return text or None
    except Exception:
        return None


def mode_ai():
    return "gemini" if os.environ.get("GEMINI_API_KEY", "").strip() else "template"


def _draf_dasar(jenis, judul):
    draf = {"status": "draf", "butuh_persetujuan": True, "agent": KODE,
            "nama_agent": NAMA, "jenis": jenis, "judul": judul,
            "mode": mode_ai(), "tanggal": date.today().isoformat(),
            "catatan": "DRAF — wajib diperiksa dan disetujui Cipta sebelum dipakai/dikirim."}
    try:
        if not os.environ.get("PK_NO_LOG"):
            from dashboard import log_activity
            log_activity(KODE, "buat draf: " + jenis, judul)
    except Exception:
        pass
    return draf


def _polish(teks, pakai_ai=False):
    """Bila pakai_ai=True dan ada key, minta Gemini memperbaiki draf tanpa mengubah fakta/harga/tautan/angka."""
    if not pakai_ai or not (teks or "").strip():
        return None
    return gemini_ask("Perbaiki draf berikut tanpa mengubah fakta, harga, tautan, atau angka. "
                      "Jangan tambah janji views/viral/penjualan. Jangan karang klien, penghasilan, atau rating.\n\n" + teks)


def cek_draf(teks):
    """Periksa teks draf: kata terlarang + teks kosong. Kembalikan daftar masalah (kosong = bersih)."""
    masalah = []
    t = (teks or "")
    if not t.strip():
        masalah.append("Teks draf kosong.")
        return masalah
    rendah = t.lower()
    for kata in KATA_TERLARANG:
        if kata in rendah:
            masalah.append("Kata terlarang: '{}'".format(kata))
    return masalah


def info():
    """Metadata agent (untuk tes + tab Pusat Komando)."""
    return {"kode": KODE, "nama": NAMA, "divisi": DIVISI, "atasan": ATASAN,
            "job_desc": JOB_DESC, "dipetakan_ke": DIPETAKAN_KE, "status": STATUS,
            "gemini_divisi": GEMINI_DIVISI, "gemini_peran": GEMINI_PERAN,
            "gemini_kpi": list(GEMINI_KPI), "gemini_tools": list(GEMINI_TOOLS),
            "pasif": True}


def ringkasan():
    """Ringkasan status agent."""
    d = info()
    d["mode"] = mode_ai()
    d["catatan"] = ("Agent pasif — dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri. "
                    "Semua output DRAF untuk persetujuan Cipta.")
    return d

ENAM_SYARAT = ["Masalah pelanggan yang diselesaikan", "Target pembeli yang jelas",
               "Keunikan dibandingkan produk pesaing", "Perkiraan harga dan biaya",
               "Bukti minat pasar", "Rencana promosi dan distribusi"]


def _terisi(nilai):
    return bool(nilai) and str(nilai).strip() not in ("", "belum cukup data")


def buat_konsep_produk(nama, masalah, customer, keunikan="", harga_rp=None,
                       bukti="belum cukup data", rencana="", pakai_ai=False):
    """Draf konsep produk dengan 6 syarat wajib (Share #18).
    Bila ada syarat kosong / 'belum cukup data', konsep ditandai belum lengkap."""
    draf = _draf_dasar("konsep_produk", "Konsep produk: {}".format((nama or "").strip() or "?"))
    draf["nama"] = (nama or "").strip()
    draf["masalah_customer"] = (masalah or "").strip()
    draf["target_customer"] = (customer or "").strip()
    draf["keunikan"] = (keunikan or "").strip()
    draf["harga_rp"] = harga_rp
    draf["bukti_minat_pasar"] = (bukti or "").strip()
    draf["rencana_promosi_distribusi"] = (rencana or "").strip()
    kosong = [k for k in ("masalah_customer", "target_customer", "keunikan",
                          "bukti_minat_pasar", "rencana_promosi_distribusi")
              if not _terisi(draf[k])]
    if harga_rp is None:
        kosong.append("harga_rp")
    draf["syarat_wajib"] = ENAM_SYARAT
    draf["lengkap"] = not kosong
    draf["yang_kurang"] = kosong
    draf["target_rancangan_gemini"] = GEMINI_KPI
    versi_ai = _polish("Konsep produk {} untuk {}. Keunikan: {}.".format(
        draf["nama"], draf["target_customer"], draf["keunikan"]), pakai_ai)
    if versi_ai:
        draf["versi_ai"] = versi_ai
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return buat_konsep_produk("eBook Resep Kucing", "Pemilik kucing bingung masak", "Pemilik kucing", "Resep dari sudut pandang Oyen", 29000, "belum cukup data", "TikTok + Instagram")


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
