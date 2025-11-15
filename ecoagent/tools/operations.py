"""Tools for managing long-running operations - pause/resume capabilities."""

from typing import Dict, Any, Optional, List
from ecoagent.operations import operations_manager, OperationStatus


def start_long_running_operation(
    agent_name: str,
    task_description: str,
    estimated_duration_minutes: int = 30,
    metadata: Optional[Dict[str, Any]] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    Start a new long-running operation.
    
    This tool should be called when an agent begins a task that might take
    significant time and may need to be paused/resumed.
    
    Args:
        agent_name: Name of the agent executing the task
        task_description: Description of what the task does
        estimated_duration_minutes: Estimated time to complete in minutes
        metadata: Additional metadata to store with the operation
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Operation details including operation_id
    """
    user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
    
    operation_id = operations_manager.create_operation(
        user_id=user_id,
        agent_name=agent_name,
        task_description=task_description,
        estimated_duration_minutes=estimated_duration_minutes,
        metadata=metadata
    )
    
    # Start the operation
    operations_manager.start_operation(operation_id)
    
    operation = operations_manager.get_operation(operation_id)
    
    return {
        "status": "success",
        "operation_id": operation_id,
        "agent": agent_name,
        "task": task_description,
        "message": f"Operation {operation_id} started for agent {agent_name}"
    }


def update_operation_progress(
    operation_id: str,
    progress: float,
    state: Optional[Dict[str, Any]] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    Update the progress of a running operation.
    
    Args:
        operation_id: The operation ID to update
        progress: Progress percentage (0-100)
        state: Optional state data to save
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Updated operation progress
    """
    success = operations_manager.update_operation_progress(
        operation_id=operation_id,
        progress=progress,
        state=state
    )
    
    if success:
        operation = operations_manager.get_operation(operation_id)
        return {
            "status": "success",
            "operation_id": operation_id,
            "progress": operation["progress"],
            "message": f"Progress updated to {progress}%"
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to update progress. Operation may not exist or be in invalid state."
        }


def pause_operation(
    operation_id: str,
    reason: Optional[str] = None,
    checkpoint_state: Optional[Dict[str, Any]] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    Pause a running operation.
    
    This creates a checkpoint that can be used to resume the operation later
    with the exact same state.
    
    Args:
        operation_id: The operation ID to pause
        reason: Reason for pausing (optional)
        checkpoint_state: State to save for resumption (optional)
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Pause confirmation with checkpoint info
    """
    success = operations_manager.pause_operation(
        operation_id=operation_id,
        reason=reason,
        checkpoint_state=checkpoint_state
    )
    
    if success:
        operation = operations_manager.get_operation(operation_id)
        return {
            "status": "success",
            "operation_id": operation_id,
            "paused_at": operation["paused_at"],
            "progress": operation["progress"],
            "pause_reason": reason,
            "message": f"Operation paused at {operation['progress']}% completion"
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to pause operation. It may not be running or may not exist."
        }


def resume_operation(
    operation_id: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Resume a paused operation.
    
    This retrieves the checkpoint and returns the saved state so execution
    can continue from where it was paused.
    
    Args:
        operation_id: The operation ID to resume
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Checkpoint data with saved state for resuming
    """
    checkpoint = operations_manager.resume_operation(operation_id)
    
    if checkpoint:
        operation = operations_manager.get_operation(operation_id)
        return {
            "status": "success",
            "operation_id": operation_id,
            "resumed_at": operation["started_at"],
            "progress": checkpoint.progress,
            "state": checkpoint.state,
            "message": f"Operation resumed from {checkpoint.progress}% progress",
            "checkpoint_timestamp": checkpoint.timestamp
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to resume operation. It may not be paused or may not exist."
        }


def complete_operation(
    operation_id: str,
    result: Optional[Dict[str, Any]] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    Mark an operation as completed.
    
    Args:
        operation_id: The operation ID to complete
        result: Optional result data from the operation
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Completion confirmation
    """
    success = operations_manager.complete_operation(
        operation_id=operation_id,
        result=result
    )
    
    if success:
        operation = operations_manager.get_operation(operation_id)
        return {
            "status": "success",
            "operation_id": operation_id,
            "completed_at": operation["completed_at"],
            "duration": operation.get("duration"),
            "message": "Operation completed successfully"
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to complete operation."
        }


def fail_operation(
    operation_id: str,
    error_message: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Mark an operation as failed with an error message.
    
    Args:
        operation_id: The operation ID that failed
        error_message: Error message describing the failure
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Failure confirmation
    """
    success = operations_manager.fail_operation(
        operation_id=operation_id,
        error_message=error_message
    )
    
    if success:
        return {
            "status": "success",
            "operation_id": operation_id,
            "message": f"Operation marked as failed: {error_message}"
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to mark operation as failed."
        }


def cancel_operation(
    operation_id: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Cancel a pending, running, or paused operation.
    
    Args:
        operation_id: The operation ID to cancel
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Cancellation confirmation
    """
    success = operations_manager.cancel_operation(operation_id)
    
    if success:
        return {
            "status": "success",
            "operation_id": operation_id,
            "message": "Operation cancelled successfully"
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Failed to cancel operation."
        }


def get_operation_status(
    operation_id: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Get the current status of an operation.
    
    Args:
        operation_id: The operation ID to check
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Operation status and details
    """
    operation = operations_manager.get_operation(operation_id)
    
    if operation:
        return {
            "status": "success",
            "operation_id": operation_id,
            "operation_status": operation["status"],
            "progress": operation["progress"],
            "agent": operation["agent_name"],
            "task": operation["task_description"],
            "created_at": operation["created_at"],
            "started_at": operation["started_at"],
            "paused_at": operation["paused_at"],
            "completed_at": operation["completed_at"],
            "pause_reason": operation.get("pause_reason")
        }
    else:
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Operation not found"
        }


def list_user_operations(
    status: Optional[str] = None,
    agent_name: Optional[str] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    List all operations for the current user.
    
    Args:
        status: Optional filter by status (pending, running, paused, completed, failed, cancelled)
        agent_name: Optional filter by agent name
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        List of operations matching criteria
    """
    user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
    
    operations = operations_manager.get_user_operations(
        user_id=user_id,
        status=status,
        agent_name=agent_name
    )
    
    return {
        "status": "success",
        "count": len(operations),
        "operations": [
            {
                "operation_id": op["operation_id"],
                "agent": op["agent_name"],
                "task": op["task_description"],
                "status": op["status"],
                "progress": op["progress"],
                "created_at": op["created_at"]
            }
            for op in operations
        ]
    }


def list_paused_operations(tool_context=None) -> Dict[str, Any]:
    """
    List all paused operations for the current user.
    
    Args:
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        List of paused operations
    """
    user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
    
    paused_ops = operations_manager.get_paused_operations(user_id)
    
    return {
        "status": "success",
        "count": len(paused_ops),
        "paused_operations": [
            {
                "operation_id": op["operation_id"],
                "agent": op["agent_name"],
                "task": op["task_description"],
                "progress": op["progress"],
                "paused_at": op["paused_at"],
                "pause_reason": op.get("pause_reason")
            }
            for op in paused_ops
        ]
    }


def get_operation_history(
    operation_id: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Get the complete history of actions taken on an operation.
    
    Args:
        operation_id: The operation ID
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        List of operations with timestamps and details
    """
    history = operations_manager.get_operation_history(operation_id)
    
    return {
        "status": "success",
        "operation_id": operation_id,
        "history_count": len(history),
        "history": [
            {
                "action": h["action"],
                "timestamp": h["timestamp"],
                "details": h["details"]
            }
            for h in history
        ]
    }
