"""BINTANG COMMAND CENTER — Agent A26 Customer Service.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Menjawab pertanyaan, komentar dan keluhan pelanggan
Divisi: Penjualan · Atasan: A25
Dipetakan ke (sistem kita): A1 + A13 (WA Web rusak; IG/Threads Messages terhubung)
Pemetaan Gemini #1: Divisi 4 — CS & Closer — 4 — Omnichannel CS & Closer
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

KODE = "A26"
NAMA = "Customer Service"
DIVISI = "Penjualan"
ATASAN = "A25"
JOB_DESC = "Menjawab pertanyaan, komentar dan keluhan pelanggan"
DIPETAKAN_KE = "A1 + A13 (WA Web rusak; IG/Threads Messages terhubung)"
STATUS = "Aktif"
GEMINI_DIVISI = "Divisi 4 — CS & Closer"
GEMINI_PERAN = "4 — Omnichannel CS & Closer"
GEMINI_KPI = ['Respons < 1 jam (target rancangan)']
GEMINI_TOOLS = []


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

def buat_draf_balasan(pesan, topik="harga"):
    """Draf balasan customer: jawab dari info yang sudah disetujui (harga jasa, eBook Rp29.000,
    pemesanan via WA/website). Negosiasi/custom/pembayaran/keluhan DITERUSKAN ke Cipta — jangan dijawab sendiri."""
    topik = (topik or "harga").strip().lower()
    jawaban = {
        "harga": "Harga jasa video promo: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000 (DP min 50%). "
                 "eBook Rp29.000. Aplikasi mulai Rp499.000. Detail: https://podcastmeong.github.io/",
        "cara_beli": "Pemesanan via WhatsApp atau website https://podcastmeong.github.io/ — "
                     "eBook juga tersedia di KaryaKarsa dan Lynk.id.",
        "cara_pakai": "Aplikasi kami file HTML tunggal: buka di browser HP/laptop, bisa 'Tambah ke Layar Utama'. "
                      "Data tersimpan per perangkat, bisa offline.",
    }
    draf = _draf_dasar("draf_balasan", "Draf balasan CS — topik: {}".format(topik))
    draf["pesan_customer"] = (pesan or "").strip()
    draf["topik"] = topik
    if topik in jawaban:
        draf["balasan_draf"] = jawaban[topik]
        draf["tindakan"] = "Jawab dengan draf di atas (setelah Cipta setuju bila ini balasan keluar)."
    else:
        draf["balasan_draf"] = ""
        draf["tindakan"] = "TERUSKAN ke Cipta — topik di luar info yang sudah disetujui (negosiasi/custom/pembayaran/keluhan)."
    draf["target_rancangan_gemini"] = GEMINI_KPI
    return draf

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return buat_draf_balasan("Berapa harga video promonya?", "harga")


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
