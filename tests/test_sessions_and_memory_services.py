"""Tests for Sessions and Memory Services."""

import pytest
import tempfile
from datetime import datetime, timedelta
import json

from ecoagent.sessions_and_memory import (
    Session, SessionStatus, Memory, MemoryType, MemoryImportance
)
from ecoagent.sessions_and_memory_services import (
    InMemorySessionService, PersistentSessionService,
    InMemoryMemoryBank, PersistentMemoryBank,
    SessionRegistry, get_session_registry
)
from ecoagent.database import EcoAgentDB


class TestInMemorySessionService:
    """Test in-memory session service."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return InMemorySessionService()
    
    def test_create_session(self, service):
        """Test session creation."""
        session = service.create_session("user1", ttl_seconds=1800)
        
        assert session.id is not None
        assert session.user_id == "user1"
        assert session.ttl_seconds == 1800
        assert session.status == SessionStatus.CREATED
    
    def test_activate_session(self, service):
        """Test session activation."""
        session = service.create_session("user1")
        activated = service.activate_session(session.id)
        
        assert activated is not None
        assert activated.status == SessionStatus.ACTIVE
        assert activated.started_at is not None
    
    def test_get_session(self, service):
        """Test retrieving a session."""
        created = service.create_session("user1")
        retrieved = service.get_session(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_pause_resume_session(self, service):
        """Test pausing and resuming sessions."""
        session = service.create_session("user1")
        service.activate_session(session.id)
        
        paused = service.pause_session(session.id)
        assert paused.status == SessionStatus.PAUSED
        
        resumed = service.resume_session(session.id)
        assert resumed.status == SessionStatus.ACTIVE
    
    def test_close_session(self, service):
        """Test closing a session."""
        session = service.create_session("user1")
        closed = service.close_session(session.id)
        
        assert closed.status == SessionStatus.CLOSED
        assert closed.closed_at is not None
    
    def test_get_user_sessions(self, service):
        """Test retrieving user sessions."""
        service.create_session("user1")
        service.create_session("user1")
        service.create_session("user2")
        
        user1_sessions = service.get_user_sessions("user1")
        assert len(user1_sessions) == 2
        
        user2_sessions = service.get_user_sessions("user2")
        assert len(user2_sessions) == 1
    
    def test_cleanup_expired(self, service):
        """Test cleanup of expired sessions."""
        session = service.create_session("user1", ttl_seconds=1)
        service.activate_session(session.id)
        
        # Manually expire the session
        session.expires_at = datetime.now() - timedelta(seconds=1)
        
        cleaned = service.cleanup_expired()
        assert cleaned >= 0


class TestPersistentSessionService:
    """Test persistent session service."""
    
    @pytest.fixture
    def db(self):
        """Create in-memory database."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        database = EcoAgentDB(db_path)
        # Create user for foreign key
        database.save_user_profile("user1", {"name": "Test User"})
        database.save_user_profile("user2", {"name": "Another User"})
        
        yield database
    
    @pytest.fixture
    def service(self, db):
        """Create service instance."""
        return PersistentSessionService(database=db)
    
    def test_create_and_save_session(self, service):
        """Test creating and saving a session."""
        session = service.create_session("user1", ttl_seconds=1800, metadata={"test": "data"})
        
        assert session.id is not None
        assert session.user_id == "user1"
        
        retrieved = service.get_session(session.id)
        assert retrieved is not None
        assert retrieved.user_id == "user1"
        assert retrieved.metadata.get("test") == "data"
    
    def test_persistence(self, db):
        """Test that sessions persist across service instances."""
        service1 = PersistentSessionService(database=db)
        session = service1.create_session("user1")
        session_id = session.id
        
        service2 = PersistentSessionService(database=db)
        retrieved = service2.get_session(session_id)
        
        assert retrieved is not None
        assert retrieved.id == session_id
    
    def test_add_message_to_session(self, service):
        """Test adding messages to a session."""
        session = service.create_session("user1")
        service.activate_session(session.id)
        
        success = service.add_message(session.id, "user", "Hello")
        assert success
        
        messages = service.get_messages(session.id)
        assert len(messages) > 0


class TestInMemoryMemoryBank:
    """Test in-memory memory bank."""
    
    @pytest.fixture
    def bank(self):
        """Create memory bank instance."""
        return InMemoryMemoryBank()
    
    def test_add_memory(self, bank):
        """Test adding a memory."""
        memory = bank.add_memory(
            user_id="user1",
            content="User prefers vegetarian diet",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            source="user_input",
            tags=["diet", "preference"]
        )
        
        assert memory.id is not None
        assert memory.content == "User prefers vegetarian diet"
        assert memory.memory_type == MemoryType.SEMANTIC
    
    def test_retrieve_memory(self, bank):
        """Test retrieving a memory."""
        memory = bank.add_memory(
            user_id="user1",
            content="Test content",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        retrieved = bank.retrieve_memory(memory.id)
        assert retrieved is not None
        assert retrieved.content == "Test content"
        assert retrieved.access_count > 0
    
    def test_search_memories(self, bank):
        """Test searching memories."""
        bank.add_memory(
            user_id="user1",
            content="Carbon reduction plan",
            memory_type=MemoryType.PROCEDURAL,
            importance=MemoryImportance.HIGH,
            source="test",
            tags=["carbon", "reduction"]
        )
        
        bank.add_memory(
            user_id="user1",
            content="Energy saving tips",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test",
            tags=["energy", "tips"]
        )
        
        results = bank.search_memories("user1", "carbon")
        assert len(results) > 0
        assert results[0][0].content == "Carbon reduction plan"
    
    def test_memory_filtering(self, bank):
        """Test memory type filtering."""
        bank.add_memory(
            user_id="user1",
            content="Episodic event",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        bank.add_memory(
            user_id="user1",
            content="Semantic fact",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        results = bank.search_memories(
            "user1", "event", memory_type=MemoryType.EPISODIC
        )
        assert len(results) >= 1
        assert results[0][0].memory_type == MemoryType.EPISODIC
    
    def test_get_user_memories(self, bank):
        """Test getting all user memories."""
        bank.add_memory(
            user_id="user1",
            content="Memory 1",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            source="test"
        )
        
        bank.add_memory(
            user_id="user1",
            content="Memory 2",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        memories = bank.get_user_memories("user1")
        assert len(memories) == 2


class TestPersistentMemoryBank:
    """Test persistent memory bank."""
    
    @pytest.fixture
    def db(self):
        """Create in-memory database."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        database = EcoAgentDB(db_path)
        database.save_user_profile("user1", {"name": "Test User"})
        
        yield database
    
    @pytest.fixture
    def bank(self, db):
        """Create memory bank instance."""
        return PersistentMemoryBank(database=db)
    
    def test_add_and_retrieve_memory(self, bank):
        """Test adding and retrieving a memory."""
        memory = bank.add_memory(
            user_id="user1",
            content="User lives in urban area",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            source="profile",
            tags=["location", "urban"]
        )
        
        assert memory.id is not None
        
        retrieved = bank.retrieve_memory(memory.id)
        assert retrieved is not None
        assert retrieved.content == "User lives in urban area"
    
    def test_persistence_across_instances(self, db):
        """Test memory persistence across instances."""
        bank1 = PersistentMemoryBank(database=db)
        memory = bank1.add_memory(
            user_id="user1",
            content="Important memory",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            source="test"
        )
        memory_id = memory.id
        
        bank2 = PersistentMemoryBank(database=db)
        retrieved = bank2.retrieve_memory(memory_id)
        
        assert retrieved is not None
        assert retrieved.content == "Important memory"
    
    def test_search_persistent_memories(self, bank):
        """Test searching persistent memories."""
        bank.add_memory(
            user_id="user1",
            content="First sustainable action",
            memory_type=MemoryType.PROCEDURAL,
            importance=MemoryImportance.HIGH,
            source="test",
            tags=["sustainability", "action"]
        )
        
        bank.add_memory(
            user_id="user1",
            content="Second sustainable goal",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test",
            tags=["sustainability", "goal"]
        )
        
        results = bank.search_memories("user1", "sustainable")
        assert len(results) >= 2
    
    def test_delete_memory(self, bank):
        """Test deleting a memory."""
        memory = bank.add_memory(
            user_id="user1",
            content="To be deleted",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.LOW,
            source="test"
        )
        
        deleted = bank.delete_memory(memory.id)
        assert deleted
        
        retrieved = bank.retrieve_memory(memory.id)
        assert retrieved is None


class TestSessionRegistry:
    """Test session registry."""
    
    @pytest.fixture
    def registry(self):
        """Create registry with in-memory services."""
        return SessionRegistry(use_persistence=False)
    
    def test_create_session_with_registry(self, registry):
        """Test creating session through registry."""
        session = registry.create_session("user1", activate=True)
        
        assert session.id is not None
        assert session.status == SessionStatus.ACTIVE
    
    def test_add_memory_with_registry(self, registry):
        """Test adding memory through registry."""
        memory = registry.add_memory(
            user_id="user1",
            content="Registry memory",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        assert memory.id is not None
    
    def test_search_through_registry(self, registry):
        """Test searching memories through registry."""
        registry.add_memory(
            user_id="user1",
            content="Searchable memory",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.HIGH,
            source="test",
            tags=["search"]
        )
        
        results = registry.search_memories("user1", "searchable")
        assert len(results) > 0
    
    def test_get_status(self, registry):
        """Test getting user status."""
        registry.create_session("user1")
        registry.add_memory(
            user_id="user1",
            content="Status memory",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        status = registry.get_status("user1")
        
        assert "sessions" in status
        assert "memory" in status
        assert status["sessions"]["total_sessions"] >= 1


class TestMemoryStrength:
    """Test memory strength calculations."""
    
    @pytest.fixture
    def bank(self):
        """Create memory bank."""
        return InMemoryMemoryBank()
    
    def test_memory_importance_affects_strength(self, bank):
        """Test that importance affects memory strength."""
        critical_memory = bank.add_memory(
            user_id="user1",
            content="Critical",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.CRITICAL,
            source="test"
        )
        
        trivial_memory = bank.add_memory(
            user_id="user1",
            content="Trivial",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.TRIVIAL,
            source="test"
        )
        
        critical_strength = critical_memory.get_strength()
        trivial_strength = trivial_memory.get_strength()
        
        assert critical_strength > trivial_strength
    
    def test_memory_access_increases_strength(self, bank):
        """Test that access count affects strength."""
        memory = bank.add_memory(
            user_id="user1",
            content="Accessed memory",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            source="test"
        )
        
        initial_strength = memory.get_strength()
        
        bank.retrieve_memory(memory.id)
        bank.retrieve_memory(memory.id)
        
        retrieved = bank.retrieve_memory(memory.id)
        final_strength = retrieved.get_strength()
        
        assert final_strength >= initial_strength


@pytest.mark.parametrize("service_type", [
    pytest.param("in_memory", marks=pytest.mark.unit),
    pytest.param("persistent", marks=pytest.mark.integration),
])
def test_session_lifecycle(service_type):
    """Test complete session lifecycle."""
    if service_type == "in_memory":
        service = InMemorySessionService()
    else:
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        database = EcoAgentDB(db_path)
        database.save_user_profile("user1", {"name": "Test"})
        service = PersistentSessionService(database=database)
    
    # Create session
    session = service.create_session("user1")
    assert session.status == SessionStatus.CREATED
    
    # Activate session
    service.activate_session(session.id)
    session = service.get_session(session.id)
    assert session.status == SessionStatus.ACTIVE
    
    # Pause session
    service.pause_session(session.id)
    session = service.get_session(session.id)
    assert session.status == SessionStatus.PAUSED
    
    # Resume session
    service.resume_session(session.id)
    session = service.get_session(session.id)
    assert session.status == SessionStatus.ACTIVE
    
    # Close session
    service.close_session(session.id)
    session = service.get_session(session.id)
    assert session.status == SessionStatus.CLOSED
