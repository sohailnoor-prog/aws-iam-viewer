"""IAM user retrieval service."""
from typing import List
from botocore.exceptions import ClientError
from app.models.iam import IAMUser, Tag
from datetime import datetime


class UserRetriever:
    """Retrieves IAM users from AWS."""
    
    def __init__(self, iam_client):
        """
        Initialize user retriever.
        
        Args:
            iam_client: boto3 IAM client
        """
        self.iam_client = iam_client
    
    def get_all_users(self) -> List[IAMUser]:
        """
        Retrieve all IAM users from AWS account with pagination.
        
        Returns:
            List of IAMUser objects
            
        Raises:
            ClientError: If AWS API call fails
        """
        users = []
        
        try:
            # Use paginator to handle accounts with many users
            paginator = self.iam_client.get_paginator('list_users')
            
            for page in paginator.paginate():
                for user_data in page.get('Users', []):
                    user = self._parse_user(user_data)
                    users.append(user)
            
            return users
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise ClientError(
                {'Error': {'Code': error_code, 'Message': f"Failed to retrieve users: {error_message}"}},
                'list_users'
            )
    
    def _parse_user(self, user_data: dict) -> IAMUser:
        """
        Parse AWS IAM user response into IAMUser object.
        
        Args:
            user_data: User data from AWS API
            
        Returns:
            IAMUser object
        """
        # Parse tags if present
        tags = []
        if 'Tags' in user_data:
            tags = [Tag(key=tag['Key'], value=tag['Value']) for tag in user_data['Tags']]
        
        # Parse password last used (may be None)
        password_last_used = None
        if 'PasswordLastUsed' in user_data:
            password_last_used = user_data['PasswordLastUsed']
        
        return IAMUser(
            username=user_data['UserName'],
            user_id=user_data['UserId'],
            arn=user_data['Arn'],
            create_date=user_data['CreateDate'],
            password_last_used=password_last_used,
            tags=tags
        )
