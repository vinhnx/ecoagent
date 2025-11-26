# EcoAgent MCP Server - Quick Publication Setup

## 🚀 One-Click Deployment Instructions

### Prerequisites
- Hugging Face account: [https://huggingface.co/join](https://huggingface.co/join)
- Google API key: [https://aistudio.google.com/](https://aistudio.google.com/)
- GitHub account for version control

### Step 1: Create Hugging Face Space
1. Go to [https://huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in:
   - **Space ID**: `your-username/ecoagent-mcp-server`
   - **SDK**: **Gradio**
   - **Hardware**: **CPU Basic** (or higher if needed)
   - **Template**: **From Scratch** 
   - **Visibility**: **Public**
3. Click **Create Space**

### Step 2: Upload Files
Upload these files to your new Space:

**app.py**:
```python
from ecoagent.mcp_server import EcoAgentMCP

def main():
    """Main entry point for EcoAgent MCP Server."""
    mcp_server = EcoAgentMCP()
    return mcp_server.create_gradio_interface()

# Create the interface
demo = main()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, mcp_server=True)
```

**requirements.txt**:
```
gradio>=4.40.0
google-adk>=0.7.0
google-generativeai>=0.8.0
fastapi>=0.115.0
pydantic>=2.0.0
requests>=2.31.0
pydantic[email]>=2.0.0
click>=8.0.0
SQLAlchemy>=2.0.0
asyncpg>=0.29.0
python-multipart>=0.0.18
alembic>=1.13.0
```

### Step 3: Add Environment Variables
1. Go to your Space → Settings → Secrets
2. Add `GOOGLE_API_KEY` with your Gemini API key value

### Step 4: Verify MCP Endpoint
1. Once deployed, visit your Space URL
2. Find endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`

## 🏷️ Required README Setup

Create your `README.md` with these exact tags for hackathon:

```markdown
---
title: EcoAgent MCP Server - Consumer Sustainability
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
  - environmental-analysis
  - eco-friendly
---

# 🌱 EcoAgent MCP Server - Consumer Sustainability Tools

**MCP 1st Birthday Hackathon Submission - Building MCP Track**

## 🏷️ Category: Building MCP - Consumer

**Tag**: `building-mcp-track-consumer`

## 🎬 Demo Video
[Embed link to your demo video showing Claude/Cursor integration]

## 📱 Social Media Post  
[Link to your social media post about the project]

## 🚀 MCP Endpoint
```
https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse
```

## 🎯 Consumer-Focused Sustainability Tools (13 Tools)

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

## 🎯 Consumer Focus Features

- **Personal Carbon Tracking**: Individual transport, energy, lifestyle impact
- **Home Sustainability**: Energy efficiency and home-related recommendations
- **Lifestyle Advice**: Transport, diet, consumption guidance
- **Local Resources**: Find environmental resources by location
- **Simple Parameters**: Easy-to-use for everyday consumers

## 🧠 MCP Client Integration

### Claude Desktop Setup
1. Go to Settings → MCP Servers
2. Add endpoint: `https://your-space-url.hf.space/gradio_api/mcp/sse`
3. Claude will auto-discover all sustainability tools
4. Tools become available during conversations

### Cursor IDE Setup
1. Go to Preferences → MCP Configuration
2. Add server with endpoint
3. Tools appear in Cursor's AI assistant
4. Available for code-related environmental analysis

## 🏆 Hackathon Alignment

### Building MCP Requirements
- ✅ Functioning MCP server with 13 consumer tools
- ✅ Gradio app with MCP support
- ✅ Consumer-focused sustainability features
- ✅ Full MCP protocol compliance
- ✅ Environmental impact focus
- ✅ Tagged as building-mcp-track-consumer

## 💡 Use Cases

### Personal Carbon Footprint
Calculate and reduce individual transportation, energy, and lifestyle emissions

### Sustainable Living  
Get personalized recommendations for transportation, diet, and energy usage

### Local Environmental Action
Discover environmental resources and practices in your area

---

**EcoAgent MCP Server** - Making sustainability accessible to consumers through MCP protocol
```

## 📹 Create Demo Video (Required)

### Video Content (1-5 minutes):
1. **Intro** (15s): Project title and hackathon category
2. **Setup** (60s): Show MCP client configuration with your endpoint
3. **Demo** (120s): Use 3-4 key tools showing real value:
   - Transportation carbon calculation
   - Sustainability recommendations
   - Local resource discovery
4. **Real-world** (30s): Show practical consumer use case
5. **Outro** (15s): Impact and hackathon participation

### Video Tips:
- Record screen with MCP client integration
- Show actual tool responses
- Narrate the consumer sustainability focus
- Demonstrate real environmental impact value
- Keep under 5 minutes

## 📱 Social Media Post (Required)

### Post Content:
```
🌱 Just launched EcoAgent MCP Server for the #MCPHackathon! 

Full MCP-compliant sustainability assistant with 13 tools for consumers to calculate carbon footprints, get eco-friendly recommendations, and access environmental data through AI assistants like Claude Desktop and Cursor.

Perfect for consumers wanting to make environmentally conscious decisions through familiar AI interfaces.

Features:
✅ 13 sustainability tools (transportation, energy, diet, home)
✅ Real-time carbon calculations
✅ Personalized eco recommendations
✅ Local resource discovery
✅ MCP protocol compliant

Try it out: https://your-space.hf.space
Demo: [video_link]

#MCP #Sustainability #AI #Hackathon #BuildingMCP #ConsumerMCP #ClimateAction
```

## ✅ Pre-Submission Checklist

Before Nov 30 deadline:

**Space Configuration:**
- [ ] Space created with Gradio SDK
- [ ] Files uploaded (app.py, requirements.txt, README.md)
- [ ] Google API key added as secret
- [ ] Space running without errors

**Hackathon Requirements:**
- [ ] README has `building-mcp-track-consumer` tag
- [ ] MCP endpoint working at `/gradio_api/mcp/sse`
- [ ] All 13 consumer tools functional
- [ ] Consumer focus clearly demonstrated

**Required Content:**
- [ ] Demo video created and hosted (YouTube, etc.)
- [ ] Social media post published with Space link
- [ ] Social media link added to README
- [ ] Video embedded/link in README

**Testing:**
- [ ] Claude Desktop integration tested
- [ ] Cursor integration tested
- [ ] All tools work with MCP protocol
- [ ] Error handling works properly

**Organization:**
- [ ] Joined MCP-1st-Birthday organization
- [ ] Hackathon registration completed
- [ ] Team members (if any) registered and joined
- [ ] All code created during Nov 14-30 period

## 🚀 Quick Test After Deployment

1. Visit your Space URL: `https://your-username-ecoagent-mcp-server.hf.space`
2. Test endpoint: `https://your-username-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse`
3. Configure MCP client with your endpoint
4. Verify all 13 tools are discovered
5. Test transportation_carbon tool with sample data
6. Confirm consumer sustainability focus

## 🏆 Success Indicators

Your publication is successful when:
- ✅ MCP clients can discover and use all sustainability tools
- ✅ Video shows live integration with real MCP clients
- ✅ Social media post generates interest in sustainability
- ✅ Consumer tools help individual users with environmental decisions
- ✅ MCP protocol is fully compliant and functional  
- ✅ Hackathon submission requirements are completely met

Good luck! 🌱