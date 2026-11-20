# ======================================================================
# PUSAT KOMANDO — salinan dari agent-email (Agent 13 Email).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Perubahan dari aslinya:
# - data (contoh-email.json, aturan-triase-email.json,
#   log-aktivitas-email.json, draf-balasan-email.json) dialihkan ke
#   data/ bersama pusat-komando/ (ditandai komentar 'PUSAT KOMANDO')
# - ATURAN KERAS tetap berlaku: TIDAK ADA tombol kirim — hanya "Simpan
#   Draf"; kode verifikasi TIDAK PERNAH disimpan di file/log/memori.
# - Agent 13 berada DI BAWAH KENDALI MUSE; keputusan penting tetap di
#   tangan Cipta.
# ======================================================================
# -*- coding: utf-8 -*-
"""
Agent 13 — Email (Penjaga Email) — Podcast Meong
=================================================
Aplikasi Gradio mandiri. Memegang kendali email Cipta — dengan ATURAN KERAS:

- Agent TIDAK PERNAH mengirim, menghapus, atau mengarsip email sendiri.
- Semua yang dibuatnya adalah DRAF yang butuh persetujuan Cipta sebelum
  dikirim. TIDAK ADA tombol kirim di aplikasi ini — hanya "Simpan Draf".
- Penghapusan / pengiriman / penandaan email ASLI hanya oleh Cipta sendiri.
- Tidak mengarang isi email; bila data tidak ada tulis "BELUM CUKUP DATA".

Akun email Cipta (jangan mengarang akun lain):
- masduki1189@gmail.com (utama, default)
- lawaklucu182@gmail.com
- kikimtflb@gmail.com
- ciptabintanglestari@gmail.com

MODE DEMO: koneksi Gmail BELUM ada, jadi kotak masuk diisi contoh email
REALISTIS dari konteks Podcast Meong (data/contoh-email.json), ditandai
jelas sebagai CONTOH. Lapisan integrasi Gmail API (OAuth) disiapkan di
kode tapi JANGAN diaktifkan — butuh Cipta menghubungkan Gmail sekali.

Fitur (4 tab):
1) Kotak Masuk — triase (kategori + prioritas), ringkasan belum dibaca,
   tandai butuh balasan (hanya di data CONTOH ini).
2) Draf Balasan — draf balasan dari email terpilih, 5 template
   (affiliate, lomba, bisnis, umum, tolak sopan). Setiap draf berlabel
   "BUTUH PERSETUJUAN Cipta sebelum dikirim". Hanya tombol "Simpan Draf".
3) Cari Email — kata kunci + filter akun / kategori / tanggal.
4) Aturan & Log — aturan triase yang bisa diedit + log aktivitas (JSON)
   + status koneksi Gmail.

TUGAS TAMBAHAN — Bantu Verifikasi Login (perintah Cipta, 19 Nov 2026):
bila browser / Muse sedang sign-in dan menunggu kode verifikasi dari
email, Agent 13 membantu menemukan email kode terbaru yang cocok dan
menampilkannya supaya login bisa lanjut. ATURAN KERAS:
- Kode verifikasi TIDAK PERNAH disimpan di file / log / memori agent.
- Kode TIDAK PERNAH dikirim ke siapa pun — hanya dipakai untuk login
  yang sedang berjalan itu.
- Kode hanya dicari saat ada permintaan login yang jelas (nama layanan
  wajib diisi).

TUGAS HARIAN — DIPERBARUI 20 Nov 2026 (perintah Cipta, poin 27 — "biar
tidak lupa dan dilaksanakan sepenuh hati"):
- STANDBY SETIAP SAAT + FAST RESPON: begitu ada email penting masuk
  (lomba, keuangan, affiliate/bisnis, platform), triase SEGERA dan
  laporkan ke Muse/Cipta — JANGAN tunggu sampai laporan malam.
- CEK EMAIL SETIAP HARI: pagi (dalam rencana 05:00) + malam (dalam
  laporan 20:00) + setiap kali Muse meminta. Laporkan: berapa email
  baru, mana yang penting, mana yang butuh balasan, mana yang spam.
- DRAF BALASAN: buatkan draf balasan dari 5 template (affiliate, lomba,
  bisnis, umum, tolak sopan). SEMUA draf BUTUH PERSETUJUAN Cipta
  sebelum dikirim. TIDAK PERNAH kirim, hapus, atau arsip email sendiri.
- BANTU KODE VERIFIKASI: bila login menunggu kode dari email, bantu
  temukan kode terbaru yang cocok. Kode TIDAK PERNAH disimpan di file /
  log / memori agent, dan TIDAK PERNAH dikirim ke siapa pun.
- LAPORAN: catat semua aktivitas di log (data/log-aktivitas-email.json)
  dan laporkan ke Muse untuk laporan malam 20:00.
- MODE DEMO (sampai Cipta menghubungkan Gmail sekali): kotak masuk yang
  dipantau masih CONTOH (data/contoh-email.json), bukan email asli.
  Bila Gmail sudah terhubung, pantau kotak masuk ASLI keempat akun.
  Akun: masduki1189, lawaklucu182, kikimtflb, ciptabintanglestari
  (semua @gmail.com).

STRUKTUR KOMANDO (SOP Kerja Sama Agent AI, berlaku 18 Nov 2026):
Agent 13 berada DI BAWAH KENDALI MUSE — Muse yang mengarahkan dan
mengoordinasikan; Agent 13 bekerja untuk kepentingan Muse dan Cipta.
Keputusan penting (kirim email, hapus, ubah setelan) tetap di tangan
Cipta. Rantai komando: Cipta → Muse → Agent 13.

CATATAN PEMISAHAN: aplikasi Meong Tales (lomba #BuildHybridAI 2026)
adalah proyek TERPISAH — BUKAN bagian Agent 13. Jangan campur keduanya.

Semua output adalah DRAF untuk persetujuan Cipta. Tidak ada layanan
berbayar. Telemetri Gradio dimatikan. API key HANYA dari env var
GEMINI_API_KEY. Kredensial Gmail HANYA dari env var GMAIL_CREDENTIALS_JSON
(bila suatu hari dihubungkan) — tidak pernah ditulis di file.
"""
import json
import os
import re
import sys

# Quirk mesin Muse (18 Nov 2026): NO_PROXY bawaan berisi entri IPv6 dalam
# kurung ([::1], [fd8b:...]) yang membuat httpx (dipakai Gradio) gagal impor
# dengan "Invalid port". Bersihkan entri berkutung sebelum impor gradio.
# Ini hanya memengaruhi proses aplikasi ini, bukan sistem.
for _var in ("NO_PROXY", "no_proxy"):
    _val = os.environ.get(_var, "")
    if "[" in _val:
        _bersih = ",".join(p for p in _val.split(",") if "[" not in p.strip())
        os.environ[_var] = _bersih or "localhost,127.0.0.1"

import gradio as gr  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
# PUSAT KOMANDO: data di data/ bersama pusat-komando/ (bukan data/ agent)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
EMAIL_PATH = os.path.join(DATA_DIR, "contoh-email.json")  # PUSAT KOMANDO: data/ bersama
ATURAN_PATH = os.path.join(DATA_DIR, "aturan-triase-email.json")  # PUSAT KOMANDO: data/ bersama
LOG_PATH = os.path.join(DATA_DIR, "log-aktivitas-email.json")  # PUSAT KOMANDO: data/ bersama
DRAF_PATH = os.path.join(DATA_DIR, "draf-balasan-email.json")  # PUSAT KOMANDO: data/ bersama
os.makedirs(DATA_DIR, exist_ok=True)

AKUN = [
    "masduki1189@gmail.com",
    "lawaklucu182@gmail.com",
    "kikimtflb@gmail.com",
    "ciptabintanglestari@gmail.com",
]
AKUN_UTAMA = AKUN[0]
KATEGORI = ["Penting", "Lomba", "Keuangan", "Affiliate/Bisnis", "Promo",
            "Spam", "BELUM CUKUP DATA"]
PRIORITAS = ["Tinggi", "Sedang", "Rendah", "—"]
LABEL_PERSETUJUAN = "BUTUH PERSETUJUAN Cipta sebelum dikirim"

DISCLAIMER = (
    "\n\n---\n🔒 **Aturan keras Agent 13:** agent TIDAK PERNAH mengirim, "
    "menghapus, atau mengarsip email. Semua output adalah DRAF — "
    f"{LABEL_PERSETUJUAN}."
)

MODE_DEMO = (
    "⚠️ **MODE DEMO — Gmail BELUM terhubung.** Semua email di bawah ini "
    "adalah **CONTOH** (data/contoh-email.json) yang meniru email nyata "
    "dari konteks Podcast Meong. Bukan salinan kotak masuk asli Cipta. "
    "Penandaan di sini hanya mengubah data CONTOH, bukan email asli."
)


# ---------------------------------------------------------------------------
# Lapisan integrasi Gmail API — DISIAPKAN, TIDAK DIAKTIFKAN
# ---------------------------------------------------------------------------
def status_gmail():
    """Status koneksi Gmail. TIDAK PERNAH mencoba login sendiri.

    Aktivasi butuh: Cipta menghubungkan Gmail via OAuth SEKALI (di mesin
    Muse / browser), lalu kredensial disimpan sebagai env var
    GMAIL_CREDENTIALS_JSON. Tanpa itu fungsi ini selalu mengembalikan
    BELUM TERHUBUNG dan aplikasi tetap jalan dalam mode demo.
    """
    if os.environ.get("GMAIL_CREDENTIALS_JSON", "").strip():
        return (
            "🟡 **Kredensial Gmail tersedia di env var — TAPI BELUM DIAKTIFKAN.**\n\n"
            "Kode baca Gmail belum dihubungkan ke UI. Minta Muse mengaktifkan "
            "lapisan ini SETELAH Cipta menyelesaikan OAuth dan menyetujui "
            "ruang lingkup akses (hanya baca + buat draf, tanpa kirim/hapus)."
        )
    return (
        "🔴 **Gmail BELUM TERHUBUNG.**\n\n"
        "Yang dibutuhkan (sekali saja, oleh Cipta): hubungkan Gmail via OAuth "
        "di mesin Muse — kredensial HANYA lewat env var "
        "`GMAIL_CREDENTIALS_JSON`, tidak pernah ditulis di file, tidak pernah "
        "meminta kata sandi lewat chat. Sampai saat itu aplikasi jalan dalam "
        "mode demo dengan data CONTOH."
    )


def baca_gmail_api():
    """Stub baca Gmail API — SELALU menolak sebelum OAuth diaktifkan.

    Mengembalikan (None, pesan). Fungsi ini sengaja tidak memanggil API
    apa pun: tidak ada token, tidak ada koneksi, tidak ada pengiriman.
    """
    return None, (
        "BELUM TERHUBUNG — Gmail belum dihubungkan via OAuth. "
        "Gunakan data CONTOH (mode demo) sampai Cipta menghubungkannya."
    )


# ---------------------------------------------------------------------------
# Utilitas JSON
# ---------------------------------------------------------------------------
def _muat_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, type(default)) else default
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _simpan_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _muat_email():
    data = _muat_json(EMAIL_PATH, {})
    email = data.get("email", []) if isinstance(data, dict) else []
    return [e for e in email if isinstance(e, dict)]


def _simpan_email(daftar):
    data = _muat_json(EMAIL_PATH, {})
    if not isinstance(data, dict):
        data = {}
    data["email"] = daftar
    _simpan_json(EMAIL_PATH, data)


def _muat_aturan():
    data = _muat_json(ATURAN_PATH, {})
    aturan = data.get("aturan", []) if isinstance(data, dict) else []
    return [a for a in aturan if isinstance(a, dict)]


def _simpan_aturan(daftar):
    data = _muat_json(ATURAN_PATH, {})
    if not isinstance(data, dict):
        data = {}
    data["aturan"] = daftar
    _simpan_json(ATURAN_PATH, data)


def _muat_log():
    return _muat_json(LOG_PATH, [])


def _muat_draf():
    return _muat_json(DRAF_PATH, [])


def _catat_log(aksi, detail, hasil=""):
    from datetime import datetime

    log = _muat_log()
    log.append({
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aksi": aksi,
        "detail": (detail or "")[:200],
        "hasil": (hasil or "")[:200],
    })
    _simpan_json(LOG_PATH, log)
    return log


def _log_ke_tabel(log=None):
    log = log if log is not None else _muat_log()
    if not log:
        return [["(belum ada entri)", "", "", ""]]
    return [[e.get("tanggal", ""), e.get("aksi", ""), e.get("detail", ""),
             e.get("hasil", "")] for e in reversed(log)]


def _draf_ke_tabel(draf=None):
    draf = draf if draf is not None else _muat_draf()
    if not draf:
        return [["(belum ada draf tersimpan)", "", "", "", ""]]
    return [[d.get("id", ""), d.get("email_id", ""), d.get("template", ""),
             d.get("subjek_balasan", ""), d.get("status", "")]
            for d in reversed(draf)]


# ---------------------------------------------------------------------------
# Fitur 1 — Triase kotak masuk
# ---------------------------------------------------------------------------
def triase_email(email, aturan=None):
    """Klasifikasikan satu email dengan aturan triase.

    Urutan: aturan 'pengirim' dulu (paling spesifik, cocok dengan alamat
    pengirim), lalu 'kata_kunci' (cocok dengan subjek + isi). Aturan
    pertama yang cocok menang. Bila tidak ada yang cocok:
    ('BELUM CUKUP DATA', '—', None).
    Mengembalikan (kategori, prioritas, id_aturan_atau_None).
    """
    aturan = aturan if aturan is not None else _muat_aturan()
    pengirim = (email.get("pengirim_email", "") or "").lower()
    teks = "{} {}".format(email.get("subjek", "") or "",
                         email.get("isi", "") or "").lower()
    for jenis in ("pengirim", "kata_kunci"):
        for a in aturan:
            if not a.get("aktif", True):
                continue
            if a.get("jenis") != jenis:
                continue
            pola = (a.get("pola", "") or "").lower().strip()
            if not pola:
                continue
            if jenis == "pengirim" and pola in pengirim:
                return a.get("kategori", "BELUM CUKUP DATA"), \
                    a.get("prioritas", "—"), a.get("id", "?")
            if jenis == "kata_kunci" and pola in teks:
                return a.get("kategori", "BELUM CUKUP DATA"), \
                    a.get("prioritas", "—"), a.get("id", "?")
    return "BELUM CUKUP DATA", "—", None


def _baris_email(daftar):
    return [[e.get("id", ""), (e.get("tanggal", "") or "")[:10],
             e.get("pengirim", ""), e.get("subjek", ""),
             e.get("kategori", "BELUM CUKUP DATA"),
             e.get("prioritas", "—"),
             "Belum" if not e.get("dibaca") else "Ya",
             "Ya" if e.get("butuh_balasan") else "—"]
            for e in sorted(daftar, key=lambda x: x.get("tanggal", ""),
                            reverse=True)]


def muat_kotak_masuk(akun):
    """Fitur 1. Mengembalikan (ringkasan_md, tabel, pilihan_email)."""
    semua = _muat_email()
    daftar = [e for e in semua if e.get("akun") == akun] if akun != "Semua" \
        else list(semua)
    belum = sum(1 for e in daftar if not e.get("dibaca"))
    butuh = [e for e in daftar if e.get("butuh_balasan")]
    hitung_kat = {}
    for e in daftar:
        k = e.get("kategori", "BELUM CUKUP DATA")
        hitung_kat[k] = hitung_kat.get(k, 0) + 1
    baris = ["## 📥 Kotak Masuk — {}".format(akun),
             MODE_DEMO, "",
             "**Total: {} email** · Belum dibaca: **{}** · Butuh balasan: **{}**".format(
                 len(daftar), belum, len(butuh)),
             "",
             "**Per kategori:** " + (", ".join(
                 "{}: {}".format(k, v) for k, v in sorted(hitung_kat.items()))
                 if hitung_kat else "—"),
             ""]
    if butuh:
        baris.append("**Butuh balasan:**")
        for e in butuh:
            baris.append("- **{}** — {} ({})".format(
                e.get("id", "?"), e.get("subjek", "?"),
                e.get("pengirim", "?")))
        baris.append("")
    baris.append("Kategori & prioritas di tabel berasal dari aturan triase "
                 "(tab Aturan & Log). Email tanpa aturan yang cocok "
                 "berkategori **BELUM CUKUP DATA** — bukan berarti tidak "
                 "penting, hanya belum ada aturannya.")
    _catat_log("muat_kotak_masuk", "akun={} (CONTOH)".format(akun),
               "{} email, {} belum dibaca".format(len(daftar), belum))
    pilihan = ["{} — {}".format(e.get("id", "?"), e.get("subjek", "?"))
               for e in sorted(daftar, key=lambda x: x.get("tanggal", ""),
                               reverse=True)]
    return "\n".join(baris), _baris_email(daftar), \
        gr.update(choices=pilihan, value=pilihan[0] if pilihan else None)


def _cari_email_by_id(email_id):
    for e in _muat_email():
        if e.get("id") == email_id:
            return e
    return None


def detail_email(pilihan):
    """Tampilkan isi lengkap satu email CONTOH."""
    if not pilihan:
        return "Pilih dulu satu email dari daftar."
    email_id = (pilihan or "").split(" — ")[0].strip()
    e = _cari_email_by_id(email_id)
    if e is None:
        return "⚠️ Email {} tidak ditemukan di data CONTOH.".format(email_id)
    aturan = _muat_aturan()
    kat, pri, id_aturan = triase_email(e, aturan)
    return "\n".join([
        "## ✉️ {} — {}".format(e.get("id", "?"), e.get("subjek", "?")),
        "",
        "| | |",
        "|---|---|",
        "| **Dari** | {} |".format(e.get("pengirim", "?")),
        "| **Untuk akun** | {} |".format(e.get("akun", "?")),
        "| **Tanggal** | {} |".format(e.get("tanggal", "?")),
        "| **Dibaca** | {} |".format("Ya" if e.get("dibaca") else "Belum"),
        "| **Butuh balasan** | {} |".format("Ya" if e.get("butuh_balasan") else "Tidak"),
        "| **Kategori (data)** | {} |".format(e.get("kategori", "?")),
        "| **Kategori (aturan saat ini)** | {} (aturan {}) |".format(
            kat, id_aturan or "tidak ada yang cocok"),
        "| **Prioritas** | {} |".format(e.get("prioritas", "?")),
        "",
        "**Isi email:**",
        "",
        "> " + (e.get("isi", "") or "(kosong)").replace("\n", "\n> "),
        "",
        "**Catatan konteks:** {}".format(e.get("catatan", "—")),
        "",
        "🏷️ **CONTOH** — isi di atas adalah data demo, bukan salinan kotak "
        "masuk asli.",
    ]) + DISCLAIMER


def tandai_butuh_balasan(pilihan):
    """Tandai email CONTOH sebagai butuh balasan (hanya data demo)."""
    if not pilihan:
        return "Pilih dulu satu email.", None, None
    email_id = (pilihan or "").split(" — ")[0].strip()
    daftar = _muat_email()
    for e in daftar:
        if e.get("id") == email_id:
            e["butuh_balasan"] = True
            _simpan_email(daftar)
            _catat_log("tandai_butuh_balasan",
                       "{} — {}".format(email_id, e.get("subjek", "")),
                       "ditandai butuh balasan (data CONTOH)")
            return ("✅ **{}** ditandai butuh balasan (data CONTOH saja — "
                    "email asli tidak diubah).".format(email_id)), \
                _baris_email(daftar), _log_ke_tabel()
    return "⚠️ Email {} tidak ditemukan.".format(email_id), None, None


def tandai_sudah_dibaca(pilihan):
    """Tandai email CONTOH sebagai sudah dibaca (hanya data demo)."""
    if not pilihan:
        return "Pilih dulu satu email.", None, None
    email_id = (pilihan or "").split(" — ")[0].strip()
    daftar = _muat_email()
    for e in daftar:
        if e.get("id") == email_id:
            e["dibaca"] = True
            _simpan_email(daftar)
            _catat_log("tandai_sudah_dibaca",
                       "{} — {}".format(email_id, e.get("subjek", "")),
                       "ditandai sudah dibaca (data CONTOH)")
            return ("✅ **{}** ditandai sudah dibaca (data CONTOH saja — "
                    "email asli tidak diubah).".format(email_id)), \
                _baris_email(daftar), _log_ke_tabel()
    return "⚠️ Email {} tidak ditemukan.".format(email_id), None, None


# ---------------------------------------------------------------------------
# Fitur 2 — Draf Balasan (TIDAK ADA tombol kirim — hanya "Simpan Draf")
# ---------------------------------------------------------------------------
TEMPLATE_DRAF = {
    "affiliate": {
        "nama": "Affiliate / Kerjasama",
        "template": (
            "Halo {nama},\n\n"
            "Terima kasih atas penawaran affiliate / kerjasamanya terkait "
            "\"{subjek}\".\n\n"
            "Boleh saya minta detailnya: produk yang ditawarkan, besaran "
            "komisi, dan syarat-syaratnya? Setelah saya cek, saya kabari "
            "lagi.\n\n"
            "Salam,\n"
            "Masduki Kiki — Podcast Meong"
        ),
    },
    "lomba": {
        "nama": "Lomba",
        "template": (
            "Halo,\n\n"
            "Terima kasih atas informasinya terkait \"{subjek}\".\n\n"
            "Saya sudah mencatat tenggat dan syaratnya. Bila ada dokumen "
            "atau langkah tambahan yang diperlukan, mohon informasinya.\n\n"
            "Salam,\n"
            "Masduki Kiki — Podcast Meong"
        ),
    },
    "bisnis": {
        "nama": "Bisnis / Jasa Video Promo",
        "template": (
            "Halo {nama},\n\n"
            "Terima kasih atas ketertarikan Anda pada jasa video promo "
            "KikiWorks (Podcast Meong).\n\n"
            "Paket kami: 15 detik Rp75.000, 30 detik Rp150.000, "
            "60 detik Rp250.000. Contoh video bisa dilihat di kanal "
            "YouTube Podcast Meong (@Podcastmeong).\n\n"
            "Boleh diceritakan kebutuhan videonya (produk, durasi, gaya "
            "yang diinginkan)? Setelah itu saya buatkan penawaran dan "
            "jadwal produksinya.\n\n"
            "Salam,\n"
            "Masduki Kiki — Podcast Meong"
        ),
    },
    "umum": {
        "nama": "Umum",
        "template": (
            "Halo {nama},\n\n"
            "Terima kasih atas email Anda terkait \"{subjek}\".\n\n"
            "Saya sudah membacanya dan akan menindaklanjuti. Bila ada hal "
            "mendesak, silakan sampaikan lagi di email balasan ini.\n\n"
            "Salam,\n"
            "Masduki Kiki — Podcast Meong"
        ),
    },
    "tolak_sopan": {
        "nama": "Tolak Sopan",
        "template": (
            "Halo {nama},\n\n"
            "Terima kasih atas tawaran dan kepercayaannya terkait "
            "\"{subjek}\".\n\n"
            "Dengan menyesal, saat ini saya belum bisa mengambil "
            "kesempatan ini karena jadwal dan prioritas yang sudah berjalan. "
            "Semoga sukses dengan programnya, dan silakan hubungi lagi di "
            "kesempatan lain.\n\n"
            "Salam,\n"
            "Masduki Kiki — Podcast Meong"
        ),
    },
}


def _nama_pengirim(email):
    pengirim = email.get("pengirim", "") or ""
    nama = pengirim.split("<")[0].strip()
    if not nama:
        nama = (email.get("pengirim_email", "") or "").split("@")[0]
    return nama or "Bapak/Ibu"


def _draf_template(email, template_key, catatan=""):
    tpl = TEMPLATE_DRAF.get(template_key) or TEMPLATE_DRAF["umum"]
    isi = tpl["template"].format(
        nama=_nama_pengirim(email), subjek=email.get("subjek", ""))
    if (catatan or "").strip():
        isi += "\n\nCatatan tambahan dari Cipta:\n" + catatan.strip()
    return {
        "template": template_key,
        "subjek_balasan": "Re: {}".format(email.get("subjek", "")),
        "isi": isi,
    }


def _draf_gemini(email, template_key, catatan=""):
    """Minta Gemini menulis draf balasan. Kembalikan dict draf atau None
    bila tidak ada key / gagal (pemanggil memakai template)."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        return None, "tanpa API key"
    try:
        import google.generativeai as genai

        genai.configure(api_key=kunci)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "Tulis draf balasan email berbahasa Indonesia, sopan, singkat, "
            "dari Masduki Kiki (Podcast Meong). Jenis balasan: "
            f"{TEMPLATE_DRAF.get(template_key, {}).get('nama', 'Umum')}.\n"
            f"Email yang dibalas — dari: {email.get('pengirim', '?')}; "
            f"subjek: {email.get('subjek', '?')}; isi: {email.get('isi', '')}\n"
            f"Catatan tambahan dari Cipta: {catatan or '(tidak ada)'}\n"
            "Aturan: jangan mengarang janji (harga, jadwal, hadiah) yang "
            "tidak ada di email atau catatan; bila detail belum jelas, minta "
            "detail itu di draf. Jangan menulis salam pembuka yang berlebihan. "
            "Kembalikan HANYA isi draf balasan, tanpa penjelasan."
        )
        r = model.generate_content(prompt)
        teks = (r.text or "").strip()
        if not teks:
            return None, "Gemini mengembalikan teks kosong"
        return {"template": template_key,
                "subjek_balasan": "Re: {}".format(email.get("subjek", "")),
                "isi": teks}, "Gemini (gemini-2.0-flash)"
    except Exception as e:  # noqa: BLE001
        return None, "Gemini gagal: {}".format(e)


def pratinjau_draf(pilihan_email, template_key, catatan=""):
    """Fitur 2 — langkah 1: buat pratinjau draf (BELUM disimpan).

    Mengembalikan (pratinjau_md, draf_state). Pratinjau hanya tampil di
    layar; penyimpanan terjadi HANYA lewat tombol 'Simpan Draf'."""
    if not pilihan_email:
        return "Pilih dulu satu email dari daftar.", None
    email_id = (pilihan_email or "").split(" — ")[0].strip()
    email = _cari_email_by_id(email_id)
    if email is None:
        return "⚠️ Email {} tidak ditemukan di data CONTOH.".format(email_id), None
    draf, mode = _draf_gemini(email, template_key, catatan)
    if draf is None:
        draf = _draf_template(email, template_key, catatan)
        mode = ("template (tanpa API key Gemini)" if mode == "tanpa API key"
                else "template (fallback: {})".format(mode))
    draf_state = {
        "email_id": email_id,
        "template": draf["template"],
        "subjek_balasan": draf["subjek_balasan"],
        "isi": draf["isi"],
        "mode": mode,
    }
    pratinjau = "\n".join([
        "## ✍️ Pratinjau Draf Balasan (BELUM DISIMPAN)",
        "",
        "⚠️ **{}** — draf ini BELUM terkirim dan BELUM tersimpan. "
        "Agent 13 TIDAK PERNAH mengirim email. Simpan dulu dengan tombol "
        "'💾 Simpan Draf', lalu Cipta yang memutuskan.".format(
            LABEL_PERSETUJUAN),
        "",
        "| | |",
        "|---|---|",
        "| **Membalas email** | {} — {} |".format(email_id,
                                                  email.get("subjek", "?")),
        "| **Template** | {} |".format(
            TEMPLATE_DRAF.get(template_key, {}).get("nama", template_key)),
        "| **Mode** | {} |".format(mode),
        "| **Subjek balasan** | {} |".format(draf["subjek_balasan"]),
        "",
        "**Isi draf:**",
        "",
        draf["isi"],
    ]) + DISCLAIMER
    return pratinjau, draf_state


def simpan_draf(draf_state):
    """Fitur 2 — langkah 2: simpan pratinjau ke data/draf-balasan.json.

    TIDAK ADA pengiriman di sini — hanya penyimpanan draf. Mengembalikan
    (pesan, tabel_draf)."""
    if not draf_state:
        return ("⚠️ Belum ada pratinjau draf. Klik dulu 'Lihat Pratinjau "
                "Draf'.", _draf_ke_tabel())
    from datetime import datetime

    draf = _muat_draf()
    baru_id = "D{:03d}".format(len(draf) + 1)
    entri = {
        "id": baru_id,
        "email_id": draf_state.get("email_id", "?"),
        "template": draf_state.get("template", "?"),
        "subjek_balasan": draf_state.get("subjek_balasan", ""),
        "isi": draf_state.get("isi", ""),
        "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "DRAF — {}".format(LABEL_PERSETUJUAN),
        "mode": draf_state.get("mode", ""),
    }
    draf.append(entri)
    _simpan_json(DRAF_PATH, draf)
    _catat_log("simpan_draf",
               "{} membalas {} (template {})".format(
                   baru_id, entri["email_id"], entri["template"]),
               "disimpan sebagai DRAF — belum dikirim")
    return ("✅ Draf **{}** disimpan (status: DRAF — {}). "
            "Draf TIDAK terkirim — Cipta yang memutuskan pengirimannya.".format(
                baru_id, LABEL_PERSETUJUAN)), _draf_ke_tabel()


# ---------------------------------------------------------------------------
# Fitur 3 — Cari Email
# ---------------------------------------------------------------------------
def cari_email(kata_kunci, akun, kategori, tgl_dari, tgl_sampai):
    """Cari di data CONTOH: kata kunci (subjek + isi + pengirim) dan filter
    akun / kategori / rentang tanggal. Mengembalikan (hasil_md, tabel)."""
    semua = _muat_email()
    kunci = (kata_kunci or "").strip().lower()
    hasil = []
    for e in semua:
        if akun != "Semua" and e.get("akun") != akun:
            continue
        if kategori != "Semua" and e.get("kategori") != kategori:
            continue
        tgl = (e.get("tanggal", "") or "")[:10]
        if tgl_dari and tgl < str(tgl_dari):
            continue
        if tgl_sampai and tgl > str(tgl_sampai):
            continue
        if kunci:
            gabung = "{} {} {}".format(e.get("subjek", ""),
                                       e.get("isi", ""),
                                       e.get("pengirim", "")).lower()
            if kunci not in gabung:
                continue
        hasil.append(e)
    _catat_log("cari_email",
               "kunci='{}' akun={} kategori={}".format(kunci, akun, kategori),
               "{} hasil".format(len(hasil)))
    if not hasil:
        return ("## 🔍 Hasil Pencarian: 0 email\n\n"
                "Tidak ada email CONTOH yang cocok. Bila yang dicari adalah "
                "email asli, ingat: Gmail BELUM terhubung — data di sini "
                "hanya CONTOH. Tulis **BELUM CUKUP DATA** bila ragu."), []
    baris = ["## 🔍 Hasil Pencarian: {} email".format(len(hasil)), "",
             "Filter: kata kunci '{}' · akun {} · kategori {} · "
             "tanggal {} s.d. {}".format(kunci or "—", akun, kategori,
                                         tgl_dari or "—", tgl_sampai or "—"),
             ""]
    for e in sorted(hasil, key=lambda x: x.get("tanggal", ""), reverse=True):
        baris.append("- **{}** — {} · {} · {} · {}".format(
            e.get("id", "?"), e.get("subjek", "?"), e.get("pengirim", "?"),
            e.get("kategori", "?"), (e.get("tanggal", "") or "")[:10]))
    return "\n".join(baris), _baris_email(hasil)


# ---------------------------------------------------------------------------
# Fitur 4 — Aturan triase & log
# ---------------------------------------------------------------------------
def _aturan_ke_tabel(aturan=None):
    aturan = aturan if aturan is not None else _muat_aturan()
    if not aturan:
        return [["(belum ada aturan)", "", "", "", "", ""]]
    return [[a.get("id", ""), a.get("jenis", ""), a.get("pola", ""),
             a.get("kategori", ""), a.get("prioritas", ""),
             "Aktif" if a.get("aktif", True) else "Nonaktif"]
            for a in aturan]


def tambah_aturan(jenis, pola, kategori, prioritas, catatan=""):
    """Tambah satu aturan triase baru."""
    pola = (pola or "").strip()
    if not pola:
        return "⚠️ Pola wajib diisi (alamat email / kata kunci).", \
            _aturan_ke_tabel()
    aturan = _muat_aturan()
    if any(a.get("pola", "").lower() == pola.lower()
           and a.get("jenis") == jenis for a in aturan):
        return ("⚠️ Aturan dengan pola '{}' ({}) sudah ada — tidak "
                "ditambahkan dua kali.".format(pola, jenis)), \
            _aturan_ke_tabel()
    nomor = [int(a["id"][1:]) for a in aturan
             if str(a.get("id", "")).startswith("R")
             and str(a["id"][1:]).isdigit()]
    baru_id = "R{:02d}".format((max(nomor) if nomor else 0) + 1)
    aturan.append({"id": baru_id, "jenis": jenis, "pola": pola,
                   "kategori": kategori, "prioritas": prioritas,
                   "aktif": True, "catatan": (catatan or "").strip()})
    _simpan_aturan(aturan)
    _catat_log("tambah_aturan",
               "{}: {} '{}' -> {} / {}".format(baru_id, jenis, pola,
                                               kategori, prioritas),
               "aturan ditambahkan")
    return "✅ Aturan **{}** ditambahkan: {} '{}' → {} / {}.".format(
        baru_id, jenis, pola, kategori, prioritas), _aturan_ke_tabel()


def hapus_aturan(id_aturan):
    """Hapus satu aturan triase berdasarkan ID."""
    if not id_aturan:
        return "⚠️ Pilih dulu ID aturan yang dihapus.", _aturan_ke_tabel()
    aturan = _muat_aturan()
    sisa = [a for a in aturan if a.get("id") != id_aturan]
    if len(sisa) == len(aturan):
        return "⚠️ Aturan {} tidak ditemukan.".format(id_aturan), \
            _aturan_ke_tabel()
    _simpan_aturan(sisa)
    _catat_log("hapus_aturan", id_aturan, "aturan dihapus")
    return "✅ Aturan **{}** dihapus.".format(id_aturan), _aturan_ke_tabel()


def ubah_status_aturan(id_aturan):
    """Aktifkan / nonaktifkan satu aturan triase."""
    if not id_aturan:
        return "⚠️ Pilih dulu ID aturan.", _aturan_ke_tabel()
    aturan = _muat_aturan()
    for a in aturan:
        if a.get("id") == id_aturan:
            a["aktif"] = not a.get("aktif", True)
            _simpan_aturan(aturan)
            status = "Aktif" if a["aktif"] else "Nonaktif"
            _catat_log("ubah_status_aturan", id_aturan,
                       "status -> {}".format(status))
            return "✅ Aturan **{}** sekarang **{}**.".format(id_aturan,
                                                             status), \
                _aturan_ke_tabel()
    return "⚠️ Aturan {} tidak ditemukan.".format(id_aturan), \
        _aturan_ke_tabel()


# ---------------------------------------------------------------------------
# TUGAS TAMBAHAN — Bantu Verifikasi Login (perintah Cipta, 19 Nov 2026)
# ---------------------------------------------------------------------------
# ATURAN KERAS (ditulis di app + LAPORAN):
# 1) Kode verifikasi TIDAK PERNAH disimpan di file / log / memori agent.
#    Fungsi di bawah ini HANYA menampilkan kode di layar dan TIDAK
#    menulisnya ke mana pun — log aktivitas hanya mencatat bahwa pencarian
#    dilakukan (layanan + ditemukan/tidak), TANPA kodenya.
# 2) Kode TIDAK PERNAH dikirim ke siapa pun — kode hanya dipakai untuk
#    login yang sedang berjalan itu (browser/Muse yang sedang sign-in).
# 3) Kode hanya dicari saat ada permintaan login yang jelas: pemanggil
#    WAJIB mengisi nama layanan (mis. TikTok / Google / Instagram).
#    Tanpa nama layanan, fungsi menolak mencari.
# 4) Di mode demo, kode yang ditemukan berasal dari data CONTOH dan
#    ditandai PALSU — jangan dipakai untuk login sungguhan.
POLA_KODE = [
    re.compile(r"(?:kode verifikasi|verification code|kode login|kode otp|"
               r"\bOTP\b)[^\d]{0,40}(\d{4,8})", re.IGNORECASE),
    re.compile(r"(?:adalah|is)\s+(\d{4,8})", re.IGNORECASE),
    re.compile(r"\b(\d{6})\b"),
]


def _ekstrak_kode(teks):
    """Ambil kode verifikasi dari teks email. Kembalikan kode (string)
    atau None. Fungsi ini murni membaca teks — tidak menyimpan apa pun."""
    teks = teks or ""
    for pola in POLA_KODE:
        m = pola.search(teks)
        if m:
            return m.group(1)
    return None


def cari_kode_verifikasi(layanan, pengirim_hint=""):
    """Cari email kode verifikasi TERBARU yang cocok dengan layanan.

    WAJIB ada nama layanan (permintaan login yang jelas). Mengembalikan
    markdown untuk ditampilkan di layar SAJA. Kode TIDAK PERNAH ditulis
    ke file/log — _catat_log di bawah ini sengaja TIDAK menerima kode.
    """
    layanan = (layanan or "").strip()
    if not layanan:
        return ("⚠️ **Isi dulu nama layanannya** (mis. TikTok, Google, "
                "Instagram) — kode hanya dicari saat ada permintaan login "
                "yang jelas.")
    hint = (pengirim_hint or "").strip().lower()
    kunci = layanan.lower()
    kandidat = []
    for e in _muat_email():
        gabung = "{} {} {}".format(e.get("subjek", ""), e.get("isi", ""),
                                   e.get("pengirim", "")).lower()
        if kunci not in gabung:
            continue
        if hint and hint not in gabung:
            continue
        if "verifikasi" not in gabung and "verification" not in gabung \
                and "kode" not in gabung and "otp" not in gabung:
            continue
        kandidat.append(e)
    kandidat.sort(key=lambda x: x.get("tanggal", ""), reverse=True)
    for e in kandidat:
        kode = _ekstrak_kode("{} {}".format(e.get("subjek", ""),
                                            e.get("isi", "")))
        if not kode:
            continue
        # LOG TANPA KODE — hanya layanan + hasil.
        _catat_log("cari_kode_verifikasi",
                   "layanan={} (email {})".format(layanan, e.get("id", "?")),
                   "kode ditemukan — TIDAK disimpan di log")
        contoh = " (CONTOH — kode PALSU, jangan dipakai login sungguhan)" \
            if e.get("contoh") else ""
        return "\n".join([
            "## 🔑 Kode Verifikasi — {}".format(layanan),
            "",
            "Kode terbaru dari email **{}** ({}):".format(
                e.get("pengirim", "?"), e.get("tanggal", "?")),
            "",
            "# `{}`".format(kode),
            "",
            "⚠️ **Aturan keras:** kode ini HANYA tampil di layar — "
            "**tidak disimpan** di file, log, atau memori agent. Pakai "
            "untuk login yang sedang berjalan ini saja, jangan bagikan ke "
            "siapa pun.{}".format(contoh),
        ])
    _catat_log("cari_kode_verifikasi", "layanan={}".format(layanan),
               "tidak ditemukan — BELUM CUKUP DATA")
    return ("## 🔑 Kode Verifikasi — {}\n\n"
            "❌ **Tidak ditemukan** email kode verifikasi yang cocok untuk "
            "'{}' di data CONTOH.\n\n"
            "Kemungkinan: (1) kodenya belum masuk / masuk ke akun email lain "
            "(cek pemilih akun), (2) Gmail belum terhubung sehingga agent "
            "hanya melihat data CONTOH, (3) layanan ditulis berbeda "
            "(coba nama lain, mis. 'Google' bukan 'Gmail').\n\n"
            "**BELUM CUKUP DATA** — jangan menebak kode.".format(
                layanan, layanan))


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
def _pilihan_email_semua():
    semua = _muat_email()
    return ["{} — {}".format(e.get("id", "?"), e.get("subjek", "?"))
            for e in sorted(semua, key=lambda x: x.get("tanggal", ""),
                            reverse=True)]


def build_ui():
    with gr.Blocks(title="Agent 13 — Email (Penjaga Email)",
                   analytics_enabled=False) as demo:
        gr.Markdown(
            "# 📧 Agent 13 — Email (Penjaga Email)\n"
            "Memegang kendali email Cipta: triase kotak masuk, draf balasan, "
            "pencarian email, aturan triase — dan membantu menemukan kode "
            "verifikasi login terbaru.\n\n"
            "🔒 **Aturan keras:** agent TIDAK PERNAH mengirim, menghapus, "
            "atau mengarsip email. Semua output adalah DRAF — "
            f"{LABEL_PERSETUJUAN}. Kode verifikasi TIDAK PERNAH disimpan "
            "di file / log / memori agent.\n\n"
            "🎛️ **Struktur komando:** Agent 13 berada DI BAWAH KENDALI "
            "MUSE — Muse yang mengarahkan dan mengoordinasikan; Agent 13 "
            "bekerja untuk kepentingan Muse dan Cipta. Keputusan penting "
            "(kirim email, hapus, ubah setelan) tetap di tangan Cipta.")

        with gr.Tab("📥 Kotak Masuk"):
            gr.Markdown(MODE_DEMO)
            with gr.Row():
                akun_dd = gr.Dropdown(choices=["Semua"] + AKUN,
                                      value=AKUN_UTAMA,
                                      label="Akun email")
                btn_muat = gr.Button("Muat Kotak Masuk", variant="primary")
            gr.Markdown("### 🟢 Status Siaga — Agent 13 STANDBY (Tugas Harian poin 27)")
            status_siaga = gr.Markdown(status_siaga_md())
            with gr.Row():
                btn_cek = gr.Button("🔄 Cek Email Sekarang", variant="primary")
            gr.Markdown("### 📋 Log Pemeriksaan (terbaru di atas)")
            log_tabel_pemeriksaan = gr.Dataframe(
                headers=["Tanggal", "Total", "Baru", "Penting Baru",
                         "Draf Dibuat", "Durasi (dtk)"],
                value=_log_pemeriksaan_ke_tabel(), interactive=False,
                wrap=True)
            btn_cek.click(fn=cek_email_sekarang_ui, inputs=[akun_dd],
                          outputs=[status_siaga, log_tabel_pemeriksaan])
            ringkasan = gr.Markdown()
            tabel_inbox = gr.Dataframe(
                headers=["ID", "Tanggal", "Pengirim", "Subjek", "Kategori",
                         "Prioritas", "Dibaca", "Butuh Balasan"],
                interactive=False, wrap=True)
            with gr.Row():
                pilih_email = gr.Dropdown(choices=_pilihan_email_semua(),
                                          label="Pilih email (untuk detail / draf / tandai)")
                btn_detail = gr.Button("Lihat Detail")
            detail = gr.Markdown()
            with gr.Row():
                btn_butuh = gr.Button("🚩 Tandai Butuh Balasan")
                btn_dibaca = gr.Button("✓ Tandai Sudah Dibaca")
            pesan_tandai = gr.Markdown("")
            gr.Markdown("### 📋 Log Aktivitas (terbaru di atas)")
            log_tabel_inbox = gr.Dataframe(
                headers=["Tanggal", "Aksi", "Detail", "Hasil"],
                value=_log_ke_tabel(), interactive=False, wrap=True)
            btn_muat.click(fn=muat_kotak_masuk, inputs=[akun_dd],
                           outputs=[ringkasan, tabel_inbox, pilih_email])
            btn_detail.click(fn=detail_email, inputs=[pilih_email],
                             outputs=[detail])
            btn_butuh.click(fn=tandai_butuh_balasan, inputs=[pilih_email],
                            outputs=[pesan_tandai, tabel_inbox,
                                     log_tabel_inbox])
            btn_dibaca.click(fn=tandai_sudah_dibaca, inputs=[pilih_email],
                             outputs=[pesan_tandai, tabel_inbox,
                                      log_tabel_inbox])

            gr.Markdown("---\n### 🔑 Bantu Verifikasi Login")
            gr.Markdown(
                "Bila browser / Muse sedang sign-in dan menunggu kode "
                "verifikasi dari email, agent membantu menemukan email kode "
                "terbaru yang cocok dan menampilkannya supaya login bisa "
                "lanjut.\n\n"
                "**Aturan keras:** kode TIDAK PERNAH disimpan di file / log "
                "/ memori agent · TIDAK PERNAH dikirim ke siapa pun — hanya "
                "dipakai untuk login yang sedang berjalan itu · hanya dicari "
                "saat ada permintaan login yang jelas (nama layanan wajib "
                "diisi).")
            with gr.Row():
                layanan_tb = gr.Textbox(
                    label="Layanan yang sedang login *",
                    placeholder="cth. TikTok / Google / Instagram")
                pengirim_tb = gr.Textbox(
                    label="Pengirim (opsional — bila tahu)",
                    placeholder="cth. tiktok.com / accounts.google.com")
            btn_kode = gr.Button("🔑 Cari Kode Verifikasi Terbaru",
                                 variant="primary")
            hasil_kode = gr.Markdown()
            btn_kode.click(fn=cari_kode_verifikasi,
                           inputs=[layanan_tb, pengirim_tb],
                           outputs=[hasil_kode])

        with gr.Tab("✍️ Draf Balasan"):
            gr.Markdown(
                "Buat draf balasan dari email terpilih. **TIDAK ADA tombol "
                "kirim** — draf hanya bisa disimpan, lalu Cipta yang "
                "memutuskan pengirimannya.\n\n"
                f"Setiap draf berlabel: **{LABEL_PERSETUJUAN}**.")
            with gr.Row():
                draf_email = gr.Dropdown(choices=_pilihan_email_semua(),
                                         label="Balas email *")
                draf_template = gr.Dropdown(
                    choices=[(v["nama"], k)
                             for k, v in TEMPLATE_DRAF.items()],
                    value="umum", label="Template *")
            draf_catatan = gr.Textbox(
                label="Catatan tambahan dari Cipta (opsional)",
                placeholder="cth. Tanyakan juga jadwal pengiriman produknya",
                lines=2)
            with gr.Row():
                btn_pratinjau = gr.Button("👁️ Lihat Pratinjau Draf",
                                          variant="primary")
                btn_simpan = gr.Button("💾 Simpan Draf")
            draf_state = gr.State(None)
            pratinjau = gr.Markdown()
            pesan_simpan = gr.Markdown("")
            gr.Markdown("### 📋 Draf Tersimpan (terbaru di atas)")
            tabel_draf = gr.Dataframe(
                headers=["ID", "Email", "Template", "Subjek Balasan",
                         "Status"],
                value=_draf_ke_tabel(), interactive=False, wrap=True)
            btn_pratinjau.click(fn=pratinjau_draf,
                                inputs=[draf_email, draf_template,
                                        draf_catatan],
                                outputs=[pratinjau, draf_state])
            btn_simpan.click(fn=simpan_draf, inputs=[draf_state],
                             outputs=[pesan_simpan, tabel_draf])

        with gr.Tab("🔍 Cari Email"):
            gr.Markdown(
                "Cari di data CONTOH berdasarkan kata kunci + filter akun / "
                "kategori / tanggal. Bila yang dicari adalah email asli dan "
                "Gmail belum terhubung, hasilnya bisa kosong — itu "
                "**BELUM CUKUP DATA**, bukan berarti emailnya tidak ada.")
            with gr.Row():
                cari_kunci = gr.Textbox(label="Kata kunci",
                                        placeholder="cth. devpost / lomba / pajak")
                cari_akun = gr.Dropdown(choices=["Semua"] + AKUN,
                                        value="Semua", label="Akun")
                cari_kat = gr.Dropdown(choices=["Semua"] + KATEGORI,
                                       value="Semua", label="Kategori")
            with gr.Row():
                cari_dari = gr.Textbox(label="Tanggal dari (YYYY-MM-DD)",
                                       placeholder="2026-11-18")
                cari_sampai = gr.Textbox(label="Tanggal sampai (YYYY-MM-DD)",
                                         placeholder="2026-11-19")
            btn_cari = gr.Button("🔍 Cari", variant="primary")
            hasil_cari = gr.Markdown()
            tabel_cari = gr.Dataframe(
                headers=["ID", "Tanggal", "Pengirim", "Subjek", "Kategori",
                         "Prioritas", "Dibaca", "Butuh Balasan"],
                interactive=False, wrap=True)
            btn_cari.click(fn=cari_email,
                           inputs=[cari_kunci, cari_akun, cari_kat,
                                   cari_dari, cari_sampai],
                           outputs=[hasil_cari, tabel_cari])

        with gr.Tab("⚙️ Aturan & Log"):
            gr.Markdown(
                "Aturan triase menentukan kategori + prioritas setiap email. "
                "Urutan cek: aturan **pengirim** dulu, lalu **kata_kunci**; "
                "aturan pertama yang cocok menang. Tanpa aturan yang cocok → "
                "**BELUM CUKUP DATA**.")
            gr.Markdown("### 📏 Daftar Aturan Triase")
            tabel_aturan = gr.Dataframe(
                headers=["ID", "Jenis", "Pola", "Kategori", "Prioritas",
                         "Status"],
                value=_aturan_ke_tabel(), interactive=False, wrap=True)
            with gr.Row():
                at_jenis = gr.Dropdown(choices=["pengirim", "kata_kunci"],
                                       value="kata_kunci", label="Jenis *")
                at_pola = gr.Textbox(label="Pola *",
                                     placeholder="cth. support@devpost.com / lomba")
                at_kat = gr.Dropdown(choices=KATEGORI, value="Penting",
                                     label="Kategori *")
                at_pri = gr.Dropdown(choices=["Tinggi", "Sedang", "Rendah"],
                                     value="Sedang", label="Prioritas *")
            at_catatan = gr.Textbox(label="Catatan (opsional)",
                                    placeholder="cth. Semua email lomba poster")
            btn_tambah_aturan = gr.Button("➕ Tambah Aturan",
                                          variant="primary")
            with gr.Row():
                at_id = gr.Dropdown(
                    choices=[a.get("id", "") for a in _muat_aturan()],
                    label="ID aturan")
                btn_toggle = gr.Button("🔄 Aktifkan / Nonaktifkan")
                btn_hapus = gr.Button("🗑️ Hapus Aturan")
            pesan_aturan = gr.Markdown("")
            btn_tambah_aturan.click(
                fn=tambah_aturan,
                inputs=[at_jenis, at_pola, at_kat, at_pri, at_catatan],
                outputs=[pesan_aturan, tabel_aturan])
            btn_toggle.click(fn=ubah_status_aturan, inputs=[at_id],
                             outputs=[pesan_aturan, tabel_aturan])
            btn_hapus.click(fn=hapus_aturan, inputs=[at_id],
                            outputs=[pesan_aturan, tabel_aturan])

            gr.Markdown("### 🔌 Status Koneksi Gmail")
            gr.Markdown(status_gmail())
            gr.Markdown("### 📋 Log Aktivitas (terbaru di atas)")
            log_tabel = gr.Dataframe(
                headers=["Tanggal", "Aksi", "Detail", "Hasil"],
                value=_log_ke_tabel(), interactive=False, wrap=True)
            btn_muat_log = gr.Button("🔄 Muat Ulang Log")
            btn_muat_log.click(fn=lambda: _log_ke_tabel(), outputs=[log_tabel])

        # Pemeriksaan berkala otomatis (poin 27): cek sekali saat UI dibuka,
        # lalu tiap jam selama UI terbuka — memakai akun yang sedang dipilih
        # di Tab 1. (gr.Timer = pemicu berkala Gradio 6.)
        demo.load(fn=cek_email_sekarang_ui, inputs=[akun_dd],
                  outputs=[status_siaga, log_tabel_pemeriksaan])
        timer_siaga = gr.Timer(INTERVAL_CEK_DETIK)
        timer_siaga.tick(fn=cek_email_sekarang_ui, inputs=[akun_dd],
                         outputs=[status_siaga, log_tabel_pemeriksaan])
    return demo


# ---------------------------------------------------------------------------
# TUGAS HARIAN POIN 27 — Agent 13 STANDBY dan FAST RESPON (Cipta, 19 Nov 2026)
# ---------------------------------------------------------------------------
# Agent 13 harus SELALU CEK EMAIL: (a) indikator status "Siaga" di UI;
# (b) tombol "Cek Email Sekarang" + pemeriksaan berkala otomatis tiap jam
# saat UI terbuka; (c) draf balasan cepat untuk email penting (target draf
# siap <1 menit setelah email penting masuk); (d) log setiap pemeriksaan
# (waktu + jumlah email baru + yang penting) di log-pemeriksaan.json;
# (e) mode CLI sekali-jalan `python app.py --check-once` supaya cron Muse
# bisa menjalankan pemeriksaan tiap jam tanpa membuka UI.
SIAGA_PATH = os.path.join(DATA_DIR, "status-siaga-email.json")  # PUSAT KOMANDO: data/ bersama
PERIKSA_PATH = os.path.join(DATA_DIR, "log-pemeriksaan-email.json")  # PUSAT KOMANDO: data/ bersama
INTERVAL_CEK_DETIK = 3600  # pemeriksaan berkala: tiap 1 jam (saat UI terbuka)
TARGET_DRAF_CEPAT_DETIK = 60  # draf penting siap < 1 menit
KATEGORI_PENTING_DRAF = ("Penting", "Lomba", "Keuangan", "Affiliate/Bisnis")


def _muat_siaga():
    data = _muat_json(SIAGA_PATH, {})
    if not isinstance(data, dict):
        data = {}
    data.setdefault("terakhir_cek", None)
    data.setdefault("email_terlihat", [])
    data.setdefault("total_cek", 0)
    return data


def _muat_log_pemeriksaan():
    return _muat_json(PERIKSA_PATH, [])


def _log_pemeriksaan_ke_tabel(log=None):
    log = log if log is not None else _muat_log_pemeriksaan()
    if not log:
        return [["(belum ada pemeriksaan)", "", "", "", "", ""]]
    return [[e.get("tanggal", ""), str(e.get("total_email", "")),
             str(e.get("baru", "")), str(e.get("penting_baru", "")),
             str(e.get("draf_dibuat", "")),
             str(e.get("durasi_detik", ""))]
            for e in reversed(log)]


def status_siaga_md():
    """(a) Indikator status Siaga untuk UI."""
    siaga = _muat_siaga()
    log = _muat_log_pemeriksaan()
    terakhir = log[-1] if log else None
    baris = ["🟢 **SIAGA — Agent 13 aktif memantau email.**",
             "",
             "- **Pemeriksaan berkala:** tiap {} menit saat UI terbuka "
             "(+ tombol 'Cek Email Sekarang' + CLI `--check-once` untuk "
             "cron tiap jam).".format(INTERVAL_CEK_DETIK // 60),
             "- **Total pemeriksaan:** {} kali.".format(
                 siaga.get("total_cek", 0)),
             "- **Terakhir cek:** {}.".format(
                 siaga.get("terakhir_cek") or "belum pernah"),
             ]
    if terakhir:
        baris.append("- **Hasil cek terakhir:** {} email total, {} baru, "
                     "{} penting baru, {} draf cepat dibuat, durasi {} "
                     "detik.".format(
                         terakhir.get("total_email", "?"),
                         terakhir.get("baru", "?"),
                         terakhir.get("penting_baru", "?"),
                         terakhir.get("draf_dibuat", "?"),
                         terakhir.get("durasi_detik", "?")))
    baris.append("- **Mode:** {} (Gmail belum terhubung — data CONTOH).".format(
        "demo"))
    baris.append("")
    baris.append("Target: draf balasan untuk email penting siap "
                 "dalam <{} detik setelah email masuk.".format(
                     TARGET_DRAF_CEPAT_DETIK))
    return "\n".join(baris)


def _template_untuk_draf_cepat(email):
    """Pilih template draf cepat dari kategori email."""
    kat = email.get("kategori", "")
    if kat == "Lomba":
        return "lomba"
    if kat == "Affiliate/Bisnis":
        return "bisnis"
    return "umum"


def _adalah_email_kode(email):
    """True bila email ini berisi kode verifikasi — email kode TIDAK
    pernah dibuatkan draf balasan (tidak ada yang perlu dibalas)."""
    gabung = "{} {}".format(email.get("subjek", ""),
                            email.get("isi", "")).lower()
    return "kode verifikasi" in gabung or "verification code" in gabung


def draf_cepat_penting(email_penting_baru):
    """(c) Buat draf balasan cepat (mode template — instan, tanpa menunggu
    Gemini) untuk email penting baru.

    Mengembalikan (daftar_id_draf, durasi_detik). Draf yang dibuat
    berstatus DRAF + label persetujuan, sama seperti draf biasa.
    Email kode verifikasi dilewati — tidak dibuatkan draf."""
    import time

    mulai = time.time()
    from datetime import datetime

    draf_lama = _muat_draf()
    sudah = {d.get("email_id") for d in draf_lama}
    dibuat = []
    for e in email_penting_baru:
        if e.get("id") in sudah:
            continue
        if _adalah_email_kode(e):
            continue
        kunci = _template_untuk_draf_cepat(e)
        d = _draf_template(e, kunci)
        baru_id = "D{:03d}".format(len(draf_lama) + len(dibuat) + 1)
        draf_lama.append({
            "id": baru_id,
            "email_id": e.get("id", "?"),
            "template": kunci,
            "subjek_balasan": d["subjek_balasan"],
            "isi": d["isi"],
            "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "DRAF — {}".format(LABEL_PERSETUJUAN),
            "mode": "template-cepat (siaga, <{} dtk)".format(
                TARGET_DRAF_CEPAT_DETIK),
        })
        dibuat.append(baru_id)
    if dibuat:
        _simpan_json(DRAF_PATH, draf_lama)
    return dibuat, round(time.time() - mulai, 2)


def cek_email_sekarang(akun="Semua"):
    """(b)+(d) Pemeriksaan siaga sekali-jalan.

    Membandingkan kotak masuk (CONTOH) dengan daftar email yang sudah
    terlihat di status-siaga.json, membuat draf cepat untuk email penting
    baru, mencatat hasilnya ke log-pemeriksaan.json + log aktivitas.
    Mengembalikan (status_md, tabel_log_pemeriksaan, ringkasan_teks)
    untuk UI dan CLI."""
    import time
    from datetime import datetime

    mulai = time.time()
    sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    siaga = _muat_siaga()
    terlihat = set(siaga.get("email_terlihat", []))
    semua = _muat_email()
    cakupan = list(semua)
    if akun != "Semua":
        cakupan = [e for e in semua if e.get("akun") == akun]
    baru = [e for e in cakupan if e.get("id") not in terlihat]
    penting_baru = [e for e in baru
                    if e.get("prioritas") == "Tinggi"
                    and e.get("kategori") in KATEGORI_PENTING_DRAF
                    and not _adalah_email_kode(e)]
    dibuat, durasi_draf = draf_cepat_penting(penting_baru)
    durasi = round(time.time() - mulai, 2)

    siaga["terakhir_cek"] = sekarang
    siaga["email_terlihat"] = sorted({e.get("id", "") for e in semua
                                      if e.get("id")})
    siaga["total_cek"] = siaga.get("total_cek", 0) + 1
    _simpan_json(SIAGA_PATH, siaga)

    log = _muat_log_pemeriksaan()
    log.append({"tanggal": sekarang, "mode": "demo (CONTOH)",
                "akun": akun, "total_email": len(cakupan),
                "baru": len(baru), "penting_baru": len(penting_baru),
                "draf_dibuat": len(dibuat), "durasi_detik": durasi,
                "durasi_draf_detik": durasi_draf})
    _simpan_json(PERIKSA_PATH, log)
    _catat_log("cek_email", "akun={} (siaga)".format(akun),
               "{} baru, {} penting, {} draf cepat".format(
                   len(baru), len(penting_baru), len(dibuat)))

    target_ok = "✅" if durasi_draf < TARGET_DRAF_CEPAT_DETIK else "⚠️"
    ringkasan = ("Pemeriksaan {} — total {} email, {} baru, {} penting baru, "
                 "{} draf cepat dibuat {} (durasi draf {} dtk, target <{} "
                 "dtk).".format(sekarang, len(cakupan), len(baru),
                                len(penting_baru), len(dibuat), target_ok,
                                durasi_draf, TARGET_DRAF_CEPAT_DETIK))
    if penting_baru:
        ringkasan += "\nEmail penting baru: " + ", ".join(
            "{} ({})".format(e.get("id", "?"), e.get("subjek", "?"))
            for e in penting_baru)
    if dibuat:
        ringkasan += "\nDraf cepat: " + ", ".join(dibuat)
    return status_siaga_md(), _log_pemeriksaan_ke_tabel(), ringkasan


def cek_email_sekarang_ui(akun="Semua"):
    """Pembungkus untuk tombol / pemicu berkala di UI."""
    status_md, tabel, _ = cek_email_sekarang(akun)
    return status_md, tabel


def cli_check_once(akun="Semua"):
    """(e) Mode CLI sekali-jalan untuk cron Muse (tiap jam, tanpa UI).

    Mencetak ringkasan pemeriksaan ke stdout, keluar dengan kode 0.
    Dipakai: `python app.py --check-once [--akun masduki1189@gmail.com]`.
    """
    _, _, ringkasan = cek_email_sekarang(akun)
    print("=== Agent 13 — Cek Email Sekarang (CLI, mode demo) ===")
    print(ringkasan)
    print("Log pemeriksaan: data/log-pemeriksaan.json")
    print("Draf tersimpan: data/draf-balasan.json "
          "(BUTUH PERSETUJUAN Cipta sebelum dikirim)")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Agent 13 — Email (Penjaga Email)")
    parser.add_argument(
        "--check-once", action="store_true",
        help="Pemeriksaan siaga sekali-jalan lalu keluar (untuk cron Muse "
             "tiap jam, tanpa membuka UI).")
    parser.add_argument(
        "--akun", default="Semua",
        help="Akun email yang diperiksa (default: Semua).")
    args = parser.parse_args()
    if args.check_once:
        sys.exit(cli_check_once(args.akun))
    demo = build_ui()
    demo.launch(server_name="0.0.0.0",
                server_port=int(os.environ.get("PORT", "7860")))
