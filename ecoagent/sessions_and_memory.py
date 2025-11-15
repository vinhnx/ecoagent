"""Sessions and Memory Management for EcoAgent.

This module provides:
- Session management with lifecycle control
- Long-term memory bank for user information
- Memory organization and retrieval
- Session state persistence and recovery
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from enum import Enum
import json
import uuid
from abc import ABC, abstractmethod


class SessionStatus(Enum):
    """Session lifecycle states."""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    EXPIRED = "expired"


class MemoryType(Enum):
    """Types of memories stored in the memory bank."""
    EPISODIC = "episodic"      # Specific events/conversations
    SEMANTIC = "semantic"       # Facts, knowledge, preferences
    PROCEDURAL = "procedural"   # How-to, processes, patterns
    EMOTIONAL = "emotional"     # Feelings, reactions, sentiment
    RELATIONAL = "relational"   # User goals, values, relationships


class MemoryImportance(Enum):
    """Importance levels for memories."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1


@dataclass
class Memory:
    """Represents a single memory in the memory bank."""
    id: str
    memory_type: MemoryType
    content: str
    context: Dict[str, Any]
    importance: MemoryImportance
    timestamp: datetime
    source: str  # Where the memory came from (e.g., "user_input", "inference")
    tags: List[str] = field(default_factory=list)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    decay_factor: float = 1.0  # How much this memory has decayed (0-1)
    relationships: List[str] = field(default_factory=list)  # IDs of related memories
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_age_days(self) -> float:
        """Get age of memory in days."""
        return (datetime.now() - self.timestamp).total_seconds() / 86400
    
    def update_access(self) -> None:
        """Update access metadata."""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def apply_decay(self, days_old: float) -> None:
        """Apply time-based decay to memory strength."""
        # Decay formula: strength decreases over time
        # After 30 days: 50%, after 90 days: 25%
        decay_rate = 0.977  # ~2.3% per day
        self.decay_factor = max(0.1, (decay_rate ** days_old))
    
    def get_strength(self) -> float:
        """Get current memory strength (0-1)."""
        age_days = self.get_age_days()
        self.apply_decay(age_days)
        
        # Strength combines importance, recency, and access
        importance_factor = (self.importance.value / 5.0)
        recency_factor = self.decay_factor
        access_factor = min(self.access_count * 0.05, 1.0)
        
        # Weighted average
        strength = (importance_factor * 0.5 + recency_factor * 0.3 + access_factor * 0.2)
        return min(1.0, strength)


@dataclass
class Session:
    """Represents a user session."""
    id: str
    user_id: str
    status: SessionStatus = SessionStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    paused_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    ttl_seconds: int = 3600  # Default 1 hour
    messages: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    total_interactions: int = 0
    
    def activate(self) -> None:
        """Activate session."""
        self.status = SessionStatus.ACTIVE
        self.started_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
    
    def pause(self) -> None:
        """Pause session."""
        self.status = SessionStatus.PAUSED
        self.paused_at = datetime.now()
    
    def resume(self) -> None:
        """Resume paused session."""
        if self.status == SessionStatus.PAUSED:
            self.status = SessionStatus.ACTIVE
            self.expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
    
    def close(self) -> None:
        """Close session."""
        self.status = SessionStatus.CLOSED
        self.closed_at = datetime.now()
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def is_active(self) -> bool:
        """Check if session is currently active."""
        return self.status == SessionStatus.ACTIVE and not self.is_expired()
    
    def get_duration_seconds(self) -> float:
        """Get session duration in seconds."""
        start = self.started_at or self.created_at
        end = self.closed_at or datetime.now()
        return (end - start).total_seconds()
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """Add message to session."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        self.total_interactions += 1
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of session context."""
        return {
            "total_interactions": self.total_interactions,
            "total_messages": len(self.messages),
            "duration_seconds": self.get_duration_seconds(),
            "status": self.status.value,
            "context_keys": list(self.context.keys())
        }


class MemoryBank:
    """Manages long-term user memories."""
    
    def __init__(self, max_memories: int = 1000):
        """
        Initialize memory bank.
        
        Args:
            max_memories: Maximum memories to store
        """
        self.max_memories = max_memories
        self.memories: Dict[str, Memory] = {}
    
    def add_memory(
        self,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance,
        source: str,
        tags: List[str] = None,
        context: Dict[str, Any] = None
    ) -> Memory:
        """
        Add a memory to the bank.
        
        Args:
            content: Memory content
            memory_type: Type of memory
            importance: Importance level
            source: Where memory came from
            tags: Optional tags for organization
            context: Optional contextual information
            
        Returns:
            Created Memory object
        """
        memory = Memory(
            id=str(uuid.uuid4()),
            memory_type=memory_type,
            content=content,
            context=context or {},
            importance=importance,
            timestamp=datetime.now(),
            source=source,
            tags=tags or []
        )
        
        self.memories[memory.id] = memory
        
        # Enforce max memories
        if len(self.memories) > self.max_memories:
            self._prune_memories()
        
        return memory
    
    def retrieve_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a specific memory and update access."""
        memory = self.memories.get(memory_id)
        if memory:
            memory.update_access()
        return memory
    
    def search_memories(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        min_importance: MemoryImportance = MemoryImportance.LOW
    ) -> List[Tuple[Memory, float]]:
        """
        Search memories by content and attributes.
        
        Returns list of (memory, relevance_score) tuples sorted by relevance.
        """
        results = []
        query_lower = query.lower()
        
        for memory in self.memories.values():
            # Check type filter
            if memory_type and memory.memory_type != memory_type:
                continue
            
            # Check importance filter
            if memory.importance.value < min_importance.value:
                continue
            
            # Check tag filter
            if tags and not any(tag in memory.tags for tag in tags):
                continue
            
            # Calculate relevance score
            relevance = self._calculate_relevance(memory, query_lower)
            if relevance > 0:
                results.append((memory, relevance))
        
        # Sort by relevance and strength
        results.sort(
            key=lambda x: (x[1], x[0].get_strength()),
            reverse=True
        )
        
        return results
    
    def get_memories_by_type(self, memory_type: MemoryType) -> List[Memory]:
        """Get all memories of a specific type."""
        return [
            m for m in self.memories.values()
            if m.memory_type == memory_type
        ]
    
    def get_recent_memories(self, days: int = 7) -> List[Memory]:
        """Get memories from the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            m for m in self.memories.values()
            if m.timestamp > cutoff
        ]
    
    def consolidate_memories(self) -> Dict[str, Any]:
        """
        Consolidate memories by removing weak/redundant ones.
        
        Returns consolidation report.
        """
        before_count = len(self.memories)
        
        # Identify weak memories
        weak_memories = [
            m for m in self.memories.values()
            if m.get_strength() < 0.2 and m.get_age_days() > 30
        ]
        
        # Remove weak memories
        for memory in weak_memories:
            del self.memories[memory.id]
        
        # Identify potential duplicates
        duplicates = self._find_duplicate_memories()
        for dup_id in duplicates:
            if dup_id in self.memories:
                del self.memories[dup_id]
        
        return {
            "before_count": before_count,
            "after_count": len(self.memories),
            "removed_weak": len(weak_memories),
            "removed_duplicates": len(duplicates),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of memory bank."""
        by_type = {}
        by_importance = {}
        
        for memory in self.memories.values():
            type_key = memory.memory_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            imp_key = memory.importance.name
            by_importance[imp_key] = by_importance.get(imp_key, 0) + 1
        
        return {
            "total_memories": len(self.memories),
            "by_type": by_type,
            "by_importance": by_importance,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_relevance(self, memory: Memory, query: str) -> float:
        """Calculate relevance score for a memory given a query."""
        query_words = set(query.lower().split())
        content_words = set(memory.content.lower().split())
        tag_match = any(query in tag.lower() for tag in memory.tags)
        
        # Calculate overlap
        overlap = len(query_words & content_words) / len(query_words) if query_words else 0
        
        # Tag matching is worth more
        tag_score = 0.5 if tag_match else 0
        
        # Combine with memory strength
        base_relevance = (overlap * 0.7 + tag_score * 0.3)
        memory_strength = memory.get_strength()
        
        return base_relevance * memory_strength
    
    def _prune_memories(self) -> None:
        """Remove weakest memories when limit exceeded."""
        memories_by_strength = sorted(
            self.memories.values(),
            key=lambda m: m.get_strength()
        )
        
        # Remove bottom 10%
        remove_count = max(1, len(memories_by_strength) // 10)
        for memory in memories_by_strength[:remove_count]:
            del self.memories[memory.id]
    
    def _find_duplicate_memories(self) -> List[str]:
        """Find and identify duplicate memories."""
        duplicates = []
        seen = {}
        
        for memory in self.memories.values():
            # Simple duplicate detection based on content
            content_hash = hash(memory.content[:50])
            if content_hash in seen:
                # Keep the stronger one
                other = seen[content_hash]
                if memory.get_strength() < other.get_strength():
                    duplicates.append(memory.id)
                else:
                    duplicates.append(other.id)
                    seen[content_hash] = memory
            else:
                seen[content_hash] = memory
        
        return duplicates


class SessionManager:
    """Manages user sessions."""
    
    def __init__(self):
        """Initialize session manager."""
        self.sessions: Dict[str, Session] = {}
        self.user_sessions: Dict[str, List[str]] = {}
    
    def create_session(
        self,
        user_id: str,
        ttl_seconds: int = 3600,
        metadata: Dict[str, Any] = None
    ) -> Session:
        """
        Create a new session.
        
        Args:
            user_id: User ID
            ttl_seconds: Time-to-live in seconds
            metadata: Optional metadata
            
        Returns:
            Created Session object
        """
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            ttl_seconds=ttl_seconds,
            metadata=metadata or {}
        )
        
        self.sessions[session.id] = session
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        self.user_sessions[user_id].append(session.id)
        
        return session
    
    def activate_session(self, session_id: str) -> Optional[Session]:
        """Activate a session."""
        session = self.sessions.get(session_id)
        if session:
            session.activate()
        return session
    
    def get_active_session(self, user_id: str) -> Optional[Session]:
        """Get user's currently active session."""
        user_session_ids = self.user_sessions.get(user_id, [])
        
        for session_id in user_session_ids:
            session = self.sessions.get(session_id)
            if session and session.is_active():
                return session
        
        return None
    
    def pause_session(self, session_id: str) -> Optional[Session]:
        """Pause a session."""
        session = self.sessions.get(session_id)
        if session:
            session.pause()
        return session
    
    def resume_session(self, session_id: str) -> Optional[Session]:
        """Resume a paused session."""
        session = self.sessions.get(session_id)
        if session:
            session.resume()
        return session
    
    def close_session(self, session_id: str) -> Optional[Session]:
        """Close a session."""
        session = self.sessions.get(session_id)
        if session:
            session.close()
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session."""
        return self.sessions.get(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all sessions for a user."""
        session_ids = self.user_sessions.get(user_id, [])
        return [self.sessions[sid] for sid in session_ids if sid in self.sessions]
    
    def get_active_sessions(self, user_id: str) -> List[Session]:
        """Get all active sessions for a user."""
        sessions = self.get_user_sessions(user_id)
        return [s for s in sessions if s.is_active()]
    
    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        expired_ids = [
            sid for sid, session in self.sessions.items()
            if session.is_expired()
        ]
        
        for sid in expired_ids:
            session = self.sessions[sid]
            session.close()
        
        return len(expired_ids)
    
    def get_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's sessions."""
        sessions = self.get_user_sessions(user_id)
        active_sessions = [s for s in sessions if s.is_active()]
        
        return {
            "total_sessions": len(sessions),
            "active_sessions": len(active_sessions),
            "closed_sessions": len([s for s in sessions if s.status == SessionStatus.CLOSED]),
            "total_interactions": sum(s.total_interactions for s in sessions),
            "timestamp": datetime.now().isoformat()
        }


# Tool Functions for ADK Integration

def create_session(
    user_id: str,
    ttl_seconds: int = 3600,
    metadata: Dict[str, Any] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Create a new session.
    
    Args:
        user_id: User ID
        ttl_seconds: Time-to-live
        metadata: Optional metadata
        tool_context: ADK tool context
        
    Returns:
        Session creation report
    """
    if "session_manager" not in tool_context.state:
        tool_context.state["session_manager"] = SessionManager()
    
    manager = tool_context.state["session_manager"]
    session = manager.create_session(user_id, ttl_seconds, metadata)
    manager.activate_session(session.id)
    
    return {
        "status": "Session created",
        "session_id": session.id,
        "user_id": user_id,
        "created_at": session.created_at.isoformat(),
        "expires_at": session.expires_at.isoformat() if session.expires_at else None
    }


def get_active_session(user_id: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """Get user's active session."""
    if "session_manager" not in tool_context.state:
        return {"status": "No session manager"}
    
    manager = tool_context.state["session_manager"]
    session = manager.get_active_session(user_id)
    
    if session:
        return {
            "status": "Active session found",
            "session_id": session.id,
            "summary": session.get_context_summary()
        }
    else:
        return {"status": "No active session"}


def add_memory(
    content: str,
    memory_type: str,
    importance: str,
    source: str,
    tags: List[str] = None,
    context: Dict[str, Any] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Add memory to the memory bank.
    
    Args:
        content: Memory content
        memory_type: Type of memory (EPISODIC, SEMANTIC, etc.)
        importance: Importance level (CRITICAL, HIGH, etc.)
        source: Source of memory
        tags: Optional tags
        context: Optional context
        tool_context: ADK tool context
        
    Returns:
        Memory creation report
    """
    if "memory_bank" not in tool_context.state:
        tool_context.state["memory_bank"] = MemoryBank()
    
    bank = tool_context.state["memory_bank"]
    
    try:
        mem_type = MemoryType[memory_type.upper()]
        importance_level = MemoryImportance[importance.upper()]
    except KeyError as e:
        return {"status": "error", "message": f"Invalid enum: {e}"}
    
    memory = bank.add_memory(
        content=content,
        memory_type=mem_type,
        importance=importance_level,
        source=source,
        tags=tags,
        context=context
    )
    
    return {
        "status": "Memory added",
        "memory_id": memory.id,
        "type": memory_type,
        "importance": importance,
        "timestamp": memory.timestamp.isoformat()
    }


def search_memories(
    query: str,
    memory_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Search for memories.
    
    Args:
        query: Search query
        memory_type: Optional type filter
        tags: Optional tag filters
        tool_context: ADK tool context
        
    Returns:
        Search results
    """
    if "memory_bank" not in tool_context.state:
        return {"status": "No memory bank", "results": []}
    
    bank = tool_context.state["memory_bank"]
    
    mem_type = None
    if memory_type:
        try:
            mem_type = MemoryType[memory_type.upper()]
        except KeyError:
            pass
    
    results = bank.search_memories(query, memory_type=mem_type, tags=tags)
    
    return {
        "status": "Search complete",
        "query": query,
        "results": [
            {
                "id": memory.id,
                "content": memory.content,
                "type": memory.memory_type.value,
                "strength": memory.get_strength(),
                "relevance": score,
                "timestamp": memory.timestamp.isoformat()
            }
            for memory, score in results[:10]  # Top 10
        ],
        "total_results": len(results)
    }


def get_memory_bank_summary(tool_context: ToolContext = None) -> Dict[str, Any]:
    """Get summary of memory bank."""
    if "memory_bank" not in tool_context.state:
        return {"status": "No memory bank"}
    
    bank = tool_context.state["memory_bank"]
    return bank.get_summary()


def consolidate_memories(tool_context: ToolContext = None) -> Dict[str, Any]:
    """Consolidate memories (remove weak/duplicates)."""
    if "memory_bank" not in tool_context.state:
        return {"status": "No memory bank"}
    
    bank = tool_context.state["memory_bank"]
    report = bank.consolidate_memories()
    
    return {
        "status": "Memories consolidated",
        **report
    }


def pause_session(session_id: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """Pause a session."""
    if "session_manager" not in tool_context.state:
        return {"status": "No session manager"}
    
    manager = tool_context.state["session_manager"]
    session = manager.pause_session(session_id)
    
    if session:
        return {
            "status": "Session paused",
            "session_id": session.id,
            "paused_at": session.paused_at.isoformat()
        }
    else:
        return {"status": "Session not found"}


def resume_session(session_id: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """Resume a paused session."""
    if "session_manager" not in tool_context.state:
        return {"status": "No session manager"}
    
    manager = tool_context.state["session_manager"]
    session = manager.resume_session(session_id)
    
    if session:
        return {
            "status": "Session resumed",
            "session_id": session.id,
            "resumed_at": datetime.now().isoformat()
        }
    else:
        return {"status": "Session not found"}


def get_session_summary(user_id: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """Get summary of user's sessions."""
    if "session_manager" not in tool_context.state:
        return {"status": "No session manager"}
    
    manager = tool_context.state["session_manager"]
    return {
        "user_id": user_id,
        **manager.get_summary(user_id)
    }


# Define all tools
sessions_and_memory_tools = [
    create_session,
    get_active_session,
    add_memory,
    search_memories,
    get_memory_bank_summary,
    consolidate_memories,
    pause_session,
    resume_session,
    get_session_summary
]
