# ======================================================================
# PUSAT KOMANDO — Tim 9A Rancang (di bawah Agent 9 Produksi Game &
# Aplikasi). Membuat spesifikasi tiap aplikasi/game dari antrean
# produksi: daftar fitur, data contoh, dan kriteria demo lolos.
# Ditambahkan 19 Nov 2026 atas perintah Cipta ("tambah 3 tim Agent 9",
# "langsung hubungkan dengan wadah").
# Aplikasi Gradio pasif; semua output adalah DRAF untuk persetujuan
# Cipta — tidak ada yang diterbitkan otomatis (SOP v1.3).
# ======================================================================
"""Tim 9A Rancang — spesifikasi aplikasi/game Agent 9."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a09_pipa as pipa

STATUS_TULIS = ["antrean", "spesifikasi-selesai"]


def _pecah_baris(teks):
    return [b.strip() for b in (teks or "").splitlines() if b.strip()]


def tambah_proyek(nama, jenis, catatan):
    """Tambah proyek baru ke antrean produksi (status: antrean)."""
    nama = (nama or "").strip()
    if not nama:
        return "Nama proyek wajib diisi.", pipa.tabel_pipeline()
    if jenis not in pipa.JENIS_PROYEK:
        return "Jenis harus 'aplikasi' atau 'game'.", pipa.tabel_pipeline()
    data = pipa.muat_data()
    if pipa.cari(data, nama) is not None:
        return "Proyek '{}' sudah ada di antrean.".format(nama), pipa.tabel_pipeline()
    data.append({"nama": nama, "jenis": jenis, "status": "antrean",
                 "spesifikasi": None, "hasil_uji": None, "listing": None,
                 "catatan": (catatan or "").strip()})
    pipa.simpan_data(data)
    return "Proyek '{}' ditambahkan ke antrean (status: antrean).".format(nama), pipa.tabel_pipeline()


def buat_spesifikasi(nama, target_pengguna, fitur_utama, data_contoh, kriteria_lolos, panduan):
    """Tulis (atau tulis ulang) spesifikasi proyek; status -> spesifikasi-selesai.

    Standar produk (Cipta, 19 Nov 2026): setiap aplikasi harus berisi buku
    panduan penggunaan di dalamnya — spesifikasi wajib mencakup isinya
    (cara memakai tiap fitur, Bahasa Indonesia).
    """
    nama = (nama or "").strip()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan di antrean.".format(nama), "", pipa.tabel_pipeline()
    if proyek.get("status") not in STATUS_TULIS:
        return ("Proyek '{}' sudah lewat tahap rancang (status: {}). "
                "Spesifikasi hanya ditulis dari status antrean.".format(
                    nama, proyek.get("status"))), "", pipa.tabel_pipeline()
    fitur = _pecah_baris(fitur_utama)
    kriteria = _pecah_baris(kriteria_lolos)
    if not fitur:
        return "Daftar fitur wajib diisi (satu fitur per baris).", "", pipa.tabel_pipeline()
    if not kriteria:
        return "Kriteria demo lolos wajib diisi (satu kriteria per baris).", "", pipa.tabel_pipeline()
    panduan = (panduan or "").strip()
    if not panduan:
        return ("Isi buku panduan penggunaan wajib diisi (cara memakai tiap "
                "fitur, Bahasa Indonesia)."), "", pipa.tabel_pipeline()
    proyek["spesifikasi"] = {
        "tanggal": pipa._hari_ini(),
        "target_pengguna": (target_pengguna or "").strip() or "UMKM / toko / perusahaan kecil",
        "fitur": fitur,
        "data_contoh": (data_contoh or "").strip(),
        "kriteria_lolos": kriteria,
        "panduan": panduan,
    }
    proyek["status"] = "spesifikasi-selesai"
    pipa.simpan_data(data)
    return ("Spesifikasi '{}' selesai (status: spesifikasi-selesai). "
            "Tim 9B bisa lanjut menguji.".format(nama)), teks_spesifikasi(proyek), pipa.tabel_pipeline()


def teks_spesifikasi(proyek):
    """Spesifikasi proyek sebagai Markdown (DRAF)."""
    spec = proyek.get("spesifikasi") or {}
    if not spec:
        return "Proyek '{}' belum punya spesifikasi.".format(proyek.get("nama", "?"))
    baris = ["# Spesifikasi: {n}\n".format(n=proyek.get("nama", "?")),
             "**Jenis:** {j} · **Status:** {s} · **Tanggal:** {t}".format(
                 j=proyek.get("jenis", "?"), s=proyek.get("status", "?"),
                 t=spec.get("tanggal", "?")),
             "**Target pengguna:** {}".format(spec.get("target_pengguna", "?")),
             "\n**Status:** DRAF — menunggu persetujuan Cipta.",
             "\n## Fitur"]
    for f in spec.get("fitur", []):
        baris.append("- {}".format(f))
    baris.append("\n## Data Contoh")
    baris.append(spec.get("data_contoh") or "(belum diisi)")
    baris.append("\n## Kriteria Demo Lolos")
    for k in spec.get("kriteria_lolos", []):
        baris.append("- [ ] {}".format(k))
    baris.append("\n## Buku Panduan Penggunaan")
    baris.append(spec.get("panduan") or "(belum diisi)")
    baris.append("\n**Batas jujur (demo v1):** data hanya berlaku selama aplikasi "
                 "dibuka; penyimpanan permanen, multi-user, dan fitur berbayar "
                 "adalah pengembangan lanjutan versi pembeli.")
    return "\n".join(baris)


def ubah_status(nama, status_baru):
    """Kembalikan proyek ke antrean / spesifikasi-selesai (untuk revisi)."""
    nama = (nama or "").strip()
    if status_baru not in STATUS_TULIS:
        return "Status baru harus 'antrean' atau 'spesifikasi-selesai'.", pipa.tabel_pipeline()
    data = pipa.muat_data()
    proyek = pipa.cari(data, nama)
    if proyek is None:
        return "Proyek '{}' tidak ditemukan.".format(nama), pipa.tabel_pipeline()
    if proyek.get("status") not in STATUS_TULIS:
        return ("Proyek '{}' sudah lewat tahap rancang (status: {}). "
                "Minta tim 9B/9C mengembalikan dulu bila perlu revisi.".format(
                    nama, proyek.get("status"))), pipa.tabel_pipeline()
    proyek["status"] = status_baru
    pipa.simpan_data(data)
    return "Status '{}' diubah menjadi {}.".format(nama, status_baru), pipa.tabel_pipeline()


# ---------------------------------------------------------------- Antarmuka
def bangun_ui():
    import gradio as gr

    with gr.Blocks(title="Tim 9A Rancang — Agent 9",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 📝 Tim 9A Rancang — Agent 9 Produksi Game & Aplikasi\n"
            "Membuat spesifikasi tiap aplikasi/game dari antrean produksi: "
            "daftar fitur, data contoh, dan kriteria demo lolos. "
            "Semua output adalah **DRAF untuk persetujuan Cipta** — "
            "tidak ada yang diterbitkan otomatis.\n\n"
            "Alur: antrean → **spesifikasi-selesai** (9A) → diuji-lolos (9B) → "
            "siap-jual (9C) → di-toko.")
        with gr.Tabs():
            with gr.Tab("📋 Antrean Produksi"):
                gr.Markdown("Status tiap proyek di alur produksi Agent 9.")
                out_tabel = gr.Markdown(value=pipa.tabel_pipeline(), label="Antrean produksi")
                btn_muat = gr.Button("🔄 Muat Ulang Tabel")
                btn_muat.click(lambda: pipa.tabel_pipeline(), None, out_tabel,
                               api_name="muat_tabel_9a")

            with gr.Tab("📝 Tulis Spesifikasi"):
                gr.Markdown(
                    "Tulis spesifikasi untuk proyek berstatus antrean "
                    "(atau tulis ulang bila masih spesifikasi-selesai). "
                    "Spesifikasi wajib mencakup isi buku panduan penggunaan "
                    "(standar produk: setiap aplikasi berisi buku panduan — "
                    "cara memakai tiap fitur, Bahasa Indonesia). "
                    "Setelah disimpan, proyek pindah ke tim 9B lewat aturan rute R11.")
                data_awal = pipa.muat_data()
                nama_s = gr.Dropdown(
                    choices=pipa.daftar_nama(data_awal, STATUS_TULIS),
                    label="Proyek")
                target_s = gr.Textbox(label="Target pengguna",
                                      value="UMKM / toko / perusahaan kecil")
                fitur_s = gr.Textbox(label="Daftar fitur (satu fitur per baris)",
                                     lines=6,
                                     placeholder="contoh:\nCari + filter produk\nKeranjang + diskon\nLaporan omzet + unduh CSV")
                data_s = gr.Textbox(label="Data contoh",
                                    lines=3,
                                    placeholder="contoh: 16 produk contoh (sembako, minuman, snack, elektronik); toko contoh 'Toko Berkah Jaya'")
                kriteria_s = gr.Textbox(label="Kriteria demo lolos (satu kriteria per baris)",
                                        lines=4,
                                        placeholder="contoh:\nSemua tombol berfungsi tanpa error\nTampilan rapi di HP dan laptop\nData contoh benar dan masuk akal")
                panduan_s = gr.Textbox(
                    label="Isi buku panduan penggunaan (wajib — cara memakai tiap fitur)",
                    lines=4,
                    placeholder="contoh:\n1. Buka tab Data Barang untuk menambah produk (nama, harga, stok).\n2. Pilih produk di tab Kasir, atur jumlah, lalu tekan Bayar.\n3. Lihat ringkasan penjualan di tab Laporan; unduh CSV bila perlu.")
                btn_simpan = gr.Button("💾 Simpan Spesifikasi", variant="primary")
                pesan_s = gr.Textbox(label="Pesan", interactive=False)
                out_spes = gr.Markdown(label="Draf spesifikasi")
                btn_simpan.click(buat_spesifikasi,
                                 [nama_s, target_s, fitur_s, data_s, kriteria_s, panduan_s],
                                 [pesan_s, out_spes, out_tabel],
                                 api_name="buat_spesifikasi_9a")

            with gr.Tab("➕ Tambah Proyek"):
                gr.Markdown("Tambah proyek baru ke antrean produksi Agent 9.")
                nama_p = gr.Textbox(label="Nama proyek",
                                    placeholder="contoh: Arsip Dokumen")
                jenis_p = gr.Dropdown(choices=pipa.JENIS_PROYEK, value="aplikasi",
                                      label="Jenis")
                catatan_p = gr.Textbox(label="Catatan",
                                       placeholder="contoh: DMS sederhana untuk perusahaan kecil")
                btn_tambah = gr.Button("➕ Tambah Proyek", variant="primary")
                pesan_p = gr.Textbox(label="Pesan", interactive=False)
                btn_tambah.click(tambah_proyek, [nama_p, jenis_p, catatan_p],
                                 [pesan_p, out_tabel], api_name="tambah_proyek_9a")
                gr.Markdown("### ↩️ Kembalikan Status (revisi)")
                status_baru = gr.Dropdown(choices=STATUS_TULIS, value="antrean",
                                          label="Status baru")
                btn_ubah = gr.Button("✏️ Ubah Status")
                btn_ubah.click(ubah_status, [nama_p, status_baru],
                               [pesan_p, out_tabel], api_name="ubah_status_9a")
    return demo


if __name__ == "__main__":
    demo = bangun_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
