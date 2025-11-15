"""Context Engineering for EcoAgent - Advanced context management and compaction.

This module provides sophisticated context management including:
- Context summarization and compaction
- Relevance-based context filtering
- Context window optimization
- Hierarchical context organization
- Context lifecycle management
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
import json
import hashlib
from enum import Enum


class ContextImportance(Enum):
    """Importance levels for context items."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1


class ContextType(Enum):
    """Types of context items."""
    USER_PROFILE = "user_profile"
    CONVERSATION_HISTORY = "conversation_history"
    SUSTAINABILITY_GOALS = "sustainability_goals"
    SUSTAINABILITY_ACTIONS = "sustainability_actions"
    CARBON_FOOTPRINT = "carbon_footprint"
    RECOMMENDATIONS = "recommendations"
    OPERATION_STATE = "operation_state"
    PREFERENCES = "preferences"
    CONSTRAINTS = "constraints"
    METADATA = "metadata"


@dataclass
class ContextItem:
    """Individual context item with metadata."""
    key: str
    value: Any
    context_type: ContextType
    importance: ContextImportance
    timestamp: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    ttl_seconds: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if context item has expired."""
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def update_access(self):
        """Update access metadata."""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def get_age_seconds(self) -> float:
        """Get age of context item in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()
    
    def get_relevance_score(self) -> float:
        """
        Calculate relevance score based on importance, recency, and access patterns.
        Higher score = more relevant.
        """
        age_seconds = self.get_age_seconds()
        age_hours = age_seconds / 3600
        
        # Base score from importance
        base_score = self.importance.value * 20
        
        # Recency factor: newer is better (decay with time)
        recency_factor = 100 / (1 + age_hours / 24)  # Halves every 24 hours
        
        # Access frequency factor: frequently accessed is more relevant
        access_factor = min(self.access_count * 5, 30)
        
        # Total relevance score
        total_score = base_score + recency_factor + access_factor
        
        return total_score


@dataclass
class ContextSnapshot:
    """Snapshot of context at a point in time."""
    timestamp: datetime
    items: Dict[str, ContextItem]
    total_size_bytes: int = 0
    compression_ratio: float = 1.0
    hash_id: str = ""
    
    def calculate_size(self) -> int:
        """Calculate approximate size of context in bytes."""
        total = 0
        for item in self.items.values():
            try:
                total += len(json.dumps(item.value).encode('utf-8'))
            except (TypeError, ValueError):
                total += len(str(item.value).encode('utf-8'))
        return total
    
    def calculate_hash(self) -> str:
        """Calculate hash of context for deduplication."""
        content = json.dumps(
            {k: str(v.value) for k, v in self.items.items()},
            sort_keys=True,
            default=str
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class ContextCompactor:
    """Handles context compaction and summarization."""
    
    def __init__(self, max_context_tokens: int = 10000):
        """
        Initialize context compactor.
        
        Args:
            max_context_tokens: Maximum tokens to keep in context
        """
        self.max_context_tokens = max_context_tokens
        self.compression_history: List[Tuple[datetime, float]] = []
    
    def compact_context(
        self, 
        items: Dict[str, ContextItem],
        target_reduction: float = 0.3
    ) -> Dict[str, ContextItem]:
        """
        Compact context by removing low-relevance items.
        
        Args:
            items: Dictionary of context items
            target_reduction: Target reduction ratio (0.3 = reduce to 70%)
            
        Returns:
            Compacted context dictionary
        """
        # Score all items by relevance
        scored_items = [
            (key, item, item.get_relevance_score())
            for key, item in items.items()
        ]
        
        # Remove expired items first
        scored_items = [
            (k, i, s) for k, i, s in scored_items 
            if not i.is_expired()
        ]
        
        # Sort by relevance score (descending)
        scored_items.sort(key=lambda x: x[2], reverse=True)
        
        # Calculate target size
        original_size = len(scored_items)
        target_size = max(1, int(original_size * (1 - target_reduction)))
        
        # Keep top relevance items
        compacted = {
            key: item 
            for key, item, _ in scored_items[:target_size]
        }
        
        compression_ratio = len(compacted) / original_size if original_size > 0 else 1.0
        self.compression_history.append((datetime.now(), compression_ratio))
        
        return compacted
    
    def summarize_items(self, items: Dict[str, ContextItem]) -> Dict[str, str]:
        """
        Summarize context items into concise representations.
        
        Args:
            items: Dictionary of context items
            
        Returns:
            Dictionary of summarized items
        """
        summaries = {}
        
        for key, item in items.items():
            summary = self._summarize_item(item)
            summaries[key] = summary
        
        return summaries
    
    def _summarize_item(self, item: ContextItem) -> str:
        """Summarize a single context item."""
        if isinstance(item.value, dict):
            # For dictionaries, include key stats
            keys = list(item.value.keys())[:5]  # Top 5 keys
            return f"{item.context_type.value}: {len(item.value)} items, keys: {', '.join(keys)}"
        elif isinstance(item.value, list):
            # For lists, include length and first item
            first = str(item.value[0])[:50] if item.value else "empty"
            return f"{item.context_type.value}: {len(item.value)} items, first: {first}..."
        else:
            # For simple values, truncate
            value_str = str(item.value)[:100]
            return f"{item.context_type.value}: {value_str}"


class ContextWindow:
    """Manages context window for conversation."""
    
    def __init__(self, max_window_size: int = 8000):
        """
        Initialize context window.
        
        Args:
            max_window_size: Maximum size in tokens
        """
        self.max_window_size = max_window_size
        self.current_items: Dict[str, ContextItem] = {}
        self.compactor = ContextCompactor(max_window_size)
        self.snapshots: List[ContextSnapshot] = []
    
    def add_item(
        self,
        key: str,
        value: Any,
        context_type: ContextType,
        importance: ContextImportance = ContextImportance.MEDIUM,
        ttl_seconds: Optional[int] = None
    ) -> None:
        """
        Add item to context window.
        
        Args:
            key: Item key
            value: Item value
            context_type: Type of context
            importance: Importance level
            ttl_seconds: Time-to-live in seconds
        """
        expires_at = None
        if ttl_seconds:
            expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        
        self.current_items[key] = ContextItem(
            key=key,
            value=value,
            context_type=context_type,
            importance=importance,
            timestamp=datetime.now(),
            expires_at=expires_at,
            ttl_seconds=ttl_seconds
        )
    
    def get_item(self, key: str) -> Optional[ContextItem]:
        """Retrieve and update access for a context item."""
        item = self.current_items.get(key)
        if item and not item.is_expired():
            item.update_access()
            return item
        elif item and item.is_expired():
            del self.current_items[key]
        return None
    
    def remove_item(self, key: str) -> bool:
        """Remove item from context window."""
        if key in self.current_items:
            del self.current_items[key]
            return True
        return False
    
    def cleanup_expired(self) -> int:
        """Remove all expired items."""
        expired_keys = [
            key for key, item in self.current_items.items()
            if item.is_expired()
        ]
        for key in expired_keys:
            del self.current_items[key]
        return len(expired_keys)
    
    def optimize(self, target_reduction: float = 0.2) -> Dict[str, Any]:
        """
        Optimize context window.
        
        Args:
            target_reduction: Target reduction ratio
            
        Returns:
            Optimization report
        """
        before_size = len(self.current_items)
        
        # Remove expired items
        expired_count = self.cleanup_expired()
        
        # Compact if still too large
        if len(self.current_items) > 0:
            self.current_items = self.compactor.compact_context(
                self.current_items,
                target_reduction
            )
        
        after_size = len(self.current_items)
        
        return {
            "before_size": before_size,
            "after_size": after_size,
            "expired_removed": expired_count,
            "reduction_ratio": 1 - (after_size / before_size) if before_size > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of context window."""
        by_type = {}
        by_importance = {}
        
        for item in self.current_items.values():
            # Group by type
            type_key = item.context_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            # Group by importance
            imp_key = item.importance.name
            by_importance[imp_key] = by_importance.get(imp_key, 0) + 1
        
        return {
            "total_items": len(self.current_items),
            "by_type": by_type,
            "by_importance": by_importance,
            "timestamp": datetime.now().isoformat()
        }
    
    def take_snapshot(self) -> ContextSnapshot:
        """Take snapshot of current context."""
        snapshot = ContextSnapshot(
            timestamp=datetime.now(),
            items=dict(self.current_items)
        )
        snapshot.total_size_bytes = snapshot.calculate_size()
        snapshot.hash_id = snapshot.calculate_hash()
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_window_data(self) -> Dict[str, Any]:
        """Get all context data as dictionary."""
        return {
            key: {
                "value": item.value,
                "type": item.context_type.value,
                "importance": item.importance.name,
                "age_seconds": item.get_age_seconds(),
                "access_count": item.access_count
            }
            for key, item in self.current_items.items()
            if not item.is_expired()
        }


def compact_context(tool_context: ToolContext, target_reduction: float = 0.2) -> Dict[str, Any]:
    """
    Tool to compact context in the current session.
    
    Args:
        tool_context: The ADK tool context
        target_reduction: Target reduction ratio
        
    Returns:
        Compaction report
    """
    # Get or create context window from state
    if "context_window" not in tool_context.state:
        tool_context.state["context_window"] = ContextWindow()
    
    context_window = tool_context.state["context_window"]
    
    # Perform optimization
    report = context_window.optimize(target_reduction)
    
    return {
        "status": "Context compacted",
        **report
    }


def get_context_summary(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to get current context window summary.
    
    Args:
        tool_context: The ADK tool context
        
    Returns:
        Context summary
    """
    if "context_window" not in tool_context.state:
        return {"status": "No context window", "items": 0}
    
    context_window = tool_context.state["context_window"]
    return context_window.get_summary()


def get_context_data(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve all context data.
    
    Args:
        tool_context: The ADK tool context
        
    Returns:
        All context data
    """
    if "context_window" not in tool_context.state:
        return {}
    
    context_window = tool_context.state["context_window"]
    return context_window.get_window_data()


def manage_context_item(
    key: str,
    value: Any,
    context_type: str,
    importance: str = "MEDIUM",
    ttl_seconds: Optional[int] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Tool to manage individual context items.
    
    Args:
        key: Item key
        value: Item value
        context_type: Type of context (enum name)
        importance: Importance level (enum name)
        ttl_seconds: Time-to-live in seconds
        tool_context: The ADK tool context
        
    Returns:
        Operation status
    """
    if "context_window" not in tool_context.state:
        tool_context.state["context_window"] = ContextWindow()
    
    context_window = tool_context.state["context_window"]
    
    try:
        c_type = ContextType[context_type.upper()]
        importance_level = ContextImportance[importance.upper()]
    except KeyError as e:
        return {"status": "error", "message": f"Invalid enum value: {e}"}
    
    context_window.add_item(key, value, c_type, importance_level, ttl_seconds)
    
    return {
        "status": "Item added",
        "key": key,
        "context_type": c_type.value,
        "importance": importance_level.name
    }


def purge_context(
    context_type: Optional[str] = None,
    older_than_hours: Optional[int] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Tool to purge context items based on criteria.
    
    Args:
        context_type: Optional context type to filter
        older_than_hours: Optional age threshold in hours
        tool_context: The ADK tool context
        
    Returns:
        Purge report
    """
    if "context_window" not in tool_context.state:
        return {"status": "No context window", "purged": 0}
    
    context_window = tool_context.state["context_window"]
    keys_to_remove = []
    
    threshold_time = None
    if older_than_hours:
        threshold_time = datetime.now() - timedelta(hours=older_than_hours)
    
    for key, item in context_window.current_items.items():
        # Check type filter
        if context_type:
            try:
                target_type = ContextType[context_type.upper()]
                if item.context_type != target_type:
                    continue
            except KeyError:
                pass
        
        # Check age filter
        if threshold_time and item.timestamp < threshold_time:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        context_window.remove_item(key)
    
    return {
        "status": "Context purged",
        "purged_items": len(keys_to_remove),
        "remaining_items": len(context_window.current_items)
    }


# Define context engineering tools
context_engineering_tools = [
    compact_context,
    get_context_summary,
    get_context_data,
    manage_context_item,
    purge_context
]
