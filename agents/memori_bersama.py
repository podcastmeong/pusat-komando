"""BINTANG COMMAND CENTER — Memori Bersama antar agen (shared memory).

Dibuat 21 Nov 2026 atas perintah Cipta ("Gimana cara untuk ingatan bersama
antar agent"). GRATIS: Python + SQLite saja, tanpa layanan berbayar.

CARA PAKAI (untuk semua modul agen b01..b36):
    import memori_bersama as MB
    MB.simpan("A09", "harga_pesaing", "sribu:video-promo-15dtk", {...}, sumber="https://www.sribu.com")
    MB.baca(jenis="harga_pesaing")            # semua harga pesaing yang pernah dicatat
    MB.baca(kunci="toko:lead-01")             # satu fakta
    MB.cari("pet shop")                       # cari di kunci + nilai
    MB.catat_tugas("A25", "draf penawaran 7 toko", "7 draf dibuat", "selesai")
    MB.riwayat_tugas("A25")                   # riwayat tugas satu agen

ATURAN PAKAI:
- Modul ini PASIF seperti agen lain: hanya baca/tulis data. TIDAK PUNYA
  fungsi kirim / bayar / publikasi / submit apa pun, sengaja.
- JANGAN simpan kata sandi, kode OTP/verifikasi, NIK/nomor KTP, nomor
  rekening, atau data identitas lain ke database ini. Bila data JSON yang
  dimigrasi mengandung kontak toko (IG/WhatsApp publik dari pencarian web),
  itu disalin apa adanya — bukan data identitas Cipta.
- Bila data kurang, tulis "belum cukup data" — jangan mengarang.
- Database: data/memori_bersama.db (SQLite). File JSON asli di data/
  TIDAK dihapus — database ini salinan bersama yang bisa dibaca semua agen.

SKEMA:
- agen(kode, nama, peran, status, instruksi, diperbarui)
- memori(id, jenis, kunci, nilai, sumber, tanggal, agen_pencatat)
  UNIQUE(jenis, kunci) — simpan() menimpa fakta lama dengan yang baru.
- riwayat_tugas(id, agen, tugas, hasil, status, waktu)
- izin_alat(id, agen, alat, boleh) UNIQUE(agen, alat)
  Default: kirim/bayar/publikasi/submit = TIDAK BOLEH untuk semua agen;
  baca/tulis memori = BOLEH.
"""
import json
import sqlite3
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
DB_PATH = BASE / "memori_bersama.db"

SKEMA = """
CREATE TABLE IF NOT EXISTS agen (
    kode TEXT PRIMARY KEY,
    nama TEXT,
    peran TEXT,
    status TEXT,
    instruksi TEXT,
    diperbarui TEXT
);
CREATE TABLE IF NOT EXISTS memori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jenis TEXT NOT NULL,
    kunci TEXT NOT NULL,
    nilai TEXT NOT NULL,
    sumber TEXT DEFAULT '',
    tanggal TEXT DEFAULT '',
    agen_pencatat TEXT DEFAULT '',
    UNIQUE(jenis, kunci)
);
CREATE TABLE IF NOT EXISTS riwayat_tugas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agen TEXT NOT NULL,
    tugas TEXT NOT NULL,
    hasil TEXT DEFAULT '',
    status TEXT DEFAULT 'selesai',
    waktu TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS izin_alat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agen TEXT NOT NULL,
    alat TEXT NOT NULL,
    boleh INTEGER NOT NULL DEFAULT 0,
    UNIQUE(agen, alat)
);
"""

ALAT_TERLARANG = ["kirim", "bayar", "publikasi", "submit"]
ALAT_MEMORI = ["baca_memori", "tulis_memori"]


def _koneksi(db_path=None):
    p = Path(db_path) if db_path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.row_factory = sqlite3.Row
    return con


def init_db(db_path=None):
    """Buat tabel bila belum ada. Kembalikan path database."""
    con = _koneksi(db_path)
    try:
        con.executescript(SKEMA)
        con.commit()
    finally:
        con.close()
    return str(Path(db_path) if db_path else DB_PATH)


def simpan(agen, jenis, kunci, nilai, sumber="", tanggal=None, db_path=None):
    """Simpan satu fakta. nilai boleh str/dict/list (dict/list disimpan JSON).
    Bila (jenis, kunci) sudah ada, ditimpa. Kembalikan True bila tersimpan."""
    if not (jenis or "").strip() or not (kunci or "").strip():
        return False
    if isinstance(nilai, (dict, list)):
        nilai = json.dumps(nilai, ensure_ascii=False)
    nilai = str(nilai)
    tgl = tanggal or date.today().isoformat()
    con = _koneksi(db_path)
    try:
        con.execute(
            "INSERT INTO memori (jenis, kunci, nilai, sumber, tanggal, agen_pencatat)"
            " VALUES (?,?,?,?,?,?)"
            " ON CONFLICT(jenis, kunci) DO UPDATE SET"
            " nilai=excluded.nilai, sumber=excluded.sumber,"
            " tanggal=excluded.tanggal, agen_pencatat=excluded.agen_pencatat",
            ((jenis or "").strip(), (kunci or "").strip(), nilai,
             (sumber or "").strip(), tgl, (agen or "").strip()))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


def baca(kunci=None, jenis=None, agen=None, limit=100, db_path=None):
    """Baca fakta dari memori bersama. Tanpa argumen = semua (dibatasi limit).
    Kembalikan list dict: jenis, kunci, nilai, sumber, tanggal, agen_pencatat.
    nilai yang tersimpan sebagai JSON dikembalikan sebagai dict/list."""
    con = _koneksi(db_path)
    try:
        sql = "SELECT jenis, kunci, nilai, sumber, tanggal, agen_pencatat FROM memori"
        where, params = [], []
        if kunci:
            where.append("kunci = ?")
            params.append(kunci)
        if jenis:
            where.append("jenis = ?")
            params.append(jenis)
        if agen:
            where.append("agen_pencatat = ?")
            params.append(agen)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY jenis, kunci LIMIT ?"
        params.append(int(limit))
        rows = []
        for r in con.execute(sql, params):
            d = dict(r)
            try:
                d["nilai"] = json.loads(d["nilai"])
            except Exception:
                pass
            rows.append(d)
        return rows
    except Exception:
        return []
    finally:
        con.close()


def cari(kata, limit=50, db_path=None):
    """Cari kata kunci di kunci + nilai. Kembalikan list dict seperti baca()."""
    kata = "%{}%".format((kata or "").strip())
    if kata == "%%":
        return []
    con = _koneksi(db_path)
    try:
        rows = []
        for r in con.execute(
                "SELECT jenis, kunci, nilai, sumber, tanggal, agen_pencatat"
                " FROM memori WHERE kunci LIKE ? OR nilai LIKE ?"
                " ORDER BY jenis, kunci LIMIT ?",
                (kata, kata, int(limit))):
            d = dict(r)
            try:
                d["nilai"] = json.loads(d["nilai"])
            except Exception:
                pass
            rows.append(d)
        return rows
    except Exception:
        return []
    finally:
        con.close()


def catat_tugas(agen, tugas, hasil="", status="selesai", db_path=None):
    """Catat satu tugas yang dikerjakan agen ke riwayat_tugas."""
    if not (agen or "").strip() or not (tugas or "").strip():
        return False
    con = _koneksi(db_path)
    try:
        con.execute(
            "INSERT INTO riwayat_tugas (agen, tugas, hasil, status, waktu)"
            " VALUES (?,?,?,?,?)",
            ((agen or "").strip(), (tugas or "").strip(), str(hasil or ""),
             (status or "selesai").strip(),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


def riwayat_tugas(agen=None, limit=50, db_path=None):
    """Baca riwayat tugas. Bila agen diisi, hanya tugas agen itu."""
    con = _koneksi(db_path)
    try:
        if agen:
            cur = con.execute(
                "SELECT agen, tugas, hasil, status, waktu FROM riwayat_tugas"
                " WHERE agen = ? ORDER BY id DESC LIMIT ?",
                (agen, int(limit)))
        else:
            cur = con.execute(
                "SELECT agen, tugas, hasil, status, waktu FROM riwayat_tugas"
                " ORDER BY id DESC LIMIT ?", (int(limit),))
        return [dict(r) for r in cur]
    except Exception:
        return []
    finally:
        con.close()


def profil_agen(kode, nama="", peran="", status="", instruksi="",
               diperbarui=None, db_path=None):
    """Simpan/perbarui profil satu agen di tabel agen."""
    if not (kode or "").strip():
        return False
    con = _koneksi(db_path)
    try:
        con.execute(
            "INSERT INTO agen (kode, nama, peran, status, instruksi, diperbarui)"
            " VALUES (?,?,?,?,?,?)"
            " ON CONFLICT(kode) DO UPDATE SET nama=excluded.nama,"
            " peran=excluded.peran, status=excluded.status,"
            " instruksi=excluded.instruksi, diperbarui=excluded.diperbarui",
            ((kode or "").strip(), (nama or "").strip(), (peran or "").strip(),
             (status or "").strip(), (instruksi or "").strip(),
             diperbarui or date.today().isoformat()))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


def daftar_agen(db_path=None):
    """Kembalikan semua profil agen (kode, nama, peran, status)."""
    con = _koneksi(db_path)
    try:
        cur = con.execute(
            "SELECT kode, nama, peran, status, instruksi, diperbarui"
            " FROM agen ORDER BY kode")
        return [dict(r) for r in cur]
    except Exception:
        return []
    finally:
        con.close()


def atur_izin(agen, alat, boleh, db_path=None):
    """Atur izin alat untuk satu agen. boleh=True/False."""
    if not (agen or "").strip() or not (alat or "").strip():
        return False
    con = _koneksi(db_path)
    try:
        con.execute(
            "INSERT INTO izin_alat (agen, alat, boleh) VALUES (?,?,?)"
            " ON CONFLICT(agen, alat) DO UPDATE SET boleh=excluded.boleh",
            ((agen or "").strip(), (alat or "").strip(), 1 if boleh else 0))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


def cek_izin(agen, alat, db_path=None):
    """Cek apakah agen boleh memakai alat. Default: TIDAK BOLEH bila belum
    diatur (fail-closed — aman)."""
    con = _koneksi(db_path)
    try:
        r = con.execute(
            "SELECT boleh FROM izin_alat WHERE agen = ? AND alat = ?",
            ((agen or "").strip(), (alat or "").strip())).fetchone()
        return bool(r["boleh"]) if r else False
    except Exception:
        return False
    finally:
        con.close()


def _izin_default(db_path=None):
    """Isi izin default untuk semua agen di tabel agen: kirim/bayar/
    publikasi/submit = TIDAK BOLEH; baca/tulis memori = BOLEH."""
    for a in daftar_agen(db_path):
        for alat in ALAT_TERLARANG:
            atur_izin(a["kode"], alat, False, db_path)
        for alat in ALAT_MEMORI:
            atur_izin(a["kode"], alat, True, db_path)


def migrasi(db_path=None):
    """Migrasi 4 file JSON di data/ ke database. File JSON ASLI TIDAK dihapus.
    Kembalikan dict jumlah baris per file + catatan apa adanya."""
    hasil = {"leads.json": 0, "referensi_kompetitor.json": 0,
             "status_agent.json": 0, "approvals.json": 0, "catatan": []}
    init_db(db_path)

    # 1. leads.json — 27 toko -> memori jenis "toko"
    try:
        data = json.loads((BASE / "leads.json").read_text(encoding="utf-8"))
        leads = data.get("leads", []) if isinstance(data, dict) else []
        tgl = data.get("_tanggal_acuan_follow_up", "") if isinstance(data, dict) else ""
        for lead in leads:
            if not isinstance(lead, dict) or not lead.get("id"):
                continue
            simpan("A25", "toko", "toko:{}".format(lead["id"]), lead,
                   sumber="leads.json", tanggal=tgl or None, db_path=db_path)
            hasil["leads.json"] += 1
        if isinstance(data, dict) and data.get("_aturan_skor_minat"):
            simpan("A25", "aturan", "aturan_skor_minat",
                   data["_aturan_skor_minat"], sumber="leads.json",
                   tanggal=tgl or None, db_path=db_path)
            hasil["leads.json"] += 1
    except Exception as e:
        hasil["catatan"].append("leads.json gagal dibaca: {}".format(e))

    # 2. referensi_kompetitor.json — 1 referensi -> memori jenis "referensi_kompetitor"
    try:
        data = json.loads((BASE / "referensi_kompetitor.json").read_text(encoding="utf-8"))
        for ref in (data if isinstance(data, list) else []):
            if not isinstance(ref, dict):
                continue
            kunci = "referensi:{}".format(ref.get("id") or ref.get("judul") or "?")
            simpan("A09", "referensi_kompetitor", kunci, ref,
                   sumber="referensi_kompetitor.json",
                   tanggal=ref.get("tanggal_diambil") or None, db_path=db_path)
            hasil["referensi_kompetitor.json"] += 1
    except Exception as e:
        hasil["catatan"].append("referensi_kompetitor.json gagal dibaca: {}".format(e))

    # 3. status_agent.json — 36 agen -> tabel agen
    try:
        data = json.loads((BASE / "status_agent.json").read_text(encoding="utf-8"))
        for a in (data.get("agent", []) if isinstance(data, dict) else []):
            if not isinstance(a, dict) or not a.get("kode"):
                continue
            profil_agen(a.get("kode"), nama=a.get("nama", ""),
                        peran=a.get("alasan", "")[:500],
                        status=a.get("status", ""),
                        instruksi="jalur: {}".format(a.get("jalur", "")),
                        diperbarui=a.get("diperbarui") or data.get("diperbarui"),
                        db_path=db_path)
            hasil["status_agent.json"] += 1
        simpan("A01", "aturan", "aturan_status_agent",
               data.get("aturan", "") if isinstance(data, dict) else "",
               sumber="status_agent.json",
               tanggal=data.get("diperbarui") if isinstance(data, dict) else None,
               db_path=db_path)
    except Exception as e:
        hasil["catatan"].append("status_agent.json gagal dibaca: {}".format(e))

    # 4. approvals.json — 10 persetujuan -> memori jenis "persetujuan"
    try:
        data = json.loads((BASE / "approvals.json").read_text(encoding="utf-8"))
        for ap in (data.get("approvals", []) if isinstance(data, dict) else []):
            if not isinstance(ap, dict) or not ap.get("id"):
                continue
            simpan(ap.get("agent", "A01"), "persetujuan",
                   "approval:{}".format(ap["id"]), ap,
                   sumber="approvals.json",
                   tanggal=ap.get("sejak") or None, db_path=db_path)
            hasil["approvals.json"] += 1
    except Exception as e:
        hasil["catatan"].append("approvals.json gagal dibaca: {}".format(e))

    _izin_default(db_path)
    return hasil


def contoh():
    """Contoh tulis-baca lintas agen (untuk tes)."""
    simpan("A09", "harga_pesaing", "contoh:video-promo-15dtk",
           {"pesaing": "Studio Contoh", "harga_rp": 100000,
            "sumber": "https://example.com", "tanggal_cek": "2026-11-21"},
           sumber="contoh")
    return baca(kunci="contoh:video-promo-15dtk", jenis="harga_pesaing")


if __name__ == "__main__":
    import sys
    print("Memori bersama:", init_db())
    hasil = migrasi()
    for k, v in hasil.items():
        print(" ", k, "->", v)
    print("Agen di DB:", len(daftar_agen()))
    print("Contoh tulis-baca:", contoh())
