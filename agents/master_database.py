# -*- coding: utf-8 -*-
"""Master Database Pusat Komando 10.0 — Tahap 1 Foundation.

Satu database operasional (SQLite) untuk seluruh Pusat Komando, sesuai
Blueprint Pusat Komando 10.0 (ChatGPT, 22 Nov 2026) + Audit 40 Agent.

12 tabel:
  AGENTS, DIVISIONS, TASKS, PROJECTS, WORKFLOWS, INTELLIGENCE,
  PRODUCTS, CUSTOMERS, FINANCE, APPROVALS, PERFORMANCE, AUDIT_LOGS

Aturan:
- Status tugas seragam 9: BACKLOG, READY, IN_PROGRESS, REVIEW, REVISION,
  PENDING_APPROVAL, APPROVED, PUBLISHED, FAILED (CHECK constraint).
- Agent TIDAK BOLEH mengubah status jadi APPROVED/PUBLISHED sendiri;
  persetujuan umum diserahkan Cipta ke Muse (perintah 22 Nov 2026, wajib;
  diperbarui 10:23). Yang KHUSUS (tetap Cipta) HANYA: bayar/kirim uang
  dan keputusan urgent. Selebihnya UMUM = Muse (termasuk video, eBook,
  kirim proposal, keputusan harga). Kata sandi/kode verifikasi bukan
  persetujuan — hanya Cipta yang bisa memasukkan/mengetuknya.
- ID tugas: TASK-0001 dst; ID proyek: PROJECT-001 dst.
- File database TIDAK di-commit (lihat .gitignore: data/memori_bersama.db
  juga tidak di-commit). Bangun ulang kapan saja dengan:
      python agents/master_database.py
  Sumber seed: data/agents.json (40 agent) + data/crm.json (48 kontak)
  + fakta terverifikasi yang ditulis di SEED_* di bawah ini.

  v2.0 (22 Nov 2026): + dashboard_markdown() (ringkasan untuk tab
  "D · Master Database" di app.py), ensure_db() (bangun bila belum ada),
  set_kpi() (isi KPI per agent), KPI nyata untuk 5 agent dari laporan
  22 Nov 2026 yang terverifikasi; sisanya NULL = belum diukur.
"""

import json
import os
import sqlite3

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "data", "master_database.db")
AGENTS_JSON = os.path.join(BASE, "data", "agents.json")
CRM_JSON = os.path.join(BASE, "data", "crm.json")

STATUSES = [
    "BACKLOG", "READY", "IN_PROGRESS", "REVIEW", "REVISION",
    "PENDING_APPROVAL", "APPROVED", "PUBLISHED", "FAILED",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS AGENTS (
    code TEXT PRIMARY KEY, name TEXT NOT NULL, division TEXT NOT NULL,
    job TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'AKTIF',
    skills TEXT NOT NULL DEFAULT '[]', updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS DIVISIONS (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, agent_count INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS TASKS (
    task_id TEXT PRIMARY KEY, project_id TEXT NOT NULL,
    agent_id TEXT NOT NULL, division TEXT, task_name TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'MEDIUM',
    status TEXT NOT NULL DEFAULT 'BACKLOG'
        CHECK (status IN ('BACKLOG','READY','IN_PROGRESS','REVIEW','REVISION',
                          'PENDING_APPROVAL','APPROVED','PUBLISHED','FAILED')),
    created_at TEXT NOT NULL, deadline TEXT, output_url TEXT,
    quality_score REAL, approval_required INTEGER NOT NULL DEFAULT 1,
    approved_by TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS PROJECTS (
    project_id TEXT PRIMARY KEY, name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'IN_PROGRESS', created_at TEXT NOT NULL,
    deadline TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS WORKFLOWS (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, schedule TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'AKTIF', owner TEXT
);
CREATE TABLE IF NOT EXISTS INTELLIGENCE (
    code TEXT PRIMARY KEY, name TEXT NOT NULL, group_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'RENCANA', notes TEXT
);
CREATE TABLE IF NOT EXISTS PRODUCTS (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, marketplace TEXT NOT NULL,
    price_usd REAL NOT NULL, status TEXT NOT NULL, url TEXT
);
CREATE TABLE IF NOT EXISTS CUSTOMERS (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, channel TEXT,
    status TEXT NOT NULL DEFAULT 'PROSPEK', notes TEXT
);
CREATE TABLE IF NOT EXISTS FINANCE (
    id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('MASUK','KELUAR')),
    amount REAL NOT NULL, currency TEXT NOT NULL DEFAULT 'USD',
    platform TEXT, description TEXT
);
CREATE TABLE IF NOT EXISTS APPROVALS (
    id TEXT PRIMARY KEY, item TEXT NOT NULL, decided_by TEXT NOT NULL,
    decision TEXT NOT NULL, decided_at TEXT NOT NULL, notes TEXT
);
CREATE TABLE IF NOT EXISTS PERFORMANCE (
    agent_code TEXT PRIMARY KEY, kpi_name TEXT NOT NULL,
    kpi_value REAL, measured_at TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS AUDIT_LOGS (
    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
    actor TEXT NOT NULL, action TEXT NOT NULL, details TEXT
);
"""

# --- Seed: 15 Intelligence Systems (Blueprint 10.0) ---
SEED_INTELLIGENCE = [
    ("I01", "Command Intelligence", "A Strategis"),
    ("I02", "Decision Intelligence", "A Strategis"),
    ("I03", "Market Intelligence", "A Strategis"),
    ("I04", "Competitor Intelligence", "A Strategis"),
    ("I05", "Trend Intelligence", "A Strategis"),
    ("I06", "Workflow Intelligence", "B Operasional"),
    ("I07", "Agent Performance Intelligence", "B Operasional"),
    ("I08", "Quality Intelligence", "B Operasional"),
    ("I09", "Memory Intelligence", "B Operasional"),
    ("I10", "Learning Intelligence", "B Operasional"),
    ("I11", "Revenue Intelligence", "C Bisnis"),
    ("I12", "Product Intelligence", "C Bisnis"),
    ("I13", "Customer Intelligence", "C Bisnis"),
    ("I14", "Risk & Security Intelligence", "D Perlindungan"),
    ("I15", "Resource Intelligence", "D Perlindungan"),
]

SEED_DIVISIONS = [
    ("D01", "Direksi", 5),
    ("D02", "Riset", 5),
    ("D03", "Produksi", 9),
    ("D04", "Marketing", 5),
    ("D05", "Penjualan", 3),
    ("D06", "Peluang & Keuangan", 3),
    ("D07", "Pendukung lintas divisi", 10),
]

# Produk terverifikasi live/draf (harga + status sesuai catatan 22 Nov 2026).
SEED_PRODUCTS = [
    ("SWARMS-001", "Skill Pusat Komando", "Swarms", 12.00, "PUBLISHED",
     "https://swarms.world/prompt/c8542bab-4ebb-4dc3-85c2-ecdb8f059af4"),
    ("PAYHIP-001", "Rindu di Ujung Senja (eBook)", "Payhip", 5.00, "PUBLISHED",
     "https://payhip.com/b/wgT2k"),
    ("PAYHIP-002", "eBook Nabi Yunus", "Payhip", 4.99, "PUBLISHED",
     "https://payhip.com/b/naSAH"),
    ("PAYHIP-003", "eBook Nabi Nuh", "Payhip", 4.99, "PUBLISHED",
     "https://payhip.com/b/Um5zX"),
    ("PAYHIP-004", "eBook Nabi Yusuf", "Payhip", 4.99, "PUBLISHED",
     "https://payhip.com/b/pjoQi"),
    ("PAYHIP-005", "eBook Nabi Musa", "Payhip", 4.99, "PUBLISHED",
     "https://payhip.com/b/sRoN9"),
    ("PAYHIP-006", "eBook Nabi Ibrahim", "Payhip", 4.99, "PUBLISHED",
     "https://payhip.com/b/QUk9F"),
    ("CODESTER-001", "Faktur & Invoice Manager", "Codester", 29.00, "DRAFT",
     "https://podcastmeong.github.io/aplikasi-faktur-invoice/"),
    ("ENVATO-001", "Kasir Toko", "Envato", 59.00, "DRAFT", None),
    ("CODECANYON-001", "Kasir Toko", "CodeCanyon", 59.00, "DRAFT", None),
]

# Persetujuan Cipta yang tercatat (keputusan.md, 22 Nov 2026).
SEED_APPROVALS = [
    ("APR-2026-11-22-01", "Tabel harga global Payhip (eBook $4,99, bundle, aplikasi, game, website, video promo, POD, musik)", "Cipta", "SETUJU", "2026-11-22 06:58", ""),
    ("APR-2026-11-22-02", "Harga skill Pusat Komando $12 (Agensi.io/Swarms/PromptBase)", "Cipta", "SETUJU", "2026-11-22 07:16", ""),
    ("APR-2026-11-22-03", "Harga aplikasi per level, level tidak disebut di toko", "Cipta", "SETUJU", "2026-11-22 08:02", ""),
    ("APR-2026-11-22-04", "Listing Codester Faktur & Invoice $29", "Cipta", "SETUJU", "2026-11-22 09:29", ""),
    ("APR-2026-11-22-05", "Kirim balasan $12 ke Joeri (Agensi.io)", "Cipta", "SETUJU", "2026-11-22 09:30", ""),
    ("APR-2026-11-22-06", "Naskah video detektif Oyen untuk produksi 21:00", "Cipta", "SETUJU", "2026-11-22 10:05", ""),
    ("APR-2026-11-22-07", "Mulai Tahap 1 Master Database Pusat Komando 10.0", "Cipta", "SETUJU", "2026-11-22 10:15", ""),
    ("APR-2026-11-22-08", "Semua persetujuan umum diserahkan ke Muse (perintah, wajib)", "Cipta", "SETUJU", "2026-11-22 10:20", "Pengecualian awal: bayar/kirim uang, video+judul+caption persis, eBook per buku, sandi/kode verifikasi, keputusan urgent."),
    ("APR-2026-11-22-09", "Perbarui aturan persetujuan: yang khusus HANYA bayar/kirim uang + keputusan urgent; selebihnya umum (termasuk video, eBook, kirim proposal, harga)", "Cipta", "SETUJU", "2026-11-22 10:23", "Mencabut pengecualian video/eBook dari APR-2026-11-22-08. Kata sandi/kode verifikasi bukan persetujuan — hanya Cipta yang memasukkan."),
]

SEED_PROJECTS = [
    ("PROJECT-001", "Eksekusi 20 Marketplace", "IN_PROGRESS", "2026-11-22", None,
     "Satu-satu dari no. 1; Swarms selesai, Codester + itch.io tertahan Turnstile."),
    ("PROJECT-002", "Pusat Komando 10.0", "IN_PROGRESS", "2026-11-22", None,
     "Blueprint + Audit ChatGPT 22 Nov 2026; Tahap 1 Foundation berjalan."),
    ("PROJECT-003", "Video Harian Podcast Meong", "IN_PROGRESS", "2026-11-15", None,
     "Upload 07:00 + 20:00 WIB; produksi 21:00 dari naskah yang disetujui."),
]

# Tugas terbuka saat database dibuat (status jujur per 22 Nov 2026 10:15).
SEED_TASKS = [
    ("TASK-0001", "PROJECT-001", "A37", "Eksekusi marketplace",
     "Listing Codester Faktur & Invoice $29", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "Turnstile gagal 2x; menunggu Cipta ketuk checkbox di browser live."),
    ("TASK-0002", "PROJECT-001", "A37", "Eksekusi marketplace",
     "Registrasi itch.io (akun SatuKiki)", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "Turnstile gagal 5x; tab t3 masih terbuka di halaman verifikasi."),
    ("TASK-0003", "PROJECT-001", "A37", "Eksekusi marketplace",
     "Registrasi PromptBase + Creative Market", "MEDIUM", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "PromptBase akun @bintangzilla JADI 11:34; S1 TERKIRIM 12:51, sedang direview (15 mnt-36 jam); payout Zoneless USDC ke Solflare terverifikasi, tanpa foto KTP. 8 listing lain terblokir (klip mentah + Share Link). Creative Market DILEWATI Cipta 12:08."),
    ("TASK-0004", "PROJECT-003", "A11", "Produksi",
     "Produksi video detektif Oyen (slot 21:00)", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, "Cipta",
     "Naskah disetujui 10:05; produksi jalan cron 21:00."),
    ("TASK-0005", "PROJECT-002", "A32", "Pendukung lintas divisi",
     "Hapus harga paket aplikasi di toko, ganti harga per aplikasi", "HIGH", "BACKLOG",
     "2026-11-22", None, None, None, 0, None,
     "Edit lewat artifact toko-aplikasi, lalu export + push + verifikasi live."),
    ("TASK-0006", "PROJECT-002", "A38", "Pendukung lintas divisi",
     "Verifikasi live demo Faktur & Invoice (harga lama harus hilang)", "MEDIUM", "APPROVED",
     "2026-11-22", None, None, None, 0, None,
     "Terverifikasi bersih live 22 Nov 12:52 — seksi Harga Aplikasi TIDAK ada; halaman hanya berisi fitur invoice + garansi Pemula/Profesional/Bisnis."),
    ("TASK-0007", "PROJECT-002", "A32", "Pendukung lintas divisi",
     "Update nama Komando 40 di semua tempat", "MEDIUM", "IN_PROGRESS",
     "2026-11-22", None, None, None, 0, None,
     "Paket skill Swarms + app Pusat Komando + listing live Swarms."),
    ("TASK-0008", "PROJECT-002", "A35", "Pendukung lintas divisi",
     "Lengkapi profil Freelancer.co.id (nama belakang + foto)", "HIGH", "PENDING_APPROVAL",
     "2026-11-22", "2026-11-23 05:00", None, None, 0, None,
     "Bidding proyek $60 tutup ~23 Nov 05:00; menunggu jawaban Cipta."),
    ("TASK-0009", "PROJECT-001", "A37", "Eksekusi marketplace",
     "Akun Whop + buat produk", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "Akun JADI 12:41 — Cipta daftar dari HP-nya, screenshot whop.com/home/ (akun Pribadi, saldo US$0,00). Verifikasi sisi Muse masih jalan (browser masuk lewat email); produk (video promo, aplikasi, eBook) belum dibuat."),
    ("TASK-0010", "PROJECT-001", "A37", "Eksekusi marketplace",
     "Akun Udemy + buat kursus AI", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "Akun JADI 12:44 — Cipta daftar dari HP-nya (login Google 12:41; email Google 12:42 + 2 kode verifikasi Udemy 12:42). Profil instructor + kursus belum dibuat; kursus dari 4 modul AI (video kuliah wajib Udemy)."),
    ("TASK-0011", "PROJECT-001", "A37", "Riset pasar",
     "Riset sukses per platform + strategi eksekusi", "HIGH", "IN_PROGRESS",
     "2026-11-22", None, None, None, 1, None,
     "Riset 7 grup SELESAI semua 22 Nov 13:04 (Swarms+Agensi; Gumroad+Payhip; PromptBase+Whop; Fiverr+Udemy; Zazzle+Etsy+CM+Adobe+Dreamstime; KaryaKarsa+Lynk+KBM+Sribu; Pinterest+YT+TikTok+IG). Semua hasil di data/strategi-platform-riset.md; strategi eksekusi target $5.000/bulan sudah disusun."),
]

SEED_WORKFLOWS = [
    ("WF-001", "Rencana pagi", "cron harian 05:00", "AKTIF", "A03"),
    ("WF-002", "Persiapan video", "cron harian 06:30", "AKTIF", "A11"),
    ("WF-003", "Cari lowongan freelance (draf saja)", "cron harian 08:00", "AKTIF", "A28"),
    ("WF-004", "Gerakan operasional", "cron harian 10:00", "AKTIF", "A03"),
    ("WF-005", "Cek email customer", "cron tiap 30 menit", "AKTIF", "A27"),
    ("WF-006", "Follow-up penjualan", "cron harian 19:30", "AKTIF", "A25"),
    ("WF-007", "Produksi video", "cron harian 21:00", "AKTIF", "A11"),
    ("WF-008", "Laporan malam", "cron harian 20:00", "AKTIF", "A03"),
    ("WF-009", "Cek balasan Joeri 24 jam (Agensi.io)", "runonce 23 Nov 09:35", "AKTIF", "A27"),
]

# KPI nyata per agent — HANYA yang terverifikasi dari laporan 22 Nov 2026.
# (kode, nama KPI, nilai, diukur, sumber)
SEED_KPI = [
    ("A04", "Skor QC terakhir (/10)", 8, "2026-11-22 10:00",
     "Video Promo POD v1 8/10 LOLOS (laporan A04, progres.json 22 Nov)."),
    ("A25", "Toko dihubungi", 7, "2026-11-22 10:00",
     "21 Nov 2026 (laporan A05, progres.json 22 Nov)."),
    ("A31", "Produk live", 7, "2026-11-22 09:56",
     "6 Payhip + 1 Swarms (tabel PRODUCTS)."),
    ("A37", "Marketplace terbit (dari 20)", 1, "2026-11-22 09:56",
     "Swarms live $12 (tabel PRODUCTS)."),
    ("A29", "Transaksi tercatat", 0, "2026-11-22 10:00",
     "FINANCE kosong; pemasukan Rp0/$0 (laporan A29)."),
]


def _load_roster():
    with open(AGENTS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for a in data["agent_30"]["agents"]:
        rows.append((
            a["code"], a["name"], a["division"], a.get("job_desc", ""),
            a.get("status", "Aktif"),
            json.dumps(a.get("skills", []), ensure_ascii=False),
            "2026-11-22",
        ))
    for a in data["agent_lama"]["agents"]:
        if not a.get("kode_baru"):
            continue
        rows.append((
            a["kode_baru"], a.get("nama_baru", ""), "Pendukung lintas divisi",
            a.get("tugas", ""), "Aktif",
            json.dumps(a.get("skills", []), ensure_ascii=False),
            "2026-11-22",
        ))
    return rows


def _load_customers():
    with open(CRM_JSON, encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for c in data.get("kontak", []):
        rows.append((
            c.get("id", ""), c.get("nama", ""), c.get("platform", ""),
            "PROSPEK",
            (c.get("jenis", "") + " / " + c.get("kategori", "")).strip(" /"),
        ))
    return rows


def build(db_path=DB_PATH, fresh=True):
    """Bangun (ulang) Master Database + seed. Kembalikan dict jumlah baris."""
    if fresh and os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.executemany("INSERT OR REPLACE INTO DIVISIONS VALUES (?,?,?)", SEED_DIVISIONS)
        conn.executemany("INSERT OR REPLACE INTO INTELLIGENCE VALUES (?,?,?,?,?)",
                         [(c, n, g, "RENCANA", "") for c, n, g in SEED_INTELLIGENCE])
        conn.executemany("INSERT OR REPLACE INTO PRODUCTS VALUES (?,?,?,?,?,?)", SEED_PRODUCTS)
        conn.executemany("INSERT OR REPLACE INTO APPROVALS VALUES (?,?,?,?,?,?)", SEED_APPROVALS)
        conn.executemany("INSERT OR REPLACE INTO PROJECTS VALUES (?,?,?,?,?,?)", SEED_PROJECTS)
        conn.executemany("INSERT OR REPLACE INTO TASKS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", SEED_TASKS)
        conn.executemany("INSERT OR REPLACE INTO WORKFLOWS VALUES (?,?,?,?,?)", SEED_WORKFLOWS)
        conn.executemany("INSERT OR REPLACE INTO AGENTS VALUES (?,?,?,?,?,?,?)", _load_roster())
        conn.executemany("INSERT OR REPLACE INTO CUSTOMERS VALUES (?,?,?,?,?)", _load_customers())
        # PERFORMANCE: KPI nyata (SEED_KPI) + sisanya NULL = belum diukur (jujur).
        _kpi = {code: (name, value, measured, notes)
                for code, name, value, measured, notes in SEED_KPI}
        perf = []
        for code in [r[0] for r in _load_roster()]:
            if code in _kpi:
                name, value, measured, notes = _kpi[code]
                perf.append((code, name, value, measured, notes))
            else:
                perf.append((code, "Tugas selesai & lolos QC (>=8/10)", None, None,
                             "Belum diukur — pengukuran per agent dimulai Tahap 1."))
        conn.executemany("INSERT OR REPLACE INTO PERFORMANCE VALUES (?,?,?,?,?)", perf)
        conn.execute(
            "INSERT INTO AUDIT_LOGS (timestamp, actor, action, details) VALUES (?,?,?,?)",
            ("2026-11-22 10:15", "Muse", "MASTER_DB_DIBUAT",
             "Tahap 1 Foundation: 12 tabel + seed 40 agent, 48 kontak, 15 intelligence."),
        )
        conn.commit()
        counts = {}
        for (t,) in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        return counts
    finally:
        conn.close()


def verify(db_path=DB_PATH):
    """Cek integritas: jumlah baris + status tugas valid + 40 agent."""
    conn = sqlite3.connect(db_path)
    try:
        problems = []
        n_agents = conn.execute("SELECT COUNT(*) FROM AGENTS").fetchone()[0]
        if n_agents != 40:
            problems.append(f"AGENTS = {n_agents}, harus 40")
        bad = conn.execute(
            "SELECT task_id, status FROM TASKS WHERE status NOT IN "
            "('BACKLOG','READY','IN_PROGRESS','REVIEW','REVISION',"
            "'PENDING_APPROVAL','APPROVED','PUBLISHED','FAILED')").fetchall()
        if bad:
            problems.append(f"Status tugas tidak valid: {bad}")
        orphan = conn.execute(
            "SELECT task_id FROM TASKS WHERE project_id NOT IN "
            "(SELECT project_id FROM PROJECTS)").fetchall()
        if orphan:
            problems.append(f"Tugas tanpa proyek: {orphan}")
        fk = conn.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            problems.append(f"Foreign key check: {fk}")
        counts = {}
        for (t,) in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        return {"counts": counts, "problems": problems}
    finally:
        conn.close()


def ensure_db(db_path=DB_PATH):
    """Bangun database bila file belum ada; kembalikan path."""
    if not os.path.exists(db_path):
        build(db_path)
    return db_path


def set_kpi(db_path, agent_code, kpi_name, value, notes=""):
    """Isi/ubah KPI satu agent (nilai terverifikasi saja)."""
    ensure_db(db_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT OR REPLACE INTO PERFORMANCE "
            "(agent_code, kpi_name, kpi_value, measured_at, notes) "
            "VALUES (?,?,?,?,?)",
            (agent_code, kpi_name, value,
             __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"), notes))
        conn.commit()
    finally:
        conn.close()


def dashboard_markdown(db_path=DB_PATH):
    """Ringkasan Master Database sebagai Markdown (untuk tab D di app.py)."""
    ensure_db(db_path)
    conn = sqlite3.connect(db_path)
    try:
        out = ["### 🗄️ Master Database v2.0 — Ringkasan\n"]
        counts = {}
        for (t,) in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name"):
            counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        out.append("**Isi:** {} agent · {} tugas · {} proyek · {} produk · "
                   "{} pelanggan · {} persetujuan · {} workflow · "
                   "{} intelligence · {} entri keuangan.".format(
                       counts.get("AGENTS", 0), counts.get("TASKS", 0),
                       counts.get("PROJECTS", 0), counts.get("PRODUCTS", 0),
                       counts.get("CUSTOMERS", 0), counts.get("APPROVALS", 0),
                       counts.get("WORKFLOWS", 0), counts.get("INTELLIGENCE", 0),
                       counts.get("FINANCE", 0)))
        masuk = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM FINANCE WHERE type='MASUK'"
        ).fetchone()[0]
        keluar = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM FINANCE WHERE type='KELUAR'"
        ).fetchone()[0]
        out.append("\n**Keuangan:** masuk ${:,.2f} · keluar ${:,.2f} · "
                   "saldo ${:,.2f}.".format(masuk, keluar, masuk - keluar))
        out.append("\n### 📋 Tugas Terbuka\n")
        out.append("| ID | Tugas | Agent | Status | Prioritas |")
        out.append("|---|---|---|---|---|")
        for row in conn.execute(
                "SELECT task_id, task_name, agent_id, status, priority FROM TASKS "
                "WHERE status NOT IN ('APPROVED','PUBLISHED','FAILED') "
                "ORDER BY task_id"):
            out.append("| {} | {} | {} | {} | {} |".format(*row))
        out.append("\n### 🛒 Produk\n")
        out.append("| ID | Produk | Marketplace | Harga | Status |")
        out.append("|---|---|---|---|---|")
        for row in conn.execute(
                "SELECT id, name, marketplace, price_usd, status FROM PRODUCTS "
                "ORDER BY status DESC, id"):
            out.append("| {} | {} | {} | ${:,.2f} | {} |".format(*row))
        out.append("\n### ✅ Persetujuan Terakhir\n")
        for row in conn.execute(
                "SELECT id, item, decided_by, decided_at FROM APPROVALS "
                "ORDER BY decided_at DESC LIMIT 5"):
            out.append("- **{}** · {} — {} ({}).".format(row[0], row[1], row[2], row[3]))
        out.append("\n### 📈 KPI per Agent (nilai kosong = belum diukur)\n")
        out.append("| Agent | KPI | Nilai |")
        out.append("|---|---|---|")
        for row in conn.execute(
                "SELECT agent_code, kpi_name, kpi_value FROM PERFORMANCE "
                "ORDER BY agent_code"):
            nilai = ("{}".format(row[2]) if row[2] is not None
                     else "belum diukur")
            out.append("| {} | {} | {} |".format(row[0], row[1], nilai))
        out.append("\n_Status tugas 9 nilai; persetujuan umum di tangan Muse, "
                   "khusus (bayar/kirim uang, keputusan urgent) di tangan Cipta._")
        return "\n".join(out)
    finally:
        conn.close()


if __name__ == "__main__":
    counts = build()
    result = verify()
    print("Master Database:", DB_PATH)
    for table, n in sorted(counts.items()):
        print(f"  {table}: {n}")
    if result["problems"]:
        print("MASALAH:", result["problems"])
        raise SystemExit(1)
    print("Verifikasi OK: 40 agent, status tugas valid, semua tugas punya proyek.")
