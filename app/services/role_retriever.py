"""IAM role retrieval service."""
from typing import List
from botocore.exceptions import ClientError
from app.models.iam import IAMRole, Tag
import json


class RoleRetriever:
    """Retrieves IAM roles from AWS."""
    
    def __init__(self, iam_client):
        """
        Initialize role retriever.
        
        Args:
            iam_client: boto3 IAM client
        """
        self.iam_client = iam_client
    
    def get_all_roles(self) -> List[IAMRole]:
        """
        Retrieve all IAM roles from AWS account with pagination.
        
        Returns:
            List of IAMRole objects
            
        Raises:
            ClientError: If AWS API call fails
        """
        roles = []
        
        try:
            # Use paginator to handle accounts with many roles
            paginator = self.iam_client.get_paginator('list_roles')
            
            for page in paginator.paginate():
                for role_data in page.get('Roles', []):
                    role = self._parse_role(role_data)
                    roles.append(role)
            
            return roles
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise ClientError(
                {'Error': {'Code': error_code, 'Message': f"Failed to retrieve roles: {error_message}"}},
                'list_roles'
            )
    
    def _parse_role(self, role_data: dict) -> IAMRole:
        """
        Parse AWS IAM role response into IAMRole object.
        
        Args:
            role_data: Role data from AWS API
            
        Returns:
            IAMRole object
        """
        # Parse tags if present
        tags = []
        if 'Tags' in role_data:
            tags = [Tag(key=tag['Key'], value=tag['Value']) for tag in role_data['Tags']]
        
        # Parse assume role policy document
        # It's URL-encoded JSON, need to decode it
        assume_role_policy = role_data.get('AssumeRolePolicyDocument', {})
        if isinstance(assume_role_policy, str):
            assume_role_policy = json.loads(assume_role_policy)
        
        # Description is optional
        description = role_data.get('Description')
        
        return IAMRole(
            role_name=role_data['RoleName'],
            role_id=role_data['RoleId'],
            arn=role_data['Arn'],
            create_date=role_data['CreateDate'],
            assume_role_policy=assume_role_policy,
            description=description,
            tags=tags
        )
