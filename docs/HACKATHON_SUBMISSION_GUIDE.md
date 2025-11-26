# EcoAgent MCP Server - MCP 1st Birthday Hackathon Submission Guide

## Overview

**Project**: EcoAgent MCP Server - Sustainability Assistant for Consumer Environmental Impact Analysis  
**Track**: Track 1: Building MCP  
**Category**: Consumer MCP Servers  
**Tag**: `building-mcp-track-consumer`

EcoAgent MCP Server is a fully MCP (Model Context Protocol)-compliant server that provides powerful sustainability tools for AI agents. Built on top of the EcoAgent sustainability assistant, it allows AI agents to access carbon footprint calculations, personalized environmental recommendations, and real-time environmental data through the standardized MCP protocol.

## Prerequisites

Before submitting, ensure you have:
- A Hugging Face account
- A Hugging Face access token with write permissions
- Google API Key for Gemini features
- A social media account for sharing
- Video recording capability for demo video

## Step 1: Create Hugging Face Space

1. **Go to Hugging Face Spaces**:
   - Visit [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create New Space"

2. **Configure Space Settings**:
   - **Space ID**: `your-username/ecoagent-mcp-server` (or similar)
   - **SDK**: Gradio
   - **Hardware**: Choose based on needs (CPU sufficient for most use cases)
   - **Visibility**: Public (required for hackathon)
   - **Repository**: Create from existing repository or upload files

3. **Join MCP-1st-Birthday Organization**:
   - Join the [MCP-1st-Birthday organization](https://huggingface.co/MCP-1st-Birthday)
   - Ensure all team members join if applicable

## Step 2: Prepare Your Repository

### Repository Structure
```
ecoagent-mcp-server/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── README.md             # Space README with hackathon tags
├── .env.example          # Environment variables template
├── .gitignore            # Git ignores
├── src/                  # Source code
│   ├── mcp_server/
│   ├── chatgpt_app/
│   └── tools/
├── docs/                 # Documentation
├── resources/            # Assets
└── demo/                 # Demo materials
```

### Create main app.py for the Space
```python
from src.mcp_server.mcp_server import EcoAgentMCP

def main():
    mcp_server = EcoAgentMCP()
    return mcp_server.create_gradio_interface()

demo = main()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        mcp_server=True
    )
```

### Requirements file (requirements.txt):
```
gradio>=4.40.0
google-adk>=0.7.0
google-generativeai>=0.8.0
fastapi>=0.115.0
pydantic>=2.0.0
requests>=2.31.0
```

## Step 3: Hackathon-Compliant README.md

Create a README.md that follows the hackathon requirements:

```markdown
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
  - gradio
  - carbon-footprint
  - environmental-impact
  - building-mcp-track-consumer
---

# 🌱 EcoAgent MCP Server - Sustainability Assistant

**Submission to MCP's 1st Birthday Hackathon - Track 1: Building MCP**

## 🏷️ Hackathon Information
- **Track**: Building MCP - Consumer Category
- **Tag**: `building-mcp-track-consumer`
- **Category**: Consumer MCP Servers

## 🚀 Features

### MCP Protocol Compliance
- Full MCP protocol implementation with proper tool discovery
- 13 consumer-focused sustainability tools following JSON Schema specification
- Real-time carbon footprint calculations
- Personalized environmental recommendations
- Local environmental resource discovery

### Sustainability Tools (13 Consumer-Focused Tools)
1. `calculate_transportation_carbon` - Vehicle emissions (miles_driven, vehicle_mpg)
2. `calculate_flight_carbon` - Flight emissions (miles_flown, flight_class) 
3. `calculate_home_energy_carbon` - Home energy (kwh_used, renewable_ratio, energy_source)
4. `calculate_total_carbon` - Aggregate footprint
5. `convert_units_with_context` - Sustainability units
6. `suggest_transportation_alternatives` - Green transport options
7. `suggest_energy_efficiency_improvements` - Home energy tips
8. `suggest_dietary_changes` - Eco diet recommendations
9. `search_environmental_info` - Environmental search
10. `get_local_environmental_resources` - Local resources
11. `get_latest_environmental_news` - Environmental news
12. `get_sustainability_practice_info` - Practice details
13. `calculate_sustainability_score` - Impact assessment

### MCP Client Integration
- Compatible with Claude Desktop, Cursor, Cline, and other MCP clients
- Endpoint: `/gradio_api/mcp/sse` (when deployed to Space)
- Automatic tool discovery via MCP protocol
- Proper parameter validation and error handling

## 🎬 Demo Video

[Watch the integration video showing EcoAgent MCP Server working with Claude Desktop and providing carbon footprint calculations and sustainability recommendations](link-to-your-video)

## 📱 Social Media Post

[Link to your social media post about the project](link-to-social-media-post)

## 🚀 Setup for MCP Clients

### Claude Desktop Integration
1. Configure MCP server with endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
2. Claude will auto-discover all sustainability tools
3. Use tools for environmental impact analysis during conversations

### Cursor IDE Integration  
1. Add endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
2. Tools become available in Cursor's AI assistant
3. Use for sustainability analysis in coding workflows

## 🎯 Consumer Focus

The EcoAgent MCP Server focuses on individual consumers by providing tools for:
- Personal carbon footprint analysis (transportation, flights, home energy)
- Home sustainability recommendations (energy efficiency, eco-friendly practices)
- Lifestyle recommendations (transportation alternatives, dietary changes)
- Local environmental resource discovery
- Accessible parameter requirements for everyday users

## 💡 Technical Implementation

- **Gradio-based**: Full MCP server with Gradio interface
- **MCP Protocol**: Proper ListTools/CallTools implementation
- **JSON Schema**: All tools follow proper JSON Schema specification
- **Error Handling**: MCP-compliant error responses
- **Consumer Tools**: 13 sustainability-focused tools for individual users
- **Real-time Data**: Access to live environmental information

## 🏆 Hackathon Alignment

### Track 1: Building MCP - Consumer Category
- ✅ Functioning MCP server with 13 consumer-focused tools
- ✅ Proper MCP protocol implementation via Gradio
- ✅ Video showing Claude/Cursor integration
- ✅ Consumer sustainability tools with environmental impact focus
- ✅ Tagged as: `building-mcp-track-consumer`

## 🤝 Contributing

Contribute to EcoAgent: [GitHub Repository](https://github.com/your-repo)

## 📄 License

Apache 2.0 License

---
**EcoAgent MCP Server** - Empowering AI agents to make sustainability accessible to consumers through MCP protocol
```

## Step 4: Create Demo Video

1. **Record a 1-5 minute video showing**:
   - EcoAgent MCP Server interface
   - MCP client integration (Claude Desktop or Cursor)
   - Example tool usage (carbon calculations, recommendations)
   - Real-world environmental impact examples

2. **Upload video** to YouTube, Vimeo, or similar platform
   - Title: "EcoAgent MCP Server - Consumer Sustainability Integration"
   - Description: Include project details and hackathon information
   - Tag as appropriate for environmental/sustainability content

3. **Get video link** to include in your Space README

## Step 5: Create Social Media Post

Create a social media post announcing your project and include the link in your Space README:

**Suggested LinkedIn/Twitter/X post**:
```
🌱 Excited to announce EcoAgent MCP Server for the #MCPHackathon! 
A full MCP-compliant sustainability assistant with 13 tools for consumers to calculate carbon footprints, get eco-friendly recommendations, and access environmental data via AI assistants.
Built for Claude, Cursor and other MCP clients to help users make environmentally conscious decisions.
#MCP #Sustainability #AI #Hackathon #BuildingMCP #ConsumerMCP
[Your video link]
```

## Step 6: Upload to Hugging Face Space

1. **Option A: Git-based upload**:
   ```bash
   git clone https://huggingface.co/spaces/your-username/ecoagent-mcp-server
   cd ecoagent-mcp-server
   # Copy your files
   git add .
   git commit -m "Initial MCP hackathon submission"
   git push origin main
   ```

2. **Option B: Direct upload via HF CLI**:
   ```bash
   pip install huggingface_hub
   huggingface-cli upload your-username/ecoagent-mcp-server . --repo-type=space
   ```

3. **Option C: Upload via web interface**:
   - Go to your Space page
   - Click "Files" → "Upload Files"
   - Upload all necessary files

## Step 7: Add Secrets to Space

1. Go to your Space settings
2. Navigate to "Settings" → "Secrets"
3. Add required secrets:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `ENVIRONMENT`: production (optional)

## Step 8: Verify MCP Endpoint

After deployment, verify your MCP endpoint works:
- Space URL: `https://your-username-ecoagent-mcp-server.hf.space`
- MCP Endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
- Test with an MCP client to ensure tools are discoverable

## Step 9: Test with MCP Clients

1. **Test with Claude Desktop**:
   - Add your MCP server endpoint
   - Verify tool discovery works
   - Test various sustainability tools

2. **Test with Cursor IDE**:
   - Configure MCP server in settings
   - Verify tool availability
   - Test functionality

3. **Document any issues** and fix before submission deadline

## Step 10: Final Verification Checklist

Before November 30, 2025 deadline:

- [ ] Space is created with proper tags
- [ ] README.md includes hackathon information and tags
- [ ] MCP server is functioning at `/gradio_api/mcp/sse`
- [ ] All 13 sustainability tools are working
- [ ] Demo video is uploaded and linked
- [ ] Social media post is created and linked
- [ ] All team members joined MCP-1st-Birthday organization
- [ ] Project uses only original code created during Nov 14-30 timeframe
- [ ] Consumer category tools are properly implemented
- [ ] MCP protocol compliance verified
- [ ] Claude/Cursor integration tested

## Example Working Space

Here's an example of how your Space should function:

1. **Visit**: `https://your-username-ecoagent-mcp-server.hf.space`
2. **MCP Endpoint**: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
3. **Tools Available**: 13 sustainability-focused tools
4. **Client Integration**: MCP clients auto-discover tools
5. **Consumer Focus**: Individual carbon footprint, home energy, transportation tools

## Troubleshooting

**Common Issues**:
- MCP endpoint not working: Check `mcp_server=True` in launch configuration
- Tools not discovered: Verify JSON Schema compliance and MCP protocol
- API key errors: Ensure secrets are properly set in Space settings
- Performance issues: Consider hardware upgrade in Space settings

**Debugging**:
- Check Space logs in Hugging Face Space interface
- Verify all imports work correctly
- Test endpoints manually if needed
- Ensure all required environment variables are set

## Submission Requirements Verification

✅ **Published as Hugging Face Space**: `https://your-username-ecoagent-mcp-server.hf.space`  
✅ **Track tags in README**: `building-mcp-track-consumer`  
✅ **Social media post link**: Included in README  
✅ **Demo video**: 1-5 minutes, showing MCP integration  
✅ **Original work only**: Created during Nov 14-30 timeframe  
✅ **Consumer focus**: 13 sustainability tools for individuals  
✅ **MCP compliance**: Full protocol implementation  
✅ **Gradio app**: MCP server implemented as Gradio app  

## Prizes

By participating in Track 1 Building MCP Consumer category, you're eligible for:
- **Overall Winner**: $1,500 USD + $1,250 Claude API credits
- **Consumer Category Winner**: $750 Claude API credits
- **Integration Impact**: Real environmental awareness in AI workflows

Good luck with your submission! 🌱