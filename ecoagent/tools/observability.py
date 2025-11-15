"""Observability tools for EcoAgent system - logging, tracing, and metrics."""

import logging
from typing import Dict, Any
from google.adk.tools import ToolContext
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EcoAgentTracer:
    """Simple tracer for tracking agent interactions and performance."""
    
    def __init__(self):
        self.traces = []
        self.metrics = {
            "total_interactions": 0,
            "carbon_calculations": 0,
            "recommendations_provided": 0,
            "goals_set": 0,
            "user_engagement_days": set()
        }
    
    def trace_interaction(self, agent_name: str, user_input: str, response: str, metadata: Dict[str, Any] = None):
        """Record an interaction trace."""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "user_input": user_input,
            "response": response,
            "metadata": metadata or {}
        }
        self.traces.append(trace)
        
        # Update metrics
        self.metrics["total_interactions"] += 1
        if "carbon" in user_input.lower():
            self.metrics["carbon_calculations"] += 1
        elif "recommend" in user_input.lower() or "suggest" in user_input.lower():
            self.metrics["recommendations_provided"] += 1
        elif "goal" in user_input.lower():
            self.metrics["goals_set"] += 1
            
        # Extract date for engagement tracking
        date = datetime.now().strftime("%Y-%m-%d")
        self.metrics["user_engagement_days"].add(date)
        
        # Log interaction
        logger.info(f"Interaction with {agent_name}: {user_input[:50]}...")
    
    def get_traces(self, limit: int = 10) -> list:
        """Get recent traces."""
        return self.traces[-limit:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        metrics_copy = self.metrics.copy()
        metrics_copy["user_engagement_days"] = len(metrics_copy["user_engagement_days"])
        return metrics_copy

# Global tracer instance
tracer = EcoAgentTracer()

def log_interaction(agent_name: str, user_input: str, response: str, tool_context: ToolContext = None):
    """
    Log an interaction between user and agent.
    
    Args:
        agent_name: Name of the agent
        user_input: User's input
        response: Agent's response
        tool_context: Optional tool context
    
    Returns:
        Status message
    """
    metadata = {}
    if tool_context:
        metadata = {
            "user_id": getattr(tool_context, 'user_id', 'unknown'),
            "session_id": getattr(tool_context, 'session_id', 'unknown')
        }
    
    tracer.trace_interaction(agent_name, user_input, response, metadata)
    return {
        "status": "Interaction logged",
        "timestamp": datetime.now().isoformat()
    }

def get_system_metrics(tool_context: ToolContext = None):
    """
    Get system metrics and performance data.
    
    Args:
        tool_context: Optional tool context
    
    Returns:
        Dictionary of system metrics
    """
    metrics = tracer.get_metrics()
    return {
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }

def get_recent_traces(limit: int = 5, tool_context: ToolContext = None):
    """
    Get recent interaction traces.
    
    Args:
        limit: Number of traces to return
        tool_context: Optional tool context
    
    Returns:
        List of recent traces
    """
    return tracer.get_traces(limit)

# Observability tools
observability_tools = [
    log_interaction,
    get_system_metrics,
    get_recent_traces
]

def setup_logging_for_agent(agent_name: str):
    """Set up logging for a specific agent."""
    logger.info(f"Initializing logging for agent: {agent_name}")
    return {"status": f"Logging initialized for {agent_name}"}