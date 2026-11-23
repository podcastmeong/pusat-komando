# ======================================================================
# PUSAT KOMANDO — salinan dari agent-keuangan (Agent 7 Keuangan).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
"""Agent Keuangan Podcast Meong — pencatat & pelapor uang masuk (GRATIS).

Agent AI ketujuh untuk Cipta. Tugasnya: mencatat pemasukan dari semua platform,
memberi ringkasan harian/mingguan/bulanan, mengingatkan payout, dan membandingkan
pemasukan dengan target. Semua angka dimasukkan MANUAL dari laporan platform.

ATURAN KERAS (tidak boleh dilanggar):
- Agent TIDAK PERNAH memindahkan, menarik, atau mentransfer uang apa pun.
- Transfer / pencairan HANYA dengan persetujuan eksplisit Cipta.
- Agent TIDAK masuk ke akun platform mana pun (tidak ada kredensial).
- Semua angka dimasukkan manual oleh pengguna/Muse dari laporan platform.
- Target adalah TARGET, bukan janji — tampilkan dengan jujur.

Teknis: Python + Gradio + Gemini free tier (gemini-4-hydrogen).
API key HANYA dari environment variable GEMINI_API_KEY — tidak pernah
tertulis di file. Tanpa key, agent tetap jalan dalam mode data lokal
(template + knowledge base), tanpa jawaban AI.
"""

import json
import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import gradio as gr

# ---------------------------------------------------------------- konstanta
KURS_USD_KE_RP = 16500  # asumsi eksplisit; dipakai bila ada pemasukan USD
TARGET_BULAN_1_MIN = 3_000_000   # Rp — TARGET Bulan 1 (bukan janji)
TARGET_BULAN_1_MAX = 25_000_000  # Rp — TARGET Bulan 1 (bukan janji)
ZONA = ZoneInfo("Asia/Jakarta")
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "keuangan_data.json")  # PUSAT KOMANDO: folder data bersama
BASELINE_TANGGAL = "2026-11-18"
BASELINE_CATATAN = "Uang masuk Rp0 / $0 di semua platform per 18 Nov 2026."

STATUS_PILIHAN = ["diterima", "menunggu", "dicairkan"]
MATA_UANG_PILIHAN = ["Rp", "USD"]

PLATFORMS = [
    "KaryaKarsa", "Lynk.id", "Mayar", "Zazzle", "Adobe Stock", "Dreamstime",
    "Saweria", "Trakteer", "TikTok", "YouTube", "Impact.com / Temu",
    "Google Play Books", "AdArena", "Lainnya",
]

# Informasi payout per platform — hanya yang diketahui; yang belum diketahui
# ditulis "cek dasbor" (jangan mengarang ambang minimum).
PAYOUT_INFO = {
    "KaryaKarsa": {
        "metode": "Transfer bank (cek dasbor KaryaKarsa)",
        "jadwal": "Sesuai ketentuan KaryaKarsa",
        "catatan": "Kreator dapat 90%. eBook Rp19.000–29.000.",
    },
    "Lynk.id": {
        "metode": "Payout tersimpan & terverifikasi",
        "jadwal": "Sesuai ketentuan Lynk.id",
        "catatan": "Payout sudah disimpan dan diverifikasi 17 Nov 2026.",
    },
    "Mayar": {
        "metode": "BCA tersimpan",
        "jadwal": "Sesuai ketentuan Mayar",
        "catatan": "KYC masih pending.",
    },
    "Zazzle": {
        "metode": "PayPal",
        "jadwal": "Sesuai ketentuan Zazzle",
        "catatan": "W-8BEN terkirim, menunggu pemrosesan Zazzle.",
    },
    "Adobe Stock": {
        "metode": "PayPal",
        "jadwal": "Sesuai ketentuan Adobe Stock",
        "catatan": "W-8BEN valid s.d. 31 Des 2028. Unduhan & penghasilan masih 0.",
    },
    "Dreamstime": {
        "metode": "PayPal (cek dasbor)",
        "jadwal": "Sesuai ketentuan Dreamstime",
        "catatan": "28 foto online, penjualan masih 0.",
    },
    "Saweria": {
        "metode": "Cashout ke BCA tersimpan",
        "jadwal": "Kapan saja (cek dasbor Saweria)",
        "catatan": "Akun aktif, cashout BCA sudah tersimpan.",
    },
    "Trakteer": {
        "metode": "TERTUNDA — butuh info cabang BCA dari Cipta",
        "jadwal": "Menunggu info dari Cipta",
        "catatan": "Payout belum bisa diatur sebelum info cabang BCA dilengkapi.",
    },
    "TikTok": {
        "metode": "Belum monetisasi",
        "jadwal": "-",
        "catatan": "Rp0 — belum ada penghasilan dari TikTok.",
    },
    "YouTube": {
        "metode": "Belum monetisasi (butuh 1.000 subscriber)",
        "jadwal": "-",
        "catatan": "Rp0 — 75 subscriber per 18 Nov 2026.",
    },
    "Impact.com / Temu": {
        "metode": "Menunggu 500 follower",
        "jadwal": "-",
        "catatan": "Temu butuh 500+ follower; saat ini 73 subscriber YouTube.",
    },
    "Google Play Books": {
        "metode": "Belum tampil di toko",
        "jadwal": "Setelah peninjauan kebijakan awal selesai (s.d. 30 hari)",
        "catatan": "Info pajak akun BELUM lengkap — lengkapi agar payout bisa jalan.",
    },
    "AdArena": {
        "metode": "Transfer bank / Payoneer / USDC Solana (TANPA PayPal)",
        "jadwal": "Siklus bulanan, dibayar tanggal 15",
        "catatan": "Uang tunai hanya peringkat 1–15; peringkat 16–40 dapat kredit Kolbo AI.",
    },
    "Lainnya": {
        "metode": "Cek ketentuan platform",
        "jadwal": "-",
        "catatan": "Isi manual di kolom produk.",
    },
}

# ---------------------------------------------------------------- data lokal
def data_kosong():
    return {
        "baseline_tanggal": BASELINE_TANGGAL,
        "baseline_catatan": BASELINE_CATATAN,
        "kurs_usd_ke_rp": KURS_USD_KE_RP,
        "entries": [],  # tiap entry: tanggal, platform, produk, jumlah, mata_uang, status
    }


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "entries" in data:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    data = data_kosong()
    save_data(data)
    return data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- util
def format_rp(nilai):
    return "Rp" + f"{nilai:,.0f}".replace(",", ".")


def format_usd(nilai):
    return "$" + f"{nilai:,.2f}"


def ke_rupiah(jumlah, mata_uang):
    return jumlah * KURS_USD_KE_RP if mata_uang == "USD" else jumlah


def hari_ini():
    return datetime.now(ZONA).date()


def parse_tanggal(teks):
    try:
        return date.fromisoformat(teks.strip())
    except ValueError:
        return None


def bar_ascii(nilai, maksimum, lebar=20):
    if maksimum <= 0:
        return ""
    penuh = int(round(nilai / maksimum * lebar))
    return "█" * penuh + "░" * (lebar - penuh)


# ---------------------------------------------------------------- fitur 1: catat
def tambah_pemasukan(tanggal, platform, produk, jumlah, mata_uang, status):
    """Tambah satu pemasukan. Mengembalikan (pesan, tabel)."""
    tgl = parse_tanggal(tanggal) if tanggal else None
    if tgl is None:
        return "Tanggal tidak valid. Pakai format YYYY-MM-DD, contoh 2026-11-18.", tabel_entries()
    if not produk or not str(produk).strip():
        return "Produk/lomba wajib diisi (contoh: eBook Kolam, AdArena The Last Key).", tabel_entries()
    try:
        jumlah = float(jumlah)
    except (TypeError, ValueError):
        return "Jumlah harus angka, contoh 29000 atau 25.", tabel_entries()
    if jumlah <= 0:
        return "Jumlah harus lebih dari 0.", tabel_entries()
    if platform not in PLATFORMS:
        platform = "Lainnya"
    if status not in STATUS_PILIHAN:
        status = "diterima"

    data = load_data()
    data["entries"].append({
        "tanggal": tgl.isoformat(),
        "platform": platform,
        "produk": str(produk).strip(),
        "jumlah": jumlah,
        "mata_uang": mata_uang,
        "status": status,
    })
    data["entries"].sort(key=lambda e: e["tanggal"])
    save_data(data)
    setara = ke_rupiah(jumlah, mata_uang)
    pesan = (
        f"Tercatat: {platform} — {produk} — "
        f"{format_usd(jumlah) if mata_uang == 'USD' else format_rp(jumlah)} "
        f"(setara {format_rp(setara)}) — {status}."
    )
    return pesan, tabel_entries()


def hapus_pemasukan(nomor):
    """Hapus entry berdasarkan nomor baris (1-based). Mengembalikan (pesan, tabel)."""
    data = load_data()
    try:
        idx = int(nomor) - 1
    except (TypeError, ValueError):
        return "Nomor baris harus angka, contoh 1.", tabel_entries()
    if idx < 0 or idx >= len(data["entries"]):
        return f"Tidak ada baris nomor {nomor}.", tabel_entries()
    terhapus = data["entries"].pop(idx)
    save_data(data)
    return (
        f"Dihapus: {terhapus['platform']} — {terhapus['produk']} "
        f"({terhapus['tanggal']}).",
        tabel_entries(),
    )


def tabel_entries():
    data = load_data()
    baris = []
    for i, e in enumerate(data["entries"], start=1):
        jumlah_txt = (
            format_usd(e["jumlah"]) if e["mata_uang"] == "USD"
            else format_rp(e["jumlah"])
        )
        baris.append([
            i, e["tanggal"], e["platform"], e["produk"], jumlah_txt,
            e["mata_uang"], format_rp(ke_rupiah(e["jumlah"], e["mata_uang"])),
            e["status"],
        ])
    return baris


# ---------------------------------------------------------------- fitur 2: ringkasan
def ringkasan_markdown():
    data = load_data()
    entries = data["entries"]
    hari = hari_ini()
    awal_minggu = hari - timedelta(days=hari.weekday())  # Senin
    awal_bulan = hari.replace(day=1)

    def total_rp(filter_fn):
        return sum(
            ke_rupiah(e["jumlah"], e["mata_uang"])
            for e in entries if filter_fn(e)
        )

    def tgl(e):
        return parse_tanggal(e["tanggal"]) or date.min

    total_hari = total_rp(lambda e: tgl(e) == hari)
    total_minggu = total_rp(lambda e: awal_minggu <= tgl(e) <= hari)
    total_bulan = total_rp(lambda e: tgl(e) >= awal_bulan)
    total_semua = total_rp(lambda e: True)
    total_menunggu = total_rp(lambda e: e["status"] == "menunggu")
    total_dicairkan = total_rp(lambda e: e["status"] == "dicairkan")

    def dua_mata_uang(total):
        return f"{format_rp(total)} (≈ {format_usd(total / KURS_USD_KE_RP)})"

    md = []
    md.append("## Ringkasan Pemasukan\n")
    md.append(f"Titik awal: **{data.get('baseline_catatan', BASELINE_CATATAN)}**")
    md.append(f"Kurs asumsi: Rp{KURS_USD_KE_RP:,}/USD.\n".replace(",", "."))
    md.append(f"- **Hari ini ({hari.isoformat()})**: {dua_mata_uang(total_hari)}")
    md.append(f"- **Minggu ini (sejak {awal_minggu.isoformat()})**: {dua_mata_uang(total_minggu)}")
    md.append(f"- **Bulan ini (sejak {awal_bulan.isoformat()})**: {dua_mata_uang(total_bulan)}")
    md.append(f"- **Total semua**: {dua_mata_uang(total_semua)}")
    md.append(f"- Menunggu (belum diterima): {dua_mata_uang(total_menunggu)}")
    md.append(f"- Sudah dicairkan: {dua_mata_uang(total_dicairkan)}\n")

    # Per platform
    per_platform = {}
    for e in entries:
        per_platform[e["platform"]] = per_platform.get(e["platform"], 0) + ke_rupiah(e["jumlah"], e["mata_uang"])
    md.append("### Per Platform\n")
    if not per_platform:
        md.append("_Belum ada pemasukan tercatat._\n")
    else:
        maks = max(per_platform.values())
        for p, v in sorted(per_platform.items(), key=lambda kv: -kv[1]):
            md.append(f"- {p}: {format_rp(v)} {bar_ascii(v, maks)}")

    # Per produk
    per_produk = {}
    for e in entries:
        per_produk[e["produk"]] = per_produk.get(e["produk"], 0) + ke_rupiah(e["jumlah"], e["mata_uang"])
    md.append("\n### Per Produk / Lomba\n")
    if not per_produk:
        md.append("_Belum ada pemasukan tercatat._\n")
    else:
        maks = max(per_produk.values())
        for p, v in sorted(per_produk.items(), key=lambda kv: -kv[1]):
            md.append(f"- {p}: {format_rp(v)} {bar_ascii(v, maks)}")

    # Tren 7 hari terakhir (ASCII)
    md.append("\n### Tren 7 Hari Terakhir\n")
    ada = False
    for i in range(6, -1, -1):
        d = hari - timedelta(days=i)
        v = total_rp(lambda e, d=d: tgl(e) == d)
        if v > 0:
            ada = True
        md.append(f"- {d.isoformat()}: {format_rp(v)}")
    if not ada:
        md.append("_Belum ada pemasukan dalam 7 hari terakhir._")
    return "\n".join(md)


# ---------------------------------------------------------------- fitur 3: payout
def payout_markdown():
    md = ["## Pengingat Payout\n"]
    md.append("Agent ini **hanya mencatat dan mengingatkan** — agent **TIDAK BISA** menarik atau mentransfer uang. Pencairan hanya dengan persetujuan Cipta.\n")
    data = load_data()
    diterima = {}
    for e in data["entries"]:
        if e["status"] in ("diterima", "menunggu"):
            diterima[e["platform"]] = diterima.get(e["platform"], 0) + ke_rupiah(e["jumlah"], e["mata_uang"])
    for p in PLATFORMS:
        info = PAYOUT_INFO.get(p, PAYOUT_INFO["Lainnya"])
        saldo = diterima.get(p, 0)
        md.append(f"### {p}")
        md.append(f"- Metode: {info['metode']}")
        md.append(f"- Jadwal: {info['jadwal']}")
        md.append(f"- Catatan: {info['catatan']}")
        md.append(f"- Saldo tercatat (diterima/menunggu): {format_rp(saldo)}\n")
    md.append("### Yang Masih Tertunda")
    md.append("- **Trakteer**: payout menunggu info cabang BCA dari Cipta.")
    md.append("- **Google Play Books**: info pajak akun belum lengkap — lengkapi agar payout bisa jalan; buku juga belum tampil di toko (peninjauan kebijakan awal).")
    md.append("- **Mayar**: KYC masih pending.")
    md.append("- **Zazzle**: W-8BEN terkirim, menunggu pemrosesan.")
    md.append("- **Impact.com / Temu**: menunggu 500 follower sebelum bisa menghasilkan.")
    return "\n".join(md)


# ---------------------------------------------------------------- fitur 4: target
def target_markdown():
    data = load_data()
    hari = hari_ini()
    awal_bulan = hari.replace(day=1)
    total_bulan = sum(
        ke_rupiah(e["jumlah"], e["mata_uang"])
        for e in data["entries"]
        if (parse_tanggal(e["tanggal"]) or date.min) >= awal_bulan
    )
    persen_min = total_bulan / TARGET_BULAN_1_MIN * 100 if TARGET_BULAN_1_MIN else 0
    persen_max = total_bulan / TARGET_BULAN_1_MAX * 100 if TARGET_BULAN_1_MAX else 0
    sisa_min = max(0, TARGET_BULAN_1_MIN - total_bulan)

    md = ["## Target vs Realisasi\n"]
    md.append("**Target Bulan 1: Rp3.000.000 – Rp25.000.000.** Ini TARGET, bukan janji — angka realistis hanya tercapai bila ada penjualan nyata.\n")
    md.append(f"- Pemasukan bulan ini ({hari.strftime('%B %Y')}): **{format_rp(total_bulan)}**")
    md.append(f"- Terhadap batas bawah target (Rp3.000.000): **{persen_min:.1f}%** {bar_ascii(min(total_bulan, TARGET_BULAN_1_MIN), TARGET_BULAN_1_MIN)}")
    md.append(f"- Terhadap batas atas target (Rp25.000.000): **{persen_max:.1f}%** {bar_ascii(min(total_bulan, TARGET_BULAN_1_MAX), TARGET_BULAN_1_MAX)}")
    if total_bulan < TARGET_BULAN_1_MIN:
        md.append(f"- Masih kurang **{format_rp(sisa_min)}** untuk mencapai batas bawah target bulan ini.")
    else:
        md.append("- Batas bawah target bulan ini sudah tercapai.")
    md.append("\nPenilaian jujur: bila total masih Rp0, itu berarti belum ada penjualan — fokus ke agent Penjualan (cari customer) dan agent Produksi (buat produk).")
    return "\n".join(md)


# ---------------------------------------------------------------- tanya agent (Gemini / fallback)
def _model_gemini():
    """Bangun model Gemini bila ada key; bila tidak ada, kembalikan None."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=kunci)
        return genai.GenerativeModel(
            "gemini-4-hydrogen",
            system_instruction=(
                "Kamu Agent Keuangan Podcast Meong. Jawab Bahasa Indonesia, singkat dan jujur. "
                "Kamu hanya mencatat dan melaporkan uang — kamu TIDAK BISA mentransfer, menarik, "
                "atau memindahkan uang, dan tidak bisa masuk ke akun platform. Bila ditanya soal "
                "transfer/pencairan, jawab bahwa itu butuh persetujuan Cipta. "
                "Kurs asumsi Rp16.500/USD. Target Bulan 1 Rp3–25 juta adalah TARGET, bukan janji. "
                "Bila tidak tahu jawabannya, katakan tidak tahu."
            ),
        )
    except Exception:
        return None


def jawab_pertanyaan(pesan, riwayat):
    """Chat: Gemini bila ada key, bila tidak ada pakai jawaban template lokal."""
    pesan = (pesan or "").strip()
    if not pesan:
        return riwayat
    data = load_data()
    total_semua = sum(ke_rupiah(e["jumlah"], e["mata_uang"]) for e in data["entries"])
    hari = hari_ini()
    total_bulan = sum(
        ke_rupiah(e["jumlah"], e["mata_uang"])
        for e in data["entries"]
        if (parse_tanggal(e["tanggal"]) or date.min) >= hari.replace(day=1)
    )

    model = _model_gemini()
    if model is not None:
        try:
            konteks = (
                f"Data tercatat: total semua {format_rp(total_semua)}, "
                f"bulan ini {format_rp(total_bulan)}, "
                f"jumlah entry {len(data['entries'])}. "
                f"Baseline: {data.get('baseline_catatan', BASELINE_CATATAN)}"
            )
            jawaban = model.generate_content(f"{konteks}\nPertanyaan: {pesan}").text.strip()
            riwayat = riwayat + [(pesan, jawaban)]
            return riwayat
        except Exception:
            pass  # jatuh ke mode template

    rendah = pesan.lower()
    if any(k in rendah for k in ["total", "berapa", "pemasukan", "uang masuk", "saldo"]):
        jawaban = (
            f"Total tercatat: {format_rp(total_semua)} "
            f"(bulan ini {format_rp(total_bulan)}, {len(data['entries'])} entry). "
            f"Titik awal: {data.get('baseline_catatan', BASELINE_CATATAN)}"
        )
    elif any(k in rendah for k in ["target"]):
        jawaban = (
            "Target Bulan 1: Rp3.000.000–Rp25.000.000 (TARGET, bukan janji). "
            f"Bulan ini tercatat {format_rp(total_bulan)}. "
            "Lihat tab Target untuk perbandingan lengkap."
        )
    elif any(k in rendah for k in ["payout", "cair", "tarik", "transfer", "ambil uang"]):
        jawaban = (
            "Saya hanya mencatat dan mengingatkan — saya tidak bisa menarik atau mentransfer uang. "
            "Pencairan hanya dengan persetujuan Cipta. Lihat tab Payout untuk metode dan yang masih tertunda "
            "(Trakteer menunggu info cabang BCA; pajak Google Play belum lengkap)."
        )
    elif any(k in rendah for k in ["karyakarsa", "zazzle", "adobe", "saweria", "mayar", "lynk"]):
        jawaban = (
            "Ringkasan platform ada di tab Payout. Contoh: KaryaKarsa kreator dapat 90%; "
            "Zazzle & Adobe Stock payout via PayPal; Saweria cashout BCA tersimpan; "
            "AdArena dibayar tanggal 15 tiap bulan."
        )
    else:
        jawaban = (
            "Saya Agent Keuangan — saya mencatat dan melaporkan uang masuk. "
            "Tanya soal total pemasukan, target, atau payout. "
            "(Mode AI penuh butuh API key Gemini gratis di GEMINI_API_KEY; "
            "saat ini saya menjawab dari data lokal.)"
        )
    riwayat = riwayat + [(pesan, jawaban)]
    return riwayat

# ---------------------------------------------------------------- antarmuka
def build_ui():
    with gr.Blocks(title="Agent Keuangan Podcast Meong") as demo:
        gr.Markdown(
            "# 💰 Agent Keuangan Podcast Meong\n"
            "Mencatat dan melaporkan uang masuk dari semua platform.\n\n"
            "**Aturan keras:** agent ini TIDAK BISA mentransfer, menarik, atau memindahkan uang. "
            "Pencairan hanya dengan persetujuan Cipta. Semua angka dimasukkan manual dari laporan platform."
        )

        with gr.Tab("📝 Catat Pemasukan"):
            gr.Markdown(
                "Isi pemasukan dari laporan platform (dasbor KaryaKarsa, Zazzle, Adobe, dll). "
                "Status: **diterima** (uang sudah masuk), **menunggu** (sudah dicatat tapi belum masuk), "
                "**dicairkan** (sudah dipindah ke rekening/PayPal)."
            )
            with gr.Row():
                inp_tanggal = gr.Textbox(
                    label="Tanggal (YYYY-MM-DD)",
                    value=hari_ini().isoformat(),
                )
                inp_platform = gr.Dropdown(
                    label="Platform", choices=PLATFORMS, value="KaryaKarsa",
                )
            inp_produk = gr.Textbox(
                label="Produk / Lomba",
                placeholder="Contoh: eBook Kolam, Kaos Oyen Zazzle, AdArena The Last Key",
            )
            with gr.Row():
                inp_jumlah = gr.Number(label="Jumlah", value=29000)
                inp_mata_uang = gr.Dropdown(
                    label="Mata Uang", choices=MATA_UANG_PILIHAN, value="Rp",
                )
                inp_status = gr.Dropdown(
                    label="Status", choices=STATUS_PILIHAN, value="diterima",
                )
            btn_tambah = gr.Button("Catat Pemasukan", variant="primary")
            pesan_catatan = gr.Textbox(label="Hasil", interactive=False)
            tabel = gr.Dataframe(
                headers=["No", "Tanggal", "Platform", "Produk", "Jumlah",
                         "Mata Uang", "Setara Rp", "Status"],
                value=tabel_entries,
                label="Semua Pemasukan Tercatat",
                interactive=False,
            )
            with gr.Row():
                inp_hapus = gr.Number(label="Hapus baris nomor", value=1, precision=0)
                btn_hapus = gr.Button("Hapus Baris")
            btn_tambah.click(
                tambah_pemasukan,
                inputs=[inp_tanggal, inp_platform, inp_produk, inp_jumlah,
                        inp_mata_uang, inp_status],
                outputs=[pesan_catatan, tabel],
            )
            btn_hapus.click(
                hapus_pemasukan, inputs=[inp_hapus], outputs=[pesan_catatan, tabel],
            )

        with gr.Tab("📊 Ringkasan"):
            btn_ringkasan = gr.Button("Perbarui Ringkasan", variant="primary")
            out_ringkasan = gr.Markdown(value=ringkasan_markdown)
            btn_ringkasan.click(ringkasan_markdown, outputs=[out_ringkasan])

        with gr.Tab("💳 Payout & Pengingat"):
            btn_payout = gr.Button("Perbarui Info Payout", variant="primary")
            out_payout = gr.Markdown(value=payout_markdown)
            btn_payout.click(payout_markdown, outputs=[out_payout])

        with gr.Tab("🎯 Target & Tanya Agent"):
            btn_target = gr.Button("Perbarui Target", variant="primary")
            out_target = gr.Markdown(value=target_markdown)
            btn_target.click(target_markdown, outputs=[out_target])
            gr.Markdown(
                "### Tanya Agent\n"
                "Tanya soal total pemasukan, target, atau payout. "
                "Dengan API key Gemini, agent menjawab memakai AI; tanpa key, agent menjawab dari data lokal."
            )
            chat = gr.ChatInterface(
                fn=jawab_pertanyaan,
                title="Agent Keuangan",
                analytics_enabled=False,
            )
    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7860)
