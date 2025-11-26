# EcoAgent ChatGPT Apps SDK Implementation Guide

**Status**: Implementation Plan  
**Reference**: https://developers.openai.com/apps-sdk  
**MCP Foundation**: Already implemented via Gradio MCP server  
**Date**: November 26, 2025

---

## 📋 Executive Summary

EcoAgent can be transformed into a full **ChatGPT Apps SDK** application by:

1. Building a proper web UI component (currently we have Gradio)
2. Registering MCP resources for the UI
3. Implementing the `window.openai` bridge for interactive components
4. Adding structured tool metadata for ChatGPT integration

**Good News**: Our existing MCP server (`mcp_server.py`) is 80% of the way there. We need to:
- Build a React/HTML UI component
- Register it as an MCP resource
- Add proper tool metadata
- Deploy and test with ChatGPT Developer Mode

---

## 🎯 What is the Apps SDK?

### Key Concepts

**Apps SDK** = MCP + Web UI + Interactive Bridge

```
┌─────────────────────────────────────────┐
│         ChatGPT Conversation            │
└─────────────────────────────────────────┘
                    ↓
        ┌───────────────────┐
        │   Tool Call       │
        │ (via MCP)         │
        └───────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  EcoAgent Apps SDK Server               │
├─────────────────────────────────────────┤
│  MCP Resources:                         │
│  - UI Component (HTML/React)            │
│  - Tool Metadata                        │
│  - Data Structure                       │
├─────────────────────────────────────────┤
│  Web Component (Rendered in iframe)     │
│  ┌─────────────────────────────────────┐│
│  │ window.openai bridge                 ││
│  │ ├─ toolOutput (current state)        ││
│  │ ├─ callTool (invoke tool)            ││
│  │ └─ setGlobals (configuration)        ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### Three Components Needed

1. **Web Component** (UI)
   - HTML/React/Vue component
   - Rendered in ChatGPT iframe
   - Accesses `window.openai` API

2. **MCP Server** (Logic + Metadata)
   - Register UI resource
   - Define tools with metadata
   - Handle structured content

3. **Tool Metadata** (Integration)
   - `openai/outputTemplate` - which UI to show
   - `openai/toolInvocation/*` - status messages
   - `openai/widgetPrefersBorder` - styling hints

---

## 🏗️ Implementation Roadmap

### Phase 1: Architecture Assessment (Current)

**What we have**:
- ✅ MCP server (`mcp_server.py`)
- ✅ 13 sustainability tools
- ✅ Gradio interface
- ✅ Tool definitions with JSON schemas
- ✅ System prompt with KNOW/DO/SHOW framework

**What we need**:
- ⏳ Web component (HTML/React)
- ⏳ MCP resource registration
- ⏳ Tool metadata enhancement
- ⏳ `window.openai` bridge implementation

### Phase 2: Web Component Development

**Option A: Simple HTML (Recommended for MVP)**
- Single HTML file with inline CSS/JS
- Like the to-do example in quickstart
- No build step required
- Fast to iterate

**Option B: React Component**
- More complex but more scalable
- Can use Apps SDK UI library
- Better for feature-rich apps

### Phase 3: MCP Server Enhancement

Add to existing `mcp_server.py`:
```python
# Register UI resource
server.registerResource(
    "ecoagent-ui",
    "ui://widget/ecoagent.html",
    {},
    async () => {
        contents: [
            {
                uri: "ui://widget/ecoagent.html",
                mimeType: "text/html+skybridge",
                text: html_content,
                _meta: {
                    "openai/widgetPrefersBorder": true
                }
            }
        ]
    }
)
```

### Phase 4: Tool Metadata Enhancement

Update tool definitions with OpenAI metadata:
```python
tools = {
    "calculate_carbon_footprint": {
        "description": "...",
        "inputSchema": {...},
        "_meta": {
            "openai/outputTemplate": "ui://widget/ecoagent.html",
            "openai/toolInvocation/invoking": "Calculating your carbon footprint...",
            "openai/toolInvocation/invoked": "Carbon footprint calculated",
        }
    }
}
```

### Phase 5: Testing & Deployment

1. Set up ngrok tunnel for local testing
2. Enable ChatGPT Developer Mode
3. Create test connector
4. Iterate on UI/UX
5. Deploy to production

---

## 💻 Web Component Implementation

### Option A: Simple HTML Component (Recommended)

Create `public/ecoagent-widget.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>EcoAgent - Carbon Calculator</title>
    <style>
        :root {
            color: #0b0b0f;
            font-family: "Inter", system-ui, -apple-system, sans-serif;
        }
        html, body {
            width: 100%;
            min-height: 100%;
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 16px;
            background: #f6f8fb;
        }
        main {
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
            background: #fff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }
        h2 {
            margin: 0 0 16px;
            font-size: 1.25rem;
            color: #1e7e34;
        }
        .carbon-display {
            background: #f0fdf4;
            border: 1px solid #86efac;
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        }
        .carbon-value {
            font-size: 2rem;
            font-weight: bold;
            color: #16a34a;
        }
        .carbon-context {
            font-size: 0.875rem;
            color: #666;
            margin-top: 8px;
        }
        .recommendation {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px;
            margin: 12px 0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <main>
        <h2>🌱 Your Carbon Impact</h2>
        
        <div id="impact-display">
            <!-- Will be populated by JavaScript -->
        </div>
        
        <div id="recommendations">
            <!-- Will be populated by JavaScript -->
        </div>
    </main>

    <script type="module">
        // Bridge to ChatGPT
        const getToolOutput = () => window.openai?.toolOutput || {};
        const callTool = (toolName, args) => {
            if (window.openai?.callTool) {
                return window.openai.callTool(toolName, args);
            }
        };

        // Update UI when tool output changes
        const updateUI = () => {
            const output = getToolOutput();
            const displayDiv = document.getElementById('impact-display');
            const recDiv = document.getElementById('recommendations');
            
            if (output.carbon_pounds) {
                displayDiv.innerHTML = `
                    <div class="carbon-display">
                        <div class="carbon-value">${output.carbon_pounds} lbs CO₂</div>
                        <div class="carbon-context">${output.description}</div>
                        <div style="font-size: 0.8rem; margin-top: 8px; color: #888;">
                            = ${output.carbon_kg} kg CO₂
                        </div>
                    </div>
                `;
            }
            
            if (output.breakdown) {
                Object.entries(output.breakdown).forEach(([category, value]) => {
                    if (value > 0) {
                        recDiv.innerHTML += `
                            <div class="recommendation">
                                <strong>${category.charAt(0).toUpperCase() + category.slice(1)}:</strong>
                                ${value} lbs CO₂
                            </div>
                        `;
                    }
                });
            }
        };

        // Listen for updates
        window.addEventListener('openai-tool-output-updated', updateUI);
        
        // Initial render
        updateUI();
    </script>
</body>
</html>
```

### Option B: React Component

For more complex UI, use React with Apps SDK UI Library:

```typescript
// components/EcoAgentWidget.tsx
import { useEffect, useState } from 'react';

export function EcoAgentWidget() {
    const [carbonData, setCarbonData] = useState(null);
    
    useEffect(() => {
        // Listen for window.openai updates
        const updateData = () => {
            const output = window.openai?.toolOutput;
            if (output?.carbon_pounds) {
                setCarbonData(output);
            }
        };
        
        window.addEventListener('openai-tool-output-updated', updateData);
        updateData(); // Initial render
        
        return () => {
            window.removeEventListener('openai-tool-output-updated', updateData);
        };
    }, []);
    
    if (!carbonData) return <div>Loading...</div>;
    
    return (
        <div className="ecoagent-widget">
            <h2>🌱 Your Carbon Impact</h2>
            <div className="carbon-display">
                <div className="carbon-value">
                    {carbonData.carbon_pounds} lbs CO₂
                </div>
                <div className="carbon-context">
                    {carbonData.description}
                </div>
            </div>
        </div>
    );
}
```

---

## 🔧 MCP Server Enhancement

### Update `mcp_server.py` for Apps SDK

```python
from mcp.server import Server
from mcp.types import Resource

class EcoAgentAppsSDK(EcoAgentMCP):
    """Enhanced MCP server with Apps SDK support."""
    
    def __init__(self):
        super().__init__()
        self.setup_apps_sdk()
    
    def setup_apps_sdk(self):
        """Register Apps SDK resources and enhanced metadata."""
        
        # Read the web component
        with open('public/ecoagent-widget.html', 'r') as f:
            widget_html = f.read()
        
        # Register UI resource
        self.server.register_resource(
            "ecoagent-widget",
            "ui://widget/ecoagent.html",
            {},
            lambda: {
                "contents": [
                    {
                        "uri": "ui://widget/ecoagent.html",
                        "mimeType": "text/html+skybridge",
                        "text": widget_html,
                        "_meta": {
                            "openai/widgetPrefersBorder": True
                        }
                    }
                ]
            }
        )
    
    def enhance_tool_metadata(self):
        """Add Apps SDK metadata to tools."""
        
        # Calculate carbon tool
        self.tools["calculate_carbon_footprint"]["_meta"] = {
            "openai/outputTemplate": "ui://widget/ecoagent.html",
            "openai/toolInvocation/invoking": "Calculating your carbon footprint...",
            "openai/toolInvocation/invoked": "Carbon footprint calculated!",
            "openai/widgetPrefersBorder": True,
        }
        
        # Recommendations tool
        self.tools["get_sustainability_recommendations"]["_meta"] = {
            "openai/toolInvocation/invoking": "Finding recommendations...",
            "openai/toolInvocation/invoked": "Recommendations ready",
        }
```

---

## 📊 Tool Metadata Reference

### Available Metadata Fields

```python
"_meta": {
    # Which UI to show for this tool's output
    "openai/outputTemplate": "ui://widget/ecoagent.html",
    
    # Status messages while tool is executing
    "openai/toolInvocation/invoking": "Calculating...",
    "openai/toolInvocation/invoked": "Calculation complete",
    
    # UI styling hints
    "openai/widgetPrefersBorder": True,
    "openai/widgetPrefersDarkMode": False,
    
    # Structured content hints
    "openai/structuredContentSchema": {
        "type": "object",
        "properties": {
            "carbon_pounds": {"type": "number"},
            "breakdown": {"type": "object"}
        }
    }
}
```

---

## 🚀 Deployment Steps

### Step 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt
npm install  # if using React

# Start local server
python mcp_server.py

# In another terminal, expose with ngrok
ngrok http 8000
```

### Step 2: Enable ChatGPT Developer Mode

1. Go to ChatGPT Settings
2. Apps & Connectors → Advanced Settings
3. Enable Developer Mode
4. Go to Settings → Connectors → Create

### Step 3: Add Connector

```
MCP URL: https://<ngrok-url>/gradio_api/mcp/sse
Name: EcoAgent
Description: Sustainability tools for carbon tracking and eco-recommendations
```

### Step 4: Test in ChatGPT

1. Open a new chat
2. Click **More** menu
3. Select **EcoAgent**
4. Try: "Calculate my carbon footprint for a 100-mile drive"

### Step 5: Iterate

- Test various intents
- Refine UI based on ChatGPT rendering
- Update tool metadata
- Click **Refresh** in Settings → Connectors after changes

---

## 📋 Developer Guidelines Checklist

From OpenAI's app developer guidelines:

### Safety
- ✅ Comply with OpenAI usage policies
- ✅ Appropriate for all audiences
- ✅ Clear error handling
- ✅ No hidden behavior

### Privacy
- ✅ Include privacy policy
- ✅ Minimal data collection
- ✅ Clear permissions
- ✅ No sensitive data (PCI, PHI, SSN)
- ✅ No tracking/surveillance

### Quality
- ✅ Clear purpose
- ✅ Reliable behavior
- ✅ Accurate results
- ✅ Tested thoroughly
- ✅ Low latency

### Metadata
- ✅ Clear app name/description
- ✅ Accurate screenshots
- ✅ Clear tool names
- ✅ Mark read vs write actions

---

## 🎨 Design Guidelines Summary

### Best Practices for EcoAgent App

1. **Immediate Value**
   - Show carbon calculation instantly
   - Display in multiple units
   - Include context/comparison

2. **Visual Clarity**
   - Green/sustainability colors
   - Clear typography
   - Minimal clutter

3. **Interactive Elements**
   - Breakdown by category
   - Comparison widgets
   - Action recommendations

4. **Conversation Integration**
   - Keep UI compact
   - Don't overwhelm chat
   - Support both vague + specific intents

---

## 📈 Success Metrics

Once deployed to ChatGPT:

1. **Engagement**
   - % of users who click on EcoAgent
   - Average interactions per session
   - Return usage rate

2. **Functionality**
   - % successful tool calls
   - Error rates
   - Response time

3. **User Satisfaction**
   - Star ratings
   - Feedback sentiment
   - Support tickets

4. **Impact**
   - Carbon calculations performed
   - Recommendations accepted
   - Estimated CO2 reductions

---

## 🔗 Next Steps

### Immediate (This Week)
- [ ] Build simple HTML widget
- [ ] Update MCP server with resource registration
- [ ] Add tool metadata
- [ ] Test locally with ngrok

### Short Term (Next Week)
- [ ] Enable ChatGPT Developer Mode
- [ ] Create test connector
- [ ] Refine UI based on ChatGPT rendering
- [ ] Test various user intents

### Medium Term (Before Submission)
- [ ] Polish UI/UX
- [ ] Comprehensive testing
- [ ] Add advanced features (if time)
- [ ] Prepare for app directory submission

### Long Term (Post-Launch)
- [ ] Monitor metrics
- [ ] Gather user feedback
- [ ] Iterate on features
- [ ] Consider monetization

---

## 📚 Key Resources

| Resource | URL |
|----------|-----|
| **Apps SDK Docs** | https://developers.openai.com/apps-sdk |
| **Quickstart** | https://developers.openai.com/apps-sdk/quickstart |
| **Design Guidelines** | https://developers.openai.com/apps-sdk/concepts/design-guidelines |
| **Developer Guidelines** | https://developers.openai.com/apps-sdk/app-developer-guidelines |
| **Example Repo** | https://github.com/openai/openai-apps-sdk-examples |
| **MCP Inspector** | https://modelcontextprotocol.io/docs/tools/inspector |
| **ngrok** | https://ngrok.com |

---

## 💡 Key Insights

### From OpenAI's Apps SDK

1. **Apps are not minis of your product** - They're focused toolkits
2. **Web component + MCP** - That's all you need
3. **window.openai bridge** - Connects UI to ChatGPT
4. **Metadata matters** - Guides ChatGPT's behavior
5. **Ecosystem-first** - Apps work with other ChatGPT tools

### For EcoAgent

- We have the tools (13 of them)
- We have the MCP server (Gradio)
- We need the Web UI component
- We need to enhance metadata
- We're ready to go live!

---

## 🎯 Success Criteria

✅ **MVP Ready When**:
- Web component renders in ChatGPT
- Tools execute correctly
- Data displays clearly
- No errors or crashes

✅ **Production Ready When**:
- All 4 criteria above met
- Thoroughly tested
- UI polished
- Documentation complete

✅ **App Directory Ready When**:
- Meets developer guidelines
- High design quality
- Performance optimized
- Ready for mass users

---

**Status**: Ready to implement  
**Effort**: ~40-60 hours for full Apps SDK integration  
**Timeline**: 2-3 weeks for MVP, 4-5 weeks for full implementation  
**Team**: 1 developer (you can do this!)

Let's build! 🚀

