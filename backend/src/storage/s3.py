"""AWS S3 Storage"""
from src.storage.base import StorageBackend
from typing import List
import logging

logger = logging.getLogger(__name__)

class S3StorageBackend(StorageBackend):
    """S3 Backend - REAL API"""
    def __init__(self, bucket_name: str, region: str = "us-east-1", access_key: str = None, secret_key: str = None):
        try:
            import boto3
            self.bucket_name = bucket_name
            self.region = region
            if access_key and secret_key:
                self.client = boto3.client('s3', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            else:
                self.client = boto3.client('s3', region_name=region)
            logger.info(f"✅ S3: {bucket_name}")
        except Exception as e:
            logger.error(f"S3 init failed: {e}")
            raise
    
    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        try:
            self.client.upload_file(local_path, self.bucket_name, remote_path)
            return True
        except Exception as e:
            logger.error(f"❌ S3 upload: {e}")
            return False
    
    async def download_file(self, remote_path: str, local_path: str) -> bool:
        try:
            self.client.download_file(self.bucket_name, remote_path, local_path)
            return True
        except Exception as e:
            logger.error(f"❌ S3 download: {e}")
            return False
    
    async def list_files(self, prefix: str = "") -> List[str]:
        try:
            files = []
            paginator = self.client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
            for page in pages:
                if 'Contents' in page:
                    files.extend([obj['Key'] for obj in page['Contents']])
            return files
        except Exception as e:
            logger.error(f"❌ S3 list: {e}")
            return []
    
    async def delete_file(self, remote_path: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=remote_path)
            return True
        except Exception as e:
            logger.error(f"❌ S3 delete: {e}")
            return False
    
    async def file_exists(self, remote_path: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=remote_path)
            return True
        except self.client.exceptions.NoSuchKey:
            return False
        except Exception as e:
            logger.error(f"❌ S3 exists: {e}")
            return False
    
    async def get_file_metadata(self, remote_path: str) -> dict:
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=remote_path)
            return {
                "size": response['ContentLength'],
                "last_modified": response['LastModified'].isoformat(),
                "path": remote_path,
                "exists": True
            }
        except Exception as e:
            logger.error(f"❌ S3 metadata: {e}")
            return {"exists": False}
