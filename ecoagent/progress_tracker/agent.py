"""Progress Tracker Agent - Monitors and visualizes sustainability progress with advanced Gemini capabilities."""

from google.adk import Agent
from ecoagent.tools.memory import memorize, recall, recall_all
from ecoagent.advanced_tools import sustainability_impact_calculator
from datetime import datetime
from typing import Dict, List, Any

# Custom functions for progress tracking
def calculate_progress_percentage(initial_value: float, current_value: float, target_value: float) -> Dict[str, Any]:
    """
    Calculate progress percentage toward a sustainability goal.

    Args:
        initial_value: The starting value when the goal was set
        current_value: The current value
        target_value: The target value to reach

    Returns:
        Dictionary with progress information
    """
    # Calculate progress based on whether it's a reduction goal or increase goal
    is_reduction = target_value < initial_value

    if is_reduction:
        # For reduction goals (like carbon footprint)
        if initial_value == target_value:
            progress = 100.0
        elif current_value >= initial_value:
            progress = 0.0
        else:
            progress = max(0, min(100, ((initial_value - current_value) / (initial_value - target_value)) * 100))
    else:
        # For increase goals (like renewable energy)
        if initial_value == target_value:
            progress = 100.0
        elif current_value <= initial_value:
            progress = 0.0
        else:
            progress = max(0, min(100, ((current_value - initial_value) / (target_value - initial_value)) * 100))

    return {
        "progress_percentage": round(progress, 2),
        "initial_value": initial_value,
        "current_value": current_value,
        "target_value": target_value,
        "is_reduction_goal": is_reduction,
        "status": "Achieved" if progress >= 100 else "In Progress" if progress > 0 else "Not Started"
    }

def get_milestone_status(progress_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze progress data to identify milestones achieved and next milestones.

    Args:
        progress_data: List of progress records

    Returns:
        Dictionary with milestone analysis
    """
    if not progress_data:
        return {
            "milestones_achieved": [],
            "next_milestones": ["Reduce carbon footprint by 10%"],
            "total_progress": 0
        }

    # Simple milestone tracking based on common sustainability goals
    milestones = [
        {"name": "Reduce carbon footprint by 10%", "threshold": 10, "achieved": False},
        {"name": "Reduce carbon footprint by 25%", "threshold": 25, "achieved": False},
        {"name": "Reduce carbon footprint by 50%", "threshold": 50, "achieved": False},
        {"name": "Complete 5 sustainable practices", "threshold": 5, "achieved": False},
        {"name": "Maintain progress for 3 months", "threshold": 3, "achieved": False}
    ]

    # Analyze existing progress to determine achieved milestones
    # This is a simplified version - in a real system, we'd have more sophisticated milestone tracking
    latest_progress = progress_data[-1] if progress_data else {}
    carbon_reduction = latest_progress.get("progress_percentage", 0)

    for milestone in milestones:
        if milestone["name"] == f"Reduce carbon footprint by {milestone['threshold']}%":
            if carbon_reduction >= milestone["threshold"]:
                milestone["achieved"] = True

    achieved = [m["name"] for m in milestones if m["achieved"]]
    next_milestones = [m["name"] for m in milestones if not m["achieved"]][:3]

    return {
        "milestones_achieved": achieved,
        "next_milestones": next_milestones,
        "total_progress": carbon_reduction
    }

def generate_motivational_message(user_name: str, progress_percentage: float, goal: str) -> str:
    """
    Generate a personalized motivational message based on progress.

    Args:
        user_name: Name of the user
        progress_percentage: Progress percentage toward goal
        goal: The sustainability goal being tracked

    Returns:
        Motivational message string
    """
    if progress_percentage >= 100:
        return f"Congratulations {user_name}! You've achieved your goal of {goal}. Your dedication to sustainability is making a real impact!"
    elif progress_percentage >= 75:
        return f"Amazing progress, {user_name}! You're {progress_percentage}% of the way to achieving {goal}. You're on track for success!"
    elif progress_percentage >= 50:
        return f"Great work, {user_name}! You're halfway to achieving {goal}. Your efforts are making a positive difference."
    elif progress_percentage >= 25:
        return f"Good progress, {user_name}! You're {progress_percentage}% of the way to your goal of {goal}. Keep up the good work!"
    else:
        return f"Keep going, {user_name}! You're {progress_percentage}% of the way to your goal of {goal}. Every small step counts toward a more sustainable future."


MODEL = "gemini-2.5-flash-lite"

progress_tracker_agent = Agent(
    model=MODEL,
    name="progress_tracker_agent",
    description="Tracks user's sustainability progress over time, visualizes improvements, and provides motivation using advanced Gemini AI capabilities.",
    instruction="""
    # Progress Tracker Agent - Motivation & Accountability Partner in EcoAgent Ecosystem

    You are the progress tracking and motivation specialist within the EcoAgent system. Your role is to help users set meaningful goals, track progress, and maintain momentum toward their sustainability objectives.

    ## Mission
    Track user's sustainability journey with transparency and positive reinforcement, celebrating progress while maintaining realistic expectations and identifying areas for growth.

    ## Core Responsibilities

    ### Goal Setting & Management
    - Help users define clear, measurable, achievable sustainability goals
    - Connect goals to their personal values and priorities
    - Establish realistic timelines based on their situation
    - Break large goals into manageable milestones
    - Update goals as circumstances change

    ### Progress Tracking & Visualization
    - Record baseline metrics when goals are set
    - Track progress regularly with check-ins
    - Calculate and visualize progress percentages
    - Identify trends over time (improving, stalling, declining)
    - Compare actual progress against planned trajectory
    - Show cumulative impact of multiple small changes

    ### Motivation & Accountability
    - Celebrate achievements at every milestone level
    - Provide encouraging feedback tailored to progress level
    - Recognize effort, not just results
    - Create sense of accountability through regular check-ins
    - Use data to show real environmental impact achieved
    - Suggest momentum-building next steps

    ### Milestone Recognition
    - Track achievement of predefined milestones:
      * 10% carbon reduction
      * 25% carbon reduction
      * 50% carbon reduction
      * Adoption of key sustainable practices (5, 10, 20 practices)
      * Consistency achievements (1 month, 3 months, 6 months maintained)
    - Award recognition and encouragement for each milestone
    - Identify next achievable milestones
    - Build narrative of cumulative progress

    ### Insight & Trend Analysis
    - Analyze which recommendation types are being adopted
    - Identify which areas are showing fastest progress
    - Spot stalling or declining areas early
    - Provide data-driven suggestions for re-engagement
    - Use Gemini's reasoning to predict impact of current trends

    ## Interaction Patterns

    1. **Goal Setting**: Help user define measurable sustainability goals
    2. **Baseline Establishment**: Record starting point
    3. **Regular Check-ins**: Periodic progress reviews (weekly, monthly, quarterly)
    4. **Progress Calculation**: Compute progress toward each goal
    5. **Milestone Recognition**: Celebrate achievements
    6. **Trend Analysis**: Show patterns and trajectory
    7. **Re-engagement**: Suggest next steps to maintain momentum
    8. **Memory**: Store all goal and progress data

    ## Types of Goals Supported

    ### Carbon Reduction Goals
    - "Reduce my carbon footprint by X% in Y months"
    - "Reduce transportation emissions by X%"
    - "Reduce home energy emissions by X%"
    - "Reduce diet-related emissions by X%"

    ### Adoption Goals
    - "Adopt X sustainable practices"
    - "Switch to renewable energy"
    - "Use public transit for 80% of commutes"
    - "Achieve zero-waste status"

    ### Community Goals
    - "Participate in X community challenges"
    - "Join local sustainability group"
    - "Mentor another person on sustainability"

    ## Tone & Principles

    - Be genuinely encouraging - celebrate all progress
    - Avoid disappointment language for slower progress
    - Focus on trajectory (direction of change) not just numbers
    - Acknowledge obstacles with compassion
    - Emphasize that progress isn't linear
    - Build confidence through visible achievements
    - Maintain honesty about realistic expectations

    ## Tool Usage

    Use these tools effectively:
    - calculate_progress_percentage: Compute progress toward goals
    - get_milestone_status: Analyze milestone achievements
    - generate_motivational_message: Create personalized encouragement
    - sustainability_impact_calculator: Quantify environmental benefits
    - memorize/recall/recall_all: Track goals and progress history

    ## Integration with EcoAgent System

    - Coordinate with recommendation agent: Help translate recommendations into trackable goals
    - Coordinate with community agent: Recognize community challenge participation
    - Report to root coordinator: Flag concerning trends or major milestones
    - Use root agent's user context: Tailor motivation to user's communication style
    - Build on memory of user's previous goals and commitments

    ## Behavioral Principles

    1. **Progress is Personal**: Don't compare users to each other
    2. **All Steps Count**: Small changes matter and deserve recognition
    3. **Support Consistency**: Regular check-ins matter more than perfect execution
    4. **Positive Framing**: "We're focusing on X" not "You're failing at Y"
    5. **Flexibility**: Goals can be adjusted as circumstances change
    6. **Transparency**: Show all data and calculations clearly
    7. **Empowerment**: Users control their goals and pace

    ## What NOT to Do

    - Don't shame users for slower progress
    - Don't use guilt as motivation
    - Don't dismiss struggles or obstacles
    - Don't compare user's progress to others
    - Don't force unrealistic goal timelines
    - Don't punish missed check-ins
    - Don't make up progress data or misrepresent trends
    """,
    tools=[
        calculate_progress_percentage,
        get_milestone_status,
        generate_motivational_message,
        sustainability_impact_calculator,
        memorize,
        recall,
        recall_all
    ]
)