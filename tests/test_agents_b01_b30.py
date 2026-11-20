# ======================================================================
# Unit test 30 Agent Bintang (b01..b30) — Pusat Komando.
#
# Jalankan dari folder pusat-komando/ dengan venv pengujian:
#   env -i PATH="$PATH" HOME="$HOME" ~/workspace/tmp/venv-pk/bin/python \
#     -m unittest discover -s tests -v
# (env bersih diperlukan karena gradio gagal impor bila variabel proxy
# VM ini terbaca.)
# Semua test tanpa panggilan jaringan (mode template; tanpa GEMINI_API_KEY).
# ======================================================================
import importlib
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("PK_NO_LOG", "1")  # tes modul B tidak menulis log aktivitas nyata

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
sys.path.insert(0, str(AGENTS))
sys.path.insert(0, str(ROOT))

EXPECTED = [{'kode': 'A01', 'file': 'b01_ceo_director.py', 'nama': 'CEO Director', 'divisi': 'Direksi', 'atasan': 'Pemilik', 'job': 'Menentukan arah, target, prioritas dan keputusan perusahaan', 'peta': 'Muse (koordinator / CEO)', 'status': 'Aktif', 'gdiv': 'Agent 0 — Chief Orchestrator', 'gperan': '0 — Chief Orchestrator', 'kpi': ['Semua agen aktif setiap hari (target rancangan)', '1 produk baru dirilis setiap hari (target rancangan)', 'Laporan harian tepat waktu (target rancangan)'], 'tools': ['Gemini Advanced / ChatGPT', 'Notion', 'Google Sheets'], 'contoh': 'buat_arahan([{"judul": "Selesaikan halaman demo #18", "prioritas": "P2", "penanggung_jawab": "A14", "status": "Dikerjakan"}])', 'keys': ['prioritas', 'keputusan_butuh_persetujuan'], 'checks': []}, {'kode': 'A02', 'file': 'b02_coo_manager.py', 'nama': 'COO Manager', 'divisi': 'Direksi', 'atasan': 'A01', 'job': 'Mengatur operasi, kapasitas, jadwal dan koordinasi divisi', 'peta': 'Muse + koordinasi.py', 'status': 'Aktif sebagian', 'gdiv': 'Agent 0 — Chief Orchestrator', 'gperan': '0 — Chief Orchestrator (dukungan operasional)', 'kpi': ['Semua agen aktif setiap hari (target rancangan)'], 'tools': ['Gemini Advanced / ChatGPT', 'Notion', 'Google Sheets'], 'contoh': 'susun_jadwal([{"judul": "Riset tren", "penanggung_jawab": "A06"}, {"judul": "Produksi video", "penanggung_jawab": "A11"}])', 'keys': ['jadwal'], 'checks': []}, {'kode': 'A03', 'file': 'b03_command_controller.py', 'nama': 'Command Controller', 'divisi': 'Direksi', 'atasan': 'A02', 'job': 'Membagi tugas, melacak status dan mengonsolidasikan laporan', 'peta': 'Pusat Komando (Faable) + koordinasi.py', 'status': 'Aktif', 'gdiv': 'Agent 0 — Chief Orchestrator', 'gperan': '0 — Chief Orchestrator (pembagian tugas)', 'kpi': ['Semua agen aktif setiap hari (target rancangan)', 'Laporan harian tepat waktu (target rancangan)'], 'tools': ['Gemini Advanced / ChatGPT', 'Notion', 'Google Sheets'], 'contoh': 'bagi_tugas("Buat draf proposal Upwork", "A28")', 'keys': ['penanggung_jawab'], 'checks': [('penanggung_jawab', 'A28')]}, {'kode': 'A04', 'file': 'b04_quality_control.py', 'nama': 'Quality Control', 'divisi': 'Direksi', 'atasan': 'A02', 'job': 'Memeriksa akurasi, kualitas dan kepatuhan hasil', 'peta': 'Muse + A9F verifikasi', 'status': 'Aktif', 'gdiv': 'Agent 0 — Chief Orchestrator', 'gperan': 'Bagian dari Agent 0 — QC melekat pada orchestrator', 'kpi': [], 'tools': [], 'contoh': 'periksa_draf("Halo Kak, saya Masduki dari Podcast Meong. Jasa video promo 15 detik Rp75.000.")', 'keys': ['layak', 'masalah', 'verdict'], 'checks': [('layak', True)]}, {'kode': 'A05', 'file': 'b05_business_analyst.py', 'nama': 'Business Analyst', 'divisi': 'Direksi', 'atasan': 'A02', 'job': 'Menganalisis KPI, hasil, risiko dan profitabilitas', 'peta': 'A7 Keuangan + Muse', 'status': 'Aktif', 'gdiv': 'Divisi 5 — Freelance & Finance', 'gperan': '5B — Finance & Operational Controller (analisis)', 'kpi': ['Laporan pembukuan harian/mingguan (target rancangan)'], 'tools': ['Google Sheets', 'Notion'], 'contoh': 'hitung_laba(29000, 0)', 'keys': ['laba_bersih'], 'checks': [('laba_bersih', 29000.0)]}, {'kode': 'A06', 'file': 'b06_market_researcher.py', 'nama': 'Market Researcher', 'divisi': 'Riset', 'atasan': 'A03', 'job': 'Meneliti kebutuhan, masalah dan segmen pelanggan', 'peta': 'A10 Riset', 'status': 'Aktif', 'gdiv': 'Divisi 1 — R&D', 'gperan': '1A — Market Researcher', 'kpi': ['5 ide produk valid/hari (target rancangan)'], 'tools': ['Google Trends', 'Perplexity.ai', 'Gemini Deep Research'], 'contoh': 'buat_brief_riset("eBook anak", "Anak bosan baca", "Orang tua anak 5–10 tahun")', 'keys': ['niche', 'masalah_customer'], 'checks': []}, {'kode': 'A07', 'file': 'b07_trend_hunter.py', 'nama': 'Trend Hunter', 'divisi': 'Riset', 'atasan': 'A03', 'job': 'Memantau tren, topik dan permintaan pasar', 'peta': 'A10 Riset', 'status': 'Aktif', 'gdiv': 'Divisi 1 — R&D', 'gperan': '1A — Market Researcher (tren)', 'kpi': ['5 tren produk/hari (target rancangan)'], 'tools': ['Google Trends', 'Perplexity.ai', 'Gemini Deep Research'], 'contoh': 'catat_tren("Video kucing memasak", "TikTok", "Banyak yang menonton video masak kucing")', 'keys': ['topik', 'sumber', 'status_validasi'], 'checks': []}, {'kode': 'A08', 'file': 'b08_product_developer.py', 'nama': 'Product Developer', 'divisi': 'Riset', 'atasan': 'A03', 'job': 'Mengubah kebutuhan tervalidasi menjadi konsep dan produk', 'peta': 'A5 Produksi + A9', 'status': 'Aktif', 'gdiv': 'Divisi 1 — R&D', 'gperan': '1A — Market Researcher (pengembangan konsep)', 'kpi': ['5 ide produk valid/hari (target rancangan)'], 'tools': ['Google Trends', 'Perplexity.ai', 'Gemini Deep Research'], 'contoh': 'buat_konsep_produk("eBook Resep Kucing", "Pemilik kucing bingung masak", "Pemilik kucing", "Resep dari sudut pandang Oyen", 29000, "belum cukup data", "TikTok + Instagram")', 'keys': ['lengkap', 'yang_kurang'], 'checks': [('lengkap', False)]}, {'kode': 'A09', 'file': 'b09_competitor_analyst.py', 'nama': 'Competitor Analyst', 'divisi': 'Riset', 'atasan': 'A06', 'job': 'Menganalisis pesaing, penawaran, harga dan celah pasar', 'peta': 'A10 Riset', 'status': 'Aktif', 'gdiv': 'Divisi 1 — R&D', 'gperan': '1B — Competition & Grant Scout', 'kpi': ['3 info lomba baru/hari (target rancangan)', '5–10 lomba diikuti/bulan (target rancangan)'], 'tools': ['Google Search', 'Gemini Deep Research', 'Email Alerts'], 'contoh': 'bandingkan_harga("Jasa video promo 15 dtk", 75000, 150000, "Studio X")', 'keys': ['selisih', 'kesimpulan'], 'checks': [('selisih', -75000.0)]}, {'kode': 'A10', 'file': 'b10_product_validator.py', 'nama': 'Product Validator', 'divisi': 'Riset', 'atasan': 'A08', 'job': 'Menguji manfaat, kelayakan, permintaan dan kesiapan produk', 'peta': 'A9F verifikasi + Muse', 'status': 'Aktif', 'gdiv': 'Divisi 1 — R&D', 'gperan': '1A — Market Researcher (validasi)', 'kpi': ['5 ide produk valid/hari (target rancangan)'], 'tools': ['Google Trends', 'Perplexity.ai', 'Gemini Deep Research'], 'contoh': 'cek_kelayakan_produk({"nama": "eBook Resep Kucing", "masalah_customer": "x", "target_customer": "y", "keunikan": "z", "harga_rp": 29000, "bukti_minat_pasar": "belum cukup data", "rencana_promosi_distribusi": "TikTok"})', 'keys': ['skor', 'verdict'], 'checks': [('skor', 10)]}, {'kode': 'A11', 'file': 'b11_ai_video_producer.py', 'nama': 'AI Video Producer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat naskah, storyboard dan video AI', 'peta': 'A5 Produksi + A11/A12 pitch', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2B — Visual & AI Media Producer (video)', 'kpi': ['5–10 aset visual/hari, termasuk video AI (target rancangan)'], 'tools': ['Kling AI', 'Hailuo AI', 'CapCut Desktop'], 'contoh': 'buat_naskah_video("Oyen Masak Nasi Goreng", "Oyen & Momo memasak")', 'keys': ['klip', 'aturan_kualitas'], 'checks': []}, {'kode': 'A12', 'file': 'b12_ai_image_designer.py', 'nama': 'AI Image Designer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat visual, foto, ilustrasi dan aset desain AI', 'peta': 'A5 Produksi', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2B — Visual & AI Media Producer', 'kpi': ['5–10 aset visual/hari (target rancangan)'], 'tools': ['Bing Image Creator', 'Leonardo.ai', 'Flux (HuggingFace)'], 'contoh': 'buat_brief_visual("ilustrasi eBook", "Oyen menjaga kolam ikan")', 'keys': ['prompt_gambar_draf'], 'checks': []}, {'kode': 'A13', 'file': 'b13_app_developer.py', 'nama': 'App Developer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat prototipe dan aplikasi', 'peta': 'A9 + tim 9A–9F', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2C — Web, App & Micro-Game Developer', 'kpi': ['1 tools/game/landing page per minggu (target rancangan)'], 'tools': ['Gemini / ChatGPT / Claude', 'VS Code', 'GitHub'], 'contoh': 'buat_spesifikasi_aplikasi("Kasir Warung", "Kasir sederhana untuk warung", ["Tambah produk", "Transaksi", "Laporan harian"])', 'keys': ['level', 'standar_level_3'], 'checks': [('level', 3)]}, {'kode': 'A14', 'file': 'b14_web_developer.py', 'nama': 'Web Developer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat website, landing page dan katalog', 'peta': 'A9 + Muse', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2C — Web, App & Micro-Game Developer', 'kpi': ['1 tools/game/landing page per minggu (target rancangan)'], 'tools': ['Gemini / ChatGPT / Claude', 'VS Code', 'GitHub'], 'contoh': 'buat_spesifikasi_website("Toko Kue Bu Sari", "Toko online sederhana", ["Beranda", "Katalog", "Kontak"])', 'keys': ['harga_paket_jasa'], 'checks': []}, {'kode': 'A15', 'file': 'b15_pod_designer.py', 'nama': 'POD Designer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat desain produk print-on-demand', 'peta': 'A5 Produksi', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2B — Visual & AI Media Producer (POD)', 'kpi': ['5–10 aset visual/hari (target rancangan)'], 'tools': ['Bing Image Creator', 'Leonardo.ai'], 'contoh': 'buat_brief_pod("Kaos", "Oyen tertawa")', 'keys': ['platform'], 'checks': []}, {'kode': 'A16', 'file': 'b16_ebook_publisher.py', 'nama': 'eBook Publisher', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Menulis, menyunting dan menyiapkan eBook', 'peta': 'A5 Produksi', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2A — Literary & Content Writer', 'kpi': ['1 bab cerbung / 1 puisi-cerpen / 1 draf eBook per hari (target rancangan)'], 'tools': ['Gemini / ChatGPT', 'Google Docs'], 'contoh': 'buat_kerangka_ebook("Si Oyen Penjaga Kolam Ikan", "Cerita kucing untuk anak")', 'keys': ['bab'], 'checks': []}, {'kode': 'A17', 'file': 'b17_creative_writer.py', 'nama': 'Creative Writer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Membuat puisi, cerpen dan cerita bersambung', 'peta': 'A5 Produksi', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2A — Literary & Content Writer', 'kpi': ['1 bab cerbung / 1 puisi-cerpen / 1 draf eBook per hari (target rancangan)'], 'tools': ['Gemini / ChatGPT', 'Google Docs'], 'contoh': 'buat_kerangka_cerita("cerpen", "Oyen dan Ikan yang Hilang", "Persahabatan")', 'keys': ['standar'], 'checks': [('standar', '~800 kata')]}, {'kode': 'A18', 'file': 'b18_game_developer.py', 'nama': 'Game Developer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Merancang dan mengembangkan game', 'peta': 'A9 Produksi Game', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2C — Web, App & Micro-Game Developer', 'kpi': ['1 tools/game/landing page per minggu (target rancangan)'], 'tools': ['Gemini / ChatGPT / Claude', 'VS Code', 'GitHub'], 'contoh': 'buat_konsep_game("Oyen Tangkap Ikan 2", "Arcade", "Anak-anak")', 'keys': ['level_maks'], 'checks': [('level_maks', 3)]}, {'kode': 'A19', 'file': 'b19_content_producer.py', 'nama': 'Content Producer', 'divisi': 'Produksi', 'atasan': 'A08', 'job': 'Mengubah produk dan riset menjadi materi konten', 'peta': 'A5 Produksi + A3', 'status': 'Aktif', 'gdiv': 'Divisi 2 — Creative Studio', 'gperan': '2A/2B + Divisi 3 (content producer)', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', '1 produk → 7 format konten (strategi rancangan)'], 'tools': ['Gemini / ChatGPT', 'CapCut'], 'contoh': 'buat_paket_konten("eBook Kolam Ikan", ["Instagram", "TikTok"])', 'keys': ['format_7'], 'checks': []}, {'kode': 'A20', 'file': 'b20_instagram_manager.py', 'nama': 'Instagram Manager', 'divisi': 'Marketing', 'atasan': 'A03', 'job': 'Mengelola dua akun Instagram, konten dan interaksi', 'peta': 'A3 Pertumbuhan (IG @meongcast terhubung; @podcast_meong login ditolak)', 'status': 'Aktif', 'gdiv': 'Divisi 3 — Social Growth', 'gperan': '3 — Multi-Channel Publisher & Growth Hacker', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', 'Target +20% followers/bulan (target rancangan)', '1 produk → 7 format konten (strategi rancangan)', 'CTA ke Lynk.id / KaryaKarsa / Saweria / Trakteer'], 'tools': ['Gemini / ChatGPT', 'CapCut'], 'contoh': 'buat_draf_posting("eBook Kolam Ikan", "Reels")', 'keys': ['hashtag', 'cta'], 'checks': []}, {'kode': 'A21', 'file': 'b21_tiktok_manager.py', 'nama': 'TikTok Manager', 'divisi': 'Marketing', 'atasan': 'A03', 'job': 'Mengelola dua akun TikTok dan analitik', 'peta': 'A3 Pertumbuhan (TikTok @podcast_kucing jalan; @meongcast butuh login Cipta)', 'status': 'Aktif sebagian', 'gdiv': 'Divisi 3 — Social Growth', 'gperan': '3 — Multi-Channel Publisher & Growth Hacker', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', 'Target +20% followers/bulan (target rancangan)', '1 produk → 7 format konten (strategi rancangan)', 'CTA ke Lynk.id / KaryaKarsa / Saweria / Trakteer'], 'tools': ['Gemini / ChatGPT', 'CapCut'], 'contoh': 'buat_draf_posting("Jasa Video Promo", "Video pendek")', 'keys': ['hashtag'], 'checks': []}, {'kode': 'A22', 'file': 'b22_youtube_manager.py', 'nama': 'YouTube Manager', 'divisi': 'Marketing', 'atasan': 'A03', 'job': 'Mengelola dua channel YouTube dan analitik', 'peta': 'A3 Pertumbuhan (YT Podcast meong jalan; @meongcast tertahan verifikasi)', 'status': 'Aktif sebagian', 'gdiv': 'Divisi 3 — Social Growth', 'gperan': '3 — Multi-Channel Publisher & Growth Hacker', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', 'Target +20% followers/bulan (target rancangan)', '1 produk → 7 format konten (strategi rancangan)', 'CTA ke Lynk.id / KaryaKarsa / Saweria / Trakteer'], 'tools': ['Gemini / ChatGPT', 'CapCut'], 'contoh': 'buat_draf_video("Oyen Masak Nasi Goreng", "Shorts")', 'keys': ['tag'], 'checks': []}, {'kode': 'A23', 'file': 'b23_threads_manager.py', 'nama': 'Threads Manager', 'divisi': 'Marketing', 'atasan': 'A03', 'job': 'Mengelola satu akun Threads dan percakapan', 'peta': 'A3 Pertumbuhan (Threads @ciptabintanglestari terhubung)', 'status': 'Aktif', 'gdiv': 'Divisi 3 — Social Growth', 'gperan': '3 — Multi-Channel Publisher & Growth Hacker', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', 'Target +20% followers/bulan (target rancangan)', '1 produk → 7 format konten (strategi rancangan)', 'CTA ke Lynk.id / KaryaKarsa / Saweria / Trakteer'], 'tools': ['Gemini / ChatGPT', 'CapCut'], 'contoh': 'buat_draf_threads("eBook Kolam Ikan")', 'keys': ['utas'], 'checks': []}, {'kode': 'A24', 'file': 'b24_seo_growth.py', 'nama': 'SEO & Growth', 'divisi': 'Marketing', 'atasan': 'A03', 'job': 'SEO, optimasi distribusi dan pertumbuhan organik', 'peta': 'A3 Pertumbuhan', 'status': 'Aktif', 'gdiv': 'Divisi 3 — Social Growth', 'gperan': '3 — Multi-Channel Publisher & Growth Hacker (SEO)', 'kpi': ['3–5 konten terbit/hari di seluruh kanal (target rancangan)', 'Target +20% followers/bulan (target rancangan)'], 'tools': ['Google Trends', 'Perplexity.ai'], 'contoh': 'buat_daftar_kata_kunci("kasir toko")', 'keys': ['kata_kunci'], 'checks': []}, {'kode': 'A25', 'file': 'b25_sales_manager.py', 'nama': 'Sales Manager', 'divisi': 'Penjualan', 'atasan': 'A02', 'job': 'Mengelola pipeline, penawaran dan target penjualan', 'peta': 'A2 + A4 Penjualan', 'status': 'Aktif', 'gdiv': 'Divisi 4 — CS & Closer', 'gperan': '4 — Omnichannel CS & Closer', 'kpi': ['Respons < 1 jam (target rancangan)', '1–3 penjualan langsung (closing)/hari (target rancangan)', 'Pembayaran hanya ke BCA / PayPal / KaryaKarsa / Lynk.id / Saweria / Trakteer — JANGAN ke Mayar sampai KYC selesai'], 'tools': [], 'contoh': 'buat_draf_penawaran("Paws & Claws", "video", "toko pet shop ramai di Instagram")', 'keys': ['teks'], 'checks': []}, {'kode': 'A26', 'file': 'b26_customer_service.py', 'nama': 'Customer Service', 'divisi': 'Penjualan', 'atasan': 'A25', 'job': 'Menjawab pertanyaan, komentar dan keluhan pelanggan', 'peta': 'A1 + A13 (WA Web rusak; IG/Threads Messages terhubung)', 'status': 'Aktif', 'gdiv': 'Divisi 4 — CS & Closer', 'gperan': '4 — Omnichannel CS & Closer', 'kpi': ['Respons < 1 jam (target rancangan)'], 'tools': [], 'contoh': 'buat_draf_balasan("Berapa harga video promonya?", "harga")', 'keys': ['balasan_draf'], 'checks': []}, {'kode': 'A27', 'file': 'b27_email_administrator.py', 'nama': 'Email Administrator', 'divisi': 'Penjualan', 'atasan': 'A02', 'job': 'Memilah email, membuat draft dan menindaklanjuti', 'peta': 'A13 Email (Gmail TIDAK terhubung — baca via browser)', 'status': 'Aktif sebagian', 'gdiv': 'Divisi 4 — CS & Closer', 'gperan': '4 — Omnichannel CS & Closer (email)', 'kpi': ['Respons < 1 jam (target rancangan)', 'Email diperiksa 2–3 kali/hari (target rancangan)'], 'tools': [], 'contoh': 'buat_draf_triase({"pengirim_email": "toko@example.com", "subjek": "Tanya harga video promo", "isi": "Berapa harga video 15 detik?"})', 'keys': ['kategori'], 'checks': []}, {'kode': 'A28', 'file': 'b28_opportunity_hunter.py', 'nama': 'Opportunity Hunter', 'divisi': 'Peluang & Keuangan', 'atasan': 'A02', 'job': 'Mencari lomba, freelance, hibah dan kemitraan', 'peta': 'A6 + A14', 'status': 'Aktif', 'gdiv': 'Divisi 5 — Freelance & Finance', 'gperan': '5A — Freelance & Gig Bidder', 'kpi': ['5 proposal/hari — DRAF saja, kirim hanya setelah Cipta setuju (target rancangan)', 'Target 1–2 proyek didapat/bulan (target rancangan)'], 'tools': [], 'contoh': 'nilai_peluang_draf("Lomba video AI gratis, boleh AI, hadiah Rp1.000.000, pendaftaran sampai 31 Desember 2026, terbuka untuk umum di Indonesia.", "Lomba Video AI")', 'keys': ['penilaian'], 'checks': []}, {'kode': 'A29', 'file': 'b29_finance_manager.py', 'nama': 'Finance Manager', 'divisi': 'Peluang & Keuangan', 'atasan': 'A02', 'job': 'Mencatat pendapatan, biaya, saldo dan laporan', 'peta': 'A7 Keuangan (baseline Rp0)', 'status': 'Aktif', 'gdiv': 'Divisi 5 — Freelance & Finance', 'gperan': '5B — Finance & Operational Controller', 'kpi': ['Laporan pembukuan harian/mingguan (target rancangan)', 'Pantau status KYC Mayar'], 'tools': ['Google Sheets', 'Notion'], 'contoh': 'format_laporan(29000, 0)', 'keys': ['laba_rp'], 'checks': [('laba_rp', 29000.0)]}, {'kode': 'A30', 'file': 'b30_operations_manager.py', 'nama': 'Operations Manager', 'divisi': 'Peluang & Keuangan', 'atasan': 'A02', 'job': 'Mengelola dokumen, SOP, jadwal dan administrasi', 'peta': 'koordinasi.py + Pusat Komando', 'status': 'Aktif', 'gdiv': 'Agent 0 — Chief Orchestrator', 'gperan': 'Agent 0 — Chief Orchestrator (dukungan operasional; Gemini #1 tidak punya divisi operasional terpisah)', 'kpi': [], 'tools': [], 'contoh': 'buat_kerangka_sop("Upload video harian", ["Periksa naskah", "Generate klip", "Cek pitch", "Minta persetujuan Cipta", "Upload"])', 'keys': ['langkah'], 'checks': []}]

MODUL = {}
for _e in EXPECTED:
    MODUL[_e["kode"]] = importlib.import_module(_e["file"][:-3])


class TestMetadata(unittest.TestCase):
    def test_jumlah_30_dan_kode_unik(self):
        self.assertEqual(len(EXPECTED), 30)
        self.assertEqual(len({e["kode"] for e in EXPECTED}), 30)
        self.assertEqual({e["kode"] for e in EXPECTED},
                         {"A%02d" % i for i in range(1, 31)})

    def test_metadata_sesuai_roster(self):
        for e in EXPECTED:
            m = MODUL[e["kode"]]
            self.assertEqual(m.KODE, e["kode"])
            self.assertEqual(m.NAMA, e["nama"])
            self.assertEqual(m.DIVISI, e["divisi"])
            self.assertEqual(m.ATASAN, e["atasan"])
            self.assertEqual(m.JOB_DESC, e["job"])
            self.assertEqual(m.DIPETAKAN_KE, e["peta"])
            self.assertEqual(m.STATUS, e["status"])
            self.assertIn(m.STATUS, ("Aktif", "Aktif sebagian"))
            i = m.info()
            self.assertEqual(i["kode"], e["kode"])
            self.assertTrue(i["pasif"])
            self.assertEqual(i["gemini_divisi"], e["gdiv"])
            self.assertEqual(i["gemini_peran"], e["gperan"])
            self.assertEqual(i["gemini_kpi"], e["kpi"])
            self.assertEqual(i["gemini_tools"], e["tools"])

    def test_pembagian_6_kelompok(self):
        kelompok = {}
        for e in EXPECTED:
            kelompok.setdefault(e["divisi"], []).append(e["kode"])
        self.assertEqual({k: len(v) for k, v in kelompok.items()},
                         {"Direksi": 5, "Riset": 5, "Produksi": 9,
                          "Marketing": 5, "Penjualan": 3,
                          "Peluang & Keuangan": 3})

    def test_status_nyata(self):
        sebagian = {e["kode"] for e in EXPECTED if e["status"] == "Aktif sebagian"}
        self.assertEqual(sebagian, {"A02", "A21", "A22", "A27"})
        self.assertEqual(sum(1 for e in EXPECTED if e["status"] == "Aktif"), 26)


class TestGeminiMapping(unittest.TestCase):
    def test_a01_master_prompt(self):
        m = MODUL["A01"]
        self.assertIn("CHIEF ORCHESTRATOR", m.MASTER_PROMPT_GEMINI)
        self.assertIn("5 divisi", m.MASTER_PROMPT_GEMINI)
        self.assertIn("Mayar masih proses KYC", m.MASTER_PROMPT_GEMINI)
        self.assertIn("6 Divisi", m.CATATAN_GEMINI_DIVISI)
        self.assertIn("5 divisi", m.CATATAN_GEMINI_DIVISI)

    def test_rencana_30_hari_a01_a03(self):
        for kode in ("A01", "A03"):
            r = MODUL[kode].rencana_30_hari()
            self.assertEqual(len(r["fase"]), 5)
            self.assertEqual([f["hari"] for f in r["fase"]],
                             ["1–3", "4–7", "8–14", "15–21", "22–30"])
            self.assertEqual(r["target_30_hari"]["produk_digital_selesai"], 15)
            self.assertEqual(r["target_30_hari"]["konten_terbit"], 30)
            self.assertEqual(r["target_30_hari"]["followers_baru"], 1000)
            self.assertIn("pemuatan pertama", r["catatan_jujur"])
            self.assertIn("TARGET RANCANGAN", r["catatan_jujur"])

    def test_jadwal_harian_a03(self):
        j = MODUL["A03"].jadwal_harian()
        jam = [s["jam"] for s in j["jadwal"]]
        self.assertEqual(jam, ["06.00", "08.00", "11.00, 15.00, 19.00",
                               "Sepanjang hari", "21.00"])
        self.assertIn("Bukan jadwal otomatis", j["catatan_jujur"])

    def test_kpi_gemini_divisi(self):
        self.assertIn("5 ide produk valid/hari (target rancangan)",
                      MODUL["A06"].GEMINI_KPI)
        self.assertIn("3 info lomba baru/hari (target rancangan)",
                      MODUL["A09"].GEMINI_KPI)
        self.assertIn("5–10 aset visual/hari (target rancangan)",
                      MODUL["A12"].GEMINI_KPI)
        self.assertIn("1 tools/game/landing page per minggu (target rancangan)",
                      MODUL["A13"].GEMINI_KPI)
        self.assertIn("Target +20% followers/bulan (target rancangan)",
                      MODUL["A20"].GEMINI_KPI)
        self.assertIn("Respons < 1 jam (target rancangan)",
                      MODUL["A26"].GEMINI_KPI)
        self.assertTrue(any("JANGAN ke Mayar" in k for k in MODUL["A25"].GEMINI_KPI))
        self.assertTrue(any("DRAF saja" in k for k in MODUL["A28"].GEMINI_KPI))
        self.assertIn("Google Trends", MODUL["A06"].GEMINI_TOOLS)
        self.assertIn("Kling AI", MODUL["A11"].GEMINI_TOOLS)
        self.assertIn("Bing Image Creator", MODUL["A12"].GEMINI_TOOLS)


class TestFungsiInti(unittest.TestCase):
    def test_contoh_mengembalikan_draf(self):
        for e in EXPECTED:
            m = MODUL[e["kode"]]
            hasil = m.contoh()
            self.assertIsInstance(hasil, dict, e["kode"])
            self.assertEqual(hasil.get("status"), "draf", e["kode"])
            self.assertTrue(hasil.get("butuh_persetujuan"), e["kode"])
            self.assertEqual(hasil.get("agent"), e["kode"], e["kode"])
            for kunci in e["keys"]:
                self.assertIn(kunci, hasil, (e["kode"], kunci))
            for kunci, nilai in e["checks"]:
                self.assertEqual(hasil.get(kunci), nilai, (e["kode"], kunci))

    def test_b04_qc_menolak_kata_terlarang(self):
        m = MODUL["A04"]
        bersih = m.periksa_draf("Halo Kak, harga video promo 15 detik Rp75.000.")
        self.assertTrue(bersih["layak"])
        self.assertEqual(bersih["masalah"], [])
        kotor = m.periksa_draf("Dijamin viral! Views naik pasti! 100% viral!")
        self.assertFalse(kotor["layak"])
        self.assertTrue(kotor["masalah"])

    def test_b08_konsep_belum_lengkap_tanpa_bukti(self):
        m = MODUL["A08"]
        konsep = m.buat_konsep_produk("X", "masalah", "customer", "unik",
                                      1000, "belum cukup data", "TikTok")
        self.assertFalse(konsep["lengkap"])
        self.assertIn("bukti_minat_pasar", konsep["yang_kurang"])

    def test_b10_skor_bukti_kosong_tidak_dihitung(self):
        m = MODUL["A10"]
        penuh = m.cek_kelayakan_produk(
            {"nama": "X", "masalah_customer": "a", "target_customer": "b",
             "keunikan": "c", "harga_rp": 1000, "bukti_minat_pasar": "survei 20 orang",
             "rencana_promosi_distribusi": "TikTok"})
        self.assertEqual(penuh["skor"], 12)
        kosong = m.cek_kelayakan_produk({"nama": "X"})
        self.assertEqual(kosong["skor"], 0)
        self.assertEqual(kosong["verdict"], "BELUM LAYAK")

    def test_b03_kode_tidak_dikenal_ditolak(self):
        m = MODUL["A03"]
        draf = m.bagi_tugas("Tugas X", "A99")
        self.assertIn("masalah", draf)
        self.assertIn("A99", draf["masalah"])
        ok = m.bagi_tugas("Tugas X", "a01")
        self.assertEqual(ok["penanggung_jawab"], "A01")

    def test_b24_volume_tidak_dikarang(self):
        m = MODUL["A24"]
        hasil = m.buat_daftar_kata_kunci("kasir toko")
        self.assertTrue(hasil["kata_kunci"])
        for k in hasil["kata_kunci"]:
            self.assertEqual(k["volume_pencarian"], "belum cukup data")

    def test_b25_penawaran_ada_nama_masduki(self):
        m = MODUL["A25"]
        draf = m.buat_draf_penawaran("Paws & Claws", "video", "toko pet shop ramai")
        self.assertIn("Masduki", draf["teks"])
        self.assertIn("JANGAN ke Mayar", draf["pembayaran"])

    def test_b26_topik_luar_diteruskan(self):
        m = MODUL["A26"]
        draf = m.buat_draf_balasan("Saya mau nego harga", "negosiasi")
        self.assertEqual(draf["balasan_draf"], "")
        self.assertIn("TERUSKAN ke Cipta", draf["tindakan"])

    def test_b29_laporan_keuangan(self):
        m = MODUL["A29"]
        lap = m.format_laporan(58000, 0)
        self.assertEqual(lap["laba_rp"], 58000.0)
        self.assertEqual(lap["pendapatan_teks"], "Rp58.000")
        self.assertIn("KYC Mayar", lap["pantau_kyc_mayar"])

    def test_b11_tiga_klip(self):
        m = MODUL["A11"]
        naskah = m.buat_naskah_video("Judul", "Tema", 30)
        self.assertEqual(len(naskah["klip"]), 3)
        self.assertIn("17–25 kata", naskah["klip"][0]["dialog_template"])

    def test_b17_standar_per_jenis(self):
        m = MODUL["A17"]
        self.assertEqual(m.buat_kerangka_cerita("puisi", "X", "Y")["standar"],
                         "Tepat 20 baris")
        self.assertEqual(m.buat_kerangka_cerita("cerbung", "X", "Y")["standar"],
                         "Outline per bab")


class TestKejujuran(unittest.TestCase):
    def test_docstring_menyebut_pasif(self):
        for e in EXPECTED:
            m = MODUL[e["kode"]]
            doc = (m.__doc__ or "")
            self.assertIn("PASIF", doc, e["kode"])
            self.assertIn("24 jam", doc, e["kode"])
            self.assertIn("DRAF", doc, e["kode"])

    def test_tidak_ada_fungsi_kirim_bayar_publikasi(self):
        terlarang = ("kirim", "bayar", "publikasi", "publish", "submit",
                     "upload", "transfer")
        for e in EXPECTED:
            m = MODUL[e["kode"]]
            nama_fungsi = [n for n in dir(m)
                           if not n.startswith("_") and callable(getattr(m, n))]
            for nama in nama_fungsi:
                rendah = nama.lower()
                for kata in terlarang:
                    self.assertNotIn(kata, rendah, (e["kode"], nama))

    def test_mode_tanpa_key_template(self):
        os.environ.pop("GEMINI_API_KEY", None)
        for e in EXPECTED:
            self.assertEqual(MODUL[e["kode"]].mode_ai(), "template", e["kode"])

    def test_cek_draf_tolak_kata_terlarang(self):
        m = MODUL["A04"]
        self.assertTrue(m.cek_draf("dijamin viral"))
        self.assertEqual(m.cek_draf("teks bersih biasa"), [])


if __name__ == "__main__":
    unittest.main()
