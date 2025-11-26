"""AWS Cognito authentication service."""
import boto3
from botocore.exceptions import ClientError
from typing import Optional
import os
from app.models.user import CognitoTokens, User
from datetime import datetime
import hmac
import hashlib
import base64


class CognitoAuthService:
    """Handles AWS Cognito authentication operations."""
    
    def __init__(self):
        """Initialize Cognito client."""
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('COGNITO_CLIENT_ID')
        self.client_secret = os.getenv('COGNITO_CLIENT_SECRET')
        self.region = os.getenv('COGNITO_REGION', 'us-east-1')
        
        self.client = boto3.client('cognito-idp', region_name=self.region)
    
    def _calculate_secret_hash(self, username: str) -> str:
        """Calculate SECRET_HASH for Cognito authentication."""
        message = username + self.client_id
        dig = hmac.new(
            self.client_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
    
    def authenticate_user(self, username: str, password: str) -> Optional[CognitoTokens]:
        """
        Authenticate user with Cognito.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            CognitoTokens if authentication successful, None otherwise
        """
        try:
            auth_params = {
                'USERNAME': username,
                'PASSWORD': password
            }
            
            # Add SECRET_HASH if client secret is configured
            if self.client_secret:
                auth_params['SECRET_HASH'] = self._calculate_secret_hash(username)
            
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters=auth_params
            )
            
            auth_result = response.get('AuthenticationResult')
            if not auth_result:
                return None
            
            return CognitoTokens(
                access_token=auth_result['AccessToken'],
                id_token=auth_result['IdToken'],
                refresh_token=auth_result['RefreshToken'],
                expires_in=auth_result['ExpiresIn']
            )
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['NotAuthorizedException', 'UserNotFoundException']:
                return None
            raise
    
    def validate_token(self, access_token: str) -> bool:
        """
        Validate Cognito access token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            True if token is valid, False otherwise
        """
        try:
            self.client.get_user(AccessToken=access_token)
            return True
        except ClientError:
            return False
    
    def refresh_token(self, refresh_token: str, username: str) -> Optional[CognitoTokens]:
        """
        Refresh expired access token.
        
        Args:
            refresh_token: Cognito refresh token
            username: Username for SECRET_HASH calculation
            
        Returns:
            New CognitoTokens if refresh successful, None otherwise
        """
        try:
            auth_params = {
                'REFRESH_TOKEN': refresh_token
            }
            
            # Add SECRET_HASH if client secret is configured
            if self.client_secret:
                auth_params['SECRET_HASH'] = self._calculate_secret_hash(username)
            
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters=auth_params
            )
            
            auth_result = response.get('AuthenticationResult')
            if not auth_result:
                return None
            
            return CognitoTokens(
                access_token=auth_result['AccessToken'],
                id_token=auth_result['IdToken'],
                refresh_token=refresh_token,  # Refresh token doesn't change
                expires_in=auth_result['ExpiresIn']
            )
            
        except ClientError:
            return None
    
    def get_user_attributes(self, access_token: str) -> Optional[dict]:
        """
        Get user attributes from access token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            Dictionary of user attributes or None if token invalid
        """
        try:
            response = self.client.get_user(AccessToken=access_token)
            
            # Convert attribute list to dictionary
            attributes = {}
            for attr in response.get('UserAttributes', []):
                attributes[attr['Name']] = attr['Value']
            
            return {
                'username': response['Username'],
                'attributes': attributes
            }
            
        except ClientError:
            return None
    
    def create_user_from_token(self, access_token: str) -> Optional[User]:
        """
        Create User object from access token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            User object or None if token invalid
        """
        user_data = self.get_user_attributes(access_token)
        if not user_data:
            return None
        
        attributes = user_data['attributes']
        
        return User(
            username=user_data['username'],
            email=attributes.get('email', ''),
            cognito_sub=attributes.get('sub', ''),
            user_pool_id=self.user_pool_id,
            created_at=datetime.now(),
            last_login=datetime.now(),
            attributes=attributes
        )
