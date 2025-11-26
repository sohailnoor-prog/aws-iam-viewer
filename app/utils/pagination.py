"""Pagination utility for IAM entity lists."""
from typing import List, TypeVar, Generic
from dataclasses import dataclass
from math import ceil

T = TypeVar('T')


@dataclass
class PaginatedResult(Generic[T]):
    """Paginated result container."""
    items: List[T]
    page: int
    per_page: int
    total_items: int
    total_pages: int
    has_prev: bool
    has_next: bool
    prev_page: int = None
    next_page: int = None


def paginate(items: List[T], page: int = 1, per_page: int = 50) -> PaginatedResult[T]:
    """
    Paginate a list of items.
    
    Args:
        items: List of items to paginate
        page: Current page number (1-indexed)
        per_page: Number of items per page (default: 50)
        
    Returns:
        PaginatedResult containing paginated items and metadata
    """
    # Ensure page is at least 1
    page = max(1, page)
    
    # Calculate total pages
    total_items = len(items)
    total_pages = ceil(total_items / per_page) if total_items > 0 else 1
    
    # Ensure page doesn't exceed total pages
    page = min(page, total_pages)
    
    # Calculate start and end indices
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get items for current page
    paginated_items = items[start_idx:end_idx]
    
    # Calculate navigation
    has_prev = page > 1
    has_next = page < total_pages
    prev_page = page - 1 if has_prev else None
    next_page = page + 1 if has_next else None
    
    return PaginatedResult(
        items=paginated_items,
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        prev_page=prev_page,
        next_page=next_page
    )
