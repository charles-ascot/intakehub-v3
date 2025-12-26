"""IntakeHub A v3.0.0 - FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import settings
from src.database.connection import init_db

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("🚀 Initializing IntakeHub backend...")
        await init_db()
        logger.info("✅ Database initialized")
        logger.info(f"📦 Storage backend: {settings.storage_backend}")
        yield
    finally:
        logger.info("🛑 Shutting down...")

app = FastAPI(
    title="IntakeHub A v3.0.0",
    description="Vendor-agnostic data intake platform",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "IntakeHub A v3.0.0",
        "environment": settings.environment
    }

@app.get("/api/version")
async def version():
    return {"version": "3.0.0"}

@app.get("/api/config")
async def config():
    return {
        "storage_backend": settings.storage_backend,
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.backend_port)
