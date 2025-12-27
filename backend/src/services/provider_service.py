"""Service: provider_service - Manage provider instances and adapters"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Provider, HealthCheck, AuditLog
from src.integrations.registry import get_adapter
from src.integrations.base import ProviderConfig, ProviderType
from src.services.credential_service import CredentialService
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)
credential_service = CredentialService()

class ProviderService:
    async def register_provider(self, db: AsyncSession, provider_type: str, name: str, description: str = None) -> Provider:
        """Register a new provider"""
        try:
            provider = Provider(
                provider_type=provider_type,
                name=name,
                description=description,
                enabled=True
            )
            db.add(provider)
            await db.commit()
            await db.refresh(provider)
            
            # Audit log
            await self._audit_log(db, "CREATE", "provider", provider.id, {"provider_type": provider_type, "name": name})
            
            logger.info(f"✅ Registered provider: {name} ({provider_type})")
            return provider
        except Exception as e:
            logger.error(f"❌ Failed to register provider: {e}")
            await db.rollback()
            raise
    
    async def get_provider(self, db: AsyncSession, provider_id: str) -> Provider:
        """Get provider by ID"""
        result = await db.execute(select(Provider).where(Provider.id == provider_id))
        return result.scalars().first()
    
    async def list_providers(self, db: AsyncSession) -> list:
        """List all providers"""
        result = await db.execute(select(Provider))
        return result.scalars().all()
    
    async def authenticate_provider(self, db: AsyncSession, provider_id: str, credentials: dict) -> bool:
        """Authenticate a provider and store credentials"""
        try:
            provider = await self.get_provider(db, provider_id)
            if not provider:
                logger.error(f"Provider {provider_id} not found")
                return False
            
            # Store encrypted credentials
            await credential_service.store_credentials(db, provider_id, "api_credentials", credentials)
            
            # Get adapter and authenticate
            config = ProviderConfig(
                provider_id=provider_id,
                provider_type=ProviderType(provider.provider_type),
                name=provider.name
            )
            adapter = get_adapter(config)
            success = await adapter.authenticate(credentials)
            
            if success:
                logger.info(f"✅ Authenticated provider: {provider.name}")
                await self._audit_log(db, "AUTHENTICATE", "provider", provider_id, {"status": "success"})
                return True
            else:
                logger.error(f"❌ Authentication failed for {provider.name}")
                await self._audit_log(db, "AUTHENTICATE", "provider", provider_id, {"status": "failed"})
                return False
                
        except Exception as e:
            logger.error(f"❌ Auth error: {e}")
            await self._audit_log(db, "AUTHENTICATE", "provider", provider_id, {"error": str(e)})
            return False
    
    async def fetch_provider_data(self, db: AsyncSession, provider_id: str, **kwargs) -> dict:
        """Fetch data from a provider"""
        try:
            provider = await self.get_provider(db, provider_id)
            if not provider:
                return {"error": "Provider not found"}
            
            # Get stored credentials
            creds = await credential_service.get_credentials(db, provider_id)
            if not creds:
                return {"error": "No credentials stored for this provider"}
            
            # Get adapter instance
            config = ProviderConfig(
                provider_id=provider_id,
                provider_type=ProviderType(provider.provider_type),
                name=provider.name
            )
            adapter = get_adapter(config)
            
            # Authenticate with stored credentials
            auth_success = await adapter.authenticate(creds)
            if not auth_success:
                return {"error": "Failed to authenticate with stored credentials"}
            
            # Fetch data
            data = await adapter.fetch_raw_data(**kwargs)
            
            # Log ingestion
            await self._log_ingestion(db, provider_id, "success", len(str(data)))
            
            logger.info(f"✅ Fetched data from {provider.name}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Fetch error: {e}")
            await self._log_ingestion(db, provider_id, "error", 0, str(e))
            return {"error": str(e)}
    
    async def health_check_provider(self, db: AsyncSession, provider_id: str) -> dict:
        """Check provider health"""
        try:
            provider = await self.get_provider(db, provider_id)
            if not provider:
                return {"status": "unavailable"}
            
            # Get credentials
            creds = await credential_service.get_credentials(db, provider_id)
            
            # Get adapter
            config = ProviderConfig(
                provider_id=provider_id,
                provider_type=ProviderType(provider.provider_type),
                name=provider.name
            )
            adapter = get_adapter(config)
            
            # Authenticate if credentials exist
            if creds:
                await adapter.authenticate(creds)
            
            # Check health
            health = await adapter.health_check()
            
            # Store health check result
            status = health.get("status", "unknown")
            response_time = health.get("response_time_ms", 0)
            
            hc = HealthCheck(
                provider_id=provider_id,
                health_status=status,
                response_time_ms=response_time
            )
            db.add(hc)
            await db.commit()
            
            return health
            
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _audit_log(self, db: AsyncSession, action: str, resource_type: str, resource_id: str, details: dict = None):
        """Log an action to audit log"""
        try:
            log = AuditLog(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details
            )
            db.add(log)
            await db.commit()
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    async def _log_ingestion(self, db: AsyncSession, provider_id: str, status: str, record_count: int = 0, error_msg: str = None):
        """Log a data ingestion event"""
        try:
            from src.database.models import DataIngestion
            ingestion = DataIngestion(
                provider_id=provider_id,
                status=status,
                record_count=record_count,
                error_message=error_msg,
                ingestion_timestamp=datetime.utcnow()
            )
            db.add(ingestion)
            await db.commit()
        except Exception as e:
            logger.error(f"Failed to log ingestion: {e}")
