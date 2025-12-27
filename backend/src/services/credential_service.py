"""Service: credential_service - Encrypted storage for provider credentials"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Credential
from src.config import settings
import json
import logging
from cryptography.fernet import Fernet
import base64
import hashlib

logger = logging.getLogger(__name__)

class CredentialService:
    def __init__(self):
        # Derive encryption key from settings.encryption_key
        key_hash = hashlib.sha256(settings.encryption_key.encode()).digest()
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(key_hash))
    
    def _encrypt(self, data: dict) -> str:
        """Encrypt credential data"""
        json_data = json.dumps(data)
        encrypted = self.cipher_suite.encrypt(json_data.encode())
        return encrypted.decode()
    
    def _decrypt(self, encrypted_data: str) -> dict:
        """Decrypt credential data"""
        decrypted = self.cipher_suite.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())
    
    async def store_credentials(self, db: AsyncSession, provider_id: str, cred_type: str, credentials: dict) -> Credential:
        """Store encrypted credentials for a provider"""
        try:
            encrypted = self._encrypt(credentials)
            cred = Credential(
                provider_id=provider_id,
                credential_type=cred_type,
                encrypted_data=encrypted
            )
            db.add(cred)
            await db.commit()
            await db.refresh(cred)
            logger.info(f"✅ Credentials stored for provider {provider_id}")
            return cred
        except Exception as e:
            logger.error(f"❌ Failed to store credentials: {e}")
            await db.rollback()
            raise
    
    async def get_credentials(self, db: AsyncSession, provider_id: str) -> dict:
        """Retrieve and decrypt credentials for a provider"""
        try:
            result = await db.execute(
                select(Credential).where(Credential.provider_id == provider_id)
            )
            cred = result.scalars().first()
            
            if not cred:
                logger.warning(f"⚠️ No credentials found for provider {provider_id}")
                return {}
            
            decrypted = self._decrypt(cred.encrypted_data)
            logger.info(f"✅ Credentials retrieved for provider {provider_id}")
            return decrypted
        except Exception as e:
            logger.error(f"❌ Failed to retrieve credentials: {e}")
            return {}
    
    async def delete_credentials(self, db: AsyncSession, provider_id: str) -> bool:
        """Delete credentials for a provider"""
        try:
            result = await db.execute(
                select(Credential).where(Credential.provider_id == provider_id)
            )
            cred = result.scalars().first()
            
            if cred:
                await db.delete(cred)
                await db.commit()
                logger.info(f"✅ Credentials deleted for provider {provider_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to delete credentials: {e}")
            await db.rollback()
            return False
