"""Storage Factory - Select backend at runtime"""
from src.storage.base import StorageBackend
from src.storage.local import LocalStorageBackend
from src.config import settings
import logging

logger = logging.getLogger(__name__)

def get_storage_backend() -> StorageBackend:
    """Get configured storage backend"""
    if settings.storage_backend == "local":
        logger.info("🔧 Using Local Storage")
        return LocalStorageBackend(settings.local_storage_path)
    elif settings.storage_backend == "gcs":
        logger.info("🔧 Using Google Cloud Storage")
        from src.storage.gcs import GoogleCloudStorageBackend
        return GoogleCloudStorageBackend(settings.gcs_project_id, settings.gcs_bucket_name, settings.gcs_credentials_path)
    elif settings.storage_backend == "s3":
        logger.info("🔧 Using AWS S3")
        from src.storage.s3 import S3StorageBackend
        return S3StorageBackend(settings.aws_bucket_name, settings.aws_region, settings.aws_access_key_id, settings.aws_secret_access_key)
    else:
        raise ValueError(f"Unknown backend: {settings.storage_backend}")

storage_backend = None

def init_storage():
    global storage_backend
    storage_backend = get_storage_backend()
    return storage_backend

def get_storage() -> StorageBackend:
    if storage_backend is None:
        raise RuntimeError("Storage not initialized")
    return storage_backend
