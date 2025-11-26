"""User model for administrator authentication."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Administrator user with Cognito attributes."""
    username: str
    email: str
    cognito_sub: str
    user_pool_id: str
    created_at: datetime
    last_login: Optional[datetime] = None
    attributes: dict = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


@dataclass
class CognitoTokens:
    """Cognito JWT tokens for session management."""
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
