# ======================================================================
# PUSAT KOMANDO — Tim 9C Jualan (di bawah Agent 9 Produksi Game &
# Aplikasi). Menyiapkan listing toko (deskripsi, fitur, harga/nego),
# tombol demo, dan draf penawaran untuk tiap aplikasi/game yang selesai.
# Ditambahkan 19 Nov 2026 atas perintah Cipta ("tambah 3 tim Agent 9",
# "langsung hubungkan dengan wadah").
# Aplikasi Gradio pasif; semua output adalah DRAF untuk persetujuan
# Cipta — tidak ada yang diterbitkan otomatis (SOP v1.3).
# ======================================================================
"""Tim 9C Jualan — listing toko & penawaran aplikasi/game Agent 9."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a09_pipa as pipa


def _pecah_baris(teks):
    return [b.strip() for b in (teks or "").splitlines() if b.strip()]


def buat_listing(nama, deskripsi, fitur_utama, harga, tautan_demo):
    """Buat listing toko untuk proyek berstatus diuji-lolos; status -> siap-jual."""
    nama = (nama or "").strip()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), "", pipa.tabel_pipeline()
    if proyek.get("status") != "diuji-lolos":
        return ("Proyek '{}' belum bisa dibuatkan listing (status: {}). "
                "Listing hanya dari status diuji-lolos.".format(
                    nama, proyek.get("status"))), "", pipa.tabel_pipeline()
    fitur = _pecah_baris(fitur_utama)
    if not fitur:
        return "Daftar fitur listing wajib diisi (satu fitur per baris).", "", pipa.tabel_pipeline()
    deskripsi = (deskripsi or "").strip()
    if not deskripsi:
        return "Deskripsi listing wajib diisi.", "", pipa.tabel_pipeline()
    proyek["listing"] = {
        "tanggal": pipa._hari_ini(),
        "deskripsi": deskripsi,
        "fitur": fitur,
        "harga": (harga or "").strip() or "bisa negosiasi",
        "tautan_demo": (tautan_demo or "").strip(),
    }
    proyek["status"] = "siap-jual"
    pipa.simpan_data(data)
    return ("Listing '{}' selesai (status: siap-jual). "
            "Tandai 'di-toko' setelah masuk Toko Aplikasi.".format(nama)), teks_listing(proyek), pipa.tabel_pipeline()


def teks_listing(proyek):
    """Listing toko proyek sebagai Markdown (DRAF)."""
    listing = proyek.get("listing") or {}
    if not listing:
        return "Proyek '{}' belum punya listing toko.".format(proyek.get("nama", "?"))
    baris = ["# Listing Toko: {n}\n".format(n=proyek.get("nama", "?")),
             "**Jenis:** {j} · **Status:** {s} · **Tanggal:** {t}".format(
                 j=proyek.get("jenis", "?"), s=proyek.get("status", "?"),
                 t=listing.get("tanggal", "?")),
             "**Harga:** {}".format(listing.get("harga", "bisa negosiasi")),
             "**Demo:** {}".format(listing.get("tautan_demo") or "(belum ada)"),
             "\n**Status:** DRAF — menunggu persetujuan Cipta.",
             "\n## Deskripsi",
             listing.get("deskripsi", ""),
             "\n## Fitur"]
    for f in listing.get("fitur", []):
        baris.append("- {}".format(f))
    baris.append("\nCara pesan: WhatsApp (tautan wa.me di Toko Aplikasi), "
                 "bayar manual dulu — pembayaran otomatis + link unduhan aman "
                 "adalah pengembangan lanjutan, bukan janji v1.")
    return "\n".join(baris)


def draf_penawaran(nama, target_pembeli):
    """Draf penawaran (gaya WA) untuk proyek yang sudah punya listing."""
    nama = (nama or "").strip()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama)
    listing = proyek.get("listing") or {}
    if not listing:
        return ("Proyek '{}' belum punya listing toko — buat listing dulu "
                "di tab Listing.".format(nama))
    target = (target_pembeli or "").strip() or "toko / perusahaan"
    draf = """# Draf Penawaran (WA): {n}

**Status:** DRAF — periksa dulu, kirim hanya setelah Cipta menyetujui teks persisnya.

---
Halo! Kami dari Podcast Meong (SatuKiki) punya aplikasi **{n}** untuk {t}.

{deskripsi}

Fitur utama:
{fitur}

Harga: {harga}
Coba demonya di sini: {demo}

Bila tertarik, balas pesan ini — kami bantu penyesuaian nama toko/perusahaan dan data awal. Terima kasih!
---
Catatan jujur: demo v1 datanya hanya berlaku selama aplikasi dibuka; versi pembeli (penyimpanan permanen, multi-user) adalah pengembangan lanjutan.
""".format(
        n=nama, t=target,
        deskripsi=listing.get("deskripsi", ""),
        fitur="\n".join("- {}".format(f) for f in listing.get("fitur", [])),
        harga=listing.get("harga", "bisa negosiasi"),
        demo=listing.get("tautan_demo") or "(tautan demo menyusul)")
    return draf


def tandai_di_toko(nama):
    """Tandai proyek siap-jual sudah masuk Toko Aplikasi (status -> di-toko)."""
    nama = (nama or "").strip()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan.".format(nama), pipa.tabel_pipeline()
    if proyek.get("status") != "siap-jual":
        return ("Proyek '{}' belum bisa ditandai di-toko (status: {}). "
                "Hanya dari status siap-jual.".format(
                    nama, proyek.get("status"))), pipa.tabel_pipeline()
    proyek["status"] = "di-toko"
    pipa.simpan_data(data)
    return "✅ '{}' ditandai sudah di Toko Aplikasi (status: di-toko).".format(nama), pipa.tabel_pipeline()


# ---------------------------------------------------------------- Antarmuka
def bangun_ui():
    import gradio as gr

    with gr.Blocks(title="Tim 9C Jualan — Agent 9",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🛒 Tim 9C Jualan — Agent 9 Produksi Game & Aplikasi\n"
            "Menyiapkan listing toko (deskripsi, fitur, harga/nego), tombol "
            "demo, dan draf penawaran untuk tiap aplikasi/game yang selesai. "
            "Semua output adalah **DRAF untuk persetujuan Cipta** — "
            "tidak ada yang diterbitkan otomatis.\n\n"
            "Alur: antrean → spesifikasi-selesai (9A) → diuji-lolos (9B) → "
            "**siap-jual** (9C) → di-toko.")
        with gr.Tabs():
            with gr.Tab("📋 Antrean Produksi"):
                gr.Markdown("Status tiap proyek di alur produksi Agent 9.")
                out_tabel = gr.Markdown(value=pipa.tabel_pipeline(), label="Antrean produksi")
                btn_muat = gr.Button("🔄 Muat Ulang Tabel")
                btn_muat.click(lambda: pipa.tabel_pipeline(), None, out_tabel,
                               api_name="muat_tabel_9c")

            with gr.Tab("🏪 Buat Listing"):
                gr.Markdown(
                    "Buat listing toko untuk proyek berstatus diuji-lolos. "
                    "Harga aplikasi tetap **'bisa negosiasi'** sampai Cipta "
                    "mematok harga — jangan mengarang harga.")
                data_awal = pipa.muat_data()
                nama_l = gr.Dropdown(
                    choices=pipa.daftar_nama(data_awal, ["diuji-lolos"]),
                    label="Proyek (diuji-lolos)")
                desk_l = gr.Textbox(label="Deskripsi listing", lines=3,
                                    placeholder="contoh: Aplikasi absensi online untuk toko dan perusahaan kecil — absen masuk/pulang, terlambat otomatis, rekap CSV.")
                fitur_l = gr.Textbox(label="Fitur listing (satu fitur per baris)",
                                     lines=5,
                                     placeholder="contoh:\nAbsen masuk/pulang + deteksi terlambat otomatis\nIzin/Sakit + ringkasan harian\nRekap kehadiran + unduh CSV")
                harga_l = gr.Textbox(label="Harga", value="bisa negosiasi")
                demo_l = gr.Textbox(label="Tautan demo",
                                    placeholder="contoh: tautan artefak demo aplikasi")
                btn_listing = gr.Button("💾 Simpan Listing", variant="primary")
                pesan_l = gr.Textbox(label="Pesan", interactive=False)
                out_listing = gr.Markdown(label="Draf listing")
                btn_listing.click(buat_listing,
                                  [nama_l, desk_l, fitur_l, harga_l, demo_l],
                                  [pesan_l, out_listing, out_tabel],
                                  api_name="buat_listing_9c")

            with gr.Tab("✉️ Draf Penawaran"):
                gr.Markdown(
                    "Draf penawaran gaya WA dari listing yang sudah ada. "
                    "**Periksa dulu** — kirim hanya setelah Cipta menyetujui "
                    "teks persisnya.")
                data_awal2 = pipa.muat_data()
                nama_w = gr.Dropdown(
                    choices=pipa.daftar_nama(data_awal2, ["siap-jual", "di-toko"]),
                    label="Proyek (siap-jual / di-toko)")
                target_w = gr.Textbox(label="Target pembeli",
                                      placeholder="contoh: toko kelontong di Jakarta Selatan")
                btn_w = gr.Button("✉️ Buat Draf Penawaran", variant="primary")
                out_w = gr.Markdown(label="Draf penawaran")
                btn_w.click(draf_penawaran, [nama_w, target_w], out_w,
                            api_name="draf_penawaran_9c")

            with gr.Tab("✅ Tandai di Toko"):
                gr.Markdown(
                    "Tandai proyek siap-jual yang sudah masuk Toko Aplikasi "
                    "(status menjadi di-toko).")
                nama_t = gr.Dropdown(
                    choices=pipa.daftar_nama(pipa.muat_data(), ["siap-jual"]),
                    label="Proyek (siap-jual)")
                btn_t = gr.Button("✅ Tandai Sudah di Toko", variant="primary")
                pesan_t = gr.Textbox(label="Pesan", interactive=False)
                btn_t.click(tandai_di_toko, nama_t, [pesan_t, out_tabel],
                            api_name="tandai_di_toko_9c")
    return demo


if __name__ == "__main__":
    demo = bangun_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
