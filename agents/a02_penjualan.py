# ======================================================================
# PUSAT KOMANDO — salinan dari agent-penjualan-oracle (Agent 2 Penjualan).
# JANGAN edit logika di sini sembarangan: perbaikan sebaiknya dibuat di
# agent aslinya lalu disalin ulang. Satu-satunya perubahan dari aslinya:
# path data dialihkan ke folder data/ bersama di pusat-komando/ (ditandai
# komentar 'PUSAT KOMANDO').
# ======================================================================
# Agent Penjualan Podcast Meong
# Chat penjualan + generator promosi + pelacak leads + rencana harian.
# GRATIS: model Google Gemini free tier (google-genai). API key HANYA dari
# environment variable GEMINI_API_KEY — tidak pernah ditulis di file.
# Tanpa key, semua fitur tetap jalan dalam mode template/knowledge-base.
import json
import os
import re
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

BASE = Path(__file__).resolve().parent.parent / "data"  # PUSAT KOMANDO: folder data bersama
LEADS_FILE = BASE / "leads.json"
MODEL = "gemini-4-hydrogen"
PORT = int(os.environ.get("PORT", "8000"))

# ---------------------------------------------------------------- knowledge base
KB = """DATA RESMI PODCAST MEONG (satu-satunya sumber kebenaran — jangan mengarang di luar ini):
- Podcast Meong: podcast komedi kucing Oyen (oren) & Momo (abu-abu). Episode tayang 07:00 & 19:00 WIB.
- YouTube @Podcastmeong, TikTok @podcast_kucing, Instagram podcast_meong. Website: https://podcastmeong.github.io/
- JASA VIDEO PROMO (KikiWorks, produk utama): video vertikal 9:16 (TikTok, Reels, WhatsApp), tokoh Oyen & Momo.
  Paket Sederhana 15 detik Rp75.000 (1 video, 1 produk, teks + musik).
  Paket Standar 30 detik Rp150.000 (dialog singkat, 1-2 produk, teks + musik + SFX).
  Paket Storytelling 60 detik Rp250.000 (cerita komedi pendek Oyen+Momo, teks + musik + SFX).
  Semua paket termasuk naskah singkat + 1x revisi kecil.
- Video contoh jasa: https://www.youtube.com/shorts/ONkM6dQQHxg
- Cara pesan: DM Instagram @podcast_meong.
- eBook: Cerita Nabi & Orang Sholeh untuk anak Rp29.000 (KaryaKarsa); "Si Oyen Penjaga Kolam Ikan" Rp29.000; "Rindu di Ujung Senja" Rp19.000.
- POD: kaos & produk kucing di Zazzle (toko Podcast_Meong).
- ATURAN JUJUR: jangan janjikan views, viral, atau penjualan naik. Yang dijual hanya video promosi + naskah + 1x revisi kecil. Tidak ada klaim penghasilan palsu. Target realistis: 1-3 pelanggan dari 10-15 penawaran pertama."""

SYSTEM_PROMPT = (
    "Anda adalah Asisten Penjualan Podcast Meong. Jawab Bahasa Indonesia, ramah, singkat, sopan. "
    "Anda membantu calon pembeli memahami jasa video promo, eBook, dan produk POD. "
    "Gunakan HANYA data di bawah ini. Jangan mengarang harga, tautan, testimoni, atau janji hasil. "
    "Bila ditanya hal di luar data, katakan tidak tahu dan arahkan ke DM Instagram @podcast_meong.\n\n" + KB
)

PAKET = {
    "15": {"nama": "Sederhana", "durasi": "15 detik", "harga": "Rp75.000",
           "isi": "1 video promosi pendek, tokoh Oyen/Momo, 1 produk, teks + musik"},
    "30": {"nama": "Standar", "durasi": "30 detik", "harga": "Rp150.000",
           "isi": "Video promosi + dialog singkat, 1-2 produk, teks + musik + SFX"},
    "60": {"nama": "Storytelling", "durasi": "60 detik", "harga": "Rp250.000",
           "isi": "Cerita komedi pendek Oyen+Momo mempromosikan produk, teks + musik + SFX"},
}
CONTOH_VIDEO = "https://www.youtube.com/shorts/ONkM6dQQHxg"
STATUS_LEAD = ["baru", "dihubungi", "menunggu", "setuju", "tolak"]

app = FastAPI(title="Agent Penjualan Podcast Meong")


# ---------------------------------------------------------------- Gemini (opsional)
def gemini_client():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception:
        return None


def gemini_ask(prompt: str):
    """Kembalikan teks jawaban Gemini, atau None bila key tidak ada / gagal."""
    client = gemini_client()
    if client is None:
        return None
    try:
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        text = (getattr(resp, "text", "") or "").strip()
        return text or None
    except Exception:
        return None


def mode_ai():
    return "gemini" if os.environ.get("GEMINI_API_KEY", "").strip() else "template"


# ---------------------------------------------------------------- chat (fallback template)
def jawab_template(pesan: str) -> str:
    p = pesan.lower()
    if re.search(r"harga|paket|biaya|tarif|berapa", p):
        baris = "\n".join(
            f"- {v['nama']} {v['durasi']}: {v['harga']} — {v['isi']}"
            for v in PAKET.values()
        )
        return (
            "Ini paket jasa video promo kami (sudah termasuk naskah singkat + 1x revisi kecil):\n"
            f"{baris}\n\nVideo contoh: {CONTOH_VIDEO}\n"
            "Untuk pesan, silakan DM Instagram @podcast_meong. "
            "Boleh saya tahu produk Kakak apa dan mau paket yang mana?"
        )
    if re.search(r"ebook|e-book|buku|cerita nabi|orang sholeh", p):
        return (
            "eBook kami: Cerita Nabi & Orang Sholeh untuk anak Rp29.000 (di KaryaKarsa), "
            "\"Si Oyen Penjaga Kolam Ikan\" Rp29.000, dan \"Rindu di Ujung Senja\" Rp19.000. "
            "Info lengkap: https://podcastmeong.github.io/"
        )
    if re.search(r"kaos|pod|zazzle|merch|baju", p):
        return (
            "Produk POD kami (kaos & produk kucing) ada di toko Zazzle Podcast_Meong. "
            "Silakan cek katalognya di website: https://podcastmeong.github.io/"
        )
    if re.search(r"pesan|order|beli|dm|cara (pesan|order|beli)", p):
        return (
            "Untuk memesan jasa video promo, silakan DM Instagram @podcast_meong "
            "dengan menyebutkan nama toko, produk, dan paket yang diinginkan "
            "(15 detik Rp75.000 / 30 detik Rp150.000 / 60 detik Rp250.000). "
            f"Video contoh: {CONTOH_VIDEO}"
        )
    if re.search(r"contoh|sample|demo|lihat video", p):
        return f"Video contoh jasa video promo kami: {CONTOH_VIDEO}\nEpisode podcast Oyen & Momo tayang 07:00 & 19:00 WIB di YouTube @Podcastmeong dan TikTok @podcast_kucing."
    if re.search(r"halo|hai|hi|pagi|siang|sore|malam|selamat", p):
        return (
            "Halo Kak! Saya Asisten Penjualan Podcast Meong. Saya bisa bantu info paket video promo "
            "(15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000), eBook, dan produk POD. "
            "Kakak mau tanya yang mana?"
        )
    return (
        "Terima kasih Kak! Saya bisa bantu info paket jasa video promo, eBook, dan produk POD Podcast Meong. "
        "Silakan tanyakan harga paket, video contoh, atau cara pemesanan. "
        "Untuk pemesanan langsung: DM Instagram @podcast_meong."
    )


class ChatIn(BaseModel):
    message: str


@app.post("/api/chat")
def chat(inp: ChatIn):
    pesan = (inp.message or "").strip()
    if not pesan:
        raise HTTPException(status_code=400, detail="Pesan kosong.")
    jawaban = gemini_ask(SYSTEM_PROMPT + "\n\nPertanyaan calon pembeli: " + pesan)
    if jawaban:
        return {"reply": jawaban, "mode": "gemini"}
    return {"reply": jawab_template(pesan), "mode": "template"}


# ---------------------------------------------------------------- generator promosi
class GenerateIn(BaseModel):
    jenis: str  # caption_tiktok | caption_ig | caption_yt | wa_outreach | wa_followup | dm_ig | email
    nama_toko: str = ""
    produk: str = ""
    paket: str = "30"  # 15 | 30 | 60


def template_generator(jenis: str, nama_toko: str, produk: str, paket: str) -> str:
    toko = nama_toko.strip() or "[Nama Toko]"
    produk_txt = produk.strip() or "produk"
    pk = PAKET.get(paket, PAKET["30"])
    harga = pk["harga"]
    durasi = pk["durasi"]
    if jenis == "caption_tiktok":
        return (
            f"Si Oyen lagi promosiin {produk_txt} dari {toko}! 🐱✨\n"
            f"Video promosi {durasi} cuma {harga} — tokoh kucing lucu, naskah + 1x revisi sudah termasuk.\n"
            f"Contoh videonya: {CONTOH_VIDEO}\n"
            "Pesan via DM IG @podcast_meong 📩\n"
            "#PodcastMeong #Oyen #VideoPromo #PetShop #FYP #KucingOren"
        )
    if jenis == "caption_ig":
        return (
            f"✨ {toko} x Podcast Meong ✨\n"
            f"{produk_txt} sekarang punya video promosi sendiri — dibintangi Oyen & Momo! 🐱\n"
            f"Paket {pk['nama']} {durasi}: {harga} (naskah + 1x revisi kecil termasuk).\n"
            f"Lihat contoh: {CONTOH_VIDEO}\n"
            "Pesan: DM @podcast_meong 📩\n"
            "#PodcastMeong #Oyen #Momo #VideoPromo #PetShop #UMKM"
        )
    if jenis == "caption_yt":
        return (
            f"Video promosi {produk_txt} untuk {toko} — dibintangi Oyen & Momo! 🐱🎥\n"
            f"Paket {pk['nama']} {durasi}: {harga}. Sudah termasuk naskah singkat + 1x revisi kecil.\n"
            f"Contoh: {CONTOH_VIDEO}\n"
            "Pesan jasa video promo: DM Instagram @podcast_meong.\n"
            "Podcast Meong — episode baru 07:00 & 19:00 WIB."
        )
    if jenis == "wa_outreach":
        return (
            f"Halo Kak, perkenalkan saya Masduki dari Podcast Meong (video kucing Oyen & Momo). "
            f"Saya menawarkan jasa video promosi AI untuk {toko}: video pendek 9:16 dengan karakter kucing lucu, "
            f"cocok untuk TikTok, Reels, dan WhatsApp. Contoh: {CONTOH_VIDEO}. "
            f"Harga: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000 "
            "(termasuk naskah + 1x revisi kecil). "
            f"Bila berminat, saya bisa buatkan contoh konsep dulu untuk {produk_txt}. Terima kasih 🙏"
        )
    if jenis == "wa_followup":
        return (
            f"Halo Kak, saya Masduki dari Podcast Meong — izin follow-up penawaran video promosi untuk {toko} kemarin. "
            f"Paketnya tetap: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000. "
            f"Contoh video: {CONTOH_VIDEO}. "
            "Kalau Kakak berkenan, saya bisa kirim contoh konsep untuk "
            f"{produk_txt} dulu, tanpa komitmen. Terima kasih 🙏"
        )
    if jenis == "dm_ig":
        return (
            f"Halo Kak, saya Masduki dari Podcast Meong — channel video kucing Oyen & Momo. "
            f"Saya buatkan video promosi AI pendek untuk {toko}: tokoh kucing lucu yang mempromosikan {produk_txt}. "
            f"Contoh videonya: {CONTOH_VIDEO}. "
            f"Paket: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000 "
            "(sudah termasuk naskah + 1x revisi kecil). "
            "Kalau Kakak berkenan, boleh saya kirim contoh konsep untuk toko Kakak? Terima kasih 🙏"
        )
    if jenis == "email":
        return (
            f"Subjek: Penawaran video promosi untuk {toko}\n\n"
            f"Halo Kak,\n\nSaya Masduki dari Podcast Meong, channel video kucing Oyen & Momo. "
            f"Saya menawarkan jasa video promosi AI: video pendek 9:16 dengan karakter kucing lucu "
            f"untuk mempromosikan {produk_txt}. Contoh video: {CONTOH_VIDEO}. "
            f"Paket: 15 detik Rp75.000, 30 detik Rp150.000, 60 detik Rp250.000 "
            "(termasuk naskah + 1x revisi kecil). Bila berkenan, saya bisa mengirim contoh konsep terlebih dahulu.\n\n"
            "Terima kasih,\nMasduki — Podcast Meong"
        )
    raise HTTPException(status_code=400, detail="Jenis tidak dikenal.")


@app.post("/api/generate")
def generate(inp: GenerateIn):
    draf = template_generator(inp.jenis, inp.nama_toko, inp.produk, inp.paket)
    hasil_ai = gemini_ask(
        "Anda copywriter pemasaran Podcast Meong. Perbaiki draf promosi berikut agar lebih menarik, "
        "tetap sopan, singkat, Bahasa Indonesia, dan JANGAN ubah harga, tautan, atau fakta apa pun. "
        "Jangan tambahkan janji viral/views/penjualan. Jangan tambahkan testimoni.\n\n" + draf
    )
    if hasil_ai:
        return {"hasil": hasil_ai, "mode": "gemini"}
    return {"hasil": draf, "mode": "template"}


# ---------------------------------------------------------------- leads (JSON lokal)
def load_leads():
    if not LEADS_FILE.exists():
        return []
    return json.loads(LEADS_FILE.read_text(encoding="utf-8")).get("leads", [])


def save_leads(leads):
    LEADS_FILE.write_text(
        json.dumps({"leads": leads}, ensure_ascii=False, indent=1), encoding="utf-8"
    )


class LeadIn(BaseModel):
    nama: str
    kontak: str = ""
    alamat: str = ""
    jenis: str = "pet shop"
    status: str = "baru"
    terverifikasi: bool = False
    catatan: str = ""


@app.get("/api/leads")
def list_leads():
    return {"leads": load_leads()}


@app.post("/api/leads")
def add_lead(inp: LeadIn):
    if not inp.nama.strip():
        raise HTTPException(status_code=400, detail="Nama lead wajib diisi.")
    if inp.status not in STATUS_LEAD:
        raise HTTPException(status_code=400, detail="Status tidak dikenal.")
    leads = load_leads()
    new_id = "lead-%02d" % (max([int(l["id"].split("-")[1]) for l in leads], default=0) + 1)
    lead = {"id": new_id, "nama": inp.nama.strip(), "kontak": inp.kontak.strip(),
            "alamat": inp.alamat.strip(), "jenis": inp.jenis.strip() or "pet shop",
            "status": inp.status, "terverifikasi": bool(inp.terverifikasi),
            "catatan": inp.catatan.strip()}
    leads.append(lead)
    save_leads(leads)
    return {"lead": lead}


@app.put("/api/leads/{lead_id}")
def update_lead(lead_id: str, inp: LeadIn):
    leads = load_leads()
    for lead in leads:
        if lead["id"] == lead_id:
            if inp.status not in STATUS_LEAD:
                raise HTTPException(status_code=400, detail="Status tidak dikenal.")
            lead.update({"nama": inp.nama.strip() or lead["nama"], "kontak": inp.kontak,
                         "alamat": inp.alamat, "jenis": inp.jenis or lead["jenis"],
                         "status": inp.status, "terverifikasi": bool(inp.terverifikasi),
                         "catatan": inp.catatan})
            save_leads(leads)
            return {"lead": lead}
    raise HTTPException(status_code=404, detail="Lead tidak ditemukan.")


@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: str):
    leads = load_leads()
    baru = [l for l in leads if l["id"] != lead_id]
    if len(baru) == len(leads):
        raise HTTPException(status_code=404, detail="Lead tidak ditemukan.")
    save_leads(baru)
    return {"ok": True}


# ---------------------------------------------------------------- rencana harian
@app.get("/api/rencana")
def rencana():
    leads = load_leads()
    by_status = {s: [l for l in leads if l["status"] == s] for s in STATUS_LEAD}
    aksi = []
    baru = by_status["baru"]
    if baru:
        prioritas = [l for l in baru if "WA" in l["kontak"] or "085" in l["kontak"] or "081" in l["kontak"]]
        pilih = (prioritas or baru)[:3]
        nama = ", ".join(l["nama"] for l in pilih)
        aksi.append({
            "judul": "Hubungi 3 lead baru (prioritas yang nomor WA-nya jelas)",
            "detail": f"Hubungi: {nama}. Pakai generator pesan WA outreach. Ingat: verifikasi dulu kontaknya (IG/TikTok/Shopee masih aktif) sebelum mengirim. Jangan hubungi yang statusnya masih 'belum terverifikasi' tanpa cek.",
            "lead": [l["id"] for l in pilih],
        })
    else:
        aksi.append({
            "judul": "Cari 5 target baru",
            "detail": "Semua lead awal sudah dihubungi. Cari 5 pet shop / toko hewan baru di Jakarta Selatan (Google Maps / Instagram), catat nama + kontak, dan tandai 'belum terverifikasi'.",
            "lead": [],
        })
    menunggu = by_status["menunggu"]
    if menunggu:
        nama = ", ".join(l["nama"] for l in menunggu[:3])
        aksi.append({
            "judul": "Follow-up lead yang menunggu jawaban",
            "detail": f"Kirim pesan follow-up sopan ke: {nama}. Pakai generator 'wa_followup'. Satu follow-up per lead, jangan spam.",
            "lead": [l["id"] for l in menunggu[:3]],
        })
    else:
        aksi.append({
            "judul": "Buat 1 konten promosi jasa hari ini",
            "detail": "Pakai generator caption TikTok/IG untuk mempromosikan paket video promo (contoh video: "
                      + CONTOH_VIDEO + "). Posting di akun @podcast_kucing / @meongcast setelah disetujui.",
            "lead": [],
        })
    dihubungi = by_status["dihubungi"]
    setuju = by_status["setuju"]
    if setuju:
        nama = ", ".join(l["nama"] for l in setuju)
        aksi.append({
            "judul": "Lanjutkan pelanggan yang sudah setuju",
            "detail": f"Konfirmasi paket + jadwal produksi untuk: {nama}. Minta detail produk dan kirim invoice/konfirmasi harga sesuai paket.",
            "lead": [l["id"] for l in setuju],
        })
    elif dihubungi:
        nama = ", ".join(l["nama"] for l in dihubungi[:3])
        aksi.append({
            "judul": "Cek balasan lead yang sudah dihubungi",
            "detail": f"Periksa balasan dari: {nama}. Yang membalas → ubah status ke 'menunggu' atau 'setuju'. Yang belum membalas 2 hari → kirim follow-up sekali.",
            "lead": [l["id"] for l in dihubungi[:3]],
        })
    else:
        aksi.append({
            "judul": "Perbarui status leads",
            "detail": "Tidak ada lead 'dihubungi'/'setuju' hari ini. Setelah outreach, segera ubah status lead di tab Leads agar rencana besok akurat.",
            "lead": [],
        })
    ringkas = {s: len(by_status[s]) for s in STATUS_LEAD}
    belum_verif = sum(1 for l in leads if not l.get("terverifikasi"))
    return {"tanggal": str(date.today()), "ringkasan": ringkas,
            "belum_terverifikasi": belum_verif, "total": len(leads), "aksi": aksi[:3]}


@app.get("/api/health")
def health():
    return {"ok": True, "mode": mode_ai(), "model": MODEL,
            "leads": len(load_leads())}


# ---------------------------------------------------------------- UI (HTML sederhana)
HTML = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Penjualan Podcast Meong</title>
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:900px;margin:0 auto;padding:16px;background:#faf8f5;color:#3b3631}
h1{font-size:22px;margin:0 0 4px}.sub{color:#7a6f66;margin:0 0 16px}
.badge{display:inline-block;padding:2px 10px;border-radius:999px;background:#f6e9df;color:#a8643f;font-size:12px;border:1px solid #e7e0d6}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}
.tabs button{padding:8px 14px;border-radius:999px;border:1px solid #e7e0d6;background:#fff;cursor:pointer;color:#3b3631}
.tabs button.on{background:#c07a54;color:#fff;border-color:#c07a54}
.card{background:#fff;border:1px solid #e7e0d6;border-radius:12px;padding:16px;margin-bottom:16px}
input,select,textarea{width:100%;padding:8px;border:1px solid #e7e0d6;border-radius:8px;margin:4px 0 10px;box-sizing:border-box;font:inherit}
button.go{background:#c07a54;color:#fff;border:0;padding:9px 18px;border-radius:999px;cursor:pointer}
button.ghost{background:#fff;border:1px solid #e7e0d6;padding:6px 12px;border-radius:999px;cursor:pointer}
pre{white-space:pre-wrap;background:#faf8f5;border:1px solid #e7e0d6;border-radius:8px;padding:12px}
#chatlog{height:280px;overflow:auto;border:1px solid #e7e0d6;border-radius:8px;padding:10px;background:#fff;margin-bottom:10px}
.msg{margin:6px 0}.msg b{color:#a8643f}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{border-bottom:1px solid #eee;padding:6px 4px;text-align:left;vertical-align:top}
.warn{background:#fff4e5;border:1px solid #f0dfc2;border-radius:8px;padding:10px;font-size:13px;margin-bottom:12px}
label{font-size:13px;font-weight:600}
</style>
</head>
<body>
<h1>🐱 Agent Penjualan Podcast Meong</h1>
<p class="sub">Jualan · promosi · pemasaran · cari customer — <span class="badge" id="mode">memuat…</span></p>
<div class="warn">⚠️ Semua kontak lead di sini <b>belum terverifikasi</b> (dari pencarian web 17 Nov 2026). Verifikasi dulu (buka IG/TikTok/Shopee toko, pastikan masih aktif) sebelum menghubungi. Jangan janjikan views/viral — yang dijual hanya video + naskah + 1x revisi.</div>
<div class="tabs">
  <button class="on" onclick="show('chat')">💬 Chat Penjualan</button>
  <button onclick="show('gen')">✍️ Generator Promosi</button>
  <button onclick="show('leads')">📋 Leads</button>
  <button onclick="show('rencana')">📅 Rencana Harian</button>
</div>

<div id="tab-chat" class="card">
  <div id="chatlog"><div class="msg"><b>Agent:</b> Halo Kak! Saya Asisten Penjualan Podcast Meong. Tanya harga paket, video contoh, atau cara pesan — saya bantu. 😊</div></div>
  <input id="chatinput" placeholder="Tulis pertanyaan calon pembeli…" onkeydown="if(event.key==='Enter')kirimChat()">
  <button class="go" onclick="kirimChat()">Kirim</button>
</div>

<div id="tab-gen" class="card" style="display:none">
  <label>Jenis</label>
  <select id="g-jenis">
    <option value="caption_tiktok">Caption TikTok</option>
    <option value="caption_ig">Caption Instagram</option>
    <option value="caption_yt">Caption YouTube</option>
    <option value="wa_outreach">Pesan WhatsApp — penawaran pertama</option>
    <option value="wa_followup">Pesan WhatsApp — follow-up</option>
    <option value="dm_ig">DM Instagram</option>
    <option value="email">Email penawaran</option>
  </select>
  <label>Nama toko / bisnis</label><input id="g-toko" placeholder="cth: Deku Petshop and Clinic">
  <label>Produk yang dipromosikan</label><input id="g-produk" placeholder="cth: makanan kucing / jasa grooming">
  <label>Paket</label>
  <select id="g-paket"><option value="15">Sederhana — 15 detik Rp75.000</option><option value="30" selected>Standar — 30 detik Rp150.000</option><option value="60">Storytelling — 60 detik Rp250.000</option></select>
  <button class="go" onclick="buatPromo()">Buat</button>
  <button class="ghost" onclick="salinHasil()">Salin hasil</button>
  <pre id="g-hasil">Hasil akan muncul di sini.</pre>
</div>

<div id="tab-leads" class="card" style="display:none">
  <div id="lead-summary"></div>
  <table><thead><tr><th>Nama</th><th>Kontak</th><th>Status</th><th>Terverifikasi</th><th></th></tr></thead><tbody id="lead-rows"></tbody></table>
  <h3>Tambah lead</h3>
  <label>Nama bisnis</label><input id="l-nama">
  <label>Kontak (IG/WA/telp/Shopee)</label><input id="l-kontak">
  <label>Alamat / platform</label><input id="l-alamat">
  <label>Jenis</label><select id="l-jenis"><option>pet shop</option><option>toko online</option><option>bisnis lain</option></select>
  <label>Catatan</label><input id="l-catatan">
  <button class="go" onclick="tambahLead()">Tambah lead</button>
</div>

<div id="tab-rencana" class="card" style="display:none">
  <button class="go" onclick="muatRencana()">Tampilkan rencana hari ini</button>
  <div id="rencana"></div>
</div>

<script>
async function api(path, opts){ const r = await fetch(path, opts); if(!r.ok){ const e = await r.json().catch(()=>({})); throw new Error(e.detail || r.status); } return r.json(); }
function show(tab){ ['chat','gen','leads','rencana'].forEach(t=>{ document.getElementById('tab-'+t).style.display = t===tab ? '' : 'none'; }); document.querySelectorAll('.tabs button').forEach((b,i)=>b.classList.toggle('on', ['chat','gen','leads','rencana'][i]===tab)); if(tab==='leads') muatLeads(); if(tab==='rencana') muatRencana(); }
async function kirimChat(){ const inp = document.getElementById('chatinput'); const v = inp.value.trim(); if(!v) return; const log = document.getElementById('chatlog'); log.innerHTML += `<div class="msg"><b>Anda:</b> ${v}</div>`; inp.value=''; try{ const d = await api('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})}); log.innerHTML += `<div class="msg"><b>Agent:</b> ${d.reply.replace(/\n/g,'<br>')}</div><div class="msg" style="font-size:11px;color:#999">mode: ${d.mode}</div>`; }catch(e){ log.innerHTML += `<div class="msg"><b>Agent:</b> Maaf, terjadi kesalahan: ${e.message}</div>`; } log.scrollTop = log.scrollHeight; }
async function buatPromo(){ const body = {jenis:document.getElementById('g-jenis').value, nama_toko:document.getElementById('g-toko').value, produk:document.getElementById('g-produk').value, paket:document.getElementById('g-paket').value}; try{ const d = await api('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); document.getElementById('g-hasil').textContent = d.hasil + `\n\n[mode: ${d.mode}]`; }catch(e){ document.getElementById('g-hasil').textContent = 'Gagal: ' + e.message; } }
function salinHasil(){ navigator.clipboard.writeText(document.getElementById('g-hasil').textContent); alert('Disalin.'); }
async function muatLeads(){ const d = await api('/api/leads'); const s = {}; d.leads.forEach(l=>s[l.status]=(s[l.status]||0)+1); document.getElementById('lead-summary').innerHTML = `<p>Total <b>${d.leads.length}</b> lead — ` + Object.entries(s).map(([k,v])=>`${k}: ${v}`).join(' · ') + ` — belum terverifikasi: <b>${d.leads.filter(l=>!l.terverifikasi).length}</b></p>`;
  document.getElementById('lead-rows').innerHTML = d.leads.map(l=>`<tr><td><b>${l.nama}</b><br><small>${l.jenis} · ${l.alamat||''}</small></td><td>${l.kontak||'-'}<br><small>${l.catatan||''}</small></td><td><select onchange="ubahStatus('${l.id}',this.value)">${['baru','dihubungi','menunggu','setuju','tolak'].map(x=>`<option ${x===l.status?'selected':''}>${x}</option>`).join('')}</select></td><td><input type="checkbox" ${l.terverifikasi?'checked':''} onchange="ubahVerif('${l.id}',this.checked)"> ${l.terverifikasi?'Ya':'Belum'}</td><td><button class="ghost" onclick="hapusLead('${l.id}')">Hapus</button></td></tr>`).join(''); }
async function ubahStatus(id, st){ const d = await api('/api/leads'); const l = d.leads.find(x=>x.id===id); await api('/api/leads/'+id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({...l, status:st})}); muatLeads(); }
async function ubahVerif(id, v){ const d = await api('/api/leads'); const l = d.leads.find(x=>x.id===id); await api('/api/leads/'+id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({...l, terverifikasi:v})}); muatLeads(); }
async function hapusLead(id){ if(!confirm('Hapus lead ini?')) return; await api('/api/leads/'+id,{method:'DELETE'}); muatLeads(); }
async function tambahLead(){ const body = {nama:document.getElementById('l-nama').value, kontak:document.getElementById('l-kontak').value, alamat:document.getElementById('l-alamat').value, jenis:document.getElementById('l-jenis').value, catatan:document.getElementById('l-catatan').value, status:'baru', terverifikasi:false}; try{ await api('/api/leads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); muatLeads(); }catch(e){ alert('Gagal: '+e.message); } }
async function muatRencana(){ const d = await api('/api/rencana'); document.getElementById('rencana').innerHTML = `<p><b>${d.tanggal}</b> — total ${d.total} lead · belum terverifikasi ${d.belum_terverifikasi} · ` + Object.entries(d.ringkasan).map(([k,v])=>`${k}: ${v}`).join(' · ') + `</p>` + d.aksi.map((a,i)=>`<div class="card"><b>${i+1}. ${a.judul}</b><p>${a.detail}</p></div>`).join(''); }
fetch('/api/health').then(r=>r.json()).then(d=>{ document.getElementById('mode').textContent = d.mode==='gemini' ? 'Mode AI Gemini aktif' : 'Mode template (isi GEMINI_API_KEY untuk AI penuh)'; });
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
