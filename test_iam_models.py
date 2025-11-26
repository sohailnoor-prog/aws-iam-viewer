"""Test IAM data models."""
from app.models.iam import IAMUser, IAMRole, Permission, PermissionStatement, Tag
from datetime import datetime

print("Testing IAM Data Models")
print("=" * 60)

# Test IAMUser
print("\n1. Testing IAMUser model...")
user = IAMUser(
    username="john.doe",
    user_id="AIDAI23HXS4WEXAMPLE",
    arn="arn:aws:iam::123456789012:user/john.doe",
    create_date=datetime.now(),
    password_last_used=datetime.now(),
    tags=[
        Tag(key="Department", value="Engineering"),
        Tag(key="Environment", value="Production")
    ]
)
print(f"   ✓ Created user: {user.username}")
print(f"   ✓ User ID: {user.user_id}")
print(f"   ✓ ARN: {user.arn}")
print(f"   ✓ Tags: {len(user.tags)}")

# Test IAMRole
print("\n2. Testing IAMRole model...")
role = IAMRole(
    role_name="EC2-Admin-Role",
    role_id="AROAI23HXS4WEXAMPLE",
    arn="arn:aws:iam::123456789012:role/EC2-Admin-Role",
    create_date=datetime.now(),
    assume_role_policy={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    },
    description="Admin role for EC2 instances",
    tags=[Tag(key="Application", value="WebServer")]
)
print(f"   ✓ Created role: {role.role_name}")
print(f"   ✓ Role ID: {role.role_id}")
print(f"   ✓ Description: {role.description}")
print(f"   ✓ Assume role policy statements: {len(role.assume_role_policy['Statement'])}")

# Test Permission and PermissionStatement
print("\n3. Testing Permission and PermissionStatement models...")
statement = PermissionStatement(
    effect="Allow",
    actions=["s3:GetObject", "s3:PutObject"],
    resources=["arn:aws:s3:::my-bucket/*"],
    conditions={"StringEquals": {"s3:x-amz-acl": "public-read"}}
)
print(f"   ✓ Created statement with effect: {statement.effect}")
print(f"   ✓ Actions: {len(statement.actions)}")
print(f"   ✓ Resources: {len(statement.resources)}")

permission = Permission(
    policy_name="S3-ReadWrite-Policy",
    policy_type="managed",
    policy_arn="arn:aws:iam::123456789012:policy/S3-ReadWrite-Policy",
    statements=[statement]
)
print(f"   ✓ Created permission: {permission.policy_name}")
print(f"   ✓ Policy type: {permission.policy_type}")
print(f"   ✓ Statements: {len(permission.statements)}")

# Test Tag
print("\n4. Testing Tag model...")
tag = Tag(key="Owner", value="DevOps Team")
print(f"   ✓ Created tag: {tag.key}={tag.value}")

print("\n" + "=" * 60)
print("✓ All IAM data models working correctly!")
