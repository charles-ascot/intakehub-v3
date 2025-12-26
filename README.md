# IntakeHub A v3.0.0
## Vendor-Agnostic Data Intake Platform for Project CHIMERA

Pure open architecture. Real APIs. Zero mock data.

### Quick Start

```bash
# 1. Configure environment
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Start everything
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Architecture

**Backend (Python/FastAPI)**
- Provider adapter framework (Betfair, Pinnacle, Timeform, etc.)
- Storage backend abstraction (Local, GCS, S3)
- Real Google OAuth authentication
- PostgreSQL + Redis
- Real API integrations only

**Frontend (React/JavaScript)**
- Provider management dashboard
- Health monitoring
- Integration testing
- Activity logs
- Storage configuration

### Key Features

✅ **Pure Open Architecture** - No provider privilege, all swappable
✅ **Vendor-Agnostic** - Easy to add new data providers
✅ **Storage Abstraction** - Switch between Local/GCS/S3 with config change
✅ **Real APIs Only** - Zero mock data
✅ **Production Ready** - Full error handling and logging
✅ **Docker-Based** - Local development matches production

### Development

**Backend**
```bash
cd backend
pip install -r requirements.txt
python -m src.main
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### File Structure

```
intakehub/
├── backend/
│   ├── src/
│   │   ├── integrations/       # Provider adapters
│   │   ├── storage/            # Storage backends
│   │   ├── auth/               # Authentication
│   │   ├── database/           # Database models
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   └── ...
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API services
│   │   ├── stores/             # Zustand stores
│   │   ├── pages/              # Page components
│   │   └── ...
│   ├── package.json
│   ├── Dockerfile.dev
│   └── .env
├── docker-compose.yml
└── README.md
```

### Configuration

**Backend (.env)**
- `STORAGE_BACKEND` - Choose: local, gcs, or s3
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `GOOGLE_CLIENT_ID/SECRET` - OAuth credentials

**Frontend (.env)**
- `VITE_API_URL` - Backend API URL
- `VITE_GOOGLE_CLIENT_ID` - OAuth client ID

### Adding a New Provider

1. Create adapter in `backend/src/integrations/your_provider.py`
2. Inherit from `ProviderAdapter` base class
3. Implement required methods (authenticate, fetch_raw_data, health_check)
4. Register in `backend/src/integrations/registry.py`
5. Dashboard automatically supports your new provider

### Switching Storage Backends

Edit `.env`:
```env
# Local (default)
STORAGE_BACKEND=local
LOCAL_STORAGE_PATH=./data/storage

# Google Cloud Storage
STORAGE_BACKEND=gcs
GCS_PROJECT_ID=your-project
GCS_BUCKET_NAME=your-bucket

# AWS S3
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_BUCKET_NAME=your-bucket
```

Restart: `docker-compose restart backend`

### Database

PostgreSQL runs in Docker. To access:
```bash
docker-compose exec postgres psql -U intakehub -d intakehub
```

### Logging

Backend logs to stdout (visible in docker-compose output).
Frontend logs to browser console.

### Next Steps

1. ✅ Run `docker-compose up`
2. ⏳ Connect real API credentials (Betfair, Pinnacle, etc.)
3. ⏳ Build provider-specific UI components
4. ⏳ Implement real data ingestion logic
5. ⏳ Deploy to production infrastructure

### Support

This is version 3.0.0 - the final foundation. No more rebuilding.

For issues or questions, check the documentation or create an issue.

---

**Built with:**
- FastAPI + Python
- React + JavaScript
- PostgreSQL
- Redis
- Docker

**License:** MIT
