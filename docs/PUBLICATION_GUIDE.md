# EcoAgent MCP Server - Publication Guide

This guide will walk you through the complete publication process for the MCP 1st Birthday hackathon.

## Prerequisites

Before publishing, ensure you have:

1. **Hugging Face Account** - Create at: https://huggingface.co/join
2. **Google API Key** - For Gemini integration: https://aistudio.google.com/
3. **GitHub Account** - For repository management
4. **Social Media Account** - For required social media post
5. **Video Recording Capability** - For the required demo video

## Step 1: Join the MCP Hackathon Organization

1. **Join the MCP 1st Birthday organization**: 
   - Go to: https://huggingface.co/MCP-1st-Birthday
   - Request to join the organization
   - Wait for admin approval

2. **Register for the hackathon**:
   - Use the registration link provided in the hackathon announcement
   - Fill out your details and track selection

## Step 2: Prepare Your Repository

### Create the main app.py file:
```python
from ecoagent.mcp_server import EcoAgentMCP

def main():
    """Main entry point for EcoAgent MCP Server."""
    mcp_server = EcoAgentMCP()
    return mcp_server.create_gradio_interface()

# Create the Gradio interface
demo = main()

# The Space will automatically use this as the main entry point
if __name__ == "__main__":
    demo.launch()
```

### Create requirements.txt:
```
gradio>=4.40.0
google-adk>=0.7.0
google-generativeai>=0.8.0
fastapi>=0.115.0
pydantic>=2.0.0
requests>=2.31.0
pydantic[email]>=2.0.0
click>=8.0.0
python-multipart>=0.0.18
SQLAlchemy>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0
uv>=0.1.0
```

### Create the Space README with proper tags:
```markdown
---
title: EcoAgent MCP - Consumer Sustainability Server
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
  - consumer-mcp
  - eco-friendly
  - environmental-analysis
---

# 🌱 EcoAgent MCP Server - Consumer Sustainability Assistant

**MCP 1st Birthday Hackathon Submission - Track 1: Building MCP (Consumer Category)**

## 🏷️ Hackathon Information
- **Track**: Building MCP - Consumer Category  
- **Tag**: `building-mcp-track-consumer`
- **Category Focus**: Consumer sustainability tools for individual users

## 🚀 Features

### MCP Protocol Compliance
- Full MCP (Model Context Protocol) implementation with proper tool discovery
- 13 consumer-focused sustainability tools following JSON Schema specification
- Real-time carbon footprint calculations
- Personalized environmental recommendations
- Local environmental resource discovery

### Available Consumer Sustainability Tools (13 Total)
1. **transportation_carbon** - Calculate vehicle emissions based on miles and MPG
2. **flight_carbon** - Calculate flight emissions with class considerations  
3. **home_energy_carbon** - Calculate home energy emissions with source type
4. **total_carbon** - Aggregate carbon footprints from multiple sources
5. **unit_converter** - Convert sustainability units with context
6. **suggest_transportation_alternatives** - Recommend green transport options
7. **suggest_energy_efficiency_improvements** - Home energy efficiency tips
8. **suggest_dietary_changes** - Eco-friendly diet recommendations
9. **search_environmental_info** - Environmental information search
10. **get_local_environmental_resources** - Find local green resources
11. **get_latest_environmental_news** - Access environmental news
12. **get_sustainability_practice_info** - Detailed practice information
13. **calculate_sustainability_score** - Overall environmental impact assessment

## 🎬 Demo Video

[Watch our demo video showing Claude Desktop integration and sustainability tools in action](LINK_TO_YOUR_VIDEO)

## 📱 Social Media Post

[Link to your social media post about the project](LINK_TO_SOCIAL_MEDIA_POST)

## 🚀 MCP Client Integration

### Endpoint
```
https://your-username-ecoagent-mcp.hf.space/gradio_api/mcp/sse
```

### Compatible MCP Clients:
- Claude Desktop (configure in Settings → MCP Servers)
- Cursor IDE (MCP settings in preferences) 
- Cline and other MCP-compatible tools
- Any MCP-enabled AI agent

## 🎯 Consumer Focus

This MCP server specializes in tools for individual consumers:
- **Personal carbon tracking**: Transportation, energy, and lifestyle footprint analysis
- **Home sustainability**: Energy efficiency and home-related recommendations  
- **Lifestyle recommendations**: Transportation, diet, and consumption advice
- **Local resources**: Find environmental resources in user's area
- **Accessible tools**: Simple parameters designed for everyday users

## 💡 How It Works

MCP clients will automatically discover all sustainability tools and can use them to:
- Calculate personal carbon footprints during conversations
- Provide personalized environmental recommendations
- Access real-time environmental data and resources
- Help users make environmentally conscious decisions

## 🏆 Hackathon Compliance

### Track 1: Building MCP - Consumer Category
- ✅ Functioning MCP server with 13 sustainability tools
- ✅ Gradio app with MCP capabilities
- ✅ Consumer-focused tools for individual users
- ✅ Proper MCP protocol implementation
- ✅ Environmental impact and sustainability focus
- ✅ Tagged as: `building-mcp-track-consumer`

## 🤝 Contributing

[Your GitHub Repository Link]

## 📄 License

Apache 2.0 License

---
**EcoAgent MCP Server** - Empowering AI agents to make sustainability accessible to consumers through MCP protocol
```

## Step 3: Create Required Demo Video

### Video Requirements:
- Duration: 1-5 minutes
- Must show MCP client integration
- Show actual tool usage in Claude Desktop, Cursor, or similar

### Video Content Suggestions:
1. **Introduction** (10-15 seconds): Brief project introduction
2. **MCP Client Setup** (30-60 seconds): Show configuring Claude Desktop/Cursor with your endpoint
3. **Tool Demonstration** (60-120 seconds): Demonstrate 2-3 key tools in action:
   - Transportation carbon calculation
   - Sustainability recommendations
   - Environmental search
4. **Real-world Example** (30-60 seconds): Show practical use case
5. **Conclusion** (10-15 seconds): Highlight consumer environmental impact

### Sample Video Script:
```
"Welcome to EcoAgent MCP Server. I'm demonstrating how Claude Desktop can access sustainability tools through the MCP protocol.

First, I'll add the EcoAgent MCP server endpoint to Claude's settings. 

Now Claude automatically discovers the 13 sustainability tools including transportation carbon calculation, flight emissions, and personalized recommendations.

Let me ask Claude to calculate my weekly commuting carbon footprint. Claude calls the transportation carbon tool and provides me with the exact emissions and suggestions for improvement.

This shows how AI agents can help consumers make environmentally conscious decisions through standardized tool access. EcoAgent MCP Server makes sustainability accessible to everyone."
```

## Step 4: Create Social Media Post

### Required Social Media Content:
Post on Twitter/X, LinkedIn, or similar platform with:
- Project announcement
- Link to your Hugging Face Space
- Mention of MCP hackathon
- Link to demo video

### Sample Tweet/X Post:
```
🌱 Just built EcoAgent MCP Server for the #MCPHackathon! 
A full MCP-compliant sustainability assistant with 13 tools for consumers to calculate carbon footprints, get eco-friendly recommendations, and access environmental data via AI assistants.
Enables Claude, Cursor and other MCP clients to help users make environmentally conscious decisions.
#MCP #Sustainability #AI #Hackathon #BuildingMCP #ConsumerMCP
[Link to your Space]
[Link to demo video]
```

### Sample LinkedIn Post:
```
🌟 Excited to share my submission to the MCP 1st Birthday Hackathon - EcoAgent MCP Server!

Built a fully MCP-compliant sustainability assistant that provides 13 environmental impact tools for AI agents. The server enables Claude Desktop, Cursor, and other MCP clients to help individual users calculate carbon footprints, get personalized sustainability recommendations, and access real-time environmental data.

Key features:
✅ 13 consumer-focused sustainability tools
✅ Full MCP protocol compliance
✅ Carbon footprint calculations (transportation, flights, home energy)
✅ Personalized eco-friendly recommendations
✅ Local environmental resource discovery

Perfect for the Building MCP - Consumer category, helping individual users make environmentally conscious decisions through familiar AI interfaces.

#MCP #Sustainability #AI #MCPHackathon #BuildingMCP #EnvironmentalTech
```

## Step 5: Deploy to Hugging Face Space

### Method 1: Direct Space Creation
1. Go to: https://huggingface.co/new-space
2. Fill in details:
   - **Space ID**: `your-username/ecoagent-mcp-server`
   - **SDK**: Gradio
   - **Hardware**: Choose based on needs (CPU sufficient for most use cases)
   - **Visibility**: Public
3. Click "Create Space"

### Method 2: Git-based Deployment
```bash
# Clone the repository
git clone https://huggingface.co/spaces/your-username/ecoagent-mcp-server

# Copy your files
cp app.py requirements.txt README.md ecoagent/ [your-space-folder]/

# Commit and push
cd [your-space-folder]
git add .
git commit -m "EcoAgent MCP Server - MCP Hackathon Submission"
git push origin main
```

### Add Secrets to Your Space
1. Go to your Space → Settings → Secrets
2. Add secret: `GOOGLE_API_KEY` with your Google API key value
3. Save the secret

## Step 6: Test Your Deployment

### Verify MCP Endpoint
1. Visit your Space: `https://your-username-ecoagent-mcp-server.hf.space`
2. Test endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
3. Verify all 13 tools are properly discovered by MCP clients

### Test with MCP Clients
1. **Claude Desktop**: Add your endpoint in Settings → MCP Servers
2. **Cursor IDE**: Add to MCP configuration
3. **Other MCP clients**: Verify tool discovery and execution

## Step 7: Update README with Final Links

After deployment, update your README.md with:
- Actual Space URL
- Actual video link  
- Actual social media post link
- Team member HF usernames (if applicable)

## Step 8: Final Submission Verification

Before Nov 30 deadline, verify:

- [ ] Space deployed at `your-username-ecoagent-mcp-server.hf.space`
- [ ] MCP endpoint working at `/gradio_api/mcp/sse`
- [ ] All 13 sustainability tools discoverable by MCP clients
- [ ] README.md has `building-mcp-track-consumer` tag
- [ ] Demo video uploaded and linked in README
- [ ] Social media post published and linked in README
- [ ] All team members joined MCP-1st-Birthday organization
- [ ] Original work created during Nov 14-30 period
- [ ] Consumer-focused tools working properly
- [ ] MCP protocol compliance confirmed
- [ ] No prohibited shortcuts (all original code)

## Troubleshooting Common Issues

### MCP Endpoint Not Working
- Check that `mcp_server=True` parameter is used in launch
- Verify endpoint path is `/gradio_api/mcp/sse`

### Tools Not Discovered by MCP Clients
- Confirm JSON Schema validation is properly implemented
- Check that all required parameters are defined
- Verify tool descriptions are clear and helpful

### API Key Issues
- Ensure `GOOGLE_API_KEY` is set as Space secret, not in code
- Check that other environment variables are properly configured

## Post-Deployment Checklist

- [ ] Claude Desktop integration tested
- [ ] Cursor integration tested  
- [ ] All 13 tools working with MCP clients
- [ ] Video shows actual integration working
- [ ] Social media post includes Space link
- [ ] MCP hackathon organization joined
- [ ] Registration completed
- [ ] README tags properly set
- [ ] Everything built during Nov 14-30 timeframe

## Success Metrics

Your deployment is successful when:
- ✅ MCP clients can discover and use all 13 sustainability tools
- ✅ Video shows real integration with Claude/Cursor
- ✅ Social media post reaches the AI agent community
- ✅ Consumer sustainability tools help users make environmental decisions
- ✅ MCP protocol compliance fully implemented
- ✅ Hackathon requirements completely fulfilled

Good luck with your MCP hackathon submission! 🌱