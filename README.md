# FastAPI Auth & User Management API

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115%2B-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## 🇮🇩 Bahasa Indonesia | En English

**[ENGLISH BELOW](#english-version)**

---

## Deskripsi
API otentikasi & manajemen user berbasis FastAPI, mendukung:
- Role-based access (admin/user)
- API key security
- Integrasi AI (face recognition, spoofing)
- Email verifikasi
- Custom OpenAPI docs
- Milvus vector DB (via Docker)

---

## Fitur Utama
- Otentikasi & otorisasi (JWT & API Key)
- Admin-only user & API key creation
- AI endpoint dummy/real (face match, spoofing)
- Email notifikasi (SMTP, Mailtrap, Gmail)
- Custom OpenAPI untuk admin
- Setup multiplatform otomatis (`setup/`)

---

## Arsitektur
- **FastAPI** (backend utama)
- **Milvus** (vector DB, Docker)
- **insightface, transformers** (AI/ML)
- **SQLite** (default DB)
- **SMTP** (email)

---

## Setup & Instalasi
Lihat [setup/README.md](setup/README.md) untuk panduan otomatis (Linux, Mac, Windows).

---

## Cara Menjalankan
```bash
# Aktifkan venv
source venv/bin/activate
# Jalankan Milvus (jika belum)
bash standalone_embed.sh start
# Jalankan server
uvicorn app.main:app --port 80
```

---

## Struktur Folder
```
├── app/                # Source utama FastAPI
│   ├── ai_core/        # Modul AI/ML (face, spoofing)
│   ├── routes/         # API routes
│   ├── models/         # Model DB
│   └── core/           # Core logic
├── setup/              # Script setup otomatis & panduan
├── static/             # Static files (jika ada)
├── requirements.txt    # Dependency
├── standalone_embed.sh # Script Milvus (Docker)
├── app.db              # SQLite DB (jangan di-push)
└── ...
```

---

## Dokumentasi API
- Swagger UI: `/docs`
- Redoc: `/redoc`
- Custom OpenAPI (admin): `/openapi-admin?api_key=...`

**Contoh endpoint:**
- `POST /auth/login` — Login user
- `POST /auth/register` — Register user
- `POST /ai/face-match` — Face recognition
- `POST /ai/spoof-check` — Face spoofing detection

---

## Best Practice
- Gunakan `.env` untuk credentials/secret
- Jangan push file data, model, atau venv ke git
- Selalu gunakan venv (isolasi dependency)
- Untuk production: gunakan reverse proxy (nginx), HTTPS, dan harden security
- Lihat `.gitignore` untuk file yang diabaikan

---

## Kontributor
- [Nama Anda](https://github.com/USERNAME)
- Pull request & issue sangat diterima!

---

## Lisensi
MIT License

---

# English Version

## Description
FastAPI-based authentication & user management API with:
- Role-based access (admin/user)
- API key security
- AI integration (face recognition, spoofing)
- Email verification
- Custom OpenAPI docs
- Milvus vector DB (via Docker)

---

## Main Features
- Authentication & authorization (JWT & API Key)
- Admin-only user & API key creation
- AI endpoints (face match, spoofing)
- Email notification (SMTP, Mailtrap, Gmail)
- Custom OpenAPI for admin
- Multiplatform auto-setup (`setup/`)

---

## Architecture
- **FastAPI** (main backend)
- **Milvus** (vector DB, Docker)
- **insightface, transformers** (AI/ML)
- **SQLite** (default DB)
- **SMTP** (email)

---

## Setup & Installation
See [setup/README.md](setup/README.md) for automatic guide (Linux, Mac, Windows).

---

## How to Run
```bash
# Activate venv
source venv/bin/activate
# Run Milvus (if not running)
bash standalone_embed.sh start
# Run server
uvicorn app.main:app --port 80
```

---

## Folder Structure
```
├── app/                # Main FastAPI source
│   ├── ai_core/        # AI/ML modules (face, spoofing)
│   ├── routes/         # API routes
│   ├── models/         # DB models
│   └── core/           # Core logic
├── setup/              # Auto-setup scripts & guide
├── static/             # Static files (if any)
├── requirements.txt    # Dependencies
├── standalone_embed.sh # Milvus script (Docker)
├── app.db              # SQLite DB (do not push)
└── ...
```

---

## API Documentation
- Swagger UI: `/docs`
- Redoc: `/redoc`
- Custom OpenAPI (admin): `/openapi-admin?api_key=...`

**Example endpoints:**
- `POST /auth/login` — User login
- `POST /auth/register` — User registration
- `POST /ai/face-match` — Face recognition
- `POST /ai/spoof-check` — Face spoofing detection

---

## Best Practice
- Use `.env` for credentials/secrets
- Do not push data, model, or venv files to git
- Always use venv (dependency isolation)
- For production: use reverse proxy (nginx), HTTPS, and harden security
- See `.gitignore` for ignored files

---

## Contributors
- [Your Name](https://github.com/USERNAME)
- Pull requests & issues are welcome!

---

## License
MIT License 
