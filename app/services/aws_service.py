"""AWS connection and credential management service."""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional
from flask import session
from app.models.aws_credentials import AWSCredentials
from app.services.credential_manager import CredentialManager


class AWSService:
    """Manages AWS credential validation and IAM client creation."""
    
    def __init__(self):
        """Initialize AWS service with credential manager."""
        self.credential_manager = CredentialManager()
    
    def validate_credentials(self, access_key: str, secret_key: str, region: str) -> bool:
        """
        Validate AWS credentials using STS get_caller_identity.
        
        Args:
            access_key: AWS access key ID
            secret_key: AWS secret access key
            region: AWS region
            
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Create STS client with provided credentials
            sts_client = boto3.client(
                'sts',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            
            # Attempt to get caller identity
            response = sts_client.get_caller_identity()
            
            # If we get here, credentials are valid
            return True
            
        except (ClientError, NoCredentialsError):
            return False
        except Exception:
            return False
    
    def store_credentials(self, access_key: str, secret_key: str, region: str) -> None:
        """
        Encrypt and store AWS credentials in session.
        
        Args:
            access_key: AWS access key ID
            secret_key: AWS secret access key
            region: AWS region
        """
        # Create credentials dictionary
        credentials_dict = {
            'access_key_id': access_key,
            'secret_access_key': secret_key,
            'region': region
        }
        
        # Encrypt credentials
        encrypted = self.credential_manager.encrypt_credentials(credentials_dict)
        
        # Store in session
        session['aws_credentials'] = encrypted
        session['aws_connected'] = True
        session['aws_region'] = region
    
    def clear_credentials(self) -> None:
        """Clear AWS credentials from session."""
        session.pop('aws_credentials', None)
        session.pop('aws_connected', None)
        session.pop('aws_region', None)
    
    def get_credentials(self) -> Optional[AWSCredentials]:
        """
        Retrieve and decrypt AWS credentials from session.
        
        Returns:
            AWSCredentials object if credentials exist, None otherwise
        """
        encrypted = session.get('aws_credentials')
        if not encrypted:
            return None
        
        try:
            # Decrypt credentials
            credentials_dict = self.credential_manager.decrypt_credentials(encrypted)
            
            return AWSCredentials(
                access_key_id=credentials_dict['access_key_id'],
                secret_access_key=credentials_dict['secret_access_key'],
                region=credentials_dict['region'],
                encrypted_blob=encrypted
            )
        except ValueError:
            # Decryption failed, clear invalid credentials
            self.clear_credentials()
            return None
    
    def create_iam_client(self):
        """
        Create boto3 IAM client using stored credentials.
        
        Returns:
            boto3 IAM client or None if no credentials stored
            
        Raises:
            ValueError: If credentials are not stored in session
        """
        credentials = self.get_credentials()
        if not credentials:
            raise ValueError("No AWS credentials stored in session")
        
        return boto3.client(
            'iam',
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            region_name=credentials.region
        )
    
    def is_connected(self) -> bool:
        """
        Check if AWS credentials are stored and valid.
        
        Returns:
            True if connected, False otherwise
        """
        return session.get('aws_connected', False) and self.get_credentials() is not None
