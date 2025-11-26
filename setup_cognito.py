"""Script to set up AWS Cognito User Pool for IAM Viewer."""
import boto3
import json
from botocore.exceptions import ClientError

REGION = 'us-west-2'

def create_user_pool():
    """Create Cognito User Pool."""
    client = boto3.client('cognito-idp', region_name=REGION)
    
    try:
        print("Creating Cognito User Pool...")
        response = client.create_user_pool(
            PoolName='iam-viewer-user-pool',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': True
                }
            },
            AutoVerifiedAttributes=['email'],
            UsernameAttributes=['email'],
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Required': True,
                    'Mutable': True
                }
            ],
            AccountRecoverySetting={
                'RecoveryMechanisms': [
                    {
                        'Priority': 1,
                        'Name': 'verified_email'
                    }
                ]
            }
        )
        
        user_pool_id = response['UserPool']['Id']
        print(f"✓ User Pool created: {user_pool_id}")
        return user_pool_id
        
    except ClientError as e:
        print(f"✗ Error creating user pool: {e}")
        return None


def create_user_pool_client(user_pool_id):
    """Create User Pool App Client."""
    client = boto3.client('cognito-idp', region_name=REGION)
    
    try:
        print("\nCreating User Pool App Client...")
        response = client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='iam-viewer-client',
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH'
            ],
            GenerateSecret=False,  # Set to True if you want a client secret
            PreventUserExistenceErrors='ENABLED'
        )
        
        client_id = response['UserPoolClient']['ClientId']
        print(f"✓ App Client created: {client_id}")
        return client_id
        
    except ClientError as e:
        print(f"✗ Error creating app client: {e}")
        return None


def create_test_user(user_pool_id, username, email, temp_password):
    """Create a test user."""
    client = boto3.client('cognito-idp', region_name=REGION)
    
    try:
        print(f"\nCreating test user: {username}...")
        client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'}
            ],
            TemporaryPassword=temp_password,
            MessageAction='SUPPRESS'  # Don't send email
        )
        
        print(f"✓ Test user created: {username}")
        print(f"  Email: {email}")
        print(f"  Temporary password: {temp_password}")
        print(f"  Note: User will need to change password on first login")
        return True
        
    except ClientError as e:
        print(f"✗ Error creating test user: {e}")
        return False


def set_permanent_password(user_pool_id, username, password):
    """Set permanent password for user (skip password change requirement)."""
    client = boto3.client('cognito-idp', region_name=REGION)
    
    try:
        print(f"\nSetting permanent password for {username}...")
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )
        print(f"✓ Permanent password set")
        return True
        
    except ClientError as e:
        print(f"✗ Error setting password: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("AWS Cognito User Pool Setup for IAM Viewer")
    print(f"Region: {REGION}")
    print("=" * 60)
    
    # Create User Pool
    user_pool_id = create_user_pool()
    if not user_pool_id:
        return
    
    # Create App Client
    client_id = create_user_pool_client(user_pool_id)
    if not client_id:
        return
    
    # Create test user
    test_username = "testadmin"
    test_email = "testadmin@example.com"
    test_password = "TestPass123!"
    
    if create_test_user(user_pool_id, test_username, test_email, test_password):
        set_permanent_password(user_pool_id, test_username, test_password)
    
    # Print configuration
    print("\n" + "=" * 60)
    print("Setup Complete! Add these to your .env file:")
    print("=" * 60)
    print(f"COGNITO_USER_POOL_ID={user_pool_id}")
    print(f"COGNITO_CLIENT_ID={client_id}")
    print(f"COGNITO_CLIENT_SECRET=")
    print(f"COGNITO_REGION={REGION}")
    print(f"\nTest Credentials:")
    print(f"Username: {test_username}")
    print(f"Password: {test_password}")
    print("=" * 60)


if __name__ == "__main__":
    main()
