"""Input validators"""

def validate_provider_name(name: str) -> bool:
    return len(name) > 0 and len(name) <= 255
