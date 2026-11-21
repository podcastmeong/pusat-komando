# ======================================================================
# BINTANG COMMAND CENTER — Mesin Eksekusi 30 Agent Bintang.
# Dibuat 21 Nov 2026 atas perintah Cipta ("Bangun mesin eksekusi").
# Pusat Komando v2.0: 30 Agent Bintang + mesin ini + 14 mesin lama pasif.
#
# CARA KERJA (baca dulu — kejujuran wajib):
# - Mesin ini menjalankan 30 Agent Bintang SAJA (A01–A30). Titik jalan:
#   FUNGSI INTI tiap modul b01–b30 (bukan sekadar contoh()) — setiap
#   eksekusi memanggil fungsi kerja nyata sesuai job description agent
#   (mis. A06 buat_brief_riset, A11 buat_naskah_video, A25
#   buat_draf_penawaran, A28 nilai_peluang_draf), dengan argumen dari
#   tugas antrean. Bila tugas tidak membawa argumen yang cukup, mesin
#   memanggil contoh() modul itu dan MENCATAT mode="contoh" di log —
#   tidak pernah mengaku sudah mengerjakan isi tugas.
# - 14 agent lama (a01–a14) TIDAK dihapus: modul + data tetap utuh
#   sebagai MESIN (engine/pustaka) yang dipakai modul Bintang
#   (mis. b25 → a04.draf_personal). Mereka pasif non-job: tidak lagi
#   punya pekerjaan/tugas sendiri.
# - STRATEGI SESUAI ChatGPT + Gemini (perintah Cipta 04:39):
#   jadwal harian mengikuti alur Gemini #1 (06:00 riset, 08:00 produksi,
#   11/15/19 distribusi, CS sepanjang hari, 21:00 audit) dalam bingkai
#   06:00–21:00 ChatGPT #18; KPI/target per agent memakai gemini_kpi
#   yang SUDAH ADA di data/agents.json (tidak ada KPI ChatGPT per-agent
#   di agents.json — lihat KONFLIK di bawah); target 30 hari Gemini
#   (15 produk, 30 konten, 1000 followers baru, 5–10 lomba,
#   Rp500rb–Rp2jt) jadi tolok ukur dashboard.
# - KONFLIK ChatGPT vs Gemini yang ditemukan (diutamakan yang tercatat
#   di agents.json):
#   (1) Jadwal rinci 12 baris ChatGPT #18 (06:00–21:00) TIDAK tercatat
#       di agents.json — mesin memakai 5 slot alur Gemini #1 (dari
#       b03.jadwal_harian()) dalam bingkai 06:00–21:00.
#   (2) KPI ChatGPT per-agent TIDAK tercatat di agents.json (hanya
#       gemini_kpi per agent) — mesin memakai gemini_kpi sebagai target.
#   (3) Gemini bilang "6 divisi" tapi isinya 5 divisi + Agent 0 —
#       dipakai yang nyata: 5 divisi + Agent 0 (sudah dicatat 21 Nov).
# - PLATFORM (perintah Cipta 04:41): tiap agent Bintang memegang daftar
#   platform di data/agents.json (key "platform": terhubung +
#   belum_terhubung). Platform yang belum terhubung TIDAK PERNAH
#   dipakai seolah terhubung.
# - KENDALA HARUS DIINFOKAN (perintah Cipta 04:41): pekerjaan yang
#   tidak bisa jalan (platform belum terhubung, data tidak ada, butuh
#   login/keputusan Cipta, error) mendapat status "terkendala" di
#   antrean + audit log, lengkap dengan penyebab dan apa yang
#   dibutuhkan dari Cipta. Tidak diam-diam dilewati, tidak ditebak.
#
# ATURAN KERAS (SOP Kerja Sama Agent AI, berlaku 18 Nov 2026):
# - Semua output adalah DRAF untuk persetujuan Cipta.
# - Mesin TIDAK PERNAH mengirim, membayar, mempublikasi, submit, atau
#   upload apa pun. Tidak ada fungsi kirim/bayar di modul ini.
# - Dilarang mengarang data pasar, angka, atau janji. Bila data kurang,
#   tulis "belum cukup data" / "—".
# - Mode Hybrid + anggaran Rp0. Mesin hanya jalan saat dipicu (tombol
#   "Jalankan" di Dashboard / CLI) — BUKAN layanan otonom 24 jam.
# ======================================================================
import importlib
import inspect
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
AGENTS_DIR = Path(__file__).resolve().parent
if str(AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTS_DIR))

VERSI_MESIN = "1.0"
WIB = timezone(timedelta(hours=7))
LOG_MESIN_NAMA = "mesin_eksekusi_log.json"
LOG_AKTIVITAS_NAMA = "activity_log.json"
MAKS_LOG = 500

STATUS_ANTREAN = ("menunggu", "diproses", "menunggu persetujuan",
                  "selesai", "terkendala")
PRIORITAS_URUTAN = {"tinggi": 0, "normal": 1, "rendah": 2}

# Handoff jenis -> agent Bintang (dipakai bila jenisnya spesifik).
RUTE_JENIS = {
    "product-brief": "A08",
    "draft-approval": "A04",
    "sales-lead": "A25",
    "contest-entry": "A28",
    "finance-entry": "A29",
    "translation-job": "A17",
    "game-pipeline": "A13",
}
# Handoff ke_agent "Agent N" (mesin lama) -> agent Bintang yang memakai
# mesin itu. Dipakai untuk jenis umum ("penugasan", "lainnya").
RUTE_MESIN_KE_BINTANG = {
    "1": "A26", "2": "A25", "3": "A24", "4": "A25", "5": "A19",
    "6": "A28", "7": "A29", "8": "A17", "9": "A13", "10": "A06",
    "11": "A11", "12": "A11", "13": "A27", "14": "A28",
}

# Platform belum terhubung (dari daftar terverifikasi 21 Nov 2026) +
# kata kunci aksi yang menandakan tugas butuh platform itu, bukan draf.
# Dipakai tentukan_kendala(): hanya bila teks tugas menyebut platform
# DAN aksi yang butuh platform tersebut.
KENDALA_PLATFORM = [
    (("upwork",), ("kirim", "daftar", "lamar", "buka", "buat akun"),
     "Upwork (belum ada akun)",
     "Cipta klik Cloudflare 'Verify you are human' lalu buat akun Upwork."),
    (("gmail",), ("kirim", "cek", "buka", "balas", "login"),
     "Gmail (tidak terhubung)",
     "Hubungkan Gmail, atau setujui kerja via browser (baca email di browser)."),
    (("mayar",), ("bayar", "kirim", "buka", "checkout", "terima"),
     "Mayar (KYC belum selesai)",
     "Selesaikan KYC Mayar dulu; sampai saat itu pembayaran hanya via BCA / PayPal / KaryaKarsa / Lynk.id / Saweria / Trakteer."),
    (("@meongcast", "tiktok"), ("posting", "upload", "kirim", "login", "masuk"),
     "TikTok @meongcast (butuh login Cipta)",
     "Cipta login sendiri ke TikTok @meongcast di HP-nya."),
    (("@meongcast", "youtube", "yt"), ("posting", "upload", "kirim", "login", "masuk"),
     "YouTube @meongcast (tertahan verifikasi)",
     "Cipta ketuk 'Ya' di notifikasi Google di HP-nya, atau beri kata sandi yang benar via Secure Vault."),
    (("podcast_meong", "instagram"), ("posting", "upload", "kirim", "login", "masuk"),
     "Instagram @podcast_meong (login ditolak)",
     "Cipta perbaiki login Instagram @podcast_meong dulu."),
]
KATA_AKSI_PLATFORM = ("kirim", "posting", "upload", "login", "masuk",
                      "cek inbox", "buka", "tautkan", "hubungkan", "daftar")


def _waktu_sekarang():
    return datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")


def _baca_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, type(default)) else default
    except (OSError, ValueError):
        return default


def _tulis_json_atomik(path, data):
    """Tulis JSON lewat file sementara + ganti atomik (anti korup)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _log_activity(kode, aksi, hasil, detail="", base=None):
    """Cerminan dashboard.log_activity (modul ini tidak mengimpor
    dashboard — supaya mesin tetap berdiri sendiri). Diam bila gagal;
    tidak menulis apa pun bila env PK_NO_LOG disetel (dipakai saat tes)."""
    if os.environ.get("PK_NO_LOG"):
        return False
    folder = Path(base) if base else DATA_DIR
    path = folder / LOG_AKTIVITAS_NAMA
    try:
        folder.mkdir(parents=True, exist_ok=True)
        log = _baca_json(path, [])
        log.append({"waktu": _waktu_sekarang()[:16],
                    "kode_agent": str(kode),
                    "aksi": str(aksi), "hasil": str(hasil),
                    "detail": str(detail or "")})
        _tulis_json_atomik(path, log[-MAKS_LOG:])
        return True
    except Exception:  # noqa: BLE001 — log tidak boleh mematikan pemanggil
        return False


# ---------------------------------------------------------------------------
# Daftar agent Bintang (dari data/agents.json — jangan karang)
# ---------------------------------------------------------------------------
def daftar_agent_bintang(base=None):
    """30 agent Bintang A01–A30 beserta metadata + platform + target."""
    folder = Path(base) if base else DATA_DIR
    data = _baca_json(folder / "agents.json", {})
    return (data.get("agent_30") or {}).get("agents", [])


def info_agent(kode, base=None):
    for e in daftar_agent_bintang(base):
        if e.get("code") == kode:
            return e
    return None


def muat_modul_bintang(kode, base=None):
    """Impor modul bXX agent. Kembalikan (modul, pesan_error)."""
    entri = info_agent(kode, base)
    if entri is None:
        return None, "Agent {} tidak ada di data/agents.json.".format(kode)
    nama_file = (entri.get("file", "") or "").replace("agents/", "")
    nama_file = nama_file.replace(".py", "")
    if not nama_file:
        return None, "Agent {} tidak punya nama file modul.".format(kode)
    try:
        return importlib.import_module(nama_file), None
    except Exception as e:  # noqa: BLE001
        return None, "{}: {}".format(type(e).__name__, e)


# ---------------------------------------------------------------------------
# Jadwal harian mesin — SIKLUS SOP (9 tahap, 07:00–16:30) sejak keputusan
# Cipta 21 Nov 2026 ("Mesin ikut SOP" / "Mesin ikut siklus SOP").
# Sumber tunggal: sop_harian.siklus_harian di agents.json. Jadwal Gemini #1
# (b03.jadwal_harian + salinan darurat di bawah) hanya fallback bila SOP
# belum ada di data.
# ---------------------------------------------------------------------------
_JADWAL_DARURAT = [
    {"jam": "06.00", "kegiatan": "Riset & Lomba",
     "agent": "1A & 1B (A06, A07, A09, A10)",
     "output": "5 tren produk harian, 3 info lomba terbaru, 2 peluang freelance"},
    {"jam": "08.00", "kegiatan": "Produksi",
     "agent": "2A, 2B & 2C (A11–A19)",
     "output": "1 aset utama (1 bab cerbung / 1 desain POD / 1 aplikasi web sederhana)"},
    {"jam": "11.00, 15.00, 19.00", "kegiatan": "Distribusi",
     "agent": "Agent 3 (A20–A24)",
     "output": "Publikasi konten ke 2 IG, 2 TikTok, 2 YouTube, 1 Threads dengan CTA ke Lynk.id"},
    {"jam": "Sepanjang hari", "kegiatan": "CS & Closing",
     "agent": "Agent 4 (A25–A27)",
     "output": "Balas email, komentar, dan DM penawaran ke calon pembeli (DRAF — kirim setelah Cipta setuju)"},
    {"jam": "21.00", "kegiatan": "Audit Keuangan & Operasional",
     "agent": "5B (A29)",
     "output": "Rekap mutasi BCA, PayPal, Saweria, Trakteer, KaryaKarsa, Lynk.id; laporan saldo harian"},
]
# Tambahan atas pemetaan Gemini (dicatat jujur, bukan dari share):
# - Slot 06.00: A28 (Opportunity Hunter) ikut — output slot menyebut
#   "2 peluang freelance", dan A28-lah pemburu peluang/freelance.
# - Slot 21.00: A05 (Business Analyst) ikut — audit butuh analisis KPI.
_TAMBAHAN_SLOT = {"06.00": ["A28"], "21.00": ["A05"]}


def _kode_dari_teks(teks):
    """Ambil kode agent A01–A30 dari teks (termasuk rentang A11–A19,
    dengan '-' atau '–')."""
    import re
    kode = []
    for m in re.finditer(r"A(\d{2})\s*[–-]\s*A(\d{2})", teks or ""):
        a, b = int(m.group(1)), int(m.group(2))
        kode.extend("A%02d" % i for i in range(min(a, b), max(a, b) + 1))
    for m in re.finditer(r"A(\d{2})", teks or ""):
        k = "A" + m.group(1)
        if k not in kode:
            kode.append(k)
    return sorted(set(kode))


def _rentang_jam(teks):
    """'07.00–07.20' -> (420, 440) menit. Bukan rentang -> None."""
    import re
    m = re.match(r"(\d{1,2})\.(\d{2})\s*[–-]\s*(\d{1,2})\.(\d{2})$",
                 (teks or "").strip())
    if not m:
        return None
    return (int(m.group(1)) * 60 + int(m.group(2)),
            int(m.group(3)) * 60 + int(m.group(4)))


def jadwal_harian_mesin(base=None):
    """Siklus harian SOP (9 tahap, 07:00–16:30) — keputusan Cipta
    21 Nov 2026: mesin ikut SOP. Sumber: sop_harian.siklus_harian di
    agents.json. Bila SOP belum ada, fallback ke 5 slot Gemini #1
    (b03.jadwal_harian, lalu salinan darurat).
    Tiap slot: jam, kegiatan, agent (kode Bintang), output."""
    folder = Path(base) if base else DATA_DIR
    sop = (_baca_json(folder / "agents.json", {}).get("sop_harian") or {})
    siklus = sop.get("siklus_harian") or []
    if siklus:
        slot = []
        for s in siklus:
            slot.append({"jam": s.get("jam", "?"),
                         "kegiatan": s.get("tahap", "?"),
                         "agent": _kode_dari_teks(s.get("penanggung_jawab", "")),
                         "agent_teks": s.get("penanggung_jawab", ""),
                         "output": s.get("hasil_wajib", "")})
        return {"sumber": ("SOP Harian 30 Agent Bintang (keputusan Cipta "
                           "21 Nov 2026 — mesin ikut SOP)"),
                "bingkai": "07:00–16:30 (SOP)",
                "catatan": ("Jadwal referensi — BUKAN jadwal otomatis. Agent pasif; "
                            "mesin hanya jalan saat dipicu (tombol/CLI). "
                            "Di luar 07:00–16:30 tidak ada tahap SOP."),
                "slot": slot}
    try:
        b03, _err = muat_modul_bintang("A03", base)
        data = b03.jadwal_harian() if b03 is not None else None
        jadwal = (data or {}).get("jadwal") or []
        sumber = (data or {}).get("sumber", "")
        if not jadwal:
            raise ValueError("jadwal kosong")
    except Exception:  # noqa: BLE001 — fallback darurat
        jadwal = _JADWAL_DARURAT
        sumber = ("Salinan darurat (b03.jadwal_harian tidak bisa dimuat) — "
                  "isi sama dengan Share Gemini #1")
    slot = []
    for s in jadwal:
        jam = s.get("jam", "?")
        kode = _kode_dari_teks(s.get("agent", ""))
        for t in _TAMBAHAN_SLOT.get(jam, []):
            if t not in kode:
                kode.append(t)
        slot.append({"jam": jam, "kegiatan": s.get("kegiatan", "?"),
                     "agent": sorted(kode),
                     "agent_teks": s.get("agent", ""),
                     "output": s.get("output", "")})
    return {"sumber": sumber,
            "bingkai": "06:00–21:00 (ChatGPT #18)",
            "catatan": ("Jadwal referensi — BUKAN jadwal otomatis. Agent pasif; "
                        "mesin hanya jalan saat dipicu (tombol/CLI)."),
            "slot": slot}


def slot_untuk_jam(jam=None):
    """Slot yang berlaku untuk satu jam (0–23 WIB). Tanpa argumen:
    jam sekarang WIB. Siklus SOP: tahap yang rentang jamnya memuat
    jam itu; di luar 07:00–16:30 (mis. istirahat 12:00–13:00, malam)
    tidak ada tahap -> None. Jadwal Gemini lama (fallback) memakai
    pemetaan jam tetap."""
    if jam is None:
        jam = datetime.now(WIB).hour
    jadwal = jadwal_harian_mesin()
    slot = jadwal["slot"]
    if not slot:
        return None
    menit = jam * 60
    for s in slot:
        rentang = _rentang_jam(s.get("jam", ""))
        if rentang and rentang[0] <= menit < rentang[1]:
            return s
    if any(_rentang_jam(s.get("jam", "")) for s in slot):
        return None  # jadwal SOP, jam di luar tahap mana pun
    if jam in (6, 7):
        return slot[0]
    if jam in (8, 9, 10):
        return slot[1]
    if jam in (11, 15, 19):
        return slot[2]
    if jam in (21, 22):
        return slot[4]
    return slot[3]  # CS & Closing sepanjang hari


# ---------------------------------------------------------------------------
# Target 30 hari Gemini (tolok ukur dashboard) — dari b01.rencana_30_hari()
# ---------------------------------------------------------------------------
def target_30_hari(base=None):
    """Target + realisasi nyata dari file data/ (jujur: yang tidak ada
    datanya ditulis 'belum cukup data', bukan 0)."""
    folder = Path(base) if base else DATA_DIR
    try:
        b01, _err = muat_modul_bintang("A01", base)
        rencana = b01.rencana_30_hari() if b01 is not None else None
        target = (rencana or {}).get("target_30_hari") or {}
        sumber = (rencana or {}).get("sumber", "")
        if not target:
            raise ValueError("target kosong")
    except Exception:  # noqa: BLE001 — fallback ke angka tercatat
        target = {"produk_digital_selesai": 15, "konten_terbit": 30,
                  "followers_baru": 1000, "lomba_diikuti": "5–10",
                  "pemasukan_pertama_rp": "500.000–2.000.000"}
        sumber = ("Salinan darurat (b01.rencana_30_hari tidak bisa dimuat) — "
                  "angka sama dengan Share Gemini #1")
    produk = _baca_json(folder / "produksi_game.json", [])
    lomba = _baca_json(folder / "lomba.json", [])
    dikirim = [x for x in lomba if x.get("status") == "dikirim"]
    keuangan = _baca_json(folder / "keuangan_data.json", {})
    entri = keuangan.get("entries", []) if isinstance(keuangan, dict) else []
    pemasukan = sum(float(e.get("jumlah_rp", 0) or 0)
                    for e in entri if str(e.get("jenis", "")).lower() == "masuk")
    return {
        "sumber": sumber,
        "catatan_jujur": ("Target rancangan Gemini #1, bukan janji. Jendela 30 hari "
                          "belum punya tanggal mulai tercatat — angka realisasi di "
                          "bawah adalah TOTAL tercatat di data/, bukan hitungan "
                          "dalam jendela 30 hari."),
        "target": [
            {"nama": "Produk digital selesai", "target": target.get("produk_digital_selesai", 15),
             "realisasi": len(produk) if isinstance(produk, list) else "belum cukup data",
             "satuan": "produk",
             "catatan": "Total produk tercatat di produksi_game.json."},
            {"nama": "Konten terbit", "target": target.get("konten_terbit", 30),
             "realisasi": "belum cukup data", "satuan": "konten",
             "catatan": "Tidak ada file data/ yang menghitung konten terbit."},
            {"nama": "Followers baru", "target": target.get("followers_baru", 1000),
             "realisasi": "belum cukup data", "satuan": "followers",
             "catatan": "Tidak ada file data/ yang mencatat jumlah followers."},
            {"nama": "Lomba diikuti", "target": target.get("lomba_diikuti", "5–10"),
             "realisasi": len(dikirim), "satuan": "lomba",
             "catatan": "Lomba berstatus 'dikirim' di lomba.json (total tercatat 28)."},
            {"nama": "Pemasukan pertama", "target": target.get("pemasukan_pertama_rp", "500.000–2.000.000"),
             "realisasi": "Rp{:,.0f}".format(pemasukan).replace(",", "."),
             "satuan": "rupiah",
             "catatan": "Jumlah entri 'masuk' di keuangan_data.json (baseline Rp0, {} entri).".format(len(entri))},
        ],
    }


# ---------------------------------------------------------------------------
# Dispatch: fungsi kerja nyata tiap agent + cara membangun argumennya dari
# tugas. Tiap entri: (nama_fungsi, [kunci_argumen_berurutan],
# [kunci_wajib]). Bila kunci wajib tidak ada di tugas -> contoh().
# Argumen dipanggil SECARA POSISIONAL sesuai urutan kunci.
# ---------------------------------------------------------------------------
FUNGSI_JALAN = {
    "A01": ("buat_arahan", ["tugas"], ["tugas"]),
    "A02": ("susun_jadwal", ["jadwal"], ["jadwal"]),
    "A03": ("bagi_tugas", ["ringkasan", "penanggung_jawab"], ["ringkasan"]),
    "A04": ("periksa_draf", ["teks"], ["teks"]),
    "A05": ("hitung_laba", ["pendapatan", "pengeluaran"], ["pendapatan", "pengeluaran"]),
    "A06": ("buat_brief_riset", ["niche", "masalah", "target"], ["niche", "masalah"]),
    "A07": ("catat_tren", ["topik", "sumber", "catatan"], ["topik", "sumber"]),
    "A08": ("buat_konsep_produk", ["nama", "masalah", "target", "keunikan", "harga", "bukti", "promosi"], ["nama", "masalah", "target"]),
    "A09": ("bandingkan_harga", ["produk", "harga_kita", "harga_pesaing", "pesaing"], ["produk", "harga_kita", "harga_pesaing"]),
    "A10": ("cek_kelayakan_produk", ["produk"], ["produk"]),
    "A11": ("buat_naskah_video", ["judul", "tema"], ["judul"]),
    "A12": ("buat_brief_visual", ["jenis", "tema"], ["tema"]),
    "A13": ("buat_spesifikasi_aplikasi", ["nama", "tujuan", "fitur"], ["nama"]),
    "A14": ("buat_spesifikasi_website", ["nama", "tujuan", "halaman"], ["nama"]),
    "A15": ("buat_brief_pod", ["produk", "tema"], ["tema"]),
    "A16": ("buat_kerangka_ebook", ["judul", "tema"], ["judul"]),
    "A17": ("buat_kerangka_cerita", ["jenis", "judul", "tema"], ["judul"]),
    "A18": ("buat_konsep_game", ["nama", "genre", "pemain"], ["nama"]),
    "A19": ("buat_paket_konten", ["produk", "kanal"], ["produk"]),
    "A20": ("buat_draf_posting", ["produk", "format"], ["produk"]),
    "A21": ("buat_draf_posting", ["produk", "format"], ["produk"]),
    "A22": ("buat_draf_video", ["judul", "format"], ["judul"]),
    "A23": ("buat_draf_threads", ["topik"], ["topik"]),
    "A24": ("buat_daftar_kata_kunci", ["topik"], ["topik"]),
    "A25": ("buat_draf_penawaran", ["nama_toko", "produk", "observasi"], ["nama_toko"]),
    "A26": ("buat_draf_balasan", ["pesan", "topik"], ["pesan"]),
    "A27": ("buat_draf_triase", ["email"], ["email"]),
    "A28": ("nilai_peluang_draf", ["teks", "nama"], ["teks"]),
    "A29": ("format_laporan", ["pendapatan", "pengeluaran"], ["pendapatan", "pengeluaran"]),
    "A30": ("buat_kerangka_sop", ["judul", "langkah"], ["judul"]),
}
# Alih nama kunci tugas -> kunci argumen fungsi (tugas memakai nama umum).
_ALIH_KUNCI = {
    "ringkasan": {"teks": "ringkasan", "nama": "ringkasan", "topik": "ringkasan",
                  "judul": "ringkasan", "pesan": "ringkasan"},
}
# ---------------------------------------------------------------------------
# Dispatch MESIN (bukan agent): Mesin Penjualan + Mesin Pemasaran.
# Dicatat jujur: FUNGSI_JALAN di atas HANYA memetakan kode agent A01–A30
# (satu fungsi per agent) — CRM pun TIDAK ada di FUNGSI_JALAN, CRM hanya
# lewat Tool Registry (baca_crm/simpan_crm). Mesin bukan agent (tidak ada
# di data/agents.json), jadi tidak bisa dipaksakan masuk FUNGSI_JALAN:
# jalankan_agent() menolak kode yang bukan agent sebelum dispatch.
# Karena itu mesin memakai tabel paralel ini + jalankan_mesin(), dengan
# pola dispatch yang SAMA persis (bangun argumen, cek signature,
# fallback contoh(), catat run ke log mesin, status "menunggu
# persetujuan"). Hanya fungsi BACA/RINGKASAN yang dipetakan di sini;
# fungsi tulis DRAFT (catat_transaksi, buat_kampanye, catat_hasil)
# tetap lewat Tool Registry (simpan_penjualan/simpan_pemasaran) —
# sama seperti CRM. Tidak ada pemetaan ke fungsi kirim/bayar
# (tidak ada juga di kedua mesin).
# ---------------------------------------------------------------------------
FUNGSI_MESIN = {
    "penjualan": ("laporan_pemasukan", ["dari", "sampai"], []),
    "pemasaran": ("laporan_kampanye", ["kampanye_id"], []),
}
_MESIN_MODUL = {"penjualan": "penjualan", "pemasaran": "pemasaran"}
_MESIN_JUDUL = {"penjualan": "Mesin Penjualan",
                "pemasaran": "Mesin Pemasaran"}


# Nilai default untuk kunci argumen OPSIONAL (bukan wajib). Kunci wajib
# yang hilang -> contoh() (lihat _bangun_argumen), bukan ditebak.
_DEFAULT_ARG = {
    "penanggung_jawab": "A08", "topik": "umum", "produk": "video",
    "format": "Video pendek", "observasi": "", "jenis": "konten",
    "catatan": "", "genre": "Arcade", "pemain": "Anak-anak",
    "kanal": ["Instagram"], "fitur": [], "halaman": [], "langkah": [],
    "target": "umum", "niche": "umum", "masalah": "belum cukup data",
    "sumber": "belum cukup data", "keunikan": "—",
    "bukti": "belum cukup data", "promosi": "TikTok", "pesaing": "—",
}
# Default per-agent (menang atas _DEFAULT_ARG) — karena satu kunci bisa
# berarti beda di tiap fungsi (mis. "jenis": A12 ilustrasi, A17 cerpen).
_DEFAULT_PER_AGENT = {
    "A08": {"harga": None},
    "A11": {"tema": "umum"},
    "A12": {"jenis": "ilustrasi"},
    "A13": {"tujuan": "umum"},
    "A14": {"tujuan": "website sederhana", "halaman": ["Beranda"]},
    "A15": {"produk": "Kaos"},
    "A16": {"tema": "umum"},
    "A17": {"jenis": "cerpen", "tema": "umum"},
    "A20": {"format": "Reels"},
    "A21": {"format": "Video pendek"},
    "A22": {"format": "Shorts"},
    "A26": {"topik": "harga"},
}


def _bangun_argumen(kode, tugas):
    """Bangun daftar argumen posisional untuk fungsi jalan agent dari
    dict tugas. Kembalikan None bila kunci wajib tidak tersedia."""
    if kode not in FUNGSI_JALAN:
        return None
    nama_fungsi, kunci, wajib = FUNGSI_JALAN[kode]
    tugas = tugas or {}
    # Normalisasi: tugas dari antrean membawa "ringkasan" sebagai teks utama.
    isi = dict(tugas)
    for kunci_arg, asal in _ALIH_KUNCI.get("ringkasan", {}).items():
        if kunci_arg not in isi and isi.get("ringkasan"):
            isi[kunci_arg] = isi.get("ringkasan")
    # A01/A02 menerima daftar tugas — bangun dari ringkasan bila perlu.
    if kode == "A01" and "tugas" not in isi and isi.get("ringkasan"):
        isi["tugas"] = [{"judul": str(isi["ringkasan"])[:100],
                         "prioritas": isi.get("prioritas", "P2"),
                         "penanggung_jawab": isi.get("penanggung_jawab", kode),
                         "status": "Dikerjakan"}]
    if kode == "A02" and "jadwal" not in isi and isi.get("ringkasan"):
        isi["jadwal"] = [{"judul": str(isi["ringkasan"])[:100],
                          "penanggung_jawab": isi.get("penanggung_jawab", kode)}]
    # A28: "nama" peluang dari jenis tugas bila tidak disebut.
    if kode == "A28" and not isi.get("nama"):
        isi["nama"] = str(isi.get("jenis") or "Peluang")[:80]
    for k in wajib:
        if isi.get(k) in (None, "", [], {}):
            return None
    per_agent = _DEFAULT_PER_AGENT.get(kode, {})
    return [isi.get(k, per_agent.get(k, _DEFAULT_ARG.get(k))) for k in kunci]


def _panggil_fungsi_jalan(modul, kode, tugas):
    """Panggil fungsi kerja nyata agent dengan argumen dari tugas.
    Kembalikan (draf, mode, alasan). mode: 'tugas' (argumen dari tugas)
    atau 'contoh' (fallback — tugas tidak membawa argumen yang cukup)."""
    nama_fungsi, _kunci, _wajib = FUNGSI_JALAN.get(kode, (None, [], []))
    if nama_fungsi and hasattr(modul, nama_fungsi):
        argumen = _bangun_argumen(kode, tugas)
        if argumen is not None:
            fungsi = getattr(modul, nama_fungsi)
            try:
                sig = inspect.signature(fungsi)
                params = [p for p in sig.parameters.values()
                          if p.kind in (p.POSITIONAL_ONLY,
                                        p.POSITIONAL_OR_KEYWORD)]
                wajib_jumlah = sum(1 for p in params
                                   if p.default is inspect.Parameter.empty)
                if len(argumen) >= wajib_jumlah:
                    draf = fungsi(*argumen[:len(params)]) if params else fungsi()
                    return draf, "tugas", ""
            except Exception as e:  # noqa: BLE001 — jatuh ke contoh()
                return None, "gagal", "{}: {}".format(type(e).__name__, e)
    if hasattr(modul, "contoh"):
        try:
            return modul.contoh(), "contoh", (
                "Tugas tidak membawa argumen yang cukup untuk fungsi {} — "
                "dijalankan contoh() modul.".format(nama_fungsi or "?"))
        except Exception as e:  # noqa: BLE001
            return None, "gagal", "{}: {}".format(type(e).__name__, e)
    return None, "gagal", "Modul {} tidak punya fungsi jalan maupun contoh().".format(kode)


# ---------------------------------------------------------------------------
# Dispatch MESIN — cermin _bangun_argumen/_panggil_fungsi_jalan di atas,
# tapi memakai FUNGSI_MESIN (nama mesin, bukan kode agent).
# ---------------------------------------------------------------------------
def _bangun_argumen_mesin(nama, tugas):
    """Bangun daftar argumen posisional untuk fungsi jalan mesin dari
    dict tugas. Kembalikan None bila kunci wajib tidak tersedia."""
    if nama not in FUNGSI_MESIN:
        return None
    _nama_fungsi, kunci, wajib = FUNGSI_MESIN[nama]
    isi = dict(tugas or {})
    for kunci_arg, asal in _ALIH_KUNCI.get("ringkasan", {}).items():
        if kunci_arg not in isi and isi.get("ringkasan"):
            isi[kunci_arg] = isi.get("ringkasan")
    for k in wajib:
        if isi.get(k) in (None, "", [], {}):
            return None
    return [isi.get(k, _DEFAULT_ARG.get(k)) for k in kunci]


def _panggil_fungsi_mesin(modul, nama, tugas):
    """Panggil fungsi jalan mesin. Kembalikan (draf, mode, alasan).
    mode: 'tugas' atau 'contoh' (fallback — tugas tidak membawa
    argumen yang cukup)."""
    nama_fungsi, _kunci, _wajib = FUNGSI_MESIN.get(nama, (None, [], []))
    if nama_fungsi and hasattr(modul, nama_fungsi):
        argumen = _bangun_argumen_mesin(nama, tugas)
        if argumen is not None:
            fungsi = getattr(modul, nama_fungsi)
            try:
                sig = inspect.signature(fungsi)
                params = [p for p in sig.parameters.values()
                          if p.kind in (p.POSITIONAL_ONLY,
                                        p.POSITIONAL_OR_KEYWORD)]
                wajib_jumlah = sum(1 for p in params
                                   if p.default is inspect.Parameter.empty)
                if len(argumen) >= wajib_jumlah:
                    draf = fungsi(*argumen[:len(params)]) if params else fungsi()
                    return draf, "tugas", ""
            except Exception as e:  # noqa: BLE001 — jatuh ke contoh()
                return None, "gagal", "{}: {}".format(type(e).__name__, e)
    if hasattr(modul, "contoh"):
        try:
            return modul.contoh(), "contoh", (
                "Tugas tidak membawa argumen yang cukup untuk fungsi {} — "
                "dijalankan contoh() modul.".format(nama_fungsi or "?"))
        except Exception as e:  # noqa: BLE001
            return None, "gagal", "{}: {}".format(type(e).__name__, e)
    return None, "gagal", "Modul {} tidak punya fungsi jalan maupun contoh().".format(nama)


def muat_modul_mesin(nama):
    """Impor modul agents/<nama>.py (penjualan/pemasaran).
    Kembalikan (modul, pesan_error)."""
    if nama not in _MESIN_MODUL:
        return None, "Mesin {} tidak dikenal.".format(nama)
    try:
        return importlib.import_module(_MESIN_MODUL[nama]), None
    except Exception as e:  # noqa: BLE001
        return None, "{}: {}".format(type(e).__name__, e)


def jalankan_mesin(nama, tugas=None, base=None):
    """Jalankan SATU mesin (penjualan/pemasaran): panggil fungsi
    jalan baca/ringkasannya. tugas: dict argumen (boleh None).
    Kembalikan dict hasil dan catat run ke log mesin + activity log.
    Output selalu DRAF; mesin TIDAK PERNAH mengirim/membayar."""
    folder = Path(base) if base else DATA_DIR
    nama = (nama or "").lower()
    if nama not in FUNGSI_MESIN:
        return {"ok": False, "mesin": nama,
                "alasan": "Mesin {} tidak dikenal (pilih: {}).".format(
                    nama, ", ".join(sorted(FUNGSI_MESIN)))}
    kode_log = "MESIN-" + nama
    modul, err = muat_modul_mesin(nama)
    if modul is None:
        _catat_run({"kode_agent": kode_log,
                    "nama_agent": _MESIN_JUDUL.get(nama, nama),
                    "tugas": tugas or {}, "mode": "gagal",
                    "status": "terkendala",
                    "penyebab": "Modul gagal dimuat: {}".format(err),
                    "dibutuhkan_dari_cipta": "Perbaiki modul agents/{}.py.".format(
                        _MESIN_MODUL[nama]),
                    "draf": None}, base)
        return {"ok": False, "mesin": nama,
                "alasan": "Modul gagal dimuat: {}".format(err)}
    mulai = _waktu_sekarang()
    draf, mode, alasan = _panggil_fungsi_mesin(modul, nama, tugas)
    selesai = _waktu_sekarang()
    if draf is None:
        _catat_run({"kode_agent": kode_log,
                    "nama_agent": _MESIN_JUDUL.get(nama, nama),
                    "tugas": tugas or {}, "mode": mode,
                    "status": "terkendala",
                    "penyebab": "Fungsi jalan gagal: {}".format(alasan or "?"),
                    "dibutuhkan_dari_cipta": "Periksa modul agents/{}.py.".format(
                        _MESIN_MODUL[nama]),
                    "draf": None,
                    "waktu_mulai": mulai, "waktu_selesai": selesai}, base)
        return {"ok": False, "mesin": nama, "mode": mode, "alasan": alasan}
    log = _baca_log_mesin(folder)
    run_id = _id_run_baru(log, kode_log)
    hasil = _ringkas_draf(draf)
    _catat_run({"id": run_id, "kode_agent": kode_log,
                "nama_agent": _MESIN_JUDUL.get(nama, nama),
                "tugas": tugas or {}, "mode": mode,
                "status": "menunggu persetujuan",
                "keputusan": None, "oleh": None,
                "draf": draf, "hasil": hasil,
                "waktu_mulai": mulai, "waktu_selesai": selesai}, base)
    _log_activity(kode_log,
                  "mesin eksekusi: " + (_MESIN_JUDUL.get(nama, nama) or ""),
                  hasil,
                  detail="mode={}; run {}".format(mode, run_id), base=folder)
    return {"ok": True, "id": run_id, "mesin": nama, "mode": mode,
            "status": "menunggu persetujuan", "draf": draf,
            "alasan": alasan}


# ---------------------------------------------------------------------------
# Log eksekusi mesin (audit log) — data/mesin_eksekusi_log.json
# ---------------------------------------------------------------------------
def _baca_log_mesin(base=None):
    folder = Path(base) if base else DATA_DIR
    return _baca_json(folder / LOG_MESIN_NAMA, [])


def _tulis_log_mesin(log, base=None):
    folder = Path(base) if base else DATA_DIR
    _tulis_json_atomik(folder / LOG_MESIN_NAMA, log[-MAKS_LOG:])


def _id_run_baru(log, kode):
    ts = datetime.now(WIB).strftime("%Y%m%d%H%M%S")
    sama = sum(1 for e in log
               if str(e.get("id", "")).startswith("ME-" + ts + "-" + kode))
    return "ME-{}-{}-{:03d}".format(ts, kode, sama + 1)


def _ringkas_draf(draf):
    if isinstance(draf, dict):
        for k in ("judul", "nama", "topik", "tema", "produk"):
            if draf.get(k):
                return str(draf[k])[:120]
        return json.dumps(draf, ensure_ascii=False)[:120]
    return str(draf)[:120]


def jalankan_agent(kode, tugas=None, base=None):
    """Jalankan SATU agent Bintang sesuai job description-nya.
    tugas: dict argumen (boleh None -> contoh()). Kembalikan dict hasil
    dan catat run ke log mesin + activity log. Output selalu DRAF."""
    folder = Path(base) if base else DATA_DIR
    entri = info_agent(kode, base)
    if entri is None:
        return {"ok": False, "kode": kode,
                "alasan": "Agent {} tidak ada di data/agents.json.".format(kode)}
    modul, err = muat_modul_bintang(kode, base)
    if modul is None:
        _catat_run({"kode_agent": kode, "nama_agent": entri.get("name", ""),
                    "tugas": tugas or {}, "mode": "gagal",
                    "status": "terkendala",
                    "penyebab": "Modul gagal dimuat: {}".format(err),
                    "dibutuhkan_dari_cipta": "Perbaiki modul agents/{}.".format(
                        (entri.get("file", "") or "").replace("agents/", "")),
                    "draf": None}, base)
        return {"ok": False, "kode": kode,
                "alasan": "Modul gagal dimuat: {}".format(err)}
    mulai = _waktu_sekarang()
    draf, mode, alasan = _panggil_fungsi_jalan(modul, kode, tugas)
    selesai = _waktu_sekarang()
    if draf is None:
        _catat_run({"kode_agent": kode, "nama_agent": entri.get("name", ""),
                    "tugas": tugas or {}, "mode": mode,
                    "status": "terkendala",
                    "penyebab": "Fungsi jalan gagal: {}".format(alasan or "?"),
                    "dibutuhkan_dari_cipta": "Periksa modul agents/{}.".format(
                        (entri.get("file", "") or "").replace("agents/", "")),
                    "draf": None,
                    "waktu_mulai": mulai, "waktu_selesai": selesai}, base)
        return {"ok": False, "kode": kode, "mode": mode, "alasan": alasan}
    log = _baca_log_mesin(folder)
    run_id = _id_run_baru(log, kode)
    hasil = _ringkas_draf(draf)
    _catat_run({"id": run_id, "kode_agent": kode,
                "nama_agent": entri.get("name", ""),
                "tugas": tugas or {}, "mode": mode,
                "status": "menunggu persetujuan",
                "keputusan": None, "oleh": None,
                "draf": draf, "hasil": hasil,
                "waktu_mulai": mulai, "waktu_selesai": selesai}, base)
    _log_activity(kode, "mesin eksekusi: " + (entri.get("job_desc", "") or ""),
                  hasil,
                  detail="mode={}; run {}".format(mode, run_id), base=folder)
    return {"ok": True, "id": run_id, "kode": kode, "mode": mode,
            "status": "menunggu persetujuan", "draf": draf,
            "alasan": alasan}


def _catat_run(entri, base=None):
    folder = Path(base) if base else DATA_DIR
    log = _baca_log_mesin(folder)
    if "id" not in entri:
        entri["id"] = _id_run_baru(log, entri.get("kode_agent", "?"))
    if "waktu_mulai" not in entri:
        entri["waktu_mulai"] = _waktu_sekarang()
    if "waktu_selesai" not in entri:
        entri["waktu_selesai"] = _waktu_sekarang()
    log.append(entri)
    _tulis_log_mesin(log, folder)
    return entri


def catat_persetujuan(id_pekerjaan, keputusan, oleh="Cipta", catatan="", base=None):
    """Catat keputusan Cipta atas satu run (audit log). keputusan:
    'disetujui' atau 'ditolak'. Mengembalikan True bila ditemukan."""
    folder = Path(base) if base else DATA_DIR
    if keputusan not in ("disetujui", "ditolak"):
        return False
    log = _baca_log_mesin(folder)
    for e in log:
        if e.get("id") == id_pekerjaan:
            e["status"] = "selesai"
            e["keputusan"] = keputusan
            e["oleh"] = oleh
            e["catatan_keputusan"] = catatan or ""
            e["waktu_keputusan"] = _waktu_sekarang()
            _tulis_log_mesin(log, folder)
            _log_activity(e.get("kode_agent", "?"),
                          "persetujuan: {}".format(keputusan),
                          "{} — {}".format(id_pekerjaan, e.get("hasil", "?")),
                          detail="oleh {}".format(oleh), base=folder)
            return True
    return False


def audit_log(base=None, limit=50):
    """Entri log mesin terbaru dulu (eksekusi + persetujuan + kendala)."""
    log = _baca_log_mesin(base)
    if limit:
        log = log[-limit:]
    return list(reversed(log))


# ---------------------------------------------------------------------------
# Kendala — pekerjaan yang tidak bisa jalan harus DILAPORKAN, bukan dilewati
# ---------------------------------------------------------------------------
def tentukan_kendala(item):
    """Periksa satu item antrean: butuh platform belum terhubung atau
    data kritis tidak ada? Kembalikan (penyebab, dibutuhkan_dari_cipta)
    atau None bila tidak ada kendala yang terdeteksi."""
    import re
    teks = ((item.get("ringkasan") or "") + " " +
            json.dumps(item.get("tugas") or {}, ensure_ascii=False)).lower()
    # Alamat email (mis. masduki1189@gmail.com) bukan "butuh Gmail".
    teks = re.sub(r"\S+@\S+", "", teks)
    for kunci_platform, kata_aksi, nama, dibutuhkan in KENDALA_PLATFORM:
        # SEMUA kunci platform harus ada (mis. "@meongcast" DAN "tiktok").
        if not all(k in teks for k in kunci_platform):
            continue
        if any(a in teks for a in kata_aksi) or any(
                a in teks for a in KATA_AKSI_PLATFORM):
            return ("Platform belum terhubung: {} — tugas butuh platform itu."
                    .format(nama), dibutuhkan)
    if item.get("sumber") == "penawaran-toko" and not (item.get("tugas") or {}).get("nama_toko"):
        return ("Data tidak ada: nama toko kosong pada draf penawaran.",
                "Periksa data/penjualan_toko.json — isi nama toko.")
    return None


# ---------------------------------------------------------------------------
# Antrean kerja — dari handoff.json + draf penawaran toko + log mesin
# ---------------------------------------------------------------------------
def _agen_untuk_handoff(item):
    jenis = str(item.get("jenis", ""))
    if jenis in RUTE_JENIS:
        return RUTE_JENIS[jenis]
    ke = str(item.get("ke_agent", ""))
    nomor = ke.replace("Agent", "").strip()
    if nomor in RUTE_MESIN_KE_BINTANG:
        return RUTE_MESIN_KE_BINTANG[nomor]
    return "A01"


def antrean_kerja(base=None):
    """Daftar pekerjaan menunggu: status + prioritas + tenggat + agent
    Bintang + kendala (bila ada). Jujur: handoff.json tidak mencatat
    prioritas/tanggal — default prioritas 'normal', tenggat '—'."""
    folder = Path(base) if base else DATA_DIR
    log_mesin = _baca_log_mesin(folder)
    sudah_diproses = {e.get("id_antrean") for e in log_mesin
                      if e.get("id_antrean")}
    antrean = []
    handoff = _baca_json(folder / "handoff.json", [])
    for h in handoff:
        status_asal = str(h.get("status", ""))
        if status_asal not in ("draf", "diperiksa"):
            continue
        kode = _agen_untuk_handoff(h)
        tugas = dict(h.get("isi") or {}) if isinstance(h.get("isi"), dict) else {}
        tugas["ringkasan"] = h.get("ringkasan", "")
        tugas["jenis"] = h.get("jenis", "")
        item = {"id": "HO-" + str(h.get("id", "?")),
                "sumber": "handoff", "jenis": h.get("jenis", "?"),
                "agent": kode, "ringkasan": h.get("ringkasan", ""),
                "status": ("menunggu" if status_asal == "draf"
                           else "menunggu persetujuan"),
                "prioritas": h.get("prioritas", "normal") or "normal",
                "tenggat": h.get("tenggat", "—") or "—",
                "tugas": tugas,
                "sudah_diproses": ("HO-" + str(h.get("id", "?"))) in sudah_diproses}
        kendala = tentukan_kendala(item)
        if kendala:
            item["status"] = "terkendala"
            item["penyebab"], item["dibutuhkan_dari_cipta"] = kendala
        antrean.append(item)
    toko = _baca_json(folder / "penjualan_toko.json", {}).get("toko", [])
    for t in toko:
        if t.get("status") != "draf":
            continue
        catatan = str(t.get("catatan") or "")
        observasi = catatan.split("| HASIL")[0].strip()[:200]
        tugas = {"nama_toko": t.get("nama", ""), "produk": "video",
                 "observasi": observasi, "ringkasan": t.get("draf", "")[:200]}
        item = {"id": "TK-" + str(t.get("id", "?")),
                "sumber": "penawaran-toko", "jenis": "draf-penawaran",
                "agent": "A25", "ringkasan": "Penawaran ke {}".format(t.get("nama", "?")),
                "status": "menunggu",
                "prioritas": t.get("prioritas", "normal") or "normal",
                "tenggat": t.get("tenggat", "—") or "—",
                "tugas": tugas,
                "sudah_diproses": ("TK-" + str(t.get("id", "?"))) in sudah_diproses}
        kendala = tentukan_kendala(item)
        if kendala:
            item["status"] = "terkendala"
            item["penyebab"], item["dibutuhkan_dari_cipta"] = kendala
        antrean.append(item)
    for e in log_mesin:
        if e.get("status") in ("menunggu persetujuan", "terkendala"):
            antrean.append({
                "id": str(e.get("id", "?")), "sumber": "mesin",
                "jenis": "draf-mesin",
                "agent": e.get("kode_agent", "?"),
                "ringkasan": str(e.get("hasil", "?")),
                "status": e.get("status", "?"),
                "prioritas": "normal", "tenggat": "—",
                "tugas": e.get("tugas") or {},
                "penyebab": e.get("penyebab", ""),
                "dibutuhkan_dari_cipta": e.get("dibutuhkan_dari_cipta", ""),
                "sudah_diproses": True})
    antrean.sort(key=lambda x: (PRIORITAS_URUTAN.get(x.get("prioritas", "normal"), 1),
                                x.get("id", "")))
    return antrean


def tugas_terkendala(base=None):
    """Hanya item antrean berstatus 'terkendala'."""
    return [a for a in antrean_kerja(base) if a.get("status") == "terkendala"]


def jalankan_antrean(base=None, maks=5):
    """Proses item antrean berstatus 'menunggu' (maks N). Item
    'terkendala' TIDAK dijalankan — dicatat sebagai terkendala di log.
    Item yang sudah punya draf menunggu persetujuan dilewati (tidak dobel).
    Kembalikan ringkasan {dijalankan, berhasil, terkendala, dilewati, rincian}."""
    folder = Path(base) if base else DATA_DIR
    antrean = antrean_kerja(folder)
    ringkasan = {"dijalankan": 0, "berhasil": 0, "terkendala": 0,
                 "dilewati": 0, "rincian": []}
    diproses = 0
    for item in antrean:
        if diproses >= maks:
            break
        if item.get("status") == "terkendala":
            # Sudah mentok sebelumnya — tampil di tabel terkendala
            # Dashboard, bukan dihitung sebagai kendala baru run ini.
            ringkasan["dilewati"] += 1
            continue
        if item.get("status") != "menunggu" or item.get("sudah_diproses"):
            ringkasan["dilewati"] += 1
            continue
        diproses += 1
        ringkasan["dijalankan"] += 1
        hasil = jalankan_agent(item["agent"], tugas=item.get("tugas"),
                               base=folder)
        if hasil.get("ok"):
            ringkasan["berhasil"] += 1
            _tandai_antrean_diproses(hasil.get("id"), item["id"], folder)
        else:
            ringkasan["terkendala"] += 1
        ringkasan["rincian"].append({
            "id": item["id"], "agent": item["agent"],
            "status": ("menunggu persetujuan" if hasil.get("ok")
                       else "terkendala"),
            "mode": hasil.get("mode", "?"),
            "hasil": hasil.get("draf") and _ringkas_draf(hasil.get("draf")) or hasil.get("alasan", ""),
            "run_id": hasil.get("id")})
    return ringkasan


def _tandai_antrean_diproses(run_id, id_antrean, base=None):
    folder = Path(base) if base else DATA_DIR
    log = _baca_log_mesin(folder)
    for e in log:
        if e.get("id") == run_id:
            e["id_antrean"] = id_antrean
            break
    _tulis_log_mesin(log, folder)


def jalankan_slot(jam=None, base=None):
    """Jalankan semua agent pada slot jam tersebut (siklus SOP).
    Tanpa tugas antrean -> mode 'contoh' (dicatat jujur di log)."""
    folder = Path(base) if base else DATA_DIR
    slot = slot_untuk_jam(jam)
    if slot is None:
        return {"ok": False, "alasan": "Tidak ada slot jadwal."}
    hasil = {"slot": slot["jam"], "kegiatan": slot["kegiatan"],
             "dijalankan": 0, "berhasil": 0, "terkendala": 0, "rincian": []}
    for kode in slot["agent"]:
        hasil["dijalankan"] += 1
        r = jalankan_agent(kode, tugas=None, base=folder)
        if r.get("ok"):
            hasil["berhasil"] += 1
        else:
            hasil["terkendala"] += 1
        hasil["rincian"].append({"agent": kode, "ok": bool(r.get("ok")),
                                 "mode": r.get("mode", "?"),
                                 "run_id": r.get("id")})
    return hasil


# ---------------------------------------------------------------------------
# KPI per agent Bintang — target dari gemini_kpi di agents.json
# ---------------------------------------------------------------------------
def kpi_agent(base=None):
    """Satu baris per agent Bintang: target (gemini_kpi) + realisasi
    dari log mesin. Agent tanpa eksekusi: eksekusi 0, terakhir '—'."""
    folder = Path(base) if base else DATA_DIR
    log = _baca_log_mesin(folder)
    rows = []
    for e in daftar_agent_bintang(folder):
        kode = e.get("code", "")
        jalan = [x for x in log if x.get("kode_agent") == kode]
        rows.append({
            "kode": kode, "nama": e.get("name", ""),
            "divisi": e.get("division", ""),
            "job_desc": e.get("job_desc", ""),
            "target": list(e.get("gemini_kpi") or []),
            "kpi_chatgpt": e.get("kpi_chatgpt") or None,
            "platform_terhubung": (e.get("platform") or {}).get("terhubung", []),
            "platform_belum": (e.get("platform") or {}).get("belum_terhubung", []),
            "status": e.get("status", ""),
            "eksekusi": len(jalan),
            "draf_menunggu": sum(1 for x in jalan if x.get("status") == "menunggu persetujuan"),
            "disetujui": sum(1 for x in jalan if x.get("keputusan") == "disetujui"),
            "ditolak": sum(1 for x in jalan if x.get("keputusan") == "ditolak"),
            "terkendala": sum(1 for x in jalan if x.get("status") == "terkendala"),
            "terakhir": jalan[-1].get("waktu_selesai", "—") if jalan else "—"})
    return rows


def platform_per_agent(base=None):
    """Pemetaan platform per agent Bintang (dari agents.json)."""
    folder = Path(base) if base else DATA_DIR
    return [{"kode": e.get("code", ""), "nama": e.get("name", ""),
             "terhubung": (e.get("platform") or {}).get("terhubung", []),
             "belum_terhubung": (e.get("platform") or {}).get("belum_terhubung", [])}
            for e in daftar_agent_bintang(folder)]


# ---------------------------------------------------------------------------
# CLI — python -m agents.mesin_eksekusi [KODE | --mesin NAMA [TUGAS-JSON] | --antrean | --kpi | --slot [JAM] | --jadwal | --target | --daftar]
# Tanpa argumen: jalankan antrean menunggu (maks 5).
# ---------------------------------------------------------------------------
def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    # PK_DATA_DIR (dipakai tes): arahkan semua baca/tulis data ke folder lain.
    base = os.environ.get("PK_DATA_DIR") or None
    if not args:
        hasil = jalankan_antrean(base)
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--antrean":
        print(json.dumps(antrean_kerja(base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--kpi":
        print(json.dumps(kpi_agent(base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--jadwal":
        print(json.dumps(jadwal_harian_mesin(base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--target":
        print(json.dumps(target_30_hari(base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--daftar":
        print(json.dumps(daftar_agent_bintang(base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--slot":
        jam = int(args[1]) if len(args) > 1 else None
        print(json.dumps(jalankan_slot(jam, base), ensure_ascii=False, indent=2))
        return 0
    if args[0] == "--mesin":
        if len(args) < 2:
            print(json.dumps(
                {"ok": False,
                 "alasan": "Pilih mesin: {}.".format(
                     ", ".join(sorted(FUNGSI_MESIN)))},
                ensure_ascii=False, indent=2))
            return 1
        tugas_mesin = None
        if len(args) > 2:
            try:
                tugas_mesin = json.loads(" ".join(args[2:]))
            except ValueError:
                tugas_mesin = {"ringkasan": " ".join(args[2:])}
        hasil = jalankan_mesin(args[1], tugas=tugas_mesin, base=base)
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return 0 if hasil.get("ok") else 1
    kode = args[0].upper()
    tugas = None
    if len(args) > 1:
        try:
            tugas = json.loads(" ".join(args[1:]))
        except ValueError:
            tugas = {"ringkasan": " ".join(args[1:])}
    hasil = jalankan_agent(kode, tugas=tugas, base=base)
    print(json.dumps(hasil, ensure_ascii=False, indent=2))
    return 0 if hasil.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
