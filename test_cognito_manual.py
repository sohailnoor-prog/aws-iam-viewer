"""Manual test script for Cognito authentication."""
from app.services.cognito_auth import CognitoAuthService
from dotenv import load_dotenv

load_dotenv()

def test_authentication():
    """Test Cognito authentication flow."""
    service = CognitoAuthService()
    
    # Test with your credentials
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    print("\n1. Testing authentication...")
    tokens = service.authenticate_user(username, password)
    
    if tokens:
        print("✓ Authentication successful!")
        print(f"  Access token: {tokens.access_token[:50]}...")
        print(f"  Expires in: {tokens.expires_in} seconds")
        
        print("\n2. Testing token validation...")
        is_valid = service.validate_token(tokens.access_token)
        print(f"✓ Token valid: {is_valid}")
        
        print("\n3. Testing get user attributes...")
        user_data = service.get_user_attributes(tokens.access_token)
        if user_data:
            print(f"✓ Username: {user_data['username']}")
            print(f"  Email: {user_data['attributes'].get('email', 'N/A')}")
        
        print("\n4. Testing create user from token...")
        user = service.create_user_from_token(tokens.access_token)
        if user:
            print(f"✓ User created: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Cognito Sub: {user.cognito_sub}")
        
        print("\n5. Testing token refresh...")
        new_tokens = service.refresh_token(tokens.refresh_token, username)
        if new_tokens:
            print("✓ Token refresh successful!")
        else:
            print("✗ Token refresh failed")
    else:
        print("✗ Authentication failed - check credentials")

if __name__ == "__main__":
    test_authentication()
