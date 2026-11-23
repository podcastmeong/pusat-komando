#!/usr/bin/env python3
# ======================================================================
# PUSAT KOMANDO 2.0 — llm_router.py
# Router LLM gratis multi-provider untuk 30 Agent Bintang (A01–A30)
# + Agent 31 & 2. Dibuat 21 Nov 2026.
#
# SIFAT: modul PASIF. Modul ini tidak berjalan sendiri dan tidak
# mengirim apa pun tanpa dipanggil. Muse yang menjalankan lewat cron,
# dan semua output yang dihasilkan lewat router ini adalah DRAF untuk
# persetujuan Cipta — bukan kiriman final.
#
# ANGGARAN: Rp0. Hanya provider dengan paket gratis yang dipakai.
# Tidak ada layanan berbayar, tidak ada pembelian, tidak ada upload
# file ke pihak ketiga dari modul ini.
#
# RUTE BERDASAR BERAT TUGAS
#   - "berat" (coding, strategi, analisis)  -> Gemini Free Tier dulu,
#     cadangan OpenRouter model :free.
#   - "cepat" (triase, riset, draf sosmed, tugas massal)
#     -> OpenRouter :free dulu, cadangan Groq, Cerebras, Cloudflare
#     Workers AI (semuanya gratis).
#
# FALLBACK: bila satu provider kena rate-limit (HTTP 429), timeout,
# atau error 5xx / kunci ditolak, router otomatis mencoba provider
# berikutnya yang tersedia untuk kelas tugas yang sama. Setiap
# percobaan (termasuk fallback) dicatat di log.
#
# AI GATEWAY 3.1 — FREE EDITION (21 Nov 2026, perintah Cipta "Eksekusi",
# rencana ChatGPT "AI BUSINESS AUTONOMOUS AGENT 3.1 – FREE EDITION"):
#   - Retry maks 3x per provider dengan backoff 2/5/10 detik (hanya
#     untuk kegagalan sementara: timeout, 429, 5xx — bukan untuk
#     kesalahan kunci / 4xx lain).
#   - Timeout per percobaan 45 detik (bukan 120) agar satu panggilan
#     macet tidak menggantung seluruh antrean.
#   - Cache hasil sementara (data/llm_cache.json, TTL 24 jam): prompt
#     yang sama tidak memanggil API dua kali.
#   - Antrean dalam proses (threading.Lock): 36 agen tidak memanggil
#     API bersamaan di satu proses. Antrean ANTAR proses dijaga oleh
#     agents/task_queue.py (satu konsumen).
#   - Batas ukuran: prompt dipotong maks 8.000 karakter, jawaban maks
#     4.096 karakter yang disimpan.
#   - Bila SEMUA provider gagal: hasil "coba_lagi": True — tugas
#     ditandai untuk dicoba lagi, BUKAN dipalsukan berhasil dan BUKAN
#     jawaban template yang diklaim sebagai jawaban AI.
#
# AI GATEWAY 3.2 — PERBAIKAN GEMINI FLAKY (21 Nov 2026, perintah Cipta
# "Bila ada solusinya dan gratis pula, eksekusi"; jawaban DeepSeek +
# ChatGPT + Gemini web, ketiganya sepakat — file lengkap di
# ~/workspace/research_notes/skill-upgrade-ai/):
#   - STREAMING sebagai jalur utama Gemini (:streamGenerateContent):
#     server mengirim potongan pertama dalam hitungan detik sehingga
#     koneksi tidak idle dan tidak diputus NAT/load balancer. Bila
#     streaming gagal (429/5xx/timeout), coba non-streaming sekali,
#     lalu pindah model. Jalur REST langsung memakai httpx + transport
#     kustom: TCP keepalive (SO_KEEPALIVE=1, TCP_KEEPIDLE=60,
#     TCP_KEEPINTVL=15, TCP_KEEPCNT=4) dan HTTP/1.1 dipaksa
#     (http2=False) — transport kustom harus disertai proxy eksplisit
#     dari env, kalau tidak TLS gagal (transport kustom melewati
#     proxy egress VM). Bila jalur REST langsung tidak tersedia
#     (httpx/surrogate tidak ada), pakai helper resmi sebagai cadangan.
#   - FAIL-FAST: timeout per percobaan 30 dtk (bukan 600, bukan 45):
#     bila server diam 30 dtk, koneksi itu sudah tersangkut — putus
#     dan pindah model lebih cepat. Retry dengan backoff jitter:
#     2**percobaan + random 0,5–2,0 dtk.
#   - RANTAI FALLBACK MODEL (TERBUKTI LIVE 21 Nov 2026, tes REST
#     thinkingBudget=0, prompt "Reply only OK"):
#       gemini-3.5-flash-lite (0,89 dtk) -> gemini-3.5-flash (5,34 dtk)
#       -> gemini-3.8-flash (sering 503 high demand).
#     24 Nov 2026: gemini-4-hydrogen ditambah paling depan (prioritas
#     Cipta, gratis saja); rantai 3.5 di atas tetap sebagai fallback.
#     Rantai lama MATI: gemini-2.5-flash-lite / gemini-2.5-flash /
#     gemini-2.0-flash semuanya 404 "no longer available to new users"
#     (Google menyarankan 3.5-flash-lite / 3.8-flash sebagai ganti).
#     gemini-3.6-flash mengembalikan 200 tanpa teks; gemini-3.7-flash
#     menggantung sampai timeout — keduanya TIDAK dipakai.
#   - THINKING: thinkingBudget=0 untuk model non-lite (3.5-flash dan
#     3.8-flash menerimanya). Model *-lite MENOLAK thinkingConfig
#     (400 INVALID_ARGUMENT) — untuk lite, thinkingConfig dihilangkan.
#   - SDK google-genai TIDAK terpasang di VM ini dan TIDAK BISA
#     di-upgrade (pip diblokir PEP 668; hanya --break-system-packages
#     yang berisiko — tidak dipakai). Router TIDAK BUTUH SDK: kunci
#     hanya bisa diakses lewat mekanisme surrogate secure storage
#     (dynamic_credentials), dan SDK butuh kunci mentah yang tidak
#     pernah tersedia untuk kode. Jalur REST langsung di bawah ini
#     setara dengan generate_content_stream SDK.
#   - Catatan jujur: streaming TIDAK selalu lebih cepat dari
#     non-streaming di sini (3.5-flash: streaming 14,42 dtk vs
#     non-streaming 5,34 dtk; chunk pertama streaming 3.5-flash
#     datang di akhir). Nilai streaming adalah koneksi tetap hidup;
#     yang menyelamatkan dari gantung adalah timeout 30 dtk +
#     pindah model. Bila SEMUA model Gemini gagal total, cadangan
#     berikutnya adalah kunci gratis Groq/Cerebras (butuh Cipta
#     mendaftar sendiri — agen TIDAK mendaftar atas nama Cipta).
#
# KUNCI API — ATURAN KEAMANAN (WAJIB)
#   - Kunci HANYA dibaca dari environment variable. TIDAK PERNAH
#     ditulis di file ini, di file lain, di log, atau di pesan error.
#   - Provider yang kuncinya tidak ada di env = "TIDAK TERSEDIA".
#     Jangan dipalsukan sebagai tersedia.
#   - Pengecualian: Gemini memakai helper resmi yang sudah ada
#     (custom.gemini/bin/gemini.py) — kuncinya tersimpan di secure
#     storage Muse, bukan di env dan bukan di file. Router memanggil
#     helper itu lewat subprocess dan TIDAK PERNAH membaca atau
#     menampilkan kuncinya.
#   - Variabel yang dibaca:
#       GEMINI_API_KEY        (opsional; hanya bila helper tidak ada)
#       OPENROUTER_API_KEY    (wajib untuk OpenRouter)
#       CLOUDFLARE_API_TOKEN  (wajib untuk Cloudflare Workers AI)
#       CLOUDFLARE_ACCOUNT_ID (wajib untuk Cloudflare Workers AI)
#       GROQ_API_KEY          (wajib untuk Groq)
#       CEREBRAS_API_KEY      (wajib untuk Cerebras)
#
# CARA CIPTA MENDAPATKAN KUNCI (daftar sendiri, gratis — agen TIDAK
# membuat akun dan TIDAK mendaftar apa pun atas nama Cipta):
#   1. Gemini — buka Google AI Studio (aistudio.google.com) -> "Get
#      API key" -> "Create API key". Gratis (Free Tier). Simpan lewat
#      alur konektor aman Muse (bukan ditempel di chat/file).
#      CATATAN 21 Nov 2026: kunci Gemini yang tersimpan TERBUKTI
#      VALID — panggilan `models` ke Google berhasil (HTTP 200) dan
#      generate dengan model gemini-3.8-flash mengembalikan jawaban.
#      (Kunci lama 15 Nov 2026 sempat ditolak 400 API_KEY_INVALID;
#      kunci ini dibuat baru oleh Cipta 20 Nov 2026.) Model lama
#      gemini-2.0-flash dan gemini-2.5-flash sudah dipensiunkan Google
#      untuk pengguna baru — TERBUKTI 404 di tes REST 21 Nov 2026.
#      Router memakai rantai gemini-3.5-flash-lite -> gemini-3.5-flash
#      -> gemini-3.8-flash (terbukti menjawab di tes REST yang sama).
#   2. Groq — buka console.groq.com -> daftar gratis -> menu "API
#      Keys" -> "Create API Key". Salin kuncinya sekali saja.
#   3. Cerebras — buka cloud.cerebras.ai -> daftar gratis -> menu
#      "API Keys" -> buat kunci baru.
#   4. OpenRouter — buka openrouter.ai -> daftar gratis -> menu
#      "Keys" -> "Create Key". Model yang dipakai router ini memakai
#      akhiran ":free" (gratis, tanpa kartu kredit).
#   5. Cloudflare Workers AI — buka dash.cloudflare.com -> daftar
#      gratis -> catat Account ID (di sidebar kanan dashboard) ->
#      "My Profile" -> "API Tokens" -> "Create Token" dengan akses
#      Workers AI. Dua nilai dibutuhkan: token DAN Account ID.
#
# CARA MENYETEL ENV VAR (tanpa menulis kunci ke file repo):
#   - Sekali jalan di terminal:
#       export GROQ_API_KEY="kunci-Anda-di-sini"
#       python3 agents/llm_router.py --test
#   - Untuk cron: pasang variabelnya di lingkungan job cron itu
#     sendiri (bukan di file .py / .json / .md di repo).
#   - JANGAN menulis kunci ke file apa pun di folder ini, JANGAN
#     menempel kunci di chat, JANGAN commit kunci ke git.
#
# PENGGUNAAN
#   python3 agents/llm_router.py --status
#       Tabel ketersediaan semua provider (tanpa panggilan jaringan).
#   python3 agents/llm_router.py --test
#       Per provider: tersedia/tidak; bila tersedia, SATU panggilan
#       kecil nyata, hasilnya dilaporkan apa adanya (berhasil / gagal
#       / timeout). Keluar 0 bila >= 1 provider berhasil, 1 bila
#       tidak ada yang berhasil.
#   python3 agents/llm_router.py --route --kelas berat
#       Simulasi rute (tanpa panggilan jaringan): urutan provider
#       dan status ketersediaannya untuk kelas tugas itu.
#   python3 agents/llm_router.py --ask --kelas cepat \
#       --tugas "triase email" --prompt "Ringkas teks ini: ..."
#       Panggilan nyata lewat rute kelas tugas itu; hasil dicetak
#       (teks jawaban + provider + model yang dipakai).
#
# Dipakai dari modul agent lain:
#   from llm_router import jalankan
#   hasil = jalankan(kelas="cepat", tugas="draf sosmed",
#                    prompt="Buat draf caption ...")
#   # hasil = {"ok": True/False, "provider": ..., "model": ...,
#   #          "teks": ... (bila ok), "error": ... (bila gagal),
#   #          "percobaan": [ {...}, ... ]}
#
# LOG: setiap pemakaian dicatat ke data/llm_router_log.json berisi
# timestamp, tugas, kelas, provider, model, status, durasi — TANPA
# kunci, TANPA isi prompt/respons penuh (hanya jumlah karakternya).
# Maksimal 500 entri terbaru.
#
# Python 3.12. Hanya stdlib + requests bila tersedia (bila requests
# tidak ada, otomatis memakai urllib).
# ======================================================================
import argparse
import hashlib
import json
import random
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import requests  # type: ignore
    _ADA_REQUESTS = True
except ImportError:  # pragma: no cover - cadangan bila requests tiada
    requests = None  # type: ignore
    _ADA_REQUESTS = False

BASE = Path(__file__).resolve().parent.parent
LOG_FILE = BASE / "data" / "llm_router_log.json"
GEMINI_HELPER = (
    Path.home()
    / "workspace"
    / "custom-connectors"
    / "custom.gemini"
    / "bin"
    / "gemini.py"
)
WIB = ZoneInfo("Asia/Jakarta")
MAKS_LOG = 500
PANGGILAN_UJI = "Balas hanya dengan kata: OK"

# --- AI GATEWAY 3.2 (21 Nov 2026) — konstanta fail-fast + streaming. ---
# Timeout per percobaan 30 detik untuk SEMUA provider (Gemini web:
# "bila server diam 20–30 dtk, koneksi sudah tersangkut"; DeepSeek +
# ChatGPT sepakat 45–60 dtk, tapi tes live menunjukkan 30 dtk cukup —
# model yang sehat menjawab <15 dtk). Timeout 600 dihapus: satu
# panggilan macet tidak boleh lagi menahan antrean sampai 10 menit.
# Retry: rantai model Gemini maks 2 ronde; provider lain maks 3x.
# Backoff jitter: 2**percobaan + random 0,5–2,0 dtk (lihat
# _backoff_jitter). Cache + antrean + coba_lagi dipertahankan.
TIMEOUT_PER_PROVIDER = {"gemini": 30}
GATEWAY_TIMEOUT_DEFAULT = 30
GATEWAY_RETRY_MAKS = 3
GEMINI_RONDE_MAKS = 2
# Rantai fallback model Gemini — TERBUKTI LIVE 21 Nov 2026 (tes REST,
# thinkingBudget=0, prompt "Reply only OK"):
#   gemini-3.5-flash-lite 0,89 dtk | gemini-3.5-flash 5,34 dtk |
#   gemini-3.8-flash sering 503 high demand (cadangan terakhir).
# Model 2.5-flash-lite / 2.5-flash / 2.0-flash: 404 pensiun — JANGAN
# dipakai lagi. Env GEMINI_MODEL (bila disetel) ditaruh paling depan.
# 24 Nov 2026 (perintah Cipta "Prioritas Hydrogen, yang gratis"):
#   gemini-4-hydrogen ditaruh PALING DEPAN — free tier, diverifikasi
#   ADA + bisa diakses kunci gratis (22 Nov: 1x berhasil; 24 Nov:
#   2x 503 overload — free tier tidak stabil saat beban tinggi).
#   Bila Hydrogen gagal, rantai otomatis jatuh ke 3.5 (terbukti live).
GEMINI_MODEL_CHAIN = [
    "gemini-4-hydrogen",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
]
PROMPT_MAKS_CHARS = 8000
TEKS_MAKS_CHARS = 4096
CACHE_FILE = BASE / "data" / "llm_cache.json"
CACHE_TTL_DETIK = 86400  # 24 jam
CACHE_MAKS_ENTRI = 200
# Antrean dalam proses: satu panggilan API dalam satu waktu.
_ANTREAN_LOCK = threading.Lock()

# Urutan provider per kelas tugas. Provider pertama = rute utama
# sesuai spesifikasi; sisanya cadangan bila yang utama gagal / 429.
RUTE = {
    "berat": ["gemini", "openrouter"],
    "cepat": ["openrouter", "groq", "cerebras", "cloudflare"],
}

# Model default gratis per provider. Bisa diubah lewat env var
# <PROVIDER>_MODEL tanpa mengubah file ini.
MODEL_DEFAULT = {
    "gemini": "gemini-4-hydrogen",
    "openrouter": "meta-llama/llama-3.3-70b-instruct:free",
    "groq": "llama-3.3-70b-versatile",
    "cerebras": "llama-3.3-70b",
    "cloudflare": "@cf/meta/llama-3-8b-instruct",
}
MODEL_ENV = {
    "gemini": "GEMINI_MODEL",
    "openrouter": "OPENROUTER_MODEL",
    "groq": "GROQ_MODEL",
    "cerebras": "CEREBRAS_MODEL",
    "cloudflare": "CLOUDFLARE_MODEL",
}

# Env var kunci per provider. Gemini: None karena memakai helper
# secure storage; GEMINI_API_KEY hanya cadangan bila helper tiada.
KUNCI_ENV = {
    "gemini": "GEMINI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    "cloudflare": "CLOUDFLARE_API_TOKEN",
}

# Endpoint chat-completions gaya OpenAI (Groq, Cerebras, OpenRouter).
ENDPOINT_OPENAI = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "cerebras": "https://api.cerebras.ai/v1/chat/completions",
}


# ----------------------------------------------------------------------
# Utilitas keamanan: kunci tidak boleh bocor ke log / error / output.
# ----------------------------------------------------------------------
def _daftar_kunci():
    """Kumpulkan nilai kunci dari env (di memori saja) untuk disensor."""
    nilai = []
    for nama in list(KUNCI_ENV.values()) + ["CLOUDFLARE_ACCOUNT_ID"]:
        v = __import__("os").environ.get(nama)
        if v and len(v) >= 8:
            nilai.append(v)
    return nilai


def _sensor(teks):
    """Ganti kemunculan nilai kunci apa pun dengan penanda aman."""
    if teks is None:
        return ""
    teks = str(teks)
    for k in _daftar_kunci():
        teks = teks.replace(k, "[KUNCI-DISEMBUNYIKAN]")
    return teks


def _waktu_sekarang():
    return datetime.now(WIB).isoformat(timespec="seconds")


def _model(provider):
    import os

    return os.environ.get(MODEL_ENV[provider]) or MODEL_DEFAULT[provider]


# ----------------------------------------------------------------------
# Ketersediaan provider (tanpa panggilan jaringan).
# ----------------------------------------------------------------------
def status_provider():
    """Kembalikan dict {provider: {...}} — jujur, tanpa dipalsukan.

    "tersedia" True hanya bila ada jalur kredensial yang nyata:
    Gemini = helper secure-storage ada (atau GEMINI_API_KEY di env);
    lainnya = kunci + (untuk Cloudflare: Account ID) ada di env.
    """
    import os

    hasil = {}
    for p in ("gemini", "openrouter", "groq", "cerebras", "cloudflare"):
        env_nama = KUNCI_ENV[p]
        kunci_ada = bool(os.environ.get(env_nama))
        if p == "gemini":
            helper_ada = GEMINI_HELPER.is_file()
            tersedia = helper_ada or kunci_ada
            cara = (
                "helper secure storage (custom.gemini)"
                if helper_ada
                else ("env GEMINI_API_KEY" if kunci_ada else "-")
            )
            catatan = (
                "Kunci di secure storage. TERBUKTI LIVE 21 Nov 2026 "
                "(tes REST): gemini-3.5-flash-lite + gemini-3.5-flash "
                "menjawab; gemini-3.8-flash sering 503 high demand; "
                "model 2.5/2.0 pensiun (404)."
                if helper_ada
                else ""
            )
        elif p == "cloudflare":
            akun_ada = bool(os.environ.get("CLOUDFLARE_ACCOUNT_ID"))
            tersedia = kunci_ada and akun_ada
            cara = "env CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID"
            catatan = (
                ""
                if tersedia
                else "Butuh token DAN Account ID di env."
            )
        else:
            tersedia = kunci_ada
            cara = f"env {env_nama}"
            catatan = ""
        hasil[p] = {
            "tersedia": tersedia,
            "status": "TERSEDIA" if tersedia else "TIDAK TERSEDIA",
            "model": _model(p),
            "kredensial": cara,
            "catatan": catatan,
        }
    return hasil


def tersedia(provider):
    return status_provider()[provider]["tersedia"]


# ----------------------------------------------------------------------
# Log pemakaian (tanpa kunci, tanpa isi prompt/respons penuh).
# ----------------------------------------------------------------------
def _catat_log(entri):
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = []
        if LOG_FILE.is_file():
            try:
                data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
                if not isinstance(data, list):
                    data = []
            except (json.JSONDecodeError, OSError):
                data = []
        data.append(entri)
        data = data[-MAKS_LOG:]
        tmp = LOG_FILE.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(LOG_FILE)
    except OSError:
        # Log gagal ditulis: jangan gagalkan tugas utama karenanya.
        pass


# ----------------------------------------------------------------------
# Lapisan HTTP (requests bila ada, urllib bila tidak).
# Mengembalikan (ok, teks_jawaban, http_status, pesan_error_sanitized).
# ----------------------------------------------------------------------
def _post_json(url, headers, payload, timeout):
    if _ADA_REQUESTS:
        try:
            r = requests.post(
                url, headers=headers, json=payload, timeout=timeout
            )
            return r.status_code, r.text
        except requests.exceptions.Timeout:
            return None, "timeout"
        except requests.exceptions.RequestException as e:
            return None, f"error koneksi: {type(e).__name__}"
    import urllib.error
    import urllib.request

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as e:
        if isinstance(e, TimeoutError) or "timed out" in str(e):
            return None, "timeout"
        return None, f"error koneksi: {type(e).__name__}"


def _panggil_openai_compatible(provider, prompt, timeout, max_tokens):
    import os

    kunci = os.environ.get(KUNCI_ENV[provider]) or ""
    headers = {
        "Authorization": f"Bearer {kunci}",
        "Content-Type": "application/json",
    }
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://podcastmeong.github.io/"
        headers["X-Title"] = "Pusat Komando 2.0"
    payload = {
        "model": _model(provider),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    status, body = _post_json(
        ENDPOINT_OPENAI[provider], headers, payload, timeout
    )
    if status is None:
        return False, "", None, _sensor(body)
    if status == 429:
        return False, "", 429, "rate-limit (HTTP 429)"
    if status != 200:
        pesan = _sensor(body)[:300]
        return False, "", status, f"HTTP {status}: {pesan}"
    try:
        data = json.loads(body)
        teks = data["choices"][0]["message"]["content"]
        return True, str(teks), 200, ""
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return False, "", 200, "respons tidak dapat dibaca (format tak dikenal)"


def _panggil_cloudflare(prompt, timeout, max_tokens):
    import os

    token = os.environ.get("CLOUDFLARE_API_TOKEN") or ""
    akun = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or ""
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{akun}/ai/run/{_model('cloudflare')}"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    status, body = _post_json(url, headers, payload, timeout)
    if status is None:
        return False, "", None, _sensor(body)
    if status == 429:
        return False, "", 429, "rate-limit (HTTP 429)"
    if status != 200:
        pesan = _sensor(body)[:300]
        return False, "", status, f"HTTP {status}: {pesan}"
    try:
        data = json.loads(body)
        teks = data["result"]["response"]
        return True, str(teks), 200, ""
    except (KeyError, TypeError, json.JSONDecodeError):
        return False, "", 200, "respons tidak dapat dibaca (format tak dikenal)"


def _panggil_gemini_helper(prompt, timeout, max_tokens, model=None):
    """Gemini lewat helper resmi (secure storage). Tanpa kunci di sini.

    max_tokens tidak diteruskan: helper tidak punya opsi itu.
    Helper juga tidak mendukung thinkingConfig/streaming — dipakai hanya
    sebagai cadangan bila jalur REST langsung tidak tersedia.
    """
    if not GEMINI_HELPER.is_file():
        return _panggil_gemini_rest(prompt, timeout, max_tokens, model)
    cmd = [
        sys.executable,
        str(GEMINI_HELPER),
        "generate",
        "--model",
        model or _model("gemini"),
        "--prompt",
        prompt,
    ]
    try:
        # Teruskan timeout ke helper: helper sendiri punya batas
        # internal (default 120 dtk) — tanpa ini, timeout fail-fast
        # gateway (30 dtk) tidak pernah tercapai karena helper memutus
        # duluan... sebenarnya sebaliknya: helper memutus duluan bila
        # timeout gateway lebih besar; dengan timeout 30 dtk, batas
        # subprocess inilah yang memutus panggilan macet.
        import os

        env = dict(os.environ)
        env["GEMINI_HELPER_TIMEOUT"] = str(timeout)
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=env
        )
    except subprocess.TimeoutExpired:
        return False, "", None, f"timeout ({timeout} dtk, panggilan tidak kembali)"
    except OSError as e:
        return False, "", None, f"gagal menjalankan helper: {type(e).__name__}"
    if proc.returncode != 0:
        pesan = _sensor(proc.stderr or proc.stdout)[:300]
        return False, "", None, f"helper gagal: {pesan}"
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return False, "", None, "respons helper bukan JSON"
    if isinstance(data, dict) and data.get("error"):
        return False, "", None, f"Gemini menolak: {_sensor(str(data['error'])[:300])}"
    try:
        bagian = []
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "text" in part:
                    bagian.append(part["text"])
        if not bagian:
            return False, "", 200, "respons Gemini kosong / tanpa teks"
        return True, "\n".join(bagian), 200, ""
    except (AttributeError, TypeError):
        return False, "", 200, "respons tidak dapat dibaca (format tak dikenal)"


def _panggil_gemini_rest(prompt, timeout, max_tokens, model=None):
    """Cadangan bila helper tiada: REST langsung dgn GEMINI_API_KEY env.

    thinkingBudget=0 untuk model non-lite; model *-lite MENOLAK
    thinkingConfig (400) sehingga config itu dihilangkan untuk lite.
    """
    import os

    model = model or _model("gemini")
    kunci = os.environ.get("GEMINI_API_KEY") or ""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    headers = {
        "x-goog-api-key": kunci,
        "Content-Type": "application/json",
    }
    cfg = {"maxOutputTokens": max_tokens}
    if "lite" not in model:
        cfg["thinkingConfig"] = {"thinkingBudget": 0}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": cfg,
    }
    status, body = _post_json(url, headers, payload, timeout)
    if status is None:
        return False, "", None, _sensor(body)
    if status == 429:
        return False, "", 429, "rate-limit (HTTP 429)"
    if status != 200:
        pesan = _sensor(body)[:300]
        return False, "", status, f"HTTP {status}: {pesan}"
    try:
        data = json.loads(body)
        bagian = []
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "text" in part:
                    bagian.append(part["text"])
        if not bagian:
            return False, "", 200, "respons Gemini kosong / tanpa teks"
        return True, "\n".join(bagian), 200, ""
    except (KeyError, TypeError, json.JSONDecodeError):
        return False, "", 200, "respons tidak dapat dibaca (format tak dikenal)"


# ----------------------------------------------------------------------
# Gemini 3.2 — jalur REST langsung (streaming utama) + rantai model.
# ----------------------------------------------------------------------
class _JalurTidakTersedia(Exception):
    """Jalur REST langsung tidak bisa dipakai di lingkungan ini
    (httpx/surrogate tidak ada) — pemanggil beralih ke helper."""


def _backoff_jitter(percobaan_ke):
    """Backoff eksponensial + jitter acak (Gemini web): 2**n + 0,5–2,0 dtk."""
    return (2 ** int(percobaan_ke)) + random.uniform(0.5, 2.0)


def _rantai_model_gemini():
    """Urutan model Gemini yang dicoba. Env GEMINI_MODEL (bila disetel)
    ditaruh paling depan; sisanya mengikuti rantai yang terbukti live."""
    rantai = list(GEMINI_MODEL_CHAIN)
    try:
        import os

        utama = os.environ.get("GEMINI_MODEL", "").strip()
    except Exception:
        utama = ""
    if utama:
        rantai = [utama] + [m for m in rantai if m != utama]
    return rantai


def _extract_text_gemini(data):
    """Ambil semua teks dari respons generateContent/stream."""
    bagian = []
    try:
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "text" in part:
                    bagian.append(part["text"])
    except (AttributeError, TypeError):
        pass
    return "".join(bagian)


def _panggil_gemini_rest_langsung(prompt, timeout, max_tokens, model,
                                  streaming):
    """REST Gemini langsung via httpx + surrogate secure storage.

    Jalur utama (streaming=True): :streamGenerateContent?alt=sse —
    potongan pertama tiba dalam hitungan detik sehingga koneksi tidak
    idle. Transport kustom: TCP keepalive + HTTP/1.1 dipaksa
    (http2=False). Transport kustom melewati proxy egress VM, jadi
    proxy HARUS diteruskan eksplisit dari env (tanpa itu TLS gagal
    "wrong version number"). Kunci TIDAK PERNAH dibaca nilainya:
    hanya surrogate (hsurr:...) yang ditaruh di header dan diganti
    kunci asli oleh Sentinel saat request keluar.

    thinkingBudget=0 untuk model non-lite; model *-lite menolak
    thinkingConfig (400) sehingga dihilangkan untuk lite.
    Timeout httpx dipisah: connect 10 dtk, read = timeout per
    percobaan (fail-fast 30 dtk), write/pool 10 dtk.
    """
    import os

    try:
        import httpx
    except ImportError:
        raise _JalurTidakTersedia("httpx tidak terpasang")
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    try:
        from dynamic_credentials import dynamic_credential_entry
    except ImportError:
        raise _JalurTidakTersedia("dynamic_credentials tidak tersedia")
    try:
        entri = dynamic_credential_entry("custom.gemini", "access_token")
        penempatan = entri.get("placement") or {}
        header_nama = (
            penempatan.get("custom_header", "x-goog-api-key")
            if isinstance(penempatan, dict)
            else "x-goog-api-key"
        )
        surrogate = str(entri.get("surrogate") or "")
        if not surrogate.startswith("hsurr:"):
            raise _JalurTidakTersedia("surrogate kredensial tidak valid")
    except _JalurTidakTersedia:
        raise
    except Exception as e:
        raise _JalurTidakTersedia(
            f"gagal memuat kredensial: {type(e).__name__}"
        ) from e

    cfg = {"maxOutputTokens": max_tokens}
    if "lite" not in model:
        cfg["thinkingConfig"] = {"thinkingBudget": 0}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": cfg,
    }
    endpoint = (
        ":streamGenerateContent?alt=sse" if streaming else ":generateContent"
    )
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}{endpoint}"
    )
    headers = {header_nama: surrogate, "Content-Type": "application/json"}
    import socket

    transport = httpx.HTTPTransport(
        socket_options=[
            (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
            (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60),
            (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15),
            (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 4),
        ],
    )
    proxy = (
        os.environ.get("https_proxy")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("http_proxy")
        or os.environ.get("HTTP_PROXY")
    )
    batas = httpx.Timeout(
        float(timeout), connect=10.0, read=float(timeout),
        write=10.0, pool=10.0,
    )
    try:
        with httpx.Client(
            transport=transport, proxy=proxy, timeout=batas, http2=False
        ) as klien:
            if streaming:
                with klien.stream(
                    "POST", url, headers=headers, json=payload
                ) as resp:
                    if resp.status_code == 429:
                        return False, "", 429, "rate-limit (HTTP 429)"
                    if resp.status_code != 200:
                        body = resp.read().decode(
                            "utf-8", errors="replace"
                        )[:300]
                        return (
                            False, "", resp.status_code,
                            f"HTTP {resp.status_code}: {_sensor(body)}",
                        )
                    teks = ""
                    for baris in resp.iter_lines():
                        if baris.startswith("data:"):
                            try:
                                data = json.loads(baris[5:].strip())
                                teks += _extract_text_gemini(data)
                            except json.JSONDecodeError:
                                continue
                    if not teks:
                        return (
                            False, "", 200,
                            "respons Gemini kosong / tanpa teks",
                        )
                    return True, teks, 200, ""
            resp = klien.post(url, headers=headers, json=payload)
            if resp.status_code == 429:
                return False, "", 429, "rate-limit (HTTP 429)"
            if resp.status_code != 200:
                pesan = _sensor(resp.text)[:300]
                return (
                    False, "", resp.status_code,
                    f"HTTP {resp.status_code}: {pesan}",
                )
            try:
                data = resp.json()
            except json.JSONDecodeError:
                return False, "", 200, "respons bukan JSON"
            teks = _extract_text_gemini(data)
            if not teks:
                return False, "", 200, "respons Gemini kosong / tanpa teks"
            return True, teks, 200, ""
    except httpx.TimeoutException:
        return False, "", None, f"timeout ({timeout} dtk, panggilan tidak kembali)"
    except httpx.HTTPError as e:
        return False, "", None, f"error koneksi: {type(e).__name__}"


def _panggil_gemini(prompt, timeout, max_tokens, model):
    """Satu model Gemini: streaming dulu, lalu non-streaming sekali.

    Bila jalur REST langsung tidak tersedia di lingkungan ini
    (httpx/surrogate tidak ada), pakai helper resmi sebagai cadangan.
    4xx non-429 langsung dikembalikan (model/argumen bermasalah —
    tidak ada gunanya mencoba jalur kedua untuk model yang sama).
    """
    try:
        ok, teks, http, err = _panggil_gemini_rest_langsung(
            prompt, timeout, max_tokens, model, streaming=True
        )
    except _JalurTidakTersedia:
        return _panggil_gemini_helper(prompt, timeout, max_tokens, model)
    if ok:
        return True, teks, http, ""
    if http is not None and http < 500 and http != 429:
        return False, "", http, err
    ok2, teks2, http2, err2 = _panggil_gemini_rest_langsung(
        prompt, timeout, max_tokens, model, streaming=False
    )
    if ok2:
        return True, teks2, http2, ""
    return False, "", http2, err2


def _panggil_gemini_rantai(prompt, timeout, max_tokens):
    """Rantai model Gemini: tiap model sekali per ronde, maks 2 ronde.

    Pindah model langsung tanpa tidur (fail-fast); tidur dengan
    backoff+jitter hanya antar ronde. 4xx non-429 (mis. 404 model
    pensiun, 400 argumen tak didukung) langsung lanjut ke model
    berikutnya. Mengembalikan (hasil_terakhir, daftar_percobaan).
    """
    models = _rantai_model_gemini()
    percobaan = []
    hasil = None
    for ronde in range(GEMINI_RONDE_MAKS):
        for model in models:
            with _ANTREAN_LOCK:
                hasil = panggil_provider(
                    "gemini", prompt, timeout, max_tokens, model=model
                )
            percobaan.append(
                {
                    "percobaan_ke": len(percobaan) + 1,
                    "provider": "gemini",
                    "model": hasil["model"],
                    "status": (
                        "ok"
                        if hasil["ok"]
                        else (
                            "fallback-429"
                            if hasil["http_status"] == 429
                            else "gagal"
                        )
                    ),
                    "http_status": hasil["http_status"],
                    "error": hasil["error"],
                    "durasi_ms": hasil["durasi_ms"],
                }
            )
            if hasil["ok"]:
                return hasil, percobaan
        if ronde + 1 < GEMINI_RONDE_MAKS:
            time.sleep(_backoff_jitter(ronde))
    return hasil, percobaan


def _potong_prompt(prompt):
    """Batasi ukuran prompt (ChatGPT: batasi ukuran prompt dan hasil).

    Mengembalikan (prompt_terpotong, dipotong_bool).
    """
    teks = str(prompt)
    if len(teks) > PROMPT_MAKS_CHARS:
        return teks[:PROMPT_MAKS_CHARS], True
    return teks, False


def _cache_kunci(provider, model, prompt):
    mentah = f"{provider}|{model}|{prompt}".encode("utf-8")
    return hashlib.sha256(mentah).hexdigest()


def _cache_baca(kunci):
    """Baca cache hasil (bila ada dan belum kedaluwarsa)."""
    try:
        if not CACHE_FILE.is_file():
            return None
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        entri = data.get(kunci)
        if not entri:
            return None
        if time.time() - float(entri.get("waktu_epoch", 0)) > CACHE_TTL_DETIK:
            return None
        return entri.get("teks", "")
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def _cache_tulis(kunci, teks):
    """Simpan hasil ke cache (maks CACHE_MAKS_ENTRI, yang terlama dibuang)."""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        if CACHE_FILE.is_file():
            try:
                data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    data = {}
            except (json.JSONDecodeError, OSError):
                data = {}
        data[kunci] = {"waktu_epoch": time.time(), "teks": teks[:TEKS_MAKS_CHARS]}
        # Buang entri terlama bila melebihi batas (urutkan pakai waktu).
        while len(data) > CACHE_MAKS_ENTRI:
            kunci_lama = min(data, key=lambda k: data[k].get("waktu_epoch", 0))
            del data[kunci_lama]
        tmp = CACHE_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(CACHE_FILE)
    except OSError:
        pass


def _bisa_retry(hasil):
    """Layak dicoba ulang? Hanya kegagalan sementara: timeout, 429, 5xx.

    Kunci ditolak (400/401/403) dan 4xx lain TIDAK di-retry — mengulang
    tidak akan mengubah hasilnya.
    """
    if hasil.get("ok"):
        return False
    if hasil.get("http_status") == 429:
        return True
    if hasil.get("http_status") is not None and hasil["http_status"] >= 500:
        return True
    err = (hasil.get("error") or "").lower()
    return "timeout" in err or "timed out" in err


def _panggil_dengan_retry(provider, prompt, timeout, max_tokens):
    """Satu provider, retry + backoff jitter.

    Gemini: rantai model (lihat _panggil_gemini_rantai) — tiap model
    sekali per ronde, maks 2 ronde. Provider lain: maks
    GATEWAY_RETRY_MAKS percobaan + backoff jitter. Timeout per
    percobaan mengikuti peta per provider (30 dtk, fail-fast) dan
    tidak pernah melebihi `timeout` yang diminta pemanggil. Tiap
    percobaan tunggal lewat antrean (_ANTREAN_LOCK) agar 36 agen
    tidak memanggil API bersamaan. Mengembalikan (hasil_terakhir,
    daftar_percobaan).
    """
    batas = TIMEOUT_PER_PROVIDER.get(provider, GATEWAY_TIMEOUT_DEFAULT)
    timeout = min(int(timeout), batas)
    if provider == "gemini":
        return _panggil_gemini_rantai(prompt, timeout, max_tokens)
    percobaan = []
    hasil = None
    for i in range(GATEWAY_RETRY_MAKS):
        with _ANTREAN_LOCK:
            hasil = panggil_provider(provider, prompt, timeout, max_tokens)
        percobaan.append(
            {
                "percobaan_ke": i + 1,
                "provider": provider,
                "model": hasil["model"],
                "status": (
                    "ok"
                    if hasil["ok"]
                    else ("fallback-429" if hasil["http_status"] == 429 else "gagal")
                ),
                "http_status": hasil["http_status"],
                "error": hasil["error"],
                "durasi_ms": hasil["durasi_ms"],
            }
        )
        if hasil["ok"] or not _bisa_retry(hasil):
            break
        if i + 1 < GATEWAY_RETRY_MAKS:
            time.sleep(_backoff_jitter(i))
    return hasil, percobaan


def panggil_provider(provider, prompt, timeout=30, max_tokens=512,
                      model=None):
    """Satu panggilan ke satu provider. Kembalikan dict hasil.

    model: hanya dipakai untuk Gemini (rantai fallback); bila None,
    pakai model default provider itu.
    """
    mulai = time.monotonic()
    model_dipakai = model or _model(provider)
    if provider == "gemini":
        ok, teks, http, err = _panggil_gemini(
            prompt, timeout, max_tokens, model_dipakai
        )
    elif provider == "cloudflare":
        ok, teks, http, err = _panggil_cloudflare(prompt, timeout, max_tokens)
    elif provider in ENDPOINT_OPENAI:
        ok, teks, http, err = _panggil_openai_compatible(
            provider, prompt, timeout, max_tokens
        )
    else:
        return {
            "ok": False,
            "provider": provider,
            "model": "",
            "teks": "",
            "http_status": None,
            "error": f"provider tidak dikenal: {provider}",
            "durasi_ms": 0,
        }
    return {
        "ok": ok,
        "provider": provider,
        "model": model_dipakai,
        "teks": teks,
        "http_status": http,
        "error": _sensor(err),
        "durasi_ms": int((time.monotonic() - mulai) * 1000),
    }


# ----------------------------------------------------------------------
# Rute utama: pilih provider berdasar kelas, fallback otomatis.
# ----------------------------------------------------------------------
def jalankan(kelas, tugas, prompt, timeout=30, max_tokens=512):
    """Jalankan satu tugas lewat AI Gateway 3.1 (cache + retry + antrean).

    kelas: "berat" atau "cepat". tugas: label singkat untuk log.
    Mengembalikan dict: ok, provider, model, teks (bila ok),
    error (bila gagal), percobaan (daftar tiap provider dicoba),
    dari_cache (bool), coba_lagi (bool — True bila semua gagal dan
    tugas harus dicoba lagi nanti, BUKAN dipalsukan berhasil).
    """
    if kelas not in RUTE:
        raise ValueError(
            f"kelas tidak dikenal: {kelas!r} (pilih 'berat' atau 'cepat')"
        )
    if not prompt or not str(prompt).strip():
        raise ValueError("prompt kosong — tidak ada yang dikirim")
    prompt, prompt_dipotong = _potong_prompt(prompt)
    max_tokens = min(int(max_tokens), 1024)
    percobaan = []
    for provider in RUTE[kelas]:
        if not tersedia(provider):
            info = {
                "provider": provider,
                "model": _model(provider),
                "status": "dilewati-tidak-tersedia",
                "http_status": None,
                "error": "TIDAK TERSEDIA (kunci tidak ada di env)",
                "durasi_ms": 0,
            }
            percobaan.append(info)
            _catat_log(
                {
                    "waktu": _waktu_sekarang(),
                    "tugas": str(tugas)[:120],
                    "kelas": kelas,
                    "provider": provider,
                    "model": _model(provider),
                    "status": "dilewati-tidak-tersedia",
                    "http_status": None,
                    "durasi_ms": 0,
                    "prompt_chars": len(prompt),
                    "response_chars": 0,
                    "error": "TIDAK TERSEDIA (kunci tidak ada di env)",
                }
            )
            continue
        # Cache dulu: prompt yang sama tidak memanggil API dua kali.
        kunci_cache = _cache_kunci(provider, _model(provider), prompt)
        teks_cache = _cache_baca(kunci_cache)
        if teks_cache:
            _catat_log(
                {
                    "waktu": _waktu_sekarang(),
                    "tugas": str(tugas)[:120],
                    "kelas": kelas,
                    "provider": provider,
                    "model": _model(provider),
                    "status": "ok-cache",
                    "http_status": 200,
                    "durasi_ms": 0,
                    "prompt_chars": len(prompt),
                    "response_chars": len(teks_cache),
                    "error": "",
                }
            )
            return {
                "ok": True,
                "provider": provider,
                "model": _model(provider),
                "teks": teks_cache,
                "error": "",
                "percobaan": percobaan,
                "dari_cache": True,
                "coba_lagi": False,
                "prompt_dipotong": prompt_dipotong,
            }
        hasil, percobaan_provider = _panggil_dengan_retry(
            provider, prompt, timeout, max_tokens
        )
        percobaan.extend(percobaan_provider)
        if hasil["ok"]:
            status = "ok"
        elif hasil["http_status"] == 429:
            status = "fallback-429"
        else:
            status = "gagal"
        _catat_log(
            {
                "waktu": _waktu_sekarang(),
                "tugas": str(tugas)[:120],
                "kelas": kelas,
                "provider": provider,
                "model": hasil["model"],
                "status": status,
                "http_status": hasil["http_status"],
                "durasi_ms": hasil["durasi_ms"],
                "prompt_chars": len(prompt),
                "response_chars": len(hasil["teks"]) if hasil["ok"] else 0,
                "error": hasil["error"][:300],
            }
        )
        if hasil["ok"]:
            _cache_tulis(kunci_cache, hasil["teks"])
            return {
                "ok": True,
                "provider": provider,
                "model": hasil["model"],
                "teks": hasil["teks"][:TEKS_MAKS_CHARS],
                "error": "",
                "percobaan": percobaan,
                "dari_cache": False,
                "coba_lagi": False,
                "prompt_dipotong": prompt_dipotong,
            }
        # Gagal (429 / timeout / 5xx / kunci ditolak): coba berikutnya.
    return {
        "ok": False,
        "provider": "",
        "model": "",
        "teks": "",
        "error": "Semua provider untuk kelas "
        f"'{kelas}' gagal / tidak tersedia. "
        "Lihat 'percobaan' untuk rincian per provider.",
        "percobaan": percobaan,
        "dari_cache": False,
        "coba_lagi": True,
        "saran": "Tandai tugas untuk dicoba lagi nanti (retry di lain "
        "waktu). Jangan klaim jawaban template sebagai jawaban AI.",
        "prompt_dipotong": prompt_dipotong,
    }


# ----------------------------------------------------------------------
# Uji satu provider: SATU panggilan kecil nyata (bila tersedia).
# ----------------------------------------------------------------------
def uji_provider(provider, timeout=30):
    """Uji satu provider apa adanya. Kembalikan dict hasil uji."""
    info = status_provider()[provider]
    if not info["tersedia"]:
        hasil = {
            "provider": provider,
            "model": info["model"],
            "tersedia": False,
            "status": "TIDAK TERSEDIA",
            "hasil_uji": "tidak diuji (tidak ada kredensial)",
            "http_status": None,
            "error": "Kunci tidak ada di environment variable.",
            "durasi_ms": 0,
        }
        _catat_log(
            {
                "waktu": _waktu_sekarang(),
                "tugas": "--test",
                "kelas": "-",
                "provider": provider,
                "model": info["model"],
                "status": "tidak-tersedia",
                "http_status": None,
                "durasi_ms": 0,
                "prompt_chars": 0,
                "response_chars": 0,
                "error": "TIDAK TERSEDIA (kunci tidak ada di env)",
            }
        )
        return hasil
    hasil = panggil_provider(provider, PANGGILAN_UJI, timeout, max_tokens=16)
    status = "BERHASIL" if hasil["ok"] else "GAGAL"
    _catat_log(
        {
            "waktu": _waktu_sekarang(),
            "tugas": "--test",
            "kelas": "-",
            "provider": provider,
            "model": hasil["model"],
            "status": "ok" if hasil["ok"] else "gagal-uji",
            "http_status": hasil["http_status"],
            "durasi_ms": hasil["durasi_ms"],
            "prompt_chars": len(PANGGILAN_UJI),
            "response_chars": len(hasil["teks"]) if hasil["ok"] else 0,
            "error": hasil["error"][:300],
        }
    )
    return {
        "provider": provider,
        "model": hasil["model"],
        "tersedia": True,
        "status": status,
        "hasil_uji": (
            f"panggilan nyata berhasil ({hasil['durasi_ms']} ms)"
            if hasil["ok"]
            else "panggilan nyata gagal"
        ),
        "http_status": hasil["http_status"],
        "error": hasil["error"],
        "durasi_ms": hasil["durasi_ms"],
        "jawaban_uji": hasil["teks"][:100] if hasil["ok"] else "",
    }


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def _cetak_status():
    print("LLM Router — status provider (tanpa panggilan jaringan)")
    print(f"requests tersedia: {'ya' if _ADA_REQUESTS else 'tidak (pakai urllib)'}")
    print(f"helper Gemini: {GEMINI_HELPER} "
          f"({'ada' if GEMINI_HELPER.is_file() else 'TIDAK ADA'})")
    print()
    for p, info in status_provider().items():
        print(f"- {p:<12} {info['status']:<15} model: {info['model']}")
        print(f"  {'':<12} kredensial: {info['kredensial']}")
        if info["catatan"]:
            print(f"  {'':<12} catatan: {info['catatan']}")
    print()
    print("Rute: berat -> " + " -> ".join(RUTE["berat"]))
    print("      cepat -> " + " -> ".join(RUTE["cepat"]))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Router LLM gratis Pusat Komando 2.0 "
        "(berat -> Gemini, cepat -> OpenRouter/Groq/Cerebras/Cloudflare)."
    )
    parser.add_argument("--status", action="store_true",
                        help="tampilkan ketersediaan provider (tanpa jaringan)")
    parser.add_argument("--test", action="store_true",
                        help="uji tiap provider tersedia dengan SATU panggilan kecil nyata")
    parser.add_argument("--route", action="store_true",
                        help="simulasi rute tanpa panggilan jaringan")
    parser.add_argument("--ask", action="store_true",
                        help="lakukan satu panggilan nyata lewat rute kelas tugas")
    parser.add_argument("--kelas", choices=["berat", "cepat"], default="cepat",
                        help="kelas tugas (default: cepat)")
    parser.add_argument("--tugas", default="tugas-cli",
                        help="label tugas untuk log")
    parser.add_argument("--prompt", default="",
                        help="teks prompt untuk --ask")
    parser.add_argument("--timeout", type=int, default=30,
                        help="timeout per percobaan dalam detik (default: 30, fail-fast)")
    parser.add_argument("--max-tokens", type=int, default=512,
                        help="maks token jawaban (default: 512)")
    parser.add_argument("--json", action="store_true",
                        help="cetak hasil sebagai JSON")
    args = parser.parse_args(argv)

    if args.status:
        if args.json:
            print(json.dumps(status_provider(), ensure_ascii=False, indent=2))
        else:
            _cetak_status()
        return 0

    if args.route:
        info = status_provider()
        urutan = [
            {"provider": p, "model": _model(p),
             "status": info[p]["status"]}
            for p in RUTE[args.kelas]
        ]
        if args.json:
            print(json.dumps({"kelas": args.kelas, "rute": urutan},
                             ensure_ascii=False, indent=2))
        else:
            print(f"Rute kelas '{args.kelas}' (tanpa panggilan jaringan):")
            for i, u in enumerate(urutan, 1):
                print(f"  {i}. {u['provider']} ({u['model']}) — {u['status']}")
        return 0

    if args.test:
        print("LLM Router --test: SATU panggilan kecil nyata per provider tersedia")
        print(f"Prompt uji: {PANGGILAN_UJI!r} (jawaban tidak disimpan penuh di log)")
        print()
        hasil_semua = []
        ada_berhasil = False
        for p in ("gemini", "openrouter", "groq", "cerebras", "cloudflare"):
            print(f"[{p}] menguji ...", flush=True)
            hasil = uji_provider(p)
            hasil_semua.append(hasil)
            if hasil["status"] == "BERHASIL":
                ada_berhasil = True
            print(f"[{p}] {hasil['status']} — {hasil['hasil_uji']}")
            if hasil["error"]:
                print(f"[{p}] keterangan: {_sensor(hasil['error'])[:300]}")
            if hasil.get("jawaban_uji"):
                print(f"[{p}] jawaban uji: {hasil['jawaban_uji']!r}")
            print()
        if args.json:
            print(json.dumps(hasil_semua, ensure_ascii=False, indent=2))
        print(f"Log tersimpan di: {LOG_FILE}")
        print("Ringkasan: "
              f"{sum(1 for h in hasil_semua if h['status'] == 'BERHASIL')} berhasil, "
              f"{sum(1 for h in hasil_semua if h['status'] == 'GAGAL')} gagal, "
              f"{sum(1 for h in hasil_semua if h['status'] == 'TIDAK TERSEDIA')} tidak tersedia.")
        return 0 if ada_berhasil else 1

    if args.ask:
        if not args.prompt.strip():
            print("error: --ask butuh --prompt yang tidak kosong",
                  file=sys.stderr)
            return 2
        hasil = jalankan(args.kelas, args.tugas, args.prompt,
                         timeout=args.timeout, max_tokens=args.max_tokens)
        if args.json:
            print(json.dumps(hasil, ensure_ascii=False, indent=2))
        else:
            if hasil["ok"]:
                print(f"[OK] provider: {hasil['provider']} "
                      f"(model: {hasil['model']})")
                print(hasil["teks"])
            else:
                print(f"[GAGAL] {hasil['error']}")
                for pc in hasil["percobaan"]:
                    print(f"  - {pc['provider']}: {pc['status']}"
                          + (f" — {pc['error']}" if pc["error"] else ""))
        return 0 if hasil["ok"] else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
