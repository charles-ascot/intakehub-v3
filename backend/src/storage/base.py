"""Base Storage Backend"""
from abc import ABC, abstractmethod
from typing import Optional, List

class StorageBackend(ABC):
    """All storage backends implement this - NO PRIVILEGE"""
    
    @abstractmethod
    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        pass
    
    @abstractmethod
    async def download_file(self, remote_path: str, local_path: str) -> bool:
        pass
    
    @abstractmethod
    async def list_files(self, prefix: str = "") -> List[str]:
        pass
    
    @abstractmethod
    async def delete_file(self, remote_path: str) -> bool:
        pass
    
    @abstractmethod
    async def file_exists(self, remote_path: str) -> bool:
        pass
    
    @abstractmethod
    async def get_file_metadata(self, remote_path: str) -> dict:
        pass
