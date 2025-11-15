"""Long-running Operations Management - Pause/Resume for Agent Tasks."""

import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from ecoagent.database import db


class OperationStatus(str, Enum):
    """Status of a long-running operation."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class OperationCheckpoint:
    """Checkpoint for resuming an operation."""
    operation_id: str
    timestamp: str
    progress: float  # 0-100
    state: Dict[str, Any]  # Operation-specific state
    agent_name: str
    task_description: str


class LongRunningOperation:
    """Manages long-running agent operations with pause/resume support."""
    
    def __init__(self):
        """Initialize operation manager."""
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.checkpoints: Dict[str, List[OperationCheckpoint]] = {}
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables for operations."""
        with db.get_connection() as conn:
            # Operations table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operations (
                    operation_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    task_description TEXT,
                    status TEXT DEFAULT 'pending',
                    progress REAL DEFAULT 0.0,
                    state JSON DEFAULT '{}',
                    metadata JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    paused_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    estimated_completion TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            ''')
            
            # Operation checkpoints table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operation_checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    operation_id TEXT NOT NULL,
                    checkpoint_data JSON NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (operation_id) REFERENCES operations (operation_id)
                )
            ''')
            
            # Operation history table (for auditing)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details JSON DEFAULT '{}',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (operation_id) REFERENCES operations (operation_id)
                )
            ''')
            
            # Create indexes
            conn.execute('CREATE INDEX IF NOT EXISTS idx_operations_user_id ON operations (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_operations_status ON operations (status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_operations_agent ON operations (agent_name)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_checkpoints_operation ON operation_checkpoints (operation_id)')
    
    def create_operation(
        self,
        user_id: str,
        agent_name: str,
        task_description: str,
        estimated_duration_minutes: int = 30,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new long-running operation.
        
        Args:
            user_id: User identifier
            agent_name: Name of the agent executing the operation
            task_description: Description of the task
            estimated_duration_minutes: Estimated duration in minutes
            metadata: Additional metadata for the operation
            
        Returns:
            Operation ID
        """
        operation_id = str(uuid.uuid4())
        now = datetime.now()
        estimated_completion = now + timedelta(minutes=estimated_duration_minutes)
        
        operation_data = {
            "operation_id": operation_id,
            "user_id": user_id,
            "agent_name": agent_name,
            "task_description": task_description,
            "status": OperationStatus.PENDING.value,
            "progress": 0.0,
            "state": {},
            "metadata": metadata or {},
            "created_at": now.isoformat(),
            "started_at": None,
            "paused_at": None,
            "completed_at": None,
            "estimated_completion": estimated_completion.isoformat(),
            "pause_reason": None,
            "error_message": None
        }
        
        # Save to database
        self._save_operation(operation_data)
        
        # Cache in memory
        self.operations[operation_id] = operation_data
        self.checkpoints[operation_id] = []
        
        # Log operation creation
        self._log_operation_history(operation_id, "created", {
            "agent_name": agent_name,
            "task": task_description
        })
        
        return operation_id
    
    def start_operation(self, operation_id: str) -> bool:
        """
        Start a pending operation.
        
        Args:
            operation_id: Operation ID
            
        Returns:
            True if operation started successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        if operation["status"] != OperationStatus.PENDING.value:
            return False
        
        now = datetime.now()
        operation["status"] = OperationStatus.RUNNING.value
        operation["started_at"] = now.isoformat()
        
        self._save_operation(operation)
        self._log_operation_history(operation_id, "started", {})
        
        return True
    
    def update_operation_progress(
        self,
        operation_id: str,
        progress: float,
        state: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update operation progress.
        
        Args:
            operation_id: Operation ID
            progress: Progress percentage (0-100)
            state: Optional state data to save
            
        Returns:
            True if progress updated successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        if operation["status"] not in [
            OperationStatus.RUNNING.value,
            OperationStatus.PAUSED.value
        ]:
            return False
        
        operation["progress"] = min(100.0, max(0.0, progress))
        
        if state:
            operation["state"] = state
        
        self._save_operation(operation)
        
        return True
    
    def pause_operation(
        self,
        operation_id: str,
        reason: Optional[str] = None,
        checkpoint_state: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Pause a running operation and save checkpoint.
        
        Args:
            operation_id: Operation ID
            reason: Reason for pausing
            checkpoint_state: State to save for resumption
            
        Returns:
            True if operation paused successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        if operation["status"] != OperationStatus.RUNNING.value:
            return False
        
        now = datetime.now()
        operation["status"] = OperationStatus.PAUSED.value
        operation["paused_at"] = now.isoformat()
        operation["pause_reason"] = reason
        
        # Update state with checkpoint data
        if checkpoint_state:
            operation["state"] = checkpoint_state
        
        self._save_operation(operation)
        
        # Create checkpoint for resumption
        checkpoint = OperationCheckpoint(
            operation_id=operation_id,
            timestamp=now.isoformat(),
            progress=operation["progress"],
            state=operation["state"],
            agent_name=operation["agent_name"],
            task_description=operation["task_description"]
        )
        
        self._save_checkpoint(checkpoint)
        
        self._log_operation_history(operation_id, "paused", {
            "reason": reason,
            "progress": operation["progress"]
        })
        
        return True
    
    def resume_operation(self, operation_id: str) -> Optional[OperationCheckpoint]:
        """
        Resume a paused operation.
        
        Args:
            operation_id: Operation ID
            
        Returns:
            Checkpoint data for resumption, or None if failed
        """
        if operation_id not in self.operations:
            return None
        
        operation = self.operations[operation_id]
        
        if operation["status"] != OperationStatus.PAUSED.value:
            return None
        
        # Retrieve latest checkpoint
        checkpoint = self._get_latest_checkpoint(operation_id)
        
        if not checkpoint:
            return None
        
        # Resume operation
        now = datetime.now()
        operation["status"] = OperationStatus.RUNNING.value
        operation["paused_at"] = None
        operation["pause_reason"] = None
        
        self._save_operation(operation)
        
        self._log_operation_history(operation_id, "resumed", {
            "progress": operation["progress"],
            "checkpoint_timestamp": checkpoint.timestamp
        })
        
        return checkpoint
    
    def complete_operation(
        self,
        operation_id: str,
        result: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Mark operation as completed.
        
        Args:
            operation_id: Operation ID
            result: Operation result data
            
        Returns:
            True if operation completed successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        if operation["status"] not in [
            OperationStatus.RUNNING.value,
            OperationStatus.PAUSED.value
        ]:
            return False
        
        now = datetime.now()
        operation["status"] = OperationStatus.COMPLETED.value
        operation["completed_at"] = now.isoformat()
        operation["progress"] = 100.0
        
        if result:
            operation["metadata"]["result"] = result
        
        self._save_operation(operation)
        self._log_operation_history(operation_id, "completed", {
            "duration_seconds": self._calculate_duration(operation),
            "result": result
        })
        
        return True
    
    def fail_operation(
        self,
        operation_id: str,
        error_message: str
    ) -> bool:
        """
        Mark operation as failed.
        
        Args:
            operation_id: Operation ID
            error_message: Error message
            
        Returns:
            True if operation failed successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        now = datetime.now()
        operation["status"] = OperationStatus.FAILED.value
        operation["completed_at"] = now.isoformat()
        operation["error_message"] = error_message
        
        self._save_operation(operation)
        self._log_operation_history(operation_id, "failed", {
            "error": error_message
        })
        
        return True
    
    def cancel_operation(self, operation_id: str) -> bool:
        """
        Cancel a pending or running operation.
        
        Args:
            operation_id: Operation ID
            
        Returns:
            True if operation cancelled successfully
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        if operation["status"] not in [
            OperationStatus.PENDING.value,
            OperationStatus.RUNNING.value,
            OperationStatus.PAUSED.value
        ]:
            return False
        
        now = datetime.now()
        operation["status"] = OperationStatus.CANCELLED.value
        operation["completed_at"] = now.isoformat()
        
        self._save_operation(operation)
        self._log_operation_history(operation_id, "cancelled", {})
        
        return True
    
    def get_operation(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get operation details."""
        return self.operations.get(operation_id)
    
    def get_user_operations(
        self,
        user_id: str,
        status: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get operations for a user, optionally filtered by status or agent."""
        with db.get_connection() as conn:
            query = "SELECT * FROM operations WHERE user_id = ?"
            params = [user_id]
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)
            
            query += " ORDER BY created_at DESC"
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            operations = []
            for row in rows:
                op = dict(row)
                op["state"] = json.loads(op["state"] or "{}")
                op["metadata"] = json.loads(op["metadata"] or "{}")
                operations.append(op)
            
            return operations
    
    def get_operation_history(self, operation_id: str) -> List[Dict[str, Any]]:
        """Get history of actions for an operation."""
        with db.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operation_history WHERE operation_id = ? ORDER BY timestamp ASC',
                (operation_id,)
            )
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                h = dict(row)
                h["details"] = json.loads(h["details"] or "{}")
                history.append(h)
            
            return history
    
    def get_active_operations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active (running or paused) operations for a user."""
        active_statuses = [
            OperationStatus.PENDING.value,
            OperationStatus.RUNNING.value,
            OperationStatus.PAUSED.value
        ]
        
        return [
            op for op in self.get_user_operations(user_id)
            if op["status"] in active_statuses
        ]
    
    def get_paused_operations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all paused operations for a user."""
        return self.get_user_operations(user_id, status=OperationStatus.PAUSED.value)
    
    def cleanup_old_operations(self, days: int = 30) -> int:
        """
        Delete completed/failed operations older than specified days.
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of operations deleted
        """
        with db.get_connection() as conn:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor = conn.execute(
                '''DELETE FROM operations 
                   WHERE (status = ? OR status = ?) 
                   AND completed_at < ?''',
                (OperationStatus.COMPLETED.value, OperationStatus.FAILED.value, cutoff_date)
            )
            
            return cursor.rowcount
    
    # Private helper methods
    
    def _save_operation(self, operation: Dict[str, Any]):
        """Save operation to database."""
        with db.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT OR REPLACE INTO operations 
                    (operation_id, user_id, agent_name, task_description, status, progress, 
                     state, metadata, started_at, paused_at, completed_at, estimated_completion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    operation["operation_id"],
                    operation["user_id"],
                    operation["agent_name"],
                    operation["task_description"],
                    operation["status"],
                    operation["progress"],
                    json.dumps(operation["state"]),
                    json.dumps(operation["metadata"]),
                    operation["started_at"],
                    operation["paused_at"],
                    operation["completed_at"],
                    operation["estimated_completion"]
                ))
            except Exception as e:
                print(f"Error saving operation: {e}")
    
    def _save_checkpoint(self, checkpoint: OperationCheckpoint):
        """Save operation checkpoint to database."""
        checkpoint_id = str(uuid.uuid4())
        
        with db.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO operation_checkpoints 
                    (checkpoint_id, operation_id, checkpoint_data)
                    VALUES (?, ?, ?)
                ''', (
                    checkpoint_id,
                    checkpoint.operation_id,
                    json.dumps(asdict(checkpoint))
                ))
            except Exception as e:
                print(f"Error saving checkpoint: {e}")
    
    def _get_latest_checkpoint(self, operation_id: str) -> Optional[OperationCheckpoint]:
        """Get the most recent checkpoint for an operation."""
        with db.get_connection() as conn:
            cursor = conn.execute(
                '''SELECT checkpoint_data FROM operation_checkpoints 
                   WHERE operation_id = ? ORDER BY created_at DESC LIMIT 1''',
                (operation_id,)
            )
            
            row = cursor.fetchone()
            
            if row:
                checkpoint_data = json.loads(row[0])
                return OperationCheckpoint(**checkpoint_data)
            
            return None
    
    def _log_operation_history(
        self,
        operation_id: str,
        action: str,
        details: Dict[str, Any]
    ):
        """Log operation history."""
        with db.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO operation_history (operation_id, action, details)
                    VALUES (?, ?, ?)
                ''', (operation_id, action, json.dumps(details)))
            except Exception as e:
                print(f"Error logging operation history: {e}")
    
    def _calculate_duration(self, operation: Dict[str, Any]) -> int:
        """Calculate operation duration in seconds."""
        started = operation.get("started_at")
        completed = operation.get("completed_at")
        
        if not started or not completed:
            return 0
        
        try:
            start_time = datetime.fromisoformat(started)
            end_time = datetime.fromisoformat(completed)
            return int((end_time - start_time).total_seconds())
        except:
            return 0


# Global operations manager instance
operations_manager = LongRunningOperation()
