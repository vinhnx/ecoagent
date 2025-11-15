# EcoAgent: AI-Powered Sustainability Assistant

![EcoAgent Logo](resources/ecoagent.png)

EcoAgent is an advanced AI system designed to help individuals and organizations understand, track, and reduce their environmental impact. Built with Google's Agent Development Kit (ADK) and powered by Gemini AI, it provides personalized recommendations, carbon footprint calculations, progress tracking, and community engagement for sustainability.

## Features

-   **Carbon Footprint Calculator**: Accurate calculation of environmental impact from transportation, energy usage, and consumption
-   **Personalized Recommendations**: Tailored sustainability advice based on user profile and goals
-   **Progress Tracking**: Monitor and visualize environmental improvements over time
-   **Community Engagement**: Connect users with local sustainability groups and challenges
-   **Advanced AI Integration**: Powered by Google's Gemini model for sophisticated analysis
-   **Google Search Grounding**: Real-time environmental information retrieval and current news
-   **Location-Based Resources**: Access to local environmental resources and services
-   **Memory & State Management**: Persistent user profiles and progress tracking
-   **Multi-Agent Architecture**: Specialized agents for different sustainability aspects
-   **Observability**: Logging, metrics, and monitoring capabilities

![demo](resources/demo.png)

## Quick Start

### Prerequisites

-   Python 3.9+
-   Google Cloud account with access to Gemini API
-   Google Custom Search API key and search engine ID (optional, for search grounding features)
-   Docker (optional, for containerization)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/vinhnx/ecoagent.git
cd ecoagent
```

2. **Install uv (if not already installed):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Set up the environment and dependencies:**

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

4. **Configure API keys:**

```bash
export GOOGLE_API_KEY='your-gemini-api-key'
```

### Configuration

Create a `.env` file in the root directory with your configuration:

```env
# Required: Your Gemini API key
GOOGLE_API_KEY=your_api_key_here

# Optional: Other settings
ECOAGENT_ENVIRONMENT=development
ECOAGENT_DB_PATH=/path/to/db.sqlite
LOG_LEVEL=INFO

# Optional: Gemini Google Search grounding (enabled by default)
ECOAGENT_ENABLE_GOOGLE_SEARCH=true
```

Gemini includes built-in Google Search grounding for real-time environmental information—no additional API keys or setup required.

## Running the Application

### Development Mode

```bash
uv run python -m ecoagent.main
```

### Production Mode

```bash
# Using Docker
docker build -t ecoagent .
docker run -p 8080:8080 -e GOOGLE_API_KEY=$GOOGLE_API_KEY ecoagent

# Or directly with Python
python -m ecoagent.main --host 0.0.0.0 --port 8080
```

## CLI Usage

The EcoAgent system includes a powerful command-line interface for interacting with the sustainability assistant without needing a web interface.

### Installation

After installing the package with `uv pip install -e .`, you can use the CLI directly:

```bash
# Get help
ecoagent --help

# Calculate carbon footprint
ecoagent carbon --transportation.miles_driven 500 --transportation.vehicle_mpg 25

# Get sustainability recommendations
ecoagent recommend --profile.diet vegetarian --profile.location urban --goal "reduce-energy-use"

# Track sustainability goals
ecoagent track --goal "Reduce household energy consumption" --target_value 20.0

# Chat with the EcoAgent
ecoagent chat --user_id myname
ecoagent chat --message "How can I reduce my carbon footprint?"
```

### Available Commands

-   `carbon`: Calculate your carbon footprint from transportation, flights, or energy usage
-   `recommend`: Get personalized sustainability recommendations based on your profile
-   `track`: Set and track sustainability goals
-   `profile`: Manage your user profile information
-   `chat`: Interact directly with the EcoAgent in conversation
-   `serve`: Run the API service (alternative to direct API usage)
-   `info`: Show system information

### Advanced Usage

```bash
# Interactive chat session
ecoagent chat

# Run the API service
ecoagent serve --host 0.0.0.0 --port 8080

# Get detailed system information
ecoagent info
```

## Architecture

### Multi-Agent System

The system implements a hierarchical multi-agent architecture:

-   **Root Coordinator Agent**: Manages conversation flow and delegates to specialists
-   **Carbon Calculator Agent**: Computes environmental impact from user data
-   **Recommendation Agent**: Provides personalized sustainability recommendations
-   **Progress Tracker Agent**: Monitors and visualizes sustainability progress
-   **Community Agent**: Facilitates community engagement and resource sharing

### Search Grounding System

The system includes a Google Search grounding capability:

-   **Environmental Information Search**: Real-time search for current environmental topics and best practices
-   **Local Resources Finder**: Location-based search for environmental services and organizations
-   **News Aggregation**: Latest updates on environmental topics and sustainability practices
-   **Practice Information**: Detailed information about specific sustainability practices

### Technology Stack

-   **Backend**: Google Agent Development Kit (ADK)
-   **AI**: Google Gemini for advanced reasoning
-   **Database**: SQLite for local development, PostgreSQL for production
-   **API**: FastAPI for web interface
-   **Observability**: Structured logging and metrics collection
-   **Containerization**: Docker for deployment

## Google Search Grounding

EcoAgent leverages Gemini's built-in Google Search grounding for real-time environmental information. This feature is enabled by default and includes:

-   **Real-time information** - Latest environmental news, policies, and research
-   **Location-based results** - Find local environmental resources and services
-   **Current data** - Recent sustainability metrics and climate information
-   **Source citations** - Automatic links to authoritative sources

For detailed information, see [Google Search Grounding Guide](docs/GOOGLE_SEARCH_GROUNDING.md).

**Note:** This feature is optional. Set `ECOAGENT_ENABLE_GOOGLE_SEARCH=false` to use only Gemini's training data.

## Development

### Testing

```bash
# Run unit tests
uv run pytest tests/

# Run with code coverage
uv run pytest --cov=ecoagent tests/
```

### Linting & Formatting

```bash
# Lint the code
uv run flake8 ecoagent/

# Format the code
uv run black ecoagent/
```

### Type Checking

```bash
uv run mypy ecoagent/
```

## Metrics & Monitoring

EcoAgent provides comprehensive observability:

-   **Logs**: Structured JSON logs with contextual information
-   **Metrics**: Runtime metrics for performance monitoring
-   **Traces**: Request tracing for debugging
-   **Health Checks**: Built-in health check endpoint

## Deployment

### Docker Deployment

```bash
# Build the image
docker build -t ecoagent:latest .

# Run the container
docker run -d --name ecoagent \
  -p 8080:8080 \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --restart unless-stopped \
  ecoagent:latest
```

### Kubernetes Deployment

The repository includes Kubernetes manifests in the `/deploy` directory for production deployments.

## Quick Start Demo

Try these commands to experience EcoAgent in 5 minutes:

```bash
# 1. Interactive chat (recommended starting point)
uv run python -m ecoagent.cli chat

# 2. Calculate your carbon footprint
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 500 \
  --transportation.vehicle_mpg 25

# 3. Get sustainability recommendations
uv run python -m ecoagent.cli recommend \
  --profile.location "San Francisco" \
  --profile.diet vegetarian

# 4. Run interactive demo with menus
uv run python demo/interactive_demo.py

# 5. See all examples at once
bash demo/quickstart_examples.sh
```

For detailed demo documentation, see [Demo Guide](demo/README.md)

## Example Usage

### Using the CLI (Recommended)

```bash
# Interactive chat
uv run python -m ecoagent.cli chat

# Single query
uv run python -m ecoagent.cli chat --message "How can I reduce my carbon footprint?"

# Carbon calculation
uv run python -m ecoagent.cli carbon --transportation.miles_driven 500 --transportation.vehicle_mpg 25

# Recommendations
uv run python -m ecoagent.cli recommend --profile.diet vegetarian --profile.location urban

# Track goals
uv run python -m ecoagent.cli track --goal "Reduce energy by 20%" --target_value 20.0
```

### Using the API Service

```python
from ecoagent.main import get_app
import asyncio

async def main():
    app = get_app()
    await app.initialize()

    response = await app.process_query(
        user_id="user123",
        session_id="session456",
        query="How can I reduce my carbon footprint from transportation?"
    )
    print(response)

asyncio.run(main())
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache 2.0 License - see [LICENSE](LICENSE) for details.

## Support

For support, please open an issue in this repository or contact the maintainers.
