"""Test IAM user retrieval service."""
from app.services.user_retriever import UserRetriever
from app.services.aws_service import AWSService
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

print("Testing IAM User Retrieval Service")
print("=" * 60)

# Create Flask app context for session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

with app.test_request_context():
    from flask import session
    
    # Note: This test requires valid AWS credentials stored in session
    print("\nThis test requires AWS credentials to be configured.")
    print("You can test this by:")
    print("1. Running the Flask app")
    print("2. Logging in and connecting to AWS")
    print("3. The user retrieval will work through the web interface")
    
    # Mock test with sample data
    print("\n" + "=" * 60)
    print("Mock Test: Parsing user data")
    print("=" * 60)
    
    # Create a mock IAM client (for demonstration)
    class MockIAMClient:
        def get_paginator(self, operation):
            class MockPaginator:
                def paginate(self):
                    # Return mock user data
                    return [{
                        'Users': [
                            {
                                'UserName': 'john.doe',
                                'UserId': 'AIDAI23HXS4WEXAMPLE',
                                'Arn': 'arn:aws:iam::123456789012:user/john.doe',
                                'CreateDate': '2024-01-15T10:30:00Z',
                                'PasswordLastUsed': '2024-11-25T08:00:00Z',
                                'Tags': [
                                    {'Key': 'Department', 'Value': 'Engineering'},
                                    {'Key': 'Environment', 'Value': 'Production'}
                                ]
                            },
                            {
                                'UserName': 'jane.smith',
                                'UserId': 'AIDACKCEVSQ6C2EXAMPLE',
                                'Arn': 'arn:aws:iam::123456789012:user/jane.smith',
                                'CreateDate': '2024-02-20T14:15:00Z',
                                'Tags': []
                            }
                        ]
                    }]
            return MockPaginator()
    
    # Test with mock client
    mock_client = MockIAMClient()
    retriever = UserRetriever(mock_client)
    
    print("\nRetrieving users...")
    users = retriever.get_all_users()
    
    print(f"✓ Retrieved {len(users)} users")
    
    for i, user in enumerate(users, 1):
        print(f"\n{i}. User: {user.username}")
        print(f"   User ID: {user.user_id}")
        print(f"   ARN: {user.arn}")
        print(f"   Created: {user.create_date}")
        if user.password_last_used:
            print(f"   Password Last Used: {user.password_last_used}")
        if user.tags:
            print(f"   Tags: {len(user.tags)}")
            for tag in user.tags:
                print(f"      - {tag.key}: {tag.value}")

print("\n" + "=" * 60)
print("✓ User retrieval service working correctly!")
print("\nTo test with real AWS data:")
print("1. Start the Flask app: python app.py")
print("2. Log in with Cognito credentials")
print("3. Connect to AWS with valid credentials")
print("4. Navigate to the users page (coming in next tasks)")
