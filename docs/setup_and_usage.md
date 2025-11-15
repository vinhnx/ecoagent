# EcoAgent Setup and Usage Guide

## Prerequisites

- Python 3.9 or higher
- Google Cloud Account with access to Gemini API
- Git (for cloning the repository)
- [uv package manager](https://github.com/astral-sh/uv) installed

### Installing uv (if not already installed)

```bash
# Using curl (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew (macOS)
brew install uv
```

## Installation with uv

### 1. Clone the Repository

```bash
git clone https://github.com/vinhnx/ecoagent.git
cd ecoagent
```

### 2. Install Dependencies with uv

```bash
# Create virtual environment and install dependencies (uv automatically creates venv if not present)
uv sync

# Or to install in development mode
uv pip install -e .
```

### 3. Activate the Virtual Environment

uv automatically manages the virtual environment, but if you need to activate it:

```bash
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

### 4. Set Up API Keys

#### Google Gemini API Key

```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API key" in the top right
3. A popup will appear with your API key—copy it
4. Set it in your environment: `export GOOGLE_API_KEY="your-key"`

That's all you need! Gemini includes built-in Google Search grounding for real-time information.

## Configuration

### Environment Variables

Set the following environment variables:

```bash
# Required: Your Google Gemini API key
export GOOGLE_API_KEY="your-api-key-here"

# Optional: Environment configuration
export ECOAGENT_ENVIRONMENT="development"  # or "production"
export ECOAGENT_DATABASE_URL="sqlite:///./ecoagent.db"
export LOG_LEVEL="INFO"

# Optional: Control Gemini Google Search grounding
export ECOAGENT_ENABLE_GOOGLE_SEARCH="true"  # Default: true
```

## Running EcoAgent

### 1. Running the API Service (Recommended)

For web applications and API access:

```bash
# Using uv run (automatically manages the environment)
uv run python -m ecoagent.main

# Or with uvicorn for development with auto-reload
uv run uvicorn ecoagent.api:app --reload --host 0.0.0.0 --port 8080

# In production with gunicorn
uv run gunicorn ecoagent.api:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

The API will be available at:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 2. Running with CLI

The CLI provides an interactive interface to the agent:

```bash
# Interactive chat with the EcoAgent
uv run python -m ecoagent.cli chat

# Send a single message to the agent
uv run python -m ecoagent.cli chat --message "How can I reduce my carbon footprint?"

# Calculate carbon footprint
uv run python -m ecoagent.cli carbon --transportation.miles_driven 500 --transportation.vehicle_mpg 25

# Get recommendations
uv run python -m ecoagent.cli recommend --profile.diet vegetarian --profile.location urban

# Track goals
uv run python -m ecoagent.cli track --goal "Reduce energy use" --target_value 20
```

### 3. Using with Custom Interface

You can integrate EcoAgent with your own interface by importing either system:

```python
# Using the API system (recommended for programmatic access)
from ecoagent.main import get_app
app = get_app()
response = await app.process_query(
    user_id="user123",
    session_id="session456",
    query="How can I reduce my carbon footprint?"
)

# Using the CLI system
import subprocess
result = subprocess.run([
    "uv", "run", "python", "-m", "ecoagent.cli", "chat",
    "--message", "How can I reduce my carbon footprint?"
], capture_output=True, text=True)
print(result.stdout)
```

## Gemini Google Search Grounding

EcoAgent uses Gemini's built-in Google Search grounding to provide real-time environmental information. This feature is enabled by default and requires no additional setup beyond your Gemini API key.

### What It Does

When enabled, Gemini automatically:
- **Searches the web** for current information when needed
- **Provides citations** linking to source URLs
- **Synthesizes information** to answer questions about recent events and data
- **Includes verification** from authoritative sources

Examples of questions that benefit from Google Search grounding:
- "What are the latest solar panel efficiency improvements?"
- "What recycling centers are near me?"
- "What's the latest news on carbon credit markets?"

### Disabling Google Search Grounding

If you want to use only Gemini's training data (to save API calls or avoid web searches):

```bash
export ECOAGENT_ENABLE_GOOGLE_SEARCH=false
```

Or add to your `.env` file:
```env
ECOAGENT_ENABLE_GOOGLE_SEARCH=false
```

For detailed information about Google Search grounding, see [Google Search Grounding Guide](GOOGLE_SEARCH_GROUNDING.md).

## System Architecture Overview

EcoAgent implements a dual architecture system:

### API Service (FastAPI)
- **Best for**: Web applications, mobile apps, programmatic access
- **Access**: HTTP/REST API with automatic documentation
- **Features**: Authentication, rate limiting, monitoring, web hooks
- **Scalability**: Horizontal scaling with standard web patterns

### ADK Agent System (Google ADK)
- **Best for**: Conversational interfaces, direct agent interaction
- **Access**: Agent Development Kit with A2A protocol
- **Features**: Natural conversation flow, agent coordination, memory management
- **Integration**: Native Google AI Platform integration

Both systems share the same underlying tools, models, and functionality.

## Using EcoAgent

### API Service Examples

#### Carbon Footprint Calculation API
```bash
curl -X POST http://localhost:8080/carbon/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "transportation": {"miles_driven": 1000, "vehicle_mpg": 25.0},
    "flight": {"miles_flown": 2000},
    "energy": {"kwh_used": 800, "renewable_ratio": 0.2}
  }'
```

#### Sustainability Goals API
```bash
curl -X POST http://localhost:8080/goals/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "description": "Reduce transportation carbon by 20%",
    "target_value": 200.0,
    "current_value": 250.0,
    "target_date": "2024-12-31T23:59:59"
  }'
```

### CLI Examples

#### Carbon Footprint Calculation
```bash
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 1000 \
  --transportation.vehicle_mpg 25 \
  --flight.miles_flown 4000 \
  --energy.kwh_used 800 \
  --energy.renewable_ratio 0.2
```

#### Recommendations
```bash
uv run python -m ecoagent.cli recommend \
  --profile.name "John" \
  --profile.location "urban" \
  --profile.diet "vegetarian" \
  --goal "reduce-energy-use"
```

#### Interactive Chat
```bash
uv run python -m ecoagent.cli chat

# At prompt:
# > How can I reduce my carbon footprint?
# > What are sustainable practices for urban living?
# > quit
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=ecoagent tests/

# Run specific test file
uv run pytest tests/test_ecoagent.py
```

### Code Quality Checks

```bash
# Linting
uv run ruff check ecoagent/

# Formatting
uv run ruff format ecoagent/

# Type checking
uv run mypy ecoagent/
```

### Dependency Management with uv

```bash
# Add a new dependency
uv add requests

# Add a dev dependency
uv add --dev pytest

# Sync dependencies from pyproject.toml
uv sync

# Update all dependencies
uv sync --refresh

# Generate requirements.txt from uv.lock
uv export -o requirements.txt
```

## Deployment

### Docker Deployment (using uv)

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY . .

# Install dependencies with uv
RUN uv sync --no-dev

# Expose port
EXPOSE 8080

# Run the application
CMD ["uv", "run", "uvicorn", "ecoagent.api:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Production Deployment

For production deployments, consider:

- Use a process manager like systemd or supervisord
- Set up a reverse proxy (nginx, Apache)
- Configure SSL/TLS termination
- Set up monitoring and logging aggregation
- Use a production database (PostgreSQL instead of SQLite)

### Environment-Specific Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
ECOAGENT_ENVIRONMENT=production
ECOAGENT_DATABASE_URL=postgresql://user:password@localhost:5432/ecoagent
LOG_LEVEL=WARNING
UV_CACHE_DIR=/tmp/uv_cache
```

## Troubleshooting

### uv-Specific Issues

#### Dependency Resolution Issues
If you encounter dependency resolution issues:
```bash
# Clear uv cache
uv cache clean

# Refresh dependencies
uv sync --refresh

# Check for conflicts
uv pip check
```

#### Virtual Environment Issues
```bash
# Regenerate virtual environment
rm -rf .venv
uv sync
```

### API Service Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8080

# Kill process using a specific port
kill $(lsof -t -i:8080)
```

### Google Search Grounding Issues

#### Grounding Not Working

If Google Search grounding isn't providing real-time results:

1. **Verify API Key:**
   ```bash
   echo $GOOGLE_API_KEY
   # Should output your API key, not blank
   ```

2. **Check Configuration:**
   ```bash
   echo $ECOAGENT_ENABLE_GOOGLE_SEARCH
   # Should output 'true' or be blank (true is default)
   ```

3. **Test with a Current Event Question:**
   ```bash
   uv run python -m ecoagent.cli chat --message "What are the latest solar innovations?"
   ```

#### Disabling Google Search

If you want to disable Google Search to save API calls or avoid web searches:

```bash
export ECOAGENT_ENABLE_GOOGLE_SEARCH=false
```

### Gemini API Issues

#### API Key Not Recognized
- Verify `GOOGLE_API_KEY` environment variable is set
- Check that the API key has proper permissions for Generative Language API
- Get a new key at [Google AI Studio](https://aistudio.google.com)
- Restart your terminal/shell after setting the environment variable

#### API Quota Exceeded
- Check your usage at [Google Cloud Console](https://console.cloud.google.com)
- Gemini has rate limits; if exceeded, wait before retrying
- For production, consider upgrading to a paid plan

## Advanced Usage

### Running Multiple Interfaces Simultaneously

For development, you can run both API and CLI systems simultaneously:

```bash
# Terminal 1: Run API service
uv run uvicorn ecoagent.api:app --reload --port 8000

# Terminal 2: Test CLI
uv run python -m ecoagent.cli chat --message "Hello"

# Terminal 3: Run interactive CLI
uv run python -m ecoagent.cli chat
```

### Custom Tool Development

To create custom tools that can be used by both systems:

```python
# All tools are located in ecoagent/tools/ and can be imported by both systems
from ecoagent.tools.carbon_calculator import transportation_carbon_tool
from ecoagent.tools.memory import memorize, recall
```

## Examples

### Example 1: Complete Carbon Footprint Calculation (API)

```python
import requests

response = requests.post("http://localhost:8080/carbon/calculate", json={
    "user_id": "example_user",
    "transportation": {"miles_driven": 1500, "vehicle_mpg": 20.0},
    "flight": {"miles_flown": 4000},
    "energy": {"kwh_used": 1000, "renewable_ratio": 0.3}
})

print(f"Total carbon footprint: {response.json()['total_carbon_lbs']} lbs CO2")
```

### Example 2: Sustainability Recommendations (ADK)

```
Input: "I want to become more sustainable but don't know where to start"
Output: "I recommend starting with these high-impact, low-effort changes:
         1. Reduce meat consumption - biggest individual impact
         2. Switch to renewable energy if possible
         3. Reduce car usage by walking/cycling/transit
         4. Minimize food waste
         Would you like specific recommendations based on your location and lifestyle?"
```

The dual architecture allows you to choose the best interface for your use case while maintaining the same powerful underlying functionality.