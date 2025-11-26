# EcoAgent MCP Server - Organized Project Structure

## Overview

This document describes the organized project structure for the EcoAgent MCP Server, designed for the MCP hackathon submission. The project has been reorganized to follow best practices for modularity, maintainability, and MCP protocol compliance.

## Project Architecture

```
ecoagent/
├── src/                          # Source code modules
│   ├── core/                     # Core EcoAgent functionality
│   │   ├── __init__.py          # Package initialization
│   │   ├── main.py              # Main application entry point
│   │   ├── api.py               # API layer
│   │   └── cli.py               # Command line interface
│   ├── mcp_server/              # MCP protocol implementation
│   │   ├── __init__.py          # Package initialization
│   │   └── mcp_server.py        # Main MCP server implementation
│   ├── chatgpt_app/             # ChatGPT integration
│   │   ├── __init__.py          # Package initialization
│   │   ├── chatgpt_app.py       # ChatGPT interface
│   │   └── chatgpt_integration.py # OpenAI API integration
│   ├── tools/                   # Shared tools and utilities
│   │   ├── __init__.py          # Package initialization
│   │   ├── carbon_calculator.py # Carbon footprint calculation tools
│   │   ├── agent.py             # Recommendation agents
│   │   ├── search_grounding.py  # Environmental search tools
│   │   └── unit_converter.py    # Unit conversion tools
│   └── utils/                   # Utility functions
├── docs/                        # Documentation
│   ├── mcp/                     # MCP protocol documentation
│   ├── hackathon/               # Hackathon-specific docs
│   ├── api/                     # API documentation
│   └── tutorials/               # Tutorial materials
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── mcp/                     # MCP protocol tests
│   └── chatgpt/                 # ChatGPT integration tests
├── examples/                    # Usage examples
│   ├── mcp/                     # MCP client examples
│   ├── chatgpt/                 # ChatGPT examples
│   └── quickstart/              # Quick start examples
├── resources/                   # Assets and resources
│   ├── logos/                   # Logo files
│   ├── icons/                   # Icon files
│   └── demos/                   # Demo materials
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Package configuration
└── .env.example                 # Environment variable template
```

## Key Components

### 1. SCP Server Module (`src/mcp_server/`)
- **Full MCP Protocol Compliance**: Implements all MCP requirements
- **13 Sustainability Tools**: Consumer-focused environmental tools
- **Gradio Interface**: For testing and demonstration
- **JSON Schema Validation**: All tools validate inputs properly

### 2. ChatGPT Integration (`src/chatgpt_app/`)
- **OpenAI API Integration**: GPT-4o with function calling
- **Consumer Sustainability Tools**: Available via ChatGPT interface
- **Professional UI**: Gradio-based ChatGPT-style interface

### 3. Core Tools (`src/tools/`)
- **Carbon Calculators**: Transportation, flight, home energy, total
- **Recommendation Engines**: Transportation, energy, dietary suggestions
- **Search Tools**: Environmental information access
- **Utility Functions**: Unit conversions, local resources

### 4. Documentation Structure
- **MCP Protocol**: Complete MCP implementation documentation
- **Hackathon Materials**: Submission documentation and guidelines
- **API References**: Tool-specific documentation
- **Tutorials**: Step-by-step guides for users

## MCP Protocol Implementation

### Tool Discovery
```python
# MCP-compliant tool listing
{
  "tools": [
    {
      "name": "calculate_transportation_carbon",
      "description": "Calculate carbon emissions from vehicle usage...",
      "inputSchema": {
        "type": "object",
        "properties": {
          "miles_driven": {"type": "number", "minimum": 0},
          "vehicle_mpg": {"type": "number", "minimum": 0.1}
        },
        "required": ["miles_driven", "vehicle_mpg"]
      }
    }
  ]
}
```

### Tool Execution
- MCP clients automatically discover available tools
- JSON Schema validation ensures proper inputs
- Structured responses follow MCP specification
- Proper error handling for invalid inputs

## Consumer Focus

### Sustainability Tools (13 Tools)
1. **transportation_carbon** - Vehicle emissions calculation
2. **flight_carbon** - Flight emissions calculation
3. **home_energy_carbon** - Home energy emissions calculation
4. **total_carbon** - Aggregate carbon footprint
5. **unit_converter** - Sustainability unit conversions
6. **suggest_transportation_alternatives** - Green transport options
7. **suggest_energy_efficiency_improvements** - Home energy tips
8. **suggest_dietary_changes** - Eco diet recommendations
9. **search_environmental_info** - Environmental search
10. **get_local_environmental_resources** - Local sustainability resources
11. **get_latest_environmental_news** - Environmental news
12. **get_sustainability_practice_info** - Sustainability practice details
13. **calculate_sustainability_score** - Overall impact assessment

### MCP Client Integration
**Endpoint**: `http://localhost:8000/gradio_api/mcp/sse`

Compatible with:
- Claude Desktop
- Cursor IDE
- Cline
- Other MCP-compatible clients

## OpenAI Integration

### Best ChatGPT App Requirements
- [x] Well-scoped capabilities for sustainability
- [x] NEW THINGS TO KNOW: Real-time carbon calculations
- [x] NEW THINGS TO DO: Sustainability recommendations
- [x] Better ways to show: Structured environmental impact data
- [x] Immediate value delivery
- [x] Privacy by design
- [x] Ecosystem ready

### Best API Integration Requirements
- [x] Professional OpenAI API usage
- [x] Proper function calling implementation
- [x] Error handling and validation
- [x] Asynchronous API calls
- [x] Ecosystem compatibility

## Project Benefits

### Modularity
- Clean separation of concerns
- Independent modules for different functionality
- Easy maintenance and updates

### Scalability
- Horizontal scaling through independent modules
- Easy addition of new tools
- Flexible deployment options

### MCP Compliance
- Full protocol implementation
- Proper tool schemas
- Standard error handling

### Consumer Focus
- Tools designed for individual users
- Simple parameters for accessibility
- Real-world environmental impact

## Deployment

### Local Development
```bash
# Install dependencies
pip install -e .

# Set API keys
export GOOGLE_API_KEY='your-google-api-key'
export OPENAI_API_KEY='your-openai-api-key'  # Optional for ChatGPT

# Run MCP server
python -m ecoagent.mcp_server
```

### Hugging Face Spaces
1. Create Space with Gradio SDK
2. Add `GOOGLE_API_KEY` secret
3. Server auto-deploys with MCP support

### MCP Client Configuration
- Endpoint: `https://your-space.hf.space/gradio_api/mcp/sse`
- Tools auto-discovered by MCP clients
- JSON Schema validation automatically applied

## Quality Assurance

### Testing Strategy
- Unit tests for individual tools
- Integration tests for MCP protocol
- End-to-end tests for full functionality
- Consumer usability testing

### Documentation
- Complete API documentation
- MCP protocol compliance guide
- Consumer usage examples
- Developer integration guides

## Hackathon Submission

### Building MCP Track - Consumer Category
- [x] **Functioning MCP server**: Complete MCP implementation
- [x] **Can be Gradio app**: Gradio interface with MCP support
- [x] **Video integration**: Demo video script provided
- [x] **Consumer focus**: 13 tools for individual users
- [x] **Documentation**: Comprehensive documentation
- [x] **Tag**: `building-mcp-track-consumer`

### OpenAI Category Awards
- [x] **Best ChatGPT App**: Consumer sustainability tools
- [x] **Best API Integration**: Professional OpenAI integration
- [x] **OpenAI Best Practices**: All guidelines followed

This organized structure provides a maintainable, scalable, and MCP-compliant server that delivers powerful sustainability tools to AI agents and consumers while meeting all hackathon requirements.