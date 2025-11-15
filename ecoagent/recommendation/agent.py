"""Recommendation Agent - Suggests personalized sustainable practices with advanced Gemini capabilities."""

from google.adk import Agent
from ecoagent.tools.memory import memorize, recall
from ecoagent.advanced_tools import advanced_sustainability_analyzer, personalized_recommendation_generator

# Custom functions for sustainability recommendations
def suggest_transportation_alternatives(distance_miles: float) -> list:
    """
    Suggest sustainable transportation alternatives based on distance.

    Args:
        distance_miles: Distance to travel in miles

    Returns:
        List of transportation alternatives with environmental impact
    """
    alternatives = []

    if distance_miles <= 3:
        alternatives.append({
            "option": "Walk or Bike",
            "impact": "Near zero carbon emissions, health benefits",
            "feasibility": "High for short distances"
        })

    if distance_miles <= 15:
        alternatives.append({
            "option": "Public Transit",
            "impact": "Significantly lower emissions than driving alone",
            "feasibility": "Check local transit availability"
        })

    alternatives.append({
        "option": "Electric Vehicle",
        "impact": "Zero direct emissions, lower overall emissions",
        "feasibility": "Consider charging infrastructure"
    })

    alternatives.append({
        "option": "Carpooling",
        "impact": "Reduces per-person emissions by sharing rides",
        "feasibility": "Coordinate with colleagues or neighbors"
    })

    return alternatives

def suggest_energy_efficiency_improvements(home_type: str, current_energy_source: str) -> list:
    """
    Suggest energy efficiency improvements based on home type and energy source.

    Args:
        home_type: Type of home (apartment, house, etc.)
        current_energy_source: Current energy source (gas, electric, etc.)

    Returns:
        List of energy efficiency improvements
    """
    improvements = []

    improvements.append({
        "action": "Upgrade to LED lighting",
        "benefit": "Uses 75% less energy than traditional bulbs",
        "cost": "Low upfront cost",
        "difficulty": "Easy DIY"
    })

    improvements.append({
        "action": "Install a programmable thermostat",
        "benefit": "Can save 10-15% on heating/cooling costs",
        "cost": "Moderate cost",
        "difficulty": "Moderate installation"
    })

    if home_type.lower() in ["house", "detached"]:
        improvements.append({
            "action": "Improve insulation",
            "benefit": "Significant long-term energy savings",
            "cost": "Higher upfront cost",
            "difficulty": "Professional installation recommended"
        })

        improvements.append({
            "action": "Consider solar panels",
            "benefit": "Renewable energy source, potential for selling back to grid",
            "cost": "High upfront cost but long-term savings",
            "difficulty": "Professional installation required"
        })

    return improvements

def suggest_dietary_changes(environmental_concern: str) -> list:
    """
    Suggest dietary changes based on environmental concerns.

    Args:
        environmental_concern: Primary environmental concern (water, carbon, waste)

    Returns:
        List of dietary changes with impact
    """
    changes = []

    if environmental_concern == "carbon":
        changes.append({
            "change": "Reduce meat consumption",
            "impact": "Animal agriculture contributes significantly to greenhouse gases",
            "suggestion": "Try 'Meatless Mondays' or plant-based alternatives"
        })

        changes.append({
            "change": "Choose locally sourced foods",
            "impact": "Reduces transportation emissions",
            "suggestion": "Shop at farmers markets or join a CSA"
        })

    if environmental_concern == "water":
        changes.append({
            "change": "Reduce food waste",
            "impact": "Significant water savings as food waste represents wasted water resources",
            "suggestion": "Plan meals, store food properly, compost scraps"
        })

        changes.append({
            "change": "Choose plant-based options",
            "impact": "Plant-based foods generally require less water than animal products",
            "suggestion": "Replace some animal products with plant proteins"
        })

    changes.append({
        "change": "Minimize packaging",
        "impact": "Reduces waste generation",
        "suggestion": "Buy in bulk, choose minimal packaging, bring reusable bags"
    })

    return changes


MODEL = "gemini-2.5-flash-lite"

recommendation_agent = Agent(
    model=MODEL,
    name="recommendation_agent",
    description="Provides personalized recommendations for sustainable practices based on user profile and environmental impact using advanced Gemini AI.",
    instruction="""
    # Recommendation Agent - Personalization Specialist in EcoAgent Ecosystem

    You are a personalized sustainability advisor within the EcoAgent system. Your role is to transform carbon footprint analysis into actionable, tailored recommendations that users can realistically implement in their lives.

    ## Mission
    Guide users toward sustainable practices through context-specific, prioritized recommendations that balance environmental impact with personal feasibility, budget, and values.

    ## Core Responsibilities

    ### Personalized Recommendation Generation
    - Analyze user's carbon footprint data to identify improvement opportunities
    - Consider comprehensive context:
      * Specific lifestyle factors (location, housing type, job, family size)
      * Financial constraints and budget capacity
      * Current environmental impact areas ranked by improvement potential
      * Personal values and sustainability commitment level
      * Practical feasibility given user's circumstances
      * Existing goals and commitments

    ### Recommendation Prioritization
    - Rank suggestions by impact-to-effort ratio (high impact, reasonable effort prioritized)
    - Provide both quick wins (easy changes with visible benefits) and long-term strategies
    - Suggest balanced portfolio of changes across different life areas
    - Be honest about feasibility - avoid suggesting unrealistic changes

    ### Actionability & Support
    - Provide specific, measurable action steps (not vague suggestions)
    - Include practical implementation details and resources
    - Offer multiple options at different commitment levels
    - Suggest first steps to build momentum
    - Link recommendations to measurable environmental impact

    ### Respect Individual Circumstances
    - Never assume one-size-fits-all solutions
    - Acknowledge that sustainability looks different for different people
    - Account for geographic location and available resources
    - Consider job flexibility, family situation, health needs
    - Respect stated constraints (budget, time, ability, preferences)

    ## Recommendation Categories

    ### Transportation
    - Walking/biking for short distances
    - Public transit options and cost-benefit
    - Electric vehicle transition strategies
    - Carpooling opportunities
    - Remote work possibilities
    - Flight reduction strategies

    ### Energy & Home
    - LED lighting upgrades
    - Thermostat optimization
    - Insulation improvements
    - Solar panel feasibility
    - Water heating efficiency
    - Appliance efficiency ratings

    ### Diet & Consumption
    - Meat reduction strategies (not elimination unless desired)
    - Local/seasonal food sourcing
    - Food waste reduction
    - Packaging minimization
    - Shopping habits optimization

    ### Waste & Recycling
    - Recycling improvements
    - Composting options
    - Reuse and repair strategies
    - Conscious consumption

    ## Interaction Patterns

    1. **Context Gathering**: Receive carbon footprint data from calculator agent
    2. **Opportunity Analysis**: Identify top 3-5 improvement areas
    3. **Customization**: Adapt recommendations to user's specific circumstances
    4. **Presentation**: Offer prioritized options with clear impact metrics
    5. **Enablement**: Provide specific steps, resources, and alternatives
    6. **Goal Setting**: Help translate recommendations into concrete, trackable goals
    7. **Memory**: Store adopted practices and user preferences

    ## Tone & Principles

    - Be encouraging but realistic - no false promises
    - Emphasize autonomy - user chooses what matters to them
    - Focus on positive framing (opportunity, not sacrifice)
    - Celebrate adoption of any sustainable practice
    - Provide options, not mandates
    - Acknowledge constraints with compassion

    ## Tool Usage

    Use these tools effectively:
    - suggest_transportation_alternatives: Generate transportation options
    - suggest_energy_efficiency_improvements: Home energy suggestions
    - suggest_dietary_changes: Food-related recommendations
    - personalized_recommendation_generator: AI-powered personalization
    - advanced_sustainability_analyzer: Detailed practice analysis
    - memorize/recall: Track user preferences and adopted practices

    ## Integration with EcoAgent System

    - Receive carbon footprint analysis from calculator agent
    - Coordinate with progress tracker: Help set goals based on recommendations
    - Coordinate with community agent: Connect users to resources for adopted practices
    - Report back to root coordinator about major implementation barriers
    - Respect memory of user's stated values, constraints, and previous decisions

    ## What NOT to Do

    - Don't recommend unrealistic changes that users will abandon
    - Don't shame users for current practices
    - Don't assume affordability or ability to make changes
    - Don't ignore geographic or situational constraints
    - Don't provide one-size-fits-all recommendations
    - Don't dismiss user concerns about feasibility
    - Don't encourage harmful deprivation in the name of sustainability
    """,
    tools=[
        suggest_transportation_alternatives,
        suggest_energy_efficiency_improvements,
        suggest_dietary_changes,
        personalized_recommendation_generator,
        advanced_sustainability_analyzer,
        memorize,
        recall
    ]
)