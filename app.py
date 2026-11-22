# ==========================================================================
# PUSAT KOMANDO PODCAST MEONG — v2.0
# 30 Agent Bintang (A01–A30) + Mesin Eksekusi + Dashboard Agent +
# Command Center (3.0) + Papan Handoff + bus Koordinasi antar-agent
# (5 tab) dalam SATU Space Gradio, berbagi satu folder data/ — supaya
# output satu agent langsung bisa dipakai agent lain lewat Papan Handoff,
# tanpa antre lewat Muse.
#
# v2.0 (21 Nov 2026, perintah Cipta): 30 Agent Bintang + mesin eksekusi
# (agents/mesin_eksekusi.py) + 14 agent lama menjadi PASIF NON-JOB
# (modul + data tetap utuh sebagai mesin/engine yang dipakai 30 Bintang;
# tab UI mereka dihapus, hanya tab B/C/0/Handoff/Koordinasi yang tampil).
# v1 = sistem 14 agent bernomor + 6 tim Agent 9 + workshop Avatar Podcast.
#
# 30 Agent Bintang (modul agents/b01–b30, job description dari Share
# ChatGPT #18/#19 + Share Gemini #1; dipetakan ke 14 mesin lama + Muse +
# Pusat Komando; strategi SESUAI ChatGPT + Gemini: KPI gemini_kpi, target
# 30 hari Gemini; JADWAL MESIN = siklus SOP 07:00–16:30, keputusan Cipta
# 21 Nov 2026 "Mesin ikut SOP" — slot Gemini hanya fallback).
# 14 mesin lama (a01–a14): Asisten, Penjualan, Pertumbuhan, Penjualan
# Harian, Produksi Produk, Lomba, Keuangan, Terjemah Inggris, Game &
# Aplikasi (+ tim 9A–9F), Riset Produk, Oyen, Momo, Email, Upwork.
#
# ATURAN YANG TETAP BERLAKU (SOP Kerja Sama Agent AI, berlaku 18 Nov 2026):
# - Semua output agent adalah DRAF untuk persetujuan Cipta.
# - TIDAK ADA yang otomatis upload / kirim / transfer / bayar.
# - Dilarang mengarang data pasar, ayat, hadis, atau angka; bila data kurang
#   tulis "belum cukup data". Tidak ada janji penghasilan.
# - Fokus gratis dulu: Gemini free tier via env var GEMINI_API_KEY saja;
#   tanpa key semua agent jalan mode template lokal. Tanpa layanan berbayar.
# - Kendala HARUS diinfokan: pekerjaan yang tidak bisa jalan mendapat
#   status "terkendala" + penyebab + apa yang dibutuhkan dari Cipta.
# - Telemetri Gradio dimatikan.
# - ATURAN WAJIB 27 POIN (Cipta, 22 Nov 2026) — teks lengkap di
#   data/aturan-wajib-27-poin.md, tampil di HEADER app; wajib ditaati
#   semua agent (Muse + 30 Bintang + A31–A36).
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
              4: "4 · Penjualan Harian",
              5: "5 · Produksi Produk", 6: "6 · Lomba", 7: "7 · Keuangan",
              8: "8 · Terjemah Inggris", 9: "9 · Game & Aplikasi",
              "9A": "9A · Rancang", "9B": "9B · Bangun", "9C": "9C · Jualan",
              "9D": "9D · Bangun-2", "9E": "9E · Bangun-3",
              "9F": "9F · Verifikasi & Katalog",
              10: "10 · Riset Produk", 11: "11 · Oyen", 12: "12 · Momo",
              13: "13 · Email", 14: "14 · Upwork"}
# Urutan agent di dropdown (angka dulu, tim 9A–9F tepat setelah 9) —
# sorted() biasa tidak bisa dipakai karena kunci campuran int + str.
_URUTAN_AGENT = [1, 2, 3, 4, 5, 6, 7, 8, 9, "9A", "9B", "9C", "9D", "9E", "9F",
                 10, 11, 12, 13, 14]
MODE_AI = bool(os.environ.get("GEMINI_API_KEY", "").strip())
VERSI = "2.0"  # Pusat Komando v2.0 (21 Nov 2026): 30 Bintang + mesin eksekusi


# ---------------------------------------------------------------------------
# Muat modul agent (defensif: satu agent gagal tidak menjatuhkan yang lain)
# ---------------------------------------------------------------------------
def _muat(nama_modul):
    try:
        return importlib.import_module(nama_modul), None
    except Exception as e:  # noqa: BLE001 — tampilkan sebagai tab error
        return None, "{}: {}".format(type(e).__name__, e)


# 14 modul lama (a01–a14) TIDAK dimuat di sini lagi sejak v2.0 — mereka
# tetap bisa diimpor sebagai mesin oleh modul Bintang (b01–b30) dan mesin
# eksekusi; tab UI mereka dihapus. Yang dimuat di app.py: koordinasi,
# dashboard, dan mesin eksekusi.
KOORD, EKOORD = _muat("koordinasi")
DASH, E_DASH = _muat("dashboard")
MESIN, E_MESIN = _muat("mesin_eksekusi")


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


# ---------------------------------------------------------------------------
# 30 Agent Bintang (B) — dimuat defensif dari data/agents.json (key agent_30)
# ---------------------------------------------------------------------------
def _muat_b30():
    """Muat 30 modul b01..b30. Satu modul gagal tidak menjatuhkan yang lain."""
    hasil, kesalahan = {}, {}
    data = _baca_json(DATA_DIR / "agents.json", {})
    for entri in (data.get("agent_30") or {}).get("agents", []):
        kode = entri.get("code", "")
        nama_file = (entri.get("file", "") or "").replace("agents/", "").replace(".py", "")
        if not kode or not nama_file:
            continue
        modul, err = _muat(nama_file)
        hasil[kode] = modul
        kesalahan[kode] = err
    return hasil, kesalahan


B30, E_B30 = _muat_b30()


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
# COMMAND CENTER 3.0 — CEO + 8 direktorat + Approval Center
# Pemetaan AI Business Autonomous Agent 3.0 (Share ChatGPT #16/#17) ke
# 14 agen nyata. Konfigurasi di data/agents.json. Semua pekerjaan DRAF —
# keputusan akhir selalu di tangan Cipta.
# ---------------------------------------------------------------------------
AGENTS3_FILE = DATA_DIR / "agents.json"
_OTORITAS_LABEL = {"hijau": "🟢 Hijau — otomatis",
                   "kuning": "🟡 Kuning — periksa dulu",
                   "merah": "🔴 Merah — wajib persetujuan Cipta"}


def _muat_agents3():
    return _baca_json(AGENTS3_FILE, {})


def tampilkan_command_center():
    a3 = _muat_agents3()
    if not a3:
        return ("# 🎛️ Command Center\n\n"
                "File `data/agents.json` belum ada — jalankan pemetaan 3.0 dulu.")
    baris = ["# 🎛️ Command Center — AI Business Autonomous Agent 3.0\n",
             "CEO Agent: **{}**. Pemilik: **{}** (pengendali tertinggi).\n".format(
                 a3.get("command", {}).get("ceo", "Muse (koordinator)"),
                 a3.get("command", {}).get("owner", "Cipta")),
             "Model: **{}** · Anggaran: **{}** · Prioritas: **{}** · "
             "Persetujuan pemilik: **{}**.\n".format(
                 a3.get("decisions", {}).get("automation_model", "?"),
                 a3.get("decisions", {}).get("budget", "?"),
                 a3.get("decisions", {}).get("priority", "?"),
                 a3.get("decisions", {}).get("owner_approval", "?"))]
    for d in a3.get("directorates", []):
        agents = d.get("agents", [])
        hitung = {}
        for ag in agents:
            hitung[ag.get("status", "?")] = hitung.get(ag.get("status", "?"), 0) + 1
        baris.append("\n## {} · {} — {} ({} agent, {})".format(
            d.get("id", "?"), d.get("name", "?"), d.get("chief", "?"),
            len(agents), ", ".join("{}: {}".format(k, v)
                                   for k, v in sorted(hitung.items()))))
        baris.append("Dipetakan ke: {}.".format(", ".join(d.get("mapped_to", []))))
    baris.append("\n## 🔑 Tingkat Kewenangan")
    baris.append("🟢 **Hijau** — AI boleh otomatis sesuai aturan (riset, draft, "
                 "pencatatan, klasifikasi, laporan, pemantauan, QC).")
    baris.append("🟡 **Kuning** — AI menyiapkan untuk diperiksa (draf siap kirim, "
                 "konten siap upload, usulan harga, laporan harian).")
    baris.append("🔴 **Merah** — WAJIB persetujuan Cipta (upload, kirim keluar, "
                 "proposal freelance, ikut lomba, ubah harga, transfer uang — "
                 "TIDAK PERNAH dilakukan AI — hapus akun/data, pembayaran, "
                 "tanda tangan).")
    baris.append("\n## ⚠️ Catatan Jujur")
    for n in a3.get("honest_notes", []):
        baris.append("- {}".format(n))
    return "\n".join(baris)


def _tabel_agent3():
    a3 = _muat_agents3()
    rows = []
    for d in a3.get("directorates", []):
        for ag in d.get("agents", []):
            rows.append([ag.get("code", ""), "{} · {}".format(d.get("id", ""), d.get("name", "")),
                         ag.get("task", ""), ag.get("mapped_to", ""),
                         ag.get("status", ""),
                         _OTORITAS_LABEL.get(ag.get("authority", ""), ag.get("authority", ""))])
    return rows


def _tabel_approval():
    items = [h for h in _muat_handoff() if h.get("status") in ("draf", "diperiksa")]
    return [[h.get("id", ""), h.get("jenis", ""), str(h.get("dari_agent", "")),
             str(h.get("ke_agent", "")), h.get("ringkasan", ""),
             h.get("status", ""), h.get("tanggal", "")] for h in items]


def _segarkan_command_center():
    return tampilkan_command_center(), _tabel_agent3(), _tabel_approval()


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
# UI — satu Blocks (5 tab sejak v2.0)
# ---------------------------------------------------------------------------
HEADER = """# 🎛️ Pusat Komando Podcast Meong — v2.0

**30 Agent Bintang** (A01–A30) + **Mesin Eksekusi** + **Dashboard Agent** + Command Center + Papan Handoff + bus Koordinasi — berbagi satu folder `data/`, jadi output satu agent
langsung bisa dipakai agent lain lewat **Papan Handoff** dan **bus Koordinasi**. Mesin lama (a01–a14): no 1–6 **aktif**, diganti nama jadi A31–A36 (Publish, Build, Pertumbuhan, Penerjemah, Ngetik, Copywriter); no 7–14 **pasif non-job**: modul + datanya tetap utuh sebagai engine yang dipakai 30 Bintang, tab UI-nya dihapus.

**Aturan keras (SOP, berlaku 18 Nov 2026):** semua hasil adalah **DRAF** untuk persetujuan
Cipta · **tidak ada** yang otomatis upload / kirim / transfer / bayar · dilarang mengarang
data, ayat, hadis, atau angka pasar — bila data kurang, tulis **"belum cukup data"** ·
tidak ada janji penghasilan · fokus **gratis dulu** (Gemini free tier; tanpa layanan berbayar).

**📜 Aturan Wajib 27 Poin (perintah Cipta — wajib ditaati semua agent; teks lengkap di `data/aturan-wajib-27-poin.md`):**
1) Upload YouTube, TikTok, Instagram jam 7 pagi dan jam 8 malam. 2) Kuota harian: video min 5, foto 50, eBook 5, lagu 5, musik 5, puisi 5, cerpen 5, POD 5, game 5, website 5, aplikasi 5, dan lain-lain sesuai aturan platform. 3) Evaluasi yang sudah, belum, dan kendala; cari solusi lalu eksekusi. 4) Cek uang masuk di semua platform; bila syarat terpenuhi, transfer ke PayPal dan BCA. 5) Fokus tingkatkan promosi, pemasaran, penjualan, like, view, follow, subscribe dari akun promo dan platform penjualan. 6) Bangun dan jaga komunikasi bila ada komunikasi customer/netizen di platform. 7) Cek berkala perkembangan dan kondisi semua platform. 8) Setiap jam 5 pagi berikan informasi hari itu — apa saja yang akan dikerjakan. 9) Berikan masukan dan solusi agar ke depan lebih baik dan target tercapai. 10) Tanya ke Gemini, ChatGPT, Claude, DeepSeek, dan tim agent.ai untuk tukar pikiran, cari informasi, solusi, menyelesaikan masalah, dan bikin planning — target jangka pendek dan jangka panjang. 11) Besok harus lebih baik dari hari ini; hari ini harus lebih baik dari kemarin. 12) Wajib inisiatif, kreatif, inovatif, visioner, berani ambil risiko terukur, ciptakan peluang, kesempatan, dan kesiapan. 13) Cari info lomba yang bisa diikuti — nasional, global, internasional — foto, video, puisi, cerpen, eBook, POD, musik, lagu, ide usaha, website, sistem, aplikasi, game, dan lain-lain yang Muse bisa — GRATIS, AMAN, potensi, menarik, berpeluang menang, dan bisa pakai AI. 14) 5 akun ciptabintanglestari (Threads, Facebook, Instagram, TikTok, YouTube) + 3 akun Podcast Meong wajib dihandle — promosi, konten, affiliate, marketing, jualan, edukasi, produk; tingkatkan follow, subscribe, like, view secara organik; buat strategi dari riset; durasi konten tidak harus 60 detik — yang penting tersampaikan; menarik, aman, potensi, peluang. 15) Peraturan yang wajib dan harus dilaksanakan. 16) Tugas Muse dan agen.ai lainnya patuh laksanakan — jangan banyak nanya. 17) Kritik dan saran boleh beserta solusinya. 18) Selalu update, cek selalu, dan jangan mengulangi kesalahan yang sama. 19) Selalu belajar dan memperbaiki diri. 20) Belajar dari agent.ai yang sudah berpengalaman dan terbukti. 21) Cek berkala pesan masuk email, platform, website, dan selalu update. 22) Tugas Cipta: memberi keputusan bila urgent. Semua diserahkan ke Muse. 23) Verifikasi, kode, sandi, email koordinasi dengan agent.ai 27 (A27) — untuk login, setting, edit, dan lain-lain selama untuk pekerjaan Cipta, disetujui, kecuali yang aneh-aneh dan urgent. 24) Keputusan Cipta mutlak, tak bisa ditolak. 25) Setiap hari mulai jam 8 pagi, kirim lamaran ATAU cari proyek yang mudah dan gampang — Freelancer.co.id 10, Fiverr 10, Sribu 10 per hari. Draf dulu baru dikirim. 26) Selalu aktif, berusaha mencapai target kerja, target Cipta, loyalitas, dan dedikasi tinggi. 27) Setiap agent.ai WAJIB mencatat, wajib dan on time setiap pekerjaan dan jobdesknya — tidak perlu dipicu/disuruh Muse. Jalan sendiri. Inisiatif dan profesional.
"""

MODE_TEKS = ("**Mode: AI penuh (Gemini free tier).**" if MODE_AI
             else "**Mode: template lokal** — isi `GEMINI_API_KEY` untuk AI penuh; "
                  "semua fitur tetap jalan dengan template.")


def _tab_error(pesan):
    gr.Markdown("⚠️ {}\n\nTab ini tidak bisa dibuka. Agent aslinya tetap bisa dipakai "
                "terpisah di foldernya masing-masing.".format(pesan))


# ---------------------------------------------------------------------------
# Tab B — 30 Agent Bintang (A01–A30, Share ChatGPT #18/#19 + Gemini #1)
# ---------------------------------------------------------------------------
def _daftar_b30():
    """Metadata 30 agent dari data/agents.json (key agent_30)."""
    data = _baca_json(DATA_DIR / "agents.json", {})
    return (data.get("agent_30") or {}).get("agents", [])


def _tabel_b30():
    rows = []
    for e in _daftar_b30():
        kode = e.get("code", "")
        modul = B30.get(kode)
        muat = "✅" if modul is not None else "⚠️ gagal: {}".format(E_B30.get(kode) or "?")
        rows.append([kode, e.get("name", ""), e.get("division", ""), e.get("boss", ""),
                     e.get("job_desc", ""), e.get("mapped_to", ""), e.get("status", ""),
                     e.get("gemini_division", ""), muat])
    return rows


def _detail_agent30(kode):
    entri = next((e for e in _daftar_b30() if e.get("code") == kode), None)
    if entri is None:
        return "⚠️ Agent {} tidak ditemukan di data/agents.json.".format(kode)
    modul = B30.get(kode)
    baris = ["# {} · {}\n".format(entri.get("code", ""), entri.get("name", "")),
             "**Divisi:** {} · **Atasan:** {} · **Status:** {}\n".format(
                 entri.get("division", ""), entri.get("boss", ""), entri.get("status", "")),
             "**Job description (ChatGPT #18):** {}\n".format(entri.get("job_desc", "")),
             "**Dipetakan ke (sistem kita):** {}\n".format(entri.get("mapped_to", "")),
             "**Pemetaan Gemini #1:** {} — {}\n".format(
                 entri.get("gemini_division", ""), entri.get("gemini_role", "")),
             "**KPI Gemini (target rancangan, bukan janji):** {}\n".format(
                 "; ".join(entri.get("gemini_kpi", []) or ["—"])),
             "**Tools Gemini:** {}\n".format(", ".join(entri.get("gemini_tools", []) or ["—"]))]
    if modul is None:
        baris.append("\n⚠️ Modul gagal dimuat: {}".format(E_B30.get(kode) or "?"))
        return "\n".join(baris)
    try:
        contoh = modul.contoh()
    except Exception as e:  # noqa: BLE001
        baris.append("\n⚠️ Gagal membuat contoh draf: {}: {}".format(type(e).__name__, e))
        return "\n".join(baris)
    baris.append("\n## 📄 Contoh Draf (mode: {})\n".format(contoh.get("mode", "?")))
    baris.append("```json\n{}\n```".format(json.dumps(contoh, ensure_ascii=False, indent=2)))
    if kode == "A01":
        try:
            r = modul.rencana_30_hari()
            baris.append("\n## 📅 Rencana 30 Hari Gemini (target rancangan)")
            for f in r.get("fase", []):
                baris.append("- **Hari {} ({}):** {}".format(
                    f.get("hari", ""), f.get("nama", ""), f.get("fokus", "")))
            baris.append("\n{}".format(r.get("catatan_jujur", "")))
        except Exception:  # noqa: BLE001
            pass
    if kode == "A03":
        try:
            if MESIN is not None:
                j = MESIN.jadwal_harian_mesin()
                sop = "SOP" in j.get("sumber", "")
                baris.append("\n## 🕐 Siklus Harian SOP — jadwal yang diikuti mesin"
                             if sop else
                             "\n## 🕐 Jadwal Harian Gemini (referensi, bukan jadwal otomatis)")
                for s in j.get("slot", []):
                    baris.append("- **{} ({}):** {} — {}".format(
                        s.get("jam", ""), s.get("agent_teks", ""),
                        s.get("kegiatan", ""), s.get("output", "")))
                baris.append("\n{}".format(j.get("catatan", "")))
            else:
                raise RuntimeError("mesin tidak dimuat")
        except Exception:  # noqa: BLE001 — fallback ke jadwal Gemini b03
            try:
                j = modul.jadwal_harian()
                baris.append("\n## 🕐 Jadwal Harian Gemini (referensi, bukan jadwal otomatis)")
                for s in j.get("jadwal", []):
                    baris.append("- **{}:** {}".format(s.get("jam", ""), s.get("kegiatan", "")))
                baris.append("\n{}".format(j.get("catatan_jujur", "")))
            except Exception:  # noqa: BLE001
                pass
    baris.append("\n_Agent pasif — dijalankan Muse, bukan layanan otonom 24 jam. "
                 "Semua output DRAF untuk persetujuan Cipta._")
    return "\n".join(baris)


def _segarkan_b30():
    return _tabel_b30(), _detail_agent30("A01")


# ---------------------------------------------------------------------------
# Tab C — Dashboard Pergerakan Agent (modul agents/dashboard.py)
# ---------------------------------------------------------------------------
def _ringkasan_dashboard_md():
    if DASH is None:
        return "⚠️ Modul dashboard gagal dimuat: {}".format(E_DASH)
    try:
        r = DASH.ringkasan_dashboard()
    except Exception as e:  # noqa: BLE001
        return "⚠️ Gagal membaca ringkasan: {}: {}".format(type(e).__name__, e)
    teks = ("# 📊 Dashboard Pergerakan Agent — Pusat Komando v{}\n\n"
            "**30 Agent Bintang** — ✅ Aktif: **{}** · 🟡 Aktif sebagian: **{}** · "
            "⏸️ Belum jalan: **{}**.\n\n"
            "🔧 Mesin lama: **{} aktif (A31–A36)** · **{} pasif — non job** (modul + data tetap, dipakai "
            "sebagai engine oleh 30 Bintang).\n\n"
            "📥 Handoff menunggu: **{}** · 📨 Draf penawaran toko: **{}** · "
            "🚧 Pekerjaan terkendala: **{}** · 📝 Entri log aktivitas: **{}**.\n\n"
            "_\"Belum jalan\" = status Aktif tapi belum ada aktivitas tercatat di folder "
            "data/. Agent yang bekerja lewat Muse tanpa menulis ke data/ tetap tampil "
            "\"belum ada aktivitas\"._").format(
                VERSI, r["aktif"], r["aktif_sebagian"],
                r["belum_jalan"], 14 - r["mesin_pasif"], r["mesin_pasif"],
                r["handoff_menunggu"], r["penawaran_toko_draf"],
                r["terkendala"], r["entri_log"])
    try:
        target = DASH.target_harian_dashboard()
        jalan = sum(1 for t in target if t["jalan"])
        teks += ("\n\n## 🎯 Target Harian (SOP)\n\n"
                 "Target harian per agent (SOP Harian 30 Agent Bintang) — "
                 "**{} dari 30 agent sudah jalan hari ini.** \"Jalan\" = ada run "
                 "mesin hari ini. Target SOP umumnya kualitatif — tercapai "
                 "tidaknya dinilai di QC 11.30, bukan dari angka di sini.\n\n"
                 "| Agent | Target harian | Jalan hari ini | Draf menunggu |\n"
                 "|---|---|---|---|\n".format(jalan))
        for t in target:
            teks += "| **{} {}** | {} | {} | {} |\n".format(
                t["kode"], t["nama"], t["target_harian"],
                "✅ {}×".format(t["jalan_hari_ini"]) if t["jalan"] else "⏳ 0",
                t["draf_menunggu"])
    except Exception:  # noqa: BLE001 — tabel target tidak boleh merusak ringkasan
        pass
    return teks


def _tabel_antrean():
    if DASH is None:
        return []
    try:
        antrean = DASH.antrean_kerja()
    except Exception:  # noqa: BLE001
        return []
    return [[a.get("id", ""), a.get("jenis", ""), a.get("agent", ""),
             a.get("ringkasan", "")[:100], a.get("status", ""),
             a.get("prioritas", ""), a.get("tenggat", "")]
            for a in antrean]


def _tabel_terkendala():
    if DASH is None:
        return []
    try:
        antrean = DASH.tugas_terkendala()
    except Exception:  # noqa: BLE001
        return []
    return [[a.get("id", ""), a.get("jenis", ""), a.get("agent", ""),
             a.get("ringkasan", "")[:100], a.get("penyebab", "")[:150],
             a.get("dibutuhkan_dari_cipta", "")[:150]]
            for a in antrean]


def _target_30_hari_md():
    if DASH is None:
        return "⚠️ Modul dashboard gagal dimuat: {}".format(E_DASH)
    try:
        t = DASH.target_30_hari()
    except Exception as e:  # noqa: BLE001
        return "⚠️ Gagal membaca target: {}: {}".format(type(e).__name__, e)
    baris = ["### 🎯 Target 30 Hari Gemini (tolok ukur, bukan janji)\n"]
    for item in t.get("target", []):
        baris.append("- **{}**: target **{}** {} — realisasi: **{}**{}.".format(
            item.get("nama", "?"), item.get("target", "?"),
            item.get("satuan", ""), item.get("realisasi", "?"),
            (" — " + item.get("catatan", "")) if item.get("catatan") else ""))
    baris.append("\n_{}_".format(t.get("catatan_jujur", "")))
    return "\n".join(baris)


def _tabel_platform():
    if DASH is None:
        return []
    try:
        data = DASH.platform_per_agent()
    except Exception:  # noqa: BLE001
        return []
    return [[p.get("kode", ""), p.get("nama", ""),
             ", ".join(p.get("terhubung", []) or ["—"]),
             ", ".join(p.get("belum_terhubung", []) or ["—"])]
            for p in data]


def _jalankan_mesin():
    """Tombol Dashboard: jalankan antrean menunggu lewat mesin eksekusi
    (maks 5 item). Semua output DRAF — menunggu persetujuan Cipta."""
    if MESIN is None:
        return ("⚠️ Mesin eksekusi gagal dimuat: {}".format(E_MESIN),
                _ringkasan_dashboard_md(), _tabel_dashboard(),
                _feed_dashboard_md(), _tabel_antrean(), _tabel_terkendala())
    try:
        hasil = MESIN.jalankan_antrean()
    except Exception as e:  # noqa: BLE001
        return ("⚠️ Mesin gagal jalan: {}: {}".format(type(e).__name__, e),
                _ringkasan_dashboard_md(), _tabel_dashboard(),
                _feed_dashboard_md(), _tabel_antrean(), _tabel_terkendala())
    baris = ["# ▶️ Mesin Eksekusi — hasil jalan\n",
             "Dijalankan: **{}** · Berhasil (draf menunggu persetujuan): **{}** · "
             "Terkendala: **{}** · Dilewati: **{}**.\n".format(
                 hasil.get("dijalankan", 0), hasil.get("berhasil", 0),
                 hasil.get("terkendala", 0), hasil.get("dilewati", 0))]
    for r in hasil.get("rincian", []):
        baris.append("- `{}` · **{}** — {} (mode: {}; run: {})".format(
            r.get("id", "?"), r.get("agent", "?"), r.get("status", "?"),
            r.get("mode", "?"), r.get("run_id", "?")))
    baris.append("\n_Semua draf menunggu persetujuan Cipta — mesin tidak pernah "
                 "mengirim/mempublikasi apa pun._")
    return ("\n".join(baris), _ringkasan_dashboard_md(), _tabel_dashboard(),
            _feed_dashboard_md(), _tabel_antrean(), _tabel_terkendala())


def _tabel_dashboard(f_divisi="Semua", f_agent="Semua"):
    if DASH is None:
        return []
    try:
        rows = DASH.tabel_semua_agent()
    except Exception:  # noqa: BLE001
        return []
    out = []
    for r in rows:
        if f_divisi and f_divisi != "Semua" and r["kelompok"] != f_divisi:
            continue
        if f_agent and f_agent != "Semua" and r["kode"] != f_agent:
            continue
        out.append([r["kode"], r["nama"], r["kelompok"], r["dipetakan_ke"],
                    r["status"], r["aktivitas_terakhir"], r["output_terakhir"]])
    return out


def _feed_dashboard_md():
    if DASH is None:
        return "⚠️ Modul dashboard gagal dimuat: {}".format(E_DASH)
    try:
        log = DASH.baca_log(limit=20)
    except Exception as e:  # noqa: BLE001
        return "⚠️ Gagal membaca log: {}: {}".format(type(e).__name__, e)
    if not log:
        return "Belum ada aktivitas tercatat."
    baris = ["### 📝 Umpan Aktivitas (20 terbaru)\n"]
    for e in log:
        baris.append("- **{}** · `{}` · **{}** — {}".format(
            e.get("waktu", "?"), e.get("kode_agent", "?"),
            e.get("aksi", "?"), e.get("hasil", "?")))
    return "\n".join(baris)


def _segarkan_dashboard(f_divisi="Semua", f_agent="Semua"):
    return (_ringkasan_dashboard_md(), _tabel_dashboard(f_divisi, f_agent),
            _feed_dashboard_md(), _tabel_antrean(), _tabel_terkendala(),
            _target_30_hari_md(), _tabel_platform())


def build_app():
    with gr.Blocks(title="Pusat Komando Podcast Meong v2.0",
                   analytics_enabled=False) as demo:
        gr.Markdown(HEADER)
        gr.Markdown(MODE_TEKS)

        with gr.Tabs():
            # ============================ COMMAND CENTER (3.0) ============================
            with gr.Tab("0 · Command Center"):
                gr.Markdown(
                    "CEO Agent (Muse) + 8 direktorat + Approval Center. "
                    "Konfigurasi di `data/agents.json` (pemetaan AI Business "
                    "Autonomous Agent 3.0, Share ChatGPT #16/#17). "
                    "Semua pekerjaan di sini DRAF — keputusan akhir di tangan Cipta.")
                gr.Markdown(
                    "### 🎯 Target & Strategi $5.000/bulan (revisi 21 Nov 2026 — teks lengkap di `data/target-dan-strategi.md`)\n\n"
                    "**Target (tidak berubah):** $5.000/bulan untuk seluruh tim · $5.000 sebelum 30 Nov 2026 · "
                    "$10.000 sebelum 31 Des 2026. Posisi awal: pemasukan semua platform Rp0.\n\n"
                    "**Strategi:** BERHENTI tambah produk (171 cukup) — SATU niche (rekomendasi: aplikasi & sistem bisnis UMKM), "
                    "kurasi 5–10 produk jadi tangga $0 → $19–$29 → $49 → $97–$149. Etsy duluan, Gumroad kedua. "
                    "Mesin trafik: Pinterest + video pendek → lead magnet gratis → email list target ±2.000 subscriber. "
                    "UGC jembatan uang tercepat (median ±$175/video — butuh tampil kamera, keputusan Cipta). "
                    "Konten = funnel, bukan sumber uang. Timeline jujur 6–12 bulan. "
                    "Batas upload: maks 3 video/hari/platform, jeda 2–4 jam. 70% jam kerja untuk pemasaran.\n\n"
                    "**Minggu 1 (22–28 Nov):** 1 niche + tangga harga · toko Etsy + Gumroad LIVE · lead magnet + 5 email sambutan · "
                    "NEXTALE 20 episode · Basabasi terkirim · uang masuk pertama (target ≥Rp500.000). "
                    "**Minggu 2:** peluncuran pertama, 50–100 subscriber, 1–10 penjualan. "
                    "**Minggu 3:** diagnosis funnel + produk #2. **Minggu 4:** laporan keuangan bulanan pertama + gandakan pemenang.")
                gr.Markdown(
                    "### 🛒 Eksekusi 20 Marketplace — WAJIB, Tim Produksi (teks lengkap di `data/marketplace-20-eksekusi.md`)\n\n"
                    "**Perintah Cipta 22 Nov 2026:** eksekusi semua 20 marketplace, satu-satu dari no. 1, selesai → next. "
                    "Yang bisa dulu; berhenti hanya bila benar-benar mentok. Diserahkan ke **Tim Produksi (A11–A19)** — WAJIB.\n\n"
                    "**Produk:** 1 Swarms skill $12 · 2 Agensi.io skill $12 · 3 MCP Market (bukan toko — verifikasi) · "
                    "4 Neura Market workflow+prompt · 5 Apify (belum cocok) · 6 Salesforce (enterprise) · 7 AWS (enterprise) · "
                    "8 Microsoft (enterprise) · 9 Envato Kasir Toko $59 · 10 CodeCanyon Kasir Toko $59 · 11 Codester Faktur & Invoice $29 · "
                    "12 Unity (tidak cocok) · 13 Gumroad LIVE · 14 Creative Market 14 item · 15 Etsy eBook · 16 PromptBase 9 prompt · "
                    "17 Payhip LIVE · 18 Whop · 19 Fiverr jasa · 20 Udemy kursus.\n\n"
                    "**Status:** no. 1 paket skill SIAP, menunggu masuk Google Cipta (masduki1189) → API key → publish. "
                    "No. 11 paket Codester SIAP, menunggu setuju teks+$29+bahasa UI. No. 14/16 draf + harga usulan siap, menunggu persetujuan harga. "
                    "No. 9/10 pendaftaran tutup/dijeda. No. 13/17 sudah LIVE.")
                cc_papan = gr.Markdown(tampilkan_command_center())
                btn_cc = gr.Button("🔄 Segarkan Command Center", variant="primary")
                gr.Markdown("### 🧑‍💼 62 Agent Spesialis → 14 Mesin (6 aktif A31–A36 · 8 pasif non-job)")
                cc_tabel = gr.Dataframe(
                    value=_tabel_agent3(),
                    headers=["Kode", "Direktorat", "Tugas", "Dipetakan ke",
                             "Status", "Otoritas"],
                    interactive=False, wrap=True)
                gr.Markdown("### ✅ Approval Center — Antrean Menunggu Persetujuan Cipta")
                cc_approval = gr.Dataframe(
                    value=_tabel_approval(),
                    headers=["ID", "Jenis", "Dari", "Ke", "Ringkasan",
                             "Status", "Tanggal"],
                    interactive=False, wrap=True)
                btn_cc.click(fn=_segarkan_command_center,
                             outputs=[cc_papan, cc_tabel, cc_approval],
                             api_name="segarkan_command_center")

            # ============================ 30 AGENT BINTANG ============================
            with gr.Tab("B · 30 Agent"):
                gr.Markdown(
                    "30 Agent Bintang A01–A30 (Bintang Command Center) — rancangan Share "
                    "ChatGPT #18/#19 + Share Gemini #1, dipetakan ke 14 mesin lama "
                    "(no 1–6 aktif A31–A36, no 7–14 pasif non-job) + Muse + Pusat Komando. **Agent pasif** (dijalankan "
                    "Muse/mesin eksekusi, bukan layanan otonom 24 jam); semua output "
                    "DRAF untuk persetujuan Cipta. Konfigurasi di "
                    "`data/agents.json` (key `agent_30`).")
                b30_tabel = gr.Dataframe(
                    value=_tabel_b30(),
                    headers=["Kode", "Nama", "Divisi", "Atasan", "Job Description",
                             "Dipetakan ke", "Status", "Divisi Gemini", "Modul"],
                    interactive=False, wrap=True)
                b30_dd = gr.Dropdown(
                    choices=[e.get("code", "") for e in _daftar_b30()],
                    value="A01", label="Detail agent")
                b30_detail = gr.Markdown(_detail_agent30("A01"))
                btn_b30 = gr.Button("🔄 Segarkan 30 Agent", variant="primary")
                b30_dd.change(fn=_detail_agent30, inputs=b30_dd, outputs=b30_detail,
                              api_name="detail_agent30")
                btn_b30.click(fn=_segarkan_b30, outputs=[b30_tabel, b30_detail],
                              api_name="segarkan_b30")

            # ============================ DASHBOARD AGENT ============================
            with gr.Tab("C · Dashboard Agent"):
                gr.Markdown(
                    "Pergerakan **30 Agent Bintang** dari data NYATA di "
                    "folder `data/` — bukan angka karangan. Bila kosong tertulis "
                    "\"belum ada aktivitas\". Mesin lama tampil terpisah: no 1–6 aktif "
                    "(A31–A36), no 7–14 \"Pasif — non job\". Umpan aktivitas dibaca dari "
                    "`data/activity_log.json`; modul b01–b30 menulis ke sana tiap kali "
                    "menghasilkan draf.")
                dash_ringkas = gr.Markdown(_ringkasan_dashboard_md())
                with gr.Row():
                    dash_divisi = gr.Dropdown(
                        choices=["Semua"] + (DASH.daftar_divisi() if DASH else []),
                        value="Semua", label="Filter divisi")
                    dash_agent = gr.Dropdown(
                        choices=["Semua"] + [r["kode"] for r in
                                             (DASH.tabel_semua_agent() if DASH else [])],
                        value="Semua", label="Filter agent")
                    btn_dash_filter = gr.Button("🔍 Terapkan Filter")
                dash_tabel = gr.Dataframe(
                    value=_tabel_dashboard(),
                    headers=["Kode", "Nama", "Kelompok", "Dipetakan ke", "Status",
                             "Aktivitas Terakhir", "Output Terakhir"],
                    interactive=False, wrap=True)
                btn_dash = gr.Button("🔄 Segarkan Dashboard", variant="primary")
                dash_feed = gr.Markdown(_feed_dashboard_md())
                gr.Markdown("### ▶️ Mesin Eksekusi")
                btn_mesin = gr.Button("▶️ Jalankan Mesin Eksekusi (antrean menunggu, maks 5)",
                                      variant="primary")
                hasil_mesin = gr.Markdown("")
                gr.Markdown("### 📋 Antrean Kerja (status + prioritas + tenggat)")
                dash_antrean = gr.Dataframe(
                    value=_tabel_antrean(),
                    headers=["ID", "Jenis", "Agent Bintang", "Ringkasan",
                             "Status", "Prioritas", "Tenggat"],
                    interactive=False, wrap=True)
                gr.Markdown("### 🚧 Pekerjaan Terkendala (butuh info/keputusan Cipta)")
                dash_terkendala = gr.Dataframe(
                    value=_tabel_terkendala(),
                    headers=["ID", "Jenis", "Agent Bintang", "Ringkasan",
                             "Penyebab", "Dibutuhkan dari Cipta"],
                    interactive=False, wrap=True)
                dash_target = gr.Markdown(_target_30_hari_md())
                gr.Markdown("### 🔌 Platform per Agent Bintang")
                dash_platform = gr.Dataframe(
                    value=_tabel_platform(),
                    headers=["Kode", "Nama", "Platform Terhubung",
                             "Platform Belum Terhubung"],
                    interactive=False, wrap=True)
                btn_dash_filter.click(fn=_tabel_dashboard,
                                      inputs=[dash_divisi, dash_agent],
                                      outputs=dash_tabel,
                                      api_name="filter_dashboard")
                btn_dash.click(fn=_segarkan_dashboard,
                               inputs=[dash_divisi, dash_agent],
                               outputs=[dash_ringkas, dash_tabel, dash_feed,
                                        dash_antrean, dash_terkendala,
                                        dash_target, dash_platform],
                               api_name="segarkan_dashboard")
                btn_mesin.click(fn=_jalankan_mesin,
                                outputs=[hasil_mesin, dash_ringkas, dash_tabel,
                                         dash_feed, dash_antrean, dash_terkendala],
                                api_name="jalankan_mesin_eksekusi")

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

        gr.Markdown(
            "---\n*Pusat Komando Podcast Meong v2.0 — 30 Agent Bintang + Mesin Eksekusi + Dashboard Agent + Command Center + Papan Handoff + bus Koordinasi, 1 Space, 1 folder data. "
            "Mesin lama (a01–a14): no 1–6 aktif A31–A36, no 7–14 pasif non-job: modul + data tetap, dipakai sebagai engine oleh 30 Bintang. "
            "Data di `data/` hilang bila Space di-rebuild — unduh berkala. "
            "SOP Kerja Sama Agent AI berlaku (18 Nov 2026).*")
    return demo


if __name__ == "__main__":
    build_app().launch(server_name="0.0.0.0",
                       server_port=int(os.environ.get("PORT", "7860")))
