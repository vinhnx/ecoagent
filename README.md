# EcoAgent: Multi-Platform Sustainability Assistant

---
title: EcoAgent MCP Server - Consumer Sustainability
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: apache-2.0
---

# 🌱 EcoAgent MCP Server - Consumer Sustainability Tools

**MCP 1st Birthday Hackathon Submission - Building MCP Track**

## Category: Building MCP - Consumer

**Tag**: `building-mcp-track-consumer`

## Demo Video
[Embed link to your demo video showing Claude/Cursor integration]

## Social Media Post  
[Link to your social media post about the project]

## 🚀 MCP Endpoint
```
https://vinhnx90-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse
```

## Consumer-Focused Sustainability Tools (13 Tools)

### Carbon Calculation Tools
1. `transportation_carbon` - Vehicle emissions calculator
2. `flight_carbon` - Flight emissions with class adjustment  
3. `home_energy_carbon` - Home energy impact analysis
4. `total_carbon` - Aggregate footprint from multiple sources

### Recommendation Tools  
5. `suggest_transportation_alternatives` - Green transport options
6. `suggest_energy_efficiency_improvements` - Home energy tips
7. `suggest_dietary_changes` - Eco diet recommendations

### Information Tools
8. `search_environmental_info` - Environmental search
9. `get_local_environmental_resources` - Local green resources
10. `get_latest_environmental_news` - Environmental news
11. `get_sustainability_practice_info` - Practice details

### Utility Tools
12. `convert_units_with_context` - Sustainability unit conversions
13. `calculate_sustainability_score` - Impact assessment

## Consumer Focus Features

- **Personal Carbon Tracking**: Individual transport, energy, lifestyle impact
- **Home Sustainability**: Energy efficiency and home-related recommendations
- **Lifestyle Advice**: Transport, diet, consumption guidance
- **Local Resources**: Find environmental resources by location
- **Simple Parameters**: Easy-to-use for everyday consumers

## MCP Client Integration

### Claude Desktop Setup
1. Go to Settings → MCP Servers
2. Add endpoint: `https://vinhnx90-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
3. Claude will auto-discover all sustainability tools
4. Tools become available during conversations

### Cursor IDE Setup
1. Go to Preferences → MCP Configuration
2. Add server with endpoint
3. Tools appear in Cursor's AI assistant
4. Available for code-related environmental analysis

## Use Cases

### Personal Carbon Footprint
Calculate and reduce individual transportation, energy, and lifestyle emissions

### Sustainable Living  
Get personalized recommendations for transportation, diet, and energy usage

### Local Environmental Action
Discover environmental resources and practices in your area

---

**EcoAgent MCP Server** - Making sustainability accessible to consumers through MCP protocol
# EcoAgent: AI-Powered Sustainability Assistant

[![EcoAgent Logo](resources/ecoagent.png)](resources/ecoagent.png)

EcoAgent is a comprehensive sustainability assistant that provides powerful environmental tools through multiple platforms: Model Context Protocol (MCP) server and OpenAI ChatGPT integration. Built on top of the EcoAgent sustainability assistant, it allows AI agents to access carbon footprint calculations, personalized environmental recommendations, and real-time environmental data.

## MCP Track: Building MCP (Consumer Category)

**Category**: Building MCP - Consumer Track
**Tag**: `building-mcp-track-consumer`

Full MCP-compliant server with 13 sustainability-focused tools for consumer use.

### MCP Features

-   **Full MCP Protocol Compliance**: Implements all MCP protocol requirements with proper tool discovery and execution
-   **Standardized Tool Schemas**: Each tool follows JSON Schema specification for proper parameter validation
-   **Carbon Footprint Tools**: Transportation, flight, home energy, and aggregate calculations
-   **Sustainability Recommendations**: Personalized advice for transportation, energy, and diet
-   **Environmental Information Access**: Real-time search and local resource discovery
-   **MCP Client Integration**: Works with Claude Desktop, Cursor, and other MCP-compatible tools

## OpenAI - ChatGPT App & API Integration

**Category**: OpenAI Integration Track
**Target**: Best ChatGPT App & Best API Integration

### OpenAI Best Practices Implementation

-   **Well-Scoped Capabilities**: Focused on specific sustainability jobs-to-be-done
-   **NEW THINGS TO KNOW**: Real-time carbon calculations, environmental data access
-   **NEW THINGS TO DO**: Sustainability recommendations, unit conversions
-   **BETTER WAYS TO SHOW**: Structured environmental impact data and metrics
-   **Immediate Value**: Quick, relevant responses on first interaction
-   **Privacy by Design**: Minimal required parameters, no unnecessary context
-   **Ecosystem Ready**: Outputs designed for chaining with other tools

## Multi-Platform Features

### MCP Protocol Implementation

-   `transportation_carbon` - Calculate vehicle emissions
-   `flight_carbon` - Calculate flight emissions
-   `home_energy_carbon` - Calculate home energy emissions
-   `total_carbon` - Aggregate carbon from multiple sources
-   `suggest_transportation_alternatives` - Recommend green transport
-   `suggest_energy_efficiency_improvements` - Home energy tips
-   `suggest_dietary_changes` - Eco diet recommendations
-   `search_environmental_info` - Environmental search
-   `get_local_environmental_resources` - Local sustainability resources
-   `get_latest_environmental_news` - Environmental news
-   `get_sustainability_practice_info` - Practice details
-   `convert_units_with_context` - Unit conversions

### OpenAI ChatGPT Integration

-   Function calling for all 13 sustainability tools
-   Conversational interface for environmental questions
-   Context-aware recommendations
-   Real-time carbon footprint calculations
-   Professional Gradio interface

## Architecture

The EcoAgent platform implements both MCP protocol and OpenAI API integration:

-   **MCP Server**: Full MCP compliance with standardized tool discovery and execution
-   **OpenAI Integration**: GPT-4o with function calling for sustainability tools
-   **Multi-Agent System**: Hierarchical agents for different sustainability aspects
-   **Dual Interface**: MCP server and ChatGPT app from same codebase
-   **Unified Tools**: Same 13 sustainability tools available via both interfaces

## Requirements

-   Python 3.9+
-   OpenAI API Key (for ChatGPT integration)
-   Google API Key (for extended Gemini features)
-   Gradio with MCP support
-   [uv](https://github.com/astral-sh/uv) (recommended package manager)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/vinhnx/ecoagent.git
cd ecoagent

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Configure API keys
export OPENAI_API_KEY='your-openai-api-key'      # Required for ChatGPT
export GOOGLE_API_KEY='your-gemini-api-key'      # Optional for advanced features
```

### Running the MCP Server

```bash
# Run the MCP server
uv run python -m ecoagent.mcp_server
```

The MCP server will be available at:

-   Web Interface: http://localhost:8000
-   MCP Endpoint: http://localhost:8000/gradio_api/mcp/sse

### Running the ChatGPT App

```bash
# Run the ChatGPT app
uv run python -m chatgpt_app
```

The ChatGPT app will be available at:

-   Web Interface: http://localhost:7860

## Configuration

Create a `.env` file in the root directory:

```env
# Required: Your OpenAI API key for ChatGPT integration
OPENAI_API_KEY=your_openai_api_key

# Optional: Your Google API key for extended features
GOOGLE_API_KEY=your_api_key_here

# Optional: Other settings
ECOAGENT_ENVIRONMENT=development
LOG_LEVEL=INFO

# Optional: Gemini Google Search grounding (enabled by default)
ECOAGENT_ENABLE_GOOGLE_SEARCH=true
```

## Platform Integration

### MCP Client Integration

Configure MCP clients with the endpoint: `http://localhost:8000/gradio_api/mcp/sse`

### OpenAI ChatGPT Integration

The ChatGPT app provides a conversational interface with 13 sustainability tools accessible through function calling.

## Example Use Cases

### For MCP-Compatible AI Agents (Claude Desktop, Cursor, etc.)

-   Calculate user carbon footprints during conversations using MCP protocol
-   Provide personalized sustainability recommendations via standardized tools
-   Access real-time environmental data through MCP tool calls

### For ChatGPT Integration

-   Natural language queries about sustainability
-   Conversational carbon footprint analysis
-   Context-aware environmental recommendations
-   Real-time tool usage through function calling

### For Developers

-   Integrate sustainability features via MCP protocol
-   Use ChatGPT-style interface for direct user interaction
-   Build sustainability workflows using either approach

## OpenAI Alignment

### Best ChatGPT App

-   [x] ChatGPT-style conversation interface
-   [x] Professional Gradio user interface
-   [x] Real-time sustainability assistance
-   [x] 13 specialized environmental tools
-   [x] Context-aware recommendations

### Best API Integration

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

We welcome contributions to enhance the EcoAgent platform! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see [LICENSE](LICENSE) for details.

## Acknowledgments

-   Built with Google's Agent Development Kit (ADK)
-   Powered by OpenAI API for ChatGPT integration
-   Gradio MCP support for seamless protocol integration
-   MCP Protocol specification compliance
-   Inspired by the need for sustainable AI practices

[Demo Screenshot](resources/demo.png)

---

**Made with love for the environment**

_EcoAgent - Empowering AI agents and users to make sustainability accessible through MCP and ChatGPT integration_
