"""Delegation tracking and user notification tools for A2A communication."""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DelegationTracker:
    """Tracks and manages agent delegations for observability and user notification."""
    
    def __init__(self):
        self.delegations = []
        self.user_notifications = {}
    
    def log_delegation(self, user_id: str, from_agent: str, to_agent: str, 
                      task: str, notification: str) -> Dict[str, Any]:
        """
        Log a delegation and prepare user notification.
        
        Args:
            user_id: User ID
            from_agent: Source agent name
            to_agent: Target agent name
            task: Description of task being delegated
            notification: Message to show user
            
        Returns:
            Delegation record
        """
        record = {
            "id": len(self.delegations),  # Track record by index
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "task": task,
            "notification": notification,
            "status": "initiated",
            "completion_timestamp": None,
            "result_summary": None
        }
        self.delegations.append(record)
        
        # Store notification for user
        if user_id not in self.user_notifications:
            self.user_notifications[user_id] = []
        self.user_notifications[user_id].append(notification)
        
        logger.info(f"Delegation logged: {from_agent} -> {to_agent} | User: {user_id} | Task: {task}")
        
        return record
    
    def mark_delegation_complete(self, delegation_id: int, result_summary: str = None) -> Dict[str, Any]:
        """
        Mark a delegation as completed.
        
        Args:
            delegation_id: ID of the delegation record
            result_summary: Summary of the delegation results
            
        Returns:
            Updated delegation record
        """
        if 0 <= delegation_id < len(self.delegations):
            record = self.delegations[delegation_id]
            record["status"] = "completed"
            record["completion_timestamp"] = datetime.now().isoformat()
            record["result_summary"] = result_summary
            logger.info(f"Delegation completed: {record['from_agent']} -> {record['to_agent']} | User: {record['user_id']}")
            return record
        return None
    
    def get_user_notifications(self, user_id: str) -> list:
        """Get pending notifications for a user."""
        return self.user_notifications.get(user_id, [])
    
    def clear_user_notifications(self, user_id: str):
        """Clear notifications for a user after displaying them."""
        if user_id in self.user_notifications:
            self.user_notifications[user_id] = []
    
    def get_delegation_history(self, user_id: str = None, limit: int = 10) -> list:
        """Get delegation history, optionally filtered by user."""
        if user_id:
            history = [d for d in self.delegations if d["user_id"] == user_id]
        else:
            history = self.delegations
        
        return history[-limit:] if limit else history

# Global delegation tracker
delegation_tracker = DelegationTracker()

def notify_user_of_delegation(delegated_to: str, reason: str, tool_context=None) -> str:
    """
    Create a user-friendly notification about delegation.
    
    Args:
        delegated_to: Name of agent being delegated to
        reason: Why we're delegating
        tool_context: ADK tool context
        
    Returns:
        User notification message
    """
    user_id = getattr(tool_context, 'user_id', 'user') if tool_context else 'user'
    
    # Create appropriate notification based on agent
    notifications = {
        "carbon_calculator_agent": f"I'm delegating this to our carbon footprint specialist who will provide detailed calculations for {reason}.",
        "recommendation_agent": f"I'm passing this to our recommendation specialist to provide personalized sustainability advice on {reason}.",
        "progress_tracker_agent": f"I'm delegating this to our progress tracking specialist to help you monitor and celebrate your {reason}.",
        "community_agent": f"I'm connecting you with our community specialist who can help with {reason}."
    }
    
    notification = notifications.get(
        delegated_to, 
        f"I'm delegating this to a specialist to help with {reason}."
    )
    
    # Log the delegation
    delegation_tracker.log_delegation(
        user_id=user_id,
        from_agent="root_agent",
        to_agent=delegated_to,
        task=reason,
        notification=notification
    )
    
    logger.info(f"User notification: {user_id} | {delegated_to} | {reason}")
    
    return notification

def log_delegation_completion(user_id: str, from_agent: str, to_agent: str, 
                             result_summary: str, tool_context=None) -> Dict[str, Any]:
    """
    Log completion of a delegation.
    
    Args:
        user_id: User ID
        from_agent: Source agent
        to_agent: Target agent
        result_summary: Summary of results
        tool_context: ADK tool context
        
    Returns:
        Completion record
    """
    completion = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "result_summary": result_summary,
        "status": "completed"
    }
    
    logger.info(f"Delegation completed: {from_agent} <- {to_agent} | User: {user_id}")
    
    return completion

def get_delegation_stats(user_id: str = None, tool_context=None) -> Dict[str, Any]:
    """
    Get statistics about delegations.
    
    Args:
        user_id: Optional user ID to filter by
        tool_context: ADK tool context
        
    Returns:
        Delegation statistics
    """
    history = delegation_tracker.get_delegation_history(user_id)
    
    stats = {
        "total_delegations": len(history),
        "by_agent": {},
        "recent_delegations": history[-5:] if history else [],
        "pending_notifications": delegation_tracker.get_user_notifications(user_id) if user_id else []
    }
    
    for record in history:
        agent = record["to_agent"]
        stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
    
    return stats
