"""Advanced tools for EcoAgent system that leverage Gemini capabilities."""

from ecoagent.tools.memory import memorize, recall
from ecoagent.gemini_utils import analyze_sustainability_practice, get_personalized_recommendations, get_gemini_client
from google.adk.tools import ToolContext
from typing import Dict, Any, List
import json

def advanced_sustainability_analyzer(practice_description: str, user_context: Dict[str, Any] = None, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Advanced analysis of sustainability practices using Gemini AI.
    
    Args:
        practice_description: Description of the sustainability practice to analyze
        user_context: Additional context about the user (optional)
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Detailed analysis of the practice
    """
    # Use the Gemini utility function
    analysis = analyze_sustainability_practice(practice_description)
    
    # Add user context if provided
    if user_context:
        analysis["user_context_applied"] = True
        analysis["user_friendly_explanation"] = f"Based on your situation ({user_context}), this practice would be {analysis['effectiveness']} effective."
    else:
        analysis["user_context_applied"] = False
        analysis["user_friendly_explanation"] = f"This practice is {analysis['effectiveness']} effective at reducing environmental impact."
    
    return analysis

def personalized_recommendation_generator(user_profile: Dict[str, Any], goals: List[str], tool_context: ToolContext = None) -> List[Dict[str, Any]]:
    """
    Generate personalized sustainability recommendations using Gemini AI.
    
    Args:
        user_profile: Dictionary containing user information
        goals: List of user sustainability goals
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        List of personalized recommendations
    """
    return get_personalized_recommendations(user_profile, goals)

def sustainability_impact_calculator(data: Dict[str, Any], tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Calculate and analyze sustainability impact using Gemini AI.
    
    Args:
        data: Dictionary containing sustainability data to analyze
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Analysis of the environmental impact
    """
    client = get_gemini_client()
    if not client:
        return {
            "error": "Gemini API not available",
            "estimates": {
                "carbon_footprint_reduction": "Unknown",
                "water_savings": "Unknown", 
                "waste_reduction": "Unknown"
            }
        }
    
    prompt = f"""
    Analyze the following sustainability data and calculate environmental impact:
    
    {json.dumps(data, indent=2)}
    
    Calculate estimated environmental impact in these areas:
    1. Carbon footprint reduction (in lbs or kg of CO2 equivalent)
    2. Water savings (in gallons or liters)  
    3. Waste reduction (in lbs or kg)
    4. Additional environmental benefits
    
    Provide estimates even if some data is approximate.
    """
    
    schema = {
        "carbon_footprint_reduction": "string",
        "water_savings": "string",
        "waste_reduction": "string", 
        "additional_benefits": "string",
        "confidence_level": "string"
    }
    
    return client.generate_structured_output(prompt, schema)

# List of all advanced tools - these are just functions that will be used by ADK as tools
advanced_tools = [
    advanced_sustainability_analyzer,
    personalized_recommendation_generator,
    sustainability_impact_calculator,
    memorize,
    recall
]