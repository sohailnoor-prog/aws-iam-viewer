"""Credential encryption and decryption service."""
from cryptography.fernet import Fernet
import base64
import hashlib
import os
import json


class CredentialManager:
    """Manages encryption and decryption of AWS credentials."""
    
    def __init__(self, secret_key: str = None):
        """
        Initialize credential manager with encryption key.
        
        Args:
            secret_key: Flask secret key to derive encryption key from
        """
        if secret_key is None:
            secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
        
        # Derive a Fernet-compatible key from the Flask secret key
        self.encryption_key = self._derive_key(secret_key)
        self.cipher = Fernet(self.encryption_key)
    
    def _derive_key(self, secret_key: str) -> bytes:
        """
        Derive a Fernet-compatible encryption key from Flask secret key.
        
        Args:
            secret_key: Flask secret key
            
        Returns:
            Base64-encoded 32-byte key suitable for Fernet
        """
        # Use SHA256 to create a 32-byte hash
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        # Fernet requires base64-encoded key
        return base64.urlsafe_b64encode(key_hash)
    
    def encrypt_credentials(self, credentials: dict) -> str:
        """
        Encrypt AWS credentials dictionary.
        
        Args:
            credentials: Dictionary containing AWS credentials
                        (access_key_id, secret_access_key, region)
        
        Returns:
            Encrypted credentials as base64-encoded string
        """
        # Convert credentials dict to JSON string
        credentials_json = json.dumps(credentials)
        
        # Encrypt the JSON string
        encrypted_data = self.cipher.encrypt(credentials_json.encode())
        
        # Return as base64 string for easy storage
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_credentials(self, encrypted_credentials: str) -> dict:
        """
        Decrypt AWS credentials.
        
        Args:
            encrypted_credentials: Base64-encoded encrypted credentials string
            
        Returns:
            Dictionary containing decrypted AWS credentials
            
        Raises:
            ValueError: If decryption fails or data is invalid
        """
        try:
            # Decode from base64
            encrypted_data = base64.urlsafe_b64decode(encrypted_credentials.encode())
            
            # Decrypt the data
            decrypted_json = self.cipher.decrypt(encrypted_data).decode()
            
            # Parse JSON back to dictionary
            credentials = json.loads(decrypted_json)
            
            return credentials
            
        except Exception as e:
            raise ValueError(f"Failed to decrypt credentials: {str(e)}")
