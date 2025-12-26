"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    environment: str = "development"
    backend_port: int = 8000
    database_url: str
    redis_url: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    storage_backend: str = "local"
    gcs_project_id: Optional[str] = None
    gcs_bucket_name: Optional[str] = None
    gcs_credentials_path: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_bucket_name: Optional[str] = None
    aws_region: str = "us-east-1"
    local_storage_path: str = "./data/storage"
    encryption_key: str
    secret_key: str
    log_level: str = "INFO"
    gemini_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
