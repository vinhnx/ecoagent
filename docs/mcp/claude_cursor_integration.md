# Claude/Cursor Integration Guide for EcoAgent MCP Server

This guide provides detailed instructions for integrating the EcoAgent MCP Server with Claude Desktop and Cursor IDE.

## Overview

The EcoAgent MCP Server provides 13 sustainability-focused tools that can be used by Claude Desktop, Cursor, and other MCP-compatible clients to perform environmental impact analysis and sustainability recommendations.

## Prerequisites

- Claude Desktop or Cursor IDE installed
- EcoAgent MCP Server running locally
- Access to internet for any Gemini-powered features

## Setting Up the MCP Server

### 1. Start the EcoAgent MCP Server
```bash
# In your project directory
python -m ecoagent.mcp_server

# The server will be available at:
# Web Interface: http://localhost:8000
# MCP Endpoint: http://localhost:8000/gradio_api/mcp/sse
```

### 2. Verify Server Status
- Open http://localhost:8000 in your browser
- Check that all 13 sustainability tools are listed
- Test a few tools to confirm functionality

## Claude Desktop Integration

### 1. Configure MCP Server in Claude
1. Open Claude Desktop
2. Go to Preferences → Beta Features
3. Enable "MCP servers" if not already enabled
4. Go to Preferences → MCP Servers
5. Click "Add Server"
6. Enter the server URL: `http://localhost:8000/gradio_api/mcp/sse`
7. Claude will automatically discover and connect to all available tools

### 2. Using EcoAgent Tools in Claude
Once connected, you can use any of the 13 EcoAgent tools in Claude conversations:

**Example 1 - Transportation Carbon Calculation:**
```
What's the carbon impact of my daily commute?
<uses calculate_transportation_carbon(miles_driven=20, vehicle_mpg=28)>
```

**Example 2 - Sustainability Recommendations:**
```
How can I reduce energy usage in my home?
<uses suggest_energy_efficiency_improvements(home_type="apartment", current_energy_source="grid")>
```

**Example 3 - Local Environmental Resources:**
```
Find recycling centers in Seattle to help with my sustainability goals.
<uses get_local_environmental_resources(location="Seattle", resource_type="recycling")>
```

## Cursor IDE Integration

### 1. Configure MCP Server in Cursor
1. Open Cursor IDE
2. Go to Settings → MCP Integration
3. Add new server with URL: `http://localhost:8000/gradio_api/mcp/sse`
4. Cursor will auto-discover all EcoAgent sustainability tools

### 2. Using EcoAgent Tools in Cursor
In Cursor's chat interface, you can trigger EcoAgent tools for sustainability analysis:

**Example - Code Sustainability:**
```
Analyze the environmental impact of this data processing script.
<uses search_environmental_info(query="data center energy efficiency")>
```

## Available EcoAgent Tools

### Carbon Calculation Tools
1. `calculate_transportation_carbon` - Calculates emissions from vehicle usage
   - Parameters: `miles_driven` (required), `vehicle_mpg` (required)

2. `calculate_flight_carbon` - Calculates emissions from air travel
   - Parameters: `miles_flown` (required), `flight_class` (optional)

3. `calculate_home_energy_carbon` - Calculates emissions from home energy
   - Parameters: `kwh_used` (required), `renewable_ratio` (optional), `energy_source` (optional)

4. `calculate_total_carbon` - Aggregates carbon from multiple sources
   - Parameters: `transportation_carbon`, `flight_carbon`, `home_energy_carbon` (all optional)

### Recommendation Tools
5. `suggest_transportation_alternatives` - Suggests eco-friendly transport
   - Parameters: `distance_miles` (required)

6. `suggest_energy_efficiency_improvements` - Home energy recommendations
   - Parameters: `home_type` (required), `current_energy_source` (required)

7. `suggest_dietary_changes` - Eco-friendly diet suggestions
   - Parameters: `environmental_concern` (required)

### Information Tools
8. `search_environmental_info` - Environmental data search
   - Parameters: `query` (required)

9. `get_local_environmental_resources` - Local sustainability resources
   - Parameters: `location` (required), `resource_type` (optional)

10. `get_latest_environmental_news` - Current environmental news
    - Parameters: `topic` (optional)

11. `get_sustainability_practice_info` - Details about sustainability practices
    - Parameters: `practice` (required)

### Utility Tools
12. `convert_units_with_context` - Unit conversions for sustainability measurements
    - Parameters: `from_value` (required), `from_unit` (required), `to_unit` (required)

## Best Practices for MCP Integration

### For Claude Desktop Users:
- Be specific with transportation parameters for accurate carbon calculations
- Use location-based tools to get relevant environmental resources
- Combine multiple tools for comprehensive sustainability analysis

### For Cursor Users:
- Use environmental search tools when analyzing code's resource usage
- Apply energy efficiency recommendations to infrastructure decisions
- Leverage local resource tools for community sustainability projects

## Demo Scenarios

### Scenario 1: Personal Carbon Footprint Analysis
1. User: "Help me understand my monthly carbon footprint"
2. Claude automatically uses: `calculate_transportation_carbon`, `calculate_flight_carbon`, `calculate_home_energy_carbon`
3. Claude: "Your estimated monthly footprint is [calculated value] lbs CO2, with transportation being the largest contributor."

### Scenario 2: Home Sustainability Improvements
1. User: "What can I do to make my home more energy efficient?"
2. Cursor automatically uses: `suggest_energy_efficiency_improvements`
3. Cursor: "For a [home_type] using [energy_source], consider: [recommendations]"

### Scenario 3: Local Environmental Resources
1. User: "I want to start composting but don't know where to begin"
2. Claude automatically uses: `get_sustainability_practice_info` and `get_local_environmental_resources`
3. Claude: "Here's how composting works and local resources in [location] to help you get started."

## Troubleshooting

### Common Issues:

**Issue**: Claude/Cursor can't connect to MCP server
- **Solution**: Verify server is running at `http://localhost:8000/gradio_api/mcp/sse`
- **Solution**: Check firewall settings if running remotely

**Issue**: Tool execution fails with parameter errors
- **Solution**: Ensure required parameters are provided with correct types
- **Solution**: Check parameter values meet schema requirements (minimums, enums)

**Issue**: Tools return minimal results
- **Solution**: Ensure GOOGLE_API_KEY is set for enhanced functionality
- **Solution**: Verify internet connectivity for external API calls

## Verification Checklist

Before recording demo video:
- [ ] MCP server running at http://localhost:8000
- [ ] MCP endpoint available at http://localhost:8000/gradio_api/mcp/sse
- [ ] Claude Desktop connects and discovers all 13 tools
- [ ] Cursor IDE connects and discovers all 13 tools
- [ ] Sample tool calls execute successfully
- [ ] Results are meaningful and actionable
- [ ] Error handling works properly

## Video Demo Script

### Opening
"Welcome to the EcoAgent MCP Server demo. I'll show you how to integrate sustainability analysis into Claude Desktop and Cursor IDE."

### Integration Setup
1. Show EcoAgent MCP Server web interface
2. Demonstrate Claude Desktop MCP configuration
3. Verify tool discovery

### Live Usage Examples
1. "In Claude, I can ask: 'Calculate my commute carbon footprint' - this automatically uses calculate_transportation_carbon"
2. "For home sustainability: 'How can I improve my apartment's energy efficiency' - this uses suggest_energy_efficiency_improvements"
3. "To find local resources: 'Recycling centers in my area' - this uses get_local_environmental_resources"

### Conclusion
"The EcoAgent MCP Server brings environmental impact analysis directly into your AI workflows, making sustainability accessible and actionable in everyday conversations and development tasks."

This integration guide ensures seamless operation with MCP-compatible clients and maximizes the real-world impact of the EcoAgent sustainability tools.