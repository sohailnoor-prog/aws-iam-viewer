"""IAM service orchestration layer."""
from typing import List, Optional
from app.models.iam import IAMUser, IAMRole
from app.services.user_retriever import UserRetriever
from app.services.role_retriever import RoleRetriever
from app.services.aws_service import AWSService
from datetime import datetime, timedelta


class IAMService:
    """Orchestrates IAM data retrieval with caching."""
    
    def __init__(self):
        """Initialize IAM service."""
        self.aws_service = AWSService()
        self._users_cache = None
        self._users_cache_time = None
        self._roles_cache = None
        self._roles_cache_time = None
        self.cache_ttl = timedelta(minutes=5)  # 5-minute cache TTL
    
    def get_all_users(self, use_cache: bool = True) -> List[IAMUser]:
        """
        Get all IAM users with caching.
        
        Args:
            use_cache: Whether to use cached data if available
            
        Returns:
            List of IAMUser objects
        """
        # Check cache
        if use_cache and self._is_cache_valid(self._users_cache_time):
            return self._users_cache
        
        # Retrieve from AWS
        iam_client = self.aws_service.create_iam_client()
        retriever = UserRetriever(iam_client)
        users = retriever.get_all_users()
        
        # Update cache
        self._users_cache = users
        self._users_cache_time = datetime.now()
        
        return users
    
    def get_all_roles(self, use_cache: bool = True) -> List[IAMRole]:
        """
        Get all IAM roles with caching.
        
        Args:
            use_cache: Whether to use cached data if available
            
        Returns:
            List of IAMRole objects
        """
        # Check cache
        if use_cache and self._is_cache_valid(self._roles_cache_time):
            return self._roles_cache
        
        # Retrieve from AWS
        iam_client = self.aws_service.create_iam_client()
        retriever = RoleRetriever(iam_client)
        roles = retriever.get_all_roles()
        
        # Update cache
        self._roles_cache = roles
        self._roles_cache_time = datetime.now()
        
        return roles
    
    def _is_cache_valid(self, cache_time: Optional[datetime]) -> bool:
        """
        Check if cache is still valid.
        
        Args:
            cache_time: Time when cache was last updated
            
        Returns:
            True if cache is valid, False otherwise
        """
        if cache_time is None:
            return False
        
        age = datetime.now() - cache_time
        return age < self.cache_ttl
    
    def clear_cache(self):
        """Clear all cached data."""
        self._users_cache = None
        self._users_cache_time = None
        self._roles_cache = None
        self._roles_cache_time = None
