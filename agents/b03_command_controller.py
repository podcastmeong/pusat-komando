"""BINTANG COMMAND CENTER — Agent A03 Command Controller.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Membagi tugas, melacak status dan mengonsolidasikan laporan
Divisi: Direksi · Atasan: A02
Dipetakan ke (sistem kita): Pusat Komando (Faable) + koordinasi.py
Pemetaan Gemini #1: Agent 0 — Chief Orchestrator — 0 — Chief Orchestrator (pembagian tugas)
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

KODE = "A03"
NAMA = "Command Controller"
DIVISI = "Direksi"
ATASAN = "A02"
JOB_DESC = "Membagi tugas, melacak status dan mengonsolidasikan laporan"
DIPETAKAN_KE = "Pusat Komando (Faable) + koordinasi.py"
STATUS = "Aktif"
GEMINI_DIVISI = "Agent 0 — Chief Orchestrator"
GEMINI_PERAN = "0 — Chief Orchestrator (pembagian tugas)"
GEMINI_KPI = ['Semua agen aktif setiap hari (target rancangan)', 'Laporan harian tepat waktu (target rancangan)']
GEMINI_TOOLS = ['Gemini Advanced / ChatGPT', 'Notion', 'Google Sheets']
JADWAL_HARIAN = {'sumber': 'Share Gemini #1 — Alur Kerja Harian (Standard Operating Procedure)', 'catatan_jujur': 'Jadwal referensi dari rancangan Gemini. Bukan jadwal otomatis — agent bersifat pasif; Muse yang menjalankan.', 'jadwal': [{'jam': '06.00', 'kegiatan': 'Riset & Lomba', 'agent': '1A & 1B (A06, A07, A09, A10)', 'output': '5 tren produk harian, 3 info lomba terbaru, 2 peluang freelance'}, {'jam': '08.00', 'kegiatan': 'Produksi', 'agent': '2A, 2B & 2C (A11–A19)', 'output': '1 aset utama (1 bab cerbung / 1 desain POD / 1 aplikasi web sederhana)'}, {'jam': '11.00, 15.00, 19.00', 'kegiatan': 'Distribusi', 'agent': 'Agent 3 (A20–A24)', 'output': 'Publikasi konten ke 2 IG, 2 TikTok, 2 YouTube, 1 Threads dengan CTA ke Lynk.id'}, {'jam': 'Sepanjang hari', 'kegiatan': 'CS & Closing', 'agent': 'Agent 4 (A25–A27)', 'output': 'Balas email, komentar, dan DM penawaran ke calon pembeli (DRAF — kirim setelah Cipta setuju)'}, {'jam': '21.00', 'kegiatan': 'Audit Keuangan & Operasional', 'agent': '5B (A29)', 'output': 'Rekap mutasi BCA, PayPal, Saweria, Trakteer, KaryaKarsa, Lynk.id; laporan saldo harian'}]}

RENCANA_30_HARI = {'sumber': "Share Gemini #1 — 'Checklist Sistem 30 Hari'", 'catatan_jujur': 'Bagian ini hanya tampil pada pemuatan pertama share Gemini dan hilang setelah muat ulang. Isinya dicatat dari pemuatan pertama. Target di bawah ini adalah TARGET RANCANGAN, bukan hasil nyata dan bukan janji.', 'fase': [{'hari': '1–3', 'nama': 'Setup Sistem', 'isi': 'Buat akun di semua tools gratis (n8n/CrewAI, Google AI Studio, Notion, Google Sheets); salin Master System Prompt ke Gemini Custom (Gem) atau AI Studio; siapkan 1 folder Google Drive untuk semua aset produk.'}, {'hari': '4–7', 'nama': 'Produksi Awal', 'isi': 'Produksi 3 E-book/Cerbung, 5 desain POD, dan 3 video AI; daftarkan produk di KaryaKarsa, Lynk.id, KBM, dan Zazzle.'}, {'hari': '8–14', 'nama': 'Distribusi Massal', 'isi': 'Posting 3–5 konten per hari ke semua 7 akun sosmed; mulai kirim 5 proposal freelance per hari di Upwork/Fiverr (DRAF — kirim hanya setelah Cipta setuju).'}, {'hari': '15–21', 'nama': 'Optimasi & Penjualan', 'isi': 'Fokus pada CS & Direct Sales (balas semua DM/komentar); ikuti 5 lomba pertama.'}, {'hari': '22–30', 'nama': 'Skala & Evaluasi', 'isi': 'Evaluasi produk terlaris, buat lebih banyak varian, dan tingkatkan frekuensi posting untuk produk yang viral.'}], 'target_30_hari': {'produk_digital_selesai': 15, 'konten_terbit': 30, 'followers_baru': 1000, 'lomba_diikuti': '5–10', 'pemasukan_pertama_rp': '500.000–2.000.000'}}

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

KODE_30 = ["A%02d" % i for i in range(1, 31)]


def bagi_tugas(tugas, penanggung_jawab):
    """Bagi satu tugas ke agent A01–A30. Kode penanggung jawab harus valid;
    bila tidak, kembalikan draf dengan masalah."""
    draf = _draf_dasar("pembagian_tugas", "Pembagian tugas — {}".format((tugas or "").strip() or "?"))
    kode = (penanggung_jawab or "").strip().upper()
    if kode not in KODE_30:
        draf["masalah"] = "Kode agent tidak dikenal: '{}'. Kode yang benar: A01–A30.".format(penanggung_jawab)
        draf["tugas"] = (tugas or "").strip()
        return draf
    draf["tugas"] = (tugas or "").strip()
    draf["penanggung_jawab"] = kode
    draf["status_tugas"] = "Backlog"
    return draf


def lacak_status(daftar_tugas):
    """Hitung tugas per status (Backlog/Siap/Dikerjakan/Menunggu Persetujuan/QC/Selesai/Tertunda)."""
    draf = _draf_dasar("lacak_status", "Lacak status tugas — {}".format(date.today().isoformat()))
    hitung = {}
    for t in (daftar_tugas or []):
        s = t.get("status", "?") if isinstance(t, dict) else "?"
        hitung[s] = hitung.get(s, 0) + 1
    draf["per_status"] = hitung
    draf["total"] = len(daftar_tugas or [])
    return draf


def jadwal_harian():
    """Jadwal harian referensi (Share Gemini #1). Bukan jadwal otomatis."""
    return dict(JADWAL_HARIAN)


def rencana_30_hari():
    """Rencana tahap 30 hari (Share Gemini #1). Target di dalamnya TARGET RANCANGAN, bukan hasil nyata."""
    return dict(RENCANA_30_HARI)

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return bagi_tugas("Buat draf proposal Upwork", "A28")


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
