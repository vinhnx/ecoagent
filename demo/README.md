# EcoAgent Demo

This folder contains comprehensive demonstrations of the EcoAgent system capabilities, including an interactive CLI chat interface and example usage scenarios.

## Quick Start

### Prerequisites

-   Python 3.9+
-   Google API key (optional, but recommended for full functionality)
-   Project installed: `uv sync`

### Running the Interactive CLI Demo

The simplest way to experience EcoAgent is through the interactive CLI chat:

```bash
# Run interactive chat
uv run python -m ecoagent.cli chat

# Or with a specific user ID
uv run python -m ecoagent.cli chat --user_id myname
```

You'll see a prompt like this:

```
🌱 EcoAgent Interactive Chat (type 'quit' or 'exit' to exit)
Ask about carbon footprint, sustainability tips, or environmental impact.
------------------------------------------------------------
myname@ecoagent>
```

Type your questions and the EcoAgent will respond with sustainability advice. Type `quit` or `exit` to end the conversation.

## Demo Scenarios

### 1. Carbon Footprint Calculator Demo

Calculate your carbon emissions from various activities:

```bash
# Transportation carbon footprint
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 500 \
  --transportation.vehicle_mpg 25

# Include flight emissions
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 500 \
  --transportation.vehicle_mpg 25 \
  --flight.miles_flown 2000

# Include home energy usage
uv run python -m ecoagent.cli carbon \
  --energy.kwh_used 800 \
  --energy.renewable_ratio 0.25
```

### 2. Sustainability Recommendations Demo

Get personalized recommendations based on your profile:

```bash
# Get recommendations for urban vegetarian
uv run python -m ecoagent.cli recommend \
  --profile.name "Alice" \
  --profile.location "San Francisco" \
  --profile.diet vegetarian \
  --profile.family_size 2 \
  --profile.housing_type apartment

# Get recommendations for suburban family
uv run python -m ecoagent.cli recommend \
  --profile.name "Bob" \
  --profile.location "Portland" \
  --profile.diet omnivore \
  --profile.family_size 4 \
  --profile.housing_type house
```

### 3. Goal Tracking Demo

Set and track sustainability goals:

```bash
# Track a carbon reduction goal
uv run python -m ecoagent.cli track \
  --goal "Reduce household carbon footprint by 20%" \
  --target_value 20.0 \
  --current_value 0.0

# Track a renewable energy goal
uv run python -m ecoagent.cli track \
  --goal "Increase renewable energy usage to 75%" \
  --target_value 75.0 \
  --current_value 25.0
```

### 4. Profile Management Demo

View and manage your user profile:

```bash
# Get current profile information
uv run python -m ecoagent.cli profile --get --user_id demo_user

# Update profile (extended functionality)
uv run python -m ecoagent.cli profile --update --user_id demo_user
```

### 5. Single Message Chat Demo

Ask a quick question without entering interactive mode:

```bash
# Single query
uv run python -m ecoagent.cli chat \
  --user_id john_doe \
  --message "How can I reduce my carbon footprint from transportation?"

# Ask about renewable energy
uv run python -m ecoagent.cli chat \
  --message "What are the benefits of solar panels?"

# Ask about lifestyle changes
uv run python -m ecoagent.cli chat \
  --message "How can I adopt a more sustainable lifestyle?"
```

### 6. API Service Demo

Run the EcoAgent as a web service:

```bash
# Start the API service
uv run python -m ecoagent.cli serve --host 0.0.0.0 --port 8000

# In another terminal, query the service
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo_user",
    "session_id": "session_123",
    "query": "How can I reduce my carbon footprint?"
  }'
```

### 7. System Information Demo

View system information and configuration:

```bash
uv run python -m ecoagent.cli info
```

Expected output:

```
🌱 EcoAgent System Information:
  Version: 1.0.0
  Model: gemini-2.0-flash
  Environment: development
  Database: SQLite
  API Endpoint: http://localhost:8000
  API Docs: http://localhost:8000/docs
  System initialized: 2024-01-15 10:30:45
```

## Python API Usage

You can also use EcoAgent programmatically from Python:

```python
import asyncio
from ecoagent.main import get_app

async def demo():
    app = get_app()
    await app.initialize()

    # Ask a question
    response = await app.process_query(
        user_id="demo_user",
        session_id="session_123",
        query="How can I reduce my carbon footprint?"
    )
    print(f"Response: {response}")

asyncio.run(demo())
```

## Demo Stories

### Story 1: Morning Commute Optimization

Start your day with sustainable transportation questions and calculations:

1. Calculate your current commute carbon footprint
2. Ask for recommendations to reduce it
3. Track your progress over time

```bash
# Calculate current impact
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 50 \
  --transportation.vehicle_mpg 25

# Get recommendations interactively
uv run python -m ecoagent.cli chat --user_id morning_commuter
# Ask: "How can I make my 50-mile daily commute more sustainable?"
```

### Story 2: Home Energy Optimization

Understand and improve your household energy consumption:

1. Calculate your current energy carbon footprint
2. Ask about renewable energy options
3. Set goals for renewable energy adoption

```bash
# Calculate home energy impact
uv run python -m ecoagent.cli carbon \
  --energy.kwh_used 1000 \
  --energy.renewable_ratio 0.10

# Get personalized recommendations
uv run python -m ecoagent.cli chat --user_id homeowner
# Ask: "What's the best renewable energy option for my climate?"
```

### Story 3: Sustainable Lifestyle Transition

Get comprehensive guidance on adopting a sustainable lifestyle:

1. Get recommendations based on your lifestyle
2. Ask specific questions in chat
3. Track multiple sustainability goals

```bash
# Get recommendations
uv run python -m ecoagent.cli recommend \
  --profile.location "Austin, TX" \
  --profile.housing_type house \
  --profile.family_size 3 \
  --goal "live-sustainably"

# Chat about implementation
uv run python -m ecoagent.cli chat --user_id sustainability_seeker
# Ask questions about each recommendation
```

## Features Demonstrated

### 1. Carbon Calculation

-   Transportation emissions (cars, flights)
-   Home energy usage
-   Renewable energy impact
-   Comprehensive breakdown

### 2. AI-Powered Recommendations

-   Personalized based on location, lifestyle, family size
-   Specific to sustainability goals
-   Context-aware and actionable
-   Powered by Google Gemini

### 3. Goal Tracking

-   Set sustainability targets
-   Track progress over time
-   Persistent storage in database
-   Multi-user support

### 4. Interactive Chat

-   Natural language interface
-   Conversation context awareness
-   Sustainable lifestyle coaching
-   Real-time responses

### 5. Data Management

-   User profiles
-   Carbon footprint history
-   Goal tracking
-   Session management

## Troubleshooting

### API Key Issues

If you see warnings about missing API key:

```bash
export GOOGLE_API_KEY='your-api-key'
```

### Database Issues

To reset the local database:

```bash
rm ecoagent.db  # or your configured database file
```

### Chat Not Responding

Ensure your Google API key is correctly set:

```bash
echo $GOOGLE_API_KEY
```

## Advanced Options

### Logging

```bash
LOG_LEVEL=DEBUG uv run python -m ecoagent.cli chat
```

### Custom Database

```bash
ECOAGENT_DB_PATH=/custom/path/db.sqlite uv run python -m ecoagent.cli chat
```

### Production Mode

```bash
ECOAGENT_ENVIRONMENT=production uv run python -m ecoagent.cli serve
```

## Next Steps

1. **Try the interactive chat** - Get a feel for the natural language interface
2. **Calculate your carbon footprint** - See your environmental impact
3. **Get recommendations** - Discover actionable sustainability practices
4. **Set goals** - Track your progress toward a sustainable lifestyle
5. **Explore the API** - Integrate EcoAgent into your own applications

## Learning Resources

-   [Main README](../README.md) - Complete project documentation
-   [Architecture Guide](../IMPLEMENTATION_README.md) - Technical details
-   [Context Engineering](../CONTEXT_ENGINEERING_SUMMARY.md) - Advanced features
-   [API Documentation](../docs/) - API reference

## Questions or Issues?

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the main README for configuration details
3. Check log output: `LOG_LEVEL=DEBUG` to get verbose logging
4. Review the GitHub issues for similar problems

Happy sustainable living! 🌱
