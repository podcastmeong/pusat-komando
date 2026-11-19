# ==========================================================================
# PUSAT KOMANDO PODCAST MEONG
# Satu aplikasi gabungan 12 agent AI bernomor + 6 tim Agent 9 + workshop
# Avatar Podcast + bus Koordinasi antar-agent (21 tab) dalam SATU Space
# Gradio, berbagi satu folder data/ — supaya agent bisa membaca output
# agent lain langsung dari Papan Handoff, tanpa antre lewat Muse.
#
# Agent yang digabung (modul di agents/, salinan dari agent aslinya dengan
# path data dialihkan ke data/ bersama):
#   1 Asisten (a01) · 2 Penjualan (a02, FastAPI — dibuatkan tab Gradio di
#   sini) · 3 Pertumbuhan (a03) · 5 Produksi Produk (a05) · 6 Lomba (a06)
#   7 Keuangan (a07) · 8 Terjemah Inggris (a08) · 9 Produksi Game &
#   Aplikasi (a09) · 9A Rancang (a09a) · 9B Bangun (a09b) · 9C Jualan
#   (a09c) · 9D Bangun-2 (a09d) · 9E Bangun-3 (a09e) · 9F Verifikasi &
#   Katalog (a09f) — enam tim di bawah Agent 9 · 10 Riset Produk &
#   Strategi (a10) · 11 Oyen (a11_oyen) · 12 Momo (a12_momo) · 13 Email
#   (a13_email) · Workshop Avatar Podcast (a11, tanpa nomor)
# Agent 4 TIDAK ADA — dihapus atas perintah Cipta; upload harian ditangani
# Muse langsung.
#
# ATURAN YANG TETAP BERLAKU (SOP Kerja Sama Agent AI, berlaku 18 Nov 2026):
# - Semua output agent adalah DRAF untuk persetujuan Cipta.
# - TIDAK ADA yang otomatis upload / kirim / transfer / bayar.
# - Dilarang mengarang data pasar, ayat, hadis, atau angka; bila data kurang
#   tulis "belum cukup data". Tidak ada janji penghasilan.
# - Fokus gratis dulu: Gemini free tier via env var GEMINI_API_KEY saja;
#   tanpa key semua agent jalan mode template lokal. Tanpa layanan berbayar.
# - Telemetri Gradio dimatikan.
# ==========================================================================
import importlib
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
AGENTS_DIR = ROOT / "agents"
sys.path.insert(0, str(AGENTS_DIR))
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

HANDOFF_FILE = DATA_DIR / "handoff.json"
STATUS_HANDOFF = ["draf", "diperiksa", "disetujui", "ditolak", "selesai"]
JENIS_HANDOFF = ["product-brief", "draft-approval", "sales-lead",
                 "contest-entry", "finance-entry", "translation-job",
                 "game-pipeline", "lainnya"]
NAMA_AGENT = {1: "1 · Asisten", 2: "2 · Penjualan", 3: "3 · Pertumbuhan",
              5: "5 · Produksi Produk", 6: "6 · Lomba", 7: "7 · Keuangan",
              8: "8 · Terjemah Inggris", 9: "9 · Game & Aplikasi",
              "9A": "9A · Rancang", "9B": "9B · Bangun", "9C": "9C · Jualan",
              "9D": "9D · Bangun-2", "9E": "9E · Bangun-3",
              "9F": "9F · Verifikasi & Katalog",
              10: "10 · Riset Produk", 11: "11 · Oyen", 12: "12 · Momo",
              13: "13 · Email"}
# Urutan agent di dropdown (angka dulu, tim 9A–9F tepat setelah 9) —
# sorted() biasa tidak bisa dipakai karena kunci campuran int + str.
_URUTAN_AGENT = [1, 2, 3, 5, 6, 7, 8, 9, "9A", "9B", "9C", "9D", "9E", "9F",
                 10, 11, 12, 13]
MODE_AI = bool(os.environ.get("GEMINI_API_KEY", "").strip())


# ---------------------------------------------------------------------------
# Muat modul agent (defensif: satu agent gagal tidak menjatuhkan yang lain)
# ---------------------------------------------------------------------------
def _muat(nama_modul):
    try:
        return importlib.import_module(nama_modul), None
    except Exception as e:  # noqa: BLE001 — tampilkan sebagai tab error
        return None, "{}: {}".format(type(e).__name__, e)


A01, E01 = _muat("a01_asisten")
A02, E02 = _muat("a02_penjualan")
A03, E03 = _muat("a03_pertumbuhan")
A05, E05 = _muat("a05_produksi")
A06, E06 = _muat("a06_lomba")
A07, E07 = _muat("a07_keuangan")
A08, E08 = _muat("a08_terjemah")
A09, E09 = _muat("a09_game")
A09A, E09A = _muat("a09a_rancang")
A09B, E09B = _muat("a09b_bangun")
A09C, E09C = _muat("a09c_jualan")
A09D, E09D = _muat("a09d_bangun2")
A09E, E09E = _muat("a09e_bangun3")
A09F, E09F = _muat("a09f_verifikasi_katalog")
A10, E10 = _muat("a10_riset")
A11, E11 = _muat("a11_avatar")
A11O, E11O = _muat("a11_oyen")
A12M, E12M = _muat("a12_momo")
A13, E13 = _muat("a13_email")
KOORD, EKOORD = _muat("koordinasi")


def _blok_dari_modul(modul, getter, nama):
    """Ambil objek Blocks dari sebuah modul agent (demo / build_*)."""
    if modul is None:
        return None, "Agent {} gagal dimuat.".format(nama)
    try:
        blok = getter(modul)
        return blok, None
    except Exception as e:  # noqa: BLE001
        return None, "Agent {} gagal membangun UI: {}: {}".format(
            nama, type(e).__name__, e)


# ---------------------------------------------------------------------------
# Utilitas data bersama
# ---------------------------------------------------------------------------
def _hari_ini():
    return date.today().isoformat()


def _baca_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, type(default)) else default
    except (OSError, ValueError):
        return default


def _parse_tanggal(teks):
    try:
        return date.fromisoformat(str(teks)[:10])
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# PAPAN HANDOFF — ringkasan lintas agent dari folder data/ bersama
# ---------------------------------------------------------------------------
def tampilkan_papan():
    hari = date.today()
    baris = ["# 🏠 Papan Handoff — Pusat Komando\n",
             "Ringkasan lintas agent dari folder `data/` bersama. "
             "Mode: **{}**. Semua item di bawah ini DRAF — menunggu persetujuan Cipta.\n".format(
                 "AI penuh (Gemini)" if MODE_AI else "template lokal (tanpa API key)")]
    # --- 1. Brief riset yang layak (Agent 10 -> Agent 5) ---
    riset = _baca_json(DATA_DIR / "riset.json", [])
    layak = [e for e in riset if "layak" in str(e.get("verdict", "")).lower()]
    baris.append("## 🔍 Brief Riset (Agent 10 → Produksi)")
    if layak:
        for e in layak[:5]:
            baris.append("- **{}** — {} (skor {}/12, {})".format(
                e.get("niche", "?"), e.get("ide", "?"),
                e.get("skor", "?"), e.get("verdict", "?")))
        baris.append("\nPilih di bawah untuk mengirim brief ini ke Agent 5 (Produksi).")
    else:
        baris.append("Belum ada peluang berverdict *Layak dicoba*. "
                     "Nilai peluang dulu di tab Agent 10.")
    # --- 2. Draf produksi terbaru (Agent 5) ---
    baris.append("\n## 🎁 Draf Produksi Terbaru (Agent 5)")
    berkas = []
    for p in OUTPUT_DIR.rglob("*"):
        if p.is_file():
            berkas.append(p)
    berkas.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if berkas:
        for p in berkas[:8]:
            baris.append("- `{}` — {}".format(
                p.relative_to(ROOT), p.stat().st_mtime and
                date.fromtimestamp(p.stat().st_mtime).isoformat()))
        baris.append("\nPilih di bawah untuk mengirim draf ini ke Agent 2 (Penjualan) atau Agent 8 (Terjemah).")
    else:
        baris.append("Belum ada draf di `output/`. Buat draf dulu di tab Agent 5.")
    # --- 3. Lead penjualan (Agent 2) ---
    leads = _baca_json(DATA_DIR / "leads.json", {}).get("leads", [])
    baris.append("\n## 💼 Lead Penjualan (Agent 2)")
    if leads:
        hitung = {}
        for l in leads:
            hitung[l.get("status", "?")] = hitung.get(l.get("status", "?"), 0) + 1
        baris.append("Total **{}** lead — ".format(len(leads)) +
                     ", ".join("{}: {}".format(k, v) for k, v in sorted(hitung.items())))
        belum_verif = sum(1 for l in leads if not l.get("terverifikasi"))
        baris.append("Belum terverifikasi: **{}** (kontak harus dicek ulang sebelum dihubungi).".format(belum_verif))
        for l in [x for x in leads if x.get("status") == "baru"][:5]:
            baris.append("- {} ({})".format(l.get("nama", "?"), l.get("jenis", "?")))
    else:
        baris.append("Belum ada lead.")
    # --- 4. Tenggat lomba ≤ 14 hari (Agent 6) ---
    lomba = _baca_json(DATA_DIR / "lomba.json", [])
    baris.append("\n## 🏆 Tenggat Lomba ≤ 14 Hari (Agent 6)")
    dekat = []
    for l in lomba:
        t = _parse_tanggal(l.get("tenggat", ""))
        if t and 0 <= (t - hari).days <= 14 and l.get("status") not in ("selesai", "ditolak"):
            dekat.append((t, l))
    if dekat:
        for t, l in sorted(dekat, key=lambda x: x[0]):
            baris.append("- **{}** — tenggat {} ({} hari lagi, {}, AI: {})".format(
                l.get("nama", "?"), t.isoformat(), (t - hari).days,
                l.get("status", "?"), l.get("kebijakan_ai", "?")))
    else:
        baris.append("Tidak ada tenggat lomba dalam 14 hari ke depan.")
    # --- 5. Keuangan (Agent 7) ---
    keu = _baca_json(DATA_DIR / "keuangan_data.json", {})
    entries = keu.get("entries", []) if isinstance(keu, dict) else []
    baris.append("\n## 💰 Uang Masuk (Agent 7)")
    if entries:
        total_rp = sum(float(e.get("jumlah", 0) or 0) for e in entries
                       if str(e.get("mata_uang", "")).upper() in ("IDR", "RP", ""))
        total_usd = sum(float(e.get("jumlah", 0) or 0) for e in entries
                        if str(e.get("mata_uang", "")).upper() == "USD")
        baris.append("Tercatat **{}** pemasukan — total Rp{:,.0f} + ${:,.2f}.".format(
            len(entries), total_rp, total_usd))
    else:
        baris.append("Titik awal: **{}**".format(
            keu.get("baseline_catatan", "Rp0 / $0 di semua platform per 18 Nov 2026.")))
    # --- 6. Terjemah (Agent 8) ---
    prog = _baca_json(DATA_DIR / "terjemah_progress.json", {})
    baris.append("\n## 🌍 Progres Terjemah (Agent 8)")
    if prog:
        hitung = {}
        for v in prog.values():
            hitung[str(v)] = hitung.get(str(v), 0) + 1
        baris.append(", ".join("{}: {}".format(k, v) for k, v in sorted(hitung.items())))
    else:
        baris.append("Belum ada progres terjemahan yang dicatat.")
    # --- 7. Proyek game/aplikasi (Agent 9) ---
    proyek = _baca_json(DATA_DIR / "game_data.json", [])
    baris.append("\n## 🎮 Proyek Game & Aplikasi (Agent 9)")
    if proyek:
        for p in proyek[:8]:
            baris.append("- **{}** ({} — {})".format(
                p.get("nama", "?"), p.get("jenis", "?"), p.get("status", "?")))
    else:
        baris.append("Belum ada proyek game/aplikasi yang dilacak.")
    # --- 7b. Alur produksi game/aplikasi (tim 9A → 9B/9D/9E → 9F → 9C) ---
    pipa = _baca_json(DATA_DIR / "produksi_game.json", [])
    baris.append("\n## 🛠️ Alur Produksi Game & Aplikasi (9A → 9B/9D/9E → 9F → 9C)")
    if pipa:
        hitung = {}
        for p in pipa:
            hitung[p.get("status", "?")] = hitung.get(p.get("status", "?"), 0) + 1
        baris.append("Total **{}** proyek — ".format(len(pipa)) +
                     ", ".join("{}: {}".format(k, v) for k, v in sorted(hitung.items())))
        klaim_aktif = [(p.get("nama", "?"), (p.get("klaim") or {}).get("oleh", "?"))
                       for p in pipa if (p.get("klaim") or {}).get("oleh")]
        if klaim_aktif:
            baris.append("Klaim bangun aktif (satu proyek = satu tim): " +
                         ", ".join("{} (tim {})".format(n, t) for n, t in klaim_aktif))
        for p in [x for x in pipa if x.get("status") == "antrean"][:5]:
            baris.append("- ⏳ **{}** ({} — antrean, menunggu spesifikasi 9A)".format(
                p.get("nama", "?"), p.get("jenis", "?")))
        for p in [x for x in pipa if x.get("status") == "spesifikasi-selesai"][:3]:
            baris.append("- 📝 **{}** (spesifikasi selesai — menunggu uji 9B)".format(
                p.get("nama", "?")))
        for p in [x for x in pipa if x.get("status") == "diuji-lolos"][:3]:
            baris.append("- ✅ **{}** (lolos uji — menunggu listing 9C)".format(
                p.get("nama", "?")))
        for p in [x for x in pipa if x.get("status") == "siap-jual"][:3]:
            baris.append("- 🛒 **{}** (siap jual — menunggu masuk Toko Aplikasi)".format(
                p.get("nama", "?")))
    else:
        baris.append("Belum ada proyek di alur produksi (data/produksi_game.json).")
    # --- 8. Antrean handoff ---
    antrean = _muat_handoff()
    terbuka = [h for h in antrean if h.get("status") in ("draf", "diperiksa")]
    baris.append("\n## 📋 Antrean Handoff: {} terbuka / {} total".format(
        len(terbuka), len(antrean)))
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# Antrean handoff bersama (skema sama dengan template SOP di
# sop-agent/handoff/templates/*.json)
# ---------------------------------------------------------------------------
def _muat_handoff():
    return _baca_json(HANDOFF_FILE, [])


def _simpan_handoff(items):
    with open(HANDOFF_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def _id_handoff_baru(items):
    return "HO-{:03d}".format(len(items) + 1)


def tabel_handoff():
    items = _muat_handoff()
    return [[h.get("id", ""), h.get("jenis", ""), str(h.get("dari_agent", "")),
             str(h.get("ke_agent", "")), h.get("ringkasan", ""),
             h.get("status", ""), h.get("tanggal", "")] for h in items]


def daftar_id_handoff():
    return [h.get("id", "") for h in _muat_handoff() if h.get("id")]


def tambah_handoff(jenis, dari_agent, ke_agent, ringkasan, isi_teks):
    ringkasan = (ringkasan or "").strip()
    if not ringkasan:
        return ("⚠️ Isi ringkasan dulu.", tabel_handoff(),
                gr.update(choices=daftar_id_handoff()))
    try:
        isi = json.loads(isi_teks) if (isi_teks or "").strip() else {}
        if not isinstance(isi, dict):
            isi = {"teks": isi_teks}
    except ValueError:
        isi = {"teks": isi_teks}
    items = _muat_handoff()
    item = {"id": _id_handoff_baru(items), "jenis": jenis, "tanggal": _hari_ini(),
            "dari_agent": dari_agent, "ke_agent": ke_agent,
            "ringkasan": ringkasan, "isi": isi, "status": "draf",
            "keputusan_cipta": None, "catatan_muse": None}
    items.append(item)
    _simpan_handoff(items)
    return ("✅ Handoff {} dibuat ({} → {}, status draf). "
            "Menunggu diperiksa Muse, lalu persetujuan Cipta bila perlu dikirim/diterbitkan.".format(
                item["id"], dari_agent, ke_agent)), tabel_handoff(), gr.update(choices=daftar_id_handoff())


def ubah_status_handoff(id_pilihan, status_baru):
    items = _muat_handoff()
    for h in items:
        if h.get("id") == id_pilihan:
            h["status"] = status_baru
            _simpan_handoff(items)
            return "✅ {} → status '{}'.".format(id_pilihan, status_baru), tabel_handoff()
    return "⚠️ ID {} tidak ditemukan.".format(id_pilihan), tabel_handoff()


# --- Aksi cepat: brief Riset (10) -> Produksi (5) ---
def daftar_brief_layak():
    riset = _baca_json(DATA_DIR / "riset.json", [])
    return ["{} — {} ({}/12, {})".format(e.get("niche", "?"), e.get("ide", "?"),
                                         e.get("skor", "?"), e.get("verdict", "?"))
            for e in riset if "layak" in str(e.get("verdict", "")).lower()]


def kirim_brief_ke_produksi(pilihan):
    if not pilihan:
        return ("⚠️ Pilih dulu brief riset yang layak.", tabel_handoff(),
                gr.update(choices=daftar_id_handoff()))
    niche_ide = pilihan.split(" (")[0]
    if " — " not in niche_ide:
        return ("⚠️ Pilihan tidak dikenal.", tabel_handoff(),
                gr.update(choices=daftar_id_handoff()))
    niche, ide = niche_ide.split(" — ", 1)
    riset = _baca_json(DATA_DIR / "riset.json", [])
    entri = next((e for e in riset
                  if e.get("niche") == niche and e.get("ide") == ide), None)
    if entri is None:
        return ("⚠️ Brief tidak ditemukan di log riset.", tabel_handoff(),
                gr.update(choices=daftar_id_handoff()))
    items = _muat_handoff()
    isi = {"nama_produk": ide, "jenis_produk": "",
           "masalah_customer": "Lihat teks penilaian lengkap di tab Agent 10 (log riset).",
           "target_customer": "", "bukti_permintaan": "",
           "skor_peluang": entri.get("skor"), "verdict": entri.get("verdict"),
           "harga_usulan_rp": None, "platform_jualan": [],
           "catatan_kejujuran": "Skor/verdict dari Agent 10; detail masalah & bukti "
                                "ada di teks penilaian, bukan di log ringkas ini."}
    item = {"id": _id_handoff_baru(items), "jenis": "product-brief",
            "tanggal": _hari_ini(), "dari_agent": 10, "ke_agent": 5,
            "ringkasan": "{} — {} ({}/12, {})".format(
                niche, ide, entri.get("skor", "?"), entri.get("verdict", "?")),
            "isi": isi, "status": "draf",
            "keputusan_cipta": None, "catatan_muse": None}
    items.append(item)
    _simpan_handoff(items)
    return ("✅ Brief **{}** dikirim ke Agent 5 (Produksi) sebagai {} (status draf). "
            "Agent 5 memakai brief ini sebagai bahan membuat draf produk.".format(
                ide, item["id"])), tabel_handoff(), gr.update(choices=daftar_id_handoff())


# --- Aksi cepat: draf Produksi (5) -> Penjualan (2) / Terjemah (8) ---
def daftar_draf_output():
    berkas = []
    for p in OUTPUT_DIR.rglob("*"):
        if p.is_file():
            berkas.append(p)
    berkas.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(ROOT)) for p in berkas[:20]]


def _kirim_draf(pilihan, ke_agent, nama_tujuan):
    if not pilihan:
        return ("⚠️ Pilih dulu draf dari daftar.", tabel_handoff(),
            gr.update(choices=daftar_id_handoff()))
    items = _muat_handoff()
    item = {"id": _id_handoff_baru(items), "jenis": "draft-approval",
            "tanggal": _hari_ini(), "dari_agent": 5, "ke_agent": ke_agent,
            "ringkasan": "Draf {} → {}".format(pilihan, nama_tujuan),
            "isi": {"nama_item": Path(pilihan).name, "jenis": "", "file": pilihan,
                    "judul": "", "caption": "", "harga_rp": None,
                    "catatan": "Draf dari Agent 5 — butuh persetujuan Cipta sebelum dipakai/diterbitkan."},
            "status": "draf", "keputusan_cipta": None, "catatan_muse": None}
    items.append(item)
    _simpan_handoff(items)
    return ("✅ Draf **{}** dikirim ke {} sebagai {} (status draf).".format(
        pilihan, nama_tujuan, item["id"])), tabel_handoff(), gr.update(choices=daftar_id_handoff())


def kirim_draf_ke_penjualan(pilihan):
    return _kirim_draf(pilihan, 2, "Agent 2 (Penjualan)")


def kirim_draf_ke_terjemah(pilihan):
    return _kirim_draf(pilihan, 8, "Agent 8 (Terjemah Inggris)")


# ---------------------------------------------------------------------------
# Tab Koordinasi — pembungkus tipis di atas agents/koordinasi.py (message bus)
# ---------------------------------------------------------------------------
def _kunci_agent(teks):
    teks = str(teks or "").strip()
    return int(teks) if teks.isdigit() else teks


def _tabel_pesan_koord(f_ke="", f_status=""):
    if KOORD is None:
        return []
    baris = KOORD.tabel_pesan()
    if f_ke:
        nama_ke = KOORD._nama(_kunci_agent(f_ke))
        baris = [r for r in baris if r[2] == nama_ke]
    if f_status:
        baris = [r for r in baris if r[6] == f_status]
    return baris


def _daftar_id_pesan_koord():
    if KOORD is None:
        return []
    return [p.get("id", "") for p in KOORD._muat()["pesan"] if p.get("id")]


def _segarkan_koordinasi(f_ke="", f_status=""):
    if KOORD is None:
        return ("⚠️ Modul koordinasi gagal dimuat: {}".format(EKOORD), [], [],
                "Belum ada aktivitas koordinasi.")
    return (KOORD.teks_papan(), _tabel_pesan_koord(f_ke, f_status),
            gr.update(choices=_daftar_id_pesan_koord()), KOORD.teks_log())


def _kirim_pesan_koord(dari, ke, jenis, prioritas, ringkasan, isi_teks):
    if KOORD is None:
        return ("⚠️ Modul koordinasi gagal dimuat: {}".format(EKOORD),
                [], gr.update(choices=[]), "")
    try:
        isi = json.loads(isi_teks) if (isi_teks or "").strip() else {}
        if not isinstance(isi, dict):
            isi = {"teks": isi_teks}
    except ValueError:
        isi = {"teks": isi_teks}
    _pesan, info = KOORD.kirim_pesan(_kunci_agent(dari), _kunci_agent(ke),
                                     jenis, prioritas, ringkasan, isi,
                                     sumber="manual")
    return (info, _tabel_pesan_koord(),
            gr.update(choices=_daftar_id_pesan_koord()), KOORD.teks_log())


def _ubah_status_pesan_koord(id_pesan, status_baru):
    if KOORD is None:
        return ("⚠️ Modul koordinasi gagal dimuat: {}".format(EKOORD),
                [], gr.update(choices=[]), "")
    info = KOORD.ubah_status_pesan(id_pesan, status_baru)
    return (info, _tabel_pesan_koord(),
            gr.update(choices=_daftar_id_pesan_koord()), KOORD.teks_log())


def _jalankan_siklus_koord():
    if KOORD is None:
        return "⚠️ Modul koordinasi gagal dimuat: {}".format(EKOORD)
    return KOORD.jalankan_siklus_harian()


# ---------------------------------------------------------------------------
# Tab Agent 2 — Penjualan (modul FastAPI, tanpa UI Gradio; dibuatkan tab di sini)
# ---------------------------------------------------------------------------
def _rencana_markdown():
    if A02 is None:
        return "⚠️ Agent 2 gagal dimuat: {}".format(E02)
    try:
        r = A02.rencana()
    except Exception as e:  # noqa: BLE001
        return "⚠️ Gagal membuat rencana: {}: {}".format(type(e).__name__, e)
    baris = ["# 📋 Rencana Harian Penjualan — {}\n".format(r.get("tanggal", "")),
             "Total lead: **{}** (belum terverifikasi: **{}**). Ringkasan status: {}.".format(
                 r.get("total", 0), r.get("belum_terverifikasi", 0),
                 ", ".join("{}: {}".format(k, v) for k, v in (r.get("ringkasan") or {}).items()))]
    for a in r.get("aksi", []):
        baris.append("\n## {}\n{}".format(a.get("judul", ""), a.get("detail", "")))
    baris.append("\n_Draf saja — pesan outreach dikirim manual oleh Cipta setelah dicek, "
                 "dan kontak harus terverifikasi dulu._")
    return "\n".join(baris)


def _tabel_leads():
    if A02 is None:
        return []
    try:
        return [[l.get("id", ""), l.get("nama", ""), l.get("kontak", ""),
                 l.get("alamat", ""), l.get("jenis", ""), l.get("status", ""),
                 "Ya" if l.get("terverifikasi") else "Belum",
                 l.get("catatan", "")] for l in A02.load_leads()]
    except Exception:  # noqa: BLE001
        return []


def _tambah_lead(nama, kontak, alamat, jenis, status, terverifikasi, catatan):
    if A02 is None:
        return "⚠️ Agent 2 gagal dimuat: {}".format(E02), _tabel_leads()
    nama = (nama or "").strip()
    if not nama:
        return "⚠️ Nama bisnis wajib diisi.", _tabel_leads()
    leads = A02.load_leads()
    baru_id = "lead-%02d" % (max([int(l["id"].split("-")[1]) for l in leads
                                  if str(l.get("id", "")).startswith("lead-")
                                  and str(l["id"].split("-")[1]).isdigit()],
                                 default=0) + 1)
    leads.append({"id": baru_id, "nama": nama, "kontak": (kontak or "").strip(),
                  "alamat": (alamat or "").strip(),
                  "jenis": (jenis or "pet shop").strip() or "pet shop",
                  "status": status, "terverifikasi": bool(terverifikasi),
                  "catatan": (catatan or "").strip()})
    A02.save_leads(leads)
    return "✅ Lead {} ditambahkan (status: {}). Ingat: verifikasi kontak dulu sebelum dihubungi.".format(
        baru_id, status), _tabel_leads()


# ---------------------------------------------------------------------------
# UI — satu Blocks, satu tab per agent + Papan Handoff
# ---------------------------------------------------------------------------
HEADER = """# 🎛️ Pusat Komando Podcast Meong

Satu wadah untuk **12 agent AI bernomor + 6 tim Agent 9 + workshop Avatar Podcast + bus Koordinasi (21 tab)** — berbagi satu folder `data/`, jadi output satu agent
langsung bisa dipakai agent lain lewat **Papan Handoff** dan **bus Koordinasi**. Agent 4 tidak ada
(dihapus atas perintah Cipta — upload harian ditangani Muse langsung).

**Aturan keras (SOP, berlaku 18 Nov 2026):** semua hasil adalah **DRAF** untuk persetujuan
Cipta · **tidak ada** yang otomatis upload / kirim / transfer / bayar · dilarang mengarang
data, ayat, hadis, atau angka pasar — bila data kurang, tulis **"belum cukup data"** ·
tidak ada janji penghasilan · fokus **gratis dulu** (Gemini free tier; tanpa layanan berbayar).
"""

MODE_TEKS = ("**Mode: AI penuh (Gemini free tier).**" if MODE_AI
             else "**Mode: template lokal** — isi `GEMINI_API_KEY` untuk AI penuh; "
                  "semua fitur tetap jalan dengan template.")


def _tab_error(pesan):
    gr.Markdown("⚠️ {}\n\nTab ini tidak bisa dibuka. Agent aslinya tetap bisa dipakai "
                "terpisah di foldernya masing-masing.".format(pesan))


def build_app():
    with gr.Blocks(title="Pusat Komando Podcast Meong",
                   analytics_enabled=False) as demo:
        gr.Markdown(HEADER)
        gr.Markdown(MODE_TEKS)

        with gr.Tabs():
            # ============================ PAPAN HANDOFF ============================
            with gr.Tab("🏠 Papan Handoff"):
                gr.Markdown(
                    "Antrean kerja bersama semua agent. Skema handoff sama dengan "
                    "template SOP (`data/handoff-templates/`): "
                    "`id · jenis · dari_agent · ke_agent · ringkasan · isi · status` "
                    "(draf → diperiksa → disetujui / ditolak → selesai). "
                    "**Keputusan akhir selalu di tangan Cipta.**")
                papan = gr.Markdown(tampilkan_papan())
                btn_papan = gr.Button("🔄 Segarkan Papan", variant="primary")
                btn_papan.click(fn=tampilkan_papan, outputs=papan,
                                api_name="tampilkan_papan")
                gr.Markdown("### 📋 Antrean Handoff")
                tabel = gr.Dataframe(
                    value=tabel_handoff(),
                    headers=["ID", "Jenis", "Dari", "Ke", "Ringkasan", "Status", "Tanggal"],
                    interactive=False, wrap=True)
                with gr.Row():
                    h_jenis = gr.Dropdown(choices=JENIS_HANDOFF, value="product-brief",
                                          label="Jenis handoff")
                    h_dari = gr.Dropdown(
                        choices=[str(k) for k in _URUTAN_AGENT] + ["Cipta (via Muse)", "Muse"],
                        value="10", label="Dari agent")
                    h_ke = gr.Dropdown(
                        choices=[str(k) for k in _URUTAN_AGENT] + ["Cipta (via Muse)", "Muse"],
                        value="5", label="Ke agent")
                h_ringkasan = gr.Textbox(label="Ringkasan (wajib)",
                                         placeholder="Contoh: eBook Cerita Nabi Yunus versi Inggris")
                h_isi = gr.Textbox(label="Isi (JSON, opsional — bila bukan JSON disimpan sebagai teks)",
                                   placeholder='{"nama_produk": "...", "harga_usulan_rp": 29000}',
                                   lines=2)
                with gr.Row():
                    btn_tambah = gr.Button("➕ Tambah Handoff", variant="primary")
                    h_id = gr.Dropdown(choices=daftar_id_handoff(), label="ID handoff")
                    h_status = gr.Dropdown(choices=STATUS_HANDOFF, value="diperiksa",
                                           label="Status baru")
                    btn_status = gr.Button("✏️ Ubah Status")
                pesan_handoff = gr.Markdown("")
                btn_tambah.click(fn=tambah_handoff,
                                 inputs=[h_jenis, h_dari, h_ke, h_ringkasan, h_isi],
                                 outputs=[pesan_handoff, tabel, h_id],
                                 api_name="tambah_handoff")
                btn_status.click(fn=ubah_status_handoff,
                                 inputs=[h_id, h_status],
                                 outputs=[pesan_handoff, tabel],
                                 api_name="ubah_status_handoff")
                gr.Markdown("### ⚡ Aksi Cepat")
                with gr.Row():
                    dd_brief = gr.Dropdown(choices=daftar_brief_layak(),
                                           label="Brief Riset layak (Agent 10)")
                    btn_brief = gr.Button("📨 Kirim Brief → Agent 5 (Produksi)")
                with gr.Row():
                    dd_draf = gr.Dropdown(choices=daftar_draf_output(),
                                          label="Draf Produksi (Agent 5, folder output/)")
                    btn_draf_jual = gr.Button("📨 Kirim Draf → Agent 2 (Penjualan)")
                    btn_draf_terj = gr.Button("📨 Kirim Draf → Agent 8 (Terjemah)")
                pesan_aksi = gr.Markdown("")
                btn_brief.click(fn=kirim_brief_ke_produksi, inputs=dd_brief,
                                outputs=[pesan_aksi, tabel, h_id])
                btn_draf_jual.click(fn=kirim_draf_ke_penjualan, inputs=dd_draf,
                                    outputs=[pesan_aksi, tabel, h_id])
                btn_draf_terj.click(fn=kirim_draf_ke_terjemah, inputs=dd_draf,
                                    outputs=[pesan_aksi, tabel, h_id])

            # ============================ KOORDINASI ANTAR-AGENT ============================
            with gr.Tab("🔄 Koordinasi"):
                gr.Markdown(
                    "Message bus antar-agent: satu jalur pesan tercatat (`data/koordinasi.json`) "
                    "dengan aturan rute otomatis (R1–R16) dan Siklus Harian. Pesan di sini adalah "
                    "**pengingat/DRAF** — agent penerima membacanya di tabnya, Muse memeriksa, "
                    "dan Cipta tetap memegang persetujuan untuk apa pun yang keluar "
                    "(upload/kirim/bayar/terbit). **Bukan obrolan live antar-agent**: agent adalah "
                    "aplikasi pasif; pesan dibaca saat tab dibuka atau siklus dijalankan.")
                if KOORD is None:
                    _tab_error(EKOORD or "modul koordinasi tidak bisa dimuat")
                else:
                    papan_koord = gr.Markdown(KOORD.teks_papan())
                    btn_koord = gr.Button("🔄 Segarkan Papan Koordinasi", variant="primary")
                    gr.Markdown("### 💬 Pesan di Bus")
                    with gr.Row():
                        f_ke = gr.Dropdown(
                            choices=[""] + [str(k) for k in _URUTAN_AGENT] + ["Muse"],
                            value="", label="Saring: pesan masuk ke")
                        f_status = gr.Dropdown(choices=[""] + KOORD.STATUS_PESAN,
                                               value="", label="Saring: status")
                        btn_saring = gr.Button("🔍 Saring")
                    tabel_koord = gr.Dataframe(
                        value=_tabel_pesan_koord(),
                        headers=["ID", "Dari", "Ke", "Jenis", "Prioritas",
                                 "Ringkasan", "Status", "Waktu", "Sumber"],
                        interactive=False, wrap=True)
                    gr.Markdown("### ✉️ Kirim Pesan Manual")
                    with gr.Row():
                        k_dari = gr.Dropdown(
                            choices=[str(k) for k in _URUTAN_AGENT] + ["Muse", "Sistem"],
                            value="10", label="Dari")
                        k_ke = gr.Dropdown(
                            choices=[str(k) for k in _URUTAN_AGENT] + ["Muse", "Cipta (via Muse)"],
                            value="5", label="Ke")
                        k_jenis = gr.Dropdown(choices=KOORD.JENIS_PESAN, value="pengingat",
                                              label="Jenis")
                        k_prioritas = gr.Dropdown(choices=KOORD.PRIORITAS, value="normal",
                                                  label="Prioritas")
                    k_ringkasan = gr.Textbox(label="Ringkasan (wajib)",
                                             placeholder="Contoh: Brief eBook Nabi Yunus layak dicoba (10/12)")
                    k_isi = gr.Textbox(label="Isi (JSON, opsional)",
                                       placeholder='{"nama_produk": "...", "skor_peluang": 10}',
                                       lines=2)
                    with gr.Row():
                        btn_kirim = gr.Button("📨 Kirim ke Bus", variant="primary")
                        k_id = gr.Dropdown(choices=_daftar_id_pesan_koord(), label="ID pesan")
                        k_status = gr.Dropdown(choices=KOORD.STATUS_PESAN, value="dibaca",
                                               label="Status baru")
                        btn_k_status = gr.Button("✏️ Ubah Status Pesan")
                    pesan_koord = gr.Markdown("")
                    log_koord = gr.Markdown(KOORD.teks_log())
                    gr.Markdown("### 🗺️ Aturan Rute Otomatis (R1–R16)")
                    gr.Dataframe(
                        value=KOORD.tabel_aturan(),
                        headers=["ID", "Aturan", "Dari", "Ke", "Jenis", "Prioritas",
                                 "Pemicu", "Status"],
                        interactive=False, wrap=True)
                    gr.Markdown(
                        "Aturan dievaluasi oleh Siklus Harian (atau sewaktu-waktu lewat "
                        "`evaluasi_rute()`). Pesan yang dibuat aturan selalu berstatus "
                        "`baru` dan bersumber `aturan-rute-Rx`; duplikat dicegah dengan kunci "
                        "dedupe + cek handoff yang sudah ada.")
                    gr.Markdown("### ▶️ Siklus Harian")
                    gr.Markdown(
                        "Satu kali jalan memeriksa data bersama sesuai urutan ketergantungan: "
                        "riset → produksi → penjualan/terjemah → lomba/keuangan → email → "
                        "penjaga → game → terjemah, lalu memposting ringkasan ke Muse. "
                        "Mode template — tanpa panggilan eksternal, tanpa API key. "
                        "Siklus **tidak** membuat entri handoff otomatis dan **tidak** "
                        "mengirim/mengunggah apa pun.")
                    btn_siklus = gr.Button("▶️ Jalankan Siklus Harian", variant="primary")
                    hasil_siklus = gr.Markdown("")
                    gr.Markdown("### 📜 Log Aktivitas Koordinasi")
                    btn_log = gr.Button("🔄 Segarkan Log")
                    # --- wiring (semua komponen sudah didefinisikan di atas) ---
                    btn_koord.click(fn=_segarkan_koordinasi, inputs=[f_ke, f_status],
                                    outputs=[papan_koord, tabel_koord, k_id, log_koord],
                                    api_name="segarkan_koordinasi")
                    btn_saring.click(fn=_segarkan_koordinasi, inputs=[f_ke, f_status],
                                     outputs=[papan_koord, tabel_koord, k_id, log_koord])
                    btn_kirim.click(fn=_kirim_pesan_koord,
                                    inputs=[k_dari, k_ke, k_jenis, k_prioritas, k_ringkasan, k_isi],
                                    outputs=[pesan_koord, tabel_koord, k_id, log_koord],
                                    api_name="kirim_pesan_koordinasi")
                    btn_k_status.click(fn=_ubah_status_pesan_koord,
                                       inputs=[k_id, k_status],
                                       outputs=[pesan_koord, tabel_koord, k_id, log_koord],
                                       api_name="ubah_status_pesan_koordinasi")
                    btn_siklus.click(fn=_jalankan_siklus_koord, outputs=hasil_siklus,
                                     api_name="jalankan_siklus_harian")
                    btn_log.click(fn=lambda: KOORD.teks_log(), outputs=log_koord)

            # ============================ AGENT 1 — ASISTEN ============================
            with gr.Tab("1 · Asisten"):
                blok, err = _blok_dari_modul(A01, lambda m: m.demo, "1 Asisten")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E01 or "tidak diketahui")

            # ============================ AGENT 2 — PENJUALAN ============================
            with gr.Tab("2 · Penjualan"):
                gr.Markdown(
                    "Agent Penjualan (aslinya layanan FastAPI — di sini dibuatkan tab Gradio "
                    "dengan fungsi yang sama). **Draf saja:** pesan outreach dikirim manual "
                    "oleh Cipta setelah dicek, dan kontak lead harus terverifikasi dulu.")
                if A02 is None:
                    _tab_error(E02 or "tidak diketahui")
                else:
                    with gr.Row():
                        tanya = gr.Textbox(label="Tanya seputar jasa / harga (mode template)",
                                           placeholder="Contoh: berapa harga video promo 30 detik?")
                        btn_tanya = gr.Button("💬 Jawab")
                    jawab_out = gr.Textbox(label="Jawaban", lines=4)
                    btn_tanya.click(fn=A02.jawab_template, inputs=tanya, outputs=jawab_out)
                    gr.Markdown("### ✍️ Generator Draf Promosi")
                    with gr.Row():
                        gen_jenis = gr.Dropdown(
                            choices=["caption_tiktok", "caption_ig", "caption_yt",
                                     "wa_outreach", "wa_followup", "dm_ig", "email"],
                            value="caption_tiktok", label="Jenis draf")
                        gen_toko = gr.Textbox(label="Nama toko", placeholder="Contoh: Petshop Momo")
                        gen_produk = gr.Textbox(label="Produk", placeholder="Contoh: makanan kucing")
                        gen_paket = gr.Dropdown(choices=["15", "30", "60"], value="30",
                                                label="Paket (detik)")
                    btn_gen = gr.Button("✍️ Buat Draf", variant="primary")
                    gen_out = gr.Textbox(label="Draf (periksa dulu sebelum dikirim)", lines=8)
                    btn_gen.click(fn=A02.template_generator,
                                  inputs=[gen_jenis, gen_toko, gen_produk, gen_paket],
                                  outputs=gen_out)
                    gr.Markdown("### 📋 Rencana Harian")
                    btn_rencana = gr.Button("📋 Tampilkan Rencana Hari Ini")
                    rencana_out = gr.Markdown("")
                    btn_rencana.click(fn=_rencana_markdown, outputs=rencana_out)
                    gr.Markdown("### 👥 Leads (15 lead awal dari daftar target pet shop)")
                    leads_tabel = gr.Dataframe(
                        value=_tabel_leads(),
                        headers=["ID", "Nama", "Kontak", "Alamat", "Jenis",
                                 "Status", "Terverifikasi", "Catatan"],
                        interactive=False, wrap=True)
                    with gr.Row():
                        l_nama = gr.Textbox(label="Nama bisnis *")
                        l_kontak = gr.Textbox(label="Kontak (WA/telp)")
                        l_alamat = gr.Textbox(label="Alamat")
                    with gr.Row():
                        l_jenis = gr.Textbox(label="Jenis", value="pet shop")
                        l_status = gr.Dropdown(choices=A02.STATUS_LEAD, value="baru",
                                               label="Status")
                        l_verif = gr.Checkbox(label="Terverifikasi", value=False)
                    l_catatan = gr.Textbox(label="Catatan")
                    btn_lead = gr.Button("➕ Tambah Lead", variant="primary")
                    pesan_lead = gr.Markdown("")
                    btn_lead.click(fn=_tambah_lead,
                                   inputs=[l_nama, l_kontak, l_alamat, l_jenis,
                                           l_status, l_verif, l_catatan],
                                   outputs=[pesan_lead, leads_tabel])

            # ============================ AGENT 3 — PERTUMBUHAN ============================
            with gr.Tab("3 · Pertumbuhan"):
                blok, err = _blok_dari_modul(A03, lambda m: m.demo, "3 Pertumbuhan")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E03 or "tidak diketahui")

            # ============================ AGENT 5 — PRODUKSI PRODUK ============================
            with gr.Tab("5 · Produksi Produk"):
                blok, err = _blok_dari_modul(A05, lambda m: m.demo, "5 Produksi Produk")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E05 or "tidak diketahui")

            # ============================ AGENT 6 — LOMBA ============================
            with gr.Tab("6 · Lomba"):
                blok, err = _blok_dari_modul(A06, lambda m: m.build_app(), "6 Lomba")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E06 or "tidak diketahui")

            # ============================ AGENT 7 — KEUANGAN ============================
            with gr.Tab("7 · Keuangan"):
                blok, err = _blok_dari_modul(A07, lambda m: m.build_ui(), "7 Keuangan")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E07 or "tidak diketahui")

            # ============================ AGENT 8 — TERJEMAH INGGRIS ============================
            with gr.Tab("8 · Terjemah Inggris"):
                blok, err = _blok_dari_modul(A08, lambda m: m.demo, "8 Terjemah Inggris")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E08 or "tidak diketahui")

            # ============================ AGENT 9 — GAME & APLIKASI ============================
            with gr.Tab("9 · Game & Aplikasi"):
                blok, err = _blok_dari_modul(A09, lambda m: m.bangun_ui(), "9 Game & Aplikasi")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09 or "tidak diketahui")

            # ============================ TIM 9A — RANCANG ============================
            with gr.Tab("9A · Rancang"):
                blok, err = _blok_dari_modul(A09A, lambda m: m.bangun_ui(), "9A Rancang")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09A or "tidak diketahui")

            # ============================ TIM 9B — BANGUN ============================
            with gr.Tab("9B · Bangun"):
                blok, err = _blok_dari_modul(A09B, lambda m: m.bangun_ui(), "9B Bangun")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09B or "tidak diketahui")

            # ============================ TIM 9C — JUALAN ============================
            with gr.Tab("9C · Jualan"):
                blok, err = _blok_dari_modul(A09C, lambda m: m.bangun_ui(), "9C Jualan")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09C or "tidak diketahui")

            # ============================ TIM 9D — BANGUN-2 ============================
            with gr.Tab("9D · Bangun-2"):
                blok, err = _blok_dari_modul(A09D, lambda m: m.bangun_ui(), "9D Bangun-2")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09D or "tidak diketahui")

            # ============================ TIM 9E — BANGUN-3 ============================
            with gr.Tab("9E · Bangun-3"):
                blok, err = _blok_dari_modul(A09E, lambda m: m.bangun_ui(), "9E Bangun-3")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09E or "tidak diketahui")

            # ============================ TIM 9F — VERIFIKASI & KATALOG ============================
            with gr.Tab("9F · Verifikasi & Katalog"):
                blok, err = _blok_dari_modul(A09F, lambda m: m.bangun_ui(), "9F Verifikasi & Katalog")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E09F or "tidak diketahui")

            # ============================ AGENT 10 — RISET PRODUK ============================
            with gr.Tab("10 · Riset Produk"):
                blok, err = _blok_dari_modul(A10, lambda m: m.build_ui(), "10 Riset Produk")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E10 or "tidak diketahui")

            # ============================ WORKSHOP AVATAR PODCAST ============================
            with gr.Tab("Avatar Podcast"):
                blok, err = _blok_dari_modul(A11, lambda m: m.build_ui(), "Avatar Podcast")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E11 or "tidak diketahui")

            # ============================ AGENT 11 — OYEN ============================
            with gr.Tab("11 · Oyen"):
                blok, err = _blok_dari_modul(A11O, lambda m: m.build_ui(), "11 Oyen")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E11O or "tidak diketahui")

            # ============================ AGENT 12 — MOMO ============================
            with gr.Tab("12 · Momo"):
                blok, err = _blok_dari_modul(A12M, lambda m: m.build_ui(), "12 Momo")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E12M or "tidak diketahui")

            # ============================ AGENT 13 — EMAIL ============================
            with gr.Tab("13 · Email"):
                blok, err = _blok_dari_modul(A13, lambda m: m.build_ui(), "13 Email")
                if blok is not None:
                    blok.render()
                else:
                    _tab_error(err or E13 or "tidak diketahui")

        gr.Markdown(
            "---\n*Pusat Komando Podcast Meong — 12 agent bernomor + 6 tim Agent 9 + workshop Avatar Podcast + bus Koordinasi, 1 Space, 1 folder data. "
            "Data di `data/` hilang bila Space di-rebuild — unduh berkala. "
            "SOP Kerja Sama Agent AI berlaku (18 Nov 2026).*")
    return demo


if __name__ == "__main__":
    build_app().launch(server_name="0.0.0.0",
                       server_port=int(os.environ.get("PORT", "7860")))
