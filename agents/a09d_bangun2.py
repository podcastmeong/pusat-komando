# ======================================================================
# PUSAT KOMANDO — Tim 9D Bangun-2 (di bawah Agent 9 Produksi Game &
# Aplikasi). Builder paralel kedua: antarmuka bangun + verifikasi sama
# seperti Tim 9B (5 butir cek, butir 5 = buku panduan), mengerjakan
# aplikasi/game yang BERBEDA secara bersamaan dengan 9B/9E.
# Ditambahkan 19 Nov 2026 atas perintah Cipta ("tambah 3 tim Agent 9
# agar lebih cepat").
# Mekanisme klaim/kunci di data/produksi_game.json (field "klaim"):
# satu proyek spesifikasi-selesai hanya boleh dikerjakan SATU tim bangun
# dalam satu waktu — tim lain yang mencoba mengklaim/menguji proyek yang
# sama akan ditolak. Uji otomatis mengklaim bila proyek masih bebas.
# Aplikasi Gradio pasif; semua output adalah DRAF untuk persetujuan
# Cipta — tidak ada yang diterbitkan otomatis (SOP v1.3).
# ======================================================================
"""Tim 9D Bangun-2 — builder paralel kedua Agent 9."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a09_pipa as pipa

# Daftar verifikasi 5 butir — definisi bersama di a09_pipa (dipakai juga
# 9B/9E/9F). Butir 5 = buku panduan penggunaan (standar produk Cipta).
CHECKLIST = pipa.CHECKLIST_UJI

TIM = "9D"


def klaim_proyek(nama):
    """Klaim proyek spesifikasi-selesai untuk tim 9D (anti double-build)."""
    return pipa.klaim(nama, TIM)


def lepas_klaim(nama):
    """Lepas klaim proyek milik tim 9D."""
    return pipa.lepas(nama, TIM)


def uji_proyek(nama, fitur_jalan, tanpa_error, data_contoh_benar, responsif_hp,
               panduan_lengkap, catatan):
    """Verifikasi proyek berstatus spesifikasi-selesai dengan 5 butir cek.

    Semua butir lolos -> status diuji-lolos (lanjut ke verifikasi 9F).
    Ada yang gagal -> status tetap, catatan perbaikan dicatat untuk 9A.
    Bila proyek diklaim tim bangun lain, uji ditolak (anti double-build).
    """
    nama = (nama or "").strip()
    data = pipa.muat_data()
    checklist = {"fitur_jalan": bool(fitur_jalan),
                 "tanpa_error": bool(tanpa_error),
                 "data_contoh_benar": bool(data_contoh_benar),
                 "responsif_hp": bool(responsif_hp),
                 "panduan_lengkap": bool(panduan_lengkap)}
    pesan, proyek = pipa.uji_bersama(data, nama, checklist, catatan, TIM)
    if proyek is None:
        return pesan, "", pipa.tabel_pipeline()
    pipa.simpan_data(data)
    return pesan, teks_hasil_uji(proyek), pipa.tabel_pipeline()


def teks_hasil_uji(proyek):
    """Hasil uji proyek sebagai Markdown (DRAF) — sama seperti 9B."""
    from a09b_bangun import teks_hasil_uji as _teks_9b
    return _teks_9b(proyek)


# ---------------------------------------------------------------- Antarmuka
def bangun_ui():
    import gradio as gr

    with gr.Blocks(title="Tim 9D Bangun-2 — Agent 9",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 🔨 Tim 9D Bangun-2 — Agent 9 Produksi Game & Aplikasi\n"
            "Builder paralel kedua — antarmuka bangun + verifikasi sama "
            "seperti Tim 9B, mengerjakan aplikasi/game yang **berbeda** "
            "secara bersamaan dengan 9B/9E. "
            "Semua output adalah **DRAF untuk persetujuan Cipta** — "
            "tidak ada yang diterbitkan otomatis.\n\n"
            "Alur: antrean → spesifikasi-selesai (9A) → **diuji-lolos** (9D) → "
            "verifikasi 9F → siap-jual (9C) → di-toko. Klaim dulu proyek yang "
            "mau dibangun — satu proyek hanya boleh dikerjakan satu tim "
            "bangun (9B/9D/9E) dalam satu waktu.")
        with gr.Tabs():
            with gr.Tab("📋 Antrean Produksi"):
                gr.Markdown("Status tiap proyek di alur produksi Agent 9.")
                out_tabel = gr.Markdown(value=pipa.tabel_pipeline(), label="Antrean produksi")
                btn_muat = gr.Button("🔄 Muat Ulang Tabel")
                btn_muat.click(lambda: pipa.tabel_pipeline(), None, out_tabel,
                               api_name="muat_tabel_9d")

            with gr.Tab("🔒 Klaim Proyek"):
                gr.Markdown(
                    "Klaim proyek spesifikasi-selesai sebelum membangun — "
                    "satu proyek hanya boleh dikerjakan **satu tim bangun** "
                    "(9B/9D/9E) dalam satu waktu. Tim lain yang mencoba "
                    "mengklaim/menguji proyek yang sama akan ditolak. "
                    "Uji proyek otomatis mengklaim bila proyek masih bebas, "
                    "dan melepas klaim setelah uji selesai.")
                data_klaim = pipa.muat_data()
                nama_k = gr.Dropdown(
                    choices=pipa.daftar_nama(data_klaim, ["spesifikasi-selesai"]),
                    label="Proyek (spesifikasi-selesai)")
                with gr.Row():
                    btn_klaim = gr.Button("🔒 Klaim untuk Tim 9D", variant="primary")
                    btn_lepas = gr.Button("🔓 Lepas Klaim")
                pesan_k = gr.Textbox(label="Pesan", interactive=False)
                btn_klaim.click(klaim_proyek, nama_k, [pesan_k, out_tabel],
                                api_name="klaim_proyek_9d")
                btn_lepas.click(lepas_klaim, nama_k, [pesan_k, out_tabel],
                                api_name="lepas_klaim_9d")

            with gr.Tab("✅ Uji Proyek"):
                gr.Markdown(
                    "Uji proyek berstatus spesifikasi-selesai. **Semua 5 butir harus "
                    "lolos** agar proyek lanjut ke verifikasi 9F. Bila ada yang gagal, "
                    "status tetap dan catatan perbaikan diteruskan ke 9A.")
                data_awal = pipa.muat_data()
                nama_u = gr.Dropdown(
                    choices=pipa.daftar_nama(data_awal, ["spesifikasi-selesai"]),
                    label="Proyek (spesifikasi-selesai)")
                with gr.Row():
                    cb_fitur = gr.Checkbox(label=CHECKLIST[0][1], value=False)
                    cb_error = gr.Checkbox(label=CHECKLIST[1][1], value=False)
                with gr.Row():
                    cb_data = gr.Checkbox(label=CHECKLIST[2][1], value=False)
                    cb_hp = gr.Checkbox(label=CHECKLIST[3][1], value=False)
                cb_panduan = gr.Checkbox(label=CHECKLIST[4][1], value=False)
                catatan_u = gr.Textbox(
                    label="Catatan perbaikan (wajib diisi bila ada yang gagal)",
                    lines=3,
                    placeholder="contoh: tombol Bayar tidak merespons di HP; total laporan selisih Rp1.000")
                btn_uji = gr.Button("✅ Simpan Hasil Uji", variant="primary")
                pesan_u = gr.Textbox(label="Pesan", interactive=False)
                out_uji = gr.Markdown(label="Hasil uji")
                btn_uji.click(uji_proyek,
                              [nama_u, cb_fitur, cb_error, cb_data, cb_hp, cb_panduan, catatan_u],
                              [pesan_u, out_uji, out_tabel],
                              api_name="uji_proyek_9d")
    return demo


if __name__ == "__main__":
    demo = bangun_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
