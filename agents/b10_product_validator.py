"""BINTANG COMMAND CENTER — Agent A10 Product Validator.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Menguji manfaat, kelayakan, permintaan dan kesiapan produk
Divisi: Riset · Atasan: A08
Dipetakan ke (sistem kita): A9F verifikasi + Muse
Pemetaan Gemini #1: Divisi 1 — R&D — 1A — Market Researcher (validasi)
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

KODE = "A10"
NAMA = "Product Validator"
DIVISI = "Riset"
ATASAN = "A08"
JOB_DESC = "Menguji manfaat, kelayakan, permintaan dan kesiapan produk"
DIPETAKAN_KE = "A9F verifikasi + Muse"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 1 — R&D"
GEMINI_PERAN = "1A — Market Researcher (validasi)"
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

def cek_kelayakan_produk(konsep):
    """Nilai kelayakan konsep produk: 6 syarat wajib (Share #18), tiap syarat terisi = 2 poin, skor maks 12.
    'belum cukup data' dihitung KOSONG — bukan terisi."""
    draf = _draf_dasar("cek_kelayakan", "Kelayakan produk: {}".format((konsep or {}).get("nama", "?")))
    syarat = [("masalah_customer", "Masalah pelanggan yang diselesaikan"),
              ("target_customer", "Target pembeli yang jelas"),
              ("keunikan", "Keunikan dibandingkan produk pesaing"),
              ("harga_rp", "Perkiraan harga dan biaya"),
              ("bukti_minat_pasar", "Bukti minat pasar"),
              ("rencana_promosi_distribusi", "Rencana promosi dan distribusi")]
    detail = {}
    skor = 0
    for kunci, label in syarat:
        nilai = (konsep or {}).get(kunci)
        terisi = bool(nilai) and str(nilai).strip() not in ("", "belum cukup data")
        detail[label] = "terisi" if terisi else "kosong"
        skor += 2 if terisi else 0
    draf["skor"] = skor
    draf["skor_maks"] = 12
    draf["detail"] = detail
    draf["verdict"] = ("LAYAK (draf — teruskan ke produksi)" if skor >= 10
                       else ("PERLU DILENGKAPI" if skor >= 6 else "BELUM LAYAK"))
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return cek_kelayakan_produk({"nama": "eBook Resep Kucing", "masalah_customer": "x", "target_customer": "y", "keunikan": "z", "harga_rp": 29000, "bukti_minat_pasar": "belum cukup data", "rencana_promosi_distribusi": "TikTok"})


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
