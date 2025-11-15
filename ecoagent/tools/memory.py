"""Enhanced memory tools for EcoAgent system with advanced session management."""

from google.adk.tools import ToolContext
from google.adk.sessions.state import State
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information for the user session.
    
    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.
    
    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"', "timestamp": datetime.now().isoformat()}


def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information in a list format.
    
    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.
    
    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"', "list_length": len(mem_dict[key])}


def recall(key: str, tool_context: ToolContext):
    """
    Recall information from memory.
    
    Args:
        key: the label indexing the memory to retrieve.
        tool_context: The ADK tool context.
    
    Returns:
        The stored value or None if not found.
    """
    mem_dict = tool_context.state
    return mem_dict.get(key, None)


def recall_all(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Recall all stored information.
    
    Args:
        tool_context: The ADK tool context.
    
    Returns:
        A dictionary of all stored key-value pairs.
    """
    return dict(tool_context.state)


def update_user_profile(updates: Dict[str, Any], tool_context: ToolContext):
    """
    Update user profile information in memory.
    
    Args:
        updates: Dictionary of profile fields to update
        tool_context: The ADK tool context
    
    Returns:
        Status message
    """
    profile = tool_context.state.get("user_profile", {})
    profile.update(updates)
    tool_context.state["user_profile"] = profile
    return {"status": "Profile updated", "updated_fields": list(updates.keys())}


def get_user_profile(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieve user profile information.
    
    Args:
        tool_context: The ADK tool context
    
    Returns:
        User profile dictionary
    """
    return tool_context.state.get("user_profile", {})


def add_sustainability_action(action: str, impact: str, tool_context: ToolContext):
    """
    Add a sustainability action to the user's list of adopted practices.
    
    Args:
        action: Description of the sustainability action
        impact: Expected or achieved environmental impact
        tool_context: The ADK tool context
    
    Returns:
        Status message
    """
    actions = tool_context.state.get("sustainability_actions", [])
    new_action = {
        "action": action,
        "impact": impact,
        "date_added": datetime.now().isoformat()
    }
    actions.append(new_action)
    tool_context.state["sustainability_actions"] = actions
    return {"status": "Action added", "action": action, "impact": impact}


def get_sustainability_actions(tool_context: ToolContext) -> List[Dict[str, Any]]:
    """
    Retrieve the user's list of adopted sustainability actions.
    
    Args:
        tool_context: The ADK tool context
    
    Returns:
        List of sustainability actions
    """
    return tool_context.state.get("sustainability_actions", [])


def set_sustainability_goal(goal: str, target_date: str, tool_context: ToolContext):
    """
    Set a sustainability goal for the user.
    
    Args:
        goal: Description of the sustainability goal
        target_date: Target completion date (ISO format)
        tool_context: The ADK tool context
    
    Returns:
        Status message
    """
    goals = tool_context.state.get("sustainability_goals", [])
    new_goal = {
        "goal": goal,
        "target_date": target_date,
        "date_set": datetime.now().isoformat(),
        "status": "in_progress"
    }
    goals.append(new_goal)
    tool_context.state["sustainability_goals"] = goals
    return {"status": "Goal set", "goal": goal, "target_date": target_date}


def get_sustainability_goals(tool_context: ToolContext) -> List[Dict[str, Any]]:
    """
    Retrieve the user's sustainability goals.
    
    Args:
        tool_context: The ADK tool context
    
    Returns:
        List of sustainability goals
    """
    return tool_context.state.get("sustainability_goals", [])


def track_carbon_footprint(footprint_data: Dict[str, float], tool_context: ToolContext):
    """
    Track carbon footprint data with timestamp.
    
    Args:
        footprint_data: Dictionary containing carbon footprint metrics
        tool_context: The ADK tool context
    
    Returns:
        Status message
    """
    history = tool_context.state.get("carbon_footprint_history", [])
    entry = {
        "data": footprint_data,
        "timestamp": datetime.now().isoformat()
    }
    history.append(entry)
    
    # Keep only the last 20 entries to prevent memory bloat
    if len(history) > 20:
        history = history[-20:]
    
    tool_context.state["carbon_footprint_history"] = history
    return {"status": "Carbon footprint tracked", "entry_count": len(history)}


def get_carbon_footprint_history(tool_context: ToolContext) -> List[Dict[str, Any]]:
    """
    Retrieve the user's carbon footprint history.
    
    Args:
        tool_context: The ADK tool context
    
    Returns:
        List of historical carbon footprint entries
    """
    return tool_context.state.get("carbon_footprint_history", [])


def save_session_state(tool_context: ToolContext):
    """
    Helper function to save the current session state (in a real implementation,
    this would persist to a database).
    
    Args:
        tool_context: The ADK tool context
    
    Returns:
        Status message
    """
    # In a real implementation, this would save to a persistent storage
    # For this demo, we're just confirming that the state exists
    state = dict(tool_context.state)
    return {
        "status": "Session state saved", 
        "data_keys": list(state.keys()),
        "timestamp": datetime.now().isoformat()
    }

# Define all enhanced memory tools
enhanced_memory_tools = [
    memorize,
    memorize_list,
    recall,
    recall_all,
    update_user_profile,
    get_user_profile,
    add_sustainability_action,
    get_sustainability_actions,
    set_sustainability_goal,
    get_sustainability_goals,
    track_carbon_footprint,
    get_carbon_footprint_history,
    save_session_state
]