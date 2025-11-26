"""IAM data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Tag:
    """AWS resource tag."""
    key: str
    value: str


@dataclass
class IAMUser:
    """IAM User entity."""
    username: str
    user_id: str
    arn: str
    create_date: datetime
    password_last_used: Optional[datetime] = None
    tags: List[Tag] = field(default_factory=list)


@dataclass
class IAMRole:
    """IAM Role entity."""
    role_name: str
    role_id: str
    arn: str
    create_date: datetime
    assume_role_policy: dict
    description: Optional[str] = None
    tags: List[Tag] = field(default_factory=list)


@dataclass
class PermissionStatement:
    """IAM policy statement."""
    effect: str  # "Allow" or "Deny"
    actions: List[str]
    resources: List[str]
    conditions: Optional[dict] = None


@dataclass
class Permission:
    """IAM permission (policy)."""
    policy_name: str
    policy_type: str  # "managed" or "inline"
    policy_arn: Optional[str] = None
    statements: List[PermissionStatement] = field(default_factory=list)
