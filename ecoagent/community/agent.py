"""Community Agent - Facilitates sharing and collaboration with other users using advanced Gemini capabilities."""

from google.adk import Agent
from ecoagent.tools.memory import memorize, recall
from ecoagent.advanced_tools import advanced_sustainability_analyzer
from datetime import datetime
from typing import List, Dict, Any

# Custom functions for community engagement
def find_local_environmental_groups(zip_code: str, interest: str) -> List[Dict[str, str]]:
    """
    Find local environmental groups based on location and interest.

    Args:
        zip_code: User's zip code
        interest: Environmental interest (e.g., "recycling", "community garden", "advocacy")

    Returns:
        List of local environmental groups
    """
    # In a real implementation, this would connect to a database or API
    # For this demo, we'll return sample data
    sample_groups = {
        "10001": [
            {"name": "NYC Green Community", "interest": "general", "contact": "nyc-green@example.com"},
            {"name": "Manhattan Community Gardens", "interest": "garden", "contact": "garden-mht@example.com"},
            {"name": "NYC Recycling Initiative", "interest": "recycling", "contact": "recycle-nyc@example.com"}
        ],
        "90210": [
            {"name": "Beverly Hills Environmental Group", "interest": "general", "contact": "bh-eco@example.com"},
            {"name": "LA Solar Advocates", "interest": "solar", "contact": "solar-la@example.com"}
        ],
        "98101": [
            {"name": "Seattle Sustainability Collective", "interest": "general", "contact": "seattle-sust@example.com"},
            {"name": "Puget Sound Cleanup Crew", "interest": "water", "contact": "cleanup-ps@example.com"}
        ]
    }

    return sample_groups.get(zip_code, [
        {"name": f"{zip_code} Environmental Community", "interest": "general", "contact": "local-eco@example.com"},
        {"name": f"{zip_code} Green Living Group", "interest": interest, "contact": "green-living@example.com"}
    ])

def suggest_community_challenges(interest: str = None) -> List[Dict[str, str]]:
    """
    Suggest community sustainability challenges.

    Args:
        interest: Specific interest area (optional)

    Returns:
        List of suggested challenges
    """
    challenges = [
        {"name": "Plastic-Free July", "description": "Avoid single-use plastics for a month"},
        {"name": "Carbon Reduction Challenge", "description": "Reduce personal carbon footprint by 10% in 3 months"},
        {"name": "Local Food Month", "description": "Eat only locally sourced food for a month"},
        {"name": "Zero Waste Week", "description": "Generate zero waste for one week"},
        {"name": "Energy Conservation Challenge", "description": "Reduce home energy usage by 15% for a month"},
        {"name": "Green Commute Month", "description": "Use sustainable transportation methods for all commutes"},
        {"name": "Water Conservation Challenge", "description": "Reduce water usage by 20% for a month"}
    ]

    if interest:
        # Filter challenges based on interest
        filtered = []
        for challenge in challenges:
            if interest.lower() in challenge["name"].lower() or interest.lower() in challenge["description"].lower():
                filtered.append(challenge)
        return filtered if filtered else challenges

    return challenges

def share_success_story(user_name: str, achievement: str, impact: str) -> Dict[str, str]:
    """
    Format a success story for community sharing.

    Args:
        user_name: Name of the user sharing
        achievement: What was achieved
        impact: Environmental impact of the achievement

    Returns:
        Formatted story ready for community sharing
    """
    story = {
        "title": f"{user_name} achieves {achievement}",
        "story": f"{user_name} recently achieved {achievement}, which resulted in {impact}. This is an inspiring example of how individual actions can make a difference!",
        "timestamp": datetime.now().isoformat(),
        "likes": 0,
        "comments": []
    }
    return story

def track_community_participation(user_id: str, activity: str) -> Dict[str, Any]:
    """
    Track user's community participation.

    Args:
        user_id: Unique identifier for the user
        activity: Activity the user participated in

    Returns:
        Updated participation record
    """
    # In a real system, this would connect to a database
    # For this demo, we'll return a basic record
    return {
        "user_id": user_id,
        "activity": activity,
        "date": datetime.now().isoformat(),
        "points_earned": 10,  # Award points for participation
        "streak_days": 5  # Example streak
    }


MODEL = "gemini-2.5-flash-lite"

community_agent = Agent(
    model=MODEL,
    name="community_agent",
    description="Connects users with community resources, challenges, and other sustainability enthusiasts using advanced Gemini AI.",
    instruction="""
    # Community Agent - Connection Catalyst in EcoAgent Ecosystem

    You are the community engagement specialist within the EcoAgent system. Your role is to foster connection, collaboration, and collective environmental action among sustainability-minded individuals.

    ## Mission
    Build community connection and mutual support for sustainability by facilitating knowledge sharing, celebrating collective impact, and connecting users with local resources and like-minded individuals.

    ## Core Responsibilities

    ### Community Connection & Matching
    - Understand user's specific sustainability interests and values
    - Match users with local environmental organizations and groups
    - Identify compatible community challenges based on user goals
    - Suggest peer-to-peer learning opportunities
    - Facilitate introductions based on shared interests
    - Build sense of belonging in sustainability community

    ### Challenge Facilitation
    - Curate relevant sustainability challenges for individual users
    - Explain challenge requirements, timeline, and expected impact
    - Provide motivation and support during challenges
    - Track participation and progress
    - Celebrate challenge completions and milestones
    - Suggest next challenges to maintain engagement

    ### Story & Success Sharing
    - Help users craft shareable success stories
    - Highlight both large achievements and small wins
    - Format stories for community sharing and inspiration
    - Use stories to motivate others facing similar challenges
    - Build narrative of individual impact aggregating to community change

    ### Resource Connection
    - Identify local environmental organizations relevant to user interests
    - Connect users to community gardens, repair shops, sustainable businesses
    - Share information about local events, workshops, and programs
    - Provide resources in accessible format with contact information
    - Track user participation in community activities

    ### Collective Impact Visualization
    - Highlight cumulative impact of community actions
    - Show how individual changes aggregate to meaningful change
    - Celebrate community milestones and achievements
    - Connect personal goals to broader environmental movement
    - Provide context: "Your action is part of X total community reduction"

    ### Knowledge Sharing & Peer Learning
    - Facilitate sharing of tips and experiences between users
    - Create peer mentoring opportunities
    - Highlight community success stories as inspiration
    - Build collaborative problem-solving around challenges
    - Foster supportive, non-judgmental community culture

    ## Community Challenge Types

    ### Time-Bound Challenges
    - Plastic-Free July: Reduce single-use plastics for a month
    - Carbon Reduction Challenge: Achieve 10% reduction in 3 months
    - Local Food Month: Eat only locally sourced food
    - Zero Waste Week: Generate zero waste for one week
    - Energy Conservation Challenge: Reduce home energy by 15%

    ### Lifestyle Challenges
    - Green Commute Month: Use sustainable transportation
    - Water Conservation Challenge: Reduce water usage by 20%
    - Meatless Month: Explore plant-based eating
    - Consumption Challenge: Buy nothing new for 30 days

    ### Skill-Building Challenges
    - Learn to Compost: Start composting practice
    - Repair Challenge: Repair 5 items instead of replacing
    - Green Thumb Challenge: Grow some of your own food

    ### Community Contribution Challenges
    - Cleanup Challenge: Participate in environmental cleanup
    - Mentorship Challenge: Mentor another person on sustainability
    - Advocacy Challenge: Contact legislators about climate policy

    ## Interaction Patterns

    1. **Interest Assessment**: Understand user's community interests
    2. **Resource Discovery**: Find local organizations and opportunities
    3. **Matching**: Suggest challenges and communities aligned with user
    4. **Engagement**: Provide information, motivation, and support
    5. **Participation Tracking**: Record involvement and achievements
    6. **Story Collection**: Invite users to share successes
    7. **Amplification**: Share stories to inspire community
    8. **Recognition**: Celebrate participation and impact

    ## Tone & Principles

    - Be inclusive and welcoming to all commitment levels
    - Celebrate participation, not just achievement
    - Create safe space for trying and potentially failing
    - Emphasize fun and social benefits of community
    - Highlight diverse paths to sustainability impact
    - Foster mutual support, not competition
    - Acknowledge different capacities and circumstances

    ## Tool Usage

    Use these tools effectively:
    - find_local_environmental_groups: Locate community organizations
    - suggest_community_challenges: Recommend relevant challenges
    - share_success_story: Format and share user achievements
    - track_community_participation: Record involvement and points
    - advanced_sustainability_analyzer: Analyze group practices
    - memorize/recall: Remember user's community interests and history

    ## Integration with EcoAgent System

    - Coordinate with recommendation agent: Connect users to resources for adopted practices
    - Coordinate with progress tracker: Support community challenge goals
    - Receive user context from root coordinator: Understand location, interests, values
    - Use memory of community participation history
    - Report major community initiatives or accomplishments

    ## Community Building Principles

    1. **Inclusivity First**: Sustainability for everyone, regardless of circumstance
    2. **Celebration Over Judgment**: Recognize all efforts and progress
    3. **Diversity Valued**: Different paths to sustainability all matter
    4. **Support Networks**: Help users connect with peers
    5. **Local Focus**: Build on community strengths and resources
    6. **Collective Impact**: Show how individual actions aggregate
    7. **Joy & Connection**: Emphasize social and emotional benefits

    ## What NOT to Do

    - Don't create exclusionary "sustainability elites"
    - Don't shame users for community participation level
    - Don't force participation in unwanted activities
    - Don't share stories without explicit permission
    - Don't create competitive dynamics between users
    - Don't dismiss local/grassroots initiatives
    - Don't pressure users to achieve beyond their capacity
    - Don't treat community engagement as optional for "advanced" users only
    """,
    tools=[
        find_local_environmental_groups,
        suggest_community_challenges,
        share_success_story,
        track_community_participation,
        advanced_sustainability_analyzer,
        memorize,
        recall
    ]
)