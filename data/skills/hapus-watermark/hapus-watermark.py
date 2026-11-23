#!/usr/bin/env python3
"""
hapus-watermark.py — Penghapus watermark video (untuk video hasil generate KITA SENDIRI).

ATURAN (Cipta, 23 Nov 2026):
- Hanya untuk video yang kita generate sendiri (Flow/Kling/Dreamina/dll).
- Menghapus watermark TIDAK memberi hak komersial. Output tier GRATIS
  (mis. Kling free: watermark + tanpa hak komersial) TETAP tidak boleh
  dipakai jualan — untuk jualan wajib paket berbayar (Kling Standard
  $8,80/bln). Alat ini hanya membersihkan tampilan untuk draf/uji
  non-komersial, atau video yang haknya memang sudah kita miliki.
- Jangan pernah dipakai untuk menghapus watermark milik kreator lain.

Metode:
  delogo  : filter ffmpeg delogo (cepat, tanpa unduhan) — default.
  inpaint : inpainting OpenCV Telea per frame (lebih halus, lebih lambat).
  crop    : potong strip bawah (kehilangan sedikit frame).

Preset (koordinat untuk 720x1280; disesuaikan otomatis bila resolusi beda):
  kling   : logo "KlingAI" kanan bawah.
  tiktok  : TIDAK didukung penuh — watermark TikTok berpindah posisi;
            delogo hanya menutup satu posisi tetap.

Pakai:
  hapus-watermark.py <video.mp4> [--preset kling] [--metode delogo|inpaint|crop]
                       [--box x,y,w,h] [--out hasil.mp4]
Keluar: <nama>-nowm.mp4 di folder yang sama.
Butuh: ffmpeg (+ cv2+numpy bila metode inpaint).
"""
import argparse
import os
import subprocess
import sys

PRESET = {
    # x, y, w, h pada kanvas 720x1280
    "kling": (540, 1205, 175, 65),
}


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height",
         "-of", "csv=p=0", path], capture_output=True, text=True)
    w, h = out.stdout.strip().split(",")
    return int(w), int(h)


def scale_box(box, w, h):
    x, y, bw, bh = box
    sx, sy = w / 720.0, h / 1280.0
    return (int(x * sx), int(y * sy), int(bw * sx), int(bh * sy))


def delogo(path, out, box):
    x, y, w, h = box
    vf = f"delogo=x={x}:y={y}:w={w}:h={h}:show=0"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", vf,
           "-c:a", "copy", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:500])
    return out


def crop_bottom(path, out, box):
    _, _, _, bh = box
    _, h = probe(path)
    vf = f"crop=iw:ih-{bh}:0:0"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", vf,
           "-c:a", "copy", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:500])
    return out


def inpaint(path, out, box):
    import cv2
    import numpy as np
    import tempfile
    x, y, w, h = box
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path,
                    os.path.join(tmp, "f-%04d.png")], check=True)
    mask = np.zeros((h, w), dtype=np.uint8)
    # mask hanya area watermark (relatif terhadap frame penuh)
    files = sorted(f for f in os.listdir(tmp) if f.startswith("f-"))
    for fn in files:
        img = cv2.imread(os.path.join(tmp, fn))
        m = np.zeros(img.shape[:2], dtype=np.uint8)
        m[y:y + h, x:x + w] = 255
        img2 = cv2.inpaint(img, m, 3, cv2.INPAINT_TELEA)
        cv2.imwrite(os.path.join(tmp, fn), img2)
    # rakit kembali + audio asli
    fps = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", fps,
           "-i", os.path.join(tmp, "f-%04d.png"), "-i", path,
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt",
           "yuv420p", "-c:a", "copy", "-shortest", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:500])
    return out


def main():
    ap = argparse.ArgumentParser(description="Hapus watermark video sendiri.")
    ap.add_argument("video")
    ap.add_argument("--preset", default="kling", choices=list(PRESET) + ["custom"])
    ap.add_argument("--metode", default="delogo", choices=["delogo", "inpaint", "crop"])
    ap.add_argument("--box", default="", help="x,y,w,h (untuk preset custom)")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    if a.preset == "custom":
        if not a.box:
            ap.error("--box wajib untuk preset custom")
        box0 = tuple(int(v) for v in a.box.split(","))
    else:
        box0 = PRESET[a.preset]
    w, h = probe(a.video)
    box = scale_box(box0, w, h)
    out = a.out or (os.path.splitext(a.video)[0] + "-nowm.mp4")
    print(f"video : {a.video} ({w}x{h})")
    print(f"box   : x={box[0]} y={box[1]} w={box[2]} h={box[3]}  metode={a.metode}")
    if a.metode == "delogo":
        delogo(a.video, out, box)
    elif a.metode == "crop":
        crop_bottom(a.video, out, box)
    else:
        inpaint(a.video, out, box)
    print(f"hasil : {out}")
    print("INGAT: hapus watermark TIDAK memberi hak komersial — "
          "output tier gratis tetap tidak boleh dipakai jualan.")


if __name__ == "__main__":
    main()
