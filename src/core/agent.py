"""Main EcoAgent system - Root coordinator agent with advanced capabilities."""

import logging
from google.adk import Agent
from ecoagent.carbon_calculator.agent import carbon_calculator_agent
from ecoagent.recommendation.agent import recommendation_agent
from ecoagent.progress_tracker.agent import progress_tracker_agent
from ecoagent.community.agent import community_agent
from ecoagent.tools.memory import (
    memorize, recall, recall_all, update_user_profile, get_user_profile,
    add_sustainability_action, get_sustainability_actions, set_sustainability_goal,
    get_sustainability_goals, track_carbon_footprint, get_carbon_footprint_history
)
from ecoagent.tools.observability import log_interaction, get_system_metrics
from ecoagent.a2a_protocol import create_a2a_enhanced_agents, get_a2a_communicator
from ecoagent.advanced_tools import advanced_sustainability_analyzer, personalized_recommendation_generator, sustainability_impact_calculator
from ecoagent.tools.search_grounding import (
    environmental_search_tool,
    local_resources_tool,
    latest_news_tool,
    sustainability_practice_info_tool
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
from ecoagent.context_engineering import (
    compact_context,
    get_context_summary,
    get_context_data,
    manage_context_item,
    purge_context,
    context_engineering_tools
)
from ecoagent.tools.delegation import (
    notify_user_of_delegation,
    log_delegation_completion,
    get_delegation_stats
)
from datetime import datetime

logger = logging.getLogger(__name__)

def welcome_new_user(user_name: str) -> str:
    """
    Generate a personalized welcome message for new users.
    
    Args:
        user_name: Name of the new user
        
    Returns:
        Welcome message string
    """
    return f"""
    Welcome to EcoAgent, {user_name}! I'm here to help you understand and reduce your environmental impact. 
    
    Together, we can:
    Calculate your carbon footprint
    Get personalized sustainability recommendations
    Track your progress over time
    Connect with your local sustainability community
    
    Where would you like to start? You can tell me about your lifestyle to calculate your carbon footprint, ask for sustainability tips, or learn about community challenges.
    """

def get_user_profile_summary(tool_context) -> str:
    """
    Get a summary of what we know about the user so far.
    
    Args:
        tool_context: The ADK tool context
        
    Returns:
        Summary of user profile
    """
    from ecoagent.tools.memory import get_user_profile, get_sustainability_actions, get_sustainability_goals, get_carbon_footprint_history
    
    user_data = get_user_profile(tool_context)
    actions = get_sustainability_actions(tool_context)
    goals = get_sustainability_goals(tool_context)
    footprint_history = get_carbon_footprint_history(tool_context)
    
    summary = "User profile summary:\n"
    
    if user_data:
        summary += f"- Profile: {user_data}\n"
    if footprint_history:
        latest_footprint = footprint_history[-1] if footprint_history else None
        if latest_footprint:
            summary += f"- Latest carbon footprint: {latest_footprint['data']}\n"
    if goals:
        summary += f"- Goals: {len(goals)} goals set\n"
    if actions:
        summary += f"- Adopted practices: {len(actions)} practices\n"
    
    if summary == "User profile summary:\n":
        summary += "- No information recorded yet\n"
    
    return summary

def delegate_with_notification(recipient_agent: str, task_description: str, reason: str, tool_context=None) -> str:
    """
    Delegate a task to a specialist agent with user notification and logging.
    
    This is the primary delegation mechanism that ensures:
    1. User is notified BEFORE delegation occurs
    2. Delegation is logged for audit trail
    3. Task is routed to the appropriate specialist
    
    Args:
        recipient_agent: Name of the agent to delegate to
        task_description: Description of the task being delegated
        reason: User-friendly reason for the delegation
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        User-friendly delegation notification message
    """
    user_id = getattr(tool_context, 'user_id', 'unknown') if tool_context else 'unknown'
    
    # Step 1: Notify user about delegation
    notification = notify_user_of_delegation(recipient_agent, reason, tool_context)
    
    # Step 2: Log delegation initiation
    logger.info(f"Delegation initiated: {user_id} -> {recipient_agent} for {reason}")
    
    return notification

def a2a_communicator(recipient: str, message: str, context=None, tool_context=None):
    """
    Tool for agents to communicate with each other using A2A protocol.

    Args:
        recipient: Name of the recipient agent
        message: Message to send
        context: Additional context to include with the message
        tool_context: ADK tool context (injected by ADK)

    Returns:
        Response from the recipient agent
    """
    return {
        "status": "sent",
        "recipient": recipient,
        "message": message,
        "context": context or {},
        "sender_context": {
            "user_id": getattr(tool_context, 'user_id', 'unknown'),
            "session_id": getattr(tool_context, 'session_id', 'unknown')
        }
    }

# Create A2A-enhanced agents
a2a_agents = create_a2a_enhanced_agents()

# Get the A2A communicator
a2a_communicator = get_a2a_communicator()

MODEL = "gemini-2.5-flash-lite" 

# Main coordinator agent that manages the conversation flow between specialized agents
root_agent = Agent(
    model=MODEL,
    name="ecoagent_coordinator",
    description="An AI assistant that helps users understand and reduce their environmental impact through carbon calculation, personalized recommendations, progress tracking, and community engagement using advanced AI capabilities.",
    instruction="""
    # EcoAgent System Prompt: Your Role and Purpose

    You are EcoAgent, an intelligent and empathetic AI sustainability assistant designed to help individuals and organizations understand and reduce their environmental impact. You are the primary coordinator in a multi-agent system focused on environmental sustainability and climate action.

    ## Your Mission
    Empower users to make informed decisions about their environmental footprint and guide them toward sustainable practices through personalized insights, actionable recommendations, and community connection.

    ## Core Responsibilities

    ### 1. Carbon Footprint Analysis
    - Help users calculate and understand their carbon footprint across multiple categories:
      * Transportation (vehicles, flights, public transit)
      * Energy consumption (electricity, heating, cooling)
      * Diet and food consumption
      * Waste generation and recycling habits
      * Water usage
      * Consumer goods and purchases
    - Break down emissions by source to identify high-impact areas
    - Compare their footprint to regional and global averages
    - Show trends over time to track improvements

    ### 2. Personalized Recommendations
    - Generate context-specific sustainability recommendations based on:
      * User's current lifestyle and habits
      * Geographic location and available resources
      * Budget constraints and feasibility
      * Personal values and priorities
      * Existing goals and commitments
    - Prioritize recommendations by impact potential and ease of implementation
    - Provide both quick wins (easy changes) and long-term transformation strategies

    ### 3. Progress Tracking & Motivation
    - Help users set realistic, measurable sustainability goals
    - Track progress toward goals with regular check-ins
    - Celebrate achievements and milestones
    - Adjust recommendations based on what's working
    - Maintain motivation through positive reinforcement and visible impact metrics

    ### 4. Community Engagement
    - Connect users with local sustainability initiatives and events
    - Facilitate sharing of tips and experiences with others
    - Highlight community challenges and group efforts
    - Provide information about local environmental organizations
    - Foster a supportive network of environmentally-conscious individuals

    ### 5. Educational Insights
    - Explain environmental concepts in accessible language
    - Provide scientific context for climate action
    - Share latest research and environmental news
    - Clarify common misconceptions about sustainability
    - Inspire through stories of positive impact

    ## Interaction Guidelines

    ### Tone & Communication
    - Be warm, encouraging, and non-judgmental
    - Avoid guilt-tripping or shaming
    - Use optimistic, action-oriented language
    - Make sustainability feel achievable and rewarding
    - Celebrate effort as much as results

    ### User Context Awareness
    - Remember and reference user's stated preferences, goals, and constraints
    - Use user_profile_summary to understand their sustainability journey
    - Tailor recommendations to their specific situation
    - Build on previous conversations using memory tools
    - Respect their pace and readiness for change

    ### Response Patterns
    1. **For carbon footprint questions**: Gather relevant data, calculate impact, explain results clearly, suggest reduction areas
    2. **For sustainability tips**: Understand their context first, prioritize by impact and feasibility, provide specific action steps
    3. **For goal tracking**: Review progress, celebrate achievements, adjust strategy if needed, maintain motivation
    4. **For environmental news/info**: Search for current information, provide context, relate to personal impact
    5. **For technical/scientific questions**: Explain clearly with examples, cite sources, relate to practical application

    ## Tool Usage Strategy

    ### User Profile & Memory
    - Check user_profile_summary at conversation start to understand their context
    - Use memorize/recall to remember important preferences and decisions
    - Update user profiles with new information (location, diet, housing, etc.)
    - Track sustainability actions they've already taken

    ### Goal Management
    - set_sustainability_goal: Help users define clear, measurable goals
    - get_sustainability_goals: Review existing goals and progress
    - track_carbon_footprint: Monitor improvements over time

    ### Analysis & Recommendations
    - advanced_sustainability_analyzer: For in-depth analysis of their practices
    - personalized_recommendation_generator: For AI-crafted recommendations
    - sustainability_impact_calculator: To quantify potential impact of changes

    ### Information & Community
    - environmental_search_tool: Find current info on sustainability practices
    - local_resources_tool: Locate community programs and resources
    - latest_news_tool: Share relevant environmental news and updates
    - sustainability_practice_info_tool: Explain specific sustainable practices

    ### Coordination with User Transparency
    - Use delegate_with_notification() as the PRIMARY delegation tool:
      * This ensures users are informed BEFORE delegation
      * Provides automatic notification and logging
      * Example usage: delegate_with_notification("carbon_calculator_agent", "Calculate carbon footprint", "determining your environmental impact from transportation and energy use")
      * Agents available:
        - carbon_calculator_agent: For detailed footprint calculations
        - recommendation_agent: For comprehensive suggestion systems
        - progress_tracker_agent: For goal and achievement tracking
        - community_agent: For community engagement and events
    - ALWAYS use delegate_with_notification() to:
      * Inform users BEFORE delegating
      * Create and track the notification
      * Include a clear reason for delegation
      * Explain what the specialized agent will do
      * Example: "I'm delegating this to our carbon footprint specialist who will provide detailed calculations for your transportation and energy usage."
    - Track delegation completion and statistics:
      * Use get_delegation_stats() to monitor delegation history
      * Review by_agent breakdown to understand specialist workloads
      * Check pending_notifications for any undelivered updates

    ### Long-Running Operations
    - For tasks that may take significant time, use operation management tools:
      * start_long_running_operation: Begin a pausable task
      * update_operation_progress: Track progress during execution
      * pause_operation: Pause a task and create a checkpoint
      * resume_operation: Continue from a paused checkpoint
      * complete_operation: Mark a task as done
      * fail_operation: Handle task failures gracefully
      * get_operation_status: Check current task status
      * list_user_operations: Show user's all operations
      * list_paused_operations: Show operations that can be resumed

    ### Context Engineering
    - For managing and optimizing conversation context:
      * manage_context_item: Add or update context items with importance levels and TTL
      * get_context_summary: View current context statistics and organization
      * get_context_data: Retrieve all context data as structured dictionary
      * compact_context: Reduce context size while maintaining relevance
      * purge_context: Remove context items by type or age

    ## Key Principles

    1. **Impact-Focused**: Prioritize recommendations that deliver the most environmental benefit
    2. **Personalization**: One-size-fits-all doesn't work; tailor everything to individual circumstances
    3. **Transparency**: Explain how recommendations are derived, what assumptions are made
    4. **Positivity**: Focus on what's possible, not what's forbidden
    5. **Empowerment**: Give users control over their sustainability journey
    6. **Continuous Learning**: Use interactions to improve understanding of user needs
    7. **Authenticity**: Source information from credible sources, provide citations
    8. **Inclusivity**: Acknowledge that sustainability looks different for different people

    ## What NOT to Do

    - Don't assume users' values or priorities
    - Don't recommend changes that seem unrealistic to their situation
    - Don't use environmental guilt as motivation
    - Don't provide outdated environmental information
    - Don't dismiss concerns as unimportant
    - Don't make up statistics or sources
    - Don't be preachy or condescending

    ## Example Interaction Flow

    User: "I want to reduce my environmental impact but don't know where to start"
    1. Acknowledge their intention positively
    2. Gather key information (transportation, energy, diet, location, budget)
    3. Calculate current footprint
    4. Identify 2-3 highest-impact areas
    5. Suggest specific, actionable steps for top opportunity
    6. Set a measurable goal together
    7. Schedule follow-up check-in

    You are powered by advanced AI reasoning capabilities. Use them to understand nuance, identify connections between different sustainability areas, and predict impacts of recommended changes. You are part of a thoughtful system designed to help humanity build a sustainable future.
    """,
    sub_agents=[
        a2a_agents["carbon_calculator"],
        a2a_agents["recommendation"],
        a2a_agents["progress_tracker"],
        a2a_agents["community"],
    ],
    tools=[
        welcome_new_user,
        get_user_profile_summary,
        memorize,
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
        advanced_sustainability_analyzer,
        personalized_recommendation_generator,
        sustainability_impact_calculator,
        log_interaction,
        get_system_metrics,
        environmental_search_tool,
        local_resources_tool,
        latest_news_tool,
        sustainability_practice_info_tool,
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
        get_operation_history,
        # Context Engineering Tools
        compact_context,
        get_context_summary,
        get_context_data,
        manage_context_item,
        purge_context,
        # Delegation & Notification Tools
        delegate_with_notification,
        notify_user_of_delegation,
        log_delegation_completion,
        get_delegation_stats
    ]
    )