"""BINTANG COMMAND CENTER — Agent A19 Content Producer.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Mengubah produk dan riset menjadi materi konten
Divisi: Produksi · Atasan: A08
Dipetakan ke (sistem kita): A5 Produksi + A3
Pemetaan Gemini #1: Divisi 2 — Creative Studio — 2A/2B + Divisi 3 (content producer)
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
MODEL = "gemini-4-hydrogen"

KODE = "A19"
NAMA = "Content Producer"
DIVISI = "Produksi"
ATASAN = "A08"
JOB_DESC = "Mengubah produk dan riset menjadi materi konten"
DIPETAKAN_KE = "A5 Produksi + A3"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 2 — Creative Studio"
GEMINI_PERAN = "2A/2B + Divisi 3 (content producer)"
GEMINI_KPI = ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', '1 produk → 7 format konten (strategi rancangan)']
GEMINI_TOOLS = ['Gemini / ChatGPT', 'CapCut']


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

def buat_paket_konten(produk, kanal, pakai_ai=False):
    """Draf paket konten: 1 produk → 7 format (strategi Gemini Divisi 3).
    Hook 3 detik pertama, CTA ke toko."""
    draf = _draf_dasar("paket_konten", "Paket konten: {}".format((produk or "").strip() or "?"))
    draf["produk"] = (produk or "").strip()
    draf["kanal"] = list(kanal or ["Instagram", "TikTok", "YouTube", "Threads"])
    draf["format_7"] = ["Reels IG", "Video TikTok", "Shorts YT", "Post Threads",
                        "Foto/carousel", "Story", "Artikel/landing page"]
    draf["hook_draf"] = "[Hook 3 detik pertama — kaitkan dengan masalah pelanggan]"
    draf["cta"] = "Lihat katalog: https://podcastmeong.github.io/ — beli via KaryaKarsa / Lynk.id."
    draf["target_rancangan_gemini"] = GEMINI_KPI
    versi_ai = _polish("Paket konten untuk {}.".format(draf["produk"]), pakai_ai)
    if versi_ai:
        draf["versi_ai"] = versi_ai
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return buat_paket_konten("eBook Kolam Ikan", ["Instagram", "TikTok"])


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
