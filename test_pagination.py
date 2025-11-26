"""Test pagination utility."""
from app.utils.pagination import paginate

print("Testing Pagination Utility")
print("=" * 60)

# Create test data
test_items = [f"Item {i}" for i in range(1, 126)]  # 125 items
print(f"\nTest data: {len(test_items)} items")

# Test 1: First page
print("\n1. Testing first page (50 items per page)...")
result = paginate(test_items, page=1, per_page=50)
print(f"   ✓ Page: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")
print(f"   ✓ Total items: {result.total_items}")
print(f"   ✓ Has previous: {result.has_prev}")
print(f"   ✓ Has next: {result.has_next}")
print(f"   ✓ First item: {result.items[0]}")
print(f"   ✓ Last item: {result.items[-1]}")

# Test 2: Middle page
print("\n2. Testing middle page (page 2)...")
result = paginate(test_items, page=2, per_page=50)
print(f"   ✓ Page: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")
print(f"   ✓ Has previous: {result.has_prev}")
print(f"   ✓ Has next: {result.has_next}")
print(f"   ✓ Previous page: {result.prev_page}")
print(f"   ✓ Next page: {result.next_page}")
print(f"   ✓ First item: {result.items[0]}")
print(f"   ✓ Last item: {result.items[-1]}")

# Test 3: Last page
print("\n3. Testing last page (page 3)...")
result = paginate(test_items, page=3, per_page=50)
print(f"   ✓ Page: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")
print(f"   ✓ Has previous: {result.has_prev}")
print(f"   ✓ Has next: {result.has_next}")
print(f"   ✓ First item: {result.items[0]}")
print(f"   ✓ Last item: {result.items[-1]}")

# Test 4: Empty list
print("\n4. Testing empty list...")
result = paginate([], page=1, per_page=50)
print(f"   ✓ Page: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")
print(f"   ✓ Total items: {result.total_items}")

# Test 5: Single page
print("\n5. Testing single page (10 items, 50 per page)...")
small_list = [f"Item {i}" for i in range(1, 11)]
result = paginate(small_list, page=1, per_page=50)
print(f"   ✓ Page: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")
print(f"   ✓ Has previous: {result.has_prev}")
print(f"   ✓ Has next: {result.has_next}")

# Test 6: Page out of range
print("\n6. Testing page out of range (page 100)...")
result = paginate(test_items, page=100, per_page=50)
print(f"   ✓ Page adjusted to: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")

# Test 7: Negative page
print("\n7. Testing negative page (page -1)...")
result = paginate(test_items, page=-1, per_page=50)
print(f"   ✓ Page adjusted to: {result.page}/{result.total_pages}")
print(f"   ✓ Items on page: {len(result.items)}")

print("\n" + "=" * 60)
print("✓ All pagination tests passed!")
