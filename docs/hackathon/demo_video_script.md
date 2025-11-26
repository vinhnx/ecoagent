# EcoAgent MCP Server Demo Video Script

## Introduction (0:00-0:15)
"Welcome to the EcoAgent MCP Server demo. I'm showing you how to integrate our sustainability-focused MCP server with AI agents using the Model Context Protocol."

## Overview (0:15-0:45)
"In this demo, I'll show you:
- The EcoAgent MCP Server interface
- How to connect MCP clients to our sustainability tools
- Live examples of sustainability calculations
- Integration with popular MCP-compatible applications"

## Server Setup (0:45-1:30)
1. "First, let's start the EcoAgent MCP server by running: `python -m ecoagent.mcp_server`"
2. "The server starts at http://localhost:7860"
3. "The MCP endpoint is available at: http://localhost:7860/gradio_api/mcp/sse"
4. "The server provides a user-friendly interface for testing tools"

## Available Tools Overview (1:30-2:30)
"Let's look at the sustainability tools available:
- Transportation Carbon Calculator: Calculates emissions based on miles driven and vehicle efficiency
- Flight Carbon Calculator: Calculates emissions from air travel with class consideration
- Home Energy Carbon Calculator: Calculates emissions from home energy usage
- Sustainability Recommendations: Provides personalized eco-friendly suggestions
- Environmental Search: Accesses real-time environmental information
- Local Resource Finder: Locates sustainability resources by location"

## Integration Example with Claude Desktop (2:30-3:45)
1. "Open Claude Desktop and go to Settings"
2. "Navigate to Model Context Protocol (MCP) settings"
3. "Add new server with endpoint: http://localhost:7860/gradio_api/mcp/sse"
4. "The server will auto-discover all available sustainability tools"
5. "Now Claude can access these tools during conversations"
6. "Example: 'Calculate the carbon footprint of driving 100 miles in a 25 MPG car'"
7. "Claude will call the transportation_carbon tool with the parameters"
8. "The result shows the carbon emissions in pounds of CO2"

## Integration Example with Cursor IDE (3:45-4:30)
1. "In Cursor IDE, open the MCP integration panel"
2. "Add the same endpoint: http://localhost:7860/gradio_api/mcp/sse"
3. "The tools appear in Cursor's tool palette"
4. "When writing code that needs sustainability analysis, the tools are available"
5. "Example: Cursor can suggest sustainable practices when writing code that uses resources"

## Live Tool Usage (4:30-5:30)
1. "Let's use the web interface to test a calculation"
2. "Select 'transportation_carbon' tool" 
3. "Enter 150 miles and 30 MPG"
4. "Click execute - result shows 98.0 lbs CO2 emissions"
5. "Now let's try 'suggest_transportation_alternatives' with distance 5 miles"
6. "Result provides walking/biking options for short distances"

## Real-World Use Case (5:30-6:15)
"Example workflow: A user asks Claude for help reducing their environmental impact.
1. Claude uses 'transportation_carbon' to calculate current emissions
2. Claude uses 'suggest_transportation_alternatives' for improvement ideas
3. Claude uses 'get_local_environmental_resources' to find local options
4. Claude provides a comprehensive sustainability plan"

## Performance and Analytics (6:15-6:45)
"The MCP server provides performance analytics:
- Tool usage statistics
- Success rates and response times
- Error tracking and monitoring
- These help optimize the sustainability tools"

## Conclusion (6:45-7:00)
"The EcoAgent MCP Server enables any MCP-compatible AI agent to access powerful sustainability tools. This makes environmental consciousness accessible to any AI workflow. Thanks for watching!"

## Technical Notes
- Server uses Google Gemini for advanced reasoning
- All tools include proper error handling
- Unit conversion support for international use
- Real-time environmental data access
- Integration with Google Search for current information