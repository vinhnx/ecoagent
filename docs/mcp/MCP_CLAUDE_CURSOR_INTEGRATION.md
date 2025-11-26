# MCP Claude/Cursor Integration Guide

Complete setup guide for connecting EcoAgent MCP Server to Claude Desktop and Cursor.

---

## Prerequisites

- EcoAgent MCP Server running: `python3 mcp_server.py`
- Claude Desktop or Cursor installed
- For remote access: `ngrok` installed and available

---

## Quick Start (Local Development)

### 1. Start the Server

```bash
cd /path/to/ecoagent
python3 mcp_server.py
```

**Expected output:**
```
🌱 Starting EcoAgent MCP Server...
MCP endpoint will be available at: http://localhost:8000/gradio_api/mcp/sse
Optimized for Claude Desktop, Cursor, and other MCP-compatible clients.

📋 Available tools:
   1. calculate_transportation_carbon: Calculate carbon emissions...
   2. calculate_flight_carbon: Calculate carbon emissions from air travel...
   ...
```

### 2. Verify Server is Running

```bash
curl http://localhost:8000
# Should return HTML (Gradio interface)
```

---

## Claude Desktop Setup

### Step 1: Locate Claude Configuration File

**macOS/Linux:**
```bash
cat ~/.claude_desktop/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Step 2: Edit Configuration

Add or update the `mcpServers` section:

```json
{
  "mcpServers": {
    "ecoagent": {
      "command": "python3",
      "args": ["-m", "mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/ecoagent"
      }
    }
  }
}
```

**Or for SSE endpoint (recommended for running server):**

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "http://localhost:8000/gradio_api/mcp/sse"
    }
  }
}
```

### Step 3: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. In a conversation, click the **"+" button** (or **Tools** menu)
4. You should see **EcoAgent** tools listed

### Step 4: Test Integration

In Claude, try:

```
Calculate the carbon footprint for a 100-mile drive in a car that gets 25 MPG.
```

Claude should:
- Recognize the request requires the carbon calculator
- Call `calculate_transportation_carbon` with your parameters
- Display the result with environmental context

---

## Cursor Setup

### Step 1: Locate Cursor Configuration

**macOS:**
```bash
cat ~/.cursor/cursorrc
# or
cat ~/.cursor/settings.json
```

**Linux:**
```bash
cat ~/.config/Cursor/cursorrc
```

**Windows:**
```
%APPDATA%\Cursor\cursorrc
```

### Step 2: Add MCP Server Configuration

Edit the config file to include:

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "http://localhost:8000/gradio_api/mcp/sse"
    }
  }
}
```

Or if starting the server directly:

```json
{
  "mcpServers": {
    "ecoagent": {
      "command": "python3",
      "args": ["/path/to/ecoagent/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/ecoagent"
      }
    }
  }
}
```

### Step 3: Restart Cursor

1. Close all Cursor windows
2. Reopen Cursor
3. Open a new conversation
4. Click **Tools** in the chat interface
5. EcoAgent tools should appear

### Step 4: Test Integration

In Cursor's chat, try:

```
What's the carbon emissions for a 2000-mile flight in business class?
```

---

## Remote Access (Production)

### Step 1: Install ngrok

**macOS:**
```bash
brew install ngrok
```

**Or download:** https://ngrok.com/download

### Step 2: Expose Server with ngrok

In a **new terminal** (keep your server running):

```bash
ngrok http 8000
```

**Output:**
```
Forwarding    https://abc123def456.ngrok.io -> http://localhost:8000
```

Copy the HTTPS URL.

### Step 3: Update Claude/Cursor Configuration

Replace `localhost:8000` with your ngrok URL:

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "https://abc123def456.ngrok.io/gradio_api/mcp/sse"
    }
  }
}
```

### Step 4: Restart Claude/Cursor

The tools should now be available.

---

## MCP Endpoint Details

### Endpoint URL
```
http://localhost:8000/gradio_api/mcp/sse
```

### Protocol
- **Type:** Server-Sent Events (SSE)
- **Method:** Follows Model Context Protocol (MCP) specification
- **Format:** JSON-RPC over SSE

### Available Tools

12 sustainability tools organized by category:

#### Carbon Calculators
- `calculate_transportation_carbon` - Vehicle emissions
- `calculate_flight_carbon` - Air travel emissions
- `calculate_home_energy_carbon` - Home energy emissions
- `calculate_total_carbon` - Combined footprint

#### Unit Conversion
- `convert_units_with_context` - Sustainability units

#### Recommendations
- `suggest_transportation_alternatives` - Eco-friendly transport
- `suggest_energy_efficiency_improvements` - Home efficiency
- `suggest_dietary_changes` - Sustainable diet

#### Information
- `search_environmental_info` - General environmental search
- `get_local_environmental_resources` - Local sustainability resources
- `get_latest_environmental_news` - Environmental news
- `get_sustainability_practice_info` - Sustainability practices

---

## Testing Tools

### Test in Claude/Cursor Interface

```
Carbon Calculations:
- "Calculate carbon for 500 miles in a car with 30 MPG"
- "How much CO2 for a 2000-mile flight in business class?"
- "I used 1000 kWh last month with 20% solar. What's my carbon?"

Recommendations:
- "Give me sustainable alternatives for a 10-mile commute"
- "Suggest energy efficiency improvements for my apartment"
- "What dietary changes reduce carbon footprint most?"

Information:
- "Search for renewable energy benefits"
- "Find recycling centers near San Francisco"
- "Latest news on climate change"
- "Tell me about composting"
```

### Expected Behavior

When you ask a question that requires a tool:

1. Claude/Cursor recognizes the request
2. Calls the appropriate MCP tool automatically
3. Shows the result with formatting
4. Provides additional context and recommendations

---

## Troubleshooting

### "Tools not showing in Claude/Cursor"

**Check 1: Server running?**
```bash
lsof -i :8000
# Should show Python process
```

**Check 2: Config file syntax?**
```bash
# Validate JSON
python3 -m json.tool ~/.claude_desktop/claude_desktop_config.json
```

**Check 3: Endpoint accessible?**
```bash
curl http://localhost:8000/gradio_api/mcp/sse
# Should connect (SSE stream)
```

**Check 4: Restart required?**
```bash
# Restart Claude/Cursor completely
# (Not just the chat window)
```

### "Connection refused" or "Cannot connect"

**For localhost (127.0.0.1):**
- Ensure server is running: `python3 mcp_server.py`
- Check port 8000 is not in use: `lsof -i :8000`

**For remote (ngrok):**
- Ensure ngrok is running: `ngrok http 8000`
- Update config with new ngrok URL (URLs expire)
- Check firewall allows outbound HTTPS

### "Tool call fails with validation error"

**Example error:**
```json
{
  "error": "validation error for CallToolRequest"
}
```

**Solutions:**
1. Check parameter types match tool schema
2. Ensure required parameters are provided
3. Check value ranges (e.g., MPG > 0)
4. Review server logs: `tail -f /tmp/server.log`

### "Server crashes or shows errors"

**Check logs:**
```bash
cat /tmp/server.log | tail -50
```

**Common issues:**
- Missing dependencies: `pip3 install -r requirements.txt`
- Wrong Python version: `python3 --version` (need 3.9+)
- Port already in use: `kill $(lsof -t -i :8000)`

---

## Configuration Examples

### Claude Desktop (macOS)

File: `~/.claude_desktop/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "http://localhost:8000/gradio_api/mcp/sse"
    }
  }
}
```

### Cursor (macOS)

File: `~/.cursor/settings.json`

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "http://localhost:8000/gradio_api/mcp/sse"
    }
  }
}
```

### With ngrok (All Platforms)

```json
{
  "mcpServers": {
    "ecoagent": {
      "url": "https://your-ngrok-url.ngrok.io/gradio_api/mcp/sse"
    }
  }
}
```

---

## Advanced Setup

### Environment Variables

When starting the server, you can configure:

```bash
# Custom port
PORT=9000 python3 mcp_server.py

# Custom host (for remote access)
HOST=0.0.0.0 python3 mcp_server.py

# With API key (if using grounded search)
GOOGLE_API_KEY=your-key python3 mcp_server.py
```

### Running in Background

**macOS/Linux:**
```bash
nohup python3 mcp_server.py > /tmp/ecoagent.log 2>&1 &
echo $!  # Save the PID
```

**Stop later:**
```bash
kill <PID>
```

### Docker (Future)

```bash
docker run -p 8000:8000 ecoagent:latest
```

---

## Performance Tuning

### Response Time

Tools typically respond in < 2 seconds locally.

**If slow:**
1. Check CPU usage: `top`
2. Check network latency: `ping localhost`
3. Check server logs for errors

### Concurrent Requests

The server handles multiple tool calls simultaneously.

**If hitting limits:**
- Upgrade host machine
- Run server on more powerful system
- Consider containerization (Docker)

---

## Security Considerations

### Local Development
- Using `localhost` is safe for local development
- No authentication required for local connections

### Production (Remote Access)
- Use HTTPS (ngrok provides this automatically)
- Consider adding authentication layer
- Run on secure, dedicated server
- Monitor and log all tool calls

### API Keys
- Never commit API keys to git
- Use environment variables for sensitive config
- Use `.env` files (in `.gitignore`)

---

## Next Steps

1. ✅ Start server: `python3 mcp_server.py`
2. ✅ Configure Claude/Cursor
3. ✅ Test with example queries
4. ✅ Deploy to production if needed

---

## Help & Support

- **Server Issues:** Check `/tmp/server.log`
- **Config Issues:** Validate JSON syntax
- **Tool Issues:** Review tool schema in Gradio UI
- **MCP Protocol:** See [Model Context Protocol Docs](https://modelcontextprotocol.io/)

---

**Status:** ✅ Ready to integrate

MCP endpoint is available and tools are discoverable by Claude/Cursor clients.
