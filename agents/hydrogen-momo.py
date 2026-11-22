#!/usr/bin/env python3
"""Runner agen pintar — satu runner, bisa pilih model (Hydrogen / Carbon).

Pakai: python3 hydrogen-momo.py [--model hydrogen|carbon] "tugas yang harus dikerjakan"
  atau: echo "tugas..." | python3 hydrogen-momo.py [--model hydrogen|carbon]
Membaca instruksi sistem dari data/instruksi-hydrogen-momo.md,
menggabungkannya dengan tugas, lalu memanggil gemini.py generate
dengan model yang dipilih. Mencetak hanya teks jawabannya.

MODEL (rencana kombinasi, perintah Cipta 22 Nov 2026 16:05 — untuk NANTI):
- hydrogen (default, GRATIS): gemini-4-hydrogen, free tier, ~20 panggilan/hari.
  Untuk tugas sehari-hari: riset, draf naskah, draf balasan, ringkasan.
- carbon (BERBAYAR, BELUM AKTIF): gemini-4-carbon, skor independen tertinggi.
  Peran yang dirancang (Cipta 16:06): OTAK STANDBY — menilai pesan masuk
  (email + DM) secara berkala: mana yang penting/urgent, lalu bertindak
  atau meneruskan. Standby itu sendiri adalah kerja sistem (cron +
  watchdog yang membangunkan agent); Carbon hanya otaknya.
  Biaya Carbon: $2/$10 per 1 juta token s.d. 30 Nov 2026, lalu $4/$20;
  kuota gratis 0. Standby terus-menerus dengan Carbon = biaya token
  jalan terus. Karena itu Carbon TERKUNCI: hanya jalan bila ada
  persetujuan biaya Cipta (file data/persetujuan-carbon.md ADA dan
  env SATUKIKI_CARBON_APPROVED=1). Tanpa itu, runner menolak
  dengan exit code 3 — JANGAN pernah mengakali kunci ini.
  Bila Cipta menyetujui nanti, yang diganti hanya model di pemanggil
  (cron standby: cek-pesan-masuk-sosial, cek-chat-customer-wa,
  cek-email-customer-cepat) dari --model hydrogen ke --model carbon.

Catatan jujur: Hydrogen free tier TIDAK STABIL saat beban tinggi
(22 Nov: 1x HTTP 503 overload + 1x read timeout; 1x berhasil).
Bila Hydrogen gagal, coba lagi sekali; bila tetap gagal, kerjakan
tugas secara langsung (koordinator/Muse) dan catat kegagalannya.
JANGAN pakai model berbayar sebagai jalan pintas.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GEMINI_PY = Path.home() / "workspace/custom-connectors/custom.gemini/bin/gemini.py"
INSTRUKSI = REPO / "data/instruksi-hydrogen-momo.md"
LOG_PAKAI = REPO / "data/log-penggunaan-model.jsonl"

MODELS = {
    "hydrogen": "gemini-4-hydrogen",
    "carbon": "gemini-4-carbon",
}
HYDROGEN_HARIAN_MAX = 20  # panggilan/hari, free tier (rencana Cipta 16:05)


def _log_pakai(model: str, tugas: str) -> None:
    """Catat pemakaian model (best-effort; gagal catat tidak menggagalkan tugas)."""
    try:
        with open(LOG_PAKAI, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "model": model,
                "tugas": tugas[:80],
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _hitung_hydrogen_hari_ini() -> int:
    """Hitung panggilan Hydrogen hari ini (WIB) dari log pemakaian."""
    try:
        hari = datetime.now(timezone.utc).astimezone().date().isoformat()
        n = 0
        with open(LOG_PAKAI, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if d.get("model") == "gemini-4-hydrogen" and d.get("ts", "")[:10] == hari:
                    n += 1
        return n
    except OSError:
        return 0


def main():
    ap = argparse.ArgumentParser(description="Runner agen pintar (Hydrogen/Carbon)")
    ap.add_argument("--model", choices=list(MODELS), default="hydrogen",
                    help="model yang dipakai (default: hydrogen, gratis)")
    ap.add_argument("tugas", nargs="*", help="tugas yang harus dikerjakan")
    args = ap.parse_args()
    tugas = " ".join(args.tugas)
    if not tugas:
        tugas = sys.stdin.read().strip()
    if not tugas:
        print("Berikan tugas sebagai argumen atau lewat stdin.", file=sys.stderr)
        sys.exit(2)

    model = MODELS[args.model]
    if args.model == "carbon":
        # KUNCI: Carbon berbayar — hanya bila Cipta menyetujui biayanya.
        persetujuan = REPO / "data/persetujuan-carbon.md"
        if os.environ.get("SATUKIKI_CARBON_APPROVED") != "1" or not persetujuan.exists():
            print("DITOLAK: Carbon berbayar ($2/$10 per 1 jt token s.d. 30 Nov 2026, "
                  "lalu $4/$20; kuota gratis 0) dan belum ada persetujuan biaya Cipta. "
                  "Pakai --model hydrogen (gratis).", file=sys.stderr)
            sys.exit(3)

    if args.model == "hydrogen":
        n = _hitung_hydrogen_hari_ini()
        if n >= 15:
            print(f"PERINGATAN: panggilan Hydrogen hari ini sudah {n} "
                  f"(batas free tier ~{HYDROGEN_HARIAN_MAX}/hari, dipakai BERSAMA "
                  f"semua agent — hemat untuk tugas penting). Tetap mencoba; "
                  f"bila API menolak, tunggu besok.", file=sys.stderr)

    instruksi = INSTRUKSI.read_text(encoding="utf-8").strip()
    prompt = instruksi + "\n\nTUGAS:\n" + tugas
    _log_pakai(model, tugas)
    out = subprocess.run(
        [sys.executable, str(GEMINI_PY), "generate", "--model", model, "--prompt", prompt],
        capture_output=True, text=True, timeout=300,
    )
    if out.returncode != 0:
        print(out.stderr.strip() or out.stdout.strip(), file=sys.stderr)
        sys.exit(1)
    data = json.loads(out.stdout)
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        print(json.dumps(data, indent=2, ensure_ascii=False))
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
