"""Base Provider Adapter - Open Architecture Core"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class ProviderType(str, Enum):
    BETFAIR = "betfair"
    PINNACLE = "pinnacle"
    TIMEFORM = "timeform"
    RACING_POST = "racing_post"
    SPORTRADAR = "sportradar"
    CUSTOM_API = "custom_api"
    LOCAL_FILE = "local_file"

@dataclass
class ProviderConfig:
    provider_id: str
    provider_type: ProviderType
    name: str
    description: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    config_params: Optional[Dict[str, Any]] = None
    enabled: bool = True
    polling_interval_seconds: Optional[int] = None
    rate_limits: Optional[Dict[str, int]] = None

class ProviderAdapter(ABC):
    """All providers implement this interface - NO PRIVILEGE"""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.is_authenticated = False
        self.last_health_check: Optional[datetime] = None
        self.health_status: str = "unknown"
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """REAL API CALL ONLY"""
        pass
    
    @abstractmethod
    async def fetch_raw_data(self, **kwargs) -> Dict[str, Any]:
        """REAL API CALL ONLY"""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """REAL API TEST ONLY"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """REAL API CHECK ONLY"""
        pass
    
    @abstractmethod
    async def get_provider_schema(self) -> Dict[str, Any]:
        """Return provider schema"""
        pass
    
    def get_config(self) -> ProviderConfig:
        return self.config
    
    def is_healthy(self) -> bool:
        return self.health_status == "healthy"
