# EcoAgent ChatGPT Integration - OpenAI API Enhanced Sustainability Assistant

This project integrates the EcoAgent sustainability tools with OpenAI's API to create a powerful ChatGPT app for environmental impact analysis and sustainability recommendations.

## OpenAI Application

This integration is designed for the **OpenAI **:

-   ✅ **Best ChatGPT App**: Full ChatGPT integration with sustainability tools
-   ✅ **Best API Integration**: Uses OpenAI API with function calling for enhanced capabilities

## Features

-   **OpenAI API Integration**: Uses GPT-4o with function calling capabilities
-   **Sustainability Tools**: 13 specialized tools for environmental analysis:
    -   Carbon footprint calculations (transportation, flights, home energy)
    -   Sustainability recommendations (transportation, energy, diet)
    -   Environmental information access
    -   Unit conversions for sustainability metrics
-   **ChatGPT Interface**: User-friendly Gradio interface for ChatGPT-like experience
-   **Real-time Analysis**: Instant carbon calculations and recommendations
-   **Local Resource Finder**: Locate environmental resources by location

## Architecture

The integration includes:

1. **OpenAI API Layer**: Uses OpenAI's Chat Completions API with tool/function calling
2. **EcoAgent Tools Bridge**: Maps EcoAgent functions to OpenAI-compatible format
3. **Gradio Interface**: ChatGPT-style interface for user interaction
4. **MCP Compatibility**: Maintains MCP server functionality alongside ChatGPT features

## Requirements

-   Python 3.9+
-   OpenAI API key
-   Gradio
-   EcoAgent dependencies

## Installation

```bash
# Install dependencies
pip install -e .

# Install OpenAI package if not already included
pip install openai>=0.27.0

# Set OpenAI API key
export OPENAI_API_KEY='your-openai-api-key'
```

## Usage

### Run the ChatGPT App

```bash
python -m chatgpt_app
```

The app will be available at: http://localhost:7860

### Example Conversations

```
User: "How much CO2 do I emit driving 100 miles in a car that gets 25 MPG?"
Assistant: [Uses calculate_transportation_carbon tool and responds with results]

User: "What are sustainable alternatives for a 3-mile trip?"
Assistant: [Uses suggest_transportation_alternatives tool and provides options]

User: "How can I reduce energy usage in my home?"
Assistant: [Uses suggest_energy_efficiency_improvements tool with personalized suggestions]
```

## OpenAI Tools Available

| Tool Name                              | Description                            | Parameters                                               |
| -------------------------------------- | -------------------------------------- | -------------------------------------------------------- |
| calculate_transportation_carbon        | Calculate vehicle emissions            | miles_driven, vehicle_mpg                                |
| calculate_flight_carbon                | Calculate flight emissions             | miles_flown, flight_class                                |
| calculate_home_energy_carbon           | Calculate home energy emissions        | kwh_used, renewable_ratio, energy_source                 |
| calculate_total_carbon                 | Aggregate carbon from multiple sources | transportation_carbon, flight_carbon, home_energy_carbon |
| convert_units_with_context             | Convert sustainability units           | from_value, from_unit, to_unit                           |
| suggest_transportation_alternatives    | Recommend green transport              | distance_miles                                           |
| suggest_energy_efficiency_improvements | Home energy tips                       | home_type, current_energy_source                         |
| suggest_dietary_changes                | Eco diet recommendations               | environmental_concern                                    |
| search_environmental_info              | Environmental search                   | query                                                    |
| get_local_environmental_resources      | Local sustainability resources         | location, resource_type                                  |
| get_latest_environmental_news          | Environmental news                     | topic                                                    |
| get_sustainability_practice_info       | Practice details                       | practice                                                 |

## API Integration Details

The integration uses OpenAI's function calling feature with GPT-4o to connect ChatGPT with EcoAgent's sustainability tools. Each EcoAgent function is formatted according to OpenAI's function specification and passed to the API call.

```python
# Example of tool formatting for OpenAI API
openai_tool = {
    "type": "function",
    "function": {
        "name": "calculate_transportation_carbon",
        "description": "Calculate carbon emissions from vehicle usage...",
        "parameters": {
            "type": "object",
            "properties": {
                "miles_driven": {"type": "number", "description": "Number of miles driven"},
                "vehicle_mpg": {"type": "number", "description": "Vehicle fuel efficiency in MPG"}
            },
            "required": ["miles_driven", "vehicle_mpg"]
        }
    }
}
```

## Error Handling

-   API authentication failures
-   Rate limit errors
-   Tool execution errors
-   Graceful degradation when tools fail

## MCP Server Compatibility

This ChatGPT integration maintains compatibility with the original MCP server functionality:

-   Run ChatGPT app: `python -m chatgpt_app`
-   Run MCP server: `python -m ecoagent.mcp_server`
-   Both use the same underlying EcoAgent tools

## OpenAI Alignment

This integration addresses the OpenAI requirements:

### Best ChatGPT App

-   ✅ ChatGPT-style interface with conversation flow
-   ✅ Function calling for sustainability tools
-   ✅ Real-time, interactive sustainability assistance
-   ✅ Professional Gradio interface

### Best API Integration

-   ✅ OpenAI API integration with GPT-4o
-   ✅ Function calling for specialized tools
-   ✅ Proper API error handling and rate limiting
-   ✅ Asynchronous API calls for better performance

## Configuration

Create a `.env` file for your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key  # for EcoAgent features
```

## Development

```bash
# Test the ChatGPT integration
python -m chatgpt_integration

# Run the interface
python -m chatgpt_app

# Run MCP server (maintains compatibility)
python -m ecoagent.mcp_server
```

## License

This project is licensed under the Apache 2.0 License.

## Acknowledgments

-   OpenAI for the API integration
-   EcoAgent for sustainability tools
-   Gradio for the web interface
