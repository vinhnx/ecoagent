"""Tests for context engineering module."""

import pytest
from datetime import datetime, timedelta
from ecoagent.context_engineering import (
    ContextItem,
    ContextImportance,
    ContextType,
    ContextSnapshot,
    ContextCompactor,
    ContextWindow,
    compact_context,
    get_context_summary,
    get_context_data,
    manage_context_item,
    purge_context
)


class TestContextItem:
    """Tests for ContextItem."""
    
    def test_context_item_creation(self):
        """Test creating a context item."""
        item = ContextItem(
            key="test_key",
            value="test_value",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.HIGH,
            timestamp=datetime.now()
        )
        
        assert item.key == "test_key"
        assert item.value == "test_value"
        assert item.access_count == 0
        assert not item.is_expired()
    
    def test_context_item_expiration(self):
        """Test context item expiration."""
        past_time = datetime.now() - timedelta(hours=1)
        item = ContextItem(
            key="expired",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.MEDIUM,
            timestamp=past_time,
            expires_at=past_time
        )
        
        assert item.is_expired()
    
    def test_context_item_access_update(self):
        """Test updating access metadata."""
        item = ContextItem(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.MEDIUM,
            timestamp=datetime.now()
        )
        
        assert item.access_count == 0
        item.update_access()
        assert item.access_count == 1
        assert item.last_accessed is not None
    
    def test_context_item_age_calculation(self):
        """Test age calculation."""
        old_time = datetime.now() - timedelta(seconds=10)
        item = ContextItem(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.MEDIUM,
            timestamp=old_time
        )
        
        age = item.get_age_seconds()
        assert 9 < age < 11  # Allow for test execution time
    
    def test_relevance_score_calculation(self):
        """Test relevance score calculation."""
        item = ContextItem(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.CRITICAL,
            timestamp=datetime.now()
        )
        
        # Critical importance should give high score
        score1 = item.get_relevance_score()
        assert score1 > 0
        
        # Access should increase score
        item.update_access()
        score2 = item.get_relevance_score()
        assert score2 > score1


class TestContextSnapshot:
    """Tests for ContextSnapshot."""
    
    def test_snapshot_creation(self):
        """Test creating a context snapshot."""
        items = {
            "key1": ContextItem(
                key="key1",
                value={"data": "test"},
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.HIGH,
                timestamp=datetime.now()
            )
        }
        
        snapshot = ContextSnapshot(timestamp=datetime.now(), items=items)
        assert len(snapshot.items) == 1
        assert snapshot.total_size_bytes == 0  # Not calculated yet
    
    def test_snapshot_size_calculation(self):
        """Test size calculation."""
        items = {
            "key1": ContextItem(
                key="key1",
                value={"data": "test_value"},
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.HIGH,
                timestamp=datetime.now()
            )
        }
        
        snapshot = ContextSnapshot(timestamp=datetime.now(), items=items)
        size = snapshot.calculate_size()
        assert size > 0
    
    def test_snapshot_hash_calculation(self):
        """Test hash calculation for deduplication."""
        items = {
            "key1": ContextItem(
                key="key1",
                value={"data": "test"},
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.HIGH,
                timestamp=datetime.now()
            )
        }
        
        snapshot = ContextSnapshot(timestamp=datetime.now(), items=items)
        hash1 = snapshot.calculate_hash()
        assert hash1
        assert len(hash1) == 16


class TestContextCompactor:
    """Tests for ContextCompactor."""
    
    def test_compactor_initialization(self):
        """Test compactor initialization."""
        compactor = ContextCompactor(max_context_tokens=5000)
        assert compactor.max_context_tokens == 5000
        assert len(compactor.compression_history) == 0
    
    def test_compact_context_removes_expired(self):
        """Test that compaction removes expired items."""
        compactor = ContextCompactor()
        
        items = {
            "expired": ContextItem(
                key="expired",
                value="data",
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.LOW,
                timestamp=datetime.now() - timedelta(hours=1),
                expires_at=datetime.now() - timedelta(minutes=1)
            ),
            "valid": ContextItem(
                key="valid",
                value="data",
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.CRITICAL,
                timestamp=datetime.now()
            )
        }
        
        compacted = compactor.compact_context(items, target_reduction=0.0)
        assert "expired" not in compacted
        assert "valid" in compacted
    
    def test_compact_context_by_relevance(self):
        """Test compaction removes low-relevance items."""
        compactor = ContextCompactor()
        
        items = {
            "low": ContextItem(
                key="low",
                value="data",
                context_type=ContextType.METADATA,
                importance=ContextImportance.TRIVIAL,
                timestamp=datetime.now() - timedelta(hours=2)
            ),
            "high": ContextItem(
                key="high",
                value="data",
                context_type=ContextType.SUSTAINABILITY_GOALS,
                importance=ContextImportance.CRITICAL,
                timestamp=datetime.now()
            )
        }
        
        compacted = compactor.compact_context(items, target_reduction=0.5)
        assert "high" in compacted
        # Low might be removed due to 50% reduction target
    
    def test_summarize_items(self):
        """Test item summarization."""
        compactor = ContextCompactor()
        
        items = {
            "dict_item": ContextItem(
                key="dict_item",
                value={"key1": "val1", "key2": "val2"},
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.MEDIUM,
                timestamp=datetime.now()
            ),
            "list_item": ContextItem(
                key="list_item",
                value=["item1", "item2", "item3"],
                context_type=ContextType.SUSTAINABILITY_ACTIONS,
                importance=ContextImportance.MEDIUM,
                timestamp=datetime.now()
            )
        }
        
        summaries = compactor.summarize_items(items)
        assert "dict_item" in summaries
        assert "list_item" in summaries
        assert "dict_item" not in summaries["dict_item"]  # Summarized
        assert "3 items" in summaries["list_item"]


class TestContextWindow:
    """Tests for ContextWindow."""
    
    def test_context_window_creation(self):
        """Test creating a context window."""
        window = ContextWindow(max_window_size=5000)
        assert window.max_window_size == 5000
        assert len(window.current_items) == 0
    
    def test_add_item(self):
        """Test adding items to context window."""
        window = ContextWindow()
        window.add_item(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.HIGH
        )
        
        assert "test" in window.current_items
        assert window.current_items["test"].value == "data"
    
    def test_get_item(self):
        """Test retrieving items from context window."""
        window = ContextWindow()
        window.add_item(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE
        )
        
        item = window.get_item("test")
        assert item is not None
        assert item.value == "data"
        assert item.access_count == 1  # Access updated
    
    def test_get_item_not_found(self):
        """Test getting non-existent item."""
        window = ContextWindow()
        item = window.get_item("nonexistent")
        assert item is None
    
    def test_remove_item(self):
        """Test removing items."""
        window = ContextWindow()
        window.add_item(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE
        )
        
        removed = window.remove_item("test")
        assert removed
        assert "test" not in window.current_items
    
    def test_cleanup_expired(self):
        """Test cleaning up expired items."""
        window = ContextWindow()
        
        # Add expired item
        window.add_item(
            key="expired",
            value="data",
            context_type=ContextType.USER_PROFILE,
            ttl_seconds=0  # Immediately expires
        )
        
        import time
        time.sleep(0.1)  # Ensure expiration
        
        count = window.cleanup_expired()
        assert count > 0
        assert "expired" not in window.current_items
    
    def test_optimize_window(self):
        """Test context window optimization."""
        window = ContextWindow()
        
        # Add multiple items
        for i in range(10):
            window.add_item(
                key=f"item_{i}",
                value=f"data_{i}",
                context_type=ContextType.USER_PROFILE,
                importance=ContextImportance.MEDIUM
            )
        
        report = window.optimize(target_reduction=0.3)
        assert report["before_size"] == 10
        assert report["after_size"] <= 10
        assert "reduction_ratio" in report
    
    def test_get_summary(self):
        """Test getting context window summary."""
        window = ContextWindow()
        
        window.add_item(
            key="profile",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.CRITICAL
        )
        
        window.add_item(
            key="goals",
            value="data",
            context_type=ContextType.SUSTAINABILITY_GOALS,
            importance=ContextImportance.HIGH
        )
        
        summary = window.get_summary()
        assert summary["total_items"] == 2
        assert "by_type" in summary
        assert "by_importance" in summary
    
    def test_take_snapshot(self):
        """Test taking context snapshot."""
        window = ContextWindow()
        
        window.add_item(
            key="test",
            value={"data": "test"},
            context_type=ContextType.USER_PROFILE
        )
        
        snapshot = window.take_snapshot()
        assert snapshot is not None
        assert len(snapshot.items) == 1
        assert len(window.snapshots) == 1
    
    def test_get_window_data(self):
        """Test getting all window data."""
        window = ContextWindow()
        
        window.add_item(
            key="test",
            value="data",
            context_type=ContextType.USER_PROFILE,
            importance=ContextImportance.HIGH
        )
        
        data = window.get_window_data()
        assert "test" in data
        assert data["test"]["value"] == "data"
        assert data["test"]["importance"] == "HIGH"


class TestContextEngineeringTools:
    """Tests for context engineering tools."""
    
    def test_manage_context_item_tool(self):
        """Test manage_context_item tool."""
        # Mock tool context
        class MockToolContext:
            def __init__(self):
                self.state = {}
        
        tool_context = MockToolContext()
        
        result = manage_context_item(
            key="test",
            value="data",
            context_type="USER_PROFILE",
            importance="HIGH",
            tool_context=tool_context
        )
        
        assert result["status"] == "Item added"
        assert "context_window" in tool_context.state
    
    def test_get_context_summary_tool(self):
        """Test get_context_summary tool."""
        class MockToolContext:
            def __init__(self):
                self.state = {}
        
        tool_context = MockToolContext()
        
        # Without context window
        result = get_context_summary(tool_context)
        assert result["items"] == 0
        
        # With context window
        tool_context.state["context_window"] = ContextWindow()
        result = get_context_summary(tool_context)
        assert "total_items" in result
    
    def test_compact_context_tool(self):
        """Test compact_context tool."""
        class MockToolContext:
            def __init__(self):
                self.state = {"context_window": ContextWindow()}
        
        tool_context = MockToolContext()
        
        # Add some items
        context_window = tool_context.state["context_window"]
        for i in range(5):
            context_window.add_item(
                key=f"item_{i}",
                value=f"data_{i}",
                context_type=ContextType.USER_PROFILE
            )
        
        result = compact_context(tool_context, target_reduction=0.2)
        assert result["status"] == "Context compacted"
        assert "reduction_ratio" in result
    
    def test_purge_context_tool(self):
        """Test purge_context tool."""
        class MockToolContext:
            def __init__(self):
                self.state = {"context_window": ContextWindow()}
        
        tool_context = MockToolContext()
        context_window = tool_context.state["context_window"]
        
        # Add items with different ages
        context_window.add_item(
            key="old",
            value="data",
            context_type=ContextType.USER_PROFILE
        )
        
        result = purge_context(
            context_type="USER_PROFILE",
            older_than_hours=0,
            tool_context=tool_context
        )
        
        assert result["status"] == "Context purged"
        assert "purged_items" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
