"""Local Filesystem Storage"""
from src.storage.base import StorageBackend
from typing import List
import os
import logging
import aiofiles

logger = logging.getLogger(__name__)

class LocalStorageBackend(StorageBackend):
    def __init__(self, base_path: str = "./data/storage"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        logger.info(f"✅ Local storage: {os.path.abspath(self.base_path)}")
    
    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        try:
            full_path = os.path.join(self.base_path, remote_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            async with aiofiles.open(local_path, 'rb') as src:
                data = await src.read()
            async with aiofiles.open(full_path, 'wb') as dst:
                await dst.write(data)
            logger.info(f"📤 Uploaded: {remote_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            return False
    
    async def download_file(self, remote_path: str, local_path: str) -> bool:
        try:
            full_path = os.path.join(self.base_path, remote_path)
            async with aiofiles.open(full_path, 'rb') as src:
                data = await src.read()
            async with aiofiles.open(local_path, 'wb') as dst:
                await dst.write(data)
            return True
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return False
    
    async def list_files(self, prefix: str = "") -> List[str]:
        try:
            prefix_path = os.path.join(self.base_path, prefix) if prefix else self.base_path
            files = []
            for root, dirs, filenames in os.walk(prefix_path):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    relative = os.path.relpath(filepath, self.base_path)
                    files.append(relative)
            return files
        except Exception as e:
            logger.error(f"❌ List failed: {e}")
            return []
    
    async def delete_file(self, remote_path: str) -> bool:
        try:
            full_path = os.path.join(self.base_path, remote_path)
            os.remove(full_path)
            return True
        except Exception as e:
            logger.error(f"❌ Delete failed: {e}")
            return False
    
    async def file_exists(self, remote_path: str) -> bool:
        full_path = os.path.join(self.base_path, remote_path)
        return os.path.exists(full_path)
    
    async def get_file_metadata(self, remote_path: str) -> dict:
        try:
            full_path = os.path.join(self.base_path, remote_path)
            stat = os.stat(full_path)
            return {
                "size": stat.st_size,
                "last_modified": stat.st_mtime,
                "path": remote_path,
                "exists": True
            }
        except Exception as e:
            logger.error(f"❌ Metadata failed: {e}")
            return {"exists": False}
