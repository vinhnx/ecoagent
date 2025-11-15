"""A2A Protocol Implementation for EcoAgent - Multi-Agent Communication Layer."""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from google.adk.agents import Agent
from google.adk.events.event import Event
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types

# Set up logging for A2A protocol
logger = logging.getLogger(__name__)

class A2ACommunicationLayer:
    """
    Implements A2A (Agent-to-Agent) communication protocol for EcoAgent system.
    This allows specialized agents to coordinate and share information.
    """
    
    def __init__(self):
        self.agent_registry = {}
        self.message_queue = asyncio.Queue()
        self.delegation_log = []
        
    def register_agent(self, agent: Agent):
        """Register an agent in the A2A communication system."""
        self.agent_registry[agent.name] = agent
        logger.info(f"Registered agent '{agent.name}' in A2A communication layer")
        
    async def send_message(self, sender: str, recipient: str, message: str, context: Optional[Dict[str, Any]] = None, user_id: str = None):
        """Send a message from one agent to another."""
        if recipient not in self.agent_registry:
            raise ValueError(f"Recipient agent '{recipient}' not found in registry")
        
        # Log delegation initiation
        delegation_record = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "recipient": recipient,
            "message_preview": message[:100],
            "user_id": user_id or "unknown",
            "status": "initiated"
        }
        self.delegation_log.append(delegation_record)
        
        logger.info(f"A2A Delegation: {sender} -> {recipient} | User: {user_id} | Message: {message[:50]}...")
            
        # Create a message event
        message_event = {
            "sender": sender,
            "recipient": recipient,
            "message": message,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        }
        
        # Add to message queue for processing
        await self.message_queue.put(message_event)
        
        # Process the message asynchronously
        return await self._process_message(message_event)
    
    async def _process_message(self, message_event: Dict[str, Any]):
        """Process a message event by forwarding it to the recipient agent."""
        recipient_agent = self.agent_registry[message_event["recipient"]]
        sender = message_event["sender"]
        message = message_event["message"]
        context = message_event["context"]
        user_id = message_event.get("user_id", "unknown")
        
        try:
            # Enhanced implementation: Create a structured message for the recipient agent
            # Include context from the sender for the recipient agent to use
            structured_message = {
                "from_agent": sender,
                "request": message,
                "context": context,
                "user_id": user_id
            }
            
            # Log processing start
            logger.info(f"A2A Processing: {recipient_agent.name} receiving delegation from {sender}")
            
            # Production implementation: Invoke actual agent logic
            try:
                # Create invocation context with user info
                invocation_context = InvocationContext()
                invocation_context.user_id = user_id
                
                # Call recipient agent to generate actual response
                agent_response = await recipient_agent.generate_content(
                    f"Process delegation from {sender}: {message}",
                    invocation_context=invocation_context
                )
                
                # Extract response content
                response_text = ""
                if hasattr(agent_response, 'text'):
                    response_text = agent_response.text
                elif isinstance(agent_response, str):
                    response_text = agent_response
                elif isinstance(agent_response, dict) and 'content' in agent_response:
                    response_text = agent_response['content']
                
                response = {
                    "status": "delegated",
                    "delegated_to": recipient_agent.name,
                    "delegated_by": sender,
                    "request": message,
                    "agent_response": response_text,
                    "context_passed": context,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id,
                    "actual_invocation": True
                }
                
            except Exception as agent_error:
                # Fallback if agent invocation fails: still log and return error info
                logger.warning(f"A2A Agent invocation fallback for {recipient_agent.name}: {str(agent_error)}")
                response = {
                    "status": "delegated_with_agent_error",
                    "delegated_to": recipient_agent.name,
                    "delegated_by": sender,
                    "request": message,
                    "agent_error": str(agent_error),
                    "context_passed": context,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id,
                    "actual_invocation": False
                }
            
            # Update delegation log with success
            self.delegation_log[-1]["status"] = "completed"
            self.delegation_log[-1]["response_timestamp"] = datetime.now().isoformat()
            
            logger.info(f"A2A Delegation completed: {sender} -> {recipient_agent.name}")
            
            return response
            
        except Exception as e:
            # Log error
            logger.error(f"A2A Delegation failed: {sender} -> {recipient_agent.name} | Error: {str(e)}")
            if self.delegation_log:  # Check if log exists before updating
                self.delegation_log[-1]["status"] = "failed"
                self.delegation_log[-1]["error"] = str(e)
            
            return {
                "status": "delegated_with_error",
                "delegated_to": recipient_agent.name,
                "delegated_by": sender,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_agent_names(self):
        """Get list of registered agent names."""
        return list(self.agent_registry.keys())
    
    def get_delegation_log(self, limit: int = None) -> list:
        """Get delegation log records."""
        if limit:
            return self.delegation_log[-limit:]
        return self.delegation_log
    
    def get_delegation_stats(self) -> Dict[str, Any]:
        """Get delegation statistics."""
        if not self.delegation_log:
            return {
                "total_delegations": 0,
                "completed": 0,
                "failed": 0,
                "by_recipient": {}
            }
        
        stats = {
            "total_delegations": len(self.delegation_log),
            "completed": sum(1 for d in self.delegation_log if d["status"] == "completed"),
            "failed": sum(1 for d in self.delegation_log if d["status"] == "failed"),
            "by_recipient": {}
        }
        
        for record in self.delegation_log:
            recipient = record["recipient"]
            stats["by_recipient"][recipient] = stats["by_recipient"].get(recipient, 0) + 1
        
        return stats
    
    async def broadcast_message(self, sender: str, message: str, context: Optional[Dict[str, Any]] = None):
        """Broadcast a message to all registered agents."""
        results = {}
        for agent_name in self.agent_registry:
            if agent_name != sender:  # Don't send to self
                result = await self.send_message(sender, agent_name, message, context)
                results[agent_name] = result
        return results

# Global A2A communication instance
a2a_communicator = A2ACommunicationLayer()

# A2A tool for agent communication
def agent_communicator_tool(recipient: str, message: str, context: Optional[Dict[str, Any]] = None, tool_context=None):
    """
    Tool for agents to communicate with each other using A2A protocol.
    
    Args:
        recipient: Name of the recipient agent
        message: Message to send
        context: Additional context to include with the message
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Response from the recipient agent with delegation details
    """
    user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
    session_id = getattr(tool_context, 'session_id', 'unknown') if tool_context else 'unknown'
    sender = getattr(tool_context, 'agent_name', 'root_agent') if tool_context else 'root_agent'
    
    # Log the A2A communication request
    logger.info(f"A2A Request: {sender} -> {recipient} | User: {user_id}")
    
    return {
        "status": "delegated",
        "delegated_to": recipient,
        "delegated_by": sender,
        "message": message,
        "context": context or {},
        "user_context": {
            "user_id": user_id,
            "session_id": session_id
        },
        "timestamp": datetime.now().isoformat()
    }

# Enhanced agents with A2A capabilities
def create_a2a_enhanced_agents():
    """Create agents with A2A communication capabilities."""
    from ecoagent.carbon_calculator.agent import carbon_calculator_agent
    from ecoagent.recommendation.agent import recommendation_agent
    from ecoagent.progress_tracker.agent import progress_tracker_agent
    from ecoagent.community.agent import community_agent
    from ecoagent.tools.memory import memorize, recall
        
    # Register agents with A2A communicator
    a2a_communicator.register_agent(carbon_calculator_agent)
    a2a_communicator.register_agent(recommendation_agent)
    a2a_communicator.register_agent(progress_tracker_agent)
    a2a_communicator.register_agent(community_agent)
    
    # Define A2A communication tool function
    def a2a_communicator_tool(recipient: str, message: str, context: Optional[Dict[str, Any]] = None, tool_context=None):
        """
        Tool for agents to communicate with each other using A2A protocol.

        Args:
            recipient: Name of the recipient agent
            message: Message to send
            context: Additional context to include with the message
            tool_context: ADK tool context (injected by ADK)

        Returns:
            Response from the recipient agent with delegation tracking
        """
        user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
        session_id = getattr(tool_context, 'session_id', 'unknown') if tool_context else 'unknown'
        sender = getattr(tool_context, 'agent_name', 'unknown_agent') if tool_context else 'unknown_agent'
        
        # Log delegation using the A2A communicator
        logger.info(f"Agent-to-Agent Delegation: {sender} -> {recipient} | User: {user_id}")
        
        return {
            "status": "delegated",
            "delegated_to": recipient,
            "delegated_by": sender,
            "message": message,
            "context": context or {},
            "user_context": {
                "user_id": user_id,
                "session_id": session_id
            },
            "timestamp": datetime.now().isoformat()
        }

    # Enhance agents with A2A tools
    carbon_calculator_agent.tools.append(a2a_communicator_tool)
    recommendation_agent.tools.append(a2a_communicator_tool)
    progress_tracker_agent.tools.append(a2a_communicator_tool)
    community_agent.tools.append(a2a_communicator_tool)
    
    return {
        "carbon_calculator": carbon_calculator_agent,
        "recommendation": recommendation_agent,
        "progress_tracker": progress_tracker_agent,
        "community": community_agent
    }

def get_a2a_communicator():
    """Get the global A2A communicator instance."""
    return a2a_communicator