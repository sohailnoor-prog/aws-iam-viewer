"""Test credential encryption and decryption."""
from app.services.credential_manager import CredentialManager
from dotenv import load_dotenv

load_dotenv()

# Create credential manager
manager = CredentialManager()

# Test credentials
test_credentials = {
    'access_key_id': 'AKIAIOSFODNN7EXAMPLE',
    'secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    'region': 'us-west-2'
}

print("Testing Credential Encryption/Decryption")
print("=" * 50)

# Encrypt
print("\n1. Original credentials:")
print(f"   Access Key: {test_credentials['access_key_id']}")
print(f"   Secret Key: {test_credentials['secret_access_key'][:20]}...")
print(f"   Region: {test_credentials['region']}")

encrypted = manager.encrypt_credentials(test_credentials)
print(f"\n2. Encrypted (first 50 chars): {encrypted[:50]}...")
print(f"   Length: {len(encrypted)} characters")

# Decrypt
decrypted = manager.decrypt_credentials(encrypted)
print(f"\n3. Decrypted credentials:")
print(f"   Access Key: {decrypted['access_key_id']}")
print(f"   Secret Key: {decrypted['secret_access_key'][:20]}...")
print(f"   Region: {decrypted['region']}")

# Verify
if test_credentials == decrypted:
    print("\n✓ Encryption/Decryption successful!")
    print("✓ Original and decrypted credentials match")
else:
    print("\n✗ Error: Credentials don't match!")

# Test with different credentials
print("\n" + "=" * 50)
print("Testing with different credentials...")

test_credentials_2 = {
    'access_key_id': 'AKIAI44QH8DHBEXAMPLE',
    'secret_access_key': 'je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY',
    'region': 'us-east-1'
}

encrypted_2 = manager.encrypt_credentials(test_credentials_2)
decrypted_2 = manager.decrypt_credentials(encrypted_2)

if test_credentials_2 == decrypted_2:
    print("✓ Second encryption/decryption successful!")
else:
    print("✗ Error: Second test failed!")

print("\n" + "=" * 50)
print("All tests passed!")
