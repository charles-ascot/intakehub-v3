"""Provider models"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProviderConfigCreate(BaseModel):
    provider_type: str
    name: str
    description: Optional[str] = None
    enabled: bool = True

class ProviderConfig(BaseModel):
    id: str
    provider_type: str
    name: str
    enabled: bool
    class Config:
        from_attributes = True
