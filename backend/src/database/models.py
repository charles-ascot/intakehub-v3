"""SQLAlchemy ORM Models"""
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Provider(Base):
    __tablename__ = "providers"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, default=True)
    polling_interval_seconds = Column(Integer)
    config_params = Column(JSON)
    rate_limits = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Credential(Base):
    __tablename__ = "credentials"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String(36), nullable=False)
    credential_type = Column(String(50), nullable=False)  # e.g., "api_key", "username_password"
    encrypted_data = Column(Text, nullable=False)  # JSON encrypted
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String(36), nullable=False)
    health_status = Column(String(50))
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    actor = Column(String(255))
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(String(255))
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DataIngestion(Base):
    __tablename__ = "data_ingestions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String(36), nullable=False)
    ingestion_timestamp = Column(DateTime)
    record_count = Column(Integer)
    status = Column(String(50))
    error_message = Column(Text)
    raw_data_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
