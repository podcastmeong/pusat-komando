# ======================================================================
# PUSAT KOMANDO — Tim 9F Verifikasi & Katalog (di bawah Agent 9 Produksi
# Game & Aplikasi). Tiga tugas:
#   (a) Verifikasi QC independen atas proyek lolos uji (9B/9D/9E):
#       checklist 5 butir yang sama seperti 9B (butir 5 = buku panduan)
#       + cek demo jalan + cek listing toko benar.
#   (b) Memperbarui katalog setiap kali status aplikasi berubah:
#       katalog-lengkap-aplikasi.md dan katalog-per-kategori/*.md
#       (status entri, tautan demo, harga, tabel ringkasan, antrean).
#   (c) Koordinator batching unggahan: mengelompokkan 5–10 demo selesai
#       per tugas unggah GitHub. BATAS JUJUR: unggahan sendiri tetap
#       berjalan berurutan, satu tugas dalam satu waktu — batching hanya
#       mengelompokkan pekerjaan, bukan memparalelkan unggahan.
# Ditambahkan 19 Nov 2026 atas perintah Cipta ("tambah 3 tim Agent 9
# agar lebih cepat").
# Aplikasi Gradio pasif; semua output adalah DRAF untuk persetujuan
# Cipta — tidak ada yang diterbitkan otomatis (SOP v1.3).
# ======================================================================
"""Tim 9F Verifikasi & Katalog — QC independen + katalog + batch unggah."""

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a09_pipa as pipa

# Daftar verifikasi 9F: 5 butir yang sama seperti 9B + 2 butir tambahan.
CHECKLIST = pipa.CHECKLIST_UJI + [
    ("demo_jalan", "Demo bisa dibuka dan dicoba (tautan demo berfungsi)"),
    ("listing_benar", "Listing toko benar (deskripsi, fitur, harga sesuai aplikasi)"),
]

TIM = "9F"

# Lokasi katalog (di luar pusat-komando; bisa ditimpa di test).
KATALOG_ROOT = Path(__file__).resolve().parent.parent.parent
KATALOG_GABUNGAN = KATALOG_ROOT / "katalog-lengkap-aplikasi.md"
KATALOG_DIR = KATALOG_ROOT / "katalog-per-kategori"
LOG_KATALOG = pipa.BASE_DIR / "log_katalog.json"
BATCH_FILE = pipa.BASE_DIR / "batch_unggah.json"

# Status pipeline -> status katalog (4 macam status katalog).
STATUS_KATALOG = {
    "antrean": "Di antrean Agent 9",
    "spesifikasi-selesai": "Sedang dibangun",
    "diuji-lolos": "Sedang dibangun",
    "siap-jual": "Sedang dibangun",
    "di-toko": "Sudah jadi",
}
STATUS_KATALOG_LANGSUNG = ["Sudah jadi", "Sedang dibangun",
                           "Di antrean Agent 9", "Kandidat"]
KETERANGAN_DEFAULT = {
    "Sudah jadi": "selesai dibangun dan masuk Toko Aplikasi.",
    "Sedang dibangun": "sedang dibangun tim Agent 9.",
    "Di antrean Agent 9": "menunggu giliran di antrean Agent 9.",
    "Kandidat": "belum dibangun, belum masuk antrean.",
}


# ---------------------------------------------------------------------------
# (a) Verifikasi QC independen
# ---------------------------------------------------------------------------
def verifikasi_proyek(nama, fitur_jalan, tanpa_error, data_contoh_benar,
                      responsif_hp, panduan_lengkap, demo_jalan, listing_benar,
                      catatan):
    """Verifikasi independen proyek berstatus diuji-lolos (7 butir cek).

    Semua butir lolos -> verifikasi_9f tercatat lolos (lanjut ke 9C).
    Ada yang gagal -> status tetap diuji-lolos, catatan perbaikan dicatat
    untuk tim bangun. Status pipeline TIDAK berubah di sini.
    """
    nama = (nama or "").strip()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), "", pipa.tabel_pipeline()
    if proyek.get("status") != "diuji-lolos":
        return ("Proyek '{}' belum bisa diverifikasi 9F (status: {}). "
                "Verifikasi hanya dari status diuji-lolos.".format(
                    nama, proyek.get("status"))), "", pipa.tabel_pipeline()
    checklist = {"fitur_jalan": bool(fitur_jalan),
                 "tanpa_error": bool(tanpa_error),
                 "data_contoh_benar": bool(data_contoh_benar),
                 "responsif_hp": bool(responsif_hp),
                 "panduan_lengkap": bool(panduan_lengkap),
                 "demo_jalan": bool(demo_jalan),
                 "listing_benar": bool(listing_benar)}
    lolos = all(checklist.values())
    proyek["verifikasi_9f"] = {
        "tanggal": pipa._hari_ini(),
        "checklist": checklist,
        "lolos": lolos,
        "catatan_perbaikan": (catatan or "").strip(),
        "diverifikasi_oleh": TIM,
    }
    proyek["terverifikasi_9f"] = lolos
    pipa.simpan_data(data)
    if lolos:
        pesan = ("✅ '{}' LOLOS VERIFIKASI 9F (QC independen). "
                 "Tim 9C bisa lanjut membuat listing toko.".format(nama))
    else:
        gagal = [label for kunci, label in CHECKLIST if not checklist[kunci]]
        pesan = ("❌ '{}' BELUM LOLOS VERIFIKASI 9F — status tetap diuji-lolos. "
                 "Yang gagal: {}. Kembalikan ke tim bangun untuk diperbaiki.".format(
                     nama, "; ".join(gagal)))
    return pesan, teks_verifikasi(proyek), pipa.tabel_pipeline()


def teks_verifikasi(proyek):
    """Hasil verifikasi 9F proyek sebagai Markdown (DRAF)."""
    hasil = proyek.get("verifikasi_9f") or {}
    if not hasil:
        return "Proyek '{}' belum pernah diverifikasi 9F.".format(proyek.get("nama", "?"))
    baris = ["# Verifikasi 9F: {n}\n".format(n=proyek.get("nama", "?")),
             "**Status:** {s} · **Tanggal:** {t} · **Verdict:** {v}".format(
                 s=proyek.get("status", "?"), t=hasil.get("tanggal", "?"),
                 v="LOLOS" if hasil.get("lolos") else "BELUM LOLOS"),
             "\n**Status:** DRAF — menunggu persetujuan Cipta.",
             "\n## Daftar Verifikasi (QC independen)"]
    for kunci, label in CHECKLIST:
        centang = "✅" if hasil.get("checklist", {}).get(kunci) else "❌"
        baris.append("- {} {}".format(centang, label))
    baris.append("\n## Catatan Perbaikan")
    baris.append(hasil.get("catatan_perbaikan") or "(tidak ada)")
    return "\n".join(baris)


# ---------------------------------------------------------------------------
# (b) Pembaruan katalog
# ---------------------------------------------------------------------------
def _nama_bersih(nama):
    """Nama proyek tanpa akhiran dalam kurung — untuk mencocokkan judul katalog."""
    return re.sub(r"\s*\(.*\)\s*$", "", str(nama or "")).strip()


def _indeks_entri(baris, nama):
    """Indeks baris judul entri katalog untuk proyek (atau None).

    Judul entri berbentuk '#### N.M Nama' (gabungan) atau '#### N.M Nama (alias)'.
    """
    target = _nama_bersih(nama).lower()
    if not target:
        return None
    for i, b in enumerate(baris):
        m = re.match(r"^#{3,4}\s+\d+\.\d+\s+(.*)$", b.strip())
        if m and target in m.group(1).lower():
            return i
    return None


def _perbarui_entri(baris, nama, status_katalog, keterangan, tautan_demo, harga):
    """Perbarui baris Status (+ Demo/Harga) satu entri katalog.

    Kembalikan True bila entri ditemukan dan baris Status diperbarui.
    """
    idx = _indeks_entri(baris, nama)
    if idx is None:
        return False
    teks_status = "- **Status:** {} — {}".format(status_katalog, keterangan)
    if tautan_demo:
        teks_status += " Demo: {}.".format(tautan_demo.strip())
    diubah = False
    for j in range(idx + 1, min(idx + 20, len(baris))):
        if baris[j].startswith("- **Status:**"):
            baris[j] = teks_status
            diubah = True
        elif harga and baris[j].startswith("- **Harga:**"):
            baris[j] = "- **Harga:** {}".format(harga.strip())
        elif baris[j].startswith("####") or baris[j].startswith("###"):
            break
    return diubah


def _hitung_status_entri(baris):
    """Hitung status entri aplikasi per kategori dari teks katalog gabungan.

    Kembalikan dict {nomor_kategori: {status: jumlah}} + urutan kategori.
    """
    hitung = {}
    urutan = []
    kategori = None
    i = 0
    while i < len(baris):
        b = baris[i]
        m = re.match(r"^#{2,3}\s+Kategori\s+(\d+)\s+—", b.strip())
        if m:
            kategori = int(m.group(1))
            if kategori not in hitung:
                hitung[kategori] = {"Sudah jadi": 0, "Sedang dibangun": 0,
                                    "Di antrean Agent 9": 0, "Kandidat": 0}
                urutan.append(kategori)
        elif re.match(r"^#{4}\s+\d+\.\d+\s+", b.strip()):
            for j in range(i + 1, min(i + 20, len(baris))):
                if baris[j].startswith("- **Status:**"):
                    teks = baris[j]
                    for status in ("Sudah jadi", "Sedang dibangun",
                                   "Di antrean Agent 9", "Kandidat"):
                        if teks.startswith("- **Status:** " + status):
                            if kategori is not None:
                                hitung[kategori][status] += 1
                            break
                    break
                if baris[j].startswith("####") or baris[j].startswith("###"):
                    break
        i += 1
    return hitung, urutan


def _perbarui_tabel_ringkas(baris):
    """Hitung ulang tabel ringkasan per kategori di katalog gabungan.

    Kembalikan True bila tabel ditemukan dan diperbarui.
    """
    awal = None
    for i, b in enumerate(baris):
        if b.strip().startswith("## Ringkasan Jumlah Produk per Kategori"):
            awal = i
            break
    if awal is None:
        return False
    hitung, urutan = _hitung_status_entri(baris)
    if not urutan:
        return False
    diubah = False
    for i in range(awal, len(baris)):
        m = re.match(r"^\|\s*(\d+)\.\s+[^|]+\|\s*(\d+)\s*\|", baris[i])
        if not m:
            if baris[i].strip().startswith("| **Subtotal aplikasi**"):
                total = {"Sudah jadi": 0, "Sedang dibangun": 0,
                         "Di antrean Agent 9": 0, "Kandidat": 0}
                for k in urutan:
                    for s in total:
                        total[s] += hitung[k][s]
                jumlah = sum(total.values())
                baris[i] = ("| **Subtotal aplikasi** | **{}** | **{}** | **{}** | "
                            "**{}** | **{}** |".format(
                                jumlah, total["Sudah jadi"], total["Sedang dibangun"],
                                total["Di antrean Agent 9"], total["Kandidat"]))
                diubah = True
                break
            continue
        nomor = int(m.group(1))
        if nomor not in hitung:
            continue
        h = hitung[nomor]
        jumlah = sum(h.values())
        nama_kategori = baris[i].split("|")[1].strip()
        baris[i] = "| {} | {} | {} | {} | {} | {} |".format(
            nama_kategori, jumlah, h["Sudah jadi"], h["Sedang dibangun"],
            h["Di antrean Agent 9"], h["Kandidat"])
        diubah = True
    return diubah


def _perbarui_kalimat_status(baris, data):
    """Perbarui angka di kalimat pengantar status (katalog gabungan)."""
    hitung = {"Sudah jadi": 0, "Di antrean Agent 9": 0}
    for p in data:
        if p.get("status") == "di-toko":
            hitung["Sudah jadi"] += 1
        elif p.get("status") == "antrean":
            hitung["Di antrean Agent 9"] += 1
    for i, b in enumerate(baris):
        if "`Sudah jadi`" in b and "aplikasi" in b:
            b2 = re.sub(r"(`Sudah jadi` \()\d+( aplikasi\))",
                        r"\g<1>{}\g<2>".format(hitung["Sudah jadi"]), b)
            b2 = re.sub(r"(`Di antrean Agent 9` \()\d+( aplikasi)",
                        r"\g<1>{}\g<2>".format(hitung["Di antrean Agent 9"]), b2)
            if b2 != b:
                baris[i] = b2
                return True
    return False


def _perbarui_baris_antrean(baris, data):
    """Bangun ulang baris 'Antrean Agent 9 (N aplikasi, urutan resmi)'."""
    antrean = [p.get("nama", "") for p in data if p.get("status") == "antrean"]
    for i, b in enumerate(baris):
        if b.strip().startswith("**Antrean Agent 9 ("):
            daftar = ", ".join("{} {}".format(n + 1, nama)
                               for n, nama in enumerate(antrean))
            baris[i] = ("**Antrean Agent 9 ({} aplikasi, urutan resmi):** {}"
                        .format(len(antrean), daftar))
            return True
    return False


def _tulis_log_katalog(entri):
    try:
        log = json.loads(LOG_KATALOG.read_text(encoding="utf-8")) \
            if LOG_KATALOG.exists() else []
        if not isinstance(log, list):
            log = []
    except (OSError, ValueError):
        log = []
    log.append(entri)
    LOG_KATALOG.parent.mkdir(parents=True, exist_ok=True)
    LOG_KATALOG.write_text(json.dumps(log, ensure_ascii=False, indent=2),
                           encoding="utf-8")


def teks_log_katalog(n=10):
    """Log perubahan katalog terakhir sebagai Markdown."""
    try:
        log = json.loads(LOG_KATALOG.read_text(encoding="utf-8")) \
            if LOG_KATALOG.exists() else []
    except (OSError, ValueError):
        log = []
    if not log:
        return "Belum ada perubahan katalog yang dicatat tim 9F."
    baris = ["# 📚 Log Perubahan Katalog (Tim 9F)\n"]
    for e in log[-n:]:
        baris.append("- **{}** — {} → {} ({}; berkas: {})".format(
            e.get("tanggal", "?"), e.get("proyek", "?"), e.get("status_baru", "?"),
            e.get("keterangan", ""), ", ".join(e.get("berkas", [])) or "-"))
    return "\n".join(baris)


def perbarui_katalog(nama, status_baru, tautan_demo="", harga="", keterangan=""):
    """Perbarui status aplikasi di katalog gabungan + katalog per kategori.

    status_baru boleh status pipeline (antrean/spesifikasi-selesai/diuji-lolos/
    siap-jual/di-toko) atau status katalog langsung (Sudah jadi/Sedang
    dibangun/Di antrean Agent 9/Kandidat). Kembalikan (pesan, laporan).
    """
    nama = (nama or "").strip()
    status_baru = (status_baru or "").strip()
    if status_baru in STATUS_KATALOG:
        status_katalog = STATUS_KATALOG[status_baru]
    elif status_baru in STATUS_KATALOG_LANGSUNG:
        status_katalog = status_baru
    else:
        return ("⚠️ Status '{}' tidak dikenal.".format(status_baru),
                teks_log_katalog())
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return ("Proyek '{}' tidak ditemukan di antrean produksi.".format(nama),
                teks_log_katalog())
    keterangan = (keterangan or "").strip() or KETERANGAN_DEFAULT[status_katalog]
    berkas_diubah = []
    # --- katalog gabungan ---
    if KATALOG_GABUNGAN.exists():
        baris = KATALOG_GABUNGAN.read_text(encoding="utf-8").splitlines()
        if _perbarui_entri(baris, nama, status_katalog, keterangan,
                           tautan_demo, harga):
            _perbarui_tabel_ringkas(baris)
            _perbarui_kalimat_status(baris, data)
            _perbarui_baris_antrean(baris, data)
            KATALOG_GABUNGAN.write_text("\n".join(baris) + "\n", encoding="utf-8")
            berkas_diubah.append(KATALOG_GABUNGAN.name)
    # --- katalog per kategori ---
    if KATALOG_DIR.is_dir():
        for path in sorted(KATALOG_DIR.glob("*.md")):
            baris = path.read_text(encoding="utf-8").splitlines()
            if _perbarui_entri(baris, nama, status_katalog, keterangan,
                               tautan_demo, harga):
                path.write_text("\n".join(baris) + "\n", encoding="utf-8")
                berkas_diubah.append("katalog-per-kategori/" + path.name)
    if not berkas_diubah:
        return ("⚠️ Entri '{}' tidak ditemukan di katalog mana pun — "
                "periksa ejaan nama proyek.".format(nama)), teks_log_katalog()
    _tulis_log_katalog({"tanggal": pipa._hari_ini(), "proyek": nama,
                        "status_baru": status_katalog, "keterangan": keterangan,
                        "berkas": berkas_diubah})
    pesan = ("✅ Katalog diperbarui: '{}' → {} (berkas: {}).".format(
        nama, status_katalog, ", ".join(berkas_diubah)))
    return pesan, teks_log_katalog()


# ---------------------------------------------------------------------------
# (c) Koordinator batching unggahan
# ---------------------------------------------------------------------------
def _muat_batch():
    try:
        data = json.loads(BATCH_FILE.read_text(encoding="utf-8")) \
            if BATCH_FILE.exists() else []
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def _simpan_batch(data):
    BATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    BATCH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")


def _id_batch_baru(data):
    return "UB-{:03d}".format(len(data) + 1)


def buat_batch(maks=10):
    """Kelompokkan demo selesai (siap-jual + ada tautan demo) jadi satu batch.

    Batch berisi 5–10 proyek. Bila kurang dari 5 proyek tersedia, batch tetap
    dibuat dengan yang ada (dicatat di pesan). Proyek yang sudah ada di batch
    'menunggu' tidak dimasukkan dua kali.
    """
    try:
        maks = int(maks)
    except (TypeError, ValueError):
        maks = 10
    maks = max(1, min(maks, 10))
    data = pipa.muat_data()
    batches = _muat_batch()
    sudah = set()
    for b in batches:
        if b.get("status") == "menunggu":
            sudah.update(b.get("proyek", []))
    kandidat = []
    for p in data:
        if p.get("status") != "siap-jual":
            continue
        if p.get("nama", "") in sudah:
            continue
        demo = ((p.get("listing") or {}).get("tautan_demo") or "").strip()
        if not demo:
            continue
        kandidat.append(p.get("nama", ""))
    if not kandidat:
        return ("⚠️ Tidak ada demo selesai yang bisa dibatch — butuh proyek "
                "siap-jual dengan tautan demo yang belum masuk batch menunggu.",
                teks_batch())
    ambil = kandidat[:maks]
    batch = {"id": _id_batch_baru(batches), "tanggal": pipa._hari_ini(),
             "proyek": ambil, "status": "menunggu",
             "catatan": "Batch unggah GitHub — dikerjakan berurutan satu tugas "
                        "dalam satu waktu; batching hanya mengelompokkan, "
                        "bukan memparalelkan unggahan."}
    batches.append(batch)
    _simpan_batch(batches)
    pesan = ("📦 Batch {} dibuat: {} demo ({}). Unggah lewat SATU tugas "
             "browser GitHub — jangan jalankan dua tugas unggah bersamaan.".format(
                 batch["id"], len(ambil), ", ".join(ambil)))
    if len(ambil) < 5:
        pesan += " (kurang dari 5 — batch kecil, boleh ditambah dulu bila mau.)"
    return pesan, teks_batch()


def tandai_diunggah(batch_id):
    """Tandai batch sudah diunggah (status menunggu -> diunggah)."""
    batch_id = (batch_id or "").strip()
    batches = _muat_batch()
    for b in batches:
        if b.get("id") == batch_id:
            if b.get("status") != "menunggu":
                return ("Batch {} sudah berstatus '{}'.".format(
                    batch_id, b.get("status"))), teks_batch()
            b["status"] = "diunggah"
            _simpan_batch(batches)
            return ("✅ Batch {} ditandai sudah diunggah ({} demo).".format(
                batch_id, len(b.get("proyek", [])))), teks_batch()
    return "⚠️ Batch {} tidak ditemukan.".format(batch_id), teks_batch()


def teks_batch():
    """Daftar batch unggahan sebagai Markdown."""
    batches = _muat_batch()
    if not batches:
        return ("Belum ada batch unggahan. Batch dibuat dari proyek siap-jual "
                "yang punya tautan demo (5–10 demo per batch).")
    baris = ["# 📦 Batch Unggahan GitHub (Tim 9F)\n",
             "Batas jujur: unggahan berjalan **berurutan, satu tugas dalam "
             "satu waktu** — batching hanya mengelompokkan pekerjaan supaya "
             "satu tugas browser membawa 5–10 demo sekaligus.\n"]
    for b in batches:
        baris.append("- **{}** ({} — {}) — {} demo: {}".format(
            b.get("id", "?"), b.get("tanggal", "?"), b.get("status", "?"),
            len(b.get("proyek", [])), ", ".join(b.get("proyek", []))))
    return "\n".join(baris)


# ---------------------------------------------------------------- Antarmuka
def bangun_ui():
    import gradio as gr

    with gr.Blocks(title="Tim 9F Verifikasi & Katalog — Agent 9",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🔍 Tim 9F Verifikasi & Katalog — Agent 9 Produksi Game & Aplikasi\n"
            "QC independen atas proyek lolos uji, pembaruan katalog tiap kali "
            "status aplikasi berubah, dan koordinator batching unggahan. "
            "Semua output adalah **DRAF untuk persetujuan Cipta** — "
            "tidak ada yang diterbitkan otomatis.\n\n"
            "Alur: antrean → spesifikasi-selesai (9A) → diuji-lolos (9B/9D/9E) → "
            "**verifikasi 9F** → siap-jual (9C) → di-toko.")
        with gr.Tabs():
            with gr.Tab("📋 Antrean Produksi"):
                gr.Markdown("Status tiap proyek di alur produksi Agent 9.")
                out_tabel = gr.Markdown(value=pipa.tabel_pipeline(), label="Antrean produksi")
                btn_muat = gr.Button("🔄 Muat Ulang Tabel")
                btn_muat.click(lambda: pipa.tabel_pipeline(), None, out_tabel,
                               api_name="muat_tabel_9f")

            with gr.Tab("✅ Verifikasi QC"):
                gr.Markdown(
                    "Verifikasi independen proyek berstatus diuji-lolos. "
                    "**Semua 7 butir harus lolos** agar proyek lanjut ke listing 9C. "
                    "Bila ada yang gagal, status tetap dan catatan perbaikan "
                    "diteruskan ke tim bangun.")
                data_awal = pipa.muat_data()
                nama_v = gr.Dropdown(
                    choices=pipa.daftar_nama(data_awal, ["diuji-lolos"]),
                    label="Proyek (diuji-lolos)")
                with gr.Row():
                    cb_fitur = gr.Checkbox(label=CHECKLIST[0][1], value=False)
                    cb_error = gr.Checkbox(label=CHECKLIST[1][1], value=False)
                with gr.Row():
                    cb_data = gr.Checkbox(label=CHECKLIST[2][1], value=False)
                    cb_hp = gr.Checkbox(label=CHECKLIST[3][1], value=False)
                cb_panduan = gr.Checkbox(label=CHECKLIST[4][1], value=False)
                cb_demo = gr.Checkbox(label=CHECKLIST[5][1], value=False)
                cb_listing = gr.Checkbox(label=CHECKLIST[6][1], value=False)
                catatan_v = gr.Textbox(
                    label="Catatan perbaikan (wajib diisi bila ada yang gagal)",
                    lines=3,
                    placeholder="contoh: demo tidak terbuka dari tautan; harga di listing beda dengan harga resmi")
                btn_verif = gr.Button("✅ Simpan Hasil Verifikasi 9F", variant="primary")
                pesan_v = gr.Textbox(label="Pesan", interactive=False)
                out_verif = gr.Markdown(label="Hasil verifikasi")
                btn_verif.click(verifikasi_proyek,
                                [nama_v, cb_fitur, cb_error, cb_data, cb_hp,
                                 cb_panduan, cb_demo, cb_listing, catatan_v],
                                [pesan_v, out_verif, out_tabel],
                                api_name="verifikasi_proyek_9f")

            with gr.Tab("📚 Perbarui Katalog"):
                gr.Markdown(
                    "Perbarui katalog (gabungan + per kategori) setiap kali status "
                    "aplikasi berubah: baris Status entri, tautan demo, harga, "
                    "tabel ringkasan, dan baris antrean Agent 9 dihitung ulang. "
                    "Perubahan dicatat di log katalog (data/log_katalog.json).")
                data_k = pipa.muat_data()
                nama_k = gr.Dropdown(
                    choices=pipa.daftar_nama(data_k),
                    label="Proyek")
                status_k = gr.Dropdown(
                    choices=["antrean", "spesifikasi-selesai", "diuji-lolos",
                             "siap-jual", "di-toko"],
                    value="di-toko", label="Status baru (pipeline)")
                demo_k = gr.Textbox(label="Tautan demo (opsional)",
                                    placeholder="contoh: https://podcastmeong.github.io/arsip-dokumen/")
                harga_k = gr.Textbox(label="Harga baru (opsional, kosongkan bila tidak berubah)",
                                     placeholder="contoh: Beli Sekali — Pemula Rp499.000 / ...")
                ket_k = gr.Textbox(label="Keterangan status (opsional)",
                                   placeholder="contoh: selesai dibangun dan masuk toko 19 Nov 2026")
                btn_kat = gr.Button("📚 Perbarui Katalog", variant="primary")
                pesan_kat = gr.Textbox(label="Pesan", interactive=False)
                out_log = gr.Markdown(value=teks_log_katalog(), label="Log perubahan katalog")
                btn_kat.click(perbarui_katalog,
                              [nama_k, status_k, demo_k, harga_k, ket_k],
                              [pesan_kat, out_log],
                              api_name="perbarui_katalog_9f")

            with gr.Tab("📦 Batch Unggahan"):
                gr.Markdown(
                    "Kelompokkan demo selesai (siap-jual + ada tautan demo) menjadi "
                    "satu batch 5–10 demo untuk SATU tugas unggah GitHub. "
                    "**Batas jujur:** unggahan tetap berjalan berurutan, satu tugas "
                    "dalam satu waktu — batching hanya mengelompokkan pekerjaan, "
                    "bukan memparalelkan unggahan. Jangan jalankan dua tugas "
                    "unggah bersamaan.")
                maks_b = gr.Number(label="Maksimal demo per batch (1–10)", value=10,
                                   precision=0)
                btn_batch = gr.Button("📦 Buat Batch Baru", variant="primary")
                pesan_b = gr.Textbox(label="Pesan", interactive=False)
                out_batch = gr.Markdown(value=teks_batch(), label="Batch unggahan")
                btn_batch.click(buat_batch, maks_b, [pesan_b, out_batch],
                                api_name="buat_batch_9f")
                gr.Markdown("### ✅ Tandai Batch Sudah Diunggah")
                batch_id = gr.Textbox(label="ID batch", placeholder="contoh: UB-001")
                btn_up = gr.Button("✅ Tandai Sudah Diunggah")
                btn_up.click(tandai_diunggah, batch_id, [pesan_b, out_batch],
                             api_name="tandai_diunggah_9f")
    return demo


if __name__ == "__main__":
    demo = bangun_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
