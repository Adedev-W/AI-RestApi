# Setup & Instalasi Otomatis FastAPI Auth

**🇮🇩 [Bahasa Indonesia](#deskripsi) | EN [English](#english-version)**

Panduan ini membantu Anda men-setup project secara otomatis di **Linux (semua distro), MacOS, dan Windows (CMD/PowerShell)**.

---

### 1. Struktur Folder
- `setup/setup.sh` → Untuk Linux/MacOS
- `setup/setup.bat` → Untuk Windows CMD
- `setup/setup.ps1` → Untuk Windows PowerShell

### 2. Langkah Cepat
#### Linux/MacOS
```bash
cd setup
chmod +x setup.sh
./setup.sh
```
#### Windows CMD
```
cd setup
setup.bat
```
#### Windows PowerShell
```
cd setup
./setup.ps1
```

---

### 3. Penjelasan Script
- **Cek Python 3.9+**: Wajib, semua fitur AI butuh Python >=3.9
- **Cek pip & virtualenv**: Untuk isolasi dependency
- **Install requirements**: Semua library di requirements.txt
- **Cek Docker**: Wajib untuk Milvus (vector DB)
- **Jalankan Milvus**: Otomatis via `standalone_embed.sh`
- **Petunjuk aktivasi venv & run server**: Disediakan di akhir script

---

### 4. Troubleshooting
- **Python tidak ditemukan**: Install Python 3.9+ dari https://www.python.org/downloads/
- **Docker tidak ditemukan**: Install Docker dari https://docs.docker.com/get-docker/
- **Permission denied**: Jalankan terminal sebagai administrator/root
- **Milvus tidak jalan**: Pastikan Docker running, cek dengan `docker ps`
- **Error dependency**: Jalankan ulang script setup

---

### 5. Edukasi & Best Practice
- **venv**: Virtual environment, isolasi python project
- **Milvus**: Vector database, wajib running untuk fitur AI/face match
- **Jangan install dependency global**: Selalu gunakan venv
- **Untuk production**: Gunakan reverse proxy (nginx) dan .env sesuai kebutuhan
- **Restart Milvus**: `bash standalone_embed.sh restart` (Linux/Mac), atau jalankan ulang script setup

---

### 6. Jalankan Server
Setelah setup selesai:
- **Aktifkan venv**
- **Jalankan server**

Contoh:
```bash
source venv/bin/activate
uvicorn app.main:app --port 80
```

---

Jika ada kendala, cek error message di terminal atau hubungi maintainer project.


---

## English

This guide helps you set up the project automatically on **Linux (all distros), MacOS, and Windows (CMD/PowerShell)**.

---

### 1. Folder Structure
- `setup/setup.sh` → For Linux/MacOS
- `setup/setup.bat` → For Windows CMD
- `setup/setup.ps1` → For Windows PowerShell

### 2. Quick Steps
#### Linux/MacOS
```bash
cd setup
chmod +x setup.sh
./setup.sh
```
#### Windows CMD
```
cd setup
setup.bat
```
#### Windows PowerShell
```
cd setup
./setup.ps1
```

---

### 3. Script Explanation
- **Check Python 3.9+**: Required, all AI features need Python >=3.9
- **Check pip & virtualenv**: For dependency isolation
- **Install requirements**: All libraries in requirements.txt
- **Check Docker**: Required for Milvus (vector DB)
- **Run Milvus**: Automatically via `standalone_embed.sh`
- **venv activation & server run instructions**: Provided at the end of the script

---

### 4. Troubleshooting
- **Python not found**: Install Python 3.9+ from https://www.python.org/downloads/
- **Docker not found**: Install Docker from https://docs.docker.com/get-docker/
- **Permission denied**: Run terminal as administrator/root
- **Milvus not running**: Make sure Docker is running, check with `docker ps`
- **Dependency error**: Re-run the setup script

---

### 5. Education & Best Practice
- **venv**: Virtual environment, isolates python project
- **Milvus**: Vector database, must be running for AI/face match features
- **Do not install dependencies globally**: Always use venv
- **For production**: Use a reverse proxy (nginx) and .env as needed
- **Restart Milvus**: `bash standalone_embed.sh restart` (Linux/Mac), or re-run the setup script

---

### 6. Run the Server
After setup is complete:
- **Activate venv**
- **Run the server**

Example:
```bash
source venv/bin/activate
uvicorn app.main:app --port 80
```

---

If you have issues, check the error message in the terminal or contact the project maintainer. 
