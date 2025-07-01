#!/usr/bin/env bash
set -e

echo "[INFO] Cek Python 3.9+ ..."
if ! command -v python3 &>/dev/null; then
  echo "[ERROR] Python3 tidak ditemukan. Silakan install Python 3.9+ terlebih dahulu."
  exit 1
fi
PYVER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PYVER < 3.9" | bc) -eq 1 ]]; then
  echo "[ERROR] Python versi $PYVER terdeteksi. Minimal Python 3.9 diperlukan."
  exit 1
fi

echo "[INFO] Cek pip & virtualenv ..."
python3 -m pip install --upgrade pip
if ! python3 -m pip show virtualenv &>/dev/null; then
  python3 -m pip install virtualenv
fi

echo "[INFO] Membuat virtual environment (venv) ..."
if [ ! -d "venv" ]; then
  python3 -m virtualenv venv
fi

echo "[INFO] Aktivasi venv & install requirements ..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[INFO] Cek Docker ..."
if ! command -v docker &>/dev/null; then
  echo "[ERROR] Docker tidak ditemukan. Silakan install Docker: https://docs.docker.com/get-docker/"
  exit 1
fi

echo "[INFO] Jalankan Milvus Standalone ..."
bash standalone_embed.sh start

echo "\n[SETUP SELESAI]"
echo "Aktifkan venv: source venv/bin/activate"
echo "Jalankan server: uvicorn app.main:app --port 80"
echo "\n[EDUKASI]"
echo "- venv = virtual environment (isolasi python project)"
echo "- Milvus = vector database, wajib running untuk fitur AI/face match"
echo "- Untuk development, jalankan ulang setup.sh jika ada error dependency"
echo "- Untuk production, gunakan reverse proxy (nginx) dan .env sesuai kebutuhan" 