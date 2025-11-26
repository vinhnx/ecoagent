# EcoAgent Hackathon Submission Checklist

**Deadline**: November 30, 2025, 11:59 PM UTC

---

## Pre-Submission (Nov 14-16)

- [ ] Register for hackathon at https://huggingface.co/spaces/MCP-1st-Birthday/gradio-hackathon-registration-winter25
- [ ] Join HF organization: `MCP-1st-Birthday`
- [ ] Join Discord: https://discord.gg/fveShqytyh
- [ ] Read judging criteria carefully
- [ ] Verify all tools work locally

---

## Space Setup (Nov 17-19)

### Create Space
- [ ] Go to https://huggingface.co/new-space
- [ ] **Name**: `ecoagent` (or similar)
- [ ] **License**: Apache 2.0 (or MIT)
- [ ] **SDK**: Docker (or Gradio)
- [ ] **Organization**: `MCP-1st-Birthday`
- [ ] **Private**: No (public submission required)

### Push Code to Space
```bash
git clone https://huggingface.co/spaces/MCP-1st-Birthday/ecoagent
cd ecoagent
cp -r ../../../ecoagent/* .
git add .
git commit -m "Initial EcoAgent MCP server submission"
git push
```

### Verify Deployment
- [ ] Space shows "Running" status
- [ ] Gradio interface loads at space URL
- [ ] MCP endpoint accessible: `https://[space-name].hf.space/gradio_api/mcp/sse`
- [ ] View API link shows MCP schema

---

## Code & Documentation (Nov 19-21)

### Space README Requirements
- [ ] Track tag in README: `` `building-mcp-track-consumer` ``
- [ ] Clear project description
- [ ] Feature list with all 13 tools
- [ ] Installation instructions (if applicable)
- [ ] MCP server details:
  - [ ] Endpoint URL format
  - [ ] How to integrate with Claude Desktop/Cursor
  - [ ] Example configuration
- [ ] Tool descriptions and capabilities
- [ ] Links to demo video (add after recording)
- [ ] Link to social media post (add after posting)

### Code Quality
- [ ] No console errors when launching
- [ ] All 13 tools respond correctly
- [ ] Error messages are clear
- [ ] Tool descriptions are consumer-friendly

---

## Demo Video (Nov 22-24)

### Recording Checklist
- [ ] Camera/screen capture working
- [ ] Audio clear (speak slowly, enunciate)
- [ ] Screen resolution at least 1080p
- [ ] Duration: 1-5 minutes (aim for 1.5-2 min)
- [ ] Include:
  - [ ] Space/interface overview
  - [ ] MCP endpoint explanation
  - [ ] At least 2 tool executions
  - [ ] MCP client integration (Claude Desktop or Cursor)
  - [ ] Clear use case explanation

### Video Upload
- [ ] Upload to YouTube (unlisted or public), Vimeo, or similar
- [ ] Title includes "EcoAgent" and "MCP"
- [ ] Description includes project info
- [ ] Get shareable link (non-YouTube may need to be embedded)
- [ ] Link in Space README under "Demo Video" or similar

---

## Social Media Post (Nov 24-25)

### Create Post (X/Twitter or LinkedIn)
Required content:
- [ ] Mention hackathon: "MCP's 1st Birthday Hackathon"
- [ ] Highlight what you built: "EcoAgent consumer MCP server"
- [ ] Key features: "13 sustainability tools for AI agents"
- [ ] Link to Space
- [ ] Hashtags: #MCPHackathon #Gradio #Sustainability #MCP #EcoAgent
- [ ] Professional tone, eye-catching

### Example Post:
```
🌱 Excited to submit EcoAgent to the MCP's 1st Birthday Hackathon!

Building a consumer MCP server with 13 sustainability tools:
• Carbon footprint calculations
• Eco-friendly recommendations  
• Real-time environmental data

Now AI agents (Claude, Cursor) can help users make sustainable choices. 🌍

Check it out: [Space URL]

#MCPHackathon #Gradio #Sustainability #MCP
```

### Get Link
- [ ] Get permalink to your post
- [ ] Copy URL
- [ ] Add to Space README

---

## Final README (Nov 26-27)

### Metadata at Top of README
```markdown
---
title: EcoAgent - Consumer MCP Server
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker  # or gradio
sdk_version: 4.0
app_file: mcp_server.py  # or appropriate entry point
models: []
datasets: []
license: apache-2.0
tags:
  - mcp
  - sustainability
  - gradio
  - carbon-calculator
  - building-mcp-track-consumer
---
```

### Content Sections
- [ ] **Title & Description** (1-2 sentences about what it does)
- [ ] **Track Info**
  ```markdown
  🏷️ **Track**: Building MCP (Track 1)  
  📂 **Category**: Consumer MCP Servers  
  🎯 **Tag**: `building-mcp-track-consumer`
  ```
- [ ] **Key Features** (bullet list of 13 tools or main features)
- [ ] **How It Works** (MCP server, tools available, etc.)
- [ ] **Getting Started** (how to use locally or on Space)
- [ ] **MCP Integration Guide** (how to add to Claude Desktop/Cursor)
- [ ] **Demo Video** (embedded or linked)
- [ ] **Social Media** (link to post)
- [ ] **Use Cases** (why this matters)
- [ ] **Installation** (if applicable)
- [ ] **Team** (your name/team)

### Example Section Template:
```markdown
## 🚀 MCP Integration

**Endpoint**: `https://[space-name].hf.space/gradio_api/mcp/sse`

### Using with Claude Desktop

1. Open `claude_desktop_config.json`
2. Add this configuration:
```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "https://[space-name].hf.space/gradio_api/mcp/sse"
    }
  }
}
```
3. Restart Claude Desktop
4. EcoAgent tools appear in tool use
```

---

## Final Submission (Nov 28-30)

### Quality Assurance
- [ ] **Reload Space** - Verify it still works after pushing changes
- [ ] **Test MCP Endpoint** - Try from external MCP client or API test tool
- [ ] **Check Links** - Video, social media post, etc. all clickable
- [ ] **Proofread README** - No typos, formatting correct
- [ ] **Verify Metadata** - Track tag visible and correct

### Before Final Submission
- [ ] All files pushed to HF Space repo
- [ ] README finalized with all required sections
- [ ] Demo video linked and accessible
- [ ] Social media post link included
- [ ] Space is public
- [ ] MCP endpoint tested and working

### Submit by Deadline
- [ ] Mark submission complete (check hackathon site for submission form)
- [ ] Verify submission received
- [ ] Note: **Deadline is Nov 30, 11:59 PM UTC**

---

## Post-Submission (Nov 30+)

- [ ] Share submission with friends/colleagues
- [ ] Engage with Discord community
- [ ] Comment on other projects
- [ ] Help others with MCP questions
- [ ] Wait for judging results (winners announced Dec 15)

---

## Important Links

| Resource | URL |
|----------|-----|
| Hackathon | https://huggingface.co/MCP-1st-Birthday |
| Registration | https://huggingface.co/spaces/MCP-1st-Birthday/gradio-hackathon-registration-winter25 |
| Discord | https://discord.gg/fveShqytyh |
| Gradio MCP Docs | https://www.gradio.app/guides/building-mcp-server-with-gradio |
| MCP Spec | https://modelcontextprotocol.io/ |
| HF Spaces Docs | https://huggingface.co/docs/hub/spaces-overview |

---

## Notes

- **Organization**: Must be in `MCP-1st-Birthday` org to be eligible
- **Original Work**: All work must be created/modified during Nov 14-30
- **Public Submission**: Space must be public
- **Completeness**: Video, README, social link required for judging
- **Language**: English for best chance of winning

---

## Questions?

- Check Discord: https://discord.gg/fveShqytyh
- Read FAQ: https://huggingface.co/MCP-1st-Birthday#faqs
- DM maintainers or post in #agents-mcp-hackathon-winter25

---

✅ **Ready to submit?** Follow this checklist top to bottom!
