"""Provider Registry - Factory for adapters"""
from src.integrations.base import ProviderType, ProviderConfig, ProviderAdapter
from src.integrations.betfair import BetfairAdapter
from src.integrations.pinnacle import PinnacleAdapter
import logging

logger = logging.getLogger(__name__)

ADAPTER_REGISTRY = {
    ProviderType.BETFAIR: BetfairAdapter,
    ProviderType.PINNACLE: PinnacleAdapter,
}

def get_adapter(config: ProviderConfig) -> ProviderAdapter:
    adapter_class = ADAPTER_REGISTRY.get(config.provider_type)
    if not adapter_class:
        raise ValueError(f"No adapter for: {config.provider_type}")
    logger.info(f"Getting adapter: {config.provider_type} -> {adapter_class.__name__}")
    return adapter_class(config)

def register_adapter(provider_type: ProviderType, adapter_class):
    ADAPTER_REGISTRY[provider_type] = adapter_class
    logger.info(f"✅ Registered: {provider_type.value}")

def list_adapters():
    return {str(ptype): adapter_class.__name__ for ptype, adapter_class in ADAPTER_REGISTRY.items()}
