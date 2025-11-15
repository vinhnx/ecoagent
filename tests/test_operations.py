"""Tests for long-running operations (pause/resume) functionality."""

import pytest
import time
from datetime import datetime, timedelta
from ecoagent.operations import (
    LongRunningOperation,
    OperationStatus,
    OperationCheckpoint,
    operations_manager
)
from ecoagent.tools.operations import (
    start_long_running_operation,
    update_operation_progress,
    pause_operation,
    resume_operation,
    complete_operation,
    fail_operation,
    cancel_operation,
    get_operation_status,
    list_user_operations,
    list_paused_operations,
    get_operation_history
)


class MockToolContext:
    """Mock tool context for testing."""
    def __init__(self, user_id="test_user"):
        self.user_id = user_id
        self.session_id = "test_session"


class TestLongRunningOperations:
    """Test suite for long-running operations."""
    
    def test_create_operation(self):
        """Test creating a new operation."""
        user_id = "test_user_1"
        agent_name = "carbon_calculator_agent"
        task = "Calculating carbon footprint"
        
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id=user_id,
            agent_name=agent_name,
            task_description=task,
            estimated_duration_minutes=30
        )
        
        assert operation_id is not None
        assert len(operation_id) > 0
        
        operation = op_mgr.get_operation(operation_id)
        assert operation is not None
        assert operation["status"] == OperationStatus.PENDING.value
        assert operation["user_id"] == user_id
        assert operation["agent_name"] == agent_name
        assert operation["progress"] == 0.0
    
    def test_start_operation(self):
        """Test starting an operation."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        result = op_mgr.start_operation(operation_id)
        assert result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.RUNNING.value
        assert operation["started_at"] is not None
    
    def test_cannot_start_non_pending_operation(self):
        """Test that we cannot start a non-pending operation."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        result = op_mgr.start_operation(operation_id)
        assert result is False
    
    def test_update_progress(self):
        """Test updating operation progress."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        
        # Update progress
        result = op_mgr.update_operation_progress(
            operation_id=operation_id,
            progress=50.0,
            state={"current_step": "processing_data"}
        )
        
        assert result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["progress"] == 50.0
        assert operation["state"]["current_step"] == "processing_data"
    
    def test_pause_and_resume_operation(self):
        """Test pausing and resuming an operation."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        op_mgr.update_operation_progress(operation_id, 50.0)
        
        # Pause operation
        pause_result = op_mgr.pause_operation(
            operation_id=operation_id,
            reason="User requested pause",
            checkpoint_state={"step": 1, "data": "important"}
        )
        assert pause_result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.PAUSED.value
        assert operation["paused_at"] is not None
        assert operation["pause_reason"] == "User requested pause"
        
        # Resume operation
        checkpoint = op_mgr.resume_operation(operation_id)
        assert checkpoint is not None
        assert checkpoint.progress == 50.0
        assert checkpoint.state["step"] == 1
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.RUNNING.value
    
    def test_complete_operation(self):
        """Test completing an operation."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        op_mgr.update_operation_progress(operation_id, 100.0)
        
        result = op_mgr.complete_operation(
            operation_id=operation_id,
            result={"carbon_footprint": 5000}
        )
        assert result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.COMPLETED.value
        assert operation["completed_at"] is not None
        assert operation["progress"] == 100.0
    
    def test_fail_operation(self):
        """Test marking operation as failed."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        
        error_msg = "Database connection failed"
        result = op_mgr.fail_operation(operation_id, error_msg)
        assert result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.FAILED.value
        assert operation["error_message"] == error_msg
    
    def test_cancel_operation(self):
        """Test cancelling an operation."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        result = op_mgr.cancel_operation(operation_id)
        assert result is True
        
        operation = op_mgr.get_operation(operation_id)
        assert operation["status"] == OperationStatus.CANCELLED.value
    
    def test_get_user_operations(self):
        """Test retrieving user operations."""
        op_mgr = LongRunningOperation()
        user_id = "test_user_2"
        
        # Create multiple operations
        op1 = op_mgr.create_operation(user_id, "agent1", "Task 1")
        op2 = op_mgr.create_operation(user_id, "agent2", "Task 2")
        op3 = op_mgr.create_operation("other_user", "agent1", "Task 3")
        
        op_mgr.start_operation(op1)
        op_mgr.complete_operation(op2)
        
        # Get user operations
        operations = op_mgr.get_user_operations(user_id)
        assert len(operations) == 2
        
        # Filter by status
        running_ops = op_mgr.get_user_operations(user_id, status=OperationStatus.RUNNING.value)
        assert len(running_ops) == 1
        
        # Filter by agent
        agent1_ops = op_mgr.get_user_operations(user_id, agent_name="agent1")
        assert len(agent1_ops) == 1
    
    def test_get_paused_operations(self):
        """Test retrieving paused operations."""
        op_mgr = LongRunningOperation()
        user_id = "test_user_3"
        
        op1 = op_mgr.create_operation(user_id, "agent1", "Task 1")
        op2 = op_mgr.create_operation(user_id, "agent2", "Task 2")
        
        op_mgr.start_operation(op1)
        op_mgr.start_operation(op2)
        
        op_mgr.pause_operation(op1, "Test pause")
        
        paused = op_mgr.get_paused_operations(user_id)
        assert len(paused) == 1
        assert paused[0]["operation_id"] == op1
    
    def test_get_operation_history(self):
        """Test operation history tracking."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        op_mgr.update_operation_progress(operation_id, 50.0)
        op_mgr.pause_operation(operation_id, "Manual pause")
        op_mgr.resume_operation(operation_id)
        op_mgr.complete_operation(operation_id)
        
        history = op_mgr.get_operation_history(operation_id)
        
        assert len(history) >= 5  # created, started, paused, resumed, completed
        assert history[0]["action"] == "created"
        assert history[-1]["action"] == "completed"
    
    def test_checkpoint_state_persistence(self):
        """Test that checkpoint state is correctly saved and retrieved."""
        op_mgr = LongRunningOperation()
        operation_id = op_mgr.create_operation(
            user_id="test_user",
            agent_name="test_agent",
            task_description="Test task"
        )
        
        op_mgr.start_operation(operation_id)
        
        state_data = {
            "current_step": 5,
            "processed_items": 100,
            "results": ["item1", "item2", "item3"]
        }
        
        op_mgr.update_operation_progress(operation_id, 75.0, state_data)
        op_mgr.pause_operation(operation_id, checkpoint_state=state_data)
        
        checkpoint = op_mgr.resume_operation(operation_id)
        
        assert checkpoint.state["current_step"] == 5
        assert checkpoint.state["processed_items"] == 100
        assert checkpoint.state["results"] == ["item1", "item2", "item3"]


class TestOperationsTools:
    """Test suite for operation tools."""
    
    def test_start_operation_tool(self):
        """Test start_long_running_operation tool."""
        tool_context = MockToolContext("test_user")
        
        result = start_long_running_operation(
            agent_name="test_agent",
            task_description="Analyze carbon data",
            estimated_duration_minutes=45,
            tool_context=tool_context
        )
        
        assert result["status"] == "success"
        assert "operation_id" in result
        assert result["agent"] == "test_agent"
    
    def test_operation_lifecycle_tools(self):
        """Test complete lifecycle using tools."""
        tool_context = MockToolContext("test_user_4")
        
        # Start operation
        start_result = start_long_running_operation(
            agent_name="calculator",
            task_description="Carbon calculation",
            tool_context=tool_context
        )
        operation_id = start_result["operation_id"]
        
        # Update progress
        progress_result = update_operation_progress(
            operation_id=operation_id,
            progress=25.0,
            tool_context=tool_context
        )
        assert progress_result["status"] == "success"
        
        # Pause operation
        pause_result = pause_operation(
            operation_id=operation_id,
            reason="User requested pause",
            tool_context=tool_context
        )
        assert pause_result["status"] == "success"
        
        # Check status
        status_result = get_operation_status(operation_id, tool_context=tool_context)
        assert status_result["operation_status"] == OperationStatus.PAUSED.value
        
        # Resume operation
        resume_result = resume_operation(operation_id, tool_context=tool_context)
        assert resume_result["status"] == "success"
        
        # Update progress again
        update_operation_progress(
            operation_id=operation_id,
            progress=100.0,
            tool_context=tool_context
        )
        
        # Complete operation
        complete_result = complete_operation(
            operation_id=operation_id,
            result={"status": "success"},
            tool_context=tool_context
        )
        assert complete_result["status"] == "success"
    
    def test_list_operations_tool(self):
        """Test listing operations."""
        tool_context = MockToolContext("test_user_5")
        
        # Create some operations
        for i in range(3):
            start_long_running_operation(
                agent_name=f"agent_{i}",
                task_description=f"Task {i}",
                tool_context=tool_context
            )
        
        # List all operations
        list_result = list_user_operations(tool_context=tool_context)
        assert list_result["status"] == "success"
        assert list_result["count"] >= 3
    
    def test_list_paused_operations_tool(self):
        """Test listing paused operations."""
        tool_context = MockToolContext("test_user_6")
        
        # Create and pause some operations
        for i in range(2):
            start_result = start_long_running_operation(
                agent_name=f"agent_{i}",
                task_description=f"Task {i}",
                tool_context=tool_context
            )
            
            pause_operation(
                operation_id=start_result["operation_id"],
                reason="Test pause",
                tool_context=tool_context
            )
        
        # List paused operations
        list_result = list_paused_operations(tool_context=tool_context)
        assert list_result["status"] == "success"
        assert list_result["count"] >= 2
    
    def test_operation_history_tool(self):
        """Test getting operation history."""
        tool_context = MockToolContext("test_user_7")
        
        # Create and manipulate operation
        start_result = start_long_running_operation(
            agent_name="test_agent",
            task_description="Test task",
            tool_context=tool_context
        )
        operation_id = start_result["operation_id"]
        
        # Get history
        history_result = get_operation_history(operation_id, tool_context=tool_context)
        assert history_result["status"] == "success"
        assert history_result["history_count"] >= 1
    
    def test_fail_operation_tool(self):
        """Test failing an operation."""
        tool_context = MockToolContext("test_user_8")
        
        start_result = start_long_running_operation(
            agent_name="test_agent",
            task_description="Test task",
            tool_context=tool_context
        )
        operation_id = start_result["operation_id"]
        
        fail_result = fail_operation(
            operation_id=operation_id,
            error_message="Connection timeout",
            tool_context=tool_context
        )
        
        assert fail_result["status"] == "success"
        
        status_result = get_operation_status(operation_id, tool_context=tool_context)
        assert status_result["operation_status"] == OperationStatus.FAILED.value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
