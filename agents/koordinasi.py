# ==========================================================================
# KOORDINASI — Message bus antar-agent di Pusat Komando Podcast Meong.
#
# Modul ini TIDAK menggantikan Muse sebagai komandan dan TIDAK menggantikan
# Papan Handoff (handoff.json). Perannya lebih kecil dan jujur:
#   1. Menyediakan SATU jalur pesan antar-agent (bus) yang tercatat di
#      data/koordinasi.json, dengan status baru -> dibaca -> dikerjakan ->
#      selesai / ditolak.
#   2. Menjalankan ATURAN RUTE otomatis: bila data bersama menunjukkan
#      sesuatu yang butuh tindak lanjut agent lain (brief layak, draf baru,
#      tenggat lomba dekat, dst.), bus memposting pesan pengingatnya — DRAF,
#      bukan perintah otomatis. Agent penerima tetap bekerja lewat tabnya
#      sendiri; Muse tetap memeriksa; Cipta tetap memegang persetujuan.
#   3. "Siklus Harian": satu kali jalan memeriksa semua data bersama sesuai
#      urutan ketergantungan (riset -> produksi -> penjualan/terjemah ->
#      lomba/keuangan -> email -> penjaga -> game -> terjemah) dan memposting
#      hasil pemeriksaan ke bus + log aktivitas.
#
# BATASAN JUJUR (SOP v1.3):
# - Agent adalah aplikasi pasif. Bus ini BUKAN obrolan live antar-agent:
#   pesan dibaca saat seseorang membuka tab Koordinasi / menjalankan siklus.
# - Tidak ada upload/kirim/daftar lomba/bayar/transfer otomatis.
# - Tidak ada data yang dikarang: bila data kurang, siklus menulis
#   "BELUM CUKUP DATA" di log, bukan menebak.
# - Siklus TIDAK membuat entri handoff.json otomatis — handoff tetap dibuat
#   Muse lewat Papan Handoff setelah diperiksa (SOP bagian 5).
#
# File data: data/koordinasi.json
#   {"pesan": [...], "log": [...], "meta": {...}}
# Pesan: id (KB-001), tanggal, waktu, dari_agent, ke_agent, jenis,
#   prioritas, ringkasan, isi (dict), status, sumber, kunci (untuk dedupe).
# ==========================================================================
import hashlib
import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _file_koordinasi(data_dir=None):
    return Path(data_dir or DATA_DIR) / "koordinasi.json"


NAMA_AGENT = {1: "1 · Asisten", 2: "2 · Penjualan", 3: "3 · Pertumbuhan",
              5: "5 · Produksi Produk", 6: "6 · Lomba", 7: "7 · Keuangan",
              8: "8 · Terjemah Inggris", 9: "9 · Game & Aplikasi",
              "9A": "9A · Rancang", "9B": "9B · Bangun", "9C": "9C · Jualan",
              "9D": "9D · Bangun-2", "9E": "9E · Bangun-3",
              "9F": "9F · Verifikasi & Katalog",
              10: "10 · Riset Produk", 11: "11 · Oyen", 12: "12 · Momo",
              13: "13 · Email", "Muse": "Muse (Komandan)",
              "Cipta (via Muse)": "Cipta (via Muse)",
              "Sistem": "Sistem (Siklus Harian)"}
AGEN_KUNCI = [1, 2, 3, 5, 6, 7, 8, 9, "9A", "9B", "9C", "9D", "9E", "9F",
              10, 11, 12, 13, "Muse"]

STATUS_PESAN = ["baru", "dibaca", "dikerjakan", "selesai", "ditolak"]
TRANSISI = {"baru": ["dibaca", "ditolak"],
            "dibaca": ["dikerjakan", "ditolak"],
            "dikerjakan": ["selesai", "ditolak"],
            "selesai": [], "ditolak": []}
PRIORITAS = ["rendah", "normal", "tinggi", "mendesak"]
JENIS_PESAN = ["product-brief", "draft-approval", "sales-lead",
               "contest-entry", "finance-entry", "translation-job",
               "pengingat", "pemberitahuan", "eskalasi",
               "laporan-harian", "permintaan-perbaikan", "lainnya"]

# ---------------------------------------------------------------------------
# Aturan rute otomatis (id, nama, dari, ke, jenis, prioritas, pemicu).
# "pemicu" dibaca manusia; logika pemicunya ada di _cek_r1() ... _cek_r8().
# ---------------------------------------------------------------------------
ATURAN_RUTE = [
    {"id": "R1", "nama": "Brief layak → Produksi",
     "dari": 10, "ke": 5, "jenis": "product-brief", "prioritas": "normal",
     "pemicu": "riset.json ada entri berverdict 'Layak dicoba' dan belum ada "
               "handoff product-brief / pesan bus untuk ide itu.",
     "aktif": True},
    {"id": "R2", "nama": "Draf baru → Penjualan + Terjemah",
     "dari": 5, "ke": [2, 8], "jenis": "draft-approval", "prioritas": "normal",
     "pemicu": "Ada file draf baru di output/ yang belum punya handoff "
               "draft-approval / pesan bus.",
     "aktif": True},
    {"id": "R3", "nama": "Tenggat lomba ≤7 hari → Produksi",
     "dari": 6, "ke": 5, "jenis": "contest-entry", "prioritas": "tinggi",
     "pemicu": "lomba.json: tenggat 0–7 hari lagi, status baru/dicek, "
               "kebijakan AI 'diizinkan'.",
     "aktif": True},
    {"id": "R4", "nama": "Payout jatuh tempo → Muse",
     "dari": 7, "ke": "Muse", "jenis": "finance-entry", "prioritas": "tinggi",
     "pemicu": "keuangan_data.json: ada entri/pengingat payout bertanggal "
               "jatuh tempo ≤7 hari, atau pemasukan berstatus 'menunggu'.",
     "aktif": True},
    {"id": "R5", "nama": "Email penting → agent terkait",
     "dari": 13, "ke": "terkait", "jenis": "pemberitahuan", "prioritas": "tinggi",
     "pemicu": "log pemeriksaan Agent 13: email prioritas Tinggi. "
               "Kategori Lomba→6, Keuangan→7, Affiliate/Bisnis→2, Promo→3, "
               "Penting→Muse.",
     "aktif": True},
    {"id": "R6", "nama": "Verdict PERLU PERBAIKAN → Produksi",
     "dari": [11, 12], "ke": 5, "jenis": "permintaan-perbaikan",
     "prioritas": "normal",
     "pemicu": "log penjagaan Oyen/Momo: ada verdict 'PERLU PERBAIKAN'.",
     "aktif": True},
    {"id": "R7", "nama": "Game/aplikasi selesai → Penjualan + Keuangan",
     "dari": 9, "ke": [2, 7], "jenis": "pemberitahuan", "prioritas": "normal",
     "pemicu": "game_data.json: ada proyek berstatus 'selesai'/'diterbitkan'.",
     "aktif": True},
    {"id": "R8", "nama": "Terjemahan selesai → Penjualan",
     "dari": 8, "ke": 2, "jenis": "translation-job", "prioritas": "normal",
     "pemicu": "terjemah_progress.json: ada buku/bagian berstatus 'selesai'.",
     "aktif": True},
    {"id": "R9", "nama": "Ringkasan siklus → Muse",
     "dari": "Sistem", "ke": "Muse", "jenis": "laporan-harian",
     "prioritas": "normal",
     "pemicu": "Setiap kali Siklus Harian dijalankan: ringkasan hasilnya "
               "diposting ke Muse untuk diperiksa.",
     "aktif": True},
    {"id": "R10", "nama": "Pesan mendesak → eskalasi ke Muse",
     "dari": "Sistem", "ke": "Muse", "jenis": "eskalasi",
     "prioritas": "mendesak",
     "pemicu": "Pesan berprioritas 'mendesak' dibuat: salinan eskalasinya "
               "otomatis diposting ke Muse (SOP bagian 7: uang, tenggat, "
               "keputusan besar harus sampai ke Cipta lewat Muse).",
     "aktif": True},
    {"id": "R11", "nama": "Spesifikasi selesai → Bangun",
     "dari": "9A", "ke": "9B", "jenis": "product-brief", "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'spesifikasi-selesai' "
               "dan belum ada pesan bus untuk proyek itu.",
     "aktif": True},
    {"id": "R12", "nama": "Uji lolos → Jualan",
     "dari": "9B", "ke": "9C", "jenis": "draft-approval", "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'diuji-lolos' "
               "dan belum ada pesan bus untuk proyek itu.",
     "aktif": True},
    {"id": "R13", "nama": "Siap jual → Penjualan",
     "dari": "9C", "ke": 2, "jenis": "draft-approval", "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'siap-jual' "
               "dan belum ada pesan bus untuk proyek itu.",
     "aktif": True},
    {"id": "R14", "nama": "Spesifikasi bebas → builder paralel (9D/9E)",
     "dari": "9B", "ke": ["9D", "9E"], "jenis": "product-brief",
     "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'spesifikasi-selesai' "
               "yang belum diklaim tim bangun mana pun — tawarkan ke builder "
               "yang sedang bebas (klaim dulu sebelum membangun; klaim "
               "pertama menang, tim lain ditolak).",
     "aktif": True},
    {"id": "R15", "nama": "Uji 9D/9E lolos → Verifikasi 9F",
     "dari": ["9D", "9E"], "ke": "9F", "jenis": "draft-approval",
     "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'diuji-lolos' yang "
               "hasil_ujinya dicatat tim 9D/9E dan belum diverifikasi 9F.",
     "aktif": True},
    {"id": "R16", "nama": "Verifikasi 9F lolos → Jualan",
     "dari": "9F", "ke": "9C", "jenis": "draft-approval", "prioritas": "normal",
     "pemicu": "produksi_game.json: ada proyek berstatus 'diuji-lolos' yang "
               "verifikasi_9f-nya lolos dan belum ada pesan bus untuk proyek itu.",
     "aktif": True},
]

KATEGORI_KE_AGENT = {"Lomba": 6, "Keuangan": 7, "Affiliate/Bisnis": 2,
                     "Affiliate": 2, "Bisnis": 2, "Promo": 3,
                     "Penting": "Muse", "Umum": "Muse"}


# ---------------------------------------------------------------------------
# Utilitas file
# ---------------------------------------------------------------------------
def _baca_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, type(default)) else default
    except (OSError, ValueError):
        return default


def _muat(data_dir=None):
    data = _baca_json(_file_koordinasi(data_dir),
                      {"pesan": [], "log": [], "meta": {}})
    if not isinstance(data, dict):
        data = {"pesan": [], "log": [], "meta": {}}
    data.setdefault("pesan", [])
    data.setdefault("log", [])
    data.setdefault("meta", {})
    return data


def _simpan(data, data_dir=None):
    with open(_file_koordinasi(data_dir), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _cap_waktu():
    kini = datetime.now()
    return kini.date().isoformat(), kini.strftime("%H:%M")


def _nama(agent):
    return NAMA_AGENT.get(agent, str(agent))


def _kunci_teks(teks):
    return hashlib.md5(str(teks).encode("utf-8")).hexdigest()[:10]


def _ada_kunci(pesan_list, kunci):
    """True bila sudah ada pesan aktif (belum ditolak) dengan kunci dedupe itu."""
    return any(p.get("kunci") == kunci and p.get("status") != "ditolak"
               for p in pesan_list)


# ---------------------------------------------------------------------------
# Pesan: kirim / ubah status / baca
# ---------------------------------------------------------------------------
def kirim_pesan(dari, ke, jenis, prioritas, ringkasan, isi=None,
                sumber="manual", kunci=None, data_dir=None):
    """Kirim satu pesan ke bus. Kembalikan (pesan_dict_atau_None, info_teks).
    Bila kunci dedupe sudah ada (dan belum ditolak), tidak dibuat duplikat."""
    ringkasan = (ringkasan or "").strip()
    if not ringkasan:
        return None, "⚠️ Ringkasan wajib diisi."
    if jenis not in JENIS_PESAN:
        return None, "⚠️ Jenis '{}' tidak dikenal.".format(jenis)
    if prioritas not in PRIORITAS:
        return None, "⚠️ Prioritas '{}' tidak dikenal.".format(prioritas)
    data = _muat(data_dir)
    if kunci and _ada_kunci(data["pesan"], kunci):
        return None, "⏭️ Sudah ada pesan aktif dengan kunci yang sama — tidak dibuat duplikat."
    tanggal, waktu = _cap_waktu()
    pesan = {"id": "KB-{:03d}".format(len(data["pesan"]) + 1),
             "tanggal": tanggal, "waktu": waktu,
             "dari_agent": dari, "ke_agent": ke,
             "jenis": jenis, "prioritas": prioritas,
             "ringkasan": ringkasan, "isi": isi or {},
             "status": "baru", "sumber": sumber,
             "kunci": kunci or ""}
    data["pesan"].append(pesan)
    # R10: pesan mendesak otomatis dieskalasi ke Muse.
    if prioritas == "mendesak" and ke != "Muse":
        eskalasi = dict(pesan)
        eskalasi["id"] = "KB-{:03d}".format(len(data["pesan"]) + 1)
        eskalasi["ke_agent"] = "Muse"
        eskalasi["jenis"] = "eskalasi"
        eskalasi["ringkasan"] = "Eskalasi (mendesak): " + ringkasan
        eskalasi["sumber"] = "aturan-rute-R10"
        eskalasi["kunci"] = (kunci + "-esc") if kunci else ""
        data["pesan"].append(eskalasi)
    _simpan(data, data_dir)
    _tambah_log("Pesan {} dibuat: {} → {} ({}, {}).".format(
        pesan["id"], _nama(dari), _nama(ke), jenis, prioritas), data_dir)
    return pesan, "✅ Pesan {} terkirim: {} → {} (status baru).".format(
        pesan["id"], _nama(dari), _nama(ke))


def ubah_status_pesan(id_pesan, status_baru, data_dir=None):
    if status_baru not in STATUS_PESAN:
        return "⚠️ Status '{}' tidak dikenal.".format(status_baru)
    data = _muat(data_dir)
    for p in data["pesan"]:
        if p.get("id") == id_pesan:
            lama = p.get("status", "baru")
            if lama in ("selesai", "ditolak"):
                return "⚠️ {} sudah '{}' (terminal) — tidak bisa diubah lagi.".format(
                    id_pesan, lama)
            if status_baru not in TRANSISI.get(lama, []) and status_baru != lama:
                return ("⚠️ Transisi '{}' → '{}' tidak diizinkan. Jalur: "
                        "baru → dibaca → dikerjakan → selesai/ditolak.".format(
                            lama, status_baru))
            p["status"] = status_baru
            _simpan(data, data_dir)
            _tambah_log("Pesan {}: {} → {}.".format(id_pesan, lama, status_baru),
                        data_dir)
            return "✅ {} → status '{}'.".format(id_pesan, status_baru)
    return "⚠️ ID {} tidak ditemukan.".format(id_pesan)


def daftar_pesan(ke=None, status=None, data_dir=None):
    out = _muat(data_dir)["pesan"]
    if ke is not None and ke != "":
        out = [p for p in out if str(p.get("ke_agent")) == str(ke)]
    if status:
        out = [p for p in out if p.get("status") == status]
    return out


def inbox(agent, data_dir=None):
    return daftar_pesan(ke=agent, data_dir=data_dir)


def outbox(agent, data_dir=None):
    data = _muat(data_dir)["pesan"]
    return [p for p in data if str(p.get("dari_agent")) == str(agent)]


def ringkasan_status(data_dir=None):
    """Hitung pesan per agent per status. Kembalikan dict."""
    hasil = {}
    for p in _muat(data_dir)["pesan"]:
        kunci = str(p.get("ke_agent"))
        hasil.setdefault(kunci, {"baru": 0, "dibaca": 0, "dikerjakan": 0,
                                 "selesai": 0, "ditolak": 0, "total": 0})
        st = p.get("status", "baru")
        if st in hasil[kunci]:
            hasil[kunci][st] += 1
        hasil[kunci]["total"] += 1
    return hasil


def _tambah_log(teks, data_dir=None, maks=200):
    data = _muat(data_dir)
    tanggal, waktu = _cap_waktu()
    data["log"].append({"tanggal": tanggal, "waktu": waktu, "teks": teks})
    data["log"] = data["log"][-maks:]
    _simpan(data, data_dir)


def ambil_log(n=30, data_dir=None):
    return _muat(data_dir)["log"][-n:]


# ---------------------------------------------------------------------------
# Pengecekan aturan rute (membaca data bersama — tanpa panggilan eksternal)
# ---------------------------------------------------------------------------
def _baca_data_bersama(nama, default, data_dir=None):
    folder = Path(data_dir or DATA_DIR)
    return _baca_json(folder / nama, default)


def _cek_r1(data, folder):
    """Brief Agent 10 berverdict Layak dicoba -> Agent 5."""
    dibuat = []
    riset = _baca_data_bersama("riset.json", [], folder)
    handoff = _baca_data_bersama("handoff.json", [], folder)
    for e in riset:
        if "layak" not in str(e.get("verdict", "")).lower():
            continue
        ide = str(e.get("ide", "?"))
        kunci = "r1:" + _kunci_teks(e.get("niche", "") + "|" + ide)
        sudah_handoff = any(
            h.get("jenis") == "product-brief"
            and ide in str(h.get("ringkasan", "")) for h in handoff)
        if sudah_handoff:
            continue
        pesan, info = kirim_pesan(
            10, 5, "product-brief", "normal",
            "{} — {} ({}/12, {})".format(e.get("niche", "?"), ide,
                                         e.get("skor", "?"), e.get("verdict", "?")),
            {"nama_produk": ide, "skor_peluang": e.get("skor"),
             "verdict": e.get("verdict"),
             "catatan_kejujuran": "Dari log riset Agent 10; detail masalah & "
                                  "bukti ada di teks penilaian, bukan di log ringkas ini."},
            sumber="aturan-rute-R1", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    return dibuat, "R1 brief layak: {} pesan baru.".format(len(dibuat))


def _cek_r2(data, folder):
    """File draf baru di output/ -> Agent 2 + Agent 8."""
    dibuat = []
    root = Path(folder).parent
    berkas = []
    for p in (root / "output").rglob("*"):
        if p.is_file():
            berkas.append(p)
    berkas.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    handoff = _baca_data_bersama("handoff.json", [], folder)
    for p in berkas[:10]:
        rel = str(p.relative_to(root))
        for ke, nama in ((2, "Agent 2 (Penjualan)"), (8, "Agent 8 (Terjemah)")):
            kunci = "r2:{}:{}".format(rel, ke)
            sudah_handoff = False
            for h in handoff:
                if h.get("jenis") != "draft-approval":
                    continue
                isi_h = h.get("isi", {})
                file_h = isi_h.get("file", "") if isinstance(isi_h, dict) else ""
                if rel in str(file_h):
                    sudah_handoff = True
                    break
            if sudah_handoff:
                continue
            pesan, _info = kirim_pesan(
                5, ke, "draft-approval", "normal",
                "Draf {} → {}".format(rel, nama),
                {"nama_item": p.name, "file": rel,
                 "catatan": "Draf dari Agent 5 — butuh persetujuan Cipta "
                            "sebelum dipakai/diterbitkan."},
                sumber="aturan-rute-R2", kunci=kunci, data_dir=folder)
            if pesan:
                dibuat.append(pesan)
    return dibuat, "R2 draf baru: {} pesan baru.".format(len(dibuat))


def _cek_r3(data, folder):
    """Tenggat lomba 0-7 hari, AI diizinkan -> Agent 5."""
    dibuat = []
    hari = date.today()
    lomba = _baca_data_bersama("lomba.json", [], folder)
    for l in lomba:
        try:
            tenggat = date.fromisoformat(str(l.get("tenggat", ""))[:10])
        except (ValueError, TypeError):
            continue
        selisih = (tenggat - hari).days
        if not (0 <= selisih <= 7):
            continue
        if str(l.get("kebijakan_ai", "")).lower() != "diizinkan":
            continue
        if l.get("status") not in ("baru", "dicek"):
            continue
        nama = str(l.get("nama", "?"))
        kunci = "r3:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            6, 5, "contest-entry", "tinggi",
            "Lomba '{}' tenggat {} hari lagi ({}).".format(
                nama, selisih, tenggat.isoformat()),
            {"nama_lomba": nama, "tenggat": tenggat.isoformat(),
             "kebijakan_ai": l.get("kebijakan_ai"),
             "catatan": "Bila layak: buat karya sesuai kategori; kirim hanya "
                        "setelah Cipta menyetujui lomba DAN karya persisnya."},
            sumber="aturan-rute-R3", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    return dibuat, "R3 tenggat lomba ≤7 hari: {} pesan baru.".format(len(dibuat))


def _cek_r4(data, folder):
    """Payout jatuh tempo / pemasukan menunggu -> Muse."""
    keu = _baca_data_bersama("keuangan_data.json", {}, folder)
    dibuat = []
    pengingat = keu.get("pengingat_payout", []) if isinstance(keu, dict) else []
    hari = date.today()
    for item in pengingat:
        try:
            jatuh = date.fromisoformat(str(item.get("tanggal", ""))[:10])
        except (ValueError, TypeError):
            continue
        if 0 <= (jatuh - hari).days <= 7:
            kunci = "r4:" + _kunci_teks(str(item.get("platform", "")) + str(jatuh))
            pesan, _info = kirim_pesan(
                7, "Muse", "finance-entry", "tinggi",
                "Payout {} jatuh tempo {}.".format(item.get("platform", "?"),
                                                   jatuh.isoformat()),
                {"platform": item.get("platform"), "tanggal": jatuh.isoformat(),
                 "catatan": "Cek syarat payout; pencairan hanya dengan "
                            "persetujuan eksplisit Cipta."},
                sumber="aturan-rute-R4", kunci=kunci, data_dir=folder)
            if pesan:
                dibuat.append(pesan)
    menunggu = [e for e in keu.get("entries", []) if isinstance(keu, dict)
                and str(e.get("status", "")).lower() in ("menunggu", "pending")]
    for e in menunggu:
        kunci = "r4:menunggu:" + _kunci_teks(str(e.get("platform", "")) +
                                             str(e.get("jumlah", "")))
        pesan, _info = kirim_pesan(
            7, "Muse", "finance-entry", "normal",
            "Pemasukan {} menunggu ({}).".format(e.get("platform", "?"),
                                                 e.get("produk", "?")),
            {"platform": e.get("platform"), "produk": e.get("produk"),
             "jumlah": e.get("jumlah")},
            sumber="aturan-rute-R4", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not pengingat and not menunggu:
        return dibuat, ("R4 payout: BELUM CUKUP DATA — tidak ada data payout "
                        "bertanggal di keuangan_data.json.")
    return dibuat, "R4 payout: {} pesan baru.".format(len(dibuat))


def _cek_r5(data, folder):
    """Email penting Agent 13 -> agent terkait."""
    dibuat = []
    log_mail = _baca_data_bersama("log-pemeriksaan-email.json", [], folder)
    if not log_mail:
        log_mail = _baca_data_bersama("draf-balasan-email.json", [], folder)
    for e in log_mail if isinstance(log_mail, list) else []:
        prioritas = str(e.get("prioritas", e.get("priority", ""))).lower()
        if prioritas not in ("tinggi", "high", "penting"):
            continue
        kategori = str(e.get("kategori", e.get("category", "Penting")))
        ke = KATEGORI_KE_AGENT.get(kategori, "Muse")
        perihal = str(e.get("perihal", e.get("subjek", e.get("subject", "?"))))
        kunci = "r5:" + _kunci_teks(perihal + "|" + kategori)
        pesan, _info = kirim_pesan(
            13, ke, "pemberitahuan", "tinggi",
            "Email penting [{}]: {}.".format(kategori, perihal),
            {"kategori": kategori, "perihal": perihal,
             "pengirim": e.get("pengirim", e.get("from", "")),
             "catatan": "Draf balasan hanya dikirim setelah Cipta menyetujui "
                        "teks persisnya."},
            sumber="aturan-rute-R5", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not dibuat:
        return dibuat, "R5 email penting: tidak ada email prioritas Tinggi yang baru."
    return dibuat, "R5 email penting: {} pesan baru.".format(len(dibuat))


def _cek_r6(data, folder):
    """Verdict PERLU PERBAIKAN dari penjaga Oyen/Momo -> Agent 5."""
    dibuat = []
    for agen, berkas in ((11, "log-penjagaan-oyen.json"),
                         (12, "log-penjagaan-momo.json")):
        log = _baca_data_bersama(berkas, [], folder)
        for e in log if isinstance(log, list) else []:
            if "PERLU PERBAIKAN" not in str(e.get("verdict", "")).upper():
                continue
            ringkasan = str(e.get("ringkasan", e.get("judul", "?")))
            kunci = "r6:{}:{}".format(agen, _kunci_teks(ringkasan))
            pesan, _info = kirim_pesan(
                agen, 5, "permintaan-perbaikan", "normal",
                "Perlu perbaikan (penjaga {}): {}.".format(
                    _nama(agen), ringkasan),
                {"verdict": e.get("verdict"), "saran": e.get("saran", ""),
                 "catatan": "Perbaiki draf sesuai saran penjaga; suara/wajah "
                            "terkunci Oyen & Momo tidak boleh diubah."},
                sumber="aturan-rute-R6", kunci=kunci, data_dir=folder)
            if pesan:
                dibuat.append(pesan)
    if not dibuat:
        return dibuat, "R6 penjaga: tidak ada verdict PERLU PERBAIKAN yang baru."
    return dibuat, "R6 penjaga: {} pesan baru.".format(len(dibuat))


def _cek_r7(data, folder):
    """Proyek game/aplikasi selesai -> Agent 2 (promosi) + Agent 7 (catat)."""
    dibuat = []
    proyek = _baca_data_bersama("game_data.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() not in ("selesai", "diterbitkan"):
            continue
        nama = str(p.get("nama", "?"))
        for ke, tujuan in ((2, "promosi"), (7, "pencatatan pemasukan")):
            kunci = "r7:{}:{}".format(_kunci_teks(nama), ke)
            pesan, _info = kirim_pesan(
                9, ke, "pemberitahuan", "normal",
                "Proyek '{}' selesai — lanjut {}.".format(nama, tujuan),
                {"nama_proyek": nama, "jenis": p.get("jenis", ""),
                 "catatan": "Penerbitan gratis (itch.io/website/Game Jolt); "
                            "pemasukan dicatat Agent 7 bila sudah ada."},
                sumber="aturan-rute-R7", kunci=kunci, data_dir=folder)
            if pesan:
                dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R7 game: BELUM CUKUP DATA — game_data.json masih kosong "
                        "(belum ada proyek yang dilacak).")
    return dibuat, "R7 game selesai: {} pesan baru.".format(len(dibuat))


def _cek_r8(data, folder):
    """Terjemahan selesai -> Agent 2 (promosi edisi Inggris)."""
    dibuat = []
    prog = _baca_data_bersama("terjemah_progress.json", {}, folder)
    for buku, status in prog.items() if isinstance(prog, dict) else []:
        if str(status).lower() != "selesai":
            continue
        kunci = "r8:" + _kunci_teks(str(buku))
        pesan, _info = kirim_pesan(
            8, 2, "translation-job", "normal",
            "Terjemahan '{}' selesai — siap dipromosikan.".format(buku),
            {"judul_inggris": buku,
             "catatan": "Terbit global (KDP/Google Play) hanya setelah Cipta "
                        "menyetujui."},
            sumber="aturan-rute-R8", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not prog:
        return dibuat, ("R8 terjemah: BELUM CUKUP DATA — belum ada progres "
                        "terjemahan yang dicatat.")
    return dibuat, "R8 terjemah selesai: {} pesan baru.".format(len(dibuat))


def _cek_r11(data, folder):
    """Spesifikasi 9A selesai -> 9B (bangun & uji)."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "spesifikasi-selesai":
            continue
        nama = str(p.get("nama", "?"))
        kunci = "r11:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            "9A", "9B", "product-brief", "normal",
            "Spesifikasi '{}' selesai — lanjut bangun & uji.".format(nama),
            {"nama_proyek": nama, "jenis": p.get("jenis", ""),
             "tahap": "spesifikasi-selesai",
             "catatan": "Spesifikasi ada di data/produksi_game.json; "
                        "uji dengan 5 butir cek tim 9B sebelum lanjut ke 9C."},
            sumber="aturan-rute-R11", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R11 spesifikasi: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R11 spesifikasi selesai: {} pesan baru.".format(len(dibuat))


def _cek_r12(data, folder):
    """Proyek lolos uji 9B -> 9C (listing toko)."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "diuji-lolos":
            continue
        nama = str(p.get("nama", "?"))
        kunci = "r12:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            "9B", "9C", "draft-approval", "normal",
            "Proyek '{}' lolos uji — lanjut buat listing toko.".format(nama),
            {"nama_proyek": nama, "jenis": p.get("jenis", ""),
             "tahap": "diuji-lolos",
             "catatan": "Hasil uji ada di data/produksi_game.json; "
                        "harga tetap 'bisa negosiasi' sampai Cipta mematok harga."},
            sumber="aturan-rute-R12", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R12 uji lolos: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R12 uji lolos: {} pesan baru.".format(len(dibuat))


def _cek_r13(data, folder):
    """Proyek siap jual 9C -> Agent 2 (promosi/penjualan)."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "siap-jual":
            continue
        nama = str(p.get("nama", "?"))
        kunci = "r13:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            "9C", 2, "draft-approval", "normal",
            "Listing '{}' siap — lanjut promosi/penjualan.".format(nama),
            {"nama_proyek": nama, "jenis": p.get("jenis", ""),
             "tahap": "siap-jual",
             "catatan": "Listing ada di data/produksi_game.json; "
                        "penawaran dikirim hanya setelah Cipta menyetujui teks persisnya."},
            sumber="aturan-rute-R13", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R13 siap jual: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R13 siap jual: {} pesan baru.".format(len(dibuat))


def _cek_r14(data, folder):
    """Spesifikasi bebas (tanpa klaim) -> builder paralel 9D/9E."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "spesifikasi-selesai":
            continue
        if (p.get("klaim") or {}).get("oleh"):
            continue
        nama = str(p.get("nama", "?"))
        for ke in ("9D", "9E"):
            kunci = "r14:{}:{}".format(_kunci_teks(nama), ke)
            pesan, _info = kirim_pesan(
                "9B", ke, "product-brief", "normal",
                "Spesifikasi '{}' bebas — klaim dulu, lalu bangun & uji.".format(nama),
                {"nama_proyek": nama, "jenis": p.get("jenis", ""),
                 "tahap": "spesifikasi-selesai",
                 "catatan": "Proyek belum diklaim tim bangun mana pun. Klaim "
                            "dulu di tab 9D/9E — klaim pertama menang, tim lain "
                            "yang mencoba akan ditolak (anti double-build)."},
                sumber="aturan-rute-R14", kunci=kunci, data_dir=folder)
            if pesan:
                dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R14 builder bebas: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R14 spesifikasi bebas: {} pesan baru.".format(len(dibuat))


def _cek_r15(data, folder):
    """Proyek lolos uji tim 9D/9E -> verifikasi independen 9F."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "diuji-lolos":
            continue
        hasil = p.get("hasil_uji") or {}
        if str(hasil.get("diuji_oleh", "")) not in ("9D", "9E"):
            continue
        if (p.get("verifikasi_9f") or {}).get("tanggal"):
            continue
        nama = str(p.get("nama", "?"))
        kunci = "r15:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            hasil.get("diuji_oleh", "9D"), "9F", "draft-approval", "normal",
            "Proyek '{}' lolos uji tim {} — lanjut verifikasi independen 9F.".format(
                nama, hasil.get("diuji_oleh", "?")),
            {"nama_proyek": nama, "jenis": p.get("jenis", ""),
             "tahap": "diuji-lolos", "diuji_oleh": hasil.get("diuji_oleh"),
             "catatan": "Verifikasi 9F memakai 7 butir cek (5 butir uji + "
                        "demo jalan + listing benar)."},
            sumber="aturan-rute-R15", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R15 verifikasi 9F: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R15 uji 9D/9E lolos: {} pesan baru.".format(len(dibuat))


def _cek_r16(data, folder):
    """Proyek lolos verifikasi 9F -> 9C (listing toko)."""
    dibuat = []
    proyek = _baca_data_bersama("produksi_game.json", [], folder)
    for p in proyek if isinstance(proyek, list) else []:
        if str(p.get("status", "")).lower() != "diuji-lolos":
            continue
        verif = p.get("verifikasi_9f") or {}
        if not verif.get("lolos"):
            continue
        nama = str(p.get("nama", "?"))
        kunci = "r16:" + _kunci_teks(nama)
        pesan, _info = kirim_pesan(
            "9F", "9C", "draft-approval", "normal",
            "Proyek '{}' lolos verifikasi 9F — lanjut buat listing toko.".format(nama),
            {"nama_proyek": nama, "jenis": p.get("jenis", ""),
             "tahap": "diuji-lolos",
             "catatan": "Hasil verifikasi 9F ada di data/produksi_game.json; "
                        "harga tetap 'bisa negosiasi' sampai Cipta mematok harga."},
            sumber="aturan-rute-R16", kunci=kunci, data_dir=folder)
        if pesan:
            dibuat.append(pesan)
    if not proyek:
        return dibuat, ("R16 verifikasi lolos: BELUM CUKUP DATA — produksi_game.json "
                        "masih kosong (belum ada proyek yang dilacak).")
    return dibuat, "R16 verifikasi 9F lolos: {} pesan baru.".format(len(dibuat))


CEK_RUTE = [("R1", "Riset → Produksi", _cek_r1),
            ("R2", "Produksi → Penjualan/Terjemah", _cek_r2),
            ("R3", "Lomba → Produksi", _cek_r3),
            ("R4", "Keuangan → Muse", _cek_r4),
            ("R5", "Email → agent terkait", _cek_r5),
            ("R6", "Penjaga → Produksi", _cek_r6),
            ("R7", "Game → Penjualan/Keuangan", _cek_r7),
            ("R8", "Terjemah → Penjualan", _cek_r8),
            ("R11", "Spesifikasi → Bangun", _cek_r11),
            ("R12", "Uji lolos → Jualan", _cek_r12),
            ("R13", "Siap jual → Penjualan", _cek_r13),
            ("R14", "Spesifikasi bebas → Builder paralel", _cek_r14),
            ("R15", "Uji 9D/9E lolos → Verifikasi 9F", _cek_r15),
            ("R16", "Verifikasi 9F lolos → Jualan", _cek_r16)]


def evaluasi_rute(data_dir=None):
    """Jalankan semua aturan rute aktif. Kembalikan (pesan_baru, baris_laporan)."""
    folder = Path(data_dir or DATA_DIR)
    data = _muat(folder)
    semua_baru = []
    baris = []
    for rid, nama, fungsi in CEK_RUTE:
        aturan = next((a for a in ATURAN_RUTE if a["id"] == rid), None)
        if aturan and not aturan.get("aktif", True):
            baris.append("- {} {}: nonaktif (dilewati).".format(rid, nama))
            continue
        try:
            baru, laporan = fungsi(data, folder)
        except Exception as exc:  # noqa: BLE001 — satu aturan gagal, lanjut
            baris.append("- {} {}: GAGAL ({}: {}).".format(rid, nama,
                                                           type(exc).__name__, exc))
            continue
        semua_baru.extend(baru)
        baris.append("- " + laporan)
    return semua_baru, baris


# ---------------------------------------------------------------------------
# Siklus Harian — pemeriksaan berurutan sesuai ketergantungan
# ---------------------------------------------------------------------------
URUTAN_SIKLUS = [
    ("1", "Riset (Agent 10) — peluang layak → Produksi", ["R1"]),
    ("2", "Produksi (Agent 5) — draf baru → Penjualan/Terjemah", ["R2"]),
    ("3", "Lomba (Agent 6) — tenggat dekat → Produksi", ["R3"]),
    ("4", "Keuangan (Agent 7) — payout → Muse", ["R4"]),
    ("5", "Email (Agent 13) — email penting → agent terkait", ["R5"]),
    ("6", "Penjaga (Agent 11/12) — PERLU PERBAIKAN → Produksi", ["R6"]),
    ("7", "Game (Agent 9 + tim 9A/9B/9C/9D/9E/9F) — alur spesifikasi → bangun → verifikasi → jualan",
     ["R7", "R11", "R12", "R13", "R14", "R15", "R16"]),
    ("8", "Terjemah (Agent 8) — terjemahan selesai → Penjualan", ["R8"]),
]


def jalankan_siklus_harian(data_dir=None):
    """Satu kali jalan Siklus Harian (mode template — tanpa panggilan eksternal).
    Kembalikan laporan Markdown."""
    folder = Path(data_dir or DATA_DIR)
    tanggal, waktu = _cap_waktu()
    baris = ["# 🔄 Siklus Harian — {} {}\n".format(tanggal, waktu),
             "Pemeriksaan data bersama sesuai urutan ketergantungan "
             "(riset → produksi → penjualan/terjemah → lomba/keuangan → "
             "email → penjaga → game → terjemah). Semua yang diposting adalah "
             "DRAF/pengingat — bukan perintah otomatis, bukan kirim/upload.\n"]
    total_baru = 0
    data = _muat(folder)
    for nomor, judul, rids in URUTAN_SIKLUS:
        baris.append("## Langkah {} — {}".format(nomor, judul))
        for rid in rids:
            fungsi = next(f for r, _n, f in CEK_RUTE if r == rid)
            try:
                baru, laporan = fungsi(data, folder)
            except Exception as exc:  # noqa: BLE001
                baris.append("- {} GAGAL ({}: {}).".format(rid, type(exc).__name__, exc))
                continue
            total_baru += len(baru)
            baris.append("- " + laporan)
            for p in baru:
                baris.append("  - {} → {}: {}".format(
                    _nama(p["dari_agent"]), _nama(p["ke_agent"]), p["ringkasan"]))
    # R9: ringkasan ke Muse.
    ringkasan = ("Siklus Harian {} {} selesai: {} pesan baru diposting ke bus "
                 "(0 duplikat). Periksa tab Koordinasi; handoff tetap dibuat "
                 "Muse lewat Papan Handoff setelah diperiksa.".format(
                     tanggal, waktu, total_baru))
    kirim_pesan("Sistem", "Muse", "laporan-harian", "normal", ringkasan,
                {"total_pesan_baru": total_baru, "tanggal": tanggal},
                sumber="aturan-rute-R9",
                kunci="r9:" + tanggal, data_dir=folder)
    baris.append("\n**Total pesan baru: {}** — ringkasan diposting ke Muse (R9).".format(
        total_baru))
    _tambah_log("Siklus Harian {} {}: {} pesan baru.".format(
        tanggal, waktu, total_baru), folder)
    data = _muat(folder)
    data.setdefault("meta", {})["siklus_terakhir"] = "{} {}".format(tanggal, waktu)
    data["meta"]["siklus_total_pesan_baru"] = total_baru
    _simpan(data, folder)
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# Penyajian untuk UI
# ---------------------------------------------------------------------------
def teks_papan(data_dir=None):
    ringkasan = ringkasan_status(data_dir)
    total = sum(v["total"] for v in ringkasan.values())
    baru = sum(v["baru"] for v in ringkasan.values())
    baris = ["# 🔄 Papan Koordinasi — Message Bus Antar-Agent\n",
             "Satu jalur pesan antar-agent di dalam Pusat Komando. "
             "Pesan di sini adalah **pengingat/DRAF**, bukan perintah otomatis: "
             "agent penerima membacanya di tabnya, Muse memeriksa, dan Cipta "
             "tetap memegang persetujuan untuk apa pun yang keluar "
             "(upload/kirim/bayar/terbit).\n",
             "**Total pesan: {}** (baru: **{}**). Status: baru → dibaca → "
             "dikerjakan → selesai / ditolak.\n".format(total, baru),
             "## 📥 Inbox per agent (pesan masuk)"]
    for agen in AGEN_KUNCI:
        v = ringkasan.get(str(agen), {"baru": 0, "dibaca": 0, "dikerjakan": 0,
                                      "selesai": 0, "ditolak": 0, "total": 0})
        baris.append("- **{}**: {} pesan (baru {}, dikerjakan {}, selesai {}, "
                     "ditolak {})".format(_nama(agen), v["total"], v["baru"],
                                          v["dikerjakan"], v["selesai"], v["ditolak"]))
    meta = _muat(data_dir).get("meta", {})
    if meta.get("siklus_terakhir"):
        baris.append("\nSiklus Harian terakhir: **{}** ({} pesan baru).".format(
            meta["siklus_terakhir"], meta.get("siklus_total_pesan_baru", "?")))
    else:
        baris.append("\nSiklus Harian belum pernah dijalankan.")
    return "\n".join(baris)


def tabel_pesan(data_dir=None):
    return [[p.get("id", ""), _nama(p.get("dari_agent")),
             _nama(p.get("ke_agent")), p.get("jenis", ""),
             p.get("prioritas", ""), p.get("ringkasan", ""),
             p.get("status", ""), "{} {}".format(p.get("tanggal", ""),
                                                p.get("waktu", "")),
             p.get("sumber", "")]
            for p in _muat(data_dir)["pesan"]]


def tabel_aturan():
    return [[a["id"], a["nama"], _nama(a["dari"]) if not isinstance(a["dari"], list)
             else ", ".join(_nama(x) for x in a["dari"]),
             _nama(a["ke"]) if not isinstance(a["ke"], list)
             else ", ".join(_nama(x) for x in a["ke"]),
             a["jenis"], a["prioritas"], a["pemicu"],
             "Aktif" if a.get("aktif", True) else "Nonaktif"]
            for a in ATURAN_RUTE]


def teks_log(n=30, data_dir=None):
    log = ambil_log(n, data_dir)
    if not log:
        return "Belum ada aktivitas koordinasi."
    return "\n".join("- {} {} — {}".format(e.get("tanggal", ""), e.get("waktu", ""),
                                           e.get("teks", "")) for e in log)
