# FastAPI O2Auth REST API

## Setup

1. Buat virtual environment (sudah disediakan di `venv/`):
   ```bash
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan db vector dan server:
   ```
   bash standalone_embed.sh start
   ```
   ```bash
   uvicorn app.main:app --port 80
   ```
   

## Fitur
- O2Auth Security Middleware
- Email verifikasi ke user (IP address, device log)

---

Struktur project dan instruksi lebih lanjut akan ditambahkan. 