"""Health models"""
from pydantic import BaseModel
from typing import Optional

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    response_time_ms: Optional[int] = None
