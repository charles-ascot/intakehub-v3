"""Custom errors"""

class IntakeHubException(Exception):
    pass

class ProviderException(IntakeHubException):
    pass

class StorageException(IntakeHubException):
    pass
