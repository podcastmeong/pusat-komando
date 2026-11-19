#!/bin/bash
# deploy-oracle-pusat-komando.sh — Install Pusat Komando Podcast Meong di VM Oracle Cloud Always Free (Ubuntu).
# Dijalankan DI DALAM VM (sekali saja). VM-nya sendiri $0 (Always Free).
# Pusat Komando = 1 aplikasi Gradio berisi 12 agent bernomor + workshop Avatar Podcast (13 tab).
# Tanpa GEMINI_API_KEY, semua agent tetap jalan dalam mode template (knowledge-base + draf).
# Jalankan sebagai user biasa (ubuntu):  bash deploy-oracle-pusat-komando.sh
set -euo pipefail

APP_DIR="$HOME/pusat-komando"
PORT="${PORT:-7860}"

echo "== 1/6 Update sistem & pasang Python =="
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip git ufw

echo "== 2/6 Siapkan folder aplikasi =="
mkdir -p "$APP_DIR"
cd "$APP_DIR"
if [ ! -f app.py ]; then
  echo "Salin dulu SELURUH folder pusat-komando ke VM ini (app.py, requirements.txt,"
  echo "README.md, agents/, data/, output/), misalnya dengan:"
  echo "  scp -i kunci-ssh.pem -r app.py requirements.txt README.md agents data output ubuntu@IP-VM:~/pusat-komando/"
  echo "Lalu jalankan lagi script ini."
  exit 1
fi

echo "== 3/6 Buat venv & pasang dependensi =="
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

echo "== 4/6 Siapkan file .env (opsional) =="
if [ ! -f .env ]; then
  printf '# Opsional — tanpa key, agent jalan mode template.\n# GEMINI_API_KEY=key-dari-Google-AI-Studio\n' > .env
  echo "File .env dibuat. OPSIONAL: isi GEMINI_API_KEY di $APP_DIR/.env untuk mode AI penuh:"
  echo "  nano $APP_DIR/.env   (isi: GEMINI_API_KEY=key-dari-Google-AI-Studio)"
fi

echo "== 5/6 Pasang systemd service (jalan terus + restart otomatis) =="
sudo tee /etc/systemd/system/pusat-komando.service > /dev/null <<EOF
[Unit]
Description=Pusat Komando Podcast Meong
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
Environment=PORT=$PORT
ExecStart=$APP_DIR/.venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable pusat-komando
sudo systemctl restart pusat-komando

echo "== 6/6 Buka port firewall =="
sudo ufw allow ${PORT}/tcp || true
sudo ufw --force enable || true

echo ""
echo "SELESAI. Cek status:"
echo "  sudo systemctl status pusat-komando"
echo "  curl http://localhost:${PORT}/"
echo ""
echo "PENTING — 2 hal di konsol Oracle Cloud (https://cloud.oracle.com):"
echo "  1) Security List / Network Security Group subnet VM: tambah Ingress Rule"
echo "     TCP, port ${PORT}, source 0.0.0.0/0 — kalau tidak, Pusat Komando tidak bisa dibuka dari internet."
echo "  2) Pastikan VM yang dibuat bertipe Always Free (Ampere A1 / Micro) agar biayanya \$0."
echo "Akses Pusat Komando dari browser: http://IP-PUBLIK-VM:${PORT}/"
echo ""
echo "CATATAN: data agent (data/*.json) tersimpan di VM — backup berkala dengan:"
echo "  scp -i kunci-ssh.pem -r ubuntu@IP-PUBLIK-VM:~/pusat-komando/data ./backup-data/"
