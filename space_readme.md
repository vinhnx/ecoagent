---
title: EcoAgent MCP Server - Sustainability Assistant
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - mcp
  - sustainability
  - carbon-footprint
  - environmental-impact
  - building-mcp-track-consumer
  - ecoagent
  - gradio
  - ai-agent-tools
  - consumer-mcp
  - environmental-analysis
---

# 🌱 EcoAgent MCP Server - Sustainability Assistant

**Track 1: Building MCP - Consumer Category Submission**

EcoAgent MCP Server provides powerful sustainability tools for AI agents through the Model Context Protocol (MCP). Enables AI agents like Claude and Cursor to calculate carbon footprints, get environmental recommendations, and access real-time environmental data.

## 🏷️ Hackathon Category: Building MCP - Consumer

This server focuses on consumer sustainability tools that help individual users make environmentally conscious decisions through AI assistants.

### Available Sustainability Tools (13 Tools)

1. **Transportation Carbon**: Calculate vehicle emissions from miles driven and MPG
2. **Flight Carbon**: Calculate flight emissions with class-based multipliers  
3. **Home Energy Carbon**: Calculate home energy emissions with renewable ratios
4. **Total Carbon**: Aggregate carbon from multiple sources
5. **Unit Converter**: Convert sustainability-related units with context
6. **Transportation Alternatives**: Suggest green transportation options
7. **Energy Efficiency Improvements**: Home energy saving recommendations
8. **Dietary Changes**: Eco-friendly diet suggestions
9. **Environmental Search**: Search environmental information
10. **Local Resources**: Find environmental resources by location
11. **Environmental News**: Get latest environmental news
12. **Practice Information**: Detailed sustainability practice info
13. **Carbon Score**: Overall environmental impact assessment

## 🚀 MCP Client Integration

### Endpoint
```
https://[your-username]-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse
```

### Compatible with:
- Claude Desktop (configure in Settings → MCP Servers)
- Cursor IDE (MCP settings in preferences)
- Cline and other MCP-compatible tools
- Any MCP-enabled AI agent

## 💡 How It Works

1. **Tool Discovery**: MCP clients automatically discover all sustainability tools
2. **Parameter Validation**: All tools validate inputs against JSON Schemas  
3. **Execution**: Tools execute calculations and return structured results
4. **Environmental Analysis**: AI agents use tools to provide carbon footprint analysis

### Example Integration:
```
User: "How much CO2 do I emit driving 100 miles in a 25 MPG car?"
Claude: [calls calculate_transportation_carbon(miles_driven=100, vehicle_mpg=25)]
Response: "Your trip emits 78.4 lbs CO2. Consider biking or EV for zero emissions."
```

## 🎯 Consumer Focus

- **Individual Carbon Tracking**: Personal transportation, energy, and lifestyle impact
- **Home Sustainability**: Energy efficiency and home-related recommendations  
- **Lifestyle Recommendations**: Transportation, diet, and consumption advice
- **Local Resources**: Find environmental resources in user's area
- **Accessible Tools**: Simple parameters for everyday users

## 🌍 Environmental Impact

- Makes carbon footprint analysis accessible through familiar AI interfaces
- Enables real-time environmental decision-making
- Provides personalized recommendations for individual impact reduction
- Democratizes access to environmental impact calculations

## 🔧 Technical Features

- Full MCP protocol compliance with proper tool schemas
- JSON Schema validation for all inputs and parameters
- MCP-compliant error handling and responses
- Consumer-focused tool design and parameter requirements
- Real-time environmental data access through Google Search integration

## 📊 Use Cases

- **Daily Commute Analysis**: Calculate and reduce transportation emissions
- **Travel Planning**: Compare environmental impact of different travel options
- **Home Energy**: Optimize home energy usage and efficiency
- **Dietary Choices**: Make environmentally conscious food decisions
- **Local Action**: Find nearby sustainability resources and practices

## 🏆 MCP Hackathon Alignment

### Track 1: Building MCP - Consumer Category
- ✅ Full MCP server implementation with 13 sustainability tools
- ✅ Consumer-focused tools for individual users
- ✅ Proper MCP protocol compliance and JSON schemas
- ✅ Gradio app with MCP server support
- ✅ Environmental impact and sustainability focus
- ✅ Tagged as: `building-mcp-track-consumer`

## 🚀 Quick Start for MCP Clients

1. Add endpoint: `https://[your-username]-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
2. Discover tools automatically via MCP protocol
3. Use tools for environmental impact analysis
4. Get real-time sustainability recommendations

## 📄 License

Apache 2.0 License - see LICENSE file for details

**EcoAgent MCP Server - Empowering AI agents to make sustainability accessible to consumers through standardized MCP protocol**