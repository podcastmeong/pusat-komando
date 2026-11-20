# ======================================================================
# BINTANG COMMAND CENTER — Dashboard Pergerakan Agent.
# Dibuat 21 Nov 2026 atas perintah Cipta ("Setelah ini buat dashboard
# agar aku bisa liat juga pergerakan agent").
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
# ======================================================================
import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
LOG_FILE_NAMA = "activity_log.json"
MAKS_LOG = 500
WIB = timezone(timedelta(hours=7))

# 14 agent lama (bernomor 1–14). Tim 9A–9F tercakup dalam baris Agent 9
# (mereka berbagi satu sumber kerja: worklist-73.json).
AGENT_LAMA = [
    ("1", "Asisten", "Agent lama", "Muse", "handoff"),
    ("2", "Penjualan", "Agent lama", "Muse", "leads"),
    ("3", "Pertumbuhan", "Agent lama", "Muse", "handoff"),
    ("4", "Penjualan Harian", "Agent lama", "Muse", "penjualan_toko"),
    ("5", "Produksi Produk", "Agent lama", "Muse", "produksi_game"),
    ("6", "Lomba", "Agent lama", "Muse", "lomba"),
    ("7", "Keuangan", "Agent lama", "Muse", "keuangan"),
    ("8", "Terjemah Inggris", "Agent lama", "Muse", "terjemahan"),
    ("9", "Game & Aplikasi", "Agent lama", "Muse", "worklist"),
    ("10", "Riset Produk", "Agent lama", "Muse", "riset"),
    ("11", "Oyen", "Agent lama", "Muse", "handoff"),
    ("12", "Momo", "Agent lama", "Muse", "handoff"),
    ("13", "Email", "Agent lama", "Muse", "email"),
    ("14", "Upwork", "Agent lama", "Muse", "upwork"),
]

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


def _aktivitas_agent_lama(folder, kode, sumber):
    """Kembalikan (aktivitas_terakhir, output_terakhir) dari data nyata."""
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
# Tabel gabungan 44 agent (30 Bintang + 14 lama)
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
    """Satu baris per agent: kode, nama, kelompok, dipetakan_ke, status,
    aktivitas_terakhir, output_terakhir. Sumber: agents.json + data nyata."""
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
    for kode, nama, kelompok, peta, sumber in AGENT_LAMA:
        aktivitas, output = _aktivitas_agent_lama(folder, kode, sumber)
        status = "Aktif (mode persiapan)" if kode == "14" else "Aktif"
        rows.append({"kode": kode, "nama": nama, "kelompok": kelompok,
                     "dipetakan_ke": peta, "status": status,
                     "aktivitas_terakhir": aktivitas,
                     "output_terakhir": output})
    return rows


def daftar_divisi(base=None):
    divisi = []
    for r in tabel_semua_agent(base):
        if r["kelompok"] not in divisi:
            divisi.append(r["kelompok"])
    return divisi


def ringkasan_dashboard(base=None):
    """Hitungan ringkas: Aktif / Aktif sebagian / Belum jalan + antrean."""
    folder = Path(base) if base else BASE
    rows = tabel_semua_agent(folder)
    aktif = sum(1 for r in rows
                if r["status"] == "Aktif"
                and r["aktivitas_terakhir"] != BELUM_ADA)
    aktif_sebagian = sum(1 for r in rows if r["status"] == "Aktif sebagian")
    belum_jalan = sum(1 for r in rows
                      if r["status"] == "Aktif"
                      and r["aktivitas_terakhir"] == BELUM_ADA)
    persiapan = sum(1 for r in rows if "mode persiapan" in r["status"])
    handoff = _baca_json(folder / "handoff.json", [])
    menunggu = [h for h in handoff if h.get("status") in ("draf", "diperiksa")]
    toko = _baca_json(folder / "penjualan_toko.json", {}).get("toko", [])
    toko_draf = [t for t in toko if t.get("status") == "draf"]
    return {"total_agent": len(rows),
            "aktif": aktif,
            "aktif_sebagian": aktif_sebagian,
            "belum_jalan": belum_jalan,
            "mode_persiapan": persiapan,
            "handoff_menunggu": len(menunggu),
            "penawaran_toko_draf": len(toko_draf),
            "entri_log": len(_baca_json(folder / LOG_FILE_NAMA, []))}


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


if __name__ == "__main__":
    import sys
    r = ringkasan_dashboard()
    print("Total agent:", r["total_agent"], "| Aktif:", r["aktif"],
          "| Aktif sebagian:", r["aktif_sebagian"],
          "| Belum jalan:", r["belum_jalan"],
          "| Mode persiapan:", r["mode_persiapan"])
    print("Handoff menunggu:", r["handoff_menunggu"],
          "| Penawaran toko draf:", r["penawaran_toko_draf"],
          "| Entri log:", r["entri_log"])
    sys.exit(0)
