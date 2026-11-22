"""BINTANG COMMAND CENTER — Agent A01 CEO Director.
Rancangan: Share ChatGPT #18 ("SISTEM KOMANDO AGENT.AI") + Share #19
("PEMBANGUNAN BINTANG COMMAND CENTER") + Share Gemini #1 ("Sistem Agent
AI Bisnis Gratis"). Dibuat 21 Nov 2026 atas perintah Cipta ("Buat 30
agent" + "Biar sesuai" + "Amati Tiru dari chatgpt Dan gemini").

Job description (ChatGPT #18): Menentukan arah, target, prioritas dan keputusan perusahaan
Divisi: Direksi · Atasan: Pemilik
Dipetakan ke (sistem kita): Muse (koordinator / CEO)
Pemetaan Gemini #1: Agent 0 — Chief Orchestrator — 0 — Chief Orchestrator
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

KODE = "A01"
NAMA = "CEO Director"
DIVISI = "Direksi"
ATASAN = "Pemilik"
JOB_DESC = "Menentukan arah, target, prioritas dan keputusan perusahaan"
DIPETAKAN_KE = "Muse (koordinator / CEO)"
STATUS = "Aktif"
GEMINI_DIVISI = "Agent 0 — Chief Orchestrator"
GEMINI_PERAN = "0 — Chief Orchestrator"
GEMINI_KPI = ['Semua agen aktif setiap hari (target rancangan)', '1 produk baru dirilis setiap hari (target rancangan)', 'Laporan harian tepat waktu (target rancangan)']
GEMINI_TOOLS = ['Gemini Advanced / ChatGPT', 'Notion', 'Google Sheets']
MASTER_PROMPT_GEMINI = 'Anda adalah CHIEF ORCHESTRATOR dari ekosistem bisnis digital otomatis dengan anggaran Rp 0. Tugas Anda adalah mengoordinasikan 5 divisi AI Agent (R&D/Lomba, Creative Studio, Social Media Growth, CS/Direct Sales, dan Freelance/Finance) untuk mengelola: - Akun Sosmed: 2 Instagram, 2 TikTok, 2 YouTube, 1 Threads, 1 Website/Toko. - Platform Monetisasi Aktif: KaryaKarsa, Lynk.id, Zazzle, KBM, Saweria, Trakteer, PayPal, BCA, Adobe Stock, Dreamstime, Impact.com, GitHub Pages, Faable, DeployVera. (Catatan: Mayar masih proses KYC, arahkan transaksi ke platform aktif). - Jenis Produk: Video AI, Foto AI, Aplikasi/Web, Game, POD, E-Book, Puisi, Cerpen, Cerita Bersambung. Setiap kali saya memberikan perintah atau meminta laporan harian, Anda wajib membagi output menjadi bagian terstruktur berdasarkan divisi yang relevan, memberikan langkah eksekusi konkret tanpa biaya (gratis), serta menyertakan draf siap pakai (kode, naskah, prompt visual, atau copywriting penawaran langsung) yang langsung mengarah pada konversi penjualan dan pertumbuhan audiens.'

CATATAN_GEMINI_DIVISI = "Catatan jujur: Gemini menyebut '6 Divisi Agen Spesialis', padahal diagram dan isi jawabannya hanya memuat 5 divisi + Agent 0 sebagai komandan. Pemetaan ini memakai isi sebenarnya (5 divisi + Agent 0)."

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
    d["catatan"] = ("Agent pasif — dijalankan Muse, kerja 24 jam nonstop lewat pemicu jadwal (cron) + Muse sebagai pemimpin tim; bukan layanan otonom mandiri. "
                    "Semua output DRAF untuk persetujuan Cipta.")
    return d

def buat_arahan(tugas, pakai_ai=False):
    """Draf arahan harian CEO: prioritas + pembagian tugas + keputusan yang butuh persetujuan Cipta."""
    daftar = [t for t in (tugas or []) if isinstance(t, dict)]
    urut = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
    prioritas = sorted(daftar, key=lambda t: urut.get(str(t.get("prioritas", "P3")), 2))
    draf = _draf_dasar("arahan_harian", "Arahan harian CEO — {}".format(date.today().isoformat()))
    draf["prioritas"] = [{"judul": t.get("judul", "?"), "prioritas": t.get("prioritas", "P3"),
                          "penanggung_jawab": t.get("penanggung_jawab", "belum ditentukan"),
                          "status": t.get("status", "Backlog")} for t in prioritas]
    draf["keputusan_butuh_persetujuan"] = [
        "Mengirim uang, membeli layanan, menandatangani kontrak, mengirim proposal resmi, "
        "mengirim email penting, menerbitkan konten sensitif, menghapus data, mengubah keamanan akun, "
        "membuat komitmen kepada pelanggan — semua wajib persetujuan Cipta (aturan hybrid)."]
    draf["target_rancangan_gemini"] = GEMINI_KPI
    draf["instruksi_orchestrator_referensi"] = "Lihat MASTER_PROMPT_GEMINI di modul ini (referensi Share Gemini #1)."
    teks = "; ".join(p["judul"] for p in draf["prioritas"])
    versi_ai = _polish(teks, pakai_ai)
    if versi_ai:
        draf["versi_ai"] = versi_ai
    return draf


def buat_laporan_kondisi(masukan):
    """Kerangka laporan perusahaan 9 bagian (format pelaporan CEO, Share #19).
    Semua bagian diisi dari masukan; yang tidak ada ditulis 'belum cukup data'."""
    bagian = ["Kondisi perusahaan", "Pekerjaan selesai", "Pekerjaan berlangsung",
              "Pekerjaan tertunda", "Hasil penjualan", "Peluang baru", "Masalah",
              "Keputusan yang dibutuhkan", "Rencana selanjutnya"]
    draf = _draf_dasar("laporan_kondisi", "Laporan kondisi perusahaan — {}".format(date.today().isoformat()))
    data = masukan or {}
    draf["bagian"] = {b: data.get(b, "belum cukup data") for b in bagian}
    return draf


def rencana_30_hari():
    """Rencana tahap 30 hari (Share Gemini #1). Target di dalamnya TARGET RANCANGAN, bukan hasil nyata."""
    return dict(RENCANA_30_HARI)

def contoh():
    """Contoh hasil fungsi inti (untuk tes + tab Pusat Komando)."""
    return buat_arahan([{"judul": "Selesaikan halaman demo #18", "prioritas": "P2", "penanggung_jawab": "A14", "status": "Dikerjakan"}])


if __name__ == "__main__":
    import sys
    print("Agent {} — {} | mode: {}".format(KODE, NAMA, mode_ai()))
    print("Dipetakan ke:", DIPETAKAN_KE, "| Status:", STATUS)
    print("Contoh draf:", json.dumps(contoh(), ensure_ascii=False)[:300])
    sys.exit(0)
