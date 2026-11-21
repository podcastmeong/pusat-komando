#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO — backup.py
# Backup otomatis Tahap 7 (BINTANG COMMAND CENTER 4.0), 21 Nov 2026.
#
# Mengarsipkan data/ + agents/ + file kunci repo ke ~/workspace/backup/
# dengan stempel tanggal. Arsip TIDAK BOLEH di-push ke GitHub (bisa
# berisi data bisnis sensitif) dan TIDAK BOLEH dikirim ke mana pun.
# Modul ini HANYA baca + arsip lokal. Tidak ada fungsi kirim/bayar/
# publikasi/submit/upload/hapus. Retensi: 7 arsip terbaru.
# ======================================================================
"""Backup harian Pusat Komando — arsip lokal data + agents."""

import json
import tarfile
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
BACKUP_DIR = Path.home() / "workspace" / "backup"
LOG_FILE = BASE / "data" / "log_backup.json"
RETENSI = 7

SUMBER_DIR = ["data", "agents"]
FILE_KUNCI = ["app.py", "README.md", "LAPORAN.md", "LAPORAN-KOORDINASI.md",
              "requirements.txt", "workflows.json", "rencana-penerapan-3.0.md"]

LEWATI = {"__pycache__", ".git", ".venv", "venv"}


def _boleh(path: Path) -> bool:
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return not any(b in path.parts for b in LEWATI)


def _stempel() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def buat_backup() -> dict:
    """Buat satu arsip tar.gz. Kembalikan dict hasil."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    nama = f"pusat-komando-{_stempel()}.tar.gz"
    tujuan = BACKUP_DIR / nama
    jumlah = 0
    with tarfile.open(tujuan, "w:gz") as tar:
        for d in SUMBER_DIR:
            sumber = BASE / d
            if not sumber.is_dir():
                continue
            for f in sorted(sumber.rglob("*")):
                if f.is_file() and _boleh(f):
                    tar.add(f, arcname=f.relative_to(BASE))
                    jumlah += 1
        for fn in FILE_KUNCI:
            f = BASE / fn
            if f.is_file():
                tar.add(f, arcname=fn)
                jumlah += 1
    # Verifikasi: arsip bisa dibuka dan berisi file.
    with tarfile.open(tujuan, "r:gz") as tar:
        anggota = tar.getnames()
    _prune()
    hasil = {
        "ok": True,
        "arsip": str(tujuan),
        "nama": nama,
        "file": jumlah,
        "anggota_terverifikasi": len(anggota),
        "ukuran_byte": tujuan.stat().st_size,
        "waktu": datetime.now().isoformat(timespec="seconds"),
    }
    _catat_log(hasil)
    return hasil


def _prune() -> list:
    """Hapus arsip lama, sisakan RETENSI terbaru. Kembalikan yang dihapus."""
    arsip = sorted(BACKUP_DIR.glob("pusat-komando-*.tar.gz"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    dihapus = []
    for lama in arsip[RETENSI:]:
        lama.unlink()
        dihapus.append(lama.name)
    return dihapus


def _catat_log(hasil: dict) -> None:
    try:
        log = json.loads(LOG_FILE.read_text()) if LOG_FILE.exists() else []
    except Exception:
        log = []
    log.append(hasil)
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2))


def daftar_backup() -> list:
    """Daftar arsip, terbaru dulu."""
    if not BACKUP_DIR.is_dir():
        return []
    out = []
    for p in sorted(BACKUP_DIR.glob("pusat-komando-*.tar.gz"),
                    key=lambda p: p.stat().st_mtime, reverse=True):
        out.append({"nama": p.name, "ukuran_byte": p.stat().st_size,
                    "waktu": datetime.fromtimestamp(
                        p.stat().st_mtime).isoformat(timespec="seconds")})
    return out


def periksa_backup_terakhir() -> dict:
    """Kapan backup terakhir. Bila belum ada, ok=False."""
    daftar = daftar_backup()
    if not daftar:
        return {"ok": False, "keterangan": "belum ada backup"}
    return {"ok": True, **daftar[0]}


def pulihkan(nama_arsip: str, anggota: str, tujuan: str) -> dict:
    """Pulihkan SATU file dari arsip ke tujuan (uji restore).

    Menolak anggota dengan path traversal. Kembalikan dict hasil.
    """
    arsip = BACKUP_DIR / nama_arsip
    if not arsip.is_file():
        return {"ok": False, "error": f"arsip tidak ditemukan: {nama_arsip}"}
    if anggota.startswith(("/", "..")) or ".." in anggota.split("/"):
        return {"ok": False, "error": "anggota ditolak (path tidak aman)"}
    tujuan_p = Path(tujuan)
    tujuan_p.mkdir(parents=True, exist_ok=True)
    with tarfile.open(arsip, "r:gz") as tar:
        if anggota not in tar.getnames():
            return {"ok": False, "error": f"anggota tidak ada di arsip: {anggota}"}
        member = tar.getmember(anggota)
        if not member.isfile():
            return {"ok": False, "error": "anggota bukan file"}
        tar.extract(member, path=tujuan_p, filter="data")
    hasil = tujuan_p / anggota
    return {"ok": hasil.is_file(), "dipulihkan": str(hasil),
            "ukuran_byte": hasil.stat().st_size if hasil.is_file() else 0}


def info() -> dict:
    return {
        "modul": "backup",
        "versi": "Tahap 7 — 21 Nov 2026",
        "backup_dir": str(BACKUP_DIR),
        "retensi": RETENSI,
        "sumber": SUMBER_DIR + FILE_KUNCI,
        "catatan": "Arsip lokal saja. Jangan push ke GitHub, jangan kirim.",
    }


def ringkasan() -> str:
    terakhir = periksa_backup_terakhir()
    daftar = daftar_backup()
    if not terakhir["ok"]:
        return "Backup: belum ada arsip."
    return (f"Backup: {len(daftar)} arsip, terakhir {terakhir['nama']} "
            f"({terakhir['ukuran_byte']} byte, {terakhir['waktu']}).")


def contoh() -> dict:
    """Mode contoh — tidak menulis apa pun, hanya gambaran."""
    return {
        "mode": "contoh",
        "akan_mengarsipkan": SUMBER_DIR + FILE_KUNCI,
        "tujuan": str(BACKUP_DIR),
        "retensi": RETENSI,
    }


def jalankan() -> dict:
    return buat_backup()


if __name__ == "__main__":
    print(json.dumps(buat_backup(), ensure_ascii=False, indent=2))
