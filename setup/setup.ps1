# FastAPI Auth Setup Script (PowerShell)

# Cek Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python tidak ditemukan. Install Python 3.9+ dulu."
    exit 1
}
python --version

# Cek pip
python -m pip install --upgrade pip

# Cek virtualenv
if (-not (python -m pip show virtualenv)) {
    python -m pip install virtualenv
}

# Setup venv
if (-not (Test-Path venv)) {
    python -m virtualenv venv
}

# Install requirements
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Cek Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Docker tidak ditemukan. Install Docker: https://docs.docker.com/get-docker/"
    exit 1
}

# Jalankan Milvus
bash standalone_embed.sh start

Write-Host ""
Write-Host "[SETUP SELESAI]"
Write-Host "Aktifkan venv: .\venv\Scripts\Activate.ps1"
Write-Host "Jalankan server: uvicorn app.main:app --port 80"
Write-Host ""
Write-Host "[EDUKASI]"
Write-Host "- venv = virtual environment (isolasi python project)"
Write-Host "- Milvus = vector database, wajib running untuk fitur AI/face match"
Write-Host "- Untuk development, jalankan ulang setup.ps1 jika ada error dependency"
Write-Host "- Untuk production, gunakan reverse proxy (nginx) dan .env sesuai kebutuhan" 