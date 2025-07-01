@echo off
REM === FastAPI Auth Setup Script (Windows CMD) ===

REM Cek Python
where python
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak ditemukan. Install Python 3.9+ dulu.
    exit /b 1
)
python --version

REM Cek pip
python -m pip install --upgrade pip

REM Cek virtualenv
python -m pip show virtualenv >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    python -m pip install virtualenv
)

REM Setup venv
IF NOT EXIST venv (
    python -m virtualenv venv
)

REM Install requirements
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

REM Cek Docker
where docker
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker tidak ditemukan. Install Docker: https://docs.docker.com/get-docker/
    exit /b 1
)

REM Jalankan Milvus
bash standalone_embed.sh start

echo.
echo [SETUP SELESAI]
echo Aktifkan venv: call venv\Scripts\activate
echo Jalankan server: uvicorn app.main:app --port 80
echo.
echo [EDUKASI]
echo - venv = virtual environment (isolasi python project)
echo - Milvus = vector database, wajib running untuk fitur AI/face match
echo - Untuk development, jalankan ulang setup.bat jika ada error dependency
echo - Untuk production, gunakan reverse proxy (nginx) dan .env sesuai kebutuhan 