"""AWS credentials data model."""
from dataclasses import dataclass


@dataclass
class AWSCredentials:
    """AWS credentials for API access."""
    access_key_id: str
    secret_access_key: str
    region: str
    encrypted_blob: str = ""  # Encrypted version for session storage
