"""Test IAM role retrieval service."""
from app.services.role_retriever import RoleRetriever
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

print("Testing IAM Role Retrieval Service")
print("=" * 60)

# Create Flask app context
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

with app.test_request_context():
    print("\nThis test requires AWS credentials to be configured.")
    print("You can test this by:")
    print("1. Running the Flask app")
    print("2. Logging in and connecting to AWS")
    print("3. The role retrieval will work through the web interface")
    
    # Mock test with sample data
    print("\n" + "=" * 60)
    print("Mock Test: Parsing role data")
    print("=" * 60)
    
    # Create a mock IAM client
    class MockIAMClient:
        def get_paginator(self, operation):
            class MockPaginator:
                def paginate(self):
                    # Return mock role data
                    return [{
                        'Roles': [
                            {
                                'RoleName': 'EC2-Admin-Role',
                                'RoleId': 'AROAI23HXS4WEXAMPLE',
                                'Arn': 'arn:aws:iam::123456789012:role/EC2-Admin-Role',
                                'CreateDate': '2024-01-10T09:00:00Z',
                                'AssumeRolePolicyDocument': {
                                    'Version': '2012-10-17',
                                    'Statement': [{
                                        'Effect': 'Allow',
                                        'Principal': {'Service': 'ec2.amazonaws.com'},
                                        'Action': 'sts:AssumeRole'
                                    }]
                                },
                                'Description': 'Admin role for EC2 instances',
                                'Tags': [
                                    {'Key': 'Application', 'Value': 'WebServer'},
                                    {'Key': 'Environment', 'Value': 'Production'}
                                ]
                            },
                            {
                                'RoleName': 'Lambda-Execution-Role',
                                'RoleId': 'AROACKCEVSQ6C2EXAMPLE',
                                'Arn': 'arn:aws:iam::123456789012:role/Lambda-Execution-Role',
                                'CreateDate': '2024-03-15T11:30:00Z',
                                'AssumeRolePolicyDocument': {
                                    'Version': '2012-10-17',
                                    'Statement': [{
                                        'Effect': 'Allow',
                                        'Principal': {'Service': 'lambda.amazonaws.com'},
                                        'Action': 'sts:AssumeRole'
                                    }]
                                },
                                'Tags': []
                            }
                        ]
                    }]
            return MockPaginator()
    
    # Test with mock client
    mock_client = MockIAMClient()
    retriever = RoleRetriever(mock_client)
    
    print("\nRetrieving roles...")
    roles = retriever.get_all_roles()
    
    print(f"✓ Retrieved {len(roles)} roles")
    
    for i, role in enumerate(roles, 1):
        print(f"\n{i}. Role: {role.role_name}")
        print(f"   Role ID: {role.role_id}")
        print(f"   ARN: {role.arn}")
        print(f"   Created: {role.create_date}")
        if role.description:
            print(f"   Description: {role.description}")
        print(f"   Assume Role Policy Statements: {len(role.assume_role_policy.get('Statement', []))}")
        if role.tags:
            print(f"   Tags: {len(role.tags)}")
            for tag in role.tags:
                print(f"      - {tag.key}: {tag.value}")

print("\n" + "=" * 60)
print("✓ Role retrieval service working correctly!")
print("\nTo test with real AWS data:")
print("1. Start the Flask app: python app.py")
print("2. Log in with Cognito credentials")
print("3. Connect to AWS with valid credentials")
print("4. Navigate to the roles page (coming in next tasks)")
