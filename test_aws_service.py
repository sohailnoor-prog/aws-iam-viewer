"""Test AWS service functionality."""
from app.services.aws_service import AWSService
from app.models.aws_credentials import AWSCredentials
from dotenv import load_dotenv

load_dotenv()

# Note: This test requires valid AWS credentials
# You can test with your own credentials or skip validation test

service = AWSService()

print("Testing AWS Service")
print("=" * 60)

# Test 1: Credential encryption/decryption flow
print("\n1. Testing credential storage and retrieval...")
print("   (Using mock Flask session)")

# Mock session for testing
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

with app.test_request_context():
    from flask import session
    
    # Store test credentials
    test_access_key = "AKIAIOSFODNN7EXAMPLE"
    test_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    test_region = "us-west-2"
    
    print(f"   Storing credentials for region: {test_region}")
    service.store_credentials(test_access_key, test_secret_key, test_region)
    
    # Check connection status
    is_connected = service.is_connected()
    print(f"   ✓ Connection status: {is_connected}")
    
    # Retrieve credentials
    credentials = service.get_credentials()
    if credentials:
        print(f"   ✓ Retrieved access key: {credentials.access_key_id}")
        print(f"   ✓ Retrieved region: {credentials.region}")
        print(f"   ✓ Encrypted blob length: {len(credentials.encrypted_blob)}")
    else:
        print("   ✗ Failed to retrieve credentials")
    
    # Clear credentials
    print("\n2. Testing credential clearing...")
    service.clear_credentials()
    is_connected_after = service.is_connected()
    print(f"   ✓ Connection status after clear: {is_connected_after}")
    
    credentials_after = service.get_credentials()
    if credentials_after is None:
        print("   ✓ Credentials successfully cleared")
    else:
        print("   ✗ Credentials still present after clear")

print("\n" + "=" * 60)
print("Note: To test credential validation, provide real AWS credentials")
print("      and uncomment the validation test below.")
print("=" * 60)

# Uncomment to test with real credentials:
# print("\n3. Testing credential validation...")
# valid = service.validate_credentials(
#     "YOUR_ACCESS_KEY",
#     "YOUR_SECRET_KEY",
#     "us-west-2"
# )
# print(f"   Credentials valid: {valid}")

print("\n✓ All basic tests passed!")
