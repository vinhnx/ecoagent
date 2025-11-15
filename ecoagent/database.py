"""Database module for EcoAgent system with SQLite support."""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import threading
import os


class EcoAgentDB:
    """Database interface for EcoAgent system."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database.
        
        Args:
            db_path: Path to the database file. If None, uses in-memory database.
        """
        self.db_path = db_path or ":memory:"
        self._local = threading.local()  # Thread-local storage for connections
        self._init_db()
    
    @contextmanager
    def get_connection(self):
        """Get a database connection, creating one per thread if needed."""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.connection.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield self._local.connection
        except Exception:
            self._local.connection.rollback()
            raise
        else:
            self._local.connection.commit()
    
    def _init_db(self):
        """Initialize the database with required tables."""
        with self.get_connection() as conn:
            # User profiles table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    location TEXT,
                    housing_type TEXT,
                    family_size INTEGER DEFAULT 1,
                    lifestyle_factors JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Carbon footprints table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS carbon_footprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    carbon_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    context JSON DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Sustainability goals table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sustainability_goals (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    target_value REAL NOT NULL,
                    current_value REAL DEFAULT 0.0,
                    target_date TIMESTAMP NOT NULL,
                    status TEXT DEFAULT 'in_progress',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Sustainability actions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sustainability_actions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    impact TEXT,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Progress records table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS progress_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    goal_id TEXT NOT NULL,
                    value REAL NOT NULL,
                    note TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
                    FOREIGN KEY (goal_id) REFERENCES sustainability_goals (id)
                )
            ''')
            
            # Sessions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    status TEXT DEFAULT 'created',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    paused_at TIMESTAMP,
                    closed_at TIMESTAMP,
                    expires_at TIMESTAMP,
                    ttl_seconds INTEGER DEFAULT 3600,
                    total_interactions INTEGER DEFAULT 0,
                    context JSON DEFAULT '{}',
                    metadata JSON DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Session messages table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS session_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON DEFAULT '{}',
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            # Memories table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context JSON DEFAULT '{}',
                    importance INTEGER DEFAULT 3,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source TEXT NOT NULL,
                    tags JSON DEFAULT '[]',
                    access_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP,
                    decay_factor REAL DEFAULT 1.0,
                    relationships JSON DEFAULT '[]',
                    metadata JSON DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Create indexes for better performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_carbon_footprints_user_id ON carbon_footprints (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_goals_user_id ON sustainability_goals (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_actions_user_id ON sustainability_actions (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_progress_user_id ON progress_records (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions (status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_session_messages_session_id ON session_messages (session_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_memories_type ON memories (memory_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories (timestamp)')
    
    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Save or update user profile data."""
        with self.get_connection() as conn:
            try:
                lifestyle_factors_json = json.dumps(profile_data.get('lifestyle_factors', {}))
                
                conn.execute('''
                    INSERT OR REPLACE INTO user_profiles 
                    (user_id, name, location, housing_type, family_size, lifestyle_factors)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    profile_data.get('name'),
                    profile_data.get('location'),
                    profile_data.get('housing_type'),
                    profile_data.get('family_size', 1),
                    lifestyle_factors_json
                ))
                return True
            except Exception:
                return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile data."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM user_profiles WHERE user_id = ?', (user_id,)
            )
            row = cursor.fetchone()
            
            if row:
                profile = dict(row)
                # Parse JSON fields
                profile['lifestyle_factors'] = json.loads(profile['lifestyle_factors'] or '{}')
                return profile
            return None
    
    def save_carbon_footprint(self, user_id: str, carbon_type: str, value: float, context: Optional[Dict[str, Any]] = None) -> bool:
        """Save carbon footprint data."""
        with self.get_connection() as conn:
            try:
                context_json = json.dumps(context or {})
                
                conn.execute('''
                    INSERT INTO carbon_footprints (user_id, carbon_type, value, context)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, carbon_type, value, context_json))
                return True
            except Exception:
                return False
    
    def get_carbon_footprints(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve carbon footprint history for a user."""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM carbon_footprints 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            footprints = []
            for row in rows:
                footprint = dict(row)
                footprint['context'] = json.loads(footprint['context'] or '{}')
                footprints.append(footprint)
            
            return footprints
    
    def save_sustainability_goal(self, goal_data: Dict[str, Any]) -> bool:
        """Save sustainability goal."""
        with self.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO sustainability_goals
                    (id, user_id, description, target_value, current_value, target_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    goal_data['id'],
                    goal_data['user_id'],
                    goal_data['description'],
                    goal_data['target_value'],
                    goal_data['current_value'],
                    goal_data['target_date'],
                    goal_data['status']
                ))
                return True
            except Exception:
                return False

    def get_user_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve sustainability goals for a user."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM sustainability_goals WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_sustainability_action(self, action_data: Dict[str, Any]) -> bool:
        """Save sustainability action."""
        with self.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO sustainability_actions 
                    (id, user_id, action, impact, completed)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    action_data['id'],
                    action_data['user_id'],
                    action_data['action'],
                    action_data['impact'],
                    action_data['completed']
                ))
                return True
            except Exception:
                return False
    
    def get_user_actions(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve sustainability actions for a user."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM sustainability_actions WHERE user_id = ? ORDER BY date_added DESC',
                (user_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_progress_record(self, record_data: Dict[str, Any]) -> bool:
        """Save a progress record."""
        with self.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO progress_records 
                    (user_id, goal_id, value, note)
                    VALUES (?, ?, ?, ?)
                ''', (
                    record_data['user_id'],
                    record_data['goal_id'],
                    record_data['value'],
                    record_data.get('note')
                ))
                return True
            except Exception:
                return False
    
    def get_progress_records(self, user_id: str, goal_id: str) -> List[Dict[str, Any]]:
        """Retrieve progress records for a specific goal."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM progress_records WHERE user_id = ? AND goal_id = ? ORDER BY timestamp DESC',
                (user_id, goal_id)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # Session management methods
    
    def save_session(self, session_data: Dict[str, Any]) -> bool:
        """Save a session."""
        with self.get_connection() as conn:
            try:
                context_json = json.dumps(session_data.get('context', {}))
                metadata_json = json.dumps(session_data.get('metadata', {}))
                
                conn.execute('''
                    INSERT OR REPLACE INTO sessions
                    (id, user_id, status, created_at, started_at, paused_at, closed_at, expires_at, 
                     ttl_seconds, total_interactions, context, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_data['id'],
                    session_data['user_id'],
                    session_data.get('status', 'created'),
                    session_data.get('created_at'),
                    session_data.get('started_at'),
                    session_data.get('paused_at'),
                    session_data.get('closed_at'),
                    session_data.get('expires_at'),
                    session_data.get('ttl_seconds', 3600),
                    session_data.get('total_interactions', 0),
                    context_json,
                    metadata_json
                ))
                return True
            except Exception:
                return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a session."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM sessions WHERE id = ?', (session_id,)
            )
            row = cursor.fetchone()
            
            if row:
                session = dict(row)
                session['context'] = json.loads(session['context'] or '{}')
                session['metadata'] = json.loads(session['metadata'] or '{}')
                return session
            return None
    
    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve sessions for a user."""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM sessions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            sessions = []
            for row in cursor.fetchall():
                session = dict(row)
                session['context'] = json.loads(session['context'] or '{}')
                session['metadata'] = json.loads(session['metadata'] or '{}')
                sessions.append(session)
            
            return sessions
    
    def add_session_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a message to a session."""
        with self.get_connection() as conn:
            try:
                metadata_json = json.dumps(metadata or {})
                
                conn.execute('''
                    INSERT INTO session_messages (session_id, role, content, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (session_id, role, content, metadata_json))
                return True
            except Exception:
                return False
    
    def get_session_messages(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve messages from a session."""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM session_messages 
                WHERE session_id = ? 
                ORDER BY timestamp ASC 
                LIMIT ?
            ''', (session_id, limit))
            
            messages = []
            for row in cursor.fetchall():
                message = dict(row)
                message['metadata'] = json.loads(message['metadata'] or '{}')
                messages.append(message)
            
            return messages
    
    # Memory management methods
    
    def save_memory(self, memory_data: Dict[str, Any]) -> bool:
        """Save a memory."""
        with self.get_connection() as conn:
            try:
                context_json = json.dumps(memory_data.get('context', {}))
                tags_json = json.dumps(memory_data.get('tags', []))
                relationships_json = json.dumps(memory_data.get('relationships', []))
                metadata_json = json.dumps(memory_data.get('metadata', {}))
                
                conn.execute('''
                    INSERT OR REPLACE INTO memories
                    (id, user_id, memory_type, content, context, importance, timestamp, source,
                     tags, access_count, last_accessed, decay_factor, relationships, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory_data['id'],
                    memory_data['user_id'],
                    memory_data['memory_type'],
                    memory_data['content'],
                    context_json,
                    memory_data.get('importance', 3),
                    memory_data.get('timestamp'),
                    memory_data['source'],
                    tags_json,
                    memory_data.get('access_count', 0),
                    memory_data.get('last_accessed'),
                    memory_data.get('decay_factor', 1.0),
                    relationships_json,
                    metadata_json
                ))
                return True
            except Exception:
                return False
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a memory."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM memories WHERE id = ?', (memory_id,)
            )
            row = cursor.fetchone()
            
            if row:
                memory = dict(row)
                memory['context'] = json.loads(memory['context'] or '{}')
                memory['tags'] = json.loads(memory['tags'] or '[]')
                memory['relationships'] = json.loads(memory['relationships'] or '[]')
                memory['metadata'] = json.loads(memory['metadata'] or '{}')
                return memory
            return None
    
    def get_user_memories(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve memories for a user."""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM memories 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            memories = []
            for row in cursor.fetchall():
                memory = dict(row)
                memory['context'] = json.loads(memory['context'] or '{}')
                memory['tags'] = json.loads(memory['tags'] or '[]')
                memory['relationships'] = json.loads(memory['relationships'] or '[]')
                memory['metadata'] = json.loads(memory['metadata'] or '{}')
                memories.append(memory)
            
            return memories
    
    def search_memories(self, user_id: str, query: str, memory_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search memories by content."""
        with self.get_connection() as conn:
            if memory_type:
                cursor = conn.execute('''
                    SELECT * FROM memories 
                    WHERE user_id = ? AND memory_type = ? AND (content LIKE ? OR tags LIKE ?)
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, memory_type, f'%{query}%', f'%{query}%', limit))
            else:
                cursor = conn.execute('''
                    SELECT * FROM memories 
                    WHERE user_id = ? AND (content LIKE ? OR tags LIKE ?)
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, f'%{query}%', f'%{query}%', limit))
            
            memories = []
            for row in cursor.fetchall():
                memory = dict(row)
                memory['context'] = json.loads(memory['context'] or '{}')
                memory['tags'] = json.loads(memory['tags'] or '[]')
                memory['relationships'] = json.loads(memory['relationships'] or '[]')
                memory['metadata'] = json.loads(memory['metadata'] or '{}')
                memories.append(memory)
            
            return memories
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory."""
        with self.get_connection() as conn:
            try:
                conn.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
                return True
            except Exception:
                return False


# Global database instance
db = EcoAgentDB(os.getenv("ECOAGENT_DB_PATH"))