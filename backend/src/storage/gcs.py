"""Google Cloud Storage"""
from src.storage.base import StorageBackend
from typing import List
import logging

logger = logging.getLogger(__name__)

class GoogleCloudStorageBackend(StorageBackend):
    """GCS Backend - REAL API"""
    def __init__(self, project_id: str, bucket_name: str, credentials_path: str = None):
        try:
            from google.cloud import storage
            self.project_id = project_id
            self.bucket_name = bucket_name
            if credentials_path:
                self.client = storage.Client(project=project_id, credentials_path=credentials_path)
            else:
                self.client = storage.Client(project=project_id)
            self.bucket = self.client.bucket(bucket_name)
            logger.info(f"✅ GCS: {bucket_name}")
        except Exception as e:
            logger.error(f"GCS init failed: {e}")
            raise
    
    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        try:
            blob = self.bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            return True
        except Exception as e:
            logger.error(f"❌ GCS upload: {e}")
            return False
    
    async def download_file(self, remote_path: str, local_path: str) -> bool:
        try:
            blob = self.bucket.blob(remote_path)
            blob.download_to_filename(local_path)
            return True
        except Exception as e:
            logger.error(f"❌ GCS download: {e}")
            return False
    
    async def list_files(self, prefix: str = "") -> List[str]:
        try:
            files = [blob.name for blob in self.client.list_blobs(self.bucket_name, prefix=prefix)]
            return files
        except Exception as e:
            logger.error(f"❌ GCS list: {e}")
            return []
    
    async def delete_file(self, remote_path: str) -> bool:
        try:
            self.bucket.blob(remote_path).delete()
            return True
        except Exception as e:
            logger.error(f"❌ GCS delete: {e}")
            return False
    
    async def file_exists(self, remote_path: str) -> bool:
        try:
            return self.bucket.blob(remote_path).exists()
        except Exception as e:
            logger.error(f"❌ GCS exists: {e}")
            return False
    
    async def get_file_metadata(self, remote_path: str) -> dict:
        try:
            blob = self.bucket.blob(remote_path)
            blob.reload()
            return {
                "size": blob.size,
                "last_modified": blob.updated.isoformat() if blob.updated else None,
                "path": remote_path,
                "exists": True
            }
        except Exception as e:
            logger.error(f"❌ GCS metadata: {e}")
            return {"exists": False}
