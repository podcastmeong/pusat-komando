#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO 2.0 — execution_engine.py
# Execution Engine 3.1 — FREE EDITION (21 Nov 2026, perintah Cipta
# "Eksekusi", rencana ChatGPT "AI BUSINESS AUTONOMOUS AGENT 3.1 –
# FREE EDITION").
#
# Satu komando menjalankan tugas agen -> simpan hasil -> kembalikan
# terstruktur. Standar 6 kemampuan (ChatGPT):
#   READ — baca data yang dibutuhkan (memori bersama / file).
#   THINK — analisis di dalam fungsi handler modul agen.
#   EXECUTE — jalankan handler modul agen (hanya fungsi baca/draf).
#   SAVE — simpan hasil ke ingatan bersama (riwayat tugas + memori).
#   REPORT — kembalikan dict hasil terstruktur.
#   HANDOFF — teruskan ke agen berikutnya bila payload berisi
#             "lanjut_ke".
#
# SIFAT: modul PASIF. Tidak berjalan sendiri; dipanggil Muse/cron.
# Handler yang terdaftar HANYA fungsi baca/draf dari modul agen
# (info/ringkasan/cek/baca/draf). TIDAK ADA handler kirim/bayar/
# publikasi/submit/upload/hapus — tugas seperti itu DITOLAK
# sebelum dieksekusi (fail-closed). Semua hasil adalah DRAF untuk
# persetujuan Cipta.
# ======================================================================
"""Execution Engine 3.1 — satu komando, hasil terstruktur."""

import importlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Handler yang diizinkan: (modul, fungsi). Semuanya fungsi baca/draf.
# Agen tanpa handler -> tugas dicatat, hasil "belum ada handler".
HANDLER = {
    "A09": ("b09_competitor_analyst", "ringkasan"),
    "A25": ("b25_sales_manager", "ringkasan"),
    "A28": ("b28_opportunity_hunter", "ringkasan"),
    "A01": ("b01_ceo_director", "ringkasan"),
    "A05": ("b05_business_analyst", "ringkasan"),
    "A06": ("b06_market_researcher", "ringkasan"),
    "A11": ("b11_ai_video_producer", "ringkasan"),
    "A13": ("b13_app_developer", "ringkasan"),
    "A14": ("b14_web_developer", "ringkasan"),
    "A16": ("b16_ebook_publisher", "ringkasan"),
    "A02": ("b02_coo_manager", "ringkasan"),
    "A03": ("b03_command_controller", "ringkasan"),
    "A04": ("b04_quality_control", "ringkasan"),
    "A07": ("b07_trend_hunter", "ringkasan"),
    "A08": ("b08_product_developer", "ringkasan"),
    "A10": ("b10_product_validator", "ringkasan"),
    "A12": ("b12_ai_image_designer", "ringkasan"),
    "A15": ("b15_pod_designer", "ringkasan"),
    "A17": ("b17_creative_writer", "ringkasan"),
    "A18": ("b18_game_developer", "ringkasan"),
    "A19": ("b19_content_producer", "ringkasan"),
    "A20": ("b20_instagram_manager", "ringkasan"),
    "A21": ("b21_tiktok_manager", "ringkasan"),
    "A22": ("b22_youtube_manager", "ringkasan"),
    "A23": ("b23_threads_manager", "ringkasan"),
    "A24": ("b24_seo_growth", "ringkasan"),
    "A26": ("b26_customer_service", "ringkasan"),
    "A27": ("b27_email_administrator", "ringkasan"),
    "A29": ("b29_finance_manager", "ringkasan"),
    "A30": ("b30_operations_manager", "ringkasan"),
    # 3.1-ext 21 Nov 2026 ("Ke semua ai"): 20 handler baru di atas
# (A02, A03, A04, A07, A08, A10, A12, A15, A17, A18, A19, A20, A21,
# A22, A23, A24, A26, A27, A29, A30) -> ringkasan(). A31-A36 tidak
# didaftarkan (tidak punya file modul b31-b33; b34-b36 bukan Bintang).
# A33 tidak punya file modul (b33_pertumbuhan.py tidak ada) —
    # sengaja tidak didaftarkan sampai modulnya dibuat.
}

JENIS_TERLARANG = [
    "kirim", "send", "bayar", "pay", "beli", "purchase", "publikasi",
    "publish", "upload", "submit", "daftar_lomba", "hapus", "delete",
    "transfer",
]


def _terlarang(teks):
    rendah = str(teks).lower()
    return any(k in rendah for k in JENIS_TERLARANG)


def _memori():
    try:
        import memori_bersama

        return memori_bersama
    except ImportError:
        return None


def jalankan_tugas(agen, tugas, payload=None):
    """Jalankan satu tugas agen lewat 6 kemampuan.

    Mengembalikan dict: ok, agen, tugas, kemampuan (6 tahap + status
    tiap tahap), hasil, lanjut_ke (bila handoff), error.
    """
    payload = payload or {}
    kemampuan = {}
    # 1. READ — baca konteks dari memori bersama (bila ada).
    mem = _memori()
    konteks = []
    if mem is not None:
        try:
            konteks = mem.baca(jenis="aturan", limit=5)
            kemampuan["READ"] = "ok (memori bersama dibaca)"
        except Exception as e:  # noqa: BLE001
            kemampuan["READ"] = f"memori gagal dibaca: {e}"
    else:
        kemampuan["READ"] = "memori_bersama tidak tersedia — lanjut tanpa konteks"
    # 2. THINK + 3. EXECUTE — tolak dulu bila jenis tugas terlarang.
    if _terlarang(tugas) or _terlarang(payload.get("jenis", "")):
        return {
            "ok": False,
            "agen": agen,
            "tugas": tugas,
            "kemampuan": {**kemampuan, "THINK": "ditolak",
                          "EXECUTE": "ditolak"},
            "hasil": "",
            "error": "DITOLAK: tugas mengandung tindakan keluar/uang "
                     "(kirim/bayar/publikasi/submit/upload/hapus).",
        }
    kemampuan["THINK"] = "ok (analisis di handler modul agen)"
    if agen not in HANDLER:
        hasil = (f"Agen {agen} belum punya handler di Execution Engine — "
                 "tugas dicatat, dikerjakan manual oleh Muse.")
        kemampuan["EXECUTE"] = "belum ada handler"
    else:
        modul_nama, fungsi_nama = HANDLER[agen]
        try:
            modul = importlib.import_module(modul_nama)
            fungsi = getattr(modul, fungsi_nama)
            hasil = fungsi()
            kemampuan["EXECUTE"] = f"ok ({modul_nama}.{fungsi_nama})"
        except Exception as e:  # noqa: BLE001
            return {
                "ok": False,
                "agen": agen,
                "tugas": tugas,
                "kemampuan": {**kemampuan, "EXECUTE": f"gagal: {e}"},
                "hasil": "",
                "error": f"{type(e).__name__}: {e}",
            }
    # 4. SAVE — simpan riwayat tugas ke ingatan bersama.
    if mem is not None:
        try:
            mem.catat_tugas(agen, tugas, str(hasil)[:2000], "selesai")
            kemampuan["SAVE"] = "ok (riwayat tugas tersimpan)"
        except Exception as e:  # noqa: BLE001
            kemampuan["SAVE"] = f"gagal disimpan: {e}"
    else:
        kemampuan["SAVE"] = "memori tidak tersedia — hasil hanya dikembalikan"
    # 5. REPORT — hasil terstruktur (di bawah).
    kemampuan["REPORT"] = "ok"
    # 6. HANDOFF — teruskan bila payload berisi lanjut_ke.
    lanjut_ke = payload.get("lanjut_ke")
    if lanjut_ke:
        kemampuan["HANDOFF"] = f"ok (diteruskan ke {lanjut_ke})"
    else:
        kemampuan["HANDOFF"] = "tidak ada (tugas selesai di sini)"
    return {
        "ok": True,
        "agen": agen,
        "tugas": tugas,
        "kemampuan": kemampuan,
        "hasil": hasil,
        "lanjut_ke": lanjut_ke or "",
        "error": "",
    }


def jalankan_antrean(maks_tugas=5):
    """Ambil tugas dari Task Queue dan jalankan satu per satu.

    Mengembalikan daftar hasil. Tugas yang gagal ditandai coba_lagi.
    """
    import task_queue

    hasil_semua = []
    for _ in range(int(maks_tugas)):
        tugas = task_queue.ambil_berikutnya()
        if tugas is None:
            break
        hasil = jalankan_tugas(tugas["agen"], tugas["tugas"],
                               tugas.get("payload") or {})
        if hasil["ok"]:
            task_queue.tandai_selesai(tugas["id"], str(hasil.get("hasil"))[:500])
        else:
            task_queue.tandai_gagal(tugas["id"], hasil.get("error", ""),
                                    coba_lagi=True)
        hasil_semua.append({"id": tugas["id"], **hasil})
    return hasil_semua


def info():
    return {
        "modul": "execution_engine",
        "versi": "3.1 FREE EDITION",
        "kemampuan_standar": ["READ", "THINK", "EXECUTE", "SAVE",
                              "REPORT", "HANDOFF"],
        "handler_terdaftar": sorted(HANDLER),
        "catatan": "Hanya handler baca/draf. Tidak ada kirim/bayar/"
                   "publikasi/submit/upload/hapus.",
    }


if __name__ == "__main__":
    print(json.dumps(info(), ensure_ascii=False, indent=2))
