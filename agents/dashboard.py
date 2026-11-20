# ======================================================================
# BINTANG COMMAND CENTER — Dashboard Pergerakan Agent. Pusat Komando v2.0.
# Dibuat 21 Nov 2026 atas perintah Cipta ("Setelah ini buat dashboard
# agar aku bisa liat juga pergerakan agent"). Diperbarui 21 Nov 2026
# (v2.0): hitungan utama 30 Agent Bintang; 14 mesin lama tampil terpisah
# sebagai "Pasif — non job" (bukan agent bertugas).
#
# Modul ini HANYA MEMBACA data nyata di folder data/ dan menulis log
# aktivitas ke data/activity_log.json. Tidak ada yang dikarang: bila
# sebuah agent belum punya aktivitas tercatat, tabel menulis
# "belum ada aktivitas". Semua output dashboard adalah RINGKASAN untuk
# dilihat Cipta — bukan perintah otomatis, bukan pengiriman.
#
# "Belum jalan" = status Aktif tapi belum ada aktivitas tercatat di
# folder data/. Hitungan ini berdasarkan data — agent yang bekerja lewat
# Muse tanpa menulis ke data/ akan tetap tampil "belum ada aktivitas".
# Target 30 hari Gemini (15 produk, 30 konten, 1000 followers baru,
# 5–10 lomba, Rp500rb–Rp2jt) dibaca dari mesin eksekusi (sumber:
# b01.rencana_30_hari, Share Gemini #1) — bukan janji.
# ======================================================================
import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
LOG_FILE_NAMA = "activity_log.json"
LOG_MESIN_NAMA = "mesin_eksekusi_log.json"
MAKS_LOG = 500
WIB = timezone(timedelta(hours=7))

# 14 mesin lama (dulu agent bernomor 1–14). Pekerjaan mereka DICABUT
# 21 Nov 2026 (perintah Cipta): modul + data tetap utuh sebagai mesin
# (engine/pustaka) yang dipakai 30 Agent Bintang, tapi tidak lagi punya
# pekerjaan/tugas sendiri. Status: "Pasif — non job". Tim 9A–9F tercakup
# dalam baris Mesin 9 (mereka berbagi satu sumber kerja: worklist-73.json).
STATUS_PASIF = "Pasif — non job"
MESIN_PASIF = [
    ("1", "Asisten", "Mesin pasif", "Muse", "handoff"),
    ("2", "Penjualan", "Mesin pasif", "Muse", "leads"),
    ("3", "Pertumbuhan", "Mesin pasif", "Muse", "handoff"),
    ("4", "Penjualan Harian", "Mesin pasif", "Muse", "penjualan_toko"),
    ("5", "Produksi Produk", "Mesin pasif", "Muse", "produksi_game"),
    ("6", "Lomba", "Mesin pasif", "Muse", "lomba"),
    ("7", "Keuangan", "Mesin pasif", "Muse", "keuangan"),
    ("8", "Terjemah Inggris", "Mesin pasif", "Muse", "terjemahan"),
    ("9", "Game & Aplikasi", "Mesin pasif", "Muse", "worklist"),
    ("10", "Riset Produk", "Mesin pasif", "Muse", "riset"),
    ("11", "Oyen", "Mesin pasif", "Muse", "handoff"),
    ("12", "Momo", "Mesin pasif", "Muse", "handoff"),
    ("13", "Email", "Mesin pasif", "Muse", "email"),
    ("14", "Upwork", "Mesin pasif", "Muse", "upwork"),
]
# Alias lama (kompatibilitas): nama lama tetap bisa diimpor.
AGENT_LAMA = MESIN_PASIF

BELUM_ADA = "belum ada aktivitas"


def _waktu_sekarang():
    return datetime.now(WIB).strftime("%Y-%m-%d %H:%M")


def _baca_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, type(default)) else default
    except (OSError, ValueError):
        return default


def _tulis_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Umpan aktivitas (activity feed)
# ---------------------------------------------------------------------------
def log_activity(kode_agent, aksi, hasil, detail="", base=None):
    """Tambah satu baris ke activity_log.json.

    Diam bila gagal (jangan pernah menjatuhkan agent yang memanggil).
    Tidak menulis apa pun bila env PK_NO_LOG disetel (dipakai saat tes).
    Mengembalikan True bila baris tersimpan.
    """
    if os.environ.get("PK_NO_LOG"):
        return False
    folder = Path(base) if base else BASE
    path = folder / LOG_FILE_NAMA
    try:
        folder.mkdir(parents=True, exist_ok=True)
        log = _baca_json(path, [])
        log.append({"waktu": _waktu_sekarang(),
                    "kode_agent": str(kode_agent),
                    "aksi": str(aksi), "hasil": str(hasil),
                    "detail": str(detail or "")})
        _tulis_json(path, log[-MAKS_LOG:])
        return True
    except Exception:  # noqa: BLE001 — log tidak boleh mematikan pemanggil
        return False


def baca_log(limit=50, base=None):
    """Baris log terbaru dulu. Kosong bila file belum ada."""
    folder = Path(base) if base else BASE
    log = _baca_json(folder / LOG_FILE_NAMA, [])
    if limit:
        log = log[-limit:]
    return list(reversed(log))


# ---------------------------------------------------------------------------
# Sumber data nyata per agent lama
# ---------------------------------------------------------------------------
def _aktivitas_handoff(folder, kode):
    """Aktivitas terakhir agent dari handoff.json (dari/ke agent tersebut)."""
    items = _baca_json(folder / "handoff.json", [])
    cocok = [h for h in items
             if str(h.get("dari_agent", "")) in ("Agent " + kode, kode)
             or str(h.get("ke_agent", "")) in ("Agent " + kode, kode)]
    if not cocok:
        return BELUM_ADA, "—"
    terakhir = cocok[-1]
    return ("Handoff {} ({} → {}, status {})".format(
                terakhir.get("id", "?"), terakhir.get("dari_agent", "?"),
                terakhir.get("ke_agent", "?"), terakhir.get("status", "?")),
            (terakhir.get("ringkasan", "") or "—")[:120])


def _aktivitas_mesin(folder, kode, sumber):
    """Kembalikan (aktivitas_terakhir, output_terakhir) dari data nyata.
    Dipakai untuk 14 mesin pasif — aktivitas HISTORIS mesin itu (apa
    yang dulu dikerjakannya sebelum pekerjaannya dicabut)."""
    if sumber == "handoff":
        return _aktivitas_handoff(folder, kode)
    if sumber == "leads":
        leads = _baca_json(folder / "leads.json", {}).get("leads", [])
        if not leads:
            return BELUM_ADA, "—"
        baru = sum(1 for l in leads if l.get("status") == "baru")
        return ("{} lead tercatat ({} baru)".format(len(leads), baru),
                "Lead terakhir: {}".format(leads[-1].get("nama", "?")))
    if sumber == "penjualan_toko":
        toko = _baca_json(folder / "penjualan_toko.json", {}).get("toko", [])
        terkirim = [t for t in toko if t.get("status") == "terkirim"]
        draf = [t for t in toko if t.get("status") == "draf"]
        if not toko:
            return BELUM_ADA, "—"
        return ("{} penawaran terkirim, {} draf".format(len(terkirim), len(draf)),
                "Terakhir terkirim: {}".format(
                    terkirim[-1].get("nama", "?") if terkirim else "—"))
    if sumber == "produksi_game":
        items = _baca_json(folder / "produksi_game.json", [])
        if not items:
            return BELUM_ADA, "—"
        hitung = Counter(i.get("status", "?") for i in items)
        return ("{} produk tercatat ({})".format(
                    len(items), ", ".join("{}: {}".format(k, v)
                                          for k, v in sorted(hitung.items()))),
                "Terakhir: {}".format(items[-1].get("nama", "?")))
    if sumber == "lomba":
        items = _baca_json(folder / "lomba.json", [])
        if not items:
            return BELUM_ADA, "—"
        hitung = Counter(i.get("status", "?") for i in items)
        dikirim = [i for i in items if i.get("status") == "dikirim"]
        return ("{} lomba tercatat ({} dikirim, {} ditolak, {} baru)".format(
                    len(items), len(dikirim),
                    hitung.get("ditolak", 0), hitung.get("baru", 0)),
                "Terakhir dikirim: {}".format(
                    dikirim[-1].get("nama", "?") if dikirim else "—"))
    if sumber == "keuangan":
        data = _baca_json(folder / "keuangan_data.json", {})
        entries = data.get("entries", [])
        if not entries:
            return ("Belum ada entri (baseline Rp0, {})".format(
                        data.get("baseline_tanggal", "?")),
                    data.get("baseline_catatan", "—"))
        terakhir = entries[-1]
        return ("Entri terakhir: {}".format(terakhir.get("tanggal", "?")),
                str(terakhir)[:120])
    if sumber == "terjemahan":
        folder_terj = folder / "terjemahan"
        isi = list(folder_terj.iterdir()) if folder_terj.is_dir() else []
        if not isi:
            return BELUM_ADA, "folder data/terjemahan kosong"
        return ("{} file terjemahan".format(len(isi)), isi[-1].name)
    if sumber == "worklist":
        items = _baca_json(folder / "worklist-73.json", [])
        if not items:
            return BELUM_ADA, "—"
        selesai = sum(1 for i in items if i.get("status") == "selesai")
        return ("{}/{} demo selesai".format(selesai, len(items)),
                "Terakhir: {}".format(items[-1].get("nama", "?")))
    if sumber == "riset":
        items = _baca_json(folder / "riset.json", [])
        if not items:
            return BELUM_ADA, "log riset kosong"
        return ("{} entri riset".format(len(items)),
                "{} — {}".format(items[-1].get("niche", "?"),
                                 items[-1].get("ide", "?")))
    if sumber == "email":
        items = _baca_json(folder / "log-aktivitas-email.json", [])
        if not items:
            return BELUM_ADA, "—"
        terakhir = items[-1]
        return ("Cek email terakhir {} ({})".format(
                    terakhir.get("tanggal", "?"), terakhir.get("aksi", "?")),
                terakhir.get("hasil", "—"))
    if sumber == "upwork":
        lamaran = _baca_json(folder / "lamaran_upwork.json", {}).get("lamaran", [])
        if not lamaran:
            return ("Belum ada lamaran (mode persiapan, akun belum ada)",
                    "Riset job + draf proposal saja")
        return ("{} lamaran".format(len(lamaran)),
                str(lamaran[-1])[:120])
    return BELUM_ADA, "—"


# ---------------------------------------------------------------------------
# Tabel gabungan: 30 Agent Bintang + 14 mesin pasif (44 baris)
# ---------------------------------------------------------------------------
def _aktivitas_b30(folder, kode):
    log = _baca_json(folder / LOG_FILE_NAMA, [])
    cocok = [e for e in log if e.get("kode_agent") == kode]
    if not cocok:
        return BELUM_ADA, "—"
    terakhir = cocok[-1]
    return ("{} — {}".format(terakhir.get("waktu", "?"),
                             terakhir.get("aksi", "?")),
            terakhir.get("hasil", "—"))


def tabel_semua_agent(base=None):
    """Satu baris per agent/mesin: kode, nama, kelompok, dipetakan_ke,
    status, aktivitas_terakhir, output_terakhir. Sumber: agents.json +
    data nyata. Urutan: 30 Bintang dulu, lalu 14 mesin pasif."""
    folder = Path(base) if base else BASE
    data = _baca_json(folder / "agents.json", {})
    b30 = (data.get("agent_30") or {}).get("agents", [])
    rows = []
    for e in b30:
        kode = e.get("code", "")
        aktivitas, output = _aktivitas_b30(folder, kode)
        rows.append({"kode": kode, "nama": e.get("name", ""),
                     "kelompok": e.get("division", ""),
                     "dipetakan_ke": e.get("mapped_to", ""),
                     "status": e.get("status", ""),
                     "aktivitas_terakhir": aktivitas,
                     "output_terakhir": output})
    for kode, nama, kelompok, peta, sumber in MESIN_PASIF:
        aktivitas, output = _aktivitas_mesin(folder, kode, sumber)
        rows.append({"kode": kode, "nama": nama, "kelompok": kelompok,
                     "dipetakan_ke": peta, "status": STATUS_PASIF,
                     "aktivitas_terakhir": aktivitas,
                     "output_terakhir": output})
    return rows


# Alias lama (kompatibilitas).
_aktivitas_agent_lama = _aktivitas_mesin


def daftar_divisi(base=None):
    divisi = []
    for r in tabel_semua_agent(base):
        if r["kelompok"] not in divisi:
            divisi.append(r["kelompok"])
    return divisi


def ringkasan_dashboard(base=None):
    """Hitungan ringkas (Pusat Komando v2.0): hitungan utama 30 Agent
    Bintang (Aktif / Aktif sebagian / Belum jalan) + 14 mesin pasif
    terpisah + antrean. 'total_agent' = 30 (Bintang); 'total_baris' = 44
    (30 Bintang + 14 mesin)."""
    folder = Path(base) if base else BASE
    rows = tabel_semua_agent(folder)
    bintang = [r for r in rows if r["kode"].startswith("A")]
    mesin = [r for r in rows if r["status"] == STATUS_PASIF]
    aktif = sum(1 for r in bintang
                if r["status"] == "Aktif"
                and r["aktivitas_terakhir"] != BELUM_ADA)
    aktif_sebagian = sum(1 for r in bintang if r["status"] == "Aktif sebagian")
    belum_jalan = sum(1 for r in bintang
                      if r["status"] == "Aktif"
                      and r["aktivitas_terakhir"] == BELUM_ADA)
    handoff = _baca_json(folder / "handoff.json", [])
    menunggu = [h for h in handoff if h.get("status") in ("draf", "diperiksa")]
    toko = _baca_json(folder / "penjualan_toko.json", {}).get("toko", [])
    toko_draf = [t for t in toko if t.get("status") == "draf"]
    return {"total_agent": len(bintang),
            "total_baris": len(rows),
            "aktif": aktif,
            "aktif_sebagian": aktif_sebagian,
            "belum_jalan": belum_jalan,
            "mesin_pasif": len(mesin),
            "terkendala": len(tugas_terkendala(folder)),
            "handoff_menunggu": len(menunggu),
            "penawaran_toko_draf": len(toko_draf),
            "entri_log": len(_baca_json(folder / LOG_FILE_NAMA, []))}


def target_harian_dashboard(base=None, tanggal=None):
    """Target harian SOP per agent Bintang + realisasi hari itu.

    Satu baris per agent: kode, nama, divisi, tugas_harian, target_harian
    (dari sop_harian di agents.json), jalan_hari_ini (jumlah run mesin
    pada tanggal itu), draf_menunggu (run hari itu yang menunggu
    persetujuan), jalan (True bila ada run hari itu).
    tanggal: 'YYYY-MM-DD' (WIB); default hari ini. Target SOP umumnya
    kualitatif — tercapai tidaknya dinilai di QC 11.30, bukan dari angka
    di sini. Jujur: kerja lewat Muse tanpa mesin tidak tercatat di sini.
    """
    folder = Path(base) if base else BASE
    if tanggal is None:
        tanggal = _waktu_sekarang()[:10]
    data = _baca_json(folder / "agents.json", {})
    b30 = (data.get("agent_30") or {}).get("agents", [])
    log = _baca_json(folder / LOG_MESIN_NAMA, [])
    rows = []
    for e in b30:
        kode = e.get("code", "")
        jalan = [x for x in log
                 if x.get("kode_agent") == kode
                 and str(x.get("waktu_selesai", ""))[:10] == tanggal]
        rows.append({"kode": kode, "nama": e.get("name", ""),
                     "divisi": e.get("division", ""),
                     "tugas_harian": e.get("tugas_harian", "—"),
                     "target_harian": e.get("target_harian", "—"),
                     "jalan_hari_ini": len(jalan),
                     "draf_menunggu": sum(
                         1 for x in jalan
                         if x.get("status") == "menunggu persetujuan"),
                     "jalan": bool(jalan)})
    return rows


def tugas_menunggu(base=None):
    """Tugas yang menunggu: handoff draf/diperiksa + draf penawaran toko.

    Jujur: handoff.json tidak mencatat tanggal, jadi tidak ada daftar
    "tugas hari ini" bertanggal — yang ada adalah antrean tugas menunggu.
    """
    folder = Path(base) if base else BASE
    handoff = _baca_json(folder / "handoff.json", [])
    menunggu = [{"id": h.get("id", "?"), "jenis": h.get("jenis", "?"),
                 "dari": str(h.get("dari_agent", "?")),
                 "ke": str(h.get("ke_agent", "?")),
                 "ringkasan": h.get("ringkasan", ""),
                 "status": h.get("status", "?")}
                for h in handoff if h.get("status") in ("draf", "diperiksa")]
    toko = _baca_json(folder / "penjualan_toko.json", {}).get("toko", [])
    toko_draf = [{"id": t.get("id", "?"), "nama": t.get("nama", "?")}
                 for t in toko if t.get("status") == "draf"]
    return {"handoff": menunggu, "penawaran_toko_draf": toko_draf,
            "catatan": ("Data handoff tidak mencatat tanggal, jadi daftar ini "
                        "adalah antrean tugas menunggu, bukan tugas bertanggal hari ini.")}


def persetujuan_menunggu(base=None):
    """Antrean yang butuh keputusan Cipta (sama dengan Approval Center tab 0)."""
    return tugas_menunggu(base)["handoff"]


# ---------------------------------------------------------------------------
# Mesin eksekusi — antrean, kendala, target 30 hari, platform
# (delegasi malas ke agents/mesin_eksekusi.py; fallback jujur bila mesin
# tidak bisa dimuat)
# ---------------------------------------------------------------------------
def _muat_mesin():
    try:
        import mesin_eksekusi as _mesin
        return _mesin
    except Exception:  # noqa: BLE001
        return None


def antrean_kerja(base=None):
    """Antrean kerja mesin: status + prioritas + tenggat + agent Bintang
    + kendala. Fallback: antrean minimal dari tugas_menunggu."""
    mesin = _muat_mesin()
    if mesin is not None:
        try:
            return mesin.antrean_kerja(base)
        except Exception:  # noqa: BLE001
            pass
    tugas = tugas_menunggu(base)
    antrean = []
    for h in tugas["handoff"]:
        antrean.append({"id": "HO-" + str(h.get("id", "?")),
                        "sumber": "handoff", "jenis": h.get("jenis", "?"),
                        "agent": "A01", "ringkasan": h.get("ringkasan", ""),
                        "status": ("menunggu" if h.get("status") == "draf"
                                   else "menunggu persetujuan"),
                        "prioritas": "normal", "tenggat": "—",
                        "tugas": {}, "sudah_diproses": False})
    for t in tugas["penawaran_toko_draf"]:
        antrean.append({"id": "TK-" + str(t.get("id", "?")),
                        "sumber": "penawaran-toko", "jenis": "draf-penawaran",
                        "agent": "A25",
                        "ringkasan": "Penawaran ke {}".format(t.get("nama", "?")),
                        "status": "menunggu", "prioritas": "normal",
                        "tenggat": "—", "tugas": {}, "sudah_diproses": False})
    return antrean


def tugas_terkendala(base=None):
    """Hanya item antrean berstatus 'terkendala' — tampil terpisah di
    Dashboard supaya Cipta langsung melihat apa yang mentok."""
    return [a for a in antrean_kerja(base) if a.get("status") == "terkendala"]


def target_30_hari(base=None):
    """Tolok ukur 30 hari Gemini (dari mesin eksekusi). Fallback: target
    + 'belum cukup data' bila mesin tidak bisa dimuat."""
    mesin = _muat_mesin()
    if mesin is not None:
        try:
            return mesin.target_30_hari(base)
        except Exception:  # noqa: BLE001
            pass
    return {"sumber": "Share Gemini #1 — Checklist Sistem 30 Hari (fallback)",
            "catatan_jujur": "Mesin eksekusi tidak bisa dimuat — realisasi tidak dihitung.",
            "target": [
                {"nama": "Produk digital selesai", "target": 15,
                 "realisasi": "belum cukup data", "satuan": "produk", "catatan": ""},
                {"nama": "Konten terbit", "target": 30,
                 "realisasi": "belum cukup data", "satuan": "konten", "catatan": ""},
                {"nama": "Followers baru", "target": 1000,
                 "realisasi": "belum cukup data", "satuan": "followers", "catatan": ""},
                {"nama": "Lomba diikuti", "target": "5–10",
                 "realisasi": "belum cukup data", "satuan": "lomba", "catatan": ""},
                {"nama": "Pemasukan pertama", "target": "500.000–2.000.000",
                 "realisasi": "belum cukup data", "satuan": "rupiah", "catatan": ""}]}


def platform_per_agent(base=None):
    """Pemetaan platform per agent Bintang (dari agents.json)."""
    mesin = _muat_mesin()
    if mesin is not None:
        try:
            return mesin.platform_per_agent(base)
        except Exception:  # noqa: BLE001
            pass
    folder = Path(base) if base else BASE
    data = _baca_json(folder / "agents.json", {})
    return [{"kode": e.get("code", ""), "nama": e.get("name", ""),
             "terhubung": (e.get("platform") or {}).get("terhubung", []),
             "belum_terhubung": (e.get("platform") or {}).get("belum_terhubung", [])}
            for e in (data.get("agent_30") or {}).get("agents", [])]


if __name__ == "__main__":
    import sys
    r = ringkasan_dashboard()
    print("Agent Bintang:", r["total_agent"], "| Aktif:", r["aktif"],
          "| Aktif sebagian:", r["aktif_sebagian"],
          "| Belum jalan:", r["belum_jalan"],
          "| Mesin pasif:", r["mesin_pasif"],
          "| Terkendala:", r["terkendala"])
    print("Handoff menunggu:", r["handoff_menunggu"],
          "| Penawaran toko draf:", r["penawaran_toko_draf"],
          "| Entri log:", r["entri_log"])
    sys.exit(0)
