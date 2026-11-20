"""BINTANG COMMAND CENTER — Agent A05 Business Analyst.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Menganalisis KPI, hasil, risiko dan profitabilitas
Divisi: Direksi · Atasan: A02
Dipetakan ke (sistem kita): A7 Keuangan + Muse
Pemetaan Gemini #1: Divisi 5 — Freelance & Finance — 5B — Finance & Operational Controller (analisis)
Status nyata: Aktif

KEJUJURAN WAJIB — BACA DULU:
- Agent ini PASIF: dijalankan Muse, BUKAN layanan otonom 24 jam.
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

KODE = "A05"
NAMA = "Business Analyst"
DIVISI = "Direksi"
ATASAN = "A02"
JOB_DESC = "Menganalisis KPI, hasil, risiko dan profitabilitas"
DIPETAKAN_KE = "A7 Keuangan + Muse"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 5 — Freelance & Finance"
GEMINI_PERAN = "5B — Finance & Operational Controller (analisis)"
GEMINI_KPI = ['Laporan pembukuan harian/mingguan (target rancangan)']
GEMINI_TOOLS = ['Google Sheets', 'Notion']


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
    d["catatan"] = ("Agent pasif — dijalankan Muse, bukan layanan otonom 24 jam. "
                    "Semua output DRAF untuk persetujuan Cipta.")
    return d

def _angka(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def hitung_laba(pendapatan, pengeluaran):
    """Laba Bersih = Total Pendapatan − Total Pengeluaran (rumus Share #18). Angka dari masukan; bukan janji."""
    p = _angka(pendapatan)
    b = _angka(pengeluaran)
    draf = _draf_dasar("hitung_laba", "Laba bersih — {}".format(date.today().isoformat()))
    draf["pendapatan"] = p
    draf["pengeluaran"] = b
    draf["laba_bersih"] = p - b
    draf["rumus"] = "Laba Bersih = Total Pendapatan − Total Pengeluaran"
    return draf


def analisis_kpi(data):
    """Bandingkan angka KPI lama vs baru dari masukan (dict {nama: (lama, baru)})."""
    draf = _draf_dasar("analisis_kpi", "Analisis KPI — {}".format(date.today().isoformat()))
    hasil = {}
    for nama, pasangan in (data or {}).items():
        try:
            lama, baru = float(pasangan[0]), float(pasangan[1])
            hasil[nama] = {"lama": lama, "baru": baru, "delta": baru - lama}
        except (TypeError, ValueError, IndexError):
            hasil[nama] = {"lama": "belum cukup data", "baru": "belum cukup data",
                           "delta": "belum cukup data"}
    draf["kpi"] = hasil
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return hitung_laba(29000, 0)


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
