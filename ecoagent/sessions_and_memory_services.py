"""Sessions and Memory Services with persistence layer.

This module provides:
- InMemorySessionService: Fast, non-persistent session management
- PersistentSessionService: Database-backed session management
- InMemoryMemoryBank: Non-persistent memory bank
- PersistentMemoryBank: Database-backed memory bank
- SessionRegistry: Global session registry for concurrent access
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid
import threading
from contextlib import contextmanager

from ecoagent.sessions_and_memory import (
    Session, SessionStatus, Memory, MemoryType, MemoryImportance
)
from ecoagent.database import db


class SessionService(ABC):
    """Abstract base class for session services."""
    
    @abstractmethod
    def create_session(
        self,
        user_id: str,
        ttl_seconds: int = 3600,
        metadata: Dict[str, Any] = None
    ) -> Session:
        """Create a new session."""
        pass
    
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        pass
    
    @abstractmethod
    def save_session(self, session: Session) -> bool:
        """Save session state."""
        pass
    
    @abstractmethod
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all sessions for a user."""
        pass
    
    @abstractmethod
    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        pass


class InMemorySessionService(SessionService):
    """Fast, non-persistent session management for development/testing."""
    
    def __init__(self):
        """Initialize in-memory session service."""
        self.sessions: Dict[str, Session] = {}
        self.user_sessions: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
    
    def create_session(
        self,
        user_id: str,
        ttl_seconds: int = 3600,
        metadata: Dict[str, Any] = None
    ) -> Session:
        """Create a new session."""
        with self._lock:
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
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.activate()
            return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        with self._lock:
            return self.sessions.get(session_id)
    
    def save_session(self, session: Session) -> bool:
        """Save session (no-op for in-memory)."""
        with self._lock:
            self.sessions[session.id] = session
            return True
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all sessions for a user."""
        with self._lock:
            session_ids = self.user_sessions.get(user_id, [])
            return [self.sessions[sid] for sid in session_ids if sid in self.sessions]
    
    def get_active_sessions(self, user_id: str) -> List[Session]:
        """Get active sessions for a user."""
        with self._lock:
            sessions = self.get_user_sessions(user_id)
            return [s for s in sessions if s.is_active()]
    
    def pause_session(self, session_id: str) -> Optional[Session]:
        """Pause a session."""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.pause()
            return session
    
    def resume_session(self, session_id: str) -> Optional[Session]:
        """Resume a paused session."""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.resume()
            return session
    
    def close_session(self, session_id: str) -> Optional[Session]:
        """Close a session."""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.close()
            return session
    
    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        with self._lock:
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
        with self._lock:
            sessions = self.get_user_sessions(user_id)
            active = [s for s in sessions if s.is_active()]
            
            return {
                "total_sessions": len(sessions),
                "active_sessions": len(active),
                "closed_sessions": len([s for s in sessions if s.status == SessionStatus.CLOSED]),
                "total_interactions": sum(s.total_interactions for s in sessions),
                "timestamp": datetime.now().isoformat()
            }


class PersistentSessionService(SessionService):
    """Database-backed session management."""
    
    def __init__(self, database=None):
        """Initialize persistent session service."""
        self.db = database or db
        self._lock = threading.RLock()
    
    def create_session(
        self,
        user_id: str,
        ttl_seconds: int = 3600,
        metadata: Dict[str, Any] = None
    ) -> Session:
        """Create a new session."""
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            ttl_seconds=ttl_seconds,
            metadata=metadata or {}
        )
        
        self.save_session(session)
        return session
    
    def activate_session(self, session_id: str) -> Optional[Session]:
        """Activate a session."""
        session = self.get_session(session_id)
        if session:
            session.activate()
            self.save_session(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        session_data = self.db.get_session(session_id)
        if not session_data:
            return None
        
        return self._deserialize_session(session_data)
    
    def save_session(self, session: Session) -> bool:
        """Save session to database."""
        session_data = {
            'id': session.id,
            'user_id': session.user_id,
            'status': session.status.value,
            'created_at': session.created_at.isoformat() if session.created_at else None,
            'started_at': session.started_at.isoformat() if session.started_at else None,
            'paused_at': session.paused_at.isoformat() if session.paused_at else None,
            'closed_at': session.closed_at.isoformat() if session.closed_at else None,
            'expires_at': session.expires_at.isoformat() if session.expires_at else None,
            'ttl_seconds': session.ttl_seconds,
            'total_interactions': session.total_interactions,
            'context': session.context,
            'metadata': session.metadata
        }
        return self.db.save_session(session_data)
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all sessions for a user."""
        session_list = self.db.get_user_sessions(user_id)
        return [self._deserialize_session(s) for s in session_list]
    
    def get_active_sessions(self, user_id: str) -> List[Session]:
        """Get active sessions for a user."""
        sessions = self.get_user_sessions(user_id)
        return [s for s in sessions if s.is_active()]
    
    def pause_session(self, session_id: str) -> Optional[Session]:
        """Pause a session."""
        session = self.get_session(session_id)
        if session:
            session.pause()
            self.save_session(session)
        return session
    
    def resume_session(self, session_id: str) -> Optional[Session]:
        """Resume a paused session."""
        session = self.get_session(session_id)
        if session:
            session.resume()
            self.save_session(session)
        return session
    
    def close_session(self, session_id: str) -> Optional[Session]:
        """Close a session."""
        session = self.get_session(session_id)
        if session:
            session.close()
            self.save_session(session)
        return session
    
    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        sessions = self.get_user_sessions("*")  # Get all
        expired_count = 0
        
        for session in sessions:
            if session.is_expired():
                session.close()
                self.save_session(session)
                expired_count += 1
        
        return expired_count
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add message to session."""
        success = self.db.add_session_message(session_id, role, content, metadata)
        
        if success:
            session = self.get_session(session_id)
            if session:
                session.add_message(role, content, metadata)
                self.save_session(session)
        
        return success
    
    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session messages."""
        return self.db.get_session_messages(session_id)
    
    @staticmethod
    def _deserialize_session(data: Dict[str, Any]) -> Session:
        """Convert database row to Session object."""
        session = Session(
            id=data['id'],
            user_id=data['user_id'],
            status=SessionStatus(data['status']),
            ttl_seconds=data['ttl_seconds'],
            metadata=data.get('metadata', {}),
        )
        
        if data.get('created_at'):
            session.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('started_at'):
            session.started_at = datetime.fromisoformat(data['started_at'])
        if data.get('paused_at'):
            session.paused_at = datetime.fromisoformat(data['paused_at'])
        if data.get('closed_at'):
            session.closed_at = datetime.fromisoformat(data['closed_at'])
        if data.get('expires_at'):
            session.expires_at = datetime.fromisoformat(data['expires_at'])
        
        session.total_interactions = data.get('total_interactions', 0)
        session.context = data.get('context', {})
        
        return session
    
    def get_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's sessions."""
        sessions = self.get_user_sessions(user_id)
        active = [s for s in sessions if s.is_active()]
        
        return {
            "total_sessions": len(sessions),
            "active_sessions": len(active),
            "closed_sessions": len([s for s in sessions if s.status == SessionStatus.CLOSED]),
            "total_interactions": sum(s.total_interactions for s in sessions),
            "timestamp": datetime.now().isoformat()
        }


class MemoryBankService(ABC):
    """Abstract base class for memory bank services."""
    
    @abstractmethod
    def add_memory(
        self,
        user_id: str,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance,
        source: str,
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Add a memory."""
        pass
    
    @abstractmethod
    def search_memories(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None
    ) -> List[Tuple[Memory, float]]:
        """Search memories."""
        pass


class InMemoryMemoryBank(MemoryBankService):
    """Non-persistent memory bank for development/testing."""
    
    def __init__(self, max_memories: int = 1000):
        """Initialize in-memory memory bank."""
        self.max_memories = max_memories
        self.memories: Dict[str, Memory] = {}
        self._user_memories: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
    
    def add_memory(
        self,
        user_id: str,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance,
        source: str,
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Add a memory."""
        with self._lock:
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
            
            if user_id not in self._user_memories:
                self._user_memories[user_id] = []
            self._user_memories[user_id].append(memory.id)
            
            if len(self.memories) > self.max_memories:
                self._prune_memories()
            
            return memory
    
    def retrieve_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory."""
        with self._lock:
            memory = self.memories.get(memory_id)
            if memory:
                memory.update_access()
            return memory
    
    def search_memories(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None
    ) -> List[Tuple[Memory, float]]:
        """Search memories."""
        with self._lock:
            results = []
            user_memory_ids = self._user_memories.get(user_id, [])
            query_lower = query.lower()
            
            for memory_id in user_memory_ids:
                memory = self.memories.get(memory_id)
                if not memory:
                    continue
                
                if memory_type and memory.memory_type != memory_type:
                    continue
                
                if tags and not any(tag in memory.tags for tag in tags):
                    continue
                
                relevance = self._calculate_relevance(memory, query_lower)
                if relevance > 0:
                    results.append((memory, relevance))
            
            results.sort(
                key=lambda x: (x[1], x[0].get_strength()),
                reverse=True
            )
            
            return results
    
    def get_user_memories(self, user_id: str) -> List[Memory]:
        """Get all memories for a user."""
        with self._lock:
            memory_ids = self._user_memories.get(user_id, [])
            return [self.memories[mid] for mid in memory_ids if mid in self.memories]
    
    def get_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's memories."""
        with self._lock:
            memories = self.get_user_memories(user_id)
            
            by_type = {}
            by_importance = {}
            
            for memory in memories:
                type_key = memory.memory_type.value
                by_type[type_key] = by_type.get(type_key, 0) + 1
                
                imp_key = memory.importance.name
                by_importance[imp_key] = by_importance.get(imp_key, 0) + 1
            
            return {
                "total_memories": len(memories),
                "by_type": by_type,
                "by_importance": by_importance,
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_relevance(self, memory: Memory, query: str) -> float:
        """Calculate relevance score."""
        query_words = set(query.lower().split())
        content_words = set(memory.content.lower().split())
        tag_match = any(query in tag.lower() for tag in memory.tags)
        
        overlap = len(query_words & content_words) / len(query_words) if query_words else 0
        tag_score = 0.5 if tag_match else 0
        
        base_relevance = (overlap * 0.7 + tag_score * 0.3)
        memory_strength = memory.get_strength()
        
        return base_relevance * memory_strength
    
    def _prune_memories(self) -> None:
        """Remove weakest memories when limit exceeded."""
        memories_by_strength = sorted(
            self.memories.values(),
            key=lambda m: m.get_strength()
        )
        
        remove_count = max(1, len(memories_by_strength) // 10)
        for memory in memories_by_strength[:remove_count]:
            del self.memories[memory.id]


class PersistentMemoryBank(MemoryBankService):
    """Database-backed memory bank."""
    
    def __init__(self, database=None):
        """Initialize persistent memory bank."""
        self.db = database or db
        self._lock = threading.RLock()
    
    def add_memory(
        self,
        user_id: str,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance,
        source: str,
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Add a memory."""
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
        
        memory_data = {
            'id': memory.id,
            'user_id': user_id,
            'memory_type': memory.memory_type.value,
            'content': memory.content,
            'context': memory.context,
            'importance': memory.importance.value,
            'timestamp': memory.timestamp.isoformat(),
            'source': memory.source,
            'tags': memory.tags,
            'access_count': memory.access_count,
            'last_accessed': memory.last_accessed.isoformat() if memory.last_accessed else None,
            'decay_factor': memory.decay_factor,
            'relationships': memory.relationships,
            'metadata': memory.metadata
        }
        
        self.db.save_memory(memory_data)
        return memory
    
    def retrieve_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory."""
        memory_data = self.db.get_memory(memory_id)
        if not memory_data:
            return None
        
        memory = self._deserialize_memory(memory_data)
        memory.update_access()
        
        # Save updated access info
        memory_data['access_count'] = memory.access_count
        memory_data['last_accessed'] = memory.last_accessed.isoformat()
        self.db.save_memory(memory_data)
        
        return memory
    
    def search_memories(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None
    ) -> List[Tuple[Memory, float]]:
        """Search memories."""
        query_type = memory_type.value if memory_type else None
        memory_list = self.db.search_memories(user_id, query, query_type)
        
        results = []
        for memory_data in memory_list:
            memory = self._deserialize_memory(memory_data)
            relevance = self._calculate_relevance(memory, query.lower())
            if relevance > 0:
                results.append((memory, relevance))
        
        results.sort(
            key=lambda x: (x[1], x[0].get_strength()),
            reverse=True
        )
        
        return results
    
    def get_user_memories(self, user_id: str) -> List[Memory]:
        """Get all memories for a user."""
        memory_list = self.db.get_user_memories(user_id)
        return [self._deserialize_memory(m) for m in memory_list]
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory."""
        return self.db.delete_memory(memory_id)
    
    def get_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's memories."""
        memories = self.get_user_memories(user_id)
        
        by_type = {}
        by_importance = {}
        
        for memory in memories:
            type_key = memory.memory_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            imp_key = memory.importance.name
            by_importance[imp_key] = by_importance.get(imp_key, 0) + 1
        
        return {
            "total_memories": len(memories),
            "by_type": by_type,
            "by_importance": by_importance,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def _deserialize_memory(data: Dict[str, Any]) -> Memory:
        """Convert database row to Memory object."""
        memory = Memory(
            id=data['id'],
            memory_type=MemoryType(data['memory_type']),
            content=data['content'],
            context=data.get('context', {}),
            importance=MemoryImportance(data.get('importance', 3)),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.now(),
            source=data['source'],
            tags=data.get('tags', []),
            access_count=data.get('access_count', 0),
            decay_factor=data.get('decay_factor', 1.0),
            relationships=data.get('relationships', []),
            metadata=data.get('metadata', {})
        )
        
        if data.get('last_accessed'):
            memory.last_accessed = datetime.fromisoformat(data['last_accessed'])
        
        return memory
    
    @staticmethod
    def _calculate_relevance(memory: Memory, query: str) -> float:
        """Calculate relevance score."""
        query_words = set(query.lower().split())
        content_words = set(memory.content.lower().split())
        tag_match = any(query in tag.lower() for tag in memory.tags)
        
        overlap = len(query_words & content_words) / len(query_words) if query_words else 0
        tag_score = 0.5 if tag_match else 0
        
        base_relevance = (overlap * 0.7 + tag_score * 0.3)
        memory_strength = memory.get_strength()
        
        return base_relevance * memory_strength


class SessionRegistry:
    """Global session and memory registry for concurrent access."""
    
    def __init__(self, use_persistence: bool = True):
        """
        Initialize session registry.
        
        Args:
            use_persistence: If True, use persistent services; else use in-memory
        """
        if use_persistence:
            self.session_service: SessionService = PersistentSessionService()
            self.memory_bank: MemoryBankService = PersistentMemoryBank()
        else:
            self.session_service: SessionService = InMemorySessionService()
            self.memory_bank: MemoryBankService = InMemoryMemoryBank()
        
        self._lock = threading.RLock()
    
    def create_session(
        self,
        user_id: str,
        ttl_seconds: int = 3600,
        metadata: Dict[str, Any] = None,
        activate: bool = True
    ) -> Session:
        """Create and optionally activate a new session."""
        with self._lock:
            session = self.session_service.create_session(user_id, ttl_seconds, metadata)
            if activate:
                self.session_service.activate_session(session.id)
            return session
    
    def get_active_session(self, user_id: str) -> Optional[Session]:
        """Get user's active session."""
        with self._lock:
            if isinstance(self.session_service, PersistentSessionService):
                return self.session_service.get_active_sessions(user_id)[0] if self.session_service.get_active_sessions(user_id) else None
            else:
                return self.session_service.get_active_sessions(user_id)[0] if self.session_service.get_active_sessions(user_id) else None
    
    def add_memory(
        self,
        user_id: str,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance,
        source: str,
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """Add a memory."""
        with self._lock:
            return self.memory_bank.add_memory(
                user_id, content, memory_type, importance, source, tags, context
            )
    
    def search_memories(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None
    ) -> List[Tuple[Memory, float]]:
        """Search memories."""
        with self._lock:
            return self.memory_bank.search_memories(user_id, query, memory_type, tags)
    
    def get_status(self, user_id: str) -> Dict[str, Any]:
        """Get user's session and memory status."""
        with self._lock:
            sessions = self.session_service.get_user_sessions(user_id) if isinstance(self.session_service, PersistentSessionService) else self.session_service.get_user_sessions(user_id)
            
            return {
                "sessions": self.session_service.get_summary(user_id),
                "memory": self.memory_bank.get_summary(user_id),
                "timestamp": datetime.now().isoformat()
            }


# Global registry instance (defaults to persistent)
_global_registry: Optional[SessionRegistry] = None

def get_session_registry(use_persistence: bool = True) -> SessionRegistry:
    """Get or create global session registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = SessionRegistry(use_persistence=use_persistence)
    return _global_registry
