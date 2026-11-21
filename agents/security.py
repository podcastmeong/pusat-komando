#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO — security.py
# Audit keamanan BACA-SAja Tahap 7 (BINTANG COMMAND CENTER 4.0),
# 21 Nov 2026.
#
# Modul ini HANYA membaca dan melaporkan. Tidak menulis, tidak
# mengubah, tidak mengirim apa pun. Nilai rahasia yang ditemukan
# TIDAK PERNAH ditampilkan — hanya nama file, nomor baris, dan nama
# pola yang cocok. Bila ada temuan, pemilik yang memutuskan
# tindakannya (mis. rotasi kunci).
# ======================================================================
"""Audit keamanan baca-saja: izin alat, rahasia bocor, backup."""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
BACKUP_DIR = Path.home() / "workspace" / "backup"

# Pola rahasia. Nilai yang cocok TIDAK PERNAH dicetak.
POLA_RAHASIA = [
    ("google_api_key", re.compile(r"AIza[0-9A-Za-z_\-]{10,}")),
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{10,}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{10,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("kunci_bernilai", re.compile(
        r"(?i)(api[_-]?key|secret|passwd|password|access[_-]?token)"
        r"\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
]

LEWATI_DIR = {"__pycache__", ".git", ".venv", "venv"}
LEWATI_SUFFIX = {".pyc", ".pyo", ".db", ".sqlite", ".xlsx", ".docx",
                 ".png", ".jpg", ".jpeg", ".webp", ".gz", ".zip", ".svg"}
LEWATI_FILE = {"security.py"}  # modul ini sendiri


def periksa_izin() -> dict:
    """Periksa Tool Registry: daftar larangan utuh + tidak ada alat kirim/bayar."""
    try:
        import tool_registry as tr
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"tool_registry tidak bisa diimpor: {e}"}
    larangan = list(getattr(tr, "DAFTAR_TERLARANG", []))
    kunci_wajib = {"kirim", "bayar", "publikasi", "submit", "upload", "hapus"}
    hilang = sorted(kunci_wajib - {str(x).lower() for x in larangan})
    alat = getattr(tr, "ALAT_BAWAAN", {})
    alat_mencurigakan = [nama for nama in alat
                         if any(k in nama.lower() for k in kunci_wajib)]
    cek_kirim = None
    try:
        cek_kirim = tr.cek_izin("A01", "kirim")
    except TypeError:
        try:
            cek_kirim = tr.cek_izin("kirim")
        except Exception:
            cek_kirim = None
    except Exception:
        cek_kirim = None
    ok = not hilang and not alat_mencurigakan and cek_kirim is False
    return {
        "ok": ok,
        "daftar_terlarang_jumlah": len(larangan),
        "larangan_hilang": hilang,
        "alat_mencurigakan": alat_mencurigakan,
        "cek_izin_kirim": cek_kirim,
        "jumlah_alat": len(alat),
    }


# Nilai yang jelas-jelas placeholder dokumentasi (bukan kunci asli).
PENANDA_PLACEHOLDER = ("<", ">", "xxx", "contoh", "changeme", "your_",
                       "your-", "masukkan", "ganti", "placeholder",
                       "kunci", "disini", "di_sini", "rahasia-anda")


def _placeholder(nilai: str) -> bool:
    rendah = nilai.lower()
    return any(p in rendah for p in PENANDA_PLACEHOLDER)


def _boleh_pindai(path: Path) -> bool:
    if path.name in LEWATI_FILE:
        return False
    if path.suffix.lower() in LEWATI_SUFFIX:
        return False
    return not any(b in path.parts for b in LEWATI_DIR)


def periksa_rahasia() -> dict:
    """Pindai repo dari pola kunci/API key. Nilai TIDAK PERNAH ditampilkan."""
    temuan = []
    placeholder = 0
    file_dipindai = 0
    for f in sorted(BASE.rglob("*")):
        if not f.is_file() or not _boleh_pindai(f):
            continue
        try:
            teks = f.read_text(errors="strict")
        except Exception:
            continue
        file_dipindai += 1
        for nomor, baris in enumerate(teks.splitlines(), start=1):
            for nama_pola, pola in POLA_RAHASIA:
                cocok = pola.search(baris)
                if cocok:
                    # Nilai yang cocok TIDAK PERNAH disimpan/ditampilkan;
                    # hanya dipakai untuk membedakan placeholder vs kunci asli.
                    nilai = cocok.group(0)
                    if _placeholder(nilai):
                        placeholder += 1
                    else:
                        temuan.append({
                            "file": str(f.relative_to(BASE)),
                            "baris": nomor,
                            "pola": nama_pola,
                        })
                    break
    return {
        "ok": len(temuan) == 0,
        "file_dipindai": file_dipindai,
        "temuan_jumlah": len(temuan),
        "temuan": temuan[:50],
        "placeholder_dilewati": placeholder,
    }


def periksa_backup() -> dict:
    """Kapan backup terakhir (baca ~/workspace/backup/)."""
    if not BACKUP_DIR.is_dir():
        return {"ok": False, "keterangan": "folder backup belum ada"}
    arsip = sorted(BACKUP_DIR.glob("pusat-komando-*.tar.gz"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not arsip:
        return {"ok": False, "keterangan": "belum ada arsip backup"}
    from datetime import datetime
    terbaru = arsip[0]
    return {
        "ok": True,
        "jumlah_arsip": len(arsip),
        "terakhir": terbaru.name,
        "waktu": datetime.fromtimestamp(
            terbaru.stat().st_mtime).isoformat(timespec="seconds"),
        "ukuran_byte": terbaru.stat().st_size,
    }


def audit() -> dict:
    """Jalankan semua pemeriksaan. Kembalikan dict hasil."""
    return {
        "izin": periksa_izin(),
        "rahasia": periksa_rahasia(),
        "backup": periksa_backup(),
    }


def ringkasan() -> str:
    """Ringkasan teks satu baris per pemeriksaan."""
    hasil = audit()
    izin = hasil["izin"]
    rah = hasil["rahasia"]
    bak = hasil["backup"]
    baris = []
    baris.append("Izin alat: " + ("OK (larangan utuh, kirim ditolak)"
                                  if izin.get("ok") else
                                  f"PERIKSA (hilang: {izin.get('larangan_hilang')}, "
                                  f"alat mencurigakan: {izin.get('alat_mencurigakan')})"))
    baris.append(f"Rahasia: {rah['temuan_jumlah']} temuan "
                 f"dari {rah['file_dipindai']} file dipindai "
                 f"({rah.get('placeholder_dilewati', 0)} placeholder dilewati)"
                 + ("" if rah["ok"] else " — PERLU TINDAKAN"))
    baris.append("Backup: " + (f"terakhir {bak.get('terakhir')} "
                               f"({bak.get('waktu')})" if bak.get("ok")
                               else bak.get("keterangan", "tidak ada")))
    return " | ".join(baris)


def info() -> dict:
    return {
        "modul": "security",
        "versi": "Tahap 7 — 21 Nov 2026",
        "sifat": "baca-saja; tidak menulis, tidak mengirim",
        "pemeriksaan": ["izin alat", "rahasia bocor", "backup"],
        "catatan": "Nilai rahasia tidak pernah ditampilkan.",
    }


def contoh() -> dict:
    """Mode contoh — tidak memindai, hanya gambaran."""
    return {
        "mode": "contoh",
        "akan_memeriksa": ["izin alat", "rahasia bocor", "backup"],
        "pola_rahasia": [nama for nama, _ in POLA_RAHASIA],
    }


def jalankan() -> dict:
    return audit()


if __name__ == "__main__":
    import json
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
