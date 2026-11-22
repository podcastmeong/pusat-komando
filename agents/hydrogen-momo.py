#!/usr/bin/env python3
"""Momo di Gemini 4 Hydrogen (free tier) — agent runner sederhana.

Pakai: python3 hydrogen-momo.py "tugas yang harus dikerjakan"
  atau: echo "tugas..." | python3 hydrogen-momo.py
Membaca instruksi sistem dari data/instruksi-hydrogen-momo.md,
menggabungkannya dengan tugas, lalu memanggil gemini.py generate
dengan model gemini-4-hydrogen. Mencetak hanya teks jawabannya.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GEMINI_PY = Path.home() / "workspace/custom-connectors/custom.gemini/bin/gemini.py"
INSTRUKSI = REPO / "data/instruksi-hydrogen-momo.md"
MODEL = "gemini-4-hydrogen"


def main():
    if len(sys.argv) > 1:
        tugas = " ".join(sys.argv[1:])
    else:
        tugas = sys.stdin.read().strip()
    if not tugas:
        print("Berikan tugas sebagai argumen atau lewat stdin.", file=sys.stderr)
        sys.exit(2)
    instruksi = INSTRUKSI.read_text(encoding="utf-8").strip()
    prompt = instruksi + "\n\nTUGAS:\n" + tugas
    out = subprocess.run(
        [sys.executable, str(GEMINI_PY), "generate", "--model", MODEL, "--prompt", prompt],
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
