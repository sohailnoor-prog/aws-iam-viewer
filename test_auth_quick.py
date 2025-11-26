"""Quick test of Cognito authentication."""
from app.services.cognito_auth import CognitoAuthService
from dotenv import load_dotenv

load_dotenv()

service = CognitoAuthService()

print("Testing Cognito Authentication...")
print(f"User Pool: {service.user_pool_id}")
print(f"Client ID: {service.client_id}")
print(f"Region: {service.region}")

# Test with the created user
username = "testadmin@example.com"
password = "TestPass123!"

print(f"\nAuthenticating as: {username}")
tokens = service.authenticate_user(username, password)

if tokens:
    print("✓ Authentication successful!")
    print(f"  Access token (first 50 chars): {tokens.access_token[:50]}...")
    print(f"  Expires in: {tokens.expires_in} seconds")
    
    print("\nValidating token...")
    is_valid = service.validate_token(tokens.access_token)
    print(f"✓ Token is valid: {is_valid}")
    
    print("\nGetting user attributes...")
    user_data = service.get_user_attributes(tokens.access_token)
    if user_data:
        print(f"✓ Username: {user_data['username']}")
        print(f"  Email: {user_data['attributes'].get('email', 'N/A')}")
        print(f"  Sub: {user_data['attributes'].get('sub', 'N/A')}")
    
    print("\nCreating User object...")
    user = service.create_user_from_token(tokens.access_token)
    if user:
        print(f"✓ User object created:")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Cognito Sub: {user.cognito_sub}")
        print(f"  User Pool ID: {user.user_pool_id}")
else:
    print("✗ Authentication failed")
